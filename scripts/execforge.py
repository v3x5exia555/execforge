#!/usr/bin/env python3
"""ExecForge repository utility.

No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import threading
import unicodedata
from datetime import datetime, timezone
import uuid

try:
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - exercised by the portability subprocess test
    _fcntl = None
try:
    import msvcrt as _msvcrt
except ImportError:  # pragma: no cover - unavailable on POSIX
    _msvcrt = None

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
_RUN_NAMESPACES = (".execforge", ".eng-level", ".q-level")
_SELECTOR_MAX_BYTES = 1024 * 1024
_INIT_LOCKS: dict[str, threading.Lock] = {}
_INIT_LOCKS_GUARD = threading.Lock()


def _terminal_safe(value: object, limit: int = 500) -> str:
    """Render untrusted metadata without terminal controls or unbounded output."""
    rendered: list[str] = []
    rendered_length = 0
    for character in str(value):
        if unicodedata.category(character).startswith("C"):
            codepoint = ord(character)
            if codepoint <= 0xFF:
                rendered.append(f"\\x{codepoint:02x}")
            elif codepoint <= 0xFFFF:
                rendered.append(f"\\u{codepoint:04x}")
            else:
                rendered.append(f"\\U{codepoint:08x}")
        else:
            rendered.append(character)
        rendered_length += len(rendered[-1])
        if rendered_length >= limit:
            break
    return "".join(rendered)[:limit]


class RunPublicationError(RuntimeError):
    def __init__(self, original: BaseException, restore_errors: list[BaseException]):
        super().__init__(
            f"run publication failed ({type(original).__name__}); "
            f"{len(restore_errors)} selector restore(s) also failed"
        )
        self.original = original
        self.restore_errors = tuple(restore_errors)


def _load_operating_state_module():
    path = Path(__file__).resolve().with_name("operating_state.py")
    spec = importlib.util.spec_from_file_location("execforge_operating_state", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load operating-state diagnostics from {path}")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


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


def build_grading_prompt(case: dict, transcript: str) -> str:
    expected = "\n".join(f"{i}. {item}" for i, item in enumerate(case["expected"]))
    failures = "\n".join(f"{i}. {item}" for i, item in enumerate(case["failures"]))
    return (
        "You are grading an agent transcript against a behavioral checklist.\n"
        "Judge only what the transcript shows; a behavior not visible in the "
        "transcript was not observed.\n\n"
        f"EXPECTED BEHAVIORS:\n{expected}\n\n"
        f"FAILURE CONDITIONS:\n{failures}\n\n"
        f"TRANSCRIPT:\n{transcript}\n\n"
        "Reply with ONLY a JSON object, no prose: "
        '{"expected": [<bool per expected behavior, in order>], '
        '"failures": [<bool per failure condition, in order>]}'
    )


def parse_verdict(text: str, n_expected: int, n_failures: int) -> dict:
    """Extract the judge's checklist verdict. The pass verdict is recomputed
    locally; the judge's own pass claim is never trusted."""
    for match in re.finditer(r"\{.*?\}", text, re.S):
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            continue
        expected = data.get("expected")
        failures = data.get("failures")
        if (isinstance(expected, list) and len(expected) == n_expected
                and isinstance(failures, list) and len(failures) == n_failures):
            expected = [bool(v) for v in expected]
            failures = [bool(v) for v in failures]
            return {
                "expected": expected,
                "failures": failures,
                "passed": all(expected) and not any(failures),
            }
    raise ValueError("judge output contained no verdict JSON with matching list sizes")


def run_eval_case(path: Path, agent_cmd: list[str], judge_cmd: list[str],
                  timeout: int = 600) -> dict:
    """Replay a case's scenario through a headless agent, then grade the transcript."""
    case = parse_eval_case(path)
    agent = subprocess.run(agent_cmd + [case["scenario"]], capture_output=True,
                           text=True, timeout=timeout)
    transcript = agent.stdout + agent.stderr
    judge = subprocess.run(judge_cmd + [build_grading_prompt(case, transcript)],
                           capture_output=True, text=True, timeout=timeout)
    verdict = parse_verdict(judge.stdout, len(case["expected"]), len(case["failures"]))
    return {"id": case["id"], "transcript": transcript, **verdict}


