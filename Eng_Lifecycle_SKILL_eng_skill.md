---
name: eng-lifecycle
description: >
  Engineering lifecycle orchestrator that runs the gstack plan-stage Engineering
  Manager review before implementation, preserves the approved plan and baseline,
  then runs the gstack Staff Engineer review against the actual branch diff.
  Reconciles plan versus implementation and issues a final SHIP, FIX, REPLAN, or
  BLOCK decision.
version: 0.2.0
tags:
  - engineering
  - architecture
  - code-review
  - staff-engineer
  - lifecycle
  - orchestration
  - gstack
---

# /eng-lifecycle — Plan → Build → Staff Review

## Purpose

Use this skill to coordinate two distinct engineering review stages:

```text
                    Engineering Lifecycle Orchestrator
                                 │
                    ┌────────────┴────────────┐
                    │                         │
          PRE-IMPLEMENTATION             POST-IMPLEMENTATION
                    │                         │
          /plan-eng-review                  /review
                    │                         │
          Approved Engineering Plan   Staff Engineer Findings
                    │                         │
                    └──── Implementation ────┘
                                 │
                         Final Ship Decision
```

The skill does not merge the two reviewers into one generic voice.

- `/plan-eng-review` determines whether the proposed engineering approach is
  correct, complete, testable, and appropriately simple before coding.
- `/review` audits the actual Git diff after coding and searches for production
  failures, incomplete work, unsafe deviations, and missing tests.
- `/eng-lifecycle` owns sequencing, state, artifacts, evidence reconciliation,
  re-entry, and the final engineering gate.

---

# Upstream Requirement Intake and User Stop Check

When an approved CEO, COO, product, ExecForge, PRD, or product-strategy plan
already exists, treat it as an upstream decision package.

The engineering lifecycle must not reinterpret or silently replace the upstream
product decision.

## Required Upstream Package

Extract and preserve:

- Product or initiative name
- Approved problem statement
- Primary user
- Product hypothesis
- Accepted scope
- Deferred scope
- Skipped scope
- Non-goals
- User-success metrics
- Business-success metrics
- Non-negotiable CEO decisions
- Non-negotiable COO controls
- Security, privacy, and compliance requirements
- Cost or operational constraints
- Rollout conditions
- Kill or sunset criteria
- Known assumptions
- Known unknowns
- Final upstream decision
- Upstream decision owner
- Source file or source reference

Write the interpreted package to:

```text
.eng-lifecycle/upstream-requirements.md
```

## Upstream Understanding Check

Before invoking either engineering reviewer, the Engineering Lifecycle
Orchestrator must produce a concise requirement interpretation containing:

1. What is being built
2. Why it is being built
3. Who it is for
4. What is explicitly in scope
5. What is explicitly out of scope
6. What must not be changed
7. What engineering may still decide
8. What success looks like
9. What would cause the project to stop
10. Which assumptions still require validation

## Mandatory User Stop Check

After interpreting the upstream package, stop and ask the user to confirm:

> I have translated the approved CEO/COO/product plan into the engineering
> requirements below. Is this the correct source of truth for the engineering
> reviews?

Allowed user responses:

- `APPROVE UPSTREAM`
- `APPROVE WITH CHANGES`
- `REJECT UPSTREAM INTERPRETATION`
- `REOPEN PRODUCT DECISION`

The lifecycle state must become:

```text
UPSTREAM_APPROVAL_REQUIRED
```

Do not invoke `/plan-eng-review`, begin implementation, or invoke `/review`
until the user has approved the upstream interpretation.

## Approval Behaviour

### `APPROVE UPSTREAM`

- Lock `.eng-lifecycle/upstream-requirements.md`
- Record approval timestamp and approver
- Continue to `/plan-eng-review`

### `APPROVE WITH CHANGES`

- Apply the user's corrections
- Show the revised interpretation
- Ask for approval again
- Do not continue until explicitly approved

### `REJECT UPSTREAM INTERPRETATION`

