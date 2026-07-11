---
name: independent-test-verifier
description: "Design and execute independent behavior-focused tests from an active goal or authoritative specification without treating the implementation as the oracle. Use when explicitly invoked, or when an explicitly activated owner workflow such as $goal-first-development delegates L2/L3 test design or test-only verification for a behavior change, regression, or bug fix."
---

# Independent Test Verifier

## Purpose

Provide a verification path that is independent from the developer's reasoning.
Derive expected behavior from the active goal and authoritative fact sources,
freeze a test charter before implementation when practical, then verify the
finished change without editing product code or weakening assertions.

This skill is a component, not a goal owner. It returns a test charter and
verification evidence to the invoking workflow; the owner workflow maintains
`goal.html` and decides status.

## Activation Contract

Use this skill when either:

1. The user explicitly invokes `$independent-test-verifier` and provides a
   goal, specification, or bounded target.
2. An explicitly activated owner workflow delegates independent verification
   under its confirmed goal contract.

Do not activate it merely because an ordinary development task includes unit
tests. Developer-authored tests remain part of normal implementation. Use this
skill for a separate correctness signal.

## Authority And Independence

- Treat `goal.html`, declared project fact sources, product requirements, API
  contracts, and platform rules as sources of expected behavior.
- Treat existing tests as evidence, not automatic truth. They may encode stale
  requirements or implementation details.
- Never derive an expected value only from the current implementation output.
- Do not pass the developer's reasoning, preferred fix, conclusions, or hidden
  answer into the verifier prompt.
- Prefer a no-context-fork subagent. Use `fork_turns: "none"` when that is the
  runtime's no-context mechanism, or the closest documented equivalent.
- For high-risk work, prefer model/provider diversity when the runtime offers
  it, but do not claim model diversity removes correlated-error risk.

## Select A Mode

### Test Design

Use before implementation for L2/L3 work when the behavior contract is stable.

1. Read only the active goal, authoritative fact sources, public contracts, and
   a reliable pre-change baseline.
2. Do not inspect a concurrently changing implementation. In a shared working
   tree, finish test design before development starts unless an isolated
   worktree or immutable snapshot is available.
3. Produce a compact test charter covering:
   - observable acceptance behavior;
   - negative and boundary cases;
   - invariants or properties;
   - regression scope;
   - required fixtures, mocks, devices, or environments;
   - for bug fixes, the expected pre-fix failure signal.
4. Return the charter to the owner workflow for inclusion in the active
   `goal.html` Check section. Do not create another active truth source.

Test Design is read-only unless the user explicitly asks for test-first files
and the owner workflow grants a test-only write scope.

### Test Verification

Use after implementation, with the frozen charter as the primary contract.

1. Inspect the final diff, relevant implementation, developer tests, and the
   frozen charter.
2. Reuse the Test Design subagent when it was kept alive and remains independent;
   otherwise open a fresh no-context verifier with the charter and neutral fact
   sources only.
3. If test changes are authorized, restrict writes to explicitly owned test,
   fixture, and test-support paths. Do not edit product code.
4. Run the smallest strong validation permitted by project rules.
5. For a bug fix, prove the new regression test fails against the pre-fix
   baseline and passes against the patch when a safe isolated baseline is
   available. Never use destructive checkout or overwrite user changes to
   manufacture this proof. If it cannot be demonstrated safely, report it as
   unproven.
6. Classify the result as `pass`, `implementation failure`, `spec conflict`, or
   `environment blocked`.

## Mutation Rules

The verifier must not:

- edit application or production source files;
- delete, skip, loosen, or rewrite assertions merely to make tests pass;
- replace an expected value with the current observed value without an
  authoritative source;
- expand product behavior beyond the confirmed goal;
- silently resolve a specification conflict;
- mark the owner goal done.

When a test fails, determine whether the implementation violates the contract,
the test conflicts with an authoritative source, the contract is ambiguous, or
the environment is invalid. Report the classification and evidence instead of
guessing.

## Default Subagent Prompt

```text
独立验证以下目标，不要继承开发者的分析或结论。

事实源：
- <active goal.html>
- <authoritative project sources>

冻结的测试章程：
- <charter, or "derive before implementation">

范围：
- <bounded code/test paths or diff>

权限：
- 只读；或仅可修改明确列出的测试路径
- 不得修改产品代码、弱化断言或自行改变验收标准

输出：测试场景或验证结论、证据、已运行命令、未覆盖范围，以及 pass / implementation failure / spec conflict / environment blocked。
```

## Response Shape

For Test Design, return:

- authoritative behavior sources
- frozen test charter
- expected pre-fix failure for bug work
- environment or fixture needs
- unresolved specification questions

For Test Verification, return:

- result classification
- tests added or inspected
- commands and outcomes
- pre-fix failure proof status
- product-code write confirmation: none
- remaining risk or uncovered scope