def cmd_eval(args) -> int:
    failed = 0
    cases: list[tuple[Path, str]] = []
    for path in sorted((ROOT / "evaluations").glob("*.eval.md")):
        try:
            cases.append((path, parse_eval_case(path)["id"]))
        except ValueError as exc:
            print(f"ERROR {path.name}: {exc}")
            failed += 1
    if args.list:
        for _, case_id in cases:
            print(case_id)
        return 1 if failed else 0
    if args.case != "all":
        cases = [(p, cid) for p, cid in cases if cid == args.case]
        if not cases:
            print(f"no eval case with id '{args.case}'")
            return 1
    if args.limit:
        cases = cases[: args.limit]
    agent_cmd = shlex.split(args.agent_cmd)
    judge_cmd = shlex.split(args.judge_cmd)
    passed = 0
    for path, _ in cases:
        try:
            result = run_eval_case(path, agent_cmd, judge_cmd)
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            print(f"ERROR {path.name}: {exc}")
            failed += 1
            continue
        print(f"{'PASS' if result['passed'] else 'FAIL'} {result['id']}")
        if result["passed"]:
            passed += 1
        else:
            failed += 1
    print(f"eval: {passed}/{len(cases)} passed")
    return 1 if failed else 0


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

    # Match the SKILL token case-sensitively. On Windows, pathlib applies
    # os.path.normcase inside glob, so `glob("*SKILL*.md")` matches
    # case-insensitively and wrongly flags legitimate lowercase files such as
    # skill-usage-feedback.md, breaking validate/doctor/install there.
    for stray in sorted(root.glob("*.md")):
        if "SKILL" in stray.name:
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


def doctor(installed: bool = False, portfolio: Path | None = None) -> int:
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

    if installed or portfolio is not None:
        operating_state = _load_operating_state_module()
        findings = ()
        if installed:
            installation_roots = tuple(
                destination_for(target) for target in ("claude", "codex", "agents")
            )
            findings += operating_state.installed_skill_diagnostics(SKILLS, installation_roots)
        if portfolio is not None:
            findings += operating_state.portfolio_diagnostics(portfolio)
        for finding in findings:
            print(
                f"[{_terminal_safe(finding.severity).upper()}] "
                f"{_terminal_safe(finding.code)} "
                f"{_terminal_safe(finding.project)}: {_terminal_safe(finding.detail)}"
            )
            if finding.severity == "error":
                hard_failures += 1

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


# Must stay equal to operating_state.py's `_is_string(state.get("initiative"), 512, ...)`
# reader bound: the producer and reader disagreeing on the limit is the gap this closes.
_MAX_INITIATIVE_NAME_LENGTH = 512


def _validate_initiative_name(name: str) -> str:
    """Reject names that would corrupt generated Markdown/state artifacts."""
    stripped = name.strip()
    if not stripped:
        raise ValueError("initiative name must not be empty or whitespace-only")
    if len(stripped) > _MAX_INITIATIVE_NAME_LENGTH:
        raise ValueError(
            f"initiative name must be at most {_MAX_INITIATIVE_NAME_LENGTH} characters"
        )
    if any(
        unicodedata.category(ch).startswith("C") or ch in "  "
        for ch in stripped
    ):
        raise ValueError("initiative name must be a single line with no control characters")
    return stripped


def init_run(name: str, cwd: Path) -> Path:
    name = _validate_initiative_name(name)
    cwd = Path(cwd)
    _validate_run_storage(cwd)
    with _repository_init_lock(cwd):
        _validate_run_storage(cwd)
        return _init_run_locked(name, cwd)


