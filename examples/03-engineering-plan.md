# Example 3 — Engineering Plan

Verdict: `APPROVED WITH CONDITIONS`

## Conditions

- Define a deterministic ingestion key.
- Reject or quarantine schema-invalid rows.
- Reconciliation must compare source and target counts plus key metrics.
- Store run metadata and immutable evidence IDs.
- Add rollback and reprocessing tests.

## Tasks

1. Add schema contract and failing validation tests.
2. Add idempotency constraint and duplicate-load test.
3. Add quarantine path.
4. Add reconciliation report.
5. Add run state and observability.
