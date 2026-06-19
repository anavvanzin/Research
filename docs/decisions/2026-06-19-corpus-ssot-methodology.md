---
tags: [meta, decision, pointer, corpus, data-methodology]
date: 2026-06-19
scope: meta-workspace awareness
canonical_home: hub/iconocracy-corpus/docs/decisions/2026-06-19-ssot-apparatus-critico-design.md
---

# Ponteiro — Metodologia de dados do corpus (SSOT via aparato crítico)

> Doc canônico vive no sub-repo: `hub/iconocracy-corpus/docs/decisions/2026-06-19-ssot-apparatus-critico-design.md`
> Decidido via dialética: `hub/iconocracy-corpus/docs/decisions/dialectic-ssot-2026-06-19/`
> PR: `anavvanzin/iconocracy-corpus#90`

Este ponteiro existe para que **todo agente do meta-workspace** (os de `cowork/`, crons, ferramentas externas como Antigravity) conheça as regras canônicas de dado do corpus antes de tocá-lo.

## Decisão (resumo)
O corpus Iconocracia é um **artefato hermenêutico versionado** governado por **disciplina de aparato crítico**: a verdade canônica = sequência de **releases git congelados** (snapshot + aparato de codificação + dataset card). **Git é o log de eventos.** Um DB de consulta é **índice derivado opcional (DuckDB), nunca o mestre**.

## Regras operacionais para TODOS os agentes (previnem erros reais de 2026-06-19)
1. **`origin/main` é canônico** (records.jsonl=308 / corpus-data.json=309). Clones locais podem ser **forks stale** — SEMPRE `git fetch origin` e comparar com `origin/main` ANTES de agir sobre qualquer contagem. Nunca confiar em contagem local.
2. **`corpus-data.json` é EXPORT derivado** de `records.jsonl` (via `records_to_corpus.py`). Editá-lo direto é efêmero (regenerado). Mude o mestre e reexporte. **NUNCA `records_to_corpus.py --replace`** (remove `id`/`country`/`support`); use o modo default (merge).
3. **Quarentena/uncoded JÁ EXISTE** — `tools/scripts/tag_uncoded_purification.py` + `data/processed/purification-manifest.json` + `docs/decisions/quarantine-uncoded-2026-05-30.json`. Não reinventar. Eixo de validade = `coded_by`; ler `docs/decisions/*` PRIMEIRO.
4. `endurecimento_score=0` é **score válido** (baixa purificação), não "uncoded". N analítico = só codificados (~223), nunca 309.
5. Há **automação (crons/worktrees)** que apaga arquivos untracked no working tree do main local. Trabalhar via branch/worktree isolado e PR; não confiar em arquivos untracked persistirem.

## Próximo (Phase 0 do plano do sub-repo)
Reconciliar o fork local ↔ `origin/main`=309 antes de congelar o primeiro release. Operação planejada, com aval da Ana — não bulldoze.
