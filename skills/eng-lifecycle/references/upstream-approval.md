# Upstream Approval Contract

## Required package

- Initiative
- Problem and target user
- Product hypothesis
- Accepted, deferred, and skipped scope
- Non-goals
- User and business success metrics
- CEO decisions
- COO controls
- Security, privacy, and compliance requirements
- Cost and operating constraints
- Rollout and kill criteria
- Facts, assumptions, and unknowns
- Source and owner

## Approval behavior

### APPROVE UPSTREAM

Lock the interpretation, approver, timestamp, and source hash where available.

### APPROVE WITH CHANGES

Apply changes, show the revised interpretation, and request approval again.

### REJECT UPSTREAM INTERPRETATION

Preserve the rejected version, correct it, and request approval again.

### REOPEN PRODUCT DECISION

Stop engineering and return to `execforge`.

## Traceability

| Upstream requirement | Source | Plan item | Implementation evidence | Test evidence | Status |
|---|---|---|---|---|---|

Statuses:

- SATISFIED
- PARTIAL
- NOT SATISFIED
- CHANGED WITH APPROVAL
- UNVERIFIABLE
- NOT APPLICABLE
