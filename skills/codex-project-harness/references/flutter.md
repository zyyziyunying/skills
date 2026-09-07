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

## Commands and Execution Constraints

Derive commands and execution constraints from the repository and the user's
request. Document relevant analysis, targeted tests, integration/device checks,
generation, local preview, and release workflows only where the project needs
them. Keep their operational details in the owning fact source and link to it.

Do not impose a universal permission tier for Flutter commands. Preserve
applicable project restrictions and existing user authorization; already
authorized steps do not need repeat approval.

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

Source-size thresholds, TODO placement, and generated-file exceptions belong
to applicable user and project rules. Document or enforce those rules without
inventing a threshold or exemption. Source-code markers belong in the applicable
source file, not in Markdown documents.
