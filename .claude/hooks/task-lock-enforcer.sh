#!/bin/bash
#
# Hook: Task Lock Enforcer (PreToolUse)
# Purpose: Block edits to files owned by IN_PROGRESS tasks locked by another session
# Exit 2 = Block the tool call with error message
# Exit 0 = Allow the tool call
#
# This hook implements file-based locking for multi-instance coordination:
# 1. Checks if edited file belongs to a tracked MASTER_PLAN task
# 2. If task is locked by another session -> BLOCK (exit 2)
# 3. If task is not locked -> Acquire lock and ALLOW (exit 0)
#

set -euo pipefail

# Ensure CLAUDE_PROJECT_DIR is declared to prevent unbound variable errors
CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
if [[ -z "$CLAUDE_PROJECT_DIR" ]]; then
  # Fallback to git root if available, otherwise default to current directory
  CLAUDE_PROJECT_DIR=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
fi

# Configuration
LOCKS_DIR="${CLAUDE_PROJECT_DIR}/.claude/locks"
MASTER_PLAN="${CLAUDE_PROJECT_DIR}/docs/MASTER_PLAN.md"
LOCK_EXPIRY_HOURS=4  # Stale locks older than this are auto-cleared

# Ensure locks directory exists
mkdir -p "$LOCKS_DIR"

# Guard against missing jq package
if ! command -v jq &>/dev/null; then
  # If jq is missing, silently bypass lock enforcement to avoid blocking developer
  exit 0
fi

# Read JSON input from stdin safely
INPUT=$(cat || echo "")

# Extract data from hook input with safe fallbacks
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""' 2>/dev/null || echo "")
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // ""' 2>/dev/null || echo "")
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""' 2>/dev/null || echo "")

# Global override / bypass variable check
CLAUDE_BYPASS_LOCKS="${CLAUDE_BYPASS_LOCKS:-0}"
if [[ "$CLAUDE_BYPASS_LOCKS" == "1" ]] || [[ "$CLAUDE_BYPASS_LOCKS" == "true" ]]; then
  exit 0
fi

# Only apply to Edit and Write tools
if [[ "$TOOL_NAME" != "Edit" ]] && [[ "$TOOL_NAME" != "Write" ]]; then
  exit 0
fi

