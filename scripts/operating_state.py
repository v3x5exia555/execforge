#!/usr/bin/env python3
"""Read-only operating-state diagnostics for ExecForge."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Iterable, NamedTuple


class Finding(NamedTuple):
    """An immutable, content-safe diagnostic result."""

    severity: str
    code: str
    project: str
    detail: str


_CONFLICT_CODES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
_STATE_FIELDS = {"initiative", "state", "branch", "base_branch", "run_id"}


def _tree_digest(root: Path) -> str:
    """Hash a directory's complete names, entry types, and file contents."""
    digest = hashlib.sha256()

    def add(value: bytes) -> None:
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)

    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        directories.sort()
        files.sort()
        for name in directories:
            path = current_path / name
            relative = path.relative_to(root).as_posix().encode("utf-8", "surrogateescape")
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                add(b"L")
                add(relative)
                add(os.readlink(path).encode("utf-8", "surrogateescape"))
            else:
                add(b"D")
                add(relative)
        for name in files:
            path = current_path / name
            relative = path.relative_to(root).as_posix().encode("utf-8", "surrogateescape")
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                add(b"L")
                add(relative)
                add(os.readlink(path).encode("utf-8", "surrogateescape"))
                continue
            if stat.S_ISREG(metadata.st_mode):
                add(b"F")
                add(relative)
                add(metadata.st_size.to_bytes(8, "big"))
                with path.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        digest.update(chunk)
                continue
            add(b"S")
            add(relative)
            add(stat.S_IFMT(metadata.st_mode).to_bytes(4, "big"))
    return digest.hexdigest()


def installed_skill_diagnostics(
    bundled_root: Path, installation_roots: Iterable[Path]
) -> tuple[Finding, ...]:
    """Compare every bundled skill with each supplied installation root."""
    bundled_root = Path(bundled_root)
    skill_names = sorted(path.name for path in bundled_root.iterdir() if path.is_dir())
    expected = {name: _tree_digest(bundled_root / name) for name in skill_names}
    findings: list[Finding] = []

    for installation_root in installation_roots:
        installation_root = Path(installation_root)
        for name in skill_names:
            installed = installation_root / name
            if not installed.is_dir():
                findings.append(
                    Finding("error", "installed_skill_missing", str(installation_root), name)
                )
                continue
            if installed.is_symlink():
                findings.append(
                    Finding("error", "installed_skill_drift", str(installation_root), name)
                )
                continue
            try:
                actual = _tree_digest(installed)
            except OSError:
                findings.append(
                    Finding("error", "installed_skill_unreadable", str(installation_root), name)
                )
                continue
            if actual != expected[name]:
                findings.append(
                    Finding("error", "installed_skill_drift", str(installation_root), name)
                )
    return tuple(findings)


def _run_git(project: Path, *arguments: str) -> tuple[str | None, Finding | None]:
    """Run a read-only Git query without repository fsmonitor execution.

    The Git executable selected by PATH and configuration unrelated to fsmonitor
    remain part of the caller's local trust boundary.
    """
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *arguments],
            cwd=project,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            check=False,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )
    except (OSError, subprocess.SubprocessError):
        return None, Finding(
            "error", "git_command_error", project.name, f"git {' '.join(arguments)} failed"
        )
    if result.returncode:
        return None, Finding(
            "error", "git_command_error", project.name, f"git {' '.join(arguments)} failed"
        )
    return result.stdout, None


