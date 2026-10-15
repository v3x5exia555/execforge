# Plan: ExecForge — UI/UX Spec Review (`ux-level` gains a `spec` lens)

**Author:** operator (Tyson) + ExecForge orchestrator
**Companion skills:** `skills/ux-level/` (extends) · `skills/design-html/` (downstream) · `skills/c-level/` (router row)
**Date:** 2026-09-30

> In plain words: this plan adds a third way of using the `ux-level` review skill —
> checking a written design document ("spec") for holes before anything gets built,
> instead of only reviewing a user's step-by-step journey. A "lens" below just means
> a way of looking; "multi-tenant" means many customers sharing one system.

**Status:** SHIPPED in release 0.17.0, merged to main in PR #30 on 2026-10-15.
Earlier: IMPLEMENTED 2026-10-14 — operator said "proceed", then "include ux-level with
the lifecycle", so it was built in the same cycle as `client-level` instead of after it.
What shipped: the `spec` mode and seven pillars in `skills/ux-level/SKILL.md`,
`skills/ux-level/references/spec-pillars.md`, the Stage 2 wiring in
`skills/full-cycle/SKILL.md` (spec mode gates `design-html` when a written spec
exists), router and alias rows in `skills/c-level/SKILL.md` covering "review the
spec / PRD / plan / proposal" for UI/UX documents, the eval case
`evaluations/ux-level-spec-review.eval.md`, and the decision record
`docs/decisions/2026-10-14-ux-level-spec-mode.md`.

**Honest note on the eval (2026-10-15):** the eval case file exists and parses, but it
has **not been run**. The CI eval job only runs the first five case files by name
(`--limit 5` — raised from 4 in this same branch so an older case was not pushed out),
and this case sorts 16th, so CI will not run it either. The "Done =" line in Part 4 is
therefore only partly met: `validate` passes and nothing regressed, but the eval's
pass is unproven. Fixing CI eval selection so changed skills' cases actually run is a
recorded P1 TODO (see `TODOS.md`).

## Risks (operator format)

### Risk A — Mode picks wrong: a spec reviewed as a journey, or the reverse

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | The review answers the wrong question — a document gets a step walk-through, or a described flow gets a document audit. The operator retypes and loses a few minutes. |
| **Short or long term?** | `SHORT` — phrasing triggers are adjusted as misses appear. |
| **Solution** | Explicit trigger words (naming a document selects `spec`); the skill says which mode ran and why in one line, so a wrong pick is visible immediately. |
| **What would the solution fix?** | operational load |
| **Risk of the solution itself** | More alias rows add reading cost to routing. |
| **Cost** | Minutes per adjustment. `not measured`. |
| **What we expect after** | "Review this spec/PRD/plan" lands in spec mode without asking. |
| **Does a human need training?** | `NO` |

### Risk B — The gate becomes ceremony on tiny specs

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | A one-paragraph change gets a seven-pillar audit; the operator starts skipping the gate, and then it also misses the specs that matter. |
| **Short or long term?** | `LONG` — gate fatigue is the documented failure of this operator's history (33 bare "proceed" in three months). |
| **Solution** | Stage 2 wiring fires only when a written spec exists; non-UI scope stays `NOT APPLICABLE`; small changes without a spec document never enter the mode. |
| **What would the solution fix?** | operational load |
| **Risk of the solution itself** | A real spec disguised as a chat message slips past the gate. |
| **Cost** | None beyond the wording. Upkeep `not measured`. |
| **What we expect after** | The mode fires on documents, not on every UI sentence. |
| **Does a human need training?** | `NO` |

---

## Executive summary

ExecForge reviews UI/UX **journeys** (`ux-level`) and translates approved scope into UI
**structure** (`design-html`). It has no lens that reviews a **written UI/UX
specification** *before* a journey exists or a screen is built — the upstream document
review that asks "is this spec complete, consistent, and buildable?"

That is the exact stage where OrbixShield leaked: scope, tenancy, and target-user were
*inferred* rather than specified, states and failure paths were discovered by hitting
them in production, and reviews ran *after* the build. A spec-review lens is the cheapest
possible gate — it catches missing states and contradictions while they are still words,
not code.

**The fix follows the role-architecture principle: not a new skill, a new lens.**
`ux-level` already selects between `product` and `technical` modes. Add a third mode,
`spec`, that reviews a specification document instead of a described journey — same actor,
same severity matrix, same verdict vocabulary.

---

## Part 1 — The gap, with evidence

### Finding 1 — `ux-level` reviews journeys, not specs (by design)

`skills/ux-level/SKILL.md` is explicit:

> *"Reviews a described journey; it does not design screens, write code, or replace
> product approval."*
> *"Review the journey the user actually described. Do not invent steps the user did not
> state."*

Its required inputs are **product context, target user, and the journey in order**. Hand
it a spec document and it either waits for a journey it was not given, or reviews half a
thing. The skill is correct to refuse — journey review is a different job. But it means
spec review has **no owner**.

### Finding 2 — `design-html` assumes the spec is already sound

`design-html` "translates approved product scope into UX/interface structure." It consumes
a spec; it does not critique one. If the spec is missing an error state, `design-html`
inherits the gap.

### Finding 3 — the un-owned stage is where OrbixShield broke

From `skill-usage-feedback.md` (OrbixShield retro):