- Preserve the rejected interpretation for audit history
- Correct the interpretation
- Ask for approval again

### `REOPEN PRODUCT DECISION`

- Stop the engineering lifecycle
- Return control to the CEO/COO/product planning workflow
- Set lifecycle state to `RETURN_TO_PRODUCT_PLAN`

## No-Silent-Assumption Rule

If the upstream package is incomplete:

- Do not fill the gap with invented product requirements
- Mark the missing item as `UNKNOWN`
- Show whether the gap blocks engineering planning
- Ask the user to approve the assumption or reopen the product decision

Engineering reviewers may propose technical options, but they may not redefine
the product outcome without explicit user approval.

---

# Shared Understanding for Both Engineering Actors

Both engineering actors must understand the same approved upstream
requirements, but they use them differently.

## Plan Engineering Reviewer Receives

- Approved upstream requirements
- Accepted and rejected product scope
- Non-goals
- Success metrics
- Non-negotiable CEO decisions
- Non-negotiable COO controls
- Known assumptions and unknowns
- Repository context
- Existing architecture and constraints

Its responsibility is:

> Convert the approved product decision into a correct and complete engineering
> plan without changing the approved product intent.

## Staff Engineering Reviewer Receives

- The same approved upstream requirements
- The approved engineering plan
- Plan conditions and controls
- Actual Git diff
- Test results
- Known intentional deviations

Its responsibility is:

> Verify that the implementation satisfies both the approved product
> requirements and the approved engineering plan.

## Upstream Traceability Matrix

Maintain:

```text
.eng-lifecycle/upstream-traceability.md
```

Use:

| Upstream Requirement | Source | Engineering Plan Item | Implementation Evidence | Test Evidence | Status |
|---|---|---|---|---|---|

Statuses:

- `SATISFIED`
- `PARTIAL`
- `NOT SATISFIED`
- `CHANGED WITH APPROVAL`
- `UNVERIFIABLE`
- `NOT APPLICABLE`

A requirement cannot be marked `SATISFIED` without implementation or test
evidence where such evidence is applicable.

---

# When to Invoke

Invoke when the user asks to:

- Review an engineering plan and then review its implementation
- Orchestrate plan review and Staff Engineer review
- Run a complete engineering lifecycle gate
- Validate architecture before coding and code before merging
- Compare an approved plan against the implemented branch
- Decide whether work should ship, return to implementation, or return to plan

Example:

```text
/eng-lifecycle Review and gate this feature from engineering plan through final diff.
```

Optional modes:

```text
/eng-lifecycle --mode=plan
/eng-lifecycle --mode=review
/eng-lifecycle --mode=full
/eng-lifecycle --mode=auto
/eng-lifecycle --mode=status
```

Default:

```text
--mode=auto
```

---

# Non-Negotiable Separation of Duties

Use this topology:

```text
Plan Engineering Reviewer
            \
             Engineering Lifecycle Orchestrator → Final Engineering Decision
            /
Staff Engineering Reviewer
```

Rules:

1. The plan reviewer evaluates intended implementation before coding.
2. The Staff Engineer evaluates actual implementation after coding.
3. The Staff Engineer receives the approved plan as comparison evidence but
   must independently inspect the repository and diff.
4. The plan reviewer must not approve code that does not yet exist.
5. The Staff Engineer must not treat plan intent as proof of implementation.
6. Neither nested reviewer owns the final lifecycle verdict.
7. Only the Engineering Lifecycle Orchestrator may issue:
   - `SHIP`
   - `SHIP WITH REQUIRED FIXES`
   - `RETURN TO IMPLEMENTATION`
   - `RETURN TO PLAN`
   - `BLOCK`
8. Do not run both reviews in parallel. Their inputs belong to different
   lifecycle stages.
9. Do not claim a full lifecycle review when the implementation checkpoint has
   not been reached.
10. Preserve the original findings of both reviewers; do not silently rewrite
    one review to make it agree with the other.

---

# Upstream Skill Resolution

