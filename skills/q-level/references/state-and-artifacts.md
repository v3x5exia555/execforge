# Q Level State and Artifacts

## State machine

```text
NO_QA_CONTEXT
→ QA_INPUT_REQUIRED
→ QA_PLAN_REQUIRED
→ QA_PLAN_APPROVAL_REQUIRED
→ QA_READY
→ QA_IN_PROGRESS
→ QA_RETEST_REQUIRED
→ QA_PASSED
→ QA_RELEASE_READY
```

Return/block states:

- `RETURN_TO_IMPLEMENTATION`
- `RETURN_TO_ENGINEERING_PLAN`
- `RETURN_TO_PRODUCT`
- `BLOCKED`
- `UNVERIFIABLE`

## Artifact directory

```text
.q-level/
├── state.json
├── qa-context.md
├── qa-plan.md
├── environment-approval.md
├── coverage-matrix.md
├── execution-evidence.md
├── defects.md
├── retest.md
└── decision.md
```

## Evidence format

For every executed test record:

- Test/scenario ID
- Requirement ID
- Layer
- Command or procedure
- Environment/build
- Start/end time
- Result
- Evidence path
- Defect ID when failed

## Final decision record

Include:

- QA verdict
- Build/commit
- Plan approval
- Coverage summary
- Open defects by severity
- Untested/unverifiable areas
- Accepted risks and owners
- Required next action
- Re-entry condition
