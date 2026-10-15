# Collect recent use cases and find what to improve

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.

- **Started:** 2026-10-14
- **Last updated:** 2026-10-14
- **Role(s):** c-level (review of how ExecForge is being used)
- **Branch:** main
- **Status:** DONE

## What was asked

"can you help me collect my recently use case what can we improve for this execforge"

The operator wants two things:
1. Gather how they actually used ExecForge recently (what they asked for, in which projects).
2. From that evidence, say what ExecForge should improve next.

## The plan

1. Read the last review of this kind (`prompt-history/SUMMARY.md`, done 2026-07-12) so we
   do not repeat work. Note which of its fixes already shipped.
2. Pull the operator's own prompts from the local Claude session logs
   (`~/.claude/projects/*`), but only from 2026-07-13 onward — the day after the last
   review stopped.
3. Sort the prompts by project and by which ExecForge skill they triggered.
4. Look for patterns: which skills get used, which get skipped, where the operator
   repeats themself, where a gate was waved through, where a request had no good home.
5. Compare the patterns against the roadmap and product plan, so we do not propose
   something already planned or already rejected.
6. Report findings with a clear recommendation, plus business and technical risk for
   every option, per the project rule.

## Risks

### Risk A — Session logs hold secrets

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | The last review found a live API key and passwords pasted into old session logs. If this review quotes prompts without care, a secret could end up in a committed file in this repo. |
| **Short or long term?** | `LONG` — the logs keep growing and the habit of pasting secrets may continue. |
| **Solution** | Quote no secret in any output. Paraphrase prompts that contain one. Keep raw extracts in the throwaway scratch folder, never in the repo. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | Paraphrasing can soften evidence; a reader may doubt a claim with no verbatim quote. |
| **Cost** | A few minutes of care per quote. `not measured`. |
| **What we expect after** | No secret appears in this plan file or in the final report. |
| **Does a human need training?** | `YES` — the operator should stop pasting live secrets into prompts and point to a gitignored file instead (already advised on 2026-07-12). |

### Risk B — Logs may understate real use

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | If the operator used ExecForge on another machine or deleted sessions, the picture is partial, and a recommendation could rest on missing data. |
| **Short or long term?** | `SHORT` — only affects this one review. |
| **Solution** | Say plainly in the report what period and which projects the data covers, and call every count a count of *what is on this machine*. |
| **What would the solution fix?** | none of these — it is honesty, not a fix. |
| **Risk of the solution itself** | None beyond a slightly longer report. |
| **Cost** | None. |
| **What we expect after** | Every number in the report names its source and window. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-10-14 | Review only prompts from 2026-07-13 onward | The 2026-07-12 review already covered everything before that; repeating it adds nothing. |
| 2026-10-14 | Operator said "proceed" on the recommendation | Option A (client-level skill) built first — see `plans/20261014_client-level-skill.md`; the spec-review proposal adopted, and later the same day built in the same cycle on the operator's instruction — see `plans/20260930_ux-level-spec-review.md`. |

## What happened

- 2026-10-14 — Plan written. Pulled every prompt from 2026-07-13 to 2026-10-14 from the
  local session logs: about 590 real prompts across 8 projects (some appear twice when a
  session was retried). Raw extract stayed in the throwaway scratch folder, not in the
  repo. No secret was copied into this file or the report.

## What the logs show (the use cases)

| Project | Prompts | What it really was |
| --- | --- | --- |
| client A assessment | ~420 | A paid client job: a cloud-workspace security assessment. Checklists, access setup, run scripts, client Q&A, reports as PDF/slides, pricing. |
| home folder | ~110 | Terminal/desktop tooling (watching which ExecForge actor runs), plus deal talks for the same client job (price split, invoice). |
| client B back office + bot | ~127 | A chat bot for a client's back office, read-only database answers, cloud deploy, feature proposals. |
| training platform | ~23 | Phishing-simulation campaign test and report. |
| others | ~30 | Forex platform idea with budget, small cleanups, this repo. |

Patterns, counted on this machine only:

1. The main use of ExecForge now is **client consulting work**, not building products.
   Most asks are: explain in layman terms, answer the client's question with a scenario
   and a risk, make a slide / PDF / proposal, tell me what to sell. No skill owns this.
2. `execforge` is mostly triggered to **think of new ideas** ("what more potential",
   "what can we sales", "what feature can the bot do") — discovery, not a build/kill gate.
3. The operator keeps asking for **one seamless run**: "run all stage now…, run it
   seamless", "trigger execforge auto", "fully automated until all items completed".
4. **Rubber-stamp approvals continue**: 33 bare "proceed/continue". One gate was approved
   with a typo ("APPROVE STREAM") and once while asking what the gate even means. Same
   rate as the July review (37 of 468).
5. **"Test it until fix" still appears (8×) with no pass test.** The July fix (acceptance
   criteria in the upstream contract) is written down but nothing enforces it.
6. **Live passwords and a database login were pasted into prompts again**, after the July
   review already warned about it. They must be rotated.
7. Long lifecycle runs keep **running out of context**; the operator types "continue back
   the last session" and work restarts from a summary.
8. The operator **built their own viewer** to see which lifecycle actor is running — a
   real demand for run visibility that ExecForge does not give.

Shipped since July (so not re-proposed): eng-level roles, alias table, ux-level,
risk register, plan tracking, post-hoc review, stop-after.

- 2026-10-14 — Operator shared a proposal from Downloads (`ux-level-spec-review.md`,
  dated 2026-09-30): add a third mode to `ux-level` that reviews a written UI spec before
  anything is built. Checked its claims against the repo: all true. Verdict given:
  useful and sound, worth adopting, but after the client-engagement skill (Option A),
  because the usage data shows `ux-level` ran only ~2 times in 3 months while client
  work ran daily. One gap noted: the operator's real phrasing ("review this project
  plan", "review the proposal") routes to `eng-level` today, so the router and alias
  table must send plan/spec/proposal reviews to the new mode or it will never fire.

## Result

Report delivered to the operator with five improvement options and one recommendation:
build a client-engagement skill first (the biggest unowned surface), then a true
auto mode for full-cycle, then enforce pass criteria, then a secret warning, then run
visibility. Each option carries business risk, technical risk, term, and failure
scenario, per the project rule. No code changed in this task.
