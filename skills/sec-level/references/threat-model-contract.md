# Threat Model Contract

Produced at plan stage, before implementation. Scope it to the change under review, not the whole system.

## Required content

1. **Assets** — data and capabilities worth attacking (credentials, PII, funds, admin functions, tokens, the build pipeline itself).
2. **Entry points** — every path attacker-controlled input can enter: endpoints, uploads, webhooks, headers, query parameters, message queues, imported files, third-party callbacks.
3. **Trust boundaries** — where the privilege or trust level changes: browser→API, API→database, service→service, user→admin, tenant→tenant, app→third-party.
4. **Threats by STRIDE** — for each boundary, consider Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Record only threats that are plausible for this change; do not pad.
5. **Controls** — for each recorded threat: the control, whether it already exists in the repository (cite where), and its gate: `BEFORE MVP` / `BEFORE PRODUCTION` / `BEFORE SCALE`.
6. **Assumptions and unknowns** — labelled explicitly. An unknown that affects an S0/S1-class threat blocks plan approval until resolved.

## Rules

- Reuse existing repository controls before inventing new ones; cite file paths for controls claimed to exist.
- A threat with no feasible attack path may be recorded `ACCEPTED` with a reason and an owner — silence is not acceptance.
- The threat model's entry-point list feeds `q-level` security scenarios; keep identifiers stable.

## Verdict

- `SEC PASS` — all recorded threats have controls or explicit accepted-risk entries.
- `FIX REQUIRED` — the plan must add controls before approval.
- `BLOCK` — a critical threat has no feasible control under the proposed architecture; return to engineering planning.
