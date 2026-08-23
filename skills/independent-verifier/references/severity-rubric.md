# Impact Severity Rubric

Use P labels for harm when the issue occurs; keep scheduling priority separate
unless the project explicitly defines P labels as priority.

Calibrate each dimension against project facts. Unsupported or artificially
constructed claims should lower confidence or change the verdict. A reproduced
flag-gated or migration-only bug can still be high confidence; account for the
gate and affected audience in reachability and blast radius. Deferred status
changes scheduling, not impact severity. Violations of a reachable core
workflow, API contract, data-integrity rule, security/privacy rule, or release
goal can support a higher impact label.

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

Classify validity and confidence before severity. A stale test, invalid fixture,
unreachable path, or feature request presented as a bug should change the
verdict or confidence rather than receive an inflated P label. For confirmed or
likely bugs, choose P0-P3 from the actual harm, reachability, blast radius,
frequency, and available workaround. Developer inconvenience or a simple
workaround usually supports P3 unless stronger user impact is evidenced.
