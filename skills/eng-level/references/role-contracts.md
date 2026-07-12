# Role Contracts

Roles are lenses, not lifecycle stages. The lifecycle supplies the stages; roles attach to
them. The same role performs a different function at different stages.

## Stage-to-role map

| Stage | Roles attached | Execution |
|---|---|---|
| Plan | `architect` and `manager` always; `backend-engineer` and `platform-engineer` as advisors when the change touches their surface | Parallel, then reconciled. Pair a `purist` when integrity-critical. |
| Implement | `backend-engineer` and `platform-engineer` — building, not reviewing | Sequential, in the plan's action order |
| Review | `staff-engineer` always; `backend-engineer` and `platform-engineer` re-attach as auditors of their own surface | Parallel; `staff-engineer` merges |
| QA | `q-level` | Per the Q Level bridge |
| Ship | Orchestrator only | Single verdict |

`backend-engineer` and `platform-engineer` therefore appear three times each: advising at
plan, building at implement, auditing at review.

## Defaults

```text
--mode=plan    with no role → architect + manager
--mode=review  with no role → staff-engineer
--role=<r>                  → that lens only
--role=auto    (default)    → see role-routing.md
```

Existing invocations without `--role` behave exactly as before.

## Per-role contracts

### architect

Owns system and data design, trade-offs, capacity and cost sizing, scale ceilings, and the
order in which things fail.

- Must state the failure order, not just the failure set.
- Must state a flip condition for any deferral: the measurable threshold at which the
  deferred work becomes this-cycle work.
- Must label a capacity claim `UNKNOWN` unless it was measured.
- Verdict: `SOUND` / `SOUND WITH CONDITIONS` / `REDESIGN` / `UNVERIFIABLE`.
- May not rule on diff conformance.

### manager

Owns decomposition, sequencing, dependencies, and acceptance criteria.

- Every ticket carries a binary pass test. A ticket without one is not ready.
- Verdict: `PLAN READY` / `PLAN INCOMPLETE`.
- `PLAN READY` is unavailable while any ticket lacks a pass test. List the missing ones.
- May not rule on architecture soundness.

### staff-engineer

Owns whole-branch diff review and plan-to-code conformance. Existing behavior, unchanged.

- Requires a real diff and a known base commit.
- Severity `P0`–`P3`; conformance status per requirement and task.
- Merges specialist findings from `backend-engineer` and `platform-engineer`.
- Runtime behavior and actual code outrank plan intent.

### backend-engineer

Owns schema, queries, indexes, migrations, API contracts, idempotency, and data integrity.

- Must check that predicates are sargable and that declared indexes are actually usable.
- Must check that the schema owns its invariants rather than relying on read-time repair.
- Must check migration reversibility and identify constraints that cannot be dropped in
  place.
- Returns findings. Does not issue a ship verdict.

### platform-engineer

Owns deploy topology, containers, reverse proxy, DNS, TLS, email authentication, secrets
placement, rollback, and runbook.

- Must validate configuration syntax before it reaches an environment, not after.
- Must check field-length and encoding limits on externally hosted records (DNS values are
  a recurring truncation hazard).
- Must check file ownership and writability of mounted volumes and copied artifacts.
- Must check that a setting applies unconditionally when it is required unconditionally.
- Must state the rollback for every change to a running environment.
- Returns findings. Does not issue a ship verdict.

## Authority

Only the orchestrator issues `SHIP`, `SHIP WITH REQUIRED FIXES`, `RETURN TO
IMPLEMENTATION`, `RETURN TO PLAN`, or `BLOCK`. Roles produce findings and role-scoped
verdicts. No role self-certifies.

Read [subagent dispatch](subagent-dispatch.md) for how roles are dispatched and how their
disagreements are resolved.
