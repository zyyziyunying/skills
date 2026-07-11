---
name: expert-agent-team
description: "Orchestrate complex tasks with bounded expert subagents, explicit ownership, integration, and validation. Use when the user explicitly invokes $expert-agent-team, or when an explicitly activated owner workflow such as $goal-first-development delegates execution under a confirmed goal contract."
---

# Expert Agent Team

## Purpose

Use this skill as a deliberate manual front door for complex work where the user wants an expert-agent team style execution plan. The skill turns a prompt shaped like "启用专家级AGENT团队，执行 XXX" into a scoped workflow: task framing, optional user-named skill use, available/useful subagent delegation, local implementation, review, and validation.

Use this skill either as a manual front door or as the execution engine of an
explicitly activated owner workflow. When delegated, the owner workflow retains
goal lifecycle and completion authority.

## Trigger Contract

Allow activation through either:

1. Direct explicit invocation:

```text
$expert-agent-team 启用专家级AGENT团队，执行 <task>
$expert-agent-team 启用专家级AGENT团队，执行 <task>，借助 <optional skills or skill categories>
```

Accept equivalent wording after `$expert-agent-team`, including English prompts such as:

```text
Use $expert-agent-team to assemble an expert agent team for <task>.
Use $expert-agent-team to assemble an expert agent team for <task>, using $skill-a and $skill-b.
```

2. Internal delegation from an explicitly activated owner workflow, such as
   `$goal-first-development`, when that workflow has a confirmed goal contract
   and determines expert-agent execution is useful.

If the user says only "启用专家级AGENT团队..." without `$expert-agent-team`
and no owner workflow delegated it, do not activate this skill. Treat it as
ordinary natural language unless another active instruction applies.

## Workflow

1. Parse the command.
   - Extract the concrete task from the full explicit `$expert-agent-team` invocation. Accept Chinese forms such as "执行 <task>" and English forms such as "for <task>"; do not depend on a single keyword.
   - Treat "借助 <skills>", "using <skills>", and explicit skill mentions as optional user-named skills. If omitted, do not force additional optional skill use.
   - If the user names skills, load only those that are installed and relevant.
   - If no optional skills are named, do not infer optional skills just to fill the workflow; briefly remind the user they may name skills when they want them involved, then continue without extra optional skill loading.
   - When invoked by an owner workflow, treat skills required by the confirmed
     goal's validation contract as owner-required components rather than
     unnamed optional skills.
   - Do not use the optional-skill rule to suppress skills that higher-priority instructions, installed skill trigger rules, or the task itself require.
   - Separate required output, constraints, write scope, validation expectations, and deadline or cost constraints.
   - When delegated by a goal owner, read the active `goal.html` first. Treat
     its frozen goal, non-goals, behavior, correctness sources, and Check
     criteria as authoritative. Do not edit or reinterpret them.
   - Ask one concise blocking question only when the target, write permission, or scope cannot be inferred safely.

2. Load optional skill instructions.
   - For each selected or otherwise required installed skill, follow the normal skill-loading contract: read its `SKILL.md` completely, then read any directly referenced resources required for the current task.
   - It is valid to use no additional skills.
   - Do not scan or evaluate unnamed optional skills just to fill the workflow.
   - Respect each selected skill's trigger rules. Only discuss skipped explicit-only skills when the user named that skill/category or explicitly asked to evaluate available skills.
   - Let repository instructions, user instructions, and active project docs override generic skill guidance.

