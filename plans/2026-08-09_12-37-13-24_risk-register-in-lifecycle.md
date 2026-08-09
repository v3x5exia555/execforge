# Put the risk framework into the lifecycle

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-08-09
- **Last updated:** 2026-08-09
- **Role(s):** full-cycle (lifecycle), c-level (routing)
- **Branch:** lz-risk-register-stage
- **Status:** IN PROGRESS

## What was asked

"Include this into the lifecycle too." Then: "include this new framework between c-level
and eng-level."

The framework is the nine-question risk register landed yesterday in `plans/TEMPLATE.md`.
It works for plan files. The operator wants it inside the governed lifecycle as well.

## Where "between c-level and eng-level" lands

`c-level` is the router — it runs before everything and picks the workflow. `eng-level`
first appears at Stage 1, the upstream approval gate.

So the risk pass sits **after the product decision, before the approval gate**. That
placement has a real benefit beyond following the instruction: the user approving scope
at Stage 1 sees the risks at the same moment. Approving scope and approving its risks
become one decision instead of two.

## Why a lettered stage, not a renumber

Inserting a numbered stage would push Stages 3–9 up by one. Measured blast radius:

| Files referencing stage numbers | Count |
| --- | --- |
| `docs/plans/` historical plans | 2 files, 27 references |
| `skills/full-cycle/references/fallback-implementation-contract.md` | 6 |
| `evaluations/full-cycle*.eval.md` | 2 files, 7 |
| `docs/`, `README.md`, other skills | 4 |

Two of those are historical plan records. Rewriting them to fit a change made a month
later would falsify the record. `Stage 0b` costs nothing and touches none of them.

## Risks

### Risk A — the register becomes a form, not a thought

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` |
| **What actually happens?** | Nine questions per risk is a lot of boxes. People fill them to look complete — "risk of the solution: none", "cost: low" — and the section stops carrying information. Everyone downstream then trusts a document that was never thought about, which is worse than having no document. |
| **Short or long term?** | `LONG` — it gets worse as the habit sets, not better. |
| **Solution** | Three guards already in the framework: `none` on the solution-risk line is called out as almost always wrong; costs must say `not measured` rather than be invented; and "no risks" requires writing why. Add one more at the lifecycle level: the validation gate refuses a `HIGH` risk that has neither a solution nor a recorded decision to accept it. |
| **What would the solution fix?** | Operational load — a reviewer at Stage 1 does not have to work out whether the section was thought about. |
| **Risk of the solution itself** | A gate that blocks on `HIGH` risks creates pressure to grade a real `HIGH` as `MEDIUM` to keep moving. That is a worse failure than an empty box, because it hides rather than bores. |
| **Cost** | One stage in `full-cycle`, one template, one validation line. No code. Upkeep: the template needs revisiting if the nine questions ever change. |
| **What we expect after** | Every lifecycle run reaching Stage 1 carries risks a user can act on, and no `HIGH` reaches Stage 9 silently. |
| **Does a human need training?** | `NO` to fill in — the template asks plain questions. `YES` to judge severity well, and that judgement is the part that cannot be templated. |

### Risk B — the stage is skipped for small work

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | A one-line change does not need nine questions per risk. If the stage feels heavy, it gets skipped quietly, and skipping quietly spreads to changes that did need it. |
| **Short or long term?** | `SHORT` — it shows up as soon as the first small change runs the cycle. |
| **Solution** | Allow `No risks identified` with a one-line reason, exactly as the plan template does. Skipping is fine; skipping silently is not. |
| **What would the solution fix?** | Manual work — no ceremony for changes that do not need it. |
| **Risk of the solution itself** | The escape hatch gets used by default. The reason line is the only thing stopping that, and it depends on the writer being honest. |
| **Cost** | One sentence in the stage definition. `not measured` for upkeep. |
| **What we expect after** | Small changes pass through in one line; the record still shows the question was asked. |
| **Does a human need training?** | `NO`. |

### Risk C — renumbering the lifecycle stages

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` if done, `LOW` as planned |
| **What actually happens?** | Renumbering breaks 10 files, including two eval cases that pin stage numbers and two historical plan documents. Rewriting history to match a later change makes the record untrustworthy. |
| **Short or long term?** | `LONG` — a falsified record stays falsified. |
| **Solution** | Use `Stage 0b`. No existing number moves. |
| **What would the solution fix?** | Operational load and compliance — the audit trail stays true. |
| **Risk of the solution itself** | Lettered stages are slightly odd to read, and a second one later (`0c`) would look worse. If the lifecycle ever needs a real restructure, that is the moment to renumber deliberately, once. |
| **Cost** | Nothing. It is a naming choice. |
| **What we expect after** | The new stage exists and no eval, doc, or historical plan needs editing. |
| **Does a human need training?** | `NO`. |

## The plan

1. `Stage 0b — Risk register` in the `full-cycle` stage sequence, between Stage 0 and
   the Stage 1 approval gate.
2. An operating rule saying what the stage produces and that its output feeds the Stage 1
   user gate.
3. A validation-gate line: no `HIGH` risk reaches the final verdict without a solution or
   a recorded decision to accept it.
4. `skills/full-cycle/assets/risk-register.template.md`, matching how `q-level` and
   `design-html` ship templates.
5. A `c-level` router row between the product row and the engineering-plan row, plus
   trigger words.
6. `docs/full-cycle.md`, CHANGELOG, version bump.

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-09 | `Stage 0b`, not a renumber | Renumbering touches 10 files including historical records. Measured, not assumed. |
| 2026-08-09 | Before the Stage 1 approval gate | The user approves scope and its risks in one decision instead of two. |
| 2026-08-09 | Gate on `HIGH` only | Gating on every risk would guarantee the form-filling failure in Risk A. |
| 2026-08-09 | Allow `No risks identified` with a reason | Without an honest escape hatch, small changes teach people to skip silently. |

## What happened

- 2026-08-09 — Measured what renumbering would break: 10 files, 2 of them historical.

## Still unclear

- Whether `eng-level` should re-check the register at Stage 6. Not doing it now; one
  placement first, then see whether anything is actually missed.

## Result

Shipped as 0.15.0.

- `Stage 0b — Risk register` in the `full-cycle` stage sequence, between Stage 0 and the
  Stage 1 approval gate.
- Operating rule 5b defines what the stage produces and that it feeds the Stage 1 gate.
- Validation gate: no `HIGH` risk reaches the final verdict without a solution or a
  recorded acceptance naming who accepted it. The skill names grading-down as the failure
  that line exists to catch.
- `skills/full-cycle/assets/risk-register.template.md`, with sections for the Stage 1
  approval, accepted risks, and changes during the cycle.
- `c-level` router row placed between the product row and the engineering-plan row, plus
  trigger words.
- `docs/full-cycle.md` stage table updated.

No stage was renumbered, so none of the 10 files carrying stage numbers needed editing —
including the two historical plan records.

Verified: 104 passed, 221 subtests; validate passed; release-check consistent; the
`Authorization / Rules-of-Engagement gate` string that `test_skill_bundle` pins is
still present.
