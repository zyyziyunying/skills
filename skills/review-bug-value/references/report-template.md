# Bug Value Review Template

Use this structure for concise reviews. Omit sections that do not add signal.

## Short Form

Decision: use one decision label from `SKILL.md`.

Impact severity: `P0 | P1 | P2 | P3 | Not a defect | Unknown`

Recommended priority/timing: `Fix immediately | Schedule soon | Backlog | No fix now | Clarify first`

Reason:

- Project fact source:
- Expected behavior source:
- Actual behavior evidence:
- Product/workflow context:
- Module/API boundary:
- User/business impact:
- Reproducibility and reachability:
- Architecture or migration impact:
- Source conflicts:
- Fix risk:
- Missing facts or assumptions:

Primary next action: choose exactly one.

- Fix now
- Clarify product
- Downgrade
- Close
- Track separately

Secondary action: optional, only when needed.

- Add or update test
- Add monitoring, logging, or reproduction evidence
- Document known limitation

## Review Finding Form

Use this when reviewing a bug-value finding in code or a bug-fix PR after the value gate:

`[Priority] Finding title`

Explain the defect in one paragraph:

- What breaks.
- Why it breaks according to the source of truth.
- When users or systems hit it.
- What evidence supports the impact severity and recommended timing.

Then recommend the smallest safe correction. If the claimed bug is not valid, state what evidence would change that conclusion.

## Questions To Ask

- What requirement or invariant says this behavior is wrong?
- Which project fact source governs this area?
- What user workflow, role, state, permission, flag, or data prerequisite makes the issue reachable?
- Does the proposed fix respect module boundaries, API contracts, data flow, and migration direction?
- Can a real user reach this state without test-only setup?
- Is the impact user-facing, business-facing, operational, or only developer-facing?
- Would the proposed fix change behavior outside the reported path?
- Is this a bug, a missing feature, a product decision, bad data, or stale test coverage?
- What is the cost of doing nothing until the next normal planning cycle?
