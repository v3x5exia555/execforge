# Full Cycle

`full-cycle` is the end-to-end lifecycle orchestrator. Use it when one initiative should be governed from idea to ship in a single continuous engagement; use the individual skills (via `c-level` routing) when only one stage is needed.

## Stage sequence

| Stage | Owner | Gate |
|---|---|---|
| 0. Product decision | `execforge` | `KILL`/`DEFER` ends the cycle |
| 1. Upstream approval | `eng-level` stop check | **User must approve** |
| 2. UI/UX design bridge | `design-html` | UI-facing scope only |
| 3. Engineering plan review | `eng-level --mode=plan` | `APPROVED` required |
| 4. Implementation | Superpowers execution skills | — |
| 5. Verification | tests/build/validation evidence | — |
| 6. Staff Engineer review | `eng-level --mode=review` | real diff required |
| 7. QA gate | `q-level --mode=auto` | **User approves plan + environment** |
| 8. Delta review and retest | `eng-level` + `q-level` | only when QA fixes change production code |
| 9. Final decision | lifecycle orchestrator | single verdict |

## Rules

- Stages run strictly in order; entering a stage requires the previous stage's exit artifact.
- `full-cycle` owns sequencing, evidence reconciliation, and re-entry; each stage's work is delegated to its owning skill.
- The two user gates (Stage 1 and Stage 7) always stop for a real user response.
- Defects route backwards: code defects to implementation, architecture defects to plan review, product-assumption defects to the product decision.
- Automatic fix/review loops are limited to three per root cause.
- The cycle ends only with a recorded Stage 9 verdict, a Stage 0 `KILL`/`DEFER`, or an explicit user stop.

See the skill definition at `skills/full-cycle/SKILL.md`.
