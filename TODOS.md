# TODOS

## Evaluations

### Make the CI eval run pick the cases for changed skills

**What:** Change eval selection so the behavioral-evals CI job runs the eval cases for
the skills a push actually changed, instead of the first N case files by name
(`--limit` over a sorted list; currently 5 after the 2026-10-15 stopgap).

**Why:** Today a new eval case can be unreachable: `ux-level-spec-review.eval.md`
sorts 16th of 17, so CI never runs it, and adding `client-level.eval.md` (sorts 2nd)
silently pushed `eng-level-post-hoc-review.eval.md` out of the window. A gate that
exists on paper but never runs is the failure this repo's own rules name.

**Context:** Deferred by recorded operator decision during the 2026-10-15 ship of the
client-level skill and ux-level spec mode (see
`plans/20260930_ux-level-spec-review.md`, "Honest note on the eval"). The selection
lives in `scripts/execforge.py` `cmd_eval` (sorted glob, then `cases[:limit]`) and
`.github/workflows/evals.yml` (`--limit 5`). A `--skill <name>` filter on `cmd_eval`
plus a changed-paths step in the workflow is one shape; a rotation or a raised cap
are others. Whatever lands, add a reachability check so a new case cannot fall out
of the window silently again.

**Effort:** M
**Priority:** P1
**Depends on:** None

Stopgap already in place (2026-10-15): the CI cap was raised from 4 to 5 so adding
`client-level.eval.md` does not push `eng-level-post-hoc-review.eval.md` out of the
window. The spec-mode eval still does not run in CI until this item lands.

### Join wrapped checklist lines in the eval parser

**What:** Make `parse_eval_case` in `scripts/execforge.py` join a checkbox item's
continuation lines, so a judge sees the whole requirement, not just its first line.

**Why:** Proven during the 2026-10-15 ship: a wrapped `- [ ]` item was cut mid-sentence
("…a concrete") before reaching the judge. The two new eval files were reformatted to
one line per item as a workaround; every older eval file with wrapped items is still
affected.

**Context:** The parser keeps only the checkbox's first physical line. Fix in
`parse_eval_case`, add a unit test with a wrapped item, then the one-line workaround
becomes optional style.

**Effort:** S
**Priority:** P2
**Depends on:** None

### Guard the prompt hook with an integrity test

**What:** A small unit test that parses `.claude/settings.json`, checks the
UserPromptSubmit hook is a plain `echo` of valid JSON, and maps `.claude/**` to it in
`.gstack/pregate.json`.

**Why:** The hook is a shell command that runs on every prompt. Today an edit to it
reaches CI with no check at all; this cycle's edit was verified by hand.

**Context:** Suggested by the 2026-10-15 ship's security verification pass. Home:
`tests/test_repository.py`.

**Effort:** S
**Priority:** P2
**Depends on:** None

## Completed