This is a meta-skill. It orchestrates the installed gstack skills rather than
copying or replacing them.

Resolve the upstream skills in this order:

## Plan Review

Look for:

```text
~/.claude/skills/gstack/plan-eng-review/SKILL.md
.claude/skills/gstack/plan-eng-review/SKILL.md
agents/skills/gstack-plan-eng-review/SKILL.md
```

## Staff Engineer Review

Look for:

```text
~/.claude/skills/gstack/review/SKILL.md
.claude/skills/gstack/review/SKILL.md
agents/skills/gstack-review/SKILL.md
```

When a matching skill exists:

1. Read its complete current instructions.
2. Execute it as a nested workflow.
3. Follow its current contract rather than relying on remembered behaviour.
4. Do not modify the upstream skill.
5. Record the resolved path and, when available, its version or Git commit.

When an upstream skill is unavailable:

- Do not pretend it ran.
- Mark the missing dependency.
- Use the fallback review contract in this file only when the user requests
  best-effort continuation.
- Lower confidence in the final verdict.

---

# Operating Modes

## `--mode=plan`

Run only the pre-implementation engineering review.

Output:

- Approved or rejected engineering plan
- Architecture and data-flow decisions
- Edge cases
- Test matrix
- Performance expectations
- Security and reliability requirements
- Implementation task list
- Baseline Git metadata
- Conditions required before implementation

Stop after the implementation checkpoint.

## `--mode=review`

Run only the Staff Engineer review against the current branch diff.

Requirements:

- A Git repository
- A resolvable base branch or base commit
- A non-empty implementation diff

Use an approved plan when available. If no plan exists, perform a diff review
without claiming plan conformance.

## `--mode=full`

Run the plan review first. Continue through implementation only when:

- The current agent is explicitly authorised to modify code, and
- The implementation can be completed in the current session.

After implementation, run the Staff Engineer review and final lifecycle gate.

When implementation cannot be performed in the current invocation, save the
checkpoint and stop honestly at `WAITING_FOR_IMPLEMENTATION`.

## `--mode=auto`

Detect the current lifecycle state and run the next valid stage.

## `--mode=status`

Read lifecycle artifacts and Git state. Report:

- Current stage
- Plan status
- Base commit
- Diff status
- Open findings
- Next required action

Do not run a new review.

---

# Lifecycle State Machine

Use exactly one state.

```text
NO_CONTEXT
    ↓
UPSTREAM_INTAKE
    ↓
UPSTREAM_APPROVAL_REQUIRED
    ├── Reopen product decision ─────→ RETURN_TO_PRODUCT_PLAN
    ↓
PLAN_REQUIRED
    ↓
PLAN_REJECTED ───────────────→ BLOCKED
    ↓
PLAN_APPROVED
    ↓
WAITING_FOR_IMPLEMENTATION
    ↓
IMPLEMENTATION_IN_PROGRESS
    ↓
REVIEW_READY
    ↓
STAFF_REVIEW_FAILED ─────────→ RETURN_TO_IMPLEMENTATION
    │                                  │
    │                                  └────→ REVIEW_READY
    │
    ├── Architecture assumption invalid → RETURN_TO_PLAN
    │                                        │
    │                                        └────→ PLAN_REQUIRED
    │
    └── Critical blocker ───────────────→ BLOCKED

REVIEW_PASSED
    ↓
SHIP_READY
```

## State Definitions

### `NO_CONTEXT`

The initiative, repository, base branch, or intended change cannot be
identified.

### `UPSTREAM_INTAKE`

An existing CEO, COO, product, PRD, or ExecForge plan is being translated into
an engineering requirement package.

### `UPSTREAM_APPROVAL_REQUIRED`

The translated upstream requirements are waiting for explicit user approval.
No engineering review or implementation may begin.

### `RETURN_TO_PRODUCT_PLAN`

The engineering lifecycle is paused because the approved product intent,
scope, controls, or success criteria must be reopened upstream.

### `PLAN_REQUIRED`

