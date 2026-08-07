# Add a user-journey review skill to ExecForge

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-08-07
- **Last updated:** 2026-08-07
- **Role(s):** c-level (router) → execforge (product decision)
- **Branch:** lz-ux-level, cut fresh from `main`
- **Status:** IN PROGRESS

## What was asked

The operator pasted two prompt templates and said: "could you put this for product framework skill".

Template one: a Senior Product Manager and Lead UX Researcher who reviews a user journey for friction points, time-to-value, edge cases and dead ends, then gives 3–5 improvements.

Template two: the same role, but with four heuristic pillars for data-heavy and compliance products — system visibility and data feedback, error prevention and recovery, flexibility and efficiency, information architecture and cognitive load — plus a severity matrix.

Three questions were asked before building. The answers:

- Ship it inside ExecForge, not as a personal skill.
- Give it its own skill, do not fold it into `design-html`.
- Carry both templates, as two modes of one skill.

## The product decision (execforge)

**Mode used:** single isolated review. The change is documentation only, touches no
auth, secrets, schema or data, adds no dependency, and one revert undoes it. That fails
the bar for two independent reviewers.

**Gatekeeper — does the user actually need this? YES.**
Evidence, labelled honestly:

- FACT: the operator wrote the framework themselves and asked for it to be packaged.
- FACT: ExecForge has no skill that judges an existing flow. `design-html` builds
  screens from approved scope. `q-level` tests whether software works, not whether the
  journey makes sense.
- ASSUMPTION: it will be reused across the operator's compliance and scraping projects.
  Not yet proven by usage.

**Scope mode:** Selective Expansion. One new skill, no change to how any existing skill
decides anything.

**CEO view (advisory):** the real gap is judging a flow *before* it is built, which
today happens in nobody's lane. The 10× move is making the review a gate that
`full-cycle` can call, not a one-off prompt. Risk: a ninth skill nobody triggers.

**COO view (advisory):** cost is low and ongoing upkeep is small — it is prose, with no
runtime and no data. The real cost is the bundle contract: nine files must agree or
`validate` and `release-check` fail. Main risk is routing. `c-level` already sends
"UX review" to `design-html`, so without a routing change the new skill is unreachable.

**Contradictions:** none between the two views.

**Scope ledger:**

| Item | Call | Why |
| --- | --- | --- |
| `ux-level` skill with two modes | ADD NOW | The operator's direct ask. |
| Routing row and trigger words in `c-level` | ADD NOW | Without it the skill can never be reached. |
| Docs, example, README row, CHANGELOG, version bump | ADD NOW | The bundle contract fails without them. |
| Wiring it into `full-cycle` as a gate | DEFER | Changes the lifecycle for every user. Revisit once the skill has been used on real journeys. |
| Any runtime, scoring engine, or stored artifact | SKIP | The problem is judgement, not software. |

**Verdict: GO WITH CONDITIONS.** Ship the skill and its routing. Do not touch the
lifecycle yet.

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-07 | Name it `ux-level` | The bundle already uses `eng-level`, `q-level`, `sec-level` for review skills that end in a verdict. `ux-level` slots in and is easy to guess. |
| 2026-08-07 | Give it a verdict: UX PASS / FIX REQUIRED / REDESIGN | Every other `-level` skill ends in a decision. A review with no verdict cannot be used as a gate later. |
| 2026-08-07 | Two modes, not two skills | The pasted templates share a role and an output shape. Splitting them would make the user choose before they know which fits. |
| 2026-08-07 | Branch off `main`, not the current branch | The current branch carries unrelated platform-role work. |
| 2026-08-07 | Version 0.13.0, not 0.12.3 | A new skill is a new feature, not a fix. |

## What happened

- 2026-08-07 — Ran `c-level`; it routed to `execforge`. Ran the product review above.
- 2026-08-07 — Asked three questions, got the answers recorded above.
- 2026-08-07 — Wrote this plan.
- 2026-08-07 — Built `skills/ux-level/` (SKILL.md, `references/pillars.md`,
  `assets/journey-review.template.md`).
- 2026-08-07 — Wired it into the bundle: `BUNDLED_SKILLS`, both plugin manifests,
  README table, `docs/ux-level.md`, mkdocs nav, `examples/09-ux-journey-review.md`,
  CHANGELOG, version 0.13.0, and the `c-level` router.
- 2026-08-07 — First test run failed: `evaluations/ux-level.eval.md` was missing. The
  repo requires an evaluation case for every bundled skill. Wrote it, reran, green.

## Still unclear

- Should `full-cycle` call this skill as a real gate? Deferred on purpose. The operator
  decides once the skill has been used a few times.

## Result

Shipped as PR #15 on branch `lz-ux-level`, cut from `main`.

Checked and passing:

- `pytest tests/` — 97 passed, 213 subtests.
- `scripts/execforge.py validate` — passed.
- `scripts/execforge.py release-check` — consistent.
- `scripts/execforge.py install` into a temp folder — verified 9 skills, `ux-level`
  among them, with its `references/` and `assets/` intact.

One behaviour change to watch: the words "UX review" used to reach `design-html` and
now reach `ux-level`. `designer`, `design plan`, and `UI review` are unchanged.

Known conflict ahead: this branch edits `scripts/execforge.py`, and so does the
uncommitted platform-role work on `lz-platform-role-baseline`. Both also add a
CHANGELOG entry at the top and set a version. Whichever lands second needs a merge fix.
Landing the platform-role work first would make this the smaller of the two fixes.
