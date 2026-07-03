---
name: execforge
description: >
  A hybrid CEO/COO product-engineering review skill that pressure-tests whether
  an initiative should exist, selects the right scope posture, evaluates product
  value and operational strength, resolves contradictions, and produces a final
  evidence-based execution decision.
version: 0.2.0
author: ExecForge
tags:
  - product-strategy
  - product-engineering
  - ceo-review
  - coo-review
  - multi-agent
  - scope-control
  - execution-planning
  - compliance
  - operations
---

# ExecForge — Hybrid CEO/COO Product Engineering Skill

## Purpose

Use this skill to evaluate a product, feature, platform, workflow, automation,
data initiative, AI capability, or architecture proposal before committing to
implementation.

The skill combines:

- Founder-mode product and scope pressure-testing
- CEO-level product strategy
- COO-level operational discipline
- Product-engineering execution planning
- Evidence validation
- Hallucination controls
- Contradiction detection
- Explicit Go / Modify / Pilot / Defer / Kill decisions

The goal is not to produce the longest plan. The goal is to produce the
smallest defensible plan that creates measurable user value without creating
uncontrolled operational debt.

---

# Invocation

Use this skill when the user asks to:

- Review a new product or feature
- Pressure-test an initiative
- Create a product-engineering plan
- Evaluate whether something should be built
- Compare product value against operational cost
- Review architecture, scalability, compliance, or support readiness
- Create an MVP, rollout plan, or sunset decision
- Run CEO and COO reviews
- Resolve conflicting product and operational priorities

Example invocation:

```text
/execforge Review this initiative: [initiative description]
```

Optional execution mode:

```text
/execforge --mode=single
/execforge --mode=dual
/execforge --mode=auto
```

Default mode:

```text
--mode=auto
```

---

# Execution Mode Router

Before running the full framework, select the lightest execution mode that is
appropriate for the initiative.

## Single-Agent Mode

Use one agent applying both CEO and COO lenses when the initiative is:

- Small
- Low risk
- Reversible
- Internally contained
- Clearly scoped
- Low cost
- Not compliance-sensitive
- Not expected to create long-term platform dependencies

Typical examples:

- Small workflow improvement
- Minor internal feature
- SQL or data validation enhancement
- Configuration change
- Low-risk automation
- Small UI improvement

## Dual-Agent Mode

Use two specialist subagents plus one main orchestrator when the initiative is:

- Expensive
- Cross-functional
- Customer-facing
- Compliance-sensitive
- Security-sensitive
- Difficult to reverse
- Architecturally significant
- Likely to affect many users or teams
- Expected to run at large scale
- Based on uncertain assumptions
- Likely to generate strategic disagreement

## Auto Mode Decision

Use dual-agent mode if any two of the following are true:

- More than one business unit is affected
- Production architecture changes are required
- Sensitive or regulated data is involved
- The decision is hard to reverse
- The initiative requires more than one quarter of delivery effort
- A new service, system of record, vendor, or database is introduced
- Failure may cause financial, legal, reputational, or customer impact
- The evidence supporting the initiative is weak or disputed

Otherwise, use single-agent mode.

State the selected mode and the reason.

---

# Required Multi-Agent Topology

When the runtime supports subagents, use exactly this topology:

```text
CEO Subagent
    \
     Main Orchestrator → Final Decision
    /
COO Subagent
```

The CEO and COO are specialist advisory agents. Both report only to the Main
Orchestrator. The Main Orchestrator is the only agent authorised to produce the
final user-visible decision.

## Topology Rules

1. The CEO and COO receive the same shared context package.
2. They analyse the initiative independently and may run in parallel.
3. They must not directly merge their answers.
4. They must not negotiate privately or overwrite each other's findings.
5. Neither subagent may issue the final Go / Modify / Pilot / Defer / Kill verdict.
6. Both subagents return structured findings, evidence labels, assumptions,
   confidence, risks, and recommendations to the Main Orchestrator.
7. All rebuttals are mediated by the Main Orchestrator.
8. The Main Orchestrator validates evidence before accepting any recommendation.
9. The Main Orchestrator owns the contradiction register, scope ledger, risk
   register, and final decision record.
10. Only the Main Orchestrator communicates the final unified answer to the user.

## Execution Sequence

