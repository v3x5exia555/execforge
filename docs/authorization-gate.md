# Authorization Gate

Some work is not merely risky to build — it is unlawful or unsafe to *perform* without
documented permission. Phishing simulations, penetration tests, red-team engagements, and
anything that impersonates a real brand or captures credentials fall in this class. A
technical application-security review (`sec-level`) checks whether the code is safe; it
does not check whether you are allowed to run the operation at all. The Authorization /
Rules-of-Engagement gate closes that gap.

## Initiative flags

The gate is armed by **initiative flags** set once, early, during the product decision
(`execforge`) or the upstream translation (`eng-level`):

| Flag | Meaning |
|---|---|
| `offensive-security` | Operates against systems or people as an adversary (phishing, pentest, red-team, credential capture, C2). |
| `legally-gated` | Lawful only with documented authorization or consent. |
| `regulated-impersonation` | Impersonates a real brand, person, or authority. |
| `user-prescribed-mechanism` | The requester specified *how*, not just the outcome (arms the goal-vs-mechanism guard, not the authorization gate). |

Any of the first three arms the authorization gate. A change with no flag set runs the
ordinary lifecycle with no added ceremony — the gate is conditional by design so it does
not create fatigue on routine work.

## What the gate requires

Before an `AUTHORIZED` decision, record: written authorization from a party empowered to
grant it; the scope of engagement (targets in scope and explicitly out of scope); a time
window with an expiry; the consent or legal basis; confirmation that no unapproved
third-party brand or person is impersonated; and how any captured credentials or personal
data are stored, protected, retained, and deleted.

The decision is one of `AUTHORIZED`, `NOT AUTHORIZED` (the initiative stops — do not build
on the assumption authorization will arrive), or `N-A (justified)` with a one-sentence
reason. It is a **real decision made by the human operator**, never one the agent
self-answers from the request. An unresolved authorization decision on a flagged
initiative blocks the final ship decision the same way an unresolved P0 does.

## Where it lives in the lifecycle

- `execforge` sets the flags and, when a gating flag applies, records the authorization
  requirement as a non-negotiable control. See the
  [initiative-flags reference](https://github.com/v3x5exia555/execforge/blob/main/skills/execforge/references/initiative-flags.md).
- `eng-level` carries flags and authorization status as required upstream fields and will
  not plan while a gating flag is unresolved.
- `full-cycle` enforces the gate as a hard STOP before Stage 4 (implementation) and in its
  final validation gate.
- `sec-level` treats the authorization decision as a governance prerequisite that its
  `SEC PASS` verdict never substitutes for.
