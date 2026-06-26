---
name: patrol-e2e
description: Use only when the current user request explicitly invokes `$patrol-e2e` or explicitly asks to use the Patrol E2E skill. Provides a constrained Flutter Patrol workflow for setup, harness work, smoke tests, device/simulator execution, Patrol CLI/MCP iteration, and evidence capture while preserving project-level build/run prohibitions outside this explicit skill boundary.
---

# Patrol E2E

## Overview

Use this skill as a narrow exception around Flutter Patrol E2E work. It allows Patrol-specific setup and execution only after the user explicitly invokes `$patrol-e2e`; ordinary Flutter development, unit/widget/route tests, release work, generic QA, and generic device debugging stay under the repository's default AGENTS rules.

For BesideYou Flutter, this skill exists to protect the full testing loop: scope the run, keep release-sensitive flows isolated, use a debug/mock harness first, run the smallest useful Patrol target, and record evidence back into the active goal.

## Activation Gate

Proceed only when the current user message explicitly names `$patrol-e2e`, says to use the Patrol E2E skill, or points to a project AGENTS rule that grants this same explicit exception for the current task. If the user merely asks about Patrol, E2E strategy, testing, Flutter tests, or QA without invoking this skill, discuss or edit docs/code under the normal AGENTS restrictions and do not run Patrol/build/device commands.

This skill does not authorize broad release builds, generic `flutter run`, emulator bootstrapping, device exploration, store packaging, production account flows, payment flows, or media upload/download experiments. Ask for a separate explicit approval when the task needs those surfaces.

## Preflight

Before changing or running anything:

1. Read the nearest `AGENTS.md`, then `SPEC.md` and `TEST.md` for BesideYou Flutter work.
2. Read the active `goals/<date>-*/goal.html` when the user references a goal.
3. If the active goal links a Patrol execution runbook under `goals/*/evidence/`, read it before setup or commands and follow its order, stop conditions, and evidence backfill rules.
4. Confirm current Patrol behavior from official Patrol docs when setup, CLI behavior, supported platforms, MCP, or native configuration matters.
5. In Codex app-only worktrees, run `tool/codex_workspace.sh status`; if dependency, test, or code-generation commands are needed and the wrapper is missing or incomplete, run `tool/codex_workspace.sh repair --skip-pub-get` first.
6. Identify the exact platform, target device/simulator, test target file, flavor/configuration, and mock/staging data boundary before any Patrol run.

## Command Boundary

Allowed after the activation gate and preflight:

- Patrol CLI inspection: `patrol doctor`, `patrol devices`, `patrol --version`, `patrol test --help`.
- Patrol test execution for a named target: `patrol test --target patrol_test/<name>_test.dart` plus narrowly necessary Patrol flags such as `--device`, `--flavor`, `--tags`, `--exclude-tags`, `--dart-define`, `--build-name`, or `--build-number`.
- Patrol development loop: `patrol develop` only when the user is explicitly working on Patrol MCP or live Patrol iteration.
- Patrol setup edits: `pubspec.yaml` Patrol section, `dev_dependencies`, `.gitignore` for generated `patrol_test/test_bundle.dart`, `patrol_test/` sources, Android/iOS native Patrol setup, and app-owned debug/mock bootstrap code.
- Dependency commands that do not build or run the app, such as adding the Patrol dev dependency or refreshing package resolution, only when needed for the requested Patrol setup.

Still forbidden unless the user gives a separate explicit instruction:

- Generic `flutter build`, `flutter run`, `./gradlew build`, direct `xcodebuild`, release packaging, store submission, or broad native build commands outside Patrol's own CLI.
- Booting, creating, wiping, or operating emulators/simulators/devices outside the specific Patrol command being run.
- Running all Patrol tests by default when a single smoke target would answer the question.
- Production login, real payment, real account deletion, real photo/video upload, or mutable backend-state flows without a written test data plan.
- Silent installation of global tools. If `patrol_cli`, Android SDK, Xcode tooling, or device dependencies are missing, report the gap and ask before installing or changing global state.

## Workflow

1. Classify the task as docs planning, setup, harness, smoke test, failure diagnosis, CI, iOS expansion, or Patrol MCP.
2. When a goal-specific execution runbook exists, use it as the concrete step order instead of improvising a broader setup path.
3. Keep the first implementation path Android-first unless the user explicitly chooses another platform.
4. Prefer BesideYou's debug/mock scenario seams and `BesideYouApp` dependency injection over production accounts, payments, real backend state, or release entry points.
5. Start with a single smoke test that proves the app can launch through the Patrol harness to a stable page. Add broader flows only after that evidence is recorded.
6. Use stable keys for Patrol-visible UI anchors. Reuse existing app keys when they are product-stable; introduce a single app-owned key source only when Patrol needs new anchors.
7. Send a short user update before running any Patrol command that builds, installs, or touches a device.
8. Capture the exact command, target platform/device, result summary, report/log path, and any manual follow-up needed.
9. When the active goal provides a validation record template under `goals/*/evidence/`, fill or append to that template before summarizing the result.
10. Update the active goal's `goal.html` with current conclusions, validation evidence, and open problems. Put long logs or stage notes under `evidence/` only as attachments, with a one-line authoritative summary in `goal.html`.

## BesideYou Defaults

- Treat the app as pre-first-release but store-review-sensitive: protect account, privacy, payment, media, permissions, package identity, and reviewer paths.
- Keep production startup behavior in `lib/main.dart` unless the user explicitly changes that contract.
- Use local/debug entries and mock scenario composition for Patrol harnesses when practical.
- Do not let Patrol tests replace existing focused unit/widget/route tests; use Patrol only for native/device/E2E boundaries.
- Record real-device validation expectations in the goal instead of claiming Codex proved runtime behavior when no device run occurred.

## Failure Handling

Stop at the first meaningful Patrol setup or runtime failure, preserve the relevant output, and classify the failure as environment, dependency, native setup, harness bootstrap, app logic, test flake, or device-specific behavior. Do not paper over failures by widening the command scope or switching to production flows. Update the active goal/problem record when the failure affects the adoption workflow.
