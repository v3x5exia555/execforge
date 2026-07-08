# Full-Cycle Stage 4 Fallback Implementation Contract — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give `full-cycle` a fallback implementation discipline for Stage 4 so harnesses without Superpowers still build under governance instead of free-styling.

**Architecture:** One new progressive reference under `skills/full-cycle/references/` defining the contract, linked from the `full-cycle` SKILL.md operating rules; the existing structural test map is extended so the link is enforced. No new actor — the coding agent remains the builder.

**Tech Stack:** Markdown skill files, Python `unittest`, existing `execforge.py` validator.

## Global Constraints

- Skill `SKILL.md` files stay ≤ 500 lines (validator rule).
- All local links in SKILL.md must resolve (validator rule).
- Plan files use `YYYYMMDD_HHMMSS_<title>.md` naming (AGENTS.md).
- Never claim a review/test ran without evidence (repo invariant; the contract itself must restate it).
- Fallback output must be explicitly labeled as fallback (matches `eng-level` fallback-contract precedent).

---

### Task 1: Enforce the new reference structurally (failing test first)

**Files:**
- Modify: `tests/test_skill_bundle.py` (the `expected` map in `test_progressive_references_are_linked_from_skill_files`)

**Interfaces:**
- Produces: test expectation that `skills/full-cycle/references/fallback-implementation-contract.md` exists and is linked from `skills/full-cycle/SKILL.md`.

- [ ] **Step 1: Extend the test map**

```python
        expected = {
            "execforge": ["references/review-phases.md", "references/execution-and-governance.md"],
            "eng-level": ["references/lifecycle-protocol.md", "references/fallback-review-contracts.md"],
            "full-cycle": ["references/fallback-implementation-contract.md"],
        }
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest tests.test_skill_bundle.SkillBundleTests.test_progressive_references_are_linked_from_skill_files -v`
Expected: FAIL with `Missing references/fallback-implementation-contract.md`

### Task 2: Write the fallback implementation contract and link it

**Files:**
- Create: `skills/full-cycle/references/fallback-implementation-contract.md`
- Modify: `skills/full-cycle/SKILL.md` (operating rule 2)

**Interfaces:**
- Consumes: Stage 3 exit artifacts (`.eng-level/engineering-plan.md`, `implementation-tasks.md`, `test-matrix.md`).
- Produces: the reference file linked from SKILL.md.

- [ ] **Step 1: Create the reference with this exact content**

```markdown
# Fallback Implementation Contract (Stage 4)

Use only when the Superpowers execution skills cannot be resolved in the current harness and the user asks to continue. When Superpowers is installed, its current skills always take precedence.

## Preconditions

- Stage 3 exit artifacts exist: approved `.eng-level/engineering-plan.md`, `implementation-tasks.md`, and `test-matrix.md`.
- The baseline (base branch, merge-base, approved scope, non-goals, required controls) is locked.
- The user authorised implementation in this invocation.

## Discipline

1. Work one implementation task at a time, in plan order; do not start a task whose dependencies are incomplete.
2. For every behavior change, write the failing test first, watch it fail, implement the minimal change, and watch it pass. If the repository has no test harness for the area, record that explicitly instead of skipping silently.
3. Stay inside the approved scope: no files, dependencies, or capabilities beyond the task's plan entry. Discovered necessary scope goes back to Stage 3 as a plan change, not into the diff.
4. Commit per completed task with the task ID in the message.
5. Update the task's status and evidence (test command and result) in `.eng-level/implementation-tasks.md` immediately after each task.
6. Before claiming Stage 4 complete: run the full relevant test suite, confirm every plan task is `DONE` or explicitly reported otherwise, and leave the working tree clean.

## Stop conditions

Stop and report instead of improvising when: a plan assumption fails against the real code, a required tool or credential is unavailable, the same fix fails twice for one root cause, or a change would touch a locked non-goal.

## Labeling

State in the Stage 4 report:

    Fallback implementation discipline used; Superpowers execution skills were unavailable.

A fallback build cannot claim behavioural equivalence with a Superpowers-driven build; the Stage 6 Staff Engineer review and Stage 7 QA gate remain mandatory and unchanged.
```

- [ ] **Step 2: Link it from `skills/full-cycle/SKILL.md` operating rule 2**

Replace:

```markdown
2. Delegate each stage to its owning skill and follow that skill's current instructions; `full-cycle` owns only sequencing, evidence reconciliation, and re-entry.
```

with:

```markdown
2. Delegate each stage to its owning skill and follow that skill's current instructions; `full-cycle` owns only sequencing, evidence reconciliation, and re-entry. When Superpowers is unavailable at Stage 4, follow [the fallback implementation contract](references/fallback-implementation-contract.md).
```

- [ ] **Step 3: Run the test to verify it passes**

Run: `python3 -m unittest tests.test_skill_bundle.SkillBundleTests.test_progressive_references_are_linked_from_skill_files -v`
Expected: PASS

### Task 3: Record, verify, install

**Files:**
- Modify: `CHANGELOG.md` (Unreleased section)

- [ ] **Step 1: Add the CHANGELOG line**

```markdown
- Added a Stage 4 fallback implementation contract to `full-cycle` for harnesses without Superpowers: task-by-task, test-first execution with explicit stop conditions and mandatory fallback labeling.
```

- [ ] **Step 2: Full verification**

Run: `python3 scripts/execforge.py validate && python3 -m unittest discover -s tests -v`
Expected: `ExecForge validation passed.` and `OK` (13 tests)

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "Add full-cycle Stage 4 fallback implementation contract"
```

- [ ] **Step 4: Install to all harnesses**

Run: `for t in claude codex agents; do python3 scripts/execforge.py install --target $t --force; done`
Expected: `verified 7 installed skills` for each target
