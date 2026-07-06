# ExecForge Skill Improvement Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand ExecForge so it has a stronger `q-level`, a new `design-html` skill that turns approved product scope into UX/interface output, and a dedicated data-QA planning layer without breaking the current product -> engineering -> QA lifecycle.

**Architecture:** Keep product scope decisions in `execforge`, add `design-html` as a downstream UX/interface translator for UI-facing work, and strengthen `q-level` with better artifacts plus a data-QA specialization. Implement the work in thin vertical slices so skills, docs, installer metadata, examples, and tests stay synchronized.

**Tech Stack:** Markdown skills, JSON schemas, Python 3 CLI/validation, MkDocs, `unittest`.

---

## Review Baseline

- Only `c-level`, `execforge`, `eng-level`, and `q-level` are bundled today.
- `q-level` has a strong decision contract, but its templates and examples are still thin.
- Backend/data concerns exist inside `q-level`, but there is no dedicated data-QA planning artifact set yet.
- Local validation worked with `python3`, not `python`.

## Scope

- In:
  - Improve `skills/q-level/` instructions, templates, state, examples, and tests.
  - Create `skills/design-html/` as a first-class bundled skill.
  - Add a data-QA planning specialization under the `q-level` workflow.
  - Update installer/manifest/docs/test surfaces so the bundle remains internally consistent.
- Out:
  - Shipping real Playwright/Schemathesis/k6/ZAP executors in this phase.
  - Replacing `execforge` with a design-discovery workflow.
  - Creating a separate full warehouse/ETL governance system unless the first data-QA pass proves generic `q-level` cannot hold it.

### Task 1: Lock the Bundle Shape and Fix Command Portability

**Files:**
- Modify: `scripts/execforge.py`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.codex-plugin/plugin.json`
- Modify: `README.md`
- Modify: `docs/getting-started.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/troubleshooting.md`
- Modify: `docs/index.md`

- [ ] Decide the bundle boundary for phase 1: add `design-html` as a bundled skill, keep data QA as a `q-level` specialization instead of a separate top-level skill.
- [ ] Replace the current hardcoded four-skill assumptions in `scripts/execforge.py` with one source of truth that can include the new bundle member cleanly.
- [ ] Update both plugin manifests so install surfaces match the actual bundled skill list.
- [ ] Normalize local commands in docs from `python` to `python3`, or explicitly document the alias requirement in one place and reference it everywhere else.
- [ ] Run `python3 scripts/execforge.py validate` and `python3 -m unittest discover -s tests -v` after the registry and doc-command changes.

### Task 2: Strengthen `q-level` Core Planning Artifacts

**Files:**
- Modify: `skills/q-level/SKILL.md`
- Modify: `skills/q-level/references/qa-plan-contract.md`
- Modify: `skills/q-level/references/state-and-artifacts.md`
- Modify: `skills/q-level/references/tool-routing.md`
- Modify: `skills/q-level/assets/qa-plan.template.md`
- Modify: `skills/q-level/assets/coverage-matrix.template.md`
- Modify: `skills/q-level/assets/state.template.json`
- Modify: `schemas/q-level-state.schema.json`
- Modify: `scripts/execforge.py`
- Create: `skills/q-level/assets/environment-approval.template.md`
- Create: `skills/q-level/assets/execution-evidence.template.md`
- Create: `skills/q-level/assets/defects.template.md`
- Create: `skills/q-level/assets/retest.template.md`

- [ ] Expand the `q-level` contract so the planner must record scenario IDs, roles, risk ranking, test data setup/cleanup, allowed destructive actions, evidence paths, and accepted-risk expiry.
- [ ] Make the coverage matrix more traceable by adding requirement IDs, role coverage, scenario references, result status, defect linkage, and owner/follow-up columns.
- [ ] Extend the state template and schema with the fields needed to track plan approval metadata, build/commit under test, evidence completeness, and non-blocking accepted risks.
- [ ] Add the missing artifact templates so `q-level` can produce environment approval, execution evidence, defect logs, and retest records without inventing format on the fly.
- [ ] Update `scripts/execforge.py init-run` so a new run seeds the expanded `.q-level/` artifact set.

### Task 3: Add a Data-QA Planning Extension Inside `q-level`

**Files:**
- Modify: `skills/q-level/SKILL.md`
- Create: `skills/q-level/references/data-qa-plan-contract.md`
- Create: `skills/q-level/assets/data-qa-plan.template.md`
- Create: `examples/07-data-qa-plan.md`
- Create: `docs/data-qa.md`
- Modify: `docs/q-level.md`
- Modify: `docs/examples.md`
- Modify: `mkdocs.yml`

- [ ] Add a dedicated data-QA contract covering migrations, reconciliation, lineage, idempotency, replay, ordering, timezone/precision, null mapping, rollback, audit persistence, and backfill safety.
- [ ] Define when the generic `q-level` plan is enough and when the data-QA extension must be attached.
- [ ] Add a reusable data-QA plan template that fits the existing `q-level` approval gate instead of inventing a parallel workflow.
- [ ] Add one realistic example focused on a backend/data transaction so the skill demonstrates how to validate state, not just HTTP responses.
- [ ] Publish a dedicated doc page and link it from the existing QA docs and examples index.

### Task 4: Create the `design-html` Skill

**Files:**
- Create: `skills/design-html/SKILL.md`
- Create: `skills/design-html/references/product-intent-to-ux.md`
- Create: `skills/design-html/references/interface-output-contract.md`
- Create: `skills/design-html/references/quality-bar.md`
- Create: `skills/design-html/assets/page-brief.template.md`
- Create: `skills/design-html/assets/screen-inventory.template.md`
- Create: `skills/design-html/assets/interface-checklist.template.md`
- Create: `examples/08-design-html.md`
- Create: `docs/design-html.md`

- [ ] Define `design-html` as a post-product, pre-implementation skill for UI-facing initiatives: it should read approved product scope, derive user journeys and interface states, and produce production-oriented HTML/CSS guidance.
- [ ] Keep the role boundary explicit: `execforge` decides whether the product should exist and what scope is allowed; `design-html` must not silently expand scope or invent new product goals.
- [ ] Make the output contract concrete: target user, journey, information architecture, key screens, empty/loading/error states, accessibility expectations, responsive behavior, and HTML/CSS delivery expectations.
- [ ] Add lightweight assets that let the skill produce consistent output without bloating the main `SKILL.md`.
- [ ] Add one end-to-end example showing product plan -> UX/interface decisions -> HTML/CSS-oriented deliverables.

### Task 5: Update Routing and Lifecycle Documentation

**Files:**
- Modify: `skills/c-level/SKILL.md`
- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/index.md`
- Modify: `docs/getting-started.md`
- Modify: `docs/eng-level.md`
- Modify: `docs/q-level.md`
- Modify: `docs/roadmap.md`
- Modify: `docs/examples.md`
- Modify: `mkdocs.yml`

