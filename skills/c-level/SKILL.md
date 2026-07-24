---
name: c-level
description: Use when starting work that may involve product scope, feature planning, architecture, implementation, code review, portal/API/backend QA, release readiness, CEO/COO review, gstack review, or Superpowers workflows.
license: MIT
compatibility: Works with Agent Skills-compatible coding agents. Optional integrations require separately installed gstack and Superpowers skills.
metadata:
  author: ExecForge contributors
  version: "0.8.0"
---

# C Level

## Rule

Before acting, select the smallest applicable workflow. Do not inspect code, ask planning questions, or implement first and route later.

## Router

| Situation | Required workflow |
|---|---|
| Initiative must be governed end-to-end from idea to ship in one engagement | Use `full-cycle` |
| New product, feature, platform, automation, or unclear user need | Use `execforge` |
| Approved product scope needs UX/interface structure or production-oriented HTML/CSS guidance | Use `design-html`; forward `--design-system=<name\|auto\|none>` when the operator set one |
| Approved product/PRD needs engineering planning | Use `eng-level --mode=plan` |
| Triggered job is low-impact per the Ponytail fast path criteria below | Use `ponytail lite` fast path; user approval required before any commit |
| Implementation plan is approved and code work starts | Use the installed Superpowers execution skills |
| Existing branch needs final audit | Use `eng-level --mode=review` |
| Web portal/API/backend behavior needs test planning or execution | Use `q-level` |
| Change touches auth, user input, secrets, sensitive data, new dependencies, or network exposure | Attach `sec-level` (threat model at plan stage, security review at diff stage) |
| QA finds a code defect | Return to implementation, then retest |
| QA finds an architecture/integration defect | Return to `eng-level --mode=plan` |
| QA finds unclear or contradictory acceptance criteria | Return to `execforge` |
| Product assumption becomes invalid during implementation | Return to `execforge` |
| Architecture assumption becomes invalid during implementation | Return to `eng-level --mode=plan` |

## Ponytail fast path (optional)

`ponytail` is a third-party simplicity persona
(github.com/DietrichGebert/ponytail), vendored in this bundle as a pinned
verbatim copy (`skills/ponytail/`) — never fetched at runtime, never
auto-updated. When it is not installed, the fast-path row is inert and every
job uses the normal router rows. Installed, it sits at the
domain-implementation tier — below every workflow in this router — with its
pinned commit recorded in `skills/ponytail/PROVENANCE.md`.

A triggered job is **low-impact** only when ALL hold:

- Single repo, no cross-team or production architecture surface
- Reversible in one revert
- Touches no auth, secrets, trust-boundary input handling, schema or data
  migration, and adds no network exposure (otherwise attach `sec-level` and
  use the normal flow)
- Adds no new dependency
- Produces no governance gate output

Fast path procedure:

1. Invoke `ponytail lite` and implement the job.
2. Precedence: where ponytail conflicts with Superpowers
   `test-driven-development`, TDD wins — ponytail governs implementation
   style, never test discipline. Gate outputs are never shortened, skipped,
   or claimed without evidence.
3. When the operator has a pilot observation job configured, log the run
   (for example `.execforge/bin/ponytail-observe.sh record <task-slug> on`).
4. Present the diff summary to the user and ask for explicit approval
   BEFORE committing or claiming the job done. No approval, no commit.

Any doubt about impact means not low-impact: use the normal router rows.
Adoption governance, precedence rules, and kill triggers live in the
operator's ExecForge decision record for the ponytail initiative.

## Trigger aliases

Users do not type canonical skill names. Route these to the real skill without asking:

| What the user says | Route to |
|---|---|
| `product plan`, `c-plan`, `CEO plan`, `COO review`, `product review` | `execforge` |
| `eng-plan`, `eng plan`, `engineering review`, `tech review`, `CR review` | `eng-level` |
| `eng-lifecycle`, `eng-lifecyle`, `the lifecycle`, `full lifecycle`, `end to end` | `full-cycle` |
| `QA-level`, `QA plan`, `QA it`, `test it` | `q-level` |
| `designer`, `design plan`, `UI review`, `UX review` | `design-html` |
| `security review`, `threat model`, `pentest review` | `sec-level` |
| `exec-forge`, `excecforge`, `execforge lifecycle` | `execforge`, or `full-cycle` when the request spans build-to-ship |

Misspellings and casing variants of any skill name route to that skill. When a request names
several — "trigger product plan and eng-level" — run them in lifecycle order, not the order
spoken.

Do not ask the user to restate a request in canonical form.

## Roles inside eng-level

`eng-level` carries roles: `architect`, `manager`, `staff-engineer`, `backend-engineer`,
`platform-engineer`. Do not ask which one. Infer from the request and the change surface:
cost and capacity questions are `architect`; schema and query work is `backend-engineer`;
deploy, DNS, containers, and TLS are `platform-engineer`; tickets and sequencing are
`manager`; diff review is `staff-engineer`. Requests carrying several roles get all of them.

## Superpowers bridge

When Superpowers is installed, use its current skill instructions rather than memory.

Recommended mapping:

1. Product ambiguity: `execforge`; use Superpowers `brainstorming` only when design discovery is still required.
2. UI-facing scope translation: `design-html`, with `--design-system` forwarded when a visual language is required.
3. Approved technical design: Superpowers `using-git-worktrees`.
4. Atomic execution plan: Superpowers `writing-plans`.
5. Implementation: `subagent-driven-development` or `executing-plans`.
6. Every behavior change: `test-driven-development`.
7. Before completion claims: `verification-before-completion`.
8. Final branch handling: `finishing-a-development-branch`.
9. Final product-to-plan-to-diff audit: `eng-level --mode=review`.
10. Portal/API/backend quality gate: `q-level --mode=auto`.
11. If QA fixes change production code, run a final Staff Engineer delta review and QA retest.

## Priority

Direct user instructions override skills. ExecForge governance skills set decision boundaries. Superpowers process skills control implementation discipline. Domain skills perform the technical work.

## Stop conditions

Stop rather than guess when:

- The upstream product interpretation is not user-approved.
- A factual contradiction changes scope or safety.
- Required repository evidence is unavailable.
- A critical product, security, compliance, or data-integrity blocker remains.
- A lifecycle stage has not actually occurred.

Never claim a review, test, or approval that did not happen.