No approved engineering plan exists for the intended change.

### `PLAN_REJECTED`

The plan has unresolved architecture, safety, data-integrity, performance, or
testability blockers.

### `PLAN_APPROVED`

The engineering plan is sufficiently complete to begin implementation.

### `WAITING_FOR_IMPLEMENTATION`

The plan is approved, but no implementation diff exists yet.

### `IMPLEMENTATION_IN_PROGRESS`

A diff exists, but required implementation tasks or tests are incomplete.

### `REVIEW_READY`

A meaningful diff exists and the implementation is ready for Staff Engineer
review.

### `STAFF_REVIEW_FAILED`

The actual implementation has findings that prevent shipping.

### `RETURN_TO_IMPLEMENTATION`

The architecture remains valid; code or tests must be corrected.

### `RETURN_TO_PLAN`

The implementation exposed a false or incomplete architecture assumption.
Planning must be reopened.

### `BLOCKED`

A dependency, security issue, data-integrity risk, missing evidence, or
unresolvable critical failure prevents safe continuation.

### `REVIEW_PASSED`

No unresolved blocking Staff Engineer findings remain.

### `SHIP_READY`

The approved plan, implementation, tests, and required controls are aligned.

---

# Artifact Directory

Store lifecycle artifacts in:

```text
.eng-lifecycle/
```

Recommended layout:

```text
.eng-lifecycle/
├── state.json
├── context.md
├── upstream-requirements.md
├── upstream-traceability.md
├── upstream-approval.md
├── engineering-plan.md
├── implementation-tasks.md
├── test-matrix.md
├── plan-review.md
├── staff-review.md
├── conformance.md
├── contradictions.md
├── decision.md
└── runs/
    └── <timestamp>/
```

Do not place secrets, credentials, tokens, or sensitive production data in
these artifacts.

---

# State Contract

Maintain `.eng-lifecycle/state.json`.

Example schema:

```json
{
  "version": "1",
  "initiative": "feature-name",
  "mode": "auto",
  "state": "UPSTREAM_APPROVAL_REQUIRED",
  "upstream_source": "<path-or-reference>",
  "upstream_approval_status": "PENDING",
  "upstream_approved_by": null,
  "upstream_approved_at": null,
  "base_branch": "main",
  "base_commit": "<sha>",
  "plan_path": ".eng-lifecycle/engineering-plan.md",
  "plan_status": "APPROVED_WITH_CONDITIONS",
  "plan_reviewed_at": "<ISO-8601>",
  "implementation_head": null,
  "staff_reviewed_at": null,
  "final_decision": null,
  "open_blockers": [],
  "required_conditions": []
}
```

Update state only after the relevant stage is actually completed.

Never write:

- `PLAN_APPROVED` before the plan review finishes
- `REVIEW_PASSED` before the branch diff is reviewed
- `SHIP_READY` while blocking findings remain

---

# Step 0 — Establish Repository and Initiative Context

Determine:

- Repository root
- Current branch
- Base branch
- Merge base
- Current HEAD
- Working-tree status
- Whether a diff exists
- Initiative name
- User objective
- Existing plan artifacts
- Relevant design or product decisions
- Test commands
- Build commands
- CI configuration
- Repository conventions

Prefer repository evidence over assumptions.

Useful Git evidence includes:

```bash
git rev-parse --show-toplevel
git status --short
git branch --show-current
git remote show origin
git merge-base HEAD <base>
git diff --stat <base>...HEAD
git diff --name-status <base>...HEAD
```

Do not mutate the repository during context discovery.

## Base Branch Resolution

Resolve in this order:

1. Explicit user-provided base branch
2. Pull-request base branch from available metadata
3. Remote default branch
4. `main`
5. `master`

If unresolved, ask only when the decision materially changes the diff. When
interaction is unavailable, mark the base as unknown and do not issue a ship
verdict.

---

# Step 1 — Detect Lifecycle State

Use evidence:

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

---

# Step 2 — Create the Shared Engineering Context

