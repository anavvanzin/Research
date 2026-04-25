#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
BASE_DIR = REPO_ROOT / ".claude" / "self-improving-agent"
MEMORY_DIR = BASE_DIR / "memory"
SCHEMA_PATH = MEMORY_DIR / "semantic-patterns.schema.json"
SEMANTIC_PATH = MEMORY_DIR / "semantic-patterns.json"
EPISODIC_DIR = MEMORY_DIR / "episodic"
WORKING_DIR = MEMORY_DIR / "working"
CURRENT_SESSION_PATH = WORKING_DIR / "current_session.json"
LAST_ERROR_PATH = WORKING_DIR / "last_error.json"
SESSION_END_PATH = WORKING_DIR / "session_end.json"
MAX_TEXT = 4000
MAX_EVENTS = 200
ISSUE_THRESHOLD_DEFAULT = 3
ISSUE_LABEL = "self-improving-agent"
SCHEMA_VERSION = "1.1"


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def trim_text(value: str | None, limit: int = MAX_TEXT) -> str:
    if not value:
        return ""
    normalized = value.strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, data: Any) -> None:
    """Write JSON atomically via tempfile + os.replace.

    Avoids the read-modify-write race flagged in the 2026-04-21 security review:
    pre-tool and post-bash hooks can fire concurrently and a plain write_text
    would let the second writer overwrite the first's changes mid-cycle.
    os.replace is atomic on POSIX.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=True) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    os.replace(tmp, path)


def run_command(args: list[str], timeout: int = 8) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 1, "", ""
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def github_name_from_remote(remote: str) -> str | None:
    if not remote:
        return None
    match = re.search(
        r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote
    )
    if not match:
        return None
    return f"{match.group('owner')}/{match.group('repo')}"


def get_repo_info() -> dict[str, Any]:
    repo: dict[str, Any] = {
        "root": str(REPO_ROOT),
        "nameWithOwner": None,
        "url": None,
        "defaultBranch": None,
        "branch": None,
        "commit": None,
        "origin": None,
    }

    _, branch, _ = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    _, commit, _ = run_command(["git", "rev-parse", "HEAD"])
    _, origin, _ = run_command(["git", "remote", "get-url", "origin"])
    repo["branch"] = branch or None
    repo["commit"] = commit or None
    repo["origin"] = origin or None

    if shutil.which("gh"):
        code, stdout, _ = run_command(
            ["gh", "repo", "view", "--json", "nameWithOwner,url,defaultBranchRef"]
        )
        if code == 0 and stdout:
            try:
                parsed = json.loads(stdout)
                repo["nameWithOwner"] = parsed.get("nameWithOwner")
                repo["url"] = parsed.get("url")
                default_branch = parsed.get("defaultBranchRef") or {}
                repo["defaultBranch"] = default_branch.get("name")
                return repo
            except json.JSONDecodeError:
                pass

    repo["nameWithOwner"] = github_name_from_remote(origin)
    if origin:
        repo["url"] = origin.replace(
            "git@github.com:", "https://github.com/"
        ).removesuffix(".git")
    return repo


def default_semantic(repo: dict[str, Any] | None = None) -> dict[str, Any]:
    repo_info = repo or get_repo_info()
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "repo": {
            "nameWithOwner": repo_info.get("nameWithOwner"),
            "url": repo_info.get("url"),
            "defaultBranch": repo_info.get("defaultBranch"),
        },
        "patterns": {},
    }


def default_session(repo: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "started_at": utc_now(),
        "repo": repo or get_repo_info(),
        "events": [],
        "stats": {
            "pre_tool_calls": 0,
            "post_bash_calls": 0,
            "successes": 0,
            "errors": 0,
        },
    }


def migrate_semantic(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") in (None, "1.0"):
        data["schema_version"] = SCHEMA_VERSION
        for _key, pat in data.get("patterns", {}).items():
            if isinstance(pat, dict):
                pat.setdefault("contradicts", None)
                pat.setdefault("supersedes", None)
                pat.setdefault("github_issue", None)
                pat.setdefault("quality_rules", [])
                pat.setdefault("recovery_hints", [])
    return data


def validate_semantic(
    data: dict[str, Any], schema: dict[str, Any] | None = None
) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("Root must be an object")
        return errors
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be '{SCHEMA_VERSION}', got {data.get('schema_version')!r}"
        )
    if "generated_at" not in data:
        errors.append("Missing required field: generated_at")
    if "patterns" not in data:
        errors.append("Missing required field: patterns")
    if not isinstance(data.get("patterns"), dict):
        errors.append("patterns must be an object")
        return errors
    for key, pat in data["patterns"].items():
        if not isinstance(pat, dict):
            errors.append(f"Pattern '{key}' must be an object")
            continue
        for req in (
            "id",
            "name",
            "source",
            "confidence",
            "applications",
            "created",
            "last_seen",
            "category",
            "pattern",
            "problem",
            "solution",
            "target_skills",
        ):
            if req not in pat:
                errors.append(f"Pattern '{key}' missing required field: {req}")
        conf = pat.get("confidence")
        if conf is not None and not (
            isinstance(conf, (int, float)) and 0.0 <= conf <= 1.0
        ):
            errors.append(f"Pattern '{key}' confidence must be 0-1, got {conf!r}")
        apps = pat.get("applications")
        if apps is not None and not (isinstance(apps, int) and apps >= 0):
            errors.append(
                f"Pattern '{key}' applications must be non-negative int, got {apps!r}"
            )
    if schema and isinstance(schema, dict):
        try:
            import jsonschema

            jsonschema.validate(instance=data, schema=schema)
        except ImportError:
            pass
        except jsonschema.ValidationError as exc:
            errors.append(f"jsonschema: {exc.message}")
    return errors


def ensure_layout() -> None:
    EPISODIC_DIR.mkdir(parents=True, exist_ok=True)
    WORKING_DIR.mkdir(parents=True, exist_ok=True)
    if not SEMANTIC_PATH.exists():
        write_json(SEMANTIC_PATH, default_semantic())
    else:
        existing = read_json(SEMANTIC_PATH, {})
        migrated = migrate_semantic(existing)
        if migrated != existing:
            write_json(SEMANTIC_PATH, migrated)


def classify_failure(output: str, exit_code: int) -> str:
    text = output.lower()
    if "permission denied" in text or "authentication" in text or "forbidden" in text:
        return "auth_or_permissions"
    if "not found" in text or "no such file" in text or exit_code == 127:
        return "environment_or_path"
    if "syntax error" in text or "unexpected token" in text:
        return "syntax"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if "rate limit" in text or "502" in text or "503" in text or "504" in text:
        return "external_api"
    return "logic_or_unknown"


def next_episode_id() -> str:
    return "ep-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def episode_path(timestamp: str) -> Path:
    year = timestamp[:4]
    dated_dir = EPISODIC_DIR / year
    dated_dir.mkdir(parents=True, exist_ok=True)
    stamp = timestamp.replace(":", "").replace("-", "")
    return dated_dir / f"{stamp}-bash.json"


def meaningful_line(output: str, fallback: str) -> str:
    for line in output.splitlines():
        if line.strip():
            return trim_text(line, 240)
    return fallback


def maybe_get_copilot_hint(
    command: str, output: str, exit_code: int, repo: dict[str, Any]
) -> str | None:
    if os.environ.get("SELF_IMPROVING_USE_COPILOT", "").lower() not in {
        "1",
        "true",
        "yes",
    }:
        return None
    if not shutil.which("gh"):
        return None

    prompt = (
        "Summarize this shell failure in at most three short bullets. "
        "Focus on reusable prevention advice for the repository automation.\n\n"
        f"Repo: {repo.get('nameWithOwner') or repo.get('root')}\n"
        f"Branch: {repo.get('branch')}\n"
        f"Command: {trim_text(command, 500)}\n"
        f"Exit code: {exit_code}\n"
        f"Output: {trim_text(output, 1200)}"
    )
    code, stdout, _ = run_command(["gh", "copilot", "-p", prompt], timeout=20)
    if code != 0 or not stdout:
        return None
    return trim_text(stdout, 1200)


def create_github_issue(
    pattern_key: str, record: dict[str, Any], repo: dict[str, Any]
) -> int | None:
    if not shutil.which("gh"):
        return None
    name_with_owner = repo.get("nameWithOwner")
    if not name_with_owner:
        return None
    if record.get("github_issue") is not None:
        return record["github_issue"]
    title = (
        f"[self-improving-agent] Repeated failure: {record.get('name', pattern_key)}"
    )
    body_lines = [
        f"**Pattern ID**: `{pattern_key}`",
        f"**Category**: {record.get('category', 'unknown')}",
        f"**Confidence**: {record.get('confidence', 0)}",
        f"**Occurrences**: {record.get('applications', 0)}",
        f"**First seen**: {record.get('created', 'unknown')}",
        f"**Last seen**: {record.get('last_seen', 'unknown')}",
        "",
        f"**Problem**: {record.get('problem', 'N/A')}",
        "",
        f"**Pattern**: {record.get('pattern', 'N/A')}",
        "",
    ]
    solution = record.get("solution", {})
    if isinstance(solution, dict):
        hints = solution.get("recovery_hints", [])
        if hints:
            body_lines.append("**Recovery hints**:")
            for h in hints[:5]:
                body_lines.append(f"- {h}")
    body_lines.append("")
    body_lines.append("---")
    body_lines.append(
        "*Auto-created by self-improving-agent hook. Close when resolved and update `github_issue` in semantic-patterns.json.*"
    )
    body = "\n".join(body_lines)
    cmd = [
        "gh",
        "issue",
        "create",
        "--repo",
        name_with_owner,
        "--title",
        title,
        "--body",
        body,
        "--label",
        ISSUE_LABEL,
    ]
    code, stdout, stderr = run_command(cmd, timeout=30)
    if code != 0:
        print(
            f"[self-improving-agent] Failed to create issue: {stderr}", file=sys.stderr
        )
        return None
    match = re.search(r"/issues/(\d+)", stdout)
    if match:
        return int(match.group(1))
    try:
        return int(stdout.strip().split("/")[-1])
    except (ValueError, IndexError):
        return None


def update_semantic_pattern(episode: dict[str, Any]) -> None:
    semantic = read_json(SEMANTIC_PATH, default_semantic(episode.get("repo")))
    semantic = migrate_semantic(semantic)
    patterns = semantic.setdefault("patterns", {})
    details = episode.get("details", {})
    command = details.get("command", "")
    output_excerpt = details.get("output_excerpt", "")
    failure_class = details.get("classification", "logic_or_unknown")
    summary = episode.get("summary", "bash failure")
    try:
        command_prefix = " ".join(shlex.split(command)[:3])
    except ValueError:
        command_prefix = command[:80]
    raw_key = f"{failure_class}|{command_prefix}|{summary.lower()}"
    pattern_key = (
        re.sub(r"[^a-z0-9]+", "_", raw_key.lower()).strip("_")[:120] or "bash_failure"
    )

    record = patterns.get(pattern_key)
    if record is None:
        record = {
            "id": pattern_key,
            "name": f"Bash failure pattern: {summary}",
            "source": "hook_error",
            "confidence": 0.35,
            "applications": 0,
            "created": episode["timestamp"],
            "last_seen": episode["timestamp"],
            "category": "bash_failure",
            "pattern": f"Review repeated `{failure_class}` shell failures before retrying the same automation step.",
            "problem": summary,
            "solution": {
                "command_prefix": command_prefix,
                "recovery_hints": [
                    "Capture the exact failing command and first meaningful output line.",
                    "Re-check repository context and dependencies before retrying.",
                ],
            },
            "target_skills": ["self-improving-agent"],
            "contradicts": None,
            "supersedes": None,
            "github_issue": None,
            "quality_rules": [],
        }
        patterns[pattern_key] = record

    record["applications"] = int(record.get("applications", 0)) + 1
    record["confidence"] = round(
        min(0.95, 0.35 + (record["applications"] - 1) * 0.10), 2
    )
    record["last_seen"] = episode["timestamp"]
    recovery_hints = record.setdefault("solution", {}).setdefault("recovery_hints", [])
    copilot_hint = details.get("copilot_hint")
    if copilot_hint and copilot_hint not in recovery_hints:
        recovery_hints.append(copilot_hint)
    if output_excerpt and meaningful_line(output_excerpt, "") not in recovery_hints:
        recovery_hints.append(meaningful_line(output_excerpt, ""))

    threshold = int(
        os.environ.get("SELF_IMPROVING_ISSUE_THRESHOLD", str(ISSUE_THRESHOLD_DEFAULT))
    )
    if record["applications"] >= threshold and record.get("github_issue") is None:
        repo = episode.get("repo", {})
        issue_num = create_github_issue(pattern_key, record, repo)
        if issue_num is not None:
            record["github_issue"] = issue_num

    semantic["generated_at"] = utc_now()
    semantic["repo"] = {
        "nameWithOwner": episode.get("repo", {}).get("nameWithOwner"),
        "url": episode.get("repo", {}).get("url"),
        "defaultBranch": episode.get("repo", {}).get("defaultBranch"),
    }
    semantic["schema_version"] = SCHEMA_VERSION
    write_json(SEMANTIC_PATH, semantic)


def handle_pre_tool(tool_name: str, tool_input: str) -> None:
    ensure_layout()
    repo = get_repo_info()
    session = read_json(CURRENT_SESSION_PATH, default_session(repo))
    if not session.get("started_at"):
        session = default_session(repo)
    session["repo"] = repo
    event = {
        "timestamp": utc_now(),
        "phase": "before_start",
        "tool_name": tool_name,
        "tool_input": trim_text(tool_input),
    }
    events = session.setdefault("events", [])
    events.append(event)
    session["events"] = events[-MAX_EVENTS:]
    stats = session.setdefault("stats", {})
    stats["pre_tool_calls"] = int(stats.get("pre_tool_calls", 0)) + 1
    write_json(CURRENT_SESSION_PATH, session)


def handle_post_bash(tool_output: str, exit_code: int) -> None:
    ensure_layout()
    repo = get_repo_info()
    session = read_json(CURRENT_SESSION_PATH, default_session(repo))
    session["repo"] = repo
    events = session.setdefault("events", [])
    current_bash = next(
        (
            event
            for event in reversed(events)
            if event.get("tool_name") == "Bash"
            and event.get("phase") == "before_start"
            and "completed_at" not in event
        ),
        None,
    )

    timestamp = utc_now()
    status = "success" if exit_code == 0 else "error"
    command = current_bash.get("tool_input", "") if current_bash else ""
    if current_bash is not None:
        current_bash["completed_at"] = timestamp
        current_bash["exit_code"] = exit_code
        current_bash["status"] = status

    stats = session.setdefault("stats", {})
    stats["post_bash_calls"] = int(stats.get("post_bash_calls", 0)) + 1
    if status == "success":
        stats["successes"] = int(stats.get("successes", 0)) + 1
    else:
        stats["errors"] = int(stats.get("errors", 0)) + 1

    episode = {
        "schema_version": SCHEMA_VERSION,
        "id": next_episode_id(),
        "timestamp": timestamp,
        "event": "bash_complete" if status == "success" else "on_error",
        "tool_name": "Bash",
        "repo": repo,
        "status": status,
        "summary": meaningful_line(tool_output, f"Bash exited with code {exit_code}"),
        "details": {
            "command": trim_text(command, 800),
            "output_excerpt": trim_text(tool_output, 2000),
            "exit_code": exit_code,
            "classification": classify_failure(tool_output, exit_code),
        },
        "evidence_refs": [str(CURRENT_SESSION_PATH)],
    }

    if status == "error":
        copilot_hint = maybe_get_copilot_hint(command, tool_output, exit_code, repo)
        if copilot_hint:
            episode["details"]["copilot_hint"] = copilot_hint
        write_json(LAST_ERROR_PATH, episode)
        update_semantic_pattern(episode)

    write_json(episode_path(timestamp), episode)
    write_json(CURRENT_SESSION_PATH, session)


def handle_session_end() -> None:
    ensure_layout()
    repo = get_repo_info()
    session = read_json(CURRENT_SESSION_PATH, default_session(repo))
    events = session.get("events", [])
    tool_counts = Counter(event.get("tool_name", "unknown") for event in events)
    started_at = session.get("started_at")
    summary = {
        "schema_version": SCHEMA_VERSION,
        "started_at": started_at,
        "ended_at": utc_now(),
        "repo": repo,
        "counts": {
            "tools": dict(tool_counts),
            **session.get("stats", {}),
        },
        "last_error": str(LAST_ERROR_PATH) if LAST_ERROR_PATH.exists() else None,
    }
    write_json(SESSION_END_PATH, summary)
    if CURRENT_SESSION_PATH.exists():
        CURRENT_SESSION_PATH.unlink()


def handle_validate() -> None:
    ensure_layout()
    schema = read_json(SCHEMA_PATH, None)
    if schema is None:
        print(
            f"[self-improving-agent] Schema file not found: {SCHEMA_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)
    data = read_json(SEMANTIC_PATH, None)
    if data is None:
        print(
            f"[self-improving-agent] Data file not found: {SEMANTIC_PATH}",
            file=sys.stderr,
        )
        sys.exit(1)
    data = migrate_semantic(data)
    write_json(SEMANTIC_PATH, data)
    errors = validate_semantic(data, schema)
    if errors:
        print("[self-improving-agent] Validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(
            f"[self-improving-agent] Validation OK — {len(data.get('patterns', {}))} pattern(s)"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Repo-local self-improvement automation"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    pre_tool = subparsers.add_parser("pre-tool")
    pre_tool.add_argument("--tool-name", default="unknown")
    pre_tool.add_argument("--tool-input", default="")

    post_bash = subparsers.add_parser("post-bash")
    post_bash.add_argument("--tool-output", default="")
    post_bash.add_argument("--exit-code", type=int, default=0)

    subparsers.add_parser("session-end")

    subparsers.add_parser("validate")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "pre-tool":
        handle_pre_tool(args.tool_name, args.tool_input)
    elif args.command == "post-bash":
        handle_post_bash(args.tool_output, args.exit_code)
    elif args.command == "session-end":
        handle_session_end()
    elif args.command == "validate":
        handle_validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