```text
1. User Request
       ↓
2. Main Orchestrator creates Shared Context Package
       ├──→ CEO Subagent Review
       └──→ COO Subagent Review
                    ↓
3. Main Orchestrator validates both outputs
       ↓
4. Main Orchestrator detects evidence gaps and contradictions
       ↓
5. Optional orchestrator-mediated rebuttal round
       ↓
6. Main Orchestrator resolves scope, risk, cost, and control decisions
       ↓
7. Main Orchestrator issues Final Decision
```

## 1. CEO Subagent

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

### CEO Output Contract

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

## 2. COO Subagent

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

### COO Output Contract

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

## 3. Main Orchestrator

The Main Orchestrator:

- Owns the original user request
- Creates one neutral shared context package
- Sends the same factual context to both subagents
- Prevents one subagent's conclusions from biasing the other's first review
- Checks whether both subagents completed their required output contracts
- Checks evidence quality and unsupported assumptions
- Detects factual and strategic contradictions
- Requests a single rebuttal round when a material disagreement exists
- Maintains the authoritative contradiction register
- Maintains the authoritative scope ledger
- Maintains the authoritative risk and decision registers
- Resolves disagreements using evidence, user value, cost, risk, and reversibility
- Rejects invented metrics and unsupported certainty
- Produces the final unified decision
- Explains which recommendations were accepted, rejected, or deferred and why

The Main Orchestrator is the final judge, not a simple response merger.

### Main Orchestrator Final-Decision Authority

Only the Main Orchestrator may:

- Approve or reject the Gatekeeper result
- Select the final scope mode
- Accept, defer, skip, or kill scope items
- Decide whether unresolved facts block execution
- Set non-negotiable controls
- Select GO / GO WITH CONDITIONS / MODIFY / PILOT / DEFER / KILL
- Produce the final user-visible response

## Fallback Behaviour

If the runtime does not support true subagents:

- Simulate the CEO and COO as two isolated review passes
- Use the same shared context for both passes
- Complete the CEO review before exposing it to the simulated COO review, or
  otherwise preserve independent reasoning
- Do not blend their findings until the Main Orchestrator phase
- Apply the same evidence, contradiction, and reconciliation rules
- State that the execution used simulated role separation
- Preserve the same topology conceptually:

```text
Simulated CEO Review
          \
           Main Orchestrator → Final Decision
          /
Simulated COO Review
```

---

# Evidence and Truthfulness Protocol

Every material claim must be labelled as one of:

- **FACT** — directly supported by provided evidence or verified sources
- **ASSUMPTION** — plausible but not confirmed
- **INFERENCE** — reasoned conclusion derived from available facts
- **UNKNOWN** — information required but not available

Rules:

1. Never present an assumption as a fact.
2. Never invent baselines, percentages, costs, dates, regulations, or user demand.
3. If a target must be proposed without a baseline, label it as a provisional target.
4. If external verification is available and material, verify the claim.
5. If verification is unavailable, preserve the uncertainty.
6. Confidence must be stated as High, Medium, or Low.
7. A confident tone is not evidence.
8. Agreement between agents is not proof.
9. Repeated claims from the same source remain one source of evidence.
10. Unknowns that materially affect the decision must appear in the final risk section.

---

# Contradiction Protocol

The Main Orchestrator must create a contradiction register whenever the CEO and
COO disagree.

Classify each disagreement as:

## Strategic Disagreement

Example:

- CEO recommends real-time processing for user experience.
- COO recommends batch processing for cost control.

Resolve using:

1. User impact
2. Evidence strength
3. Reversibility
4. Cost
5. Risk
6. Time-to-value
7. Ability to test with a smaller experiment

## Factual Contradiction

Example:

- One agent claims the current platform supports an API.
- Another agent claims only file-based integration is available.

Do not average, merge, or guess.

The Main Orchestrator must:

1. Identify the exact conflicting claims
2. Identify the evidence behind each claim
3. Verify the fact where possible
4. Mark the issue unresolved if it cannot be verified
5. Prevent the final plan from depending on the unresolved fact
6. Add a validation action and owner

## Contradiction Register Format

| ID | Topic | CEO Claim | COO Claim | Type | Evidence | Resolution | Owner |
|---|---|---|---|---|---|---|---|

---

# Phase 0 — Initiative Context

Summarise:

