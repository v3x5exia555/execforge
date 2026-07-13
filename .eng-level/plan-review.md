# Stage 3 — Engineering Plan Review (fallback contract)

Reviewer: eng-level --mode=plan, fallback review contract (interactive gstack
`plan-eng-review` not invoked; this is a direct structured review).
Base branch: main. Verdict: **APPROVED WITH CONDITIONS**.

## Approved design: Initiative Flags mechanism

A small set of named flags captured at the product/upstream stage that drive conditional
downstream gates. Chosen over inline one-liners per the Stage 1 user decision ("create
flags — will need more scope").

Flags (v1):
- `offensive-security` — the work operates against systems/people as an adversary would
  (phishing simulation, pentest, red-team, credential capture, C2).
- `legally-gated` — the work requires documented authorization/consent to be lawful.
- `regulated-impersonation` — the work impersonates a real brand, person, or authority.
- `user-prescribed-mechanism` — the requester specified *how*, not just the outcome.

Setting `offensive-security`, `legally-gated`, or `regulated-impersonation` arms the
**Authorization / Rules-of-Engagement gate**. Setting `user-prescribed-mechanism` arms the
**goal-vs-mechanism guard**.

## Architecture & constraints (verified against the codebase)

1. **No shared skill directory.** `scripts/execforge.py: validate_repo` iterates every dir
   under `skills/`, requires a `SKILL.md`, and enforces a kebab-case name. A
   `skills/_shared/` folder fails validation. → The authoritative flag catalog lives in
   `skills/execforge/references/initiative-flags.md`.
2. **Skills install standalone** into `~/.claude/skills/<name>/`. Cross-skill relative
   links (`../full-cycle/...`) are brittle. → Each consuming `SKILL.md` names the flags
   inline and self-contained; only execforge hard-links the catalog file.
3. **SKILL.md ≤ 500 lines** (validator). Current: execforge 132, eng-level 185,
   full-cycle 78, sec-level 83. Additions are tight; detail pushed to references. Safe.
4. **All local links in SKILL.md must resolve** (validator). Any new reference must exist
   and be linked from its owning skill only.
5. **Version/manifest coupling.** `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
   skill lists must equal BUNDLED_SKILLS (unchanged — no skills added). Per-skill
   `metadata.version` and plugin `version` bump by convention.

## Exact implementation tasks and expected files

1. `skills/execforge/references/initiative-flags.md` (NEW) — flag catalog; Authorization/RoE
   gate contract (required evidence: written authorization, scope of engagement, consent/
   legal basis, no unapproved third-party impersonation, captured-credential handling &
   retention); goal-vs-mechanism guard; authorization record format + AUTHORIZED /
   NOT AUTHORIZED / N-A(justified) decision values.
2. `skills/execforge/SKILL.md` — add a flag-setting step to the orchestrator process; add
   the goal-vs-mechanism guard rule + a "goal vs mechanism" output-ledger field; add
   authorization to non-negotiable controls when a gating flag is set; link the new
   reference.
3. `skills/eng-level/SKILL.md` — upstream stop check gains two required fields:
   "Acceptance criteria / definition of done" and "Initiative flags & authorization
   status"; planning may not proceed while a gating flag has an unresolved authorization
   decision.
4. `skills/full-cycle/SKILL.md` — add operating rule 7: Authorization/RoE gate is a hard
   STOP before Stage 4 whenever a gating flag is set; an unresolved authorization decision
   blocks Stage 9 like a P0. Extend the validation gate.
5. `skills/sec-level/SKILL.md` — one paragraph: the authorization/RoE gate is a governance
   prerequisite distinct from technical appsec; reference it by name (no cross-file link).
6. `tests/test_skill_bundle.py` — add `references/initiative-flags.md` to the linked-
   references expectation for execforge; add a test asserting the flag names + gate verdict
   values appear in the flag catalog (locks the contract).
7. `docs/authorization-gate.md` (NEW) + `mkdocs.yml` nav entry — concept doc.
8. `evaluations/full-cycle.eval.md` / `execforge.eval.md` — add authorization-gate and
   goal-vs-mechanism scenarios (or dedicated eval files) with expected STOP behavior and
   failure conditions (agent self-answering the gate; gate firing on ordinary work).
9. `CHANGELOG.md` entry; bump versions: plugin manifests 0.6.0→0.7.0; touched skills'
   metadata.version.

## Failure paths / edge cases

- **Gate fatigue (false positives):** gate is strictly conditional on flags; ordinary
  changes set no gating flag and never hit the STOP. Covered by an eval failure condition.
- **Agent self-answering the gate:** contract states it is a real recorded user STOP;
  eval failure condition asserts the agent must not infer authorization.
- **Standalone install link breakage:** mitigated by self-contained inline flag naming.

## Tests / definition of done

- `python3 -m unittest discover -s tests` green (existing 13 + new assertions).
- `python3 scripts/execforge.py validate` (or equivalent) reports no errors.
- Dry-run walkthrough (Stage 5): phishing-style initiative hits the Authorization STOP; an
  ordinary refactor does not; a prescribed-mechanism request surfaces the guard.

## Conditions

- Keep each SKILL.md self-contained (no cross-skill file links).
- Keep the gate conditional; prove no false hard-stop in the dry run.

## Threat-model note (sec-level, light)

This change introduces no runtime/attack surface. The asset being protected is the
**integrity of the authorization gate** itself. Primary threat (STRIDE: Repudiation /
Elevation): the gate is bypassed or self-answered so unauthorized offensive work proceeds.
Control: the gate is a real user STOP with a recorded authorization artifact, and an
unresolved decision blocks ship — mirroring existing "never claim a gate that did not
happen." No S0/S1 threats. Full `sec-level review` at Stage 6 will confirm the shipped
text encodes this control.
