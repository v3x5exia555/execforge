# Final Engineering Decision — v0.9.0 Evidence Bridges & Executable Evals

Run: eng-level full lifecycle, 2026-07-13. Branch: `feat/v0.9.0-evidence-bridges`.
Base: `feat/v0.8.0-role-architecture` @ `98db516` (locked in plan review).
Upstream: APPROVE UPSTREAM (2026-07-13). Plan review: APPROVED WITH CONDITIONS.

## Verdict: SHIP (committed on branch — push/PR/merge awaits operator go-ahead)

## Conformance to upstream requirements

| Requirement | Status | Evidence |
|---|---|---|
| Executable eval harness (runner + advisory CI) | DONE | `execforge eval` (parse → agent → judge → locally recomputed verdict); `evals.yml` advisory, path-filtered, key-gated, capped; 13 tests in `tests/test_eval_runner.py` |
| Harness catches doc-vs-code drift (KR2) | DONE | First parser run caught the nonconforming two-scenario `eng-level-post-hoc-and-stop.eval.md`; split into two conforming cases |
| gstack bridge: q-level `/browse`+`/qa` | DONE | `skills/q-level/references/tool-routing.md` Portal section; installed-only condition + fallback unchanged |
| gstack bridge: post-SHIP `/land-and-deploy` handoff | DONE | `skills/eng-level/SKILL.md` Final decision rules |
| gstack bridge: sec-level `/cso` runtime evidence | DONE | `skills/sec-level/SKILL.md` lifecycle integration |
| Version gate (manifests ↔ CHANGELOG ↔ tag) | DONE | `execforge release-check`; `release-gate.yml` on tag push; consistency step in `ci.yml`; rejects `v.1.0.0` form (verified in dry run) |
| Hygiene: untrack `__pycache__`/`site/` | NO LONGER NEEDED | `git ls-files` shows both already untracked and gitignored |
| Remove stray `v.1.0.0` tag | DEFERRED (operator) | Exact commands documented in CHANGELOG 0.9.0 entry; COO control requires operator supervision |
| No hard gstack dependency | DONE | All three bridge texts conditional; fallback contracts untouched |
| CHANGELOG/version bump | DONE | 0.9.0 in both manifests + CHANGELOG head; `release-check: consistent` |

## Staff Engineer review

Whole-branch review at medium effort (harness code-review instrument; installed gstack
`review` unavailable). Findings: 0×P0/P1, 2×P3 CONFIRMED (malformed eval file crashed
`--list`; missing CHANGELOG crashed `release_check`), 1×PLAUSIBLE (CI eval agent's
default headless permissions may make artifact-writing behaviors unobservable →
systematic advisory FAILs). The two CONFIRMED items were fixed test-first in the same
cycle; the fix pass also caught and corrected a pass/fail miscount in the summary line.
Delta review of the fix commit: clean.

## QA

`q-level` NOT APPLICABLE: the change is repository CLI tooling, docs, and CI
configuration — no portal, API, or backend service surface. The CLI was driven end to
end (`eval --list`, stubbed eval run with correct FAIL/exit-1, `release-check` both
paths). 35 unit tests pass; `validate` and `doctor` clean.

## Open risks (non-blocking)

- The advisory CI job's real behavior on GitHub is unobserved until the branch is
  pushed with an `ANTHROPIC_API_KEY` secret; by design it cannot block merges
  (`continue-on-error`, key-gated skip).
- PLAUSIBLE permission-noise finding above — evaluate during the advisory period before
  any promotion to a required check (recorded in `.eng-level/backlog.md`).
