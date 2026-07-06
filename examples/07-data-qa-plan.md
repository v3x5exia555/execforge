# Example 7 — Data-QA Attachment

## Change

An application approval workflow now writes a decision row, emits an audit event, and updates a reporting table asynchronously.

## Why data QA is required

- A replayed event could duplicate reporting rows.
- A failed async consumer could leave the API result correct but downstream state stale.
- Audit history must persist even when reporting retries.

## Data invariants

| Invariant ID | Rule |
|---|---|
| DQ-1 | One approval row per application version |
| DQ-2 | Audit event exists for every approved decision |
| DQ-3 | Reporting table converges to approved state after retry |

## Sample scenarios

| Scenario ID | Flow | Evidence |
|---|---|---|
| DQ-S1 | Approve application once | Decision row + audit record + reporting row |
| DQ-S2 | Replay approval event | No duplicate reporting row |
| DQ-S3 | Fail consumer, then retry | Reporting row converges after retry |
