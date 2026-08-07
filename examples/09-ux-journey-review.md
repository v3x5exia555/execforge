# Example 9 — UX Level Journey Review

## Mode and scope

Mode: `technical`. The product is a compliance dashboard with long-running assessment
work and a hand-off to another person, so the four pillars apply. The time-to-value
question from `product` mode is added because this is a first-run journey.

## Inputs used

- **Product context:** a compliance platform with Data Protection Officer (DPO) modules
  and Data Protection Impact Assessment (DPIA) dashboards.
- **Target user:** a newly hired DPO. New to this company's data landscape, and does
  not yet know which department owns which system.
- **Journey supplied:** six steps, user actions only. System responses were stated for
  step 6 alone.
- **Missing inputs:** what the system does at steps 1–5; what a DPIA record contains;
  whether the department head is already a user. These are marked `UNKNOWN` below.

## Journey breakdown

### Step 1 — User logs in for the first time via email link

- **System response:** not stated — `UNKNOWN`
- **Finding:** a first login by email link has no stated expiry, no resend path, and no
  fallback if the link is opened on a different device. `INFERRED`
- **Severity:** `MEDIUM`

### Step 2 — User lands on the main DPIA dashboard showing an empty state

- **Finding:** the first thing a new DPO sees is nothing. There is no orientation, no
  worked example, and no indication of what a finished DPIA looks like. `OBSERVED`
- **Severity:** `HIGH` — pillar 4, cognitive load. This is the moment the product has
  to teach, and it is spent on an empty screen.

### Step 3 — User clicks "Start New DPIA"

- **Finding:** the user is asked to assess a processing activity before they have been
  shown what activities exist in the company. A new hire cannot name one. `INFERRED`
- **Severity:** `HIGH` — the journey assumes knowledge the stated persona does not have.

### Step 4 — User fills out a 5-page form on the processing activity

- **System response:** not stated. Whether the form saves as you go is `UNKNOWN`.
- **Finding:** five pages with no stated autosave and no stated validation point. If
  validation happens at submit, a single bad field can cost the whole session.
  `INFERRED`
- **Severity:** `HIGH` — pillar 2, error prevention and recovery.
- **Finding:** no stated way to answer "I don't know" and come back. A DPIA routinely
  stalls on facts held by another team. `OBSERVED`
- **Severity:** `MEDIUM`

### Step 5 — User clicks "Save & Assign" and picks a department head from a dropdown

- **Finding:** the dropdown assumes the DPO knows which department head owns this
  system. For a new hire this is the hardest question in the journey, and it is
  presented as a routine field. `INFERRED`
- **Severity:** `HIGH` — pillar 4.
- **Finding:** nothing stated about what the department head receives, whether they have
  an account, or what happens if they never respond. A journey that depends on another
  person with no chase path is unfinished. `OBSERVED`
- **Severity:** `HIGH` — pillar 2.

### Step 6 — System shows "Successfully Assigned" and returns to the dashboard

- **Finding:** the toast is the only feedback, and it disappears. The user is returned
  to a dashboard that now shows one half-finished item with no stated status language.
  `OBSERVED`
- **Severity:** `MEDIUM` — pillar 1, system visibility.
- **Finding:** time-to-value is never reached. The user has done work and received no
  compliance insight. The product's promise — see your risk — has not been delivered
  once in six steps. `OBSERVED`
- **Severity:** `HIGH`

## Severity matrix

| # | Finding | Step | Pillar or criterion | Severity | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | No value delivered in the whole journey | 6 | Time-to-value | `HIGH` | `OBSERVED` |
| 2 | Empty first screen teaches nothing | 2 | 4 — cognitive load | `HIGH` | `OBSERVED` |
| 3 | Assumes knowledge a new hire lacks | 3, 5 | 4 — cognitive load | `HIGH` | `INFERRED` |
| 4 | Five-page form, autosave unknown | 4 | 2 — recovery | `HIGH` | `INFERRED` |
| 5 | Hand-off with no chase path | 5 | 2 — recovery | `HIGH` | `OBSERVED` |
| 6 | Assignment feedback is a vanishing toast | 6 | 1 — visibility | `MEDIUM` | `OBSERVED` |
| 7 | Login link has no stated recovery | 1 | 2 — recovery | `MEDIUM` | `INFERRED` |
| 8 | No "I don't know, come back later" path | 4 | 2 — recovery | `MEDIUM` | `OBSERVED` |

## Prioritized recommendations

1. **Give the empty dashboard a job.** Replace it with two or three pre-filled DPIA
   templates for common processing activities, plus one worked example marked as a
   sample. This closes findings 2 and 3, and turns the first screen from a blocker into
   the teaching moment. Rough cost: medium.
2. **Show risk before asking for work.** On first login, run whatever the platform
   already knows — connected systems, prior imports, sector defaults — and show a
   provisional risk view. The DPO sees value before filling anything in. Closes finding
   1. Rough cost: large; the strongest single change in this journey.
3. **Make the form survivable.** Autosave every page, validate each field as it is
   filled, and add an explicit "assign this section to someone else" action so an
   unknown fact does not stall the whole DPIA. Closes findings 4 and 8. Rough cost:
   medium.
4. **Give the hand-off a life of its own.** After assigning, show a tracked item with
   status, who holds it, when they were asked, and a reminder action. Replace the toast
   with a persistent row. Closes findings 5 and 6. Rough cost: medium.
5. **Suggest the department head instead of asking.** Rank the dropdown by system
   ownership the platform already holds, and let the DPO confirm rather than recall.
   Closes the rest of finding 3. Rough cost: small.

## Handed to other skills

- **`sec-level`:** the email login link — expiry, single use, and device binding.
- **`design-html`:** the reworked empty state and the tracked hand-off row.
- **`execforge`:** recommendation 2 changes what the product promises on day one and is
  a scope decision, not a UX tweak.

## Verdict

`REDESIGN` — the journey asks a brand-new DPO for expert knowledge before giving them
anything, and never delivers value in six steps. Fixing the form or the toast will not
save it; the first run has to start from what the platform already knows rather than
from an empty page.
