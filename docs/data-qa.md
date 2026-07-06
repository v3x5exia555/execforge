# Data QA

Data QA is the persisted-state attachment for `/q-level`.

Use it when release quality depends on more than the immediate request/response path, for example:

- migrations or backfills
- replay or retry safety
- reconciliation between source-of-truth and derived state
- queue/event processing
- timezone, precision, null, or mapping correctness
- rollback after persistent writes

## Workflow

Start with the normal `/q-level` plan, then attach `data-qa-plan.md` when data-risk is material.

The attachment should define:

- systems of record
- invariants
- reconciliation method
- rollback method
- evidence proving real state

## Evidence standard

Do not treat API success alone as enough. Data QA should include direct state proof such as integration assertions, query results, reconciliation output, queue/event evidence, or audit/lineage records.

See `examples/07-data-qa-plan.md` for a small example.
