# Product Decision

Use `/execforge` before implementation when the user need, scope, economics, or risk is uncertain.

## Gatekeeper

> Does the end-user actually need this?

Outcomes:

- YES — continue.
- PARTIAL — reframe or reduce.
- NO — defer or kill.

## Scope modes

- Scope Expansion
- Selective Expansion
- Hold Scope
- Scope Reduction

## Verdicts

- GO
- GO WITH CONDITIONS
- MODIFY
- PILOT
- DEFER
- KILL

## New platform role baseline

Every new platform, portal, or tenant-facing system ships four roles, entered in the
scope ledger as ADD NOW:

- `superadmin` — the whole platform across accounts; platform operator only.
- `accountadmin` — one customer account end to end, including plan, billing, and admins.
- `admin` — one workspace or team inside an account.
- `user` — own work only.

Deny by default, audit-log every admin-level action, and attach `sec-level` because the
role model touches auth. Extra roles need evidence; dropping a baseline role needs a
recorded reason, owner, and date.

## Required evidence discipline

Label every material statement as FACT, ASSUMPTION, INFERENCE, or UNKNOWN.

See the skill references for contradiction and decision contracts.