- Initiative name
- Problem statement
- Primary user
- Secondary users
- Current workflow
- Proposed change
- Expected outcome
- Known constraints
- Known deadlines
- Existing systems
- Dependencies
- Regulatory considerations
- Evidence provided

Separate:

- Confirmed facts
- Assumptions
- Unknowns

## Evidence Strength

Select one:

- Strong
- Moderate
- Weak
- Unknown

Explain why.

---

# Phase 1 — Ultimate Gatekeeper

Answer:

> Does the end-user actually need this product, feature, or change?

Select exactly one:

## YES — Proceed

Prove the need using:

- Concrete user pain
- Affected user group
- Frequency
- Severity
- Current workaround
- Cost of the workaround
- Impact of doing nothing
- Evidence that the proposed change is better than the current process

## PARTIALLY — Reframe or Reduce

Use when:

- The problem is real but the solution is oversized
- A process change may be enough
- The implementation is premature
- A prototype should be used first
- The proposal solves only a symptom

## NO — Kill or Defer

Explain:

- Which assumption is unsupported
- Why the initiative should not proceed
- The lower-cost alternative
- The cost avoided by stopping
- The evidence required to reconsider it later

## Gatekeeper Output

Provide:

- Verdict
- Confidence
- Evidence strength
- Core user pain
- Cost of doing nothing
- Cost of building the wrong thing
- Immediate recommendation

Do not continue into a full build plan if the verdict is Kill.

---

# Phase 2 — Founder-Mode Scope Review

Select exactly one scope mode.

## Scope Expansion

Use when the proposal is too narrow and a larger product opportunity may exist.

## Selective Expansion

Use when the core is correct but up to five high-leverage additions may
materially improve the outcome.

## Hold Scope

Use when the current scope is appropriate and adding more would delay value.

Focus on:

- Clarity
- Sequencing
- Simplicity
- Measurement
- Dependency reduction

## Scope Reduction

Use when the proposal contains unnecessary capability, excessive dependency,
or an unclear MVP.

## Scope Mode Output

Provide:

- Selected mode
- Reason
- Main scope risk
- Expected benefit
- What must not happen

---

# Phase 3 — 10× Product Challenge

Answer:

> What would make this product ten times more valuable instead of only ten
> percent better?

Separate:

## 10% Improvements

Examples:

- Faster loading
- Better formatting
- More filters
- Minor workflow shortcuts
- Small interface enhancements

## 10× Improvements

Examples:

- Remove an entire manual workflow
- Convert a multi-day process into minutes
- Prevent failure before it occurs
- Replace fragmented tools with one trusted journey
- Make self-service possible
- Produce audit evidence automatically
- Turn reactive work into proactive automation

For the strongest 10× idea, provide:

- User pain solved
- Value created
- Effort
- Risk
- MVP / Later / Aspirational recommendation

Do not confuse more features with more value.

---

# Phase 4 — Platonic Ideal

Ignoring current organisational, technical, and resource constraints, describe
the ideal end-to-end user experience.

Cover:

1. Entry point
2. Information required from the user
3. Information already known by the system
4. Automated work
5. Decision or output
6. Completion time
7. Exception handling
8. Trust and explainability
9. Evidence or confirmation
10. Post-completion follow-up

Then perform an Ideal-Gap Analysis:

- Essential now
- Valuable later
- Unnecessary
- Constraints to challenge
- Non-negotiable constraints

The Platonic Ideal is a discovery mechanism, not an automatic commitment.

---

# Phase 5 — Scope Ledger

Evaluate each proposed capability independently.

| Scope Item | User Pain | User Value | Business Value | Effort | Risk | Decision | Reason |
|---|---|---:|---:|---:|---:|---|---|

Allowed decisions:

- **ADD NOW**
- **DEFER**
- **SKIP**
- **KILL**

For each item, record:

- Evidence
- Decision owner
- Decision date
- Reopen condition

Previously settled decisions must not be reopened without new evidence.

---

# Phase 6 — Complexity Smell Test

Challenge:

- Can fewer components achieve the same outcome?
- Can an existing service be reused?
- Can a new API be avoided?
- Can a new database be avoided?
- Can real-time processing be replaced with batch?
- Can configuration replace custom code?
- Can a new approval step be avoided?
- Is the design solving unproven future scale?
- Is ownership clear?
- Is rollback possible?

Warning indicators:

