# Changelog

All notable changes to this repository will be documented in this file.

## Unreleased

### Changed

- Simplified goal/project documentation routing: global or long-lived records
  use project documentation; short-lived task context stays with the goal.

### Added

- Added `session-work-report` for concise, evidence-backed session recaps,
  completion reports, and handoffs, with Mermaid or tabular visuals selected
  only when they materially improve understanding.
- Added `flutter-app-size` for Flutter release artifact measurement, DevTools App Size Tool analysis, size diff evidence, split debug info, obfuscation, asset/package reduction, and iOS App Thinning guidance.
- Added `humanizer` as a manual-only English prose skill for removing common AI-writing tells while preserving meaning and voice.
- Added `independent-verifier` as the single entry for focused review, bug-value
  triage, test design, and test verification, preferring fresh-context
  delegation when it adds value.
- Added a repo-managed `r8-analyzer` that uses current HTML Configuration
  Analyzer outputs, preserves read-only and build-authorization boundaries, and
  falls back to an explicitly heuristic audit instead of requiring missing
  protobuf conversion scripts.

### Breaking Changes

- Merged `manage-goal-docs` into `goal-first-development` and removed the
  standalone `$manage-goal-docs` entry.
  - Affected API/behavior: `skills/manage-goal-docs`, its helper path, and the
    `$manage-goal-docs` invocation no longer exist. Goal creation and updates
    now belong to `$goal-first-development`.
  - Affected callers: prompts, automation, local discovery links, or scripts
    that invoke the removed skill or its former `create_goal.py` path.
  - Migration: invoke `$goal-first-development`; direct helper callers should
    use `skills/goal-first-development/scripts/create_goal.py` instead.
  - Validation/docs: README lists only the consolidated workflow. Refresh local
    discovery links with `./scripts/link-local-skills.sh`.
- Removed `patrol-e2e` as an installable skill.
  - Affected API/behavior: `skills/patrol-e2e` and the explicit
    `$patrol-e2e` invocation no longer exist.
  - Affected callers: prompts, local discovery links, docs, or automation that
    reference the removed skill.
  - Migration: use the target project's current testing instructions and obtain
    the required explicit authority before running Patrol or device commands.
  - Validation/docs: README no longer lists the skill. Refresh local discovery
    links with `./scripts/link-local-skills.sh` to remove managed stale links.
- Corrected explicit-file `local-image-to-webp --output-mode subdir` placement
  and made generated output subtrees symlink-safe.
  - Affected API/behavior: an explicit file now produces
    `<parent>/webp/<stem>.webp`; the previous implementation ignored `subdir`
    for files and produced `<parent>/<stem>.webp`. Existing symlinks or
    non-directory components inside the generated `webp` output subtree are
    rejected before conversion instead of being followed. Existing output files
    with multiple hard links are also rejected before conversion.
  - Affected callers: automation that consumes the former same-directory path
    despite selecting `subdir`, and local setups that intentionally point a
    generated `webp` directory or one of its descendants through a symlink, or
    intentionally reuse an output inode through hard links.
  - Migration: use `same-dir` to retain same-directory placement, otherwise
    consume the new `webp` path. Replace a symlinked generated output subtree
    with a real directory before using `subdir`; preserve or relocate its
    existing contents first when needed. Replace a hard-linked output pathname
    with an independent regular file, or remove it so the converter can create
    one.
  - Validation/docs: focused tests cover explicit-file placement, lexical file
    symlinks, output-subtree rejection before writes, collision preflight,
    single-output hard-link rejection, mixed-success batch reporting, and
    `same-dir` file-symlink compatibility. Keep the skill's output-mode contract
    in sync with these paths.
