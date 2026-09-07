---
name: dart-add-unit-test
description: Write and organize unit tests for functions, methods, and classes using `package:test`. Use when creating new logic or fixing bugs to ensure code remains correct and regression-free.
---
# Dart Unit Tests

## Scope and Command Boundary

- Mirror the target library under `test/` and end filenames with
  `_test.dart`. Put integration tests in `integration_test/`.
- Use `package:test/test.dart` for Dart; Flutter tests may use
  `package:flutter_test/flutter_test.dart`.
- For a pure Dart package, use targeted `dart test test/...`; for Flutter,
  use targeted `flutter test test/...` with relevant analysis checks.
- Derive validation commands and execution constraints from the applicable
  project instructions and user request. Continue already authorized steps
  without repeat approval; do not expand unit-test work into unrelated release
  or external-state operations.

## Test Oracle

Derive expected behavior from the active goal, project fact sources, domain or
API contracts, and confirmed user-visible behavior before writing assertions.

- Existing tests are evidence, not automatic truth.
- Prefer observable results, state, errors, and boundary contracts over private
  structure or call counts; assert interactions only when they are contractual.
- Never copy current implementation output into an expected value just to turn a
  test green.
- For a confirmed bug, encode its pre-fix failure. Demonstrate fail-before-fix
  and pass-after-fix only when a safe isolated baseline exists; otherwise report
  that the pre-fix proof is unverified.

Developer-authored unit tests are implementation evidence, not the only
acceptance evidence when an active workflow needs independent verification.

## Workflow

1. Bound the target behavior and its authoritative expectation.
2. Create the mirrored test file; group related cases and initialize only the
   fixtures or fakes the contract needs.
3. Cover normal, boundary, error, and asynchronous behavior that is relevant to
   the change.
4. Run the narrowest suitable test command.
5. Classify a failure before editing: implementation failure, assertion/source
   conflict, specification ambiguity, or invalid environment/fixture.
6. Fix implementation when it violates the contract. Change an assertion only
   when an authoritative source proves it wrong; otherwise surface the product
   question.
7. Re-run the targeted suite and report its result, the governing fact source,
   and any unproven pre-fix behavior.

## Conditional Recipes

Read [unit-test-recipes.md](references/unit-test-recipes.md) for a compact
`group`/`setUp` example, async and error patterns, or project-approved
Mockito generation.
