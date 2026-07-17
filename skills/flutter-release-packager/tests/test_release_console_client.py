#!/usr/bin/env python3
"""Offline regression tests for release agent contract validation."""

from __future__ import annotations

import copy
import io
import importlib.util
import json
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


if __name__ == "__main__":
    unittest.main()
