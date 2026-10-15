# Decision — Add the client-level skill (client engagement lens)

- **Date:** 2026-10-14
- **Decider:** operator (v3x5exia555), by "proceed" on the recommendation in
  `plans/20261014_collect-recent-use-cases.md`
- **Decision:** APPROVE adding a tenth bundled skill, `client-level`, that turns
  technical findings into client-facing material: plain-words answers with scenario
  and risk, deliverable readiness review, and proposals with honest effort.

## Why this record exists

Key result 1 of the product plan: every change that adds or removes a skill carries a
recorded decision. This change adds `skills/client-level/`, registers it in
`scripts/execforge.py` and `.claude-plugin/plugin.json`, and adds router and alias rows
to `skills/c-level/SKILL.md`.

## The evidence

A review of every operator prompt from 2026-07-13 to 2026-10-14 (about 590 prompts on
the operator's machine, logged in `plans/20261014_collect-recent-use-cases.md`) found
the dominant use case is paid client consulting — a Microsoft 365 security assessment
(~420 prompts) and a client back-office bot (~127 prompts). The recurring asks were:
explain this to my client in layman terms, answer with a scenario and a risk, make a
proposal, is this report good enough to present. No bundled skill owned that work; the
same gap was noted in the 2026-07-12 review ("no home for client/pre-sales work") and
deferred. It is now the main workload, so it stops being deferred.

## What it deliberately does not do

- It does not decide what to build — that stays with `execforge`.
- It does not set prices — the operator sets prices; the skill only structures them
  and writes `not measured` where no figure exists.
- It does not soften or replace `sec-level` findings — it translates them for a client
  without changing their severity.
- It does not itself implement the ux-level `spec` mode adopted the same day
  (`plans/20260930_ux-level-spec-review.md`); that mode was then built in the same
  cycle on the operator's later instruction and carries its own decision record
  (`2026-10-14-ux-level-spec-mode.md`).
