# Impact Severity Rubric

Use this rubric to challenge or assign impact severity: the harm if the issue occurs. Keep priority or scheduling as a separate decision unless the project explicitly defines P labels as priority labels.

Calibrate severity against the affected project's declared facts before applying generic labels. Raise confidence when the issue violates a documented product invariant, core workflow, API contract, data integrity rule, security/privacy rule, or current release goal. Lower confidence when the behavior is intentionally unsupported, deferred, deprecated, flag-gated, migration-related, or reachable only through invalid fixtures or unsupported API use.

## P0

Production emergency level impact. Immediate action is often justified when at least one is true:

- Broad outage of a core user or business workflow.
- Data loss, corruption, irreversible destructive action, or serious billing/accounting error.
- Active security or privacy exposure.
- Deployment is blocked because release would create one of the above.

Evidence should include production impact, clear reproduction, monitoring, logs, or a high-confidence code path.

## P1

High-impact defect:

- Core workflow blocked for many users or an important segment.
- No acceptable workaround.
- Significant revenue, compliance, trust, or operational risk.
- Regression in a recently released critical path.

Downgrade if impact is only theoretical, limited to test data, behind an unused flag, or has an acceptable workaround.

## P2

Meaningful defect:

- Non-core but important workflow is degraded.
- Workaround exists but is costly or easy to miss.
- Repeated support burden or noticeable user confusion.
- Localized regression with clear user impact.

Downgrade if the issue is cosmetic, rare, or only affects internal convenience.

## P3

Low-impact issue:

- Cosmetic mismatch, copy nit, layout polish, non-blocking edge case.
- Internal-only inconvenience.
- Rare issue with simple workaround.
- Improvement request incorrectly filed as a bug.

P3 can still be worth fixing when the change is small, safe, and adjacent to current work, but the priority/timing decision should state that separately.

## Common Mislabels

- P1 label on a behavior that matches requirements.
- P1 label on a failing test whose assumption is stale.
- P2 label on an unreachable state created by mocks or invalid fixtures.
- Bug label on a missing feature or product preference.
- Severity based on how annoying the issue is to developers rather than user or business harm.
- Priority labels reused as impact labels without saying so.
- Severity assigned without checking the project's fact sources, core workflows, module contracts, or known limitations.
