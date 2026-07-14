# Security Review — Operating Layer Phase 1

- Base commit: `aa276d09cd1a0dcac701705ac1b3e4bf0225ced4`
- Diff reviewed: `aa276d0..bc5b9b0`
- Threat model: no standalone artifact; plan review recorded trust-boundary controls
- Date: 2026-07-14

## Areas examined

| Area | Examined / Not applicable | Notes |
|---|---|---|
| AI-generated-code hot spots | Examined | User-controlled names/paths/state, terminal rendering, bounded reads, and exceptional paths reviewed. |
| A01 Broken Access Control | Not applicable | Local CLI; no authentication, tenancy, URL fetch, or network boundary. |
| A02 Security Misconfiguration | Examined | No debug, CORS, default credential, cloud, or container changes. |
| A03 Software Supply Chain | Examined | No dependency, lockfile, remote build, or install-time code changes. |
| A04 Cryptographic Failures | Not applicable | No cryptographic or transport surface. |
| A05 Injection | Examined | Subprocesses use argument arrays; revisions are validated; all scoped terminal output is escaped and bounded. |
| A06 Insecure Design | Examined | Portfolio scope, resource bounds, lineage, and fail-closed behavior reviewed. |
| A07 Identification & Authentication | Not applicable | No identity or session surface. |
| A08 Software & Data Integrity | Examined | Selector containment, publication/rollback, approval, Git lineage, and frozen evidence reviewed. |
| A09 Security Logging & Alerting | Not applicable | No service logging surface; diagnostics avoid blocker/state contents. |
| A10 Exceptional Conditions | Examined | Malformed/special/oversized files, concurrency, restore failures, and stale evidence fail closed. |

## Findings

| ID | Severity | File:line | Attack scenario | Required action | Verification |
|---|---|---|---|---|---|
| SEC-01 | S1 — resolved | `scripts/execforge.py` init output | Controlled path characters affect terminal rendering | Escape and bound emitted paths | Controlled-character probe and regression test contain no raw controls |
| SEC-02 | S2 — resolved | selector/backlog readers | Oversized or special local metadata blocks or exhausts a command | Bounded regular-file descriptor reads | Oversized, FIFO, symlink, and no-`O_NOFOLLOW` tests pass |
| SEC-03 | S2 — resolved | portfolio lineage reconciliation | Same-branch stale review evidence appears current | Apply commit/frozen lineage checks | Divergent, invalid, and missing-lineage tests pass |
| SEC-04 | S2 — resolved | portfolio enumeration | Stable direct-child link escapes requested root | Reject links/junctions and require resolved direct-child containment | External target is not dispatched for diagnostics |
| SEC-05 | S3 — owned | path-based portfolio dispatch | Actively replacing a child after the final check can race the scan | Descriptor-anchored design before adversarial concurrent filesystems | Backlog item 9 |

## Verdict

- Verdict: `SEC PASS`
- Unresolved S0/S1: none
- Owned S2/S3: SEC-05 (S3), owner ExecForge maintainers, due before adversarial concurrent portfolio scanning
- Rationale: final focused security checks passed; the full strict suite passed 89 tests; no unresolved merge-blocking security finding remains.
