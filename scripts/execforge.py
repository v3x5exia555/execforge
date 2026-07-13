#!/usr/bin/env python3
"""ExecForge repository utility.

No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
BUNDLED_SKILLS = {"c-level", "design-html", "eng-level", "execforge", "full-cycle", "q-level", "sec-level"}
REQUIRED_SKILLS = BUNDLED_SKILLS
PLUGIN_MANIFESTS = [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]
Q_LEVEL_ASSET_FILES = {
    "coverage-matrix.md": "coverage-matrix.template.md",
    "decision.md": "decision.template.md",
    "defects.md": "defects.template.md",
    "environment-approval.md": "environment-approval.template.md",
    "execution-evidence.md": "execution-evidence.template.md",
    "qa-context.md": "qa-context.template.md",
    "qa-plan.md": "qa-plan.template.md",
    "retest.md": "retest.template.md",
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: unclosed YAML frontmatter") from exc

    result: dict[str, str] = {}
    current_key = None
    for line in lines[1:end]:
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        result[current_key] = value.strip().strip('"')
    return result


def markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def parse_eval_case(path: Path) -> dict:
    """Parse an evaluations/*.eval.md case into scenario + graded checklists."""
    meta = parse_frontmatter(path)
    text = path.read_text(encoding="utf-8")

    def section(name: str) -> str:
        match = re.search(rf"^## {re.escape(name)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not match:
            raise ValueError(f"{path.name}: missing required section '## {name}'")
        return match.group(1).strip()

    def checklist(name: str) -> list[str]:
        items = re.findall(r"^- \[ \] (.+)$", section(name), re.M)
        if not items:
            raise ValueError(f"{path.name}: section '## {name}' has no checklist items")
        return items

    return {
        "id": meta.get("id", path.stem),
        "skill": meta.get("skill", ""),
        "type": meta.get("type", ""),
        "scenario": section("Scenario"),
        "expected": checklist("Expected behavior"),
        "failures": checklist("Failure conditions"),
    }


def validate_repo(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return ["skills/ directory is missing"]

    discovered = {p.name for p in skills_root.iterdir() if p.is_dir()}
    missing = BUNDLED_SKILLS - discovered
    if missing:
        errors.append(f"Missing required skills: {', '.join(sorted(missing))}")

    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{skill_dir}: SKILL.md is missing")
            continue
        try:
            meta = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        name = meta.get("name", "")
        description = meta.get("description", "")
        if name != skill_dir.name:
            errors.append(f"{skill_file}: name '{name}' must match directory '{skill_dir.name}'")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"{skill_file}: invalid skill name '{name}'")
        if not description.lower().startswith("use when"):
            errors.append(f"{skill_file}: description must start with 'Use when'")
        if len(description) > 1024:
            errors.append(f"{skill_file}: description exceeds 1024 characters")
        line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            errors.append(f"{skill_file}: {line_count} lines; keep SKILL.md at or below 500")

        for target in markdown_links(skill_file):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (skill_file.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                errors.append(f"{skill_file}: broken local link {target}")

    for rel in [
        "README.md", "LICENSE", "mkdocs.yml",
        *PLUGIN_MANIFESTS,
        "schemas/execforge-decision.schema.json",
        "schemas/eng-level-state.schema.json",
        "schemas/q-level-state.schema.json",
    ]:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")

    for stray in root.glob("*SKILL*.md"):
        errors.append(f"{stray.name}: legacy root skill file; skill bodies belong under skills/<name>/")

    for path in list((root / "schemas").glob("*.json")) + list((root / ".claude-plugin").glob("*.json")) + list((root / ".codex-plugin").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")

    # Each host defines its own manifest contract. Validating both against one
    # shape is what previously hid the Codex manifest being unloadable.
    errors.extend(_validate_claude_manifest(root))
    errors.extend(_validate_codex_manifest(root))

    return errors


def _validate_claude_manifest(root: Path) -> list[str]:
    """Claude plugin manifest: skills is a list of bundled skill names."""
    errors: list[str] = []
    manifest = root / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        return errors

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    skills = payload.get("skills")
    if not isinstance(skills, list):
        errors.append(f"{manifest}: 'skills' must be a list of skill names for the Claude plugin format")
        return errors

    if set(skills) != BUNDLED_SKILLS:
        errors.append(
            f"{manifest}: skills {sorted(set(skills))} must match bundled skills {sorted(BUNDLED_SKILLS)}"
        )
    return errors


def _validate_codex_manifest(root: Path) -> list[str]:
    """Codex plugin manifest: skills is a plugin-root-relative directory path.

    Per the Codex plugin contract, `skills`/`mcpServers`/`apps` are relative path
    strings beginning with './' -- not arrays. A name array is silently unloadable,
    so assert the path shape and that the directory it names actually holds the
    bundled skills.
    """
    errors: list[str] = []
    manifest = root / ".codex-plugin" / "plugin.json"
    if not manifest.exists():
        return errors

    payload = json.loads(manifest.read_text(encoding="utf-8"))

    for field in ("name", "version", "description"):
        if not payload.get(field):
            errors.append(f"{manifest}: missing required field '{field}'")

    skills = payload.get("skills")
    if not isinstance(skills, str):
        errors.append(
            f"{manifest}: 'skills' must be a plugin-root-relative path string such as './skills/', "
            f"not {type(skills).__name__}; a name array does not load as a Codex plugin"
        )
        return errors

    if not skills.startswith("./"):
        errors.append(f"{manifest}: 'skills' path {skills!r} must be plugin-root-relative and start with './'")

    skills_dir = root / skills.lstrip("./").rstrip("/")
    if not skills_dir.is_dir():
        errors.append(f"{manifest}: 'skills' path {skills!r} does not resolve to a directory")
        return errors

    discovered = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists()}
    missing = BUNDLED_SKILLS - discovered
    if missing:
        errors.append(f"{manifest}: 'skills' path {skills!r} is missing bundled skills {sorted(missing)}")

    return errors


def destination_for(target: str) -> Path:
    home = Path.home()
    mapping = {
        "claude": home / ".claude" / "skills",
        "codex": home / ".codex" / "skills",
        "agents": home / ".agents" / "skills",
    }
    return mapping[target]


def verify_installed_skill(target: Path) -> list[str]:
    problems: list[str] = []
    skill_file = target / "SKILL.md"
    if not skill_file.exists():
        return [f"{target}: SKILL.md missing after install"]
    try:
        meta = parse_frontmatter(skill_file)
    except ValueError as exc:
        return [str(exc)]
    if meta.get("name") != target.name:
        problems.append(f"{skill_file}: installed name '{meta.get('name')}' does not match directory '{target.name}'")
    for link in markdown_links(skill_file):
        if "://" in link or link.startswith("#"):
            continue
        if not (skill_file.parent / link.split("#", 1)[0]).resolve().exists():
            problems.append(f"{skill_file}: broken local link {link}")
    return problems


def install(destination: Path, force: bool = False) -> None:
    errors = validate_repo()
    if errors:
        raise RuntimeError(
            "repository validation failed; refusing to install a broken bundle:\n  "
            + "\n  ".join(errors)
        )
    destination.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    for skill_name in sorted(BUNDLED_SKILLS):
        source = SKILLS / skill_name
        target = destination / source.name
        if target.exists():
            if not force:
                raise FileExistsError(f"{target} exists; rerun with --force")
            shutil.rmtree(target)
        shutil.copytree(source, target)
        problems.extend(verify_installed_skill(target))
        print(f"installed {source.name} -> {target}")
    if problems:
        raise RuntimeError("post-install verification failed:\n  " + "\n  ".join(problems))
    print(f"verified {len(BUNDLED_SKILLS)} installed skills at {destination}")


def seed_q_level_artifacts(destination: Path) -> None:
    assets_root = SKILLS / "q-level" / "assets"
    for target_name, template_name in Q_LEVEL_ASSET_FILES.items():
        shutil.copy2(assets_root / template_name, destination / target_name)


def doctor() -> int:
    hard_failures = 0

    def report(label: str, ok: bool, detail: str, hard: bool = True) -> None:
        nonlocal hard_failures
        status = "OK" if ok else ("FAIL" if hard else "WARN")
        print(f"[{status}] {label}: {detail}")
        if not ok and hard:
            hard_failures += 1

    version = sys.version_info
    report(
        "python",
        version >= (3, 9),
        f"{version.major}.{version.minor}.{version.micro} (requires >= 3.9)",
    )

    errors = validate_repo()
    report("repository", not errors, "validation passed" if not errors else "; ".join(errors))

    git = shutil.which("git")
    report("git", git is not None, git or "not found; eng-level diff review needs Git", hard=False)

    mkdocs = shutil.which("mkdocs")
    report("mkdocs", mkdocs is not None, mkdocs or "not found; optional, only needed to build docs", hard=False)

    for target in ["claude", "codex", "agents"]:
        destination = destination_for(target)
        probe = destination
        while not probe.exists() and probe != probe.parent:
            probe = probe.parent
        writable = os.access(probe, os.W_OK)
        report(f"install target {target}", writable, str(destination), hard=False)

    superpowers = check_superpowers() == 0
    report("superpowers", superpowers, "detected" if superpowers else "not detected; optional", hard=False)

    if hard_failures:
        print(f"doctor found {hard_failures} blocking problem(s).")
        return 1
    print("doctor found no blocking problems.")
    return 0


def check_superpowers() -> int:
    candidates = [
        Path.home() / ".claude" / "plugins",
        Path.home() / ".claude" / "skills" / "using-superpowers",
        Path.home() / ".codex" / "skills" / "using-superpowers",
        Path.home() / ".agents" / "skills" / "using-superpowers",
        ROOT / ".claude" / "skills" / "using-superpowers",
    ]
    found = [p for p in candidates if p.exists()]
    if found:
        print("Superpowers-related installation found:")
        for path in found:
            print(f"  - {path}")
        print("Read the installed current skill instructions before invoking them.")
        return 0
    print("Superpowers was not detected in common locations.")
    print("Install it separately using the official obra/superpowers instructions.")
    return 1


def init_run(name: str, cwd: Path) -> Path:
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-") or "initiative"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = cwd / ".execforge" / "runs" / f"{timestamp}-{safe}"
    run.mkdir(parents=True, exist_ok=False)
    (run / "shared-context.md").write_text(
        f"# Shared Context\n\n- Initiative: {name}\n- Created: {timestamp}\n\n"
        "## Facts\n\n## Assumptions\n\n## Inferences\n\n## Unknowns\n",
        encoding="utf-8",
    )
    (run / "scope-ledger.md").write_text(
        "# Scope Ledger\n\n| Item | Decision | Evidence | Reason | Owner |\n"
        "|---|---|---|---|---|\n",
        encoding="utf-8",
    )
    lifecycle = cwd / ".eng-level"
    lifecycle.mkdir(exist_ok=True)
    state_source = SKILLS / "eng-level" / "assets" / "state.template.json"
    state = json.loads(state_source.read_text(encoding="utf-8"))
    state["initiative"] = name
    (lifecycle / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    upstream_source = SKILLS / "eng-level" / "assets" / "upstream-requirements.template.md"
    shutil.copy2(upstream_source, lifecycle / "upstream-requirements.md")
    backlog_source = SKILLS / "eng-level" / "assets" / "backlog.template.md"
    shutil.copy2(backlog_source, lifecycle / "backlog.md")

    qa = cwd / ".q-level"
    qa.mkdir(exist_ok=True)
    qa_state_source = SKILLS / "q-level" / "assets" / "state.template.json"
    qa_state = json.loads(qa_state_source.read_text(encoding="utf-8"))
    qa_state["initiative"] = name
    (qa / "state.json").write_text(json.dumps(qa_state, indent=2) + "\n", encoding="utf-8")
    seed_q_level_artifacts(qa)

    print(f"created run: {run}")
    print(f"created lifecycle state: {lifecycle / 'state.json'}")
    print(f"created Q Level state: {qa / 'state.json'}")
    return run


def print_backlog(backlog_file: Path) -> None:
    """Surface deferred work. A parked plan nobody can find is not parked, it is lost."""
    if not backlog_file.exists():
        print("backlog: (none)")
        return

    rows = []
    for line in backlog_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Skip the header row and the unfilled template row.
        if not cells or cells[0] in {"#", ""} or not any(cells[1:2]):
            continue
        rows.append(cells)

    if not rows:
        print("backlog: (empty)")
        return

    print(f"backlog: {len(rows)} deferred action(s) in {backlog_file}")
    for cells in rows:
        num = cells[0] if len(cells) > 0 else "?"
        action = cells[1] if len(cells) > 1 else "?"
        cycle = cells[2] if len(cells) > 2 else "?"
        unblocks = cells[5] if len(cells) > 5 else ""
        suffix = f" | unblocked by: {unblocks}" if unblocks else ""
        print(f"  - [{cycle}] {num} {action}{suffix}")


def show_status(cwd: Path) -> int:
    found = False

    state_file = cwd / ".eng-level" / "state.json"
    if state_file.exists():
        found = True
        state = json.loads(state_file.read_text(encoding="utf-8"))
        print("[engineering]")
        for key in [
            "initiative", "state", "upstream_approval_status", "plan_status",
            "base_branch", "base_commit", "final_decision"
        ]:
            print(f"{key}: {state.get(key)}")

        # A stop boundary that is not reported is a brake nobody can see.
        roles = state.get("routed_roles") or []
        print(f"routed_roles: {', '.join(roles) if roles else '(none recorded)'}")
        print(f"adversarial_pair: {state.get('adversarial_pair', False)}")
        stop_after = state.get("stop_after")
        if stop_after:
            print(f"stop_after: {stop_after}  <- run halts here; do not resume without a new instruction")
        else:
            print("stop_after: None")
        if state.get("post_hoc_review"):
            print("post_hoc_review: true  <- ungated diff; SHIP is unavailable")

        blockers = state.get("open_blockers", [])
        print(f"open_blockers: {len(blockers)}")
        for blocker in blockers:
            print(f"  - {blocker}")

        print_backlog(cwd / ".eng-level" / "backlog.md")

    qa_file = cwd / ".q-level" / "state.json"
    if qa_file.exists():
        found = True
        state = json.loads(qa_file.read_text(encoding="utf-8"))
        print("[qa]")
        for key in [
            "initiative", "state", "plan_status", "plan_approval_status",
            "environment_approval_status", "target_environment", "build_or_commit",
            "execution_status", "evidence_status", "data_qa_required", "final_verdict"
        ]:
            print(f"{key}: {state.get(key)}")
        print(f"open_q0: {len(state.get('open_q0', []))}")
        print(f"open_q1: {len(state.get('open_q1', []))}")
        print(f"untested_areas: {len(state.get('untested_areas', []))}")

    if not found:
        print("No engineering or Q Level state found.")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="execforge")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="validate repository structure and skills")

    install_parser = sub.add_parser("install", help="install skills")
    install_parser.add_argument("--target", choices=["claude", "codex", "agents"])
    install_parser.add_argument("--destination", type=Path)
    install_parser.add_argument("--force", action="store_true")

    sub.add_parser("check-superpowers", help="check common Superpowers locations")

    sub.add_parser("doctor", help="check installation prerequisites and dependencies")

    init_parser = sub.add_parser("init-run", help="initialize decision and lifecycle artifacts")
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--root", type=Path, default=Path.cwd())

    status_parser = sub.add_parser("status", help="show lifecycle state")
    status_parser.add_argument("--root", type=Path, default=Path.cwd())

    args = parser.parse_args()

    if args.command == "validate":
        errors = validate_repo()
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("ExecForge validation passed.")
        return 0

    if args.command == "install":
        if bool(args.target) == bool(args.destination):
            parser.error("install requires exactly one of --target or --destination")
        destination = destination_for(args.target) if args.target else args.destination.expanduser().resolve()
        try:
            install(destination, args.force)
        except (FileExistsError, RuntimeError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        return 0

    if args.command == "check-superpowers":
        return check_superpowers()

    if args.command == "doctor":
        return doctor()

    if args.command == "init-run":
        init_run(args.name, args.root.resolve())
        return 0

    if args.command == "status":
        return show_status(args.root.resolve())

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
