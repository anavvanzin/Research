# Brainstorming Retrospective — Todos os 11 Specs

**Criado:** 2026-06-30
**Autor:** Safo (Hermes Agent)
**Perfil:** Ana Vanzin — PPGD/UFSC, tese ICONOCRACIA
**Status:** Em construção

---

## Tese

Catalogar, avaliar e planejar o estado de implementação de todos os 11 specs de brainstorming produzidos entre abril e junho de 2026, identificando o que está implementado, o que está pendente, o que foi arquivado, e quais dependências cruzadas existem entre eles.

---

## Os Fios (agrupamento por dependência, não cronológico)

### Grupo A — Infraestrutura & Tooling (fundacional)

| Fase | Spec | Data | Status |
|------|------|------|--------|
| 1 | Skill Discovery — Path Z | 2026-04-14 | `completed` — implementado e verificado |
| 2 | Cronjob Orchestration Layer | 2026-04-28 | `partial` — implementado via cron nativo, 3 jobs pausados |
| 3 | Two-Machine Reconciliation | 2026-05-25 | `pending` — runbook aprovado, execução incerta |
| 4 | Honcho Memory Activation | 2026-06-07 | `resolved` — peer card povoado organicamente, seeder redundante |
| 5 | Zettelkasten Triagem | 2026-06-05 | `partial` — Zettelkasten criado, vaults 13→7, fases F2/F4/F5/F6 incertas |
| 6 | Corpus Inventory | 2026-04-29 | `completed` — scripts existem, verificar se CSV atualizado |
| 7 | New Corpus Statistical Analysis (05–07) | 2026-04-17 | `completed` — notebooks existem, precisam re-run com N=328 |
| 8 | IRR Calculation | 2026-05-24 | `completed` — script existe, verificar se precisa re-run |
| 9 | Reliability Audit / IconoCode | 2026-06-19 | `pending` — draft-for-review, CRÍTICO |
| 10 | Research Wing | 2026-06-23 | `pending` — design aprovado, pré-implementação |
| 11 | Atlas Iconocrático v2 | 2026-06-24 | `pending` — decisões locked, timeline apertado |

### Grupo B — Corpus & Data Quality

| Fase | Spec | Data | Status |
|------|------|------|--------|
| 6 | Corpus Inventory | 2026-04-29 | `completed` |
| 7 | New Corpus Statistical Analysis (05–07) | 2026-04-17 | `completed` |
| 8 | IRR Calculation | 2026-05-24 | `completed` |
| 9 | Reliability Audit / IconoCode | 2026-06-19 | `pending` — CRÍTICO |

### Grupo C — Superfícies Públicas

| Fase | Spec | Data | Status |
|------|------|------|--------|
| 10 | Research Wing | 2026-06-23 | `pending` |
| 11 | Atlas Iconocrático v2 | 2026-06-24 | `pending` |

---

## Cadência-âncora

Este plano é retrospectivo + prospersivo. Não tem cadência recorrente — é um snapshot de estado que deve ser consultado antes de iniciar qualquer implementação dos specs pendentes.

---

## Fases Detalhadas

### Fase 1 — Skill Discovery — Path Z
**Status:** `completed`
**Especificação:** `/Users/ana/Research/archive/zombies-2026-06-07/Specs/2026-04-14-skill-discovery-design.md`
**Resumo:** Catálogo curado de skills em CLAUDE.md/AGENTS.md (max 10 entradas) + skill `find-skill` com fuzzy search via ripgrep.
**Decisões chave:** Manual curation (não auto-gerado); sem DB/ML; drift tolerável.
**Estado atual:** IMPLEMENTADO (verificado 2026-06-30). O skill `find-skill` está referenciado no AGENTS.md atual como rota primária de descoberta. Os blocos `## Skills for this workspace` existem em múltiplos AGENTS.md.
**Próximo passo:** Nenhum — funcional. Manter curadoria dos blocos em revisões periódicas.

---

