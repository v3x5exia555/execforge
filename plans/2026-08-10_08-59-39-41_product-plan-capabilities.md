# Add four working methods to the product plan, and put the plan into the lifecycle

> Write this file in plain, simple English. Short everyday words. Short sentences.

- **Started:** 2026-08-10
- **Last updated:** 2026-08-10
- **Role(s):** execforge (product plan change), full-cycle (lifecycle change)
- **Branch:** lz-plan-capabilities, cut from `main`
- **Status:** DONE (PR open)

## What was asked

The user asked whether the product plan covers four things: strategic roadmapping,
a prioritization framework, evidence synthesis, and scope & dependency management.
The answer was: one fully (evidence), two half-way, one missing. Then the user said:
"add this into the product plan and also include this product plan into the lifecycle."

Plain meaning:

1. Add those four working methods to `docs/product-plan.md`.
2. Make the lifecycle (the `full-cycle` skill) actually use the product plan,
   so it is a living document, not a page nobody reads.

## The plan

1. Write this plan file first.
2. Add four sections to `docs/product-plan.md`:
   - **How this plan reads evidence** — write down the rules the plan already
     follows (only measured numbers, facts kept apart from guesses).
   - **How work gets picked** — the ADD NOW / DEFER / SKIP ledger, plus a
     simple ordering rule for what goes first.
   - **Strategic roadmap** — take the flat list in `docs/roadmap.md` and say,
     for each item: which key result it serves, who is better off, and what
     blocks it. Items that only help "other people" wait behind the open
     question (who is ExecForge for).
   - **Scope and dependencies** — how scope changes are decided and recorded,
     and the named things that block other things.
3. Point `docs/roadmap.md` at that new strategic view (one line).
4. Change `skills/full-cycle/SKILL.md`: Stage 0 must check the product plan.
   Every new initiative must say which objective or key result it serves, or
   say plainly that it serves none. If a decision changes the plan (who it is
   for, what it is, a key result), the plan is updated in the same cycle.
5. Record this change as a decision in `docs/decisions/` — the plan's own
   key result 1 says skill changes must carry a recorded decision.
6. Bump version to 0.16.0, update the changelog, run the tests, open a PR.

## Risks

### Risk A — The roadmap table goes stale

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | `docs/roadmap.md` changes later but the mapping table in the product plan does not. The two disagree, and a reader trusts the wrong one. |
| **Short or long term?** | `LONG` — it stays until something keeps them in step. |
| **Solution** | A one-line pointer in `roadmap.md` telling editors the strategic view lives in the product plan. No automation yet. |
| **What would the solution fix?** | Manual work (a reminder, not a guarantee). |
| **Risk of the solution itself** | A pointer can be ignored. It gives false comfort that the two files stay in step. |
| **Cost** | Minutes to add. Upkeep: `not measured`. |
| **What we expect after** | Anyone editing the roadmap sees the pointer and updates both files, or at least knows they exist. |
| **Does a human need training?** | `NO` — the pointer is the instruction. |

### Risk B — The lifecycle gains ceremony

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | Every future cycle must now answer "which key result does this serve?". If that turns into pages of text, cycles get slower and people start skipping the gate — the exact failure ExecForge exists to stop. |
| **Short or long term?** | `LONG` — it is a permanent rule in the lifecycle. |
| **Solution** | Cap it: the answer is one sentence, and "serves none" is an allowed answer that flags the decision rather than blocking it. |
| **What would the solution fix?** | Operational load. |
| **Risk of the solution itself** | "One sentence" can become an empty ritual — people write a sentence without thinking. The gatekeeper still has to read it. |
| **Cost** | One sentence per cycle. Upkeep: `not measured`. |
| **What we expect after** | Stage 0 decisions name the key result they serve, and drift from the plan is visible instead of silent. |
| **Does a human need training?** | `YES` — anyone running `full-cycle` must know the product plan exists and what its key results are. Reading it takes minutes. |

### Risk C — The "who benefits" column is judgment, not measurement

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | The new roadmap table says who each item helps. That is my judgment, not a measured fact. If a judgment is wrong, an item may wait behind the open question when it should not, or jump the queue. |
| **Short or long term?** | `SHORT` — each entry is corrected the moment the operator disagrees; nothing structural. |
| **Solution** | Label the column as judgment in the document itself, so nobody mistakes it for data. |
| **What would the solution fix?** | None of these — it is honesty, not a fix. |
| **Risk of the solution itself** | Labeling everything "judgment" can dull the reader; they may stop weighing which judgments matter. |
| **Cost** | Zero beyond a sentence. |
| **What we expect after** | The operator can overrule any row with one edit, and the table never pretends to be measured. |
| **Does a human need training?** | `NO` |

### Risk D — Skill edits sit near locked text

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | `CLAUDE.md` locks parts of `skills/execforge/` and the OKR aliases in `skills/c-level/`. This task edits `skills/full-cycle/` only, but a careless edit elsewhere would break the lock and the trust it protects. |
| **Short or long term?** | `SHORT` — only during this change. |
| **Solution** | Touch only `full-cycle`, and run `tests/test_restored_sections.py` before committing. |
| **What would the solution fix?** | Compliance. |
| **Risk of the solution itself** | Trusting the test alone; if the test itself were weakened the lock would be silent. Not touching the test at all keeps this risk near zero. |
| **Cost** | One test run. |
| **What we expect after** | The lock test passes untouched, proving locked sections were not edited. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-10 | Put the strategic view inside the product plan, not in `roadmap.md` | The plan is where the key results live; a strategy split from its measures goes stale faster. |
| 2026-08-10 | "Serves none" is allowed at Stage 0, and flags rather than blocks | A hard block would make people invent a key result to pass the gate — fake links are worse than honest none. |
| 2026-08-10 | Do not rewrite `roadmap.md` as benefits yet | The earlier decision to defer that still stands: a benefit needs a beneficiary, and that is the open question only the operator can answer. |
| 2026-08-10 | Record this change as a decision in `docs/decisions/` | Key result 1 demands it: skill changes carry a recorded decision. This is the first one that does. |

## What happened

- 2026-08-10 — Plan written. Work starting.
- 2026-08-10 — Four sections added to `docs/product-plan.md`. Pointer added to
  `docs/roadmap.md`. Rule 5a, a diagram note, and a validation-gate line added to
  `full-cycle` (0.9.0). Decision recorded in
  `docs/decisions/2026-08-10-product-plan-in-lifecycle.md`. Version 0.16.0.
- 2026-08-10 — Checks: 104 tests OK (lock test untouched and passing),
  `validate` passed, `release-check` consistent.

## Still unclear

- **Who is ExecForge for?** Still open, still the operator's. The new roadmap
  section does not answer it — it shows how much of the roadmap is waiting on it.

## Result

Done, on branch `lz-plan-capabilities`, version 0.16.0.

- The product plan now carries all four working methods the user asked about:
  evidence rules, a picking order, a strategic roadmap table, and scope and
  dependency rules. The table makes one thing plain: seven of ten roadmap items
  wait on the open question (who is ExecForge for).
- The lifecycle now uses the plan: `full-cycle` Stage 0 must name the key result
  an initiative serves, or say `serves none`. The validation gate checks it.
- Left out on purpose: rewriting `roadmap.md` as benefits (still behind the open
  question), and any answer to the open question itself — that stays the
  operator's.
- Proof: 104 tests OK, `validate` passed, `release-check` consistent. Decision
  record at `docs/decisions/2026-08-10-product-plan-in-lifecycle.md`.
