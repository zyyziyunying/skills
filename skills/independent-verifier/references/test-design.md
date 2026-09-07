# Independent Test Design

Use this mode to design behavior-focused tests before implementation. Use the
supplied specification or public contract; a goal document or separate test
track is not a prerequisite. Surface material ambiguity in the result.

## Inputs

Give the verifier the active goal or specification, authoritative behavior
sources, and public contracts. Include a reliable pre-change baseline when
pre-fix regression evidence is part of the task. Do not give it
the developer's preferred implementation or inspect concurrently changing code
unless the verifier has an isolated immutable baseline.

## Charter

Derive a compact test charter covering the relevant items:

- observable acceptance behavior;
- negative and boundary cases;
- invariants or properties;
- regression scope;
- required fixtures, mocks, devices, or environments;
- for a bug fix, the expected pre-fix failure signal.

Expected values must come from authoritative sources rather than current
implementation output. Existing tests are evidence, not automatic truth.

This mode is read-only unless the user or delegating owner authorizes a bounded
test-only write scope.

## Result

Return the authoritative behavior sources, test charter, expected pre-fix
failure when relevant, environment needs, and unresolved specification questions.
If persistence is requested, update the existing test-plan or acceptance fact
source. Otherwise return the result directly; do not create a document merely
to satisfy this mode.
