# Skill Usage Feedback — OrbixShield Build

## Context
Reflection on how the governance/lifecycle skills (execforge, eng-level, q-level,
sec-level, full-cycle) were used while building a commercial phishing-awareness
platform, with concrete improvement areas.

## What's working well
- **The governance skills are actually being triggered** — most teams skip this entirely.
- **Review findings are accepted, not overridden** — hard calls (deprecating a
  redundant feature, acting on an opsec flag) were respected. That's the whole point
  of a gate.
- **Real-world constraints are surfaced** when they matter (deployment target,
  tooling availability).

## Improvement areas

### 1. Trigger reviews *before* building, not after
The recurring pattern was *"do X, and trigger eng-level for it"* — the review wrapped
a decision already made. Real cost: a full feature (DB-backed sender-domain registry —
schema, API, integration, UI, tests) was built over many iterations, then a product
review concluded it shouldn't exist. Running the product/eng review **first** would
have avoided the entire build.
> **Fix:** for anything net-new, make the product/eng review step 1, and treat the
> "STOP for approval" as a real fork — not a formality.

### 2. State the *goal*, not the *mechanism*
Prescribing the solution led to wasted cycles: *"improve the email HTML to avoid spam"*
— but HTML was never the cause (sender reputation was), and one HTML "improvement" made
the spam score worse. By contrast, *"make it so new recipients don't get spam"* (a goal)
let the review redirect to the correct solution (recipient-side allowlisting).
> **Fix:** lead with the outcome + constraints; let the review choose the mechanism.

### 3. Define "done" before saying "test until fix"
"QA it, test until fix" was used without a pass criterion. For an ambiguous problem,
"fixed" could mean several different things (accepted by the mail server? delivered to
inbox? which inbox?).
> **Fix:** state the acceptance test up front (e.g., "pass = lands in inbox for an
> allowlisted seed mailbox").

### 4. Provide scope and non-goals upfront
Scope, tenancy, and target-user often had to be inferred. One line each of
*in-scope / non-goals / success metric* dramatically sharpens the output.

## Gaps for this use case (a phishing platform)

### 1. No security review — on a security product
Deploying phishing infrastructure, handling credentials, exposing an admin console,
and hitting real opsec issues (admin URL placed on a sending domain; brand-impersonation
content; API keys spread across servers) — yet a dedicated security review (**sec-level**)
was never triggered. For this domain that's the largest gap: a threat model + authz/
secrets review should gate go-live.

### 2. Thin authorization/compliance rigor
Phishing simulations are legally gated (written authorization, consent, no unapproved
third-party impersonation). This should be an explicit hard checklist item per
engagement, not an afterthought.

### 3. Lifecycle stages were hand-chained
Stages were run manually across many turns. A single orchestrated run (**full-cycle**:
product decision -> approval -> plan -> build -> staff review -> QA -> ship) would be
smoother and less error-prone.

### 4. Fixes were prescribed before diagnosis
A deliverability problem ran many iterations of symptom-fixing (template tweaks) before
the root cause (IP/DNS reputation) was diagnosed.
> **Fix:** when something breaks, request a **diagnosis first**, approve the fix second.

## Summary
The skills are being used as a **wrapper around decisions already made**. Their real
value is as a **gate before the decision**:
1. Trigger reviews **earlier** (before building).
2. State **goals, not mechanisms**.
3. Define **"done"** / acceptance criteria.
4. Provide **scope + non-goals** upfront.
5. For a security product: **add a security review + an authorization gate** to the
   default flow.
6. Use **full-cycle** to orchestrate, and **diagnose before fixing**.
