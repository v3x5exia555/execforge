# Execution and Governance Detail

Use these expansions when the initiative is approved to proceed and the full framework applies.

## A-C-T-I-O-N Operational Matrix

### A — Assess the Problem

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

### C — Cost Optimisation

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

### T — Technical Tactics

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

### I — Incorporate Security, Governance, and Compliance

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

### O — Operational Work Reduction

Define:

- Manual steps removed
- Hours saved
- Handoffs eliminated
- Service-level indicator
- Service-level objective
- Alert threshold
- Dashboard owner
- Escalation path

### N — No Manual Work by Default

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

## Automated runbook

For each critical failure specify detection, automated containment, retry strategy, rollback or isolation, notification condition, evidence captured, escalation condition, and business-continuity fallback.

| Failure | Detection | Automated Action | Retry | Rollback | Escalation | Evidence |
|---|---|---|---|---|---|---|

## Business strength

- **Moat:** proprietary workflow knowledge, unique data, network effects, deep integration, switching cost, regulatory capability, reliability, faster learning loop, trust. Reject artificial moats that are easy to copy.
- **Compliance as an advantage:** faster enterprise approval, audit readiness, lower procurement friction, stronger trust, easier regulatory review, expansion into regulated markets.
- **Adoption engine:** user incentive, friction removed, time-to-first-value, migration, training, communication, champion, feedback mechanism, adoption dashboard, old-process retirement. The new workflow must be easier than the old one, not merely mandatory.
- **Kill switch:** minimum adoption, minimum business impact, maximum operating cost, maximum failure rate, evaluation period, review date, owner, shutdown, rollback, and data-retention processes.

## Architecture review

Describe the full flow: trigger, input validation, authentication and access, core processing, decision or transformation, storage, output delivery, monitoring, failure handling, reconciliation, audit evidence, feedback loop.

Evaluate simplicity, modularity, scalability, security, reliability, observability, testability, portability, cost efficiency, maintainability, and reversibility. Identify systems of record, upstream/downstream systems, vendors, APIs, databases, queues, file transfers, human approvals, and ownership boundaries.

### Data contract

Where data is involved define source, owner, schema, required fields, validation, freshness, quality threshold, versioning, retention, lineage, reconciliation, and failure destination.

### AI controls

Where AI is involved define approved use case, human oversight, confidence threshold, fallback, evaluation dataset, bias and quality testing, explainability, prompt and model versioning, output logging, leakage prevention, and retirement criteria.

## Decision and risk matrices

| Decision | Impact | Velocity Benefit | Complexity | Reversibility | 1-Year Risk | Mitigation | Owner |
|---|---|---|---|---|---|---|---|

Cover build versus buy, scope mode, MVP scope, architecture, data storage, integration, automation, security, vendor dependency, deployment, and support ownership.

| Risk | Probability | Impact | Early Signal | Prevention | Contingency | Owner |
|---|---|---|---|---|---|---|

Cover product, adoption, operations, technical, security, compliance, financial, dependency, delivery, and ownership risks.

## Delivery roadmap

1. **Discovery** — evidence review, user research, baseline, prototype, riskiest assumption, exit criteria.
2. **MVP** — minimum scope, target users, required controls, metrics, release plan, rollback, exit criteria.
3. **Production hardening** — reliability, performance, security, compliance sign-off, monitoring, documentation, support readiness, exit criteria.
4. **Scale** — capacity, wider adoption, cost optimisation, automation, expansion, exit criteria.
5. **Optimise or sunset** — review cadence, cost and adoption review, debt reduction, feature retirement, sunset triggers.

Every stage records deliverables, owner, dependencies, target date, success criteria, and a go / no-go decision.

## Ownership and governance

Assign product, engineering, operations, security, compliance, data, business-sponsor, support, and final-decision owners.

| Workstream | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|

No critical workflow may have unclear ownership.

## One-year obviousness

If a detached engineer inherits this product in 12 months, will the journey, architecture, data flow, decision logic, ownership, controls, and failure recovery be obvious? Evaluate documentation, naming, code structure, diagrams, lineage, business-rule visibility, tests, runbooks, ownership records, decision logs, dependency map, deployment reproducibility, and scope history.

Select: Obvious / Understandable with Guidance / Hidden Operational Debt. For each accepted debt item record the debt, reason accepted, risk, removal date, and owner.
