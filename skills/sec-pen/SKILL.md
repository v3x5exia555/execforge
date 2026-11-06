---
name: sec-pen
description: Use when an authorized penetration test should be run with the Strix AI pentest tool and its findings folded into the security review — preparing a gated run against an in-scope target, or triaging a completed Strix run into verified evidence for sec-level. Never issues the security verdict and never runs without a recorded AUTHORIZED decision.
license: MIT
compatibility: Bridges the separately installed, Apache-2.0 Strix tool (github.com/usestrix/strix), which requires Docker and an LLM API key. Inert when Strix is not installed. Produces evidence for sec-level; it does not grade findings or issue a ship verdict.
metadata:
  author: ExecForge contributors
  version: "0.1.0"
  role: offensive-security-operator
---

# Sec Pen

## Core principle

A penetration test is an adversarial operation against a running system. It is lawful
and safe only with documented permission and a defined scope. This skill drives one
specific tool — **Strix** — under that permission. It produces evidence; it never
decides whether the code is safe and never decides whether the operation was allowed.
Both of those are decided elsewhere.

## What Strix is

Strix (`github.com/usestrix/strix`, Apache-2.0) is an AI penetration-testing agent. It
runs a target dynamically, searches for vulnerabilities, and attempts to validate them
with proof-of-concept exploits inside a Docker sandbox. It takes a local directory, a
repository URL, a live URL, or an API specification as its target, and writes results
to `strix_runs/<run-name>`.

It is **not** vendored in this repository. It is installed separately by the operator
and needs Docker running and an LLM API key. When it is not installed, this skill is
inert: say that Strix is not present and stop.

## The two hard gates

Neither gate is one the agent may answer for itself.

1. **Authorization.** Strix is `offensive-security` work. It must clear the
   [Authorization / Rules-of-Engagement gate](https://github.com/v3x5exia555/execforge/blob/main/docs/authorization-gate.md) with a
   recorded `AUTHORIZED` decision before any run against any target. The decision is
   made by the human operator — written authorization from a party empowered to grant
   it, the in-scope and out-of-scope targets, a time window with an expiry, the consent
   or legal basis, and captured-data handling. `NOT AUTHORIZED` stops the initiative.
   An unresolved decision on this flagged work blocks shipping the same way an open P0
   does. A `sec-level` `SEC PASS` never substitutes for this decision, and this
   decision never substitutes for `sec-level`.

2. **Data path.** Strix sends the target's code and traffic to whatever LLM provider is
   configured (`STRIX_LLM` / `LLM_API_KEY`). For a paying client, the provider and the
   data path must be named in the authorization record, and the client's contract must
   allow it, before the run. The `client-level` rule against carrying one engagement's
   content into another applies to anything this skill captures.

If either gate is unmet, do not run. Say which gate is open and what is needed to close
it.

## Modes

Pick one. Infer it from the request; do not ask which.

| Mode | Use when | Output |
|---|---|---|
| `plan` | A pentest is proposed | A scoped run plan: the target, the authorization decision and its scope, the model provider and data path, and the exact Strix command — nothing executed yet |
| `run` | Both gates are met and the operator wants the run prepared | The ready-to-run command and its preconditions, for a target the operator owns or has written permission to test; the run folder path to expect |
| `triage` | A `strix_runs/<run-name>` folder exists | Each finding deduplicated, labelled with an evidence label, mapped to a `sec-level` finding — no verdict |

## Mode: plan

Produce, in order:

1. **Target** — exactly what is in scope, quoted from the authorization record, and
   what is explicitly out of scope.
2. **Authorization** — the `AUTHORIZED` decision reference, the granting party, and the
   expiry. If it is missing or expired, stop here and say so.
3. **Data path** — the model provider the run will use and confirmation the contract
   allows it.
4. **Command** — the exact invocation (for example `strix --target <in-scope-target>`),
   with headless `strix -n` noted when a non-interactive run is wanted.
5. **What this does not cover** — Strix tests what it reaches; name what stays out of
   its reach and still needs `sec-level`'s reading review.

## Mode: run

Only when both gates are met and the target is one the operator owns or has written
permission to test.

- State the preconditions you checked: Strix installed, Docker running, `AUTHORIZED`
  decision present and unexpired, target in scope, provider allowed.
- Give the exact command and the `strix_runs/<run-name>` path to expect.
- Do not widen the target beyond the authorized scope to make a command simpler.
- If a command fails because Strix changed, read the tool's current `strix --help`
  rather than repeating a stale command from this skill.

## Mode: triage

Read the completed `strix_runs/<run-name>` output and turn it into evidence `sec-level`
can use.

1. **Deduplicate** — collapse repeats and near-duplicates into one finding each.
2. **Label the basis** of every finding before it moves on:
   - `OBSERVED` — Strix reached it and showed it, with a proof-of-concept.
   - `REPORTED` — Strix flagged it but did not prove it; unverified.
   - `ASSUMED` — inferred to fill a gap; must be confirmed before anyone relies on it.
3. **Map** each to a `sec-level` finding with its evidence, the affected location, and
   Strix's CVSS / OWASP tag carried as input, not as the final severity.
4. **Hand off** to `sec-level` for re-verification. `sec-level` owns the severity and
   the `SEC PASS / FIX REQUIRED / BLOCK` verdict.

A `REPORTED` or `ASSUMED` item never reaches a client deliverable as established fact.

## What this skill never does

- It **never issues** the security verdict. `sec-level` and the lifecycle orchestrator
  (`eng-level` or `full-cycle`) do. This skill returns evidence.
- It never re-grades or softens a `sec-level` finding, and never raises one to sell
  work.
- It never self-answers the authorization decision or the data-path approval.
- It never runs against a target outside the authorized scope.
- It never translates findings for a client — `client-level` does that, after
  `sec-level` has verified them.

## Stop conditions

Stop and say why when:

- Strix is not installed, or Docker is not running.
- No `AUTHORIZED` decision exists for the target, or it has expired.
- The target is not clearly inside the authorized scope.
- The model provider or data path is not approved for a client target.
- You are asked to run against a system the operator neither owns nor has written
  permission to test.

## Boundaries

- `sec-pen` drives one tool and produces evidence. `sec-level` reviews code and owns the
  security verdict. The authorization gate decides whether the operation is allowed at
  all.
- Installing, updating, and configuring Strix is the operator's step, outside this repo.
- Rendering findings for a client is `client-level`, after `sec-level` verification.

## Detail

- [Authorization gate](https://github.com/v3x5exia555/execforge/blob/main/docs/authorization-gate.md)
- [Initiative flags](../execforge/references/initiative-flags.md)
