---
name: q-level
description: Use when a web portal, API, backend service, database workflow, or end-to-end business transaction needs a risk-based QA plan, cross-layer test execution, defect triage, retesting, or a QA PASS/BLOCK RELEASE decision.
license: MIT
compatibility: Requires repository or deployed-environment evidence. Uses Playwright, Schemathesis, native tests, Testcontainers, k6, axe-core, ZAP, or Pact only when separately available and appropriate.
metadata:
  author: ExecForge contributors
  version: "0.4.0"
---

# Q Level — Portal → API → Backend/Data

## Core principle

A layer passing alone does not prove the business transaction works end to end.

For every accepted requirement, verify:

```text
Portal action
→ API request and authorization
→ Backend rule
→ Database, queue, or event state
→ API response
→ Portal result
```

## Required topology

```text
Portal QA Subagent ───────┐
API QA Subagent ──────────┼→ QA Main Orchestrator → Final QA Verdict
Backend/Data QA Subagent ─┘
```

The three subagents provide evidence. Only the QA Main Orchestrator approves the QA plan and issues the final verdict.

If real subagents are unavailable, run three isolated review passes and merge them only in the orchestrator phase.

## Modes

- `plan` — create a risk-based QA plan and stop for approval.
- `execute` — run an already approved QA plan.
- `full` — plan, request approval, and execute only after approval.
- `retest` — verify fixes without silently reducing expectations.
- `auto` — detect and run the next valid stage.
- `status` — report state and open defects.

## Required inputs

Use the approved source of truth:

- Product requirements and non-goals
- User roles and critical journeys
- Engineering plan and architecture
- API specification or known routes
- Backend/data invariants
- Security, compliance, and performance controls
- Supported browsers and environments
- Implementation diff and test commands
- Known risks, dependencies, and accepted limitations

If product or engineering requirements are unclear, return to the correct upstream workflow rather than inventing acceptance criteria.

## QA plan approval stop check

Before executing browser automation, API fuzzing, load tests, security scans, destructive data tests, or privileged workflows:

1. Create `.q-level/qa-plan.md`.
2. Create `.q-level/coverage-matrix.md`.
3. Record target environment, test identities, permitted actions, test data, cleanup, rate limits, and excluded tests.
4. Set `QA_PLAN_APPROVAL_REQUIRED`.
5. Stop and request one response:
   - `APPROVE QA PLAN`
   - `APPROVE QA PLAN WITH CHANGES`
   - `REJECT QA PLAN`
   - `RETURN TO ENGINEERING PLAN`
   - `RETURN TO PRODUCT`

Never run load or active security scans against production without explicit authorization.

Read [the QA planning contract](references/qa-plan-contract.md).

## QA Planner responsibility

The QA Main Orchestrator creates a risk-based plan containing:

- Entry and exit criteria
- Critical user journeys
- Positive, negative, boundary, authorization, and failure scenarios
- Portal/API/backend coverage
- Test data and environment strategy
- Regression scope
- Manual versus automated split
- Tool selection and fallback
- Evidence requirements
- Defect severity and retest policy
- Untested areas and accepted risks

Prioritize by user impact, data integrity, security, reversibility, frequency, and defect escape cost.

## Portal QA Subagent

Verify critical behavior through the user interface:

- Authentication, sessions, and logout
- Role-based visibility and actions
- Forms, validation, navigation, and error states
- Duplicate clicks and repeated submissions
- Loading, timeout, empty, partial, and stale states
- Browser behavior and responsive layout where required
- Accessibility checks where applicable
- Correct display of final backend state

Prefer Playwright when available. Capture commands, screenshots, traces, console errors, network failures, and reproduction steps.

Do not assert backend correctness from UI text alone.

## API QA Subagent

Verify the service boundary:

- Authentication and authorization by role
- Required/optional fields, types, enums, nulls, and boundaries
- Positive and negative response contracts
- Status codes and error bodies
- Idempotency, retry, pagination, filtering, and concurrency
- Stateful workflows and lifecycle transitions
- Backward compatibility and versioning
- Portal-to-API contract compatibility
- No unexpected 5xx responses