- [ ] Insert `design-html` into the documented lifecycle for UI work so the repo clearly describes when design happens relative to product, engineering, and QA.
- [ ] Clarify that data QA is a specialization of `q-level` in phase 1, not a disconnected workflow.
- [ ] Update the roadmap to replace the now-implemented gap items and leave only the remaining future work.
- [ ] Add navigation links so new docs are reachable from the main docs site.

### Task 6: Add Repository and Behavior-Surface Tests

**Files:**
- Modify: `tests/test_repository.py`
- Create: `tests/test_skill_bundle.py`

- [ ] Add assertions that the bundled skill registry, both plugin manifests, and the installed directories all agree on the final bundle contents.
- [ ] Add assertions that `init-run` creates the expanded `.q-level/` artifacts expected by the new templates.
- [ ] Add tests that required docs/examples/assets for `design-html` and the data-QA extension exist and are wired into the repository structure.
- [ ] Keep tests structural and deterministic; do not claim real tool adapters executed if the repo only ships contracts and templates.

### Task 7: Validate, Review, and Prepare for Execution

**Files:**
- Modify: `CHANGELOG.md`
- Review: working tree for stray generated files such as `__pycache__`

- [ ] Run `python3 scripts/execforge.py validate`.
- [ ] Run `python3 -m unittest discover -s tests -v`.
- [ ] Run `python3 -m pip install -r requirements-docs.txt` and `mkdocs build --strict`.
- [ ] Review the diff to confirm docs, manifests, tests, examples, and seeded artifacts remain consistent.
- [ ] Update `CHANGELOG.md` with the new skill and QA capability additions after validation passes.

## Execution Notes

- Execute Tasks 1 and 2 first; they establish the bundle shape and the QA artifact format that later tasks depend on.
- Execute Task 3 before Task 5 so lifecycle docs can point to concrete data-QA artifacts instead of placeholders.
- Execute Task 4 before Task 6 so tests can validate real `design-html` files and manifests.
- Keep generated cache files out of commits.

## Open Questions

- Should `design-html` be callable only after an approved product decision, or also directly from a user prompt when early UI exploration is explicitly requested?
- Does phase-1 data QA need to cover only transactional systems, or should the first pass already include warehouse/ETL/backfill workflows?
- Should `design-html` become a required bundled skill immediately, or land as optional until one full end-to-end repo pass is validated?
