# Upstream Requirements — Evidence Bridges & Executable Evals (v0.9.0 candidate)

Source: `.execforge/decision.md` (GO WITH CONDITIONS, 2026-07-13)
Status: UPSTREAM_APPROVAL_REQUIRED — awaiting operator response

## What / why / for whom

Execute the bundled skills' behavioral evals in CI and bridge q-level / eng-level ship /
sec-level to installed gstack tooling, so ExecForge's verdicts are backed by executed
evidence. For the operator governing real client portals (DataRex, security-awareness
platform, portal-template, hotel-webscrap) where gstack is already in use.

## In scope

1. **Executable eval harness** — a runner (extend `scripts/execforge.py` or a sibling
   script) that executes `evaluations/*.eval.md` cases against a headless agent and
   asserts the required behaviors; plus an advisory CI job triggered only by changes to
   `skills/**` or `evaluations/**`, model and case-count capped.
2. **gstack bridge routing (docs-only)** —
   - `skills/q-level/references/tool-routing.md`: prefer gstack `/browse` + `/qa` for
     portal evidence when installed; fallback unchanged.
   - `skills/eng-level` (SKILL.md or lifecycle-protocol.md): post-SHIP handoff note to
     gstack `/land-and-deploy` when installed.
   - `skills/sec-level`: list gstack `/cso` as an optional runtime-evidence tool.
3. **Version gate** — CI check that a release tag matches the CHANGELOG head entry;
   one-time cleanup of the `v.1.0.0` typo tag (operator-supervised).
4. **Hygiene** — gitignore and untrack `__pycache__/` and `site/`.

## Deferred / skipped / non-goals

- DEFER: retro/learn skill; cross-project decision search.
- SKIP: rebuilding gstack runtime tooling (browser daemon, deploy scripts, analytics).
- Non-goals: no hard gstack dependency; no new runtime service or data store; no
  unconditional CI cost growth (eval job is path-filtered and capped).

## Product success metrics

- KR1: every bundled skill has ≥1 eval executed in CI on skill-file changes (baseline 0).
- KR2: harness catches a seeded doc-vs-code drift in a dry run.
- KR3: one governed QA run on DataRex UAT yields browser-driven evidence via the bridge.
- KR4: CI eval spend within cap; zero flake-blocks during the advisory period.

## Acceptance criteria (definition of done)

- `python3 scripts/execforge.py eval <case>` (or equivalent) runs a real eval case
  locally and reports pass/fail per required behavior.
- CI shows the advisory eval job green on a skill-touching PR and skipped on a
  docs-only PR.
- Version-gate job fails a deliberately mismatched tag/CHANGELOG pair in a dry run.
- The three bridge texts name gstack skills, state the installed-only condition, and
  leave fallback contracts unchanged (verified by reading the diffs).
- `git status` shows no tracked `__pycache__`/`site` files; CHANGELOG and version bumped
  per repo convention.

## Initiative flags and authorization status

`offensive-security` NOT SET · `legally-gated` NOT SET · `regulated-impersonation`
NOT SET · `user-prescribed-mechanism` NOT SET. Authorization gate: N-A (justified — no
gating flag set).

## Non-negotiable CEO decisions

- Bridges are conditional; zero-dependency install story is preserved.
- No rebuild of gstack capabilities.

## Non-negotiable COO controls

- Eval CI job lands advisory; promotion to required is a separate recorded decision.
- `ANTHROPIC_API_KEY` repo secret is least-privilege and spend-capped; never committed.
- Remote tag cleanup happens once, operator-supervised.

## Assumptions / unknowns

- Assumption: a headless agent invocation (e.g. `claude -p`) is available in CI with the
  repo secret; to confirm in Stage 3 plan.
- Assumption: `feat/v0.8.0-role-architecture` merges before or under v0.9.0 work.
- Unknown: exact eval assertion format (grep-style required phrases vs structured
  rubric) — Stage 3 plan decision.
- Unknown: whether the eval runner lives in `execforge.py` or a sibling script —
  Stage 3 plan decision.

## Kill criteria

- Harness flakes >2×/week in advisory period → keep runner local-only, drop CI job.
- Bridge text confuses agents in dry runs → revert to fallback-only text.
