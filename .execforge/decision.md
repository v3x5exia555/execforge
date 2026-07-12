# ExecForge Product Decision — Skill-System Improvements from OrbixShield Retrospective

Run date: 2026-07-08
Execution mode: Single isolated review (small, reversible, evidence-backed change to
governance skill text). CEO and COO lenses applied inline by the orchestrator; no
production architecture, data store, or vendor is introduced. Rollback = `git revert`
of Markdown edits.

## 1. Initiative

Fold the six improvement areas from `skill-usage-feedback.md` into the ExecForge skill
system so the fixes are enforced by default rather than left to operator discipline.

Target user: the operator (and future agents) running ExecForge governance on real
builds — concretely, teams building security/regulated products like the phishing-
awareness platform (OrbixShield) that generated this retrospective.

## 2. Gatekeeper verdict — PARTIAL → reduce scope

Does the end user need all six fixes built? No. Diagnosis of the **current** skill
versions (evidence: direct file reads, 2026-07-08) shows most are already implemented:

| Retro fix | Already in current skills? | Evidence |
|---|---|---|
| 1. Review before building | **YES** | `full-cycle` Stage 1 upstream user gate; strict stage ordering; `eng-level` mandatory upstream stop check |
| 2. State goal, not mechanism | **NO (gap)** | No prescribed-solution guard in `execforge`; "ideal is a discovery mechanism" is close but not a guard against user-prescribed mechanisms |
| 3. Define "done"/acceptance up front | **PARTIAL** | Present in `eng-level` plan review + `q-level`, but not a required *upstream* artifact field |
| 4. Scope + non-goals up front | **YES** | `execforge` MVP/non-goals; `eng-level` upstream translation (in scope/deferred/skipped/non-goals) |
| 5a. Security review on security product | **YES (mechanism exists)** | `sec-level` threat-model + review modes, triggers, S0–S3, verdicts; `full-cycle` rule 6 attaches it |
| 5b. Authorization / legal gate for phishing/pentest | **NO (gap)** | Only data-privacy "consent/purpose limitation" exists; no rules-of-engagement / written-authorization gate anywhere |
| 6a. Use full-cycle to orchestrate | **YES** | `full-cycle` exists and orchestrates the chain |
| 6b. Diagnose before fixing | **YES** | `full-cycle` feedback routing + `eng-level` three-cycle cap before replan |

Building the "YES" rows again would repeat the retrospective's own #1 mistake
(build-then-review). Gatekeeper therefore reduces scope to the genuine deltas.

## 3. CEO finding (product lens)

- Job-to-be-done: the operator wants the governance system to *catch* the failure
  classes the retro hit, without adding ceremony to low-risk work.
- 10× value is concentrated in one place: an **authorization/compliance gate** for
  legally-gated work. On a phishing/offensive-security product, shipping without written
  authorization is a legal/reputational failure a technical appsec review does not catch.
  This is the single highest-leverage addition.
- Secondary, cheap wins: a goal-vs-mechanism guard (prevents the "fix the HTML" class of
  wasted cycles) and making acceptance criteria a required upstream field.
- Non-goal: rebuilding security review, scope/non-goals capture, or orchestration —
  already shipped. Adding them again is negative value (maintenance + false novelty).

## 4. COO finding (operations lens)

- Cost: Markdown-only edits to existing skills; no runtime, no infra, no vendor. Near-zero
  operating cost; maintenance cost is the risk of gate fatigue if over-scoped.
- Compliance/legal: the authorization gate is a genuine control that reduces real legal
  exposure for offensive-security engagements. Worth a hard STOP.
- Reliability risk of over-gating: if the authorization gate fires on all work it becomes
  noise and gets ignored. Must be **conditional** on offensive-security / legally-gated /
  regulated-impersonation scope, mirroring how `sec-level` triggers conditionally.
- Ownership: changes live in `skills/`; versioned; reversible per-file. Kill/sunset: if a
  new gate proves noisy, revert that gate's block without touching the rest.

## 5. Contradiction register

- Apparent contradiction: user said "go thru the improve[ments]" (all six) vs diagnosis
  showing three-plus already exist. Resolution (factual, verified by file reads): honor
  intent (close the gaps the retro cares about) by implementing the genuine deltas and
  explicitly recording the already-satisfied items, rather than rebuilding them. This is
  the retro's own lesson applied to itself.

## 6. Final scope ledger

- **ADD** — Authorization / Rules-of-Engagement gate for offensive-security & legally-gated
  work (written authorization, scope of engagement, consent basis, no unapproved third-
  party impersonation, data-handling & retention for captured credentials). Wire as: a
  conditional trigger + hard STOP in `full-cycle`, a required control in `execforge`, and a
  required field in the `eng-level` upstream stop check. New `sec-level` attention or a
  short shared reference.
- **ADD (light)** — Goal-vs-mechanism guard in `execforge`: capture outcome + constraints;
  when the user prescribed a mechanism, flag it and allow the review to redirect to the
  cause. One rule + one output field.
- **ADD (light)** — Acceptance-criteria-before-build: make "definition of done /
  acceptance test" a required field in the `eng-level` upstream requirements artifact.
- **SKIP (already shipped)** — security review rebuild; scope/non-goals capture;
  full-cycle orchestration; diagnose-before-fix routing. Record as satisfied; reaffirm in
  docs only where a one-line pointer helps.
- **DEFER** — none.
- **KILL** — none.

## 7. Product hypothesis and objective

If ExecForge adds a conditional authorization gate and a goal-vs-mechanism guard, then
governed builds of legally-gated/security products will stop before unauthorized
operation and waste fewer cycles on prescribed-but-wrong mechanisms — without adding
ceremony to ordinary changes.

## 8. Measurable KRs (provisional — no historical baseline instrumented)

- KR1: 100% of initiatives flagged offensive-security/legally-gated reach an explicit
  authorization decision (AUTHORIZED / NOT AUTHORIZED / N-A-justified) before Stage 4.
  Baseline today: 0% (no gate exists).
- KR2: Every `eng-level` upstream-requirements artifact contains a populated acceptance-
  criteria field. Baseline: not required today.
- KR3: Authorization gate fires only on qualifying scope (0 false-positive hard stops on
  non-gated changes in the validation examples). Guards against gate fatigue.

## 9. Non-negotiable controls

- The authorization gate is **conditional** (must not block ordinary non-gated work).
- The gate is a real STOP with a recorded user decision, not a checkbox the agent
  self-answers — consistent with existing "never claim a gate that did not happen."
- No rebuild of already-shipped mechanisms.

## 10. Roadmap / owners / rollback / kill criteria

- Owner: this engagement (skill-system maintainer).
- Sequence: this is a doc/skill change → `eng-level --mode=plan` (Stage 3) will detail the
  exact files/edits; `sec-level` NOT the primary actor here but the change *defines* a
  security/compliance control so a light threat-model note applies.
- Rollback: per-file `git revert`.
- Kill criteria: if the authorization gate generates false hard-stops on ordinary work in
  validation, revert that gate and re-scope to a softer prompt.

## 11. Final verdict

**GO WITH CONDITIONS** — Implement the three genuine deltas (authorization/RoE gate;
goal-vs-mechanism guard; acceptance-criteria-as-required-upstream-field). Do **not**
rebuild already-shipped mechanisms. Condition: the authorization gate must be conditional
on qualifying scope to avoid gate fatigue.
