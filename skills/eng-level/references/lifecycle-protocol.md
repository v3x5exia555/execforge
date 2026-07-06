# Lifecycle Operating Protocol

Step-by-step protocol for a full Eng Level run. State names, the artifact directory, evidence precedence, and replan triggers are defined in [state-and-artifacts.md](state-and-artifacts.md).

## Step 0 — Establish repository and initiative context

Determine repository root, current branch, base branch, merge base, current HEAD, working-tree status, whether a diff exists, initiative name, user objective, existing plan artifacts, relevant product decisions, test/build commands, CI configuration, and repository conventions. Prefer repository evidence over assumptions. Do not mutate the repository during context discovery.

Resolve the base branch in this order:

1. Explicit user-provided base branch
2. Pull-request base branch from available metadata
3. Remote default branch
4. `main`, then `master`

If unresolved and interaction is unavailable, mark the base as unknown and do not issue a ship verdict.

## Step 1 — Detect lifecycle state

| Evidence | Result |
|---|---|
| No initiative or repo context | `NO_CONTEXT` |
| Existing upstream plan not yet translated | `UPSTREAM_INTAKE` |
| Upstream interpretation waiting for user confirmation | `UPSTREAM_APPROVAL_REQUIRED` |
| User reopens product intent or scope | `RETURN_TO_PRODUCT_PLAN` |
| Approved upstream requirements, no engineering plan | `PLAN_REQUIRED` |
| Approved plan, no diff | `WAITING_FOR_IMPLEMENTATION` |
| Diff exists, plan tasks incomplete | `IMPLEMENTATION_IN_PROGRESS` |
| Diff exists and implementation claims completion | `REVIEW_READY` |
| Staff review has blocking code findings | `RETURN_TO_IMPLEMENTATION` |
| Staff review invalidates architecture | `RETURN_TO_PLAN` |
| Critical unresolved safety or integrity issue | `BLOCKED` |
| Review passed and all conditions met | `SHIP_READY` |

In `--mode=auto`, run only the next valid stage.

## Step 2 — Shared engineering context

Write `.eng-level/context.md` with the initiative (problem, intended outcome, scope, non-goals, constraints, dependencies) and the repository (branches, base commit, HEAD, relevant directories, existing patterns, test and build commands). Label material claims `FACT` / `ASSUMPTION` / `INFERENCE` / `UNKNOWN`. Do not invent requirements to make the plan appear complete.

## Step 3 — Plan review

Run when state is `PLAN_REQUIRED` or after `RETURN_TO_PLAN`. Supply the reviewer with the approved upstream requirements, traceability matrix, shared context, product plan, existing repository patterns, constraints, and previous findings.

The review must cover architecture, component boundaries, data flow and state transitions, reuse versus new abstractions, failure paths, idempotency and retries, security and trust boundaries, data integrity and migration safety, performance and capacity assumptions, observability, rollback, test strategy, exact implementation tasks, expected files, and the definition of done.

Verdicts: `APPROVED`, `APPROVED_WITH_CONDITIONS` (record mandatory conditions), `REVISE`, `REJECTED`, `UNVERIFIABLE` (critical evidence unavailable).

Write `.eng-level/plan-review.md`, `engineering-plan.md`, `implementation-tasks.md`, and `test-matrix.md`. Task format:

```markdown
- [ ] **T1 — <imperative task title>**
  - Why: <finding or requirement>
  - Files: <expected paths>
  - Dependencies: <task IDs or external dependencies>
  - Verify: <exact test or observable result>
  - Risk: <Low / Medium / High>
```

Every task must be traceable to a plan finding or requirement.

## Step 4 — Lock the baseline

After approval, record base branch, merge-base commit, approval timestamp, current HEAD, approved scope, non-goals, required controls, required tests, and performance expectations. The baseline prevents the later review from comparing against a moving target. Do not modify Git history to create this record.

## Step 5 — Implementation checkpoint

