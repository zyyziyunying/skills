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

## Manual Validation

[List devices, browsers, hardware, manual commands, and evidence expectations.]

## Agent Boundary

[Say what Codex may run and what must be deferred.]

## Bug Reports

[List required device/build/repro/evidence fields.]

## Related Fact Sources

[Link SPEC, AGENTS, LOCAL, PACKAGING, GENERATION.]
