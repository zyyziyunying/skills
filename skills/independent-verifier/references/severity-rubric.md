# Impact Severity Rubric

Use P labels for harm when the issue occurs; keep scheduling priority separate
unless the project explicitly defines P labels as priority.

Calibrate against project facts. Raise confidence for violations of a core
workflow, API contract, data-integrity rule, security/privacy rule, or release
goal. Lower confidence for unsupported, deferred, flag-gated, migration-only,
or artificially constructed states.

## P0

Production emergency: broad core-workflow outage, data loss or corruption,
irreversible destructive action, serious billing error, or active security or
privacy exposure. Require production evidence or a high-confidence reachable
path.

## P1

High impact: a core workflow is blocked for many users or an important segment,
there is no acceptable workaround, or the defect creates significant revenue,
compliance, trust, or operational risk.

## P2

Meaningful impact: an important non-core workflow is degraded, the workaround
is costly or easy to miss, or the defect creates repeated support burden or
clear user confusion.

## P3

Low impact: cosmetic mismatch, non-blocking edge case, internal inconvenience,
or a rare issue with a simple workaround. It may still be worth fixing when the
change is small, safe, and adjacent to current work.

Downgrade labels based only on stale tests, invalid fixtures, theoretical
reachability, developer inconvenience, or a feature request presented as a bug.
