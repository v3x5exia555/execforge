# Sec Level

`sec-level` is the application-security actor. It runs a **threat model** at plan stage and an **adversarial security review** against the real diff, issuing a `SEC PASS / FIX REQUIRED / BLOCK` verdict that the lifecycle orchestrator folds into the final ship decision.

## Why a dedicated actor

Security lines inside the COO controls and the Staff Engineer review describe *what* should be true; `sec-level` owns proving it against actual code. AI-generated code fails in predictable ways — missing input sanitization, absent authentication or authorization, hard-coded secrets, unrestricted backend access — so the review checks those hot spots first, then works through an OWASP Top 10:2025-mapped checklist.

## Modes

| Mode | Stage | Artifact |
|---|---|---|
| `threat-model` | plan, before implementation | `.sec-level/threat-model.md` |
| `review` | diff, with/after Staff Engineer review | `.sec-level/security-review.md` |
| `auto` | picked from lifecycle evidence | — |

## Attachment triggers

Attach `sec-level` when the change touches authentication/authorization/session/tenancy, user-controlled input reaching a parser/query/template/shell/renderer, secrets or credential storage, personal/financial/regulated data, new dependencies or build steps, or public network exposure. Otherwise record `SEC NOT APPLICABLE` with justification.

## Severity and verdicts

Findings use `S0`–`S3` (aligned with eng-level's `P0`–`P3`); an unresolved `S0`/`S1` blocks shipping exactly like a `P0`/`P1`. Each mode issues its own verdict — a passing threat model never carries over to the diff.

## References

- OWASP Top 10:2025 — https://owasp.org/Top10/2025/en/
- Skill definition: `skills/sec-level/SKILL.md`
