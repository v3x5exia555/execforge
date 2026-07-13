# Changelog

## 0.10.0 — 2026-07-14

Operating layer: ExecForge now watches itself and its siblings across a multi-repository,
multi-harness setup — a single operator running Claude Code and Codex over several
projects.

- Added **`doctor --installed`**: compares bundled skills against every known install
  root (`~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`) and reports missing or
  content-drifted files without modifying any installation.
- Added **`doctor --portfolio <path>`**: a read-only scan of direct-child Git
  repositories for missing `AGENTS.md`/`CLAUDE.md` instruction parity, unresolved Git
  conflicts, and lifecycle state whose recorded branch or commit lineage no longer
  matches what is actually checked out.
- Added **initiative-scoped operating state**: `init-run` now creates matching run IDs
  under `.execforge/runs/<run-id>`, `.eng-level/runs/<run-id>`, and
  `.q-level/runs/<run-id>`, selected through an authoritative `.execforge/current.json`.
  `.eng-level/current.json` and `.q-level/current.json` remain compatibility
  projections, not stronger evidence than the run artifacts, Git, code, or tests.
  Legacy root state stays readable and is never silently migrated or deleted.
- Added **`resume --root <repo>`** and **`next --root <repo>`**: `resume` reports the
  selected run, the repository's real branch/HEAD, staleness warnings, blockers, the
  stop-after boundary, and evidence paths. `next` derives exactly one safe next action
  and fails closed on Git conflicts, unsafe or stale state, missing approval, blockers,
  or a `stop_after` boundary.
- Built and reviewed as its own fully governed initiative (upstream requirements, plan
  review, staff review, security review — `SEC PASS`) in
  `.eng-level/operating-layer-phase-1/`; 89 tests pass including fail-closed coverage
  for cross-platform selector links, frozen review lineage, and stale branch evidence.
- Verified against the operator's real project portfolio during integration:
  `doctor --portfolio` caught genuinely stale `.eng-level/state.json` in two sibling
  repositories whose recorded branch no longer matched the branch actually checked out.
- Deferred (see `.eng-level/backlog.md`): fsync-before-publish durability, versioned
  state schemas, external-producer input bounds, Windows runtime verification, and a
  concurrent portfolio-scan race — none block this phase's scope.

## 0.9.0 — 2026-07-13

Evidence release: the skills' behavioral evals now execute, and governed verdicts can
route through installed gstack tooling.

