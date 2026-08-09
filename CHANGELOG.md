# Changelog

## 0.15.0 — 2026-08-09

- New **Stage 0b — Risk register** in `full-cycle`, sitting between the Stage 0 product
  decision and the Stage 1 upstream approval gate. Nine questions per risk: how bad; what
  actually happens; short or long term; the solution; what the solution would fix
  (operational load / manual work / automation / compliance); the risk of the solution
  itself; cost including ongoing upkeep; what we expect after; and whether a human needs
  training. Ships with `skills/full-cycle/assets/risk-register.template.md`.
- Placed before the approval gate on purpose: the user approves scope **and** its risks in
  one decision instead of two. The register is updated, never rewritten, when a later
  stage finds a new risk.
- New validation-gate line: no `HIGH` risk reaches the final verdict without a solution or
  a recorded decision to accept it, naming who accepted it. Grading a risk down to dodge
  that line is named in the skill as the failure it exists to catch.
- Numbered `0b` rather than renumbering Stages 3–9. Renumbering would have touched 10
  files, including two eval cases and two historical plan records — and rewriting history
  to match a later change would falsify the record.
- `c-level` gains a router row between the product row and the engineering-plan row, plus
  trigger words (`risk register`, `risk framework`, `risk assessment`, `what are the
  risks`).
- `No risks identified` with a one-line reason is allowed, so small changes are not forced
  through ceremony. A silent skip is not.

## 0.14.3 — 2026-08-08

- New `docs/product-plan.md`. ExecForge required a product hypothesis, job-to-be-done,
  objective, and key results with real baselines from every initiative it reviewed, and
  had never applied that to itself. It does now.
- Every figure in it is measured, not estimated: 0 stars / 0 forks / 0 watchers after
  5 weeks public, 1 human contributor, 9 skills, 19 releases, 99 commits, and **2
  recorded ExecForge decisions across those 99 commits** — the sharpest gap the plan
  names, and the only key result fully within reach.
- The target user is recorded as an **open question owned by the operator**, not filled
  in. The evidence says one person today; that is a legitimate answer but has to be
  chosen rather than defaulted into, and almost every other line of the plan depends on
  it. Inventing an adoption target would be the exact fabrication the skill forbids, so
  KR3 carries `no baseline yet`.
- Known gaps are named rather than quietly fixed: the roadmap lists features instead of
  benefits (deferred — a benefit needs a beneficiary, which is the open question), plans
  live in two folders, and 19 releases have shipped with no feedback loop.

## 0.14.2 — 2026-08-08

- `.gitattributes` now pins every file to LF on every platform (`* text=auto eol=lf`),
  not just the vendored `ponytail` paths. 0.14.1 fixed the one folder that had already
  broken; this closes the class. Any file added later — including a future vendored
  snapshot pinned by hash — is covered without anyone remembering to add a rule.
- Verified as a no-op today: the repo is already all-LF, and `git add --renormalize .`
  rewrites nothing. The `skills/ponytail/**  -text` rule still wins for those paths, so
  the hash-pinned snapshot keeps the strictest treatment available.

## 0.14.1 — 2026-08-08

- Fix a live Windows failure in `validate`, and therefore in `doctor` and `install`,
  which both run it first. The stray-root-skill check used `glob("*SKILL*.md")`; on
  Windows `pathlib` applies `os.path.normcase` inside `glob`, so the pattern matched
  case-insensitively and flagged the repo's own `skill-usage-feedback.md` as a legacy
  root skill file. The token is now matched case-sensitively. Landed in PR #9 (branch
  dated 2026-07-17) without a CHANGELOG entry; recorded here.
- New `windows-latest` CI job running the test suite, so this class of platform bug is
  caught rather than reasoned about. POSIX-only tests are guarded. Every other workflow
  remains `ubuntu-latest`.
- New evaluation case `evaluations/eng-level-verify-before-claiming.eval.md`.
- Fix a second Windows failure, found by that new job on its first real run. The
  vendored `ponytail` snapshot is pinned by SHA-256 in `PROVENANCE.md`, but Git's
  automatic line-ending translation rewrote it to CRLF on Windows checkouts, so the
  recorded hash could never match — `1316a2f3` expected, `46a57e26` computed. A new
  `.gitattributes` marks `skills/ponytail/**` as non-text, disabling translation and
  keeping the snapshot verbatim on every platform, which is the point of vendoring it.

## 0.14.0 — 2026-08-07

- New `execforge sessions --root <repo>` command: lists other working copies and any
  branches holding commits `HEAD` does not have, so a merge is not made blind to work in
  progress elsewhere. Wired into the merge gate, with `docs/getting-started.md` and a
  README entry. Six tests cover the clear case, branches with unmerged commits, branches
  already contained in `HEAD`, other working copies, a path that is not a git repository,
  and the merge gate requiring the check.

## 0.13.3 — 2026-08-07

