# Architecture

## Product layer

```text
CEO Subagent ─┐
              ├─ Main Orchestrator → Product Decision
COO Subagent ─┘
```

The first passes are independent. The orchestrator resolves contradictions and owns the final verdict.

## Engineering layer

```text
Approved product scope
             ↓
 Optional design-html bridge for UI work
             ↓
 Upstream requirement interpretation
             ↓
     User approval stop check
             ↓
    Plan Engineering Review
             ↓
        Implementation
             ↓
    Staff Engineer Review
             ↓
 Final Engineering Decision
```

## Evidence flow

```text
Product evidence
→ Scope ledger
→ Approved upstream requirements
→ Interface brief / screen inventory when UI work applies
→ Engineering plan
→ Implementation tasks
→ Git diff
→ Test evidence
→ Conformance matrix
→ Final decision
```

## Separation of duties

- CEO optimizes user value and strategic advantage.
- COO optimizes safe, scalable, economic operation.
- Plan reviewer validates intended technical design.
- Implementers execute approved tasks.
- Staff reviewer attacks actual code and configuration.
- Orchestrators own reconciliation and verdicts.


## QA layer

```text
Portal QA ───────┐
API QA ──────────┼→ QA Main Orchestrator → QA Verdict
Backend/Data QA ─┘
```

QA evidence flows back to implementation, engineering planning, or product depending on the root cause. Production-code fixes require a final delta review and affected QA retest.
