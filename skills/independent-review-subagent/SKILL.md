---
name: independent-review-subagent
description: "Use only when the user explicitly invokes $independent-review-subagent. Opens a no-context-fork subagent for a bounded independent review/check/audit with only the scoped target and output requirements."
---

# Independent Review Subagent

## Purpose

Use this skill only when the user explicitly invokes `$independent-review-subagent`. It delegates a bounded read-only review/check/audit to a subagent while preserving independence. The default posture is: no context fork, minimal prompt, explicit scope, no parent conclusions, and no file edits.

## Trigger Contract

Require explicit invocation with `$independent-review-subagent`.

If the user asks for an "independent review" or similar wording without writing `$independent-review-subagent`, do not activate this skill. Treat the request as an ordinary review unless another active instruction applies.

## Workflow

1. Confirm the scope.
   - Use the user's provided files, directories, URLs, screenshots, diffs, or task boundaries.
   - If the scope is missing or ambiguous enough that the subagent could inspect the wrong target, ask one concise question.
   - Do not expand the scope unless the user asks for a broader review.

2. Spawn the subagent.
   - Use `fork_context: false`.
   - Use an `explorer` subagent for read-only review/check/audit.
   - Do not override the model unless the user explicitly asks for a model or there is a clear task-specific reason.
   - If the user asks the subagent to edit files, this skill no longer applies as a read-only review flow; use a worker-style delegation with explicit write ownership instead.
   - Treat no-context-fork explorer support as a hard precondition. If the runtime cannot spawn an explorer subagent, cannot set `fork_context: false`, or the spawn fails, stop and state that an independent subagent review is unavailable.
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
- <path, diff, URL, artifact, or bounded target>

输出：只列问题、风险和必要改进建议，按严重程度排序。每个 finding 必须包含 severity、证据路径/行号、风险理由和必要改进。如果没有问题，明确说明已检查范围和未覆盖范围。
```

For English-language tasks, use the same shape in English.

5. Handle the result.
   - Wait for the subagent when the user expects the review result in the current turn.
   - Relay the findings faithfully, preserving severity, evidence, and uncertainty. Prefer verbatim or structure-equivalent transfer over lossy summaries.
   - Close the subagent after it completes unless there is a clear reason to keep it open.
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
