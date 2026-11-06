# Sec Pen

`sec-pen` drives the open-source [Strix](https://github.com/usestrix/strix) AI
penetration-testing tool and folds its findings into the security review. It is a
bridge, not the tool: Strix is installed separately by the operator and needs Docker
and an LLM API key. When Strix is not installed, the skill is inert.

## What it is and is not

- It **produces evidence**. It never issues the `SEC PASS / FIX REQUIRED / BLOCK`
  verdict — `sec-level` and the lifecycle orchestrator own that.
- It **never runs without permission**. A pentest is `offensive-security` work, so it
  must clear the [Authorization gate](authorization-gate.md) with a human-recorded
  `AUTHORIZED` decision for the specific target before any run.
- It **never self-authorizes** and never widens the target beyond the authorized scope.

## The two hard gates

1. **Authorization.** A recorded `AUTHORIZED` decision with written authorization, the
   in-scope and out-of-scope targets, an expiry, the consent or legal basis, and
   captured-data handling. `NOT AUTHORIZED` stops the work.
2. **Data path.** Strix sends the target's code and traffic to the configured LLM
   provider. For a client, the provider and data path must be named in the engagement
   record and allowed by the contract before the run.

## Modes

| Mode | Use when | Output |
|---|---|---|
| `plan` | A pentest is proposed | A scoped run plan: target, authorization reference, model provider, and the exact command — nothing executed |
| `run` | Both gates are met | The ready-to-run command for an owned or written-permission target, and the `strix_runs/<run-name>` path to expect |
| `triage` | A `strix_runs` folder exists | Each finding deduplicated and labelled `OBSERVED` / `REPORTED` / `ASSUMED`, mapped to a `sec-level` finding — no verdict |

## Where it sits

```text
Authorization gate (AUTHORIZED)  →  sec-pen run  →  strix_runs/<name>
          →  sec-pen triage (evidence labels)  →  sec-level re-verifies + verdict
          →  client-level translates for the client
```

Strix is Apache-2.0. It tests only systems you own or have explicit written permission
to test.
