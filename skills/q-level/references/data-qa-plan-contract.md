# Data-QA Plan Contract

Use this attachment when release quality depends on validating persisted state, migrations, backfills, reconciliation, or asynchronous data movement.

## Required context

Record:

- System(s) of record and downstream copies
- Tables, topics, queues, files, or datasets affected
- Migration / backfill / replay strategy
- Reconciliation source and comparison method
- Rollback method and point-of-no-return
- Audit, lineage, and retention requirements

## Required scenario types

For each material data flow consider:

- Create / update / delete state transition
- Duplicate or replayed input
- Partial failure and retry
- Ordering and concurrency
- Null, precision, timezone, and mapping behavior
- Migration forward / backward compatibility
- Reconciliation after asynchronous processing
- Backfill safety and resumability
- Audit trail persistence

## Evidence expectations

Collect evidence that proves real state, not only API responses:

- Query output, fixture assertion, or integration-test proof
- Queue / event publication or consumption evidence
- Reconciliation delta or row-count proof
- Audit / lineage record evidence
- Cleanup confirmation when destructive data setup was used

## Exit criteria

Define:

- Invariants proven or explicitly untestable
- Reconciliation differences explained or zero
- Rollback / recovery confidence
- Accepted data risks with owner and review date
