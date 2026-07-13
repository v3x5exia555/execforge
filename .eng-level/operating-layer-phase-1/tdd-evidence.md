# Task 1 TDD Evidence

## RED reproduction

- Locked base: `05a4672`
- Isolation: detached temporary Git worktree at `<temporary-base-worktree>`
- Overlay check: `git status --short` reported only `M tests/test_repository.py`
- Production files from Task 1 were not overlaid.

Command, run from `<temporary-base-worktree>`:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_installed_skill_diagnostics tests.test_repository.RepositoryTests.test_portfolio_diagnostics -v
```

Result:

- Exit status: `1`
- Failure phase: test module loading
- Failure reason: `FileNotFoundError` for `scripts/operating_state.py`; the diagnostic API did not exist at the locked base.
- No diagnostic test reached a passing state during this reproduction.

The temporary worktree was removed after the run.

## GREEN verification

Focused diagnostic tests:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_installed_skill_diagnostics tests.test_repository.RepositoryTests.test_portfolio_diagnostics -v
```

- Exit status: `0`
- Result: `2` tests passed.

Complete unit test suite:

```sh
python3 -m unittest discover -s tests -v
```

- Exit status: `0`
- Result: `37` tests passed.

Repository and source verification:

```sh
python3 -m py_compile scripts/operating_state.py scripts/execforge.py
python3 scripts/execforge.py validate
git diff --check
```

- Exit status: `0` for each command.
- Repository validation reported `ExecForge validation passed.`
- Diff whitespace validation produced no findings.

# Task 2 Authoritative-First Commit Correction Evidence

Locked correction base: `c960f81cc39a05ca34f88e3bb664bb016eb26578`.

This correction intentionally replaces the earlier authoritative-last design.
The authoritative `.execforge/current.json` selector is now published first;
Eng/QA pointers are compatibility projections. Readers prefer the authoritative
selector, so every observable post-commit state is consistent on both fresh and
replacement repositories.

RED command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_authoritative_first_publication_is_observable_after_every_step tests.test_repository.RepositoryTests.test_projection_restore_failure_retains_all_new_run_targets tests.test_repository.RepositoryTests.test_authoritative_reader_rejects_symlinked_namespace_roots -v
```

- Exit status: `1`.
- Result: `4` failures and `1` error across three tests with parameterized
  publication and namespace cases.
- Generic failures: replacement runs still exposed the old authoritative state
  after compatibility projection writes; a failed projection restore deleted
  the newly referenced run targets; and symlinked Eng/QA namespace roots were
  accepted by the authoritative reader.

GREEN command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_authoritative_first_publication_is_observable_after_every_step tests.test_repository.RepositoryTests.test_projection_restore_failure_retains_all_new_run_targets tests.test_repository.RepositoryTests.test_authoritative_reader_rejects_symlinked_namespace_roots tests.test_repository.RepositoryTests.test_old_selector_wins_before_authoritative_commit tests.test_repository.RepositoryTests.test_base_exceptions_restore_all_selectors_after_each_publish_boundary tests.test_repository.RepositoryTests.test_restore_failures_are_aggregated_and_all_restores_attempted tests.test_repository.RepositoryTests.test_failed_authoritative_restore_keeps_referenced_new_run -v
```

- Exit status: `0`.
- Result: all seven focused tests passed.

The accepted conservative cleanup rule is used: if any selector restoration
fails, no newly created run directory is deleted. This prevents a surviving
authoritative or compatibility selector from becoming dangling.

Final verification:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- The complete suite passed all `64` tests.
- Validation, bytecode compilation, and diff whitespace validation each exited
  `0`.

# Task 2 Authoritative Selector Hardening Evidence

Locked hardening base: `6cea45df639bf8b185a193243536913ef7f11515`.

