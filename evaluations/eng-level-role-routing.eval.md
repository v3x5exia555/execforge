---
skill: eng-level
id: eng-level-role-routing
type: routing
---

# Eng Level — routes roles from intent, without being told

## Scenario

The user never names a role and never passes a flag. Each request below is real phrasing.
The skill must infer the role set, announce it, and proceed.

| Request | Expected role set |
|---|---|
| "eng-level to see the db design and optimise it" | `backend-engineer` |
| "trigger eng-level for review the cost and scale for me, i need domain and vps" | `architect` |
| "can moodle and gophish handle 1500 of ppl using it?" | `architect` |
| "trigger eng-level to setup gophish, able to do the simulation, end to end process able to be run" | `platform-engineer` |
| "please check https://example.com why cant access, trigger eng-level" | `platform-engineer` |
| "trigger eng-level to create the technical plan and ticket, ensure the list is covered" | `manager` |
| "trigger eng-level to review this on this CR, then QA it" | `staff-engineer`, then `q-level` |
| "create me a plan to improve this platform, and make sure the scraper only use 1gb ram" | `architect` + `backend-engineer` |
| "the database is fine, but the server is down" | `platform-engineer` only |
| "add a column and deploy it" | `backend-engineer` + `platform-engineer`, adversarial pair ON |

## Expected behavior

- [ ] Infers the role set from the request and the change surface; never asks the user to name a role.
- [ ] Announces the routed set in one line and proceeds without a confirmation gate.
- [ ] Returns a set, not a single role, when the request carries several intents.
- [ ] Attaches `staff-engineer` whenever a real diff exists, regardless of how the request was phrased.
- [ ] Engages the adversarial `pragmatist`/`purist` pair when the change touches schema, migrations, money, identity resolution, or third-party evidence — without being asked.
- [ ] Attaches an extra role when relevance is genuinely ambiguous, rather than guessing a single one.
- [ ] Accepts a one-word correction to the routed set.

## Failure conditions

- [ ] Asks the user which role to use, or requires a `--role` flag to be typed.
- [ ] Routes on keyword presence: dispatches `backend-engineer` for "the database is fine, but the server is down".
- [ ] Picks exactly one role for a multi-intent request.
- [ ] Skips the adversarial pair on a migration because the user did not request one.
- [ ] Lets a dispatched subagent issue a SHIP verdict.
- [ ] Opens an `AskUserQuestion` confirmation gate for the routing decision.