- More than approximately eight major file or module changes for a small feature
- More than two new core services or major classes
- Multiple new data stores
- More than one new system of record
- Manual reconciliation
- Duplicate business logic
- Hidden dependencies
- Irreversible rollout
- Support burden greater than user value

These are heuristics, not absolute rules.

Select:

- Simple Enough
- Acceptable with Controls
- Overengineered
- Architectural Redesign Required

State what should be removed.

---

# Phase 7 — Adversarial Review

## CEO Challenge

The CEO answers:

1. What is the actual product?
2. Who is the primary user?
3. What painful job are they trying to complete?
4. Why is the current solution inadequate?
5. What creates a 10-star experience?
6. What creates a 10× improvement?
7. What drives adoption or business impact?
8. What creates defensibility?
9. What is the smallest useful version?
10. What should be excluded?

## COO Pushback

The COO answers:

1. What will it cost to build?
2. What will it cost to operate?
3. What will it cost to support?
4. What breaks at 10× scale?
5. What breaks at 100× scale?
6. Where can operational leakage occur?
7. What manual work is created?
8. What compliance, privacy, security, or audit risks exist?
9. What are the single points of failure?
10. Who owns it after launch?
11. How does recovery work?
12. How does the system prove it operated correctly?

## Rebuttal Round

Run one rebuttal round when material disagreement exists.

The CEO responds to:

- Cost concerns
- Operational limits
- Compliance blockers
- Scope reduction proposals

The COO responds to:

- Expansion proposals
- Speed arguments
- MVP shortcuts
- Risk acceptance

## Executive Resolution

The Main Orchestrator states:

- Agreements
- Disagreements
- Decisions
- Deferred decisions
- Non-negotiable controls
- Final scope posture

---

# Phase 8 — Product Definition and OKRs

## Product Hypothesis

Use:

> We believe that **[target user]** experiences **[specific problem]**.
> By providing **[capability]**, we expect **[measurable outcome]**.

## Job-to-Be-Done

Define:

- Primary user
- Secondary user
- User job
- Current workaround
- Moment of greatest friction
- Desired outcome
- Frequency
- Evidence

## Scope

### Must Have

Required to prove the hypothesis.

### Should Have

Materially improves usability, adoption, reliability, or compliance.

### Could Have

Useful but must not delay the MVP.

### Non-Goals

Explicitly excluded.

### Deferred

Valuable later.

### Skipped

Rejected and recorded.

## Objective

One qualitative objective.

## Key Results

Provide two to four measurable results.

Each result must include:

- Baseline
- Target
- Measurement method
- Measurement period
- Owner

Never fabricate a baseline.

---

# Phase 9 — A-C-T-I-O-N Operational Matrix

## A — Assess the Problem

Identify:

- User problem
- Business problem
- Root cause
- System bottleneck
- Process failure
- Data failure
- Latency problem
- Reliability issue
- Cost of the current state

Use:

> The problem occurs because **[root cause]**, causing **[measurable impact]**
> for **[user or business area]**.

## C — Cost Optimisation

Evaluate:

- Development cost
- Infrastructure cost
- Licensing
- Support
- Maintenance
- Cost per user
- Cost per transaction
- Current-scale cost
- 10×-scale cost
- 100×-scale cost
- Build versus buy
- Payback period
- Opportunity cost

Identify the cost driver most likely to become uncontrolled.

## T — Technical Tactics

For every tactic, state:

- Benefit
- Effort
- Risk
- Owner
- Success metric

Consider:

- Reuse
- Simplification
- Batch versus real time
- Event-driven processing
- Caching
- Serverless versus provisioned compute
- Partitioning
- Idempotency
- Schema validation
- API standards
- Automated testing
- Infrastructure as code
- Feature flags
- Progressive rollout
- Archival
- Removal of duplicate systems

## I — Incorporate Security, Governance, and Compliance

Evaluate:

- Authentication
- Authorisation
- Least privilege
- Sensitive-data handling
- Encryption
- Masking
- Consent
- Purpose limitation
- Retention
- Deletion
- Regulatory requirements
- Audit trails
- Data lineage
- Change history
- Segregation of duties
- Approval
- Evidence retention
- AI governance, where applicable

Classify every control:

- Before Prototype
- Before MVP
- Before Production
- Before Scale
- Not Applicable

## O — Operational Work Reduction

