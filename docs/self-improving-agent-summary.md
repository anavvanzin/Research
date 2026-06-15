# Self-Improving Agent — Technical Summary

## Overview

Self-improving agent for `/Users/ana/Research` that captures errors, corrections, and feature requests across sessions, validates semantic memory against a JSON Schema, and auto-creates GitHub issues when error patterns repeat beyond a configurable threshold.

## Architecture

```
Hook (PreToolUse / PostBash / SessionEnd)
    → self_improve.py  (--hook <name>)
        → memory/semantic-patterns.json  (semantic + episodic patterns)
        → memory/semantic-patterns.schema.json  (JSON Schema draft 2020-12 v1.1)
        → .learnings/ERRORS.md | FEATURE_REQUESTS.md | LEARNINGS.md
        → GitHub Issues (via gh CLI, when threshold exceeded)
```

## Components

| File | Purpose |
|---|---|
| `.claude/self-improving-agent/scripts/self_improve.py` | Main script — ingest, validate, migrate, report, issue creation |
| `.claude/self-improving-agent/hooks/pre-tool.sh` | Pre-tool hook for blocking operations |
| `.claude/self-improving-agent/hooks/post-bash.sh` | Post-bash hook for error detection |
| `.claude/self-improving-agent/hooks/session-end.sh` | Session-end hook for session summary |
| `.claude/self-improving-agent/memory/semantic-patterns.json` | Canonical semantic memory store |
| `.claude/self-improving-agent/memory/semantic-patterns.schema.json` | JSON Schema v1.1 for memory validation |
| `.learnings/ERRORS.md` | Error log per session |
| `.learnings/FEATURE_REQUESTS.md` | Feature request log |
| `.learnings/LEARNINGS.md` | Session learnings log |

## Configuration

### Threshold (GitHub Issue Auto-Creation)

Environment variable `SELF_IMPROVING_ISSUE_THRESHOLD` (default: `3`). When an error pattern appears ≥ N times across sessions, a GitHub issue is auto-created.

### Hook Wiring (settings.local.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "self-improving-pre-tool",
        "path": "/Users/ana/Research/.claude/self-improving-agent/hooks/pre-tool.sh",
        "enabled": true
      }
    ],
    "PostToolUse": [
      {
        "name": "self-improving-post-tool",
        "trigger": {"event: { "tool": "bash" } },
        "script": "cd /Users/ana/Research && ./.claude/self-improving-agent/hooks/post-bash.sh"
      }
    ],
    "Stop": [
      {
        "name": "self-improving-session-end",
        "command": "cd /Users/ana/Research && ./.claude/self-improving-agent/hooks/session-end.sh"
      }
    ]
  }
}
```

## Usage

```bash
# Validate memory
conda run -n iconocracy python .claude/self-improving-agent/scripts/self_improve.py --validate

# Ingest error (called by hooks)
conda run -n iconocracy python .claude/self-improving-agent/scripts/self_improve.py \
  --hook post-bash --pattern "command not found" --context "..."

# Session summary
conda run -n iconocracy python .claude/self-improving-agent/scripts/self_improve.py --session-summary

# Generate report
conda run -n iconocracy python .claude/self-improving-agent/scripts/self_improve.py --report
```

## Schema

Semantic memory uses JSON Schema draft 2020-12, version `"1.1"`. Auto-migrates from `"1.0"` on load. Key fields: `id`, `pattern`, `description`, `count`, `resolved`, `source`, `last_seen`.
