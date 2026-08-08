# Product Plan

What ExecForge is for, and how anyone would know it is working.

Every number here was measured on 2026-08-08. Nothing is estimated. Where no baseline
exists, this document says `no baseline yet` rather than inventing one — the same rule
`execforge` applies to everyone else.

## The problem

An AI agent will tell you the work is done. It will say the tests passed, the review
happened, the fix is safe. Sometimes that is true. Sometimes it is a confident sentence
with nothing behind it, and you find out later, in the worst way.

Checking every claim by hand costs more than doing the work yourself. Checking none of
them means shipping on trust.

Evidence that this is real, all from this repository:

- `CLAUDE.md` carries the rule *"Never claim an upstream review, implementation, test, or
  final gate ran unless evidence shows it actually ran."* Rules like that get written
  after being burned, not before.
- On 2026-08-08 a CI job that had waited since 17 July ran for the first time and found
  that `validate`, `doctor` and `install` were **all broken on Windows**. Nobody knew.
  Nothing had reported a problem.
- On the same day an `execforge` review returned `GO` on a feature that was not needed.
  It was reversed only when the operator asked "do I need this?" The review had quoted a
  true number — *"2 of 2 warnings were noise"* — in a misleading way.
- The `sessions` command found three pieces of stray work that `git status` cannot show.

Each of those is the same failure: something looked fine and was not.

## Who it is for

**Today: one person.** The author, governing their own AI-assisted work.

That is the measurement, not a guess:

| Signal | Value | Measured |
| --- | --- | --- |
| Public on GitHub since | 2026-07-03 | 5 weeks |
| Stars / forks / watchers | 0 / 0 / 0 | 2026-08-08 |
| Human contributors | 1 | `git shortlog` |

**This is the open question of the whole plan.** A tool for one person is a legitimate
choice — it just has to be a choice. Almost everything below changes depending on the
answer:

- *If ExecForge is for one person*, adoption does not matter, the roadmap should be cut
  to what that person needs, and 19 releases in 5 weeks is fine.
- *If ExecForge is for other people*, then 5 weeks public with zero signal is the most
  important fact in this document, and the next work is finding one external user, not
  shipping a tenth skill.

**Owner: the operator. Until it is answered, treat every "user" below as meaning the
author.**

## Job to be done

> When I hand work to an AI agent, I want to know what actually happened — not what it
> says happened — so I can ship without either trusting blindly or re-checking
> everything myself.

- **Primary user:** someone directing AI agents on real code.
- **Current workaround:** reading every diff, or trusting and hoping.
- **Moment of greatest friction:** the agent says "done, tests pass" and there is no
  cheap way to know whether that sentence is true.
- **Frequency:** every task.

## Product hypothesis

> We believe that **someone directing AI agents on real code** cannot tell a finished
> job from a confident sentence. By **forcing every claim to carry evidence, and every
> decision to be recorded with its reasoning**, we expect **fewer changes shipped on
> claims that turn out to be false**.

## Objective

Work claimed as done is work that demonstrably happened.

## Key results

Two of these are in the operator's control. The third is not, which is why it has no
target yet.

| # | Key result | Baseline (2026-08-08) | Target |
| --- | --- | --- | --- |
| 1 | ExecForge changes carrying a recorded decision | **2 in 99 commits** | Every change that adds or removes a skill |
| 2 | Platforms the test suite actually runs on | **2 of 2** — Linux and Windows, since 2026-08-08 | Hold at 2; no platform ships unverified |
| 3 | People outside this machine using it | **0**, after 5 weeks public | `no baseline yet` — depends on the open question above |

On KR1: the tool exists to make people record decisions with evidence, and across its own
99 commits it has recorded two — neither for a skill. That is the sharpest gap in this
document, and the only one entirely within reach.

## What ExecForge is

A set of skills that put gates between an idea and a shipped change: a product decision,
an engineering plan, a security review, a QA gate, a journey review, and a final ship
verdict. Each ends in a stated verdict rather than a feeling.

## What ExecForge is not

- **Not a code generator.** It decides and reviews. Other tools write.
- **Not a CI system.** It produces judgements a human reads, not automated pass/fail.
- **Not a way to go faster.** It is deliberately slower at the point of decision, in
  exchange for fewer reversals later.
- **Not self-executing.** Every gate can be skipped by a person who wants to skip it.

## Kill criteria

Written now, while it is cheap to be honest:

- If claims still ship unverified with the gates in place, the gates are decoration —
  fix them or remove them.
- If the operator stops using it on their own work, it has failed its only confirmed
  user.
- If the answer to the open question is "other people", and after a fair attempt there is
  still no external user, reduce it to a personal tool and stop paying the cost of
  packaging, docs and release process.

## Known gaps

- **`docs/roadmap.md` lists features, not benefits.** Every line says what gets built,
  none says who is better off. Deliberately not fixed yet: a benefit needs a beneficiary,
  and that is the open question above.
- **Plans live in two folders** — `plans/` and `docs/plans/` — with different naming.
- **19 releases in 5 weeks with no feedback loop.** Speed is not the problem; the absence
  of any signal about whether releases help is.
