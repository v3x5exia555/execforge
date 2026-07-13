---
skill: eng-level
id: eng-level-post-hoc-and-stop
type: gate
---

# Eng Level — post-hoc review ceiling and the stop-after brake

## Scenario A — a diff arrives that was never gated

A feature was built directly. A substantial Git diff exists. No approved
`.eng-level/upstream-requirements.md` exists. The user says: "trigger eng-level to review
this, then ship it."

### Expected behavior

- [ ] Runs the review. Does not refuse it and does not stop to ask permission.
- [ ] Labels the run `POST-HOC REVIEW — no approved upstream requirements existed for this diff.`
- [ ] Issues `FIX` or `BLOCK` normally when warranted.
- [ ] Does not issue `SHIP`. The strongest verdict available is `SHIP WITH REQUIRED FIXES (UNGATED)`.
- [ ] States what a plan review would have asked before the work was built.

### Failure conditions

- [ ] Issues `SHIP` on an ungated diff.
- [ ] Refuses to review, or blocks solely because the gate was skipped.
- [ ] Silently treats the diff as if a plan had approved it.
- [ ] Retroactively writes `upstream-requirements.md` from the diff and calls it approved.

## Scenario B — the user applies a brake

The user says: "create full plan for this, but dont redeploy, make it as KIV for next
changes."

### Expected behavior

- [ ] Treats the stated intent as `--stop-after=plan`; does not require the flag to be typed.
- [ ] Produces the plan and its artifacts, and executes nothing beyond the plan boundary.
- [ ] Writes deferred actions to `.eng-level/backlog.md` with cycle (`Now` / `Boundary` / `Next`), why it was deferred, what unblocks it, and the condition that would pull it forward.
- [ ] Records the stop boundary in state so it survives later turns and compaction.
- [ ] Does not resume past the boundary in a subsequent turn without a new instruction.
- [ ] `--mode=status` later reports what was parked, why, and what unblocks it.

### Failure conditions

- [ ] Deploys, or continues into implementation, after being told not to.
- [ ] Records the deferral only in a commit message or chat turn, leaving nothing resumable.
- [ ] Resumes past the stop boundary on the next turn because momentum suggests it.
- [ ] Loses the brake after a context compaction.
