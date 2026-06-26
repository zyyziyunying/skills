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
    return contract


def target_by_id(contract: dict[str, Any], target_id: str) -> dict[str, Any]:
    targets = contract.get("targets", [])
    if not isinstance(targets, list):
        raise SystemExit("contract targets must be a list")
    for target in targets:
        if isinstance(target, dict) and target.get("id") == target_id:
            return target
    raise SystemExit(f"unknown target in contract: {target_id}")


def git_status_short(project: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def redact(value: str, contract: dict[str, Any]) -> str:
    redacted = value
    secret_config = contract.get("secretRedaction", {})
    prefixes = []
    key_names = []
    patterns = []
    if isinstance(secret_config, dict):
        prefixes = [str(item) for item in secret_config.get("environmentPrefixes", [])]
        key_names = [str(item) for item in secret_config.get("keyNames", [])]
        patterns = [str(item) for item in secret_config.get("patterns", [])]

    for prefix in prefixes:
        redacted = re.sub(
            rf"({re.escape(prefix)}[A-Za-z0-9_]*=)[^\s]+",
            r"\1<redacted>",
            redacted,
        )
    for key in key_names:
        redacted = re.sub(
            rf"({re.escape(key)}[=:]\s*)[^\s,;]+",
            r"\1<redacted>",
            redacted,
            flags=re.IGNORECASE,
        )
    for pattern in patterns:
        redacted = re.sub(pattern, "<redacted>", redacted)
    redacted = re.sub(r"(token=)[^&\s]+", r"\1<redacted>", redacted)
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
        options[key] = coerce_option_value(raw_value)
    return options


def validate_options(target: dict[str, Any], options: dict[str, Any]) -> None:
    allowed = target.get("allowedOptions", [])
    forbidden = target.get("forbiddenOptions", [])
    allowed_set = {str(item) for item in allowed} if isinstance(allowed, list) else set()
    forbidden_set = (
        {str(item) for item in forbidden} if isinstance(forbidden, list) else set()
    )
    for key in options:
        if key in forbidden_set:
            raise SystemExit(f"option is forbidden by contract for this target: {key}")
        if allowed_set and key not in allowed_set:
            raise SystemExit(f"option is not allowed by contract for this target: {key}")


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
            raise SystemExit(f"HTTP {error.code} from release console: {body}")


def print_status(status: dict[str, Any], project: Path, contract: dict[str, Any]) -> None:
    print("Project:", status.get("projectRoot", project))
    print("Branch:", status.get("branch", "-"))
    print("Commit:", status.get("commit", "-"))
    print("Version:", status.get("pubspecVersion", "-"))
    dirty_files = git_status_short(project)
    print("Dirty count:", len(dirty_files) if dirty_files else status.get("dirtyCount", 0))
    if dirty_files:
        print("Dirty files:")
        for line in dirty_files:
            print(f"  {line}")
    checks = status.get("checks", [])
    if isinstance(checks, list):
        print("Checks:")
        for item in checks:
            if not isinstance(item, dict):
                continue
            label = "OK" if item.get("exists") is True else "MISSING"
            print(f"  {label} {item.get('path', '-')}")
    targets = status.get("targets", [])
    if isinstance(targets, list):
        print("Targets:")
        for item in targets:
            if isinstance(item, dict):
                print(f"  {item.get('id')}: {item.get('label')}")


def run_status(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    contract = load_contract(project, args.contract)
    console = ReleaseConsole(project, contract)
    try:
        console.start(quiet=args.json)
        status = console.request_json("GET", console.endpoint("statusEndpoint"))
        if args.json:
            print(json.dumps(status, indent=2, sort_keys=True))
        else:
            print_status(status, project, contract)
        return 0
    finally:
        console.close()


def upload_requested(target: dict[str, Any], payload: dict[str, Any]) -> bool:
    upload = target.get("upload", {})
    if not isinstance(upload, dict) or not upload.get("supported"):
        return False
    for key in ("uploadAfterBuild", "iosUploadAfterBuild", "upload"):
        if payload.get(key) is True:
            return True
    return False


def run_build(args: argparse.Namespace) -> int:
    if not args.confirm_build:
        raise SystemExit("refusing to build without --confirm-build")
    project = Path(args.project).expanduser().resolve()
    contract = load_contract(project, args.contract)
    target = target_by_id(contract, args.target)
    options = parse_options(args.option)
    validate_options(target, options)
    validate_required_files(project, target)

    dirty_files = git_status_short(project)
    if dirty_files and target.get("storeLike") is True and not args.allow_dirty:
        joined = "\n  ".join(dirty_files)
        raise SystemExit(
            "refusing store-like release with dirty worktree; use --allow-dirty "
            f"only after explicit confirmation:\n  {joined}"
        )

    payload = {"target": args.target, **options}
    if upload_requested(target, payload) and not args.confirm_upload:
        raise SystemExit("refusing upload without --confirm-upload")

    print("Build payload:")
    print(redact(json.dumps(payload, indent=2, sort_keys=True), contract))

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
                print_evidence(previous_logs, target, contract)
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
                    print(f"cancel request failed: {error}", file=sys.stderr)
        print("interrupted; terminating release console", file=sys.stderr)
        if upload_requested(target, payload):
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
) -> None:
    evidence_config = target.get("evidence", {})
    labels: list[str] = []
    if isinstance(evidence_config, dict):
        for key in ("artifactLabels", "manifestLabels", "symbolLabels"):
            value = evidence_config.get(key, [])
            if isinstance(value, list):
                labels.extend(str(item) for item in value)
    if not labels:
        return
    found: dict[str, str] = {}
    for line in logs:
        for label in labels:
            prefix = f"{label}:"
            if line.startswith(prefix):
                found[label] = line[len(prefix) :].strip()
    if not found:
        print("Release evidence: none found in final logs")
        return
    print("Release evidence:")
    for label, value in found.items():
        print(f"  {label}: {redact(value, contract)}")


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
