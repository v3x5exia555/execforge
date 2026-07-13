# Engineering Plan Review — Operating Layer Phase 1

Fallback plan review used; upstream gstack `/plan-eng-review` was unavailable because the installed command symlinks target a missing `data-reg/gstack` checkout.

## Verdict: APPROVED WITH CONDITIONS

The plan uses the existing dependency-free CLI and artifact conventions, separates operating-state logic from command parsing, and keeps authoritative evidence above machine pointers. It is reversible because it adds namespaced files and read-only diagnostics without deleting legacy artifacts.

## Architecture and data flow

1. `execforge.py` parses commands and renders findings.
2. `operating_state.py` reads Git metadata, skill trees, pointers, and lifecycle state.
3. `init-run` creates one immutable run directory per initiative and atomically replaces only the small current pointer.
4. `resume` reconciles Git with selected state and labels discrepancies.
5. `next` chooses one action through explicit precedence rather than an LLM classifier.

## Failure paths and controls

- Malformed JSON becomes a finding/warning; it must not raise through the CLI.
- Missing Git or a non-repository child is reported or skipped deterministically.
- Same-name runs created in rapid succession require collision-safe IDs.
- Pointer paths must remain repository-relative and may not escape the repository.
- Installed comparison must cover the complete skill directory, not only frontmatter versions.
- Diagnostics may expose filenames and statuses but not file contents.

## Mandatory conditions

- C1: Generate collision-safe run IDs and write pointers atomically.
- C2: Validate pointer containment before reading the selected run.
- C3: Treat legacy singleton state as compatibility fallback only.
- C4: Keep portfolio and installed checks read-only and tolerant of malformed state.
- C5: Implement each behavior through an observed RED→GREEN test cycle.
- C6: Skip every dirty or instruction-less external repository during parity rollout.

## Rollback

Revert the feature branch. Namespaced run directories are additive; legacy state is preserved. External `AGENTS.md` additions can be removed independently without changing `CLAUDE.md`.
