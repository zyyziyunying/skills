# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

### Added

- Added `flutter-app-size` for Flutter release artifact measurement, DevTools App Size Tool analysis, size diff evidence, split debug info, obfuscation, asset/package reduction, and iOS App Thinning guidance.
- Added `humanizer` as a manual-only English prose skill for removing common AI-writing tells while preserving meaning and voice.
- Added `independent-verifier` as the single entry for focused review, bug-value
  triage, test design, and test verification, preferring fresh-context
  delegation when it adds value.

### Breaking Changes

- Consolidated `independent-review-subagent`, `independent-test-verifier`, and
  `review-bug-value` into `independent-verifier`, and removed
  `expert-agent-team` as a standalone skill.
  - Affected API/behavior: the four removed install paths and explicit
    `$skill-name` invocations no longer exist. `$independent-verifier` selects
    review, bug-value, test-design, or test-verification mode and loads only the
    corresponding reference. It may also activate from natural-language requests
    for independent review, bug-value triage, or independent test verification;
    these requests may now use a verifier subagent when that adds value. General
    worker delegation uses native runtime capabilities rather than a skill wrapper.
  - Affected callers: prompts, local discovery links, docs, goal workflows, or
    automation that invoke any removed skill; callers that expected ordinary
    multi-agent execution to load `expert-agent-team`; prompt tests or cost
    assumptions that treated non-`$skill` review requests as direct-only.
  - Migration: replace independent component invocations with
    `$independent-verifier` and state the desired mode or bounded outcome. Let
    `$goal-first-development` route modes for goal-owned delivery. Request
    bounded subagents directly when parallel execution is needed. Use an explicit
    direct-review instruction when a verifier subagent is not desired.
  - Validation/docs: README, `goal-first-development`, skill metadata, and
    reference routing use the consolidated name. Validate explicit and implicit
    triggers, direct fallback labeling, changed skill folders, internal links,
    stale active references, and refreshed local discovery links.
- Simplified the `$goal-first-development` validation contract.
  - Affected API/behavior: L1/L2/L3 are now risk guides rather than fixed
    pipelines. L2 no longer automatically requires an independent check, and L3
    no longer automatically requires every independent test, final-review, and
    external-evidence mode. The goal's material risks, project rules, confirmed
    contract, and best available evidence determine the checks. A missing fresh
    verifier may fall back to a clearly labeled direct check.
  - Affected callers: active or generated goal Check sections that encode the
    former three-gate L2 requirement, and workflows that use a fixed component
    sequence rather than risk-matched verification.
  - Migration: keep stricter project-specific gates when authoritative;
    otherwise replace fixed mode lists with the evidence actually needed for the
    goal. Label direct verification honestly and preserve any external evidence
    that the confirmed acceptance contract still requires.
  - Validation/docs: forward-test L1 mechanical work, L2 behavior and structural
    changes, unresolved bug claims, and L3 high-risk work; verify that the flow
    neither invents evidence nor blocks solely because a verifier is unavailable.

- Changed `manage-goal-docs` from a single-file truth-source contract to a
  one-owner-per-fact model rooted at `goal.html`.
  - Affected API/behavior: `goal.html` now owns the goal-level overview and
    document routing, while semantic Markdown or HTML documents may own detailed
    research, design, checks, plans, problems, or evidence. The creation template
    no longer requires those concerns as fixed sections. `create_goal.py` also
    accepts a concise outcome instead of enforcing one sentence and accepts any
    lowercase kebab-case slug up to 80 characters instead of requiring 3 to 8
    words.
  - Affected callers: `$goal-first-development`, prompts or tooling that read
    only `goal.html`, and existing workflows that duplicate all mutable current
    facts into the overview.
  - Migration: keep existing single-file goals when they remain clear. For split
    goals, link every scoped owner from `goal.html`, state its ownership area,
    update the owning document first, and teach callers to follow those links
    before applying completeness, validation, or closure gates.
  - Validation/docs: `goal-first-development`, README, skill metadata, and the
    generated template now use the same ownership model. Validate frontmatter,
    create a goal through the bundled script, and verify that goal-level status
    remains in `goal.html` while detailed facts are not duplicated.