Write `.eng-lifecycle/context.md` containing:

## Initiative

- Problem
- Intended user or system outcome
- Scope
- Non-goals
- Constraints
- Dependencies

## Repository

- Current branch
- Base branch
- Base commit
- Current HEAD
- Relevant directories
- Existing architecture patterns
- Test and build commands

## Evidence Labels

Label material claims:

- `FACT`
- `ASSUMPTION`
- `INFERENCE`
- `UNKNOWN`

Do not invent requirements to make the plan appear complete.

---

# Step 3 — Run `/plan-eng-review`

Run when state is `PLAN_REQUIRED`, or when a Staff Engineer finding requires
`RETURN_TO_PLAN`.

Supply the nested reviewer with:

- User-approved upstream requirements
- Upstream traceability matrix
- Shared engineering context
- Product or feature plan
- Existing repository patterns
- Known constraints
- Relevant previous review findings
- Any specific architecture questions

The plan review must cover at minimum:

1. Architecture
2. Component boundaries
3. Data flow and state transitions
4. Reuse versus new abstractions
5. Failure paths
6. Idempotency and retries where relevant
7. Security and trust boundaries
8. Data integrity and migration safety
9. Performance and capacity assumptions
10. Observability
11. Rollback and reversibility
12. Test strategy
13. Exact implementation tasks
14. Files or modules expected to change
15. Definition of done

## Plan Verdict

Select exactly one:

- `APPROVED`
- `APPROVED_WITH_CONDITIONS`
- `REVISE`
- `REJECTED`
- `UNVERIFIABLE`

### `APPROVED`

The implementation approach is ready.

### `APPROVED_WITH_CONDITIONS`

Implementation may begin only with recorded mandatory conditions.

### `REVISE`

The core direction may work, but the plan must be corrected before coding.

### `REJECTED`

The proposed approach is unsafe, unnecessarily complex, or misaligned.

### `UNVERIFIABLE`

Critical repository, dependency, schema, or requirement evidence is unavailable.

## Required Plan Artifacts

Write:

- `.eng-lifecycle/plan-review.md`
- `.eng-lifecycle/engineering-plan.md`
- `.eng-lifecycle/implementation-tasks.md`
- `.eng-lifecycle/test-matrix.md`

## Implementation Task Format

```markdown
- [ ] **T1 — <imperative task title>**
  - Why: <finding or requirement>
  - Files: <expected paths>
  - Dependencies: <task IDs or external dependencies>
  - Verify: <exact test or observable result>
  - Risk: <Low / Medium / High>
```

Every task must be traceable to a plan finding or requirement.

---

# Step 4 — Lock the Baseline

After the plan is approved:

Record:

- Base branch
- Merge-base commit
- Plan approval timestamp
- Current HEAD
- Approved scope
- Non-goals
- Required controls
- Required tests
- Performance expectations

The baseline prevents the later review from comparing the implementation
against a moving or vague target.

Do not modify Git history merely to create this record.

---

# Step 5 — Implementation Checkpoint

After plan approval, decide whether implementation can continue now.

## Continue in Current Invocation

Continue only when:

- The user authorised implementation
- Required tools are available
- The work can be performed and verified now
- No mandatory external approval is pending

## Stop at Checkpoint

Stop with state `WAITING_FOR_IMPLEMENTATION` when:

- Another developer or agent will implement
- The user requested review only
- External work is required
- The implementation cannot be completed now
- The repository is read-only
- Critical decisions remain open

Output:

```text
Plan status: <status>
Lifecycle state: WAITING_FOR_IMPLEMENTATION
Approved plan: .eng-lifecycle/engineering-plan.md
Implementation tasks: .eng-lifecycle/implementation-tasks.md
Resume command: /eng-lifecycle --mode=auto
```

Do not promise background execution.

---

# Step 6 — Determine Review Readiness

Before running `/review`, verify:

