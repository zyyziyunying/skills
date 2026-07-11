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
- L1 validation: [Developer checks and deterministic suite required for
  mechanical or presentation-only work.]
- L2 validation: [Independent test charter, completed independent test
  verification, and final independent review required for ordinary behavior
  changes and bug fixes.]
- L3 validation: [All L2 gates plus a user-approved oracle and the applicable
  E2E, device, security, or manual evidence required for high-risk work.]

Do not use the current implementation output as the sole expected value. Treat
existing tests as evidence that may be stale or coupled to implementation.

## Agent Test Ownership

- Developer agents may modify: [product paths and focused developer-test paths.]
- Independent test verifiers may modify: [explicit test, fixture, and
  test-support paths only.]
- Independent test verifiers must not modify: [product code, goal semantics, or
  assertions merely to obtain a pass.]
- Independent reviewers are read-only and receive no parent conclusions.

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

Default allowed:

- [Static reading and project-owned code or documentation edits.]
- [Fast deterministic lint, type, schema, or targeted test commands.]

Conditionally allowed when `AGENTS.md`, this document, another authoritative
project source, or the current user request explicitly allows the exact action:

- [Integration, preview, browser, simulator, container, or expensive suite.]
- [Commands that create or refresh project-owned generated outputs.]

Requires separate confirmation:

- [Release, deployment, signing, publishing, production, or external messaging.]
- [Account, payment, private-data, real-device, or mutable external-state flows.]

## Bug Reports

[List required environment/build/reproduction/evidence fields.]

## Related Fact Sources

[Link SPEC, AGENTS, LOCAL, PACKAGING, GENERATION.]
