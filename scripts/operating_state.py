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
import threading
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
_STALE_CODES = {
    "branch_mismatch", "commit_mismatch", "base_commit_mismatch",
    "base_commit_missing", "implementation_head_mismatch",
    "implementation_head_missing",
}
_UNSAFE_CODES = {
    "selector_malformed", "lifecycle_state_malformed", "git_command_error"
}
_SELECTOR_MAX_BYTES = 1024 * 1024
_STATE_MAX_BYTES = 4 * 1024 * 1024
_GIT_OUTPUT_MAX_BYTES = 1024 * 1024
_MAX_BLOCKERS = 100
_MAX_BLOCKER_LENGTH = 4096
_FROZEN_IMPLEMENTATION_STATES = {"REVIEW_READY", "REVIEW_PASSED", "SHIP_READY"}


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


def _run_git_process(
    project: Path, *arguments: str
) -> tuple[str | None, int | None, Finding | None]:
    """Run a read-only Git query without repository fsmonitor execution.

    The Git executable selected by PATH and configuration unrelated to fsmonitor
    remain part of the caller's local trust boundary.
    """
    command = ["git", "-c", "core.fsmonitor=false", *arguments]
    try:
        process = subprocess.Popen(
            command,
            cwd=project,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )
        captured = bytearray()
        overflow = threading.Event()

        def collect_stdout() -> None:
            assert process.stdout is not None
            while len(captured) <= _GIT_OUTPUT_MAX_BYTES:
                remaining = _GIT_OUTPUT_MAX_BYTES + 1 - len(captured)
                chunk = process.stdout.read(min(64 * 1024, remaining))
                if not chunk:
                    return
                captured.extend(chunk)
            overflow.set()
            try:
                process.kill()
            except OSError:
                pass

        collector = threading.Thread(target=collect_stdout, daemon=True)
        collector.start()
        try:
            returncode = process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            collector.join()
            if process.stdout is not None:
                process.stdout.close()
            return None, None, Finding(
                "error", "git_command_error", project.name,
                f"git {' '.join(arguments)} failed",
            )
        collector.join()
        if process.stdout is not None:
            process.stdout.close()
        if overflow.is_set() or len(captured) > _GIT_OUTPUT_MAX_BYTES:
            return None, None, Finding(
                "error", "git_command_error", project.name,
                f"git {' '.join(arguments)} exceeded safe output limit",
            )
        output = captured.decode("utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        return None, None, Finding(
            "error", "git_command_error", project.name, f"git {' '.join(arguments)} failed"
        )
    return output, returncode, None


def _run_git(project: Path, *arguments: str) -> tuple[str | None, Finding | None]:
    output, returncode, finding = _run_git_process(project, *arguments)
    if finding is not None:
        return None, finding
    if returncode:
        return None, Finding(
            "error", "git_command_error", project.name, f"git {' '.join(arguments)} failed"
        )
    return output, None


def _is_contained(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        return False
    return True


def _load_json_object(path: Path, max_bytes: int = _SELECTOR_MAX_BYTES) -> dict | None:
    try:
        metadata = path.lstat()
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > max_bytes:
            return None
        with path.open("rb") as stream:
            raw = stream.read(max_bytes + 1)
        if len(raw) > max_bytes:
            return None
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _is_canonical_run_id(run_id: object) -> bool:
    return bool(
        isinstance(run_id, str)
        and len(run_id) <= 255
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
    if isinstance(pointer.get("state_path"), str) and len(pointer["state_path"]) <= 4096:
        relative = Path(pointer["state_path"])
        if not relative.is_absolute():
            candidate = (
                project / relative
                if relative.parts and relative.parts[0] == namespace
                else lifecycle_root / relative
            )
    elif isinstance(pointer.get("artifact_root"), str) and len(pointer["artifact_root"]) <= 4096:
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
        if not isinstance(value, str) or len(value) > 4096 or Path(value).is_absolute():
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


def _is_string(value: object, maximum: int, *, allow_empty: bool = True) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) <= maximum
        and (allow_empty or value)
    )


def _is_nullable_string(
    value: object, maximum: int, *, allow_empty: bool = True
) -> bool:
    return value is None or _is_string(value, maximum, allow_empty=allow_empty)


def _is_blocker_list(value: object) -> bool:
    return bool(
        isinstance(value, list)
        and len(value) <= _MAX_BLOCKERS
        and all(_is_string(item, _MAX_BLOCKER_LENGTH) for item in value)
    )


