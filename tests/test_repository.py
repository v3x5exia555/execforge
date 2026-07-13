from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import contextlib
import importlib.util
import io
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
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

    def _initialize_operating_repo(self, repo: Path, initiative: str = "Resume Initiative"):
        self._initialize_repo(repo)
        (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
        self._git(repo, "add", ".")
        self._git(repo, "commit", "-m", "base")
        module.init_run(initiative, repo)
        pointer = json.loads((repo / ".eng-level" / "current.json").read_text())
        state_file = repo / pointer["state_path"]
        return state_file, json.loads(state_file.read_text())

    def _run_operating_command(self, command: str, repo: Path):
        output = io.StringIO()
        function = module.resume_run if command == "resume" else module.show_next
        with contextlib.redirect_stdout(output):
            returncode = function(repo)
        return returncode, output.getvalue()

    def _write_state(self, state_file: Path, payload: dict, **updates):
        payload.update(updates)
        state_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

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

            pointer = json.loads((cwd / ".eng-level" / "current.json").read_text())
            state_file = cwd / pointer["state_path"]
            state = json.loads(state_file.read_text())
            state["stop_after"] = "plan"
            state["routed_roles"] = ["architect", "backend-engineer"]
            state["adversarial_pair"] = True
            state_file.write_text(json.dumps(state, indent=2))

            backlog = state_file.parent / "backlog.md"
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

    def test_resume_reports_fresh_selected_run_without_inference(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            state_file, state = self._initialize_operating_repo(repo, "Fresh Run")
            returncode, output = self._run_operating_command("resume", repo)

            self.assertEqual(0, returncode)
            self.assertIn("initiative: Fresh Run", output)
            self.assertIn(f"run_id: {state['run_id']}", output)
            self.assertIn("git_branch: main", output)
            self.assertIn(f"git_head: {state['commit']}", output)
            self.assertIn("lifecycle_state: UPSTREAM_INTAKE", output)
            self.assertIn("stop_after: none", output)
            self.assertIn("blockers: 0", output)
            self.assertIn(f"artifact_root: {state['artifact_root']}", output)
            self.assertIn(f"evidence_root: {state_file.parent}", output)
            self.assertIn(f"backlog_location: {state_file.parent / 'backlog.md'}", output)
            self.assertIn("backlog_summary: 0 deferred action(s)", output)
            self.assertIn("recorded_next_action: Complete upstream intake and secure approval.", output)
            self.assertIn("warning: dirty_worktree", output)

    def test_next_pending_approval_and_open_blocker_are_safety_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            approval_repo = root / "approval"
            state_file, state = self._initialize_operating_repo(approval_repo)
            self._write_state(
                state_file, state, state="UPSTREAM_APPROVAL_REQUIRED",
                upstream_approval_status="PENDING",
            )
            returncode, output = self._run_operating_command("next", approval_repo)
            self.assertEqual(0, returncode)
            self.assertEqual(1, len([line for line in output.splitlines() if line.startswith("next_action:")]))
            self.assertIn("next_action: request upstream approval", output)

            blocker_repo = root / "blocker"
            state_file, state = self._initialize_operating_repo(blocker_repo)
            self._write_state(
                state_file, state, state="BLOCKED",
                upstream_approval_status="APPROVED", open_blockers=["credential=do-not-print"],
            )
            returncode, output = self._run_operating_command("next", blocker_repo)
            self.assertEqual(1, returncode)
            self.assertIn("next_action: resolve open blockers", output)
            self.assertNotIn("do-not-print", output)
            self.assertEqual(1, len([line for line in output.splitlines() if line.startswith("next_action:")]))

    def test_next_real_merge_conflict_has_highest_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            state_file, state = self._initialize_operating_repo(repo)
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "operating state")
            self._git(repo, "checkout", "-b", "other")
            (repo / "tracked.txt").write_text("other\n", encoding="utf-8")
            self._git(repo, "commit", "-am", "other")
            self._git(repo, "checkout", "main")
            (repo / "tracked.txt").write_text("main\n", encoding="utf-8")
            self._git(repo, "commit", "-am", "main")
            self._git(repo, "merge", "other", check=False)
            self._write_state(
                state_file, state, state="BLOCKED", branch="stale",
                commit="stale", open_blockers=["secret blocker"],
            )

            returncode, output = self._run_operating_command("next", repo)
            self.assertEqual(1, returncode)
            self.assertIn("next_action: resolve Git conflicts", output)
            self.assertNotIn("secret blocker", output)
            self.assertEqual(1, len([line for line in output.splitlines() if line.startswith("next_action:")]))

    def test_next_honors_each_stop_boundary_only_after_it_is_reached(self):
        cases = {
            "product": ("UPSTREAM_APPROVAL_REQUIRED", "PLAN_REQUIRED", "request upstream approval"),
            "plan": ("PLAN_REQUIRED", "WAITING_FOR_IMPLEMENTATION", "create or revise engineering plan"),
            "implement": ("IMPLEMENTATION_IN_PROGRESS", "REVIEW_READY", "complete or fix implementation"),
            "review": ("REVIEW_READY", "REVIEW_PASSED", "run Staff Engineer review"),
            "qa": ("REVIEW_PASSED", "SHIP_READY", "run q-level --mode=auto"),
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for boundary, (before, reached, before_action) in cases.items():
                with self.subTest(boundary=boundary, phase="not-reached"):
                    repo = root / f"{boundary}-before"
                    state_file, state = self._initialize_operating_repo(repo)
                    self._write_state(
                        state_file, state, state=before, stop_after=boundary,
                        upstream_approval_status=("PENDING" if before == "UPSTREAM_APPROVAL_REQUIRED" else "APPROVED"),
                    )
                    returncode, output = self._run_operating_command("next", repo)
                    self.assertEqual(0, returncode)
                    self.assertIn(f"next_action: {before_action}", output)
                with self.subTest(boundary=boundary, phase="reached"):
                    repo = root / f"{boundary}-reached"
                    state_file, state = self._initialize_operating_repo(repo)
                    self._write_state(
                        state_file, state, state=reached, stop_after=boundary,
                        upstream_approval_status="APPROVED",
                    )
                    returncode, output = self._run_operating_command("next", repo)
                    self.assertEqual(0, returncode)
                    self.assertIn("next_action: await explicit user instruction", output)
                    self.assertEqual(1, len([line for line in output.splitlines() if line.startswith("next_action:")]))

    def test_resume_and_next_warn_and_stop_for_branch_or_commit_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = {
                "branch": ({"branch": "other"}, "branch_mismatch"),
                "commit": ({"commit": "0" * 40}, "commit_mismatch"),
                "implementation": (
                    {"implementation_head": "1" * 40}, "implementation_head_mismatch"
                ),
            }
            for name, (updates, warning) in cases.items():
                with self.subTest(name=name):
                    repo = root / name
                    state_file, state = self._initialize_operating_repo(repo)
                    self._write_state(state_file, state, **updates)
                    resume_code, resume_output = self._run_operating_command("resume", repo)
                    next_code, next_output = self._run_operating_command("next", repo)
                    self.assertEqual(0, resume_code)
                    self.assertIn(f"warning: {warning}", resume_output)
                    self.assertEqual(1, next_code)
                    self.assertIn("next_action: reconcile stale lifecycle state", next_output)

    def test_malformed_unsafe_selector_uses_safe_legacy_only_for_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            self._initialize_repo(repo)
            (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            (repo / ".execforge").mkdir()
            (repo / ".execforge" / "current.json").write_text(
                json.dumps({"run_id": "../../escape", "sensitive": "do-not-print"})
            )
            (repo / ".eng-level").mkdir()
            (repo / ".eng-level" / "state.json").write_text(
                json.dumps({"initiative": "Legacy Safe", "state": "PLAN_REQUIRED"})
            )

            resume_code, resume_output = self._run_operating_command("resume", repo)
            next_code, next_output = self._run_operating_command("next", repo)
            self.assertEqual(0, resume_code)
            self.assertIn("initiative: Legacy Safe", resume_output)
            self.assertIn("warning: selector_malformed", resume_output)
            self.assertNotIn("do-not-print", resume_output + next_output)
            self.assertEqual(1, next_code)
            self.assertIn("next_action: reconcile unreadable or unsafe lifecycle state", next_output)

            malformed_state = Path(tmp) / "malformed-state"
            state_file, state = self._initialize_operating_repo(malformed_state)
            self._write_state(
                state_file, state, artifact_root="../../unsafe", sensitive="do-not-print"
            )
            resume_code, resume_output = self._run_operating_command("resume", malformed_state)
            next_code, next_output = self._run_operating_command("next", malformed_state)
            self.assertEqual(1, resume_code)
            self.assertIn("warning: lifecycle_state_malformed", resume_output)
            self.assertEqual(1, next_code)
            self.assertIn("next_action: reconcile unreadable or unsafe lifecycle state", next_output)
            self.assertNotIn("do-not-print", resume_output + next_output)

            no_state = Path(tmp) / "no-state"
            self._initialize_repo(no_state)
            resume_code, resume_output = self._run_operating_command("resume", no_state)
            next_code, next_output = self._run_operating_command("next", no_state)
            self.assertEqual(1, resume_code)
            self.assertIn("lifecycle_state: unknown", resume_output)
            self.assertEqual(1, next_code)
            self.assertIn("next_action: reconcile unreadable or unsafe lifecycle state", next_output)

    def test_legacy_unknown_and_terminal_lifecycle_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = {
                "legacy": ("PLAN_REQUIRED", "create or revise engineering plan"),
                "unknown": ("FUTURE_STATE", "reconcile lifecycle state"),
                "review-ready": ("REVIEW_READY", "run Staff Engineer review"),
                "review-passed": ("REVIEW_PASSED", "run q-level --mode=auto"),
                "ship-ready": ("SHIP_READY", "prepare ship-ready handoff"),
            }
            for name, (lifecycle_state, action) in cases.items():
                with self.subTest(name=name):
                    repo = root / name
                    self._initialize_repo(repo)
                    (repo / "tracked.txt").write_text("base\n", encoding="utf-8")
                    self._git(repo, "add", ".")
                    self._git(repo, "commit", "-m", "base")
                    (repo / ".eng-level").mkdir()
                    (repo / ".eng-level" / "state.json").write_text(
                        json.dumps(
                            {
                                "initiative": name, "state": lifecycle_state,
                                "upstream_approval_status": (
                                    "PENDING" if name == "unknown" else "APPROVED"
                                ),
                                "open_blockers": [],
                            }
                        )
                    )
                    returncode, output = self._run_operating_command("next", repo)
                    self.assertEqual(0, returncode)
                    self.assertIn(f"next_action: {action}", output)
                    self.assertEqual(1, len([line for line in output.splitlines() if line.startswith("next_action:")]))

    def test_resume_and_next_are_registered_cli_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            self._initialize_operating_repo(repo)
            resume = subprocess.run(
                [sys.executable, str(SCRIPT), "resume", "--root", str(repo)],
                capture_output=True, text=True,
            )
            next_result = subprocess.run(
                [sys.executable, str(SCRIPT), "next", "--root", str(repo)],
                capture_output=True, text=True,
            )
            self.assertEqual(0, resume.returncode, resume.stdout + resume.stderr)
            self.assertIn("lifecycle_state: UPSTREAM_INTAKE", resume.stdout)
            self.assertEqual(0, next_result.returncode, next_result.stdout + next_result.stderr)
            self.assertEqual(
                ["next_action: capture upstream context"],
                [line for line in next_result.stdout.splitlines() if line.startswith("next_action:")],
            )

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

    def test_state_schemas_accept_template_state(self):
        """Each template must validate against the repository's corresponding schema."""
        for level in ("eng-level", "q-level"):
            schema = json.loads((ROOT / "schemas" / f"{level}-state.schema.json").read_text())
            template = json.loads(
                (ROOT / "skills" / level / "assets" / "state.template.json").read_text()
            )
            props = schema["properties"]
            metadata = {
                "run_id", "created_at", "updated_at", "branch", "commit",
                "artifact_root", "next_action",
            }
            self.assertTrue(metadata.isdisjoint(schema["required"]))
            for key, value in template.items():
                self.assertIn(
                    key, props, f"{level} state template key {key!r} is absent from the schema"
                )
                if "enum" in props[key]:
                    self.assertIn(
                        value,
                        props[key]["enum"],
                        f"{level} {key}={value!r} is not a schema-valid value",
                    )
                self.assertTrue(
                    self._matches_json_type(value, props[key].get("type")),
                    f"{level} template field {key!r} has the wrong JSON type",
                )
                if props[key].get("type") == "array":
                    self.assertIn("items", props[key])
                    for item in value:
                        self.assertTrue(
                            self._matches_json_type(item, props[key]["items"].get("type"))
                            or item in props[key]["items"].get("enum", []),
                            f"{level} array item in {key!r} violates its schema",
                        )

    def test_schema_allows_ungated_post_hoc_verdict(self):
        schema = json.loads((ROOT / "schemas" / "eng-level-state.schema.json").read_text())
        self.assertIn(
            "SHIP WITH REQUIRED FIXES (UNGATED)",
            schema["properties"]["final_decision"]["enum"],
        )

    def test_init_run_creates_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            product_run = module.init_run("Example Initiative", cwd)
            authoritative = json.loads((cwd / ".execforge" / "current.json").read_text())
            eng_pointer = json.loads((cwd / ".eng-level" / "current.json").read_text())
            qa_pointer = json.loads((cwd / ".q-level" / "current.json").read_text())
            eng_run = cwd / ".eng-level" / "runs" / eng_pointer["run_id"]
            qa_run = cwd / ".q-level" / "runs" / qa_pointer["run_id"]
            state = json.loads((eng_run / "state.json").read_text())
            self.assertEqual("Example Initiative", state["initiative"])
            self.assertEqual("UPSTREAM_INTAKE", state["state"])
            self.assertEqual([], state["routed_roles"])
            self.assertIsNone(state["stop_after"])
            self.assertTrue((eng_run / "backlog.md").exists())
            self.assertTrue((eng_run / "upstream-requirements.md").exists())
            qa_state = json.loads((qa_run / "state.json").read_text())
            self.assertEqual("Example Initiative", qa_state["initiative"])
            self.assertEqual("QA_INPUT_REQUIRED", qa_state["state"])
            self.assertEqual(eng_pointer["run_id"], qa_pointer["run_id"])
            self.assertEqual(eng_pointer["run_id"], product_run.name)
            self.assertEqual(product_run.name, authoritative["run_id"])
            self.assertEqual(eng_pointer["state_path"], authoritative["eng_state_path"])
            self.assertEqual(qa_pointer["state_path"], authoritative["qa_state_path"])
            self.assertEqual("1", eng_pointer["version"])
            self.assertEqual(
                f".eng-level/runs/{eng_pointer['run_id']}/state.json",
                eng_pointer["state_path"],
            )
            self.assertEqual(
                f".q-level/runs/{qa_pointer['run_id']}/state.json",
                qa_pointer["state_path"],
            )
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
                {path.name for path in qa_run.iterdir()},
            )

            for level, generated_state, artifact_root in (
                ("eng-level", state, f".eng-level/runs/{eng_pointer['run_id']}"),
                ("q-level", qa_state, f".q-level/runs/{qa_pointer['run_id']}"),
            ):
                self.assertEqual(eng_pointer["run_id"], generated_state["run_id"])
                self.assertEqual(artifact_root, generated_state["artifact_root"])
                self.assertEqual(generated_state["created_at"], generated_state["updated_at"])
                self.assertIn("T", generated_state["created_at"])
                self.assertIn("next_action", generated_state)
                self.assertIn("branch", generated_state)
                self.assertIn("commit", generated_state)
                schema = json.loads((ROOT / "schemas" / f"{level}-state.schema.json").read_text())
                self.assertTrue(set(schema["required"]).issubset(generated_state))
                for key, value in generated_state.items():
                    prop = schema["properties"][key]
                    self.assertTrue(self._matches_json_type(value, prop.get("type")))
                    if "enum" in prop:
                        self.assertIn(value, prop["enum"])

    def test_rapid_init_runs_are_distinct_and_preserve_prior_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            first_product = module.init_run("Collision Safe Initiative", cwd)
            first_eng_pointer = json.loads((cwd / ".eng-level" / "current.json").read_text())
            first_qa_pointer = json.loads((cwd / ".q-level" / "current.json").read_text())
            first_eng = cwd / ".eng-level" / "runs" / first_eng_pointer["run_id"]
            first_qa = cwd / ".q-level" / "runs" / first_qa_pointer["run_id"]
            (first_eng / "backlog.md").write_text("first run marker\n", encoding="utf-8")

            second_product = module.init_run("Collision Safe Initiative", cwd)
            second_eng_pointer = json.loads((cwd / ".eng-level" / "current.json").read_text())
            second_qa_pointer = json.loads((cwd / ".q-level" / "current.json").read_text())
            second_eng = cwd / ".eng-level" / "runs" / second_eng_pointer["run_id"]
            second_qa = cwd / ".q-level" / "runs" / second_qa_pointer["run_id"]

            self.assertNotEqual(first_product, second_product)
            self.assertNotEqual(first_eng, second_eng)
            self.assertNotEqual(first_qa, second_qa)
            self.assertEqual("first run marker\n", (first_eng / "backlog.md").read_text())
            self.assertTrue((first_qa / "state.json").is_file())
            self.assertEqual(second_product.name, second_eng_pointer["run_id"])
            self.assertEqual(second_product.name, second_qa_pointer["run_id"])
            self.assertRegex(
                second_product.name,
                r"^\d{8}T\d{12}Z-[0-9a-f]{8}-collision-safe-initiative$",
            )
            self.assertEqual([], list((cwd / ".eng-level").glob(".current.json.*.tmp")))
            self.assertEqual([], list((cwd / ".q-level").glob(".current.json.*.tmp")))

    def test_pointer_replace_failure_preserves_current_pointer(self):
        with tempfile.TemporaryDirectory() as tmp:
            lifecycle = Path(tmp) / ".eng-level"
            selected = lifecycle / "runs" / "selected"
            replacement = lifecycle / "runs" / "replacement"
            selected.mkdir(parents=True)
            replacement.mkdir(parents=True)
            (selected / "state.json").write_text("{}\n", encoding="utf-8")
            (replacement / "state.json").write_text("{}\n", encoding="utf-8")
            original = {"version": "1", "run_id": "selected"}
            (lifecycle / "current.json").write_text(json.dumps(original), encoding="utf-8")

            with mock.patch.object(Path, "replace", side_effect=OSError("replace failed")):
                with self.assertRaises(OSError):
                    module._write_current_pointer(lifecycle, "replacement")

            self.assertEqual(original, json.loads((lifecycle / "current.json").read_text()))
            self.assertEqual([], list(lifecycle.glob(".current.json.*.tmp")))

    def test_init_run_rejects_symlinked_namespace_roots_and_runs_without_outside_writes(self):
        for namespace in (".execforge", ".eng-level", ".q-level"):
            for attack in ("root", "runs"):
                with self.subTest(namespace=namespace, attack=attack):
                    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as out:
                        cwd = Path(tmp)
                        outside = Path(out)
                        if attack == "root":
                            (cwd / namespace).symlink_to(outside, target_is_directory=True)
                        else:
                            (cwd / namespace).mkdir()
                            (cwd / namespace / "runs").symlink_to(
                                outside, target_is_directory=True
                            )

                        with self.assertRaises(ValueError):
                            module.init_run("No Escape", cwd)

                        self.assertEqual([], list(outside.iterdir()))

    def test_failed_publication_restores_both_pointers_and_removes_new_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            first = module.init_run("First", cwd)
            eng_pointer = cwd / ".eng-level" / "current.json"
            qa_pointer = cwd / ".q-level" / "current.json"
            original_eng = eng_pointer.read_bytes()
            original_qa = qa_pointer.read_bytes()
            original_writer = module._write_current_pointer
            calls = 0

            def fail_second(root, run_id):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("second publication failed")
                return original_writer(root, run_id)

            with mock.patch.object(module, "_write_current_pointer", side_effect=fail_second):
                with self.assertRaises(OSError):
                    module.init_run("Second", cwd)

            self.assertEqual(original_eng, eng_pointer.read_bytes())
            self.assertEqual(original_qa, qa_pointer.read_bytes())
            self.assertEqual({first.name}, {path.name for path in (cwd / ".execforge" / "runs").iterdir()})
            self.assertEqual({first.name}, {path.name for path in (cwd / ".eng-level" / "runs").iterdir()})
            self.assertEqual({first.name}, {path.name for path in (cwd / ".q-level" / "runs").iterdir()})

    def test_failed_preparation_preserves_pointers_and_removes_new_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            first = module.init_run("First", cwd)
            pointers = {
                namespace: (cwd / namespace / "current.json").read_bytes()
                for namespace in (".eng-level", ".q-level")
            }
            original_copy = module.shutil.copy2
            calls = 0

            def fail_during_copy(source, destination):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("copy failed")
                return original_copy(source, destination)

            with mock.patch.object(module.shutil, "copy2", side_effect=fail_during_copy):
                with self.assertRaises(OSError):
                    module.init_run("Second", cwd)

            for namespace, content in pointers.items():
                self.assertEqual(content, (cwd / namespace / "current.json").read_bytes())
            for namespace in (".execforge", ".eng-level", ".q-level"):
                self.assertEqual(
                    {first.name},
                    {path.name for path in (cwd / namespace / "runs").iterdir()},
                )

    def test_failed_run_directory_creation_cleans_partial_new_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            first = module.init_run("First", cwd)
            pointers = {
                namespace: (cwd / namespace / "current.json").read_bytes()
                for namespace in (".eng-level", ".q-level")
            }
            original_mkdir = Path.mkdir

            def fail_qa_run(path, *args, **kwargs):
                if path.parent.name == "runs" and path.parent.parent.name == ".q-level":
                    raise OSError("run directory creation failed")
                return original_mkdir(path, *args, **kwargs)

            with mock.patch.object(Path, "mkdir", new=fail_qa_run):
                with self.assertRaises(OSError):
                    module.init_run("Second", cwd)

            for namespace, content in pointers.items():
                self.assertEqual(content, (cwd / namespace / "current.json").read_bytes())
            for namespace in (".execforge", ".eng-level", ".q-level"):
                self.assertEqual(
                    {first.name},
                    {path.name for path in (cwd / namespace / "runs").iterdir()},
                )

    def test_failed_initial_publication_restores_pointer_absence(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            original_writer = module._write_current_pointer
            calls = 0

            def fail_second(root, run_id):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("second publication failed")
                return original_writer(root, run_id)

            with mock.patch.object(module, "_write_current_pointer", side_effect=fail_second):
                with self.assertRaises(OSError):
                    module.init_run("First", cwd)

            self.assertFalse((cwd / ".eng-level" / "current.json").exists())
            self.assertFalse((cwd / ".q-level" / "current.json").exists())
            self.assertFalse((cwd / ".execforge" / "current.json").exists())
            for namespace in (".execforge", ".eng-level", ".q-level"):
                self.assertEqual([], list((cwd / namespace / "runs").iterdir()))

    def test_concurrent_init_runs_are_serialized_and_publish_aligned_pointers(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            original_seed = module.seed_q_level_artifacts
            guard = threading.Lock()
            active = 0
            maximum_active = 0

            def observed_seed(destination):
                nonlocal active, maximum_active
                with guard:
                    active += 1
                    maximum_active = max(maximum_active, active)
                time.sleep(0.05)
                try:
                    return original_seed(destination)
                finally:
                    with guard:
                        active -= 1

            with mock.patch.object(module, "seed_q_level_artifacts", side_effect=observed_seed):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    runs = list(pool.map(lambda name: module.init_run(name, cwd), ("One", "Two")))

            self.assertEqual(1, maximum_active)
            self.assertEqual(2, len({run.name for run in runs}))
            eng = json.loads((cwd / ".eng-level" / "current.json").read_text())
            qa = json.loads((cwd / ".q-level" / "current.json").read_text())
            self.assertEqual(eng["run_id"], qa["run_id"])
            authoritative = json.loads((cwd / ".execforge" / "current.json").read_text())
            self.assertEqual(eng["run_id"], authoritative["run_id"])

    def test_old_selector_wins_before_authoritative_commit(self):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            first = module.init_run("Old Authoritative", cwd)
            observed = {}

            def interrupt_before_authoritative(root, run_id):
                observed["eng"] = json.loads((cwd / ".eng-level" / "current.json").read_text())
                observed["qa"] = json.loads((cwd / ".q-level" / "current.json").read_text())
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    module.show_status(cwd)
                observed["status"] = output.getvalue()
                observed["portfolio_state"] = operating_state._state_metadata(cwd)[0]
                raise SystemExit("interrupted before authoritative publish")

            with mock.patch.object(
                module, "_write_authoritative_pointer", side_effect=interrupt_before_authoritative
            ):
                with self.assertRaises(SystemExit):
                    module.init_run("New Projection", cwd)

            self.assertEqual(first.name, observed["eng"]["run_id"])
            self.assertEqual(observed["eng"]["run_id"], observed["qa"]["run_id"])
            self.assertIn("initiative: Old Authoritative", observed["status"])
            self.assertNotIn("initiative: New Projection", observed["status"])
            self.assertEqual("Old Authoritative", observed["portfolio_state"]["initiative"])

    def test_base_exceptions_restore_all_selectors_after_each_publish_boundary(self):
        for boundary in ("after_eng", "after_qa", "before_authoritative", "at_authoritative"):
            with self.subTest(boundary=boundary):
                with tempfile.TemporaryDirectory() as tmp:
                    cwd = Path(tmp)
                    first = module.init_run("First", cwd)
                    selector_paths = (
                        cwd / ".eng-level" / "current.json",
                        cwd / ".q-level" / "current.json",
                        cwd / ".execforge" / "current.json",
                    )
                    originals = {path: path.read_bytes() for path in selector_paths}
                    projection_writer = module._write_current_pointer
                    authoritative_writer = module._write_authoritative_pointer
                    projection_calls = 0

                    def projections(root, run_id):
                        nonlocal projection_calls
                        projection_calls += 1
                        projection_writer(root, run_id)
                        if boundary == "after_eng" and projection_calls == 1:
                            raise KeyboardInterrupt()
                        if boundary == "after_qa" and projection_calls == 2:
                            raise KeyboardInterrupt()

                    def authoritative(root, run_id):
                        if boundary == "before_authoritative":
                            raise SystemExit()
                        authoritative_writer(root, run_id)
                        if boundary == "at_authoritative":
                            raise SystemExit()

                    with mock.patch.object(module, "_write_current_pointer", side_effect=projections), mock.patch.object(
                        module, "_write_authoritative_pointer", side_effect=authoritative
                    ):
                        with self.assertRaises((KeyboardInterrupt, SystemExit)):
                            module.init_run("Second", cwd)

                    for path, content in originals.items():
                        self.assertEqual(content, path.read_bytes())
                    for namespace in (".execforge", ".eng-level", ".q-level"):
                        self.assertEqual(
                            {first.name},
                            {path.name for path in (cwd / namespace / "runs").iterdir()},
                        )

    def test_authoritative_first_publication_is_observable_after_every_step(self):
        import contextlib
        import io

        for repository_kind in ("fresh", "replacement"):
            for boundary in ("authoritative", "eng_projection", "qa_projection"):
                with self.subTest(repository_kind=repository_kind, boundary=boundary):
                    with tempfile.TemporaryDirectory() as tmp:
                        cwd = Path(tmp)
                        if repository_kind == "replacement":
                            module.init_run("Old", cwd)
                        original_authoritative = module._write_authoritative_pointer
                        original_projection = module._write_current_pointer
                        projection_calls = 0
                        observed = {}

                        def observe_committed():
                            output = io.StringIO()
                            with contextlib.redirect_stdout(output):
                                module.show_status(cwd)
                            observed["status"] = output.getvalue()

                        def authoritative(root, run_id):
                            original_authoritative(root, run_id)
                            if boundary == "authoritative":
                                observe_committed()
                                raise KeyboardInterrupt()

                        def projection(root, run_id):
                            nonlocal projection_calls
                            projection_calls += 1
                            original_projection(root, run_id)
                            expected = 1 if boundary == "eng_projection" else 2
                            if boundary != "authoritative" and projection_calls == expected:
                                observe_committed()
                                raise KeyboardInterrupt()

                        with mock.patch.object(
                            module, "_write_authoritative_pointer", side_effect=authoritative
                        ), mock.patch.object(
                            module, "_write_current_pointer", side_effect=projection
                        ):
                            with self.assertRaises(KeyboardInterrupt):
                                module.init_run("New Committed", cwd)

                        self.assertIn("initiative: New Committed", observed["status"])

    def test_projection_restore_failure_retains_all_new_run_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("Old", cwd)
            original_authoritative = module._write_authoritative_pointer
            original_projection = module._write_current_pointer
            original_restore = module._restore_pointer
            published = {}

            def publish_then_fail(root, run_id):
                published["run_id"] = run_id
                original_authoritative(root, run_id)

            projection_calls = 0

            def fail_after_projection(root, run_id):
                nonlocal projection_calls
                projection_calls += 1
                original_projection(root, run_id)
                if projection_calls == 1:
                    raise OSError("projection publish failed")

            def fail_eng_restore(pointer, snapshot):
                if pointer == cwd / ".eng-level" / "current.json":
                    raise OSError("projection restore failed")
                return original_restore(pointer, snapshot)

            with mock.patch.object(
                module, "_write_authoritative_pointer", side_effect=publish_then_fail
            ), mock.patch.object(
                module, "_write_current_pointer", side_effect=fail_after_projection
            ), mock.patch.object(
                module, "_restore_pointer", side_effect=fail_eng_restore
            ):
                with self.assertRaises(module.RunPublicationError):
                    module.init_run("New Retained", cwd)

            run_id = published["run_id"]
            for namespace in (".execforge", ".eng-level", ".q-level"):
                self.assertTrue((cwd / namespace / "runs" / run_id).is_dir())

    def test_authoritative_reader_rejects_symlinked_namespace_roots(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as out:
            base = Path(tmp)
            outside = Path(out)
            for namespace in (".execforge", ".eng-level", ".q-level"):
                with self.subTest(namespace=namespace):
                    project = base / namespace.removeprefix(".")
                    project.mkdir()
                    module.init_run("Selected", project)
                    original = project / namespace
                    moved = outside / namespace.removeprefix(".")
                    shutil.move(original, moved)
                    original.symlink_to(moved, target_is_directory=True)

                    selected, finding = operating_state._selected_state_path(
                        project / ".eng-level"
                    )

                    self.assertIsNone(selected)
                    self.assertIsNotNone(finding)

    def test_restore_failures_are_aggregated_and_all_restores_attempted(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("First", cwd)
            original_restore = module._restore_pointer
            restored = []

            def record_restore(pointer, snapshot):
                restored.append(pointer)
                if len(restored) in {1, 2}:
                    raise OSError(f"restore {len(restored)} failed")
                return original_restore(pointer, snapshot)

            with mock.patch.object(
                module, "_write_authoritative_pointer", side_effect=ValueError("publish cause")
            ), mock.patch.object(module, "_restore_pointer", side_effect=record_restore):
                with self.assertRaises(module.RunPublicationError) as raised:
                    module.init_run("Second", cwd)

            self.assertEqual(3, len(restored))
            self.assertIsInstance(raised.exception.__cause__, ValueError)
            self.assertEqual(2, len(raised.exception.restore_errors))

    def test_failed_authoritative_restore_keeps_referenced_new_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            module.init_run("First", cwd)
            original_authoritative = module._write_authoritative_pointer
            original_restore = module._restore_pointer

            def publish_then_fail(root, run_id):
                original_authoritative(root, run_id)
                raise OSError("post-publish interruption")

            def fail_authoritative_restore(pointer, snapshot):
                if pointer == cwd / ".execforge" / "current.json":
                    raise OSError("authoritative restore failed")
                return original_restore(pointer, snapshot)

            with mock.patch.object(
                module, "_write_authoritative_pointer", side_effect=publish_then_fail
            ), mock.patch.object(module, "_restore_pointer", side_effect=fail_authoritative_restore):
                with self.assertRaises(module.RunPublicationError) as raised:
                    module.init_run("Referenced New", cwd)

            selected = json.loads((cwd / ".execforge" / "current.json").read_text())["run_id"]
            self.assertIsInstance(raised.exception.__cause__, OSError)
            for namespace in (".execforge", ".eng-level", ".q-level"):
                self.assertTrue((cwd / namespace / "runs" / selected).is_dir())

    def test_cli_imports_when_fcntl_is_unavailable(self):
        code = (
            "import builtins, runpy; original=builtins.__import__; "
            "builtins.__import__=lambda name,*a,**k: "
            "(_ for _ in ()).throw(ImportError('blocked')) if name=='fcntl' else original(name,*a,**k); "
            f"runpy.run_path({str(SCRIPT)!r}, run_name='execforge_import_test')"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, check=False
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_cross_process_init_runs_are_serialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            commands = [
                [sys.executable, str(SCRIPT), "init-run", "--name", name, "--root", str(cwd)]
                for name in ("Process One", "Process Two")
            ]
            processes = [
                subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for command in commands
            ]
            results = [process.communicate(timeout=15) + (process.returncode,) for process in processes]
            for stdout, stderr, returncode in results:
                self.assertEqual(0, returncode, stdout + stderr)
            authoritative = json.loads((cwd / ".execforge" / "current.json").read_text())
            eng = json.loads((cwd / ".eng-level" / "current.json").read_text())
            qa = json.loads((cwd / ".q-level" / "current.json").read_text())
            self.assertEqual(authoritative["run_id"], eng["run_id"])
            self.assertEqual(authoritative["run_id"], qa["run_id"])
            for namespace in (".execforge", ".eng-level", ".q-level"):
                self.assertEqual(2, len(list((cwd / namespace / "runs").iterdir())))

    def test_pointer_reader_rejects_noncanonical_ids_and_symlinked_selected_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            lifecycle = Path(tmp) / ".eng-level"
            safe = lifecycle / "runs" / "safe-run"
            safe.mkdir(parents=True)
            (safe / "state.json").write_text("{}\n", encoding="utf-8")
            pointer = lifecycle / "current.json"

            for run_id in (".", "..", "runs/other", r"runs\\other"):
                with self.subTest(run_id=run_id):
                    pointer.write_text(json.dumps({"run_id": run_id}), encoding="utf-8")
                    selected, finding = operating_state._selected_state_path(lifecycle)
                    self.assertIsNone(selected)
                    self.assertIsNotNone(finding)

            other = lifecycle / "runs" / "other-run"
            other.mkdir()
            (other / "state.json").write_text("{}\n", encoding="utf-8")
            (safe / "state.json").unlink()
            (safe / "state.json").symlink_to(other / "state.json")
            pointer.write_text(json.dumps({"run_id": "safe-run"}), encoding="utf-8")
            selected, finding = operating_state._selected_state_path(lifecycle)
            self.assertIsNone(selected)
            self.assertIsNotNone(finding)

    def test_pointer_reader_rejects_symlinked_run_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            lifecycle = Path(tmp) / ".eng-level"
            (lifecycle / "runs").mkdir(parents=True)
            actual = lifecycle / "runs" / "actual"
            actual.mkdir()
            (actual / "state.json").write_text("{}\n", encoding="utf-8")
            (lifecycle / "runs" / "selected").symlink_to(actual, target_is_directory=True)
            (lifecycle / "current.json").write_text(
                json.dumps({"run_id": "selected"}), encoding="utf-8"
            )

            selected, finding = operating_state._selected_state_path(lifecycle)

            self.assertIsNone(selected)
            self.assertIsNotNone(finding)

    def test_pointer_writer_rejects_noncanonical_ids_and_symlinked_run_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            lifecycle = Path(tmp) / ".eng-level"
            actual = lifecycle / "runs" / "actual"
            actual.mkdir(parents=True)
            (actual / "state.json").write_text("{}\n", encoding="utf-8")

            for run_id in (".", "..", "runs/other", r"runs\\other"):
                with self.subTest(run_id=run_id):
                    with self.assertRaises(ValueError):
                        module._write_current_pointer(lifecycle, run_id)

            selected = lifecycle / "runs" / "selected"
            selected.symlink_to(actual, target_is_directory=True)
            with self.assertRaises(ValueError):
                module._write_current_pointer(lifecycle, "selected")
            self.assertFalse((lifecycle / "current.json").exists())

    def test_status_uses_current_pointer_and_falls_back_only_when_invalid(self):
        import contextlib
        import io

        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            legacy_root = cwd / ".eng-level"
            legacy_root.mkdir()
            (legacy_root / "state.json").write_text(
                json.dumps({"initiative": "Legacy", "state": "PLAN_REQUIRED"}),
                encoding="utf-8",
            )
            (legacy_root / "backlog.md").write_text("# Legacy backlog\n", encoding="utf-8")

            module.init_run("Selected", cwd)
            selected = io.StringIO()
            with contextlib.redirect_stdout(selected):
                module.show_status(cwd)
            self.assertIn("initiative: Selected", selected.getvalue())
            self.assertNotIn("initiative: Legacy", selected.getvalue())

            (cwd / ".execforge" / "current.json").write_text(
                json.dumps({"version": "1", "state_path": "../../outside.json"}),
                encoding="utf-8",
            )
            fallback = io.StringIO()
            with contextlib.redirect_stdout(fallback):
                module.show_status(cwd)
            self.assertIn("initiative: Legacy", fallback.getvalue())

    def test_init_run_records_git_and_detached_head_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            self._initialize_repo(repo)
            (repo / "tracked.txt").write_text("tracked\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            commit = self._git(repo, "rev-parse", "HEAD").stdout.strip()

            module.init_run("Attached", repo)
            attached_pointer = json.loads((repo / ".eng-level" / "current.json").read_text())
            attached = json.loads((repo / attached_pointer["state_path"]).read_text())
            self.assertEqual("main", attached["branch"])
            self.assertEqual(commit, attached["commit"])

            self._git(repo, "checkout", "--detach")
            module.init_run("Detached", repo)
            detached_pointer = json.loads((repo / ".eng-level" / "current.json").read_text())
            detached = json.loads((repo / detached_pointer["state_path"]).read_text())
            self.assertIsNone(detached["branch"])
            self.assertEqual(commit, detached["commit"])

    @staticmethod
    def _matches_json_type(value, expected):
        if expected is None:
            return True
        expected_types = expected if isinstance(expected, list) else [expected]
        checks = {
            "null": value is None,
            "string": isinstance(value, str),
            "array": isinstance(value, list),
            "object": isinstance(value, dict),
            "boolean": isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        }
        return any(checks.get(item, False) for item in expected_types)


if __name__ == "__main__":
    unittest.main()
