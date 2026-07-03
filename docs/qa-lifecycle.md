# QA Lifecycle

`/qa-lifecycle` is optimized for a web portal that calls APIs backed by services, databases, queues, or data pipelines.

## Topology

```text
Portal QA ───────┐
API QA ──────────┼→ QA Main Orchestrator → Final QA Verdict
Backend/Data QA ─┘
```

## Test the transaction, not only the layers

```text
Portal action
→ API authorization and validation
→ Backend business rule
→ Database/queue/event state
→ API response
→ Portal display
```

Each accepted requirement receives one cross-layer coverage row.

## Modes

- `plan`
- `execute`
- `full`
- `retest`
- `auto`
- `status`

## Approval gate

The orchestrator stops at `QA_PLAN_APPROVAL_REQUIRED` before executing the approved plan.

Responses:

```text
APPROVE QA PLAN
APPROVE QA PLAN WITH CHANGES
REJECT QA PLAN
RETURN TO ENGINEERING PLAN
RETURN TO PRODUCT
```

## Default stack

- Portal: Playwright
- API: Schemathesis or native API tests
- Backend/data: native unit/integration tests plus Testcontainers
- Optional: k6, axe-core, ZAP, Pact

Tools are adapters, not the source of truth. Actual executed evidence determines the verdict.

## Verdicts

- QA PASS
- QA PASS WITH ACCEPTED RISKS
- RETURN TO IMPLEMENTATION
- RETURN TO ENGINEERING PLAN
- RETURN TO PRODUCT
- BLOCK RELEASE
- UNVERIFIABLE
