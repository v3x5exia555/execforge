# Artifacts and Schemas

## Product artifacts

Recommended `.execforge/` content:

- shared-context.md
- ceo-review.md
- coo-review.md
- contradictions.md
- scope-ledger.md
- final-decision.json

## Engineering artifacts

Recommended `.eng-lifecycle/` content:

- state.json
- upstream-requirements.md
- upstream-approval.md
- upstream-traceability.md
- engineering-plan.md
- implementation-tasks.md
- test-matrix.md
- staff-review.md
- conformance.md
- contradictions.md
- decision.md

## Schemas

- `schemas/execforge-decision.schema.json`
- `schemas/eng-lifecycle-state.schema.json`

Validate structure with:

```bash
python scripts/execforge.py validate
```


## QA artifacts

Recommended `.qa-lifecycle/` content:

- state.json
- qa-context.md
- qa-plan.md
- environment-approval.md
- coverage-matrix.md
- execution-evidence.md
- defects.md
- retest.md
- decision.md

Schema:

- `schemas/qa-lifecycle-state.schema.json`
