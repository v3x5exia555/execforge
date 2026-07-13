# Operating Layer Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add read-only portfolio/version diagnostics and reliable initiative-scoped resume/next state to ExecForge, then close Claude/Codex root-instruction gaps in clean active repositories.

**Architecture:** Keep `scripts/execforge.py` as the CLI boundary and add `scripts/operating_state.py` as a focused, dependency-free domain module. Machine state is a rebuildable index: each initiative owns `.eng-level/runs/<run-id>/` and `.q-level/runs/<run-id>/`, while small `current.json` pointers select the active run. Diagnostics read only allowlisted metadata and Git porcelain output.

**Tech Stack:** Python 3.9+ standard library, `unittest`, Git CLI, JSON and Markdown artifacts.

---

### Task 1: Installed and portfolio diagnostics

**Files:**
- Create: `scripts/operating_state.py`
- Modify: `scripts/execforge.py`
- Modify: `tests/test_repository.py`

- [ ] **Step 1: Write failing tests** for installed-skill equality, missing runtime skills, root instruction coverage, conflict detection, malformed state, and recorded-branch mismatch. Tests construct temporary repositories and skill directories and assert structured findings rather than matching incidental console formatting.
- [ ] **Step 2: Run the diagnostic tests** with `python3 -m unittest tests.test_repository.RepositoryTests.test_installed_skill_diagnostics tests.test_repository.RepositoryTests.test_portfolio_diagnostics -v`; expected result is failure because the diagnostic APIs do not exist.
- [ ] **Step 3: Implement the minimal diagnostic model** with an immutable finding record containing `severity`, `code`, `project`, and `detail`; compare SHA-256 hashes for installed skills; use `git status --porcelain` and `git branch --show-current`; parse only top-level JSON metadata required for branch/state checks.
- [ ] **Step 4: Wire CLI flags** so `doctor --installed` checks all three known destinations and `doctor --portfolio PATH` scans direct child repositories without changing them.
- [ ] **Step 5: Run the focused tests and full suite**; expected result is zero failures.

### Task 2: Initiative-scoped state and pointers

**Files:**
- Modify: `scripts/operating_state.py`
- Modify: `scripts/execforge.py`
- Modify: `tests/test_repository.py`
- Modify: `schemas/eng-level-state.schema.json`
- Modify: `skills/eng-level/assets/state.template.json`

- [ ] **Step 1: Write failing tests** proving two `init-run` calls create distinct engineering and QA run directories, preserve the first run, and update valid `current.json` pointers to the second run.
- [ ] **Step 2: Run the focused init-run test**; expected result is failure because current code overwrites root singleton artifacts.
- [ ] **Step 3: Implement run identifiers and pointer writes** using UTC timestamp plus a normalized initiative slug. Add `run_id`, `created_at`, `updated_at`, `branch`, `commit`, `artifact_root`, and `next_action` to generated state. Write pointer files atomically through a temporary sibling followed by `Path.replace()`.
- [ ] **Step 4: Preserve compatibility** by allowing status/resume to read legacy root `state.json` only when no valid pointer exists; never silently migrate or delete legacy artifacts.
- [ ] **Step 5: Run focused and full tests**; expected result is zero failures.

### Task 3: Resume and next-action commands

**Files:**
- Modify: `scripts/operating_state.py`
- Modify: `scripts/execforge.py`
- Modify: `tests/test_repository.py`

- [ ] **Step 1: Write failing tests** for a fresh run, pending approval, open blocker, merge conflict, stop-after boundary, branch mismatch, malformed pointer, and completed/ship-ready state.
- [ ] **Step 2: Run the resume/next tests**; expected result is failure because the commands are absent.
- [ ] **Step 3: Implement `resume`** to return initiative, run ID, Git branch/HEAD, lifecycle state, stop boundary, blockers, backlog location, evidence root, and warnings. Missing data is printed as `unknown`, never inferred as healthy.
- [ ] **Step 4: Implement `next`** with precedence: Git conflicts; unreadable/stale state; open blockers; upstream approval; plan; implementation; review; QA; ship-ready handoff. Print one action line plus supporting warning lines.
- [ ] **Step 5: Run focused and full tests**; expected result is zero failures.

### Task 4: Contracts and documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/getting-started.md`
- Modify: `skills/eng-level/SKILL.md`
- Modify: `skills/eng-level/references/state-and-artifacts.md`
- Modify: `tests/test_repository.py`

- [ ] **Step 1: Add failing documentation-contract assertions** for the new CLI commands and initiative-scoped artifact layout.
- [ ] **Step 2: Run the focused contract tests**; expected result is failure until documentation changes are present.
- [ ] **Step 3: Document exact commands, evidence precedence, compatibility fallback, privacy boundary, and recovery behavior.** Do not describe telemetry, hooks, or dashboards as implemented.
- [ ] **Step 4: Run repository validation and all tests**; expected result is zero failures.

### Task 5: Clean-repository instruction parity

**Files:**
- Create outside this worktree after core verification: `AGENTS.md` in `security-awareness-reporting-platform`, `hotel-webscrap`, `portal-template`, and `code-ai-monitor` when each repository is clean and has an authoritative `CLAUDE.md`.

- [ ] **Step 1: Recheck each target with `git status --porcelain`** and skip any repository that is not clean or lacks `CLAUDE.md`.
- [ ] **Step 2: Create `AGENTS.md` with byte-identical content to `CLAUDE.md`** using patch-based edits, preserving existing files.
- [ ] **Step 3: Verify parity** with `cmp -s CLAUDE.md AGENTS.md` in every changed repository and confirm DPO has no new diff.
- [ ] **Step 4: Report these cross-repository changes separately** because they are not part of the ExecForge feature branch.

### Task 6: Verification and branch review

**Files:**
- Create: `.eng-level/operating-layer-phase-1/staff-review.md`
- Create: `.eng-level/operating-layer-phase-1/conformance.md`

- [ ] **Step 1: Run `python3 scripts/execforge.py validate`.** Expected output: `ExecForge validation passed.`
- [ ] **Step 2: Run `python3 -m unittest discover -s tests -v`.** Expected output: all tests pass with zero failures.
- [ ] **Step 3: Run `python3 scripts/execforge.py doctor --installed --portfolio /Users/tysonchua/Desktop/project`.** Expected output: diagnostics identify real instruction/version/state issues without mutation or traceback.
- [ ] **Step 4: Review the complete branch diff** against every upstream acceptance criterion and record P0–P3 findings and conformance statuses.
- [ ] **Step 5: Run `git diff --check` and repeat the complete test suite after review fixes.** Expected result: clean diff and zero test failures.

