---
name: flutter-project-harness
description: Create or maintain project-level fact-source docs for Flutter apps, packages, plugins, examples, or workspace subprojects. Use when bootstrapping or refreshing SPEC.md, TEST.md, DESIGN.md, GENERATION.md, LOCAL.md, PACKAGING.md, AGENTS.md reading paths, and related project governance docs without running app builds or device commands.
---

# Flutter Project Harness

## Overview

Use this skill to create or maintain the small set of project-level fact sources that make a Flutter app, package, plugin, example, or subproject easy for humans and agents to work in. The target is governance scaffolding and reading paths, not runtime test/debug harness code.

## Canonical Files

Prefer these root-level files inside each independent Flutter app, package, plugin, or example:

- `SPEC.md`: project stage, goals, non-goals, compatibility posture, release/hardware/API assumptions.
- `TEST.md`: test scope, validation matrix, device/hardware facts, bug-report requirements, agent command boundary.
- `DESIGN.md`: project-level UI/display/interaction/visual facts.
- `GENERATION.md`: generated-file ownership, commands, ignored outputs, whether outputs are committed.
- `LOCAL.md`: local setup, debug entry, secrets, human-run commands, machine-local files.
- `PACKAGING.md`: package identity, signing, versioning, artifacts, install/update/deployment rules.
- `AGENTS.md`: execution rules and read-before-editing path that points to the files above.

Use only the relevant subset. A pure Dart package may not need `DESIGN.md` or `PACKAGING.md`; a Flutter plugin may need separate app/package/example packaging notes; a docs-only area may only need a short `AGENTS.md` reading path.

## Workflow

1. Read the nearest `AGENTS.md` and the workspace root `AGENTS.md` when coordination or validation policy matters.
2. Identify project type: Flutter app, package, plugin, example app, workspace root, tooling area, docs-only area, or submodule.
3. Inspect existing fact sources and do not overwrite useful project-specific content.
4. Create missing files from the closest template in `assets/templates/`, then adapt the content to the actual project stage and platform.
5. Update `AGENTS.md` so future work reads the right fact source before editing.
6. Keep the docs short, current, and opinionated. Avoid PRD-sized detail, architecture dumps, stale checklists, or duplicating implementation docs.
7. Do not run Flutter, Android, iOS, emulator, simulator, or device commands unless the user or the project's `AGENTS.md` explicitly allows the exact command.

## File Ownership Rules

- `SPEC.md` owns project posture. Do not bury stage or compatibility decisions only in `README.md`.
- `TEST.md` owns validation scope. It should say what tests are worth writing and what must be manually validated.
- `DESIGN.md` owns project-wide design facts. Feature-specific details belong near the feature.
- `GENERATION.md` owns generated artifacts. Every generator should list source paths, output paths, command, commit/ignore policy, and whether Codex may run it.
- `LOCAL.md` owns local setup. Keep secrets, ignored files, and machine-local entries explicit.
- `PACKAGING.md` owns installable or publishable artifacts. Apps need versioning, signing, artifact naming, release channel, and rollback notes; packages need publishing and compatibility rules.
- `AGENTS.md` owns agent execution and reading order. It should reference fact sources instead of duplicating their current details.

## Flutter Defaults

- Treat root workspace validation policy as binding unless a nearer `AGENTS.md` narrows it.
- For Flutter apps, Codex should not run build, run, install, emulator, simulator, or device commands by default.
- For packages, prefer lightweight static/test validation only when the project rules allow it and dependencies are already available.
- For submodules, commit subproject documentation inside the submodule and commit parent submodule-pointer changes separately.
- Use the current date in document headers.
- If a source code file already exceeds or will exceed 2000 lines and the project uses a shared code-size rule, add the required code TODO in source files only; do not add code-size markers to Markdown docs.

## Template Use

Templates are skeletal. Read only the relevant template:

- `assets/templates/SPEC.md`
- `assets/templates/TEST.md`
- `assets/templates/DESIGN.md`
- `assets/templates/GENERATION.md`
- `assets/templates/LOCAL.md`
- `assets/templates/PACKAGING.md`
- `assets/templates/AGENTS-reading-path.md`

Replace bracketed placeholders and remove sections that do not apply. Do not leave generic template language in the project.

## Validation

Before finishing:

- Check `git status` in the target project and parent workspace when submodules are involved.
- Confirm new fact-source links resolve.
- Confirm `AGENTS.md` reading order matches the new docs.
- State which validation commands were intentionally deferred by policy.
