# Example 5 — Portal/API/Backend QA Plan

## Journey

A permitted user submits an application in the portal.

## Cross-layer checks

| Requirement | Portal | API | Backend/data |
|---|---|---|---|
| Create application | Form and confirmation | POST schema/status | Row and audit record |
| Prevent duplicate | Double click | Repeated idempotency key | One row only |
| Block unauthorized role | Action hidden/blocked | 403 | No write |
| Show final status | Status screen | GET response | Stored status |

## Approval

State: `QA_PLAN_APPROVAL_REQUIRED`

```text
APPROVE QA PLAN
```
