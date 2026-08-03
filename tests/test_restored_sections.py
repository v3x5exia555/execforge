"""Lock for the restored initial-version sections (operator decision 2026-07-31).

The CEO Subagent, COO Subagent, Phase 5 Scope Ledger, and Phase 8 Product
Definition and OKRs sections were restored verbatim from the pre-deletion
monolith (`git show 4123e3d^:ExecForge_SKILL.md`) after the v0.5.0 restructure
dropped them. The operator locked them: they must not be edited, condensed, or
removed without explicit operator instruction. These tests fail on any drift.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

CEO_EVALUATES = """The CEO Subagent independently evaluates:

- Whether the user actually needs the initiative
- Product-market fit
- User pain
- Product hypothesis
- 10-star user experience
- 10× product opportunity
- Scope mode
- Platonic Ideal
- MVP scope
- Adoption
- Strategic moat
- Business impact
- Add / Defer / Skip recommendations

The CEO must challenge technically interesting work that lacks user value."""

CEO_CONTRACT = """The CEO returns only an advisory review containing:

- Gatekeeper recommendation
- Evidence-labelled product claims
- Scope-mode recommendation
- 10× opportunity
- Platonic Ideal
- Proposed Add / Defer / Skip items
- Adoption and moat assessment
- Product risks
- Confidence level
- Questions or facts requiring verification

The CEO must not produce the final executive verdict."""

COO_EVALUATES = """The COO Subagent independently evaluates:

- Total cost of ownership
- Scalability
- Reliability
- Compliance
- Security
- Privacy
- Architecture
- Operational readiness
- Support burden
- Automation
- Failure recovery
- Data lineage
- Auditability
- Ownership
- Technical debt
- Sunset criteria

The COO must challenge valuable ideas that cannot operate safely, economically,
or predictably."""

COO_CONTRACT = """The COO returns only an advisory review containing:

- Cost and unit-economics assessment
- Evidence-labelled operational claims
- Scalability and reliability risks
- Compliance, security, and privacy controls
- Automation and recovery requirements
- Non-negotiable production gates
- Kill and sunset criteria
- Confidence level
- Questions or facts requiring verification

The COO must not produce the final executive verdict."""

SCOPE_LEDGER = """## Phase 5 — Scope Ledger

Evaluate each proposed capability independently.

| Scope Item | User Pain | User Value | Business Value | Effort | Risk | Decision | Reason |
|---|---|---:|---:|---:|---:|---|---|

Allowed decisions:

- **ADD NOW**
- **DEFER**
- **SKIP**
- **KILL**

For each item, record:

- Evidence
- Decision owner
- Decision date
- Reopen condition

Previously settled decisions must not be reopened without new evidence."""

OKR_HYPOTHESIS = """> We believe that **[target user]** experiences **[specific problem]**.
> By providing **[capability]**, we expect **[measurable outcome]**."""

CEO_PLAN_BRIDGE = """The internal CEO Subagent review above ALWAYS runs. It is never replaced, skipped, or
shortened by any external integration.

When the installed gstack `plan-ceo-review` skill is available, run it IN ADDITION to
the internal review to produce a second, independent CEO plan artifact. Present both
findings; route any disagreement between them through the orchestrator's contradiction
register like any other strategic disagreement. When gstack is unavailable, state that
only the internal CEO Subagent contract ran and label the output:"""

CEO_PLAN_FALLBACK_LABEL = "Fallback CEO plan used; upstream gstack /plan-ceo-review was unavailable."

ACTION_ROOT_CAUSE_TEMPLATE = """> The problem occurs because **[root cause]**, causing **[measurable impact]**
> for **[user or business area]**."""

ACTION_NO_MANUAL_WORK = """### N — No Manual Work by Default

Include:

- Idempotency
- Retry with exponential backoff
- Dead-letter queue or quarantine
- Duplicate prevention
- Checkpointing
- Automatic reconciliation
- Automatic rollback
- Self-healing
- Reprocessing
- Poison-message handling
- Data-correction strategy
- Maximum retry threshold
- Human approval conditions

Human intervention is reserved for:

- Policy decisions
- Security incidents
- Irrecoverable corruption
- Repeated systemic failure
- Material financial exceptions
- Regulatory-impact exceptions"""

OKR_KEY_RESULTS = """Provide two to four measurable results.

Each result must include:

- Baseline
- Target
- Measurement method
- Measurement period
- Owner

Never fabricate a baseline."""


class RestoredSectionLockTests(unittest.TestCase):
    def assert_locked(self, path: Path, block: str, label: str):
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            block,
            text,
            f"LOCKED section drifted or was removed: {label} in {path}. "
            "Restore it verbatim; edits require explicit operator instruction.",
        )

    def test_ceo_and_coo_plans_are_locked_in_execforge_skill(self):
        skill = ROOT / "skills" / "execforge" / "SKILL.md"
        self.assert_locked(skill, CEO_EVALUATES, "CEO Subagent evaluation list")
        self.assert_locked(skill, CEO_CONTRACT, "CEO output contract")
        self.assert_locked(skill, COO_EVALUATES, "COO Subagent evaluation list")
        self.assert_locked(skill, COO_CONTRACT, "COO output contract")

    def test_scope_ledger_and_okr_framework_are_locked_in_review_phases(self):
        phases = ROOT / "skills" / "execforge" / "references" / "review-phases.md"
        self.assert_locked(phases, SCOPE_LEDGER, "Phase 5 — Scope Ledger")
        self.assert_locked(phases, "## Phase 8 — Product Definition and OKRs", "Phase 8 heading")
        self.assert_locked(phases, OKR_HYPOTHESIS, "Product hypothesis template")
        self.assert_locked(phases, OKR_KEY_RESULTS, "Key results requirements")

    def test_ceo_plan_gstack_bridge_is_locked_in_execforge_skill(self):
        skill = ROOT / "skills" / "execforge" / "SKILL.md"
        self.assert_locked(skill, "### CEO plan", "CEO plan heading")
        self.assert_locked(skill, CEO_PLAN_BRIDGE, "CEO plan gstack bridge")
        self.assert_locked(skill, CEO_PLAN_FALLBACK_LABEL, "CEO plan fallback label")

    def test_action_matrix_is_locked_in_execution_and_governance(self):
        governance = ROOT / "skills" / "execforge" / "references" / "execution-and-governance.md"
        self.assert_locked(governance, "## A-C-T-I-O-N Operational Matrix", "A-C-T-I-O-N heading")
        self.assert_locked(governance, ACTION_ROOT_CAUSE_TEMPLATE, "Root-cause template")
        self.assert_locked(governance, ACTION_NO_MANUAL_WORK, "N — No Manual Work by Default")

    def test_okr_aliases_are_locked_in_c_level_router(self):
        c_level = ROOT / "skills" / "c-level" / "SKILL.md"
        self.assert_locked(
            c_level,
            "`OKR plan`, `OKRs`, `okr framework`, `product hypothesis`, `scope ledger`",
            "OKR trigger aliases",
        )


if __name__ == "__main__":
    unittest.main()
