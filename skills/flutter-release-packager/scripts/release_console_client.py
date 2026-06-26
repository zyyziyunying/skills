#!/usr/bin/env python3
"""Contract-driven client for project-owned Flutter release consoles."""

from __future__ import annotations

import argparse
import json
import os
import re
import selectors
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT_PATH = "tool/release_console/agent-contract.json"
REDACTION_MARKER = "<redacted>"
SUPPORTED_SCHEMA_VERSION = 1
DIRTY_POLICIES = {"block", "block-store-release", "warn", "allow"}
UPLOAD_TRIGGER_FALLBACK = ("uploadAfterBuild", "iosUploadAfterBuild", "upload")


def parse_bool(value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise argparse.ArgumentTypeError("expected true or false")


def coerce_option_value(value: str) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def load_contract(project: Path, contract_path: str) -> dict[str, Any]:
    path = Path(contract_path).expanduser()
    if not path.is_absolute():
        path = project / path
    if not path.is_file():
        raise SystemExit(f"release agent contract not found: {path}")
    with path.open(encoding="utf-8") as handle:
        contract = json.load(handle)
    if not isinstance(contract, dict):
        raise SystemExit("release agent contract must be a JSON object")
    validate_contract(contract)
    return contract


def require_string_list(
    value: Any,
    field_name: str,
    *,
    required: bool = False,
) -> list[str]:
    if value is None:
        if required:
            raise SystemExit(f"{field_name} must be a string array")
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SystemExit(f"{field_name} must be a string array")
    return [str(item) for item in value]


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("schemaVersion") != SUPPORTED_SCHEMA_VERSION:
        raise SystemExit(
            f"release agent contract schemaVersion must be {SUPPORTED_SCHEMA_VERSION}"
        )
    policy = contract.get("dirtyWorktreePolicy")
    if policy not in DIRTY_POLICIES:
        raise SystemExit(
            "dirtyWorktreePolicy must be one of: "
            + ", ".join(sorted(DIRTY_POLICIES))
        )
    targets = contract.get("targets")
    if not isinstance(targets, list) or not targets:
        raise SystemExit("contract targets must be a non-empty list")
    seen: set[str] = set()
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            raise SystemExit(f"contract target at index {index} must be an object")
        target_id = target.get("id")
        if not isinstance(target_id, str) or not target_id:
            raise SystemExit(f"contract target at index {index} must define id")
        if target_id in seen:
            raise SystemExit(f"duplicate target id in contract: {target_id}")
        seen.add(target_id)
        if not isinstance(target.get("storeLike"), bool):
            raise SystemExit(f"target {target_id} must define boolean storeLike")
        allowed_option_names(target)
        require_string_list(target.get("forbiddenOptions"), f"target {target_id}.forbiddenOptions")
        validate_upload_schema(target)
        validate_evidence_schema(target)


def target_by_id(contract: dict[str, Any], target_id: str) -> dict[str, Any]:
    targets = contract.get("targets", [])
    if not isinstance(targets, list):
        raise SystemExit("contract targets must be a list")
    for target in targets:
        if isinstance(target, dict) and target.get("id") == target_id:
            return target
    raise SystemExit(f"unknown target in contract: {target_id}")


def git_status_short(project: Path, *, fail_closed: bool = False) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if fail_closed:
            detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
            raise SystemExit(f"unable to inspect git status before build: {detail}")
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def secret_redaction_config(contract: dict[str, Any]) -> dict[str, Any]:
    secret_config = contract.get("secretRedaction", {})
    return secret_config if isinstance(secret_config, dict) else {}


def redaction_key_names(contract: dict[str, Any]) -> set[str]:
    return {
        str(item).lower()
        for item in require_string_list(
            secret_redaction_config(contract).get("keyNames"),
            "secretRedaction.keyNames",
        )
    }


def redact_data(value: Any, contract: dict[str, Any], key_name: str | None = None) -> Any:
    if key_name is not None and key_name.lower() in redaction_key_names(contract):
        return REDACTION_MARKER
    if isinstance(value, dict):
        return {
            str(key): redact_data(item, contract, str(key))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_data(item, contract) for item in value]
    if isinstance(value, str):
        return redact(value, contract)
    return value


def redact(value: str, contract: dict[str, Any]) -> str:
    redacted = value
    secret_config = secret_redaction_config(contract)
    prefixes = []
    key_names = []
    patterns = []
    prefixes = require_string_list(
        secret_config.get("environmentPrefixes"),
        "secretRedaction.environmentPrefixes",
    )
    key_names = require_string_list(secret_config.get("keyNames"), "secretRedaction.keyNames")
    patterns = require_string_list(secret_config.get("patterns"), "secretRedaction.patterns")

    for prefix in prefixes:
        redacted = re.sub(
            rf"({re.escape(prefix)}[A-Za-z0-9_]*=)[^\s]+",
            r"\1<redacted>",
            redacted,
        )
    for key in key_names:
        quoted = re.escape(key)
        redacted = re.sub(
            rf'("{quoted}"\s*:\s*")[^"]*(")',
            rf"\1{REDACTION_MARKER}\2",
            redacted,
            flags=re.IGNORECASE,
        )
        redacted = re.sub(
            rf"(\b{quoted}\b\s*[=:]\s*)(\"[^\"]*\"|'[^']*'|[^\s,;]+)",
            rf"\1{REDACTION_MARKER}",
            redacted,
            flags=re.IGNORECASE,
        )
    for pattern in patterns:
        try:
            redacted = re.sub(pattern, REDACTION_MARKER, redacted)
        except re.error as error:
            raise SystemExit(f"invalid secret redaction pattern {pattern!r}: {error}") from error
    redacted = re.sub(r"([?&]token=)[^&\s]+", rf"\1{REDACTION_MARKER}", redacted)
    redacted = re.sub(r"(token=)[^&\s]+", rf"\1{REDACTION_MARKER}", redacted)
    return redacted


def sanitized_environment(contract: dict[str, Any]) -> dict[str, str]:
    env = dict(os.environ)
    prefixes = [str(item) for item in contract.get("stripEnvironmentPrefixes", [])]
    secret_config = contract.get("secretRedaction", {})
    if isinstance(secret_config, dict):
        prefixes.extend(str(item) for item in secret_config.get("stripPrefixes", []))
    for key in list(env):
        if any(key.startswith(prefix) for prefix in prefixes):
            env.pop(key, None)
    return env


def validate_required_files(project: Path, target: dict[str, Any]) -> None:
    missing: list[str] = []
    for key in ("requiredFiles", "requiredEnvFiles"):
        values = target.get(key, [])
        if not isinstance(values, list):
            continue
        for value in values:
            rel = str(value)
            if not (project / rel).exists():
                missing.append(rel)
    if missing:
        joined = "\n  ".join(missing)
        raise SystemExit(f"missing required release inputs:\n  {joined}")


def parse_options(items: list[str]) -> dict[str, Any]:
    options: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"--option must use key=value: {item}")
        key, raw_value = item.split("=", 1)
        if not key:
            raise SystemExit(f"--option key is empty: {item}")
        if key in options:
            raise SystemExit(f"duplicate --option is not allowed: {key}")
        options[key] = coerce_option_value(raw_value)
    return options


