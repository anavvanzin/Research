# CLAUDE.md — `/Users/ana/Research`

Meta-workspace root for Ana Vanzin's ICONOCRACIA doctoral research.
This file is for Claude Code sessions; the human-readable counterpart is
[`README.md`](README.md).

> Global config: `~/.claude/CLAUDE.md` (always loaded). This file does **not**
> duplicate it — read it for user profile, environment, harness rules, citation
> defaults, conda env, caveman mode, etc.

## Workspace shape

This is a **meta-workspace, not a monorepo.** Only versions meta files
(`cowork/`, `docs/`, `.claude/AUTOMATION.md`, `.gitignore`). Sub-repos are
siblings with their own `.git`.

```
/Users/ana/Research/      ← THIS REPO (git: anavvanzin/Research)
├── cowork/               ← 85 agentes + 12 integrações + opencode.json
├── docs/                 ← seminários, protótipos
├── .claude/              ← AUTOMATION.md + self-improving-agent + skills
├── .opencode/            ← plans/iconocracy-priority-plan.md
├── hub/
│   ├── iconocracy-corpus/ ← thesis monorepo (git: anavvanzin/iconocracy-corpus)
│   └── mnemosyne-scout/   ← scout staging area (no .git)
├── apps/                  ← iconocracia-companion, iconocracia-db, iconocracia-space
├── pipelines/             ← Atlas, indexing (sibling sub-repos)
├── vaults/                ← Obsidian vaults (dir410340/346, iconocracy)
├── shared/                ← iconclass-data, the-book-of-secret-knowledge
├── deep-memory/           ← own .git
├── hermes-workspace/      ← own .git
└── labs/                  ← experimental sub-repos
```

## Primary surface: the thesis

**`hub/iconocracy-corpus/`** is the canonical thesis monorepo.
Navigate: `cd hub/iconocracy-corpus`

Quick paths (from `hub/iconocracy-corpus/`):

| What | Path |
| --- | --- |
| Capítulos da tese | `vault/tese/` |
| Manuscrito + revisões | `tese/{manuscrito,revisoes}/` |
| Entrega mais recente | `tese/Entrega_Orientador_Mar2026_FINAL/` |
| Corpus canônico | `corpus/corpus-data.json` (264 itens) |
| Notebooks | `notebooks/` (01–08) |
| Compilação | `make -C vault/tese/` |

## Sibling repos

- `deep-memory/` — Persistent-memory agent (own `.git`)
- `hermes-workspace/` — Hermes experimental workspace (own `.git`)
- `apps/iconocracia-companion/` · `apps/iconocracia-db/` · `apps/iconocracia-space/`
- `pipelines/Atlas/` · `pipelines/indexing/`
- `vaults/` — Obsidian vaults (see `vaults/CLAUDE.md`)
- `shared/` — shared datasets and reference libraries

## Automation

Single index: → **[`.claude/AUTOMATION.md`](.claude/AUTOMATION.md)**

## Workflow Specifications

ICONOCRACY pipeline workflows (W1–W6 + S1–S5) are documented in `Specs/WORKFLOW-*.md`:

| File | Content |
| --- | --- |
| `Specs/WORKFLOW-REGISTRY.md` | Master index: all workflows, item lifecycle, gate checklist |
| `Specs/WORKFLOW-iconocracy-corpus-acquisition.md` | W1: Gallica → vault → ledger |
| `Specs/WORKFLOW-iconocracy-visual-analysis.md` | W2: Panofsky + ENDURECIMENTO scoring |
| `Specs/WORKFLOW-iconocracy-synchronization.md` | W3: records.jsonl → vault → corpus-data.json → HF |
| `Specs/ZOTERO-MCP-SETUP-STATUS.md` | Zotero MCP troubleshooting (setup broken, use Web API fallback) |

These are the authoritative process docs — update them when the pipeline changes.

## Conventions (workspace-specific)

- **Sub-repo containment.** Only `cowork/` and `docs/` are tracked here.
  Do NOT run `git add` on anything else from this repo.
- **conda env:** `iconocracy` (Python 3.12). Never system Python.
- **ABNT NBR 6023:2025** for Portuguese drafts; Chicago for English.
- **Caveman mode** active by default (`~/.caveman-active`); `stop caveman` per session.
- Always confirm path before creating new files.

## What this file does *not* cover

- User profile, plan tier → `~/.claude/CLAUDE.md`
- Workspace-level layout → `~/Documents/CLAUDE.md`
- Thesis pipeline internals → `hub/iconocracy-corpus/CLAUDE.md`
- Skill catalog → `find-skill` skill
