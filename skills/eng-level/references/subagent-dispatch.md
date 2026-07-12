# Subagent Dispatch and Conflict Protocol

Two axes. Role decides what is examined. Temperament decides what counts as unacceptable.

| Axis | Values | Default |
|---|---|---|
| Role | `architect`, `manager`, `staff-engineer`, `backend-engineer`, `platform-engineer` | `auto` — see [role routing](role-routing.md) |
| Temperament | `pragmatist`, `purist` | `auto` — pair when the change is integrity-critical |

## When to dispatch

Dispatch subagents when both hold:

- Two or more roles have independent, non-overlapping scopes.
- The plan or diff is non-trivial.

Otherwise run in-line, single-threaded. A three-file change does not need four agents.

Dispatch an adversarial pair on the same scope when the change touches schema, migrations,
money, identity resolution, or data a third party relies on as evidence. Read
[the reviewer briefs](reviewer-briefs.md).

## Subagent contract

Each dispatched reviewer:

- Receives the approved upstream requirements, the plan, the diff, and its own scope only.
- Cites `file:line` for every claim about code.
- Labels each claim `FACT`, `INFERENCE`, or `UNKNOWN`.
- Never invents metrics.
- When paired, states where it expects its counterpart to disagree, and rebuts pre-emptively.
- Returns findings with severity `P0`–`P3`.

No subagent may issue a ship verdict. Findings go up; the orchestrator rules.

## Conflict protocol

When reviewers disagree:

1. **Reconcile by sequencing, not averaging.** Most disagreements are about order, not
   truth. A correctness demand and a shipping constraint usually resolve into one plan once
   ordered — the strict reviewer's shape on the pragmatic reviewer's timeline.
2. **Escalate only the irreducible.** Reconcile everything that reconciles. Hand the user
   the residue, and only the residue. One genuine taste call is a good outcome; five is a
   failure to reconcile.
3. **Never split the difference on correctness.** A defect is in scope because it is
   verified, not because two reviewers voted for it. A finding one reviewer missed is still
   a finding.
4. **Verify before adopting.** A finding raised by one reviewer is confirmed by the
   orchestrator against the code before it enters the action list.

## Action provenance

Mark every action in the resulting plan:

| Marker | Meaning |
|---|---|
| `[C]` | consensus — both reviewers agreed |
| `[R]` | resolved disagreement — reviewers differed; record the resolution |
| `[gate]` | blocked on an external dependency or an authorization flag |

Provenance makes the contested parts of a plan auditable. Report which actions carry `[R]`.

## Cost discipline

Subagents are not free. Do not dispatch a role whose surface the change does not touch. The
relevance test is the change itself — does the diff touch migrations, schema, or queries
(backend); container, proxy, DNS, CI, or secrets config (platform) — not whether a keyword
appeared in the request.

When relevance is genuinely ambiguous, attach the role. A missed lens ships a defect; an
extra lens costs tokens.
