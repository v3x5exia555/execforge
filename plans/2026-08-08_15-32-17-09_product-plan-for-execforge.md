# Write a product plan for ExecForge itself

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-08-08
- **Last updated:** 2026-08-08
- **Role(s):** execforge (product decision), applied to ExecForge
- **Branch:** lz-product-plan, cut from `main`
- **Status:** IN PROGRESS

## What was asked

"Do we have product plan here?" — no, there was none. Then: "include product now."

## What the check found

There are plenty of records of single choices: 6 plan files in `plans/`, 4 older ones in
`docs/plans/`, 1 decision record in `docs/decisions/`, 2 full decision runs in
`.execforge/runs/`, and a roadmap.

There was no document saying who ExecForge is for, what problem they have, or how anyone
would know it is working. A search for "product hypothesis", "job-to-be-done", "key
results" and "baseline" across `docs/`, `plans/` and `.execforge/` returned nothing about
ExecForge. Those phrases appear only inside the skills, telling other people to write
them.

## The numbers, all real

Gathered on 2026-08-08. Nothing here is estimated.

| Fact | Value |
| --- | --- |
| Public on GitHub since | 2026-07-03 (5 weeks) |
| Stars / forks / watchers | 0 / 0 / 0 |
| Human contributors | 1 (two committer names, same person) |
| Skills shipped | 9 |
| Versions released | 19 |
| Commits | 99 |
| Tests | 104, plus 221 subtests |
| Recorded ExecForge decision runs | 2 — ponytail adoption, cross-repo rollup |

Two of those sit uncomfortably together: **19 releases in 5 weeks, and zero signal that
anyone outside this machine has ever used it.** A lot of building, no feedback loop.

And a second one: the tool exists to make people record decisions with evidence, and in
its own 99 commits it has recorded **2**. Neither was for a skill.

## The product decision (execforge)

**Mode:** single isolated review. A document, no code, one revert undoes it.

**Gatekeeper: YES, but narrower than asked.** The pain is real and provable — see the
evidence below. What is *not* provable is that anyone else wants this. So the plan is
written for the operator who exists, not the community that might.

### Evidence the problem is real

All from this repository, labelled honestly:

- FACT: `CLAUDE.md` carries the rule "Never claim an upstream review, implementation,
  test, or final gate ran unless evidence shows it actually ran." A rule like that gets
  written after being burned.
- FACT: on 2026-08-08 a CI job that had been waiting since 17 July found a bug on its
  first run — `validate`, `doctor` and `install` were all broken on Windows and nobody
  knew.
- FACT: on the same day, an ExecForge review returned `GO` on a feature that was not
  needed. It was reversed only because the operator asked "do I need this?" The review
  had used a true statistic — "2 of 2 warnings were noise" — in a misleading way.
- FACT: the `sessions` command found three things `git status` could not show.
- ASSUMPTION: other people building with AI agents have the same problem. No evidence
  from this repository either way.

**Scope mode:** Hold Scope. Write down what already exists. Build nothing.

**CEO view:** the honest headline is that this is a tool of one, and that is fine if it
is chosen rather than assumed. The gap that matters is not features — it is that 19
releases have shipped with no way to tell whether any of them helped. A product plan is
worth writing only if it makes the next release answerable.

**COO view:** cost is one document. The risk is the opposite of usual — a product plan
for a solo tool can become paperwork that is written once and never read. Guard against
it by keeping the numbers real and few, and by writing the kill criteria honestly.

## Scope ledger

| Decision | Item | Why |
| --- | --- | --- |
| `ADD NOW` | `docs/product-plan.md` — hypothesis, job, objective, key results on real baselines | Answers "how would we know this is working", which nothing answers today; unlocks judging a release rather than just counting them |
| `ADD NOW` | Record the honest adoption number (0 outside signal after 5 weeks public) | Stops the plan opening with a comfortable fiction; unlocks a real decision about who this is for |
| `DEFER` | Rewriting `docs/roadmap.md` as benefits rather than features | Reopen once the target user is settled — a benefit needs a beneficiary, and that is the open question |
| `DEFER` | Merging `plans/` and `docs/plans/` into one folder | Reopen next time a plan is written in the older folder |
| `SKIP` | Setting an adoption target for other users | Only the operator can decide whether ExecForge is for anyone else. Inventing a target would be the exact fabrication the skill forbids. |
| `SKIP` | Any new skill, command, or code | The gap is a missing document, not missing software. |

**Verdict: GO WITH CONDITIONS.** Write the plan using only measured numbers. Leave the
target-user question open and visible, marked as the operator's to answer, rather than
filling it in.

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-08 | State "0 external users" plainly | The skill forbids inventing baselines. 5 weeks public with 0 stars, 0 forks, 0 watchers is the measurement. |
| 2026-08-08 | Leave the target user as an open question | Only the operator knows whether this is for one person or many. Guessing would poison every number downstream. |
| 2026-08-08 | Key results that measure discipline, not popularity | Adoption is not in the operator's control. Whether ExecForge governs its own changes is. |
| 2026-08-08 | Include the uncomfortable numbers | 19 releases with no feedback loop, and 2 recorded decisions in 99 commits. A plan that hides those is decoration. |

## What happened

- 2026-08-08 — Searched for an existing product plan. None found.
- 2026-08-08 — Gathered real adoption and size numbers from GitHub and git.

## Still unclear

- **Who is ExecForge for?** Today the evidence says one person. That is a legitimate
  answer, but it must be chosen, not defaulted into. The plan records it as open.

## Result

Added `docs/product-plan.md` and put it in the docs nav. Version 0.14.3.

What it says, using only measured numbers:

- The problem, with four pieces of evidence from this repository — including the Windows
  bug nobody knew about, and the `GO` verdict that was wrong until challenged.
- Who it is for: **one person today**, recorded as an open question the operator owns,
  not filled in.
- Product hypothesis, job-to-be-done, and one objective.
- Three key results. Two have real baselines. The third, external users, carries
  `no baseline yet` because setting an adoption target would be inventing one.
- What ExecForge is not, and kill criteria written while they are still cheap to write.
- Known gaps named rather than hidden: the roadmap lists features not benefits, plans
  live in two folders, and 19 releases have shipped with no feedback loop.

The sharpest number in it: **2 recorded ExecForge decisions across 99 commits**, neither
for a skill. The tool that demands recorded decisions has barely used itself.

Verified: 104 passed, 221 subtests; validate passed; release-check consistent.
