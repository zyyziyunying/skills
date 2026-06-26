# skills

This repository packages my personal agent skills for installation with `npx skill`.
Most skills are maintained for Flutter project work, with a few supporting workflows for Git, browser automation, screenshots, and project documentation.

The installable tree lives under `skills/<skill-name>/SKILL.md`. The top-level skill folders in this local checkout are kept for the active local agent setup and are intentionally ignored by git.

## Install with `npx skill`

After this repository is published to GitHub, install one skill with:

```bash
SKILL_BASE_URL=https://github.com/zyyziyunying/skills/tree/main npx skill skills/<skill-name>
```

Example:

```bash
SKILL_BASE_URL=https://github.com/zyyziyunying/skills/tree/main npx skill skills/flutter-build-responsive-layout
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
| `dart-add-unit-test` | Add focused Dart unit tests with `package:test`. |
| `dart-use-pattern-matching` | Apply Dart switch expressions and pattern matching where appropriate. |
| `expert-agent-team` | Manual-only orchestration for complex multi-agent tasks. |
| `flutter-add-widget-test` | Add Flutter widget tests for rendering and interactions. |
| `flutter-best-layout` | Manual-only Flutter layout planning, review, preview, and implementation workflow. |
| `flutter-build-responsive-layout` | Build or fix Flutter UI that adapts across sizes and orientations. |
| `flutter-fix-layout-issues` | Fix Flutter overflow and unbounded-constraint layout errors. |
| `flutter-implement-json-serialization` | Implement App API DTO and JSON mapping work in the BesideYou Flutter app. |
| `git-commit-helper` | Plan and create intentional atomic git commits. |
| `goal-first-development` | Manual-only goal-first workflow driven by `goal.html`. |
| `independent-review-subagent` | Manual-only independent no-context review subagent workflow. |
| `local-image-to-webp` | Convert local images to WebP while preserving originals. |
| `manage-goal-docs` | Create and maintain goal folders with a single `goal.html` truth source. |
| `patrol-e2e` | Explicit Patrol E2E workflow for Flutter setup, execution, and evidence. |
| `playwright` | Browser automation through Playwright CLI and wrapper scripts. |
| `playwright-interactive` | Persistent Playwright browser and Electron debugging. |
| `review-bug-value` | Review reported bug validity, value, priority, and business alignment. |
| `screenshot` | Capture desktop or app screenshots when OS-level capture is needed. |

## Maintain the published tree

When editing local top-level skills, refresh the GitHub install tree before committing:

```bash
./scripts/sync-published-skills.sh
```

Then verify discovery:

```bash
npx skills add ./skills --list --full-depth
```

For `npx skill`, the package specifier must start with `skills/`, so the published GitHub path must remain:

```text
skills/<skill-name>/SKILL.md
```
