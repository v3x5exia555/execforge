---
skill: ux-level
id: ux-level-spec-mode-incomplete-spec
type: gate
---

# UX Level spec mode — finds the seeded gaps in an incomplete spec and refuses to pass it

## Scenario

A user says: "review this spec, I think it's ready for build." They supply a one-page
UI specification for a "client portal file-sharing report": a table screen listing
shared files with owner and link type; a filter bar; a detail drawer per file; and a
"Revoke link" button. The spec names the stack and states plainly that the portal is
server-rendered and reads only from a snapshot refreshed once per night, with no other
data path to the client's systems. It defines the table's populated state only —
nothing about the empty, loading, error, or no-permission states. The "Revoke link"
step says nothing about what happens when revocation fails or what the user sees
afterward. The acceptance criteria read "sharing report works correctly and is easy to
use". The target user is "the client". It also requires: "when a link is revoked, the
table row updates live within one second."

## Expected behavior

- [ ] Selects `spec` mode — a written document was supplied, not a walked journey — and says in one line why.
- [ ] Produces the seven-pillar completeness matrix with every cell cited to a spec section or marked absent.
- [ ] Names the missing screen states (empty / loading / error / no-permission) under state completeness, as findings rather than charitable omissions, and never stops to ask the user for them.
- [ ] Names the missing failure and recovery path for "Revoke link".
- [ ] Marks "the client" as not a persona under scope/target-user, and tenancy as unspecified — as `missing` findings, not questions back to the user.
- [ ] Flags "works correctly and is easy to use" as untestable acceptance criteria and states what a testable version would be.
- [ ] Flags the one-second live-update requirement as `contradictory` under feasibility, because the spec's own data path is a nightly snapshot with no other path to the source systems.
- [ ] Ranks findings `HIGH` / `MEDIUM` / `LOW`, returns exactly one verdict, and that verdict is `FIX REQUIRED` (or `REDESIGN` with the model-level reason) — never `SPEC PASS` while the seeded gaps stand.
- [ ] Describes the handoff without acting on it: fixes approved would go to `design-html`, a model-level failure back to `execforge` — and does not start building screens in this standalone review.

## Failure conditions

- [ ] Returns `SPEC PASS` or `UX PASS` on the spec as supplied.
- [ ] Invents the missing states or failure paths and reviews them as if written.
- [ ] Stops to ask the user for the missing persona, states, or screens instead of recording them as findings.
- [ ] Accepts "works correctly" as an acceptance criterion without a finding.
- [ ] Misses the contradiction between the nightly-snapshot-only data path and the one-second live-update requirement.
- [ ] Reviews it as a journey (step walk-through) instead of a document, or asks the user which mode to run.
- [ ] Produces findings without severity, or a matrix cell without a citation or an explicit absence.
- [ ] Redesigns the screens, writes HTML, or chains into `design-html` instead of reviewing the document.
