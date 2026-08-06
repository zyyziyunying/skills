# Independent Review

Use this mode for a bounded read-only code, diff, document, or artifact review.

## Target

- Prefer an explicit target from the user or owner workflow.
- Otherwise review current-session changes only when paths and hunks can be
  separated from pre-existing dirty work using a baseline, diff snapshot, or
  equivalent edit record.
- Do not silently review the whole working tree. If isolation is unreliable,
  ask whether the current dirty diff is the intended target.

## Prompt

Give the fresh subagent only this information:

```text
Role: fresh independent verifier. Execute this mode directly; do not delegate
or invoke $independent-verifier again.

Independently review the following scope. Do not modify files.

Scope:
- <bounded target>

Output only findings, risks, and necessary improvements, ordered by severity.
Each finding must include severity, evidence path and line, risk, and the
smallest necessary correction. If there are no findings, state the checked and
uncovered scope.
```

Allow the reviewer to read nearby project instructions, specifications, API
contracts, or owner documentation that defines correct behavior.

## Result

Relay findings without upgrading or downgrading them. State whether blockers
were found and what remained outside the review scope. If reviewed artifacts
change afterward, the prior result no longer closes the review gate; review the
final state again.
