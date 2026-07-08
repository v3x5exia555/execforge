# Initiative Flags

Initiative flags are named attributes set once, early (product decision or upstream
translation), that arm conditional governance gates downstream. A change with no flag set
runs the ordinary lifecycle with no extra ceremony. Flags exist so that high-consequence
work — offensive-security engagements, legally-gated operations, brand impersonation, and
requests that prescribe a mechanism — cannot slip through as if it were a routine change.

Set flags explicitly. Record each as present or `not set`. Never leave a flag unstated for
qualifying work; an unstated gating flag is treated as unresolved and blocks progress.

## Flag catalog (v1)

| Flag | Set it when | Arms |
|---|---|---|
| `offensive-security` | The work operates against systems or people the way an adversary would: phishing simulation, pentest, red-team, credential capture, C2, exploit delivery. | Authorization / Rules-of-Engagement gate |
| `legally-gated` | The work is lawful only with documented authorization or consent (simulated phishing of employees, testing systems you do not own, processing regulated data for a new purpose). | Authorization / Rules-of-Engagement gate |
| `regulated-impersonation` | The work impersonates a real brand, person, or authority (lookalike sender domains, cloned login pages, spoofed internal notices). | Authorization / Rules-of-Engagement gate |
| `user-prescribed-mechanism` | The requester specified *how* to solve the problem, not just the outcome to achieve. | Goal-vs-mechanism guard |

Any of the first three arms the Authorization / Rules-of-Engagement gate. The fourth arms
the goal-vs-mechanism guard. Flags are not mutually exclusive.

## Authorization / Rules-of-Engagement gate

When any of `offensive-security`, `legally-gated`, or `regulated-impersonation` is set, the
initiative cannot proceed to implementation until an authorization decision is recorded.
This is a governance gate distinct from the technical application-security review that
`sec-level` performs — appsec asks "is the code safe?", this gate asks "are we allowed to
do this at all, and under what limits?".

Required evidence before an `AUTHORIZED` decision:

- **Written authorization** from a party with the authority to grant it, naming the
  operator and the sponsoring organization.
- **Scope of engagement**: which targets, domains, mailboxes, systems, or populations are
  in scope, and — explicitly — what is out of scope.
- **Time window**: when the engagement may run, and when authorization expires.
- **Consent / legal basis**: the basis for acting on the targets (employment agreement,
  signed engagement contract, regulatory allowance). Note jurisdiction if relevant.
- **No unapproved third-party impersonation**: any impersonated brand/person is either the
  sponsoring org's own or covered by explicit permission. Third-party brand impersonation
  without permission is out of scope by default.
- **Captured-data handling**: for anything that could capture credentials or personal
  data — where it is stored, who can access it, how it is protected, and its retention and
  deletion schedule.

The decision is one of:

- `AUTHORIZED` — all required evidence present; record it and the granting party.
- `NOT AUTHORIZED` — evidence missing or refused; the initiative stops (return to Stage 0
  or halt). Do not proceed to build on the assumption authorization will arrive.
- `N-A (justified)` — a gating flag was considered but does not truly apply; record one
  sentence of justification.

This gate is a **real, recorded decision made by the human operator**, never one the agent
self-answers from enthusiasm in the request. Treat "the user asked me to build the
phishing tool" as a request, not as authorization. An unresolved authorization decision on
a flagged initiative blocks the final ship decision the same way an unresolved P0 does.

### Authorization record format

```text
Initiative:            <name>
Flags set:             offensive-security | legally-gated | regulated-impersonation
Authorizing party:     <name, role, org>
Scope (in / out):      <targets in scope> / <explicitly out of scope>
Time window:           <start> to <expiry>
Consent / legal basis: <basis>
Third-party impersonation: none | <permitted, with evidence>
Captured-data handling: <storage, access, retention, deletion>
Decision:              AUTHORIZED | NOT AUTHORIZED | N-A (justified: <reason>)
Recorded by:           <operator> on <date>
```

## Goal-vs-mechanism guard

When `user-prescribed-mechanism` is set, separate the outcome the requester wants from the
mechanism they named, and state both. The review evaluates the *outcome + constraints* and
is free to redirect to a different mechanism when the prescribed one does not serve the
outcome — or is not the root cause.

Record a line in the scope ledger:

```text
Requested mechanism: <what the user said to do>
Underlying goal:     <the outcome + constraints>
Assessment:          mechanism serves the goal | redirect recommended: <alternative + why>
```

Prescribing a mechanism is not wrong — but do not let it foreclose diagnosis. The
retrospective example: "improve the email HTML to avoid spam" (mechanism) when the outcome
was "new recipients don't get spam" and the root cause was sender reputation, not HTML.
Leading with the goal let the review reach the correct fix.
