# Detailed Review Phases

Use these expansions when running a full review of a large initiative. For small initiatives, the compressed process in `SKILL.md` is sufficient.

## Phase 0 — Initiative context

Summarise:

- Initiative name and problem statement
- Primary and secondary users
- Current workflow
- Proposed change and expected outcome
- Known constraints, deadlines, and dependencies
- Existing systems and regulatory considerations
- Evidence provided

Separate confirmed facts, assumptions, and unknowns. Rate evidence strength as Strong, Moderate, Weak, or Unknown, and explain why.

## Phase 1 — Ultimate gatekeeper

Answer: does the end-user actually need this change? Select exactly one:

### YES — proceed

Prove the need with concrete user pain, affected group, frequency, severity, current workaround and its cost, impact of doing nothing, and evidence that the change beats the current process.

### PARTIALLY — reframe or reduce

Use when the problem is real but the solution is oversized, a process change may suffice, implementation is premature, a prototype should come first, or the proposal solves only a symptom.

### NO — kill or defer

State the unsupported assumption, why the initiative should not proceed, the lower-cost alternative, the cost avoided by stopping, and the evidence required to reconsider.

Gatekeeper output: verdict, confidence, evidence strength, core user pain, cost of doing nothing, cost of building the wrong thing, immediate recommendation. Do not continue into a build plan when the verdict is kill.

## Phase 2 — Scope mode

Select exactly one:

- **Scope Expansion** — the proposal is too narrow and a larger product opportunity may exist.
- **Selective Expansion** — the core is correct; up to five high-leverage additions may materially improve the outcome.
- **Hold Scope** — the current scope is appropriate; adding more would delay value. Focus on clarity, sequencing, simplicity, measurement, and dependency reduction.
- **Scope Reduction** — the proposal contains unnecessary capability, excessive dependency, or an unclear MVP.

Output: selected mode, reason, main scope risk, expected benefit, and what must not happen.

## Phase 3 — 10× challenge

Separate 10% improvements (faster loading, better formatting, more filters, minor shortcuts) from 10× improvements (remove an entire manual workflow, convert days to minutes, prevent failure before it occurs, replace fragmented tools with one trusted journey, enable self-service, produce audit evidence automatically).

For the strongest 10× idea, record user pain solved, value created, effort, risk, and an MVP / Later / Aspirational recommendation. More features is not more value.

## Phase 4 — Platonic Ideal

Ignoring current constraints, describe the ideal end-to-end experience:

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

Then run an ideal-gap analysis: essential now, valuable later, unnecessary, constraints to challenge, non-negotiable constraints. The ideal is a discovery mechanism, not a commitment.

## Phase 6 — Complexity smell test

Challenge whether fewer components, reuse, batch processing, configuration, or an existing service can achieve the outcome. Warning indicators:

- More than roughly eight major file or module changes for a small feature
- More than two new core services or major classes
- Multiple new data stores or more than one new system of record
- Manual reconciliation or duplicate business logic
- Hidden dependencies, irreversible rollout, or support burden greater than user value

These are heuristics. Select: Simple Enough / Acceptable with Controls / Overengineered / Architectural Redesign Required, and state what should be removed.

## Phase 7 — Adversarial review

### CEO challenge

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

### COO pushback

1. What will it cost to build, operate, and support?
2. What breaks at 10× and 100× scale?
3. Where can operational leakage occur?
4. What manual work is created?
5. What compliance, privacy, security, or audit risks exist?
6. What are the single points of failure?
7. Who owns it after launch?
8. How does recovery work?
9. How does the system prove it operated correctly?

### Rebuttal round

Run at most one orchestrator-mediated rebuttal round when material disagreement exists. The CEO responds to cost, operational limits, compliance blockers, and scope-reduction proposals. The COO responds to expansion proposals, speed arguments, MVP shortcuts, and risk acceptance. The orchestrator then states agreements, disagreements, decisions, deferred decisions, non-negotiable controls, and the final scope posture.
