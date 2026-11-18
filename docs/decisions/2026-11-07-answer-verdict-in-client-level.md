# Decision — The account manager's call lives in client-level, not in a new skill

- **Date:** 2026-11-07
- **Decider:** operator (v3x5exia555), by "proceed account-manager" on the
  recommendation in `plans/20261106_account-manager-skill.md`
- **Decision:** MODIFY the request "add an account manager skill". Do not add an
  eleventh bundled skill. Add a per-answer verdict `SAY / DON'T SAY / DON'T COMMIT /
  ESCALATE`, a new-promise check, and an ownership and track-record rule to
  `client-level` answer mode, and route `account manager` and its everyday phrasings
  there.

## Why this record exists

Key result 1 of the product plan: every change that adds or removes a skill carries a
recorded decision. This change was asked for as a skill add and was redirected. It
changes `skills/client-level/SKILL.md`, its answer template, the router aliases in
`skills/c-level/SKILL.md`, the shared eval case, docs, and the lock test.

## The evidence

The July 2026 review of 469 prompts (`plans/eng-level-role-architecture.md`, Part 4)
named `account-manager` as the only new actor the evidence supported: about 15 prompts
asking what to tell a client, what to promise, and what to decline, with no home in the
bundle. It proposed exactly this verdict vocabulary, and warned that some of those
prompts drift from positioning into claims about who built or runs a platform that are
not true. Since then `client-level` (0.17.0) took over drafting answers and proposals,
so the gap shrank to one thing: a verdict on a spoken line before it is said. The
answer mode had no verdict; only `deliverable` mode had a promise check.

Two independent reviews (CEO lens, COO lens) on 2026-11-06 both applied the July test
for a new actor — can it say a word nobody else may overrule — and found that
`client-level` already holds that authority on client-facing honesty. A separate skill
would add a name to recall, a ninth touch point, duplicated rules that drift, and an
eval file that pushes an older case out of the five-file CI window.

## What it deliberately does not do

- It does not add a bundled skill. "Account manager" is an alias.
- It does not track accounts, renewals, pipeline, or client health. No evidence, and
  the skill cannot see that data.
- It does not help a line sound smoother. Its main job is `DON'T SAY` and
  `DON'T COMMIT`, with a true line offered instead.
- It does not stop a human. The operator signs and can overrule the verdict.

## Reopen condition

Build a separate `account-manager` skill only if a later usage review shows the answer
verdict being ignored or overruled as a matter of course, which would show the
authority needs its own name.

## Addendum, same day — the sales seat (`pitch` mode)

After the first build the operator clarified the need: when a client reports a blocker
they cannot solve, turn it into an offer of work, with a strategy and the message to
send ("account manager + sales + fishing"). A single isolated review (CEO and COO
lenses) found `proposal` mode too heavy for that moment (it is a six-section document)
and a separate sales skill the wrong shape (two reviews had already rejected a split,
and the honesty rules would drift across two files). Decision: a fourth `client-level`
mode, `pitch`, with five short parts and a two-to-four-sentence message, reusing the
answer verdict. Its rules: urgency needs a labelled recurrence fact; "we can fix it"
needs the operator to confirm both ability and room; the price is always `ESCALATE`;
never manufacture the problem; no pitch on a softened or inflated finding; stay inside
what was promised. Eval case `evaluations/client-level-pitch.eval.md`; the CI eval cap
was raised from five to six files so it runs (`TODOS.md` records the stopgap). Kill the
mode if the operator bypasses it or a sent pitch carries a line the client later
challenges.