### Fase 2 — Cronjob Orchestration Layer
**Status:** `archived`
**Especificação:** `/Users/ana/Research/archive/zombies-2026-06-07/Specs/2026-04-28-cronjob-orchestration-design.md`
**Resumo:** Camada de automação 24/7 com 6 cron jobs Hermes (C1–C6) + 3 tarefas contextuais Claude (T1–T3). Custo alvo $6–10/mês.
**Decisões chave:** Hermes executa+reporta (custa tokens); Claude lembra+pergunta (custa atenção); C2 semanal (não diário) para não gerar ansiedade.
**Estado atual:** PARCIALMENTE IMPLEMENTADO VIA CRON NATIVO HERMES (verificado 2026-06-30). O Hermes `cronjob` tool tem 6 jobs iconocracy ativos correspondentes a C1–C6:
- C1 corpus-validation-watchdog (diário 06:00) — ATIVO, status ok
- C2 iconocracy-thesis-digest (segundas 08:00) — ATIVO, mas último run com erro de delivery (Telegram ConnectError)
- C3 iconocracy-vault-health (diário 22:00) — PAUSADO desde 2026-06-04, status error
- C4 iconocracy-infra-check (diário 05:00) — PAUSADO desde 2026-06-04, status error
- C5 iconocracy-external-scan (quartas 09:00) — ATIVO, status ok
- C6 iconocracy-feminist-network (domingos 10:00) — ATIVO, status ok
- C1 original (iconocracy-corpus-check, job_id 5ce9c89899dc) — PAUSADO, status error

Design NÃO foi superseded — foi implementado via cron nativo do Hermes. Spec arquivado pode ser marcado como implementado.
**Próximo passo:** Diagnosticar e reiniciar os 3 jobs pausados (subagente em background). Resolver erro de delivery Telegram no C2.

**Diagnóstico completo (2026-06-30):**
- **CAUSA RAIZ (3 jobs):** `RuntimeError: Failed to initialize OpenAI client: No module named 'openai'` — módulo `openai` ausente do Python env que o Hermes usa para cron agent. Os scripts rodam fine (exit 0); o erro é no runtime do agente, não no script.
- **FIX ÚNICO:** `pip install openai` no env que o Hermes usa para cron.
- **Job 1 (corpus-check):** Script roda, reporta WARNING — 41 records sem `purificacao` + 4 duplicate hashes. Problema de dados, não de código.
- **Job 2 (infra-check):** Script roda, reporta CDP offline + LiteLLM offline + disco 2.1% livre (CRÍTICO). Alertas reais.
- **Job 3 (vault-health):** Script roda mas output vazio — VAULT hardcoded em `/Users/ana/Research/vaults` (inexistente). Precisa update para path real.
- **FIX SCRIPT-LEVEL:** Atualizar `VAULT` em `iconocracy_vault_health.py` para path correto.
- **DISCO:** 2.1% livre é CRÍTICO — pode ter contribuído para falhas originais.

---

### Fase 3 — Two-Machine Reconciliation
**Status:** `pending`
**Especificação:** `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-05-25-two-machine-reconciliation-design.md`
**Resumo:** Reconciliação MacBook ↔ Linux VAIO (Debian 13) via git hubs (nunca direto). Track 1: iconocracy-corpus repo (snapshot → safety branch → push → ff-only pull). Track 2: dotfiles via GNU stow (common/linux/macos packages).
**Decisões chave:** 4 invariantes (no direct sync, ff-only, safety branch, no cross-OS state); conda envs não sincronizados; SSH keys não sincronizados.
**Estado atual:** Runbook aprovado. Execução incerta — MEMORY.md menciona "Two doctoral disciplines in 2026.1" sugerindo Mac ativo, mas não há confirmação de que o VAIO foi reconciliado.
**Próximo passo:** Verificar `git log --oneline` do iconocracy-corpus no Mac para confirmar se reconciliation foi executada. Se não, executar Phase 1 do runbook.

---

