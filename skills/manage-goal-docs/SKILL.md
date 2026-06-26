---
name: manage-goal-docs
description: "Create and maintain goal documents under ./goals with one goal.html truth source per goal folder and a high-quality semantic folder slug. Use when the user asks to create a goal doc, start a goal folder, consolidate research/design/plan/check/problem material, enforce a single goal.html truth source, improve goal-folder naming, or work with a goal-driven documentation flow."
---

# Manage Goal Docs

## Core Rule

Create one folder per goal under the current working directory:

```text
./goals/<yyyy-mm-dd-semantic-slug>/goal.html
```

`goal.html` is the only active truth source for that goal. The normal shape is
a single file:

```text
./goals/<yyyy-mm-dd-semantic-slug>/
  goal.html
```

Optional folders such as `evidence/`, `assets/`, or `archive/` may exist beside
it. Do not create phase-shaped current documents such as `research.html`,
`design.html`, `check.html`, `plan.html`, or `problem.html` by default. Their
current conclusions belong in `goal.html`.

Always make the first semantic content under the page title a one-sentence goal:

```html
<p class="goal-line"><strong>一句话目标：</strong>...</p>
```

This sentence must state only the target outcome. Do not include background,
root cause, solution details, risks, or implementation history in it.

Use a separate semantic folder slug for discoverability. The slug must be an
English, lowercase, kebab-case summary of the goal outcome:

- 3 to 8 semantic words, at most 64 characters.
- Include the domain, page, module, or workflow plus the target outcome.
- Prefer `subscription-global-analytics`,
  `runtime-manifest-localization`, or `moment-card-density` style names.
- Avoid weak names that only repeat the project or module, such as
  `besideyou-flutter`, `pet-space`, `my-space`, `free-plan`, or `goal-38812b`.

## Workflow

1. Use the current working directory as the root.
   - Do not auto-detect Git roots, workspace roots, package roots, or old docs
     taxonomies.
   - The goal folder is created under `./goals` relative to where the command is
     run.

2. Create or update the goal.
   - For a new goal, create `./goals/<date>-<semantic-slug>/goal.html`.
   - Before running the script, choose one high-quality semantic slug from the
     one-sentence goal. Do not rely on automatic translation or truncation.
   - Prefer the bundled script for consistent structure.
   - Pass `--slug` plus exactly one positional argument: the one-sentence goal.

```bash
/usr/bin/python3 /Users/zyyziyunying/.codex/skills/manage-goal-docs/scripts/create_goal.py \
  --slug subscription-global-analytics \
  "一句话目标内容"
```

   - Do not pass title, status, date, language, or workspace parameters.
     The script validates the slug, derives the title from the goal, uses
     today's date, creates under the current directory, starts in draft state,
     and uses the default Chinese template.

3. Keep `goal.html` current.
   - Update `goal.html` first when the real state changes.
   - Put only current conclusions, active decisions, acceptance criteria,
     validation results, and unresolved problems in `goal.html`.
   - Put long raw material under `evidence/` or `archive/` only when needed,
     then link it from `goal.html` with a one-line summary.

4. Treat the workflow phases as sections of `goal.html`.
   - `research`: facts, constraints, unknowns, and evidence.
   - `design`: chosen approach, boundaries, tradeoffs, and rejected options.
   - `check`: acceptance criteria and validation method; define it before the
     detailed plan when practical.
   - `plan`: execution steps derived from the design and check criteria.
   - `problem`: issues discovered at any point; this is a cross-cutting record,
     not a final linear phase.

5. Close the goal.
   - Mark the status as done, blocked, or superseded.
   - Record final validation evidence or the concrete blocker.
   - If the work changes a module-level truth source such as `SPEC.html`, update
     that source separately according to the active project rules.

## Required Goal Shape

Keep `goal.html` readable as a standalone current-state page. It should include:

- `一句话目标`
- current status, initially draft
- research summary
- design decision
- check criteria
- plan
- problem record
- linked evidence or archive material
- change log

The bundled script creates a Chinese template by default. If another language
is required, create the goal first and then edit `goal.html` directly.

## Evidence And Archive Material

Do not create phase-named supporting HTML files by default. If long material
would make `goal.html` unreadable, put it under:

```text
evidence/
assets/
archive/
```

Allowed supporting material includes raw logs, screenshots, payloads, source
excerpts, copied evidence, generated images, and superseded historical
snapshots. It must not contain the active research conclusion, design decision,
check criteria, plan, or problem state. Those current facts remain in
`goal.html`.

Every supporting item must be linked from `goal.html` with a one-line summary.
A reader who only opens `goal.html` must still know the current state and next
action.

## Response Shape

When creating a new goal, report:

- the `goal.html` path
- the one-sentence goal used
- the semantic slug used
- any supporting files created
- whether the goal is draft, active, blocked, done, or superseded

When updating an existing goal, report:

- the updated `goal.html` path
- the sections changed
- any remaining open problem or missing validation
