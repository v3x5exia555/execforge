# Fork each outside skill repo into this project

- **Started:** 2026-11-17
- **Last updated:** 2026-11-17
- **Role(s):** c-level (router only; direct operator instruction)
- **Branch:** lz-dependency-forks (made from lz-pstack-fork, so all forks sit together)
- **Status:** BLOCKED on one operator yes (14 gstack files held back by the push guard; everything else is pushed)

## What was asked

"let do fork each depancy repo into this project". Then: "once done inform me".

## The plan

ExecForge leans on outside skill repos. Today they are only named by link. We copy each
one into `forks/`, the same way pstack was copied.

| Repo | Why ExecForge needs it | State before this work |
| --- | --- | --- |
| garrytan/gstack | CEO plan bridge, browse, review, ship | link only |
| obra/superpowers | planning, test-first, finishing steps | link only |
| bergside/awesome-design-skills | design systems for `design-html` | link only |
| cursor/plugins pstack | extra working methods | already in `forks/pstack` |
| DietrichGebert/ponytail | simplest-solution style | already in `skills/ponytail`, pinned |

1. Write the pass test first: every copied file must match the outside repo byte for byte
   at one named commit (a commit is one saved version of a repo).
2. Copy gstack, superpowers and awesome-design-skills into `forks/<name>/`, unchanged.
3. Add a `PROVENANCE.md` to each: where it came from, which commit, licence, a hash of the
   whole copy (a hash is a fingerprint that changes if any byte changes).
4. Stop Git from changing line endings under `forks/`, so the fingerprints stay true.
5. Run the pass test, the repo tests and `validate`. Show the output.
6. Commit on this branch. Do not push. Tell the operator.

Not in this work: making ExecForge load skills from `forks/`, changing any copied file,
splitting skills, pushing, merging.

## Risks

### Risk A — the repo gets much bigger

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | gstack alone is about 90 MB and 5,000 files. Anyone who downloads ExecForge after a merge waits longer and gets files they do not use. Once pushed to the public repo, the size stays in the history for good. |
| **Short or long term?** | `LONG` |
| **Solution** | Keep it on this branch, not pushed, until the operator decides. A later option is to keep only the gstack skill files and drop its test data. |
| **What would the solution fix?** | none of these |
| **Risk of the solution itself** | A trimmed copy is no longer a true copy, so comparing with the outside repo gets harder. |
| **Cost** | not measured |
| **What we expect after** | Nothing is pushed until the operator says so. |
| **Does a human need training?** | `NO` |

### Risk B — the copies go stale

| Question | Answer |
| --- | --- |
| **How bad?** | `MEDIUM` |
| **What actually happens?** | The outside repos keep changing (gstack changed today). Our copies freeze at today's commit. Fixes made outside do not reach us unless someone updates by hand. |
| **Short or long term?** | `LONG` |
| **Solution** | Each `PROVENANCE.md` names the commit. To update: compare with that commit and review by hand. No automatic update. |
| **What would the solution fix?** | compliance (we always know exactly what we hold) |
| **Risk of the solution itself** | Manual updates get skipped, so the copies age. |
| **Cost** | Build: small. Upkeep: a hand review per update, not measured. |
| **What we expect after** | Every fork states its commit and fingerprint, and the pass test can re-check it. |
| **Does a human need training?** | `YES` — the operator needs to know the copies do not update themselves. |

### Risk C — two copies of the same skill on this Mac

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | Claude Code runs the installed copies under `~/.claude`, not `forks/`. Someone edits a file in `forks/` and nothing changes in real use, or the other way round. |
| **Short or long term?** | `LONG` |
| **Solution** | none yet. `forks/` is a reference copy only until the operator decides how it is used. |
| **What would the solution fix?** | none of these |
| **Risk of the solution itself** | not applicable until a solution is chosen |
| **Cost** | not measured |
| **What we expect after** | The provenance files say plainly that the installer does not ship these copies. |
| **Does a human need training?** | `YES` — the operator: edits in `forks/` do not change the running skills. |

### Risk D — licence and the public README

