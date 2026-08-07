# UX Level

`ux-level` reviews a user journey and says where users will get stuck, give up, or lose
their work. It is a review skill, not a design skill: it judges a flow someone else
described, and ends in a verdict.

## When to use it

Use `ux-level` when you have a journey — written as steps — and you want it pulled
apart before anyone builds it, or after a live flow starts losing people.

Do not use it to decide whether the feature should exist; that is
[`execforge`](product-decision.md). Do not use it to build screens; that is
[`design-html`](design-html.md). Do not use it to test whether software works; that is
[`q-level`](q-level.md).

## Two modes

The skill picks a mode from the journey. You do not have to choose.

| Mode | For | What it applies |
|---|---|---|
| `product` | Sign-up, onboarding, checkout, first-run — flows judged on adoption | Friction points, time-to-value, edge cases and dead ends, actionable improvements |
| `technical` | Dashboards, pipelines, compliance and admin tooling, anything with long background jobs | The four pillars below |

The four pillars in `technical` mode:

1. **System visibility and data feedback** — is the user told what is happening while a
   slow job runs?
2. **Error prevention and recovery** — what happens on a rate limit, a timeout, or bad
   input, and does the user lose work?
3. **Flexibility and efficiency** — are there bulk actions, imports, or an API for
   people who do this every day?
4. **Information architecture and cognitive load** — is the screen carrying numbers
   nobody acts on?

## What you must supply

Three things. The review is only as good as these.

1. **Product context** — what the product is and the problem it solves.
2. **Target user** — the actual persona, and what they already know. "A user" is not a
   persona.
3. **The journey** — steps in order, *including what the system does back*.

Be specific. "User creates an account" hides everything. "User enters email, receives a
6-digit code, enters the code, lands on onboarding" can be reviewed. If you list only
what the user does and never what the system does, the skill will stop and ask.

## What you get back

Six sections:

1. Mode and scope
2. Inputs used, including anything that was missing
3. Journey breakdown, step by step, every claim labelled `OBSERVED`, `INFERRED`,
   `ASSUMED`, or `UNKNOWN`
4. Severity matrix ranking each finding `HIGH`, `MEDIUM`, or `LOW`
5. Three to five prioritized recommendations, best first
6. A verdict

## Verdicts

| Verdict | Meaning |
|---|---|
| `UX PASS` | The journey works. What is left is `LOW` and can wait. |
| `FIX REQUIRED` | The shape is right, but named findings must close before release. |
| `REDESIGN` | The flow itself is wrong; fixing it step by step will not work. |

Two `HIGH` findings in one journey means the verdict cannot be `UX PASS`.

## How it fits the other skills

- Findings about auth, permissions, or data exposure are handed to
  [`sec-level`](sec-level.md). `ux-level` notes them and routes them; it does not rule
  on them.
- Screens that need building go to [`design-html`](design-html.md).
- A finding that questions whether the feature should exist goes back to
  [`execforge`](product-decision.md).

`ux-level` is not yet a gate inside [`full-cycle`](full-cycle.md). That was deferred on
purpose until the skill has been used on real journeys.

## Example

See [a worked journey review](examples.md) — `examples/09-ux-journey-review.md` reviews
a first-run compliance dashboard flow end to end.
