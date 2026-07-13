# Lifecycle State and Artifacts

## State machine

```text
NO_CONTEXT
→ UPSTREAM_INTAKE
→ UPSTREAM_APPROVAL_REQUIRED
→ PLAN_REQUIRED
→ PLAN_APPROVED
→ WAITING_FOR_IMPLEMENTATION
→ IMPLEMENTATION_IN_PROGRESS
→ REVIEW_READY
→ REVIEW_PASSED
→ SHIP_READY
```

Return states:

- `RETURN_TO_PRODUCT_PLAN`
- `RETURN_TO_PLAN`
- `RETURN_TO_IMPLEMENTATION`
- `BLOCKED`

## Evidence precedence

1. Reproducible runtime behavior and executed tests
2. Actual code, schema, and configuration
3. Git diff and commit history
4. Initiative run artifacts and recorded approvals
5. Approved engineering plan
6. Comments and stated intent
7. Unsupported assumptions

The machine selector is only a rebuildable index into that evidence. A selected
run never outranks contradictory runtime behavior, executed tests, actual code,
Git diff/history, or artifacts. Reconcile the selector or state; do not rewrite
stronger evidence to agree with it.

## Initiative-scoped artifact layout

```text
.execforge/
├── current.json                         # authoritative selector
└── runs/<run-id>/                       # product/coordination artifacts
.eng-level/
├── current.json                         # compatibility projection
└── runs/<run-id>/
    ├── state.json
    ├── upstream-requirements.md
    ├── upstream-approval.md
    ├── upstream-traceability.md
    ├── engineering-plan.md
    ├── implementation-tasks.md
    ├── test-matrix.md
    ├── staff-review.md
    ├── conformance.md
    ├── contradictions.md
    ├── backlog.md
    └── decision.md
.q-level/
├── current.json                         # compatibility projection
└── runs/<run-id>/                       # QA state and evidence
.execforge-init-run.lock                 # stable ignored coordination file
```

The three `.execforge/runs/<run-id>`, `.eng-level/runs/<run-id>`, and
`.q-level/runs/<run-id>` directories share one run ID. The authoritative
selector `.execforge/current.json` commits the active Eng/QA pair;
`.eng-level/current.json` and `.q-level/current.json` are compatibility
projection files for namespace-specific readers. They are not independent
lifecycle decisions.

The stable ignored `.execforge-init-run.lock` remains on disk after each
initialization. The OS lock is released, but retaining the file preserves a
stable inode so a new process cannot bypass an existing waiter.

## Compatibility

A contained, regular legacy root state such as `.eng-level/state.json` may be
read only when no safe current selector is available. If a safe selector names
a malformed selected state, fail closed rather than switching runs. Never
silently migrate or delete legacy root state or its sibling artifacts. Their
presence is evidence that may be needed for recovery or comparison.

## Freshness and lineage

Re-entry reconciles the state record with read-only Git queries:

- Branch equality is exact: `branch` must equal the current branch. Missing
  branch metadata is unknown lineage; `base_branch` is not a substitute. An
  absent `branch` key fails closed as `branch_lineage_unknown`. An explicit
  null represents a detached HEAD and is valid only when Git also reports no
  current branch.
- Recorded `commit` and `base_commit`, when present, must resolve to commit
  objects that are ancestors of current HEAD. Descendant work is therefore
  fresh; invalid or divergent commits are stale.
- Frozen review states — `REVIEW_READY`, `REVIEW_PASSED`, and `SHIP_READY` —
  require a non-null reachable `base_commit` plus an `implementation_head`
  exactly equal to current HEAD (the exact implementation head). Missing,
  invalid, divergent, or mismatched values require reconciliation.
- `BLOCKED` is phase-ambiguous and does not by itself freeze the implementation
  snapshot.
- Frozen review states fail closed with `material_worktree_changes` when a
  tracked or untracked path differs from HEAD. `.execforge/`, `.eng-level/`,
  `.q-level/`, and the stable `.execforge-init-run.lock` are exempt so
  governance artifacts and lock coordination can remain modified or
  untracked. The diagnostic reports only the finding code, never the path.

At `PLAN_REQUIRED` or any later-ranked state, `upstream_approval_status` must
be exactly `APPROVED`. A missing, pending, rejected, or reopened approval
returns to the approval request before planning, review, QA, or ship handoff.

Runtime behavior, tests, code, Git, and artifacts outrank any stale machine
selector or state field.

## Resume, next action, and stop boundaries

Use:

```bash
python3 scripts/execforge.py resume --root <repo>
python3 scripts/execforge.py next --root <repo>
```

`resume` reports selected run metadata, actual Git branch/HEAD, lifecycle
state, `stop_after`, blocker count, evidence/backlog locations, and warnings.
It returns `0` when a safe lifecycle state is readable, including when that
state needs stale-lineage reconciliation, and `1` when no safe state is
readable.

