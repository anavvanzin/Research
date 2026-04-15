# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Workspace purpose

`~/Research/` is the canonical root of Ana Vanzin's doctoral research ecosystem (PPGD/UFSC, thesis **ICONOCRACIA — Female Allegory in the History of Legal Culture, 19th–20th c.**). It is a **meta-workspace**, not a single codebase: it gathers several independent Git repositories under a contract of functional buckets (`hub/`, `apps/`, `pipelines/`, `labs/`, `vaults/`, `shared/`, `archive/`). See `README.md` for the canonical Workspace Index table — keep it authoritative; do not duplicate it here.

Old flat paths (`~/iconocracy-corpus`, `~/iurisvision`, `~/iconclass-data`, etc.) are now compatibility **symlinks** into `~/Research/`. They work, but new work must use the `Research/` canonical path.

## Primary repo: `hub/iconocracy-corpus`

Almost all thesis work lives here. It has its own detailed `AGENTS.md` — **always read it first when working inside the hub**. Cross-workspace facts:

- Python env: **conda `iconocracy` on Python 3.12** (`/Users/ana/.venvs/iconocracy/bin/python3.12`). Never use system Python.
- Canonical data contract: `records.jsonl` → `corpus/corpus-data.json` (145 items) → public releases. Validate after any edit:
  ```bash
  conda run -n iconocracy python tools/scripts/validate_schemas.py
  ```
- Dual-Agent Pipeline: **WebScout** (archive researcher) → **IconoCode** (visual coder, 4-stage Panofsky + purification indicators).
- Thesis compile: `make -C vault/tese/` (Pandoc) or the `compilar-tese` skill.
- Binary images belong in Google Drive, **never** in `data/raw/` — a PreToolUse hook blocks writes that try.

## Cross-workspace architecture (big picture)

Pieces share state through symlinks and the canonical JSON contract, not a single build system:

```
hub/iconocracy-corpus/          canonical source of truth (corpus, thesis, schemas)
        │
        ├── corpus/corpus-data.json     ─┐
        ├── vault/tese/                  │  consumed downstream
        └── records.jsonl               ─┘
                │
pipelines/      │
├── iconocracy-ingest   symlink → hub tracked dir; OCR + batch normalization
├── indexing            symlink → hub/indexing; search agents + Gallica MCP server
└── Atlas               symlink → hub/Atlas; iconographic analytic toolkit
                │
vaults/         │
├── iconocracy-vault    symlink → hub vault (Obsidian surface for thesis notes)
├── dir410346-vault     symlink → subdir of hub vault (disciplina)
└── dir410340-vault     symlink → subdir of hub vault (disciplina)
                │
apps/           │  read corpus-data.json / companion-data.json
├── iconocracia-companion    operational/public interface
├── iconocracia-space        Hugging Face Space (exploration)
└── webiconocracy            React+Vite+Firebase explorer (AI Studio/Gemini variant)
                │
labs/           │  exploratory, not on the canonical path
├── iurisvision             legal-vision experiments
└── iuris-visio-roadmap     planning for above
                │
shared/         │  reference data
├── iconclass-data          Iconclass ontology fork (anavvanzin)
└── iconclass-data-avmadrj  Iconclass variant (avmadrj)
```

**Git-safe phase rule**: tracked thesis content lives inside the hub. `pipelines/` and `vaults/` entries that look like directories are **symlinks into the hub**, not duplicates. Editing the symlinked path edits the hub. Don't try to initialize a separate Git repo inside a symlinked pipeline/vault.

**Archive rule**: `archive/` holds aged duplicates and retired checkouts. Read-only by convention — check the hub before reviving anything.

## Working across multiple sub-repos

- Every major sub-repo (`hub/iconocracy-corpus`, `apps/iconocracia-companion`, `apps/webiconocracy`, `pipelines/Atlas`) is its own Git repository with its own `AGENTS.md`, `package.json`, or `environment.yml`. Run commands **inside the specific sub-repo**, not at `~/Research/` root.
- Before creating a new project, decide the bucket (`apps` | `pipelines` | `labs` | `vaults` | `shared`) and add a row to the README Workspace Index. New research repos enter **only** under `~/Research/`.
- When a user request spans sub-repos, treat each as an isolated working directory (separate git status, separate env). Don't cross-commit.

## Conventions

- Citations: ABNT NBR 6023:2025.
- Iconclass code `48C51` = feminist iconography (key code for this thesis).
- Default working language: **Portuguese** for responses and thesis content; code identifiers stay in English.
- Academic voice: **criminal law history / legal iconography** — never anthropology, never sociology.
- JSON edits to corpus data: rewrite whole file with `Write` or an atomic Python script; never `sed` or partial `Edit` on large JSON.
- External APIs (Europeana, Gallica): fall back to metadata-based analysis after two failures — don't retry loops.

## Skills for this workspace

Curated skills Codex should prefer when cwd is under `~/Research/`. Sub-repos add their own catalogs; this one covers the meta-workspace.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `iconocracy-agent` | Default umbrella for thesis research — orchestrates corpus, coding, compile, progress |
| `find-skill` | Fuzzy-search installed skills by intent |
| `academic-research-skills` | 13-agent deep-research suite (lit review, writing, peer review) |
| `literature-review` | Systematic literature reviews across multiple sources |
| `compilar-tese` | Compile thesis chapters to DOCX/PDF via Pandoc |
