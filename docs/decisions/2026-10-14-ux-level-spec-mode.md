# Decision — ux-level gains a spec mode, wired into the lifecycle

- **Date:** 2026-10-14
- **Decider:** operator (v3x5exia555), by "proceed" on the adopted proposal
  (`plans/20260930_ux-level-spec-review.md`) and the same-day instruction
  "include ux-level with the lifecycle".
- **Decision:** APPROVE a third `ux-level` mode, `spec`, that reviews a written UI/UX
  specification before anything is built, against seven completeness pillars, ending
  in `SPEC PASS / FIX REQUIRED / REDESIGN`. Wire it into the lifecycle: `full-cycle`
  Stage 2 opens with spec mode when a written spec exists, and `design-html` consumes
  the spec only after it passes.

## Why this record exists

Key result 1 of the product plan: skill changes carry recorded decisions. This change
touches `skills/ux-level/`, `skills/full-cycle/SKILL.md`, and `skills/c-level/SKILL.md`.

## The evidence

The proposal (authored 2026-09-30) showed spec review had no owner: `ux-level` reviews
journeys by design, `design-html` consumes specs without critiquing them, and the
OrbixShield retro recorded the cost — scope, tenancy, and target user inferred rather
than specified, failure paths discovered in production. A mode, not a new skill,
follows the role-architecture principle that produced the eng-level role split. The
2026-10-14 usage review added one condition: the operator's real phrasing ("review
this plan", "review the proposal") must route here, so the c-level alias table carries
those phrasings scoped to UI/UX documents.

## What it deliberately does not do

- It does not review backend or infrastructure specs — `eng-level` does.
- It does not replace the product decision: a `REDESIGN` verdict routes back to
  `execforge` / Stage 0.
- It does not add flags to type; the mode is inferred from phrasing, like the
  existing `product` / `technical` split.
