#!/usr/bin/env bash
# install-statusline.sh — wire Cursor CLI status line (per-machine).
#
# ~/.cursor/cli-config.json and ~/.cursor/statusline.sh are local and NOT
# versioned. Run once per machine (or after clone) from the Research repo root.
#
# Usage:
#   bash scripts/install-statusline.sh           # install (default)
#   bash scripts/install-statusline.sh install   # same as default
#   bash scripts/install-statusline.sh test      # run mock payload through script
#   bash scripts/install-statusline.sh uninstall # remove symlink + statusLine config
#
# Prerequisite: jq (brew install jq on macOS)
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SOURCE="${REPO_ROOT}/scripts/statusline.sh"
TARGET="${HOME}/.cursor/statusline.sh"
CONFIG="${HOME}/.cursor/cli-config.json"

require_jq() {
    if ! command -v jq >/dev/null 2>&1; then
        echo "ERROR: jq is required. Install with: brew install jq"
        exit 1
    fi
}

run_test() {
    require_jq
    if [ ! -x "${SOURCE}" ]; then
        echo "ERROR: ${SOURCE} not found or not executable."
        exit 1
    fi
    echo "Running mock payload through ${SOURCE}:"
    echo ""
    echo '{"model":{"display_name":"Claude 4 Opus","param_summary":"(Thinking)"},"workspace":{"current_dir":"'"${REPO_ROOT}"'"},"context_window":{"used_percentage":34.5},"render_width_chars":120}' \
        | "${SOURCE}"
    echo ""
    echo "OK: statusline script produced output."
}

do_uninstall() {
    require_jq

    if [ -L "${TARGET}" ]; then
        rm "${TARGET}"
        echo "Removed symlink: ${TARGET}"
    elif [ -f "${TARGET}" ]; then
        echo "WARN: ${TARGET} exists but is not a symlink; not removed."
    else
        echo "No statusline symlink at ${TARGET}."
    fi

    if [ -f "${CONFIG}" ]; then
        if jq -e '.statusLine' "${CONFIG}" >/dev/null 2>&1; then
            TMP=$(mktemp)
            jq 'del(.statusLine)' "${CONFIG}" > "${TMP}"
            mv "${TMP}" "${CONFIG}"
            echo "Removed statusLine from ${CONFIG}"
        else
            echo "No statusLine key in ${CONFIG}."
        fi
    else
        echo "No config at ${CONFIG}."
    fi
}

do_install() {
    require_jq

    if [ ! -f "${SOURCE}" ]; then
        echo "ERROR: ${SOURCE} not found."
        exit 1
    fi

    chmod +x "${SOURCE}"
    mkdir -p "${HOME}/.cursor"

    # Symlink so git pull updates the live script.
    if [ -L "${TARGET}" ]; then
        rm "${TARGET}"
    elif [ -e "${TARGET}" ]; then
        cp "${TARGET}" "${TARGET}.bak.$(date +%Y%m%d-%H%M%S)"
        rm "${TARGET}"
        echo "Backed up existing ${TARGET} to ${TARGET}.bak.*"
    fi
    ln -s "${SOURCE}" "${TARGET}"
    echo "Symlinked: ${TARGET} -> ${SOURCE}"

    # Merge statusLine into cli-config.json (preserve other keys).
    STATUS_BLOCK='{
  "type": "command",
  "command": "~/.cursor/statusline.sh",
  "padding": 2,
  "updateIntervalMs": 300,
  "timeoutMs": 2000
}'

    if [ -f "${CONFIG}" ]; then
        TMP=$(mktemp)
        jq --argjson sl "${STATUS_BLOCK}" '.statusLine = $sl' "${CONFIG}" > "${TMP}"
        mv "${TMP}" "${CONFIG}"
    else
        echo "{\"statusLine\": ${STATUS_BLOCK}}" | jq '.' > "${CONFIG}"
    fi
    echo "Updated: ${CONFIG}"
    echo ""
    echo "Restart Cursor CLI or open a new session to see the status line."
    echo "Test without CLI:"
    echo "  bash scripts/install-statusline.sh test"
}

ACTION="${1:-install}"
case "${ACTION}" in
    install) do_install ;;
    test)    run_test ;;
    uninstall) do_uninstall ;;
    *)
        echo "Usage: $0 [install|test|uninstall]"
        exit 1
        ;;
esac
