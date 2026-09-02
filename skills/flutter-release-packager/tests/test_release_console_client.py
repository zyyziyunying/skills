#!/usr/bin/env python3
"""Offline regression tests for release agent contract validation."""

from __future__ import annotations

import copy
import io
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
CLIENT_PATH = SKILL_ROOT / "scripts" / "release_console_client.py"
CONTRACT_TEMPLATE_PATH = (
    SKILL_ROOT / "assets" / "templates" / "release-agent-contract.json"
)


def load_client_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("release_console_client", CLIENT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load release console client: {CLIENT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CLIENT = load_client_module()


def template_contract() -> dict[str, object]:
    with CONTRACT_TEMPLATE_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


class ValidateContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = template_contract()

    def first_target(self) -> dict[str, object]:
        targets = self.contract["targets"]
        assert isinstance(targets, list)
        target = targets[0]
        assert isinstance(target, dict)
        return target

    def release_console(self) -> dict[str, object]:
        release_console = self.contract["releaseConsole"]
        assert isinstance(release_console, dict)
        return release_console

    def test_template_contract_is_valid(self) -> None:
        self.assertEqual(self.contract["schemaVersion"], 2)
        CLIENT.validate_contract(self.contract)

    def test_legacy_schema_one_contract_remains_compatible(self) -> None:
        self.contract["schemaVersion"] = 1
        self.contract.pop("gitIdentity")
        self.contract.pop("releaseRecords")
        targets = self.contract["targets"]
        assert isinstance(targets, list)
        for target in targets:
            assert isinstance(target, dict)
            options = target.pop("options")
            assert isinstance(options, list)
            target["allowedOptions"] = [
                option["name"]
                for option in options
                if isinstance(option, dict) and isinstance(option.get("name"), str)
            ]
            for field in ("platform", "releaseLine", "branchTemplate", "command"):
                target.pop(field)
            evidence = target.get("evidence")
            if isinstance(evidence, dict):
                evidence.pop("requiredLabelGroups", None)

        CLIENT.validate_contract(self.contract)
        first_target = targets[0]
        assert isinstance(first_target, dict)
        self.assertEqual(
            CLIENT.missing_required_evidence_groups(
                first_target,
                {"AAB"},
                schema_version=1,
            ),
            [],
        )
        self.assertEqual(
            CLIENT.missing_required_evidence_groups(
                first_target,
                set(),
                schema_version=1,
            ),
            ["evidence"],
        )

    def test_schema_two_accepts_matching_legacy_allowed_options(self) -> None:
        target = self.first_target()
        options = target["options"]
        assert isinstance(options, list)
        target["allowedOptions"] = [
            option["name"]
            for option in options
            if isinstance(option, dict) and isinstance(option.get("name"), str)
        ]

        CLIENT.validate_contract(self.contract)

        target["allowedOptions"].append("notInTypedOptions")
        with self.assertRaisesRegex(SystemExit, r"must match target options schema"):
            CLIENT.validate_contract(self.contract)

    def test_unknown_contract_schema_is_rejected(self) -> None:
        self.contract["schemaVersion"] = 3
        with self.assertRaisesRegex(
            SystemExit,
            r"schemaVersion must be an integer with one of these values: 1, 2",
        ):
            CLIENT.validate_contract(self.contract)

    def test_non_integer_contract_schema_is_rejected(self) -> None:
        for value in (True, 1.0, 2.0):
            with self.subTest(value=value):
                self.contract["schemaVersion"] = value
                with self.assertRaisesRegex(
                    SystemExit,
                    r"schemaVersion must be an integer",
                ):
                    CLIENT.validate_contract(self.contract)

    def test_optional_file_arrays_may_be_omitted(self) -> None:
        target = self.first_target()
        target.pop("requiredFiles")
        target.pop("requiredEnvFiles")

        CLIENT.validate_contract(self.contract)

    def test_startup_url_pattern_may_be_omitted(self) -> None:
        self.release_console().pop("startupUrlPattern")

        CLIENT.validate_contract(self.contract)

    def test_rejects_non_array_required_file_fields(self) -> None:
        malformed_values = (None, "assets/env/release.env", {})
        for field_name in ("requiredFiles", "requiredEnvFiles"):
            for malformed_value in malformed_values:
                with self.subTest(field=field_name, value=malformed_value):
                    contract = copy.deepcopy(self.contract)
                    target = contract["targets"][0]
                    target[field_name] = malformed_value

                    with self.assertRaisesRegex(
                        SystemExit,
                        rf"target android-release-aab\.{field_name} "
                        r"must be a string array",
                    ):
                        CLIENT.validate_contract(contract)

    def test_rejects_non_string_required_file_items(self) -> None:
        target = self.first_target()
        target["requiredFiles"] = ["assets/env/release.env", 1]

        with self.assertRaisesRegex(
            SystemExit,
            r"target android-release-aab\.requiredFiles must be a string array",
        ):
            CLIENT.validate_contract(self.contract)

    def test_rejects_non_boolean_required_for_success(self) -> None:
        evidence = self.first_target()["evidence"]
        assert isinstance(evidence, dict)
        evidence["requiredForSuccess"] = "true"

        with self.assertRaisesRegex(
            SystemExit,
            r"target android-release-aab\.evidence\.requiredForSuccess must be boolean",
        ):
            CLIENT.validate_contract(self.contract)

    def test_required_evidence_needs_explicit_complete_groups(self) -> None:
        evidence = self.first_target()["evidence"]
        assert isinstance(evidence, dict)
        evidence.pop("requiredLabelGroups")

        with self.assertRaisesRegex(
            SystemExit,
            r"evidence\.requiredLabelGroups must be a string array",
        ):
            CLIENT.validate_contract(self.contract)

    def test_required_evidence_groups_and_values_must_not_be_empty(self) -> None:
        evidence = self.first_target()["evidence"]
        assert isinstance(evidence, dict)
        evidence["requiredLabelGroups"] = []
        with self.assertRaisesRegex(SystemExit, r"must not be empty"):
            CLIENT.validate_contract(self.contract)

        contract = template_contract()
        target = contract["targets"][0]
        assert isinstance(target, dict)
        evidence = target["evidence"]
        assert isinstance(evidence, dict)
        found = CLIENT.print_evidence(["AAB:"], target, contract)
        self.assertEqual(found, set())
        self.assertIn(
            "artifactLabels",
            CLIENT.missing_required_evidence_groups(target, found),
        )

    def test_missing_required_evidence_groups_are_reported(self) -> None:
        target = self.first_target()
        missing = CLIENT.missing_required_evidence_groups(target, {"AAB"})

        self.assertIn("manifestLabels", missing)
        self.assertIn("releaseRecordLabels", missing)
        self.assertNotIn("artifactLabels", missing)

    def test_release_records_require_tag_and_append_commands(self) -> None:
        records = self.contract["releaseRecords"]
        assert isinstance(records, dict)
        records.pop("appendCommand")

        with self.assertRaisesRegex(
            SystemExit,
            r"releaseRecords\.appendCommand must be a string array",
        ):
            CLIENT.validate_contract(self.contract)

    def test_explicit_null_release_records_is_rejected(self) -> None:
        self.contract["releaseRecords"] = None

        with self.assertRaisesRegex(SystemExit, r"releaseRecords must be an object"):
            CLIENT.validate_contract(self.contract)

    def test_git_identity_runtime_flags_must_be_booleans(self) -> None:
        for field in (
            "requiresCleanWorktree",
            "tagPushRequired",
            "pushTagsAutomatically",
            "requiresSeparatePushConfirmation",
        ):
            with self.subTest(field=field):
                contract = copy.deepcopy(self.contract)
                identity = contract["gitIdentity"]
                assert isinstance(identity, dict)
                identity[field] = "true"
                with self.assertRaisesRegex(
                    SystemExit,
                    rf"gitIdentity\.{field} must be a boolean",
                ):
                    CLIENT.validate_contract(contract)

    def test_target_command_is_required(self) -> None:
        self.first_target().pop("command")

        with self.assertRaisesRegex(
            SystemExit,
            r"target android-release-aab\.command must be a string array",
        ):
            CLIENT.validate_contract(self.contract)

    def test_target_identity_fields_are_required(self) -> None:
        for field in ("platform", "releaseLine", "branchTemplate"):
            with self.subTest(field=field):
                contract = copy.deepcopy(self.contract)
                target = contract["targets"][0]
                target.pop(field)
                with self.assertRaisesRegex(
                    SystemExit,
                    rf"must define non-empty {field}",
                ):
                    CLIENT.validate_contract(contract)

    def test_schema_two_allows_branchless_targets_when_identity_allows_them(self) -> None:
        identity = self.contract["gitIdentity"]
        targets = self.contract["targets"]
        assert isinstance(identity, dict)
        assert isinstance(targets, list)
        identity["requiresNamedBranch"] = False
        for target in targets:
            assert isinstance(target, dict)
            target.pop("branchTemplate")

        CLIENT.validate_contract(self.contract)

    def test_schema_two_requires_explicit_boolean_named_branch_policy(self) -> None:
        identity = self.contract["gitIdentity"]
        assert isinstance(identity, dict)
        identity.pop("requiresNamedBranch")

        with self.assertRaisesRegex(
            SystemExit,
            r"schema version 2 gitIdentity.requiresNamedBranch must be a boolean",
        ):
            CLIENT.validate_contract(self.contract)

        identity["requiresNamedBranch"] = "true"
        with self.assertRaisesRegex(
            SystemExit,
            r"schema version 2 gitIdentity.requiresNamedBranch must be a boolean",
        ):
            CLIENT.validate_contract(self.contract)

    def test_schema_two_rejects_non_object_git_identity(self) -> None:
        for value in (None, "invalid", [], True):
            with self.subTest(value=value):
                contract = copy.deepcopy(self.contract)
                contract["gitIdentity"] = value
                with self.assertRaisesRegex(
                    SystemExit,
                    r"schema version 2 gitIdentity must be an object",
                ):
                    CLIENT.validate_contract(contract)

    def test_schema_two_allows_omitted_git_identity(self) -> None:
        self.contract.pop("gitIdentity")
        self.contract.pop("releaseRecords")

        CLIENT.validate_contract(self.contract)

    def test_release_records_require_exact_git_identity_posture(self) -> None:
        identity = self.contract["gitIdentity"]
        assert isinstance(identity, dict)
        identity["requiresCleanWorktree"] = False

        with self.assertRaisesRegex(
            SystemExit,
            r"releaseRecords requires a clean Git worktree",
        ):
            CLIENT.validate_contract(self.contract)

    def test_release_records_auto_record_flag_must_be_boolean(self) -> None:
        records = self.contract["releaseRecords"]
        assert isinstance(records, dict)
        records["autoRecordAfterBuildSuccess"] = "true"

        with self.assertRaisesRegex(
            SystemExit,
            r"autoRecordAfterBuildSuccess must be a boolean",
        ):
            CLIENT.validate_contract(self.contract)

    def test_tag_push_command_must_use_declared_remote(self) -> None:
        identity = self.contract["gitIdentity"]
        records = self.contract["releaseRecords"]
        assert isinstance(identity, dict)
        assert isinstance(records, dict)
        identity["tagPushRequired"] = True
        identity["tagRemote"] = "origin"
        records["pushCommand"] = [
            "dart",
            "run",
            "tool/release_records.dart",
            "push",
            "--remote",
            "backup",
            "origin",
        ]

        with self.assertRaisesRegex(
            SystemExit,
            r"pushCommand must use gitIdentity.tagRemote",
        ):
            CLIENT.validate_contract(self.contract)

    def test_rejects_non_string_startup_url_pattern(self) -> None:
        self.release_console()["startupUrlPattern"] = 123

        with self.assertRaisesRegex(
            SystemExit,
            r"releaseConsole\.startupUrlPattern must be a string",
        ):
            CLIENT.validate_contract(self.contract)

    def test_rejects_invalid_startup_url_pattern(self) -> None:
        self.release_console()["startupUrlPattern"] = "["

        with self.assertRaisesRegex(
            SystemExit,
            r"releaseConsole\.startupUrlPattern must be a valid regular expression",
        ):
            CLIENT.validate_contract(self.contract)

    def test_rejects_startup_url_pattern_without_capture_group(self) -> None:
        self.release_console()["startupUrlPattern"] = r"Release console:\s+\S+"

        with self.assertRaisesRegex(
            SystemExit,
            r"releaseConsole\.startupUrlPattern must contain at least one capture group",
        ):
            CLIENT.validate_contract(self.contract)


class StartupUrlCaptureTest(unittest.TestCase):
    def start_console(self, pattern: str, line: str):
        contract = template_contract()
        release_console = contract["releaseConsole"]
        assert isinstance(release_console, dict)
        release_console["startupUrlPattern"] = pattern
        CLIENT.validate_contract(contract)

        process = mock.Mock()
        process.stdout = io.StringIO(line + "\n")
        process.poll.return_value = None
        selector = mock.Mock()
        selector.select.return_value = [
            (SimpleNamespace(fileobj=process.stdout), None),
        ]

        console = CLIENT.ReleaseConsole(Path.cwd(), contract)
        with (
            mock.patch.object(CLIENT.subprocess, "Popen", return_value=process),
            mock.patch.object(
                CLIENT.selectors,
                "DefaultSelector",
                return_value=selector,
            ),
        ):
            console.start(quiet=True)
        return console

    def test_start_rejects_first_capture_group_that_is_not_a_url(self) -> None:
        with self.assertRaisesRegex(
            SystemExit,
            r"first capture group must be an absolute http\(s\) URL",
        ):
            self.start_console(
                r"(Release console):\s+(https?://\S+)",
                "Release console: http://127.0.0.1:4321",
            )

    def test_start_rejects_unmatched_optional_first_capture_group(self) -> None:
        with self.assertRaisesRegex(
            SystemExit,
            r"first capture group must contain the console URL",
        ):
            self.start_console(
                r"(https?://first\.invalid)?(https?://127\.0\.0\.1:4321)",
                "http://127.0.0.1:4321",
            )

    def test_start_accepts_absolute_url_in_first_capture_group(self) -> None:
        console = self.start_console(
            r"Release console:\s+(\S+)",
            "Release console: http://127.0.0.1:4321?token=test-token",
        )

        self.assertEqual(console.base_url, "http://127.0.0.1:4321")
        self.assertEqual(console.token, "test-token")


class ReleaseLifecycleTest(unittest.TestCase):
    def test_block_dirty_policy_is_not_overridable(self) -> None:
        contract = template_contract()
        contract["dirtyWorktreePolicy"] = "block"
        target = contract["targets"][0]
        assert isinstance(target, dict)

        with (
            mock.patch.object(CLIENT, "git_status_short", return_value=[" M pubspec.yaml"]),
            self.assertRaisesRegex(SystemExit, r"refusing release under block"),
        ):
            CLIENT.enforce_dirty_policy(contract, target, Path.cwd())

    def test_git_identity_rejects_detached_head(self) -> None:
        contract = template_contract()
        target = contract["targets"][0]
        assert isinstance(target, dict)
        completed = SimpleNamespace(returncode=0, stdout="\n", stderr="")
        with (
            mock.patch.object(CLIENT.subprocess, "run", return_value=completed),
            self.assertRaisesRegex(SystemExit, r"requires a named Git branch"),
        ):
            CLIENT.enforce_git_identity(contract, target, Path.cwd())

    def test_git_identity_allows_detached_head_when_contract_allows_it(self) -> None:
        contract = template_contract()
        identity = contract["gitIdentity"]
        target = contract["targets"][0]
        assert isinstance(identity, dict)
        assert isinstance(target, dict)
        identity["requiresNamedBranch"] = False
        target.pop("branchTemplate")
        completed = SimpleNamespace(returncode=0, stdout="\n", stderr="")
        with (
            mock.patch.object(CLIENT.subprocess, "run", return_value=completed),
            mock.patch.object(CLIENT, "git_status_short", return_value=[]),
        ):
            CLIENT.enforce_git_identity(contract, target, Path.cwd())

    def test_legacy_identity_without_named_branch_allows_detached_head(self) -> None:
        contract = template_contract()
        contract["schemaVersion"] = 1
        contract.pop("releaseRecords")
        identity = contract["gitIdentity"]
        target = contract["targets"][0]
        assert isinstance(identity, dict)
        assert isinstance(target, dict)
        identity.pop("requiresNamedBranch")
        target.pop("branchTemplate")
        CLIENT.validate_contract(contract)

        completed = SimpleNamespace(returncode=0, stdout="\n", stderr="")
        with (
            mock.patch.object(CLIENT.subprocess, "run", return_value=completed),
            mock.patch.object(CLIENT, "git_status_short", return_value=[]),
        ):
            CLIENT.enforce_git_identity(contract, target, Path.cwd())

    def test_git_identity_rejects_wrong_store_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "pubspec.yaml").write_text(
                "name: fixture\nversion: 2.0.0+40\n",
                encoding="utf-8",
            )
            contract = template_contract()
            target = contract["targets"][0]
            assert isinstance(target, dict)
            branch = SimpleNamespace(
                returncode=0,
                stdout="release/store/android/not-the-version\n",
                stderr="",
            )
            with (
                mock.patch.object(CLIENT.subprocess, "run", return_value=branch),
                mock.patch.object(CLIENT, "git_status_short", return_value=[]),
                self.assertRaisesRegex(SystemExit, r"does not match target template"),
            ):
                CLIENT.enforce_git_identity(contract, target, project)

    def test_git_identity_accepts_exact_store_branch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "pubspec.yaml").write_text(
                "name: fixture\nversion: 2.0.0+40\n",
                encoding="utf-8",
            )
            contract = template_contract()
            target = contract["targets"][0]
            assert isinstance(target, dict)
            branch = SimpleNamespace(
                returncode=0,
                stdout="release/store/android/2.0.0+40\n",
                stderr="",
            )
            with (
                mock.patch.object(CLIENT.subprocess, "run", return_value=branch),
                mock.patch.object(CLIENT, "git_status_short", return_value=[]),
            ):
                CLIENT.enforce_git_identity(contract, target, project)

    def test_git_identity_rejects_invalid_daily_date(self) -> None:
        contract = template_contract()
        target = contract["targets"][0]
        assert isinstance(target, dict)
        target["branchTemplate"] = "release/daily/android-release-aab/<yyyy-mm-dd>"
        branch = SimpleNamespace(
            returncode=0,
            stdout="release/daily/android-release-aab/2026-02-30\n",
            stderr="",
        )
        with (
            mock.patch.object(CLIENT.subprocess, "run", return_value=branch),
            mock.patch.object(CLIENT, "git_status_short", return_value=[]),
            self.assertRaisesRegex(SystemExit, r"invalid calendar date"),
        ):
            CLIENT.enforce_git_identity(contract, target, Path.cwd())

    def test_record_requires_confirmation_and_runs_tag_then_append(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            contract_path = project / CLIENT.DEFAULT_CONTRACT_PATH
            contract_path.parent.mkdir(parents=True)
            contract_path.write_text(json.dumps(template_contract()), encoding="utf-8")
            event_file = project / "release-record.json"
            event_file.write_text(
                '{"git_tag":"release/store/android/v1.0.0+1"}\n',
                encoding="utf-8",
            )
            args = SimpleNamespace(
                project=str(project),
                contract=CLIENT.DEFAULT_CONTRACT_PATH,
                event_file=str(event_file),
                confirm_record=False,
            )
            with self.assertRaisesRegex(SystemExit, r"without --confirm-record"):
                CLIENT.run_record(args)

            args.confirm_record = True
            completed = SimpleNamespace(returncode=0, stdout="ok\n", stderr="")
            with mock.patch.object(
                CLIENT.subprocess,
                "run",
                return_value=completed,
            ) as run:
                self.assertEqual(CLIENT.run_record(args), 0)

            commands = [call.args[0] for call in run.call_args_list]
            self.assertEqual(commands[0][3], "tag")
            self.assertEqual(commands[1][3], "append")
            self.assertEqual(
                commands[0][-2:],
                ["--event-file", str(event_file.resolve())],
            )

    def test_successful_build_auto_records_generated_draft(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            event_file = project / "release-record.json"
            event_file.write_text("{}\n", encoding="utf-8")
            contract = template_contract()
            records = contract["releaseRecords"]
            assert isinstance(records, dict)
            records["autoRecordAfterBuildSuccess"] = True
            output = io.StringIO()

            with (
                mock.patch.object(CLIENT, "run_contract_command") as run,
                mock.patch("sys.stdout", output),
            ):
                CLIENT.finalize_release_record_after_build(
                    project,
                    [f"Release record: {event_file}"],
                    contract,
                )

            self.assertEqual(
                [call.args[2] for call in run.call_args_list],
                ["tagCommand", "appendCommand"],
            )
            self.assertIn("completed automatically", output.getvalue())

    def test_failed_build_or_requested_upload_never_finalizes_record(self) -> None:
        for requested_upload in (False, True):
            with self.subTest(requested_upload=requested_upload):
                contract = template_contract()
                records = contract["releaseRecords"]
                targets = contract["targets"]
                assert isinstance(records, dict)
                assert isinstance(targets, list)
                target = targets[0]
                assert isinstance(target, dict)
                records["autoRecordAfterBuildSuccess"] = True
                args = SimpleNamespace(
                    project=str(Path.cwd()),
                    contract=CLIENT.DEFAULT_CONTRACT_PATH,
                    target=target["id"],
                    option=[],
                    confirm_build=True,
                    confirm_upload=requested_upload,
                    poll_interval=0,
                )
                console = mock.Mock()
                console.request_json.return_value = {
                    "id": "failed-job",
                    "running": False,
                    "exitCode": 17,
                    "logs": [],
                }

                with (
                    mock.patch.object(CLIENT, "load_contract", return_value=contract),
                    mock.patch.object(CLIENT, "validate_required_files"),
                    mock.patch.object(CLIENT, "enforce_git_identity"),
                    mock.patch.object(CLIENT, "enforce_dirty_policy"),
                    mock.patch.object(
                        CLIENT,
                        "validate_upload_request",
                        return_value=requested_upload,
                    ),
                    mock.patch.object(CLIENT, "ReleaseConsole", return_value=console),
                    mock.patch.object(
                        CLIENT,
                        "finalize_release_record_after_build",
                    ) as finalize,
                ):
                    self.assertEqual(CLIENT.run_build(args), 17)

                finalize.assert_not_called()
                console.close.assert_called_once()

    def test_missing_required_evidence_never_finalizes_record(self) -> None:
        contract = template_contract()
        records = contract["releaseRecords"]
        targets = contract["targets"]
        assert isinstance(records, dict)
        assert isinstance(targets, list)
        target = targets[0]
        assert isinstance(target, dict)
        records["autoRecordAfterBuildSuccess"] = True
        args = SimpleNamespace(
            project=str(Path.cwd()),
            contract=CLIENT.DEFAULT_CONTRACT_PATH,
            target=target["id"],
            option=[],
            confirm_build=True,
            confirm_upload=False,
            poll_interval=0,
        )
        console = mock.Mock()
        console.request_json.return_value = {
            "id": "missing-evidence-job",
            "running": False,
            "exitCode": 0,
            "logs": [],
        }

        with (
            mock.patch.object(CLIENT, "load_contract", return_value=contract),
            mock.patch.object(CLIENT, "validate_required_files"),
            mock.patch.object(CLIENT, "enforce_git_identity"),
            mock.patch.object(CLIENT, "enforce_dirty_policy"),
            mock.patch.object(
                CLIENT,
                "validate_upload_request",
                return_value=False,
            ),
            mock.patch.object(CLIENT, "ReleaseConsole", return_value=console),
            mock.patch.object(
                CLIENT,
                "finalize_release_record_after_build",
            ) as finalize,
        ):
            self.assertEqual(CLIENT.run_build(args), 1)

        finalize.assert_not_called()
        console.close.assert_called_once()

    def test_auto_record_rejects_missing_draft_before_commands(self) -> None:
        contract = template_contract()
        records = contract["releaseRecords"]
        assert isinstance(records, dict)
        records["autoRecordAfterBuildSuccess"] = True

        for logs in (
            [],
            ["Release record: /tmp/missing-release-record.json"],
        ):
            with (
                self.subTest(logs=logs),
                mock.patch.object(CLIENT, "run_contract_command") as run,
                self.assertRaises(SystemExit),
            ):
                CLIENT.finalize_release_record_after_build(
                    Path.cwd(),
                    logs,
                    contract,
                )
            run.assert_not_called()

    def test_tag_failure_prevents_append(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            event_file = project / "release-record.json"
            event_file.write_text("{}\n", encoding="utf-8")
            contract = template_contract()
            records = contract["releaseRecords"]
            assert isinstance(records, dict)
            records["autoRecordAfterBuildSuccess"] = True

            with mock.patch.object(
                CLIENT,
                "run_contract_command",
                side_effect=SystemExit("tag rejected draft"),
            ) as run, self.assertRaisesRegex(SystemExit, r"tag rejected draft"):
                CLIENT.finalize_release_record_after_build(
                    project,
                    [f"Release record: {event_file}"],
                    contract,
                )

            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[2], "tagCommand")

    def test_build_leaves_draft_pending_when_auto_record_is_disabled(self) -> None:
        contract = template_contract()
        output = io.StringIO()

        with (
            mock.patch.object(CLIENT, "run_contract_command") as run,
            mock.patch("sys.stdout", output),
        ):
            CLIENT.finalize_release_record_after_build(
                Path.cwd(),
                ["Release record: /tmp/release-record.json"],
                contract,
            )

        run.assert_not_called()
        self.assertIn("pending review", output.getvalue())

    def test_record_forwards_opaque_draft_to_project_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            command_script = project / "record_command.py"
            command_script.write_text(
                "from pathlib import Path\n"
                "import sys\n"
                "event_file = Path(sys.argv[sys.argv.index('--event-file') + 1])\n"
                "trace_file = event_file.parent / 'record-commands.log'\n"
                "with trace_file.open('a', encoding='utf-8') as handle:\n"
                "    handle.write(f'{sys.argv[1]}:{event_file.name}\\n')\n"
                "if sys.argv[1] == 'tag':\n"
                "    print('Package tag not required; no tag created.')\n"
                "else:\n"
                "    print('Release record appended.')\n",
                encoding="utf-8",
            )
            contract = template_contract()
            records = contract["releaseRecords"]
            assert isinstance(records, dict)
            records["tagCommand"] = [sys.executable, str(command_script), "tag"]
            records["appendCommand"] = [
                sys.executable,
                str(command_script),
                "append",
            ]
            contract_path = project / CLIENT.DEFAULT_CONTRACT_PATH
            contract_path.parent.mkdir(parents=True)
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            event_file = project / "release-record.yaml"
            event_file.write_text(
                "release_line: daily\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(
                project=str(project),
                contract=CLIENT.DEFAULT_CONTRACT_PATH,
                event_file=str(event_file),
                confirm_record=True,
            )
            output = io.StringIO()
            with mock.patch("sys.stdout", output):
                self.assertEqual(CLIENT.run_record(args), 0)

            self.assertEqual(
                (project / "record-commands.log").read_text(encoding="utf-8").splitlines(),
                ["tag:release-record.yaml", "append:release-record.yaml"],
            )
            self.assertIn("Package tag not required", output.getvalue())
            self.assertIn("Release record appended", output.getvalue())

    def test_record_reports_push_boundary_without_claiming_remote_state(self) -> None:
        contract = {
            "gitIdentity": {
                "dailyTagRequired": False,
                "tagPushRequired": True,
            }
        }
        args = SimpleNamespace(
            project=".",
            contract=CLIENT.DEFAULT_CONTRACT_PATH,
            event_file="daily-release-record.json",
            confirm_record=True,
        )
        event_file = Path("daily-release-record.json").resolve()
        output = io.StringIO()
        with (
            mock.patch.object(CLIENT, "load_contract", return_value=contract),
            mock.patch.object(CLIENT, "resolve_event_file", return_value=event_file),
            mock.patch.object(CLIENT, "run_contract_command"),
            mock.patch("sys.stdout", output),
        ):
            self.assertEqual(CLIENT.run_record(args), 0)

        self.assertIn(
            "This command did not perform a remote tag push",
            output.getvalue(),
        )
        self.assertIn("separately confirmed push-tag flow", output.getvalue())
        self.assertNotIn("pending", output.getvalue())

    def test_push_tag_requires_separate_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            contract = template_contract()
            identity = contract["gitIdentity"]
            records = contract["releaseRecords"]
            assert isinstance(identity, dict)
            assert isinstance(records, dict)
            identity["tagPushRequired"] = True
            identity["tagRemote"] = "origin"
            records["pushCommand"] = [
                "dart",
                "run",
                "tool/release_records.dart",
                "push",
                "--remote",
                "origin",
            ]
            contract_path = project / CLIENT.DEFAULT_CONTRACT_PATH
            contract_path.parent.mkdir(parents=True)
            contract_path.write_text(json.dumps(contract), encoding="utf-8")
            event_file = project / "release-record.yaml"
            event_file.write_text(
                "tag: release/store/android/v1.0.0+1\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(
                project=str(project),
                contract=CLIENT.DEFAULT_CONTRACT_PATH,
                event_file=str(event_file),
                confirm_push=False,
            )
            with self.assertRaisesRegex(SystemExit, r"without --confirm-push"):
                CLIENT.run_push_tag(args)

            args.confirm_push = True
            completed = SimpleNamespace(returncode=0, stdout="ok\n", stderr="")
            with mock.patch.object(
                CLIENT.subprocess,
                "run",
                return_value=completed,
            ) as run:
                self.assertEqual(CLIENT.run_push_tag(args), 0)

            command = run.call_args.args[0]
            self.assertEqual(command[3], "push")
            self.assertEqual(command[4:6], ["--remote", "origin"])
            self.assertEqual(
                command[-2:],
                ["--event-file", str(event_file.resolve())],
            )


if __name__ == "__main__":
    unittest.main()