3. Decide the agent team shape.
   - Use subagents only when the current runtime provides subagent/task tooling and the task has bounded parallel work. If subagent tooling is unavailable or delegation is not useful, execute serially in the main session and state that no subagent delegation was used.
   - Keep immediate critical-path work local.
   - Spawn subagents only for bounded sidecar tasks that can run in parallel, such as independent codebase questions, disjoint implementation slices, or final review.
   - Do not force independent test design onto a parallel side path. In a shared
     working tree, complete it before implementation begins unless it uses an
     isolated baseline.
   - Do not duplicate work between the main agent and subagents.
   - For read-only questions, use explorer agents with narrow prompts.
   - For code changes, use worker agents only with explicit, disjoint file or module ownership. Do not spawn overlapping write scopes.
   - Before spawning any write-capable worker, record the dirty-worktree baseline for its owned scope, such as `git status --short` and the relevant path diff when a VCS is available. If no VCS baseline exists, state that explicitly and use file-level inspection before and after the worker returns.
   - Tell workers to preserve existing user and other-agent changes, stay inside their owned scope, and report any out-of-scope change they believe is required instead of editing it.
   - The main session owns final patch review, conflict checks, integration, and validation before reporting completion.
   - When an owner workflow delegated the task, the main session owns patch
     integration and evidence collection, while the owner workflow retains the
     decision to mark the goal done.
   - Give subagents enough uninterrupted time to complete their scoped work. Do not short-poll,催促, or interrupt them unless the user changes direction, the subagent is clearly off-scope, or there is a concrete safety problem.

4. Announce the concise execution contract.
   - State the parsed task.
   - List user-named skills and why each applies, or state that no extra skill was specified and remind the user they can name skills when needed.
   - List planned subagents, their ownership, and whether they are read-only or write-capable.
   - State what the main agent will do locally while subagents run.
   - State the first validation target.

5. Execute.
   - For an L2/L3 goal, ensure the independent test charter already exists
     before implementation. If it is missing, return control to the owner
     workflow instead of inventing one from the implementation.
   - Start useful subagents early when they do not block the next local step.
   - Continue local inspection or implementation while subagents run.
   - Wait for subagents only at integration gates where their output is actually needed. Prefer one deliberate wait over repeated short waits.
   - Review returned findings or patches before trusting them.
   - Inspect worker changes against the recorded owned-scope baseline before accepting them, resolve or reject conflicting edits, run the selected validation, and report any worker output that was ignored or not integrated.
   - Integrate only changes that fit the active project rules and the user's request.
   - Developer workers may write focused developer tests. A delegated Test
     Verifier may modify only its explicit test/fixture/test-support ownership
     and must not edit product code or weaken assertions.

6. Validate and finish.
   - Run the strongest practical validation allowed by active project instructions.
   - For L2/L3, require the independent verification and review results declared
     by the owner goal. Do not present developer-authored tests as the sole
     correctness evidence.
   - Preserve independent blockers in the handoff. Resolve them with evidence
     or return them to the owner; do not silently downgrade them.
   - If validation is blocked by policy, environment, missing credentials, or user-owned device/runtime checks, state the strongest completed check and the remaining blocker.
   - Confirm all launched subagents are completed, cancelled, or no longer awaited.
   - Close completed or no-longer-needed subagents when the runtime provides a close operation, then report any unavailable, ignored, or not-integrated output.

## Prompt Templates

Use this shape for explorer agents:

```text
独立检查以下范围，不要修改文件。

任务：
- <specific question>

范围：
- <files, directories, diffs, docs, or artifacts>

输出：只给结论、证据路径和风险；按重要性排序。如果没有发现问题，明确说明。
```

Use this shape for worker agents:

```text
你不是唯一在改这个代码库的代理。不要还原他人的修改；遇到并行变更时调整你的实现来兼容。
主会话负责最终集成和验证。你只能修改写入范围内的文件；如果发现范围外也需要修改，只报告，不要直接改。
主会话会用委派前的 owned-scope baseline 复核你的改动；不要修改未授权路径。

任务：
- <specific implementation task>

写入范围：
- <owned files or modules only>

约束：
- <project rules, validation limits, behavior contract>

完成后输出：改动文件、关键实现点、已运行验证、未验证风险。
```

## Response Shape

Before substantive execution, send a short execution contract. Do not wait for confirmation unless there is a blocking ambiguity, a write/scope risk, or an active project rule requires approval.

Short execution contract:

- parsed task
- selected skills
- planned expert agents and ownership
- local critical-path work
- validation target

After execution, respond with:

- whether the task was completed
- changed files or artifacts
- subagent findings that affected the result
- validation performed
- remaining risk or user-side checks
- owner-workflow handoff status when the team was internally delegated
