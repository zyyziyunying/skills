# Bug Value Review

Use this mode to decide whether a reported bug or regression is real, valuable
to fix, and correctly classified. Treat reports, failing tests, review comments,
and severity labels as claims rather than conclusions.

## Establish The Claim

Identify the observed behavior, affected workflow and state, claimed severity,
proposed fix, and available reproduction evidence. Then establish:

1. Expected behavior and its current source of truth.
2. Whether a real user or supported system path can reach the state.
3. The affected invariant, workflow, API, data, privacy, billing, or operational
   guarantee.
4. Who is harmed, how often, and whether a practical workaround exists.
5. Whether the smallest valid fix is worth its implementation and regression
   risk.

Prefer project-declared fact sources, explicit product or platform contracts,
stable adjacent behavior, semantic tests, and finally code patterns, in that
order. Do not invent expected behavior when those sources are absent or
conflicting; classify the result as a product question or provisional finding.

Separate impact severity from scheduling priority. When P0-P3 is relevant, load
the root skill's linked severity rubric and assess reachability, blast radius,
frequency, workaround, and evidence confidence.

## Verdicts

- `Confirmed bug`: observed behavior violates a supported expectation.
- `Likely bug`: evidence points to a defect but one material fact is missing.
- `Product question`: the intended behavior is not defined or sources conflict.
- `Expected behavior`: the observation matches the current contract.
- `Low-value change request`: plausible improvement without sufficient defect
  or impact evidence.
- `False positive`: stale tests, invalid data, tooling, or unsupported setup.
- `Duplicate / known limitation`: already tracked or intentionally deferred.

Review a proposed fix only after the value gate. Judge validity separately from
cost and regression risk; reject a fix that passes a test while violating the
product model or module boundary.

## Result

Lead with verdict, impact severity, recommended timing, and primary next action.
Support them with the governing fact source, observed evidence, reachable user
impact, fix risk, source conflicts, and missing facts. Mark provisional business
claims explicitly.
