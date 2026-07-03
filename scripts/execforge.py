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
REQUIRED_SKILLS = {"using-execforge", "execforge", "eng-lifecycle", "qa-lifecycle"}


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


def validate_repo(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return ["skills/ directory is missing"]

    discovered = {p.name for p in skills_root.iterdir() if p.is_dir()}
    missing = REQUIRED_SKILLS - discovered
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
        ".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
        "schemas/execforge-decision.schema.json",
        "schemas/eng-lifecycle-state.schema.json",
        "schemas/qa-lifecycle-state.schema.json",
    ]:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")

    for path in list((root / "schemas").glob("*.json")) + list((root / ".claude-plugin").glob("*.json")) + list((root / ".codex-plugin").glob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")

    return errors


def destination_for(target: str) -> Path:
    home = Path.home()
    mapping = {
        "claude": home / ".claude" / "skills",
        "codex": home / ".codex" / "skills",
        "agents": home / ".agents" / "skills",
    }
    return mapping[target]


def install(destination: Path, force: bool = False) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for source in sorted(SKILLS.iterdir()):
        if not source.is_dir():
            continue
        target = destination / source.name
        if target.exists():
            if not force:
                raise FileExistsError(f"{target} exists; rerun with --force")
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"installed {source.name} -> {target}")


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
    lifecycle = cwd / ".eng-lifecycle"
    lifecycle.mkdir(exist_ok=True)
    state_source = SKILLS / "eng-lifecycle" / "assets" / "state.template.json"
    state = json.loads(state_source.read_text(encoding="utf-8"))
    state["initiative"] = name
    (lifecycle / "state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    upstream_source = SKILLS / "eng-lifecycle" / "assets" / "upstream-requirements.template.md"
    shutil.copy2(upstream_source, lifecycle / "upstream-requirements.md")

    qa = cwd / ".qa-lifecycle"
    qa.mkdir(exist_ok=True)
    qa_state_source = SKILLS / "qa-lifecycle" / "assets" / "state.template.json"
    qa_state = json.loads(qa_state_source.read_text(encoding="utf-8"))
    qa_state["initiative"] = name
    (qa / "state.json").write_text(json.dumps(qa_state, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(SKILLS / "qa-lifecycle" / "assets" / "qa-plan.template.md", qa / "qa-plan.md")
    shutil.copy2(SKILLS / "qa-lifecycle" / "assets" / "coverage-matrix.template.md", qa / "coverage-matrix.md")

    print(f"created run: {run}")
    print(f"created lifecycle state: {lifecycle / 'state.json'}")
    print(f"created QA lifecycle state: {qa / 'state.json'}")
    return run


def show_status(cwd: Path) -> int:
    found = False

    state_file = cwd / ".eng-lifecycle" / "state.json"
    if state_file.exists():
        found = True
        state = json.loads(state_file.read_text(encoding="utf-8"))
        print("[engineering]")
        for key in [
            "initiative", "state", "upstream_approval_status", "plan_status",
            "base_branch", "base_commit", "final_decision"
        ]:
            print(f"{key}: {state.get(key)}")
        blockers = state.get("open_blockers", [])
        print(f"open_blockers: {len(blockers)}")
        for blocker in blockers:
            print(f"  - {blocker}")

    qa_file = cwd / ".qa-lifecycle" / "state.json"
    if qa_file.exists():
        found = True
        state = json.loads(qa_file.read_text(encoding="utf-8"))
        print("[qa]")
        for key in [
            "initiative", "state", "plan_status", "plan_approval_status",
            "target_environment", "build_or_commit", "final_verdict"
        ]:
            print(f"{key}: {state.get(key)}")
        print(f"open_q0: {len(state.get('open_q0', []))}")
        print(f"open_q1: {len(state.get('open_q1', []))}")
        print(f"untested_areas: {len(state.get('untested_areas', []))}")

    if not found:
        print("No engineering or QA lifecycle state found.")
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
        except FileExistsError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        return 0

    if args.command == "check-superpowers":
        return check_superpowers()

    if args.command == "init-run":
        init_run(args.name, args.root.resolve())
        return 0

    if args.command == "status":
        return show_status(args.root.resolve())

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
