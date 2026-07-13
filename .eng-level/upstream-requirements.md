# Upstream Requirements — ExecForge Skill Improvements

Source: `.execforge/decision.md` (GO WITH CONDITIONS, 2026-07-08)
Status: APPROVED WITH CHANGES (2026-07-08)

## Gate response

User decision: "maybe we can create a flags — will need more scope."
Interpretation (APPROVE WITH CHANGES): build the three deltas, but implement them as an
explicit **Initiative Flags** mechanism — named flags set at the product/upstream stage
that drive the conditional gates downstream — and allow scope to widen to a small shared
flag definition rather than inline one-liners. Direction confirmed at Stage 1; exact
files/edits defined in Stage 3 plan review.

## What / why / for whom

Enforce the OrbixShield retrospective's fixes inside the ExecForge skills so they hold by
default. For the operator and future agents running governed builds of security/regulated
products.

## In scope (the three genuine deltas)

1. **Authorization / Rules-of-Engagement gate** — conditional trigger + hard STOP for
   offensive-security / legally-gated / regulated-impersonation work. Requires: written
   authorization, scope of engagement, consent/legal basis, no unapproved third-party
   impersonation, handling & retention rules for any captured credentials. Wired into
   `full-cycle`, `execforge` (control), and `eng-level` upstream stop check.
2. **Goal-vs-mechanism guard** — `execforge` captures outcome + constraints, flags a
   user-prescribed mechanism, and lets the review redirect to root cause.
3. **Acceptance-criteria-before-build** — required field in the `eng-level` upstream
   requirements artifact.

## Deferred / skipped (already shipped — do NOT rebuild)

- Security review (sec-level exists), scope/non-goals capture, full-cycle orchestration,
  diagnose-before-fix routing, review-before-build gate. Recorded as satisfied.

## Non-goals

- No runtime code, infra, vendor, or data store. Markdown/skill edits only.
- No unconditional gating of ordinary changes.

## Product success metrics

- Authorization decision recorded for 100% of qualifying initiatives before build.
- Acceptance-criteria field populated in every upstream artifact.
- Zero false hard-stops on non-gated work in validation.

## Non-negotiable CEO decisions

- Reduce scope to genuine deltas; do not rebuild shipped mechanisms.

## Non-negotiable COO controls

- Authorization gate is conditional; it is a real recorded STOP, not agent self-answer.

## Assumptions / unknowns

- Assumption: skill text changes propagate to `~/.claude/skills` via the repo's existing
  sync/install path (to confirm in Stage 3).
- Unknown: whether a shared reference file or per-skill inline text is the cleaner wiring
  (Stage 3 plan decision).

## Kill criteria

- Authorization gate produces false hard-stops on ordinary work → revert that gate.

## Acceptance criteria (definition of done for THIS initiative)

- The three deltas are present in the skill files with conditional triggering.
- A dry-run walkthrough shows: (a) a phishing/pentest-style initiative hits the
  authorization STOP; (b) an ordinary refactor does NOT; (c) a prescribed-mechanism
  request surfaces the goal-vs-mechanism flag.
- CHANGELOG/version updated per repo convention.
