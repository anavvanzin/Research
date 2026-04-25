# CLAUDE.md — `/Users/ana/Research`

Workspace root for Ana Vanzin's research meta-workspace. This file is for Claude Code sessions; the human-readable counterpart is [`README.md`](README.md).

> Global config: `~/.claude/CLAUDE.md` (always loaded). This file does **not** duplicate it — read it for user profile, environment, harness rules, citation defaults, conda env, caveman mode, etc.

## Workspace shape

This is a **meta-workspace, not a monorepo.** The repo at `/Users/ana/Research/` only versions workspace-level meta files (this file, `README.md`, `.claude/AUTOMATION.md`, `.gitignore`). Sub-repos live in gitignored buckets and have their own `.git`.

```
/Users/ana/Research/
├── hub/                   # 1 sub-repo: iconocracy-corpus (THE THESIS)
├── apps/                  # 3 sub-repos: iconocracia-companion, -space, -db
├── pipelines/             # 2 sub-repos: Atlas, indexing
├── labs/                  # 3 sub-repos: iurisvision, iuris-visio-roadmap, browser-harness
├── vaults/                # tracked: iconocracy/dir410346/dir410340 vaults + own .git
├── shared/                # 3 sub-repos: iconclass-data(-avmadrj), the-book-of-secret-knowledge
├── archive/               # historical / stale (gitignored)
├── Books/                 # PDF library (gitignored)
├── Cotutela/              # cotutela admin (gitignored)
├── .claude/               # automation surfaces — see .claude/AUTOMATION.md
└── (top-level note dirs: Plans/, Specs/, LLM Skills/, Text/, Ideas/, Code/, etc., all gitignored)
```

## Primary surface: the thesis

**`hub/iconocracy-corpus/`** is the canonical thesis monorepo and has its own authoritative `CLAUDE.md` — defer to it for thesis work.

Quick paths (Portuguese, intentional):

| What | Path |
| --- | --- |
| Capítulos da tese | `hub/iconocracy-corpus/vault/tese/` |
| Manuscrito + revisões | `hub/iconocracy-corpus/tese/{manuscrito,revisoes}/` |
| Entrega mais recente | `hub/iconocracy-corpus/tese/Entrega_Orientador_Mar2026_FINAL/` |
| Corpus canônico | `hub/iconocracy-corpus/corpus/corpus-data.json` (165 itens) |
| Notebooks estatísticos | `hub/iconocracy-corpus/notebooks/` (01–04) |
| Compilação | `make -C hub/iconocracy-corpus/vault/tese/` ou skill `compilar-tese` |

Symlinks at root for fast access: `iconocracy-corpus → hub/iconocracy-corpus`, `iconocracia-companion → apps/iconocracia-companion`.

## Secondary surfaces (active, recently touched)

| Dir | Purpose | Has `.git` |
| --- | --- | --- |
| `agency-agents/` | Agent definitions destined for `~/.claude/agents/` | yes |
| `agent-thesis/` | TS agent for thesis-related tasks (`data/processed/records.jsonl` = 165 items) | yes |
| `hermes-workspace/`, `hermes-agent-camel/` | Conversational/experimental agents | yes |
| `deep-memory/` | Persistent-memory agent | yes |
| `ml-intern/` | ML intern dev work | yes |
| `openclaw/`, `alignment-for-honesty/`, `united-by-marriage/` | Other active sub-repos | yes |

These live at root for ergonomic access. They are **not** tracked by the meta-workspace repo (gitignored individually in `.gitignore`).

## Where to put new work

| New thing | Goes in |
| --- | --- |
| New paper PDF | `Books/` |
| New experiment / playground | `labs/` (clone as new sub-repo) |
| New ingest/processing pipeline | `pipelines/` (sub-repo) |
| New Obsidian note | `vaults/<vault-name>/` |
| New skill (cross-session) | `~/.claude/skills/` (global) |
| New agent | `~/.claude/agents/` (global), prototype optionally in `agency-agents/` |
| New thesis-pipeline router | `.claude/skills/iconocracia-pipeline-router/` (project skill) |
| New automated behavior | A hook in `~/.claude/settings.json` (cross-project) or `.claude/settings.json` (project). Document in `.claude/AUTOMATION.md`. |
| New scheduled task | `~/.claude/scheduled-tasks/` |
| New per-project rule | Edit the relevant `CLAUDE.md`. Do not invent new ones. |

## Automation

Single index of every hook, skill, agent, scheduled task, per-project `CLAUDE.md`, and worktree:

→ **[`.claude/AUTOMATION.md`](.claude/AUTOMATION.md)**

Read it before adding anything to `.claude/`. It also flags current tech debt (e.g. assumed-but-unverified cron cadences in the scheduled-tasks table).

## Conventions (workspace-specific)

- **Sub-repo containment.** `apps/`, `pipelines/`, `labs/`, `vaults/`, `hub/`, `shared/`, `ml-intern/`, etc. are gitignored *individually*. Do not nested-track sub-repos. Do not run `git add` from the meta-workspace on anything inside these dirs.
- **`compilar-tese` skill, not Tools/.** Thesis compile uses the global skill. `Tools/pandoc/` holds template assets only.
- **Stale duplicate cleanup.** Files with `(2)` suffix are usually stragglers from prior cleanups. Safe to delete after confirming the original landed elsewhere.
- **Worktrees in `.claude/worktrees/`** are gitignored. Inherit `CLAUDE.md` from source branch. Removed via `git worktree remove`, not `rm -rf`.
- **PDFs at root** (`ICONOCRACIA — *.pdf`) are referenced from `Plans/`, `Specs/`, `LLM Skills/Text/`. Do not move without a ref-update pass.

## Convention reminders (echoes from global)

- Caveman mode active by default (`~/.caveman-active`); `stop caveman` per session.
- Conda env `iconocracy` (Python 3.12 at `/Users/ana/.venvs/iconocracy/bin/python3.12`) — never system Python.
- ABNT NBR 6023:2025 for Portuguese drafts; Chicago for English.
- Always confirm path before creating new files; default to current project, never `/Users/` or `$HOME`.
- Iconclass code `48C51` = feminist iconography.

## What this file does *not* cover

- User profile, plan tier, language preferences → `~/.claude/CLAUDE.md`.
- Workspace-level (`~/`) layout, git/auth, external API fallbacks → `~/CLAUDE.md`.
- Thesis pipeline internals, dual-agent flow, webiconocracy app, Gallica MCP → `hub/iconocracy-corpus/CLAUDE.md`.
- Skill catalog → `find-skill` skill.
- Per-project rules (companion app, vaults, etc.) → respective `CLAUDE.md` files.
