# Make the sessions warning mean something

> Write this file in plain, simple English. Short everyday words. Short sentences.
> No jargon. If you must use a technical word, say what it means in a few words.
> Someone who does not know this codebase should still be able to follow it.

- **Started:** 2026-08-08
- **Last updated:** 2026-08-08
- **Role(s):** execforge (product decision)
- **Branch:** none yet — review only, nothing built
- **Status:** PLANNING

## What was asked

"Trigger execforge for me understand what is this about."

Read as: run a proper product review on the thing left open after PR #9 landed — the
`sessions` command warning about work that turns out to be empty, plus the two leftovers
it pointed at.

## Initiative and mode

**Initiative:** decide whether to change how `sessions` warns, and whether to clear the
two leftovers it found.

**Mode:** single isolated review. Documentation and one small function, one repo, no
auth, no data, reversible in one revert. That is below the bar for two reviewers.

## Gatekeeper — does the user actually need this? YES

The pain is measured, not guessed.

- FACT: `sessions` decides using `git merge-base --is-ancestor tip HEAD`. If the tip is
  not an ancestor, it warns. It never asks whether the branch holds any content.
- FACT: on 2026-08-08 the command produced two warnings. Both were empty.
  - `feat/v0.9.0-evidence-bridges` — 1 commit `main` lacks, **0 files different**. Its
    feature shipped in PR #2 on 13 July. The extra commit is a merge someone made back
    into the branch afterwards.
  - A worktree at `/private/tmp/execforge-task2-red.uc1jKk` — **the folder no longer
    exists**, and its commit is already in `main`.
- FACT: the repo carries 30 refs, so more leftovers are likely, not fewer.
- ASSUMPTION: the noise rate stays high as branches pile up. One day's data, not a trend.

A gate that was wrong twice out of twice teaches the reader to skip it. That is worse
than having no gate, because it still costs attention.

## Initiative flags

None set. Not offensive-security, not legally-gated, not regulated-impersonation, no
user-prescribed mechanism.

## Scope mode

**Selective Expansion.** One rule sharpened inside a command that already exists, plus
housekeeping. No new concept.

## CEO finding (advisory)

The job-to-be-done is "tell me if I am about to merge on top of someone's unfinished
work". Today the command answers a narrower question — "is this tip an ancestor" — and
that question has a different answer from the real one often enough to matter.

The 10× version is not more warnings, it is warnings the reader trusts. Content-aware
output turns a list to skim into a list to act on. Risk: a command nobody reads.

## COO finding (advisory)

Cost is one extra `git diff --quiet` per flagged branch — only for branches already
failing the ancestor check, so a handful at most. No runtime, no data, no dependency.

The operational risk is the opposite of the current one: if `sessions` hides
zero-content branches entirely, a reader could miss a branch that is genuinely stale and
should be deleted. Label them, do not hide them.

Sunset: if the noise rate stays near zero for a quarter, the extra check earns nothing
and can go.

## Contradiction register

None. Both views agree the fix is small and the risk is in presentation, not logic.

## Scope ledger

| Decision | Item | Why |
| --- | --- | --- |
| `ADD NOW` | `sessions` labels a flagged branch that has no file differences as bookkeeping, not work | Cuts today's false warnings from 2 to 0 without hiding anything; unlocks a gate a reader can trust rather than skim |
| `ADD NOW` | CHANGELOG entry and 0.14.1 for the Windows fix that landed in PR #9 | Restores the repo's own rule that shipped changes are recorded; `no baseline yet`; unlocks an honest release note |
| `ADD NOW` | Delete `feat/v0.9.0-evidence-bridges`, prune the dead worktree | Removes the two things proven empty; unlocks a clean `sessions` run where any future warning is real |
| `DEFER` | Have `sessions` delete or prune anything itself | Reopen when a reader has cleared the same leftover twice, or a third empty branch appears |
| `SKIP` | Any change to what counts as unmerged | The ancestor check is correct. The gap is what gets *said* about the result, not how it is found. |

## OKR plan

**Product hypothesis:** we believe someone landing work skips the pre-merge check
because it reports leftovers as if they were live work. By naming empty branches as
bookkeeping, we expect the check to be read rather than skipped.

**Job-to-be-done:** before merging, know whether anyone's unfinished work is about to be
buried — without sorting real work from dead branches by hand.

**Objective:** the pre-merge session check is trusted enough to act on.

**Key results:**

