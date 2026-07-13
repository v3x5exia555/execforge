#!/usr/bin/env python3
"""Read-only operating-state diagnostics for ExecForge."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from typing import Iterable, NamedTuple


class Finding(NamedTuple):
    """An immutable, content-safe diagnostic result."""

    severity: str
    code: str
    project: str
    detail: str


class OperatingSnapshot(NamedTuple):
    """Safe, read-only lifecycle and Git metadata for resume decisions."""

    project: Path
    state_path: Path | None
    state: dict | None
    git_branch: str | None
    git_head: str | None
    backlog_count: int | None
    findings: tuple[Finding, ...]


_CONFLICT_CODES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
_STATE_FIELDS = {"initiative", "state", "branch", "base_branch", "run_id"}
_STOP_BOUNDARIES = {"product": 1, "plan": 2, "implement": 3, "review": 4, "qa": 5}
_STATE_RANKS = {
    "NO_CONTEXT": 0,
    "UPSTREAM_INTAKE": 0,
    "UPSTREAM_APPROVAL_REQUIRED": 0,
    "RETURN_TO_PRODUCT_PLAN": 0,
    "PLAN_REQUIRED": 1,
    "RETURN_TO_PLAN": 1,
    "PLAN_APPROVED": 2,
    "WAITING_FOR_IMPLEMENTATION": 2,
    "IMPLEMENTATION_IN_PROGRESS": 2,
    "RETURN_TO_IMPLEMENTATION": 2,
    "REVIEW_READY": 3,
    "REVIEW_PASSED": 4,
    "SHIP_READY": 5,
}
_STALE_CODES = {"branch_mismatch", "commit_mismatch", "implementation_head_mismatch"}
_UNSAFE_CODES = {
    "selector_malformed", "lifecycle_state_malformed", "git_command_error"
}


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


def _is_canonical_run_id(run_id: object) -> bool:
    return bool(
        isinstance(run_id, str)
        and run_id not in {".", ".."}
        and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", run_id)
        and "/" not in run_id
        and "\\" not in run_id
    )


def _selected_state_path(lifecycle_root: Path) -> tuple[Path | None, Finding | None]:
    """Resolve a current pointer without permitting paths outside the repository.

    New pointers use repository-relative paths. The older run_id-only and
    lifecycle-root-relative selector forms remain readable for diagnostics.
    """
    pointer_path = lifecycle_root / "current.json"
    namespace = lifecycle_root.name
    project = lifecycle_root.parent
    runs_root = lifecycle_root / "runs"
    project_resolved = project.resolve()
    for selected_namespace in (".execforge", ".eng-level", ".q-level"):
        root = project / selected_namespace
        if root.is_symlink() or (
            root.exists() and root.resolve() != project_resolved / selected_namespace
        ):
            return None, Finding(
                "error", "lifecycle_pointer_malformed", project.name,
                f"{selected_namespace} must be a contained real directory",
            )
    authoritative = project / ".execforge" / "current.json"
    if authoritative.exists() or authoritative.is_symlink():
        selected = _authoritative_state_path(project, namespace)
        if selected is not None:
            return selected, None
        return None, Finding(
            "error", "lifecycle_pointer_malformed", project.name,
            ".execforge/current.json does not select aligned contained state files",
        )
    if lifecycle_root.is_symlink() or runs_root.is_symlink() or pointer_path.is_symlink():
        return None, Finding(
            "error", "lifecycle_pointer_malformed", project.name,
            f"{namespace}/current.json must be a contained regular file",
        )
    if not pointer_path.exists():
        return None, None
    if not _is_contained(pointer_path, lifecycle_root):
        return None, Finding(
            "error", "lifecycle_pointer_malformed", project.name,
            f"{namespace}/current.json must be a contained regular file",
        )
    pointer = _load_json_object(pointer_path)
    if pointer is None:
        return None, Finding(
            "error", "lifecycle_pointer_malformed", project.name,
            f"{namespace}/current.json is not valid JSON metadata",
        )

    candidate: Path | None = None
    if isinstance(pointer.get("state_path"), str):
        relative = Path(pointer["state_path"])
        if not relative.is_absolute():
            candidate = (
                project / relative
                if relative.parts and relative.parts[0] == namespace
                else lifecycle_root / relative
            )
    elif isinstance(pointer.get("artifact_root"), str):
        relative = Path(pointer["artifact_root"])
        if not relative.is_absolute():
            artifact_root = (
                project / relative
                if relative.parts and relative.parts[0] == namespace
                else lifecycle_root / relative
            )
            candidate = artifact_root / "state.json"
    elif isinstance(pointer.get("run_id"), str):
        run_id = pointer["run_id"]
        if _is_canonical_run_id(run_id):
            candidate = lifecycle_root / "runs" / run_id / "state.json"

    run_id = pointer.get("run_id")
    expected = (
        lifecycle_root / "runs" / run_id / "state.json"
        if _is_canonical_run_id(run_id)
        else None
    )
    selectors_disagree = expected is not None and candidate is not None and candidate != expected
    candidate_run = candidate.parent if candidate is not None else None
    candidate_layout_invalid = (
        candidate is None
        or candidate.name != "state.json"
        or candidate.is_symlink()
        or candidate_run is None
        or candidate_run.is_symlink()
        or not _is_canonical_run_id(candidate_run.name)
        or candidate_run.parent != runs_root
    )
    if (
        candidate_layout_invalid
        or selectors_disagree
        or not _is_contained(candidate, lifecycle_root)
        or not candidate.is_file()
    ):
        return None, Finding(
            "error", "lifecycle_pointer_malformed", project.name,
            f"{namespace}/current.json does not select a contained state file",
        )
    return candidate, None


def _authoritative_state_path(project: Path, namespace: str) -> Path | None:
    pointer_path = project / ".execforge" / "current.json"
    if pointer_path.is_symlink() or not _is_contained(pointer_path, project):
        return None
    pointer = _load_json_object(pointer_path)
    if pointer is None or not _is_canonical_run_id(pointer.get("run_id")):
        return None
    run_id = pointer["run_id"]
    candidates: dict[str, Path] = {}
    for selected_namespace, field in (
        (".eng-level", "eng_state_path"),
        (".q-level", "qa_state_path"),
    ):
        value = pointer.get(field)
        if not isinstance(value, str) or Path(value).is_absolute():
            return None
        candidate = project / value
        expected = project / selected_namespace / "runs" / run_id / "state.json"
        if (
            candidate != expected
            or candidate.is_symlink()
            or candidate.parent.is_symlink()
            or candidate.parent.parent.is_symlink()
            or not candidate.is_file()
            or not _is_contained(candidate, project / selected_namespace)
        ):
            return None
        candidates[selected_namespace] = candidate
    return candidates.get(namespace)


def selected_or_legacy_state_path(lifecycle_root: Path) -> Path | None:
    """Select current state, falling back only when its pointer is absent or invalid."""
    selected, _ = _selected_state_path(lifecycle_root)
    if selected is not None:
        return selected
    legacy = lifecycle_root / "state.json"
    if legacy.is_file() and not legacy.is_symlink() and _is_contained(legacy, lifecycle_root):
        return legacy
    return None


def _safe_operating_state(project: Path) -> tuple[Path | None, dict | None, list[Finding]]:
    engineering_root = project / ".eng-level"
    selected, pointer_finding = _selected_state_path(engineering_root)
    findings: list[Finding] = []
    if pointer_finding is not None:
        findings.append(
            Finding(
                "error", "selector_malformed", project.name,
                "authoritative lifecycle selector is malformed or unsafe",
            )
        )

    state_path = selected
    legacy = engineering_root / "state.json"
    if (
        state_path is None
        and not engineering_root.is_symlink()
        and engineering_root.is_dir()
        and engineering_root.resolve() == project.resolve() / ".eng-level"
        and legacy.is_file()
        and not legacy.is_symlink()
        and _is_contained(legacy, engineering_root)
    ):
        state_path = legacy
    if state_path is None:
        findings.append(
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                "no safe readable engineering lifecycle state was found",
            )
        )
        return None, None, findings

    state = _load_json_object(state_path)
    if state is None or not isinstance(state.get("initiative"), str) or not isinstance(
        state.get("state"), str
    ):
        findings.append(
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                "selected lifecycle state is malformed or unreadable",
            )
        )
        return state_path, None, findings

    nullable_strings = (
        "run_id", "branch", "base_branch", "commit", "implementation_head",
        "artifact_root", "next_action", "stop_after", "upstream_approval_status",
    )
    malformed = any(
        key in state and state[key] is not None and not isinstance(state[key], str)
        for key in nullable_strings
    )
    malformed = malformed or (
        "open_blockers" in state and not isinstance(state["open_blockers"], list)
    )
    stop_after = state.get("stop_after")
    malformed = malformed or (
        stop_after is not None and stop_after not in _STOP_BOUNDARIES
    )
    if selected is not None and "run_id" in state:
        malformed = malformed or state["run_id"] != selected.parent.name
    artifact_root = state.get("artifact_root")
    if artifact_root:
        artifact_path = Path(artifact_root)
        artifact_candidate = project / artifact_path
        malformed = (
            malformed
            or artifact_path.is_absolute()
            or not _is_contained(artifact_candidate, project)
            or artifact_candidate.resolve() != state_path.parent.resolve()
        )
    if malformed:
        findings.append(
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                "selected lifecycle state metadata is malformed or unsafe",
            )
        )
        return state_path, None, findings
    return state_path, state, findings


def _backlog_count(backlog: Path) -> int | None:
    if not backlog.is_file() or backlog.is_symlink():
        return None
    try:
        lines = backlog.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return None
    count = 0
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("|---"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0] not in {"", "#"} and any(cells[1:2]):
            count += 1
    return count


def operating_snapshot(project: Path) -> OperatingSnapshot:
    """Read the selected lifecycle state and reconcile it with read-only Git queries."""
    project = Path(project)
    state_path, state, findings = _safe_operating_state(project)

    porcelain, status_error = _run_git(project, "status", "--porcelain", "--untracked-files=all")
    if status_error is not None:
        findings.append(status_error)
    elif porcelain:
        conflicts = sorted(
            {line[:2] for line in porcelain.splitlines() if line[:2] in _CONFLICT_CODES}
        )
        if conflicts:
            findings.append(
                Finding(
                    "error", "git_conflict", project.name,
                    f"unresolved Git index status: {', '.join(conflicts)}",
                )
            )
        findings.append(
            Finding("warning", "dirty_worktree", project.name, "Git worktree has changes")
        )

    branch_output, branch_error = _run_git(project, "branch", "--show-current")
    head_output, head_error = _run_git(project, "rev-parse", "HEAD")
    for error in (branch_error, head_error):
        if error is not None:
            findings.append(error)
    git_branch = branch_output.strip() if branch_output and branch_output.strip() else None
    git_head = head_output.strip() if head_output and head_output.strip() else None

    if state is not None:
        recorded_branch = state.get("branch") if "branch" in state else state.get("base_branch")
        if recorded_branch and recorded_branch != git_branch:
            findings.append(
                Finding(
                    "error", "branch_mismatch", project.name,
                    f"recorded branch {recorded_branch!r} differs from current branch {git_branch!r}",
                )
            )
        recorded_commit = state.get("commit")
        if recorded_commit and recorded_commit != git_head:
            findings.append(
                Finding(
                    "error", "commit_mismatch", project.name,
                    "recorded lifecycle commit differs from current HEAD",
                )
            )
        implementation_head = state.get("implementation_head")
        if implementation_head and implementation_head != git_head:
            findings.append(
                Finding(
                    "error", "implementation_head_mismatch", project.name,
                    "recorded implementation HEAD differs from current HEAD",
                )
            )

    backlog_count = _backlog_count(state_path.parent / "backlog.md") if state_path else None
    if state_path is not None and backlog_count is None:
        findings.append(
            Finding("warning", "backlog_unreadable", project.name, "backlog summary is unreadable")
        )
    return OperatingSnapshot(
        project, state_path, state, git_branch, git_head, backlog_count, tuple(findings)
    )


def deterministic_next(snapshot: OperatingSnapshot) -> tuple[str, int]:
    """Return one deterministic action and its CLI exit status."""
    codes = {finding.code for finding in snapshot.findings}
    if "git_conflict" in codes:
        return "resolve Git conflicts", 1
    if snapshot.state is None or codes & _UNSAFE_CODES:
        return "reconcile unreadable or unsafe lifecycle state", 1
    if codes & _STALE_CODES:
        return "reconcile stale lifecycle state", 1

    state = snapshot.state
    lifecycle_state = state["state"]
    blockers = state.get("open_blockers") or []
    if blockers or lifecycle_state == "BLOCKED":
        return "resolve open blockers", 1
    if lifecycle_state not in _STATE_RANKS:
        return "reconcile lifecycle state", 0
    if lifecycle_state in {"NO_CONTEXT", "UPSTREAM_INTAKE", "RETURN_TO_PRODUCT_PLAN"}:
        return "capture upstream context", 0
    if lifecycle_state == "UPSTREAM_APPROVAL_REQUIRED" or state.get(
        "upstream_approval_status"
    ) not in {None, "APPROVED"}:
        return "request upstream approval", 0

    rank = _STATE_RANKS.get(lifecycle_state)
    stop_after = state.get("stop_after")
    if stop_after is not None and rank is not None and rank >= _STOP_BOUNDARIES[stop_after]:
        return f"await explicit user instruction (stop_after: {stop_after} reached)", 0

    actions = {
        "PLAN_REQUIRED": "create or revise engineering plan",
        "RETURN_TO_PLAN": "create or revise engineering plan",
        "PLAN_APPROVED": "implement approved plan",
        "WAITING_FOR_IMPLEMENTATION": "implement approved plan",
        "IMPLEMENTATION_IN_PROGRESS": "complete or fix implementation",
        "RETURN_TO_IMPLEMENTATION": "complete or fix implementation",
        "REVIEW_READY": "run Staff Engineer review",
        "REVIEW_PASSED": "run q-level --mode=auto",
        "SHIP_READY": "prepare ship-ready handoff",
    }
    return actions.get(lifecycle_state, "reconcile lifecycle state"), 0


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