def _is_contained(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        return False
    return True


def _load_json_object(path: Path) -> dict | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _selected_state_path(engineering_root: Path) -> tuple[Path | None, Finding | None]:
    pointer_path = engineering_root / "current.json"
    if pointer_path.is_symlink():
        return None, Finding(
            "error", "lifecycle_pointer_malformed", engineering_root.parent.name,
            ".eng-level/current.json must be a contained regular file",
        )
    if not pointer_path.exists():
        return None, None
    if not _is_contained(pointer_path, engineering_root):
        return None, Finding(
            "error", "lifecycle_pointer_malformed", engineering_root.parent.name,
            ".eng-level/current.json must be a contained regular file",
        )
    pointer = _load_json_object(pointer_path)
    if pointer is None:
        return None, Finding(
            "error", "lifecycle_pointer_malformed", engineering_root.parent.name,
            ".eng-level/current.json is not valid JSON metadata",
        )

    candidate: Path | None = None
    if isinstance(pointer.get("state_path"), str):
        candidate = engineering_root / pointer["state_path"]
    elif isinstance(pointer.get("artifact_root"), str):
        candidate = engineering_root / pointer["artifact_root"] / "state.json"
    elif isinstance(pointer.get("run_id"), str):
        candidate = engineering_root / "runs" / pointer["run_id"] / "state.json"

    if candidate is None or not _is_contained(candidate, engineering_root) or not candidate.is_file():
        return None, Finding(
            "error", "lifecycle_pointer_malformed", engineering_root.parent.name,
            ".eng-level/current.json does not select a contained state file",
        )
    return candidate, None


def _state_metadata(project: Path) -> tuple[dict | None, tuple[Finding, ...]]:
    engineering_root = project / ".eng-level"
    if not engineering_root.is_dir():
        return None, ()
    if engineering_root.is_symlink():
        return None, (
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                ".eng-level must be a contained directory",
            ),
        )

    selected, pointer_finding = _selected_state_path(engineering_root)
    findings = [pointer_finding] if pointer_finding else []
    candidates = [selected] if selected is not None else []
    legacy = engineering_root / "state.json"
    legacy_is_safe = (
        legacy.is_file() and not legacy.is_symlink() and _is_contained(legacy, engineering_root)
    )
    if (legacy.exists() or legacy.is_symlink()) and not legacy_is_safe:
        findings.append(
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                "legacy lifecycle state must be a contained regular file",
            )
        )
    if selected is None and legacy_is_safe:
        candidates.append(legacy)
    if not candidates:
        return None, tuple(findings)

    state = _load_json_object(candidates[0])
    if state is None or not isinstance(state.get("initiative"), str) or not isinstance(
        state.get("state"), str
    ):
        findings.append(
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                "selected lifecycle state is not valid top-level JSON metadata",
            )
        )
        state = None
    if state is None:
        return None, tuple(findings)
    return {key: state[key] for key in _STATE_FIELDS if key in state}, tuple(findings)


def _project_diagnostics(project: Path) -> tuple[Finding, ...]:
    findings: list[Finding] = []
    if not (project / "AGENTS.md").is_file():
        findings.append(
            Finding("warning", "root_agents_missing", project.name, "root AGENTS.md is missing")
        )
    if not (project / "CLAUDE.md").is_file():
        findings.append(
            Finding("warning", "root_claude_missing", project.name, "root CLAUDE.md is missing")
        )

    porcelain, git_error = _run_git(
        project, "status", "--porcelain", "--untracked-files=no"
    )
    if git_error:
        findings.append(git_error)
    elif porcelain is not None:
        conflicts = sorted(
            {line[:2] for line in porcelain.splitlines() if len(line) >= 2 and line[:2] in _CONFLICT_CODES}
        )
        if conflicts:
            findings.append(
                Finding(
                    "error", "git_conflict", project.name,
                    f"unresolved Git index status: {', '.join(conflicts)}",
                )
            )

    branch_output, branch_error = _run_git(project, "branch", "--show-current")
    if branch_error:
        findings.append(branch_error)
        actual_branch = None
    else:
        actual_branch = branch_output.strip() if branch_output else None

    state, state_findings = _state_metadata(project)
    findings.extend(state_findings)
    if state is not None and branch_error is None:
        recorded_branch = (
            state["branch"] if "branch" in state else state.get("base_branch")
        )
        if isinstance(recorded_branch, str) and recorded_branch and recorded_branch != actual_branch:
            findings.append(
                Finding(
                    "error", "branch_mismatch", project.name,
                    f"recorded branch {recorded_branch!r} differs from current branch {actual_branch!r}",
                )
            )
    return tuple(findings)


def portfolio_diagnostics(portfolio_root: Path) -> tuple[Finding, ...]:
    """Scan only direct-child Git repositories without changing them."""
    portfolio_root = Path(portfolio_root)
    try:
        children = sorted(
            (path for path in portfolio_root.iterdir() if path.is_dir()), key=lambda path: path.name
        )
    except OSError:
        return (
            Finding(
                "error", "portfolio_unreadable", str(portfolio_root),
                "portfolio root cannot be enumerated",
            ),
        )

    findings: list[Finding] = []
    for project in children:
        if not (project / ".git").exists():
            continue
        findings.extend(_project_diagnostics(project))
    return tuple(findings)
