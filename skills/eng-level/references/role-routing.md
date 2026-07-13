# Role Routing

Roles are inferred, not typed. `--role=auto` is the default. Users state intent in plain
words; the router selects the lens.

## Signal table

Use as a prior, not a regex. Classify intent, not tokens.

| Role | Request signals | Change-surface signals |
|---|---|---|
| `architect` | cost, scale, capacity, RAM/CPU sizing, "can it handle N users", trade-off, "which platform should we target", "is X enough" | no diff; a sizing or design question with nothing yet to review |
| `manager` | ticket, break down, tasks, roadmap, sequence, "what do I do next", "create the plan", "ensure the list is covered" | plan exists, no diff |
| `staff-engineer` | review, CR, PR, diff, "check the code", "is it ready", "before merge" | **a real diff exists** |
| `backend-engineer` | database, schema, index, query, migration, table, sync, "optimise the db", data integrity | diff touches migrations, schema, models, SQL, data-access code |
| `platform-engineer` | deploy, VPS, SSH, domain, DNS, DKIM/SPF/DMARC, docker, proxy config, TLS, port, "why can't access", "it's in spam", cron | diff touches Dockerfile, compose, proxy config, `.env`, CI, infra directories |

## Routing rules

1. **Return a set, not a value.** Requests routinely carry several roles at once. A request
   naming a database change under a memory constraint is `architect` and `backend-engineer`.
2. **Bias to the superset.** A missed lens ships a defect; an extra lens costs tokens. When
   genuinely ambiguous, attach both.
3. **Change surface overrides request wording.** If a real diff exists, `staff-engineer`
   attaches regardless of how the request was phrased.
4. **Temperament is inferred from the change, not the wording.** Pair a `purist` with the
   `pragmatist` when the change touches schema, migrations, money, identity resolution, or
   third-party evidence. Users do not think to ask for a purist; the router must supply one.
5. **Announce, do not ask.** Print the routed set and proceed. Accept a one-word correction.
   Do not open a confirmation gate.

## Announcement format

```text
Routing: backend-engineer + architect  (db schema + memory constraint)
Adversarial pair: ON  (migration detected)
→ override with one word if wrong
```

## Worked examples

| Request | Routed roles | Why |
|---|---|---|
| "see the db design and optimise it" | `backend-engineer` | schema/index intent, no diff |
| "review the cost and scale for me, i need domain and vps" | `architect` + `platform-engineer` | capacity is architectural; "domain and vps" is a platform signal. Superset rule: attach both rather than drop one. |
| "can it handle 1500 people?" | `architect` | scale ceiling |
| "set up the mail service, end to end process able to be run" | `platform-engineer` | deploy/ops intent |
| "why can't the site be accessed" | `platform-engineer` | availability, not code |
| "create the technical plan and tickets, ensure the list is covered" | `manager` | decomposition |
| "review this CR then QA it" | `staff-engineer` → `q-level` | diff exists |
| "improve the platform, and make sure the job only uses 1GB RAM" | `architect` + `backend-engineer` | constraint is architectural; the fix is in the data path |
| "the database is fine, but the server is down" | `platform-engineer` | intent-level: the defect is operational. Do **not** attach backend on the word "database". |
| "add a column and deploy it" | `backend-engineer` + `platform-engineer` (+ `purist` pair) | two surfaces; migration triggers the pair |

The last two are the router's real tests. Keyword matching fails both.

## Anti-pattern

Do not route on keyword presence. "Database" appearing in a sentence does not mean the
database is the subject. Read the request, decide what is actually being asked, and use the
table as a prior.
