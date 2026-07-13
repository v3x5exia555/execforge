# Contradictions and Resolutions — Operating Layer Phase 1

| Claim or tension | Evidence | Resolution |
|---|---|---|
| Citadel-like breadth versus the operator's immediate need | No measured need for a daemon, dashboard, fleet, or telemetry control plane | Selective ExecForge operating-layer improvements only; broader control-plane work deferred. |
| “Privacy contract” could imply semantic redaction | Displayed initiative/branch/path metadata can itself contain sensitive meaning | Contract renamed to bounded, allowlisted, terminal-safe metadata output; semantic secret/PII redaction is explicitly not promised. |
| Portfolio “stale” could mean branch-only or full lineage | Approved scope used stale state broadly; `resume`/`next` already enforced commit lineage | Portfolio now checks branch, reachable commits, and frozen implementation lineage. |
| Governance artifacts make worktrees dirty, while frozen implementation evidence must be stable | Blanket cleanliness would block normal state updates; source changes invalidate reviewed code | Frozen states ignore only reserved governance namespaces and the stable lock, while tracked/untracked non-governance changes fail closed. |
| Atomic selector replacement versus power-loss durability | Pointer replacement is fsynced; referenced run trees are not fully fsynced | Phase 1 claims process-failure consistency, not power-loss-safe transactions; stronger durability is deferred with a pull-forward condition. |
