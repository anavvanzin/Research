#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../../.." && pwd)"
python_bin="${SELF_IMPROVING_PYTHON:-/Users/ana/.venvs/iconocracy/bin/python3.12}"

if [[ ! -x "${python_bin}" ]]; then
  python_bin="$(command -v python3)"
fi

exec "${python_bin}" "${repo_root}/.claude/self-improving-agent/scripts/self_improve.py" post-bash \
  --tool-output "${1:-}" \
  --exit-code "${2:-0}"
