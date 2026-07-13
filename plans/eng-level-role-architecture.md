# Plan: ExecForge v0.8.0 — Role Architecture, Adversarial Review, and Brakes

**Status:** proposed, not implemented
**Evidence base:** 469 real prompts across 5 projects, extracted to `prompt-history/`
**Companion:** `prompt-history/SUMMARY.md` (findings) · this doc (the plan)

Every claim cites a real prompt as `file:line` into `prompt-history/`. Open them and check
me. Where I cite the hotel-webscrap run's own output, the path is into that repo.

---

## Contents

1. [Executive summary](#executive-summary) — what changes, in one page
2. [The diagnosis](#part-1--the-diagnosis-with-evidence) — five findings, with receipts
3. [The changes](#part-2--what-changes-why-and-how) — seven, each with why/how/evidence
4. [Rollout](#part-3--rollout)
5. [New actors: the potential](#part-4--new-actors-what-the-evidence-supports)

---

## Executive summary

`eng-level` is your most-triggered actor (41 calls). It was built to do **one** job — gate
a plan, then audit the diff that implements it. You call it for **five** jobs. Four don't
fit that lifecycle, so the skill either runs ceremony that doesn't apply or silently skips
its own gates.

The fix is not new skills. It's parameters:

| Parameter | Says | New? |
|---|---|---|
| `--mode` | *Where* in the lifecycle | exists |
| `--role` | *Which lens* is looking (architect, manager, staff, backend, platform) | **new — defaults to `auto`** |
| `--temperament` | *How hard it argues* (pragmatist ⟷ purist) | **new — defaults to `auto`** |
| `--stop-after` | *Where to halt* — a brake that survives a compaction | **new** |

**But the parameters are not the point — the router is.** In 469 prompts **you have never
typed a flag, not once** (the only `--` strings in the corpus are me explaining flags *to*
you). So every parameter above defaults to `auto` and is **inferred from how you actually
write** — *"eng-level to see the db design and optimise it"* → `backend-engineer`; *"review
the cost and scale"* → `architect`; *"setup gophish end to end"* → `platform-engineer`. A
design that requires you to type `--role=backend-engineer` would never be used. That's
**Change 0**, and it is the prerequisite for everything else in this document.

Plus three smaller structural fixes: a `POST-HOC REVIEW` verdict that makes "build first,
review after" visibly expensive; a durable KIV backlog; and auto-attaching `sec-level` when
initiative flags fire.

**The constraint that shaped every decision:** you typed bare **`proceed` 37 times.** It is
your single most common message. So *nothing below works by asking you more questions.*
Any proposal that depends on you reading a gate and answering thoughtfully is dead on
arrival — the evidence is unambiguous. Every change here either sharpens the review
*without* interrupting you, or makes a cost visible that is currently hidden.

---

## Part 1 — The diagnosis, with evidence

### Finding 1 — `eng-level` is silently doing five different jobs

Every distinct kind of request you routed to `eng-level`, with the receipt:

| What you actually asked | Where | The job it really is |
|---|---|---|
| *"trigger eng-level for review the cost and scale for me, i need domain and vps for gophish and moodle and orbixshield"* | `security:1940` | **Architect** — capacity + cost |
| *"can it handle 1500 of ppl using it?"* … *"if we go for KM4 i need to tune the serve… but go for KM8 no need so much"* | `security:1764, 1797` | **Architect** — scale ceiling |
| *"eng-level to see the db design and optimise it"* | `hotel:287` | **Backend engineer** — schema/index |
| *"trigger eng-plan"* + *"make sure the scaper only use 1gb ram of job"* | `hotel:29–31` | **Architect** (constraint) → **Backend** |
| *"trigger eng-level to setup gophish, i need to be complete by today, and able to do the simulation, and the end to end process able to be run"* | `security:404` | **Platform engineer** — deploy/ops |
| *"create the plan once we have vps and trigger eng-level for this"* — asked **3× in a row** | `security:413, 423, 432` | **Platform engineer** — infra plan |
| *"trigger eng-level for this to create the plan techinical plan and **ticket** for this ensure the list is covered"* | `security:1912` | **Engineering manager** — decomposition |
| *"trigger eng-level to review this on this CR, then QA it test it until fix"* | `security:1672` | **Staff engineer** ← the only one that fits |

Eight representative calls. **One** matches the job `eng-level` was designed for.

**Why this actually hurts.** `eng-level`'s lifecycle is `upstream → plan → implement →
staff review → QA → ship`, and its validation gate demands *"a real diff existed before
Staff review."* Ask it *"how much RAM for 1,500 users?"* and none of that exists — no diff,
no plan, no requirement to conform to. The skill has two bad options: run the ceremony
anyway (noise), or skip it. **It skipped.** The cost/scale answers came back as decent
engineering advice with *none* of ExecForge's evidence discipline attached — no
FACT/INFERENCE labels, no verdict, no conditions, no traceability. You got a chat, not a
gate.

### Finding 2 — Deployment and operations is an unowned surface

You never asked for a "platform engineer." But look at where the OrbixShield time went:

*"on the vps from hostinger, how to add domain?"* (`:143`) · *"can we use the same db mysql
instead of maria db"* (`:452`) · full DNS record tables pasted **three separate times**
(`:853`, `:934`, `:1406`) · *"Forbidden - referer invalid"* (`:1024`) · *"Invalid
Username/Password"* → *"still issue"* (`:1030`, `:1034`) · *"still at spam"* → *"still in
spam"* → *"i cant find it"* (`:1717`, `:1738`, `:1740`) · PTR/rDNS records (`:1690`).

And from that session's summary of what broke (`:1088–1103`):

- a **Caddyfile single-line syntax error that crash-looped the proxy and took the whole platform down**
- a **2048-bit DKIM key silently truncated** by Hostinger's DNS field (fix: regenerate at 1024)
- the **GoPhish DB going read-only** because `docker cp` wrote it as root
- **`wwwroot` set inside an `if HTTPS` branch** → Moodle 500

Read that list again. **Not one is a code defect.** They are all configuration,
infrastructure, and DNS — and every one was discovered by *hitting it in production*,
because no actor in ExecForge owns that surface. `eng-level` reviews **diffs**. Nobody
reviews a Caddyfile, a DKIM key length, or a container volume's ownership *before* it
ships.

This is why I add a fifth role you didn't ask for.

### Finding 3 — Dispatched subagents work; you already proved it

One prompt — *"trigger c-plan and full-cycle for this… eng-level to see the db design and
optimise it"* (`hotel:285–287`) — orchestrated `full-cycle → execforge → eng-level` and
dispatched **four subagents**:

```
CEO product review                    [product lens]
COO operations review                 [ops lens]
Eng reviewer A — pragmatist           [engineering, min-blast-radius temperament]
Eng reviewer B — architecture purist  [engineering, correctness temperament]
```

It produced `.execforge/{context,decision,upstream-approval}.md`,
`.eng-level/{db-redesign-plan,action-framework,implementation-actions-1-6}.md`, a 10-action
ordered framework — then wrote real code across `utils/database.py`, `utils/migrations.py`,
`scrapers/{agoda,booking}.py`, and three scripts.

The engineering quality is the best in the entire corpus: four scale walls **in the order
they fail**, an O(n²) sync loop (`database.py:601-609`), non-sargable `date(scraped_at)`
predicates silently disabling an index, a 5-column UNIQUE autoindex that is pure write
amplification *and* can't be dropped without a table rebuild, and an explicit flip
condition (*"if peak RSS > 2 GB post-compaction… the rebuild ships this cycle"*).

**None of that came from `eng-level`'s own logic. It came from subagents.** This plan makes
repeatable what you discovered by accident.

### Finding 4 — The mechanism is *temperament*, not domain — and this is the big one

Reviewers A and B were **not** split by domain (backend vs platform). They were split by
**temperament**, and given a brief that forced them to argue:

> *"You are Engineering Reviewer B in a two-reviewer 'agree-to-disagree' plan review. Your
> engineering temperament is CORRECTNESS / DATA-INTEGRITY / ARCHITECTURE PURIST… you must
> argue the correctness case hard with evidence. Be intellectually honest… Label claims
> FACT/INFERENCE/UNKNOWN. Do not invent metrics… **Where do you expect Reviewer A to
> disagree with you, and your pre-emptive rebuttal?**"*

That pairing paid for itself immediately. From `.eng-level/action-framework.md`:

> **Two NEW defects both surfaced / orchestrator VERIFIED (FACT)**
> - **D1 — Supabase mirror is content-corrupt.** …stamps every row sharing a `scraped_at`
>   with one record's hash → id↔content decorrelated. *The mirror is a read fallback.*
> - **D2 — Pickup revenue is overcounted.** …the same sold night summed once per hourly
>   run. **This inflates the enforcement figure.**

And in the disagreement table, against D1, **Reviewer A's column reads exactly two words:**

> **"Not raised."**

A single-lens review would have shipped a silent data-corruption defect **in a system whose
numbers feed government tax enforcement against named businesses.** The purist caught it
*because he was instructed to be a purist*. That is not a nice-to-have. That is the entire
return on this architecture.

**And the orchestrator did not average them.** It *sequenced* them:

> *"Split the difference by sequencing: ship identity+lineage+fixes this cycle; start
> `price_observations` as forward-only dual-write at cycle boundary… **This is B's
> non-big-bang shape on A's timeline.**"*
>
> *"Net: the two positions converge into ONE sequenced plan once ordered. The single
> residual taste call for the user is #1."*

Ten actions: **nine reconciled automatically, one** handed back to you. *That* is what a
gate should feel like to someone who types `proceed` 37 times — it does the reconciling and
spends your attention only on the irreducible call.

One more thing that run proved: **the `legally-gated` flag fired for real.** Action 8 is
marked `[gate]` — *"Blocked on real registry extract + legal basis (`legally-gated` flag)"*
— and it stayed blocked. The v0.7.0 flag machinery **works**. It just has to be wired to
fire without being asked (Change 6).

### Finding 5 — Two opposite failures: you under-brake, and you *can't* brake

**You under-brake.** Bare `proceed` — 37×. `APPROVE UPSTREAM` typed the instant the
interpretation prints (`:1351`). The gates aren't decision points; they're speed bumps.
And the dominant grammar of your prompts is *"do X **and** trigger eng-level for it"*
(`:52`, `:82`, `:180`, `:352`, `:373`, `:1341`) — the review wraps a decision already made.
Documented cost, from your own `skill-usage-feedback.md`: an entire sender-domain registry
(schema + API + UI + tests) was built, then reviewed, then judged as something that
shouldn't exist.

**But when you *do* want to brake, you have no way to say it.** You type it in prose,
against skills whose design goal is to drive to ship:

- *"create full plan for this, but **dont redeploy**, make it as **KIV** for next changes"* — `hotel:331`
- *"create one plan for this **but do not deploy**"* — `security:757`
- *"**wait let review first**"* — `security:615`, and **again at `:618`** (it didn't take the first time)
- *"**dont do first then**"* — `security:1811`
- *"do not approve/proceed to deployment"* — `security:1123`

And the damning admission, from that session's own summary at `:1103`:

> *"**User feedback pattern:** user reversed 'do not deploy' decisions multiple times."*

**A prose brake is not a brake.** It doesn't survive a compaction boundary and must be
re-asserted every turn.

The hotel-webscrap run demonstrates the whole problem in one sequence: `full-cycle` planned,
then **implemented and committed real code** — `626b167 feat(db): foundation hardening —
identity migrations, D1/D2 fixes, sargable reads` — and your very next message was the
handbrake, producing `5fbb805 docs(plan): KIV DB-foundation roadmap for next cycle (no
deploy)`. The brake worked — **but only because you were awake and watching at 1:30am.**

---

## Part 2 — What changes, why, and how

### Change 0 — **Role auto-detection** *(the prerequisite — without this, nothing else ships)*

**Why — a finding that nearly killed this plan.** I grepped all 469 prompts for any
explicit flag (`--mode`, `--role`, `--design-system`, anything). Result:

> **You have never typed a flag. Not once.** The only `--` strings in the entire corpus are
> *me*, explaining flags *to you* (`execforge.md:194–196`).

That is fatal to the naive design. `eng-level --role=backend-engineer` is a parameter you
would never type, so the roles would sit unused and the whole architecture would be dead
weight. **What you actually type is intent, in plain words:**

| What you type | Role it means |
|---|---|
| *"eng-level to see the **db design and optimise it**"* (`hotel:287`) | `backend-engineer` |
| *"eng-level for review the **cost and scale**"* (`security:1940`) | `architect` |
| *"eng-level to **setup gophish**… end to end process able to be run"* (`security:404`) | `platform-engineer` |
| *"eng-level… create the technical plan and **ticket**… ensure the list is covered"* (`security:1912`) | `manager` |
| *"eng-level to **review this on this CR**"* (`security:1672`) | `staff-engineer` |
| *"**why cant access**… trigger eng-level and QA-level"* (`hotel:6`) | `platform-engineer` |

So the role must be **inferred, and `auto` must be the default.** `--role=` remains
available as an override for the rare case you want to force a lens — but the design
assumes you will never use it, because the evidence says you won't.

**How — the router.** `eng-level --role=auto` (default) classifies intent from the prompt
plus repo context:

| Role | Prompt signals | Repo/context signals |
|---|---|---|
| `architect` | cost, scale, capacity, RAM, CPU, "can it handle N users", sizing, tradeoff, "which platform should we target", "is X enough" | no diff present; sizing question with no code to review |
| `manager` | ticket, break down, tasks, roadmap, sequence, "what do I do next", "ensure the list is covered", "create the plan" | plan exists, no diff |
| `staff-engineer` | review, CR, PR, diff, "check the code", "is it ready", "before merge" | **a real diff exists** |
| `backend-engineer` | db, database, schema, index, query, migration, table, sync, "optimise the db", data integrity | diff touches migrations, schema, models, SQL |
| `platform-engineer` | deploy, VPS, SSH, domain, DNS, DKIM/SPF/DMARC, docker, caddy/nginx, TLS, port, "why can't access", "it's in spam", server, cron | diff touches Dockerfile, compose, Caddyfile, `.env`, CI, infra dirs |

**Four rules that make it safe:**

1. **Bias to the superset, always.** The costs are asymmetric: a *missed* role costs a
   shipped defect (see D1 — "Not raised"); an *extra* role costs some tokens. When the
   signals are ambiguous, **run both lenses.** Never agonize over picking exactly one.
2. **Multi-intent is the norm, not the exception.** Your prompts routinely carry several
   roles at once — *"trigger c-plan and full-cycle for this… **eng-level to see the db
   design and optimise it**"* (`hotel:285–287`) is product **+** architect **+** backend, in
   one sentence. The router returns a **set**, not a single value. A router that picks one
   role from that prompt has already failed.
3. **Repo state overrides prompt words.** If a real diff exists, `staff-engineer` attaches
   regardless of what the prompt says. You cannot talk your way past a diff review by
   phrasing the request as a question.
4. **Temperament is inferred from the *change*, not the words.** The adversarial
   `pragmatist`+`purist` pair (Change 2) auto-engages when the diff or plan touches
   **migrations, schema, money/revenue fields, or data a third party relies on as
   evidence** — detected from the repo, not from how you phrased it. You will never think
   to ask for a purist. The hotel-webscrap run needed one and got it only because someone
   configured it by hand.

**Announce, don't ask.** The router prints one line and **proceeds**:

```
Routing: backend-engineer + architect  (db schema + 1GB constraint)
Adversarial pair: ON  (migration detected)
→ override with one word if wrong
```

**No `AskUserQuestion`. No confirmation gate.** With `proceed` appearing 37 times, a
question here would be answered `proceed` and would teach the router nothing. A printed
line you can correct with one word ("no, platform") is cheaper for you *and* gives an
honest correction signal. This is the same principle as Change 3 and Change 4: **make the
system's reasoning visible, never make the user adjudicate it.**

**Failure mode to design against.** The router must not become a keyword-matching toy that
sees "database" in *"the database is fine, but the VPS is down"* and dispatches a backend
engineer. Classification is **intent-level, not token-level** — the model reads the request
and decides, using the table as a prior rather than as a regex. And per rule 1, when it
genuinely can't tell, it runs both instead of guessing.

**New artifact:** `skills/eng-level/references/role-routing.md` — the signal table, the four
rules, and ~15 worked examples taken **verbatim from your real prompts** (they're the best
test set that exists, because they're the ones the router will actually see).

**Eval:** `evaluations/eng-level-routing.eval.md` — replay real prompts from
`prompt-history/`, assert the routed role set. This is the one eval in the whole plan with a
ground-truth dataset already sitting on disk.

### Change 0b — **The auto-chain**: roles attach to stages, they don't form a queue

**The ask:** *"if i wrote a prompt, trigger eng-level then u auto select the lifecycle
backend → architect → platform → manager → staff-engineer → platform."*

**The intent is exactly right** — one trigger, the whole chain runs, you never pick a role.
That is the only design consistent with 469 flagless prompts and 37 bare `proceed`s.

**The shape needs one correction.** That list flattens two axes into one queue. Roles are
**lenses**; the lifecycle already supplies the **stages**. Three problems follow from
flattening:

1. **`architect` must precede `backend`, not follow it.** Architecture decides the shape;
   backend implements *within* it. The chain as written builds the schema, then asks whether
   the schema was a good idea.
2. **At any one stage, the roles are looking at the same artifact — so they run in
   parallel, not in series.** Sequencing them makes each wait on the last for no gain.
   Parallel-then-reconcile is precisely what made the hotel-webscrap run work.
3. **Six agents on every prompt is expensive and dulls the signal.** A CSS change needs no
   backend engineer. A pure diff review needs no manager writing tickets.

**But you spotted the thing that matters: you listed `platform` twice.** That is *correct*,
and it's the whole insight — **the same role plays a different function at different
stages.** `platform-engineer` at plan time asks *"what's the deploy topology?"*; at review
time it asks *"did this diff change the Caddyfile or DKIM config safely?"* Same lens, two
jobs. Your chain is a flattened projection of a 2-D structure.

**The 2-D structure (this is what `--mode=auto` actually runs):**

| Stage | Roles that attach | How they run | Gate to pass |
|---|---|---|---|
| **1. Plan** | `architect` (always) · `manager` (always) · `backend` and/or `platform` **as consultants** *if the change touches their surface* | **Parallel**, then reconciled by sequencing (Change 2). Adversarial `purist` pair auto-engages if integrity-critical. | `PLAN READY` — every ticket has a pass test (Change 5) |
| **2. Implement** | `backend` and/or `platform` — here they **build**, not review | Sequential, per the plan's action order | tests green |
| **3. Review** | `staff-engineer` (always, whole branch) · `backend`/`platform` **re-attach as specialist reviewers on their own surface** | **Parallel**; staff-engineer merges | no unresolved P0/P1 |
| **4. QA** | `q-level` | — | `QA PASS` |
| **5. Ship** | orchestrator only | — | `SHIP` / `FIX` / `REPLAN` / `BLOCK` |

Read the `backend` and `platform` rows down the table: **each appears at plan (as an
advisor), at implement (as a builder), and at review (as an auditor).** That's your
"platform twice," generalized and put in the right places.

**Which roles attach is decided by the router (Change 0), not by you.** *"eng-level to see
the db design and optimise it"* → backend attaches at all three stages, platform at none.
*"trigger eng-level to setup gophish end to end"* → platform at all three, backend at none.
Neither prompt named a role. Neither needed to.

**Relevance gate — the roles are a superset, but not an indiscriminate one.** A role attaches
when the *change surface* touches it (repo signals: does the diff touch migrations/schema →
backend; Dockerfile/Caddyfile/DNS/CI → platform), **not** when a keyword appears in the
prompt. Rule from Change 0 still holds: when genuinely ambiguous, attach — a missed lens
costs a shipped defect, an extra lens costs tokens.

**What you see:**

```
eng-level --mode=auto  (routed: backend-engineer · adversarial pair ON)

  Stage 1  Plan      architect + manager + backend[advise]     ▸ 2 agents ∥, purist paired
  Stage 2  Implement backend[build]
  Stage 3  Review    staff-engineer + backend[audit]           ▸ 2 agents ∥
  Stage 4  QA        q-level
  Stage 5  Ship      → verdict

  → one word overrides any of it
```

One prompt in. Full chain out. No flags, no questions — and it stops wherever
`--stop-after` says (Change 4), which is how *"create full plan but dont redeploy, KIV"*
becomes a parameter instead of a sentence you have to keep repeating.

### Change 1 — `--role` parameter *(the structural fix — your idea)*

**Why:** Finding 1. Five jobs, one skill, one lifecycle that fits only one of them.

**How:** `--mode` and `--role` are orthogonal. Mode = *where in the lifecycle*. Role =
*which lens*.

| Role | Owns | Verdict it may issue | Born from |
|---|---|---|---|
| `architect` | System/data design, trade-offs, **capacity + cost sizing**, scale ceilings, failure ordering | `SOUND` / `SOUND WITH CONDITIONS` / `REDESIGN` / `UNVERIFIABLE` | `security:1764, 1797, 1940`; `hotel:31` |
| `manager` | Ticket decomposition, sequencing, dependencies, **per-ticket acceptance criteria**, blocked-on | `PLAN READY` / `PLAN INCOMPLETE` | `security:1912` |
| `staff-engineer` | Whole-branch diff review, conformance, P0–P3 | *(unchanged — today's behavior)* | `security:1672` |
| `backend-engineer` | Schema, queries, indexes, migrations, API contracts, idempotency, data integrity | findings → staff review | `hotel:287`; the D1/D2 defects |
| `platform-engineer` | Deploy topology, containers, reverse proxy, DNS/TLS/email auth, secrets placement, rollback, runbook | findings → staff review | Finding 2 — the entire ops failure list |

**Defaults preserve every existing call.** Non-negotiable: `c-level`, `full-cycle`, and the
eval cases all invoke `eng-level` today.

```
eng-level --mode=plan    (no role) → architect + manager     # that IS a plan
eng-level --mode=review  (no role) → staff-engineer          # today's behavior, unchanged
eng-level --mode=<x> --role=<r>    → that lens only
```

**Implementation shape** — the same trick as the `design-html --design-system=` flag you
already shipped: `--role` is a **runtime argument, not a new skill folder.** Therefore:

- `BUNDLED_SKILLS` in `execforge.py` — **untouched**
- `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` — **untouched**
- the validator's `manifest set == BUNDLED_SKILLS` assertion — **still passes**
- `eng-level.eval.md` — **still passes** (it exercises the no-role default path)

Files that change:
- `skills/eng-level/SKILL.md` — a `## Roles` section + routing table (~40 lines)
- `skills/eng-level/references/role-contracts.md` — **new**: per-role scope, required evidence, output schema, and what each role may **not** rule on
- `skills/eng-level/references/subagent-dispatch.md` — **new**: Change 2
- `skills/eng-level/references/reviewer-briefs.md` — **new**: Change 2
- `evaluations/eng-level-roles.eval.md` — **new**

### Change 2 — Subagent dispatch: **two axes**, and a conflict protocol

**Why:** Finding 4. My first draft of this plan had one axis (role). The finished
hotel-webscrap run proves that's half of it. The defects that mattered were found by
splitting **temperament** and forcing the halves to argue. *Role decides what you look at.
Temperament decides what you're willing to call a problem.*

| Axis | Values | Purpose |
|---|---|---|
| **Role** | `architect` · `manager` · `staff-engineer` · `backend-engineer` · `platform-engineer` | What surface is examined |
| **Temperament** | `pragmatist` (min blast radius, ship it) ⟷ `purist` (correctness, integrity, defensible schema) | What counts as unacceptable |

**Dispatch rules:**

- **Dispatch on role** when ≥2 roles have independent, non-overlapping scopes *and* the
  diff/plan is non-trivial. Otherwise run in-line. **A 3-file change does not need four agents.**
- **Dispatch as an adversarial pair** (`pragmatist` + `purist`, same scope) when the change
  touches **data integrity, money, migrations, or anything a third party relies on as
  evidence.** That is exactly the hotel-webscrap condition — and exactly where one lens failed.
- **Each subagent gets:** approved upstream requirements + plan + diff + **its own scope
  only.** Scope isolation is what keeps them sharp.
- **Each subagent must:** cite `file:line`; label every claim `FACT` / `INFERENCE` /
  `UNKNOWN`; **never invent metrics**; and when paired, answer *"where do you expect your
  counterpart to disagree, and what is your pre-emptive rebuttal?"*
- **No subagent may say SHIP.** Ever. They return findings; the orchestrator rules.

**Conflict protocol — reconcile, then escalate the remainder.** My first draft said
"surface disagreements, don't average them." Half right. The real run showed better:

1. **Reconcile by sequencing, not averaging.** Most disagreements are about *order*, not
   *truth* — *"B's non-big-bang shape on A's timeline"* dissolved 3 of 4 open questions with
   neither side conceding.
2. **Escalate only the irreducible.** Nine of ten actions reconciled; **one** taste call
   went to the user. That ratio is the target.
3. **Never split the difference on correctness.** D1 was in scope because it was *verified*,
   not because two agents voted.
4. **Mark provenance on every action:** `[C]` consensus · `[R]` resolved disagreement ·
   `[gate]` externally blocked. You can then see at a glance which parts were contested —
   and audit precisely those.

**New artifact:** `skills/eng-level/references/reviewer-briefs.md`, holding the pragmatist
and purist briefs **verbatim** from the run that worked. Do not paraphrase them — the
adversarial framing *is* the mechanism.

> This is the highest-value item in the plan, and the one I would have gotten **wrong** if
> that run hadn't finished while I was writing.

### Change 3 — `POST-HOC REVIEW` verdict

**Why:** Finding 5, first half. "Build first, review after" is your default, and it has
already cost you a whole feature. Asking you to change the habit *has been tried* — it is
item #1 in your own `skill-usage-feedback.md` — and it did not take. **So change the tool,
not the user.**

**How:** when `eng-level --mode=review` finds a substantial diff but **no approved
`.eng-level/upstream-requirements.md`**, it labels the run `POST-HOC REVIEW` and:

- may issue `FIX` / `BLOCK` normally;
- **may not issue `SHIP`** — the ceiling becomes `SHIP WITH REQUIRED FIXES (UNGATED)`;
- prints a short *"what a plan review would have asked before this was built"* section.

**Zero new stops.** It doesn't block you and doesn't ask a question you'd `proceed` past. It
makes the cost of skipping the gate **visible in the output** instead of invisible. Given
the evidence, that is the only intervention style that will work on you.

### Change 4 — `--stop-after=` and a durable KIV backlog

**Why:** Finding 5, second half. The brake exists only in prose, and prose brakes get
reversed.

**How:**

1. **`--stop-after=<product|plan|implement|review|qa>`** on `full-cycle` and `eng-level`.
   The chain runs and **halts at that boundary**, emitting artifacts, executing nothing
   beyond it. A parameter survives a compaction; a sentence does not.
2. **A durable KIV backlog: `.eng-level/backlog.md`.** Deferred work must land in a
   *resumable* artifact, not a commit message nobody re-reads. **You don't need to design
   the format — the hotel-webscrap run already invented it, ad hoc:**

   | Marker it improvised | Meaning |
   |---|---|
   | `Cycle: Now` | ship this cycle |
   | `Cycle: Boundary` | starts at cycle edge — the one user taste call |
   | `Cycle: Next` | **KIV** — literally what you asked for |
   | `[gate]` | blocked externally (`legally-gated`, real registry data) |
   | `[C]` / `[R]` | consensus / resolved-disagreement provenance |

   Actions 9 and 10 were **already** tagged `Next`. The framework produced your KIV list
   before you asked for it — it just had nowhere durable to put it.
3. **`--mode=status` reads the backlog**, so *"what did we park, why, and what unblocks it?"*
   is answerable next cycle. A parked plan nobody can find isn't parked; it's lost.

**Note the deliberate asymmetry.** `proceed` stays cheap (I am not adding a gate you'll
rubber-stamp). But **stopping becomes cheap too, and durable.** Today the tooling makes
going forward frictionless and stopping expensive. For someone shipping to real clients off
a live VPS, that is backwards.

### Change 5 — `manager` refuses tickets without a pass test

**Why:** *"test it until is fix"* appears **12×** — `:52`, `:91`, `:404`, `:588`, `:1016`,
`:1672` — almost never with a pass criterion. The spam saga is the case study: "fixed"
could have meant *accepted by the MTA* (it was — `250 OK`), *delivered* (it was), or *not in
the spam folder* (it wasn't — `:1717`, `:1738`). Three different projects, one word. You
burned ~6 iterations on the wrong one.

**How:** v0.7.0 already put acceptance criteria in the upstream contract, but nothing
*enforces* it. The `manager` role's `PLAN READY` verdict becomes **conditional on every
ticket carrying a binary pass test.** No pass test → `PLAN INCOMPLETE`, with the missing
tests listed. Enforcement lives where tickets are written — the only place it can bite.

### Change 6 — auto-attach `sec-level` on initiative flags

**Why:** `sec-level` was triggered **once in 469 prompts** — on a security product, while
you deployed phishing infrastructure, exposed an admin console on a sending domain, and
spread API keys across servers. It is the clearest "should have used it, didn't" gap in the
corpus, and it's already flagged in your own feedback doc.

**How:** `full-cycle` already computes initiative flags (`offensive-security`,
`legally-gated`, `regulated-impersonation`). When one fires, `sec-level` **attaches
automatically** — threat model at plan stage, security review at diff stage. Not offered.
Not asked. Attached. **The machinery is proven to work** — `legally-gated` correctly blocked
Action 8 in the hotel-webscrap run. It just needs to fire unprompted.

### Change 7 — trigger aliases in `c-level`

**Why:** you consistently type names that don't exist: `product plan` (`:52`), `c-plan`
(`hotel:279`), `QA-level` (`hotel:6`), `eng-lifecyle` (`:429`), `eng-plan` (`hotel:31`),
`designer` (`code-ai-monitor:25`), `excecforge` (`:101`), `exec-forge` (`:1390`). The router
usually recovers. **Usually is not a contract.**

**How:** an alias table in `c-level/SKILL.md` mapping your real vocabulary → the real skill.
One hour. Cheapest item here.

---

## Part 3 — Rollout

| Phase | Work | Risk |
|---|---|---|
| **1** | **Adversarial pair + conflict protocol** (`reviewer-briefs.md`, `subagent-dispatch.md`) | Low — additive, and *already validated by a real run* |
| **2** | **Role auto-router** (`role-routing.md` + `eng-level-routing.eval.md`) — Change 0 | Medium — it's a classifier, so it *will* misroute sometimes. Mitigated by superset bias + one-word override. **Ships with the role split, never after it** — roles without the router are unusable. |
| **2** | `--role` + `role-contracts.md`; defaults preserve all current behavior | Low — purely additive |
| **3** | `POST-HOC REVIEW` verdict | Low — new verdict value; existing ones unchanged |
| **4** | `--stop-after=` + `.eng-level/backlog.md` | Low — additive; schema already prototyped |
| **5** | `manager` pass-test enforcement | **Medium** — will fail plans that used to pass. *That is the point.* |
| **6** | `sec-level` auto-attach | Low — reuses flags that already fire correctly |
| **7** | `c-level` alias table | None |

**Phase 1 is first, deliberately.** In my first draft the role split was the headline. The
finished run reordered it: the adversarial pair is the piece with **demonstrated** return
(two verified defects a single lens missed), and it's independent of the role work. **Ship
what's proven before what's designed.**

**Validation before release:** `python execforge.py validate` passes unchanged; existing
`eng-level.eval.md`, `full-cycle.eval.md`, `design-html*.eval.md` pass **untouched**; new
`eng-level-roles.eval.md` covers each role, one dispatch case, and one adversarial-pair case
asserting the conflict protocol.

**Version:** v0.8.0 — additive parameters, no breaking change to the skill contract.

---

## Part 4 — New actors: what the evidence supports

You've asked about this twice, so let me give it the space it deserves. The thing to get
right **first** is the distinction, because it determines every subsequent answer:

> **A role is a lens inside an existing decision.**
> **An actor is a different *kind* of decision — with its own verdict vocabulary and its own
> authority to stop the line.**
>
> `backend-engineer` finds an index defect → that's a **finding**, and it flows up into a
> staff-engineer verdict. It is a **role**.
>
> `sec-level` can say **BLOCK** and mean it — nobody overrules it on security grounds. Its
> verdict vocabulary is its own. It is an **actor**.

**The test:** *Can it say a word that no one else is allowed to overrule?* If yes → actor.
If it only produces findings that feed someone else's verdict → role.

Applying it:

| Candidate | Role or actor? | Reasoning |
|---|---|---|
| `architect`, `manager`, `staff-engineer`, `backend-engineer` | **Roles** | All four feed one engineering decision. Ship as `--role`. |
| `platform-engineer` | **Role now → actor later** | Today it feeds the ship verdict. But watch Finding 2: if deploy/ops keeps generating its *own class* of failure (proxy down, DKIM truncated, DB read-only) it will eventually need authority to say **NO-GO on deploy** independently of whether the code is good. That's an actor. **Ship it as a role; promote it when it earns the veto. This is the most likely next actor in the repo.** |
| `account-manager` | **A genuine actor gap — the only one the evidence supports** | See below. |
| `finops` / cost | **No — fold into `architect`** | Cost and capacity are one conversation (*"how much will be the cost"* arrives *inside* the sizing thread at `:1782`). Splitting them forces two agents to re-derive the same workload model. |
| `data-level` | **Not yet** | One project (hotel-webscrap) generated real data-engineering depth. One project is a role, not an actor. Revisit if a second appears. |

### The one real actor gap: `account-manager`

~15 prompts have **no home** in the current bundle:

- the Pharmaniaga clarification prep (`security:1814–1819`)
- *"how to deflect question if they ask - have u done similar campaign before"* (`:1825`)
- *"the currently the one that we share to them is our parthner one right? **Nop, we say its ours.** For smaller campaign and testing. If more departments and more staff, we say we use our partner"* (`:1880`)
- *"Also last meeting the tech guy ask about templates how many templates and what platform we use — **make it a stragy to answer the question**"* (`:1869`)
- *"create a design for our platform to consume… **trigger c-level plan and account manager role for this**, if such question being ask"* (`:1893`) ← **you literally asked for this actor by name**

This is a different **decision type** (what do we tell the client, what do we commit to,
what do we decline to answer) with a different **verdict vocabulary** (`SAY` / `DON'T SAY` /
`DON'T COMMIT` / `ESCALATE`). It does not belong in `c-level`; it landed there because there
was nowhere else.

**One caution, stated plainly.** Some of that material shades from *positioning* into
*misrepresenting who built and operates the platform* — `:1880` is explicit about it. If you
build this actor, its most valuable function is not helping you answer smoothly; it's the
**`DON'T COMMIT`** verdict — flagging when an answer creates a delivery obligation or a
factual claim you can't defend under a follow-up. A client-facing actor that only optimizes
for *sounding good* will eventually walk you into a commitment you can't honor, in a
security engagement, in writing. That's the failure mode worth designing against.

### The honest read on adding actors at all

The repo has **seven** skills and the router already needs an alias table (Change 7)
*because you can't reliably remember their names.* Actor count is not free: every new one is
another route `c-level` must get right, and another name you must recall under time
pressure, at 1am, mid-demo.

**`--role` is the right shape for four of the five things you proposed precisely because it
adds power without adding a name to remember.**

**Recommendation:** ship the roles. Let `platform-engineer` prove itself against the next
deployment. Then build `account-manager` — it's the only new *actor* the evidence actually
supports, and you asked for it by name.
