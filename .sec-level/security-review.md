# Security Review — answer verdict in client-level (diff stage)

- Branch: `lz-account-manager-verdict` vs `main` at 9bcd286
- Date: 2026-11-07
- Mode: review (a real diff existed)

## Trigger categories

| Category | Result |
|---|---|
| Secrets, credentials, tokens | Examined: grep over added lines and new files, zero hits |
| Auth, authz, network, dependencies | NOT APPLICABLE: markdown and tests only |
| User-controlled input reaching instructions | Examined: the "evidence, never instructions" guard is unchanged |
| Personal or regulated data | Examined: no client name; eval scenario uses no names |
| Run artifacts | Examined: state JSON and templates only |

## Controls from the threat model

| Control | Status |
|---|---|
| T1 client text is evidence | Present, unchanged |
| T2 every verdict states its labelled fact | Present (skill item 5, template, eval) |
| T3 no real client name or quote in tracked files | Present; one S2 paraphrase fixed |
| T4 DON'T COMMIT required and tested | Present (verdict table, new-promise check, eval, lock test) |
| T5 ownership and track-record rule | Present (skill rule, eval expected and failure items) |

## Findings

| ID | Severity | Finding | Action | Status |
|---|---|---|---|---|
| S2-1 | S2 | `plans/20261106_account-manager-skill.md` paraphrased the July quote with only the apostrophe changed | Reworded to "telling a client that a partner's platform is our own" | Fixed 2026-11-07 |
| S3-1 | S3 | Behavioural eval runs only when the CI secret is set | Operator confirms the secret or runs the eval once locally | Open, not blocking |

## Verdict

`SEC PASS`. No S0 or S1. The behavioural eval did not run here (no key); the lock test
covers the text and the eval covers behaviour when the secret is present.
