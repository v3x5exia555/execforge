---
name: eng-level
description: Use when approved product requirements need engineering planning, implementation gating, plan-to-code traceability, Staff Engineer review, release readiness, or a SHIP/FIX/REPLAN/BLOCK decision.
license: MIT
compatibility: Requires a Git repository for diff review. Integrates with separately installed gstack and Superpowers skills when available.
metadata:
  author: ExecForge contributors
  version: "0.8.0"
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
- `status` — report state, including the deferred backlog, without starting a review.

Lifecycle artifacts are initiative-scoped. Resolve the selected run through the
authoritative `.execforge/current.json`; engineering state lives at
`.eng-level/runs/<run-id>/state.json`. The `.eng-level/current.json` file is a
compatibility projection, not stronger evidence than the run artifacts, Git,
code, runtime behavior, or tests.

For safe re-entry, use `python3 scripts/execforge.py resume --root <repo>` to
inspect bounded metadata and warnings, then
`python3 scripts/execforge.py next --root <repo>` to obtain exactly one derived
action. Do not print or follow the raw recorded `next_action`. Reconcile Git
conflicts, unsafe/stale state, lineage mismatches, and blockers before
advancing. Read [state and artifact contracts](references/state-and-artifacts.md).

## Roles

Roles are lenses, not stages. The lifecycle supplies the stages; roles attach to them.

- `architect` — system and data design, trade-offs, capacity and cost sizing, scale ceilings.
- `manager` — decomposition, sequencing, dependencies, acceptance criteria.
- `staff-engineer` — whole-branch diff review and conformance.
- `backend-engineer` — schema, queries, indexes, migrations, API contracts, data integrity.
- `platform-engineer` — deploy topology, containers, proxy, DNS, TLS, secrets, rollback.

`backend-engineer` and `platform-engineer` attach three times: advising at plan, building at
implement, auditing at review.

Defaults:

```text
--mode=plan    with no role → architect + manager
--mode=review  with no role → staff-engineer
--role=auto    (default)    → infer from the request and the change surface
```

**Do not require the user to name a role.** Infer it. Announce the routed set in one line
and proceed; accept a one-word correction. Do not open a confirmation gate.

Roles are model-honoured conventions, not enforced arguments. Nothing in the tooling
prevents a role from being ignored, so the discipline is the record: write the routed set to
`routed_roles`, `temperament`, and `adversarial_pair` in the selected
`.eng-level/runs/<run-id>/state.json` before the work starts, and report what
actually ran against what was routed. An unrecorded role did not run.

An explicit `--role` narrows the *advisory* lenses only. It never suppresses a lens the
lifecycle requires: `staff-engineer` always attaches when a diff exists, and `architect` plus
`manager` always attach at plan.

Read [role routing](references/role-routing.md) and [role contracts](references/role-contracts.md).

## Stop-after

`--stop-after=<product|plan|implement|review|qa>` halts the chain at that boundary, emits
its artifacts, and executes nothing beyond it.

Honour a stated intent to stop as if it were the parameter. "Plan it but do not deploy",
"keep it for next cycle", and "let me review first" all set `--stop-after`.

Write it to `stop_after` in the selected
`.eng-level/runs/<run-id>/state.json` the moment it is set. That record is what
makes the brake survive a later turn or a context compaction — an unrecorded
stop boundary does not exist. On every re-entry, read `stop_after` from state
before acting, and do not resume past it without a new instruction from the
user.

Deferred work goes to `.eng-level/runs/<run-id>/backlog.md`, not to a commit message. Read
[state and artifact contracts](references/state-and-artifacts.md).

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
2. Save `.eng-level/runs/<run-id>/upstream-requirements.md` in the selected run.
   Planning may not proceed while any gating flag has an unresolved authorization decision.
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

Every implementation task carries a binary pass test — the concrete condition that proves it
done. A plan whose tasks have no pass tests is `REVISE`; list the tasks missing one. Do not
accept "test until it works" as an acceptance criterion.

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

Dispatch `backend-engineer` and `platform-engineer` as specialist auditors when the diff
touches their surface. Pair an adversarial reviewer when the change is integrity-critical.
Read [subagent dispatch](references/subagent-dispatch.md) and use the
[reviewer briefs](references/reviewer-briefs.md) as written — the adversarial framing is the
mechanism, so do not paraphrase them into a summary.

## Post-hoc review

When a substantial diff exists but no approved selected-run
`.eng-level/runs/<run-id>/upstream-requirements.md` does, the work was built
before it was gated. Label the run:

```text
POST-HOC REVIEW — no approved upstream requirements existed for this diff.
```

Then:

- Issue `FIX` or `BLOCK` normally.
- Do not issue `SHIP`. The strongest available verdict is `SHIP WITH REQUIRED FIXES (UNGATED)`.
- State what a plan review would have asked before this was built.

Do not stop to ask permission and do not refuse the review. Run it, and make the cost of the
skipped gate visible in the output.

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
- `SHIP WITH REQUIRED FIXES (UNGATED)` — post-hoc review ceiling
- `RETURN TO IMPLEMENTATION`
- `RETURN TO PLAN`
- `BLOCK`

No role and no subagent issues a final decision. Roles return findings.

Rules:

- Any unresolved P0/P1 blocks shipping.
- Code defects with valid architecture return to implementation.
- Invalid architecture assumptions return to plan.
- Missing critical evidence or unsafe rollback blocks.
- A post-hoc review cannot return `SHIP`.
- A stop-after boundary ends the run at that stage; no verdict beyond it is issued.
- A `SHIP` verdict ends the lifecycle; ExecForge does not deploy. When the
  installed gstack `/land-and-deploy` or `/ship` skill is present, hand the
  approved branch to it and record the handoff in `decision.md`. When it is
  not, deployment stays with the operator's own release process.
- A `SHIP` on a release-bound branch (version bump, changelog entry, or tag)
  requires release-consistency evidence: version metadata, the changelog head
  entry, and the intended tag must agree. In the ExecForge repository, run
  `python3 scripts/execforge.py release-check` (add `--tag vX.Y.Z` when
  tagging) and record the output in `decision.md`; a failing check is a P1.
  In other repositories, verify the equivalent manifests manually and record
  what was checked.
- Maximum three automatic fix/review cycles before replan or block.

Read [state and artifact contracts](references/state-and-artifacts.md). For a full run, follow [the step-by-step lifecycle protocol](references/lifecycle-protocol.md) and produce [the final output contract](references/fallback-review-contracts.md).

## Validation gate

Before returning:

- Upstream requirements were approved, or the run is labelled `POST-HOC REVIEW`.
- Plan review occurred before implementation, or the run is labelled `POST-HOC REVIEW`.
- A real diff existed before Staff review.
- Every implementation task carried a binary pass test.
- Every requirement and task has a conformance status.
- Roles were routed and the routed set was announced.
- Every dispatched subagent's findings were verified before adoption; no subagent issued a
  ship verdict.
- Tests claimed as passing were actually run.
- Applicable portal/API/backend QA completed with `QA PASS` or explicitly accepted non-blocking risks.
- QA-driven production-code changes received a final delta review and retest.
- Contradictions and deviations are recorded.
- No P0/P1 is hidden behind conditional shipping.
- The final verdict is traceable to evidence.