| KR | Baseline | Target |
| --- | --- | --- |
| Warnings that turn out to be empty | 2 of 2 on 2026-08-08 | 0 of the warnings shown as work |
| Branches flagged with no content difference | 1 (`feat/v0.9.0-evidence-bridges`) | 0 after cleanup |
| Stale worktree entries | 1, folder already deleted | 0 |

Baselines are one day's real output from this repo, not estimates. No trend data exists
yet; anything beyond one day would be invented.

## A-C-T-I-O-N operational matrix

- **A — Assess the problem.** The check answers "is this tip an ancestor" when the
  reader asked "is there unfinished work here", causing warnings that are true but
  useless, for anyone about to merge.
- **C — Cost optimisation.** One `git diff --quiet` per already-flagged branch. No new
  dependency, no runtime, no storage.
- **T — Technical tactics.** Reuse the git call already in the function. No new module,
  no config, no flag.
- **I — Incorporate security, governance, compliance.** No auth, secrets, personal data,
  or network surface. Read-only git commands. `sec-level` not required.
- **O — Operational work reduction.** Removes the manual step of checking each flagged
  branch by hand to see whether it holds anything.
- **N — No manual work by default.** The label is computed, not typed. Deleting the dead
  branch stays a human decision on purpose — see the `DEFER` row.

## Non-negotiable controls

- Empty branches are **labelled, never hidden**. A silent gate is the failure mode this
  review exists to avoid.
- The ancestor check itself does not change.
- `sessions` stays read-only. It reports; it does not delete, prune, or merge.

## Roadmap, owners, rollback, kill criteria

- **Owner:** operator.
- **Roadmap:** one change to `show_sessions` plus a test; separately, the CHANGELOG entry
  and version bump; separately, the cleanup. Three small pieces, landed in that order.
- **Rollback:** one revert. Nothing persists, nothing migrates.
- **Kill criteria:** if a real branch is ever mislabelled as bookkeeping, the label goes
  and the plain warning returns.

## Final verdict — first pass

**GO.** The pain is measured rather than assumed, the fix is one comparison the code
already has the pieces for, and the failure mode is contained by labelling instead of
hiding.

## Final verdict — revised after challenge

**The operator asked "do I need this feature?" and the honest answer was no. The first
verdict was wrong.**

What the first pass got wrong: it leaned on "2 of 2 warnings were noise", which made a
one-time mess look like a repeating flaw. Checking the history properly:

- FACT: 30 refs across the repo's whole history, and exactly **one** zero-content
  branch has ever existed.
- FACT: deleting that branch removes the warning permanently — it cannot recur for that
  branch.
- FACT: merged branches are already deleted at merge time (`--delete-branch`), which is
  why this leftover survived only from July, before that habit.
- INFERRED: on a single-operator repo, "am I burying someone else's work" is a weaker
  job than it first appeared.

Cleanup costs no code, no test, and no version bump, and closes both warnings for good.
The labelling change would cost all three and be maintained forever, to catch a case
that has happened once and was about to be deleted.

**Revised verdict: the labelling change moves from `ADD NOW` to `DEFER`**, under the
reopen condition the first pass had already written — a third empty branch appears.

## Revised scope ledger

| Decision | Item | Why |
| --- | --- | --- |
| `ADD NOW` | Delete `feat/v0.9.0-evidence-bridges`, prune the dead worktree | Closed both warnings at zero cost; `sessions` now reports `clear`, so any future warning is real |
| `ADD NOW` | CHANGELOG entry and 0.14.1 for the Windows fix | Restores the rule that shipped changes are recorded; unlocks a release note that matches what actually shipped |
| `DEFER` | Label zero-content branches as bookkeeping | Reopen when a third empty branch appears, or the same leftover is cleared twice |
| `SKIP` | Any change to what counts as unmerged | The ancestor check is correct. |

## Still unclear

- Nothing. The 19 remote branches, most already merged, are housekeeping the operator
  has not asked for.

## Result

Cleanup done, no code written:

- Deleted the remote branch `feat/v0.9.0-evidence-bridges`. Verified empty first — its
  tree was identical to the merge base and `main` was 3,093 lines ahead.
- Pruned the worktree registration for `/private/tmp/execforge-task2-red.uc1jKk`, whose
  folder no longer existed.
- `sessions` now reports: `clear — no other working copy or branch holds commits
  outside HEAD`.

Recorded the Windows fix as 0.14.1. Verified: 104 passed, 221 subtests; release-check
consistent.

The feature this plan was originally written to justify was **not built**, on purpose.
