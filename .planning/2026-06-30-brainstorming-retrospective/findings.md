# Findings — Brainstorming Retrospective

**Sessão:** 2026-06-30
**Fonte:** 11 design specs produzidos entre 2026-04-14 e 2026-06-24

---

## Spec 1 — Skill Discovery — Path Z (2026-04-14)

**Problema:** Skills sprawl — centenas de skills, difícil localizar a certa.
**Abordagem:** Catálogo curado em CLAUDE.md/AGENTS.md (max 10) + skill `find-skill` com fuzzy search (ripgrep + scoring in-memory).
**Trade-offs:** Curadoria manual (não auto-gerado); sem DB/ML; drift tolerável porque find-skill cobre lacunas.
**Estado:** IMPLEMENTADO. `find-skill` referenciado no AGENTS.md atual. Blocos `## Skills for this workspace` presentes em múltiplos níveis.

---

## Spec 2 — Cronjob Orchestration Layer (2026-04-28)

**Problema:** Automatizar monitoramento do pipeline ICONOCRACIA 24/7 para reduzir carga cognitiva.
**Abordagem:** 6 cron jobs Hermes (C1 validação corpus diário, C2 thesis digest semanal, C3 vault health diário, C4 infra check diário, C5 ResearchClaw semanal, C6 48C51 semanal) + 3 tarefas contextuais Claude (T1–T3). Estado em `~/.hermes/cron-cache/iconocracy-jobs.yaml`.
**Trade-offs:** Hermes executa+reporta (tokens); Claude lembra+pergunta (atenção); C2 semanal para não gerar ansiedade.
**Estado:** ARQUIVADO em zombies-2026-06-07. Hermes agora tem `cronjob` tool nativa — design pode estar superseded.

---

## Spec 3 — Two-Machine Reconciliation (2026-05-25)

**Problema:** MacBook retornou do conserto; Linux VAIO tornou-se ativo. Reconciliar e estabelecer sync contínuo.
**Abordagem:** Track 1: iconocracy-corpus repo via git hub (snapshot → safety branch → push → ff-only pull). Track 2: dotfiles via GNU stow (common/linux/macos packages).
**Trade-offs:** 4 invariantes (no direct sync, ff-only, safety branch, no cross-OS state); conda envs e SSH keys não sincronizados.
**Estado:** Runbook aprovado. Execução incerta.

---

## Spec 4 — Honcho Memory Activation (2026-06-07)

**Problema:** 3 sistemas de memória no Hermes, só local MD funciona. Honcho peer card vazio. MEMORY.md 91% cheio, USER.md 99%.
**Abordagem:** Ativar Honcho como backend de peer-card. Seeder one-shot: lê MD files, splita por `§`, chama `honcho_conclude` com idempotência via `honcho_search` pre-check.
**Trade-offs:** One-way seed (local → Honcho); sem two-way sync; rollback simples; ~15 min, ~25 API calls.
**Estado:** Draft, não implementado via seeder. Honcho está ativo em modo hybrid — peer card pode estar povoado organicamente.

---

## Spec 5 — Zettelkasten Triagem (2026-06-05)

**Problema:** 13 vaults Obsidian no sistema. 3 são cópias divergentes do corpus. 1 ativo em ~/Downloads (1032 notes, sem git). Root ~/Research atua como container vault (6714 notes) com sub-vaults — fonte de divergência silenciosa.
**Abordagem:** Consolidar em 1 Zettelkasten canônico (`~/Zettelkasten/`). 6 fases: snapshot archive → reconcile corpus → scaffold → review per-source → discard orphans → decide Research root. Estimado 8–15h em 10–15 sessões.
**Trade-offs:** "Serve para tese?" como critério; sem novos plugins até quali Nov 2027; notas atomizadas com timestamp IDs; F4 é a long tail.
**Estado:** Aprovado, não executado.

---

## Spec 6 — Corpus Inventory (2026-04-29)

**Problema:** Extrair metadados neutros de SCOUT-*.md para CSV de análise de padrões.
**Abordagem:** Python script parseia YAML frontmatter → CSV. Campos: SCOUT ID, Title, Country, Century, Medium, Figure type, Iconclass, Promoted?.
**Trade-offs:** Extração pura (sem interpretação); ZW files incluídos mas flagados.
**Estado:** Draft. DRIFT: spec refere 288 SCOUT files; atual = 357 (132 promovidas, 199 pendentes, 360 total no vault).

---

## Spec 7 — New Corpus Statistical Analysis 05–07 (2026-04-17)

