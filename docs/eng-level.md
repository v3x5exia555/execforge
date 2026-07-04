# Eng Level

Use `/eng-level` after product intent is approved or when auditing an existing branch.

## Plan phase

The plan reviewer evaluates architecture, data flow, failure paths, security, performance, rollback, tests, and exact implementation tasks.

## Implementation phase

Superpowers is recommended for isolated worktrees, atomic plans, TDD, subagent execution, debugging, and verification.

## Review phase

The Staff Engineer review inspects the actual Git diff and executable evidence. It checks correctness, concurrency, consistency, data integrity, security, migrations, performance, backward compatibility, tests, plan completion, and scope drift.

## Final outcomes

- SHIP
- SHIP WITH REQUIRED FIXES
- RETURN TO IMPLEMENTATION
- RETURN TO PLAN
- BLOCK


## QA gate

For portal/API/backend changes, a Staff Engineer review is followed by `/q-level`. If QA fixes production code, run a final delta review and affected QA retest before `SHIP`.
