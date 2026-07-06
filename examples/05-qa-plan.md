# Example 5 — Portal/API/Backend QA Plan

## Journey

A permitted user submits an application in the portal.

## Risks

- Duplicate submission could create multiple applications.
- Unauthorized role could trigger writes through a hidden or stale portal action.
- Backend write could succeed while the portal shows stale status.

## Cross-layer checks

| Requirement ID | Requirement | Portal | API | Backend/data |
|---|---|---|---|---|
| APP-1 | Create application | Form submission + confirmation state | POST schema/status | Row and audit record |
| APP-2 | Prevent duplicate | Double click / repeated submit | Repeated idempotency key | One row only |
| APP-3 | Block unauthorized role | Action hidden or blocked | 403 | No write |
| APP-4 | Show final status | Status screen refresh | GET response | Stored status |

## Example scenarios

| Scenario ID | Layer | Command / Procedure | Expected evidence |
|---|---|---|---|
| P-1 | Portal | Submit valid form once | Confirmation UI + network trace |
| P-2 | Portal/API | Double-submit form | No duplicate network success path |
| A-1 | API | Replay create request with same idempotency key | Same logical result, no duplicate create |
| B-1 | Backend/data | Check stored row and audit record | One application row + one audit entry |

## Approval

State: `QA_PLAN_APPROVAL_REQUIRED`

```text
APPROVE QA PLAN
```
