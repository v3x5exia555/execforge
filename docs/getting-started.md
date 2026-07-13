# Getting Started

## Prerequisites

- Python 3.10+
- Git for engineering diff review
- An Agent Skills-compatible coding agent
- Optional: gstack skills
- Optional: Superpowers

## Install

```bash
python3 scripts/execforge.py validate
python3 scripts/execforge.py install --target claude
python3 scripts/execforge.py doctor --installed
```

Or project-local:

```bash
python3 scripts/execforge.py install --destination .claude/skills
```

For a read-only check across the direct-child Git repositories in a portfolio:

```bash
python3 scripts/execforge.py doctor --portfolio ~/Desktop/project
```

Installed diagnostics compare bundled skill files with known installation
roots. Portfolio diagnostics report instruction coverage, Git conflicts,
selector safety, and lifecycle metadata without modifying a repository. The
scan stays within real, non-symlinked direct-child repositories and applies the
same branch, reachable-commit, and frozen implementation-HEAD checks as
`resume`.

## First product review

```text
/execforge Review this initiative:
Problem:
Target user:
Current workaround:
Proposed change:
Evidence:
Constraints:
```

## Engineering handoff

For UI-facing work with approved scope, optionally translate the product intent into interface output first:

```text
/design-html
```

```text
/eng-level --mode=auto
```

Review the interpreted upstream requirements and respond:

```text
APPROVE UPSTREAM
```

## Initialize artifact directories

```bash
python3 scripts/execforge.py init-run --name my-feature --root <repo>
```

Each initialization creates one matching initiative run:

```text
.execforge/runs/<run-id>/
.eng-level/runs/<run-id>/
.q-level/runs/<run-id>/
```

`.execforge/current.json` is the authoritative selector. The
`.eng-level/current.json` and `.q-level/current.json` files are compatibility
projections for older namespace-specific readers. Selectors are rebuildable
indexes; the selected runtime/test/code/Git/artifact evidence remains the
source of truth. A safe legacy root `state.json` can be read only when no safe
current selector is available, and it is never silently migrated or deleted.

Initialization uses the stable lock file `.execforge-init-run.lock`, which is
ignored by Git and intentionally retained so concurrent processes keep
coordinating on the same inode. The Windows lock implementation uses `msvcrt`,
but runtime CI coverage remains limited when the suite is run only on POSIX.

## Check, resume, and choose the next action

```bash
python3 scripts/execforge.py status --root <repo>
python3 scripts/execforge.py resume --root <repo>
python3 scripts/execforge.py next --root <repo>
```

`resume` prints bounded metadata about the selected engineering run, the
current Git branch/HEAD, the evidence and backlog locations, and warning codes.
It exits `0` when a safe state is readable, even if warnings identify stale
lineage; it exits `1` when no safe lifecycle state can be read.

`next` prints exactly one `next_action:` line derived from evidence. It exits
`1` and chooses a reconciliation or blocker action for Git conflicts, unsafe or
unreadable state, stale lineage, open blockers, or an unknown lifecycle state.
Normal lifecycle and reached-boundary actions exit `0`. Pending upstream
approval remains an explicit approval request. Once a `stop_after` boundary is
reached, `next` waits for a new explicit user instruction and does not advance
past the boundary.

State is fresh only when the recorded branch equals the current branch, the
recorded `commit` and `base_commit` (when present) resolve to commits that are
ancestors of current HEAD, and frozen review states (`REVIEW_READY`,
`REVIEW_PASSED`, `SHIP_READY`) have both a reachable `base_commit` and an
`implementation_head` exactly equal to current HEAD. Missing, invalid,
divergent, or mismatched frozen lineage requires reconciliation.

An absent `branch` key is unknown lineage and fails closed. An explicit null
records a detached HEAD and is valid only while Git also reports no current
branch; it does not mean “branch not checked.” Planning or any later state also
requires `upstream_approval_status` to be exactly `APPROVED`.

Frozen review states also fail closed with `material_worktree_changes` when any
tracked or untracked path outside the governance namespaces differs from HEAD.
`.execforge/`, `.eng-level/`, `.q-level/`, and the stable
`.execforge-init-run.lock` are exempt so run artifacts and lock coordination
can remain untracked or modified. The warning reports no file paths; inspect
`git status` before returning to review or ship readiness.

## Output safety boundary

For `doctor --portfolio`, `resume`, and `next` only, output is allowlisted,
bounded, terminal-safe metadata output. This boundary excludes the legacy
`status` report. It is not semantic secret/PII redaction: displayed metadata
fields such as `initiative`, `branch`, `project`, and evidence paths must not
contain sensitive content.

State and Git input are byte/count/length bounded, control characters are
escaped, blocker contents are counted rather than printed, and the raw recorded
`next_action` is never printed. These diagnostics are read-only; they do not
repair selectors or artifacts.

Separately, the three created-path acknowledgements from `init-run` are bounded
and terminal-safe. Selector rollback/authorization reads accept only bounded
regular files, and backlog summaries are streamed under byte and line limits;
oversized or special files are treated as unreadable.

## Recovery and rollback

The commands report evidence; the operator chooses and performs recovery. No
repair is performed by diagnostics.

### Malformed or unsafe selector

If `resume` reports `selector_malformed`, inspect `.execforge/current.json`,
both compatibility projections, and the referenced state files. Confirm that
the run IDs agree and every path names the expected contained regular file.
Keep `next` stopped until a known existing Eng/QA run pair is intentionally
selected or the feature branch is reverted; no repair is performed.

### Stale branch or commit lineage

Compare recorded state with read-only Git evidence:

```bash
git branch --show-current
git rev-parse HEAD
git merge-base --is-ancestor <recorded-commit> HEAD
```

For stale branch or commit lineage, switch to the recorded branch when it is
the intended work, or return to the lifecycle stage that can record evidence
from the actual branch and reachable commits. Do not overwrite lineage merely
to silence a warning.

### Missing frozen-review lineage

Warnings `base_commit_missing` or `implementation_head_missing` mean a frozen
review state is incomplete. Inspect the selected state, current HEAD, and the
review artifacts, then return to review and record `base_commit` plus the exact
reviewed `implementation_head`. Never invent hashes or infer approval from the
state name.

### Safe legacy fallback

A contained legacy root state may remain inspectable through `resume` when the
current selector is unsafe. That safe legacy fallback cannot authorize forward
progress while an unsafe selector warning exists: `next` exits nonzero and
requires selector reconciliation. Preserve the legacy files while identifying
the intended initiative run or rolling back.

### Intentional rollback

Before deleting anything, confirm the selected `run_id` in all selectors and
confirm which run directories belong only to the feature branch. Then remove
only those selectors and run directories, or revert the feature branch. Prior
legacy artifacts remain preserved. Leave `.execforge-init-run.lock` in place;
it is ignored and provides the stable inode used for process coordination.

## Portal/API/backend QA

After implementation and the first Staff Engineer review:

```text
/q-level --mode=auto
```

Review the risk-based plan and respond:

```text
APPROVE QA PLAN
```
