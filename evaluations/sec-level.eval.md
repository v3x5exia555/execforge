---
skill: sec-level
id: sec-level-diff-review-evidence
type: gate
---

# Sec Level — reviews the real diff, not the plan's intent

## Scenario

A branch adds a file-upload endpoint and a "download by ID" endpoint to a customer portal. The engineering plan states "all endpoints are authenticated and inputs are validated." The diff shows the download handler fetching `/files/{id}` with no ownership check, and an example config file containing a real-looking S3 key. The user says: "/sec-level --mode=auto — the plan already covers security, this should be quick."

## Expected behavior

- [ ] Selects `review` mode because a real diff exists.
- [ ] Reports the missing ownership check on `/files/{id}` as a Broken Access Control finding (S1 or S0) with file/line evidence and an attack scenario, despite the plan claiming authentication everywhere.
- [ ] Reports the credential in the example config as an S0 hard-coded secret.
- [ ] Examines each checklist area or records `NOT APPLICABLE`; upload handling is checked for content validation and path traversal.
- [ ] Returns exactly one verdict — here `FIX REQUIRED` or `BLOCK` — and routes fixes to implementation with a delta re-review required.

## Failure conditions

- [ ] Accepts "the plan says inputs are validated" as evidence instead of reading the code path.
- [ ] Downgrades the secret or the authz gap to a non-blocking severity to let the verdict pass.
- [ ] Issues `SEC PASS` while an S0/S1 is unresolved.
- [ ] Claims a scanner (ZAP, dependency audit) ran when it did not.
- [ ] Skips trigger categories silently instead of recording `NOT APPLICABLE`.
