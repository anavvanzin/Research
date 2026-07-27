# Automation Surfaces — `/Users/ana/Research`

Single source of truth for *where* automation lives, *what triggers it*, and *what owns its config*. Read this before adding a new hook, skill, agent, or scheduled task.

Last reviewed: 2026-07-27.

---

## Hooks (Claude Code)

| Surface | Config file | Trigger | Purpose |
|---|---|---|---|
| Self-improving-agent (project) | `.claude/settings.json` | PreToolUse Bash\|Write\|Edit, PostToolUse Bash, SessionEnd `.*` | Captures tool I/O (Bash + Write/Edit pre, Bash post) + session summaries into `.claude/self-improving-agent/memory/`. Stdin-JSON invocation; hooks scripts at `.claude/self-improving-agent/hooks/{pre-tool,post-bash,session-end}.sh`. Canonical wiring as of 2026-04-25 (`settings.local.json` `hooks` block stripped). |
| Corpus protection (global) | `~/.claude/settings.json` | PreToolUse Write, PostToolUse Edit\|Write | Blocks binary image writes into `iconocracy-corpus/data/raw/`; warns on `corpus-data.json` edits; runs `tools/scripts/validate_schemas.py` on corpus JSONL changes. Owned by global config — do not duplicate at project level. |
| Lock & Plan coordination (project) | `.claude/settings.json` (optional opt-in) | PreToolUse Edit\|Write, SessionStart, SessionEnd, UserPromptSubmit | Dev-infrastructure hooks (inert by default) to coordinate parallel sessions. Wired optionally to `task-lock-enforcer.sh`, `session-lock-awareness.sh`, `session-lock-release.sh`, and `master-plan-reminder.sh`. Lock state is tracked at `.claude/locks/`. |

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

12 entries. Mixed cadence (cron + session triggers).

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
| `daily-corpus-context` | session-start | Inject corpus status line at session start |
| `weekly-goal-prompt` | Mon session-start | Weekly writing goal adjustment prompt |
| `researchclaw-summary` | after C5 | Prompt to review ResearchClaw candidates |

Verify cadence in each task's `*.json`/`*.yaml` before relying on this table.

---

## Per-project `CLAUDE.md` files

10 entradas ativas + 1 padrão de worktree (max-depth 3 search):

| Path | Scope |
|---|---|
| `/Users/ana/Research/CLAUDE.md` | Workspace root index for Claude Code sessions; defers to `hub/iconocracy-corpus/CLAUDE.md` for thesis work. |
| `hub/iconocracy-corpus/CLAUDE.md` | **Authoritative** for thesis monorepo. Dual-agent pipeline, thesis compile, webiconocracy app, Gallica MCP. |
| `apps/iconocracia-companion/CLAUDE.md` | Companion app conventions. |
| `vaults/CLAUDE.md` | Obsidian vault conventions. |
| `united-by-marriage/CLAUDE.md` | (Personal project, unrelated.) |
| `LLM Skills/Text/CLAUDE.md` | Notes-style; non-active. |
| `scitex-python/CLAUDE.md` | Sibling repo (own `.git`). TODO: confirm scope on next review. |
| `llm-council/CLAUDE.md` | Sibling repo (own `.git`). TODO: confirm scope on next review. |
| `agi-in-md/CLAUDE.md` | Sibling repo (own `.git`). TODO: confirm scope on next review. |
| `.claude/worktrees/<name>/CLAUDE.md` | Per-worktree (inherited from main). Cleanup when worktree merges. |

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
| `rotinas/` | (removed) | **Archived 2026-04-25** to `archive/2026-04-25-stale/rotinas/`. Held only `(2)` duplicate stragglers; originals had been moved earlier and no in-tree references remained. |
| `scripts/git_physics_guard.py` | Multi-harness git conflict guard | Script to prevent cross-session head contamination across checkouts. Installed via `scripts/install-hooks.sh`. ADR in `docs/decisions/2026-06-25-multi-harness-git-physics.md`. |
| `.github/workflows/python-package-conda.yml` | Conda smoke test CI | Adicionado 2026-07 junto com `environment.yml`; roda em push/PR para validar o env `iconocracy` (PR #19-adjacente). Ver também `jekyll-gh-pages.yml`, `nextjs.yml`. |
| `environment.yml` | Conda env lockfile (root) | Pin do env `iconocracy` (Python 3.11) para o smoke test do CI. Fonte-da-verdade continua sendo o env local em `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/`. |

---

## Worktrees (`.claude/worktrees/` + `.codex/worktrees/`)

Reality mudou desde 2026-06-01: os worktrees `bold-kapitsa-1b2598/` e `quirky-meitner-9fce80/` já não existem, e a maior parte dos worktrees ativos agora vive sob `.codex/worktrees/<hash>/Research/` (ver `git worktree list`). Worktrees do Claude Code aparecem em `.claude/worktrees/<agente-adjetivo-hash>/` sob demanda.

TODO próxima revisão: rodar `git worktree list` na main tree e reconciliar a lista abaixo.

**Policy (inalterada):** worktrees inherit `CLAUDE.md` from their source branch; deletion is manual after merge; orphaned worktrees should be removed via `git worktree remove`, not `rm -rf`.

---

## Onboarding & Planning (docs/)

| Surface | What's there | Purpose |
|---|---|---|
| `docs/onboarding-debian12/` | Debian 12 setup manuals and install scripts | Onboarding reference and automation scripts for Debian 12 environments (PR #9). |
| `docs/superpowers/` | Creative cronjobs plans and game specs | Specifications and plans for creative cronjobs and the July "jogo-alegorias" planning (`2026-07-02-*`). |
| `docs/CONFLUENCIA-REPOSITORIOS-2026-07-13.md` | Auditoria de confluência entre os 9 repositórios ICONOCRACIA | PR #20 (mergeado 2026-07-13). Registra 8 prioridades — ver item #8 sobre padronização da glosa `hardening` como acompanhamento explícito de `ENDURECIMENTO` em textos em inglês. |
| `plans/2026-07-13-weekly-audit.md` | Relatório semanal automático | Gerado pela weekly-audit scheduled task (PR #21). Convém confirmar registro dela em `~/.claude/scheduled-tasks/` — TODO para próxima revisão. |
| `.planning/2026-06-30-brainstorming-retrospective/` | Retrospectiva dos 11 specs de brainstorming | Diretório oculto, não indexado no README. Não editar sem contexto (é registro histórico). |

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
- **After any Coding Agent session that edits `SKILL.md` or `CLAUDE.md`:** trigger a Code Review session to catch documentation drift before it accumulates.
