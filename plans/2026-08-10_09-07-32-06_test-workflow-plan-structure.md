# Test: is a workflow-shaped product plan better than the current one?

> Write this file in plain, simple English. Short everyday words. Short sentences.

- **Started:** 2026-08-10
- **Last updated:** 2026-08-10
- **Role(s):** execforge (product review — judging a proposal, changing nothing)
- **Branch:** lz-plan-capabilities (no code change expected; review only)
- **Status:** DONE (verdict delivered, hybrid built on PR #28)

## What was asked

The user proposed a different shape for the product plan:

- Make the four methods (strategic roadmapping, prioritization framework,
  evidence synthesis, scope & dependency management) the **core value** of the
  product.
- Add a **product planning workflow** with four phases: discovery & alignment,
  definition & scoping, prioritization & sequencing, communication & execution.

Then: "will this better, kindly test this plan is it better than previous one."

So the job is a test, not a build. Compare the proposed shape against the
current plan (version 0.16.0) and say which is better, with reasons.

## The plan

1. Write down what a product plan here must do — the test criteria. Take them
   from the plan's own stated job, not from taste.
2. Score the current plan and the proposed shape against each criterion.
3. Check the proposed workflow against the existing lifecycle (`full-cycle`
   stages) for overlap — a new process that repeats an old one is cost, not value.
4. Give a verdict: better, worse, or partly better. If partly, name exactly
   which parts are worth taking.
5. Change no files. The verdict goes to the user; building it is a separate
   decision.

## Risks

### Risk A — The judge built the current plan

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | I wrote the 0.16.0 sections this morning. Judging a rival shape, I may favor my own work without noticing. The user gets a biased verdict dressed as a test. |
| **Short or long term?** | `SHORT` — it only affects this one review. |
| **Solution** | Name the bias in the report. Score with criteria taken from the plan's own stated job, written before scoring. Actively look for what the proposal does better — and report those parts first. |
| **What would the solution fix?** | None of these — it is honesty about the referee, not a process fix. |
| **Risk of the solution itself** | Over-correcting: praising the proposal too much to look fair. The criteria table is the guard — every score must point at something concrete. |
| **Cost** | None beyond care. |
| **What we expect after** | The user can check every score against the named evidence and overrule any of them. |
| **Does a human need training?** | `NO` |

### Risk B — Unfair fight: a finished document versus a sketch

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | The current plan is 200 lines with measured numbers. The proposal is eight words of structure. Scored naively, the finished thing always wins, and a good idea gets dismissed because it arrived short. |
| **Short or long term?** | `SHORT` |
| **Solution** | Score the proposal's *shape* as if fully built out — assume each phase would be written with the same evidence discipline. Judge the skeleton, not the word count. |
| **What would the solution fix?** | None of these — it is fairness in the test design. |
| **Risk of the solution itself** | Imagining the proposal too generously — filling its gaps with my own ideas and then crediting it for them. Where I do that, I say so. |
| **Cost** | None. |
| **What we expect after** | The verdict reflects the idea, not the length of its first draft. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-08-10 | Test only, change nothing | The user asked "is it better", not "make it so". A verdict first keeps the decision theirs. |
| 2026-08-10 | Criteria come from the plan's own job statement | "How would anyone know it is working" is the plan's declared purpose; a test against taste would be arbitrary. |

## What happened

- 2026-08-10 — Plan written. Running the comparison.
- 2026-08-10 — Verdict delivered: not better as a replacement; two pieces worth
  taking. User chose the hybrid.
- 2026-08-10 — Hybrid built: "Planning workflow" section added to the product
  plan (name-mapping table, discovery loop, communication channels), discovery
  log opened with one real entry, "no feedback loop" gap updated, changelog
  extended. 104 tests OK, validate passed, release-check consistent. Pushed to
  `lz-plan-capabilities`; rides PR #28.

## The build (added after the user chose the hybrid)

1. Add a "Planning workflow" section to `docs/product-plan.md`: a table mapping
   the user's four phase names to where each already lives, plus real content
   for the two missing halves — discovery and communication.
2. Give discovery a concrete home: a short dated log at the end of the product
   plan, with one genuine first entry. A loop with no home is a paper promise.
3. Update the "no feedback loop" known gap to match: the loop now exists on
   paper; the test is whether entries keep appearing.
4. Extend the 0.16.0 changelog entry. Same release, same open PR #28.
5. No lifecycle change — the Stage 0 anchor already covers it. Run tests,
   validate, release-check. Push to the same branch.

## Still unclear

- ~~Whether the user wants the winning parts built.~~ Answered 2026-08-10:
  build the hybrid ("proceed with your proposal").

## Result

**Verdict: NOT better as a replacement. Better in two places, and those two are
worth taking.**

Scored on eight criteria taken from the plan's own job. The current plan wins
four: it names who it is for and what is unknown; it has measurable key
results; it is built on evidence; and it does not duplicate the lifecycle.
The proposal wins two: **discovery & alignment** (a standing way for new
evidence to come in) and **communication** (how decisions reach anyone).
Those two are exactly the current plan's own named gap — 21 releases with no
feedback loop. The rest are ties or partial.

Two findings against the proposal:

1. **Three of its four phases already exist under other names.** Definition &
   scoping is Stage 0 plus the scope ledger. Prioritization & sequencing is the
   ledger plus the picking order added in 0.16.0. Execution is Stages 3–9.
   Building them again as a separate workflow means two processes for one job,
   and they will drift apart.
2. **Making the four methods the "core value" would point the plan at itself.**
   The core value is what the user gets — knowing what actually happened. The
   methods are how, not why.

Recommended if the user wants it built: keep the current shape; add a short
"planning workflow" section that maps the four phases onto where they already
live, and genuinely adds the two missing ones — a discovery/feedback step and a
communication step. Both collide with the open question (who is ExecForge for)
within one sentence of being written.

Bias declared: the same author wrote the current 0.16.0 sections and this
verdict. Every score points at something concrete so the user can overrule it.
No files changed; the decision to build is the user's.
