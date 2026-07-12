from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "execforge.py"
spec = importlib.util.spec_from_file_location("execforge_cli", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class RepositoryTests(unittest.TestCase):
    def test_repository_validation(self):
        self.assertEqual([], module.validate_repo(ROOT))

    def test_required_skills_are_discoverable(self):
        names = {
            module.parse_frontmatter(path / "SKILL.md")["name"]
            for path in (ROOT / "skills").iterdir()
            if path.is_dir()
        }
        self.assertEqual(module.BUNDLED_SKILLS, names)

    def test_install_copies_all_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "skills"
            module.install(destination)
            self.assertEqual(
                module.BUNDLED_SKILLS,
                {path.name for path in destination.iterdir() if path.is_dir()},
            )

    def test_no_legacy_root_skill_files(self):
        self.assertEqual([], list(ROOT.glob("*SKILL*.md")))

    def test_install_verifies_installed_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "skills"
            module.install(destination)
            for skill_name in module.BUNDLED_SKILLS:
                self.assertEqual([], module.verify_installed_skill(destination / skill_name))

    def test_verify_installed_skill_rejects_corrupted_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "skills"
            module.install(destination)
            corrupted = destination / "execforge" / "SKILL.md"
            corrupted.write_text("no frontmatter here\n", encoding="utf-8")
            self.assertNotEqual([], module.verify_installed_skill(destination / "execforge"))

    def test_doctor_reports_no_blocking_problems(self):
        self.assertEqual(0, module.doctor())

    def test_codex_manifest_uses_path_string_not_name_array(self):
        """A name array does not load as a Codex plugin; skills must be a './' path."""
        payload = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        skills = payload.get("skills")
        self.assertIsInstance(skills, str, "Codex 'skills' must be a relative path string")
        self.assertTrue(skills.startswith("./"), "Codex 'skills' path must start with './'")
        skills_dir = ROOT / skills.lstrip("./").rstrip("/")
        self.assertTrue(skills_dir.is_dir())
        discovered = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists()}
        self.assertEqual(set(), module.BUNDLED_SKILLS - discovered)

    def test_codex_manifest_rejects_claude_shaped_skills(self):
        """The validator must catch the name-array shape rather than pass it."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex-plugin").mkdir(parents=True)
            (root / ".codex-plugin" / "plugin.json").write_text(
                json.dumps(
                    {
                        "name": "execforge",
                        "version": "0.8.0",
                        "description": "x",
                        "skills": sorted(module.BUNDLED_SKILLS),
                    }
                )
            )
            errors = module._validate_codex_manifest(root)
            self.assertTrue(any("must be a plugin-root-relative path string" in e for e in errors))

    def test_claude_manifest_lists_bundled_skills(self):
        payload = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIsInstance(payload.get("skills"), list)
        self.assertEqual(module.BUNDLED_SKILLS, set(payload["skills"]))

    def test_state_schema_accepts_template_state(self):
        """The template must validate against the repo's own schema."""
        schema = json.loads((ROOT / "schemas" / "eng-level-state.schema.json").read_text())
        template = json.loads(
            (ROOT / "skills" / "eng-level" / "assets" / "state.template.json").read_text()
        )
        props = schema["properties"]
        for key, value in template.items():
            self.assertIn(key, props, f"state template key {key!r} is absent from the schema")
            if "enum" in props[key]:
                self.assertIn(value, props[key]["enum"], f"{key}={value!r} is not a schema-valid value")

    def test_schema_allows_ungated_post_hoc_verdict(self):
        schema = json.loads((ROOT / "schemas" / "eng-level-state.schema.json").read_text())
        self.assertIn(
            "SHIP WITH REQUIRED FIXES (UNGATED)",
            schema["properties"]["final_decision"]["enum"],
        )

    def test_init_run_creates_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("Example Initiative", cwd)
            state = json.loads((cwd / ".eng-level" / "state.json").read_text())
            self.assertEqual("Example Initiative", state["initiative"])
            self.assertEqual("UPSTREAM_INTAKE", state["state"])
            self.assertEqual([], state["routed_roles"])
            self.assertIsNone(state["stop_after"])
            self.assertTrue((cwd / ".eng-level" / "backlog.md").exists())
            qa_state = json.loads((cwd / ".q-level" / "state.json").read_text())
            self.assertEqual("Example Initiative", qa_state["initiative"])
            self.assertEqual("QA_INPUT_REQUIRED", qa_state["state"])
            self.assertEqual(
                {
                    "coverage-matrix.md",
                    "decision.md",
                    "defects.md",
                    "environment-approval.md",
                    "execution-evidence.md",
                    "qa-context.md",
                    "qa-plan.md",
                    "retest.md",
                    "state.json",
                },
                {path.name for path in (cwd / ".q-level").iterdir()},
            )


if __name__ == "__main__":
    unittest.main()
