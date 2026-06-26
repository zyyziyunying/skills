---
name: flutter-release-packager
description: Guide Flutter release packaging for Android and iOS artifacts with preflight checks, parameter confirmation, build execution boundaries, and release evidence collection. Use when preparing, running, or auditing APK, AAB, IPA, internal distribution, TestFlight, App Store, Google Play, signing, versioning, environment-file, artifact-manifest, or project-owned release-console workflows.
---

# Flutter Release Packager

## Purpose

Use this skill to package Flutter apps through a documented project release path instead of ad hoc manual choices. The agent must discover the project rules, collect release intent, explain risky parameters, run preflight checks, and only then launch the build.

## Required Reads

Before packaging, read the nearest `AGENTS.md`, then `SPEC.md`, `PACKAGING.md`, `TEST.md`, `LOCAL.md`, or a release goal/runbook when they exist. Treat `PACKAGING.md` as the human-readable packaging source of truth. If `PACKAGING.md` links a release agent contract, read it and `references/release-agent-contract.md` before asking for packaging parameters.

## Hard Rules

- Do not run a build until the target, version source, worktree policy, signing/export posture, environment inputs, upload behavior, and expected evidence have been confirmed.
- Treat store upload, production deployment, account mutation, or third-party service submission as external-state mutation. Require a separate explicit confirmation for that step.
- Do not invent signing credentials, profiles, bundle identifiers, package names, or environment values.
- Do not paste secret values, private key paths, tokens, passwords, or full signing credential paths into the final answer.
- For external, production, or store-facing releases, block on unexpected dirty worktrees unless the user explicitly accepts the dirty state and the final summary calls it out.
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

3. Ask for required parameters.
   - Target: Android APK, Android AAB, iOS IPA, internal QA, Play testing, Play production, ad hoc iOS, TestFlight, or App Store.
   - Purpose/audience: local QA, internal testing, closed testing, production update, store upload, or artifact-only handoff.
   - Version: confirm the documented source, usually `pubspec.yaml` `version:`, CI build number, or a project release file.
   - Worktree: if dirty, list `git status --short` entries and ask whether to stop or continue with the dirty state.
   - Runtime environment: release env file, API base URL posture, feature flags, analytics, crash reporting, diagnostics, or flavor values that the project explicitly documents.
   - Signing/export: keystore, provisioning profile, export method, signing mode, keychain requirements, or CI signing setup as documented by the project.
   - Upload behavior: whether to upload after build, whether to wait for remote processing, and whether this mutates external state.
   - Artifact destination and validation expectation: local artifact only, install/run validation, store upload, or handoff summary.

4. Explain the final summary before build.
   Include target, purpose, version source/value, branch/commit, dirty decision plus dirty files, required input files, env posture, signing/export settings, upload setting, artifact destination, and expected evidence. Ask for a clear build confirmation. Ask separately for external upload confirmation when applicable.

5. Launch the build through the documented path.
   - Use the project release command, CI workflow, or `scripts/release_console_client.py build` exactly as documented.
   - Pass only confirmed parameters.
   - Preserve the project's versioning policy; do not add ad hoc build-name/build-number overrides unless the docs explicitly require them.
   - Redact secrets from logs and summaries.

6. Watch the build to completion.
   If it fails, report the failing command section, exit code, nearest actionable missing prerequisite, and any evidence paths already produced. If it succeeds, prefer manifest-backed evidence over remembered parameters.

7. Close with release evidence.
   Summarize the target, version, git commit, dirty status, artifact path, manifest path, symbols/dSYM/mapping path when present, upload status, and follow-up validation that remains outside local packaging.

## Release Agent Contract

When a Flutter project needs repeatable AI-assisted release packaging, create a project-owned release agent contract instead of hardcoding project details into this skill. Read `references/release-agent-contract.md` for the field model and copy `assets/templates/release-agent-contract.json` as a starting point. Link the contract from `PACKAGING.md`.

Recommended project-owned path:

```text
tool/release_console/agent-contract.json
```

The contract may describe targets, status commands, required files, allowed options, forbidden options, environment prefixes, secret keys, build commands, upload semantics, and evidence patterns. The contract belongs to the app repository because package identities, signing rules, environment names, and release scripts are project facts.

## Helper Script

Use the generic helper only when `PACKAGING.md` points to a release agent contract with a `releaseConsole` section.

Status-only:

```bash
python3 ~/.codex/skills/flutter-release-packager/scripts/release_console_client.py status \
  --project /path/to/flutter-app
```

Build after confirmation:

```bash
python3 ~/.codex/skills/flutter-release-packager/scripts/release_console_client.py build \
  --project /path/to/flutter-app \
  --target android-release-aab \
  --option analyticsEnabled=false \
  --option crashlyticsEnabled=true \
  --confirm-build
```

Add `--allow-dirty` only after the user accepts the dirty state. Add `--confirm-upload` only after separate upload confirmation. The helper reads project facts from the contract, starts the project release console, calls the documented endpoints, redacts configured secrets, streams job logs, and prints evidence labels configured by the project.
