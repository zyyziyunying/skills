# [Project Name] LOCAL

Date: [YYYY-MM-DD]
Status: current local setup and run fact source
Scope: `[project/path]`

This document owns local setup, debug, and machine-local conventions.

## Local Setup

[Describe how to open/configure the project locally.]

## Human-Only Commands

[List build/run/device commands humans may run.]

## Codex Boundary

Default allowed:

- Static reading and code/doc edits.
- `dart analyze` / `flutter analyze`.
- Targeted `dart test` / `flutter test test/...`.

Conditionally allowed when `AGENTS.md`, `TEST.md`, this document, or the
current user request explicitly allows the exact command:

- `flutter test integration_test`.
- `flutter run -d web-server`.
- Hot reload.
- Screenshot or preview checks.

Requires separate confirmation:

- Real device or simulator install/run.
- `flutter build`, release/package work, signing, or store upload.
- Store/account/payment flows.
- Mutable backend-state flows.

## Debug Configuration

[Describe local/debug entries, defines, env files, fake-data boundaries, and ignored local files.]

## Secrets and Local Files

[List ignored secrets and machine-local files.]

## Related Fact Sources

[Link SPEC, TEST, GENERATION, PACKAGING.]
