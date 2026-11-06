# Decision — Project management is routing words, not a new skill

- **Date:** 2026-11-07
- **Decider:** operator (v3x5exia555), by "and also project management" on
  2026-11-06, with the review in `plans/20261106_project-management-skill.md`
- **Decision:** MODIFY the request "add project management". Do not add a bundled
  skill. Route the everyday phrasings to the lenses that already do the job: the
  `manager` role in `eng-level` for our own work (what is done, next, left, blocked),
  and `client-level` answer mode for a status update to a client or stakeholder. Add a
  `Due` line to the plan template so the `manager` role has a date to read.

## Why this record exists

Key result 1 of the product plan: every change that adds or removes a skill carries a
recorded decision. This change was asked for as a skill add and was redirected.

## The evidence

Across about 1,000 prompts in two usage reviews, one prompt asked for a status
sentence to a stakeholder. None asked for sprints, timelines, resourcing, or budget
tracking. The `manager` role already owns breaking work down, ordering it, naming
what blocks what, and refusing to call a plan ready without a pass test. Every role
run already keeps a plan file with status, what happened, and what is still unclear.
Two independent reviews (CEO lens, COO lens) on 2026-11-06 both found that a project
management skill would produce findings, not a verdict nobody may overrule, so it fails
the test for a new actor; it would also claim the same words the `manager` role already
routes on, so the router would flip between them.

## What it deliberately does not do

- No multi-project portfolio view. Reopen if a second prompt asks for status across
  clients.
- No tracking of time, deadlines, or tickets by the skill. It cannot see a clock or a
  ticket tool; every date is given by the operator or read from a plan file.
- No client names in tracked plan files. Real engagement tracking lives outside the
  public repo.
