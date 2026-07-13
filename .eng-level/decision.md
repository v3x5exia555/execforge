# Final Engineering Decision — Operating Layer Phase 1

## Eng Level summary

- Initiative: ExecForge Operating Layer Phase 1
- Upstream source: user-approved selective improvement after Citadel comparison
- Upstream approval: APPROVED by user on 2026-07-13
- Mode: full implementation and fallback review
- Branch: `feat/operating-layer-phase-1`
- Base: `feat/v0.9.0-evidence-bridges` at `aa276d09cd1a0dcac701705ac1b3e4bf0225ced4`
- Reviewed HEAD: `bc5b9b077178e492660483f8af196bb88b12d46d`
- Lifecycle state: SHIP_READY (engineering decision only; no merge/deploy performed)
- Plan verdict: APPROVED WITH CONDITIONS
- Staff review: APPROVED after whole-branch review and security-driven delta reviews
- Security review: SEC PASS
- QA: NOT APPLICABLE — local repository CLI/docs; no portal, API, backend, database, queue, or end-to-end service transaction
- Confidence: High for tested POSIX behavior; Windows runtime remains explicitly unverified

## Plan status

Architecture remains a dependency-free local CLI operating layer. It adds
read-only installed/portfolio diagnostics, authoritative initiative selectors,
initiative-scoped Eng/Q artifacts, and deterministic `resume`/`next`. Evidence
precedence, bounded metadata, path containment, approval, Git lineage, frozen
implementation state, rollback, legacy readability, and project-specific rules
remain non-negotiable. Telemetry, hooks, dashboards/fleets, and historical
migration remain non-goals for this phase.

## Implementation conformance

DONE 7; PARTIAL 0; NOT DONE 0; CHANGED 0; SCOPE DRIFT 0; UNVERIFIABLE 0;
NO LONGER NEEDED 0. Detailed evidence is in
`.eng-level/operating-layer-phase-1/conformance.md`.

## Blocking findings

None. All reproduced P1/S1 findings were corrected test-first and independently
delta-reviewed.

## Non-blocking findings

- P2: full run-tree fsync before selector publication, due before claiming
  power-loss-safe or regulated evidence durability.
- P2: versioned strict namespaced-state schemas, due before third-party artifact validation.
- P2: initiative producer bounds, due before external/automated ingestion.
- P2: Windows locking/runtime execution, due before cross-platform verification claims.
- S3: active portfolio child replacement race, due before adversarial concurrent scans.

Owners, rationale, and pull-forward conditions are recorded in `.eng-level/backlog.md`.

## Contradictions resolved

The selective scope, metadata-safety wording, stale-lineage meaning, governance
worktree exemption, and durability guarantee were reconciled against real code
and tests. See `.eng-level/operating-layer-phase-1/contradictions.md`.

## Verification

Fresh final commands after recording the decision artifacts:

```text
python3 scripts/execforge.py validate
python3 -m py_compile scripts/execforge.py scripts/operating_state.py tests/test_repository.py
git diff --check aa276d0..HEAD
git diff --check
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

Results: validation passed; compilation passed; whitespace checks passed; 89
tests ran in 11.830 seconds and passed. Real portfolio smoke returned bounded
findings for missing root instructions, stale branches, and missing frozen
lineage without modifying repositories. External parity `cmp` checks returned 0
for both eligible repositories.

## Final decision

> **Decision: SHIP**

Phase 1 meets every approved acceptance criterion with no unresolved P0/P1 or
S0/S1/S2. The required next action is for the operator to choose branch handling
(local merge, PR, keep, or discard). ExecForge maintainers own the deferred
hardening backlog; re-entry occurs when a recorded pull-forward condition is met.
