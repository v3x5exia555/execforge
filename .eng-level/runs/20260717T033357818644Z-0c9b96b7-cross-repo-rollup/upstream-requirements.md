# Upstream Requirements — Cross-Repo Roll-up

- Upstream source: ExecForge product decision (this session, 2026-07-17), verdict **MODIFY** — Citadel-as-proposed reaffirmed KILL; productivity goal redirected to a single read-only cross-repo roll-up command.
- Approval status: **PENDING** — awaiting `APPROVE UPSTREAM`.
- Mode: `plan` (stop after plan review; no implementation this run without a new instruction).

## What, why, and for whom

For a single operator running Claude Code and Codex across several repositories:
add one read-only CLI command that aggregates the diagnostics ExecForge already
produces per repository into a single prioritized worklist, so the operator gets
"what do I do next across all my repos, and where is there drift" from one
command instead of running `doctor --portfolio`, `status`, and `next`
repeatedly per repo.

## Primary user

Single operator, multi-repository, multi-harness (Claude Code + Codex).

## In scope

1. A new read-only CLI subcommand (working name `portfolio-next`) that, given a portfolio root, iterates its direct-child Git repositories and prints, per repo: the single next safe action (same logic as `next`) plus any drift/stale/blocker findings (same logic as `doctor --portfolio` / `resume`).
2. Deterministic ordering that surfaces blocked/stale/unsafe repos before clean ones.
3. Reuse of existing `operating_state.py` machinery (bounded reads, terminal-safe output, symlink/path containment, Git lineage checks). No new parsing or IO primitives.
4. Documentation and unit tests for the new command.
5. A runnable behavioral eval for the roll-up behavior.

## Deferred

- Opt-in local per-cycle time/cost note (product backlog #10).
- Lifecycle hooks (#11).

## Skipped

- Any second governance system (no Citadel adoption).
- Telemetry or cost attribution transmitted anywhere.

## Non-goals

- Daemon or any long-running process.
- Dashboard / GUI / web view.
- Fleet management or multi-operator control plane.
- Unattended or autonomous execution / mutation.
- Any write to, or mutation of, a scanned repository.

## Success metrics

- Time-to-"next action across all repos" drops from N per-repo command invocations to 1.
- Zero regression: every drift/stale/blocker finding the existing per-repo commands report is present in the roll-up.
- After ~2 weeks of use, the operator can name ≥1 quantified bottleneck (the evidence gate for pulling telemetry #10 forward).

## Acceptance criteria / definition of done

- AC1: Running the command against a portfolio root prints one prioritized worklist, one entry per repo; each repo shows exactly one next action plus its findings.
- AC2: The command is strictly read-only — a test asserts no scanned repository is modified (no new/changed/deleted files) after a scan.
- AC3: For a repo with a Git conflict, stale/branch-mismatched state, or an open blocker, the roll-up shows the same finding codes the existing `doctor --portfolio` / `next` produce (no-regression parity test).
- AC4: Output is bounded and terminal-safe (control characters escaped; no unbounded metadata) — reuses `_terminal_safe`; a test feeds hostile metadata and asserts sanitization.
- AC5: Malformed/legacy/unreadable state in one repo is reported, not fatal — the scan continues over remaining repos.
- AC6: `evaluations/eng-level-verify-before-claiming.eval.md` is treated as a governed acceptance artifact: the roll-up must not assert a repo is "ready/clean" without the underlying finding evidence, mirroring the verify-before-claiming invariant.
- AC7: `validate`, `test_skill_bundle`, and the full unit suite remain green on POSIX and the Windows CI job.

## CEO decisions

- Smallest defensible scope only; no control-plane features.
- The roll-up must reuse existing diagnostics, not fork or reimplement them.
- Ship as a pilot whose usage produces the "measured need" evidence the original Citadel rejection said was missing.

## COO controls

- Read-only by default; no mutation of any scanned repository.
- No prompt/credential/PII/telemetry capture; no network transmission.
- Bounded, terminal-safe output; tolerate malformed/legacy state without crashing.
- No new long-running runtime; zero new third-party dependencies.

## Assumptions

- The operator's real drain is cross-repo state-discovery/context-switching (asserted, not yet measured — KR3 is the measurement).

## Unknowns

- How many repos, and how often drift/staleness actually costs time.
- Preferred output shape (flat list vs grouped by severity) — a plan-review decision.

## Initiative flags and authorization status

- offensive-security: not set
- legally-gated: not set
- regulated-impersonation: not set
- user-prescribed-mechanism: **set** — Citadel was the named mechanism; the product decision redirected it to this minimal roll-up. Evaluate the goal, not Citadel.
- Authorization / Rules-of-Engagement: **N-A (justified)** — local, read-only developer-workflow command; no gating flag set. Existing downstream gates remain authoritative.

## Kill criteria

- The command is not used within ~2 weeks of shipping.
- It cannot surface a quantified bottleneck (fails to produce the evidence gate).
- It would require any mutation of scanned repositories, a daemon, or a second governance system to be useful.
