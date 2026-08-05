# skills

This repository packages my personal agent skills for installation with `npx skill`.
Most skills are maintained for Flutter project work, with a few supporting workflows for Git, browser automation, screenshots, and project documentation.

The installable tree lives under `skills/<skill-name>/SKILL.md`. In the local setup, `~/.agents/skills/<skill-name>` should be a symlink to this tree, and `~/.codex/skills/<skill-name>` should link through `~/.agents/skills/<skill-name>` so Codex discovers the same managed copy.

Breaking changes and migration notes are tracked in [CHANGELOG.md](CHANGELOG.md).

## Install with `npx skill`

After this repository is published to GitHub, install one skill with:

```bash
SKILL_BASE_URL=https://github.com/zyyziyunying/skills/tree/main npx skill skills/<skill-name>
```

Example:

```bash
SKILL_BASE_URL=https://github.com/zyyziyunying/skills/tree/main npx skill skills/flutter-best-layout
```

`npx skill` installs into the current directory at:

```text
.codebuddy/skills/<skill-name>
```

## Install with `npx skills`

The newer `skills` CLI can also scan this repository directly:

```bash
npx skills add zyyziyunying/skills --skill <skill-name>
```

Install all skills:

```bash
npx skills add zyyziyunying/skills --all
```

## Available skills

| Skill | Purpose |
| --- | --- |
| `codex-project-harness` | Build agent-legible project facts, navigation, plans, constraints, and validation loops. |
| `dart-add-unit-test` | Add focused Dart unit tests with `package:test`. |
| `expert-agent-team` | Expert-agent execution used directly or by an explicit owner workflow. |
| `flutter-add-widget-test` | Add Flutter widget tests for rendering and interactions. |
| `flutter-app-size` | Measure, analyze, and reduce Flutter release artifact size. |
| `flutter-best-layout` | Flutter layout planning, review, preview, implementation, and responsive/adaptive UI guidance. |
| `flutter-implement-json-serialization` | Choose and implement project-aware generated, hybrid, or manual Flutter JSON serialization. |
| `flutter-release-packager` | Guide Flutter release packaging with preflight checks and artifact evidence. |
| `git-commit-helper` | Plan and create intentional atomic git commits. |
| `goal-first-development` | Canonical goal-first delivery entry with risk-based independent validation. |
| `humanizer` | Manual-only English prose humanizer for removing AI-writing tells. |
| `independent-review-subagent` | No-context independent review used directly or by an explicit owner workflow. |
| `independent-test-verifier` | Independent test design and test-only verification from authoritative behavior sources. |
| `local-image-to-webp` | Convert local images to WebP while preserving originals. |
| `manage-goal-docs` | Create and maintain goal folders with a concise `goal.html` overview and clearly owned scoped documents. |
| `patrol-e2e` | Explicit Patrol E2E workflow for Flutter setup, execution, and evidence. |
| `playwright` | Browser automation through Playwright CLI and wrapper scripts. |
| `playwright-interactive` | Persistent Playwright browser and Electron debugging. |
| `review-bug-value` | Review reported bug validity, value, priority, and business alignment. |
| `screenshot` | Capture desktop or app screenshots when OS-level capture is needed. |

## Recommended workflow entry

Use `$goal-first-development` as the normal entry for goal-driven software
delivery. It owns `goal.html`, validation-risk classification, the frozen
behavior contract, component routing, evidence backfill, and final goal status.

Depending on the confirmed goal, it may delegate execution or validation to
`expert-agent-team`, `review-bug-value`, `independent-test-verifier`, and
`independent-review-subagent`. These component skills remain directly invokable
for bounded standalone work, but users do not need to manually sequence them for
the normal goal-first flow. Device, release, account, payment, and mutable
backend-state boundaries still require the explicit skill or approval declared
by the relevant project rules.

## Maintain local discovery

Edit skills directly under `skills/<skill-name>`. To refresh local agent and Codex discovery links:

```bash
./scripts/link-local-skills.sh
```

Then verify CLI discovery:

```bash
npx skills add ./skills --list --full-depth
```

For `npx skill`, the package specifier must start with `skills/`, so the published GitHub path must remain:

```text
skills/<skill-name>/SKILL.md
```
