# [Project Name] TEST

Date: [YYYY-MM-DD]
Status: current test and validation fact source
Scope: `[project/path]`

Use this document with `SPEC.md` when deciding what validation is meaningful.

## Automated Test Scope

Prefer automated tests for:

1. [Project-owned logic.]
2. [Parsing/mapping/state decisions.]
3. [Boundary contracts that do not require a device.]

Avoid tests whose only value is:

1. [Framework/build existence checks.]
2. [Static implementation details.]
3. [Behavior better validated on real hardware/device.]

## Validation Strategy

- Correctness sources: [SPEC sections, API/domain contracts, platform rules, or
  confirmed user-visible behavior that define expected results.]
- Required validation: [Project-defined checks and evidence, scaled to the
  behavior, risk, and available environment.]
- Independent verification: [Whether and when the project requires an
  independent charter, test verification, review, or additional E2E/device
  evidence. Omit if no such policy applies.]

Do not use the current implementation output as the sole expected value. Treat
existing tests as evidence that may be stale or coupled to implementation.

## Agent Test Ownership (When Applicable)

- Developer agents may modify: [product paths and focused developer-test paths.]
- Independent test verifiers may modify: [explicit test, fixture, and
  test-support paths only.]
- Independent test verifiers must not modify: [product code, goal semantics, or
  assertions merely to obtain a pass.]
- Independent reviewers: [Project-defined scope and required source context.]

## Bug-Fix Evidence

For confirmed bugs, record:

1. Observed behavior.
2. Expected behavior and authoritative source.
3. Regression test or equivalent observable check.
4. Whether fail-before-fix/pass-after-fix was actually demonstrated against a
   safe isolated baseline.
5. Any unproven baseline, device, backend, or environment condition.

## Manual Validation

[List devices, browsers, hardware, manual commands, and evidence expectations.]

## Agent Boundary

[Record only project-specific execution constraints and link to the authoritative
source for shared rules. Derive the boundary from applicable project instructions
and user authorization; do not require repeat approval for already authorized
steps. Identify any operation whose scope or required authorization is unresolved.]

## Bug Reports

[List required environment/build/reproduction/evidence fields.]

## Related Fact Sources

[Link SPEC, AGENTS, LOCAL, PACKAGING, GENERATION.]