def _valid_operating_state(state: dict, state_path: Path, selected: Path | None) -> bool:
    if not _is_string(state.get("initiative"), 512, allow_empty=False):
        return False
    if not _is_string(state.get("state"), 128, allow_empty=False):
        return False
    if "run_id" in state and not (
        _is_string(state["run_id"], 255, allow_empty=False)
        and _is_canonical_run_id(state["run_id"])
    ):
        return False
    if selected is not None and state.get("run_id") != selected.parent.name:
        return False
    for key in ("branch", "base_branch"):
        if key in state and not _is_nullable_string(
            state[key], 1024, allow_empty=False
        ):
            return False
    for key in ("commit", "base_commit", "implementation_head"):
        if key in state and not _is_nullable_string(state[key], 128, allow_empty=False):
            return False
    if "stop_after" in state and state["stop_after"] not in {None, *_STOP_BOUNDARIES}:
        return False
    if "artifact_root" in state and not _is_string(
        state["artifact_root"], 4096, allow_empty=False
    ):
        return False
    if "next_action" in state and not _is_string(state["next_action"], 4096):
        return False
    if "upstream_approval_status" in state and state["upstream_approval_status"] not in {
        "PENDING", "APPROVED", "REJECTED", "REOPENED"
    }:
        return False
    for key in ("blockers", "open_blockers"):
        if key in state and not _is_blocker_list(state[key]):
            return False

    artifact_root = state.get("artifact_root")
    if artifact_root:
        artifact_path = Path(artifact_root)
        project = state_path.parents[3] if selected else state_path.parent.parent
        artifact_candidate = project / artifact_path
        if (
            artifact_path.is_absolute()
            or not _is_contained(artifact_candidate, project)
            or artifact_candidate.resolve() != state_path.parent.resolve()
        ):
            return False
    return True


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

    state = _load_json_object(state_path, _STATE_MAX_BYTES)
    if state is None or not _valid_operating_state(state, state_path, selected):
        findings.append(
            Finding(
                "error", "lifecycle_state_malformed", project.name,
                "selected lifecycle state is malformed or unreadable",
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
        frozen_implementation = state["state"] in _FROZEN_IMPLEMENTATION_STATES
        recorded_branch = state.get("branch")
        if not recorded_branch:
            findings.append(
                Finding(
                    "warning", "branch_lineage_unknown", project.name,
                    "current branch lineage was not recorded",
                )
            )
        elif recorded_branch != git_branch:
            findings.append(
                Finding(
                    "error", "branch_mismatch", project.name,
                    f"recorded branch {recorded_branch!r} differs from current branch {git_branch!r}",
                )
            )
        for field, code, label in (
            ("commit", "commit_mismatch", "lifecycle commit"),
            ("base_commit", "base_commit_mismatch", "base commit"),
        ):
            revision = state.get(field)
            if revision is not None:
                reachable, lineage_error = _git_commit_reachable(project, revision, git_head)
                if lineage_error is not None:
                    findings.append(lineage_error)
                elif not reachable:
                    findings.append(
                        Finding(
                            "error", code, project.name,
                            f"recorded {label} is not a commit reachable from current HEAD",
                        )
                    )
        implementation_head = state.get("implementation_head")
        if frozen_implementation and state.get("base_commit") is None:
            findings.append(
                Finding(
                    "error", "base_commit_missing", project.name,
                    "frozen review state has no recorded base commit",
                )
            )
        if frozen_implementation and implementation_head is None:
            findings.append(
                Finding(
                    "error", "implementation_head_missing", project.name,
                    "frozen review state has no recorded implementation HEAD",
                )
            )
        # BLOCKED is phase-ambiguous and does not inherit a frozen review snapshot.
        if (
            frozen_implementation
            and implementation_head is not None
            and implementation_head != git_head
        ):
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


def _git_commit_reachable(
    project: Path, revision: str, head: str | None
) -> tuple[bool, Finding | None]:
    if head is None or not re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", revision):
        return False, None
    _, object_status, object_error = _run_git_process(
        project, "cat-file", "-e", f"{revision}^{{commit}}"
    )
    if object_error is not None:
        return False, object_error
    if object_status != 0:
        return False, None
    _, ancestor_status, ancestor_error = _run_git_process(
        project, "merge-base", "--is-ancestor", revision, head
    )
    if ancestor_error is not None:
        return False, ancestor_error
    if ancestor_status == 0:
        return True, None
    if ancestor_status == 1:
        return False, None
    return False, Finding(
        "error", "git_command_error", project.name,
        "git merge-base --is-ancestor failed",
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
    blockers = (state.get("blockers") or []) + (state.get("open_blockers") or [])
    if blockers or lifecycle_state == "BLOCKED":
        return "resolve open blockers", 1
    if lifecycle_state not in _STATE_RANKS:
        return "reconcile lifecycle state", 1
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
        recorded_branch = state.get("branch")
        if not isinstance(recorded_branch, str) or not recorded_branch:
            findings.append(
                Finding(
                    "warning", "branch_lineage_unknown", project.name,
                    "current branch lineage was not recorded",
                )
            )
        elif recorded_branch != actual_branch:
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
