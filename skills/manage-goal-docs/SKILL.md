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
one goal file plus one shared style asset for all goals:

```text
./goals/
  _shared/
    goal.css
  <yyyy-mm-dd-semantic-slug>/
    goal.html
```

Optional folders such as `evidence/`, `assets/`, or `archive/` may exist beside
it. Do not create phase-shaped current documents such as `research.html`,
`design.html`, `check.html`, `plan.html`, or `problem.html` by default. Their
current conclusions belong in `goal.html`.

`./goals/_shared/goal.css` is presentation only. It is not a goal truth source,
does not need an entry in the linked-documents section, and must not contain
facts, status, decisions, validation results, or explanations.

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
     Add `--json` only when the caller needs machine-readable metadata about
     the created `goal.html` path and whether the shared CSS was created during
     this run.

   - Resolve the active skill directory from the parent directory of the
     `SKILL.md` file that activated this skill. Substitute that exact absolute
     path for `<skill-dir>` below; do not assume `CODEX_HOME` or a particular
     installer layout.

```bash
python3 "<skill-dir>/scripts/create_goal.py" \
  --slug subscription-global-analytics \
  "一句话目标内容"
```

   - Do not pass title, status, date, language, or workspace parameters.
     The script validates the slug, derives the title from the goal, uses
     today's date, creates under the current directory, starts in draft state,
     creates `./goals/_shared/goal.css` if missing, and uses the default Chinese
     template.
   - Keep the bundled `assets/goal.css` file with the skill when publishing,
     copying, or installing the skill. The script depends on that asset to
     create workspace-local shared CSS.

3. Keep `goal.html` current.
   - Update `goal.html` first when the real state changes.
   - Put only current conclusions, active decisions, acceptance criteria,
     validation results, and unresolved problems in `goal.html`.
   - Put long raw material under `evidence/` or `archive/` only when needed,
     then link it from `goal.html` with a one-line summary.
   - Keep generated and manual CSS out of `goal.html` for new documents. Link a
     stylesheet instead so agents can read the fact source without spending
     context on presentation.
   - Keep planned completion gates distinct from achieved validation evidence.
     Before a check runs, label its required outcome as pending. Never write a
     future independent review or test result as though it already happened.
   - After implementation changes current behavior, distinguish the pre-change
     baseline from the current implementation conclusion and refresh broken or
     stale evidence links before final review.

4. Treat the workflow phases as sections of `goal.html`.
   - `research`: facts, constraints, unknowns, and evidence.
   - `design`: chosen approach, boundaries, tradeoffs, and rejected options.
   - `check`: acceptance criteria and validation method; define it before the
     detailed plan when practical.
   - `plan`: execution steps derived from the design and check criteria.
   - `problem`: issues discovered at any point; this is a cross-cutting record,
     not a final linear phase.
   - In `check`, keep correctness sources and validation separation explicit:
     observable behavior, authoritative oracle, validation risk, developer
     checks, independent checks, required runtime evidence, and the decisive
     completion evidence. For bug work, include the intended pre-fix failure.

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
- validation risk (`L1`, `L2`, or `L3`) and a short justification when the
  active workflow uses risk-based validation
- correctness sources and separate developer/independent validation expectations
- plan
- problem record
- linked evidence or archive material
- change log
- a complete semantic page title; do not shorten the active title with an
  ellipsis merely for display

The bundled script creates a Chinese template by default. If another language
is required, create the goal first and then edit `goal.html` directly.

## Style And Token Budget

For new goal documents, keep style separate from facts:

- Link `../_shared/goal.css` from `goal.html`; do not inline a `<style>` block
  unless the user explicitly asks for a self-contained portable HTML file.
- Treat the default output as workspace-local, not single-file portable. When
  moving, archiving, or sharing a normal goal, keep `goals/_shared/goal.css`
  with the goal files and preserve the relative path from each `goal.html`.
- If a goal needs one-off presentation that the shared stylesheet cannot cover,
  put a style-only CSS file under that goal's `assets/` folder and link it from
  `goal.html`.
- Do not put current facts, decisions, status, validation evidence, unresolved
  problems, or explanatory prose in CSS files, CSS comments, class names, or
  decorative markup.
- When reading or updating older goal pages that still contain inline
  `<style>...</style>`, treat them as valid legacy or self-contained pages and
  skip the style block unless the task is specifically about visual
  presentation. Do not migrate their styles during ordinary fact updates.
- Migrate styles only when the user explicitly asks for style cleanup,
  portability changes, or goal document migration. Put reusable styles in
  `goals/_shared/goal.css`, put one-goal styles in that goal's `assets/`
  folder, and verify rendering for affected pages.
- Treat `goals/_shared/goal.css` as copy-once workspace output. The script does
  not overwrite an existing shared stylesheet. Updating shared CSS is an
  explicit migration step and must not add facts or explanations to CSS.
- Do not create self-contained single-file output by default. If the user needs
  a single-file share snapshot, create it under `archive/` as a dated
  non-truth-source snapshot. Only inline CSS in the active `goal.html` when the
  user explicitly requires the current truth source itself to be portable.

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

If exact supporting-file creation status matters, run the script with `--json`
and use `shared_css_created` plus `shared_css_path`. Without `--json`, successful
script output stays compatible and prints only the `goal.html` path.

When updating an existing goal, report:

- the updated `goal.html` path
- the sections changed
- any remaining open problem or missing validation