def _init_run_locked(name: str, cwd: Path) -> Path:
    safe = re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-") or "initiative"
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%S%fZ")
    run_id = f"{timestamp}-{uuid.uuid4().hex[:8]}-{safe}"
    roots = {namespace: cwd / namespace for namespace in _RUN_NAMESPACES}
    for root in roots.values():
        root.mkdir(exist_ok=True)
        (root / "runs").mkdir(exist_ok=True)
    _validate_run_storage(cwd)

    run = roots[".execforge"] / "runs" / run_id
    lifecycle = roots[".eng-level"]
    lifecycle_run = lifecycle / "runs" / run_id
    qa = roots[".q-level"]
    qa_run = qa / "runs" / run_id
    new_runs = (run, lifecycle_run, qa_run)
    pointer_snapshots = {
        root: _snapshot_pointer(root / "current.json")
        for root in (lifecycle, qa, roots[".execforge"])
    }
    branch, commit = _git_metadata(cwd)
    created_at = now.isoformat()
    publication_started = False
    try:
        for new_run in new_runs:
            new_run.mkdir(exist_ok=False)

        (run / "shared-context.md").write_text(
            f"# Shared Context\n\n- Initiative: {name}\n- Created: {now.isoformat()}\n\n"
            "## Facts\n\n## Assumptions\n\n## Inferences\n\n## Unknowns\n",
            encoding="utf-8",
        )
        (run / "scope-ledger.md").write_text(
            "# Scope Ledger\n\n| Item | Decision | Evidence | Reason | Owner |\n"
            "|---|---|---|---|---|\n",
            encoding="utf-8",
        )

        state_source = SKILLS / "eng-level" / "assets" / "state.template.json"
        state = json.loads(state_source.read_text(encoding="utf-8"))
        state.update(
            initiative=name, run_id=run_id, created_at=created_at, updated_at=created_at,
            branch=branch, commit=commit, artifact_root=f".eng-level/runs/{run_id}",
            next_action="Complete upstream intake and secure approval.",
        )
        (lifecycle_run / "state.json").write_text(
            json.dumps(state, indent=2) + "\n", encoding="utf-8"
        )
        shutil.copy2(
            SKILLS / "eng-level" / "assets" / "upstream-requirements.template.md",
            lifecycle_run / "upstream-requirements.md",
        )
        shutil.copy2(
            SKILLS / "eng-level" / "assets" / "backlog.template.md",
            lifecycle_run / "backlog.md",
        )

        qa_state = json.loads(
            (SKILLS / "q-level" / "assets" / "state.template.json").read_text(
                encoding="utf-8"
            )
        )
        qa_state.update(
            initiative=name, run_id=run_id, created_at=created_at, updated_at=created_at,
            branch=branch, commit=commit, artifact_root=f".q-level/runs/{run_id}",
            next_action="Complete QA context after engineering handoff.",
        )
        (qa_run / "state.json").write_text(
            json.dumps(qa_state, indent=2) + "\n", encoding="utf-8"
        )
        seed_q_level_artifacts(qa_run)

        publication_started = True
        _write_authoritative_pointer(roots[".execforge"], run_id)
        _write_current_pointer(lifecycle, run_id)
        _write_current_pointer(qa, run_id)
    except BaseException as original:
        restore_errors: list[BaseException] = []
        if publication_started:
            for root, snapshot in pointer_snapshots.items():
                try:
                    _restore_pointer(root / "current.json", snapshot)
                except BaseException as restore_error:
                    restore_errors.append(restore_error)
        if not restore_errors:
            referenced_run = _authoritative_run_id(cwd)
            for new_run in reversed(new_runs):
                if new_run.name != referenced_run:
                    _remove_new_run(new_run)
        if restore_errors:
            raise RunPublicationError(original, restore_errors) from original
        raise

    print(f"created run: {_terminal_safe(run)}")
    print(f"created lifecycle state: {_terminal_safe(lifecycle_run / 'state.json')}")
    print(f"created Q Level state: {_terminal_safe(qa_run / 'state.json')}")
    return run


