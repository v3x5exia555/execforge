# Fallback Review Contracts and Final Output

## Fallback plan review

Use only when the installed gstack `/plan-eng-review` skill cannot be resolved and the user asks to continue. Evaluate architecture, data flow, state transitions, error paths, security boundaries, data integrity, performance, observability, rollback, tests, and implementation tasks. Clearly label the output:

```text
Fallback plan review used; upstream gstack /plan-eng-review was unavailable.
```

## Fallback Staff Engineer review

Use only when the installed gstack `/review` skill cannot be resolved and the user asks to continue. Inspect diff correctness, failure modes, concurrency, transactions, validation, security, data integrity, performance, compatibility, tests, plan completion, and scope drift. Clearly label the output:

```text
Fallback Staff Engineer review used; upstream gstack /review was unavailable.
```

A fallback review cannot claim exact behavioural equivalence with gstack.

## Final output contract

Produce the following sections and write the same result to `.eng-level/decision.md`:

### Eng Level summary

Initiative, upstream source, upstream approval status and approver, mode, current branch, base branch and commit, lifecycle state, plan verdict, staff review verdict, final decision, confidence.

### Plan status

Architecture decision, key controls, required tests, approved scope, non-goals.

### Implementation conformance

Counts and items for done, partial, missing, changed, scope drift, and unverifiable.

### Blocking findings

Each P0/P1 with evidence and required action.

### Non-blocking findings

Owned P2/P3 items with due conditions.

### Contradictions resolved

Plan claim, actual evidence, resolution.

### Verification

Exact commands run and their results. Never report a command that was not run.

### Final decision

> **Decision: [SHIP / SHIP WITH REQUIRED FIXES / RETURN TO IMPLEMENTATION / RETURN TO PLAN / BLOCK]**

Then explain why, the supporting evidence, the required next action, the owner, and the re-entry condition.
