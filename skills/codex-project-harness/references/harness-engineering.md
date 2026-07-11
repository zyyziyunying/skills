# Harness Engineering Reference

Source: [Harness 工程：在智能体优先的世界中运用
Codex](https://openai.com/zh-Hans-CN/index/harness-engineering/), OpenAI,
2026-02-11.

Read this reference when selecting the repository knowledge layout, deciding
what should become a mechanical constraint, or diagnosing repeated agent
failure. It is a design basis, not a claim that every project needs OpenAI's
exact directory tree.

## Operational Lessons

- Optimize the environment around the agent: repository structure, tools,
  abstractions, diagnostics, feedback loops, and recovery paths.
- Give agents a map, not a monolithic manual. Keep `AGENTS.md` concise and route
  deeper knowledge through structured repository-local sources.
- Treat repository-local, versioned knowledge as the system of record for agent
  work. External documents and tacit decisions are unavailable unless captured
  or connected deliberately.
- Separate design history, active work, completed plans, generated knowledge,
  product behavior, external references, and cross-cutting engineering policy.
- Make important constraints mechanically verifiable through CI, linters,
  structural tests, schemas, or scripts. Include actionable remediation in
  failures.
- Expose the application and its behavior to agents through usable test,
  preview, logging, metric, trace, or browser interfaces when relevant.
- Capture recurring human judgment as durable rules and run periodic gardening
  against documentation drift, quality gaps, and architectural entropy.

## Scaling Heuristic

Start with the lightweight profile. Move to indexed directories when one or
more of these conditions hold:

- A root fact source mixes unrelated domains or has multiple owners.
- Long-running plans need progress and decision logs.
- Completed plans obscure current behavior.
- Generated reference material is frequently mistaken for maintained prose.
- Agents repeatedly miss relevant facts because navigation is ambiguous.
- CI can validate structure, freshness, ownership, or cross-links usefully.

Do not use repository size alone as the trigger. Prefer demonstrated navigation,
ownership, lifecycle, or drift pressure.
