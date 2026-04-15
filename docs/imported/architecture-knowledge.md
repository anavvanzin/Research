---
type: imported-note
title: ICONOCRACY Knowledge Architecture
source_path: /Users/ana/Documents/Claude/Projects/PhD project (1)/ICONOCRACY-knowledge-architecture.md
status: active
created: 2026-04-15
---

# ICONOCRACY Knowledge Architecture

## Purpose

This note captures the working architecture for the thesis knowledge system.

## Design principles

1. One source of truth per data type.
2. Fast capture, gradual structuring.
3. Trilateral traceability: raw image, Obsidian note, master record.
4. Git as backbone for text, data, and code.
5. No Notion in the active workflow.

## Canonical ownership

- Corpus notes: Obsidian vault
- Research notes: Obsidian vault
- Thesis drafts: Obsidian vault + Google Drive copies
- Bibliography: Zotero + exported `.bib`
- Raw images: external SSD / manifests only in git
- Master records: `data/processed/records.jsonl`
- Code and scripts: `tools/` and ingest pipeline
- Session memory: local Claude memory

## Vault structure

The proposed vault layout is:

- `00-inbox/`
- `01-corpus/`
- `02-pesquisa/`
- `03-escrita/`
- `04-metodologia/`
- `05-projeto/`
- `06-derivados/`
- `07-referencias/`
- `assets/`
- `templates/`

## Sync flows

### Vault -> JSONL

`vault-to-jsonl.py` is the bridge from SCOUT notes to `records.jsonl`.

### Zotero -> vault

Zotero exports feed the reference notes and the thesis bibliography.

### Vault -> Drive

Drafts and deliveries can be exported to Google Drive for advisor-facing copies.

## Why it matters

This is the clearest statement of how the thesis system is meant to work end-to-end.
