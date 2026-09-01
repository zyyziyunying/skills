---
name: flutter-add-widget-test
description: Implement a component-level test using `WidgetTester` to verify UI rendering and user interactions (tapping, scrolling, entering text). Use when validating that a specific widget displays correct data and responds to events as expected.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Tue, 21 Apr 2026 21:15:41 GMT
---
# Flutter Widget Tests

## Scope and Setup

- Place tests under `test/` and name them `*_test.dart`.
- Use the package's existing `flutter_test` setup. If it is absent, add the
  dependency before authoring tests.

## Command Boundary

- **Default allowed:** static reading, code edits, `dart analyze`,
  `flutter analyze`, and targeted `flutter test test/...`.
- **Explicit project or user permission required:** `flutter test integration_test`,
  `flutter run -d web-server`, hot reload, and screenshot or preview checks.
- **Separate confirmation required:** real-device or simulator install/run,
  `flutter build`, release/package work, store, account, payment, or mutable
  backend-state flows.

## Test Oracle

Define assertions from the active goal, project fact sources, accessibility
requirements, and public widget contract before relying on the current widget
tree.

- Prefer observable content, state, navigation, focus, semantics, and
  interaction outcomes over private structure.
- Assert widget types, counts, keys, or callbacks only when they are stable
  contracts or required seams.
- Do not replace an expected result with current output merely to make a test
  pass.
- For a confirmed bug, model the pre-fix failure; show fail-before-fix and
  pass-after-fix only when a safe isolated baseline exists.

Developer-authored widget tests are implementation evidence, not the sole
acceptance evidence when an active workflow needs independent validation.

## Workflow

1. Bound one behavior and identify its authoritative expectation.
2. Build the widget with the inherited app context it actually needs, such as
   `MaterialApp`, localization, theme, or providers.
3. Locate stable public elements and assert the initial state.
4. Perform the user action, then pump only the frames needed for its update.
5. Assert the observable post-action result and relevant semantics or
   navigation outcome.
6. Run the narrowest relevant `flutter test test/...` command.
7. Classify a failure before editing: implementation failure, assertion/source
   conflict, specification ambiguity, or invalid harness/fixture.
8. Fix the responsible layer; change an assertion only when an authoritative
   source proves it is wrong. If the expected behavior remains ambiguous, stop
   and raise the product or specification question; do not guess or weaken the
   assertion. Otherwise re-run and report the command, outcome, and any unproven
   pre-fix behavior.

## Conditional Recipes

Read [widget-test-recipes.md](references/widget-test-recipes.md) only for text
input, scrolling, asynchronous or animated UI, or a compact worked example.
