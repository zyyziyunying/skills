---
name: review-bug-value
description: Judge whether a reported bug, regression claim, severity/priority label, or bug-fix value claim is valid, valuable, project-aware, business-aligned, and worth fixing. Use only when the user asks for bug value review, bug triage, severity/priority validation, judging whether a bug is real or valuable, distinguishing expected behavior from defects, or evaluating whether a proposed bug fix is valid, valuable, worth accepting, and aligned with project facts, requirements, user workflows, module boundaries, and real user impact. Do not use for ordinary debugging, generic code review, routine failing-test repair, or implementation work unless the user asks to evaluate bug validity/value first.
---

# Review Bug Value

## Core Rule

Treat severity labels, reviewer comments, failing tests, and user reports as claims, not conclusions.

Read the artifacts the user provides before judging the claim. If the user gives an issue, diff, test output, logs, screenshots, code paths, requirements, or tickets, inspect the relevant evidence and distinguish direct evidence from inference and missing facts.

Before deciding whether a claim is valuable, establish the affected project's context. A bug is not valuable just because a local symptom exists; it is valuable when the symptom violates the project's current facts, user workflows, product guarantees, module contracts, or operational constraints.

Before recommending a fix, establish:

1. What behavior is observed.
2. What behavior is expected.
3. Which source of truth defines that expectation.
4. Which project workflow, invariant, or module contract is affected.
5. Who is harmed if the behavior remains.
6. Whether fixing it is worth the implementation and regression risk.

If the expected behavior cannot be tied to a requirement, product invariant, platform contract, security/privacy rule, data integrity rule, or clear user workflow, classify the item as a product question or low-value change request instead of a confirmed bug. Do not invent business value when goals, user impact, or product invariants are unclear.

## Workflow

### 1. Build The Claim

Extract the smallest reviewable claim:

- Reported symptom or review comment.
- Affected product area, platform, role, locale, account type, feature flag, or data state.
- Claimed severity or priority.
- Proposed or requested fix, if any.
- Evidence already available: steps, screenshots, logs, stack trace, test output, code diff, metrics, user impact.

If key evidence is missing, say exactly what is missing and continue with a provisional classification. Tie important conclusions to concrete files, tests, logs, requirements, or tickets when available.

### 2. Establish Project Context

Before judging validity, read the task-relevant project context and nearby fact sources needed to resolve expected behavior. Expand outward only when the decision depends on it, and mark conclusions provisional when context is unavailable.

Identify:

- The declared current behavior and intended product direction.
- The product goal, user role, and workflow the affected code supports.
- The affected module boundary, API contract, data flow, and owner-facing contract.
- Whether the behavior is intentionally unsupported, deferred, deprecated, platform-specific, role-specific, locale-specific, plan-specific, flag-gated, or migration-related.
- Whether tests encode product semantics or only implementation assumptions.

If no project fact source exists, mark product and business conclusions as provisional instead of filling the gap with intuition.

### 3. Find The Source Of Truth

Prefer sources in this order:

1. Project-declared fact sources for the affected area.
2. Explicit product, legal, security, privacy, data integrity, billing, or platform requirements.
3. Existing behavior in adjacent flows or stable released versions, when not contradicted by current project facts.
4. Tests that encode real product semantics.
5. Code comments, implementation patterns, or reviewer/reporter preference.

Do not treat a test failure as automatically valuable. Tests can encode stale requirements, overly broad assumptions, or implementation details.

When sources conflict, do not average them. State the conflict, prefer the most authoritative current fact source, and classify the claim as `Product question` or `Likely bug` only if the expected behavior cannot be resolved from project evidence.

### 4. Validate Business Value

Ask whether the issue affects a real user, workflow, or system guarantee:

- Blocks a core task or money/account/data movement.
- Causes data loss, corruption, privacy/security exposure, billing errors, or irreversible user action.
- Breaks a contractual/API/platform compatibility expectation.
- Creates a frequent, confusing, or support-heavy experience for an important user segment.
- Damages observability, recovery, or operational safety.

For user-facing claims, reconstruct the real workflow: user role, entry point, required state, permissions, flags, data prerequisites, downstream consequence, and workaround. Do not assign high value to a state that only exists through invalid fixtures, unsupported API use, or impossible navigation.

If impact is cosmetic, unreachable, purely internal, or only visible under artificial data, downgrade it unless it violates a defined quality bar.

### 5. Separate Severity From Priority

Impact severity describes harm if the bug happens. Priority or timing describes whether to fix it now.

Challenge P1/P2 labels with:

- Reproducibility: always, intermittent, environment-specific, or unproven.
- Reachability: real production path or synthetic setup.
- Blast radius: one account, one segment, all users, backend-wide.
- Frequency: common workflow or rare edge case.
- Workaround: none, costly, acceptable, or trivial.
- Fix risk: isolated, shared core path, migration/data risk, security risk.

Read `references/severity-rubric.md` when the decision depends on impact severity boundaries. If a project uses P0/P1/P2/P3 as priority labels instead of severity labels, state that mapping explicitly.

### 6. Review The Fix Only After The Value Gate

When a fix is proposed, review two things separately:

- Validity: does the fix implement the true expected behavior?
- Cost/risk: does it add complexity, broaden scope, mask symptoms, or create regressions?

Before accepting a proposed fix, check whether it respects module boundaries, ownership contracts, data flow, migration strategy, and long-term architecture intent. A fix that restores the reported behavior but violates these constraints is unsafe or mis-scoped even when the bug itself is valid.

Reject fixes that make a test pass while violating the product model. Prefer narrow fixes when the bug is real and localized; recommend product clarification when expected behavior is ambiguous.

### 7. Produce A Decision

Use direct validity labels. Do not use the decision label to encode scheduling: a real defect with low impact is still a `Confirmed bug`; express low value through impact severity, recommended timing, and next action.

- `Confirmed bug`: real defect with supported expected behavior.
- `Likely bug`: evidence points to a defect but one fact still needs confirmation.
- `Product question`: expectation is plausible but not defined.
- `Expected behavior`: observed behavior matches requirements or established product logic.
- `Low-value change request`: plausible improvement or mismatch, but not a confirmed defect and impact does not justify current priority.
- `False positive`: caused by stale tests, invalid assumptions, bad data, tooling, or artificial setup.
- `Duplicate / known limitation`: already tracked or intentionally deferred.

For larger reviews, read `references/report-template.md` and use its concise structure.

## Working Style

- Lead with the decision, not the investigation narrative.
- Be explicit about assumptions and missing evidence.
- Mark business or product claims as provisional when the source of truth is absent.
- Preserve useful bug reports even when downgrading them: identify the narrower real problem if one exists.
- Do not overfit to the reporter's proposed solution.
- Do not perform broad refactors while fixing a validated bug unless the fix cannot be safe without them.
- If asked to implement after review, keep the change scoped to the confirmed defect and add focused tests or static checks when the codebase supports them.