Define:

- Manual steps removed
- Hours saved
- Handoffs eliminated
- Service-level indicator
- Service-level objective
- Alert threshold
- Dashboard owner
- Escalation path

## N — No Manual Work by Default

Include:

- Idempotency
- Retry with exponential backoff
- Dead-letter queue or quarantine
- Duplicate prevention
- Checkpointing
- Automatic reconciliation
- Automatic rollback
- Self-healing
- Reprocessing
- Poison-message handling
- Data-correction strategy
- Maximum retry threshold
- Human approval conditions

Human intervention is reserved for:

- Policy decisions
- Security incidents
- Irrecoverable corruption
- Repeated systemic failure
- Material financial exceptions
- Regulatory-impact exceptions

---

# Phase 10 — Automated Runbook

For each critical failure, specify:

1. Detection condition
2. Automated containment
3. Retry strategy
4. Rollback or isolation action
5. Notification condition
6. Evidence captured
7. Escalation condition
8. Business-continuity fallback

Use this table:

| Failure | Detection | Automated Action | Retry | Rollback | Escalation | Evidence |
|---|---|---|---|---|---|---|

---

# Phase 11 — Business Strength

## Moat

Evaluate:

- Proprietary workflow knowledge
- Unique data
- Historical decision data
- Network effects
- Deep integration
- Switching cost
- Regulatory capability
- Reliability
- Faster learning loop
- Trust

Reject artificial moats that are easy to copy.

## Compliance as a Weapon

Explain whether compliance can create:

- Faster enterprise approval
- Better audit readiness
- Lower procurement friction
- Stronger trust
- Easier regulatory review
- Lower legal risk
- Expansion into regulated markets

## Adoption Engine

Define:

- User incentive
- Friction removed
- Time-to-first-value
- Migration strategy
- Training
- Communication
- Champion
- Feedback mechanism
- Adoption dashboard
- Old-process retirement

The new workflow must be easier than the old one, not merely mandatory.

## Kill Switch

Define:

- Minimum adoption
- Minimum business impact
- Maximum operating cost
- Maximum failure rate
- Evaluation period
- Review date
- Owner
- Shutdown process
- Rollback process
- Data-retention process

---

# Phase 12 — Product and Technical Architecture

Describe the full flow:

1. Trigger
2. Input validation
3. Authentication and access
4. Core processing
5. Decision or transformation
6. Storage
7. Output delivery
8. Monitoring
9. Failure handling
10. Reconciliation
11. Audit evidence
12. Feedback loop

Evaluate:

- Simplicity
- Modularity
- Scalability
- Security
- Reliability
- Observability
- Testability
- Portability
- Cost efficiency
- Maintainability
- Reversibility

Identify:

- Systems of record
- Upstream systems
- Downstream systems
- Vendors
- APIs
- Databases
- Queues
- File transfers
- Human approvals
- Ownership boundaries

## Data Contract

Where data is involved, define:

- Source
- Owner
- Schema
- Required fields
- Validation
- Freshness
- Quality threshold
- Versioning
- Retention
- Lineage
- Reconciliation
- Failure destination

## AI Controls

Where AI is involved, define:

- Approved use case
- Human oversight
- Confidence threshold
- Fallback
- Evaluation dataset
- Bias testing
- Quality testing
- Explainability
- Prompt versioning
- Model versioning
- Output logging
- Leakage prevention
- Retirement criteria

---

# Phase 13 — Decision and Risk Matrix

## Decision Matrix

| Decision | Impact | Velocity Benefit | Complexity | Reversibility | 1-Year Risk | Mitigation | Owner |
|---|---|---|---|---|---|---|---|

Cover:

- Build versus buy
- Scope mode
- MVP scope
- Architecture
- Data storage
- Integration
- Automation
- Security
- Vendor dependency
- Deployment
- Support ownership

## Risk Register

| Risk | Probability | Impact | Early Signal | Prevention | Contingency | Owner |
|---|---|---|---|---|---|---|

Cover:

- Product
- Adoption
- Operations
- Technical
- Security
- Compliance
- Financial
- Dependency
- Delivery
- Ownership

---

# Phase 14 — Delivery Roadmap

## Stage 1 — Discovery

Include:

- Evidence review
- User research
- Baseline
- Prototype
- Riskiest assumption
- Exit criteria

