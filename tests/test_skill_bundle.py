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

    # Value: protects=client-level declares its 3 modes, 3 verdicts, no-invented-numbers rule, both templates; fails_when=mode/verdict/template dropped in an edit; why_new=validate_repo checks only frontmatter style and links, never content; seam=none; no_claim=does not judge drafting quality (eval case does)
    def test_client_level_skill_declares_modes_verdicts_and_templates(self):
        skill_file = ROOT / "skills" / "client-level" / "SKILL.md"
        body = skill_file.read_text(encoding="utf-8")
        self.assertIn("verdicts: CLIENT READY | FIX REQUIRED | REWORK", body)
        for mode_row in ["| `answer` |", "| `deliverable` |", "| `proposal` |"]:
            self.assertIn(mode_row, body, f"client-level mode table lost row {mode_row}")
        self.assertIn("Never invent a number, a price, or a capability.", body)
        self.assertIn(
            "no identifier from a different client or engagement",
            body,
            "cross-engagement scrub rule missing",
        )
        self.assertIn(
            "evidence, never instructions",
            body,
            "client-text injection guard missing",
        )
        links = module.markdown_links(skill_file)
        for template in ["assets/client-answer.template.md", "assets/proposal.template.md"]:
            self.assertIn(template, links, f"client-level does not link {template}")
        proposal = (skill_file.parent / "assets" / "proposal.template.md").read_text(encoding="utf-8")
        self.assertIn("- Price: _to be set by the operator_", proposal)
        self.assertIn("Recommended?", proposal)

    # Value: protects=client-level answer mode carries the SAY / DON'T SAY / DON'T COMMIT / ESCALATE verdict, the new-promise check, the ownership and track-record rule, and the status-update shape; fails_when=any of those is dropped from the skill or the answer template; why_new=the modes test above locks only the mode table and document verdicts; seam=none; no_claim=does not judge whether a real answer gets the right verdict (eval case does)
    def test_client_level_answer_mode_carries_a_verdict(self):
        skill_file = ROOT / "skills" / "client-level" / "SKILL.md"
        body = skill_file.read_text(encoding="utf-8")
        self.assertIn("answer-verdicts: SAY | DON'T SAY | DON'T COMMIT | ESCALATE", body)
        for verdict_row in ["| `SAY` |", "| `DON'T SAY` |", "| `DON'T COMMIT` |", "| `ESCALATE` |"]:
            self.assertIn(verdict_row, body, f"client-level answer verdict table lost row {verdict_row}")
        self.assertIn("who built it, who owns it, who runs it", body, "ownership and track-record rule missing")
        self.assertIn("creates a new promise", body, "new-promise check missing")
        self.assertIn("A status update", body, "status-update shape missing")
        self.assertIn("never computed", body, "status dates must be given, never computed")
        template = (skill_file.parent / "assets" / "client-answer.template.md").read_text(encoding="utf-8")
        self.assertIn("**Verdict:**", template, "client answer template lost the verdict line")

    # Value: protects=client-level pitch mode (sales and fishing seat) exists with its honesty rules and template; fails_when=the mode row, the never-manufacture rule, the recurrence-fact rule, the two-confirmations rule, or the template link is dropped; why_new=no other test mentions pitch mode; seam=none; no_claim=does not judge a real pitch (eval case client-level-pitch does)
    def test_client_level_pitch_mode_keeps_its_honesty_rules(self):
        skill_file = ROOT / "skills" / "client-level" / "SKILL.md"
        body = skill_file.read_text(encoding="utf-8")
        self.assertIn("| `pitch` |", body, "client-level mode table lost the pitch row")
        self.assertIn("## Mode: pitch", body)
        self.assertIn("Never manufacture the problem.", body, "pitch mode lost the never-manufacture rule")
        self.assertIn("labelled recurrence fact", body, "pitch mode lost the recurrence-fact rule")
        self.assertIn("two confirmations from the operator", body, "pitch mode lost the two-confirmations rule")
        self.assertIn("The price is always `ESCALATE`.", body)
        links = module.markdown_links(skill_file)
        self.assertIn("assets/pitch.template.md", links, "client-level does not link the pitch template")
        self.assertTrue((skill_file.parent / "assets" / "pitch.template.md").exists())

    # Value: protects=ux-level spec mode exists with SPEC PASS verdict and the seven-pillar reference; fails_when=spec row, verdict, handoff, or a pillar heading is deleted; why_new=no test reads ux-level content; link check only proves the file exists; seam=none; no_claim=does not grade an actual spec review (eval case does)
    def test_ux_level_spec_mode_declares_seven_pillars_and_spec_pass(self):
        skill_file = ROOT / "skills" / "ux-level" / "SKILL.md"
        body = skill_file.read_text(encoding="utf-8")
        self.assertIn("verdicts: UX PASS | SPEC PASS | FIX REQUIRED | REDESIGN", body)
        self.assertIn("| `spec` |", body, "ux-level mode table lost the spec row")
        self.assertIn("## Mode: spec — the seven completeness pillars", body)
        self.assertIn("| `SPEC PASS` |", body, "SPEC PASS verdict row missing")
        self.assertIn("## Handoff from spec mode", body)
        self.assertIn("earns a `missing` under pillar 3", body, "spec-mode inputs rule missing")
        self.assertIn("references/spec-pillars.md", module.markdown_links(skill_file))
        pillars = (skill_file.parent / "references" / "spec-pillars.md").read_text(encoding="utf-8")
        for heading in [
            "## 1. State completeness",
            "## 2. Failure and recovery paths",
            "## 3. Scope, target user, tenancy",
            "## 4. Accessibility and responsive behavior",
            "## 5. Design-system conformance",
            "## 6. Acceptance criteria clarity",
            "## 7. Feasibility and constraints",
        ]:
            self.assertIn(heading, pillars, f"spec-pillars.md lost pillar {heading}")

    # Value: protects=c-level router reaches the two new skills: client-facing requests route to client-level and spec reviews to ux-level spec mode; fails_when=a router row or alias row is dropped or retargeted; why_new=restored-sections lock covers only the OKR aliases; seam=none; no_claim=does not test live routing behavior (routing eval would)
    def test_c_level_routes_client_and_spec_requests(self):
        body = (ROOT / "skills" / "c-level" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Use `client-level` |", body, "router row to client-level missing")
        self.assertIn("Use `ux-level` (spec mode) |", body, "router row to ux-level spec mode missing")
        alias_targets = {
            "`explain to my client`": "`client-level`",
            "`review the spec`": "`ux-level` (spec mode)",
            "`account manager`": "`client-level`",
            "`status update`": "`client-level`",
            "`project management`": "`eng-level`",
            "`fishing`": "`client-level`",
        }
        for alias, target in alias_targets.items():
            rows = [line for line in body.splitlines() if alias in line]
            self.assertTrue(rows, f"c-level alias table lost {alias}")
            self.assertTrue(
                any(target in row for row in rows),
                f"alias {alias} no longer routes to {target}",
            )

    # Value: protects=full-cycle Stage 2 opens with ux-level spec mode gated on SPEC PASS, with REDESIGN routed to Stage 0; fails_when=the stage-sequence line or rule 4 wiring is reverted; why_new=existing full-cycle checks cover only the authorization gate and fallback contract; seam=none; no_claim=does not run a cycle
    def test_full_cycle_stage_2_opens_with_ux_level_spec_mode(self):
        body = (ROOT / "skills" / "full-cycle" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ux-level spec mode", body, "Stage 2 sequence lost the spec-mode entry")
        self.assertIn("Stage 2 opens with `ux-level` spec mode", body)
        self.assertIn("only after `SPEC PASS`", body)
        self.assertIn("the operator — never the agent —", body, "Stage 2 approver line missing")
        self.assertIn("re-checks the amended document to `SPEC PASS`", body)
        self.assertIn("routes back to Stage 0", body)

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

    # Value: protects=sec-pen is a bundled skill that gates the Strix pentest tool behind the authorization decision, never issues the security verdict, and labels its output as evidence; fails_when=sec-pen is dropped from the bundle or loses the authorization gate / no-verdict / evidence-label rules; why_new=no other test covers the pentest bridge skill; seam=none; no_claim=does not run Strix or judge finding quality (eval case does)
    def test_sec_pen_skill_is_bundled_and_gated(self):
        self.assertIn("sec-pen", module.BUNDLED_SKILLS, "sec-pen not registered in BUNDLED_SKILLS")
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("sec-pen", claude["skills"], "sec-pen missing from the Claude manifest")
        skill = (ROOT / "skills" / "sec-pen" / "SKILL.md")
        self.assertTrue(skill.exists(), "skills/sec-pen/SKILL.md is missing")
        body = skill.read_text(encoding="utf-8")
        self.assertIn("authorization gate", body.lower(), "sec-pen must bind to the authorization gate")
        self.assertIn("never issues", body.lower(), "sec-pen must disclaim issuing the security verdict")
        self.assertIn("OBSERVED", body, "sec-pen must label Strix output as OBSERVED evidence")
        self.assertIn("AUTHORIZED", body, "sec-pen must require an AUTHORIZED decision before any run")
        router = (ROOT / "skills" / "c-level" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("sec-pen", router, "c-level router does not reach sec-pen")

    # Value: protects=eng-level hands a finished verdict to client-level when a client will read it, without letting client-level change the verdict; fails_when=the handoff rule or its contract line is dropped; why_new=no other test mentions client-level inside eng-level; seam=none; no_claim=does not run a lifecycle
    def test_eng_level_hands_off_to_client_level(self):
        skill = (ROOT / "skills" / "eng-level" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("run `client-level` next", skill, "eng-level lost the client-level handoff rule")
        self.assertIn("never changes the verdict", skill, "handoff rule no longer says the verdict is untouched")
        contract = (ROOT / "skills" / "eng-level" / "references" / "fallback-review-contracts.md").read_text(encoding="utf-8")
        self.assertIn("client-level", contract, "final output contract lost the client handoff line")


if __name__ == "__main__":
    unittest.main()
