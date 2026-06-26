---
name: goal-first-development
description: "Use only when the user explicitly invokes $goal-first-development. Start or continue a goal-first workflow, delegate goal document path, naming, creation, and maintenance to $manage-goal-docs, require a complete-enough ./goals/.../goal.html before implementation, execute narrowly from that truth source, validate under active project rules, and write final evidence back."
---

# Goal First Development

## Purpose

Use this skill only when the user explicitly invokes `$goal-first-development`.
It is the front door for goal-driven implementation: clarify the real outcome,
ensure there is one current `goal.html`, make that document complete enough to
drive execution, then implement and validate from it.

Do not use this skill merely because the user asks about goals, asks for a
read-only explanation, reviews this skill, or mentions goal flow in ordinary
conversation. For read-only analysis, explain the workflow and do not create or
modify project files.

## Authority Model

- Active user instructions, repository rules, owner docs, and project fact
  sources remain authoritative for reading order, validation limits, runtime
  limits, and project-specific constraints.
- Goal document path shape, folder naming, creation, template, and maintenance
  are delegated to `$manage-goal-docs`. When creating or updating goal docs,
  load and follow that skill's current contract exactly. If it is not available,
  do not invent replacement naming rules; ask the user for a goal document path
  or for permission to proceed with a minimal `./goals/.../goal.html` fallback.
- Do not use the old project-anchor or docs-taxonomy model. Do not create
  phase-shaped current documents such as `research.html`, `design.html`,
  `check.html`, `plan.html`, or `problem.html` by default.
- If an active project rule conflicts with this workflow, follow the project
  rule and briefly state how it changes the goal-first flow.

## Flow Selection

At the start of an invocation, choose one mode:

1. Start a new goal.
   - Use when the user gives an outcome but no goal path.
   - Clarify a one-sentence target outcome first.
   - Create `goal.html` through `$manage-goal-docs` after the one-sentence goal
     is clear; let `$manage-goal-docs` define the required folder naming and
     script parameters.

2. Continue an existing goal.
   - Use when the user provides a goal folder, a `goal.html` path, or the thread
     has one unambiguous active goal.
   - Read `goal.html` before using chat memory or editing files.

3. Execute an existing goal.
   - Use when the user asks to implement from a goal document.
   - Read `goal.html`, apply the completeness gate below, then work only from
     the current conclusions in that file.

If multiple goal folders could apply and the user did not identify one, ask one
direct question for the goal path.

## Goal Document Gate

Before changing implementation files, the selected `goal.html` must be complete
enough to act as the development contract. It must include current, non-placeholder
content for:

- `一句话目标`: one sentence stating only the target outcome.
- Status: draft for clarification, active before implementation, and done,
  blocked, or superseded when closed.
- Research summary: confirmed facts, constraints, unknowns, and evidence.
- Design decision: chosen approach, boundaries, tradeoffs, and rejected options
  when they matter.
- Check criteria: observable acceptance criteria and the validation method.
- Plan: execution steps derived from the design and check criteria.
- Problem record: current blockers, open risks, or an explicit "none".
- Supporting material links when raw evidence exists outside `goal.html`.

"Complete enough" does not mean exhaustive. It means every item needed to make
the next implementation decision is either resolved in `goal.html`, explicitly
recorded as a non-blocking assumption, or recorded as a blocker.

If the document is incomplete:

- Inspect the relevant evidence first when it can answer the gap.
- Update `goal.html` with current conclusions before implementing.
- Ask only blocking questions that cannot be answered safely from local context.
- Do not edit implementation files until the check criteria and validation
  method are adequate.

## Workflow

1. Clarify the real goal.
   - Restate the outcome the user actually needs.
   - Separate confirmed facts, assumptions, constraints, unknowns, non-goals,
     and success criteria.
   - Challenge the framing when the requested solution is misaligned with the
     real objective.

2. Ensure the goal document exists.
   - For a new goal, use `$manage-goal-docs` and its bundled script according
     to that skill's current creation contract, including folder naming and
     parameters.
   - Do not duplicate, weaken, or override `$manage-goal-docs` slug or path
     rules in this skill.
   - For an existing goal, read its `goal.html` first and treat it as the
     current truth source.

3. Complete `goal.html` before implementation.
   - Read the relevant evidence: code, config, tests, docs, logs, runtime
     observations, API contracts, or owner documentation as appropriate.
   - Keep confirmed facts separate from assumptions.
   - Put current research, design, check, plan, and problem conclusions in
     `goal.html`, not in separate phase documents.

4. Confirm the concise development contract.
   - Derive the contract from `goal.html`: goal, constraints, non-goals,
     approach, check criteria, validation method, and open problems.
   - Treat explicit approval such as "确认", "可以", "按这个做", or "go ahead"
     as confirmation.
   - Treat a direct request to execute the selected goal as confirmation only
     when `goal.html` is complete enough and the requested outcome is clear.
   - If the next step could change code, files, cost, user-facing behavior,
     architecture, data semantics, or docs authority and approval is unclear,
     ask one direct confirmation question.

5. Activate the goal before implementation.
   - After the contract is confirmed, update `goal.html` from `draft` to
     `active` before changing implementation files.
   - Do not implement directly from a `done` or `superseded` goal unless the
     user explicitly asks to reopen it or create a follow-up goal.
   - If the selected goal is `blocked`, confirm the blocker is resolved or
     record the new condition before continuing.

6. Build toward the goal.
   - Implement the smallest change that satisfies the confirmed `goal.html`
     contract.
   - Preserve existing user changes and local patterns.
   - Avoid unrelated refactors.
   - If the best implementation differs from the goal document, update
     `goal.html` first and explain the material decision.

7. Validate through active project rules.
   - Choose the strongest practical check allowed by current instructions.
   - Respect project policies that forbid builds, device runs, simulators, or
     broad analysis commands.
   - If local validation is complete but final acceptance requires user-side
     runtime evidence, device checks, backend state, or another unavailable
     environment, keep the goal active and record pending validation or remaining
     risk instead of marking it blocked.
   - Mark the goal blocked only when no meaningful next step can proceed until
     an external condition is resolved.

8. Update `goal.html` after validation.
   - Record only material decisions, final validation evidence, current status,
     and unresolved problems.
   - Do not turn `goal.html` into an execution log.
   - Do not mark the goal done without decisive validation.
   - If user-side validation is still required, keep the goal active and record
     the pending validation or remaining risk.
   - If a concrete blocker prevents further progress, mark it blocked and state
     the condition that must change.

## Response Shape

Before implementation, respond with:

- selected `goal.html` path and status
- concise development contract derived from `goal.html`
- completeness gate result, including missing blocking items if any
- approval status, including whether design or architecture approval is already
  satisfied
- first validation target or first test target

After implementation, respond with:

- whether the goal was achieved
- changed files
- `goal.html` sections updated
- validation performed
- remaining risk or blocker, if any

Keep responses direct and evidence-based.