- Added `execforge eval`: parses `evaluations/*.eval.md`, replays the scenario through a
  headless agent, grades the transcript with an LLM judge, and recomputes the verdict
  locally (the judge's own pass claim is never trusted). Advisory CI job
  (`evals.yml`) runs a capped set on skill changes; skips without an API key.
- The parser's first run caught a real drift: `eng-level-post-hoc-and-stop.eval.md`
  used a two-scenario `## Scenario A/B` layout the evaluations README never allowed.
  Split into `eng-level-post-hoc-review` and `eng-level-stop-after`, one behavior each.
- Added `execforge release-check` and a tag-push Release Gate workflow: both plugin
  manifests, the CHANGELOG head entry, and the tag must agree; malformed tags (the
  historic `v.1.0.0` form) are rejected. The stray `v.1.0.0` tag has been deleted
  locally and on origin.
- Wired release consistency into the lifecycle: `eng-level` now requires
  release-consistency evidence before a `SHIP` on a release-bound branch —
  `release-check` output in this repository, a recorded manual manifest check
  elsewhere. A failing check is a P1.
- Added conditional gstack bridges: q-level tool routing prefers installed `/browse` +
  `/qa` for logged-in portal evidence; eng-level records a post-`SHIP` handoff to
  `/land-and-deploy`; sec-level lists `/cso` as an optional runtime-evidence tool.
  All bridges require gstack to be installed; every fallback contract is unchanged.

## 0.8.0 — 2026-07-12

Derived from a review of 469 real prompts across five projects. Every change below answers a
failure observed in that record, not a hypothetical one.

- Added **roles** to `eng-level` — `architect`, `manager`, `staff-engineer`, `backend-engineer`, `platform-engineer` — as lenses that attach to lifecycle stages rather than as new skills. `backend-engineer` and `platform-engineer` attach three times each: advising at plan, building at implement, auditing at review. Contracts in `skills/eng-level/references/role-contracts.md`. Roles are a runtime concern; `BUNDLED_SKILLS`, both plugin manifests, and the validator are unchanged.
- Added **role auto-routing** (`references/role-routing.md`): roles are inferred from the request and the change surface, announced in one line, and run without a confirmation gate. Users are never required to name a role or type a flag. Routing is intent-level, not keyword-level, and biases to the superset when ambiguous — a missed lens ships a defect, an extra lens costs tokens.
- Added **adversarial reviewer pairing** (`references/reviewer-briefs.md`, `references/subagent-dispatch.md`): a `pragmatist` and a `purist` review the same scope and are required to pre-rebut each other. Engages automatically when a change touches schema, migrations, money, identity resolution, or third-party evidence. Disagreements are reconciled by sequencing, not averaging; only the irreducible taste call is escalated. Actions carry `[C]` / `[R]` / `[gate]` provenance. No subagent may issue a ship verdict.
- Added the **`POST-HOC REVIEW`** label and the `SHIP WITH REQUIRED FIXES (UNGATED)` verdict ceiling: a substantial diff with no approved upstream requirements is still reviewed, but cannot return `SHIP`. Makes the cost of building before gating visible in the output instead of hidden.
- Added **`--stop-after=<stage>`** to `eng-level` and `full-cycle`, plus a durable deferred backlog at `.eng-level/backlog.md` (template in `assets/backlog.template.md`). A stated intent to stop — "plan it but do not deploy", "keep it for next cycle" — sets the parameter and survives later turns. Deferred work records why it was deferred, what unblocks it, and the condition that pulls it forward. `--mode=status` reads it.
- Made **acceptance criteria enforceable**: a plan whose implementation tasks lack binary pass tests is `REVISE`. "Test until it works" is not an acceptance criterion.
- **Gating initiative flags now attach `sec-level` automatically** (`full-cycle` rule 8). The authorization gate decides whether work is *permitted*; `sec-level` decides whether it is *safe*. Passing one never substitutes for the other.
- Added a **trigger alias table** to `c-level`: `product plan`, `c-plan`, `QA-level`, `eng-plan`, `designer`, `eng-lifecyle` and other real-world phrasings route to the correct skill without asking the user to restate the request.
- Added evaluations `eng-level-role-routing.eval.md` (real prompts as the ground-truth routing set) and `eng-level-post-hoc-and-stop.eval.md`.

### Fixed (found by an independent Codex CLI structure review)

- **The Codex plugin manifest was unloadable.** `.codex-plugin/plugin.json` declared `"skills"` as an array of skill names, copied from the Claude manifest format. The Codex plugin contract requires a plugin-root-relative **path string** (`"skills": "./skills/"`). The bundle has never been installable as a Codex plugin; `execforge.py install` masked this by copying skill directories and bypassing the manifest entirely. Manifest corrected, and `license`/`interface` metadata added.
- **The validator was asserting the broken shape.** `validate_repo` checked both manifests against one contract (`skills == BUNDLED_SKILLS`), which is what hid the defect. Split into `_validate_claude_manifest` (name array) and `_validate_codex_manifest` (path string, resolves to a real directory containing every bundled skill), with a regression test that the name-array shape is now rejected.
- **Roles, temperament, and the stop boundary are now persisted.** They were documented as parameters but nothing recorded them, so the claim that a stop boundary "survives a later turn" was false. Added `routed_roles`, `temperament`, `adversarial_pair`, `stop_after`, and `post_hoc_review` to `state.template.json` and the state schema. `eng-level` must write the routed set before work starts; an unrecorded role did not run and must not be claimed.
- **`SHIP WITH REQUIRED FIXES (UNGATED)` was invalid under the repo's own schema.** Added to the `final_decision` enum.
- **`init-run` now creates `.eng-level/backlog.md`** from the template. `--mode=status` had been documented as reading a file nothing created.
- **The state schema was missing six keys it was supposed to govern** (`upstream_source`, `upstream_approved_by`, `upstream_approved_at`, `implementation_head`, `plan_status`, `required_conditions`). `additionalProperties: true` let the template drift from the schema unnoticed. Added, plus a test asserting the template validates against the schema.
- **`--role` could suppress a mandatory lens.** `role-contracts.md` said an explicit role means "that lens only", which would let a user route around a required `staff-engineer` diff review. An explicit role now narrows advisory lenses only; `staff-engineer` (on any diff) and `architect` + `manager` (at plan) always attach.
- **Added a subagent-unavailable fallback.** Dispatch is not available in every host. Roles now run sequentially in-line when parallel dispatch is unavailable, with the run explicitly labelled and a failed role recorded as `UNVERIFIABLE` rather than passing silently.
- **Builder-audits-self independence is now stated.** When `backend-engineer` or `platform-engineer` implements a surface, its own review of that surface is a self-check, and `staff-engineer` remains the independent reviewer of record.
- Fixed a routing example that violated its own superset rule ("cost and scale… domain and vps" routes to `architect` **and** `platform-engineer`).

## 0.7.0 — 2026-07-08

- Added an **initiative-flags** mechanism to `execforge`: named flags (`offensive-security`, `legally-gated`, `regulated-impersonation`, `user-prescribed-mechanism`) set at the product/upstream stage that arm conditional downstream governance gates. Detailed catalog and contracts in `skills/execforge/references/initiative-flags.md`.
- Added an **Authorization / Rules-of-Engagement gate**: a hard STOP before implementation for offensive-security, legally-gated, or brand-impersonation work, requiring a recorded `AUTHORIZED` / `NOT AUTHORIZED` / `N-A (justified)` decision with written authorization, scope of engagement, consent basis, no unapproved third-party impersonation, and captured-data handling. Wired into `full-cycle` (operating rule 7 + validation gate), the `eng-level` upstream stop check, and clarified against technical appsec in `sec-level`. The agent never self-answers this gate.
- Added a **goal-vs-mechanism guard** to `execforge`: when a request prescribes a mechanism, the outcome and the mechanism are stated separately and the review may redirect to root cause.
- Made **acceptance criteria / definition of done** a required field in the `eng-level` upstream-requirements artifact.
- Added `docs/authorization-gate.md` (+ nav), an authorization-gate evaluation case, and repository tests covering the initiative-flags reference and gate contract.
- Added bundled `full-cycle` skill: an end-to-end lifecycle orchestrator that sequences product decision, upstream approval, optional design, plan review, implementation, Staff Engineer review, QA gate, delta review, and the final ship verdict, with two mandatory user gates and evidence-backed stage tracking.
- Added bundled `sec-level` skill: an application-security actor with plan-stage threat modeling (STRIDE), a diff-stage adversarial review mapped to OWASP Top 10:2025 and AI-generated-code failure patterns, S0–S3 severities aligned with eng-level, and a `SEC PASS / FIX REQUIRED / BLOCK` verdict.
- Added `full-cycle` and `sec-level` to the `c-level` router, `full-cycle` stage rules, plugin manifests, docs navigation, and evaluations.
- Added a Stage 4 fallback implementation contract to `full-cycle` for harnesses without Superpowers: task-by-task, test-first execution with explicit stop conditions and mandatory fallback labeling.

## 0.5.0 — 2026-07-06 (first tagged release)

- Added bundled `design-html` for translating approved product scope into UX/interface and HTML/CSS-oriented output.
- Expanded `q-level` with richer seeded artifacts, stronger state/schema tracking, and a dedicated data-QA attachment contract/template.
- Added design-html and data-QA documentation plus new example artifacts.
- Updated plugin manifests, installer/validator bundle checks, and repository tests for the expanded skill bundle.
- Split the legacy root skill monoliths (`ExecForge_SKILL.md`, `Eng_Level_SKILL_eng_skill.md`) into progressive references under `skills/execforge/references/` and `skills/eng-level/references/`, and removed the root files; the validator now rejects root-level skill files.
- Added a `doctor` CLI command for installation and dependency validation, and made `install` validate the bundle before copying and verify every installed skill afterwards.
- Added behavioral evaluation cases under `evaluations/`, one per bundled skill.
- Added GitHub Actions CI (validate, doctor, tests, strict docs build) and a GitHub Pages docs deployment workflow.
- Rewrote the README with requirements, a full CLI reference, evaluations, CI, layout, and release documentation.

## 0.4.0 — Portal/API/backend Q Level

- Added `q-level` with Portal, API, and Backend/Data QA actors.
- Added QA plan and environment approval stop check.
- Added cross-layer requirement coverage and defect routing.
- Added Playwright, Schemathesis, Testcontainers, Pact, k6, axe-core, and ZAP routing guidance.
- Integrated QA into the engineering ship lifecycle.
- Added QA schemas, templates, examples, documentation, CLI initialization, and tests.

## 0.3.0 — Platform rebuild

- Added `c-level` bootstrap/router skill.
- Reorganized skills into Agent Skills-compatible directories.
- Split large skill bodies into progressive references.
- Added upstream user approval and traceability contracts.
- Added Superpowers lifecycle integration.
- Added installer, validator, run initializer, and status CLI.
- Added JSON schemas, examples, tests, and CI.
- Added MkDocs wiki and GitHub Pages deployment workflow.
- Added Claude and Codex plugin manifests.

## 0.2.0

- Added CEO/COO subagent topology.
- Added engineering lifecycle and upstream user stop check.
