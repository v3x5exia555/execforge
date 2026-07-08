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
