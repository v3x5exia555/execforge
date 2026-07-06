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

    def test_init_run_creates_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("Example Initiative", cwd)
            state = json.loads((cwd / ".eng-level" / "state.json").read_text())
            self.assertEqual("Example Initiative", state["initiative"])
            self.assertEqual("UPSTREAM_INTAKE", state["state"])
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
