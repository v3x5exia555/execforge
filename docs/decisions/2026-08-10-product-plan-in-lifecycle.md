# Decision — Product plan gains four working methods and enters the lifecycle (0.16.0)

- **Date:** 2026-08-10
- **Decider:** operator (v3x5exia555), by direct instruction: "add this into the
  product plan and also include this product plan into the lifecycle"
- **Decision:** APPROVE two changes.
  1. `docs/product-plan.md` gains four sections: how it reads evidence, how work
     gets picked (the ADD NOW / DEFER / SKIP order), a strategic roadmap table
     mapping every `docs/roadmap.md` item to a key result, a beneficiary, and a
     blocker, and a scope-and-dependencies section.
  2. `full-cycle` Stage 0 anchors to the product plan (rule 5a, version 0.9.0):
     every Stage 0 decision names the objective or key result it serves, or
     records `serves none`; a decision that changes the plan updates it in the
     same cycle. The validation gate checks this.

## Why this record exists

Key result 1 of the product plan: every change that adds or removes a skill
carries a recorded decision. At the time of writing, the measured number was
2 recorded decisions in 99 commits — and two skill-touching releases (0.15.0
and the risk framework) had shipped since the plan without one. This change
touches `skills/full-cycle/SKILL.md`, so it records its decision. It is the
first skill change to satisfy KR1 since the key result was written.

## What it deliberately does not do

- It does not answer the open question (who is ExecForge for). The strategic
  roadmap table makes the cost of not answering visible: seven of ten roadmap
  items are blocked on it.
- It does not rewrite `docs/roadmap.md` as benefits. That stays deferred behind
  the open question, per the 2026-08-08 decision.
- It does not force a product plan on repositories that lack one: rule 5a is
  inert when `docs/product-plan.md` does not exist.
