# Functional QA Report: ExecForge CLI (ship smoke, branch lz-client-level-and-spec-mode)

| Field | Value |
|---|---|
| Date / branch / revision | 2026-10-15 / lz-client-level-and-spec-mode / HEAD 4848419 + uncommitted working tree (wtree 1e296f4e501c) |
| Caller / authority / depth | ship; writes only to .gstack/qa-reports/ship-smoke-20261015; bounded smoke 300s / 12 probes |
| Surfaces / scope | Functional (CLI): scripts/execforge.py install and eval list; changed surfaces are the new client-level skill registration and two new eval case files |
| Runtime / native tools | python3 (3.14 per homebrew path), repository-native commands only |
| Fixture ownership / destinations | Isolated: install destination .gstack/qa-reports/ship-smoke-20261015/tmp-skills (owned, throwaway); no external stores |
| Probe budget / guarded command time / stop reason | 300s/12 probes configured / 128ms used over 2 captures / stopped: scoped contracts tested |

## Contract outcomes

| Contract and source | Exact probe / evidence | Expected → observed | Outcome |
|---|---|---|---|
| Install copies and verifies every bundled skill (README usage; plan step 4) | `python3 scripts/execforge.py install --dest .gstack/qa-reports/ship-smoke-20261015/tmp-skills`; .qa-evidence/001 | exit 0 and 10 skill dirs on disk including client-level → exit 0; 10 dirs present, client-level among them | pass |
| Eval runner parses every evaluations/*.eval.md (tests/test_eval_runner.py contract; riskiest changed edge) | `python3 scripts/execforge.py eval --list`; .qa-evidence/002 | exit 0 and 17 case ids including the two new ones → exit 0; both `client-level-honest-answer-no-invented-numbers` and `ux-level-spec-mode-incomplete-spec` listed | pass |
| Repo validator passes (plan step 7 / rollout step 5) | `python3 scripts/execforge.py validate`; gstack-evidence receipt label=validate, exit 0, this invocation | "ExecForge validation passed." → same | pass |
| Full unit suite passes (plan step 7; CONTRIBUTING.md:15) | `python3 -m unittest discover -s tests -v`; gstack-evidence receipts from this invocation — first run "Ran 104 tests … OK", rerun after the ship's review fixes added 4 tests: "Ran 108 tests … OK" (capture 005 below) | all green → 108 ran, OK | pass |
| Behavioral eval run (rollout step 5) | not run | deferred to advisory CI by recorded operator decision (ship Step 6, option B) | not run (accepted, recorded decision) |

## Findings

No reproduced product defects and no setup blockers in the probed scope.

## Discoveries and permanent tests

- [checkpoint 002](exploration-002.json) — install success with client-level present shifted the risk question to whether the new eval files parse; the next probe listed eval cases and both new ids appeared.

| Hypothesis / discovery | Native test or proposed case | Red evidence before repair | Green + original + adjacent evidence | Parent disposition |
|---|---|---|---|---|
| New eval files might not match the parser's frontmatter contract | Already covered: tests/test_eval_runner.py parses every evaluations/*.eval.md | n/a (healthy contract) | capture 002 exit 0 with both ids listed; unit receipt 104/OK | no new test needed |

## Coverage limits and cleanup

- Not probed: doctor, status, sessions, release-check subcommands (unchanged by this branch; covered by the unit suite receipts). release-check is expected to report a pending version until the ship's bump step runs.
- Behavioral eval execution deferred to advisory CI by recorded operator decision; not counted as a pass.
- Cleanup: tmp-skills install directories are retained **locally only** inside the
  owned report folder; this branch's `.gitignore` excludes them from the repo, so a
  reader of the clone gets the captured outputs, not the tree copies.
- Revalidation history: the ship's review cycles changed skill files and added four
  tests after the first captures. Captures 003–005 re-ran install, eval listing, and
  the full suite on the fixed content (108 tests, OK). Earlier captures 001–002 are
  kept as history of the pre-fix content.
