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

Use `goal.html` as the stable entry point: goal, overall status, current
conclusion, important blocker or next action, and links to detailed documents.

Use the smallest clear structure. Keep a small goal in `goal.html`; split
large, fast-changing, independently reviewed, or reusable detail into semantic
Markdown or HTML documents. Use `evidence/` for raw evidence, `assets/` for
presentation assets, and `archive/` for superseded snapshots when useful.

**One owner per mutable fact.** Each active document needs a clear scope.
`goal.html` routes and summarizes; linked documents own their detailed facts.
Do not duplicate mutable detail. Resolve conflicts, or state which document
owns that scope.

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

3. Shape documents around semantic ownership, not mechanical phases. Research,
   design, checks, plans, and problems are concerns—not mandatory files or
   headings. When several active documents exist, link each from `goal.html`
   and state its owner area; identify the scoped document's purpose near the
   top when its title is not enough.

4. When a fact changes, update its owner first. Update `goal.html` only when
   its status, conclusion, blocker, next action, or routing also changes.
   Remove stale duplicates instead of synchronizing them.

5. Keep validation honest: distinguish planned criteria from achieved evidence,
   implementation checks from external or independent proof, and historical
   baselines from the current conclusion. Close by marking the goal done,
   blocked, or superseded and linking decisive evidence or the concrete blocker.
   Update any separate module-level contract that owns behavior changed by work.

## Presentation

- Keep the first semantic line under the title as a concise outcome statement:

```html
<p class="goal-line"><strong>一句话目标：</strong>...</p>
```

- For new pages, link `../_shared/goal.css`; CSS is presentation only. Preserve
  legacy inline styles unless the user asks for a style migration.
- Link supporting material from `goal.html` without copying evidence detail
  into the overview. Prefer readable current state; archive history that hides
  the current decision.

## Response

For a new goal, report its path, summary, slug, and initial status. For an
update, report changed files and ownership areas plus any blocker or missing
validation.
