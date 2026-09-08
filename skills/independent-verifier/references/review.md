# Independent Review

Use this mode for a bounded read-only code, diff, document, or artifact review.

## Target

- Prefer an explicit target from the user or owner workflow.
- Otherwise review current-session changes only when paths and hunks can be
  separated from pre-existing dirty work using a baseline, diff snapshot, or
  equivalent edit record.
- Do not silently review the whole working tree. If isolation is unreliable,
  ask whether the current dirty diff is the intended target.

## Review Criteria

Within the supplied scope, assess correctness and these maintainability concerns
where applicable; a runtime bug is not required for an actionable finding.

- **Code overengineering**: look for abstractions, indirection, configuration,
  extension points, or compatibility layers without a supported requirement;
  duplicated state or logic; and machinery whose maintenance cost exceeds its
  demonstrated benefit. Check actual callers, contracts, and project constraints
  before proposing simplification. A single caller or a long file alone does not
  prove overengineering. Identify a simpler alternative that preserves required
  behavior and boundaries; do not turn a scoped review into a broad redesign.
- **Documentation redundancy**: look for repeated instructions within or across
  documents, competing copies of mutable facts, and sections that add no distinct
  reader or workflow value. Check the designated source of truth and document
  audience. Keep mutable implementation details, behavior, validation status,
  and deferred items in that source; prefer boundaries, entry points, and links
  in higher-level documents. Cite the overlapping passages and recommend the
  authoritative location before consolidation. Useful summaries with links and
  intentional standalone references are not automatically defects.

Ground maintainability findings in a concrete cost such as extra change sites,
harder behavior tracing, conflicting instructions, or likely fact drift. Separate
them from correctness defects and optional style preferences. Do not invent user
harm or inflate severity to justify cleanup; omit unsupported taste-based advice.

## Prompt

Before delegating, resolve this rule file (`references/review.md`) against the
directory of the loaded `SKILL.md`, not the target project's working directory.
Replace `<absolute review rules path>` below with that resolved absolute path
and ensure the subagent can read it. Give the fresh subagent this information:

```text
Role: fresh independent verifier. Execute this mode directly; do not delegate
or invoke $independent-verifier again.

Independently review the following scope. Do not modify files.

Scope:
- <bounded target>

First read the review rules at `<absolute review rules path>`. Apply their
Review Criteria, including code overengineering and documentation redundancy
where applicable. If the file cannot be read, report the blocker rather than
claiming those criteria were checked.
Output only findings, risks, and necessary improvements, ordered by impact.
Each finding must include category (correctness, code complexity, or
documentation redundancy), severity with concrete impact, evidence path and
line, and the smallest necessary correction. Cite all relevant locations for
duplication findings. If there are no findings, state the checked and uncovered
scope.
```

Allow the reviewer to read nearby project instructions, specifications, API
contracts, or owner documentation that defines correct behavior.

## Result

Attribute findings to the reviewer and preserve their original assessment. If
the owner disagrees, distinguish that judgment and its supporting evidence from
the reviewer's result. State blockers and uncovered scope. If artifacts change
afterward, reassess affected findings and checks against the final state;
unrelated changes do not automatically require repeating the entire review.
