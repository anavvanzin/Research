#!/usr/bin/env bash
# PreToolUse hook for the repo-local self-improving agent.
#
# Claude Code delivers hook data as JSON on stdin; we parse it with jq.
# Manual smoke tests can still pass positional args ($1=tool_name, $2=tool_input).
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="${CLAUDE_PROJECT_DIR:-$(cd "${script_dir}/../../.." && pwd)}"

# Pick a Python: env override -> 3.12 -> 3 -> silently skip.
python_bin="${SELF_IMPROVING_PYTHON:-}"
if [[ -z "${python_bin}" || ! -x "${python_bin}" ]]; then
  python_bin="$(command -v python3.12 2>/dev/null || command -v python3 2>/dev/null || true)"
fi
[[ -n "${python_bin}" ]] || exit 0

tool_name="${1:-unknown}"
tool_input="${2:-}"
if [[ ! -t 0 ]] && command -v jq >/dev/null 2>&1; then
  payload="$(cat 2>/dev/null || true)"
  if [[ -n "${payload}" ]]; then
    tool_name="$(printf '%s' "${payload}" | jq -r '.tool_name // "unknown"' 2>/dev/null || echo "unknown")"
    tool_input="$(printf '%s' "${payload}" | jq -r '
      (.tool_input.command // .tool_input // "") |
      if type == "string" then . else tostring end
    ' 2>/dev/null || echo "")"
  fi
fi

exec "${python_bin}" "${repo_root}/.claude/self-improving-agent/scripts/self_improve.py" pre-tool \
  --tool-name="${tool_name}" \
  --tool-input="${tool_input}"
