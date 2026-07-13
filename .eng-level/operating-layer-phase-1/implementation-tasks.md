# Implementation Tasks — Operating Layer Phase 1

- [ ] **T1 — Add installed and portfolio diagnostics**
  - Why: instruction gaps, skill drift, conflicts, and stale state are currently invisible to `doctor`.
  - Files: `scripts/operating_state.py`, `scripts/execforge.py`, `tests/test_repository.py`
  - Dependencies: approved upstream requirements
  - Verify: focused diagnostic tests and full unit suite pass.
  - Risk: Medium

- [ ] **T2 — Namespace lifecycle state by initiative**
  - Why: singleton root state has become stale and contradictory across projects.
  - Files: `scripts/operating_state.py`, `scripts/execforge.py`, state template/schema, tests
  - Dependencies: T1 finding model and path safety helpers
  - Verify: two rapid `init-run` calls preserve both runs and point to the newest.
  - Risk: Medium

- [ ] **T3 — Add deterministic resume and next commands**
  - Why: both runtimes need the same current-state and next-gate answer.
  - Files: CLI, operating-state module, tests
  - Dependencies: T2 pointers and legacy fallback
  - Verify: conflict, stale state, approval, blocker, stop boundary, and ship-ready scenarios return the specified action.
  - Risk: Medium

- [ ] **T4 — Update contracts and documentation**
  - Why: users and agents must know evidence precedence and compatibility boundaries.
  - Files: README, getting started, Eng Level skill/reference, tests
  - Dependencies: T1–T3 behavior
  - Verify: documentation contract tests, validation, and full suite pass.
  - Risk: Low

- [ ] **T5 — Add instruction parity in clean repositories**
  - Why: Codex currently misses Claude-only root rules.
  - Files: external `AGENTS.md` adapters only
  - Dependencies: T1–T4 verification
  - Verify: byte equality with `CLAUDE.md`; dirty repositories and DPO unchanged.
  - Risk: Low