### Fase 4 — Honcho Memory Activation
**Status:** `pending`
**Especificação:** `/Users/ana/.hermes/docs/superpowers/specs/2026-06-07-honcho-memory-activation-design.md`
**Resumo:** Ativar Honcho como backend de peer-card para memória do Hermes. Seeder one-shot lê MEMORY.md e USER.md, splita por `§`, chama `honcho_conclude` com idempotência via `honcho_search` pre-check.
**Decisões chave:** One-way seed (local → Honcho); sem sync two-way; workspace `iconocracy-thesis`, peer `ana`; rollback simples (deletar block `honcho:`); ~15 min, ~25 API calls.
**Estado atual:** PARCIALMENTE RESOLVIDO ORGANICAMENTE (verificado 2026-06-30). `honcho_profile(peer='user')` retorna 20+ facts ativos cobrindo identidade, role, metodologia, interesses, conceitos, citações, toolset, website. O seeder script é REDUNDANTE — o peer card já está povoado. O spec pode ser marcado como resolvido sem necessidade do seeder one-shot.
**Próximo passo:** Marcar spec como parcialmente resolvido. O seeder não é mais necessário. Considerar atualizar spec para documentar que povoamento orgânico via uso do Hermes supriu a necessidade.

---

### Fase 5 — Zettelkasten Triagem
**Status:** `pending`
**Especificação:** `/Users/ana/Research/docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md`
**Resumo:** Consolidar 13 vaults Obsidian em 1 Zettelkasten canônico (`~/Zettelkasten/`). 6 fases: F1 snapshot archive → F2 reconcile corpus copies → F3 scaffold → F4 review per-source → F5 discard orphans → F6 decide Research root. Estimado 8–15h em 10–15 sessões.
**Decisões chave:** "Serve para tese?" como critério operacional; sem novos plugins até quali (Nov 2027); notas atomizadas com timestamp IDs; F4 é a long tail.
**Estado atual:** PARCIALMENTE EXECUTADO (verificado 2026-06-30). `~/Zettelkasten/` EXISTE. Vaults Obsidian reduzidos de 13 para 7 — consolidação parcial foi feita. F1 (snapshot archive) e F3 (scaffold) provavelmente completos. F2 (reconcile corpus copies), F4 (review per-source), F5 (discard orphans), F6 (decide Research root) — estado incerto.
**Próximo passo:** Verificar conteúdo de `~/Zettelkasten/` (quantas notas, estrutura de pastas). Determinar quais fases F2–F6 ainda pendentes. Atualizar spec com estado real.

---

### Fase 6 — Corpus Inventory
**Status:** `pending`
**Especificação:** `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-04-29-corpus-inventory-design.md`
**Resumo:** Extrair metadados neutros de todos os arquivos SCOUT-*.md do vault/candidatos para CSV estruturado. Campos: SCOUT ID, Title, Country, Century, Medium, Figure type, Iconclass, Promoted?. Sem interpretação — extração pura.
**Decisões chave:** Escopo limitado a extração (análise é fase separada); arquivos ZW incluídos mas flagados.
**Estado atual:** IMPLEMENTADO (verificado 2026-06-30). Scripts `inventory_corpus.py` e `inventory_report.py` existem em `tools/scripts/`. DRIFT: spec referencia 288 SCOUT files; atual = 303 SCOUT-*.md files (vault/candidatos). records.jsonl tem 328 linhas. Corpus cresceu ~14% desde o spec.
**Próximo passo:** Verificar se CSV output está atualizado com N=303. Se não, re-executar `inventory_corpus.py`. Marcar spec como implementado.

---