- A meaningful branch diff exists
- The base branch or commit is known
- Build or test commands are discoverable
- Claimed implementation tasks have statuses
- Generated or vendored files are distinguishable
- The working tree state is recorded
- Required migrations or configuration changes are visible

If there is no diff:

- Do not run Staff Engineer review.
- Return `WAITING_FOR_IMPLEMENTATION`.

If work is visibly incomplete:

- Set `IMPLEMENTATION_IN_PROGRESS`.
- Report missing tasks.
- Do not issue a ship decision.

---

# Step 7 — Run `/review` as Staff Engineer

Supply the nested reviewer with:

- User-approved upstream requirements
- Upstream traceability matrix
- Base branch or base commit
- Actual branch diff
- Approved engineering plan, when available
- Implementation task list
- Test matrix
- Plan conditions
- Known intentional deviations

The Staff Engineer must inspect actual repository evidence.

The review must cover at minimum:

1. Correctness
2. Production failure modes
3. Race conditions and concurrency
4. Idempotency and retry behaviour
5. Transactions and partial failure
6. Trust boundaries and input validation
7. Authentication and authorisation where relevant
8. Data integrity and migration safety
9. Query count, indexes, and performance
10. Resource leaks
11. Error handling and observability
12. Backward compatibility
13. Missing enum, state, or edge-case handling
14. Test realism and regression coverage
15. Plan completion
16. Scope drift
17. Rollback safety

## Finding Severity

Use:

- `P0` — Immediate critical security, corruption, outage, or irreversible-loss risk
- `P1` — Must fix before merge
- `P2` — Important improvement; may be conditionally deferred with explicit owner
- `P3` — Non-blocking polish or maintainability improvement

Every finding must include:

- Evidence
- File and line where possible
- Failure scenario
- Severity
- Required action
- Verification method

Do not create findings from style preference alone unless repository standards
make them material.

## Staff Review Artifact

Write:

```text
.eng-lifecycle/staff-review.md
```

---

# Step 8 — Plan-to-Implementation Conformance

Compare every approved task and control against actual implementation.

Use:

| Status | Meaning |
|---|---|
| `DONE` | Fully implemented and verified |
| `PARTIAL` | Some required behaviour is present |
| `NOT DONE` | Planned work is missing |
| `CHANGED` | Different implementation, same validated outcome |
| `SCOPE DRIFT` | Unapproved functionality or architecture was introduced |
| `UNVERIFIABLE` | Available evidence cannot confirm completion |
| `NO LONGER NEEDED` | New verified evidence makes the task unnecessary |

Write:

```text
.eng-lifecycle/conformance.md
```

Format:

| Task | Status | Plan Requirement | Implementation Evidence | Tests | Action |
|---|---|---|---|---|---|

Rules:

1. `CHANGED` is not automatically a failure.
2. A changed approach must still satisfy the original outcome and controls.
3. `SCOPE DRIFT` requires explicit review.
4. `NOT DONE` on a blocking task prevents shipping.
5. Passing tests do not prove an untested requirement.
6. A file existing does not prove the behaviour is correct.

---

# Step 9 — Evidence Precedence

When plan intent conflicts with implementation evidence, use:

```text
1. Reproducible runtime behaviour and executed tests
2. Actual source code, schema, and configuration
3. Git diff and commit history
4. Approved engineering plan
5. Comments, task descriptions, and stated intent
6. Unsupported assumptions
```

This does not mean actual code is automatically acceptable. It means the actual
code is authoritative evidence of what was built.

Example:

```text
Plan: Retry is idempotent.
Code: Retry inserts a second record.
Decision: The implementation is not idempotent. Return to implementation.
```

Never preserve a false plan claim merely because it was previously approved.

---

# Step 10 — Contradiction and Deviation Register

Write:

```text
.eng-lifecycle/contradictions.md
```

Use:

| ID | Topic | Plan Claim | Implementation Finding | Type | Evidence | Resolution | Owner |
|---|---|---|---|---|---|---|---|

Types:

