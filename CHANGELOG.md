# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

### Breaking Changes

- Removed `flutter-build-responsive-layout` as an independent skill.
  - Affected behavior: `skills/flutter-build-responsive-layout` is no longer an installable skill path, `$flutter-build-responsive-layout` is no longer a valid explicit skill invocation, and Flutter responsive/adaptive layout tasks now resolve through `flutter-best-layout`.
  - Affected callers: user prompts, local discovery links, scripts, docs, or install commands that reference `flutter-build-responsive-layout`.
  - Migration: replace install paths with `skills/flutter-best-layout`, replace explicit invocations with `$flutter-best-layout`, and update any local links with `./scripts/link-local-skills.sh`.
  - Validation/docs: README now lists `flutter-best-layout` as the layout entrypoint. Verify discovery with `npx skills add ./skills --list --full-depth` after updating local links.
- Changed `manage-goal-docs` new-goal output from self-contained inline CSS to shared workspace CSS.
  - Affected behavior: newly created `goal.html` files link to `../_shared/goal.css`; the script creates `goals/_shared/goal.css` from the bundled `skills/manage-goal-docs/assets/goal.css` asset when missing.
  - Affected callers: workflows that copy, archive, share, or render only the generated `goal.html`, and skill publishing or installation flows that copy only `SKILL.md` and `scripts/`.
  - Migration: keep `goals/_shared/goal.css` with moved or shared goals and preserve the relative path; include `skills/manage-goal-docs/assets/goal.css` when publishing or installing the skill. Use `--json` when callers need exact supporting-file creation metadata.
  - Validation/docs: `manage-goal-docs` now documents workspace-local shared CSS, legacy inline-style goals, self-contained snapshots, and copy-once CSS updates.

### Changed

- Expanded `flutter-best-layout` to cover responsive/adaptive layout decisions, constraint reasoning, breakpoint policy, fixed design canvas adaptation, screen/window sizing, and orientation-sensitive layout review.
- Added `flutter-best-layout/references/responsive-layout.md` for reusable layout judgment, including `MediaQuery.sizeOf`, `paddingOf`, `viewInsetsOf`, `LayoutBuilder` boundaries, surface classification, anti-patterns, review/refactor checklists, and rules against magic `600px`/`840px` breakpoints.
