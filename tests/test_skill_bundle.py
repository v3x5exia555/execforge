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
        expected = sorted(module.BUNDLED_SKILLS)
        for rel in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
            manifest = json.loads((ROOT / rel).read_text())
            self.assertEqual(expected, sorted(manifest["skills"]))

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
