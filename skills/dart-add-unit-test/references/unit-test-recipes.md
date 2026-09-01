# Dart Unit-Test Recipes

Load this reference only when the selected test needs a pattern.

## Basic Suite

```dart
import 'package:test/test.dart';
import 'package:my_package/calculator.dart';

void main() {
  group('Calculator', () {
    late Calculator calculator;

    setUp(() => calculator = Calculator());

    test('adds two numbers', () {
      expect(calculator.add(2, 3), equals(5));
    });

    test('returns an asynchronous value', () async {
      final value = await calculator.fetchValue();
      expect(value, greaterThan(0));
    });
  });
}
```

Use `throwsA`, an explicit matcher, and deterministic fakes for error paths
instead of asserting implementation details.

## Mockito When the Project Already Uses It

Keep imports before declarations. Generate mocks through the project's existing
code-generation workflow; do not add Mockito or a generator merely for a small
test that a fake can express clearly.

```dart
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/test.dart';
import 'package:my_package/api_client.dart';
import 'package:my_package/data_service.dart';

import 'data_service_test.mocks.dart';

@GenerateNiceMocks([MockSpec<ApiClient>()])
void main() {
  group('DataService', () {
    late MockApiClient apiClient;
    late DataService service;

    setUp(() {
      apiClient = MockApiClient();
      service = DataService(apiClient: apiClient);
    });

    test('parses a successful response', () async {
      when(apiClient.get('/data')).thenAnswer((_) async => '{"id": 1}');

      final result = await service.fetchData();

      expect(result.id, equals(1));
      verify(apiClient.get('/data')).called(1);
    });
  });
}
```

Verify an interaction only when it belongs to the contract, such as an
idempotency, retry, authorization, or side-effect guarantee.
