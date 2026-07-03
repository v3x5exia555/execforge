---
name: execforge
description: Use when evaluating whether to build, expand, reduce, pilot, defer, or kill a product, feature, platform, automation, AI capability, data initiative, or costly cross-team change.
license: MIT
compatibility: Supports real subagents when available and isolated simulated review passes otherwise.
metadata:
  author: ExecForge contributors
  version: "0.3.0"
---

# ExecForge Product Decision

## Core principle

Find the smallest evidence-backed scope that creates measurable user value without uncontrolled operational debt.

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

## CEO contract

Return:

- Gatekeeper recommendation
- User pain and job-to-be-done
- Scope mode
- 10× opportunity and Platonic Ideal
- MVP and non-goals
- Adoption and defensibility
- Add / Defer / Skip proposals
- Product risks, evidence labels, confidence, and unknowns

## COO contract

Return:

- Cost and unit economics
- 10× and 100× operating risks
- Reliability and support model
- Security, privacy, compliance, lineage, and audit controls
- Automation and recovery requirements
- Ownership and technical-debt constraints
- Kill/sunset thresholds
- Evidence labels, confidence, and unknowns

## Orchestrator process

1. **Gatekeeper:** Does the end-user actually need this?
   - `YES`: prove concrete pain.
   - `PARTIAL`: reduce or reframe.
   - `NO`: defer or kill.
2. **Scope mode:** select exactly one:
   - Scope Expansion
   - Selective Expansion
   - Hold Scope
   - Scope Reduction
3. **10× challenge:** separate transformational value from incremental polish.
4. **Complexity check:** remove architecture and process not required to prove value.
5. **Contradictions:** classify as factual or strategic.
6. **Optional rebuttal:** one orchestrator-mediated round for material disagreement.
7. **Resolution:** decide scope, controls, ownership, success thresholds, and kill criteria.
8. **Final verdict:** select exactly one:
   - `GO`
   - `GO WITH CONDITIONS`
   - `MODIFY`
   - `PILOT`
   - `DEFER`
   - `KILL`

Read [evidence and contradiction rules](references/evidence-and-contradictions.md) and [the detailed decision contract](references/decision-contract.md) when producing a full review.

## Required final output

1. Initiative and execution mode
2. Gatekeeper verdict and evidence strength
3. CEO finding
4. COO finding
5. Contradiction register and resolutions
6. Final scope ledger: Add / Defer / Skip / Kill
7. Product hypothesis and objective
8. Measurable KRs with real baselines or clearly provisional targets
9. Non-negotiable controls
10. Roadmap, owners, rollback, and kill criteria
11. Final verdict and one-line rationale

## Validation gate

Before returning:

- Both required reviews occurred independently.
- Every material claim is labelled.
- No invented metric is presented as fact.
- Factual contradictions are verified or remain unresolved.
- Unresolved facts do not silently support the decision.
- Security, compliance, cost, ownership, rollback, and kill criteria are visible.
- The plan is not more complex than the problem.
