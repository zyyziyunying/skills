# Flutter JSON Implementation Patterns

Use these patterns only after `SKILL.md` selects a strategy from the project
contract. Examples use `json_serializable`; adapt them to the generator already
owned by the project.

## Contents

[Owner Boundary](#keep-the-owner-boundary) ·
[Parity-Safe Fields](#parity-safe-generated-fields) ·
[Error Seam](#public-error-and-context-seam) ·
[Direct Model](#direct-generated-model) ·
[Hybrid Model](#hybrid-model) ·
[Nested Models](#nested-models) ·
[Enums](#enums) ·
[Request Bodies](#request-bodies) ·
[Parity Tests](#focused-parity-tests)

## Keep The Owner Boundary

Generated code maps a JSON object. It does not replace the project transport,
envelope, persistence, corruption, or error boundary.

A typical API flow remains:

1. The project client performs transport and validates or unwraps the response.
2. The repository validates the top-level object or list expected by the
   endpoint.
3. A generated or manual mapper reads one model.
4. A project adapter translates expected mapping failures and adds endpoint or
   source context.

Do not move HTTP status handling, response-envelope parsing, database record
selection, or cache corruption policy into a generated DTO merely to reduce
repository code.

## Parity-Safe Generated Fields

Generated casts preserve only the behavior they encode. When the existing
contract requires integer-only values, trimmed required strings, and optional
blank-to-null strings, make those semantics explicit:

```dart
import 'package:json_annotation/json_annotation.dart';

part 'pet_wire_dto.g.dart';

@JsonSerializable(
  checked: true,
  createToJson: false,
  disallowUnrecognizedKeys: false,
)
final class PetWireDto {
  const PetWireDto({
    required this.id,
    required this.name,
    this.avatarUrl,
  });

  factory PetWireDto.fromJson(Map<String, dynamic> json) =>
      _$PetWireDtoFromJson(json);

  @JsonKey(fromJson: _strictInt)
  final int id;

  @JsonKey(fromJson: _requiredTrimmedString)
  final String name;

  @JsonKey(name: 'avatar_url', fromJson: _optionalTrimmedString)
  final String? avatarUrl;
}

int _strictInt(Object? value) {
  if (value is int) {
    return value;
  }
  throw const FormatException('Expected an integer.');
}

String _requiredTrimmedString(Object? value) {
  if (value is! String) {
    throw const FormatException('Expected a string.');
  }
  final String trimmed = value.trim();
  if (trimmed.isEmpty) {
    throw const FormatException('Expected a nonblank string.');
  }
  return trimmed;
}

String? _optionalTrimmedString(Object? value) {
  if (value == null) {
    return null;
  }
  if (value is! String) {
    throw const FormatException('Expected a string or null.');
  }
  final String trimmed = value.trim();
  return trimmed.isEmpty ? null : trimmed;
}
```

This example deliberately does not use raw `int`/`String` casts for an existing
contract with stronger semantics. Add converters only for real contract rules;
do not create a generic converter layer that obscures model behavior.

Confirm the resolved generator version's missing-key and converter behavior
with focused tests. Set `disallowUnrecognizedKeys`, defaults, nullable fields,
and `includeIfNull` from project facts rather than copying this example.

## Public Error And Context Seam

Do not expose a generated factory directly when the public owner boundary must
preserve a project error type or endpoint/path/source context. Keep a small
adapter:

```dart
PetDto parsePet(
  Map<String, Object?> json, {
  required String source,
}) {
  try {
    final PetWireDto wire = PetWireDto.fromJson(
      Map<String, dynamic>.from(json),
    );
    return PetDto(
      id: wire.id,
      name: wire.name,
      avatarUrl: wire.avatarUrl,
    );
  } on CheckedFromJsonException catch (error, stackTrace) {
    throw mapProjectInvalidResponse(
      source: source,
      error: error,
      stackTrace: stackTrace,
    );
  }
}
```

`mapProjectInvalidResponse` represents the existing owner error adapter; use the
actual project helper or exception. Translate only expected serialization
failures. Do not broadly catch programming errors.

If generator callbacks can throw other documented conversion failures, verify
their resolved behavior and translate the narrow expected set. Keep the public
factory signature stable during a non-breaking migration.

## Direct Generated Model

Use a generated model directly only when its casts, nullable behavior, defaults,
unknown-key policy, enum handling, and exception contract already match the
owner's approved public contract. This is easiest for new low-risk wire models,
not for silently replacing a stricter existing parser.

For generated response-only models, disable unnecessary `toJson`. For
request-only models, disable unnecessary `fromJson` when the selected generator
supports it.

## Hybrid Model

Prefer a private or owner-local wire model when most fields are mechanical but
the public model has domain rules:

```dart
PetDto toPet(PetWireDto wire, {required String source}) {
  if (wire.id <= 0) {
    throw mapProjectValidationFailure(
      source: source,
      field: 'id',
      value: wire.id,
    );
  }
  return PetDto(
    id: wire.id,
    name: wire.name,
    avatarUrl: wire.avatarUrl,
  );
}
```

Keep aliases, normalization, cross-field validation, fallback policy, and
domain construction in the smallest readable boundary. If the adapter becomes
more complex than the removed parser, keep the model manual.

## Nested Models

Generated parent mapping normally expects the nested model's conventional
one-argument `fromJson`. It cannot automatically inject a runtime endpoint or
source label into a child factory.

Use one of these deliberate boundaries:

- translate a checked nested failure at the top-level owner seam when
  endpoint-level context is sufficient;
- manually map the nested field when precise path propagation or alias
  precedence matters;
- generate a private nested wire model, then validate it in the owner adapter.

A static `JsonKey(fromJson: ...)` converter cannot receive per-request runtime
context unless that context is encoded through another project-owned mechanism.

## Enums

Give wire values explicit names:

```dart
enum PetState {
  @JsonValue('preparing')
  preparing,

  @JsonValue('playable')
  playable,
}
```

Set unknown-value behavior from the field's owner contract:

- keep control, write, payment, security, entitlement, and navigation fields
  fail-closed unless an explicit safe fallback exists;
- use `unknownEnumValue` only when the owner defines a forward-compatible
  fallback;
- test the unknown value instead of relying on an annotation alone.

## Request Bodies

Generate `toJson` for a one-to-one request contract and test exact output:

```dart
@JsonSerializable(
  createFactory: false,
  includeIfNull: false,
  fieldRename: FieldRename.snake,
)
final class PetUpdateRequest {
  const PetUpdateRequest({this.displayName, this.avatarUrl});

  final String? displayName;
  final String? avatarUrl;

  Map<String, dynamic> toJson() => _$PetUpdateRequestToJson(this);
}
```

Keep request mapping manual when it normalizes values or chooses keys:

```dart
final class PetRenameRequest {
  const PetRenameRequest({required this.name});

  final String name;

  Map<String, Object?> toJson() => <String, Object?>{
        'name': name.trim(),
      };
}
```

Do not split a semantic request into generated leaf wrappers merely to make its
branches look mechanical. Preserve conditional omission, flattening, mutually
exclusive keys, alias priority, and security-sensitive behavior explicitly.

## Focused Parity Tests

For a migrated model, retain or add tests for every applicable difference:

- integer versus `double` or numeric string;
- leading/trailing whitespace and whitespace-only required strings;
- `null`, missing key, empty string, and blank optional string;
- alias precedence and deprecated names;
- unknown enum behavior;
- nested malformed values and source/path context;
- exact request key naming and `null` omission;
- project error type and failure classification.

These tests are the proof that generation removed boilerplate without changing
the contract.
