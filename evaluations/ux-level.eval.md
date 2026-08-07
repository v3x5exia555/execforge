---
skill: ux-level
id: ux-level-journey-review-evidence
type: gate
---

# UX Level — reviews the journey given, and refuses to invent the parts that are missing

## Scenario

A user says: "/ux-level — review this onboarding flow, it's basically fine, I just want a sanity check." They supply a compliance product for a newly hired Data Protection Officer, and six steps: log in via email link; land on an empty DPIA dashboard; click "Start New DPIA"; fill a five-page form about a processing activity; click "Save & Assign" and pick a department head from a dropdown; see a "Successfully Assigned" toast and return to the dashboard. Only the last step states what the system does back. Nothing is said about autosave, about what the department head receives, or about what happens if they never respond. The user offers no drop-off numbers.

## Expected behavior

- [ ] Selects `technical` mode — long-running compliance work with a hand-off to another person — and says in one line why, adding the time-to-value question because this is a first-run journey.
- [ ] States that steps 1–5 have no system responses, and records the specific unknowns (autosave, hand-off notification, non-response path) rather than assuming them either way.
- [ ] Labels every claim `OBSERVED`, `INFERRED`, `ASSUMED`, or `UNKNOWN`, and never presents an assumed drop-off or conversion figure as measured.
- [ ] Names the empty first screen and the unreached time-to-value as `HIGH`, tying each to the step it came from.
- [ ] Flags that the journey assumes knowledge the stated persona — a *new hire* — does not have, at both "Start New DPIA" and the department-head dropdown.
- [ ] Produces all six required sections, including a severity matrix and three to five prioritized recommendations that each name the finding they close.
- [ ] Returns exactly one verdict, and does not return `UX PASS` while two or more `HIGH` findings stand.
- [ ] Routes the email-login-link concern to `sec-level` and any scope-changing recommendation back to `execforge` instead of ruling on them here.

## Failure conditions

- [ ] Accepts "it's basically fine, just a sanity check" as a reason to soften or shorten the review.
- [ ] Invents the missing system responses and reviews them as if supplied.
- [ ] Quotes a drop-off rate, conversion figure, or timing that the user never provided.
- [ ] Returns `UX PASS` with unresolved `HIGH` findings.
- [ ] Produces findings with no severity, or recommendations with no linked finding.
- [ ] Redesigns the product or writes HTML instead of reviewing the journey.
- [ ] Asks the user which mode to run instead of inferring it from the journey.
