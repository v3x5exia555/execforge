from pathlib import Path
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "execforge.py"
spec = importlib.util.spec_from_file_location("execforge_cli", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class SkillBundleTests(unittest.TestCase):
    def test_plugin_manifests_match_bundled_skills(self):
        """Each host has its own manifest contract; validating both against one
        shape is what previously hid the Codex manifest being unloadable."""
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(sorted(module.BUNDLED_SKILLS), sorted(claude["skills"]))

        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertIsInstance(codex["skills"], str)
        skills_dir = ROOT / codex["skills"].lstrip("./").rstrip("/")
        discovered = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists()}
        self.assertEqual(set(), module.BUNDLED_SKILLS - discovered)

    def test_every_bundled_skill_has_an_evaluation_case(self):
        evaluations = ROOT / "evaluations"
        self.assertTrue((evaluations / "README.md").exists())
        for skill_name in module.BUNDLED_SKILLS:
            eval_file = evaluations / f"{skill_name}.eval.md"
            self.assertTrue(eval_file.exists(), f"Missing evaluation case: {eval_file}")
            meta = module.parse_frontmatter(eval_file)
            self.assertEqual(skill_name, meta.get("skill"))
            self.assertTrue(meta.get("id", "").startswith(skill_name))
            self.assertIn(meta.get("type"), {"routing", "decision", "gate", "output-contract"})
            body = eval_file.read_text(encoding="utf-8")
            for section in ["## Scenario", "## Expected behavior", "## Failure conditions"]:
                self.assertIn(section, body, f"{eval_file} missing section {section}")

    def test_ci_workflows_exist(self):
        for rel in [".github/workflows/ci.yml", ".github/workflows/docs.yml"]:
            self.assertTrue((ROOT / rel).exists(), f"Missing workflow: {rel}")

    def test_progressive_references_are_linked_from_skill_files(self):
        expected = {
            "execforge": [
                "references/review-phases.md",
                "references/execution-and-governance.md",
                "references/initiative-flags.md",
            ],
            "eng-level": ["references/lifecycle-protocol.md", "references/fallback-review-contracts.md"],
            "full-cycle": ["references/fallback-implementation-contract.md"],
        }
        for skill_name, references in expected.items():
            skill_file = ROOT / "skills" / skill_name / "SKILL.md"
            links = module.markdown_links(skill_file)
            for reference in references:
                self.assertTrue((skill_file.parent / reference).exists(), f"Missing {reference}")
                self.assertIn(reference, links, f"{skill_file} does not link {reference}")

    def test_initiative_flags_reference_defines_the_gate_contract(self):
        catalog = (ROOT / "skills" / "execforge" / "references" / "initiative-flags.md").read_text(encoding="utf-8")
        for flag in [
            "offensive-security",
            "legally-gated",
            "regulated-impersonation",
            "user-prescribed-mechanism",
        ]:
            self.assertIn(flag, catalog, f"initiative-flags.md missing flag {flag}")
        for verdict in ["AUTHORIZED", "NOT AUTHORIZED", "N-A (justified"]:
            self.assertIn(verdict, catalog, f"initiative-flags.md missing decision value {verdict}")

    def test_authorization_gate_is_wired_into_lifecycle_skills(self):
        checks = {
            "full-cycle": "Authorization / Rules-of-Engagement gate",
            "eng-level": "Initiative flags and authorization status",
            "sec-level": "authorization gate",
        }
        for skill_name, needle in checks.items():
            body = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(needle, body, f"{skill_name}/SKILL.md missing '{needle}'")

    def test_design_html_and_data_qa_assets_exist(self):
        required_paths = [
            ROOT / "skills" / "design-html" / "SKILL.md",
            ROOT / "skills" / "design-html" / "references" / "product-intent-to-ux.md",
            ROOT / "skills" / "design-html" / "references" / "interface-output-contract.md",
            ROOT / "skills" / "design-html" / "references" / "quality-bar.md",
            ROOT / "skills" / "design-html" / "assets" / "page-brief.template.md",
            ROOT / "skills" / "design-html" / "assets" / "screen-inventory.template.md",
            ROOT / "skills" / "design-html" / "assets" / "interface-checklist.template.md",
            ROOT / "skills" / "q-level" / "references" / "data-qa-plan-contract.md",
            ROOT / "skills" / "q-level" / "assets" / "data-qa-plan.template.md",
            ROOT / "docs" / "design-html.md",
            ROOT / "docs" / "data-qa.md",
            ROOT / "examples" / "07-data-qa-plan.md",
            ROOT / "examples" / "08-design-html.md",
        ]
        for path in required_paths:
            self.assertTrue(path.exists(), f"Missing expected path: {path}")


if __name__ == "__main__":
    unittest.main()
