# Automation Surfaces — `/Users/ana/Research`

Single source of truth for *where* automation lives, *what triggers it*, and *what owns its config*. Read this before adding a new hook, skill, agent, or scheduled task.

Last reviewed: 2026-08-30.

## Scope legend

This repo is cloned into remote and web Claude Code sessions, where **only the tracked
meta-repo exists**. Surfaces that live on Ana's Mac (`/Users/ana/Research`) but are not
versioned here are marked **🖥️ host-only** and are simply absent elsewhere — that is
expected, not breakage.

| Marker | Meaning |
|---|---|
| *(unmarked)* | Versioned in this repo. Present in every session; the CI drift guard checks it. |
| 🖥️ **host-only** | Exists only on the macOS host. Absent in remote/web sessions; not checked by the drift guard. |

Do not "restore" a 🖥️ host-only surface in a remote session — it was never committed.
See **Remote / web sessions** in [`../CLAUDE.md`](../CLAUDE.md).

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

## Agents (`~/.claude/agents/`) — 🖥️ host-only

14 agents installed globally (pruned from 20 on 2026-07-27). Thesis-specific (use these for ICONOCRACIA work):

| Agent | Purpose |
|---|---|
| `abnt-checker` | ABNT NBR 6023:2025 citation lint |
| `chapter-integrity` | Mandatory terminology + citation scan before compile |
| `corpus-dedup` | Pre-save dedup check for new corpus candidates |
| `iconclass-reviewer` | Verify Iconclass notation validity |
| `iconocode` | Full Panofsky 3-level + 10-indicator visual analysis (ICONOCRACIA protocol) |
| `iconographer` | Panofsky / Warburg method review of visual analyses |
| `legal-historian` | Legal-history rigor pass (institutional / cultural / conceptual) |
| `thesis-reviewer` | Chapter review — terminology, citation format, conceptual consistency |

Academic panel: `academic-{anthropologist,geographer,historian,narratologist,peer-reviewer,psychologist}`.

---

## Skills

**Global (`~/.claude/skills/`)** — 🖥️ **host-only**. Count is host-dependent and drifts
(`AGENTS.md` recorded 594 in Jul/2026); do **not** pin a number here. Use the `find-skills`
skill for fuzzy lookup; do **not** enumerate.

**Account-synced** — in remote/web sessions the only skills available are those synced to
the Claude account (~50), plus the versioned project skills below. Plugins do **not** sync:
a `/plugin-name:command` that works on the Mac will report *Unknown command* in a remote
session unless the capability is also shipped as a versioned project skill.

Thesis-relevant defaults: `iconocracia-agent`, `corpus-scout`, `corpus-scout-workspace`, `corpus-stats`, `iconocode-analyze`, `iconocode-batch`, `validate-corpus`, `compilar-tese`, `dir410346`, `abnt-format`, `citation-management`, `citation-audit`, `claude-md`, `AutoResearchClaw` (live-symlinked from `~/Documents/GitHub/AutoResearchClaw`).

**Project (`.claude/skills/`)** — 2 versioned entries. These travel with the clone and
work in every session:

| Skill | Purpose |
|---|---|
| `iconocracia-pipeline-router` | Routes ICONOCRACIA thesis work through the right pipeline stage. |
| `scientific-writer` | General scientific writing (artigos, grants, abstracts) — entry point that routes to `academic-pipeline`, `academic-writing-reviewer`, `iconocracy-reviewer`. Thesis work delegates to the router above. |

Present in `.claude/skills/` on the Mac but **never committed**, so 🖥️ **host-only**:

| Skill | Purpose | Why uncommitted |
|---|---|---|
| `abnt-6023` | Local ABNT NBR 6023:2025 reference formatter. | Not added to git |
| `academic-research-skills` | Bundle of research helpers for academic writing. | Not added to git |
| `AutoResearchClaw` | Autonomous 23-stage research pipeline. | Live symlink to `~/Documents/GitHub/AutoResearchClaw` — inherently uncommittable |
| `hegelian-dialectic` | Dialectic argument scaffolder. | Not added to git |
| `playwright` | Playwright browser automation helpers for research capture. | Not added to git |

To make any of these work in remote sessions, commit it under `.claude/skills/`.

---

## Scheduled tasks (`~/.claude/scheduled-tasks/`) — 🖥️ host-only

13 entries. Mixed cadence (cron + session triggers).

