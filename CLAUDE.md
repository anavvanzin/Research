# CLAUDE.md — `/home/ana/Documents/projetos/research`

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
/home/ana/Documents/projetos/research/  ← THIS REPO (git: anavvanzin/Research)
├── cowork/               ← 85 agentes + 12 integrações + opencode.json
├── docs/                 ← seminários, protótipos
├── .claude/              ← AUTOMATION.md + self-improving-agent + skills
├── .opencode/            ← plans/iconocracy-priority-plan.md
├── hub/
│   └── iconocracy-corpus/ ← thesis monorepo (git: anavvanzin/iconocracy-corpus)
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

## Automation

Single index: → **[`.claude/AUTOMATION.md`](.claude/AUTOMATION.md)**

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
