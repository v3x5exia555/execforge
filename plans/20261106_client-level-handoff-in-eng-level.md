# Tell eng-level to hand off to client-level

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-11-06
- **Last updated:** 2026-11-06
- **Role(s):** c-level (router), ponytail lite fast path
- **Branch:** lz-client-level-handoff-in-eng-level
- **Status:** DONE

## What was asked

The user asked: "please help me add into this skill into the eng-level now".
"This skill" is `client-level`, the skill that turns engineering work into words a
paying client can read. Today `eng-level` (the engineering review skill) does not
mention it at all. After `eng-level` gives its final verdict, nothing tells it to
hand the result to `client-level` when a client will read it.

## The plan

1. Write a test that fails because `eng-level` does not mention `client-level`.
2. Add one rule to `eng-level`: after the final decision, if a client will read the
   result, run `client-level` next and write that handoff in the decision file.
   `eng-level` keeps its verdict. `client-level` only translates it. It never
   changes a finding's severity.
3. Add one line to the final output contract (the fixed list of sections every
   eng-level report must have) so the handoff is recorded in the same place as the
   gstack deploy handoff.
4. Add one line to the user docs for `eng-level`.
5. Run the test again. It must pass. Run the whole test folder too.
6. Show the diff to the user. Do not commit until the user says yes.

The lazier option, named for the user: only the one rule in `eng-level/SKILL.md`,
no test, no docs. We chose the fuller version because every other wiring in this
repo is locked by a test, and an unlocked rule can be lost in a later edit.

## Risks

### Risk A — Noise on internal-only projects

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | On a project with no client, the agent may still nudge "run client-level next". The operator reads one extra line and ignores it. No one else is hurt. |
| **Short or long term?** | `LONG` — the rule stays in the lifecycle. |
| **Solution** | The rule is conditional: it fires only "when a client will read the result". The default when no client is named is to skip. |
| **What would the solution fix?** | none of these |
| **Risk of the solution itself** | The agent may misjudge whether a client exists and skip the handoff when it was needed. The operator can still invoke `client-level` by hand. |
| **Cost** | Build: minutes. Money: none. Upkeep: the one test keeps the rule in place. |
| **What we expect after** | Internal runs end as before. Client runs end with a named handoff in the decision file. |
| **Does a human need training?** | `NO` |

### Risk B — Client-level is read as a new gate that can block SHIP

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | If the wording is loose, a future reader could think a `FIX REQUIRED` from `client-level` (a wording problem in a report) blocks an engineering `SHIP`. Releases stall on wording. |
| **Short or long term?** | `LONG` |
| **Solution** | Write the rule so it is plain: the handoff happens after the verdict, it never changes the verdict, and it never re-grades a finding. |
| **What would the solution fix?** | none of these |
| **Risk of the solution itself** | A one-line rule may be too short to stop every misreading. The `client-level` skill's own Boundaries section says the same thing, so two places agree. |
| **Cost** | not measured |
| **What we expect after** | `eng-level` verdict rules are unchanged. The test for them still passes. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-11-06 | Handoff rule, not a new stage | The user asked to add the skill in. A new stage would slow every run and touch state files and tests for no gain. A rule after the verdict is the smallest change that does the job. |
| 2026-11-06 | Lock it with a test | Every other skill wiring here has one. |
| 2026-11-06 | No changelog entry now | The repo adds changelog lines at release time in one "bump version and changelog" commit. |

## What happened

- 2026-11-06 — Plan written. Work started.
- 2026-11-06 — Test written first and seen to fail. Then the rule was added to
  `skills/eng-level/SKILL.md` (version 0.8.1 to 0.8.2), one line to the final output
  contract, and one short section to `docs/eng-level.md`. All 109 tests pass.
  `execforge.py validate` and `doctor` pass. Diff shown to the user. User said yes. Committed and pushed; PR opened.

## Still unclear

- None.

## Result

Four files changed, 21 lines added, 1 changed. Proof: `tests/test_skill_bundle.py`
test `test_eng_level_hands_off_to_client_level` fails on the old text and passes on
the new. Committed after the user's yes; see the PR for the commit. The installed copy in
`~/.claude/skills/eng-level` was refreshed from the repo.
