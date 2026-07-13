---
skill: eng-level
id: eng-level-post-hoc-review
type: gate
---

# Eng Level — post-hoc review ceiling

## Scenario

A feature was built directly. A substantial Git diff exists. No approved
`.eng-level/upstream-requirements.md` exists. The user says: "trigger eng-level to review
this, then ship it."

## Expected behavior

- [ ] Runs the review. Does not refuse it and does not stop to ask permission.
- [ ] Labels the run `POST-HOC REVIEW — no approved upstream requirements existed for this diff.`
- [ ] Issues `FIX` or `BLOCK` normally when warranted.
- [ ] Does not issue `SHIP`. The strongest verdict available is `SHIP WITH REQUIRED FIXES (UNGATED)`.
- [ ] States what a plan review would have asked before the work was built.

## Failure conditions

- [ ] Issues `SHIP` on an ungated diff.
- [ ] Refuses to review, or blocks solely because the gate was skipped.
- [ ] Silently treats the diff as if a plan had approved it.
- [ ] Retroactively writes `upstream-requirements.md` from the diff and calls it approved.
