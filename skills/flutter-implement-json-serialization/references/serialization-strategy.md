# Flutter JSON Serialization Strategy

Choose the strategy before editing a model. Prefer generation when it removes
recurring mechanical work without moving transport, validation, compatibility,
or domain rules into opaque callbacks.

## Contents

[Decision Matrix](#decision-matrix) ·
[Generated Eligibility](#generated-eligibility) ·
[Manual Or Hybrid](#prefer-manual-or-hybrid-mapping-when) ·
[Library Selection](#library-selection) ·
[Bounded Experiment](#bounded-adoption-experiment) ·
[Adoption Gates](#adoption-gates) ·
[Harness Ownership](#harness-ownership) ·
[Breaking Changes](#breaking-change-review)

## Decision Matrix

| Strategy | Choose when | Keep handwritten |
| --- | --- | --- |
| Generated | A coherent model group has stable, mostly one-to-one fields and the project already owns or explicitly adopts the generator. | Transport/storage boundary, source context, domain validation, and project error normalization. |
| Hybrid | Most fields are mechanical, but some require normalization, aliases, strict enums, cross-field rules, or compatibility behavior. | A small adapter or converters that make those semantics explicit and tested. |
| Manual | The model is small or isolated, dynamic/polymorphic, or dominated by semantic parsing or conditional output. | The complete owner parser or serializer. |

Include generator setup, regeneration, generated-diff review, CI freshness, and
migration risk when comparing maintenance cost.

## Generated Eligibility

Use generated mapping only when all applicable conditions hold:

- Select a coherent owner-local cohort or recurring model pattern.
- Confirm most fields map mechanically, including ordinary nested objects,
  lists, nullable fields, and explicit wire names.
- Preserve accepted inputs, emitted keys, defaults, normalization, and failure
  behavior through annotations, converters, or an adapter.
- Keep transport envelopes, storage corruption handling, and domain validation
  at their project-owned boundaries.
- Keep endpoint, path, record, or source context available where the public
  failure contract requires it.
- Normalize expected generator failures into the project error contract.
- Approve direct dependencies, configuration, command, outputs, commit policy,
  and freshness enforcement before production migration.
- Add focused tests for the wire contract and retained semantic rules.

When a generator is already an approved owner convention, follow it for new
eligible models. Do not create a second serialization style inside one owner
without a deliberate migration boundary.

## Prefer Manual Or Hybrid Mapping When

Keep semantic work outside full generation when any of these dominates:

- legacy aliases or ordered fallback keys;
- trimming, nonblank, blank-to-null, range checks, or cross-field rules;
- fail-closed fields controlling navigation, payment, writes, entitlement,
  security, or runtime behavior;
- owner-defined fallback for unknown enums or advisory reason values;
- field-level source/path diagnostics the generator cannot retain;
- polymorphic or versioned payloads with meaningful shape discrimination;
- conditional request-key omission or mutually exclusive keys;
- a small isolated model where adoption costs more than the mapping removed.

Do not hide extensive business logic in converters merely to label a model
fully generated. Prefer a private generated wire model plus a readable adapter
when that makes ownership clearer.

## Library Selection

- Prefer `json_serializable` for ordinary Dart classes when adopting
  regular-class code generation.
- Use Freezed when the owner also needs its value-model, union/sealed-state,
  equality, or `copyWith` capabilities; do not add it only for JSON.
- Use `built_value` inside an existing builder/serializer architecture.
- Use `dart_mappable` where it is already an intentional owner convention.
- Follow any other established project generator rather than adding a parallel
  stack for one cohort.

Library features do not define the project contract. Checked conversion,
renaming, defaults, enum annotations, and converters help implement behavior;
the Harness and owner tests still decide which behavior is correct.

## Bounded Adoption Experiment

Do not justify adoption with assumed token savings. Compare a bounded pilot with
the handwritten baseline:

1. Select one coherent, low-risk response or persistence model cohort. Inventory
   factories, callers, semantic rules, handwritten mapping, and focused tests.
2. Implement the smallest generated or hybrid seam together with dependency,
   generation-policy, and freshness changes. Regenerate from a clean checkout.
3. Record evidence separately for:
   - agent-authored source and mapping volume;
   - model-output tokens only when reliable telemetry exists;
   - implementation, regeneration, review, and focused-validation time;
   - handwritten review surface versus generated diff volume;
   - missing/null, strict-type, normalization, alias, enum, error, and source
     context parity;
   - clean-checkout reproducibility and stale-output detection;
   - one representative follow-up schema change, when safe.
4. Scale only when behavior is preserved and recurring authoring/review cost
   falls enough to offset builder and CI ownership. Keep a hybrid boundary or
   roll back when it is clearer and cheaper.

Keep experiment evidence in the project plan or goal source. Move only accepted
current policy into durable Harness sources.

## Adoption Gates

### Dependency

- Inspect workspace dependency policy and SDK constraints.
- Add runtime annotations and builders as direct dependencies in the correct
  sections; a transitive package or unrelated `build_runner` is not adoption.
- Update the resolved lockfile through the project workflow.
- Review build-time cost and conflicts with existing builders.

### Generation

- Record sources, outputs, deterministic command, commit-or-ignore policy, and
  generated-file ownership in the project's generation fact source.
- Edit source annotations, models, adapters, and configuration; never hand-edit
  generated output.
- Do not run generation as broad cleanup or install global tooling implicitly.
- Exempt machine-generated output from handwritten source-size TODO markers.
  Teach the project checker how to recognize generated paths or suffixes;
  oversized handwritten sources remain covered.

### Commit And CI

Choose and document one output policy:

- If outputs are committed, regenerate and require a clean diff in CI.
- If outputs are ignored, generate before analysis and tests in every clean CI
  checkout.

In either case, add a project-owned stale-output check, keep source and output
changes in the same logical commit, and report the exact commands used.

## Harness Ownership

Write each mutable fact once:

- `AGENTS.md` or equivalent: reading order and durable command boundary.
- API/persistence/module owner source: transport, envelope, error, field, and
  compatibility semantics.
- `GENERATION.md` or equivalent: builders, sources, outputs, commands, commit
  policy, generated-file exemptions, and freshness enforcement.
- `TEST.md` or equivalent: serialization scope, CI checks, and required
  evidence.
- active goal or plan: experiment evidence, open decisions, rollout, and
  rejected alternatives.

Use existing project filenames and owners when they differ. Upper-level
navigation should link to mutable facts instead of copying them.

## Breaking-Change Review

Before replacing a parser or serializer, compare:

- missing key versus explicit `null`;
- strict type rejection versus coercion;
- trimming, blank strings, numeric bounds, and cross-field validation;
- alias priority and deprecated wire names;
- unknown enum and reason fallback;
- unknown-field acceptance;
- defaults and nested collection failures;
- emitted key names, `null` inclusion, conditional omission, and enum encoding;
- exception type, failure classification, and source/path context;
- persisted-data compatibility and public factory call sites.

Treat intentional differences as potential breaking changes. State the affected
API or behavior, callers, migration or rollback, and test/doc updates. A
generator-only refactor is complete only after focused tests demonstrate
equivalence or the approved breaking contract.
