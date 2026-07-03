# Example 6 — QA Decision

## Result

- Portal: PASS
- API: FAIL
- Backend/data: FAIL

## Defect

Q1 — Repeating the same request creates two database records.

Destination: `IMPLEMENTATION DEFECT`

## Verdict

`RETURN TO IMPLEMENTATION`

Re-entry: add an idempotency constraint, pass the duplicate-request regression, then run affected portal/API/backend tests again.