| Task | Cadence (assumed) | Purpose |
|---|---|---|
| `coding-progress` | daily | Coding session summary |
| `corpus-validation` | daily | Schema-validate corpus JSONL |
| `daily-review` | daily | Governance-doc review + terminology sweep |
| `dashboard-refresh` | daily | Rebuild thesis dashboard |
| `drift-alert` | daily | Detect drift in tracked artifacts |
| `gap-analysis` | weekly | Bibliography/coverage gap scan |
| `iconocode-backfill` | weekly | Run iconocode on un-analyzed corpus items |
| `thesis-progress-daily` | daily | Thesis chapter progress digest |
| `vault-backup` | daily | Backup Obsidian vaults |
| `dotclaude-backup` | daily | Backup `~/.claude/` config + skills |
| `daily-corpus-context` | session-start | Inject corpus status line at session start |
| `weekly-goal-prompt` | Mon session-start | Weekly writing goal adjustment prompt |
| `researchclaw-summary` | after C5 | Prompt to review ResearchClaw candidates |

Verify cadence in each task's `*.json`/`*.yaml` before relying on this table.

---

## Per-project `CLAUDE.md` files — 🖥️ host-only (except this repo's own)

8 found in workspace (max-depth 3 search):

| Path | Scope |
|---|---|
| `/Users/ana/Research/CLAUDE.md` | Workspace root index for Claude Code sessions; defers to `hub/iconocracy-corpus/CLAUDE.md` for thesis work. |
| `hub/iconocracy-corpus/CLAUDE.md` | **Authoritative** for thesis monorepo. Dual-agent pipeline, thesis compile, Gallica MCP. (webiconocracy app retired.) |
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
| Analysis script | `.claude/self-improving-agent/scripts/self_improve.py` |
| Memory store | `memory/{episodic/,working/,semantic-patterns.json}` (gitignored runtime data) |

**Status (2026-04-25):** Canonical wiring lives in `.claude/settings.json` (PreToolUse `Bash|Write|Edit`, PostToolUse `Bash`, SessionEnd `.*`, stdin-JSON invocation). The duplicate `hooks` block in `.claude/settings.local.json` <!-- drift-pin: 2026-08-30 arquivo é gitignored, não versionado --> was stripped in Sprint 3 (Task A) so each event fires exactly once per tool call. `SessionEnd` (not `Stop`) is correct for end-of-session summary semantics.

---

## Tools / Pipelines / Rotinas (workspace-local)

| Surface | What's there | Status |
|---|---|---|
| `Tools/lm-eval-harness/` | LLM eval harness | 🖥️ host-only. Standalone tool. |
| `Tools/pandoc/` | Pandoc filter / template assets | 🖥️ host-only. Used by `compilar-tese` skill. |
| `Tools/remote-kernel/` | Remote Jupyter kernel config | 🖥️ host-only. Standalone. |
| `pipelines/Atlas/` | Sub-repo (own `.git`) | 🖥️ host-only. Active research pipeline. |
| `pipelines/indexing/` | Sub-repo (own `.git`) | 🖥️ host-only. Indexing pipeline. |
| `rotinas/` | (removed) | **Archived 2026-04-25** to `archive/2026-04-25-stale/rotinas/`. Held only `(2)` duplicate stragglers; originals had been moved earlier and no in-tree references remained. |
| `scripts/git_physics_guard.py` | Multi-harness git conflict guard | Script to prevent cross-session head contamination across checkouts. Installed via `scripts/install-hooks.sh`. ADR in `docs/decisions/2026-06-25-multi-harness-git-physics.md`. |
| `scripts/statusline.sh` + `scripts/install-statusline.sh` | Cursor CLI status line | Renders Cursor CLI session context/percent in shell prompt. Added via PR #23 (2026-07-29). |

---

## Worktrees (`.claude/worktrees/`) — 🖥️ host-only

16 active worktrees (gitignored as of Sprint 0; verified 2026-08-01). List drifts as parallel Claude sessions spawn/retire trees; run `ls .claude/worktrees/` for the live set. Sample entries: `quirky-meitner-9fce80/`, `eager-wilson-f211fb/`, `reverent-solomon-051f3c/`.

The legacy `.worktrees/` directory is empty.

**Policy:** worktrees inherit `CLAUDE.md` from their source branch; deletion is manual after merge; orphaned worktrees should be removed via `git worktree remove`, not `rm -rf`.

---

## Onboarding & Planning (docs/)

