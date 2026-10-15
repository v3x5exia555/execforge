# Build the client-level skill

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.

- **Started:** 2026-10-14
- **Last updated:** 2026-10-14
- **Role(s):** execforge (decision to add a skill), eng-level (build)
- **Branch:** main (working tree only; commit waits for the operator)
- **Status:** DONE (uncommitted — waiting for the operator's ship step)

## What was asked

The operator reviewed three months of their own usage (see
`plans/20261014_collect-recent-use-cases.md`). The review recommended a new skill for
client consulting work as the top improvement, and the operator said "proceed".

## Why this skill

The usage data shows the operator's main work is now consulting for paying clients:
answering client questions in plain words, writing proposals with scenario and risk,
checking if a report is good enough to present, and preparing for client calls. About
420 of ~590 recent prompts were this kind of work, and no skill owns it today.

## The plan

1. Record the decision in `docs/decisions/2026-10-14-client-level-skill.md` (the
   product plan's key result 1: every skill add carries a recorded decision).
2. Write `skills/client-level/SKILL.md` in the house style, with three modes:
   - `answer` — turn a client question into a plain-words answer with scenario and risk.
   - `deliverable` — review or shape a client-facing document (report, slides,
     step guide) and say if it is ready to present.
   - `proposal` — turn findings into a proposal: what we offer, what it fixes, the
     risk of not doing it, and honest effort (no invented numbers).
3. Add two small templates under `skills/client-level/assets/`.
4. Register the skill: `BUNDLED_SKILLS` in `scripts/execforge.py` and the skill list
   in `.claude-plugin/plugin.json`.
5. Add a router row and a trigger-alias row to `skills/c-level/SKILL.md`, without
   touching the locked OKR alias line.
6. Add one eval case `evaluations/client-level.eval.md`: a client question that tempts
   the skill to invent a number and overclaim; it must refuse both.
7. Run `python3 scripts/execforge.py validate` and the test suite. Both must pass.
8. Do not commit. The operator decides when to ship (their `/ship` flow bumps the
   version and changelog).

## Risks

### Risk A — The skill overclaims to a client

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` |
| **What actually happens?** | A client-facing answer promises something the operator cannot deliver (a capability, a price, a security outcome). The client holds the operator to it. Trust and money are lost. |
| **Short or long term?** | `LONG` — the skill will be used on every client exchange. |
| **Solution** | Hard rules in the skill: never invent a number or price (`not measured` / "the operator sets the price"); label every claim observed / inferred / assumed; never promise a security outcome, only what was checked. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | Answers get hedged and less punchy; the operator may find them too careful and stop using the skill. |
| **Cost** | Build time only. Upkeep: keep the rules when the skill is edited. `not measured`. |
| **What we expect after** | The eval case proves the skill refuses to invent a number or promise an outcome. |
| **Does a human need training?** | `YES` — the operator must still read every client answer before sending it. The skill drafts; the operator signs. |

### Risk B — Client secrets leak into deliverables

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | A tenant id, account name, or password pasted during work ends up inside a document that goes to a different reader, or into this public repo. The client's private data is exposed. |
| **Short or long term?** | `LONG` — the operator pastes live credentials into prompts (seen again in the 2026-10-14 usage review). |
| **Solution** | A skill rule: client identifiers and credentials never appear in a deliverable unless the client is the reader and the detail is needed; the skill must say what it removed. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | Over-scrubbing can remove detail a client actually needs (for example their own tenant id in a step guide). The rule allows it when the client is the reader. |
| **Cost** | None beyond writing the rule. Upkeep `not measured`. |
| **What we expect after** | Deliverables name no secret from another engagement; the skill states its scrub. |
| **Does a human need training?** | `YES` — the operator should stop pasting live passwords into prompts (flagged twice now). |

### Risk C — Router confusion with existing skills

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | A request like "make a proposal" could route to `execforge` (product decision) instead of `client-level`, or the other way. The operator gets the wrong lens and retypes. |
| **Short or long term?** | `SHORT` — alias rows and boundaries fix it as cases appear. |
| **Solution** | Clear boundary lines in both the router and the skill: `execforge` decides what WE build; `client-level` shapes what we tell a CLIENT. |
| **What would the solution fix?** | operational load |
| **Risk of the solution itself** | More router rows add reading cost to every routing decision. |
| **Cost** | Minutes per adjustment. `not measured`. |
| **What we expect after** | Client-facing phrasings ("explain to my client", "make a proposal for the client") land on `client-level` without asking. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-10-14 | Build `client-level` before the ux-level `spec` mode | The usage data: client work ran daily; ux-level ran about twice in three months. |
| 2026-10-14 | A new skill, not a mode on an existing one | No existing skill shares its job: every other skill judges or builds the product; this one speaks to a client. The role-architecture "prefer parameters" rule applies when an actor already exists — none does here. |
| 2026-10-14 | Three modes (answer / deliverable / proposal) | They cover the three request shapes that dominate the usage log. Call prep is `answer` mode run over a list of questions. |

## What happened

- 2026-10-14 — Plan written. Build started.
- 2026-10-14 — All eight steps done: decision record, skill with three modes, two
  templates, registration in the validator and the Claude plugin manifest, router and
  alias rows in `c-level` (locked OKR alias line untouched), one eval case. The
  spec-review proposal was also brought into the repo as
  `plans/20260930_ux-level-spec-review.md`, marked adopted; later the same day the
  operator asked for it in the same cycle, and it was built (see that plan's status).
- 2026-10-14 — Gates: `python3 scripts/execforge.py validate` passed; the full test
  suite passed (104 tests, OK). Nothing committed.

## Still unclear

- Whether pricing help should ever suggest a figure. For now: never — the operator
  sets prices, the skill only structures them. The operator can change this.

## Result

ExecForge now has a tenth skill, `client-level`, with `answer`, `deliverable`, and
`proposal` modes and a `CLIENT READY / FIX REQUIRED / REWORK` verdict. Proof: the
files under `skills/client-level/`, the decision record
`docs/decisions/2026-10-14-client-level-skill.md`, the eval case
`evaluations/client-level.eval.md`, a passing validate run, and 104 passing tests.
Left out on purpose: version bump and changelog (the operator's ship step does those).
The ux-level `spec` mode, first marked "scheduled next", was then built in the same
cycle on the operator's instruction and ships in the same branch.

- 2026-10-15 — Test coverage check during the ship step. Found a gap: nothing would
  fail if the new skill text lost its mode table, if the spec mode or its `SPEC PASS`
  verdict was removed, if the router rows to the two new skills were dropped, or if
  the full-cycle Stage 2 wiring was reverted. Added four checks to
  `tests/test_skill_bundle.py` that read those files and fail if the key lines go
  missing. Proof they work: all four fail on the main branch (where the feature does
  not exist) and pass here. Suite now 108 tests, OK; validate still passes. Nothing
  committed.
