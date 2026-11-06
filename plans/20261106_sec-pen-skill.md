# Add a sec-pen skill that drives the Strix pentest tool

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-11-06
- **Last updated:** 2026-11-06
- **Role(s):** sec-level / c-level (router), ponytail lite
- **Branch:** lz-sec-pen-skill
- **Status:** IN PROGRESS (branch pushed, PR open, awaiting review)

## What was asked

The user shared the open-source tool Strix (`github.com/usestrix/strix`) and said:
"add this skill as sec-pen". Strix is an AI penetration-testing tool. It runs a
target app, looks for weak spots, and tries to prove them. The user wants a new
ExecForge skill, named `sec-pen`, that brings Strix into the framework.

## What Strix is, in plain words

- It is a separate program, not part of this repo. It needs Docker (a sandbox
  runner) and a key for a large language model to work.
- You point it at a folder, a web address, or an API description. It writes its
  findings into a folder called `strix_runs/<name>`.
- It is free and open (Apache-2.0 licence). Its own readme says in bold: only test
  systems you own or have written permission to test.
- It sends the target's code or traffic to whatever model provider you set. For a
  paying client that is a data-handling promise, not a detail.

## What `sec-pen` is, and is not

- `sec-pen` is a thin bridge. It does not contain Strix. It tells the agent how to
  use Strix safely when the operator has installed it.
- It never gives the security verdict. `sec-level` (and the lifecycle orchestrator)
  still own `SEC PASS / FIX REQUIRED / BLOCK`. `sec-pen` only produces evidence that
  `sec-level` checks.
- It is inert when Strix is not installed. The agent says so and stops.
- It never runs Strix against any target until a human has recorded an `AUTHORIZED`
  decision for that target, through the existing Authorization gate. The agent never
  marks the work authorized by itself.

## The plan

1. Write a test in `tests/test_skill_bundle.py` that fails until `sec-pen` exists
   and carries its hard rules (authorization gate, "never issues the verdict",
   evidence labels). Watch it fail first.
2. Add the skill `skills/sec-pen/SKILL.md`: three modes — `plan` (confirm
   authorization and that the target is in scope), `run` (prepare the exact Strix
   command for the operator; run only against an owned or written-permission target),
   `triage` (read the `strix_runs` output, drop duplicates, label each item as
   `OBSERVED` / `REPORTED` / `ASSUMED`, and hand it to `sec-level`). No verdict here.
3. Register the skill everywhere a skill must be listed: `BUNDLED_SKILLS` in
   `scripts/execforge.py`, the `.claude-plugin/plugin.json` skills array, an
   evaluation case `evaluations/sec-pen.eval.md`, a doc page `docs/sec-pen.md` and the
   `mkdocs.yml` nav, a README row and an actor-parameter row, and a `c-level` router
   row plus trigger aliases ("pentest it", "run strix").
4. Run the test again (must pass), then the whole test folder, `validate`, and
   `doctor`.
5. Show the diff. Commit after the user's yes. Do not cut a release unless asked.

The lazier version, named for the user: skip the new skill and add Strix as two
lines inside `sec-level`. We chose a separate skill because the user asked for one by
name, and because a tool that runs attacks needs its own authorization-gated home,
not a footnote in the code-reading skill.

## Risks

### Risk A — Strix runs against a target that was never authorized

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` |
| **What actually happens?** | An attack tool runs on a system with no written permission. That can breach a contract or a law, harm a third party, and end a client relationship. |
| **Short or long term?** | `LONG` — the risk lives for as long as the skill exists. |
| **Solution** | The skill makes an `AUTHORIZED` record a hard gate before any run, reuses the existing Authorization gate, and states the agent never self-authorizes. The `run` mode refuses without an in-scope target and a recorded decision. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | Words in a skill cannot force a human. An operator can still run Strix by hand outside the skill. The gate lowers the chance; it does not remove it. |
| **Cost** | Build: under a day. Money: none in this repo. Upkeep: one test holds the gate wording; the operator owns the real authorization paperwork. |
| **What we expect after** | No `sec-pen` run starts without a recorded `AUTHORIZED` decision and an in-scope target, and the decision file shows it. |
| **Does a human need training?** | `YES` — the operator must know that `AUTHORIZED` is their decision, what written scope means, and that running Strix by hand skips the gate. |

### Risk B — Client code or traffic goes to a model provider the client never agreed to

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` |
| **What actually happens?** | Strix sends the target's code and traffic to the configured model provider. If the client never agreed, that is a data-handling breach and a trust loss. |
| **Short or long term?** | `LONG` |
| **Solution** | The skill requires the provider and the data path to be named in the authorization record for client work, and points at `client-level`'s rule against leaking one engagement's content into another. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | The record can be filled in loosely. The skill cannot read the client contract. |
| **Cost** | not measured |
| **What we expect after** | Every client `sec-pen` run names its model provider and data path in the authorization record before it starts. |
| **Does a human need training?** | `YES` — the operator must check the client contract allows the chosen provider before running. |

