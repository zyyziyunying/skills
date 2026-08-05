---
name: manage-goal-docs
description: "Create and maintain goal folders under ./goals, with goal.html as a concise goal-level overview and router plus optional scoped truth-source documents. Use when Codex needs to create, organize, split, consolidate, or update goal documentation; clarify fact ownership; reduce goal.html bloat; or keep research, decisions, checks, plans, problems, evidence, and history discoverable without duplicating mutable facts."
---

# Manage Goal Docs

## Core Model

Create one folder per goal under the current working directory:

```text
./goals/<yyyy-mm-dd-semantic-slug>/
  goal.html
```

Use `goal.html` as the stable entry point. Keep the goal, overall status, concise
current conclusion, important blockers or next action, and links to any detailed
documents there.

A goal may use one file or several. Choose the smallest structure that remains
clear:

- Keep a small goal entirely in `goal.html`.
- Split large, fast-changing, independently reviewed, or reusable detail into
  semantic Markdown or HTML documents such as `appsflyer-check.md` or
  `release-readiness.md`.
- Use `evidence/` for raw evidence, `assets/` for presentation assets, and
  `archive/` for superseded snapshots when useful.

The invariant is **one owner per fact**, not one file per goal. Each active
document must have a clear scope. Do not maintain the same mutable detail in
multiple places. A summary in `goal.html` is navigational; the linked scoped
document owns its detailed facts. If documents conflict, resolve the conflict
or state which document owns that scope.

## Workflow

1. Use the current working directory as the root. Do not auto-detect another
   repository or package root.

2. For a new goal, choose a descriptive lowercase kebab-case slug and prefer
   the bundled script:

```bash
python3 "<skill-dir>/scripts/create_goal.py" \
  --slug subscription-global-analytics \
  "一句话目标内容"
```

Resolve `<skill-dir>` from the `SKILL.md` that activated this skill. The script
creates a draft under `./goals`, copies the shared stylesheet when missing, and
prints the new `goal.html` path. Add `--json` only when machine-readable output
is useful.

3. Adapt the document structure to the work. Research, design, checks, plans,
   and problems are useful concerns, not mandatory files or headings. Combine,
   rename, omit, or split them according to the goal. Prefer semantic ownership
   boundaries over mechanical phase documents.

4. Record ownership explicitly when more than one active document exists.
   `goal.html` should link each document and briefly state what it owns. A
   scoped document should identify its purpose near the top when ownership is
   not obvious from its title.

5. Update the owning document first when a fact changes. Update `goal.html`
   only when the goal-level status, conclusion, blocker, next action, or routing
   also changes. Remove stale duplicates instead of trying to synchronize them.

6. Keep validation honest. Distinguish planned completion criteria from
   achieved evidence, implementation checks from external or independent
   proof, and historical baselines from the current conclusion. Use validation
   risk levels only when they help the active workflow.

7. Close a goal by marking it done, blocked, or superseded and linking the
   decisive evidence or concrete blocker. Update any separate module-level
   contract or specification that owns behavior changed by the work.

## Presentation

- Keep the first semantic line under the title as a concise outcome statement:

```html
<p class="goal-line"><strong>一句话目标：</strong>...</p>
```

- For new pages, link `../_shared/goal.css`. Treat CSS as presentation only.
- Preserve legacy inline styles unless the user asks for a style migration.
- Link supporting material from `goal.html`, but do not copy every evidence
  detail into the overview.
- Prefer readable current state over a comprehensive activity log. Archive long
  or superseded history when it obscures the current decision.

## Response

For a new goal, report the created path, goal summary, slug, and initial status.
For an update, report the files and ownership areas changed plus any remaining
blocker or missing validation.
