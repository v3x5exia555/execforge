# ExecForge Decision — Adopt "ponytail" agent skill

- **Date:** 2026-07-17
- **Initiative:** Adopt DietrichGebert/ponytail (lazy-senior-dev simplicity persona) into the local Claude Code agent stack
- **Execution mode:** Dual subagents (CEO + COO), triggered by vendor-self-reported evidence and a new third-party instruction dependency in the agent trust context
- **Final verdict:** **PILOT**

## Gatekeeper

**PARTIAL.** The job (smallest correct diff → lower review burden and token cost) is real but the pain is an ASSUMPTION — never measured on this stack, and the user request was exploratory ("look into"), not an install mandate. Harness built-ins (/simplify, /code-review) already cover corrective simplification; ponytail's genuine gap is generation-time pressure.

## Initiative flags

- offensive-security: not set
- legally-gated: not set
- regulated-impersonation: not set
- user-prescribed-mechanism: not set (request was exploratory)

## Evidence summary

- [VERIFIED] 84,754 stars / 4,608 forks, MIT, created 2026-06-12 (~5 weeks old), pushed 2026-07-15, 80 open issues, ~20 harness adapters, npm installer exists, commercialization waitlist (ponytail.dev/soon). Core artifact is one ~120-line SKILL.md.
- [VENDOR-REPORTED] −54% LOC (ceiling −94%), −22% tokens, −20% cost, −27% time, 100% adversarial-safety retention — Haiku 4.5, n=4, 12 tasks, self-benchmarked (publicly corrected earlier inflated numbers — process-credibility positive, not independence).
- [VERIFIED] Textual conflict: ponytail "YAGNI applies to tests too" vs Superpowers test-driven-development.
- [UNKNOWN] Effect size on Fable/Opus-class models; behavioral arbitration of skill conflicts; net token economics of always-on injection under this stack.
- Open-issue triage: adapter/integration noise dominates; #517 (compression-plugin conflicts) and #261 (over-shrinking functional data) are real behavioral edge cases; no open disputes of safety/benchmark claims.

## Scope mode

**Scope Reduction** relative to the proposal (always-on, auto-updating plugin): pinned vendored copy, lite intensity, lowest priority tier, explicit carve-outs.

## Contradiction register

1. Ponytail test rule vs Superpowers TDD — factual (textual), verified. **Resolution:** written precedence line in CLAUDE.md; TDD wins; ponytail governs implementation style only.
2. "Active on every response" self-claim vs documented skill priority order — factual. **Resolution:** slot at domain-implementation tier (bottom); priority ladder wins.
3. Vendor benchmark magnitude vs this stack/model class — strategic, unresolved. **Resolution:** does not support the decision; PILOT exists to measure locally.

## Final scope ledger

- **Add:** read full SKILL.md before install; vendored copy pinned to commit SHA in local skills dir; CLAUDE.md addendum (bottom tier, TDD carve-out, guards non-negotiable); lite intensity; 2-week / ~10-governed-run pilot with per-task diff-size and review-effort notes anchored to existing run artifacts.
- **Defer:** full/ultra intensity; deconfliction docs vs /simplify and /code-review; any measurement harness; upstream re-syncs (manual diff review only).
- **Skip:** npm installer path; auto-updating marketplace plugin; applying ponytail to governance/skill-authoring outputs; commercial waitlist.
- **Kill (standing):** adopting ponytail's test rule over TDD.

## Hypothesis and objective

If generation-time simplicity pressure is added at the bottom of the skill stack, per-task diff size and operator review effort drop measurably without any governance-gate degradation.

## Key results (provisional targets — no local baseline exists)

1. ≥20% median diff-size reduction on comparable tasks across ~10 governed runs (provisional; baseline to be established from pre-pilot run artifacts).
2. Zero gate-degradation incidents (skipped/thinned tests, validation, or gate outputs attributable to ponytail).
3. Subjective review-burden reduction reported on ≥ half of piloted tasks.

## Non-negotiable controls

- Plain-file vendored install only; record upstream commit SHA, adoption date, full text snapshot.
- Priority: below Superpowers process skills; CLAUDE.md line: "Where ponytail and Superpowers TDD conflict, TDD wins; ponytail governs implementation style, never test discipline."
- Hard enforcement stays with eng-level/q-level/sec-level gates; persona guards are defense-in-depth only.
- Existing rule survives intact: never claim a gate ran without evidence.
- No further always-on personas without retiring/consolidating one.

## Rollback and kill criteria

- **Rollback:** delete the vendored file (minutes).
- **Immediate kill:** ponytail-attributable guard weakening twice in pilot, or once on security/data-loss surfaces; any gate skipped/abbreviated/falsely claimed with brevity/YAGNI in the causal chain.
- **Sunset:** no observable diff-size or review-effort reduction after ~10 governed runs or 4 weeks.
- **Freeze-or-remove:** upstream relicense, paywall, or compromise indicators → frozen snapshot or removal; never re-sync.
- Switching to npm/auto-update reopens this review.

## Plan B — user-triggered observation job (added 2026-07-17 at user request)

If passive per-task notes prove too easy to skip, the pilot's measurement leg has an on-demand fallback the user triggers directly:

- **Job:** `.execforge/bin/ponytail-observe.sh` (smoke-tested on clean and dirty trees).
  - `record <task-slug> <on|off> [note]` — snapshots the current `git diff HEAD` stats (files, insertions, deletions) into `pilot-log.tsv` in this run directory, tagged with whether ponytail was active.
  - `report` — prints the log and the on-vs-off averages, giving the sunset-threshold evidence (KR 1) on demand.
- **Trigger options:** run it manually after each piloted task (default), or wrap it in `/loop` / a scheduled routine if recurring automatic observation is later wanted — deferred until the manual trigger proves insufficient (YAGNI applies to the measurement too).
- **Decision rule unchanged:** the same kill/sunset thresholds apply; Plan B changes only how the evidence is collected, not what counts as evidence.

## Owner

Operator (Tyson). Vendored text is owned outright; upstream is an idea feed, not a supplier.

## Verdict

**PILOT** — downside is fully containable at near-zero cost (pinned file, bottom tier, TDD precedence, defined kill triggers); upside is unproven on this stack but cheap to test. Not GO as proposed (always-on auto-updating install); not KILL (cheap, auditable, MIT, reversible).

## Validation gate

- CEO and COO reviews ran independently (background subagents, no cross-exposure before first pass): ✔
- Material claims labelled: ✔
- No invented metric presented as fact (KRs marked provisional): ✔
- Factual contradictions resolved in writing; strategic one quarantined from supporting the decision: ✔
- Security, compliance, cost, ownership, rollback, kill criteria visible: ✔
- Plan complexity ≤ problem (one file, one CLAUDE.md paragraph, notes-based pilot): ✔
