# Add a project management skill

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.

- **Started:** 2026-11-06
- **Last updated:** 2026-11-07
- **Role(s):** c-level (router), execforge (decide whether to add it)
- **Branch:** lz-account-manager-verdict (plan file only; nothing built)
- **Status:** DONE (decision made and the small changes built; waiting for the operator's approval to commit)

## What was asked

"proceed account-manager and also project management" — the second half. No more
detail was given. Read as: add a project management skill or role to ExecForge.

## What we already know

- `eng-level` already has a `manager` role. It breaks work into tickets, puts them in
  order, names what blocks what, and refuses to call a plan ready while any ticket has
  no pass test. The role is picked from the words in the request; no flag needed.
- `client-level` already drafts status answers for a client reader.
- Every role run already keeps a dated plan file under `plans/` with status, choices,
  what happened, and what is still unclear. That is per-task tracking, by convention.
- Prompt history (about 1,000 prompts over two reviews) has almost no project
  management asks. One prompt asked for "a sentence to my stakeholder about the
  current situation". Deadline pressure shows up inside build requests, not as a
  separate job.
- The July 2026 review of possible new actors did not list project management.
- A skill cannot see a calendar, a ticket tool, or the clock. It sees only what is
  pasted or what is in the repo. There is no place in the bundle to store state
  between runs except the `plans/` files.

## The question to decide

What does "project management" mean here, and is any reading not already covered by
the `manager` role, `client-level`, or the plan-file convention? Readings: (a) track
tasks, deadlines, and status across an engagement; (b) status reports to a client or
stakeholder; (c) what the `manager` role already does; (d) a view across many projects.

## The plan

1. Write this plan file first (done).
2. One CEO reviewer and one COO reviewer, each alone, same fact package. Advisory only.
3. This session weighs both and gives one verdict: GO / GO WITH CONDITIONS / MODIFY /
   PILOT / DEFER / KILL.
4. Record the ledger, OKRs, and controls here.
5. Any build is a separate step with operator approval before any commit.

## Risks

### Risk A — Building a skill with no evidence of need

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | A twelfth skill nobody runs. It still costs a router row, a test, an eval case, a docs page, and a name to recall under pressure. The eval case also pushes an older case out of the CI window (the CI job only runs the first five eval files by name). |
| **Short or long term?** | `LONG` — a skill stays until someone removes it. |
| **Solution** | Decide from evidence. If the need is real but small, add words to an existing role instead of a new skill. |
| **What would the solution fix?** | operational load |
| **Risk of the solution itself** | The operator asked for a skill by name and may feel unheard if the answer is "it already exists". |
| **Cost** | Review time only. `not measured`. |
| **What we expect after** | A clear verdict with the reason, and the operator can overrule it in one word. |
| **Does a human need training?** | `NO` |

### Risk B — A tracking skill that cannot see time or tools

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | A skill that promises to "track deadlines" but has no clock, no calendar, and no ticket tool gives stale or made-up status. The operator trusts it and misses a date. |
| **Short or long term?** | `LONG` — it is a limit of the bundle, not a bug. |
| **Solution** | Any status output must rest on pasted facts or `plans/` files, and must label dates as given by the operator, never computed. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | Output feels hedged. |
| **Cost** | `not measured`. |
| **What we expect after** | No date or status in any output without a named source. |
| **Does a human need training?** | `YES` — the operator must paste the real dates and status; the skill cannot fetch them. |

### Risk C — Client names and dates in public plan files

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | Project tracking means engagement names, dates, and people. The `plans/` folder is tracked in a repo with a public docs site. A client could be named in public. |
| **Short or long term?** | `LONG` |
| **Solution** | Any tracking content for a real client uses the `private/` folder or made-up names. Say this in the skill or convention. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | Split between public and private files; easy to put a file in the wrong place. |
| **Cost** | `not measured`. |
| **What we expect after** | No real client name in a tracked plan file after this change. |
| **Does a human need training?** | `YES` — the operator must know which folder is private. |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-11-06 | Review before build, same as account manager | The ask is three words; the evidence is thin. |

## The review (execforge)

**How it ran.** One CEO reviewer and one COO reviewer, each alone, same fact package.
The gstack CEO review did not run (it needs the operator at the keyboard). Fallback CEO
plan.

**Gatekeeper: NO as a new skill, PARTIAL as small additions.** One prompt in about a
thousand asked for a status sentence to a stakeholder. None asked for sprints,
timelines, or budgets. The `manager` role already breaks work down and orders it, and
every role run already keeps a plan file with status.

**CEO finding (advisory).** A project management skill fails the test for a new actor:
it would give findings (what is late, what is next), not a verdict nobody may overrule.
Fold it in: alias rows so "status update" and "where are we with the client" reach
`client-level`, and "where are we", "what's next", "what's left" reach the `manager`
role; a status shape in `client-level` answer mode (done, in progress, blocked, next
date); a `Due` line in the plan template. Skip a new skill, Gantt or sprint output,
time or budget tracking.

**COO finding (advisory).** A new skill costs the same nine touch points as any other,
plus one more router row read on every prompt, and its eval file would sort fourteenth
and never run in CI. "Create the plan" and "what do I do next" are already `manager`
words, so a new skill would make the router flip between two homes. A skill cannot see
time; any deadline it "tracks" is whatever was pasted and will be stale next prompt.
Tracked plan files already name client systems and the repo is public, so engagement
tracking must not write client names into tracked files.

**Contradictions.** None. Both say fold in, no skill.

**Scope ledger.**

| Decision | Item | Why |
| --- | --- | --- |
| ADD NOW | Alias rows: `status update`, `update my stakeholder` → `client-level`; `project management`, `where are we`, `what's next`, `what's left`, `what is blocked` → `eng-level` `manager` (or `client-level` when a client reads it) | **Route** the operator's own words to the lens that already does the job — baseline: one such prompt had no home — which lets the question get answered without a new name to recall. |
| ADD NOW | Status shape in `client-level` answer mode: done, in progress, blocked, next date; dates given, never computed | **Turn** plan-file status into three plain sentences a stakeholder can read — no baseline yet — which lets the operator send an update without re-typing it. |
| ADD NOW | `Due` line in `plans/TEMPLATE.md`; `manager` role reads the plan files for status and the due line | **Give** the `manager` role a date to reason with — no baseline yet — which lets "what's next" answers name a date the operator set. |
| DEFER | Portfolio view across clients | Reopen if a second prompt asks for status across clients. |
| SKIP | A `project-management` skill; sprint, Gantt, time, or budget tracking | No evidence; the skill cannot see a clock or a ticket tool. |

**OKR plan.**
- Hypothesis: if status and next-step questions route to the existing lenses, the
  operator gets a usable answer without a new skill.
- Job to be done: "Tell me where we are, and give me three sentences for the client."
- Objective: status questions reach the right lens on the first try.
- KR1: the next five status or next-step prompts route to `client-level` or `manager`
  first time. Baseline: one of one had no home (July 2026).
- KR2: bundled skill count after this work stays at ten. Baseline: ten.
- KR3: plan files carry a `Due` line when a deadline exists. No baseline yet.

**A-C-T-I-O-N.** Assess: one homeless status prompt; `manager` already covers the rest.
Cost: alias rows and a few lines, no new skill. Technical tactics: words in the router
and the role-routing table. Security, governance, compliance: no client names in
tracked plan files; dates never computed. Operational work reduction: one paste, one
status answer. No manual work by default: no flags, mode inferred.

**Non-negotiable controls.** Lock test on the alias rows; decision record; client
names stay out of tracked plan files; locked sections untouched.

**Rollback and kill.** One revert. Kill the aliases if they steal `manager` or
`client-level` prompts in a routing eval.

**Final verdict: MODIFY.** No new skill. Routing words, a status shape, and a `Due`
line.

## What happened

- 2026-11-06 — Plan written. CEO and COO reviews dispatched.
- 2026-11-07 — Verdict MODIFY. Built on branch `lz-account-manager-verdict` together
  with the account manager change: alias rows in `skills/c-level/SKILL.md`, the
  status shape in `skills/client-level/SKILL.md`, the `Due` line in
  `plans/TEMPLATE.md`, the `manager` row in
  `skills/eng-level/references/role-routing.md`, the decision record
  `docs/decisions/2026-11-07-project-management-folded-into-existing-roles.md`, and
  a lock test on the `project management` and `status update` aliases. Tests and
  validate pass (see the account manager plan for the numbers). Nothing committed.

## Still unclear

- Which reading (a)–(d) the operator means. Only the operator can say.

## Result

Decision MODIFY, and the small changes are built and tested on the same branch as the
account manager change. Proof: the files named above, the decision record, and the
passing test run. Left out: a new skill (on purpose), and the commit (the operator
approves first).