## Stage 2 — MVP

Include:

- Minimum scope
- Target users
- Required controls
- Metrics
- Release plan
- Rollback
- Exit criteria

## Stage 3 — Production Hardening

Include:

- Reliability
- Performance
- Security
- Compliance sign-off
- Monitoring
- Documentation
- Support readiness
- Exit criteria

## Stage 4 — Scale

Include:

- Capacity
- Wider adoption
- Cost optimisation
- Automation
- Expansion
- Exit criteria

## Stage 5 — Optimise or Sunset

Include:

- Review cadence
- Cost review
- Adoption review
- Debt reduction
- Feature retirement
- Sunset triggers

For every stage, include:

- Deliverables
- Owner
- Dependencies
- Target date
- Success criteria
- Go / No-Go decision

---

# Phase 15 — Ownership and Governance

Define:

- Product owner
- Engineering owner
- Operations owner
- Security owner
- Compliance owner
- Data owner
- Business sponsor
- Support owner
- Final decision maker

Use:

| Workstream | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|

No critical workflow may have unclear ownership.

---

# Phase 16 — One-Year Obviousness

Answer:

> If a completely detached engineer inherits this product in 12 months, will
> the user journey, architecture, data flow, decision logic, ownership,
> controls, and failure recovery be obvious?

Evaluate:

- Documentation
- Naming
- Code structure
- Architecture diagrams
- Data lineage
- Business-rule visibility
- Tests
- Runbooks
- Ownership records
- Decision logs
- Dependency map
- Deployment reproducibility
- Scope history

Select:

- Obvious
- Understandable with Guidance
- Hidden Operational Debt

For each debt item, include:

- Debt
- Reason accepted
- Risk
- Removal date
- Owner

---

# Phase 17 — Final Executive Decision

Select exactly one:

- GO
- GO WITH CONDITIONS
- MODIFY
- PILOT
- DEFER
- KILL

Provide:

- Execution mode
- Gatekeeper result
- Evidence strength
- Scope mode
- Core user pain
- Product hypothesis
- 10× opportunity
- Platonic Ideal gap
- Accepted scope
- Deferred scope
- Skipped scope
- Primary value
- Largest risk
- Non-negotiable control
- MVP success threshold
- Kill threshold
- Immediate next action
- Accountable owner
- Confidence

## Final Scope Ledger

| Item | Status | Reason | Owner | Reopen Condition |
|---|---|---|---|---|

## Executive One-Liner

Use:

> We should **[decision]** using a **[scope mode]** approach because
> **[primary evidence]**, provided that **[critical condition]** is satisfied.

---

# Main Orchestrator Validation Gate

Before returning the final answer, confirm:

- The required CEO → Main Orchestrator ← COO topology was followed
- Both CEO and COO received the same shared factual context
- Both CEO and COO reviews were completed independently
- Neither subagent issued the final executive verdict
- Claims are labelled Fact / Assumption / Inference / Unknown
- No unsupported metric is presented as fact
- Factual contradictions are verified or marked unresolved
- Strategic disagreements are explicitly resolved
- Scope additions were evaluated individually
- Add / Defer / Skip decisions are recorded
- Security and compliance blockers are visible
- Cost at scale was considered
- Ownership is assigned
- Rollback exists
- Kill criteria exist
- The final verdict is traceable to evidence
- The plan is not more complex than the problem requires

If any item fails, revise the output before returning it.

---

# Output Style

The output must be:

- Direct
- Evidence-based
- Explicit about uncertainty
- Structured
- Measurable
- Actionable
- Free from invented facts
- Clear about what should not be built

Avoid:

- Generic advice
- Repetition
- Unnecessary jargon
- Fake precision
- Unsupported confidence
- Automatically approving the initiative
- Adding complexity to appear sophisticated

For small initiatives, compress the output into:

1. Gatekeeper
2. Scope mode
3. Product hypothesis
4. Main risk
5. Minimum execution plan
6. Final verdict

For large initiatives, use the complete framework.

---

# Final Principle

Two agents do not guarantee truth.

The value of ExecForge comes from:

- Independent analysis
- Evidence discipline
- Explicit contradictions
- Strong orchestration
- Scope control
- Reversible decisions
- Clear ownership
- Measurable outcomes

Always prefer a smaller validated solution over a larger impressive-looking plan.