- `IMPLEMENTATION BUG`
- `PLAN ASSUMPTION INVALID`
- `INTENTIONAL DEVIATION`
- `SCOPE DRIFT`
- `MISSING EVIDENCE`
- `TEST CONTRADICTION`

## Resolution Rules

### Implementation Bug

Return to implementation.

### Plan Assumption Invalid

Return to plan and update architecture before further fixes.

### Intentional Deviation

Accept only when:

- The outcome is equal or better
- Risks are understood
- Required controls remain intact
- Tests verify the new approach
- The decision is recorded

### Scope Drift

Remove, defer, or explicitly approve the additional scope.

### Missing Evidence

Do not guess. Add a verification action.

### Test Contradiction

Reproduce the behaviour, inspect test validity, and resolve before shipping.

---

# Step 11 — Replan Triggers

Return to plan when any of these are true:

- The selected architecture cannot satisfy a core requirement
- The implementation requires a new system of record not reviewed in the plan
- A migration is unsafe under real schema constraints
- Required performance cannot be achieved without architectural change
- The retry, consistency, or transaction model is fundamentally wrong
- Security boundaries differ materially from the approved design
- The implementation reveals a missing upstream or downstream contract
- Fixing the issue would touch substantially more scope than planned
- More than three implementation-fix cycles fail for the same root cause
- A supposedly reversible decision is discovered to be difficult to reverse

Do not repeatedly patch code when the architecture is the problem.

---

# Step 12 — Fix Loop

When the decision is `RETURN_TO_IMPLEMENTATION`:

1. Convert every blocking finding into a concrete task.
2. Preserve original finding IDs.
3. Apply fixes only when authorised.
4. Add or update regression tests.
5. Run relevant tests.
6. Re-run Staff Engineer review on the updated diff.
7. Update conformance and contradiction artifacts.
8. Limit automatic review/fix cycles to three.

After three unsuccessful cycles:

- Stop.
- Set `RETURN_TO_PLAN` or `BLOCKED`.
- Identify the repeated root cause.
- Do not claim the next patch will probably work.

---

# Step 13 — Final Engineering Decision

Only the Engineering Lifecycle Orchestrator issues the final decision.

Select exactly one:

## `SHIP`

Use when:

- No unresolved P0 or P1 findings remain
- Required plan tasks are done
- Required tests pass
- Mandatory controls are implemented
- No blocking scope drift exists
- Rollback is understood
- Evidence supports production readiness

## `SHIP WITH REQUIRED FIXES`

Use only when:

- Remaining items are non-blocking P2/P3
- Each item has an owner and due condition
- No security, corruption, compliance, or availability blocker remains
- Deferral is explicit rather than accidental

Do not use this verdict to bypass a P1.

## `RETURN TO IMPLEMENTATION`

Use when:

- Architecture remains valid
- Code, configuration, migration, or tests require correction
- The problem can be fixed without reopening the core design

## `RETURN TO PLAN`

Use when:

- A fundamental assumption is wrong
- Architecture or data flow must change
- The implementation cannot meet requirements under the approved design
- Scope or dependencies changed materially

## `BLOCK`

Use when:

- A P0 remains
- Required evidence is unavailable
- A critical dependency or approval is missing
- Safe rollback is impossible for a high-impact change
- Data integrity, security, or compliance cannot be protected

---

# Final Decision Matrix

| Condition | Verdict |
|---|---|
| Plan aligned, implementation complete, no blockers | `SHIP` |
| Only explicitly owned non-blocking findings remain | `SHIP WITH REQUIRED FIXES` |
| Correctable implementation defects | `RETURN TO IMPLEMENTATION` |
| Invalid architecture assumption | `RETURN TO PLAN` |
| Critical unresolved risk or missing evidence | `BLOCK` |

---

# Final Output Contract

Produce:

## Engineering Lifecycle Summary

- Initiative
- Upstream source
- Upstream approval status
- Upstream approver
- Mode
- Current branch
- Base branch and commit
- Lifecycle state
- Plan verdict
- Staff review verdict
- Final decision
- Confidence

