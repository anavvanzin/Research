#!/usr/bin/env bash
# SessionEnd hook for the repo-local self-improving agent.
#
# Drains stdin (Claude Code always sends a JSON payload) and invokes the
# finalizer. No payload data is needed — the call itself is the trigger.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="${CLAUDE_PROJECT_DIR:-$(cd "${script_dir}/../../.." && pwd)}"

python_bin="${SELF_IMPROVING_PYTHON:-}"
if [[ -z "${python_bin}" || ! -x "${python_bin}" ]]; then
  python_bin="$(command -v python3.12 2>/dev/null || command -v python3 2>/dev/null || true)"
fi
[[ -n "${python_bin}" ]] || exit 0

# Drain stdin so Claude Code isn't blocked.
[[ -t 0 ]] || cat >/dev/null 2>&1 || true

exec "${python_bin}" "${repo_root}/.claude/self-improving-agent/scripts/self_improve.py" session-end