def allowed_option_names(target: dict[str, Any]) -> set[str]:
    target_id = str(target.get("id", "<unknown>"))
    option_schemas = target.get("options")
    allowed_options = target.get("allowedOptions")
    if option_schemas is not None:
        if not isinstance(option_schemas, list):
            raise SystemExit(f"target {target_id}.options must be an array")
        names: set[str] = set()
        for index, item in enumerate(option_schemas):
            if not isinstance(item, dict):
                raise SystemExit(f"target {target_id}.options[{index}] must be an object")
            name = item.get("name")
            if not isinstance(name, str) or not name:
                raise SystemExit(f"target {target_id}.options[{index}].name is required")
            if name in names:
                raise SystemExit(f"duplicate option schema for target {target_id}: {name}")
            option_type = item.get("type", "string")
            if option_type not in {"boolean", "string", "path"}:
                raise SystemExit(
                    f"target {target_id}.options[{index}].type is unsupported: {option_type}"
                )
            if "allowedValues" in item:
                require_string_list(
                    item.get("allowedValues"),
                    f"target {target_id}.options[{index}].allowedValues",
                )
            names.add(name)
        if allowed_options is not None:
            allowed_set = set(
                require_string_list(allowed_options, f"target {target_id}.allowedOptions")
            )
            if allowed_set != names:
                raise SystemExit(
                    f"target {target_id}.allowedOptions must match target options schema"
                )
        return names
    return set(require_string_list(allowed_options, f"target {target_id}.allowedOptions"))


