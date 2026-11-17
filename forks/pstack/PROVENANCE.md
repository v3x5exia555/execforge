# Provenance: fork of pstack

- Upstream: https://github.com/cursor/plugins/tree/main/pstack (MIT, Copyright (c) 2026 Lauren Tan; see LICENSE)
- Pinned commit: 3fa33bb (2026-11-16), pstack version 0.15.43
- Forked: 2026-11-17
- Tree hash at fork (SHA-256 over the sorted per-file SHA-256 list, excluding this file and .claude-plugin/plugin.json): 42e1917873cb36412d54b0fd408544b6c4684ff13666d10c55c68b017cee0660
- Local edits: none yet. Upstream files are verbatim. Added files: this PROVENANCE.md and .claude-plugin/plugin.json (Claude Code manifest).

Rules for this fork:

1. It lives in forks/, not skills/. It is not one of the ExecForge bundled skills and the installer does not ship it.
2. TDD wins: where pstack's tdd skill conflicts with Superpowers test-driven-development, TDD wins (same rule as ponytail).
3. Every local edit is listed under "Local edits" above, with the date and reason.
4. No automatic upstream sync. To take upstream changes, diff against the pinned commit and review by hand.
