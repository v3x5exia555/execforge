---
name: full-cycle
description: Use when a single initiative must be governed end-to-end through the entire lifecycle — product decision, upstream approval, optional design, engineering plan, implementation, Staff Engineer review, QA gate, delta review, and final ship decision — in one continuous run.
license: MIT
compatibility: Orchestrates the other bundled ExecForge skills. Optional integrations require separately installed gstack and Superpowers skills.
metadata:
  author: ExecForge contributors
  version: "0.8.0"
---

# Full Cycle

## Core principle

One initiative, one continuous chain of evidence. Every stage either runs and leaves its artifact, is explicitly approved as not applicable, or the cycle stops. No stage may be claimed without evidence that it actually ran.

## When to use

Use `full-cycle` when the user asks to take an initiative "from idea to ship" under governance in a single engagement. For a single stage in isolation, use the routed skill from `c-level` directly instead.

## Stage sequence

```text
Stage 0  Product decision            execforge
Stage 1  Upstream approval gate      eng-level stop check   [USER GATE]
Stage 2  UI/UX design bridge         design-html [--design-system=<name|auto|none>]
                                                            (UI-facing scope only)
Stage 3  Engineering plan review     eng-level --mode=plan
Stage 4  Implementation              Superpowers execution skills
Stage 5  Verification                tests, build, validation evidence
Stage 6  Staff Engineer review       eng-level --mode=review
Stage 7  QA gate                     q-level --mode=auto    [USER GATE]
Stage 8  Delta review and retest     (only when QA fixes change production code)
Stage 9  Final engineering decision  SHIP / SHIP WITH REQUIRED FIXES /
                                     RETURN TO IMPLEMENTATION / RETURN TO PLAN / BLOCK
```

## Operating rules

1. Run stages strictly in order. Entering a stage requires the previous stage's exit artifact.
2. Delegate each stage to its owning skill and follow that skill's current instructions; `full-cycle` owns only sequencing, evidence reconciliation, and re-entry. When Superpowers is unavailable at Stage 4, follow [the fallback implementation contract](references/fallback-implementation-contract.md).
3. Two gates always stop for the user: upstream approval (Stage 1) and QA plan/environment approval (Stage 7). Never infer approval from enthusiasm in the original request.
4. Mark Stage 2 `NOT APPLICABLE` for non-UI scope, recording one sentence of justification. When the operator sets `--design-system` on the cycle, forward it to `design-html` at Stage 2; absent it, Stage 2 runs aesthetic-neutral. A design system binds visual language only — it never changes Stage 0 scope, and Stage 2 still owes its full screen and state coverage.
5. A `KILL` or `DEFER` verdict at Stage 0 ends the cycle; do not continue to planning.
6. When the change touches auth, user input, secrets, sensitive data, new dependencies, or network exposure, attach `sec-level`: `threat-model` inside Stage 3 and `review` inside Stage 6. An unresolved `S0`/`S1` blocks Stage 9 like a `P0`/`P1`.
7. When Stage 0 sets a gating initiative flag (`offensive-security`, `legally-gated`, or `regulated-impersonation`), the Authorization / Rules-of-Engagement gate is a hard STOP before Stage 4: the operator must record an `AUTHORIZED` / `NOT AUTHORIZED` / `N-A (justified)` decision with its evidence (written authorization, scope, consent basis, no unapproved third-party impersonation, captured-data handling). The agent never self-answers this gate. `NOT AUTHORIZED` or an unresolved decision blocks implementation, and blocks Stage 9 like a `P0`. This governance gate is distinct from the `sec-level` technical review. See execforge's initiative-flags reference.
8. A gating initiative flag also attaches `sec-level` automatically, without being asked. The authorization gate (rule 7) decides whether the work is *permitted*; `sec-level` decides whether it is *safe*. Passing one never substitutes for the other. A product whose own subject is security or offensive capability is the case where the technical review matters most, and is the case most often skipped.
9. `--stop-after=<stage>` halts the cycle at that stage boundary, emits its artifacts, and executes nothing beyond it. Treat a stated intent to stop — "plan it but do not deploy", "keep it for next cycle", "let me review first" — as setting this parameter. Record it so it survives later turns, and do not resume past the boundary without a new instruction. Deferred work is written to `.eng-level/backlog.md`.

## Feedback routing

| Defect discovered | Return to |
|---|---|
| Code defect with valid architecture | Stage 4 implementation, then retest |
| Invalid architecture or integration assumption | Stage 3 plan review |
| Invalid product assumption or contradictory acceptance criteria | Stage 0 product decision |
| QA-driven fix changed production code | Stage 8 delta review before Stage 9 |

Limit automatic fix/review loops to three per root cause; after that, escalate to the earlier stage instead of patching again.

## State and artifacts

Track cycle position in the stage artifacts of the delegated skills (`.execforge/`, `.eng-level/`, `.q-level/`). Before claiming any stage complete, confirm its artifact exists on disk. When resuming a cycle, detect the current stage from artifacts, not from memory or conversation claims.

## Exit contract

The cycle ends only with one of:

- A Stage 9 verdict recorded in `.eng-level/decision.md`, or
- A Stage 0 `KILL`/`DEFER` decision recorded in the ExecForge run, or
- An explicit user stop.

Report at exit: stage-by-stage status with evidence paths, open non-blocking items with owners, and the single final verdict.

## Validation gate

Before returning a final result:

- Every stage is DONE with evidence, NOT APPLICABLE with justification, or explicitly reported as not run.
- Both user gates received an actual user response.
- Any gating initiative flag has a recorded authorization decision; no `NOT AUTHORIZED` or unresolved authorization is hidden behind the final verdict.
- No P0/P1 finding or blocking QA defect is hidden behind the final verdict.
- The verdict is traceable to the recorded artifacts.
