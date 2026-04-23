#!/bin/bash
# Weekly backup script for ICONOCRACIA repos
# Created: 2026-04-22
# Runs via crontab: 0 10 * * 0

set -euo pipefail

REPOS=(
  "/Users/ana/Research/hub/iconocracy-corpus"
  "/Users/ana/Research"
  "/Users/ana/Research/apps/iconocracia-companion"
  "/Users/ana/Research/apps/iconocracia-space"
)

LOG_DIR="/Users/ana/Research/.logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/repo-backup-$(date +%Y-%m-%d).log"

exec > >(tee -a "$LOG")
exec 2>&1

echo "=== Backup run: $(date) ==="

for repo in "${REPOS[@]}"; do
  echo ""
  echo "--> $repo"
  if [ ! -d "$repo/.git" ]; then
    echo "    SKIP: not a git repo"
    continue
  fi

  cd "$repo"

  # Fetch to know the real state
  git fetch --quiet origin 2>/dev/null || true

  AHEAD=$(git rev-list origin/main..HEAD --count 2>/dev/null || echo "0")
  BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")

  if [ "$AHEAD" != "0" ]; then
    echo "    $AHEAD commits ahead — pushing..."
    git push origin HEAD:main 2>&1 && echo "    OK" || echo "    FAILED"
  elif [ "$BEHIND" != "0" ]; then
    echo "    $BEHIND commits behind — pulling..."
    git pull --ff-only origin main 2>&1 && echo "    OK" || echo "    FAILED (merge conflict?)"
  else
    echo "    Up to date"
  fi

done

echo ""

# Optional: Hugging Face dataset status check
# Requires: hf auth login (one-time browser auth)
# HF_DATASET="warholana/iconocracy-corpus"
# if command -v hf >/dev/null 2>&1; then
#   echo "--> Hugging Face dataset: $HF_DATASET"
#   hf repos info "$HF_DATASET" --repo-type dataset 2>/dev/null && echo "    Reachable" || echo "    SKIP: not authenticated"
# fi

echo "=== Done: $(date) ==="