The second review regression tests were added before selector, rollback, schema,
and portability changes. RED command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_authoritative_selector_wins_during_split_projection_window tests.test_repository.RepositoryTests.test_base_exceptions_restore_all_selectors_after_each_publish_boundary tests.test_repository.RepositoryTests.test_restore_failures_are_aggregated_and_all_restores_attempted tests.test_repository.RepositoryTests.test_failed_authoritative_restore_keeps_referenced_new_run tests.test_repository.RepositoryTests.test_cli_imports_when_fcntl_is_unavailable tests.test_repository.RepositoryTests.test_state_schemas_accept_template_state tests.test_repository.RepositoryTests.test_init_run_creates_state -v
```

- Exit status: `1`.
- Result: `2` failures and `8` errors across seven tests including
  parameterized interruption subtests.
- Generic failures: `.execforge/current.json` and its writer did not exist;
  split projection windows had no authoritative selector; `KeyboardInterrupt`
  and `SystemExit` were not coordinated rollback paths; restore failures were
  not aggregated; `fcntl` was imported unconditionally; and metadata additions
  were breaking schema requirements.

GREEN command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_authoritative_selector_wins_during_split_projection_window tests.test_repository.RepositoryTests.test_base_exceptions_restore_all_selectors_after_each_publish_boundary tests.test_repository.RepositoryTests.test_restore_failures_are_aggregated_and_all_restores_attempted tests.test_repository.RepositoryTests.test_failed_authoritative_restore_keeps_referenced_new_run tests.test_repository.RepositoryTests.test_cli_imports_when_fcntl_is_unavailable tests.test_repository.RepositoryTests.test_state_schemas_accept_template_state tests.test_repository.RepositoryTests.test_init_run_creates_state -v
```

- Exit status: `0`.
- Result: all seven focused tests passed.

The stable `.execforge-init-run.lock` inode is intentionally retained and
ignored by Git. Each operation reliably releases its OS lock and closes the
descriptor; retaining the inode prevents a new process from bypassing a waiter
that already holds the same lock file open. POSIX uses `fcntl`; Windows uses
`msvcrt` conditionally.

Final verification:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- The complete suite passed all `61` tests.
- Validation, bytecode compilation, and diff whitespace validation each exited
  `0`.

# Task 2 Quality and Security Hardening Evidence

Locked hardening base: `e6d64b40916349235a7f5c0918c1539afec43fb4`.

The review-hardening tests were added before the coordination and containment
changes. The first RED command was:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_init_run_rejects_symlinked_namespace_roots_and_runs_without_outside_writes tests.test_repository.RepositoryTests.test_failed_publication_restores_both_pointers_and_removes_new_runs tests.test_repository.RepositoryTests.test_failed_preparation_preserves_pointers_and_removes_new_runs tests.test_repository.RepositoryTests.test_concurrent_init_runs_are_serialized_and_publish_aligned_pointers tests.test_repository.RepositoryTests.test_pointer_reader_rejects_noncanonical_ids_and_symlinked_selected_state tests.test_repository.RepositoryTests.test_pointer_reader_rejects_symlinked_run_directory -v
```

- Exit status: `1`.
- Result: `9` reported failures across the six focused tests (including
  parameterized namespace subtests).
- Generic failures: symlinked roots/runs were followed and could write outside
  the repository; failed preparation left new runs behind; failed second-pointer
  publication left Eng and QA pointers inconsistent; concurrent initializations
  overlapped; and prior pointer bytes were not restored.
- The initial reader fixtures that escaped the lifecycle root were already
  rejected. They were tightened to use cross-run symlinks inside the lifecycle
  root so the regression specifically exercised aliasing between contained runs.

A supplemental writer-specific test was then added before hardening the writer
helper itself:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_pointer_writer_rejects_noncanonical_ids_and_symlinked_run_directory -v
```

- Exit status: `1`.
- Result: `1` failure because a symlinked selected run directory was accepted.

The expanded GREEN command was:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_init_run_rejects_symlinked_namespace_roots_and_runs_without_outside_writes tests.test_repository.RepositoryTests.test_failed_publication_restores_both_pointers_and_removes_new_runs tests.test_repository.RepositoryTests.test_failed_preparation_preserves_pointers_and_removes_new_runs tests.test_repository.RepositoryTests.test_failed_run_directory_creation_cleans_partial_new_runs tests.test_repository.RepositoryTests.test_failed_initial_publication_restores_pointer_absence tests.test_repository.RepositoryTests.test_concurrent_init_runs_are_serialized_and_publish_aligned_pointers tests.test_repository.RepositoryTests.test_pointer_reader_rejects_noncanonical_ids_and_symlinked_selected_state tests.test_repository.RepositoryTests.test_pointer_reader_rejects_symlinked_run_directory tests.test_repository.RepositoryTests.test_state_schemas_accept_template_state tests.test_repository.RepositoryTests.test_init_run_creates_state tests.test_repository.RepositoryTests.test_init_run_records_git_and_detached_head_metadata -v
```

- Exit status: `0`.
- Result: all `11` tests passed.

Writer-specific GREEN confirmation:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_pointer_writer_rejects_noncanonical_ids_and_symlinked_run_directory tests.test_repository.RepositoryTests.test_pointer_replace_failure_preserves_current_pointer -v
```

