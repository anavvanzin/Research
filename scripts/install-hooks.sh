#!/usr/bin/env bash
# install-hooks.sh — wire git-physics-guard as pre-commit hook (per-clone).
#
# .git/hooks/ is local and NOT versioned, so this must be run once per clone.
# Mode is "info" by default (warnings, not blocks). Promote to "enforce"
# in the script body if you want hard blocks.
#
# Usage:
#   bash scripts/install-hooks.sh           # install (info mode, default)
#   bash scripts/install-hooks.sh enforce   # install in enforce mode
#   bash scripts/install-hooks.sh uninstall # remove the symlink
#
# Refs: docs/decisions/2026-06-25-multi-harness-git-physics.md (ADR §6)
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="${REPO_ROOT}/.git/hooks"
HOOK_FILE="${HOOKS_DIR}/pre-commit"
GUARD="${REPO_ROOT}/scripts/git_physics_guard.py"

if [ "${1:-info}" = "uninstall" ]; then
    if [ -L "${HOOK_FILE}" ] && readlink "${HOOK_FILE}" | grep -q "git_physics_guard"; then
        rm "${HOOK_FILE}"
        echo "Removed: ${HOOK_FILE}"
    else
        echo "No git-physics-guard hook installed at ${HOOK_FILE}."
    fi
    exit 0
fi

MODE="${1:-info}"
if [ "${MODE}" != "info" ] && [ "${MODE}" != "enforce" ]; then
    echo "Usage: $0 [info|enforce|uninstall]"
    exit 1
fi

if [ ! -f "${GUARD}" ]; then
    echo "ERROR: ${GUARD} not found."
    exit 1
fi

# Backup any existing pre-commit hook (don't clobber user's custom hook).
if [ -e "${HOOK_FILE}" ] && [ ! -L "${HOOK_FILE}" ]; then
    cp "${HOOK_FILE}" "${HOOK_FILE}.bak.$(date +%Y%m%d-%H%M%S)"
    echo "Backed up existing hook to ${HOOK_FILE}.bak.*"
fi

# Replace existing symlink if present.
if [ -L "${HOOK_FILE}" ]; then
    rm "${HOOK_FILE}"
fi

# Write a wrapper hook that calls the guard with --mode.
cat > "${HOOK_FILE}" << EOF
#!/usr/bin/env bash
# Auto-installed by scripts/install-hooks.sh on $(date +%Y-%m-%d).
# Mode: ${MODE}
# Edit scripts/install-hooks.sh to change behavior, then re-run.
exec python3 "${GUARD}" --mode "${MODE}" --paths-from staged
EOF
chmod +x "${HOOK_FILE}"

echo "Installed: ${HOOK_FILE} -> ${GUARD} (mode: ${MODE})"
echo ""
echo "Test it:"
echo "  cd ${REPO_ROOT}"
echo "  git add some_file"
echo "  git commit -m 'test'"
echo "  # guard will print report; in info mode commit proceeds."
