# Decision — CEO plan bridge changed to both-and (0.12.1)

- **Date approved:** 2026-08-04
- **Approver:** operator (v3x5exia555)
- **Decision:** APPROVE the 0.12.1 edit to the locked CEO plan bridge in
  `skills/execforge/SKILL.md`: the internal CEO Subagent review ALWAYS runs;
  when gstack `plan-ceo-review` is installed it runs IN ADDITION, producing a
  second independent CEO plan artifact, with disagreements routed through the
  orchestrator's contradiction register. The lock pin in
  `tests/test_restored_sections.py` follows the new verbatim text.

## Why this record exists

The edit was made on 2026-07-31 as uncommitted working-tree changes (and
propagated to the installed skill copy) with no lifecycle run, no upstream
approval artifact, and no decision record — only a CHANGELOG claim of
"operator decision". The operator reviewed the diff on 2026-08-04 and gave
explicit approval, which this record captures. Per the lock in `CLAUDE.md`,
edits to these sections require exactly this kind of explicit operator
instruction.

## Also recorded the same day

- Upstream approval for the `cross-repo-rollup` run
  (`20260717T033357818644Z-0c9b96b7`), frozen at the gate since 2026-07-17,
  was granted: `upstream_approval_status: APPROVED`, approved by
  operator (v3x5exia555) at 2026-08-03T23:18:23+00:00, state advanced to
  `PLAN_REQUIRED`.
