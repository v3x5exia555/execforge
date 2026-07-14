# Engineering Context — Operating Layer Phase 1

## Repository

- FACT: branch `feat/operating-layer-phase-1`
- FACT: base branch `feat/v0.9.0-evidence-bridges`
- FACT: locked base and initial HEAD `aa276d09cd1a0dcac701705ac1b3e4bf0225ced4`
- FACT: implementation is isolated at `.worktrees/operating-layer-phase-1`.
- FACT: baseline command `python3 -m unittest discover -s tests -v` passed 35 tests.

## Initiative

- FACT: the user approved Phase 1 after reviewing the prioritized improvement list.
- FACT: existing CLI code is dependency-free Python in `scripts/execforge.py`.
- FACT: current `init-run` writes singleton `.eng-level/state.json` and `.q-level/state.json`, so later initiatives replace current machine state.
- FACT: current `doctor` validates the source repository and environment but does not compare installed skill contents or inspect a portfolio.
- INFERENCE: a focused `operating_state.py` module limits additional responsibility in the existing CLI file.
- UNKNOWN: real time or token savings; this phase creates correctness mechanisms, not an ROI claim.

## Constraints

- Diagnostics are read-only.
- Machine state is an index below reproducible behavior, code, Git, and approved artifacts in evidence precedence.
- Legacy root state remains readable and is never silently migrated.
- No third-party dependency is introduced.
- External repository edits are limited to new instruction adapters in clean repositories.
