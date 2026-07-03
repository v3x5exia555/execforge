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
Approved upstream requirements
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
