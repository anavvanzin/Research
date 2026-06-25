#!/usr/bin/env python3
"""git-physics-guard: enforce multi-harness ownership matrix at commit time.

Reads docs/decisions/AGENT-OWNERSHIP.md and validates that paths in
'git status --porcelain' or 'git diff --cached' belong to the active harness.

Runs as pre-commit hook (symlinked from .git/hooks/pre-commit) or manually.

Exit codes (consistent with drift-detector convention):
  0 = clean (all staged paths respect ownership; or info mode with warnings)
  1 = violations detected (enforce mode blocks commit)
  2 = script error (ownership matrix unreadable, git not available, etc.)

This script does NOT modify any file. Read-only detector.

Refs: docs/decisions/2026-06-25-multi-harness-git-physics.md
      docs/decisions/AGENT-OWNERSHIP.md
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


# --- defaults --------------------------------------------------------------

DEFAULT_OWNERSHIP_MATRIX = (
    "docs/decisions/AGENT-OWNERSHIP.md"
)
DEFAULT_HARNESS = "codex-app"


# --- parsing the ownership matrix -----------------------------------------

# Harness section starts with: "### <name> (`HARNESS_ACTIVE=<id>`)"
HARNESS_HEADER_RE = re.compile(
    r"^###\s+(?P<name>.+?)\s+\(`HARNESS_ACTIVE=(?P<id>[a-z0-9-]+)`\)",
    re.MULTILINE,
)
# Sub-produtor section starts with: "### <name> (`HARNESS_ACTIVE=<id>`)"
# (same regex; structure is identical in AGENT-OWNERSHIP.md)
# Owns column line: first "| Owns ..." header followed by separator and data rows
OWNS_HEADER_RE = re.compile(r"\|\s*Owns[^|]*\|", re.IGNORECASE)
# Cell value inside a markdown table row: split on '|' and trim
CELL_RE = re.compile(r"^\s*\|(.+?)\|\s*$")


@dataclass
class Ownership:
    """One row of the ownership matrix."""

    harness_id: str
    owns_paths: list[str] = field(default_factory=list)
    forbidden_paths: list[str] = field(default_factory=list)
    read_paths: list[str] = field(default_factory=list)
    notes: str = ""

    def owns(self, path: str) -> bool:
        """True if path matches any 'owns' glob for this harness."""
        for owned in self.owns_paths:
            if _path_matches(path, owned):
                return True
        return False

    def forbidden(self, path: str) -> bool:
        """True if path matches any 'forbidden' glob."""
        for forb in self.forbidden_paths:
            if _path_matches(path, forb):
                return True
        return False


def _path_matches(path: str, pattern: str) -> bool:
    """Match a path against a simple glob-like pattern.

    Supported syntax:
      - exact match: 'docs/decisions/'
      - prefix glob: '.codex/' matches .codex/cache/, .codex/sessions/, etc.
      - trailing slash: '.codex/' matches only directories
      - path component glob: 'cowork/codex/' matches cowork/codex/anything
    """
    # normalize trailing slash to indicate directory
    if pattern.endswith("/"):
        if not path.endswith("/") and not os.path.isdir(path):
            # Try the path as a directory anyway (for staged files inside)
            if not any(part == pattern.rstrip("/") for part in path.split("/")):
                return False
    # strip trailing slash for matching
    pat = pattern.rstrip("/")
    p = path.rstrip("/")
    # exact match
    if p == pat:
        return True
    # prefix match (pattern must align to path component boundary)
    if p.startswith(pat + "/"):
        return True
    return False


def parse_ownership_matrix(md_path: Path) -> dict[str, Ownership]:
    """Parse AGENT-OWNERSHIP.md into a dict of harness_id -> Ownership."""
    if not md_path.exists():
        raise FileNotFoundError(f"ownership matrix not found: {md_path}")

    text = md_path.read_text()
    matrix: dict[str, Ownership] = {}

    # Find all harness sections
    matches = list(HARNESS_HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        hid = m.group("id")
        # Section body is from this header to the next header (or EOF)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]

        # Extract Owns column values from markdown table rows
        owns = _extract_column(body, column="Owns")
        forbidden = _extract_column(body, column="Forbidden")

        matrix[hid] = Ownership(
            harness_id=hid,
            owns_paths=owns,
            forbidden_paths=forbidden,
            read_paths=["*"],  # by convention, read is universal
        )

    return matrix


def _extract_column(body: str, column: str) -> list[str]:
    """Extract all cell values from a markdown table column named `column`.

    Looks for table header line '| ... | <column> ... |' and extracts
    cell values from data rows (lines starting with '|'). If header has
    multiple values joined (e.g., 'Owns (pode versionar)'), matches by
    partial substring.
    """
    lines = body.splitlines()
    col_idx = None
    collecting = False
    values: list[str] = []

    for line in lines:
        cell_match = CELL_RE.match(line)
        if not cell_match:
            if collecting:
                # left the table
                break
            continue
        cells = [c.strip() for c in cell_match.group(1).split("|")]
        if col_idx is None:
            # Header row — find column index
            for idx, c in enumerate(cells):
                if column.lower() in c.lower():
                    col_idx = idx
                    break
            if col_idx is not None:
                # Next row is the separator (|---|---|) — skip it
                continue
        else:
            # Data row
            if col_idx < len(cells):
                val = cells[col_idx].strip()
                # Strip backticks and parentheses annotations
                val = re.sub(r"\s*\([^)]*\)\s*", " ", val).strip()
                val = val.strip("`")
                if val and val != "—" and val != "-" and val.lower() != "id":
                    # Split on commas for multi-path cells
                    for piece in val.split(","):
                        piece = piece.strip()
                        if piece:
                            values.append(piece)
    return values


# --- git integration -------------------------------------------------------


def get_staged_paths(repo_root: Path) -> list[str]:
    """Return list of paths from 'git status --porcelain' (excluding ignored).

    Detects added (A), modified (M), renamed (R), copied (C), and
    untracked-but-not-ignored (??) entries.
    """
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"ERROR: git status failed: {e}", file=sys.stderr)
        sys.exit(2)

    paths: list[str] = []
    for line in out.stdout.splitlines():
        if not line or len(line) < 3:
            continue
        # Porcelain v1: XY filename
        # Renamed/copied: XY old -> new
        if " -> " in line:
            _, new_path = line[3:].split(" -> ", 1)
            paths.append(new_path.strip())
        else:
            paths.append(line[3:].strip())
    return paths


def has_nested_git(path: str, repo_root: Path) -> bool:
    """True if `path` contains a .git dir at any level inside.

    Defensive: prevents tracking a sub-repo's .git directory.
    """
    full = repo_root / path
    if not full.exists():
        return False
    if full.is_dir():
        try:
            for entry in full.rglob(".git"):
                # rglob could be slow on huge dirs; cap depth check
                rel = entry.relative_to(repo_root)
                if rel != Path(".git"):  # ignore the meta-repo's own .git
                    return True
        except (OSError, ValueError):
            pass
    return False


# --- rendering -------------------------------------------------------------


@dataclass
class Violation:
    path: str
    harness_id: str
    reason: str
    severity: str  # INFO | WARN | BLOCK

    def row(self) -> str:
        return (
            f"| `{self.path}` | `{self.harness_id}` "
            f"| {self.reason} | {self.severity} |"
        )


def evaluate_paths(
    paths: list[str],
    harness_id: str,
    matrix: dict[str, Ownership],
    repo_root: Path,
    mode: str,
) -> list[Violation]:
    """Check each path against the ownership matrix."""
    if harness_id not in matrix:
        return [
            Violation(
                path="<harness>",
                harness_id=harness_id,
                reason=(
                    f"harness_id '{harness_id}' not in AGENT-OWNERSHIP.md. "
                    f"Known: {sorted(matrix.keys())}"
                ),
                severity="BLOCK",
            )
        ]

    owner = matrix[harness_id]
    violations: list[Violation] = []

    for path in paths:
        # Defensive: nested-git trap
        if has_nested_git(path, repo_root):
            violations.append(
                Violation(
                    path=path,
                    harness_id=harness_id,
                    reason=(
                        "nested-git trap: path contains a .git dir; "
                        "should be a separate repo with own remote"
                    ),
                    severity="BLOCK",
                )
            )
            continue

        if owner.forbidden(path):
            violations.append(
                Violation(
                    path=path,
                    harness_id=harness_id,
                    reason=(
                        f"path is FORBIDDEN for harness '{harness_id}'; "
                        f"owned by another harness (see AGENT-OWNERSHIP.md)"
                    ),
                    severity="BLOCK",
                )
            )
            continue

        if not owner.owns(path):
            violations.append(
                Violation(
                    path=path,
                    harness_id=harness_id,
                    reason=(
                        f"path not in 'Owns' column for '{harness_id}'. "
                        f"Add to AGENT-OWNERSHIP.md first or change HARNESS_ACTIVE."
                    ),
                    severity="WARN" if mode == "info" else "BLOCK",
                )
            )

    return violations


def render_report(violations: list[Violation], mode: str, harness_id: str) -> str:
    """Markdown table of violations. Empty list = clean report."""
    sep = "=" * 78
    lines = [
        sep,
        f"# git-physics-guard report",
        f"**harness**: `{harness_id}` | **mode**: `{mode}`",
        f"**violations**: {len(violations)}",
        sep,
        "",
    ]
    if not violations:
        lines.append("OK — all staged paths respect ownership matrix.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Path | Harness | Reason | Severity |")
    lines.append("|---|---|---|---|")
    for v in violations:
        lines.append(v.row())
    lines.append("")
    if mode == "info":
        lines.append(
            "**INFO mode**: warnings shown but commit proceeds. "
            "Promote to 'enforce' after 1-2 weeks of evidence."
        )
    else:
        lines.append(
            "**ENFORCE mode**: commit blocked. Fix ownership or "
            "update AGENT-OWNERSHIP.md before retrying."
        )
    lines.append("")
    return "\n".join(lines)


# --- entrypoint ------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate that staged paths belong to the active harness "
            "per docs/decisions/AGENT-OWNERSHIP.md."
        )
    )
    parser.add_argument(
        "--harness",
        default=os.environ.get("HARNESS_ACTIVE", DEFAULT_HARNESS),
        help="active harness id (default: $HARNESS_ACTIVE or codex-app)",
    )
    parser.add_argument(
        "--matrix",
        default=DEFAULT_OWNERSHIP_MATRIX,
        help="path to AGENT-OWNERSHIP.md relative to repo root",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="path to meta-repo root (default: cwd)",
    )
    parser.add_argument(
        "--mode",
        choices=["info", "enforce"],
        default="info",
        help="info = warn-only, enforce = block commit (default: info)",
    )
    parser.add_argument(
        "--paths-from",
        choices=["staged", "working"],
        default="staged",
        help="paths source: 'staged' (git diff --cached) or "
             "'working' (git status all)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="write report to file in addition to stdout",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress report when there are no violations",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    matrix_path = repo_root / args.matrix

    try:
        matrix = parse_ownership_matrix(matrix_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"ERROR: failed to parse ownership matrix: {e}", file=sys.stderr)
        return 2

    if args.paths_from == "staged":
        paths = get_staged_paths(repo_root)
    else:
        paths = get_staged_paths(repo_root)  # same source for now; future: split

    if not paths:
        if not args.quiet:
            print("git-physics-guard: no staged paths to check.")
        return 0

    violations = evaluate_paths(
        paths=paths,
        harness_id=args.harness,
        matrix=matrix,
        repo_root=repo_root,
        mode=args.mode,
    )

    report = render_report(violations, args.mode, args.harness)
    print(report)

    if args.out:
        Path(args.out).write_text(report)
        print(f"Report written to: {args.out}")

    # Exit code logic
    if not violations:
        return 0
    if args.mode == "info":
        return 0  # info mode: warnings, not blocks
    # enforce mode: block if any BLOCK violation
    if any(v.severity == "BLOCK" for v in violations):
        return 1
    if any(v.severity == "WARN" for v in violations):
        return 0  # WARN in enforce mode still passes (only BLOCK blocks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
