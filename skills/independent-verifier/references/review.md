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

Attribute findings to the reviewer and preserve their original assessment. If
the owner disagrees, distinguish that judgment and its supporting evidence from
the reviewer's result. State blockers and uncovered scope. If artifacts change
afterward, reassess affected findings and checks against the final state;
unrelated changes do not automatically require repeating the entire review.