Continue in the current invocation only when the user authorised implementation, required tools are available, the work can be verified now, and no external approval is pending. Otherwise stop with `WAITING_FOR_IMPLEMENTATION`, report the approved plan and task paths, and give the resume command. Do not promise background execution.

## Step 6 — Review readiness

Before the Staff Engineer review, verify a meaningful diff exists, the base is known, build/test commands are discoverable, claimed tasks have statuses, generated files are distinguishable, and migrations or configuration changes are visible. With no diff, return `WAITING_FOR_IMPLEMENTATION`. If work is visibly incomplete, set `IMPLEMENTATION_IN_PROGRESS` and do not issue a ship decision.

## Step 7 — Staff Engineer review

Supply the reviewer with upstream requirements, traceability matrix, base commit, the actual diff, the approved plan, task list, test matrix, plan conditions, and known intentional deviations. The reviewer must inspect actual repository evidence.

Cover at minimum: correctness, production failure modes, race conditions, idempotency and retries, transactions and partial failure, trust boundaries and input validation, authentication/authorisation, data integrity and migration safety, query counts and performance, resource leaks, error handling and observability, backward compatibility, missing enum/state/edge-case handling, test realism, plan completion, scope drift, and rollback safety.

Every finding must include evidence, file and line where possible, failure scenario, severity, required action, and verification method. Do not create findings from style preference alone. Write `.eng-level/staff-review.md`.

## Step 8 — Conformance reconciliation

Compare every approved task and control against actual implementation using the conformance statuses in `SKILL.md`. Write `.eng-level/conformance.md`:

| Task | Status | Plan Requirement | Implementation Evidence | Tests | Action |
|---|---|---|---|---|---|

Rules: `CHANGED` is not automatically a failure but must satisfy the original outcome and controls; `SCOPE DRIFT` requires explicit review; `NOT DONE` on a blocking task prevents shipping; passing tests do not prove an untested requirement; a file existing does not prove the behaviour is correct.

## Step 10 — Contradiction and deviation register

Write `.eng-level/contradictions.md`:

| ID | Topic | Plan Claim | Implementation Finding | Type | Evidence | Resolution | Owner |
|---|---|---|---|---|---|---|---|

Resolution rules by type:

- `IMPLEMENTATION BUG` — return to implementation.
- `PLAN ASSUMPTION INVALID` — return to plan; update architecture before further fixes.
- `INTENTIONAL DEVIATION` — accept only when the outcome is equal or better, risks are understood, controls remain intact, tests verify the new approach, and the decision is recorded.
- `SCOPE DRIFT` — remove, defer, or explicitly approve the additional scope.
- `MISSING EVIDENCE` — do not guess; add a verification action.
- `TEST CONTRADICTION` — reproduce, inspect test validity, and resolve before shipping.

## Step 12 — Fix loop

On `RETURN_TO_IMPLEMENTATION`: convert every blocking finding into a concrete task preserving finding IDs, apply fixes only when authorised, add regression tests, run relevant tests, re-run the Staff Engineer review on the updated diff, and update conformance and contradiction artifacts. Limit automatic review/fix cycles to three; after three failures for the same root cause, stop, set `RETURN_TO_PLAN` or `BLOCKED`, and identify the repeated root cause.

## Step 13 — Final decision matrix

| Condition | Verdict |
|---|---|
| Plan aligned, implementation complete, no blockers | `SHIP` |
| Only explicitly owned non-blocking findings remain | `SHIP WITH REQUIRED FIXES` |
| Correctable implementation defects | `RETURN TO IMPLEMENTATION` |
| Invalid architecture assumption | `RETURN TO PLAN` |
| Critical unresolved risk or missing evidence | `BLOCK` |

`SHIP WITH REQUIRED FIXES` requires every remaining item to be non-blocking P2/P3 with an owner and due condition; never use it to bypass a P1. `BLOCK` applies when a P0 remains, required evidence is unavailable, a critical dependency or approval is missing, or safe rollback is impossible for a high-impact change.
