---
name: independent-verifier
description: "Provide a focused second-pass review, bug-validity and severity triage, pre-implementation test design, or post-implementation test verification. Use when the user invokes $independent-verifier, asks for an independent review or test verification, asks whether a reported bug is real or worth fixing, or when an owner workflow delegates one of these modes. Prefer a fresh no-context subagent when useful, but allow a clearly labeled direct fallback when delegation is unavailable or disproportionate."
---

# Independent Verifier

## Result

Return a focused correctness signal grounded in the scoped artifacts and their
authoritative facts. Keep the verification proportionate to the decision rather
than forcing the same ceremony on every task.

This skill does not own implementation, redefine an active goal, or decide an
owner workflow's final status.

## Choose A Mode

- **Review**: inspect a diff, code, document, or artifact. Read
  [review.md](references/review.md).
- **Bug value**: judge whether behavior is defective and worth fixing. Read
  [bug-value.md](references/bug-value.md), plus
  [severity-rubric.md](references/severity-rubric.md) when a P0-P3 label matters.
- **Test design**: derive a behavior-focused charter before implementation. Read
  [test-design.md](references/test-design.md).
- **Test verification**: inspect or execute tests after implementation. Read
  [test-verification.md](references/test-verification.md).

Infer the mode and target from the request and available artifacts. Ask only
when a wrong assumption would materially change the result.

## Choose The Verification Shape

- Prefer a fresh subagent without inherited conversation context when a real
  second opinion adds value and the runtime supports it. Use
  `fork_turns: "none"`, `fork_context: false`, or the documented equivalent;
  otherwise treat the result as direct rather than independent.
- Give a fresh verifier neutral artifacts, fact sources, scope, and permissions;
  do not preload it with the caller's verdict or preferred fix.
- If the current agent is explicitly the fresh verifier, execute the selected
  mode directly and do not delegate again.
- For a small self-contained task, or when delegation is unavailable, verify in
  the current agent and label the result as direct rather than independent. Do
  not claim separation that did not occur.

## Keep Useful Boundaries

- Use the user- or owner-supplied target. A request to review current changes is
  sufficient authority to inspect the current staged, unstaged, and untracked
  diff; ask only when pre-existing work makes the intended scope genuinely
  unclear.
- Keep review and bug-value modes read-only. Test-design or test-verification
  modes may edit only explicitly authorized test, fixture, or test-support paths.
- Never edit product code from a verifier role, weaken assertions merely to pass,
  or silently expand product behavior or write scope.
- Derive expected behavior from authoritative facts rather than current output.

Return findings, classification, evidence, commands, uncertainty, and uncovered
scope at the level useful for the decision. When delegated by an owner workflow,
return the result to that owner without changing the goal contract or status.
