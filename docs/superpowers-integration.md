# Superpowers Integration

ExecForge and Superpowers are complementary.

## Ownership

| Framework | Owns |
|---|---|
| ExecForge | Product need, scope, economics, operations, upstream approval, final lifecycle reconciliation |
| Superpowers | Implementation process discipline |
| gstack plan review | Pre-build engineering design pressure test |
| gstack Staff review | Broad final diff audit |

## Recommended order

```text
ExecForge product decision
→ User upstream approval
→ gstack plan-eng-review
→ Superpowers worktree
→ Superpowers writing-plans
→ Superpowers subagent execution / executing-plans
→ Superpowers TDD
→ Superpowers verification
→ gstack Staff Engineer review
→ ExecForge QA Lifecycle
→ final Staff Engineer delta review when needed
→ ExecForge final engineering verdict
→ Superpowers finish branch
```

## Triggering

The `using-execforge` bootstrap routes the workflow. To guarantee session-start behavior, place the repository's `AGENTS.md`/`CLAUDE.md` instruction in the project or configure the host to load the bootstrap skill at session start.

Superpowers must be installed separately from its official repository or marketplace. ExecForge never copies its skill text.
