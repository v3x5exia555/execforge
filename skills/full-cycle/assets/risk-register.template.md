# Risk register — <initiative>

- **Cycle stage:** 0b
- **Built from:** Stage 0 approved scope
- **Date:** YYYY-MM-DD
- **Last updated:** YYYY-MM-DD

One block per risk, named `Risk A`, `Risk B`, and so on, so later stages can refer to
them. Carried into Stage 1 so the user approves scope and its risks together. Updated —
never rewritten — when a later stage finds a new risk.

Two rules that keep this honest:

- **Never invent a cost or a number.** Where none is known, write `not measured`.
- **If there is genuinely no risk**, write `No risks identified` and one line saying why.
  A silent skip is not allowed; an empty section is not the same as a considered one.

---

### Risk A — <short name>

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` / `MEDIUM` / `LOW` |
| **What actually happens?** | The real-world impact if this lands. Who is hurt and how — not the label repeated. |
| **Short or long term?** | `SHORT` — a one-off that passes. `LONG` — structural, it stays until something changes. |
| **Solution** | What we would do about it. `none yet` is an honest answer. |
| **What would the solution fix?** | Only what genuinely applies: operational load / manual work / automation / compliance. `none of these` is allowed and often true. |
| **Risk of the solution itself** | Every fix brings its own risk. `none` is almost always wrong — say what this one brings. |
| **Cost** | Build time, money, and ongoing upkeep. `not measured` where unknown. |
| **What we expect after** | What should be true once it is in place. This is what gets checked at Stage 9. |
| **Does a human need training?** | `NO` — works without anyone learning anything. `YES` — say who must learn what, because that is a hidden cost. |

### Risk B — <short name>

...repeat per risk...

---

## Stage 1 approval

- **Risks shown to the user:** yes / no
- **User response:** approved / approved with conditions / rejected
- **Conditions recorded:** …

## Accepted risks

Any `HIGH` risk carried to Stage 9 without a solution must appear here, or the validation
gate fails.

| Risk | Why accepted | Accepted by | Date |
| --- | --- | --- | --- |

## Changes during the cycle

| Date | Stage | What changed | Risk |
| --- | --- | --- | --- |
