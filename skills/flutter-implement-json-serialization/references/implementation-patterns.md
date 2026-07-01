# App API JSON Implementation Patterns

Use these examples after `SKILL.md` has established that the work belongs to BesideYou App API JSON semantics.

## DTO Objects

Use `Map<String, Object?>` for JSON objects and pass a request path/source label through parsing.

```dart
final class PetDto {
  const PetDto({required this.id, required this.name, this.avatarUrl});

  factory PetDto.fromJson(Map<String, Object?> json, String requestPath) {
    return PetDto(
      id: AppApiJsonReader.intField(json, 'id', requestPath),
      name: AppApiJsonReader.stringField(json, 'name', requestPath),
      avatarUrl: AppApiJsonReader.stringFieldOrNull(
        json,
        'avatar_url',
        requestPath,
      ),
    );
  }

  final int id;
  final String name;
  final String? avatarUrl;
}
```

## Repository Mapping

Repository mapping should stay relative to `API_BASE_URL` and parse only unwrapped `content`.

```dart
static const String petPath = 'app/v1/pets/current';

Future<PetDto> fetchCurrentPet() async {
  final Object? content = await _api.getJson(petPath);
  return PetDto.fromJson(
    AppApiJsonReader.object(content, petPath),
    petPath,
  );
}
```

For `content` arrays, convert the top-level value directly.

```dart
final Object? content = await _api.getJson(path);
if (content is! List) {
  throw AppApiJsonReader.invalidResponse(
    path,
    'API content must be an array.',
    content,
  );
}
final items = List<Object?>.of(content);
return items
    .map((Object? item) =>
        PetDto.fromJson(AppApiJsonReader.object(item, path), path))
    .toList();
```

For object fields containing arrays, use the field helper.

```dart
final items = AppApiJsonReader.listField(json, 'items', requestPath);
```

## Request Bodies

Use explicit request objects when the body has meaningful structure.

```dart
final class PetRenameRequest {
  const PetRenameRequest({required this.name});

  final String name;

  Map<String, Object?> toJson() => <String, Object?>{
        'name': name.trim(),
      };
}
```

## Enums

Model wire names explicitly and parse with `AppApiJsonReader.enumField` or `enumFromWireName`.

```dart
enum PetState {
  preparing('preparing'),
  playable('playable');

  const PetState(this.wireName);
  final String wireName;
}
```
Unsupported App API enum values should become invalid-response `AppApiException`s unless the nearest module README explicitly defines forward-compatible fallback behavior.
