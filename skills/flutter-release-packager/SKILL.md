---
name: flutter-release-packager
description: Guide Flutter release packaging for Android and iOS artifacts with preflight checks, parameter confirmation, build execution boundaries, and release evidence collection. Use when preparing, running, or auditing APK, AAB, IPA, internal distribution, TestFlight, App Store, Google Play, signing, versioning, environment-file, artifact-manifest, or project-owned release-console workflows.
---

# Flutter Release Packager

## Purpose

Use this skill to package Flutter apps through a documented project release path instead of ad hoc manual choices. The agent must discover the project rules, collect release intent, explain risky parameters, run preflight checks, and only then launch the build.

## Required Reads

Before packaging, read the nearest `AGENTS.md`, then `SPEC.md`, `PACKAGING.md`, `TEST.md`, `LOCAL.md`, or a release goal/runbook when they exist. Treat `PACKAGING.md` as the human-readable packaging source of truth.

## Reference Routing

Read `references/release-agent-contract.md` when `PACKAGING.md` links a release agent contract, when creating one for repeatable AI-assisted release packaging, or when interpreting a contract-backed release console; after reading, identify the contract fields that define allowed targets, required parameters, command/status endpoints, upload semantics, secret redaction, and evidence labels before asking for packaging parameters or running helper scripts.

## Authorization And Execution Boundaries

Use explicit authorization already provided in the conversation for the same
action and parameters. Build, upload, record, and remote tag push are distinct
actions, but a user can authorize several in one request. Ask only for missing
authorization or a material change of target, inputs, or external effect.
Helper confirmation flags attest that authorization exists; they do not require
an additional conversational round. Skill invocation alone does not authorize
an unspecified upload or remote push.

## Hard Rules

- Do not run a build until the target, version source, worktree policy, signing/export posture, environment inputs, upload behavior, and expected evidence have been confirmed.
- Treat store upload, production deployment, account mutation, or third-party service submission as external-state mutation. Require explicit authorization for that action; reuse it when already provided.
- Do not invent signing credentials, profiles, bundle identifiers, package names, or environment values.
- Do not paste secret values, private key paths, tokens, passwords, or full signing credential paths into the final answer.
- The helper enforces the project contract's dirty-worktree policy, including `block` and the store side of `block-store-release`. If it blocks the requested build, report the concrete prerequisite. Do not bypass the helper, clean user work, or alter the contract merely to proceed; an explicit request to revise project policy is a separate scoped change.
- Prefer the project-owned `PACKAGING.md` plus release agent contract over manual UI interaction.
- If `PACKAGING.md` is missing or does not identify a reliable release path, stop before building and report the missing project contract instead of improvising a store package.

## Workflow

1. Locate the Flutter project root.
   - Prefer the directory containing the app `pubspec.yaml`.
   - Confirm app roots such as `android/`, `ios/`, `macos/`, `web/`, or platform-specific release tooling before choosing targets.
   - In monorepos, distinguish the workspace root from the app/package root.

2. Discover status without mutating release state.
   - Read `PACKAGING.md` and any release agent contract linked from it.
   - Report project root, branch, commit, version source, dirty status, available targets, required input files, and known build/output directories.
   - If the contract defines a release-console status endpoint, prefer `scripts/release_console_client.py status` over hand-written discovery.

3. Resolve required parameters from the request and project facts; ask only for material missing values.
   - Target: Android APK, Android AAB, iOS IPA, internal QA, Play testing, Play production, ad hoc iOS, TestFlight, or App Store.
   - Purpose/audience: local QA, internal testing, closed testing, production update, store upload, or artifact-only handoff.
   - Version: confirm the documented source, usually `pubspec.yaml` `version:`, CI build number, or a project release file.
   - Worktree: if dirty, list `git status --short` entries. Stop when the project policy blocks it; only `warn` or `allow` may continue.
   - Runtime environment: release env file, API base URL posture, feature flags, analytics, crash reporting, diagnostics, or flavor values that the project explicitly documents.
   - Signing/export: keystore, provisioning profile, export method, signing mode, keychain requirements, or CI signing setup as documented by the project.
   - Upload behavior: whether to upload after build, whether to wait for remote processing, and whether this mutates external state.
   - Artifact destination and validation expectation: local artifact only, install/run validation, store upload, or handoff summary.

