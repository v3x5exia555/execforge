# ExecForge

ExecForge is an agent-skill platform for governing a software initiative from **product decision** through **engineering and cross-layer QA** to a final ship decision.

```text
CEO Subagent
    \
     ExecForge Orchestrator → Product Decision
    /
COO Subagent
             ↓
      User Approval Gate
             ↓
   Optional UI/UX Design Bridge
             ↓
        Eng Level Orchestrator
             ↓
  Plan Review → Build → Staff Review
             ↓
 Portal → API → Backend/Data QA
             ↓
      Final Engineering Decision
```

## Bundled skills

| Skill | Purpose |
|---|---|
| `c-level` | Bootstrap/router that selects the correct workflow and integrates installed Superpowers skills |
| `execforge` | CEO + COO product pressure test and final `GO / MODIFY / PILOT / DEFER / KILL` decision |
| `design-html` | Translates approved product scope into UX/interface structure and production-oriented HTML/CSS guidance for UI-facing work |
| `eng-level` | Upstream approval, engineering plan review, implementation conformance, Staff Engineer review, and final ship decision |
| `q-level` | Risk-based portal/API/backend QA planning, execution, retest, data-QA attachment, and `QA PASS / RETURN / BLOCK` decision |

Each skill follows the Agent Skills directory convention: a concise `SKILL.md` entry point, detailed contracts under `references/`, and reusable templates under `assets/`.

The repository also includes:

- A dependency-free Python CLI for validation, environment checks, installation, run initialization, and status
- JSON schemas for decision and lifecycle state artifacts
- Behavioral evaluation cases for every bundled skill
- Static tests and GitHub Actions CI
- A MkDocs wiki with a GitHub Pages deployment workflow
- Cross-harness plugin manifests (Claude and Codex)
- Example decision artifacts for every lifecycle stage
- Superpowers integration guidance without vendoring or modifying Superpowers

## Requirements

- **Python ≥ 3.9** — the CLI has no third-party dependencies.
- **Git** — needed by `eng-level` for diff review (optional for the CLI itself).
- **MkDocs** (optional) — only to build the documentation site: `python3 -m pip install -r requirements-docs.txt`.

Check your environment at any time:

```bash
python3 scripts/execforge.py doctor
```

## Quick start

### 1. Validate and check the environment

```bash
python3 scripts/execforge.py validate
python3 scripts/execforge.py doctor
python3 -m unittest discover -s tests -v
```

### 2. Install the skills

Installation validates the bundle first and verifies every installed skill afterwards.

```bash
# Project-local
python3 scripts/execforge.py install --destination .claude/skills

# User-level Claude installation
python3 scripts/execforge.py install --target claude

# User-level Codex installation
python3 scripts/execforge.py install --target codex
```

Add `--force` to overwrite an existing installation.

### 3. Check optional Superpowers integration

```bash
python3 scripts/execforge.py check-superpowers
```

Install Superpowers separately using its official instructions. ExecForge references Superpowers skills when present; it does not copy or fork their content.

### 4. Start with a product decision

```text
/execforge Review this initiative:
[problem, target user, proposed change, constraints, evidence]
```

### 5. Optional UI/UX design bridge

For UI-facing initiatives with approved scope:

```text
/design-html
```

### 6. Move to engineering

```text
/eng-level --mode=auto
```

The lifecycle stops at `UPSTREAM_APPROVAL_REQUIRED`. Approve the interpreted requirements with `APPROVE UPSTREAM`.

### 7. Build and review

When Superpowers is installed, the recommended implementation path is:

```text
using-git-worktrees
→ writing-plans
→ subagent-driven-development or executing-plans
→ test-driven-development
→ verification-before-completion
```

ExecForge then performs the Staff Engineer review against the real diff, runs the portal/API/backend QA gate, and requires a final delta review when QA fixes production code.

### 8. Run the QA gate

```text
/q-level --mode=auto
```

Approve the proposed test plan and target environment with `APPROVE QA PLAN`.

## CLI reference

All commands run through `scripts/execforge.py` (or `scripts/install.sh` as a thin wrapper around `install`).

| Command | Purpose |
|---|---|
| `validate` | Check repository structure, skill frontmatter, link integrity, manifests, and schemas |
| `doctor` | Check Python version, repository integrity, Git/MkDocs availability, install-target writability, and Superpowers presence |
| `install --target claude\|codex\|agents` or `--destination <dir>` | Validate, copy, and verify the skill bundle (`--force` to overwrite) |
| `check-superpowers` | Detect a separately installed Superpowers setup |
| `init-run --name <initiative>` | Seed `.execforge/`, `.eng-level/`, and `.q-level/` run artifacts |
| `status` | Report current engineering and QA lifecycle state |

## Evaluations

`evaluations/` contains one behavioral evaluation case per bundled skill: an input scenario, an expected-behavior checklist, and explicit failure conditions. A case passes only when every expected behavior is observed and no failure condition occurs. The shared invariant across all cases: **never claim a review, test, approval, or lifecycle stage ran without evidence that it actually ran.** See [`evaluations/README.md`](evaluations/README.md).

## Continuous integration

GitHub Actions runs on every push and pull request ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)):

1. `python3 scripts/execforge.py validate`
2. `python3 scripts/execforge.py doctor`
3. `python3 -m unittest discover -s tests -v`
4. `mkdocs build --strict`

A second workflow ([`.github/workflows/docs.yml`](.github/workflows/docs.yml)) deploys the MkDocs site to GitHub Pages on pushes to `main`. Enable **Settings → Pages → Source: GitHub Actions** to publish it.

## Documentation

The full guide lives under [`docs/`](docs/index.md). Build it locally:

```bash
python3 -m pip install -r requirements-docs.txt
mkdocs serve
```

## Repository layout

```text
execforge/
├── skills/              # Bundled skills (SKILL.md + references/ + assets/)
│   ├── c-level/
│   ├── design-html/
│   ├── execforge/
│   ├── eng-level/
│   └── q-level/
├── evaluations/         # Behavioral evaluation cases, one per skill
├── docs/                # MkDocs wiki source
├── examples/            # Example decision artifacts
├── schemas/             # JSON schemas for decision/state artifacts
├── scripts/             # Dependency-free CLI and install wrapper
├── tests/               # Static repository and bundle tests
├── .claude-plugin/      # Claude plugin manifest
├── .codex-plugin/       # Codex plugin manifest
└── .github/workflows/   # CI and docs deployment
```

## Decision boundaries

ExecForge answers:

> Should we build this, and what is the smallest defensible scope?

Design HTML answers:

> Given approved scope, what is the smallest clear interface that delivers the user outcome and can be implemented faithfully?

Eng Level answers:

> Does the approved engineering plan and actual implementation satisfy the approved product requirements safely enough to ship?

Q Level answers:

> Does the critical business transaction work across portal, API, and backend/data with release-quality evidence, including persisted-state risk where data QA is required?

Superpowers answers:

> How should the coding agent execute the approved implementation with disciplined planning, isolation, TDD, review, and verification?

## Versioning and releases

Releases follow semantic-style `MAJOR.MINOR.PATCH` versions, tagged as `v<version>` in Git, with plugin manifests and skill frontmatter kept in sync. Changes are recorded in [CHANGELOG.md](CHANGELOG.md).

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow and [SECURITY.md](SECURITY.md) for reporting security issues.

## License

MIT. See [LICENSE](LICENSE).
