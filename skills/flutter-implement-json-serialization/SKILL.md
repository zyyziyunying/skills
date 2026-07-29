---
name: flutter-implement-json-serialization
description: Implement, review, or migrate JSON serialization in Flutter or Dart models, API DTOs, request bodies, and persisted data. Use to choose a project-approved generated, hybrid, or manual strategy; adopt or reuse JSON code generation; preserve existing wire, validation, error, and compatibility semantics; and add focused serialization tests. Read the project Harness before changing tooling or contracts.
---

# Flutter JSON Serialization

## Decide From Project Facts

Read the nearest `AGENTS.md` and the authoritative owner sources for the touched
API, persistence, cache, or local-data boundary. Choose:

- `generated` for approved tooling and stable, mostly one-to-one fields;
- `hybrid` for generated field mapping plus handwritten normalization,
  validation, error translation, fallback, or domain conversion;
- `manual` for small, dynamic, polymorphic, security-sensitive, or conditional
  contracts.

Optimize recurring cost, not handwritten line count. Project facts override
these examples.

For migration or adoption, inspect generation/test policies, `pubspec.yaml`,
the lockfile, optional `build.yaml`, nearby sources/outputs, callers, and tests.
Record a Serialization Context Receipt:

- owner, data boundary, and accepted/emitted wire contract;
- direct dependencies and established serialization convention;
- parity rules for types, missing/null, normalization, aliases, defaults,
  enums, unknown fields, conditional output, errors, and source context;
- selected strategy, compatibility posture, command/output policy, freshness
  enforcement, tests, and allowed commands.

Share it for adoption, broad migration, or a breaking decision. Never infer
generator adoption from `build_runner` or a transitive package. Update the
authoritative Harness when the contract or generator policy changes.

## Route References

- Read [references/serialization-strategy.md](references/serialization-strategy.md)
  for adoption, library choice, migration, cohort selection, or Harness
  ownership.
- Read [references/implementation-patterns.md](references/implementation-patterns.md)
  for generated/hybrid code, converters, nested models, errors, requests,
  enums, or parity tests.
- Read both for an implementation that also adopts or migrates a generator.

Routine manual mapping should follow the nearest established owner pattern
without loading either reference.

## Preserve Owner Semantics

Generation owns mechanical conversion only. Keep project transport, envelope,
storage corruption, validation, and error boundaries outside generated code.

Preserve the existing contract through annotations, tested converters, a small
adapter, or manual mapping. Generated casts do not automatically preserve:

- integer-only versus numeric coercion;
- trim, required-nonblank, or optional blank-to-null behavior;
- missing-key versus explicit-`null` behavior;
- alias priority, enum fallback, unknown-field policy, or conditional output;
- project exception type and endpoint/path/record/source context.

Do not leak generator failures through a public boundary that defines another
error type.

## Adopt Generation Deliberately

Reuse the owner's generator. Introduce a new stack only for an explicit cohort.
Treat dependencies, configuration, command, outputs, commit policy, freshness,
Harness updates, and tests as one adoption change.

Start with a bounded pilot and inspect both source and generated diffs before
scaling. Never hand-edit generated output. Treat machine-generated files as
exempt from handwritten source-size TODO markers and enforce that exemption in
the project Harness; handwritten sources remain covered.

## Respect Request And Format Boundaries

Generate request `toJson` only for mechanical projection. Keep it manual when
it normalizes input, conditionally omits or flattens keys, chooses mutually
exclusive or legacy keys, or enforces write, entitlement, account, payment, or
security rules. Test the exact payload.

For caches, manifests, configuration, ARB, third-party contracts, and fixtures,
follow the format owner's parser and failure semantics. Do not impose an API DTO
generator on a schema- or tool-owned format without owner approval.

## Validate And Report

Use the project-approved commands and the applicable parity matrix from the
references. Verify observable wire behavior, project error translation, source
context, and generated-output freshness rather than generated boilerplate
itself. Run only Harness- or user-approved generation and dependency commands.

Treat changes to public factories, accepted inputs, emitted keys, missing/null,
normalization, unknown-value policy, errors, or persisted shapes as potentially
breaking. State affected behavior and callers, migration or rollback, and
required test/doc updates prominently.

When this skill guides implementation or review, include:

`已应用 skill: flutter-implement-json-serialization`

Report the selected strategy, touched code and Harness sources, generated
outputs, and validation. Never add skill markers or tracking fields to product
JSON, source code, generated output, fixtures, or tests.