| Question | Answer |
| --- | --- |
| **How bad?** | `LOW` |
| **What actually happens?** | All three are MIT (free to copy if the licence file is kept). The licence files are kept. gstack also carries a `licenses/` folder for parts it copied from others; it is kept too but was not read line by line. The README still says ExecForge "never forks" outside skills, which this branch makes untrue. |
| **Short or long term?** | `SHORT` |
| **Solution** | Keep every licence file. Change the README sentence before any merge. |
| **What would the solution fix?** | compliance |
| **Risk of the solution itself** | A reworded README could over-promise support for the copies. |
| **Cost** | not measured |
| **What we expect after** | Licence files present in each fork; README sentence flagged to the operator. |
| **Does a human need training?** | `NO` |

## Choices made

| Date | What we chose | Why |
| --- | --- | --- |
| 2026-11-17 | Copy whole repos unchanged, under `forks/` | Same pattern as the pstack fork; a true copy can be checked against the source. |
| 2026-11-17 | New branch from `lz-pstack-fork`, own folder | The current branch has unsaved pilot edits and a do-not-push rule. |
| 2026-11-17 | Fetch from GitHub, not from the copies installed on this Mac | Installed copies may have local changes. |
| 2026-11-17 | Push the full copies to the branch on GitHub | Operator instruction ("create a new commit and push it"), given after the size warning in Risk A. |
| 2026-11-17 | Left out: agent-skills, axe-core | ExecForge files do not name agent-skills; axe-core is a test tool, not a skill repo. |

## What happened

- 2026-11-17 — plan written; branch and folder made.
- 2026-11-17 — pass test written and seen failing first. Three repos copied. Pass test then showed all files matching. Repo tests and `validate` passed.
- 2026-11-17 — a scan found key-looking strings in 13 gstack files (mostly its own tests for hiding secrets). They are already public in gstack and were not checked one by one.
- 2026-11-17 — before the push, the key-looking strings were listed. All are plain made-up examples (counting-up digits and letters, or the word EXAMPLE). No real key seen. The samples are not quoted here, because the push guard would flag this file too.
- 2026-11-17 — operator asked for a push. The push guard on this Mac (a check that scans a push for passwords and keys) could not read one 90 MB commit, so the work was split into smaller commits with the same content and pushed part by part.
- 2026-11-17 — the guard then stopped the gstack tests: 63 serious findings in 13 files. Each line was read. All are made-up samples inside gstack's own tests (counting-up letters and digits, passwords such as "pw", a key header with no key behind it). No real key was seen. All are already public in garrytan/gstack.
- 2026-11-17 — the guard was not switched off or skipped. Pushed: superpowers, awesome-design-skills, and gstack without those 13 files. Held in one local commit, not pushed: the 13 files, one more file the guard cannot read at all (`lib/diagram-render/dist/diagram-render.html`, 7.9 MB of packed web code on very long lines; a hand scan of it found nothing serious), and gstack's `PROVENANCE.md` (held so GitHub does not claim a full copy that it does not yet have).

## Still unclear

- The 14 held gstack files: push them with the guard skipped for that one push, or leave them out for good and say so in `PROVENANCE.md`? Operator. (An allow-list would cover the 13 sample files but not the one the guard cannot read.) The list is in the last local commit.

- Should the copies be used by ExecForge (installed from `forks/`), or kept as reference? Operator.
- Keep all of gstack, or only its skill files? Operator.

## Result

Copied, unchanged, with a `PROVENANCE.md` each:

| Fork | Files | Pinned commit |
| --- | --- | --- |
| `forks/gstack` | 5,071 | 5b4fa9e (2026-11-17) |
| `forks/superpowers` | 236 | 22f0b46 (2026-11-03) |
| `forks/awesome-design-skills` | 215 | f631a09 (2026-06-28) |

Proof: the byte-for-byte check passed for all three, on the working files and again on the saved commit. Repo tests: 109 OK. `validate`: passed.

On GitHub, branch `lz-dependency-forks`: superpowers and awesome-design-skills in full, gstack minus 14 files. On this Mac only: the full copy. Left out: merging into main, the README sentence that says ExecForge never forks, and any change that makes ExecForge use these copies.
