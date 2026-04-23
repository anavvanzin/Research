#!/usr/bin/env bash
# PreToolUse hook: reads Claude Code's JSON payload from stdin and records it.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../../.." && pwd)"

python_bin="${SELF_IMPROVING_PYTHON:-}"
if [[ -z "${python_bin}" ]]; then
  python_bin="$(command -v python3.12 2>/dev/null || command -v python3 2>/dev/null || true)"
fi
if [[ -z "${python_bin}" || ! -x "${python_bin}" ]]; then
  # No usable Python — drop the payload silently rather than block the tool call.
  exit 0
fi

exec "${python_bin}" "${repo_root}/.claude/self-improving-agent/scripts/self_improve.py" pre-tool-hook
