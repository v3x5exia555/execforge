from pathlib import Path
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "execforge.py"
spec = importlib.util.spec_from_file_location("execforge_cli", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)

OPERATING_STATE = ROOT / "scripts" / "operating_state.py"
operating_spec = importlib.util.spec_from_file_location("operating_state", OPERATING_STATE)
operating_state = importlib.util.module_from_spec(operating_spec)
assert operating_spec.loader
operating_spec.loader.exec_module(operating_state)


class RepositoryTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str, check: bool = True):
        return subprocess.run(
            ["git", *args], cwd=repo, check=check, capture_output=True, text=True
        )

    def _initialize_repo(self, repo: Path):
        repo.mkdir()
        self._git(repo, "init", "-b", "main")
        self._git(repo, "config", "user.email", "tests@example.com")
        self._git(repo, "config", "user.name", "ExecForge Tests")
        (repo / "AGENTS.md").write_text("instructions\n", encoding="utf-8")
        (repo / "CLAUDE.md").write_text("instructions\n", encoding="utf-8")

    def test_installed_skill_diagnostics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundled = root / "bundled"
            (bundled / "alpha" / "references").mkdir(parents=True)
            (bundled / "alpha" / "SKILL.md").write_text("alpha\n", encoding="utf-8")
            (bundled / "alpha" / "references" / "contract.md").write_text(
                "contract\n", encoding="utf-8"
            )
            (bundled / "beta").mkdir()
            (bundled / "beta" / "SKILL.md").write_text("beta\n", encoding="utf-8")

            exact = root / "exact"
            missing = root / "missing"
            drifted = root / "drifted"
            shutil.copytree(bundled, exact)
            shutil.copytree(bundled, missing)
            shutil.copytree(bundled, drifted)
            shutil.rmtree(missing / "beta")
            (drifted / "alpha" / "references" / "contract.md").write_text(
                "changed\n", encoding="utf-8"
            )

            findings = operating_state.installed_skill_diagnostics(
                bundled, (exact, missing, drifted)
            )

            self.assertIsInstance(findings, tuple)
            self.assertEqual(
                {
                    ("error", "installed_skill_missing", str(missing), "beta"),
                    ("error", "installed_skill_drift", str(drifted), "alpha"),
                },
                {
                    (finding.severity, finding.code, finding.project, finding.detail)
                    for finding in findings
                },
            )
            with self.assertRaises(AttributeError):
                findings[0].severity = "warning"

    def test_portfolio_diagnostics(self):
        def git(repo: Path, *args: str, check: bool = True):
            return subprocess.run(
                ["git", *args], cwd=repo, check=check, capture_output=True, text=True
            )

        def initialize(repo: Path):
            repo.mkdir()
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.email", "tests@example.com")
            git(repo, "config", "user.name", "ExecForge Tests")

        with tempfile.TemporaryDirectory() as tmp:
            portfolio = Path(tmp)

            conflicted = portfolio / "conflicted"
            initialize(conflicted)
            (conflicted / "AGENTS.md").write_text("instructions\n", encoding="utf-8")
            (conflicted / "CLAUDE.md").write_text("instructions\n", encoding="utf-8")
            (conflicted / "shared.txt").write_text("base\n", encoding="utf-8")
            git(conflicted, "add", ".")
            git(conflicted, "commit", "-m", "base")
            git(conflicted, "checkout", "-b", "other")
            (conflicted / "shared.txt").write_text("other\n", encoding="utf-8")
            git(conflicted, "commit", "-am", "other")
            git(conflicted, "checkout", "main")
            (conflicted / "shared.txt").write_text("main\n", encoding="utf-8")
            git(conflicted, "commit", "-am", "main")
            git(conflicted, "merge", "other", check=False)
            selected = conflicted / ".eng-level" / "runs" / "current-run"
            selected.mkdir(parents=True)
            (selected / "state.json").write_text(
                json.dumps({"initiative": "Conflict", "state": "REVIEW_READY", "branch": "other"})
            )
            (conflicted / ".eng-level" / "current.json").write_text(
                json.dumps({"run_id": "current-run"})
            )

            malformed = portfolio / "malformed"
            initialize(malformed)
            (malformed / ".eng-level").mkdir()
            (malformed / ".eng-level" / "state.json").write_text("{not json\n", encoding="utf-8")

            unsafe_pointer = portfolio / "unsafe-pointer"
            initialize(unsafe_pointer)
            (unsafe_pointer / "AGENTS.md").write_text("instructions\n", encoding="utf-8")
            (unsafe_pointer / "CLAUDE.md").write_text("instructions\n", encoding="utf-8")
            (unsafe_pointer / ".eng-level").mkdir()
            (unsafe_pointer / ".eng-level" / "current.json").write_text(
                json.dumps({"state_path": "../../outside.json"})
            )
            (unsafe_pointer / ".eng-level" / "state.json").write_text(
                json.dumps({"initiative": "Legacy", "state": "PLAN_REQUIRED", "branch": "other"})
            )
            (portfolio / "outside.json").write_text(
                json.dumps({"initiative": "Secret", "state": "SHIP_READY", "branch": "main"})
            )

            ignored_nested = malformed / "nested"
            initialize(ignored_nested)

            findings = operating_state.portfolio_diagnostics(portfolio)
            observed = {(finding.project, finding.code) for finding in findings}

            self.assertIn(("conflicted", "git_conflict"), observed)
            self.assertIn(("conflicted", "branch_mismatch"), observed)
            self.assertIn(("malformed", "root_agents_missing"), observed)
            self.assertIn(("malformed", "root_claude_missing"), observed)
            self.assertIn(("malformed", "lifecycle_state_malformed"), observed)
            self.assertIn(("unsafe-pointer", "lifecycle_pointer_malformed"), observed)
            self.assertIn(("unsafe-pointer", "branch_mismatch"), observed)
            self.assertNotIn(("nested", "root_agents_missing"), observed)
            for finding in findings:
                self.assertNotIn("instructions", finding.detail)
                self.assertNotIn("{not json", finding.detail)
                self.assertNotIn("Secret", finding.detail)

            cli = subprocess.run(
                [sys.executable, str(SCRIPT), "doctor", "--portfolio", str(portfolio)],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, cli.returncode)
            self.assertIn("git_conflict", cli.stdout)
            self.assertNotIn("Traceback", cli.stdout + cli.stderr)

            installed_cli = subprocess.run(
                [sys.executable, str(SCRIPT), "doctor", "--installed"],
                cwd=ROOT,
                env={**os.environ, "HOME": str(portfolio / "empty-home")},
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, installed_cli.returncode)
            self.assertIn("installed_skill_missing", installed_cli.stdout)
            self.assertNotIn("Traceback", installed_cli.stdout + installed_cli.stderr)

    def test_portfolio_branch_compatibility_and_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            portfolio = Path(tmp)

            legacy = portfolio / "legacy"
            self._initialize_repo(legacy)
            (legacy / ".eng-level").mkdir()
            (legacy / ".eng-level" / "state.json").write_text(
                json.dumps(
                    {
                        "initiative": "Legacy",
                        "state": "REVIEW_READY",
                        "base_branch": "other",
                    }
                )
            )

            precedence = portfolio / "precedence"
            self._initialize_repo(precedence)
            (precedence / ".eng-level").mkdir()
            (precedence / ".eng-level" / "state.json").write_text(
                json.dumps(
                    {
                        "initiative": "Current",
                        "state": "REVIEW_READY",
                        "branch": "main",
                        "base_branch": "other",
                    }
                )
            )

            findings = operating_state.portfolio_diagnostics(portfolio)
            mismatch_projects = {
                finding.project for finding in findings if finding.code == "branch_mismatch"
            }
            self.assertIn("legacy", mismatch_projects)
            self.assertNotIn("precedence", mismatch_projects)

    def test_portfolio_git_status_disables_configured_fsmonitor(self):
        with tempfile.TemporaryDirectory() as tmp:
            portfolio = Path(tmp)
            repo = portfolio / "repo"
            self._initialize_repo(repo)
            marker = portfolio / "fsmonitor-ran"
            hook = portfolio / "fsmonitor-hook"
            hook.write_text(
                f"#!/bin/sh\ntouch {shlex.quote(str(marker))}\n",
                encoding="utf-8",
            )
            hook.chmod(0o755)
            self._git(repo, "config", "core.fsmonitor", str(hook))

            operating_state.portfolio_diagnostics(portfolio)

            self.assertFalse(marker.exists(), "portfolio diagnostics executed core.fsmonitor")

    def test_git_output_with_invalid_utf8_is_replaced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_git = root / "git"
            fake_git.write_text("#!/bin/sh\nprintf '\\377'\n", encoding="utf-8")
            fake_git.chmod(0o755)
            with mock.patch.dict(os.environ, {"PATH": str(root)}):
                output, finding = operating_state._run_git(root, "version")

            self.assertIsNone(finding)
            self.assertEqual("\ufffd", output)

    def test_installed_skill_fifo_is_hashed_without_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundled = root / "bundled"
            installed = root / "installed"
            (bundled / "alpha").mkdir(parents=True)
            (bundled / "alpha" / "SKILL.md").write_text("alpha\n", encoding="utf-8")
            shutil.copytree(bundled, installed)
            os.mkfifo(installed / "alpha" / "special")
            code = (
                "import sys; "
                f"sys.path.insert(0, {str(OPERATING_STATE.parent)!r}); "
                "import operating_state; "
                "print([finding.code for finding in "
                "operating_state.installed_skill_diagnostics("
                "sys.argv[1], (sys.argv[2],))])"
            )

            result = subprocess.run(
                [sys.executable, "-c", code, str(bundled), str(installed)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=2,
                check=True,
            )

            self.assertEqual("['installed_skill_drift']", result.stdout.strip())

    def test_malformed_selected_state_does_not_fall_back_to_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            portfolio = Path(tmp)
            repo = portfolio / "repo"
            self._initialize_repo(repo)
            selected = repo / ".eng-level" / "runs" / "selected"
            selected.mkdir(parents=True)
            (selected / "state.json").write_text("{not json\n", encoding="utf-8")
            (repo / ".eng-level" / "current.json").write_text(
                json.dumps({"run_id": "selected"})
            )
            (repo / ".eng-level" / "state.json").write_text(
                json.dumps(
                    {
                        "initiative": "Legacy",
                        "state": "REVIEW_READY",
                        "branch": "other",
                    }
                )
            )

            findings = operating_state.portfolio_diagnostics(portfolio)
            codes = {finding.code for finding in findings}
            self.assertIn("lifecycle_state_malformed", codes)
            self.assertNotIn("branch_mismatch", codes)

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

    def test_status_surfaces_stop_boundary_and_backlog(self):
        """SKILL.md claims --mode=status reports the brake and the parked work.
        If status does not print them, that claim is false."""
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("Braked Initiative", cwd)

            state_file = cwd / ".eng-level" / "state.json"
            state = json.loads(state_file.read_text())
            state["stop_after"] = "plan"
            state["routed_roles"] = ["architect", "backend-engineer"]
            state["adversarial_pair"] = True
            state_file.write_text(json.dumps(state, indent=2))

            backlog = cwd / ".eng-level" / "backlog.md"
            backlog.write_text(
                "# Deferred Backlog\n\n"
                "| # | Action | Cycle | Provenance | Why deferred | What unblocks it |\n"
                "|---|---|---|---|---|---|\n"
                "| 1 | Rebuild table | `Next` | `[R]` | risky | validated ER layer |\n"
            )

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                module.show_status(cwd)
            out = buf.getvalue()

            self.assertIn("stop_after: plan", out)
            self.assertIn("architect", out)
            self.assertIn("backend-engineer", out)
            self.assertIn("adversarial_pair: True", out)
            self.assertIn("Rebuild table", out)
            self.assertIn("validated ER layer", out)

    def test_status_reports_empty_backlog_without_crashing(self):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("Fresh Initiative", cwd)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                module.show_status(cwd)
            out = buf.getvalue()
            self.assertIn("backlog: (empty)", out)
            self.assertIn("stop_after: None", out)

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
