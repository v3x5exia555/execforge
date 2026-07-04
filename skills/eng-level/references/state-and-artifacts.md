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
└── decision.md
```

## Replan triggers

Return to plan when:

- Architecture cannot satisfy a core requirement.
- A new system of record or trust boundary appears.
- Real schema constraints make migration unsafe.
- Performance requires architectural change.
- Consistency, retry, or transaction model is fundamentally wrong.
- Fixes repeatedly fail for the same root cause.