- Exit status: `0`.
- Result: both tests passed.

Final hardening verification:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- The complete suite passed all `55` tests.
- Repository validation, bytecode compilation, and diff whitespace validation
  each exited `0`.

## Quality-review regression cycle

Five regression tests were added before production changes for branch metadata
compatibility, fsmonitor suppression, invalid Git bytes, special-file hashing,
and selected-state precedence.

RED command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_portfolio_branch_compatibility_and_precedence tests.test_repository.RepositoryTests.test_portfolio_git_status_disables_configured_fsmonitor tests.test_repository.RepositoryTests.test_git_output_with_invalid_utf8_is_replaced tests.test_repository.RepositoryTests.test_installed_skill_fifo_is_hashed_without_blocking tests.test_repository.RepositoryTests.test_malformed_selected_state_does_not_fall_back_to_legacy -v
```

- Exit status: `1`
- Result: `3` failures and `2` errors across `5` tests.
- Observed failures: legacy `base_branch` drift was missed; configured
  `core.fsmonitor` created its marker; invalid Git bytes raised
  `UnicodeDecodeError`; FIFO hashing exceeded the two-second timeout; and a
  malformed pointer-selected state incorrectly produced a legacy branch
  mismatch.

GREEN command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_portfolio_branch_compatibility_and_precedence tests.test_repository.RepositoryTests.test_portfolio_git_status_disables_configured_fsmonitor tests.test_repository.RepositoryTests.test_git_output_with_invalid_utf8_is_replaced tests.test_repository.RepositoryTests.test_installed_skill_fifo_is_hashed_without_blocking tests.test_repository.RepositoryTests.test_malformed_selected_state_does_not_fall_back_to_legacy -v
```

- Exit status: `0`
- Result: all `5` regression tests passed.

Post-fix verification commands:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- The complete suite passed all `42` tests.
- Repository validation and bytecode compilation exited `0`.
- Final diff whitespace validation exited `0` with no findings.

# Task 2 TDD Evidence

## RED reproduction

- Locked pre-Task-2 base: `dff6f5e5a4ca8db1563c296fb5106f2e9e66bdc4`
- Production GREEN commit: `375ca0fc7e51424184571b9675b2d28c77cb4bec`
- Isolation: detached temporary Git worktree at `<temporary-task-2-base-worktree>`
- Overlay check: `git status --short` reported only `M tests/test_repository.py`.
- Only `tests/test_repository.py` from the production GREEN commit was overlaid; Task 2 script,
  schema, and template changes were not present.

Command, run from `<temporary-task-2-base-worktree>`:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_state_schemas_accept_template_state tests.test_repository.RepositoryTests.test_init_run_creates_state tests.test_repository.RepositoryTests.test_rapid_init_runs_are_distinct_and_preserve_prior_artifacts tests.test_repository.RepositoryTests.test_pointer_replace_failure_preserves_current_pointer tests.test_repository.RepositoryTests.test_status_uses_current_pointer_and_falls_back_only_when_invalid -v
```

Result:

- Exit status: `1`
- Result: `1` test passed, `1` test failed, and `3` tests errored across the focused `5` tests.
- Generic missing-pointer failures: initialization and rapid repeated initialization did not
  create `.eng-level/current.json`; the atomic pointer-writing helper was absent.
- Generic singleton-state failure: status continued to read the singleton selected state after
  the current pointer was made invalid, instead of falling back to the legacy state as required.
- The schema/template compatibility test passed independently of the missing run-pointer behavior.

The temporary worktree was removed after the run.

## GREEN verification

Focused Task 2 tests:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_state_schemas_accept_template_state tests.test_repository.RepositoryTests.test_init_run_creates_state tests.test_repository.RepositoryTests.test_rapid_init_runs_are_distinct_and_preserve_prior_artifacts tests.test_repository.RepositoryTests.test_pointer_replace_failure_preserves_current_pointer tests.test_repository.RepositoryTests.test_status_uses_current_pointer_and_falls_back_only_when_invalid -v
```

- Exit status: `0`
- Result: all `5` focused tests passed.

