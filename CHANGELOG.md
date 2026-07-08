# Changelog

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
