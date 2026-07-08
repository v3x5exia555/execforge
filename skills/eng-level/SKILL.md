---
name: eng-level
description: Use when approved product requirements need engineering planning, implementation gating, plan-to-code traceability, Staff Engineer review, release readiness, or a SHIP/FIX/REPLAN/BLOCK decision.
license: MIT
compatibility: Requires a Git repository for diff review. Integrates with separately installed gstack and Superpowers skills when available.
metadata:
  author: ExecForge contributors
  version: "0.6.0"
---

# Eng Level

## Core principle

Plan intent is not implementation evidence. A correct plan cannot excuse broken code, and passing CI cannot prove untested requirements.

## Lifecycle

```text
Approved Product Decision
          ↓
User Upstream Approval
          ↓
Plan Engineering Review
          ↓
Implementation
          ↓
Staff Engineer Review
          ↓
Portal/API/Backend QA
          ↓
Final Delta Review and QA Retest
          ↓
Final Engineering Decision
```

The plan review and Staff Engineer review must not run in parallel. For web portal, API, or backend/data changes, Q Level must execute before the final ship verdict unless the QA requirement is explicitly not applicable.

## Modes

- `plan` — approve or reject the technical plan.
- `review` — audit a real Git diff.
- `full` — run every stage possible in the current session.
- `auto` — detect and run the next valid stage.
- `status` — report state without starting a review.

## Mandatory upstream stop check

When an ExecForge, CEO/COO, PRD, or product plan exists:

1. Translate it into:
   - What, why, and for whom
   - In scope, deferred, skipped, and non-goals
   - Product success metrics
   - Acceptance criteria / definition of done (the concrete pass test for the work; state
     it before building — do not rely on "test until it is fixed")
   - Initiative flags and authorization status (`offensive-security`, `legally-gated`,
     `regulated-impersonation`, `user-prescribed-mechanism`, each set or not set; and the
     authorization decision for any gating flag: `AUTHORIZED` / `NOT AUTHORIZED` /
     `N-A (justified)`)
   - Non-negotiable CEO decisions
   - Non-negotiable COO controls
   - Assumptions and unknowns
   - Kill criteria
2. Save `.eng-level/upstream-requirements.md`. Planning may not proceed while any gating
   flag has an unresolved authorization decision.
3. Set `UPSTREAM_APPROVAL_REQUIRED`.
4. Stop and request one response:
   - `APPROVE UPSTREAM`
   - `APPROVE WITH CHANGES`
   - `REJECT UPSTREAM INTERPRETATION`
   - `REOPEN PRODUCT DECISION`

Do not plan, implement, or review before approval. Read [the upstream approval contract](references/upstream-approval.md).

## Plan review

Use the current installed gstack `plan-eng-review` skill when available. Otherwise state that [the fallback contract](references/fallback-review-contracts.md) is being used.

The review must cover:

- Existing patterns and reuse
- Architecture, components, data flow, state transitions
- Failure paths, idempotency, consistency, migration safety
- Security and trust boundaries
- Performance and observability
- Rollback and reversibility
- Tests and definition of done
- Exact implementation tasks and expected files

Verdict:

- `APPROVED`
- `APPROVED WITH CONDITIONS`
- `REVISE`
- `REJECTED`
- `UNVERIFIABLE`

Lock the base branch, merge base, approved scope, controls, tests, and plan artifacts.

## Superpowers execution bridge

When installed, use current Superpowers skills:

1. `using-git-worktrees`
2. `writing-plans`
3. `subagent-driven-development` or `executing-plans`
4. `test-driven-development`
5. `verification-before-completion`

Per-task Superpowers review does not replace the final whole-branch Staff Engineer review.

Read [the integration map](references/superpowers-map.md).

## Q Level bridge

For portal, API, backend service, database, queue, or end-to-end transaction changes:

1. Complete the first Staff Engineer review.
2. Invoke `q-level --mode=auto` with approved upstream requirements, engineering plan, implementation diff, and test environment.
3. Route QA defects to implementation, engineering planning, or product according to the QA verdict.
4. When QA-driven fixes change production code, run a final Staff Engineer delta review.
5. Re-run affected QA before issuing `SHIP`.

Do not treat unit tests or a code review as a substitute for cross-layer portal/API/backend evidence.

## Staff Engineer review

Run only when:

- A meaningful Git diff exists.
- Base branch/commit is known.
- Implementation tasks have statuses.
- Relevant tests can be executed or their absence is explicit.

Use current installed gstack `review` when available. Inspect actual source, configuration, schema, diff, and test results.

Finding severity:

- `P0` — critical outage, security, corruption, or irreversible loss risk.
- `P1` — must fix before merge.
- `P2` — important, conditionally deferrable with owner.
- `P3` — non-blocking quality improvement.

## Conformance

For each upstream requirement and plan task, use:

- `DONE`
- `PARTIAL`
- `NOT DONE`
- `CHANGED`
- `SCOPE DRIFT`
- `UNVERIFIABLE`
- `NO LONGER NEEDED`

Runtime behavior and actual code outrank plan intent.

## Final decision

Only the lifecycle orchestrator selects:

- `SHIP`
- `SHIP WITH REQUIRED FIXES`
- `RETURN TO IMPLEMENTATION`
- `RETURN TO PLAN`
- `BLOCK`

Rules:

- Any unresolved P0/P1 blocks shipping.
- Code defects with valid architecture return to implementation.
- Invalid architecture assumptions return to plan.
- Missing critical evidence or unsafe rollback blocks.
- Maximum three automatic fix/review cycles before replan or block.

Read [state and artifact contracts](references/state-and-artifacts.md). For a full run, follow [the step-by-step lifecycle protocol](references/lifecycle-protocol.md) and produce [the final output contract](references/fallback-review-contracts.md).

## Validation gate

Before returning:

- Upstream requirements were approved.
- Plan review occurred before implementation.
- A real diff existed before Staff review.
- Every requirement and task has a conformance status.
- Tests claimed as passing were actually run.
- Applicable portal/API/backend QA completed with `QA PASS` or explicitly accepted non-blocking risks.
- QA-driven production-code changes received a final delta review and retest.
- Contradictions and deviations are recorded.
- No P0/P1 is hidden behind conditional shipping.
- The final verdict is traceable to evidence.
