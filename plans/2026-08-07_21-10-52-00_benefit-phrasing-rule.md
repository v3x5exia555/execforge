# Make the scope ledger say what the user gets

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-08-07
- **Last updated:** 2026-08-07
- **Role(s):** execforge (product decision)
- **Branch:** lz-benefit-phrasing, stacked on lz-ux-level
- **Status:** IN PROGRESS

## What was asked

The operator pasted an A.C.T.I.O.N. framework for turning features into benefits, then
asked whether ExecForge already thinks this way, then said: "add this for product only".

"Product only" means `execforge`. Nothing in `eng-level`, `q-level`, `full-cycle` or any
other skill changes.

## What the check found

Two corrections came out of looking properly, and both shrank the job.

1. ExecForge already has an **A-C-T-I-O-N Operational Matrix**, and it means something
   completely different: Assess the problem, Cost optimisation, Technical tactics,
   Incorporate security and governance, Operational work reduction, No manual work by
   default. Same six letters, different framework. Adding a second one under the same
   name would be a trap for every future reader.
2. The Phase 5 scope ledger already has **User Pain**, **User Value** and **Business
   Value** columns. An earlier claim that the ledger held "no value" was wrong.

So of the six letters in the operator's framework, only two were genuinely missing:

- An **action verb** rule for how the User Value cell is written. A style rule.
- **Next Step Enabled** — what the user can do *because* this shipped. Nothing in
  ExecForge asked this.

## The product decision (execforge)

**Mode used:** single isolated review. Documentation only, one revert undoes it.

**Gatekeeper: PARTIAL.** The operator's need is real, but the framework as pasted is
mostly already covered. Building all six letters would add ceremony, not judgement.
Reduced to the two parts that are actually new.

**Scope mode:** Scope Reduction. The ask was a framework; the answer is two rules.

**CEO view:** a benefit line changes how a decision *reads*, not whether it is `GO` or
`KILL`. That is worth little when the reader is the operator, and worth a lot when the
output goes to engineers or stakeholders. Small, cheap, keep it small.

**COO view:** a full product review already loads 868 lines of instructions. Every line
added is paid on every run. Six letters per scope item also invites padding, and a
padded benefit line is worse than a blunt one — it reads as checked rather than thought
about.

**Scope ledger:**

| Item | Call | Why |
| --- | --- | --- |
| Action-verb rule for the User Value cell | ADD NOW | Genuinely missing, costs a line. |
| "Next step enabled" as a recorded field | ADD NOW | The one real gap in the framework. |
| A second six-letter framework | SKIP | Four of six letters already exist elsewhere; the name collides with the locked matrix. |
| Editing the Phase 5 ledger table itself | SKIP | Phase 5 is locked by operator decision 2026-07-31. "Proceed" is not the explicit instruction the lock demands. |
| Any change to `eng-level`, `q-level`, `full-cycle` | SKIP | Operator said product only. |

**Verdict: GO WITH CONDITIONS.** Add the two rules as a new section next to the ledger.
Do not touch locked text.

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-07 | New section beside Phase 5, not new columns inside it | Phase 5 is locked and `tests/test_restored_sections.py` fails on any drift. The lock needs explicit permission, and "proceed add this" is not that. |
| 2026-08-07 | Call it "Benefit line", not A.C.T.I.O.N. | The A-C-T-I-O-N name is already taken by the locked operational matrix. Two meanings, one name, is a trap. |
| 2026-08-07 | Two rules, not six letters | Four of the six were already covered. Adding them again costs context on every run and buys nothing. |
| 2026-08-07 | Stack the branch on `lz-ux-level`, version 0.13.1 | PR #15 already claims 0.13.0. Stacking avoids a third version collision and needs no unilateral merge. |

## What happened

- 2026-08-07 — Checked the repo. Found the name collision and the existing value columns.
- 2026-08-07 — Corrected an earlier wrong claim that the ledger held no value columns.
- 2026-08-07 — Ran the product review above and cut the scope from six letters to two rules.

## Still unclear

- Whether the operator wants the ledger table itself to gain columns. That needs
  explicit permission because Phase 5 is locked. Until then the rule sits beside it.

## Result

Added **Phase 5a — Benefit line** to `skills/execforge/references/review-phases.md`,
sitting directly after the locked Phase 5 ledger. Wired into three places in
`skills/execforge/SKILL.md`: the resolution step, the required final output, and the
validation gate.

Checked and passing:

- `pytest tests/` — 97 passed, 213 subtests.
- `tests/test_restored_sections.py` — 5 passed. Every locked section is still
  byte-identical.
- `validate` — passed. `release-check` — consistent.
- `git diff --name-only -- skills/` lists only `execforge`. No engineering, QA,
  security, design, or lifecycle skill changed, which is what "product only" required.

Version 0.13.1, stacked on `lz-ux-level` because PR #15 already claims 0.13.0.