**Problema:** Preencher lacunas dos 4 notebooks existentes (01–04) com análise temporal, clustering e PCA para Cap 6.
**Abordagem:** 05_temporal (barras por regime, heatmap país×década, timeline por medium), 06_clustering (Ward + K-means, silhouette k=2..8, Cramér's V, recluster sem monocromatizacao), 07_dimensionality (PCA, scree, loadings, biplot por regime).
**Trade-offs:** Temporal é ilustrativo (não inferencial) devido a selection bias; clustering testa com e sem monocromatizacao; PCA usa StandardScaler.
**Estado:** ARQUIVADO. DRIFT GRAVE: N=165 no spec vs 299 atual. Verificar se notebooks existem.

---

## Spec 8 — IRR Calculation (2026-05-24)

**Problema:** Calcular IRR entre coder humano (Ana) e sintético (Gemini 1.5 Pro) nos 10 indicadores de endurecimento.
**Abordagem:** Script `calculate_irr.py` lê records.jsonl (purificacao) vs irr_pilot_synthetic_results.jsonl, calcula Krippendorff's Alpha ordinal por indicador + pooled, loga discrepâncias ≥ 2.
**Trade-offs:** Ordinal metric; pooled via 2×(10×N) matrix; log overwrite; flags --mock e --verbose.
**Estado:** Under review. POSSIVELMENTE SUBSET do Spec 9 (Reliability Audit). Verificar consolidação.

---

## Spec 9 — Reliability Audit / IconoCode (2026-06-19)

**Problema:** Corpus codificado por 2 instrumentos disjuntos (iconocode-opus 100 items + iconocode-opus-4.6 45 items, zero overlap). Merge N≈145 injustificado sem evidência de validade (human×AI) ou consistência (opus×4.6).
**Abordagem:** Amostra estratificada n≈50 dos 100 opus items. Layer 1: Ana codifica blind (image-only) → concordância human×opus e human×4.6. Layer 2: justifica merge opus×4.6. Regra: α ≥ 0.667 → merge; senão fallback N≈100.
**Trade-offs:** 3 comparações de 1 amostra; protocolo blind (no prior scores); capture out-of-band; se falhar, N≈100 ainda sustenta tese.
**Estado:** Draft-for-review. CRÍTICO para validade quantitativa da tese. Depende de acesso às imagens.

---

## Spec 10 — Research Wing (2026-06-23)

**Problema:** App React para conteúdo público da tese: thesis hub, visual essays, publications, reading room, symbol canvas, object dossiês. Bilingue PT/EN.
**Abordagem:** Vite + React 18 + React Router 6. Componentes shared (NavBar, Kicker, Figure, Prose, MarginNote, ObjectDossier, SymbolCanvas). Data model em ES module (`content.js`).
**Trade-offs:** PT primário / EN via localStorage; two-tier visual (Chrome = motion, Core = austero); fonts self-hosted; assets do atlaslab.
**Estado:** Design aprovado, pré-implementação. Independente.

---

## Spec 11 — Atlas Iconocrático v2 (2026-06-24)

**Problema:** 3 superfícies legacy (atlas/, atlas-lab/, canvas/) nenhuma é atlas warburgiano verdadeiro. Canvas é boa síntese mas não permite compor constelações.
**Abordagem:** Hybrid two-layer. A. Mnemosyne Viva: black bg, draggable specimen cards, curved Nachleben filiation lines, A0 PDF export per prancha. B. Cartografia Iconocrática: mapa Leaflet/D3-geo, timeline 1559–1992, pins by location, filters by Pathosformel.
**Trade-offs:** Specimen + Prancha many-to-many; vanilla JS (no React); Cloudflare Worker + R2 + KV; aesthetics warburgian; deadlines v0=2026-07-15, v1=2026-08-30.
**Estado:** Decisões locked. Pre-implementation. Timeline apertado.

---

## Análise Cross-Cutting

### Maturidade

| Estado | Specs |
|--------|-------|
| Implementado | 1 (Skill Discovery) |
| Arquivado | 2 (Cronjob Orch), 7 (Statistical Analysis) |
| Draft/Draft-for-review | 4 (Honcho), 6 (Corpus Inventory), 8 (IRR), 9 (Reliability Audit) |
| Aprovado, pré-impl | 3 (Two-Machine), 5 (Zettelkasten), 10 (Research Wing), 11 (Atlas v2) |

### Drift de Dados

| Spec | N referenciado | N atual | Drift |
|------|---------------|---------|-------|
| 6 (Inventory) | 288 SCOUT files | 357 (360 total) | +24% |
| 7 (Statistical) | 165 items | 299 records | +81% |
| 8 (IRR) | N não especificado | 299 | — |
| 9 (Reliability) | 100 opus + 45 opus-4.6 | 299 total (287 codificados) | Verificar |

### Timeline

```
Abril  ──── Skill Discovery (14) ── Statistical Analysis (17) ── Cronjob Orch (28) ── Corpus Inventory (29)
Maio   ──── IRR Calculation (24) ── Two-Machine Sync (25)
Junho  ──── Zettelkasten (05) ── Honcho (07) ── Reliability Audit (19) ── Research Wing (23) ── Atlas v2 (24)
```

### Clusters Temáticos

1. **Infraestrutura:** 1, 2, 3, 4, 5 (tooling, sync, memory, knowledge mgmt)
2. **Dados:** 6, 7, 8, 9 (inventory, analysis, IRR, reliability)
3. **Superfícies:** 10, 11 (public-facing apps)

### Prioridade Sugerida (para Ana decidir)

| Prioridade | Spec | Justificativa |
|-----------|------|---------------|
| CRÍTICA | 9 (Reliability Audit) | Sem validação, N≈145 é injustificado — toda análise quantitativa da tese depende disso |
| ALTA | 11 (Atlas v2) | Deadline v0=2026-07-15 (15 dias) |
| ALTA | 6 (Corpus Inventory) | Mecânico, ~30min, base para outras análises |
| MÉDIA | 10 (Research Wing) | Independente, pode rodar em paralelo |
| MÉDIA | 5 (Zettelkasten) | Long tail (F4), mas F1+F2+F3+F5 em ~2h |
| MÉDIA | 3 (Two-Machine) | Pré-requisito para trabalho no VAIO |
| BAIXA | 4 (Honcho) | Honcho já ativo organicamente |
| BAIXA | 7 (Statistical) | Arquivado, precisa reavaliação |
| BAIXA | 8 (IRR) | Possível subset de 9 |
| RESOLVER | 2 (Cronjob) | Verificar supersession pelo cron nativo |
| RESOLVER | 1 (Skill Discovery) | Já funciona, só curadoria |