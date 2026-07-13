# ExecForge Product Decision — Evidence Bridges & Executable Evals (v0.9.0 candidate)

Run date: 2026-07-13
Execution mode: Single isolated review (Markdown + CI-workflow changes, reversible per
file via `git revert`; no production architecture, data store, or hard vendor). CEO and
COO lenses applied inline by the orchestrator, per the v0.7.0 precedent. The one new
operational surface — API spend for CI evals — is carried as a COO control below.

Initiative flags: `offensive-security` NOT SET · `legally-gated` NOT SET ·
`regulated-impersonation` NOT SET · `user-prescribed-mechanism` NOT SET (mechanism was
agent-proposed from a repo comparison and operator-endorsed; goal and mechanism align).
No authorization gate applies.

## 1. Initiative

Close the gap between what ExecForge's skills claim and what they can prove, using two
levers: (a) execute the existing behavioral evals instead of only documenting them, and
(b) bridge the QA / ship / security stages to the operator's installed gstack tooling so
verdicts are backed by driven evidence instead of code-reading.

Target user: the operator running ExecForge governance over real client deliverables —
concretely the login-gated portals (DataRex/PDPA, security-awareness reporting platform,
portal-template) and the hotel-webscrap dashboard, all deployed to Hostinger. gstack
v1.60.x is already vendored in DPO_senthion, so the bridge targets an installed tool.

## 2. Gatekeeper verdict — PARTIAL → reduce scope

Does the operator need everything from the gstack gap analysis? No. Item by item:

| Candidate | Pain evidence | Verdict |
|---|---|---|
| Executable eval harness in CI | **Fact** (2026-07-13 file reads): 11 `.eval.md` cases exist; CI runs structure checks only. Commit 98db516 hand-fixed a doc-vs-code drift bug — the exact class a harness catches. Roadmap already lists this near-term. | IN |
| q-level → gstack `/qa`+`/browse` routing | **Fact**: q-level demands cross-layer evidence with no mechanism; all four governed projects are login-gated web UIs; `references/tool-routing.md` is the designed extension point. | IN |
| eng-level SHIP → gstack deploy handoff | **Inference**: three divergent `deploy-hostinger.sh` copies exist; lifecycle currently ends at a SHIP verdict with no handoff. Light doc bridge only. | IN (light) |
| sec-level → gstack `/cso` as evidence tool | sec-level already reviews code; `/cso` adds runtime probing. Cheap one-line routing note. | IN (light) |
| Version gate + `v.1.0.0` tag cleanup | **Fact**: typo tag `v.1.0.0` exists; nothing checks tag ↔ CHANGELOG consistency. | IN (light) |
| Repo hygiene: gitignore `__pycache__`, `site/` | **Fact**: build output and bytecode are committed. | IN (light) |
| Retro/learn skill, decision-log/gbrain cross-project memory | Pain is real but diffuse; gstack provides these directly when installed. | DEFER |
| Rebuilding any gstack runtime (browser daemon, deploy scripts, analytics) | Negative value: duplicates a maintained upstream. | SKIP |

## 3. CEO finding (product lens)

- Job-to-be-done: the operator wants a QA PASS / SHIP / SEC verdict he can show a client,
  backed by evidence the agent actually produced.
- The 10× item is the **executable eval harness**: it converts the whole skill system from
  "documented behavior" to "pinned behavior," enforcing the repo's own core principle
  ("plan intent is not implementation evidence") on itself. Every future skill edit gets
  regression coverage for free.
- The bridges are cheap distribution wins: ExecForge stays the governance front door
  (its authorization gate has no gstack equivalent) while gstack supplies the hands.
  Positioning: govern with ExecForge, execute with gstack — complementary, not competing.
- Non-goal: making gstack a hard dependency. Every bridge must degrade to the current
  fallback contract when gstack is absent, or ExecForge loses its zero-dependency
  install story (its main differentiator).

## 4. COO finding (operations lens)

- Cost: Markdown edits ≈ zero. The eval harness adds CI API spend — bounded by: run the
  gate tier only when `skills/**` or `evaluations/**` change; use the cheapest capable
  model; cap cases per run; full matrix behind `workflow_dispatch`. Requires an
  `ANTHROPIC_API_KEY` repo secret (least-privilege, spend-capped key).