- `execforge` product decision only: **Phase 5a** now defines the shape of the final
  scope ledger. Required output item 6 named it but never said what it looked like, so
  every run reinvented the layout. It is now a three-column `Decision` / `Item` / `Why`
  table, read at a glance, sitting alongside — not replacing — the eight-column Phase 5
  working table where the thinking happens.
- The `Why` column is defined per decision type, because one rule does not fit all four:
  `ADD NOW` carries the benefit line; `DEFER` carries a **checkable** reopen condition
  ("at client #3", not "when we are bigger"); `SKIP` and `KILL` carry a one-line reason.
- Evidence, decision owner, and decision date stay recorded under Phase 5 and stay out
  of the final table.
- No locked section edited; Phase 5 is untouched. No skill outside `execforge` changed.

## 0.13.2 — 2026-08-07

- `execforge`: new **New platform role baseline** section (operator instruction
  2026-08-07). Any new platform, portal, or tenant-facing system now always carries four
  roles — `superadmin`, `accountadmin`, `admin`, `user` — entered in the scope ledger as
  `ADD NOW`, with deny-by-default access, audit logging for the three admin roles, an
  evidence bar for extra roles, and a recorded reason for dropping one. Because the role
  model touches auth, `sec-level` attaches before build. The validation gate now checks
  the baseline is stated or the difference recorded. Mirrored in
  `docs/product-decision.md` and pinned by
  `tests/test_repository.py::test_new_platform_role_baseline_is_stated`. execforge 0.7.2.

## 0.13.1 — 2026-08-07

- `execforge` product decision only: new **Phase 5a — Benefit line** in
  `references/review-phases.md`. Every `ADD NOW` scope item now carries one sentence
  saying what the user achieves — an active verb, a real metric or `no baseline yet`,
  and the next step it unlocks. An item that unlocks nothing is flagged as a `DEFER`
  candidate. Wired into the orchestrator's resolution step, the required final output,
  and the validation gate.
- Scoped deliberately small. The operator's source framework was a six-letter
  features-to-benefits formula; four of its six ideas were already covered by the
  Phase 5 ledger's `User Pain` / `User Value` / `Business Value` columns and the Phase 8
  job-to-be-done section. Only the action-verb rule and "next step enabled" were new, so
  only those were added — a second six-letter framework would have cost context on every
  run and collided by name with the locked **A-C-T-I-O-N Operational Matrix**, which is
  an unrelated operational framework (assess, cost, technical tactics, incorporate
  security, operational work reduction, no manual work).
- No locked section was edited. Phase 5, Phase 8, the CEO and COO contracts, the CEO
  plan bridge, and the A-C-T-I-O-N matrix are byte-identical; Phase 5a sits beside the
  ledger rather than changing its table. No engineering, QA, security, design, or
  lifecycle skill changed.

## 0.13.0 — 2026-08-07

- New `ux-level` skill: a Senior Product Manager and Lead UX Researcher who reviews a
  described user journey and ends in a `UX PASS / FIX REQUIRED / REDESIGN` verdict.
  Two modes, chosen from the journey rather than asked for: `product` (friction,
  time-to-value, edge cases, improvements) and `technical` (four heuristic pillars —
  system visibility and data feedback, error prevention and recovery, flexibility and
  efficiency, information architecture and cognitive load). Output is a step-by-step
  journey breakdown with every claim labelled `OBSERVED` / `INFERRED` / `ASSUMED` /
  `UNKNOWN`, a `HIGH` / `MEDIUM` / `LOW` severity matrix, and three to five prioritized
  recommendations. Ships with `references/pillars.md`, an
  `assets/journey-review.template.md`, `docs/ux-level.md`, and a worked example at
  `examples/09-ux-journey-review.md`.
- `c-level` routing: new router row for journey review, and a new trigger-alias row.
  **Behaviour change** — `UX review` now routes to `ux-level` instead of `design-html`.
  `designer`, `design plan`, and `UI review` still route to `design-html`.
- `ux-level` is deliberately **not** wired into `full-cycle` as a gate yet. Deferred
  until the skill has been used on real journeys.

## 0.12.1 — 2026-08-04

- `execforge` CEO plan bridge changed from either/or to both-and (edited 2026-07-31;
  operator approval given 2026-08-04, recorded in
  `docs/decisions/2026-08-04-ceo-plan-both-and.md`):
  the internal CEO Subagent review now ALWAYS runs and is never replaced by the gstack
  integration; when gstack `plan-ceo-review` is installed it runs IN ADDITION,
  producing a second independent CEO plan artifact, with disagreements routed through
  the orchestrator's contradiction register. The fallback label and the A-C-T-I-O-N +
  OKR output requirements are unchanged. Lock pin in `tests/test_restored_sections.py`
  updated to the new verbatim text. execforge 0.7.1.

## 0.12.0 — 2026-07-31

Restored three pieces of the original monolithic `ExecForge_SKILL.md` that were lost or
over-condensed in the v0.5.0 restructure (`4123e3d`), verbatim from the pre-deletion
source (`git show 4123e3d^:ExecForge_SKILL.md`):

