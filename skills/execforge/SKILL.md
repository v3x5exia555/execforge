---
name: execforge
description: Use when evaluating whether to build, expand, reduce, pilot, defer, or kill a product, feature, platform, automation, AI capability, data initiative, or costly cross-team change.
license: MIT
compatibility: Supports real subagents when available and isolated simulated review passes otherwise.
metadata:
  author: ExecForge contributors
  version: "0.7.2"
---

# ExecForge Product Decision

## Core principle

Find the smallest evidence-backed scope that creates measurable user value without uncontrolled operational debt.

## Ponytail fast-path pre-check

When `execforge` is triggered directly (bypassing the `c-level` router), first check
whether the request is actually a concrete low-impact implementation job rather than a
build/expand/reduce/pilot/defer/kill decision. If it meets ALL of the low-impact
criteria in the `c-level` "Ponytail fast path" section (single repo, reversible in one
revert, no auth/secrets/trust-boundary/schema/data-migration surface, no new
dependency, no governance gate output) and the vendored `ponytail` skill is installed,
state that the fast path applies and route it to `ponytail lite` under the same
procedure — TDD precedence and explicit user approval before any commit included —
instead of running a product review. Any doubt about impact, or any request that is a
genuine product decision, runs the normal process below.

## Required topology

```text
CEO Subagent
    \
     Main Orchestrator → Final Product Decision
    /
COO Subagent
```

The CEO and COO are advisory. Only the Main Orchestrator issues the final verdict.

## Mode selection

Use a single isolated review for small, low-risk, reversible changes.

Use dual subagents when two or more apply:

- Multiple business units
- Production architecture change
- Sensitive or regulated data
- Difficult rollback
- New service, database, vendor, or system of record
- Material financial, legal, security, customer, or reputational impact
- Weak or disputed evidence

## Shared context

Before dispatch, create one neutral package:

- Initiative and target user
- Current workflow and pain
- Proposed change
- Evidence
- Constraints, deadlines, dependencies
- Known facts, assumptions, inferences, and unknowns

Send the same factual package to both reviewers. Do not expose one review to the other before their independent first pass.

## New platform role baseline

When the initiative is a new platform, product, portal, or tenant-facing system, it
always ships these four roles. Put them in the scope ledger as `ADD NOW`; they are not
a later phase.

| Role | Sees and controls |
|---|---|
| `superadmin` | The whole platform across every account. Held by the platform operator, never by a customer. |
| `accountadmin` | One customer account or tenant end to end: its plan, billing, admins, and account-wide settings. |
| `admin` | One workspace or team inside an account: its members, settings, and data. |
| `user` | Own work only. No setting that changes another person's access. |

Rules:

- Deny by default. A role gets only what its own scope needs, and no role reads or
  writes another account's data.
- Every action by `superadmin`, `accountadmin`, and `admin` is audit-logged with actor,
  target, and time.
- Extra roles are allowed on top of the baseline when evidence shows a real job the four
  do not cover. Removing, renaming, or merging a baseline role is a scope decision: put
  the reason in the ledger with an owner and a date.
- The role model touches auth, so attach `sec-level` before build.

## CEO Subagent

The CEO Subagent independently evaluates:

- Whether the user actually needs the initiative
- Product-market fit
- User pain
- Product hypothesis
- 10-star user experience
- 10× product opportunity
- Scope mode
- Platonic Ideal
- MVP scope
- Adoption
- Strategic moat
- Business impact
- Add / Defer / Skip recommendations

The CEO must challenge technically interesting work that lacks user value.

### CEO output contract

The CEO returns only an advisory review containing:

- Gatekeeper recommendation
- Evidence-labelled product claims
- Scope-mode recommendation
- 10× opportunity
- Platonic Ideal
- Proposed Add / Defer / Skip items
- Adoption and moat assessment
- Product risks
- Confidence level
- Questions or facts requiring verification

The CEO must not produce the final executive verdict.

### CEO plan

The internal CEO Subagent review above ALWAYS runs. It is never replaced, skipped, or
shortened by any external integration.

When the installed gstack `plan-ceo-review` skill is available, run it IN ADDITION to
the internal review to produce a second, independent CEO plan artifact. Present both
findings; route any disagreement between them through the orchestrator's contradiction
register like any other strategic disagreement. When gstack is unavailable, state that
only the internal CEO Subagent contract ran and label the output:

```text
Fallback CEO plan used; upstream gstack /plan-ceo-review was unavailable.
```

Whichever paths run, the combined CEO plan must include:

- **A-C-T-I-O-N operational matrix** — assess the problem, cost optimisation, technical
  tactics, security/governance/compliance controls, operational work reduction, and no
  manual work by default, per
  [execution and governance detail](references/execution-and-governance.md).
