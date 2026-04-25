#!/usr/bin/env bash
# PostToolUse hook (Bash only) for the repo-local self-improving agent.
#
# Claude Code delivers hook data as JSON on stdin; we parse it with jq.
# Manual smoke tests can still pass positional args ($1=tool_output, $2=exit_code).
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="${CLAUDE_PROJECT_DIR:-$(cd "${script_dir}/../../.." && pwd)}"

python_bin="${SELF_IMPROVING_PYTHON:-}"
if [[ -z "${python_bin}" || ! -x "${python_bin}" ]]; then
  python_bin="$(command -v python3.12 2>/dev/null || command -v python3 2>/dev/null || true)"
fi
[[ -n "${python_bin}" ]] || exit 0

tool_output="${1:-}"
exit_code="${2:-0}"
if [[ ! -t 0 ]] && command -v jq >/dev/null 2>&1; then
  payload="$(cat 2>/dev/null || true)"
  if [[ -n "${payload}" ]]; then
    # The tool-response shape varies between Claude Code versions; try the known keys
    # and join stdout + stderr so failure signatures survive either path.
    stdout_text="$(printf '%s' "${payload}" | jq -r '.tool_response.stdout // .tool_response.output // .tool_output.output // ""' 2>/dev/null || echo "")"
    stderr_text="$(printf '%s' "${payload}" | jq -r '.tool_response.stderr // ""' 2>/dev/null || echo "")"
    if [[ -n "${stderr_text}" ]]; then
      tool_output="${stdout_text}
${stderr_text}"
    else
      tool_output="${stdout_text}"
    fi
    exit_code="$(printf '%s' "${payload}" | jq -r '.tool_response.exit_code // .tool_output.exit_code // 0' 2>/dev/null || echo "0")"
    # Normalize to int; treat "true" (interrupted) as 1, "false" as 0.
    case "${exit_code}" in
      true)  exit_code="1" ;;
      false) exit_code="0" ;;
      null|"") exit_code="0" ;;
    esac
  fi
fi

# Silently no-op when no useful payload — avoids argparse error when stdin/args empty.
if [[ -z "${tool_output}" ]]; then
  exit 0
fi

exec "${python_bin}" "${repo_root}/.claude/self-improving-agent/scripts/self_improve.py" post-bash \
  --tool-output="${tool_output}" \
  --exit-code="${exit_code}"