Prefer Schemathesis when an OpenAPI or GraphQL schema exists. Use Pact only when independently deployed consumers/providers justify contract testing.

## Backend/Data QA Subagent

Verify actual system state:

- Business rules and invariants
- Transactions, rollback, and partial failure
- Database writes, updates, deletes, and constraints
- Duplicate prevention and idempotency
- Queue/event publication and consumption
- Retry, replay, ordering, and poison-message handling
- Migration compatibility and data reconciliation
- Timezone, date, precision, null, and mapping behavior
- Concurrent updates and race conditions
- Audit, lineage, and evidence persistence

Prefer repository-native unit/integration tests and real disposable dependencies through Testcontainers when available.

## Specialist adapters

Use only when the risk requires them:

- `k6` — load, spike, soak, and concurrency testing
- `axe-core` — automated accessibility checks
- `ZAP` — authorized staging security scanning
- `Pact` — independently deployed consumer/provider contracts

Read [the tool routing guide](references/tool-routing.md). Tool absence must be reported; never claim an adapter ran when it did not.

## Cross-layer coverage

Maintain one row per accepted requirement:

| Requirement | Portal evidence | API evidence | Backend/data evidence | Result |
|---|---|---|---|---|

Results:

- `PASS`
- `FAIL`
- `PARTIAL`
- `UNTESTED`
- `UNVERIFIABLE`
- `NOT APPLICABLE`

A requirement cannot pass solely because one layer passed.

## Defect classification

Severity:

- `Q0` — critical security, data corruption, irreversible loss, or major outage risk
- `Q1` — release-blocking functional, authorization, integrity, or critical journey failure
- `Q2` — important defect; may be accepted only with owner, rationale, and deadline
- `Q3` — non-blocking usability, maintainability, or cosmetic issue

Classify the destination:

- `IMPLEMENTATION DEFECT`
- `ENGINEERING PLAN DEFECT`
- `PRODUCT REQUIREMENT DEFECT`
- `TEST DEFECT`
- `ENVIRONMENT DEFECT`
- `MISSING EVIDENCE`

Never “fix” a failing test by weakening valid expected behavior.

## Retest loop

After a fix:

1. Reproduce the original failure.
2. Run the narrow regression test.
3. Run affected cross-layer tests.
4. Update the defect and coverage matrices.
5. Run a final delta code review when QA fixes changed production code.
6. Re-run release-critical QA.

Limit autonomous fix/retest cycles to three. Repeated failure for the same root cause returns to engineering planning or blocks release.

## Final QA verdict

Only the QA Main Orchestrator selects:

- `QA PASS`
- `QA PASS WITH ACCEPTED RISKS`
- `RETURN TO IMPLEMENTATION`
- `RETURN TO ENGINEERING PLAN`
- `RETURN TO PRODUCT`
- `BLOCK RELEASE`
- `UNVERIFIABLE`

Rules:

- Any unresolved Q0/Q1 blocks release.
- Accepted Q2/Q3 risks require explicit owner and expiry/review date.
- Missing critical environment or evidence produces `UNVERIFIABLE` or `BLOCK RELEASE`.
- Architecture/integration failures return to engineering planning.
- Contradictory or missing acceptance criteria return to product.
- Final release approval requires traceability from requirement to executed evidence.

Read [state and artifact contracts](references/state-and-artifacts.md).

## Validation gate

Before returning:

- The QA plan and environment were explicitly approved.
- Every accepted requirement has a coverage status.
- Critical roles and authorization boundaries were tested.
- Backend/data assertions verify real state, not only response text.
- Commands and results are recorded.
- Skipped and unavailable tests remain visible.
- No expected result was weakened to obtain a pass.
- Q0/Q1 defects are not hidden behind accepted risk.
- The final verdict is traceable to fresh evidence.
