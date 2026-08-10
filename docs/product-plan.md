# Product Plan

What ExecForge is for, and how anyone would know it is working.

Every number here carries the date it was measured (first version: 2026-08-08).
Nothing is estimated. Where no baseline exists, this document says `no baseline yet`
rather than inventing one — the same rule `execforge` applies to everyone else.

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

Since 0.16.0 this plan is itself part of the lifecycle: every `full-cycle` Stage 0
decision must say which objective or key result here it serves — or say plainly that it
serves none — and a decision that changes this plan updates it in the same cycle.

## What ExecForge is not

- **Not a code generator.** It decides and reviews. Other tools write.
- **Not a CI system.** It produces judgements a human reads, not automated pass/fail.
- **Not a way to go faster.** It is deliberately slower at the point of decision, in
  exchange for fewer reversals later.
- **Not self-executing.** Every gate can be skipped by a person who wants to skip it.

## How this plan reads evidence

The rules this plan was built with, written down so they outlive the person applying
them:

- **Only measured numbers.** Every figure names its source and its date. A number
  without either does not go in.
- **Facts apart from guesses.** A claim is either `FACT` with its evidence, or
  `ASSUMPTION` said plainly. The two never share a sentence.
- **`no baseline yet` beats an invented one.** A missing number written as missing is
  information; a made-up number is poison downstream.
- **Synthesis means naming the pattern.** Separate incidents (the Windows breakage, the
  wrong `GO`, the stray work) earn a place here only when they point at one named
  failure — "something looked fine and was not" — not as a list of anecdotes.

## How work gets picked

Every candidate piece of work goes through the `execforge` ledger and lands in exactly
one bucket: `ADD NOW`, `DEFER` (with the condition that reopens it), `SKIP` (with the
reason), or `KILL`. No bucket, no work.

Among `ADD NOW` items, the order is:

1. Work that moves a key result beats work that does not.
2. Among those, work fully in the operator's control goes first.
3. An item whose only beneficiary is unproven waits behind the open question
   ("who is ExecForge for") — however exciting it is.

A date is only written next to an item when it was actually decided. Excitement is not
a schedule.

## Strategic roadmap

The flat list lives in `docs/roadmap.md`. This table is the strategic view: what each
item is for, and what blocks it. The "who is better off" column is **judgment, not
measurement** — the operator can overrule any row with one edit.

| Roadmap item | Serves | Who is better off | Blocked by |
| --- | --- | --- | --- |
| Behavioral-evals CI job becomes a required check | The objective directly (gates that demonstrably ran) | The operator | The job running quiet first |
| Harness-specific session-start adapters | No current key result | Other people (unproven) | The open question |
| JSON artifact emission helpers | No current key result | Other people (unproven) | The open question |
| Release packaging | KR3, if it ever gets a target | Other people (unproven) | The open question |
| Executable adapters (Playwright, Schemathesis, k6, ZAP, Pact, Testcontainers) | Deeper QA gates | The operator, when QA runs against real services | Nothing named |
| Visual decision ledger | No current key result | Other people (unproven) | The open question |
| GitHub PR check integration | No current key result | Other people (unproven) | The open question |
| Policy packs for regulated environments | No current key result | Other people (unproven) | The open question |
| Pluggable reviewer registry | No current key result | Other people (unproven) | The open question |
| Metrics for review agreement and defect escape rate | The objective — this is the missing feedback loop | The operator | Needs enough recorded runs to measure |

What the table shows at a glance: **seven of ten roadmap items are waiting on the open
question.** Answering it is worth more than building any of them.

## Scope and dependencies

**Scope.** What ExecForge is and is not (above) is the scope. Changing it takes an
`execforge` decision recorded in `docs/decisions/` or `.execforge/runs/` — which is
also what key result 1 counts. The default mode is Hold Scope: write down what exists,
build nothing, until a decision says otherwise.

**Dependencies.** The named blockers, so nothing waits on something unwritten:

- Rewriting the roadmap as benefits → blocked by the open question (a benefit needs a
  beneficiary).
- An adoption target for KR3 → blocked by the open question.
- The agreement/escape-rate metrics → blocked by having enough recorded decisions to
  measure; KR1 feeds this.
- Every roadmap item marked "unproven" above → blocked by the open question.

An item with an unmet dependency cannot be `ADD NOW`. That is the whole rule.

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

- **`docs/roadmap.md` lists features, not benefits.** The strategic roadmap above now
  names a beneficiary and a blocker per item, but the full rewrite as benefits stays
  deliberately unfixed: a benefit needs a beneficiary, and that is the open question
  above.
- **Plans live in two folders** — `plans/` and `docs/plans/` — with different naming.
- **19 releases in 5 weeks with no feedback loop.** Speed is not the problem; the absence
  of any signal about whether releases help is.
