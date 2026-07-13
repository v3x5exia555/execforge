# Upstream Requirements — Operating Layer Phase 1

- Approval source: user said “proceed” after reviewing the prioritized improvement list.
- Approval status: APPROVED
- Approved at: 2026-07-13
- Delivery mode: isolated worktree on `feat/operating-layer-phase-1`

## What, why, and for whom

Extend ExecForge for a single operator who uses Claude Code and Codex across several repositories. The phase must make version drift, instruction gaps, stale lifecycle state, and the next valid action visible without adding Citadel as a second governance system.

## In scope

1. Portfolio diagnostics for missing root instructions, unresolved Git conflicts, and stale or branch-mismatched lifecycle state.
2. Installed-skill diagnostics comparing bundled ExecForge skills with Claude, Codex, and Agent Skills installations.
3. Initiative-scoped engineering and QA run artifacts with rebuildable `current.json` pointers.
4. Deterministic `resume` and `next` CLI commands.
5. Documentation and tests for every new behavior.
6. `AGENTS.md` parity for clean active repositories that already have `CLAUDE.md`.

## Deferred

- Telemetry and cost attribution.
- Lifecycle hooks.
- Dashboard, fleets, daemon, or unattended execution.
- Migration of historical governance artifacts.
- DPO repository changes while Git conflicts remain unresolved.

## Skipped and non-goals

- Installing Citadel or copying its skill catalog.
- Replacing ExecForge, Superpowers, or project-specific security and QA rules.
- Treating machine state as stronger evidence than Git, executed tests, or approved Markdown artifacts.
- Making Claude and Codex global skill catalogs identical.

## Acceptance criteria

1. `doctor --installed` reports missing or content-drifted bundled skills without modifying installations.
2. `doctor --portfolio <root>` reports missing `AGENTS.md`/`CLAUDE.md`, unresolved conflicts, and state whose recorded branch differs from the repository branch.
3. `init-run` creates initiative-scoped engineering and QA directories plus `.eng-level/current.json` and `.q-level/current.json` pointers, without overwriting an earlier run.
4. `resume --root <repo>` reports the selected initiative, current Git branch/HEAD, recorded lifecycle state, stale-state warnings, blockers, stop boundary, and evidence paths.
5. `next --root <repo>` returns exactly one safe action and stops on conflicts, blockers, pending approval, or `stop_after` boundaries.
6. Existing command behavior remains covered and the complete unit suite passes.
7. Clean active repositories receiving instruction parity contain an `AGENTS.md` identical to their existing `CLAUDE.md`; DPO remains unchanged.

## Initiative flags

- offensive-security: not set
- legally-gated: not set
- regulated-impersonation: not set
- user-prescribed-mechanism: set; Citadel was evaluated, but the approved mechanism is selective ExecForge improvement.
- Authorization / Rules-of-Engagement: N-A for this developer-workflow change. Existing downstream gates remain authoritative.

## Non-negotiable controls

- Read-only diagnostics by default.
- No prompt, credential, personal-data, screenshot, or security-finding capture.
- State records include branch/commit lineage and remain rebuildable from authoritative artifacts.
- Diagnostics tolerate malformed or legacy state and report it instead of crashing.
- External repository edits are limited to new `AGENTS.md` files in clean repositories.

## Kill criteria

- New state overwrites prior initiative evidence.
- Resume presents stale state as current without warning.
- Diagnostics mutate a repository or expose sensitive content.
- Runtime parity requires replacing project-specific rules.

