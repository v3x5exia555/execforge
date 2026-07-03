# Upstream Approval

The engineering lifecycle cannot silently reinterpret a CEO, COO, ExecForge, PRD, or product plan.

## Stop check

The orchestrator summarizes:

1. What and why
2. Target user
3. In scope
4. Out of scope
5. Non-negotiable decisions and controls
6. Engineering decision space
7. Success and kill criteria
8. Assumptions and unknowns

It then stops at `UPSTREAM_APPROVAL_REQUIRED`.

## Responses

```text
APPROVE UPSTREAM
APPROVE WITH CHANGES
REJECT UPSTREAM INTERPRETATION
REOPEN PRODUCT DECISION
```

Only explicit approval unlocks engineering planning.