### Risk C — A false finding from Strix reaches a client as fact

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | AI pentest tools report things that are not real. If one passes straight into a client report, the client acts on a wrong finding and loses trust when it is disproved. |
| **Short or long term?** | `LONG` |
| **Solution** | `sec-pen` never issues the verdict. Its output is `OBSERVED` evidence that `sec-level` re-verifies, and `client-level` translates only after that. The skill says the severity stays `sec-level`'s call. |
| **What would the solution fix?** | manual work |
| **Risk of the solution itself** | The re-verify step adds work. If skipped under time pressure, the guard is gone. |
| **Cost** | not measured |
| **What we expect after** | No Strix finding reaches a client report without a `sec-level` re-verification recorded against it. |
| **Does a human need training?** | `NO` — the lifecycle already carries the verify step. |

### Risk D — The skill rots because Strix changes upstream

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | Strix is not pinned inside this repo. Its commands or output folder can change, and the skill's instructions go stale. The agent runs a command that no longer works. |
| **Short or long term?** | `LONG` |
| **Solution** | The skill names the install source and the commands it was written against, and tells the agent to read Strix's own current help if a command fails, rather than trusting the skill text. |
| **What would the solution fix?** | none of these |
| **Risk of the solution itself** | A pointer to "read the current help" is weaker than a pinned version, but this repo cannot vendor a Docker tool the way it vendored ponytail. |
| **Cost** | Upkeep: re-read Strix's readme at each pilot review. `not measured`. |
| **What we expect after** | When a Strix command fails, the agent checks the tool's current help instead of repeating a stale command. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-11-06 | A separate `sec-pen` skill, not two lines in `sec-level` | The user asked for a named skill, and attack tooling needs its own authorization-gated home. |
| 2026-11-06 | Bridge only; Strix installed separately | This repo cannot vendor a Docker + model-key tool. Same pattern as the gstack and Superpowers bridges. |
| 2026-11-06 | Verdict stays with `sec-level` | One owner for the security decision. `sec-pen` makes evidence, not calls. |
| 2026-11-06 | Feature now, release later | The repo cuts releases in their own commit. Ask before tagging. |

## What happened

- 2026-11-06 — Plan written. Work started.
- 2026-11-06 — Test written first and seen to fail. Then added the skill
  `skills/sec-pen/SKILL.md` (144 lines), the eval case, the doc page and nav, the
  README rows, the c-level router row and aliases, and registered the skill in
  `BUNDLED_SKILLS` and the Claude manifest. Install verification caught that a
  `../../docs/` link breaks once a skill is copied on its own, so the gate links now
  use the full GitHub URL, matching the authorization-gate doc's own cross-links.
  All 110 tests pass; `validate` and `doctor` pass.

## Still unclear

- Which model providers the operator's client contracts allow. That gates real
  client use and is the operator's call, recorded per engagement.
- Whether this is a formal ExecForge PILOT with kill triggers (like ponytail) or a
  plain add. Treating it as a plain add for now; say if you want the pilot record.

## Result

Eleventh bundled skill `sec-pen` added on branch `lz-sec-pen-skill`. Proof:
`tests/test_skill_bundle.py::test_sec_pen_skill_is_bundled_and_gated` fails without the
skill and its gates and passes with them; full suite 110 green; `validate` and `doctor`
pass. Not released. Installed copy in `~/.claude/skills` refreshes after merge. Known
gap carried from TODOS.md: the CI eval job runs only the first few sorted eval cases, so
`sec-pen.eval.md` may not execute in CI until that P1 is fixed.
