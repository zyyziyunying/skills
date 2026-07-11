---
name: dart-add-unit-test
description: Write and organize unit tests for functions, methods, and classes using `package:test`. Use when creating new logic or fixing bugs to ensure code remains correct and regression-free.
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Fri, 24 Apr 2026 15:07:58 GMT
---
# Testing Dart and Flutter Applications

## Contents
- [Structuring Test Files](#structuring-test-files)
- [Test Authority](#test-authority)
- [Writing Tests](#writing-tests)
- [Executing Tests](#executing-tests)
- [Test Implementation Workflow](#test-implementation-workflow)
- [Examples](#examples)

## Structuring Test Files
Organize test files to mirror the `lib` directory structure to maintain predictability.

* Place all test code within the `test` directory at the root of the package.
* Append `_test.dart` to the end of all test file names (e.g., `lib/src/utils.dart` should be tested in `test/src/utils_test.dart`).
* If writing integration tests, place them in an `integration_test` directory at the root of the package.

## Test Authority

Derive expected behavior before writing assertions:

1. Use the active goal, project fact sources, API/domain contracts, and confirmed
   user-visible behavior as the oracle.
2. Treat existing tests as evidence, not automatic truth. Check whether they
   encode current product semantics or only implementation assumptions.
3. Do not copy the current implementation output into an expected value merely
   to make the test pass.
4. Prefer observable results, state, errors, and boundary contracts over private
   structure or call-count assertions. Verify interactions only when the
   interaction itself is part of the contract.
5. For a bug fix, make the regression test represent the confirmed pre-fix
   failure. Demonstrate fail-before-fix/pass-after-fix when a safe isolated
   baseline is available; otherwise report that the pre-fix proof is unverified.

Developer-authored unit tests are valuable implementation feedback, but they are
not the sole acceptance evidence when an active workflow requires independent
verification.

## Writing Tests
Utilize `package:test` as the standard testing library for Dart applications.

* Import `package:test/test.dart` (or `package:flutter_test/flutter_test.dart` for Flutter).
* Group related tests using the `group()` function to provide shared context.
* Define individual test cases using the `test()` function.
* Validate outcomes using the `expect()` function alongside matchers (e.g., `equals()`, `isTrue`, `throwsA()`).
* Write asynchronous tests using standard `async`/`await` syntax. The test runner automatically waits for the `Future` to complete.
* Manage test setup and teardown using `setUp()` and `tearDown()` callbacks.
* If testing code that relies on dependency injection, use `package:mockito` alongside `package:test` to generate mock objects, configure fixed scenarios, and verify interactions.

## Executing Tests
Select the appropriate test runner based on the project type and test location.

* If working on a pure Dart project, execute tests using the `dart test` command.
* If working on a Flutter project, execute tests using the `flutter test` command.
* If running integration tests, explicitly specify the directory path, as the default runner ignores it: `dart test integration_test` or `flutter test integration_test`.
* For Flutter projects, default to `dart analyze`, `flutter analyze`, and
  targeted `dart test` / `flutter test test/...`. Run
  `flutter test integration_test`, `flutter run -d web-server`, hot reload, or
  screenshot/preview checks only when project guidance or the current user
  request explicitly allows the exact command. Keep real device/simulator
  install/run, `flutter build`, release/package work, store/account/payment
  flows, and mutable backend-state flows behind separate confirmation.

## Test Implementation Workflow

Follow this sequential workflow when implementing new test suites. Copy the checklist to track your progress.

### Task Progress
- [ ] 1. Create the test file in the `test/` directory, ensuring the `_test.dart` suffix.
- [ ] 2. Import `package:test/test.dart` and the target library.
- [ ] 3. Define a `main()` function.
- [ ] 4. Initialize shared resources or mocks using `setUp()`.
- [ ] 5. Write `test()` cases grouped by functionality using `group()`.
- [ ] 6. Execute the test suite using the appropriate CLI command.
- [ ] 7. **Classify failures before editing.** Determine whether the implementation violates the confirmed contract, the assertion conflicts with an authoritative source, the contract is ambiguous, or the environment/fixture is invalid.
- [ ] 8. Fix implementation when it violates the contract. Change assertions only when an authoritative source proves the test is wrong, and record that source in the task evidence.
- [ ] 9. If expected behavior is ambiguous, stop and report a product/specification question. Do not guess an expected value or weaken the assertion to obtain green tests.
- [ ] 10. Re-run the targeted suite and report both the result and any unproven pre-fix behavior.

## Examples

### Standard Unit Test Suite
Demonstrates grouping, setup, synchronous, and asynchronous testing.

```dart
import 'package:test/test.dart';
import 'package:my_package/calculator.dart';

void main() {
  group('Calculator', () {
    late Calculator calc;

    setUp(() {
      calc = Calculator();
    });

    test('adds two numbers correctly', () {
      expect(calc.add(2, 3), equals(5));
    });

    test('handles asynchronous operations', () async {
      final result = await calc.fetchRemoteValue();
      expect(result, isNotNull);
      expect(result, greaterThan(0));
    });
  });
}
```

### Mocking with Mockito
Demonstrates configuring a mock object for dependency injection testing.

```dart
import 'package:test/test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:my_package/api_client.dart';
import 'package:my_package/data_service.dart';

// Generate the mock using build_runner: dart run build_runner build
@GenerateNiceMocks([MockSpec<ApiClient>()])
import 'data_service_test.mocks.dart';

void main() {
  group('DataService', () {
    late MockApiClient mockApiClient;
    late DataService dataService;

    setUp(() {
      mockApiClient = MockApiClient();
      dataService = DataService(apiClient: mockApiClient);
    });

    test('returns parsed data on successful API call', () async {
      // Configure the mock
      when(mockApiClient.get('/data')).thenAnswer((_) async => '{"id": 1}');

      // Execute the system under test
      final result = await dataService.fetchData();

      // Verify outcomes and interactions
      expect(result.id, equals(1));
      verify(mockApiClient.get('/data')).called(1);
    });
  });
}
```
