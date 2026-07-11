# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

### Added

- Added `flutter-app-size` for Flutter release artifact measurement, DevTools App Size Tool analysis, size diff evidence, split debug info, obfuscation, asset/package reduction, and iOS App Thinning guidance.
- Added `humanizer` as a manual-only English prose skill for removing common AI-writing tells while preserving meaning and voice.
- Added `independent-test-verifier` for no-context test-charter design and
  test-only verification derived from active goals and authoritative behavior
  sources rather than the current implementation.

### Breaking Changes

- Renamed and generalized `flutter-project-harness` as
  `codex-project-harness`.
  - Affected API/behavior: the install path and explicit invocation are now
    `skills/codex-project-harness` and `$codex-project-harness`. The skill now
    supports lightweight, scaled, and hybrid repository knowledge layouts for
    any software project; Flutter command and device guidance is loaded as a
    project-specific reference instead of defining the core workflow.
  - Affected callers: prompts, local discovery links, installation commands,
    docs, or automations that refer to `flutter-project-harness`; repositories
    that assume every generated command boundary contains Flutter commands.
  - Migration: replace the old path and invocation with the new name, refresh
    local discovery links, and keep existing Flutter fact sources. New runs
    detect Flutter projects and apply the preserved Flutter variant guidance.
  - Validation/docs: README and skill metadata use the new name; validate the
    renamed skill, verify repository discovery, and check that existing
    `SPEC.md`, `TEST.md`, `DESIGN.md`, `GENERATION.md`, `LOCAL.md`, and
    `PACKAGING.md` content remains authoritative during refreshes.
- Changed `goal-first-development` from a single-flow implementation helper to
  the canonical owner workflow for risk-based goal delivery.
  - Affected behavior: active goals now require an explicit L1/L2/L3 validation
    level, correctness sources, separate developer and independent checks, and
    decisive evidence appropriate to that level before `done`. L2/L3 work may
    internally delegate to `expert-agent-team`, `independent-test-verifier`,
    `independent-review-subagent`, and `review-bug-value`. Active behavior and
    Check semantics are frozen and cannot be silently weakened by an
    implementation agent.
  - Affected callers: prompts and workflows that expect
    `$goal-first-development` to implement, run developer-authored tests, and
    immediately mark a behavior-changing or high-risk goal done; manual chains
    that always invoke `$expert-agent-team` and independent review as separate
    user-selected phases.
  - Migration: keep invoking `$goal-first-development`, but normally omit the
    manual component sequence. Let the owner workflow classify risk and route
    components. Direct `$expert-agent-team`, `$independent-review-subagent`, and
    test-skill invocations remain available for standalone bounded work.
  - Validation/docs: update existing goal Check sections and project `TEST.md`
    fact sources when they govern active work. Forward-test at least L1
    mechanical work, L2 bug fixes, L3 high-risk changes, ambiguous product
    questions, and missing independent-evidence completion gates.
- Expanded `expert-agent-team`, `independent-review-subagent`, and
  `review-bug-value` activation contracts to allow internal delegation from an
  explicitly activated owner workflow.
  - Affected behavior: these skills are no longer direct-invocation-only when a
    confirmed owner workflow contract requires their execution or validation.
  - Affected callers: policies or prompt tests that assume the component skills
    can never be loaded unless the user repeats their `$skill-name` explicitly.
  - Migration: treat explicit activation of the owner workflow as authorization
    for its documented, bounded internal delegation. Standalone implicit use
    remains disallowed, and each internal skill use must still be announced.
  - Validation/docs: verify delegated agents preserve no-context review,
    explicit write ownership, product-code restrictions for test verifiers, and
    owner-only goal completion.

- Removed `dart-use-pattern-matching` as an independent skill.
  - Affected behavior: `skills/dart-use-pattern-matching` is no longer an installable skill path, and `$dart-use-pattern-matching` is no longer a valid explicit skill invocation.
  - Affected callers: user prompts, local discovery links, docs, scripts, or install commands that reference `dart-use-pattern-matching`.
  - Migration: rely on normal Dart refactoring judgment for switch expressions and patterns, or fold project-specific pattern-matching guidance into the task-specific Dart/Flutter skill that actually needs it.
  - Validation/docs: README no longer lists `dart-use-pattern-matching`. Refresh local discovery links with `./scripts/link-local-skills.sh` if this skill had been linked locally.
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
- Tightened `flutter-best-layout` delivery gates for screenshot/Figma UI restoration, fixed `Stack` overlays, text scale/localization checks, semantic affordances, visual links, and prototype shortcut disclosure.
- Updated `dart-add-unit-test` and `flutter-add-widget-test` to classify failures
  against authoritative behavior sources before editing implementation or
  assertions, prohibit assertion weakening merely to obtain passing tests, and
  record fail-before-fix evidence when safely available.
- Expanded goal and project `TEST.md` templates with correctness sources,
  L1/L2/L3 validation strategy, developer versus independent test ownership,
  and bug-fix evidence.
- Kept generated goal page titles semantically complete instead of truncating
  them, and distinguished pending completion gates from achieved validation
  evidence so final review results cannot be asserted before review occurs.
- Updated `independent-review-subagent` to express no-context forking through
  current-runtime equivalents such as `fork_turns: "none"` rather than relying
  on one obsolete API field name.
