# Changelog

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
