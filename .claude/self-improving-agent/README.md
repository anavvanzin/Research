# Repo-Local Self-Improving Agent

This repo-local automation captures tool activity inside `anavvanzin/Research` and stores reusable traces in a small multi-memory layout.

## What It Does

- Records `PreToolUse` events for `Bash` (the only tool currently wired up)
- Records `PostToolUse` outcomes for `Bash` (success/failure from `isError`/`interrupted`)
- Writes episodic records for shell failures
- Maintains a lightweight semantic memory of repeated bash failure signatures
- Captures GitHub metadata with `gh repo view`
- Can ask `gh copilot` for a short recovery hint when enabled
- **Auto-creates GitHub issues via `gh` when a pattern recurs N times**
- **Validates semantic memory against a JSON Schema**

## Activation

The hooks run only when the repo-local `.claude/settings.json` registers them. This repo ships a default registration for `PreToolUse` (Bash), `PostToolUse` (Bash), and `SessionEnd`. Claude Code invokes each hook with a JSON payload on stdin; the shell scripts pipe that payload into `scripts/self_improve.py`.

## Layout

```text
.claude/
  settings.json                       # registers the hooks
  self-improving-agent/
    hooks/                            # thin bash stubs; all logic in Python
    memory/
      semantic-patterns.json          # tracked — baseline memory contract
      semantic-patterns.schema.json   # JSON Schema for validation
      episodic/
      working/
    scripts/
      self_improve.py
```

## GitHub Issue Auto-Creation

When a pattern in `semantic-patterns.json` accumulates `applications >= SELF_IMPROVING_ISSUE_THRESHOLD` (default: **3**), the `post-bash` hook automatically creates a GitHub issue on the repo using `gh issue create`.

- The issue is labelled `self-improving-agent`.
- The issue number is stored in the pattern's `github_issue` field to prevent duplicates.
- Set `SELF_IMPROVING_ISSUE_THRESHOLD=0` to disable.

Example of an auto-created pattern with issue:

```json
{
  "logic_or_unknown_conda_run": {
    "id": "logic_or_unknown_conda_run",
    "applications": 4,
    "confidence": 0.65,
    "github_issue": 42,
    ...
  }
}
```

## Schema Validation

Run `validate` to check `semantic-patterns.json` against `semantic-patterns.schema.json`:

```bash
python3 .claude/self-improving-agent/scripts/self_improve.py validate
```

The `post-bash` hook automatically migrates `schema_version: "1.0"` → `"1.1"` and adds new fields (`contradicts`, `supersedes`, `github_issue`, `quality_rules`, `recovery_hints`) on write.

## Optional Environment Variables

- `SELF_IMPROVING_PYTHON`: override the Python executable used by the hooks (default: first of `python3.12`, `python3` found on `PATH`)
- `SELF_IMPROVING_USE_COPILOT=1`: ask `gh copilot` for a short suggestion on bash errors
- `SELF_IMPROVING_ISSUE_THRESHOLD`: number of pattern occurrences before auto-creating a GitHub issue (default: 3, set to 0 to disable)

## Manual Smoke Test

The hook subcommands read JSON from stdin, matching Claude Code's hook contract:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"false"}}' \
  | python3 .claude/self-improving-agent/scripts/self_improve.py pre-tool-hook

echo '{"tool_name":"Bash","tool_input":{"command":"false"},"tool_response":{"stdout":"","stderr":"command failed","isError":true}}' \
  | python3 .claude/self-improving-agent/scripts/self_improve.py post-bash-hook

python3 .claude/self-improving-agent/scripts/self_improve.py session-end
python3 .claude/self-improving-agent/scripts/self_improve.py validate
```

The `pre-tool` / `post-bash` CLI subcommands (positional-style, `--tool-name …`) remain for ad-hoc testing.

## Notes

- Runtime working files and episodic JSON entries are ignored by this repo (`.gitignore`).
- `semantic-patterns.json` and `semantic-patterns.schema.json` stay tracked so the baseline contract is versioned.
- GitHub context is resolved from the current repo with `gh`, falling back to `git` when needed.
- The schema version is `"1.1"`. Migration from `"1.0"` is automatic on write.
- `write_json` is atomic (tempfile + `os.replace`) so concurrent hook invocations cannot leave a partial memory file.