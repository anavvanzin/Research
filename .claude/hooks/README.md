# Dev-infrastructure hooks — INERT by default

These four scripts were installed by `/dev-setup` (claude-dev-infrastructure) on
2026-07-03. **They are not wired into any `settings.json`, so they do nothing right now.**
That is deliberate — see "Why inert" below.

| Script | Event | What it does |
|--------|-------|--------------|
| `task-lock-enforcer.sh` | PreToolUse (Edit\|Write) | Blocks edits (`exit 2`) to files listed against an active MASTER_PLAN task when another session holds the lock. |
| `session-lock-awareness.sh` | SessionStart | Reports locks held by other sessions. |
| `session-lock-release.sh` | SessionEnd | Releases this session's locks. |
| `master-plan-reminder.sh` | UserPromptSubmit | Nudges to keep `docs/MASTER_PLAN.md` current. |

## Why inert (Cowork / Claude Desktop assessment)

- The lock hooks exist to coordinate **several Claude Code CLI instances editing one
  repo in parallel**. In a single-instance Cowork workflow that coordination has no
  benefit and one real downside: a stale lock (or an edit to a file the parser matches
  to a task) can `exit 2` and **silently block your own edits**.
- They depend on the Claude Code hook contract (`${CLAUDE_PROJECT_DIR}`, JSON on stdin,
  `jq`, exit-code semantics) and would have to be **merged into your existing
  `.claude/settings.json`**, which already runs the `self-improving-agent` hooks.
- `master-plan-reminder.sh` is harmless but fires on every prompt.

## How to opt in (if you ever run parallel instances)

Merge into `.claude/settings.json` — do NOT replace the existing `hooks` block, add to it:

```json
"PreToolUse": [
  { "matcher": "Edit|Write",
    "hooks": [{ "type": "command", "command": "bash \"${CLAUDE_PROJECT_DIR}/.claude/hooks/task-lock-enforcer.sh\"" }] }
],
"SessionStart": [
  { "hooks": [{ "type": "command", "command": "bash \"${CLAUDE_PROJECT_DIR}/.claude/hooks/session-lock-awareness.sh\"" }] }
],
"SessionEnd": [
  { "hooks": [{ "type": "command", "command": "bash \"${CLAUDE_PROJECT_DIR}/.claude/hooks/session-lock-release.sh\"" }] }
]
```

Then `chmod +x .claude/hooks/*.sh`. Lock state lives in `.claude/locks/`.

To remove entirely: delete this directory and `.claude/locks/`.
