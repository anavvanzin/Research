# Automation Surfaces — `/Users/ana/Research`

Single source of truth for *where* automation lives, *what triggers it*, and *what owns its config*. Read this before adding a new hook, skill, agent, or scheduled task.

Last reviewed: 2026-04-25.

---

## Hooks (Claude Code)

| Surface | Config file | Trigger | Purpose |
|---|---|---|---|
| Self-improving-agent (project) | `.claude/settings.json` | PreToolUse Bash\|Write\|Edit, PostToolUse Bash, SessionEnd `.*` | Captures tool I/O (Bash + Write/Edit pre, Bash post) + session summaries into `.claude/self-improving-agent/memory/`. Stdin-JSON invocation; hooks scripts at `.claude/self-improving-agent/hooks/{pre-tool,post-bash,session-end}.sh`. Canonical wiring as of 2026-04-25 (`settings.local.json` `hooks` block stripped). |
| Corpus protection (global) | `~/.claude/settings.json` | PreToolUse Write, PostToolUse Edit\|Write | Blocks binary image writes into `iconocracy-corpus/data/raw/`; warns on `corpus-data.json` edits; runs `tools/scripts/validate_schemas.py` on corpus JSONL changes. Owned by global config — do not duplicate at project level. |

**Disabled via env:** `ECC_DISABLED_HOOKS=pre:bash:gateguard-fact-force,pre:edit-write:gateguard-fact-force` (set in shell, turns off ECC plugin's fact gate).

**Permission denies (global):** `git reset --hard`, `git push --force`, `rm -rf` on `iconocracy-corpus/{tese,vault,corpus}` paths.

---

## Agents (`~/.claude/agents/`)

20 agents installed globally. Thesis-specific (use these for ICONOCRACIA work):

| Agent | Purpose |
|---|---|
| `abnt-checker` | ABNT NBR 6023:2025 citation lint |
| `chapter-integrity` | Mandatory terminology + citation scan before compile |
| `corpus-dedup` | Pre-save dedup check for new corpus candidates |
| `iconclass-reviewer` | Verify Iconclass notation validity |
| `iconocode` | Full Panofsky 3-level + 10-indicator visual analysis (ICONOCRACIA protocol) |

General-purpose (academic + engineering): `academic-{anthropologist,geographer,historian,narratologist,psychologist}`, `engineering-{code-reviewer,codebase-onboarding,git-workflow-master,minimal-change-engineer,software-architect,technical-writer}`, `specialized-{document-generator,mcp-builder}`, `support-{analytics-reporter,executive-summary-generator}`.

---

## Skills

**Global (`~/.claude/skills/`)** — 100+ entries. Use the `find-skill` skill for fuzzy lookup; do **not** enumerate here.

Thesis-relevant defaults: `iconocracia-agent`, `corpus-scout`, `corpus-scout-workspace`, `corpus-stats`, `iconocode-analyze`, `iconocode-batch`, `validate-corpus`, `compilar-tese`, `dir410346`, `abnt-format`, `citation-management`, `citation-audit`, `claude-md`, `AutoResearchClaw` (live-symlinked from `~/Documents/GitHub/AutoResearchClaw`).

**Project (`.claude/skills/`)** — 1 entry:

| Skill | Purpose |
|---|---|
| `iconocracia-pipeline-router` | Routes ICONOCRACIA thesis work through the right pipeline stage. |

---

## Scheduled tasks (`~/.claude/scheduled-tasks/`)

9 entries. All cron-style.

| Task | Cadence (assumed) | Purpose |
|---|---|---|
| `coding-progress` | daily | Coding session summary |
| `corpus-validation` | daily | Schema-validate corpus JSONL |
| `daily-review` | daily | Personal review prompt |
| `dashboard-refresh` | daily | Rebuild thesis dashboard |
| `drift-alert` | daily | Detect drift in tracked artifacts |
| `gap-analysis` | weekly | Bibliography/coverage gap scan |
| `iconocode-backfill` | weekly | Run iconocode on un-analyzed corpus items |
| `thesis-progress-daily` | daily | Thesis chapter progress digest |
| `vault-backup` | daily | Backup Obsidian vaults |

Verify cadence in each task's `*.json`/`*.yaml` before relying on this table.

---

## Per-project `CLAUDE.md` files

8 found in workspace (max-depth 3 search):

| Path | Scope |
|---|---|
| `/Users/ana/Research/CLAUDE.md` | (To be (re)created in Sprint 4 — currently absent.) Workspace root index. |
| `hub/iconocracy-corpus/CLAUDE.md` | **Authoritative** for thesis monorepo. Dual-agent pipeline, thesis compile, webiconocracy app, Gallica MCP. |
| `apps/iconocracia-companion/CLAUDE.md` | Companion app conventions. |
| `vaults/CLAUDE.md` | Obsidian vault conventions. |
| `united-by-marriage/CLAUDE.md` | (Personal project, unrelated.) |
| `LLM Skills/Text/CLAUDE.md` | Notes-style; non-active. |
| `.worktrees/iconocracy-corpus-hub-consistency/CLAUDE.md` | Per-worktree (inherited from corpus). |
| `.worktrees/iconocracy-pr-33-sync/CLAUDE.md` | Per-worktree. |
| `.worktrees/iconocracy-main-crda-fix/CLAUDE.md` | Per-worktree. |

Convention: per-worktree `CLAUDE.md` inherits from main; cleanup is manual when the worktree merges.

**Plus** the global `~/.claude/CLAUDE.md` (user-level, all sessions) and `~/CLAUDE.md` (workspace-level, `~/`).

---

## Self-improving-agent (`/Users/ana/Research/.claude/self-improving-agent/`)

Captures tool I/O + session events into `memory/{episodic,working,semantic-patterns.json}`, looks for recurring issues, suggests learnings.

| Component | File |
|---|---|
| Pre-tool capture | `hooks/pre-tool.sh` |
| Post-Bash capture | `hooks/post-bash.sh` |
| Session-end summary | `hooks/session-end.sh` |
| Analysis script | `scripts/self_improve.py` |
| Memory store | `memory/{episodic/,working/,semantic-patterns.json}` (gitignored runtime data) |

**Status (2026-04-25):** Canonical wiring lives in `.claude/settings.json` (PreToolUse `Bash|Write|Edit`, PostToolUse `Bash`, SessionEnd `.*`, stdin-JSON invocation). The duplicate `hooks` block in `.claude/settings.local.json` was stripped in Sprint 3 (Task A) so each event fires exactly once per tool call. `SessionEnd` (not `Stop`) is correct for end-of-session summary semantics.

---

## Tools / Pipelines / Rotinas (workspace-local)

| Surface | What's there | Status |
|---|---|---|
| `Tools/lm-eval-harness/` | LLM eval harness | Standalone tool. |
| `Tools/pandoc/` | Pandoc filter / template assets | Used by `compilar-tese` skill. |
| `Tools/remote-kernel/` | Remote Jupyter kernel config | Standalone. |
| `pipelines/Atlas/` | Sub-repo (own `.git`) | Active research pipeline. |
| `pipelines/indexing/` | Sub-repo (own `.git`) | Indexing pipeline. |
| `rotinas/` | Only `(2)` duplicate stragglers (`SEMANTIC-MODEL`, `config.yml`, `daily.sh`, `weekly-synthesis.md`) | **Stale.** Originals moved to scheduled-tasks; archive in a follow-up cleanup pass. |

`rotinas/` should be archived to `archive/2026-04-25-stale/rotinas/` once references are confirmed nil.

---

## Worktrees (`.claude/worktrees/`)

4 active worktrees (gitignored as of Sprint 0):

- `confident-taussig-b0dac5/`
- `elastic-rhodes-65e8b5/`
- `gifted-antonelli-6d4405/`
- `tender-wozniak-7ffa31/`

Plus 3 older worktrees under `.worktrees/` (with their own CLAUDE.md, see table above).

**Policy:** worktrees inherit `CLAUDE.md` from their source branch; deletion is manual after merge; orphaned worktrees should be removed via `git worktree remove`, not `rm -rf`.

---

## What this index does *not* duplicate

- `~/.claude/CLAUDE.md` — global user config; reference, do not copy.
- `~/.claude/settings.json` — global hooks; only the *targets-this-repo* rows are mentioned above.
- `hub/iconocracy-corpus/CLAUDE.md` — authoritative thesis playbook; do not summarize here.
- Skill catalogs — use `find-skill` skill for discovery instead of listing all 100+ skills.

## Quick decision rules

- **New automated behavior (on every X):** add a hook in the right `settings.json` (project for project-scoped, global for cross-project). Do **not** add it in both.
- **New cross-session capability:** create a skill in `~/.claude/skills/` and reference here only if thesis-relevant.
- **New scheduled task:** add to `~/.claude/scheduled-tasks/` and add a row to the table above.
- **New project rule:** edit the relevant `CLAUDE.md`; do not invent a new one.
