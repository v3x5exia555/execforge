# Upstream requirements — answer verdict in client-level, project management folded into existing roles

- Run: 20261106T160037946415Z-0e243f3d-account-manager-verdict
- Source: `plans/20261106_account-manager-skill.md` (execforge verdict MODIFY) and
  `plans/20261106_project-management-skill.md` (execforge verdict MODIFY).
- Operator approval: "proceed account-manager and also project management" (2026-11-06),
  given after the product decision and its options were presented. Read as
  `APPROVE UPSTREAM` for the recommended option on both. If the operator meant a separate
  skill, this run stops and the content moves into its own skill file.

## What, why, for whom

- What: `client-level` answer mode gets a per-answer verdict
  `SAY / DON'T SAY / DON'T COMMIT / ESCALATE`, a new-promise check, an ownership and
  track-record rule, and a status-update shape. The router gets aliases so
  "account manager", "if they ask", "status update", "project management",
  "where are we" land on the right lens. The plan template gets a `Due` line. The
  `manager` role gets the project-management words as routing signals.
- Why: about 15 call-prep prompts had no home in July 2026, and one stakeholder
  status prompt had none either. The authority already lives in `client-level` and
  `eng-level manager`; what is missing is the verdict and the routing words.
- For whom: the operator; the client only sees the cleared sentence.

## In scope / deferred / skipped

- In scope: the items above, one eval case extended, lock tests, docs, two decision
  records.
- Deferred: a separate `account-manager` skill (reopen if the verdict is ignored or
  overruled in a later usage review); a multi-project portfolio view; the CI eval
  window fix in `TODOS.md`.
- Skipped: account tracking, renewals, client health, "deflect smoothly", a new
  `project-management` skill, sprint or Gantt output, time or budget tracking.
- Non-goals: no new bundled skill; no change to locked sections; no version bump or
  changelog (the operator's ship step does those).

## Success metrics

- Every answer-mode output carries one verdict (baseline: none do).
- The extended eval case fails if the partner-platform question is answered with a
  positioning line (baseline: no such check).
- Skill count stays at ten on this branch (baseline: ten).

## Acceptance criteria (binary pass tests)

1. `tests/test_skill_bundle.py` asserts the four verdict words, the ownership rule, the
   new-promise rule, and the status shape in `skills/client-level/SKILL.md`; it fails on
   main and passes on this branch.
2. The same file asserts the aliases `account manager` → `client-level` and
   `project management` → `eng-level`; fails on main, passes here.
3. `python3 scripts/execforge.py validate` passes.
4. `python3 -m unittest discover -s tests` passes, including
   `tests/test_restored_sections.py` unchanged.
5. `evaluations/client-level.eval.md` still parses with `parse_eval_case`, and its
   checklist carries the DON'T SAY expectation on the ownership question.
6. No real client name from the July history appears in the diff (reviewer reads the
   diff for it).

## Initiative flags

- `offensive-security`: not set. `legally-gated`: not set.
  `regulated-impersonation`: not set. `user-prescribed-mechanism`: set — the operator
  asked for "a skill"; the review redirected the mechanism to a verdict inside an
  existing skill and the operator said proceed. Authorization gate: `N-A (justified)` —
  no gating flag is set.

## Non-negotiable CEO decisions

- `DON'T SAY` and `DON'T COMMIT` are required verdict values; the feature is a gate,
  not a spin generator.
- No new skill name.

## Non-negotiable COO controls

- Eval text uses made-up names only.
- Lock test updated, never bypassed; locked sections untouched.
- The new eval content lives inside the existing `client-level.eval.md` so it stays in
  the five-file CI window.
- `sec-level` threat model attached (`.sec-level/threat-model.md`, SEC PASS at plan
  stage).
- Status outputs never compute a date; dates are given by the operator.

## Assumptions and unknowns

- ASSUMPTION: "proceed account-manager" means the recommended option, not a separate
  skill.
- UNKNOWN: whether the GitHub eval secret is set, so whether the eval runs in CI.

## Kill criteria

- Kill at plan stage if the operator says they meant a separate skill or account
  tracking. Sunset the verdict if the operator overrides `DON'T SAY` as a matter of
  course.
