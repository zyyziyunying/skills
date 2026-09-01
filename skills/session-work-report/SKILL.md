---
name: session-work-report
description: "Summarize substantial work from the current conversation into a concise, evidence-backed status report or handoff. Use when the user asks for a session recap, progress briefing, completion report, retrospective, or a visual summary of several workstreams; do not activate for an ordinary short final response."
---

# Session Work Report

## Outcome

Turn a long or multi-part conversation into a report that lets the reader quickly
understand the result, evidence, impact, and remaining work. Report in the
user's language unless they request another language.

By default, answer in the conversation. Do not create a document, publish a
page, send a message, or mutate project state unless the user explicitly asks.

## Establish The Record

Reconstruct the report from the current conversation, available conversation
summary, tool results, and relevant workspace artifacts. Inspect current files
or version-control state only when it resolves a material ambiguity; do not
repeat expensive work merely to produce the report.

Identify:

- the user's goal and the outcome reached;
- completed work, decisions, and meaningful changes;
- validation or other evidence actually observed;
- blockers, partial results, deferred work, and the most useful next action;
- artifacts or entry points the user is likely to open next.

Separate these states explicitly when they differ: **completed and verified**,
**completed but not verified**, **attempted or partial**, **not started**, and
**blocked**. Preserve exact commands, counts, paths, and test results only when
they are supported by the record. Do not turn a plan, intermediate update, or
tool start into a completed result.

If earlier context was compacted or unavailable, report from the available
record and disclose any material coverage limit instead of implying a complete
transcript audit. Distinguish changes made during the session from unrelated or
pre-existing workspace changes when that distinction matters.

## Shape The Report

Lead with the outcome and current status, not a chronological transcript. Scale
the structure to the amount and complexity of work:

- For a small recap, use a short outcome paragraph followed by evidence and any
  remaining action.
- For several workstreams, add a compact status table or grouped summary before
  details.
- For a handoff, emphasize current state, decisions and rationale, artifact
  locations, reproducible evidence, unresolved risk, and the next executable
  step.
- For an executive audience, foreground outcome, impact, risk, and decisions;
  keep implementation detail subordinate.

Prefer semantic grouping such as outcome, changes, evidence, and open items.
Include chronology only when sequence explains the result or a failure. Link
real local artifacts with absolute clickable paths when the interface supports
them. Omit empty sections and low-value activity logs.

End with the remaining risk or next action only when one exists. A completed
session should read as complete rather than ending with a generic offer to do
more.

## Choose A Visual Only When It Helps

Use the smallest visual that materially improves understanding and keep the
important conclusion in prose too:

- Use a Markdown table for exact status, ownership, before/after values, or
  repeated field comparisons.
- Use Mermaid `flowchart` for three or more connected workstreams,
  dependencies, decisions, or downstream effects.
- Use Mermaid `sequenceDiagram` when interactions or event order explain the
  outcome.
- Use Mermaid `stateDiagram-v2` when a small number of meaningful state
  transitions are central to the report.
- Use no visual for a flat list, a single change, or a short linear recap.

Keep Mermaid diagrams compact, normally within roughly 4–10 nodes. Use short
labels, avoid duplicating the surrounding prose, and do not put long paths,
commands, logs, or dense paragraphs inside nodes. Prefer broadly supported
Mermaid syntax and verify that node and participant names remain unambiguous.

## Evidence Integrity

- Attribute evidence to its source: tests, static analysis, runtime observation,
  diff inspection, external system, or user confirmation.
- State the scope of a check; a targeted test does not prove the whole system.
- Report failures and skipped checks close to the affected claim.
- Do not claim deployment, publication, delivery, external state, or complete
  process cleanup without direct evidence.
- Mention a breaking change prominently with affected API or behavior, callers,
  migration path, and documentation or tests that must stay synchronized.

## Final Check

Before sending, confirm that the report answers these questions without forcing
the reader to reconstruct the conversation:

1. What is the current outcome?
2. What materially changed or was decided?
3. What evidence supports the claims?
4. What remains uncertain, blocked, or next?

Remove repetition, unsupported certainty, decorative visuals, and details that
do not change the reader's understanding or next decision.