### Fase 7 — New Corpus Statistical Analysis (05–07)
**Status:** `archived`
**Especificação:** `/Users/ana/Research/archive/zombies-2026-06-07/Specs/2026-04-17-new-corpus-analysis-design.md`
**Resumo:** Três notebooks Jupyter: 05_temporal (dinâmica temporal, barras empilhadas por regime, heatmap país×década), 06_clustering (Ward + K-means, silhouette, Cramér's V, teste sem monocromatizacao), 07_dimensionality (PCA, scree, loadings, biplot).
**Decisões chave:** Análise temporal é ilustrativa (não inferencial) devido a selection bias; clustering testa com e sem monocromatizacao; PCA usa StandardScaler.
**Estado atual:** IMPLEMENTADO ANTES DO ARQUIVAMENTO (verificado 2026-06-30). Notebooks 05_temporal, 06_clustering, 07_dimensionality, 08_multidimensional_scoring TODOS existem em `notebooks/`. DRIFT GRAVE: notebooks rodaram com N=165 (hardcoded em markdown cells); records.jsonl atual = 328. O corpus quase dobrou. Output figures existem em disco (timestamp 2026-06-24 14:56–15:01) mas células foram cleared. O CSV intermediário (`corpus_dataset.csv`) tem 165 rows e está stale.
**Próximo passo:** Re-executar notebooks com N=328. Workflow: (1) regenerar corpus_dataset.csv de records.jsonl, (2) atualizar N hardcoded em markdown cells de 05/06/07, (3) rodar 05→06→07→08 em sequência (08 depende de 07), (4) verificar figuras regeneradas. Atualizar Cap 6 da tese se conclusões mudarem.

---

### Fase 8 — IRR Calculation
**Status:** `pending`
**Especificação:** `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-05-24-irr-calculation-design.md`
**Resumo:** Script `calculate_irr.py` lê ratings humanos (records.jsonl, key `purificacao`) vs sintéticos (irr_pilot_synthetic_results.jsonl), calcula Krippendorff's Alpha ordinal por indicador + pooled, loga discrepâncias (diff ≥ 2) com justificativa LLM.
**Decisões chave:** Ordinal metric; pooled alpha via 2×(10×N) matrix; log file overwrite (não append); flags `--mock` e `--verbose`.
**Estado atual:** IMPLEMENTADO (verificado 2026-06-30). `calculate_irr.py` existe em `tools/scripts/`. O spec foi implementado. Pode ter sido superseded pelo spec mais recente (Fase 9 — Reliability Audit), que é uma versão mais robusta do mesmo problema (inter-rater validity + inter-instrument consistency).
**Próximo passo:** Determinar relação com Fase 9 — o IRR Calculation é subset do Reliability Audit? Se sim, consolidar documentação. Verificar se `calculate_irr.py` precisa re-run com N atual.

---

### Fase 9 — Reliability Audit / IconoCode
**Status:** `pending`
**Especificação:** `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/decisions/2026-06-19-reliability-audit-design.md`
**Resumo:** Auditoria de confiabilidade em duas camadas a partir de amostra estratificada unificada (n≈50). Layer 1: Ana codifica blind (image-only, ordem aleatória) → concordância human×opus e human×4.6. Layer 2: justifica merge opus×4.6. Regra: α ≥ 0.667 → merge N≈145; senão fallback N≈100.
**Decisões chave:** n=50 dos 100 opus items (baseline já existe); estratificado por regime × endurecimento_score band; 3 comparações de 1 amostra; protocolo blind (image-only, no prior scores); capture out-of-band em arquivo separado.
**Estado atual:** Draft-for-review. Depende de Phase 0 (canonical corpus) e acesso às imagens. Não executado.
**Próximo passo:** Rever spec com Ana. Definir se n=50 é factível dado tempo. Verificar acesso às imagens (Google Drive). Este é o spec mais complexo e mais importante para a validade quantitativa da tese.

---

### Fase 10 — Research Wing
**Status:** `pending`
**Especificação:** `/Users/ana/Research/apps/iconocracia-research/project-docs/2026-06-23-research-wing-design.md`
**Resumo:** App React (Vite + React 18 + React Router 6) para conteúdo público da tese: thesis hub, visual essays, publications, reading room, symbol canvas, object dossiês. Bilingue PT/EN. Fonts self-hosted (Cormorant Garamond, Hanken Grotesk, JetBrains Mono). Palette Iuris Memoria com light/cabinet themes.
**Decisões chave:** PT primário / EN secundário via localStorage; two-tier visual (Chrome = motion premium, Core editorial = austero); assets do atlaslab; placeholders para unlicensed images.
**Estado atual:** Design aprovado, pré-implementação. Next steps: scaffold → port data → implement components → build routes → polish → deploy.
**Próximo passo:** Iniciar scaffold. Este spec é independente dos demais — pode ser executado em paralelo.

---

### Fase 11 — Atlas Iconocrático v2
**Status:** `pending`
**Especificação:** `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-06-24-atlas-v2-design.md`
**Resumo:** Hybrid two-layer: A. Mnemosyne Viva (black bg, draggable specimen cards, curved Nachleben filiation lines, A0 PDF export per prancha) + B. Cartografia Iconocrática (mapa Leaflet/D3-geo, timeline 1559–1992, pins by location, filters by Pathosformel). Stack: Cloudflare Worker + R2 + KV; corpus.jsonld immutable, pranchas.jsonld mutable. Vanilla JS (no React).
**Decisões chave:** Specimen (atom) + Prancha (publication) many-to-many; Pathosformel organiza browsing, Nachleben organiza panel space; vanilla JS não React; aesthetics warburgian (black bg, gold/seal, Instrument Serif + Crimson Pro); deadlines v0=2026-07-15, v1 público=2026-08-30.
**Estado atual:** Decisões locked. Pre-implementation. Roadmap definido.
**Próximo passo:** Iniciar scaffold do Cloudflare Worker + R2 + KV. Verificar se `atlaslab` repo tem código reaproveitável. Timeline apertado — v0 em 15 dias.

---

## Dependências Cruzadas

```
Fase 1 (Skill Discovery) ──────── COMPLETED (sem dependentes)
Fase 2 (Cronjob Orch) ──────────── ARCHIVED (verificar supersession)
Fase 3 (Two-Machine Sync) ──────── PENDING (pré-requisito para trabalho no VAIO)
Fase 4 (Honcho Memory) ────────── PENDING (independente)
Fase 5 (Zettelkasten) ──────────── PENDING (independente, mas F2 depende de F3)
Fase 6 (Corpus Inventory) ──────── PENDING (independente)
Fase 7 (Statistical Analysis) ──── ARCHIVED (DRIFT: N=165 vs 299 atual)
Fase 8 (IRR Calculation) ──────── PENDING (subset de Fase 9?)
Fase 9 (Reliability Audit) ─────── PENDING (CRÍTICO para validade quantitativa)
Fase 10 (Research Wing) ───────── PENDING (independente)
Fase 11 (Atlas v2) ─────────────── PENDING (independente, timeline apertado)
```

**Dependência chave:** Fase 8 pode ser subset de Fase 9. Se confirmado, consolidar.
**Dependência chave:** Fase 5 (Zettelkasten) F2 (reconcile corpus copies) depende de Fase 3 (Two-Machine Sync) estar executada.
**Sem dependências:** Fases 4, 6, 10, 11 são independentes e podem ser executadas em paralelo.

---

## Decisões Pendentes

1. **Fase 2 vs sistema de cron do Hermes:** O design original previa 6 jobs C1–C6 no Hermes layer. O Hermes agora tem `cronjob` tool nativa. O design ainda é relevante ou foi superseded?
2. **Fase 8 vs Fase 9:** IRR Calculation (F8) é subset do Reliability Audit (F9)? Consolidar em um spec único?
3. **Fase 7 — notebooks 05–07:** Foram implementados e arquivados, ou nunca executados? Se executados com N=165, precisam re-run com N=299?
4. **Fase 5 — Zettelkasten:** O cenário de 13 vaults ainda é atual? Re-executar diagnóstico?
5. **Prioridade relativa:** Qual das fases pendentes é mais urgente para a tese?

---

## Scope-Excluded

- Este plano NÃO cobre specs produzidos após 2026-06-24.
- Este plano NÃO inclui planos de implementação detalhados (são produzidos pelo skill `writing-plans` quando cada fase é ativada).
- Este plano NÃO substitui os specs originais — é um índice executivo com estado.

---

## Riscos

| Risco | Mitigação |
|-------|-----------|
| DRIFT: specs referenciam N=165/288, corpus atual=299/357 | Atualizar contagens antes de executar qualquer spec de análise |
| Fase 9 (Reliability Audit) é a mais complexa e crítica | Não iniciar sem revisão completa do spec com Ana |
| Fase 11 (Atlas v2) tem deadline v0=2026-07-15 (15 dias) | Verificar se deadline ainda é viável |
| Fase 7 arquivada pode ter sido executada parcialmente | Verificar existência dos notebooks antes de decidir |
| Fase 3 (Two-Machine Sync) pode estar parcialmente executada | Verificar git log antes de assumir pendência |

---

## Métricas de fim-de-plano

- [ ] Todos os 11 specs catalogados com estado atual verificado (não assumido)
- [ ] Dependências cruzadas mapeadas
- [ ] Drift de N identificado e documentado em cada spec afetado
- [ ] Decisões pendentes resolvidas ou escaladas para Ana
- [ ] Plano de ação para próximas 4 semanas definido