- Reliability: agent-driven evals can flake. Control: land the harness as **advisory
  (non-blocking)** first; promote to a required check only after a quiet week.
- Bridge risk: gstack moves fast (v1.60.x, near-daily commits). Pin the bridge contract
  to skill *names* (`/qa`, `/browse`, `/land-and-deploy`, `/cso`) not internals, and keep
  the fallback path authoritative.
- Tag cleanup: deleting/re-pushing a remote tag is history-visible; do it once,
  deliberately, with the operator watching.
- Ownership: solo maintainer; per-file rollback; no new data or service of record.

## 5. Contradiction register

- None factual. One tension resolved strategically: "bridge to gstack" vs "zero
  dependencies" — resolved by making every bridge conditional on gstack being installed,
  with the existing fallback contracts unchanged (CEO non-goal, COO control).

## 6. Final scope ledger

- **ADD** — Executable eval harness: a runner that executes `evaluations/*.eval.md`
  cases headlessly and asserts required behaviors; CI job (advisory at first) triggered
  on skill/eval changes. Pulls forward two roadmap near-term items.
- **ADD (light)** — gstack bridge routing: q-level `tool-routing.md` gains `/browse`+`/qa`
  as preferred evidence tools when installed; eng-level gains a post-SHIP handoff note to
  `/land-and-deploy`; sec-level review lists `/cso` as an optional runtime-evidence tool.
- **ADD (light)** — Version gate in CI (release tag must match CHANGELOG head entry) and
  one-time cleanup of the `v.1.0.0` typo tag.
- **ADD (light)** — Hygiene: gitignore `__pycache__/` and `site/`; remove them from
  tracking.
- **DEFER** — Retro/learn skill; cross-project decision search (roadmap "Later": visual
  decision ledger). Revisit after the harness proves itself.
- **SKIP** — Rebuilding gstack runtime capabilities inside ExecForge.
- **KILL** — none.

## 7. Product hypothesis and objective

If ExecForge executes its evals in CI and routes QA/ship/security evidence through
installed gstack tooling, then skill regressions are caught before merge and governed
verdicts on the operator's portals are backed by driven evidence — without ExecForge
losing its zero-dependency install.

## 8. Measurable KRs (provisional — no baseline instrumented)

- KR1: 100% of bundled skills have ≥1 eval case executed in CI on skill-file changes.
  Baseline: 0 executed (11 cases documented).
- KR2: A seeded doc-vs-code drift (like the one fixed in 98db516) is caught by the
  harness in a dry run. Baseline: caught only by manual recheck.
- KR3: One governed QA run on a real portal (DataRex UAT) produces browser-driven
  evidence artifacts via the bridge. Baseline: 0 (q-level evidence is prose today).
- KR4: CI eval spend ≤ agreed cap per month; 0 required-check flake blocks in week one
  (advisory period).

## 9. Non-negotiable controls

- Every gstack bridge is conditional on gstack being installed; fallback contracts remain
  authoritative and unchanged.
- Eval CI job lands advisory; promotion to required is a separate, recorded decision.
- API key is least-privilege with a spend cap; never committed.
- No rebuild of gstack runtime tooling.

## 10. Roadmap / owners / rollback / kill criteria

- Owner: this engagement (skill-system maintainer).
- Sequencing precondition: merge or explicitly stack on the unpushed
  `feat/v0.8.0-role-architecture` branch before starting v0.9.0 work.
- Sequence: `eng-level --mode=plan` details exact files/edits; `sec-level` light pass on
  the CI workflow (new secret surface); q-level dry run per KR3.
- Rollback: per-file `git revert`; delete the CI job to kill the harness.
- Kill criteria: eval harness flakes >2×/week during advisory period → keep runner
  local-only, drop the CI job. Bridge confuses agents in dry runs → revert to fallback
  text.

## 11. Final verdict

**GO WITH CONDITIONS** — Build the eval harness plus the three light bridges and hygiene
fixes. Conditions: bridges stay conditional (no hard gstack dependency); the CI eval job
is advisory until proven quiet; spend is capped; v0.8.0 branch is merged or stacked
first.
