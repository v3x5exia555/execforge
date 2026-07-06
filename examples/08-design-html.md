# Example 8 — Design HTML Bridge

## Scope source

Approved product scope: let an operations user review an incoming application, request changes, or approve it without leaving the queue.

## UX translation

- Primary user: operations reviewer
- Primary job: decide an application quickly with enough context to avoid mistakes
- Non-goal: analytics dashboard or cross-application reporting

## Screen inventory

| Screen / State | Purpose |
|---|---|
| Review queue | Show pending applications and priority |
| Review detail | Show application data and decision actions |
| Request changes modal | Capture missing-info request |
| Empty queue | Show no pending work |
| Error state | Recover from failed save or stale lock |

## Required states

- Loading queue
- Empty queue
- Validation error on request-changes form
- Unauthorized decision action
- Success confirmation after approve / request changes

## HTML/CSS delivery note

Use semantic sections for queue, detail, and decision panel. Keep the decision actions fixed in the reading flow so the reviewer never loses the primary action while scanning the application.
