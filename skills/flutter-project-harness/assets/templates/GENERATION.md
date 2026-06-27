# [Project Name] GENERATION

Date: [YYYY-MM-DD]
Status: current generated-file fact source
Scope: `[project/path]`

This document owns generated-file rules for [project].

## Current Generated Content

[List committed generated outputs or state that none exist.]

## Ignored Generated Content

[List ignored build/generated/cache outputs.]

## Generators

For each generator, document:

1. Source files.
2. Generated output paths.
3. Command or IDE action.
4. Whether Codex may run the command.
5. Whether outputs are committed or ignored.
6. Required validation after regeneration.

## Command Boundary

Default allowed:

- Static reading and code/doc edits.
- Generator dry-run or validation commands that do not write outside the
  project, when documented above.
- `dart analyze` / `flutter analyze`.
- Targeted `dart test` / `flutter test test/...`.

Conditionally allowed when `AGENTS.md`, `TEST.md`, `LOCAL.md`, this document,
or the current user request explicitly allows the exact command:

- Documented generator commands that modify project-owned generated outputs.
- `flutter test integration_test`.
- `flutter run -d web-server`.
- Hot reload.
- Screenshot or preview checks.

Requires separate confirmation:

- Real device or simulator install/run.
- `flutter build`, release/package work, signing, or store upload.
- Store/account/payment flows.
- Mutable backend-state flows.

## Change Rules

[State source-first editing, no hand edits to generated outputs, and doc update expectations.]