`next` emits exactly one derived `next_action:` line. Its safety precedence is:
Git conflicts; unreadable/unsafe state; stale lineage; open blockers; upstream
approval; plan; implementation; review; QA; ship-ready handoff. Conflicts,
unsafe/stale/unknown state, and blockers return `1`; ordinary lifecycle actions
and a reached stop boundary return `0`.

The persisted `stop_after` values enforce these reached boundaries:

| `stop_after` | Boundary is reached at |
|---|---|
| `product` | `PLAN_REQUIRED` or later |
| `plan` | `PLAN_APPROVED` or later |
| `implement` | `REVIEW_READY` or later |
| `review` | `REVIEW_PASSED` or later |
| `qa` | `SHIP_READY` |

Before the boundary, `next` returns the ordinary action for the current state.
At or after it, `next` returns an action to await explicit user instruction;
it never silently clears `stop_after` or advances beyond the boundary.

## Output safety and diagnostic boundary

For `doctor --portfolio`, `resume`, and `next` only, output is allowlisted,
bounded, terminal-safe metadata output. The legacy `status` report is outside
this boundary. This is not semantic secret/PII redaction. Displayed metadata
fields — including `initiative`, `branch`, `project`, and evidence paths — must
not contain sensitive content.

Selector/state files and Git output are bounded before parsing; state fields,
blocker counts, and lengths are validated. Terminal control characters,
including bidirectional and format controls, are escaped. The commands report
blocker counts rather than blocker contents, and the raw `next_action` stored
in state is not printed. `next` derives its action from validated lifecycle
evidence.

Diagnostics do not fix selectors, change Git state, reconstruct artifacts,
install hooks, send telemetry, or publish a dashboard.

## Recovery and rollback

Use the following evidence checks separately. Diagnostics make no state change;
no repair is performed.

### Malformed or unsafe selector

On `selector_malformed`, inspect `.execforge/current.json`,
`.eng-level/current.json`, `.q-level/current.json`, and their referenced state
files. Verify one canonical run ID, aligned Eng/QA paths, repository
containment, regular files, and matching run directories. Select a known
existing pair only through an intentional operator change; no repair is
performed by `resume`, `next`, or `doctor`.

### Stale branch or commit lineage

Check the repository independently of recorded state:

```bash
git branch --show-current
git rev-parse HEAD
git merge-base --is-ancestor <recorded-commit> HEAD
```

For stale branch or commit lineage, compare `branch`, `commit`, and
`base_commit` with these results. Switch to the intended recorded branch, or
return to the appropriate lifecycle stage and record evidence from actual
reachable commits. Do not rewrite lineage simply to make the warning disappear.

### Missing frozen-review lineage

Warnings `base_commit_missing` and `implementation_head_missing` mean the
selected frozen state lacks required review evidence. Inspect current HEAD,
the selected state, and staff-review artifacts; then return to review and
record a reachable `base_commit` and the exact reviewed `implementation_head`.
A lifecycle state label alone is not evidence of review or approval.

### Safe legacy fallback

When an unsafe selector exists, a contained regular legacy state can remain
inspectable in `resume`. That safe legacy fallback cannot authorize forward
progress while the unsafe selector warning exists. `next` returns a nonzero
reconciliation action even though legacy metadata was readable. Preserve the
legacy state while the operator identifies the intended run or rolls back.

### Intentional rollback

First confirm the selected `run_id` in the authoritative selector and both
compatibility projections, then identify which matching run directories were
created only by the feature branch. Remove only those selectors and run
directories, or revert the feature branch. Existing legacy artifacts remain
untouched, and the stable ignored `.execforge-init-run.lock` remains in place.

## Deferred backlog

`.eng-level/runs/<run-id>/backlog.md` holds work that was planned and deliberately not executed. Deferred
work belongs in a resumable artifact, never only in a commit message or a chat turn.

Each action carries a cycle and a provenance marker:

| Field | Values |
|---|---|
| Cycle | `Now` — ship this cycle · `Boundary` — starts at the cycle edge, user call · `Next` — deferred |
| Provenance | `[C]` consensus · `[R]` resolved disagreement · `[gate]` externally blocked |

Record for every deferred action: what it is, why it was deferred, what unblocks it, and the
measurable condition that would pull it forward.

`--mode=status` reads this file and answers what was parked, why, and what unblocks it.

## Replan triggers

Return to plan when:

- Architecture cannot satisfy a core requirement.
- A new system of record or trust boundary appears.
- Real schema constraints make migration unsafe.
- Performance requires architectural change.
- Consistency, retry, or transaction model is fundamentally wrong.
- Fixes repeatedly fail for the same root cause.
