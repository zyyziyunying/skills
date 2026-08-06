---
name: goal-first-development
description: "Use only when the user explicitly invokes $goal-first-development. Own proportionate goal-driven delivery from goal.html: establish enough of the behavior contract and correctness sources to act safely, choose validation based on actual risk, use $independent-verifier when it adds meaningful confidence, implement within scope, and close with honest evidence."
---

# Goal-First Development

## Result

Deliver the smallest change that achieves a confirmed goal. Keep `goal.html` as
the stable entry and use only as much documentation, approval, delegation, and
validation ceremony as the task actually needs.

Use this skill only when the user explicitly invokes
`$goal-first-development`. Read-only discussion does not activate it.

## Authority

- Follow user instructions, repository rules, and declared project fact sources.
- Use `$manage-goal-docs` for goal creation and fact ownership when available.
  Otherwise use an identified existing goal, or ask before creating a minimal
  `./goals/.../goal.html` fallback.
- This workflow owns the goal contract and status. Other agents return work or
  evidence; they do not silently redefine the goal or mark it done.

## Establish Enough Contract

Select the supplied goal or the one unambiguous active goal and read
`goal.html` first. For a new goal, clarify the intended outcome and create the
smallest useful goal document.

Before implementation, know or record the facts that matter now:

- target outcome, meaningful constraints, and non-goals;
- expected observable behavior and the best available correctness sources;
- chosen approach and material boundaries;
- acceptance criteria, useful validation, and current blocker if any.

Keep each mutable fact in one owner document. Resolve gaps from local evidence,
use a disclosed assumption when reasonable, and ask only when the answer would
materially change behavior, scope, architecture, data semantics, cost, or write
authority.

Keep status and contract current. Seek renewed confirmation when a material
semantic decision changes, not for routine implementation detail.

## Scale Validation To Risk

Use L1/L2/L3 as judgment aids rather than fixed pipelines:

- **L1**: mechanical, documentation, or presentation work. Focused local checks
  are normally enough.
- **L2**: ordinary behavior, state, API, interaction, or semantic refactor work.
  Choose the test, review, runtime check, or combination most likely to expose
  the actual failure. Use an independent pass when it adds meaningful confidence,
  not automatically.
- **L3**: payment, permissions, privacy, security, account state, destructive
  operations, migration, release/store paths, or high-blast-radius behavior.
  Identify the authoritative facts and strongest relevant evidence before
  closure. Use independent, device, E2E, security, manual, or external evidence
  when the risk, project rules, or confirmed contract makes it material.

Record the level and short reason when it helps later decisions. Project-specific
required checks remain authoritative. Never present an unavailable device,
backend, vendor, store, or runtime result as completed evidence.

## Use Independent Verification Selectively

Use `$independent-verifier` when another perspective materially reduces risk:

- `bug-value` when defect validity, expected behavior, or fix value is unclear;
- `test-design` when freezing behavior before implementation is useful;
- `test-verification` when tests are the strongest correctness signal;
- `review` when the final structure, contract, or diff benefits from a second pass.

Give a fresh verifier neutral facts rather than the developer's conclusion. If
no fresh verifier is available, use the best direct check and label the evidence
honestly; absence of a subagent alone does not force the goal to remain active.

## Implement And Close

Implement the smallest scoped change that satisfies the current contract.
Preserve existing user work, use local patterns, and avoid unrelated refactors.
Use bounded subagents only when authorized and useful.

Run the strongest practical validation chosen for this goal and record the
result and meaningful limitations. Mark `done` when the declared acceptance and
completion criteria have credible evidence. Keep `active` when material required
evidence is pending, and use `blocked` only when no meaningful next step can
proceed.

Update owner documents with durable facts. Keep `goal.html` concise: status,
current conclusion, blocker or next action, and routing rather than a transcript.

Before implementation, report the goal, material contract, unresolved blocker,
and intended first check. Afterward, report status, changes, evidence, and
remaining risk.
