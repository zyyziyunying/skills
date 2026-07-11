# Flutter Project Variant

Read this reference only for Flutter or Dart apps, packages, plugins, examples,
and workspaces.

## Project Shape

- A pure Dart package may not need `DESIGN.md` or `PACKAGING.md`.
- A Flutter plugin may need separate fact sources for package, platform code,
  and example app boundaries.
- An example app may inherit package behavior but should own its device and run
  instructions.
- A workspace root should point to subproject fact sources rather than duplicate
  their current details.
- For submodules, keep subproject documentation in the submodule and commit the
  parent pointer change separately.

## Command Tiers

Derive the exact commands from project facts. The usual starting boundary is:

Default lightweight validation:

- Static reading and project-owned code or documentation edits.
- `dart analyze` or `flutter analyze`.
- Targeted `dart test` or `flutter test test/...` when dependencies are present.

Conditional validation only when `AGENTS.md`, `TEST.md`, `LOCAL.md`, another
authoritative project source, or the current user request authorizes it:

- `flutter test integration_test`.
- `flutter run -d web-server`, hot reload, screenshots, or preview checks.
- Documented generators that modify project-owned outputs.

Require separate confirmation unless a more specific project contract already
authorizes the exact action:

- Real-device or simulator install and run.
- `flutter build`, signing, release packaging, or store upload.
- Store, account, payment, or mutable backend-state flows.

## Fact Mapping

- Put stage, supported platforms, compatibility, API, hardware, and release
  assumptions in `SPEC.md` or the applicable product spec.
- Put correctness sources, device matrices, meaningful test scope, independent
  validation policy, bug evidence, and commands in `TEST.md`.
- Put viewport, input, orientation, accessibility, visual, media, and interaction
  decisions in `DESIGN.md` or indexed design docs.
- Put builders, sources, outputs, commit policy, and regeneration commands in
  `GENERATION.md`.
- Put SDK setup, defines, env files, debug entries, secrets, and ignored local
  files in `LOCAL.md`.
- Put application IDs, bundle IDs, versioning, signing, artifacts, release
  channels, rollback, and publishing in `PACKAGING.md`.

If a Dart source file already exceeds or will exceed 2000 lines and the project
uses a shared code-size rule, add its required source-code TODO only to the
source file. Do not put source-size markers in Markdown documents.
