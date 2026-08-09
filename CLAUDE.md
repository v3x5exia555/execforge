# Agent Instructions

At the start of work, load `c-level` when there is any reasonable chance the task concerns product scope, engineering planning, implementation, code review, or release readiness.

Priority:

1. Direct user instructions
2. `c-level`
3. Selected ExecForge skill
4. Selected Superpowers process skill, when installed
5. Domain-specific implementation skill, including `ponytail` (vendored, pinned; see `skills/ponytail/PROVENANCE.md`)

Where ponytail and Superpowers `test-driven-development` conflict, TDD wins; ponytail governs implementation style, never test discipline.

Never claim an upstream review, implementation, test, or final gate ran unless evidence shows it actually ran.

## Plan tracking

Whenever a prompt runs an ExecForge role (`c-level`, `execforge`, `eng-level`, `q-level`, `sec-level`, `design-html`, `full-cycle`, CEO/COO review), keep a plan file under `plans/`:

- New task: create `plans/YYYY-MM-DD_HH-MM-SS-ss_<title>.md` from `plans/TEMPLATE.md`, and write the plan before starting the work. `ss` is hundredths of a second. Get the stamp with:

  ```bash
  python3 -c "from datetime import datetime as d; n=d.now(); print(n.strftime('%Y-%m-%d_%H-%M-%S-')+f'{n.microsecond//10000:02d}')"
  ```

  Use dashes in the time, never colons. A colon is illegal in a Windows filename, and one committed here makes `git clone` fail outright on Windows — which this repo supports (`scripts/execforge.py` has a Windows file-locking backend).
- Continuing an earlier task: update that same file. Do not open a second file for the same task.
- No role involved: no plan file.

Write every plan file in plain, simple English: short everyday words, short sentences, no jargon. If a technical word cannot be avoided, say what it means in a few words. Someone who does not know this codebase should still be able to follow it.

The `UserPromptSubmit` hook in `.claude/settings.json` is the reminder for this rule.

## Risk framework in every plan

Every plan file carries a `## Risks` section. One block per risk, named `Risk A`, `Risk B`, and so on. Each block answers nine questions:

| Question | Notes |
|---|---|
| **How bad?** | `HIGH` / `MEDIUM` / `LOW` |
| **What actually happens?** | The real impact, not the label — who is hurt and how |
| **Short or long term?** | `SHORT` passes on its own; `LONG` is structural and stays |
| **Solution** | `none yet` is an honest answer |
| **What would the solution fix?** | Only what genuinely applies: operational load / manual work / automation / compliance. `none of these` is allowed |
| **Risk of the solution itself** | Every fix brings its own risk. "None" is almost always wrong |
| **Cost** | Build time, money, and ongoing upkeep |
| **What we expect after** | What should be true once it is in place — this is what gets checked later |
| **Does a human need training?** | If `YES`, say who must learn what. That is a hidden cost |

Never invent a cost or a number; write `not measured`. If there is genuinely no risk, write `No risks identified` and say why — an empty section is not a considered one.

The shape lives in `plans/TEMPLATE.md`. This is a **plan-time** register and is separate from the fix-time analysis below; a plan gets this, a fix gets that, and work that is both gets both.

## Risk analysis on every fix

Whenever a bug or failure is fixed, the report on that fix carries a short risk analysis. Four parts, one or two sentences each:

| Part | What it answers |
|---|---|
| **Blast radius** | What else can this change affect? |
| **Not fixed** | What does it leave unsolved, and what related case does it not cover? |
| **Detection** | What would catch it if it regresses — the specific test, gate, or CI job? If nothing would, say so plainly. |
| **Rollback** | How is it undone? |

State the root cause as proven evidence, or say plainly that it is a hypothesis. "Probably line endings" and "confirmed: the CRLF hash matches byte for byte" are different claims and must not be written the same way.

A fix reported without this is not finished.

LOCKED (operator decision 2026-07-31): the restored CEO Subagent, COO Subagent, CEO plan (gstack `plan-ceo-review` bridge), Phase 5 Scope Ledger, Phase 8 Product Definition and OKRs, and A-C-T-I-O-N Operational Matrix sections in `skills/execforge/`, and the OKR trigger aliases in `skills/c-level/SKILL.md`, must never be edited, condensed, or removed without explicit operator instruction. `tests/test_restored_sections.py` enforces this lock.
