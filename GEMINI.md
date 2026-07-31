# Agent Instructions

At the start of work, load `c-level` when there is any reasonable chance the task concerns product scope, engineering planning, implementation, code review, or release readiness.

Priority:

1. Direct user instructions
2. `c-level`
3. Selected ExecForge skill
4. Selected Superpowers process skill, when installed
5. Domain-specific implementation skill

Never claim an upstream review, implementation, test, or final gate ran unless evidence shows it actually ran.

LOCKED (operator decision 2026-07-31): the restored CEO Subagent, COO Subagent, CEO plan (gstack `plan-ceo-review` bridge), Phase 5 Scope Ledger, Phase 8 Product Definition and OKRs, and A-C-T-I-O-N Operational Matrix sections in `skills/execforge/`, and the OKR trigger aliases in `skills/c-level/SKILL.md`, must never be edited, condensed, or removed without explicit operator instruction. `tests/test_restored_sections.py` enforces this lock.
