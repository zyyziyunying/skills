# Independent Test Verification

Use this mode after implementation with the frozen charter as the primary
contract.

## Verify

Inspect the final diff, relevant implementation, developer tests, charter, and
authoritative behavior sources. Run the smallest strong validation allowed by
project rules.

If writes are authorized, restrict them to explicitly listed test, fixture, and
test-support paths. Do not edit product code, delete or skip coverage, weaken an
assertion, or replace an expected value with the observed implementation output.

For a bug fix, demonstrate fail-before-fix and pass-after-fix when a safe
isolated baseline exists. Never destructively checkout or overwrite user work to
manufacture that proof. Otherwise mark pre-fix failure as unproven.

Classify failures against the contract instead of guessing:

- `pass`
- `implementation failure`
- `spec conflict`
- `environment blocked`

## Result

Return the classification, tests added or inspected, commands and outcomes,
pre-fix proof status, confirmation that product-code writes were `none`, and
remaining risk or uncovered scope. Do not mark the owner goal done.