- Replaced the externally installed, incomplete `r8-analyzer` workflow with the
  repo-managed HTML-first analyzer contract.
  - Affected API/behavior: `$r8-analyzer` no longer requires
    `convert_pb_to_json.py`, `analyze.py`, `tmp/keepradius`, or a strict
    report-only response. It prefers existing HTML or release evidence, uses the
    current AGP standalone HTML task only when that Gradle command is authorized,
    and labels unsupported analysis as heuristic.
  - Affected callers: prompts or automation that expected protobuf/JSON
    intermediates, parsed the former fixed report shape, automatically upgraded
    AGP/R8, or assumed invoking the skill authorized a release build.
  - Migration: consume the variant's Configuration Analyzer HTML report, pass
    explicit authority for any Gradle build, and use `flutter-app-size` when the
    primary outcome is artifact or download-size measurement. Before refreshing
    local discovery, inspect `r8-analyzer` entries under `~/.agents/skills` and
    `~/.codex/skills`. Move any existing non-symlink installation to a
    recoverable backup outside both discovery roots, then run
    `./scripts/link-local-skills.sh`; the linker intentionally refuses to
    overwrite non-symlink directories.
  - Validation/docs: validate frontmatter, README discovery, current official
    analyzer paths, local symlink refresh, and both quantitative-versus-heuristic
    reporting boundaries.
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
- Tightened schema version and release-record lifecycle behavior for
  `flutter-release-packager` contracts.
  - Affected API/behavior: `schemaVersion` must be a literal JSON integer `1`
    or `2`. When a schema version 2 contract includes `gitIdentity`, it must be
    an object and must define boolean `requiresNamedBranch`. Contracts with
    `releaseRecords` continue to require that object; explicit
    `releaseRecords: null` and non-boolean helper-consumed Git-identity flags
    are rejected. A generic record helper may invoke `tagCommand` for a tagless
    draft, so the project-owned command must succeed without creating a tag in
    that case. Record completion output now states the separate push boundary
    without claiming unread remote state.
    The BesideYou project command retains `Created package tag:` for new tags
    and reports `Verified existing package tag:` on idempotent reruns.
  - Affected callers: project-owned schema version 2 contracts and release
    record commands consumed by `scripts/release_console_client.py`, especially
    contracts that previously used a malformed non-object `gitIdentity`,
    omitted the branch-policy boolean, rejected a valid tagless draft, or parsed
    the former remote-push status sentence or assumed every successful tag
    command reported a newly created tag.
  - Migration: set `requiresNamedBranch` to `true` and provide each target's
    `branchTemplate` when a named source branch is mandatory; set it to `false`
    for detached-HEAD-compatible flows. Keep `schemaVersion` as a literal JSON
    integer `1` or `2`, rather than a boolean, float, or numeric string. If
    release records are unused, omit the key instead of assigning `null`; use
    literal JSON booleans for every Git-identity flag. If release records support
    a tagless line, make its `tagCommand` a successful no-op for those events
    while retaining normal tag creation for tagged lines. Treat the helper's
    completion text as guidance rather than remote state; use the separately
    confirmed push flow to query or mutate that state.
    Treat project tag-command exit status as the success contract, or accept
    both the created and verified success messages.
  - Validation/docs: contract tests cover literal-integer schema versions,
    omitted and malformed identities, null record configuration, runtime flag
    types, neutral push-boundary output, and the tag-before-append helper flow;
    the project regression covers tagless commands and repeated tagged-command
    readiness.
    Release-agent contract guidance documents the schema and optional-object
    boundaries.
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

- Kept `humanizer` rewrites faithful to the input by prohibiting invented facts,
  details, sources, experiences, and stance changes, and replaced the Lisbon
  and Haolai River examples that previously violated that contract.
- Separated bug validity and confidence from P0-P3 impact in
  `independent-verifier`, so stale evidence, theoretical reachability,
  frequency, blast radius, and workarounds affect the correct dimension.
- Removed the conflicting command contract from `git-commit-helper`: Git
  mutations remain narrowly allowlisted, project checks inherit existing task
  authority, and commit messages use literal, non-expanding input without `cat`
  or command substitution.
- Made `playwright-interactive` probe dependencies read-only and prefer an
  authorized temporary harness instead of modifying the target workspace's
  package files by default.
- Extended `local-image-to-webp` to accept multiple explicit files, honor
  per-file `webp` subdirectories, preflight output collisions and aliases,
  reject unsafe generated output subtrees before writing, and continue later
  inputs after a per-file output or conversion failure.
- Canonicalized local skill roots, preflighted all destination conflicts before
  mutation, and removed stale managed links whose source directory no longer
  contains `SKILL.md` while preserving valid unmanaged and alias links.
- Replaced the author-machine command in `manage-goal-docs` with an
  installer-independent `<skill-dir>` invocation resolved from the active
  `SKILL.md` path.
- Normalized `humanizer` frontmatter by moving its version into `metadata` and
  expressing `allowed-tools` as the space-separated string required by the
  Agent Skills specification, while removing the redundant `any-agent`
  compatibility declaration.