## Plan Status

- Architecture decision
- Key controls
- Required tests
- Approved scope
- Non-goals

## Implementation Conformance

- Done
- Partial
- Missing
- Changed
- Scope drift
- Unverifiable

## Blocking Findings

List each P0/P1 with evidence and required action.

## Non-Blocking Findings

List owned P2/P3 items.

## Contradictions Resolved

State:

- Plan claim
- Actual evidence
- Resolution

## Verification

Include exact commands run and their results.

## Final Decision

Use:

> **Decision: [SHIP / SHIP WITH REQUIRED FIXES / RETURN TO IMPLEMENTATION /
> RETURN TO PLAN / BLOCK]**

Then explain:

- Why
- Evidence supporting it
- Required next action
- Owner
- Re-entry condition

Write the same result to:

```text
.eng-lifecycle/decision.md
```

---

# Final Validation Gate

Before returning the answer, verify:

- The upstream CEO/COO/product requirements were captured when available
- The user explicitly approved the upstream interpretation
- Both engineering actors received the same approved upstream requirements
- Upstream requirements are traceable to plan items and implementation evidence
- The current lifecycle state was detected from evidence
- `/plan-eng-review` ran before implementation, or its absence is clearly stated
- The approved plan and baseline were preserved
- A real diff existed before `/review` ran
- `/review` inspected actual repository evidence
- Every approved plan task has a conformance status
- Every P0/P1 has an action
- No unsupported metric or test claim is presented as fact
- Plan/code contradictions are recorded
- Architecture failures return to plan rather than endless patching
- No P0/P1 is hidden behind `SHIP WITH REQUIRED FIXES`
- The final decision is issued only by the orchestrator
- The final decision is traceable to evidence

If any check fails, revise the result or lower the verdict.

---

# Fallback Plan Review Contract

Use only when the installed `/plan-eng-review` skill cannot be resolved and the
user asks to continue.

Evaluate:

- Architecture
- Data flow
- State transitions
- Error paths
- Security boundaries
- Data integrity
- Performance
- Observability
- Rollback
- Tests
- Implementation tasks

Clearly label:

```text
Fallback plan review used; upstream gstack /plan-eng-review was unavailable.
```

---

# Fallback Staff Review Contract

Use only when the installed `/review` skill cannot be resolved and the user asks
to continue.

Inspect:

- Diff correctness
- Failure modes
- Concurrency
- Transactions
- Validation
- Security
- Data integrity
- Performance
- Compatibility
- Tests
- Plan completion
- Scope drift

Clearly label:

```text
Fallback Staff Engineer review used; upstream gstack /review was unavailable.
```

A fallback review cannot claim exact behavioural equivalence with gstack.

---

# Integration with ExecForge

When invoked after the ExecForge CEO/COO decision:

```text
CEO Subagent
    \
     ExecForge Main Orchestrator → Product Decision
    /
COO Subagent
             ↓
       /eng-lifecycle
             ↓
      /plan-eng-review
             ↓
       Implementation
             ↓
          /review
             ↓
   Final Engineering Decision
```

Pass into this skill and require explicit user approval before engineering review:

- Approved product hypothesis
- Accepted scope
- Deferred scope
- Non-goals
- Non-negotiable COO controls
- MVP success criteria
- Kill conditions

ExecForge decides whether the initiative should be built.

`/eng-lifecycle` decides whether the engineering plan and implementation are
safe and complete enough to ship.

---

# Guiding Principles

1. Plan intent is not implementation evidence.
2. Passing CI is not proof of production safety.
3. A Staff Engineer review cannot repair a fundamentally invalid plan.
4. A strong plan cannot excuse a broken implementation.
5. Actual behaviour outranks comments and intentions.
6. Findings require actions, owners, and verification.
7. Repeated failed patches are an architecture signal.
8. Do not add process where the change is small and reversible.
9. Never claim a lifecycle stage that did not occur.
10. Ship only when the evidence supports it.
