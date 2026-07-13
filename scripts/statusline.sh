#!/usr/bin/env bash
# statusline.sh — Cursor CLI status line (multiline: model, cwd, git, context bar).
#
# Reads StatusLinePayload JSON from stdin. See:
#   ~/.cursor/skills-cursor/statusline/SKILL.md
#   packages/agent-cli/src/hooks/use-status-line.ts (StatusLinePayload)
set -euo pipefail

input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name // "unknown"')
PARAMS=$(echo "$input" | jq -r '.model.param_summary // empty')
DIR=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // ""')
WIDTH=$(echo "$input" | jq -r '.render_width_chars // 120')
PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
WORKTREE=$(echo "$input" | jq -r '.worktree.name // empty')

# Basename of cwd; fall back to full path if empty.
DIRNAME="${DIR##*/}"
[ -z "$DIRNAME" ] && DIRNAME="$DIR"

# Git branch (only when cwd is inside a repo).
BRANCH=""
if [ -n "$DIR" ] && git -C "$DIR" rev-parse --git-dir >/dev/null 2>&1; then
    BRANCH=$(git -C "$DIR" branch --show-current 2>/dev/null || true)
    [ -n "$BRANCH" ] && BRANCH=" | ${BRANCH}"
fi

# Worktree indicator when present.
WT=""
[ -n "$WORKTREE" ] && WT=" [wt:${WORKTREE}]"

# Model label with optional param summary (e.g. "(Thinking)").
MODEL_LABEL="[${MODEL}"
[ -n "$PARAMS" ] && MODEL_LABEL="${MODEL_LABEL} ${PARAMS}"
MODEL_LABEL="${MODEL_LABEL}]"

# Context progress bar (10 chars).
BAR_WIDTH=10
PCT_NUM=${PCT:-0}
[ "$PCT_NUM" -lt 0 ] 2>/dev/null && PCT_NUM=0
[ "$PCT_NUM" -gt 100 ] 2>/dev/null && PCT_NUM=100
FILLED=$((PCT_NUM * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))
BAR=""
[ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
[ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

# Line 1: model, directory, git branch, optional worktree.
LINE1=$(printf '\033[36m%s\033[0m  %s%s%s' "$MODEL_LABEL" "$DIRNAME" "$BRANCH" "$WT")

# Line 2: context bar.
LINE2=$(printf '\033[90mctx %s %s%%\033[0m' "$BAR" "$PCT_NUM")

# Truncate line 1 if wider than render_width_chars.
if [ "${#LINE1}" -gt "$WIDTH" ] 2>/dev/null; then
    # Strip ANSI for length check; simple truncation on visible part.
    VISIBLE=$(printf '%s' "$LINE1" | sed 's/\x1b\[[0-9;]*m//g')
    if [ "${#VISIBLE}" -gt "$WIDTH" ]; then
        TRUNC=$((WIDTH - 3))
        VISIBLE="${VISIBLE:0:$TRUNC}..."
        LINE1=$(printf '\033[36m%s\033[0m  %s' "$MODEL_LABEL" "${VISIBLE#*]  }")
    fi
fi

printf '%s\n%s\n' "$LINE1" "$LINE2"
