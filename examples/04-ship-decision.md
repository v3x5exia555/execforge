# Example 4 — Ship Decision

## Conformance

| Requirement | Status |
|---|---|
| Schema validation | DONE |
| Idempotency | DONE |
| Reconciliation | DONE |
| Quarantine | DONE |
| Audit evidence | PARTIAL |

## Finding

P1: Audit evidence is overwritten on retry.

## Decision

`RETURN TO IMPLEMENTATION`

Re-entry condition: evidence records become append-only and the regression test passes.
