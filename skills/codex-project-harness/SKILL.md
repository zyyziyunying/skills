---
name: codex-project-harness
description: Create or maintain an agent-legible project harness for software repositories and workspace subprojects. Use when bootstrapping or refreshing AGENTS.md navigation, ARCHITECTURE.md, product specs, design docs, execution plans, TEST.md or quality policy, generated-doc boundaries, references, local setup, packaging, and mechanically verifiable project governance; includes project-specific guidance for Flutter repositories.
---

# Codex Project Harness

## Purpose

Build the repository environment that lets Codex discover authoritative facts,
execute work, validate results, and improve future runs. Treat documentation,
tools, architecture constraints, validation loops, and recurring maintenance as
one harness rather than as unrelated files.

Do not treat this as a runtime test-harness skill or as a request to generate a
large documentation tree unconditionally.

## Core Model

Apply these principles:

1. Use `AGENTS.md` as a short map and execution contract, not an encyclopedia.
2. Keep current project knowledge in versioned, repository-local fact sources.
3. Use progressive disclosure: start with a stable entry point and link to the
   narrowest relevant source.
4. Separate current facts, active plans, completed plans, generated content,
   external references, and machine-local state.
5. Turn important boundaries into executable checks when feasible. Do not rely
   on prose alone for architecture, naming, size, generation, or freshness rules.
6. Treat recurring agent failures as harness signals. Add the missing fact,
   tool, abstraction, diagnostic surface, or guardrail at the smallest durable
   boundary.
7. Schedule or document lightweight gardening for stale docs, architectural
   drift, quality gaps, and accumulated technical debt when the project needs it.

Read [references/harness-engineering.md](references/harness-engineering.md) when
choosing a knowledge layout, planning enforcement, or diagnosing why agents
cannot complete repository work reliably.

## Choose a Documentation Profile

Preserve an established project fact source unless it is demonstrably unclear
or duplicated. Choose the smallest profile that makes the repository navigable.

### Lightweight profile

Use for a small app, package, plugin, example, service, tool, or independent
workspace subproject. Prefer only the relevant subset:

- `AGENTS.md`: reading order, execution rules, command boundaries, validation.
- `SPEC.md`: stage, goals, non-goals, product behavior, compatibility posture.
- `TEST.md`: correctness sources, test scope, risk, evidence, command boundary.
- `DESIGN.md`: project-wide experience and interaction facts.
- `GENERATION.md`: generated-file ownership and regeneration rules.
- `LOCAL.md`: local setup, secrets, debug entry, machine-local state.
- `PACKAGING.md`: versioning, artifacts, signing, publishing, deployment.
- `ARCHITECTURE.md`: add when module boundaries or dependency direction are not
  obvious from the codebase.

### Scaled profile

Use when multiple domains, teams, long-running plans, or recurring drift make
root-level files hard to navigate:

```text
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/
│   ├── index.md
│   └── ...
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
├── product-specs/
│   ├── index.md
│   └── ...
├── references/
├── DESIGN.md
├── PLANS.md
├── QUALITY_SCORE.md
├── RELIABILITY.md
└── SECURITY.md
```

Create only directories and cross-cutting documents with real ownership and
current content. Do not create empty category files to imitate this layout.

### Hybrid profile

Use an existing `SPEC.md`, `TEST.md`, or other project fact source as the index
for its domain while moving only the detail that has outgrown it into `docs/`.
Keep one owner for each mutable fact and replace duplicated detail with links.

## Workflow

1. Read the nearest applicable `AGENTS.md` files and follow their command and
   documentation rules.
2. Inspect repository structure, project type, existing docs, scripts, CI,
   linters, tests, generators, and current dirty changes.
3. Identify the authoritative source for product behavior, architecture,
   validation, plans, generation, local setup, and release state. Flag ambiguity
   instead of silently creating a competing source.
4. Select the lightweight, scaled, or hybrid profile based on current complexity.
5. Create missing sources from the closest template, then replace placeholders
   with verified project facts. Preserve useful project-specific content.
6. Make `AGENTS.md` point to the relevant sources before edit or validation work.
7. Add or propose mechanical enforcement for high-value invariants. Write error
   messages with enough remediation context for an agent to act on them.
8. Verify links, commands, ownership, plan lifecycle, and generated/manual
   boundaries. Record intentionally deferred checks.

## Fact-Source Ownership

- `AGENTS.md` owns agent navigation and durable execution constraints. Keep it
  short and link outward rather than copying mutable facts.
- `ARCHITECTURE.md` owns the high-level domain map, layers, dependency direction,
  cross-cutting interfaces, and links to deeper design decisions.
- `SPEC.md` or `docs/product-specs/` owns current product behavior, stage,
  non-goals, compatibility, and acceptance facts.
- `DESIGN.md` or `docs/design-docs/` owns design principles and decisions.
- `TEST.md` or the established quality source owns correctness oracles, validation
  scope, risk level, test ownership, and required evidence.
- `docs/exec-plans/active/` owns complex work in progress. Move completed plans
  to `completed/`; do not let a plan masquerade as current behavior.
- `docs/generated/` contains generated knowledge. Record its source and refresh
  command; do not hand-edit outputs.
- `docs/references/` contains external or vendored context useful to agents.
  Record provenance and freshness; do not present it as project-owned truth.
- `LOCAL.md`, `GENERATION.md`, and `PACKAGING.md` own their operational domains
  when present. Keep secrets out of committed docs.

## Project Variants

For Flutter apps, packages, plugins, examples, or workspaces, read
[references/flutter.md](references/flutter.md) before writing command tiers,
device rules, generated-file behavior, or release boundaries.

For other ecosystems, derive commands and safety boundaries from the repository
itself. Do not transplant Flutter commands or approval assumptions into them.

## Template Use

Read only the templates needed for the selected profile:

- `assets/templates/AGENTS-reading-path.md`
- `assets/templates/ARCHITECTURE.md`
- `assets/templates/INDEX.md`
- `assets/templates/SPEC.md`
- `assets/templates/TEST.md`
- `assets/templates/DESIGN.md`
- `assets/templates/PLANS.md`
- `assets/templates/GENERATION.md`
- `assets/templates/LOCAL.md`
- `assets/templates/PACKAGING.md`

Replace bracketed placeholders and delete irrelevant sections. Never leave
generic template language in the target repository.

## Validation

Before finishing:

- Check target and parent workspace status when nested repositories or submodules
  are involved.
- Confirm every new link and documented command resolves from its stated scope.
- Confirm each mutable fact has one owner and indexes do not duplicate it.
- Confirm active/completed plan placement matches reality.
- Confirm generated content records provenance and regeneration behavior.
- Run available documentation, link, schema, lint, or structure checks that stay
  within the project's command boundary.
- State which enforcement or runtime checks were deferred and why.
