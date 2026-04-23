# Tasks

> PhD ICONOCRACIA — Ana Vanzin (PPGD/UFSC)
> Last updated: 2026-04-15

## In Progress

- [ ] Redação dos capítulos da tese (Partes I–IV, 9 capítulos + Atlas Iconocrático de 8 painéis)
- [ ] Resolver flags `[VERIFICAR]` em documentos da tese (ex.: Goodrich 2017 "Imago Decidendi" paginação)
- [x] ~~Completar `notion_sync.py` (records.jsonl → Notion DB1)~~ — LEGADO: Notion não é mais workspace ativo (Obsidian é). Material existente mantido como referência.

## Pending

- [ ] Deploy Cloudflare Pages do companion (`wrangler deploy` com autenticação browser no primeiro run)
- [ ] Finalizar build do `gallica-mcp-server` (TypeScript MCP: schemas, tools, src/index.ts, README)
- [ ] Redigir textos Zwischenraum para os painéis do Atlas
- [ ] Configurar três Claude Projects separados para as disciplinas ativas

## Infrastructure (ULTRAPLAN-2026-04-16 — archived)

- [x] Sprint 0: Push hub (49 commits → 0) — completed 2026-04-22
- [x] Sprint 0: Push Research meta-workspace — completed
- [x] Sprint 0: Verify companion remote — exists at `anavvanzin/iconocracia-companion`
- [x] Sprint 1: .gitignore updated (compilacao-*, staging logs, loose files)
- [x] Sprint 1: Commit working tree (4 modified + vault content + artefact cleanup)
- [x] Sprint 2.1: ICONOCRACY_MASTER_PROMPT.md — exists and current
- [x] Sprint 2.2: docs/OPERATING_MODEL.md — exists and current
- [x] Sprint 2.3: skill v2 installed at `~/.claude/skills/iconocracy-agent/`
- [x] Sprint 3.1: notion_sync.py — marked legacy (Notion → Obsidian migration)
- [x] Sprint 3.2: DM-001 API key audit — no exposed keys in current workflows (all use `secrets.*`)
- [x] Sprint 3.3: DM-002 feminist_network — actively used by `extract_feminist_network.py` and documented
- [ ] Sprint 3.4: apps/iconocracia-space origin — NOT A SEPARATE REPO (subdir of Research); no action unless user wants to extract it
- [ ] Sprint 3.5: Weekly backup automation — not configured yet

## Courses (concurrent)

- [ ] DIR410340 — Direito Administrativo Digital
- [ ] DIR410346 — História do Direito Penal
- [ ] DIR510212 — Métodos e Metodologias

## Completed

- [x] Introdução e Capítulo 1 redigidos e revisados
- [x] Apêndice A (protocolo de codificação) reconstruído como rascunho
- [x] Companion app (dashboard interativo com diário, mini-atlas, export Obsidian) construído
- [x] KV namespace `iconocracia-diary` criado no Cloudflare
- [x] SSD externo Kingston XS1000R configurado (`/Volumes/ICONOCRACIA`)
