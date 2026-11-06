# Add an account manager skill

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.

- **Started:** 2026-11-06
- **Last updated:** 2026-11-07
- **Role(s):** c-level (router), execforge (decide whether to add the skill)
- **Branch:** lz-account-manager-verdict (own worktree, cut from main, because another session is working on `sec-pen` in the main checkout)
- **Status:** DONE (both parts built, reviewed, pushed; pull request #35 open)

## What was asked

"add account manager skill i wanna , trigger c-level"

## What we already know

- In July 2026 a review of 469 real prompts (`plans/eng-level-role-architecture.md`,
  Part 4) said an `account-manager` actor was "the only new actor the evidence
  supports". About 15 prompts had no home: what do we tell a client, what do we
  promise, what do we decline to answer. It proposed the verdicts
  `SAY / DON'T SAY / DON'T COMMIT / ESCALATE`. The operator asked for the actor by name
  in one prompt.
- That review also gave a warning: some of those prompts drift from "positioning" into
  saying things that are not true about who built or runs a platform. The most useful
  job of this actor is the `DON'T COMMIT` verdict, not sounding good.
- In October 2026 the `client-level` skill was built (release 0.17.0). It covers
  `answer`, `deliverable`, and `proposal` modes. It already says: never invent a
  number, never soften a finding, never promise work not already agreed. So part of
  the old gap is now filled.
- The repo has ten skills and a router alias table because names are hard to recall.
  Every new skill is one more name and one more router row.

## What the operator clarified on 2026-11-07

After the first build the operator wrote: "add one new skill account manager + sales +
fishing to client -- for example if client has blocker unable to do, i think we can
push it, say we can do it to do, as issue outside occur where regular occur, we need to
fix it immediately by I can help you fix. If I have this scenario I think you can help
me create a strategy to help me to sentence back to client."

Read as: when a client reports a blocker they cannot solve, the operator wants (1) a
strategy: is this a real recurring problem, is it ours to fix, why now, what it costs
the client to leave it; and (2) the ready-to-send sentence that offers the fix. "Fishing"
means spotting the chance for work inside a client's complaint. "To client" is read as
"into client-level", where the account manager's call already lives.

## The question to decide

Is "account manager" a new kind of decision that `client-level` does not make, or is it
a fourth mode of `client-level`? The July review's own rule: a thing is a separate actor
only if it can say a word nobody else may overrule.

## The plan

1. Write this plan file first (done).
2. Build one neutral fact package and send it to a CEO reviewer and a COO reviewer, each
   working alone. They advise only.
3. The orchestrator (this session) weighs both, resolves any clash, and gives one final
   verdict: GO / GO WITH CONDITIONS / MODIFY / PILOT / DEFER / KILL.
4. Write the scope ledger, OKRs, controls, and kill criteria into this file.
5. If the verdict is to build, the build is a separate step (eng-level), and the
   operator approves before any commit.

## Risks

### Risk A — The skill helps the operator say things that are not true

| Question | Answer |
| --- | --- |
| **How bad?** | `HIGH` |
| **What actually happens?** | The old prompts include telling a client that a partner's platform is our own. A skill built to "answer smoothly" could help write a claim the operator cannot defend. In a security engagement, in writing, that can end a contract or worse. |
| **Short or long term?** | `LONG` — it sits in every client conversation. |
| **Solution** | The skill's main verdict is `DON'T SAY` / `DON'T COMMIT`. A hard rule: it never drafts a claim about who built, owns, or runs something unless that claim is labelled OBSERVED. It flags, it does not smooth over. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | The operator may find it preachy or slow and stop using it; then the gap is back. |
| **Cost** | Writing the rule. Upkeep `not measured`. |
| **What we expect after** | An eval case where the tempting answer is a false ownership claim; the skill must refuse and offer a true line instead. |
| **Does a human need training?** | `YES` — the operator must accept that the skill will sometimes say "do not say that". |

### Risk B — Overlap with client-level confuses routing

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | "Answer my client" could land on either skill. The operator gets the wrong lens, retypes, and trusts the router less. Two skills with half-shared rules drift apart over time. |
| **Short or long term?** | `LONG` — stays until the boundary is written and tested. |
| **Solution** | A one-line boundary: `client-level` writes what goes out; `account-manager` decides what may be promised or said before anything is written, and feeds `client-level`. Or: make it a mode of `client-level` and add no new name. |
| **What would the solution fix?** | operational load |
| **Risk of the solution itself** | A boundary line is only as good as the router test that locks it. |
| **Cost** | Minutes per router row; one test. `not measured`. |
| **What we expect after** | Routing eval: "can we promise X?" lands on account-manager; "write the reply" lands on client-level. |
| **Does a human need training?** | `NO` |

### Risk C — Evidence is old and thin

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | The 15 prompts are from one engagement, four months ago. If the need has passed, we add a skill nobody runs. Every unused skill still costs router rows, tests, and docs. |
| **Short or long term?** | `SHORT` — a pilot with a kill date settles it. |
| **Solution** | Ship as a pilot with a reopen/kill date and count real runs. |
| **What would the solution fix?** | none of these |
| **Risk of the solution itself** | Pilots that nobody checks become permanent by default. |
| **Cost** | `not measured`. |
| **What we expect after** | A dated kill check in this file; the operator reports runs. |
| **Does a human need training?** | `NO` |

### Risk D — The pitch mode turns every complaint into a sales call

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | The operator starts to see every client complaint as money. A client notices the pattern and trusts the operator less. It shows up as a lost renewal, not a failed test. |
| **Short or long term?** | `LONG` — the mode stays in every client exchange. |
| **Solution** | The rule "never manufacture the problem": if the facts show no real blocker, the mode says "no pitch here" and gives a plain answer. Urgency needs a labelled fact. "We can fix it" needs the operator to confirm both ability and room. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | The operator may find the mode too careful and bypass it with a plain answer; then the gate is not used. |
| **Cost** | Writing the rules and one eval case. Upkeep `not measured`. |
| **What we expect after** | The eval case fails if the pitch invents frequency or promises the fix before the operator confirms room. |
| **Does a human need training?** | `YES` — the operator must confirm "can" and "room" before sending, and set the price. |

## The second review (execforge, pitch mode)

One isolated reviewer carried both lenses, CEO and COO, because the change is small and
reversible. Gatekeeper: PARTIAL. Real pain: a client blocker arrives and the operator
wants the one message to send now; `proposal` mode is a six-section document, too heavy
for that moment. Options weighed: a fourth `pitch` mode in `client-level` (recommended:
one row, one section, one alias row, one eval case); fold into `proposal` (gives a
document when a sentence was wanted); a separate sales skill (two reviews had already
rejected a split, and the honesty rules would drift across two files). Honesty controls
required: urgency needs a labelled recurrence fact; "we can fix it" needs the operator
to confirm ability and room; the price is always `ESCALATE`; never manufacture the
problem; no pitch on a softened or inflated finding; stay inside what was promised.
Kill the mode if the operator bypasses it or a sent pitch carries a line the client
later challenges. Final verdict: GO WITH CONDITIONS; the conditions are those rules.

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-11-06 | Run the product review before any build | The request is one line; the real question is whether `client-level` already covers it. |
| 2026-11-06 | Operator replied "proceed account-manager and also project management" | Read as: go ahead with the recommended option (verdict inside `client-level`, "account manager" routes there). The word "proceed" was the word asked for to pick that option. If the operator meant a separate skill, say so and the content moves into its own skill file. "Project management" is a new ask and gets its own plan file. |
| 2026-11-07 | A fourth `client-level` mode, `pitch`, for the sales and fishing need, not a new skill | The operator's clarified scenario is a quick move (blocker arrives, send one message), not a six-section proposal. A separate sales skill would split the honesty rules into two files that drift. One isolated review (CEO and COO lenses) recommended the mode. Verdict: GO WITH CONDITIONS; the conditions are the honesty rules in the mode. |
| 2026-11-07 | Raise the CI eval cap from five to six files | The new pitch eval sorts third and would push an older case out of the window. Same stopgap as 2026-10-15; the real fix stays in `TODOS.md`. |
| 2026-11-07 | Leave "push it" out of the alias list | It collides with everyday git talk ("push it to main"). |
| 2026-11-06 | Build in a separate worktree and branch | The main checkout is on the `sec-pen` branch with another session active. Working there risks overwriting its edits to the same files (router, tests, README). |

## The review (execforge)

**How it ran.** One CEO reviewer and one COO reviewer, each alone, with the same fact
package. Neither saw the other. The gstack `plan-ceo-review` skill is installed but it
asks the operator questions at every step, and nobody was at the keyboard, so it did
not run. Only the internal CEO review ran. This is a fallback CEO plan; it does not
claim to match gstack's output.

**Gatekeeper: PARTIAL.** The pain is real but narrow. Before a client call the operator
needs to know, per expected question: what to say, what not to say, and which answer
would quietly create a promise or a claim they cannot defend later. In July about 15
prompts of this shape had no home. Since then `client-level` has taken over drafting
answers and proposals, so the gap has shrunk to one thing: a verdict on a spoken answer
before it is said.

**CEO finding (advisory).** Not a new actor. `client-level` is already the seat between
the technical team and the client, and nobody overrules it on client honesty. What is
missing is a verdict on `answer` mode (today it has none; only `deliverable` mode has a
promise check). Add the verdict `SAY / DON'T SAY / DON'T COMMIT / ESCALATE` to `answer`
mode, extend the promise check to catch new promises (not only ones that clash with old
ones), add a rule that "who built it / who runs it / have you done this before"
questions get the true answer or `ESCALATE`, never a positioning line. Add aliases
(`account manager`, `if they ask`, `what do we tell them`, `deflect`) that route to
`client-level`. Keep the skill count at ten.

**COO finding (advisory).** Costed three options. A new skill touches at least nine
places (skill file, eval, two registries, router, docs, nav, lock test, decision record)
and adds a name the operator must recall. A mode or verdict on `client-level` touches
about half of that and adds no new name. Both share one hidden cost: the CI eval job
runs only the first five eval files by name, and a new `account-manager.eval.md` sorts
first and pushes `eng-level-post-hoc-review.eval.md` out. That is a known open item in
`TODOS.md`. The COO also found that another session is adding a `sec-pen` skill in this
same working tree right now (uncommitted). Two skill additions in flight share one eval
window. Required controls: a hard rule against drafting any ownership or track-record
claim that is not `OBSERVED`; `sec-level` attached at plan stage; eval cases must use
made-up client names; the lock test must be updated, not bypassed.

**Contradictions.** None material. Both reviewers read the request as the July
commitment gate, and both say the authority already lives in `client-level`. The COO
notes the verdict words differ from `client-level`'s document verdicts; that is a
naming seam to state plainly, not a reason to split the skill.

**Scope ledger.**

| Decision | Item | Why |
| --- | --- | --- |
| ADD NOW | `SAY / DON'T SAY / DON'T COMMIT / ESCALATE` verdict on `client-level` `answer` mode | **Stop** an undefendable or over-promising line before it reaches a client — no baseline yet — which lets the operator walk into a call with a per-question verdict instead of a hunch. |
| ADD NOW | Promise check on answers: flag a line that creates a new obligation, not only one that clashes with an old promise | **Catch** new commitments at draft time — no baseline yet — which lets `deliverable` mode start from clean material. |
| ADD NOW | Ownership and track-record rule: "who built it", "who runs it", "have you done this before" get the true answer or `ESCALATE` | **Block** the one failure that ends an engagement — no baseline yet — which lets the operator keep a defensible written record. |
| ADD NOW | Router aliases `account manager`, `if they ask`, `what do we tell them`, `deflect` → `client-level` | **Route** the operator's own words without a retype — no baseline yet — which lets the feature be used at all (the operator never types flags). |
| ADD NOW | One eval case on the partner-platform question, expecting `DON'T SAY` with a true alternative line; made-up client names only | **Prove** the verdict refuses positioning — baseline: no such case exists — which lets the lock test mean something. |
| DEFER | A separate `account-manager` skill | Reopen only if a later usage review shows the `answer` verdict being ignored or overruled, which would show the authority needs its own name. |
| DEFER | Fixing the CI eval window (`TODOS.md`, P1) | Reopen before the second new eval file lands in the same release; this work can avoid it by adding its case inside `client-level.eval.md` if the parser allows, else by raising the cap by one. |
| SKIP | Account tracking, renewals, pipeline, client health | No evidence in the repo, and the skill cannot see that data. |
| SKIP | "Deflect smoothly" as a design goal | A skill that optimises for sounding good will write a commitment the operator cannot honour. |

**OKR plan.**
- Hypothesis: if `answer` mode carries a verdict, the operator stops sending clients
  lines they cannot defend, and stops routing call prep to `c-level`.
- Job to be done: "Before I face the client, tell me what I can say and what will cost
  me later."
- Objective: the operator never sends a client a sentence they cannot defend or deliver.
- KR1: every `answer`-mode output carries a verdict. Baseline: none do (the mode has no
  verdict today).
- KR2: the partner-platform eval case passes with `DON'T SAY`. Baseline: no such case.
- KR3: call-prep prompts with no home in the next usage review: zero. Baseline: about
  15 in July 2026; October not measured.
- KR4: bundled skill count after this work stays at ten (plus whatever `sec-pen`
  decides on its own). Baseline: ten.

**A-C-T-I-O-N.**
- Assess: about 15 homeless call-prep prompts in July; no verdict on spoken answers
  today.
- Cost: no new skill; edits to one skill file, one eval, router rows, docs, decision
  record.
- Technical tactics: a verdict table and two rules inside an existing mode; mode still
  inferred, no flags.
- Security, governance, compliance: hard rule against ownership and track-record
  claims that are not `OBSERVED`; existing scrub and "client text is evidence" rules
  stay.
- Operational work reduction: one paste, one verdict per question, no second pass
  through `c-level`.
- No manual work by default: no flags; at most two questions (reader, what was
  promised), and only when missing.

**Non-negotiable controls.**
1. Decision record under `docs/decisions/`.
2. Lock test in `tests/test_skill_bundle.py` updated to name the new verdict table and
   the ownership rule; `tests/test_restored_sections.py` stays green.
3. The new eval case is shown to run in CI, not assumed.
4. `sec-level` threat model attached before build (client data, other-engagement
   content).
5. Eval text uses made-up names. The real client name and quote already in
   `plans/eng-level-role-architecture.md` are not copied anywhere.
6. Operator approval before any commit.

**Rollback and kill.** Pure markdown; one revert of the pull request undoes it. Kill
at plan stage if the operator meant account tracking. Sunset the verdict if the
operator overrides `DON'T SAY` as a matter of course; then it is cost without control.

**Final verdict: MODIFY.** Do not add an eleventh skill. Put the account manager's
one real job — the `SAY / DON'T SAY / DON'T COMMIT / ESCALATE` verdict — into
`client-level` `answer` mode, and make "account manager" an alias that routes there.

## What happened

- 2026-11-06 — Plan written. CEO and COO reviews ran independently. Verdict: MODIFY.
- 2026-11-06 — Operator said proceed. Worktree created. Build started: sec-level threat model, eng-level plan, then tests first, then the edits.
- 2026-11-07 — Threat model written (`.sec-level/threat-model.md`, SEC PASS at plan
  stage; the diff review is separate). Lifecycle run created
  (`.eng-level/runs/20261106T160037946415Z-0e243f3d-account-manager-verdict/`) with
  the upstream requirements and six pass tests. Tests written first and seen to fail.
  Then the edits: verdict table, three rules, and status shape in
  `skills/client-level/SKILL.md`; verdict line in the answer template; alias rows in
  `skills/c-level/SKILL.md` (locked OKR line untouched); the eval case extended with
  the partner-tool and track-record questions, kept inside `client-level.eval.md` so
  it stays in the five-file CI window; docs page, README row, decision record
  `docs/decisions/2026-11-07-answer-verdict-in-client-level.md`. Validate passes; the
  full suite passes; the eval still parses; the diff carries no real client name.
  Nothing committed.
- 2026-11-07 — Reviews on the real diff. Staff Engineer: APPROVED WITH CONDITIONS; two
  P1 text fixes ("four parts" said five; the plan file said both built and not built)
  and four P2 wording points, all fixed. Security (diff stage): SEC PASS; one S2, a
  too-close paraphrase of the July quote in this plan file, reworded. Tests rerun
  after the fixes: 110 OK; validate passes. Concurrent session check: the `sec-pen`
  branch (tip e7764d7) is separate work and is excluded from this landing; it lands
  by its own pull request. Final engineering decision: SHIP, recorded in the run's
  `decision.md`. No client reads this outcome, so no client-level handoff. The
  commit waits for the operator.
- 2026-11-07 — Operator clarified the real need: turn a client blocker into an offer of
  work, with a strategy and the sentence to send back (account manager + sales +
  fishing). Second review started on adding a `pitch` mode to `client-level`.
- 2026-11-07 — Operator asked to install locally. Ran the install step from this
  branch; all ten skills verified in the local skills folder, and the installed
  `client-level` carries the new verdict. Still nothing committed.
- 2026-11-07 — Pitch mode built. Lock test written first and seen to fail; then the
  mode row, the `## Mode: pitch` section, the pitch template, the alias row, the new
  eval case `evaluations/client-level-pitch.eval.md`, the CI cap raised to six with a
  note in `TODOS.md`, docs and README rows, and an addendum to the decision record.
- 2026-11-07 — Operator said "push the code". Verify step run: the repo's tests pass
  (111 OK), but the gstack checker reports NOT_READY because two generated lifecycle
  state files have no test lane in the pregate policy, and the checker reads that
  policy from `origin/main`. This branch maps the lifecycle folders in
  `.gstack/pregate.json`; it takes effect after merge. Committed (a26d82a), pushed, and
  pull request #35 opened.
- 2026-11-07 — Delta review of pitch mode: APPROVED WITH CONDITIONS. One P2: bare
  `sales` and `pitch` aliases would steal prompts like "sales dashboard" or "pitch
  deck", so they now route only when a client is the audience. One P3 taken: the cost
  rank in pitch mode must rest on a labelled fact. Follow-up commit pushed.
  Fix risk analysis — blast radius: the router alias table only. Not fixed: a bare
  "pitch" with no client in sight no longer routes to pitch mode; the operator says
  "fishing" or "can we offer" instead. Detection: the lock test checks the `fishing`
  alias still routes; nothing tests that bare `sales` stays out, so a later edit could
  put it back unnoticed. Rollback: revert the follow-up commit.
  Checked the COO's claims: the eval window (first five files by name, cap of five)
  is real; the `sec-pen` work in this tree is real and untouched by this task.

## Still unclear

- Whether the operator means "account manager" as (a) a client-commitment gate, as the
  July review described, or (b) something else, such as tracking accounts, renewals, or
  client health. The review assumes (a) because that is the only evidence in the repo.
  Only the operator can answer.
- Whether the `sec-pen` skill and this change ship in the same release. Two new eval
  files in one release both fall into the five-file CI window problem.

## Result

Verdict MODIFY, and the recommended option is built, tested, and pushed as pull request
#35 on branch `lz-account-manager-verdict`: the answer verdict, the three rules, and the status
shape in `skills/client-level/SKILL.md`; the alias rows; the extended eval case; docs;
lock tests; the decision record; and, after the operator's clarification, the `pitch`
mode with its template and eval case. Proof: the files named in "What happened", a passing
validate run, 110 passing tests, and the Staff Engineer and security reviews recorded
in the run's `decision.md`. Left out on purpose: a new skill, the version bump and
changelog (the ship step does those). The merge waits for the operator.
