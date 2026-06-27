# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

### Breaking Changes

- Removed `flutter-build-responsive-layout` as an independent skill.
  - Affected behavior: `skills/flutter-build-responsive-layout` is no longer an installable skill path, `$flutter-build-responsive-layout` is no longer a valid explicit skill invocation, and Flutter responsive/adaptive layout tasks now resolve through `flutter-best-layout`.
  - Affected callers: user prompts, local discovery links, scripts, docs, or install commands that reference `flutter-build-responsive-layout`.
  - Migration: replace install paths with `skills/flutter-best-layout`, replace explicit invocations with `$flutter-best-layout`, and update any local links with `./scripts/link-local-skills.sh`.
  - Validation/docs: README now lists `flutter-best-layout` as the layout entrypoint. Verify discovery with `npx skills add ./skills --list --full-depth` after updating local links.

### Changed

- Expanded `flutter-best-layout` to cover responsive/adaptive layout decisions, constraint reasoning, breakpoint policy, screen/window sizing, and orientation-sensitive layout review.
- Moved reusable responsive layout guidance into `flutter-best-layout` references, including `MediaQuery.sizeOf`, `LayoutBuilder` boundaries, `ConstrainedBox`, grid max extents, and rules against default `600px` breakpoints.