- *"Scope, tenancy, and target-user often had to be inferred."*
- *"A step with no failure path is an unfinished step"* — yet failure paths were found in
  production (spam delivery, forbidden-referer, invalid-credentials loops).
- The recurring pattern was *"do X, then trigger review"* — review **after** build.

A spec-review gate is the one review cheap enough to run **before** anything is built, and
it targets precisely the inputs OrbixShield had to guess.

---

## Part 2 — The change

### Change 0 — add mode `spec` to `ux-level` (prerequisite)

`ux-level` gains a third mode alongside `product` and `technical`:

| Mode | Reviews | Trigger phrasing (auto-inferred) |
|---|---|---|
| `product` | a consumer/business journey | "review the onboarding flow" |
| `technical` | a data/admin/dashboard journey | "review the admin console flow" |
| **`spec`** *(new)* | a **written UI/UX specification** | "review the spec", "review the PRD", "is this spec complete" |

Consistent with the role-architecture evidence (you never type flags), the mode is
**inferred from phrasing** and defaults to `auto`. Naming a document or PRD selects
`spec`; describing a walk-through selects `product`/`technical`.

### What `spec` mode checks — the seven completeness pillars

The review reads the spec and rates each pillar, citing the section (or its absence):

1. **State completeness** — every screen defines empty / loading / error / success /
   no-permission. A missing state is a finding, not an omission to be charitable about.
2. **Failure & recovery paths** — what the user does when a step fails, times out, or a
   dependency never responds. (Directly imports the ux-level "a step with no failure path
   is unfinished" rule.)
3. **Scope, target user, tenancy** — who this is for, what they already know, single- vs
   multi-tenant. "A user" is not a persona. (The OrbixShield inference gap.)
4. **Accessibility & responsive behavior** — keyboard, contrast, screen-reader intent,
   breakpoints — specified, not assumed.
5. **Design-system conformance** — reuses existing components/tokens, or flags each net-new
   element and why it must exist.
6. **Acceptance criteria clarity** — is "done" testable? Ambiguous criteria are a finding
   (the OrbixShield "test until fix with no pass criterion" failure).
7. **Feasibility & constraints** — does the spec ask for something the stack, data, or
   deploy target cannot deliver. Flag, do not silently accept.

### Output contract

- A **completeness matrix**: seven pillars × {covered / partial / missing / contradictory},
  each cell cited to a spec section or marked absent.
- A **prioritized gap list**, worst-first, each with the recommended addition and the risk
  of shipping without it (honors commit 259ae08: recommendation + risk on every list).
- A **verdict**, reusing ux-level's vocabulary shifted to spec stage:
  - `SPEC PASS` — buildable as written.
  - `FIX REQUIRED` — named gaps must be closed before build.
  - `REDESIGN` — the spec's core model is unsound; back to product decision.

### Handoff

`SPEC PASS` (or a `FIX REQUIRED` with fixes approved) hands to `design-html` for structure,
then to `ux-level` `product`/`technical` for the journey once screens exist. Spec → structure
→ journey, each gated.

---

## Part 3 — Options considered (recommendation + risk)

| Option | What | Risk | Verdict |
|---|---|---|---|
| **B — `spec` mode on `ux-level`** *(recommended)* | one UI/UX actor, three lenses, shared matrix + verdict | mode-selection must reliably distinguish "spec" from "journey" phrasing — mitigated by explicit trigger words and `auto` fallback that asks | **ADOPT** |
| A — new standalone `ux-spec-review` skill | clean separation | duplicates ux-level's persona, matrix, and verdict; two skills drift; contradicts the role-architecture "not new skills, parameters" finding | REJECT |
| C — fold spec checks into `design-html` | no new surface | conflates critique with production; design-html would both judge and build the spec — no independent gate | REJECT |

**Recommendation: Option B.** It matches the principle that produced your best release,
keeps one owner for UI/UX, and reuses proven machinery.

---

## Part 4 — Rollout

1. Extend `skills/ux-level/SKILL.md`: add the `spec` row to mode selection and a
   `Mode: spec` section with the seven pillars.
2. Add `skills/ux-level/references/spec-pillars.md` (the detailed checklist), mirroring the
   existing `references/pillars.md`.
3. Add a `c-level` router row: *"A written UI/UX spec needs reviewing before build → use
   `ux-level` (spec mode)."*
4. Add one eval case under `evaluations/` — a deliberately incomplete spec (missing an
   error state + vague acceptance criteria) that must yield `FIX REQUIRED` naming both.
5. `python3 scripts/execforge.py validate` and the eval must pass.

**Done =** the incomplete-spec eval returns `FIX REQUIRED` citing the seeded gaps; `validate`
passes; no regression in existing ux-level `product`/`technical` behavior.

---

## Non-goals

- Not a visual/branding critique (that is journey + design-html territory).
- Not backend/infra spec review (eng-level / platform).
- Does not replace the product decision — a spec that fails at the model level routes back
  to `execforge`, it is not re-decided here.
- Does not require typing flags; mode is inferred.

---

## Why this is the right next skill work

It closes the one un-owned UI/UX stage, at the cheapest point in the lifecycle, targeting
the exact inputs OrbixShield had to guess — and it does so by extending your strongest
release rather than proliferating skills. It is framework-inward work (your Mode 1
strength) that directly repairs a Mode 2 failure.
