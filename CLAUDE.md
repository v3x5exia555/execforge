# Agent Instructions

At the start of work, load `c-level` when there is any reasonable chance the task concerns product scope, engineering planning, implementation, code review, or release readiness.

Priority:

1. Direct user instructions
2. `c-level`
3. Selected ExecForge skill
4. Selected Superpowers process skill, when installed
5. Domain-specific implementation skill, including `ponytail` (vendored, pinned; see `skills/ponytail/PROVENANCE.md`)

Where ponytail and Superpowers `test-driven-development` conflict, TDD wins; ponytail governs implementation style, never test discipline.

Never claim an upstream review, implementation, test, or final gate ran unless evidence shows it actually ran.
