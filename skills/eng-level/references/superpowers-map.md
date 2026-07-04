# Superpowers Integration Map

ExecForge does not vendor or modify Superpowers. Install it separately and load its current skills.

| ExecForge stage | Superpowers skill | Relationship |
|---|---|---|
| Product idea still ambiguous | `brainstorming` | Optional discovery before product approval |
| Product and technical design approved | `using-git-worktrees` | Creates isolated implementation workspace |
| Engineering plan needs atomic tasks | `writing-plans` | Converts design into small verifiable tasks |
| Independent tasks in current session | `subagent-driven-development` | Fresh implementer plus task-level reviews |
| Plan executed in another session/batches | `executing-plans` | Batch execution with checkpoints |
| Any feature or bug fix | `test-driven-development` | RED–GREEN–REFACTOR |
| Unexpected failure | `systematic-debugging` | Root-cause process |
| Before claiming completion | `verification-before-completion` | Fresh proof |
| Branch complete | `finishing-a-development-branch` | Merge/PR/keep/discard workflow |

## Non-duplication

- Superpowers task review checks each implementation task.
- gstack Staff Engineer review performs the broad final branch audit.
- ExecForge checks product and operational alignment.
- Eng Level reconciles all evidence and owns the final engineering verdict.


## QA handoff

After implementation and the first whole-branch review, route portal/API/backend changes through `q-level`.

Superpowers verification proves executed commands and task completion. Q Level proves accepted business behavior across system layers. Neither replaces the other.