def _validate_run_storage(cwd: Path) -> None:
    if cwd.is_symlink() or not cwd.is_dir():
        raise ValueError("repository root must be a real directory")
    repository = cwd.resolve()
    for namespace in _RUN_NAMESPACES:
        root = cwd / namespace
        if root.is_symlink():
            raise ValueError(f"{namespace} must not be a symlink")
        if root.exists():
            if not root.is_dir() or root.resolve() != repository / namespace:
                raise ValueError(f"{namespace} must be a contained directory")
            runs = root / "runs"
            if runs.is_symlink():
                raise ValueError(f"{namespace}/runs must not be a symlink")
            if runs.exists() and (
                not runs.is_dir() or runs.resolve() != repository / namespace / "runs"
            ):
                raise ValueError(f"{namespace}/runs must be a contained directory")


@contextmanager
def _repository_init_lock(cwd: Path):
    key = str(cwd.resolve())
    with _INIT_LOCKS_GUARD:
        thread_lock = _INIT_LOCKS.setdefault(key, threading.Lock())
    with thread_lock:
        lock_path = cwd / ".execforge-init-run.lock"
        if lock_path.is_symlink():
            raise ValueError("repository init lock must not be a symlink")
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(lock_path, flags, 0o600)
        acquired = False
        try:
            _lock_descriptor(descriptor)
            acquired = True
            yield
        finally:
            active_error = sys.exc_info()[1]
            release_errors: list[BaseException] = []
            try:
                if acquired:
                    _unlock_descriptor(descriptor)
            except BaseException as error:
                release_errors.append(error)
            try:
                os.close(descriptor)
            except BaseException as error:
                release_errors.append(error)
            if release_errors:
                if active_error is not None:
                    setattr(active_error, "lock_cleanup_errors", tuple(release_errors))
                else:
                    raise RuntimeError(
                        f"repository lock cleanup failed ({len(release_errors)} error(s))"
                    ) from release_errors[0]


def _lock_descriptor(descriptor: int) -> None:
    if os.name == "nt":
        if _msvcrt is None:
            raise RuntimeError("Windows file locking backend is unavailable")
        if os.fstat(descriptor).st_size == 0:
            os.write(descriptor, b"\0")
        os.lseek(descriptor, 0, os.SEEK_SET)
        _msvcrt.locking(descriptor, _msvcrt.LK_LOCK, 1)
    else:
        if _fcntl is None:
            raise RuntimeError("POSIX file locking backend is unavailable")
        _fcntl.flock(descriptor, _fcntl.LOCK_EX)


def _unlock_descriptor(descriptor: int) -> None:
    if os.name == "nt":
        os.lseek(descriptor, 0, os.SEEK_SET)
        _msvcrt.locking(descriptor, _msvcrt.LK_UNLCK, 1)
    else:
        _fcntl.flock(descriptor, _fcntl.LOCK_UN)