- **OKR plan** — product hypothesis, job-to-be-done, one qualitative objective, and two
  to four measurable key results with real baselines, per Phase 8 in
  [the detailed review phases](references/review-phases.md).

A fallback CEO plan cannot claim exact behavioural equivalence with gstack.

## COO Subagent

The COO Subagent independently evaluates:

- Total cost of ownership
- Scalability
- Reliability
- Compliance
- Security
- Privacy
- Architecture
- Operational readiness
- Support burden
- Automation
- Failure recovery
- Data lineage
- Auditability
- Ownership
- Technical debt
- Sunset criteria

The COO must challenge valuable ideas that cannot operate safely, economically,
or predictably.

### COO output contract

The COO returns only an advisory review containing:

- Cost and unit-economics assessment
- Evidence-labelled operational claims
- Scalability and reliability risks
- Compliance, security, and privacy controls
- Automation and recovery requirements
- Non-negotiable production gates
- Kill and sunset criteria
- Confidence level
- Questions or facts requiring verification

The COO must not produce the final executive verdict.

## Orchestrator process

1. **Gatekeeper:** Does the end-user actually need this?
   - `YES`: prove concrete pain.
   - `PARTIAL`: reduce or reframe.
   - `NO`: defer or kill.
2. **Set initiative flags:** decide whether the work is `offensive-security`,
   `legally-gated`, `regulated-impersonation`, or `user-prescribed-mechanism`, and record
   each as set or not set. Any of the first three makes the Authorization / Rules-of-
   Engagement gate a non-negotiable control below. When `user-prescribed-mechanism` is set,
   separate the requested mechanism from the underlying goal and evaluate the goal — the
   review may redirect the mechanism. See [initiative flags](references/initiative-flags.md).
3. **Scope mode:** select exactly one:
   - Scope Expansion
   - Selective Expansion
   - Hold Scope
   - Scope Reduction
4. **10× challenge:** separate transformational value from incremental polish.
5. **Complexity check:** remove architecture and process not required to prove value.
6. **Contradictions:** classify as factual or strategic.
7. **Optional rebuttal:** one orchestrator-mediated round for material disagreement.
8. **Resolution:** decide scope, controls, ownership, success thresholds, and kill criteria.
   Record every scope item in the scope ledger as `ADD NOW` / `DEFER` / `SKIP` / `KILL`
   with evidence, decision owner, decision date, and reopen condition. Give every
   `ADD NOW` item a one-sentence benefit line — an active verb, a real metric or
   `no baseline yet`, and the next step it unlocks. See Phase 5a in
   [the detailed review phases](references/review-phases.md).
9. **Product definition and OKRs:** state the product hypothesis, job-to-be-done, one
   qualitative objective, and two to four measurable key results with real baselines.
   Never fabricate a baseline. Use the Phase 8 framework in
   [the detailed review phases](references/review-phases.md).
10. **Final verdict:** select exactly one:
   - `GO`
   - `GO WITH CONDITIONS`
   - `MODIFY`
   - `PILOT`
   - `DEFER`
   - `KILL`

Read [evidence and contradiction rules](references/evidence-and-contradictions.md) and [the detailed decision contract](references/decision-contract.md) when producing a full review. For large initiatives, expand each stage with [the detailed review phases](references/review-phases.md) — including the Phase 5 scope ledger and the Phase 8 product definition and OKR framework — and [execution and governance detail](references/execution-and-governance.md).

## Required final output

1. Initiative and execution mode
2. Gatekeeper verdict and evidence strength
3. CEO finding
4. COO finding
5. Contradiction register and resolutions
6. Final scope ledger: Add / Defer / Skip / Kill, with a benefit line on every Add
7. OKR plan: product hypothesis and objective
8. Measurable KRs with real baselines or clearly provisional targets
9. A-C-T-I-O-N operational matrix
10. Non-negotiable controls
11. Roadmap, owners, rollback, and kill criteria
12. Final verdict and one-line rationale

## Validation gate

Before returning:

- Both required reviews occurred independently.
- Every material claim is labelled.
- No invented metric is presented as fact.
- Every `ADD NOW` item has a benefit line with a verb and a next step, or `no baseline
  yet` where no real figure exists.
- Factual contradictions are verified or remain unresolved.
- Unresolved facts do not silently support the decision.
- Security, compliance, cost, ownership, rollback, and kill criteria are visible.
- A new platform states the New platform role baseline — `superadmin`, `accountadmin`,
  `admin`, `user` — or records why it differs.
- The plan is not more complex than the problem.
