# Plan Engineering Review — v0.9.0 Evidence Bridges & Executable Evals

Date: 2026-07-13 · Reviewer: staff-engineer lens (fallback review contract — installed
gstack `plan-eng-review` not available in this session)
Plan: `plans/20260713_192500_v0.9.0-evidence-bridges.md`
Upstream: `.eng-level/upstream-requirements.md` (APPROVE UPSTREAM, 2026-07-13)

## Locks

- Base branch: `feat/v0.8.0-role-architecture` @ `98db516` (merge base with `main`: `fe4aeb8`)
- Approved scope: Tasks 1–7 of the plan; deferred/skipped items recorded in the plan's
  "Out of scope" section.

## Review against the required surface

- **Existing patterns and reuse** — All runtime code extends `scripts/execforge.py`
  (single-script, stdlib-only convention); `parse_eval_case` reuses `parse_frontmatter`;
  tests mirror `tests/test_repository.py`'s importlib pattern. No new dependencies. PASS.
- **Architecture / data flow** — case file → scenario → headless agent → transcript →
  judge → locally recomputed verdict. Judge pass-claims are never trusted (recompute in
  `parse_verdict`), which keeps the grader from being an oracle. PASS.
- **Failure paths** — missing sections raise `ValueError`; judge garbage raises;
  timeouts caught in `cmd_eval`; CI job is `continue-on-error` and skips without a
  secret. PASS.
- **Security / trust boundaries** — new CI secret (`ANTHROPIC_API_KEY`) used only in the
  advisory job, gated so fork PRs skip; no secret ever written to the repo. The eval
  agent replays repo-authored scenario text only. Light sec-level note: keep the key
  spend-capped (COO control). PASS with note.
- **Performance / cost** — capped (`--limit 4`, `--max-turns`), path-filtered. PASS.
- **Rollback** — per-file revert; deleting two workflow files kills the harness. PASS.
- **Tests / definition of done** — each task carries failing-test-first steps; upstream
  acceptance criteria map to Task 3 step 5 (local run), Task 5 (CI), Task 4 step 4
  (version-gate dry run), Task 6 step 4 (bridge diffs + validate). PASS.
- **Exact tasks and files** — all seven tasks name exact paths and code. PASS.

## Conditions

1. Task 5 must verify the real `execforge.py install` CLI flags before writing the
   workflow (the plan instructs this explicitly).
2. The evals CI job stays advisory; promotion to a required check is a separate recorded
   decision (upstream control).

## Verdict

**APPROVED WITH CONDITIONS** (the two conditions above).