# Skip if no file path
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Skip non-source files (configs, tests, docs don't indicate active task work)
if [[ "$FILE_PATH" == *".json" ]] || [[ "$FILE_PATH" == *".md" ]] || [[ "$FILE_PATH" == *".sh" ]] || [[ "$FILE_PATH" == *".lock" ]]; then
  exit 0
fi

# Skip if MASTER_PLAN doesn't exist
if [[ ! -f "$MASTER_PLAN" ]]; then
  exit 0
fi

# Get just the filename for matching
FILENAME=$(basename "$FILE_PATH")

# Function to clean up stale locks
cleanup_stale_locks() {
  local current_time
  current_time=$(date +%s)
  local expiry_seconds=$((LOCK_EXPIRY_HOURS * 3600))

  # Use find instead of glob to handle empty directory case
  while IFS= read -r -d '' lock_file; do
    if [[ -f "$lock_file" ]]; then
      local lock_time
      lock_time=$(jq -r '.timestamp // 0' "$lock_file" 2>/dev/null || echo "0")
      local age=$((current_time - lock_time))
      if [[ $age -gt $expiry_seconds ]]; then
        rm -f "$lock_file"
      fi
    fi
  done < <(find "$LOCKS_DIR" -maxdepth 1 -name "*.lock" -print0 2>/dev/null)
}

# Function to find matching task for a file
find_matching_task() {
  local file_path="$1"
  local filename="$2"
  local matching_task=""
  local task_status=""

  while IFS= read -r line; do
    # Skip non-table rows and header rows
    if [[ ! "$line" =~ ^\|.*TASK-[0-9]+ ]]; then
      continue
    fi

    # Extract task ID (handle strikethrough for done tasks)
    local task_id
    task_id=$(echo "$line" | grep -oE '(~~)?TASK-[0-9]+(~~)?' | head -1 | tr -d '~')

    # Extract status (2nd column after ID)
    task_status=$(echo "$line" | cut -d'|' -f3 | xargs)

    # Skip done tasks (by ID strikethrough or DONE/COMPLETE status column)
    if [[ "$line" =~ ~~TASK-[0-9]+~~ ]] || [[ "$task_status" == "DONE" ]] || [[ "$task_status" == "COMPLETE" ]]; then
      continue
    fi

    # Extract primary files column (3rd column after ID)
    local primary_files
    primary_files=$(echo "$line" | cut -d'|' -f4 | tr -d '`' | xargs)

    # Check if edited file matches any pattern in Primary Files
    for pattern in $(echo "$primary_files" | tr ',' ' '); do
      pattern=$(echo "$pattern" | xargs)  # trim whitespace
      [[ -z "$pattern" ]] && continue

      # Match direct filename, exact path, or relative suffix pattern (e.g. docs/example.md)
      if [[ "$filename" == "$pattern" ]] || [[ "$file_path" == "$pattern" ]] || [[ "$file_path" == *"/$pattern" ]]; then
        echo "$task_id|$task_status"
        return 0
      fi

      # Glob pattern match (e.g., *.stories.ts, src/stores/*.ts)
      if [[ "$pattern" == *"*"* ]]; then
        # Convert glob to regex
        local regex
        regex=$(echo "$pattern" | sed 's/\./\\./g' | sed 's/\*/.*/g')
        if echo "$filename" | grep -qE "^$regex$" 2>/dev/null; then
          echo "$task_id|$task_status"
          return 0
        fi
        # Also check full path for directory patterns
        if echo "$file_path" | grep -qE "$regex" 2>/dev/null; then
          echo "$task_id|$task_status"
          return 0
        fi
      fi
    done
  done < "$MASTER_PLAN"

  echo ""
  return 1
}

# Function to check if task is locked by another session
check_lock() {
  local task_id="$1"
  local lock_file="$LOCKS_DIR/${task_id}.lock"

  if [[ -f "$lock_file" ]]; then
    local locked_session
    locked_session=$(jq -r '.session_id // ""' "$lock_file" 2>/dev/null || echo "")
    if [[ -n "$locked_session" ]] && [[ "$locked_session" != "$SESSION_ID" ]]; then
      # Locked by another session
      local locked_by
      local locked_at
      locked_by=$(jq -r '.session_id' "$lock_file" 2>/dev/null)
      locked_at=$(jq -r '.locked_at // "unknown"' "$lock_file" 2>/dev/null)
      echo "$locked_by|$locked_at"
      return 0
    fi
  fi
  return 1
}

# Function to acquire lock
acquire_lock() {
  local task_id="$1"
  local lock_file="$LOCKS_DIR/${task_id}.lock"
  local current_time
  current_time=$(date +%s)
  local human_time
  human_time=$(date '+%Y-%m-%d %H:%M:%S')

  cat > "$lock_file" << EOF
{
  "task_id": "$task_id",
  "session_id": "$SESSION_ID",
  "timestamp": $current_time,
  "locked_at": "$human_time",
  "files_touched": ["$FILE_PATH"]
}
EOF
}

# Main logic
cleanup_stale_locks

# Find if this file belongs to a tracked task
TASK_INFO=$(find_matching_task "$FILE_PATH" "$FILENAME" || echo "")

if [[ -z "$TASK_INFO" ]]; then
  # File doesn't belong to any tracked task, allow edit
  exit 0
fi

# Parse task info
TASK_ID=$(echo "$TASK_INFO" | cut -d'|' -f1)
TASK_STATUS=$(echo "$TASK_INFO" | cut -d'|' -f2)

# Check if task is locked by another session
LOCK_INFO=$(check_lock "$TASK_ID" || echo "")

if [[ -n "$LOCK_INFO" ]]; then
  # Task is locked by another session - BLOCK
  LOCKED_BY=$(echo "$LOCK_INFO" | cut -d'|' -f1)
  LOCKED_AT=$(echo "$LOCK_INFO" | cut -d'|' -f2)

  # Output error to stderr (will be shown to Claude / developer)
  cat >&2 << EOF
TASK CONFLICT BLOCKED: Cannot edit $FILENAME

$TASK_ID is currently locked by another Claude Code session.
  - Locked by session: ${LOCKED_BY:0:8}...
  - Locked at: $LOCKED_AT

To override or bypass:
1. Export the bypass variable before editing: export CLAUDE_BYPASS_LOCKS=1
2. Or manually remove the lock file: rm -f "$LOCKS_DIR/${TASK_ID}.lock"
3. Check docs/MASTER_PLAN.md for current active tasks.

Suggest working on a different task that doesn't conflict.
EOF

  # Exit 2 blocks the tool call
  exit 2
fi

# Task is not locked or locked by this session - acquire/refresh lock and allow
acquire_lock "$TASK_ID"

# If task was not IN_PROGRESS, we should note that we're starting work
if [[ "$TASK_STATUS" != "IN_PROGRESS" ]] && [[ "$TASK_STATUS" != *"MONITORING"* ]]; then
  # Output context about acquiring the lock (shown to Claude in verbose mode)
  echo "TASK LOCK: Acquired lock for $TASK_ID (editing $FILENAME). Status will be updated to IN_PROGRESS."
fi

exit 0
