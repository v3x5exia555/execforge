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
selector safety, and lifecycle metadata without modifying a repository.

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

The operating commands have a metadata-only output boundary. State and Git
output are byte/count/length bounded, control characters are escaped, blocker
contents are counted rather than printed, and the raw recorded `next_action`
is never printed. Diagnostics are read-only; they do not repair selectors or
artifacts.

## Recovery and rollback

To abandon operating-layer state introduced only on a feature branch, remove
the selectors and run directories created by that branch, or revert the
feature branch. Do this only after confirming the run IDs are not shared with
work you intend to keep. Prior legacy artifacts are preserved by the CLI; it
does not silently migrate or delete them. Leave the stable lock file in place:
`.execforge-init-run.lock` is harmless, ignored, and provides the stable lock
file inode needed for process coordination.

## Portal/API/backend QA

After implementation and the first Staff Engineer review:

```text
/q-level --mode=auto
```

Review the risk-based plan and respond:

```text
APPROVE QA PLAN
```
