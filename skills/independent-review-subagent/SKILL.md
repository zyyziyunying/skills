---
name: independent-review-subagent
description: "Open a no-context-fork subagent for a bounded read-only independent review, check, or audit. Use when the user explicitly invokes $independent-review-subagent, or when an explicitly activated owner workflow such as $goal-first-development delegates the final independent review required by its confirmed validation contract."
---

# Independent Review Subagent

## Purpose

Use this skill when explicitly invoked or delegated by an explicitly activated
owner workflow. It delegates a bounded read-only review/check/audit to a
subagent while preserving independence. The default posture is: no context
fork, minimal prompt, bounded scope, no parent conclusions, and no file edits.

## Trigger Contract

Allow activation through either:

1. Explicit invocation with `$independent-review-subagent`.
2. Internal delegation from an explicitly activated owner workflow when its
   confirmed validation contract requires a final independent review.

If the user asks for an "independent review" or similar wording without writing
`$independent-review-subagent` and no owner workflow delegated it, do not
activate this skill. Treat the request as an ordinary review unless another
active instruction applies.

## Workflow

1. Confirm the scope.
   - Use the user's provided files, directories, URLs, screenshots, diffs, or task boundaries.
   - If the user provides no explicit target, default to reviewing the current session's changes in the active repository or workspace only when those changes can be reliably isolated from pre-existing dirty work.
   - Build that default target from neutral local evidence that isolates current-session touched paths and hunks: a session-start baseline or diff snapshot, hunk-level tool edit record, or equivalent evidence covering edited, created, deleted, renamed, and moved paths.
   - A path list alone is not enough for files that might already be dirty. With only path-level evidence, ask one concise question to confirm the target or whether to review the current dirty diff for those paths.
   - When using the default target, pass only the isolated paths, hunks, diffs, or necessary file contents to the subagent; do not pass parent-thread reasoning, conclusions, suspicions, or conversation history.
   - If current-session changes cannot be separated from pre-existing dirty work, same-file mixed edits, or no local changed target exists, ask one concise question.
   - Do not expand the scope unless the user asks for a broader review.
   - Do not silently review the whole working tree unless it is the confirmed or clearly current-session scope.

2. Spawn the subagent.
   - Use the current runtime's no-context-fork mechanism. In Codex runtimes that
     expose `fork_turns`, use `fork_turns: "none"`; in runtimes that expose
     `fork_context`, use `fork_context: false`.
   - Use a read-only/explorer subagent when the runtime exposes agent roles;
     otherwise enforce read-only behavior in the sparse prompt.
   - Do not override the model unless the user explicitly asks for a model or there is a clear task-specific reason.
   - If the user asks the subagent to edit files, this skill no longer applies as a read-only review flow; use a worker-style delegation with explicit write ownership instead.
   - Treat no-context-fork subagent support as a hard precondition. If the
     runtime cannot spawn a subagent without inherited conversation context, or
     the spawn fails, stop and state that an independent subagent review is
     unavailable.
   - Do not simulate independence in the main thread. Continue only if the user accepts an ordinary non-independent review, and label it as non-independent.

3. Keep the prompt sparse.
   - Include only the review task, scope, mutation policy, and desired output shape.
   - Do not pass the parent agent's prior analysis, suspicions, intended fixes, preferred answer, or conversation history.
   - Do not tell the subagent what issues to find unless the user explicitly defines those as the review scope.
   - Allow the subagent to independently read neutral fact sources required by the scoped target, such as `AGENTS.md`, `SPEC.md`, owner README files, API docs, or provided artifacts. This is not scope expansion when those sources define the expected behavior.
   - Do not summarize those fact sources from the parent thread; let the subagent inspect them directly.
   - Include hard constraints only when needed to prevent wrong behavior, such as "do not modify files" or "do not fork context" already being represented by tool parameters.

4. Use this prompt shape by default.

```text
独立审核以下范围，不要修改文件。

范围：
- <explicit target, or reliably isolated current-session changes; otherwise confirmed target/current dirty diff>

输出：只列问题、风险和必要改进建议，按严重程度排序。每个 finding 必须包含 severity、证据路径/行号、风险理由和必要改进。如果没有问题，明确说明已检查范围和未覆盖范围。
```

For English-language tasks, use the same shape in English.

5. Handle the result.
   - Wait for the subagent when the user expects the review result in the current turn.
   - Relay the findings faithfully, preserving severity, evidence, and uncertainty. Prefer verbatim or structure-equivalent transfer over lossy summaries.
   - Close the subagent after it completes when the runtime provides a close
     operation. Otherwise leave no pending follow-up work and report completion.
   - Do not silently treat subagent findings as ground truth when they conflict with higher-priority project rules or direct evidence; state the conflict and resolve it in a separately labeled main-thread review or decision.

## Response Shape

When starting:

- state that a no-context-fork independent review subagent has been opened
- state the scoped target briefly
- if opening one is impossible, state that the independent review could not be performed and do not claim the skill completed

When finished:

- relay the subagent's findings faithfully
- state whether it found blockers
- close the subagent
