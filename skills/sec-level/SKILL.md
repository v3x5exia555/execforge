---
name: sec-level
description: Use when a planned or implemented change needs a threat model, an application-security review of real code, secrets/authz/injection scrutiny, or a SEC PASS / FIX REQUIRED / BLOCK security verdict before shipping.
license: MIT
compatibility: Reviews real diffs and configuration; requires a Git repository for diff review. Attaches to eng-level and q-level stages.
metadata:
  author: ExecForge contributors
  version: "0.7.0"
---

# Sec Level

## Core principle

Security findings come from the actual code, configuration, and data flow — never from the plan's stated intent. AI-generated code fails in predictable ways: missing input sanitization, absent or bypassable authentication, hard-coded secrets, and unrestricted backend access. Assume those defects exist until the evidence shows otherwise.

## Actor

The Security Reviewer is an adversarial specialist, not a checklist clerk. It reports findings with severity and evidence; only the invoking lifecycle orchestrator (eng-level or full-cycle) folds the security verdict into the final ship decision.

## Relationship to the authorization gate

`sec-level` answers "is the code safe?". It does not answer "are we allowed to do this at
all?". Offensive-security, legally-gated, or brand-impersonation work (phishing simulation,
pentest, red-team) must clear the separate Authorization / Rules-of-Engagement gate —
written authorization, scope of engagement, consent basis, no unapproved third-party
impersonation, captured-data handling — before implementation, governed by the initiative
flags set at the product/upstream stage. A `SEC PASS` never substitutes for that
authorization decision, and vice versa.

## Modes

- `threat-model` — run at plan stage, before implementation.
- `review` — run at diff stage, alongside or after the Staff Engineer review.
- `auto` — pick the mode from lifecycle evidence: no diff yet → `threat-model`; real diff exists → `review`.

## When Sec Level is required

Attach `sec-level` when the change touches any of:

- Authentication, authorization, session, or tenancy boundaries
- Handling of user-controlled input reaching a parser, query, template, shell, or renderer
- Secrets, keys, tokens, or credential storage
- Personal, financial, or regulated data
- New third-party dependencies, build steps, or supply-chain surface
- Public network exposure (new endpoint, webhook, CORS change, upload)

For changes touching none of these, record `SEC NOT APPLICABLE` with one sentence of justification instead of skipping silently.

## Threat model (plan stage)

Read [the threat model contract](references/threat-model-contract.md). Produce `.sec-level/threat-model.md` from [the template](assets/threat-model.template.md) covering assets, entry points, trust boundaries, STRIDE-classified threats, and required controls with their lifecycle gate (before MVP / before production / before scale). Unresolved critical threats block plan approval, not implementation review.

## Security review (diff stage)

Run only against a real diff with a known base. Read [the review checklist](references/security-review-checklist.md), which maps to OWASP Top 10:2025 plus AI-generated-code failure patterns. Inspect actual source, configuration, dependency manifests, and migrations. Record findings in `.sec-level/security-review.md` from [the template](assets/security-review.template.md).

Severity scale (aligned with eng-level):

- `S0` — exploitable now: secret in repo, authz bypass, injection on a reachable path. Blocks everything.
- `S1` — exploitable under realistic conditions; must fix before merge.
- `S2` — hardening gap with an owner and due condition.
- `S3` — defense-in-depth improvement.

Every finding needs evidence (file/line), an attack scenario, a required action, and a verification method. No finding may rest on "the plan says it is safe."

## Verdict

Return exactly one:

- `SEC PASS` — no unresolved S0/S1; S2 items owned.
- `FIX REQUIRED` — S1s exist; route to implementation, then re-review the delta.
- `BLOCK` — an S0 exists, required evidence is unavailable, or a control mandated by the threat model is missing with no safe fallback.

`SEC PASS` on a threat model does not carry over to the diff; each mode issues its own verdict.

## Lifecycle integration

- `eng-level --mode=plan`: attach `threat-model` before the plan verdict when the trigger list applies.
- `eng-level --mode=review`: attach `review`; an S0/S1 counts as a P0/P1 in the final engineering decision.
- `q-level`: security-relevant scenarios (authz boundaries, injection probes, ZAP routing) reference the threat model's entry points.
- QA-driven or security-driven fixes that change production code require a security delta re-review before `SHIP`.

## Validation gate

Before returning:

- The mode matched the lifecycle evidence (no diff review without a diff).
- Every trigger category was either examined or reported `NOT APPLICABLE`.
- Findings cite real files, lines, or configuration — not plan intent.
- No S0/S1 is downgraded to make a verdict pass.
- The verdict is traceable to the recorded artifacts.
- Never claim a scan, test, or review ran unless it actually ran.
