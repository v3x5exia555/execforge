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
        Eng Level Orchestrator
             ↓
  Plan Review → Build → Staff Review
             ↓
 Portal → API → Backend/Data QA
             ↓
      Final Engineering Decision
```

## What is included

| Skill | Purpose |
|---|---|
| `c-level` | Bootstrap/router that selects the correct workflow and integrates installed Superpowers skills |
| `execforge` | CEO + COO product pressure test and final `GO / MODIFY / PILOT / DEFER / KILL` decision |
| `eng-level` | Upstream approval, engineering plan review, implementation conformance, Staff Engineer review, and final ship decision |
| `q-level` | Risk-based portal/API/backend QA planning, execution, retest, and `QA PASS / RETURN / BLOCK` decision |

The repository also includes:

- A MkDocs wiki and GitHub Pages workflow
- Cross-harness plugin manifests
- A dependency-free Python CLI for installation, validation, run initialization, and status
- JSON schemas and reusable templates
- Static tests and GitHub Actions CI
- Example decision artifacts
- Superpowers integration guidance without vendoring or modifying Superpowers

## Quick start

### 1. Validate the repository

```bash
python scripts/execforge.py validate
python -m unittest discover -s tests -v
```

### 2. Install the skills

Project-local:

```bash
python scripts/execforge.py install --destination .claude/skills
```

User-level Claude installation:

```bash
python scripts/execforge.py install --target claude
```

User-level Codex installation:

```bash
python scripts/execforge.py install --target codex
```

### 3. Check optional Superpowers integration

```bash
python scripts/execforge.py check-superpowers
```

Install Superpowers separately using its official instructions. ExecForge references Superpowers skills when present; it does not copy or fork their content.

### 4. Start with a product decision

```text
/execforge Review this initiative:
[problem, target user, proposed change, constraints, evidence]
```

### 5. Move to engineering

After the product decision:

```text
/eng-level --mode=auto
```

The lifecycle stops at `UPSTREAM_APPROVAL_REQUIRED`. Approve the interpreted requirements with:

```text
APPROVE UPSTREAM
```

### 6. Build and review

When Superpowers is installed, the recommended implementation path is:

```text
using-git-worktrees
→ writing-plans
→ subagent-driven-development or executing-plans
→ test-driven-development
→ verification-before-completion
```

ExecForge then performs the Staff Engineer review against the real diff, runs the portal/API/backend QA gate, and requires a final delta review when QA fixes production code.

### 7. Run the QA gate

```text
/q-level --mode=auto
```

Approve the proposed test plan and target environment with:

```text
APPROVE QA PLAN
```

## Documentation

The full guide lives under [`docs/`](docs/index.md).

Build it locally:

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve
```

Enable **Settings → Pages → Source: GitHub Actions** to publish the wiki.

## Repository layout

```text
execforge/
├── skills/
│   ├── c-level/
│   ├── execforge/
│   ├── eng-level/
│   └── q-level/
├── docs/
├── examples/
├── schemas/
├── scripts/
├── tests/
├── .claude-plugin/
├── .codex-plugin/
└── .github/workflows/
```

## Decision boundaries

ExecForge answers:

> Should we build this, and what is the smallest defensible scope?

Eng Level answers:

> Does the approved engineering plan and actual implementation satisfy the approved product requirements safely enough to ship?

Q Level answers:

> Does the critical business transaction work across portal, API, and backend/data with release-quality evidence?

Superpowers answers:

> How should the coding agent execute the approved implementation with disciplined planning, isolation, TDD, review, and verification?

## Status

This package is a repository-ready platform for product governance, engineering review, disciplined implementation, and portal/API/backend QA. It uses Agent Skills directory conventions and progressive disclosure so the main skill files stay concise while detailed contracts live under `references/`.

## License

MIT. See [LICENSE](LICENSE).
