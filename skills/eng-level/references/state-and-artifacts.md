# Lifecycle State and Artifacts

## State machine

```text
NO_CONTEXT
→ UPSTREAM_INTAKE
→ UPSTREAM_APPROVAL_REQUIRED
→ PLAN_REQUIRED
→ PLAN_APPROVED
→ WAITING_FOR_IMPLEMENTATION
→ IMPLEMENTATION_IN_PROGRESS
→ REVIEW_READY
→ REVIEW_PASSED
→ SHIP_READY
```

Return states:

- `RETURN_TO_PRODUCT_PLAN`
- `RETURN_TO_PLAN`
- `RETURN_TO_IMPLEMENTATION`
- `BLOCKED`

## Evidence precedence

1. Reproducible runtime behavior and executed tests
2. Actual code, schema, and configuration
3. Git diff and commit history
4. Approved engineering plan
5. Comments and stated intent
6. Unsupported assumptions

## Artifact directory

```text
.eng-level/
├── state.json
├── upstream-requirements.md
├── upstream-approval.md
├── upstream-traceability.md
├── engineering-plan.md
├── implementation-tasks.md
├── test-matrix.md
├── staff-review.md
├── conformance.md
├── contradictions.md
├── backlog.md
└── decision.md
```

## Deferred backlog

`.eng-level/backlog.md` holds work that was planned and deliberately not executed. Deferred
work belongs in a resumable artifact, never only in a commit message or a chat turn.

Each action carries a cycle and a provenance marker:

| Field | Values |
|---|---|
| Cycle | `Now` — ship this cycle · `Boundary` — starts at the cycle edge, user call · `Next` — deferred |
| Provenance | `[C]` consensus · `[R]` resolved disagreement · `[gate]` externally blocked |

Record for every deferred action: what it is, why it was deferred, what unblocks it, and the
measurable condition that would pull it forward.

`--mode=status` reads this file and answers what was parked, why, and what unblocks it.

## Replan triggers

Return to plan when:

- Architecture cannot satisfy a core requirement.
- A new system of record or trust boundary appears.
- Real schema constraints make migration unsafe.
- Performance requires architectural change.
- Consistency, retry, or transaction model is fundamentally wrong.
- Fixes repeatedly fail for the same root cause.