def option_schema_by_name(target: dict[str, Any]) -> dict[str, dict[str, Any]]:
    schemas = target.get("options")
    if not isinstance(schemas, list):
        return {}
    return {
        str(item["name"]): item
        for item in schemas
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }


def validate_options(target: dict[str, Any], options: dict[str, Any]) -> None:
    allowed_set = allowed_option_names(target)
    forbidden_set = set(
        require_string_list(
            target.get("forbiddenOptions"),
            f"target {target.get('id', '<unknown>')}.forbiddenOptions",
        )
    )
    schemas = option_schema_by_name(target)
    for key in options:
        if key in forbidden_set:
            raise SystemExit(f"option is forbidden by contract for this target: {key}")
        if key not in allowed_set:
            raise SystemExit(f"option is not allowed by contract for this target: {key}")
        schema = schemas.get(key)
        if schema is not None:
            validate_option_value(key, options[key], schema)


def validate_option_value(key: str, value: Any, schema: dict[str, Any]) -> None:
    option_type = schema.get("type", "string")
    if option_type == "boolean" and not isinstance(value, bool):
        raise SystemExit(f"option {key} must be true or false")
    if option_type in {"string", "path"} and not isinstance(value, str):
        raise SystemExit(f"option {key} must be a string")
    allowed_values = schema.get("allowedValues")
    if allowed_values is not None:
        values = require_string_list(allowed_values, f"option {key}.allowedValues")
        if str(value) not in values:
            raise SystemExit(f"option {key} must be one of: {', '.join(values)}")
    if "forcedValue" in schema and value != schema.get("forcedValue"):
        raise SystemExit(f"option {key} is fixed by the contract and cannot be overridden")


def effective_option_value(target: dict[str, Any], payload: dict[str, Any], key: str) -> Any:
    if key in payload:
        return payload[key]
    schema = option_schema_by_name(target).get(key)
    if schema is None:
        return None
    if "forcedValue" in schema:
        return schema.get("forcedValue")
    return schema.get("default")


def validate_evidence_schema(target: dict[str, Any]) -> None:
    evidence = target.get("evidence", {})
    if evidence is None:
        return
    if not isinstance(evidence, dict):
        raise SystemExit(f"target {target.get('id', '<unknown>')}.evidence must be an object")
    for key, value in evidence.items():
        if key.endswith("Labels"):
            require_string_list(value, f"target {target.get('id', '<unknown>')}.evidence.{key}")


def validate_upload_schema(target: dict[str, Any]) -> None:
    target_id = str(target.get("id", "<unknown>"))
    upload = target.get("upload", {"supported": False})
    if not isinstance(upload, dict):
        raise SystemExit(f"target {target_id}.upload must be an object")
    supported = upload.get("supported", False)
    if not isinstance(supported, bool):
        raise SystemExit(f"target {target_id}.upload.supported must be boolean")
    if "requiresSeparateConfirmation" in upload and not isinstance(
        upload.get("requiresSeparateConfirmation"),
        bool,
    ):
        raise SystemExit(
            f"target {target_id}.upload.requiresSeparateConfirmation must be boolean"
        )
    if not supported:
        return
    required = upload.get("required", False)
    default_upload = upload.get("default", False)
    if not isinstance(required, bool) or not isinstance(default_upload, bool):
        raise SystemExit(f"target {target_id}.upload required/default must be boolean")
    trigger_options = require_string_list(
        upload.get("triggerOptions"),
        f"target {target_id}.upload.triggerOptions",
    )
    wait_options = require_string_list(
        upload.get("waitOptions"),
        f"target {target_id}.upload.waitOptions",
    )
    if not required and not default_upload and not trigger_options:
        raise SystemExit(
            f"target {target_id}.upload.triggerOptions is required for optional uploads"
        )
    known_options = allowed_option_names(target)
    unknown_upload_options = [
        item for item in trigger_options + wait_options if item not in known_options
    ]
    if unknown_upload_options:
        raise SystemExit(
            f"target {target_id}.upload references unknown options: "
            + ", ".join(unknown_upload_options)
        )