Complete unit test suite:

```sh
python3 -m unittest discover -s tests -v
```

- Exit status: `0`
- Result: all `45` tests passed.

Repository and source verification:

```sh
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- Exit status: `0` for each command.
- Repository validation reported `ExecForge validation passed.`
- Bytecode compilation produced no findings.
- Diff whitespace validation produced no findings.

# Task 3 TDD Evidence

## RED reproduction

- Locked pre-Task-3 base: `77b4775`.
- Production files were unchanged when the focused tests first ran.

Command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_resume_reports_fresh_selected_run_without_inference tests.test_repository.RepositoryTests.test_next_pending_approval_and_open_blocker_are_safety_stops tests.test_repository.RepositoryTests.test_next_real_merge_conflict_has_highest_precedence tests.test_repository.RepositoryTests.test_next_honors_each_stop_boundary_only_after_it_is_reached tests.test_repository.RepositoryTests.test_resume_and_next_warn_and_stop_for_branch_or_commit_mismatch tests.test_repository.RepositoryTests.test_malformed_unsafe_selector_uses_safe_legacy_only_for_resume tests.test_repository.RepositoryTests.test_legacy_unknown_and_terminal_lifecycle_actions -v
```

- Exit status: `1`.
- Result: `22` errors across `7` test methods and their parameterized subcases.
- Failure reason: the required `resume_run` and `show_next` production entry
  points did not exist. No Task 3 behavior reached a passing state.

## GREEN verification

Focused Task 3 command (including CLI subprocess coverage):

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_resume_reports_fresh_selected_run_without_inference tests.test_repository.RepositoryTests.test_next_pending_approval_and_open_blocker_are_safety_stops tests.test_repository.RepositoryTests.test_next_real_merge_conflict_has_highest_precedence tests.test_repository.RepositoryTests.test_next_honors_each_stop_boundary_only_after_it_is_reached tests.test_repository.RepositoryTests.test_resume_and_next_warn_and_stop_for_branch_or_commit_mismatch tests.test_repository.RepositoryTests.test_malformed_unsafe_selector_uses_safe_legacy_only_for_resume tests.test_repository.RepositoryTests.test_legacy_unknown_and_terminal_lifecycle_actions tests.test_repository.RepositoryTests.test_resume_and_next_are_registered_cli_commands -v
```

- Exit status: `0`.
- Result: all `8` focused test methods passed, including each reached/not-reached
  stop boundary, a real merge conflict, safe legacy fallback, unsafe selector
  and state handling, lineage mismatches, blockers, unknown state, and terminal
  lifecycle actions.

Complete unit test suite:

```sh
python3 -m unittest discover -s tests -v
```

- Exit status: `0`.
- Result: all `72` tests passed.

Repository and source verification:

```sh
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- Exit status: `0` for each command.
- Repository validation reported `ExecForge validation passed.`
- Bytecode compilation and diff whitespace validation produced no findings.

## Task 3 quality and security correction

Correction base: `0ba152d75677329312e382189886dad733b85cd4`.

### RED