4. Explain the final summary before build.
   Include target, purpose, version source/value, source branch/ref when present plus commit, dirty decision plus dirty files, required input files, env posture, signing/export settings, upload setting, artifact destination, and expected evidence. Proceed when those actions and parameters are already authorized; otherwise ask for the missing build or upload authorization.

5. Launch the build through the documented path.
   - Use the project release command, CI workflow, or `scripts/release_console_client.py build` exactly as documented.
   - Pass only confirmed parameters.
   - Preserve the project's versioning policy; do not add ad hoc build-name/build-number overrides unless the docs explicitly require them.
   - Redact secrets from logs and summaries.

6. Watch the build to completion.
   If it fails, report the failing command section, exit code, nearest actionable missing prerequisite, and any evidence paths already produced. If it succeeds, prefer manifest-backed evidence over remembered parameters.

7. Close the local package record when the project defines `releaseRecords`.
   - Summarize the target, version, Git identity, artifact, manifest, symbols, upload state, and generated record draft.
   - When `releaseRecords.autoRecordAfterBuildSuccess=true`, the confirmed build authorizes the helper to run the project-owned tag and append commands automatically after the full requested job succeeds. Do not ask for a routine second confirmation. A failed build, failed requested upload, missing evidence, or invalid draft must not record or tag the package.
   - When automatic closure is absent or false, prepare the draft for review and run the recovery `record` command only when record authorization has been provided.
   - When the project requires remote tags, explicit remote tag push authorization permits `push-tag`, including authorization already supplied in the request. Never infer push permission from build, record, Store upload, or deployment confirmation.
   - Report Store upload and any remaining external/device validation separately.

## Release Agent Contract

When a Flutter project needs repeatable AI-assisted release packaging, create a project-owned release agent contract instead of hardcoding project details into this skill. Use `assets/templates/release-agent-contract.json` as a starting point after reading the reference contract. Link the contract from `PACKAGING.md`.

The current template is schema version 2. The helper continues to read legacy
version 1 contracts without requiring the newer Git identity, release-record,
target-command, or grouped-evidence fields; do not treat that compatibility as
proof that an older project provides the stronger version 2 guarantees.

Recommended project-owned path:

```text
tool/release_console/agent-contract.json
```

The contract may describe targets, status commands, required files, allowed options, forbidden options, environment prefixes, secret keys, build commands, upload semantics, and evidence patterns. The contract belongs to the app repository because package identities, signing rules, environment names, and release scripts are project facts.

## Helper Script

Use the generic helper only when `PACKAGING.md` points to a release agent contract with a `releaseConsole` section.

Status-only:

```bash
python3 /path/to/flutter-release-packager/scripts/release_console_client.py status \
  --project /path/to/flutter-app
```

Build after confirmation:

```bash
python3 /path/to/flutter-release-packager/scripts/release_console_client.py build \
  --project /path/to/flutter-app \
  --target android-release-aab \
  --option analyticsEnabled=false \
  --option crashlyticsEnabled=true \
  --confirm-build
```

Add `--confirm-upload` only when the upload is explicitly authorized. The helper reads project facts from the contract, starts the project release console, calls the documented endpoints, redacts configured secrets, streams job logs, and prints evidence labels configured by the project.

For recovery of an earlier valid draft, or for a project that does not enable
automatic record closure:

```bash
python3 /path/to/flutter-release-packager/scripts/release_console_client.py record \
  --project /path/to/flutter-app \
  --event-file /path/to/release-record.json \
  --confirm-record
```

When the project requires the package tag on its approved remote, use existing
explicit remote-push authorization or request it if missing:

```bash
python3 /path/to/flutter-release-packager/scripts/release_console_client.py push-tag \
  --project /path/to/flutter-app \
  --event-file /path/to/release-record.json \
  --confirm-push
```