| Surface | What's there | Purpose |
|---|---|---|
| `docs/onboarding-debian12/` | Debian 12 setup manuals and install scripts | Onboarding reference and automation scripts for Debian 12 environments (PR #9). |
| `docs/superpowers/` | Creative cronjobs plans and game specs | Specifications and plans for creative cronjobs and the July "jogo-alegorias" planning (`2026-07-02-*`). |

---

## Tests / CI (versioned)

| Surface | File | Trigger | Purpose |
|---|---|---|---|
| Python syntax smoke test | `tests/test_repo_sanity.py` | `pytest` in `.github/workflows/python-package-conda.yml` (`on: [push]`) | Every tracked `.py` compiles. Also guarantees pytest collects something (empty collection = exit 5 = red build). |
| **Governance-doc drift guard** | `tests/test_docs_drift.py` | same `pytest` step | Fails the build when `CLAUDE.md`, `README.md`, `AGENTS.md`, or this file reference an in-repo path, a skill, or a count that does not exist. Enforces the **Drift protocol** in [`../AGENTS.md`](../AGENTS.md), whose `drift-detector` is 🖥️ host-only. Escape hatches: a line marked 🖥️ host-only, or carrying `<!-- drift-pin: ... -->`, is skipped. |

Removed 2026-08-30: `.github/workflows/nextjs.yml` and `.github/workflows/jekyll-gh-pages.yml` <!-- drift-pin: 2026-08-30 referência histórica; os arquivos foram deletados de propósito -->
— unmodified GitHub starter templates with no Next.js app and no Jekyll site in the repo,
both firing on every push to `main` and contending for the same `pages` concurrency group.

---

## External CI surfaces (not versioned)

Automation that posts to this repo from outside it. Nothing here lives in the tree, so the
drift guard cannot check it — and nothing here is 🖥️ host-only either, since it runs on a
third party's servers rather than on Ana's Mac. Registered so a red mark from an
unexplained source is traceable, per the **Drift protocol** in [`../AGENTS.md`](../AGENTS.md).

| Surface | Trigger | Signal | State |
|---|---|---|---|
| **Vercel Git integration** → project `anavanzin/research` | every push, all branches | legacy **commit status** (context `Vercel`), not a check run — so it is invisible to check-run APIs and to the check-suite rollup | ⚠️ see below |
| Socket Security | pull requests | check runs (`Pull Request Alerts`, `Project Report`) | active, green |
| Cursor Automation | pull requests | check run (`Find critical bugs`) | active, neutral |

### Vercel — pending removal (2026-08-30)

The project deployed this repo successfully on nearly every commit from at least
2026-07-22 to 2026-08-09, then turned red today with `"Account is blocked."`
(`research-anavanzin.vercel.app` returns HTTP 402).

It should not be connected at all: this repo has **no HTML entrypoint anywhere**, no
`package.json`, no `vercel.json`, no framework and no build output. No Root-Directory or
Output-Directory setting can produce a real site from it, so every green "Deployment has
completed" published nothing. Removal is a Vercel-dashboard action (Settings → Git →
Disconnect, or delete the project); there is nothing in this tree to change, and adding a
`vercel.json` to suppress deploys would be fighting config with config.

Two distinct problems — do not conflate them:

1. **the account block** is account-wide and affects every Vercel project on it; and
2. **this repo should not be on Vercel**, which is what removal fixes.

Disconnecting this repo does **not** lift the account block.

Update this section with the decision and its date once the disconnection is done.

---

## What this index does *not* duplicate

- `~/.claude/CLAUDE.md` — global user config; reference, do not copy.
- `~/.claude/settings.json` — global hooks; only the *targets-this-repo* rows are mentioned above.
- `hub/iconocracy-corpus/CLAUDE.md` — authoritative thesis playbook; do not summarize here.
- Skill catalogs — use `find-skills` skill for discovery instead of listing all 100+ skills.

## Quick decision rules

- **New automated behavior (on every X):** add a hook in the right `settings.json` (project for project-scoped, global for cross-project). Do **not** add it in both.
- **New cross-session capability:** create a skill in `~/.claude/skills/` and reference here only if thesis-relevant.
- **New scheduled task:** add to `~/.claude/scheduled-tasks/` and add a row to the table above.
- **New project rule:** edit the relevant `CLAUDE.md`; do not invent a new one.
- **After any Coding Agent session that edits `SKILL.md` or `CLAUDE.md`:** trigger a Code Review session to catch documentation drift before it accumulates.