class ReleaseConsole:
    def __init__(self, project: Path, contract: dict[str, Any]) -> None:
        self.project = project
        self.contract = contract
        self.proc: subprocess.Popen[str] | None = None
        self.base_url = ""
        self.token_key = ""
        self.token = ""

    @property
    def config(self) -> dict[str, Any]:
        value = self.contract.get("releaseConsole")
        if not isinstance(value, dict):
            raise SystemExit("contract must define releaseConsole")
        return value

    def start(self, quiet: bool = False) -> None:
        command = self.config.get("startCommand")
        if not isinstance(command, list) or not command:
            raise SystemExit("releaseConsole.startCommand must be a non-empty array")
        cmd = [str(item) for item in command]
        pattern = str(self.config.get("startupUrlPattern", r"Release console:\s+(\S+)"))
        auth = self.config.get("auth", {})
        if isinstance(auth, dict):
            self.token_key = str(auth.get("tokenQueryParameter", ""))

        self.proc = subprocess.Popen(
            cmd,
            cwd=self.project,
            env=sanitized_environment(self.contract),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        assert self.proc.stdout is not None
        selector = selectors.DefaultSelector()
        selector.register(self.proc.stdout, selectors.EVENT_READ)
        deadline = time.time() + float(self.config.get("startupTimeoutSeconds", 30))
        url_pattern = re.compile(pattern)

        while time.time() < deadline:
            if self.proc.poll() is not None:
                remaining = self.proc.stdout.read() or ""
                raise SystemExit(
                    "release console exited before startup:\n"
                    + redact(remaining.strip(), self.contract)
                )
            for key, _ in selector.select(timeout=0.2):
                line = key.fileobj.readline()
                if not line:
                    continue
                if not quiet:
                    print(redact(line.rstrip(), self.contract))
                match = url_pattern.search(line)
                if match:
                    parsed = urllib.parse.urlparse(match.group(1))
                    self.base_url = f"{parsed.scheme}://{parsed.netloc}"
                    if self.token_key:
                        query = urllib.parse.parse_qs(parsed.query)
                        self.token = query.get(self.token_key, [""])[0]
                        if not self.token:
                            raise SystemExit("release console URL did not include token")
                    return
        raise SystemExit("timed out waiting for release console startup")

    def close(self) -> None:
        if self.proc is None or self.proc.poll() is not None:
            return
        self._signal(signal.SIGTERM)
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._signal(signal.SIGKILL)
            self.proc.wait(timeout=5)

    def _signal(self, sig: signal.Signals) -> None:
        assert self.proc is not None
        try:
            if hasattr(os, "killpg"):
                os.killpg(self.proc.pid, sig)
            else:
                self.proc.send_signal(sig)
        except ProcessLookupError:
            return

    def endpoint(self, key: str, **values: str) -> str:
        endpoint = self.config.get(key)
        if not isinstance(endpoint, str) or not endpoint:
            raise SystemExit(f"releaseConsole.{key} must be configured")
        for name, value in values.items():
            endpoint = endpoint.replace("{" + name + "}", urllib.parse.quote(value))
        return endpoint

    def request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        query = ""
        if self.token_key:
            query = f"{self.token_key}={urllib.parse.quote(self.token)}"
        separator = "&" if "?" in path else "?"
        url = f"{self.base_url}{path}{separator}{query}" if query else f"{self.base_url}{path}"
        data = None
        headers: dict[str, str] = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise SystemExit(
                f"HTTP {error.code} from release console: {redact(body, self.contract)}"
            )


def print_status(status: dict[str, Any], project: Path, contract: dict[str, Any]) -> None:
    print("Project:", redact(str(status.get("projectRoot", project)), contract))
    print("Branch:", redact(str(status.get("branch", "-")), contract))
    print("Commit:", redact(str(status.get("commit", "-")), contract))
    print("Version:", redact(str(status.get("pubspecVersion", "-")), contract))
    dirty_files = git_status_short(project)
    print("Dirty count:", len(dirty_files) if dirty_files else status.get("dirtyCount", 0))
    if dirty_files:
        print("Dirty files:")
        for line in dirty_files:
            print(f"  {redact(line, contract)}")
    checks = status.get("checks", [])
    if isinstance(checks, list):
        print("Checks:")
        for item in checks:
            if not isinstance(item, dict):
                continue
            label = "OK" if item.get("exists") is True else "MISSING"
            print(f"  {label} {redact(str(item.get('path', '-')), contract)}")
    targets = status.get("targets", [])
    if isinstance(targets, list):
        print("Targets:")
        for item in targets:
            if isinstance(item, dict):
                print(
                    f"  {redact(str(item.get('id')), contract)}: "
                    f"{redact(str(item.get('label')), contract)}"
                )


def run_status(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    contract = load_contract(project, args.contract)
    console = ReleaseConsole(project, contract)
    try:
        console.start(quiet=args.json)
        status = console.request_json("GET", console.endpoint("statusEndpoint"))
        if args.json:
            print(json.dumps(redact_data(status, contract), indent=2, sort_keys=True))
        else:
            print_status(status, project, contract)
        return 0
    finally:
        console.close()


def upload_related_option_names(target: dict[str, Any]) -> set[str]:
    upload = target.get("upload", {})
    names = set(UPLOAD_TRIGGER_FALLBACK)
    names.update(
        item
        for item in allowed_option_names(target)
        if "upload" in item.lower()
    )
    if isinstance(upload, dict):
        names.update(
            require_string_list(
                upload.get("triggerOptions"),
                f"target {target.get('id', '<unknown>')}.upload.triggerOptions",
            )
        )
        names.update(
            require_string_list(
                upload.get("waitOptions"),
                f"target {target.get('id', '<unknown>')}.upload.waitOptions",
            )
        )
    return names


def upload_condition_allows(target: dict[str, Any], payload: dict[str, Any]) -> bool:
    upload = target.get("upload", {})
    if not isinstance(upload, dict):
        return False
    condition = upload.get("condition")
    if condition is None:
        return True
    if not isinstance(condition, dict):
        raise SystemExit(f"target {target.get('id', '<unknown>')}.upload.condition must be an object")
    option = condition.get("option")
    equals = condition.get("equals")
    if not isinstance(option, str):
        raise SystemExit(
            f"target {target.get('id', '<unknown>')}.upload.condition.option is required"
        )
    return effective_option_value(target, payload, option) == equals


def upload_requested(target: dict[str, Any], payload: dict[str, Any]) -> bool:
    upload = target.get("upload", {})
    if not isinstance(upload, dict) or not upload.get("supported"):
        return False
    if upload.get("required") is True or upload.get("default") is True:
        return True
    trigger_options = require_string_list(
        upload.get("triggerOptions"),
        f"target {target.get('id', '<unknown>')}.upload.triggerOptions",
    )
    for key in trigger_options:
        if payload.get(key) is True:
            return True
    return False


def validate_upload_request(target: dict[str, Any], payload: dict[str, Any]) -> bool:
    upload = target.get("upload", {})
    if not isinstance(upload, dict):
        raise SystemExit(f"target {target.get('id', '<unknown>')}.upload must be an object")
    related_keys = upload_related_option_names(target)
    present_upload_keys = [
        key for key in payload if key in related_keys and payload.get(key) not in (False, None, "")
    ]
    if not upload.get("supported", False):
        if present_upload_keys:
            raise SystemExit(
                "upload options are not supported for this target: "
                + ", ".join(present_upload_keys)
            )
        return False
    requested = upload_requested(target, payload)
    wait_options = require_string_list(
        upload.get("waitOptions"),
        f"target {target.get('id', '<unknown>')}.upload.waitOptions",
    )
    wait_without_upload = [
        key for key in wait_options if payload.get(key) is True and not requested
    ]
    if wait_without_upload:
        raise SystemExit(
            "upload wait options require upload to be requested: "
            + ", ".join(wait_without_upload)
        )
    if requested and not upload_condition_allows(target, payload):
        raise SystemExit("upload requested but target upload condition is not satisfied")
    return requested


def enforce_dirty_policy(
    contract: dict[str, Any],
    target: dict[str, Any],
    project: Path,
    allow_dirty: bool,
) -> None:
    policy = str(contract.get("dirtyWorktreePolicy"))
    dirty_files = git_status_short(project, fail_closed=policy != "allow")
    if not dirty_files:
        return
    joined = "\n  ".join(redact(line, contract) for line in dirty_files)
    if policy == "allow":
        print(f"Dirty worktree detected; policy allows continuing:\n  {joined}")
        return
    if policy == "warn":
        print(f"Dirty worktree detected; continuing under warn policy:\n  {joined}")
        return
    should_block = policy == "block" or (
        policy == "block-store-release" and target.get("storeLike") is True
    )
    if should_block and not allow_dirty:
        raise SystemExit(
            "refusing release with dirty worktree; use --allow-dirty only after "
            f"explicit confirmation:\n  {joined}"
        )
    print(f"Proceeding with explicitly accepted dirty worktree:\n  {joined}")


def run_build(args: argparse.Namespace) -> int:
    if not args.confirm_build:
        raise SystemExit("refusing to build without --confirm-build")
    project = Path(args.project).expanduser().resolve()
    contract = load_contract(project, args.contract)
    target = target_by_id(contract, args.target)
    options = parse_options(args.option)
    validate_options(target, options)
    validate_required_files(project, target)
    payload = {"target": args.target, **options}
    enforce_dirty_policy(contract, target, project, args.allow_dirty)

    requested_upload = validate_upload_request(target, payload)
    if requested_upload and not args.confirm_upload:
        raise SystemExit("refusing upload without --confirm-upload")

    print("Build payload:")
    print(json.dumps(redact_data(payload, contract), indent=2, sort_keys=True))

    console = ReleaseConsole(project, contract)
    job_id = ""
    try:
        console.start()
        job = console.request_json("POST", console.endpoint("buildEndpoint"), payload)
        job_id = str(job.get("id", ""))
        if not job_id:
            raise SystemExit("release console did not return a job id")
        previous_logs: list[str] = []
        while True:
            logs = job.get("logs", [])
            if isinstance(logs, list):
                current_logs = [str(line) for line in logs]
                start = overlap_index(previous_logs, current_logs)
                for line in current_logs[start:]:
                    print(redact(line, contract))
                previous_logs = current_logs
            if job.get("running") is False:
                exit_code = int(job.get("exitCode", 1) or 0)
                evidence_found = print_evidence(previous_logs, target, contract)
                if (
                    exit_code == 0
                    and target.get("storeLike") is True
                    and evidence_required(target)
                    and not evidence_found
                ):
                    print("Release evidence: required labels were not found", file=sys.stderr)
                    return 1
                return exit_code
            time.sleep(args.poll_interval)
            job = console.request_json(
                "GET",
                console.endpoint("jobEndpoint", id=job_id),
            )
    except KeyboardInterrupt:
        if job_id:
            cancel = console.config.get("cancelEndpoint")
            if isinstance(cancel, str) and cancel:
                try:
                    console.request_json(
                        "POST",
                        console.endpoint("cancelEndpoint", id=job_id),
                    )
                except SystemExit as error:
                    print(
                        redact(f"cancel request failed: {error}", contract),
                        file=sys.stderr,
                    )
        print("interrupted; terminating release console", file=sys.stderr)
        if requested_upload:
            print("remote upload may already have started", file=sys.stderr)
        return 130
    finally:
        console.close()


def overlap_index(previous: list[str], current: list[str]) -> int:
    if not previous or not current:
        return 0
    max_overlap = min(len(previous), len(current))
    for size in range(max_overlap, 0, -1):
        if previous[-size:] == current[:size]:
            return size
    return 0


def print_evidence(
    logs: list[str],
    target: dict[str, Any],
    contract: dict[str, Any],
) -> bool:
    evidence_config = target.get("evidence", {})
    labels: list[str] = []
    if isinstance(evidence_config, dict):
        for key, value in evidence_config.items():
            if key.endswith("Labels"):
                labels.extend(
                    require_string_list(
                        value,
                        f"target {target.get('id', '<unknown>')}.evidence.{key}",
                    )
                )
    if not labels:
        return False
    found: dict[str, str] = {}
    for line in logs:
        for label in labels:
            prefix = f"{label}:"
            if line.startswith(prefix):
                found[label] = line[len(prefix) :].strip()
    if not found:
        print("Release evidence: none found in final logs")
        return False
    print("Release evidence:")
    for label, value in found.items():
        print(f"  {label}: {redact(value, contract)}")
    return True


def evidence_required(target: dict[str, Any]) -> bool:
    evidence_config = target.get("evidence", {})
    return isinstance(evidence_config, dict) and evidence_config.get(
        "requiredForSuccess",
        False,
    ) is True


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=os.getcwd())
    parser.add_argument("--contract", default=DEFAULT_CONTRACT_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status")
    status.add_argument("--project", default=argparse.SUPPRESS)
    status.add_argument("--contract", default=argparse.SUPPRESS)
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=run_status)

    build = subparsers.add_parser("build")
    build.add_argument("--project", default=argparse.SUPPRESS)
    build.add_argument("--contract", default=argparse.SUPPRESS)
    build.add_argument("--target", required=True)
    build.add_argument("--option", action="append", default=[])
    build.add_argument("--allow-dirty", action="store_true")
    build.add_argument("--confirm-build", action="store_true")
    build.add_argument("--confirm-upload", action="store_true")
    build.add_argument("--poll-interval", type=float, default=1.0)
    build.set_defaults(func=run_build)
    return parser


def main() -> int:
    parser = make_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