The quality/security review regression tests were added before production
changes. Command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_portfolio_branch_compatibility_and_precedence tests.test_repository.RepositoryTests.test_lineage_accepts_descendants_and_rejects_divergent_or_invalid_commits tests.test_repository.RepositoryTests.test_implementation_head_is_frozen_only_for_review_snapshots tests.test_repository.RepositoryTests.test_operating_state_rejects_malformed_or_oversized_metadata tests.test_repository.RepositoryTests.test_terminal_output_sanitizes_controls_and_hides_recorded_next_action tests.test_repository.RepositoryTests.test_unknown_lifecycle_state_is_a_blocking_reconcile_action tests.test_repository.RepositoryTests.test_git_diagnostics_reject_oversized_output -v
```

- Exit status: `1`.
- Result: `14` failures across `7` test methods and their parameterized
  subcases.
- Failures covered legacy `base_branch` misuse, descendant commit rejection,
  non-frozen implementation snapshots, malformed/oversized metadata, raw
  terminal controls and recorded next-action disclosure, non-blocking unknown
  state, and unbounded Git output.

### GREEN

The same focused command exited `0`; all `7` methods passed. The complete suite:

```sh
python3 -m unittest discover -s tests -v
```

- Exit status: `0`.
- Result: all `78` tests passed.

Resource lifecycle verification also passed with ResourceWarnings promoted to
errors:

```sh
python3 -W error::ResourceWarning -m unittest tests.test_repository.RepositoryTests.test_lineage_accepts_descendants_and_rejects_divergent_or_invalid_commits tests.test_repository.RepositoryTests.test_git_diagnostics_reject_oversized_output -v
```

- Exit status: `0`.
- Result: both tests passed without an unclosed pipe warning.

Lineage policy fixed by this correction:

- `branch` alone records the current branch. Missing/null `branch` produces
  `branch_lineage_unknown`; `base_branch` is never compared with the current
  branch.
- `commit` and `base_commit` must resolve to Git commit objects that are
  ancestors of current HEAD, so normal descendant work remains valid while
  invalid or divergent lineage blocks.
- `implementation_head` is exact only in `REVIEW_READY`, `REVIEW_PASSED`, and
  `SHIP_READY`. `BLOCKED` is phase-ambiguous and does not inherit a frozen
  implementation snapshot.

### Security delta review

- Mode: `sec-level review` against the real diff from `0ba152d`.
- AI-generated-code hot spots / A05 injection / A08 data integrity / A10
  exceptional conditions: examined. Selector/state reads are byte-bounded,
  state consumed by the commands is type/count/length validated, Git arguments
  used for lineage are restricted commit hashes, Git output and runtime are
  bounded, errors fail closed, terminal C0/C1/format/bidi/surrogate characters
  are escaped, and recorded `next_action` content is not emitted.
- A01 access control, A02 configuration, A03 supply chain, A04 cryptography,
  A06 abuse controls, A07 authentication, and A09 security logging: not
  applicable; the diff adds no endpoint, identity boundary, dependency,
  cryptography, or logging sink.
- Secret scan found only the deliberate fake `TOP_SECRET` test fixture used to
  prove output suppression; no credential or token was added.
- Unresolved S0/S1: none.
- Verdict: `SEC PASS`.

Final repository/source checks:

```sh
python3 scripts/execforge.py validate
python3 -m py_compile scripts/operating_state.py scripts/execforge.py tests/test_repository.py
git diff --check
```

- Exit status: `0` for each command.
- Validation reported `ExecForge validation passed.`

### Final frozen-lineage correction

Correction base: `39111d870081d7b53ee98c5b1f158ae33a759264`.

RED command:

```sh
python3 -m unittest tests.test_repository.RepositoryTests.test_frozen_states_require_complete_valid_lineage tests.test_repository.RepositoryTests.test_legacy_unknown_and_terminal_lifecycle_actions tests.test_repository.RepositoryTests.test_next_honors_each_stop_boundary_only_after_it_is_reached -v
```

- Exit status: `1`.
- Result: `15` failures across `3` methods and their parameterized subcases.
- Missing/null `base_commit` and `implementation_head` allowed
  `REVIEW_READY`, `REVIEW_PASSED`, and `SHIP_READY` to advance. Legacy frozen
  records with neither lineage anchor also advanced.
- Invalid/divergent base commits and invalid/mismatched implementation heads
  already failed closed during this RED run.

GREEN focused and full commands, with resource warnings promoted to errors:

```sh
python3 -W error::ResourceWarning -m unittest tests.test_repository.RepositoryTests.test_frozen_states_require_complete_valid_lineage tests.test_repository.RepositoryTests.test_legacy_unknown_and_terminal_lifecycle_actions tests.test_repository.RepositoryTests.test_next_honors_each_stop_boundary_only_after_it_is_reached -v
python3 -W error::ResourceWarning -m unittest discover -s tests -v
```

- Exit status: `0` for both commands.
- Focused result: all `3` methods passed.
- Full result: all `79` tests passed.
- Frozen states now require a non-null base commit that resolves to a commit
  reachable from current HEAD and a non-null implementation head exactly equal
  to current HEAD. Missing, invalid, divergent, or mismatched lineage returns
  the single stale-state reconciliation action with exit `1`.
- Legacy frozen records without complete lineage emit explicit
  `base_commit_missing` and `implementation_head_missing` warnings and cannot
  advance.

Security delta review examined the fail-open state transition and new warning
paths against the real diff from `39111d8`. The correction uses fixed warning
text, exposes no state contents, adds no dependency or command argument, and
routes incomplete evidence through the existing fail-closed stale precedence.
Unresolved S0/S1: none. Verdict: `SEC PASS`.
