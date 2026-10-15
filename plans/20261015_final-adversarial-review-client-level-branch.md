# Final adversarial review of the client-level branch

> Plain English note: this file tracks a review task. A "skill" here is a
> markdown instruction file an AI agent follows. "The branch" is the set of
> changes waiting to merge.

- **Started:** 2026-10-15
- **Last updated:** 2026-10-15
- **Role(s):** c-level (review / release readiness)
- **Branch:** lz-client-level-and-spec-mode
- **Status:** DONE

## What was asked

The owner asked for one last independent hostile review of the branch before
merge. Three review rounds already ran. The job: find ways the change fails in
real use that those rounds missed. Mark each finding as FIXABLE (a fix is
known) or INVESTIGATE (a human must judge). Test and fixture files are read in
summary only, not word for word. End with one clear recommendation line.

## The plan

1. Write this plan file first (project rule).
2. List every changed file against the main branch.
3. Read the full diff of real source files: skills, scripts, docs, configs.
4. Read test and eval changes in summary form only.
5. Check untracked files too.
6. Hunt for: silent failures, instructions an agent could misread or abuse,
   gates that look real but never run, error handling that hides errors.
7. Report findings in chat with FIXABLE / INVESTIGATE labels and one
   recommendation line. No separate report file.

## Risks

### Risk A — Review misses a real defect

| Question | Answer |
| --- | --- |
| **How bad?** | MEDIUM |
| **What actually happens?** | A flaw ships. Users of the skills get wrong or unsafe behavior later. |
| **Short or long term?** | LONG — once merged it stays until found. |
| **Solution** | Review the whole diff, not samples; question every gate's reachability. |
| **What would the solution fix?** | none of these — it lowers the miss chance, nothing more. |
| **Risk of the solution itself** | Over-reporting: noise findings that waste the owner's time. |
| **Cost** | not measured |
| **What we expect after** | Owner gets a short list of real problems with clear labels. |
| **Does a human need training?** | NO |

### Risk B — Test files reviewed only in summary

| Question | Answer |
| --- | --- |
| **How bad?** | LOW |
| **What actually happens?** | A defect inside test or fixture text could be missed, because the owner asked that those files be read in summary only. |
| **Short or long term?** | SHORT — the next full review can read them. |
| **Solution** | Say plainly in the report that this coverage gap exists. |
| **What would the solution fix?** | compliance — the gap is visible, not silent. |
| **Risk of the solution itself** | None beyond a slightly longer report. "None" is justified here: it is one sentence. |
| **Cost** | not measured |
| **What we expect after** | The report names the summary-mode gap. |
| **Does a human need training?** | NO |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-10-15 | Follow the owner's review procedure directly instead of the eng-level review workflow | The owner's direct instruction set the exact procedure and output; direct instructions rank first. |

## What happened

- 2026-10-15 — Plan written. Diff listed. Review under way.
- 2026-10-15 — Whole diff read. Test files read in summary only, as asked. Ran the
  checks myself: validate passed, 108 tests passed.
- 2026-10-15 (second pass) — Final check after the fix round. Read the four changed
  skill files end to end as one system. Eval and QA evidence files read in summary
  only, as asked. Ran the checks again: validate passed, 108 tests passed. All
  earlier fixes are in place and none of the 19 old findings reopened.

## Still unclear

- Finding 7 (does a passing spec review auto-start design work?) and finding 10
  (what the pregate tool does with a file no rule matches) need the owner's call.

## Result

Twelve findings reported in chat, each marked FIXABLE or INVESTIGATE. The two worst:
the ux-level skill text tells the agent both "stop and ask" and "never ask" for the
same case, and the one automated check that would catch the wrong behavior never runs
(the CI eval job runs only the first four case files by name; the new case sorts
16th, and the new client-level case pushes an existing case out of the window).
Recommendation given: fix the named items before merge. No code was changed by this
review; the only file written is this plan file.

Second pass (after the fix round): all prior fixes hold; nothing reopened. Four new
small findings reported in chat — two one-line wording fixes worth doing before merge
(a routing shortcut in c-level that can skip the product-decision step for internal
proposals, and the full-cycle exit checklist not naming the new conditional Stage 2
approval), one cosmetic count ("three below" where the table has four rows), and one
question for the owner (which stage owns the journey re-review after screens exist).
None is a broken behavior today; all are text-consistency gaps. No code was changed
by this pass either; only this plan file was updated.
