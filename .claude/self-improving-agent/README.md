# Repo-Local Self-Improving Agent

This repo-local automation captures tool activity inside `anavvanzin/Research` and stores reusable traces in a small multi-memory layout.

## What It Does

- Records `PreToolUse` events for `Bash`, `Write`, and `Edit`
- Records `PostToolUse` outcomes for `Bash`
- Writes episodic records for shell failures
- Maintains a lightweight semantic memory of repeated bash failure signatures
- Captures GitHub metadata with `gh repo view`
- Can ask `gh copilot` for a short recovery hint when enabled
- **Auto-creates GitHub issues via `gh` when a pattern recurs N times**
- **Validates semantic memory against a JSON Schema**

## Layout

```text
.claude/self-improving-agent/
  hooks/
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
/Users/ana/.venvs/iconocracy/bin/python3.12 \
  /Users/ana/Research/.claude/self-improving-agent/scripts/self_improve.py validate
```

The `post-bash` hook automatically migrates `schema_version: "1.0"` → `"1.1"` and adds new fields (`contradicts`, `supersedes`, `github_issue`, `quality_rules`, `recovery_hints`) on write.

## Optional Environment Variables

- `SELF_IMPROVING_PYTHON`: override the Python executable used by the hooks
- `SELF_IMPROVING_USE_COPILOT=1`: ask `gh copilot` for a short suggestion on bash errors
- `SELF_IMPROVING_ISSUE_THRESHOLD`: number of pattern occurrences before auto-creating a GitHub issue (default: 3, set to 0 to disable)

## Manual Smoke Test

```bash
bash /Users/ana/Research/.claude/self-improving-agent/hooks/pre-tool.sh Bash "false"
bash /Users/ana/Research/.claude/self-improving-agent/hooks/post-bash.sh "command failed" "1"
bash /Users/ana/Research/.claude/self-improving-agent/hooks/session-end.sh
python3.12 /Users/ana/Research/.claude/self-improving-agent/scripts/self_improve.py validate
```

## Notes

- Runtime working files and episodic JSON entries are ignored by this repo (`.gitignore`).
- `semantic-patterns.json` and `semantic-patterns.schema.json` stay tracked so the baseline contract is versioned.
- GitHub context is resolved from the current repo with `gh`, falling back to `git` when needed.
- The schema version is `"1.1"`. Migration from `"1.0"` is automatic on write.