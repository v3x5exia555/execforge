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

Recommended `.eng-level/` content:

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
- `schemas/eng-level-state.schema.json`

Validate structure with:

```bash
python3 scripts/execforge.py validate
```


## QA artifacts

Recommended `.q-level/` content:

- state.json
- qa-context.md
- qa-plan.md
- data-qa-plan.md (when required)
- environment-approval.md
- coverage-matrix.md
- execution-evidence.md
- defects.md
- retest.md
- decision.md

Schema:

- `schemas/q-level-state.schema.json`
