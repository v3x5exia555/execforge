# Example 2 — Upstream Approval

## Interpretation

- What: Batch ingestion and reconciliation pipeline
- Why: Remove recurring manual checks and prevent duplicate loads
- User: Data operations team
- In scope: validation, idempotency, reconciliation, quarantine, audit trail
- Out of scope: real-time streaming and self-service UI
- COO controls: rollback, lineage, least privilege, evidence retention
- Unknown: exact current labor baseline

## Stop check

State: `UPSTREAM_APPROVAL_REQUIRED`

User response:

```text
APPROVE UPSTREAM
```