- Simplified `flutter-best-layout` from a prescriptive layout-delivery workflow
  into high-freedom widget-pattern and flexible-constraint guidance.
  - Affected API/behavior: invoking `$flutter-best-layout` no longer requires a
    Context Receipt, fixed compact/medium/wide matrix, broad reference loading,
    or automatic `LAYOUT-PREVIEW.md` creation. The public
    `references/layout-context-roadmap.md` and
    `references/layout-pitfalls.md` paths are removed. The retained
    `references/preview-workflow.md` is a smaller compatibility contract loaded
    only for app-style preview work.
  - Affected callers: prompts, project layout entries, documentation, or direct
    links that relied on those removed references or on the skill to enforce the
    former delivery gates.
  - Migration: keep project-specific required reading, design facts, device
    matrices, validation boundaries, and documentation requirements in the
    project's own `AGENTS.md`, `TEST.md`, `DESIGN.md`, owner documentation, or
    equivalent facts. Link to `layout-patterns.md` for component composition,
    `responsive-layout.md` for constraint reasoning, and `preview-workflow.md`
    only when preview reachability or lifecycle guidance is needed.
  - Validation/docs: README and skill metadata now describe the smaller scope.
    The core skill retains concise high-loss guidance for project facts, parent
    constraints, scroll ownership, semantic controls, and evidence boundaries;
    references retain bounded-axis, fixed-format, responsive, and preview
    details. Validate frontmatter, internal links, and known project preview
    consumers when updating the skill.
- Hardened `flutter-release-packager` contract validation to reject malformed
  release inputs before status or build execution.
  - Affected API/behavior: `requiredFiles` and `requiredEnvFiles`, when present,
    must be string arrays; `evidence.requiredForSuccess`, when present, must be
    boolean; and `releaseConsole.startupUrlPattern` must be a valid string
    regular expression with at least one capture group. At runtime, its first
    group must capture a non-empty absolute `http://` or `https://` URL with a
    network location. Invalid contracts or startup captures that were
    previously accepted now fail before a release-console endpoint request.
  - Affected callers: project-owned release agent contracts consumed by
    `scripts/release_console_client.py`, especially custom contracts that used
    string values in place of arrays or booleans, or a startup URL pattern
    without a capture group.
  - Migration: convert required-file fields to string arrays, convert
    `requiredForSuccess` to a JSON boolean, capture the complete absolute
    `http(s)` startup URL in the first regex group, and use non-capturing groups
    for other regex structure. Relative and non-HTTP captured URLs are no longer
    accepted. The bundled template and current BesideYou contract already
    satisfy the stricter validation.
  - Validation/docs: focused contract tests now cover valid defaults, malformed
    schema shapes, wrong first-group values, and unmatched optional first
    groups; keep project `PACKAGING.md` and contract fixtures synchronized when
    the schema changes.
- Changed `scripts/link-local-skills.sh` to reject local and Codex skill roots
  that resolve to the same physical directory.
  - Affected API/behavior: equal roots, including aliases such as `/path/x` and
    `/path/x/.`, now exit nonzero before managed links are removed or created;
    the previous behavior exited successfully while producing self-referential
    links.
  - Affected callers: local setup commands whose configured roots resolve to
    the same physical directory, whether through defaults, one or both
    environment overrides, path aliases, or directory symlinks.
  - Migration: configure two distinct directories so Codex links through the
    local agent skill root as documented in `README.md`.
  - Validation/docs: the link-script regression test covers aliased equal roots,
    preservation before rejection, and the healthy two-level link path.
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

- Refactored `flutter-implement-json-serialization` around a project-Harness
  decision gate for generated, hybrid, or manual mapping; generator adoption
  now includes dependency, command, output, freshness, compatibility, and
  focused-test policy. The skill is now project-agnostic: project transport,
  validation, error, generated-file, and compatibility rules remain in each
  repository's Harness, while the reusable skill owns strategy and
  semantic-parity guidance.
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
- Defined `independent-verifier` no-context forking through current-runtime
  equivalents such as `fork_turns: "none"` or `fork_context: false`.

### Fixed

- Replaced the author-machine command in `manage-goal-docs` with an
  installer-independent `<skill-dir>` invocation resolved from the active
  `SKILL.md` path.
- Normalized `humanizer` frontmatter by moving its version into `metadata` and
  expressing `allowed-tools` as the space-separated string required by the
  Agent Skills specification, while removing the redundant `any-agent`
  compatibility declaration.