def _read_bounded_regular_file(path: Path, max_bytes: int) -> bytes | None:
    """Read a regular file through a bounded, non-following descriptor."""
    try:
        path_metadata = os.lstat(path)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ValueError("file must be a readable regular file") from exc
    if not stat.S_ISREG(path_metadata.st_mode):
        raise ValueError("file must be a real regular file")

    flags = os.O_RDONLY
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ValueError("file must be a readable regular file") from exc
    try:
        metadata = os.fstat(descriptor)
        current_metadata = os.lstat(path)
        identity = (metadata.st_dev, metadata.st_ino)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not stat.S_ISREG(current_metadata.st_mode)
            or identity != (path_metadata.st_dev, path_metadata.st_ino)
            or identity != (current_metadata.st_dev, current_metadata.st_ino)
            or metadata.st_size > max_bytes
        ):
            raise ValueError("file must be a bounded regular file")
        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(descriptor, min(64 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > max_bytes:
            raise ValueError("file exceeds the safe byte limit")
        return payload
    finally:
        os.close(descriptor)


def _snapshot_pointer(pointer: Path) -> bytes | None:
    return _read_bounded_regular_file(pointer, _SELECTOR_MAX_BYTES)


def _atomic_write(pointer: Path, payload: bytes) -> None:
    temporary = pointer.with_name(f".{pointer.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(pointer)
        _fsync_directory(pointer.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def _fsync_directory(directory: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _restore_pointer(pointer: Path, snapshot: bytes | None) -> None:
    if snapshot is None:
        if pointer.exists() and not pointer.is_symlink():
            pointer.unlink()
        return
    _atomic_write(pointer, snapshot)


def _remove_new_run(run: Path) -> None:
    if not run.exists() or run.is_symlink():
        return
    runs_root = run.parent
    if run.resolve().parent == runs_root.resolve():
        shutil.rmtree(run)


def _authoritative_run_id(cwd: Path) -> str | None:
    pointer = cwd / ".execforge" / "current.json"
    try:
        raw = _read_bounded_regular_file(pointer, _SELECTOR_MAX_BYTES)
    except (OSError, ValueError):
        return None
    if raw is None:
        return None
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        return None
    run_id = payload.get("run_id") if isinstance(payload, dict) else None
    return run_id if _is_canonical_run_id(run_id) else None


def _git_metadata(cwd: Path) -> tuple[str | None, str | None]:
    def query(*arguments: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", "-c", "core.fsmonitor=false", *arguments],
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15,
                check=False,
                env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
            )
        except (OSError, subprocess.SubprocessError):
            return None
        value = result.stdout.strip()
        return value if result.returncode == 0 and value else None

    return query("branch", "--show-current"), query("rev-parse", "HEAD")


def _write_current_pointer(lifecycle_root: Path, run_id: str) -> None:
    """Atomically select a contained initiative run."""
    if not _is_canonical_run_id(run_id):
        raise ValueError("run_id must be a single contained path component")
    runs_root = lifecycle_root / "runs"
    run_root = runs_root / run_id
    pointer = lifecycle_root / "current.json"
    if (
        lifecycle_root.is_symlink()
        or not lifecycle_root.is_dir()
        or runs_root.is_symlink()
        or not runs_root.is_dir()
        or run_root.is_symlink()
        or not run_root.is_dir()
        or pointer.is_symlink()
    ):
        raise ValueError("current pointer must use real contained directories")
    state_path = run_root / "state.json"
    try:
        relative = state_path.resolve().relative_to(lifecycle_root.resolve())
    except (OSError, ValueError) as exc:
        raise ValueError("current pointer must select a contained initiative state") from exc
    if (
        relative != Path("runs") / run_id / "state.json"
        or state_path.parent.resolve() != run_root.resolve()
        or not state_path.is_file()
        or state_path.is_symlink()
    ):
        raise ValueError("current pointer must select a contained initiative state")
    payload = {
        "version": "1",
        "run_id": run_id,
        "state_path": state_path.relative_to(lifecycle_root.parent).as_posix(),
    }
    _atomic_write(pointer, (json.dumps(payload, indent=2) + "\n").encode("utf-8"))


def _write_authoritative_pointer(execforge_root: Path, run_id: str) -> None:
    if not _is_canonical_run_id(run_id):
        raise ValueError("run_id must be canonical")
    repository = execforge_root.parent
    eng_state = repository / ".eng-level" / "runs" / run_id / "state.json"
    qa_state = repository / ".q-level" / "runs" / run_id / "state.json"
    for state, namespace in ((eng_state, ".eng-level"), (qa_state, ".q-level")):
        run_root = state.parent
        runs_root = run_root.parent
        if (
            run_root.is_symlink()
            or runs_root.is_symlink()
            or state.is_symlink()
            or not state.is_file()
            or state.resolve().relative_to(repository.resolve())
            != Path(namespace) / "runs" / run_id / "state.json"
        ):
            raise ValueError("authoritative selector must reference contained real state")
    payload = {
        "version": "1",
        "run_id": run_id,
        "eng_state_path": eng_state.relative_to(repository).as_posix(),
        "qa_state_path": qa_state.relative_to(repository).as_posix(),
    }
    _atomic_write(
        execforge_root / "current.json",
        (json.dumps(payload, indent=2) + "\n").encode("utf-8"),
    )


def _is_canonical_run_id(run_id: object) -> bool:
    return bool(
        isinstance(run_id, str)
        and len(run_id) <= 255
        and run_id not in {".", ".."}
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", run_id)
        and "/" not in run_id
        and "\\" not in run_id
    )


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


def release_check(root: Path = ROOT, tag: str | None = None) -> list[str]:
    """A release where the manifests, the CHANGELOG, and the tag disagree is not a release."""
    problems: list[str] = []
    versions: dict[str, str] = {}
    for manifest in PLUGIN_MANIFESTS:
        try:
            versions[manifest] = json.loads((root / manifest).read_text())["version"]
        except (OSError, KeyError, json.JSONDecodeError) as exc:
            problems.append(f"{manifest}: unreadable version ({exc})")
    try:
        changelog = (root / "CHANGELOG.md").read_text()
    except OSError as exc:
        problems.append(f"CHANGELOG.md: unreadable ({exc})")
    else:
        match = re.search(r"^## (\d+\.\d+\.\d+)", changelog, re.M)
        if not match:
            problems.append("CHANGELOG.md: no '## X.Y.Z' release heading found")
        else:
            versions["CHANGELOG.md"] = match.group(1)
    if len(set(versions.values())) > 1:
        problems.append(f"version mismatch: {versions}")
    if tag is not None and not problems:
        version = next(iter(versions.values()))
        if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
            problems.append(f"tag '{tag}' is not of the form vX.Y.Z")
        elif tag != f"v{version}":
            problems.append(f"tag '{tag}' does not match version {version}")
    return problems


def cmd_release_check(args) -> int:
    problems = release_check(tag=args.tag)
    for problem in problems:
        print(f"release-check: {problem}")
    if not problems:
        print("release-check: consistent")
    return 1 if problems else 0


def show_status(cwd: Path) -> int:
    found = False

    operating_state = _load_operating_state_module()

    state_file = operating_state.selected_or_legacy_state_path(cwd / ".eng-level")
    if state_file is not None:
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

        print_backlog(state_file.parent / "backlog.md")

    qa_file = operating_state.selected_or_legacy_state_path(cwd / ".q-level")
    if qa_file is not None:
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


def _print_operating_warnings(snapshot) -> None:
    for finding in snapshot.findings:
        print(
            f"warning: {_terminal_safe(finding.code)}: "
            f"{_terminal_safe(finding.detail)}"
        )


def resume_run(cwd: Path) -> int:
    """Report authoritative lifecycle metadata reconciled with actual Git state."""
    operating_state = _load_operating_state_module()
    snapshot = operating_state.operating_snapshot(cwd)
    state = snapshot.state or {}

    def recorded(key: str) -> str:
        if key not in state:
            return "unknown"
        value = state[key]
        if value is None:
            return "none"
        return _terminal_safe(value)

    print(f"initiative: {recorded('initiative')}")
    print(f"run_id: {recorded('run_id')}")
    print(f"git_branch: {_terminal_safe(snapshot.git_branch or 'unknown')}")
    print(f"git_head: {_terminal_safe(snapshot.git_head or 'unknown')}")
    print(f"lifecycle_state: {recorded('state')}")
    print(f"stop_after: {recorded('stop_after')}")
    blocker_fields = [
        state[key] for key in ("blockers", "open_blockers") if key in state
    ]
    blockers = sum((len(items) for items in blocker_fields), 0) if blocker_fields else None
    print(f"blockers: {blockers if blockers is not None else 'unknown'}")
    print(f"artifact_root: {recorded('artifact_root')}")
    evidence_root = snapshot.state_path.parent if snapshot.state_path else None
    backlog = evidence_root / "backlog.md" if evidence_root else None
    print(f"evidence_root: {_terminal_safe(evidence_root or 'unknown')}")
    print(f"backlog_location: {_terminal_safe(backlog or 'unknown')}")
    backlog_summary = (
        f"{snapshot.backlog_count} deferred action(s)"
        if snapshot.backlog_count is not None else "unknown"
    )
    print(f"backlog_summary: {backlog_summary}")
    recorded_next_action = state.get("next_action")
    print(f"recorded_next_action: {'present' if recorded_next_action else 'none'}")
    _print_operating_warnings(snapshot)
    return 0 if snapshot.state is not None else 1


def show_next(cwd: Path) -> int:
    """Print exactly one safe next action plus content-safe warnings."""
    operating_state = _load_operating_state_module()
    snapshot = operating_state.operating_snapshot(cwd)
    action, returncode = operating_state.deterministic_next(snapshot)
    print(f"next_action: {action}")
    blockers = []
    if snapshot.state:
        blockers = (snapshot.state.get("blockers") or []) + (
            snapshot.state.get("open_blockers") or []
        )
    if blockers:
        print(f"warning: open_blockers: {len(blockers)}")
    _print_operating_warnings(snapshot)
    return returncode


def main() -> int:
    parser = argparse.ArgumentParser(prog="execforge")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="validate repository structure and skills")

    install_parser = sub.add_parser("install", help="install skills")
    install_parser.add_argument("--target", choices=["claude", "codex", "agents"])
    install_parser.add_argument("--destination", type=Path)
    install_parser.add_argument("--force", action="store_true")

    sub.add_parser("check-superpowers", help="check common Superpowers locations")

    doctor_parser = sub.add_parser(
        "doctor", help="check installation prerequisites and dependencies"
    )
    doctor_parser.add_argument(
        "--installed", action="store_true", help="compare bundled skills with all known install roots"
    )
    doctor_parser.add_argument(
        "--portfolio", type=Path, help="scan direct-child Git repositories under PATH"
    )

    init_parser = sub.add_parser("init-run", help="initialize decision and lifecycle artifacts")
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--root", type=Path, default=Path.cwd())

    status_parser = sub.add_parser("status", help="show lifecycle state")
    status_parser.add_argument("--root", type=Path, default=Path.cwd())

    resume_parser = sub.add_parser("resume", help="resume selected lifecycle context")
    resume_parser.add_argument("--root", type=Path, default=Path.cwd())

    next_parser = sub.add_parser("next", help="show the next safe lifecycle action")
    next_parser.add_argument("--root", type=Path, default=Path.cwd())

    eval_parser = sub.add_parser("eval", help="run behavioral eval cases via a headless agent")
    eval_parser.add_argument("case", nargs="?", default="all", help="case id or 'all'")
    eval_parser.add_argument("--list", action="store_true", help="list case ids")
    eval_parser.add_argument("--limit", type=int, default=0, help="cap number of cases")
    eval_parser.add_argument("--agent-cmd", default="claude -p")
    eval_parser.add_argument("--judge-cmd", default="claude -p")

    release_parser = sub.add_parser("release-check", help="verify manifests, CHANGELOG, and tag agree")
    release_parser.add_argument("--tag", default=None)

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
        return doctor(installed=args.installed, portfolio=args.portfolio)

    if args.command == "init-run":
        try:
            init_run(args.name, args.root.resolve())
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        return 0

    if args.command == "status":
        return show_status(args.root.resolve())

    if args.command == "resume":
        return resume_run(args.root.resolve())

    if args.command == "next":
        return show_next(args.root.resolve())

    if args.command == "eval":
        return cmd_eval(args)

    if args.command == "release-check":
        return cmd_release_check(args)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
