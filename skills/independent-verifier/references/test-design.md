# Independent Test Design

Use this mode before implementation when the behavior contract is stable and an
independent test track is required.

## Inputs

Give the verifier the active goal or specification, authoritative behavior
sources, public contracts, and a reliable pre-change baseline. Do not give it
the developer's preferred implementation or inspect concurrently changing code
unless the verifier has an isolated immutable baseline.

## Charter

Derive a compact frozen charter covering:

- observable acceptance behavior;
- negative and boundary cases;
- invariants or properties;
- regression scope;
- required fixtures, mocks, devices, or environments;
- for a bug fix, the expected pre-fix failure signal.

Expected values must come from authoritative sources rather than current
implementation output. Existing tests are evidence, not automatic truth.

This mode is read-only unless the user explicitly requests test-first files and
the owner grants a bounded test-only write scope.

## Result

Return the authoritative behavior sources, frozen charter, expected pre-fix
failure, environment needs, and unresolved specification questions. The owner
records the charter in the existing Check owner; do not create a second truth
source.
