---
name: flutter-implement-json-serialization
description: Use when implementing or modifying App API DTO parsing, API repository JSON mapping, JSON request bodies, or App API read-model serialization in the BesideYou Flutter app. Use AppApiGateway and AppApiJsonReader for App API work, preserve envelope/AppApiException semantics, and add focused fromJson/toJson tests when behavior changes. Do not apply by default to ARB/env/config files, runtime manifests, portrait-player manifests, third-party JSON contracts, or unrelated local JSON.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Sat, 23 May 2026 00:00:00 GMT
---
# BesideYou Flutter JSON Serialization

Use this skill for BesideYou App API JSON work:

- DTO `fromJson` / `toJson`
- repository mapping from App API `content`
- JSON request bodies
- App API-derived read models or persisted JSON
- focused parser/mapper tests

Do not use it as the default workflow for ARB, env/config JSON, runtime
manifests, portrait-player manifests, third-party contracts, or unrelated local
fixtures. Those belong to their owner module and keep that module's parser and
error semantics.

## Required Reading

For non-trivial edits, read:

1. `AGENTS.md` and `SPEC.md`
2. `lib/app/api/README.md` for App API transport/JSON rules
3. the nearest module `README.md` for the touched files
4. `../../packages/common/AGENTS.md` only when editing shared `package:common`

## Reference Routing

Read `references/implementation-patterns.md` when implementing or reviewing DTO `fromJson`, repository content mapping, App API list parsing, request-body `toJson`, or wire-name enum handling; after reading, choose the applicable parser/mapper pattern and identify the focused tests needed for the changed shape.

## Command Boundary

Use the Flutter command tiers for validation:

- Default allowed: static reading, code edits, `dart analyze`,
  `flutter analyze`, and targeted `dart test` / `flutter test test/...`
  commands.
- Conditionally allowed: `flutter test integration_test`,
  `flutter run -d web-server`, hot reload, and screenshot/preview checks only
  when the nearest `AGENTS.md`, `TEST.md`, or current user request explicitly
  allows the exact command.
- Separate confirmation required: real device or simulator install/run,
  `flutter build`, release/package work, store/account/payment flows, and
  mutable backend-state flows.

For this JSON skill, prefer the smallest parser, mapper, or repository tests
that cover the behavior change.

## Core Contract

BesideYou App API JSON is not generic HTTP JSON:

- repositories use injected `AppApiGateway`
- `AppApiGateway` owns Dio setup, auth, logging, envelope validation, error
  mapping, and `content` unwrapping
- repositories receive unwrapped `content`, not top-level `{code,msg,content}`
- DTO/read-model parsing uses `AppApiJsonReader`
- malformed App API response shapes surface as `AppApiException`

Avoid in App API work:

- `package:http`
- repository-level `jsonDecode(response.body)`
- raw `statusCode == 200` / `201` checks
- envelope parsing outside `AppApiGateway`
- generic `Exception` / `FormatException` for App API DTO parse failures
- defaulting every shape to `Map<String, dynamic>`

## Implementation Pattern

Use `Map<String, Object?>` for JSON objects and pass a request path/source label
through parsing. Repository mapping should stay relative to `API_BASE_URL` and
parse only unwrapped `content`. Use the reference routing above for concrete
DTO, list, request-body, and enum examples.

## Enums

Model wire names explicitly and parse with `AppApiJsonReader.enumField` or
`enumFromWireName`.

Unsupported App API enum values should become invalid-response
`AppApiException`s unless the nearest module README explicitly defines
forward-compatible fallback behavior.

## Local JSON Boundary

`dart:convert` is fine for local strings, fixtures, caches, and manifests. The
boundary is semantics, not file location:

- use `AppApiJsonReader` when local JSON intentionally mirrors App API
  DTO/read-model shapes
- preserve owner helpers and owner error semantics for runtime manifests,
  portrait-player manifests, third-party contracts, ARB, env/config, and
  owner-specific cache formats
- do not convert manifest `FormatException` or corruption handling into
  `AppApiException` just for consistency
- if manifest parsing needs cleanup, add a manifest-owner local helper and
  focused tests in that module

Do not offload parsing to `compute()` unless a measured jank risk justifies it.

## Tests

Add the smallest useful tests for changed behavior:

- DTO `fromJson`: required/optional fields, nested objects/lists, enums,
  malformed shapes
- request/read-model `toJson`
- repository mapping when endpoint path, gateway use, or envelope behavior
  matters

Run targeted tests only, for example:

```bash
flutter test test/app/api/app_api_json_reader_test.dart
flutter test test/app/pages/pet_create/data/pet_create_repository_test.dart
```

## Traceability

When this skill guides JSON implementation or tests, mention it in the final
response:

`已应用 skill: flutter-implement-json-serialization`

Also briefly name the touched DTO/repository/test files and verification.

Do not add skill markers, comments, metadata, or tracking fields to production
JSON, API payloads, DTO `toJson()` output, cache formats, tests, or business
code solely to record skill usage.

## Final Checks

- Keep business endpoint DTOs near their domain owner, not in `lib/app/api/`.
- Do not move BesideYou business API definitions into `packages/common`.
- If a Dart file now exceeds 2000 lines, add `// TODO 代码待拆分` after imports
  unless it already exists.
