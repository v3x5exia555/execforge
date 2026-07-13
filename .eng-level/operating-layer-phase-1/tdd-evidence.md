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