- `execforge` SKILL.md: the condensed CEO/COO contracts are replaced by the full
  initial-version **CEO Subagent** and **COO Subagent** sections — the complete
  "independently evaluates" lists, the challenge rules, the full advisory output
  contracts, and the "must not produce the final executive verdict" boundaries. The
  orchestrator process now records the scope ledger (`ADD NOW` / `DEFER` / `SKIP` /
  `KILL` with evidence, owner, date, reopen condition) and adds a product definition
  and OKRs step. Version 0.7.0.
- `execforge` references/review-phases.md: restored **Phase 5 — Scope Ledger** (per-item
  decision table and reopen rules) and **Phase 8 — Product Definition and OKRs**
  (product hypothesis template, job-to-be-done, Must/Should/Could scope, one qualitative
  objective, two to four key results with baseline/target/measurement/owner, and the
  "never fabricate a baseline" rule).
- `c-level`: new trigger aliases (`OKR plan`, `OKRs`, `okr framework`,
  `product hypothesis`, `scope ledger`) route to `execforge`. Version 0.9.0.

Also loaded the gstack CEO plan into the bundle and restored the initial-version
A-C-T-I-O-N framework:

- `execforge` SKILL.md: new **CEO plan** section wiring the installed gstack
  `plan-ceo-review` skill into the CEO stage, mirroring how `eng-level` uses
  `plan-eng-review` — gstack produces the CEO plan when installed, with a clearly
  labelled fallback to the internal CEO Subagent contract otherwise. Whichever path
  runs, the CEO plan must include the A-C-T-I-O-N operational matrix and the OKR plan.
  The required final output now lists the OKR plan and the A-C-T-I-O-N matrix
  explicitly.
- `execforge` references/execution-and-governance.md: the condensed A-C-T-I-O-N prose is
  replaced by the full initial-version **Phase 9 — A-C-T-I-O-N Operational Matrix**
  itemised framework, verbatim from the pre-deletion source
  (`git show 4123e3d^:ExecForge_SKILL.md`), including the initial section titles
  ("Incorporate Security, Governance, and Compliance") and the
  serverless-versus-provisioned-compute tactic dropped in the condensation.
- `c-level`: new trigger aliases (`gstack ceo plan`, `g stack ceo plan`,
  `plan-ceo-review`, `ACTION framework`, `ACTION matrix`) route to `execforge`.
- The restored sections are **locked** by operator decision (2026-07-31):
  `tests/test_restored_sections.py` fails on any drift from the verbatim text, and
  `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` forbid editing them without explicit operator
  instruction.

## 0.11.0 — 2026-07-24

Vendored the third-party **ponytail** simplicity persona into the bundle, executing the
2026-07-17 ExecForge PILOT decision (`.execforge/runs/20260717T0400042436000Z-f2f06790-ponytail-adoption/decision.md`).

- Added `skills/ponytail/`: verbatim upstream SKILL.md pinned at commit `b6c04480`
  (2026-07-10), with `PROVENANCE.md` recording the pin, adoption date, SHA-256, and the
  pilot governance rules (TDD wins, gates win, bottom tier, lite default, no
  auto-update). A new test verifies the snapshot still matches the recorded hash.
- `ponytail` joined `BUNDLED_SKILLS` and the Claude plugin manifest, so `install` ships
  it; the Codex manifest already ships the whole `skills/` directory.
- `validate` now exempts vendored skills (marked by a `PROVENANCE.md`) from the house
  "Use when" description style — vendored text stays verbatim.
- `c-level` fast path points at the in-repo vendored copy; `execforge` gained a
  fast-path pre-check so a direct trigger auto-detects low-impact implementation jobs
  and routes them to `ponytail lite` (TDD precedence and approval-before-commit intact)
  instead of running a product review.
- Added `evaluations/ponytail.eval.md` (gate case: simplicity never overrides test
  discipline, gates, or the approval-before-commit rule).
- `CLAUDE.md`/`AGENTS.md` slot ponytail at the domain-implementation tier with the
  TDD-wins precedence line; README and docs describe the vendored integration.

## 0.10.1 — 2026-07-14

- Closed backlog item #7: `init-run --name` now validates its input before writing any
  artifact. A name is rejected (nonzero exit, no directories created) if it is empty or
  whitespace-only after trimming, exceeds 512 characters, or contains a control
  character or Unicode line/paragraph separator (`U+2028`/`U+2029`) — the latter added
  during self-review after confirming it would otherwise slip past the same
  control-character check `_terminal_safe` already uses elsewhere in this file, since
  neither category is Unicode category "C". Without this, a multi-line `--name` could
  inject arbitrary Markdown lines into `shared-context.md` — a file every downstream
  lifecycle stage treats as trusted context. The 512-character bound matches the limit
  `operating_state.py` already enforces when *reading* the `initiative` field, closing a
  producer/reader mismatch the backlog had flagged.

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
