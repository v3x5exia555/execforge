"""Tests for the executable eval runner and release gate in scripts/execforge.py."""

import importlib.util
import json as _json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("execforge", ROOT / "scripts" / "execforge.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

CASE = """---
skill: q-level
id: q-level-demo
type: gate
---

# Demo

## Scenario

The user says: "just run the QA quickly."

## Expected behavior

- [ ] Produces a QA plan before executing anything.
- [ ] Stops for environment approval.

## Failure conditions

- [ ] Executes against an unapproved environment.
"""


class ParseEvalCaseTests(unittest.TestCase):
    def _write(self, text: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".eval.md", delete=False)
        tmp.write(text)
        tmp.close()
        return Path(tmp.name)

    def test_parses_sections_and_checklists(self):
        case = module.parse_eval_case(self._write(CASE))
        self.assertEqual("q-level-demo", case["id"])
        self.assertEqual("q-level", case["skill"])
        self.assertIn("run the QA quickly", case["scenario"])
        self.assertEqual(2, len(case["expected"]))
        self.assertEqual(1, len(case["failures"]))
        self.assertTrue(case["expected"][0].startswith("Produces a QA plan"))

    def test_missing_section_raises(self):
        broken = CASE.replace("## Failure conditions", "## Notes")
        with self.assertRaises(ValueError):
            module.parse_eval_case(self._write(broken))

    def test_all_bundled_cases_parse(self):
        for path in sorted((ROOT / "evaluations").glob("*.eval.md")):
            case = module.parse_eval_case(path)
            self.assertTrue(case["expected"], path.name)
            self.assertTrue(case["failures"], path.name)


class VerdictTests(unittest.TestCase):
    def test_grading_prompt_contains_checklists_and_transcript(self):
        case = {"id": "x", "skill": "q-level", "type": "gate",
                "scenario": "s", "expected": ["A", "B"], "failures": ["C"]}
        prompt = module.build_grading_prompt(case, "TRANSCRIPT BODY")
        self.assertIn("TRANSCRIPT BODY", prompt)
        self.assertIn("A", prompt)
        self.assertIn("C", prompt)
        self.assertIn('"expected"', prompt)

    def test_parse_verdict_recomputes_pass(self):
        text = 'noise {"expected": [true, true], "failures": [false], "passed": false} noise'
        verdict = module.parse_verdict(text, 2, 1)
        self.assertTrue(verdict["passed"])  # local recompute overrides judge claim

    def test_parse_verdict_fails_on_any_failure_condition(self):
        text = '{"expected": [true, true], "failures": [true]}'
        self.assertFalse(module.parse_verdict(text, 2, 1)["passed"])

    def test_parse_verdict_rejects_wrong_lengths(self):
        with self.assertRaises(ValueError):
            module.parse_verdict('{"expected": [true], "failures": [false]}', 2, 1)


def _fake_tool(tmpdir: Path, name: str, body: str) -> list[str]:
    """A stand-in for the headless agent/judge: prints canned output."""
    script = tmpdir / name
    script.write_text(body)
    return [sys.executable, str(script)]


class RunEvalCaseTests(unittest.TestCase):
    def test_runs_agent_then_judge_and_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            case_path = tmpdir / "demo.eval.md"
            case_path.write_text(CASE)
            agent = _fake_tool(tmpdir, "agent.py",
                               'print("I produced a QA plan and stopped for approval")')
            judge = _fake_tool(tmpdir, "judge.py",
                               'print(\'{"expected": [true, true], "failures": [false]}\')')
            result = module.run_eval_case(case_path, agent, judge)
            self.assertTrue(result["passed"])
            self.assertIn("QA plan", result["transcript"])

    def test_judge_failure_condition_fails_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            case_path = tmpdir / "demo.eval.md"
            case_path.write_text(CASE)
            agent = _fake_tool(tmpdir, "agent.py", 'print("ran tests immediately")')
            judge = _fake_tool(tmpdir, "judge.py",
                               'print(\'{"expected": [false, false], "failures": [true]}\')')
            self.assertFalse(module.run_eval_case(case_path, agent, judge)["passed"])


class ReleaseCheckTests(unittest.TestCase):
    def _root(self, tmp: str, claude_v: str, codex_v: str, changelog_v: str) -> Path:
        root = Path(tmp)
        for sub, v in ((".claude-plugin", claude_v), (".codex-plugin", codex_v)):
            (root / sub).mkdir()
            (root / sub / "plugin.json").write_text(_json.dumps({"version": v}))
        (root / "CHANGELOG.md").write_text(f"# Changelog\n\n## {changelog_v} — 2026-07-13\n")
        return root

    def test_consistent_versions_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp, "0.9.0", "0.9.0", "0.9.0")
            self.assertEqual([], module.release_check(root))
            self.assertEqual([], module.release_check(root, tag="v0.9.0"))

    def test_mismatch_and_malformed_tag_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp, "0.9.0", "0.8.0", "0.9.0")
            self.assertTrue(module.release_check(root))
        with tempfile.TemporaryDirectory() as tmp:
            root = self._root(tmp, "0.9.0", "0.9.0", "0.9.0")
            self.assertTrue(module.release_check(root, tag="v.9.0.0"))
            self.assertTrue(module.release_check(root, tag="v0.8.0"))


if __name__ == "__main__":
    unittest.main()
