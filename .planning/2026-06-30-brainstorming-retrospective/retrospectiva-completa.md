# Retrospectiva de Brainstorming — 11 Specs ICONOCRACIA

**Data:** 2026-06-30
**Autoria:** Safo (Hermes Agent) + Ana Vanzin
**Perfil:** glm-5.2:cloud via Hermes Agent
**Local:** `/Users/ana/Research/.planning/2026-06-30-brainstorming-retrospective/`

---

## 1. O que fizemos

Inventariamos todos os 11 specs de brainstorming produzidos entre abril e junho de 2026 para a tese ICONOCRACIA (PPGD/UFSC). Para cada spec, verificamos in loco — não por Assunção — o estado real de implementação. O resultado mudou drasticamente o quadro: o que parecia um acúmulo de 10 specs pendentes é, na verdade, 7 specs já implementados (parcial ou totalmente) e apenas 4 realmente pendentes.

---

## 2. Estado Real Verificado dos 11 Specs

### Grupo A — Infraestrutura & Tooling

#### Spec 1 — Skill Discovery — Path Z (2026-04-14)
- **Status:** COMPLETO
- **O que era:** Catálogo curado de skills em AGENTS.md (max 10 entradas) + skill `find-skill` com fuzzy search via ripgrep.
- **Estado verificado:** `find-skill` ativo e referenciado no AGENTS.md atual. Blocos `## Skills for this workspace` presentes em múltiplos níveis.
- **Próximo passo:** Nenhum. Manter curadoria periódica dos blocos.

#### Spec 2 — Cronjob Orchestration Layer (2026-04-28)
- **Status:** PARCIALMENTE IMPLEMENTADO
- **O que era:** 6 cron jobs Hermes (C1–C6) + 3 tarefas contextuais Claude para monitoramento 24/7 do pipeline.
- **Estado verificado:** Implementado via cron nativo do Hermes (`cronjob` tool). 6 jobs iconocracy ativos:
  - C1 corpus-validation-watchdog (diário 06:00) — ATIVO, ok
  - C2 iconocracy-thesis-digest (segundas 08:00) — ATIVO, erro de delivery Telegram
  - C3 iconocracy-vault-health (diário 22:00) — PAUSADO desde 2026-06-04
  - C4 iconocracy-infra-check (diário 05:00) — PAUSADO desde 2026-06-04
  - C5 iconocracy-external-scan (quartas 09:00) — ATIVO, ok
  - C6 iconocracy-feminist-network (domingos 10:00) — ATIVO, ok
- **Diagnóstico dos 3 jobs pausados (2026-06-30):**
  - **Causa raiz comum:** `RuntimeError: Failed to initialize OpenAI client: No module named 'openai'` — módulo `openai` ausente do Python env que o Hermes usa para cron agent. Os scripts rodam fine (exit 0); o erro é no runtime do agente LLM, não no script.
  - **Fix único:** `pip install openai` no env correto.
  - **Job 1 (corpus-check):** Script roda, reporta WARNING — 41 records sem `purificacao` + 4 duplicate hashes. Problema de dados.
  - **Job 2 (infra-check):** Script roda, reporta CDP offline + LiteLLM offline + **disco 2.1% livre (CRÍTICO)**. Alertas reais.
  - **Job 3 (vault-health):** Script roda mas output vazio — VAULT hardcoded em `/Users/ana/Research/vaults` (inexistente). Drift de path. Precisa update para `~/Obsidian/vida-os`.

#### Spec 3 — Two-Machine Reconciliation (2026-05-25)
- **Status:** PENDENTE (manual-only)
- **O que era:** Reconciliação MacBook ↔ Linux VAIO via git hubs. Track 1: iconocracy-corpus repo. Track 2: dotfiles via GNU stow.
- **Estado verificado:** Git log do Mac mostra commits recentes (último: 9d4c503). Estado no VAIO incerto — requer acesso à outra máquina.
- **Próximo passo:** Verificar se o VAIO ainda é usado. Se não, marcar como não-aplicável.

#### Spec 4 — Honcho Memory Activation (2026-06-07)
- **Status:** RESOLVIDO ORGANICAMENTE
- **O que era:** Ativar Honcho como backend de peer-card, com seeder one-shot lendo MEMORY.md e USER.md.
- **Estado verificado:** `honcho_profile(peer='user')` retorna 20+ facts ativos (identidade, role, metodologia, interesses, conceitos, toolset, website). O peer card foi povoado organicamente via uso do Hermes. O seeder script é redundante.
- **Próximo passo:** Marcar spec como resolvido. Seeder não é mais necessário.

#### Spec 5 — Zettelkasten Triagem (2026-06-05)
- **Status:** PARCIALMENTE EXECUTADO
- **O que era:** Consolidar 13 vaults Obsidian em 1 Zettelkasten canônico (`~/Zettelkasten/`). 6 fases: F1 snapshot → F2 reconcile corpus → F3 scaffold → F4 review per-source → F5 discard orphans → F6 decide Research root.
- **Estado verificado:** `~/Zettelkasten/` EXISTE. Vaults Obsidian reduzidos de 13 para 7. F1 (snapshot archive) e F3 (scaffold) provavelmente completos. F2, F4, F5, F6 — estado incerto.
- **Próximo passo:** Verificar conteúdo de `~/Zettelkasten/` (quantas notas, estrutura). Determinar fases pendentes.

### Grupo B — Corpus & Data Quality

#### Spec 6 — Corpus Inventory (2026-04-29)
- **Status:** COMPLETO
- **O que era:** Extrair metadados neutros de SCOUT-*.md para CSV estruturado.
- **Estado verificado:** Scripts `inventory_corpus.py` e `inventory_report.py` existem em `tools/scripts/`. Drift: spec referia 288 SCOUT files; atual = 303.
- **Próximo passo:** Verificar se CSV output está atualizado com N=303. Se não, re-executar.

#### Spec 7 — New Corpus Statistical Analysis 05–07 (2026-04-17)
- **Status:** IMPLEMENTADO, PRECISA RE-RUN
- **O que era:** Três notebooks: 05_temporal, 06_clustering, 07_dimensionality (+ 08_multidimensional_scoring adicionado depois).
- **Estado verificado:** Todos os 4 notebooks existem em `notebooks/`. DRIFT GRAVE:
  - Notebooks rodaram com **N=165** (hardcoded em markdown cells de 05, 06, 07).
  - `records.jsonl` atual = **328**. O corpus quase dobrou.
  - Output cells foram cleared; figuras existem em disco (timestamp 2026-06-24 14:56–15:01).
  - CSV intermediário (`corpus_dataset.csv`) tem 165 rows — stale.
- **Próximo passo:** Re-executar com N=328. Workflow: (1) regenerar corpus_dataset.csv, (2) atualizar N hardcoded, (3) rodar 05→06→07→08 em sequência, (4) verificar figuras. Atualizar Cap 6 se conclusões mudarem.

#### Spec 8 — IRR Calculation (2026-05-24)
- **Status:** COMPLETO
- **O que era:** Script `calculate_irr.py` para Krippendorff's Alpha entre coder humano e sintético.
- **Estado verificado:** `calculate_irr.py` existe em `tools/scripts/`. Provavelmente subset do Spec 9 (Reliability Audit).
- **Próximo passo:** Determinar relação com Spec 9. Verificar se precisa re-run com N atual.

#### Spec 9 — Reliability Audit / IconoCode (2026-06-19)
- **Status:** PENDENTE — CRÍTICO
- **O que era:** Auditoria de confiabilidade em duas camadas (validade human×AI + consistência opus×4.6) com amostra estratificada n≈50. Regra: α ≥ 0.667 → merge N≈145; senão fallback N≈100.
- **Estado verificado:** Draft-for-review. Não executado. É o spec mais importante para a validade quantitativa da tese — sem ele, o merge N≈145 é injustificado.
- **Problema adicional descoberto:** 41 records sem `purificacao` no corpus — drift de schema que afeta diretamente este spec.
- **Próximo passo:** Rever spec com Ana. Definir se n=50 é factível. Verificar acesso às imagens (Google Drive).

### Grupo C — Superfícies Públicas

#### Spec 10 — Research Wing (2026-06-23)
- **Status:** PENDENTE
- **O que era:** App React (Vite + React 18) para conteúdo público da tese: thesis hub, visual essays, publications, reading room, symbol canvas, object dossiês. Bilingue PT/EN.
- **Estado verificado:** Design aprovado, pré-implementação. Independente dos demais specs.
- **Próximo passo:** Iniciar scaffold (Vite + React 18 + React Router 6).

#### Spec 11 — Atlas Iconocrático v2 (2026-06-24)
- **Status:** PENDENTE — DEADLINE APERTADO
- **O que era:** Hybrid two-layer: A. Mnemosyne Viva (black bg, draggable specimen cards, curved Nachleben filiation lines, A0 PDF export) + B. Cartografia Iconocrática (mapa Leaflet/D3-geo, timeline 1559–1992, pins by location). Stack: Cloudflare Worker + R2 + KV. Vanilla JS.
- **Estado verificado:** Decisões locked. Pre-implementation. Deadlines: v0=2026-07-15, v1 público=2026-08-30.
- **Próximo passo:** Iniciar scaffold do Cloudflare Worker. Timeline apertado — 15 dias para v0.

---

## 3. Problemas Descobertos Durante a Auditoria

Três problemas que não estavam em nenhum spec mas foram revelados pelo diagnóstico:

### 3.1. Disco 2.1% livre — EMERGÊNCIA
- Descoberto pelo script `iconocracy_infra_check.py` (Job 2).
- Pode ter contribuído para as falhas originais dos cron jobs em 2026-06-04.
- **Ação:** Verificar e liberar espaço imediatamente.

### 3.2. 41 records sem `purificacao` — DRIFT DE SCHEMA
- Descoberto pelo script `iconocracy_corpus_check.py` (Job 1).
- 41 records em `records.jsonl` não têm o dict `purificacao` — afeta diretamente o Reliability Audit (Spec 9).
- Também: 4 duplicate `item_hash` values.
- **Ação:** Investigar quais records estão incompletos. Decidir se são itens não-codificados ou drift de schema.

### 3.3. Notebooks com N=165 vs corpus=328 — ANÁLISE DESATUALIZADA
- Todos os notebooks 05–08 rodaram com N=165.
- O corpus quase dobrou desde então (165 → 328).
- O CSV intermediário (`corpus_dataset.csv`) está stale.
- Toda a análise quantitativa do Cap 6 está desatualizada.
- **Ação:** Regenerar CSV, re-rodar notebooks, verificar se conclusões mudam.

---

## 4. Drift de Dados — Resumo

| Spec | N referenciado | N atual | Drift |
|------|---------------|---------|-------|
| Spec 6 (Inventory) | 288 SCOUT files | 303 SCOUT files | +5% |
| Spec 7 (Statistical) | 165 items | 328 records | +99% |
| Spec 9 (Reliability) | 100 opus + 45 opus-4.6 | 328 total (236 com purification) | Verificar |
| records.jsonl | — | 328 linhas | — |
| purification.jsonl | — | 236 linhas | — |
| vault/candidatos SCOUT-*.md | — | 303 arquivos | — |

---

## 5. Dependências Cruzadas

- Spec 8 (IRR Calculation) é provavelmente subset do Spec 9 (Reliability Audit) — consolidar.
- Spec 5 (Zettelkasten) F2 (reconcile corpus copies) depende de Spec 3 (Two-Machine Sync).
- Specs 4, 6, 10, 11 são independentes — podem executar em paralelo.
- Spec 7 (notebooks) depende de regeneração do CSV — tarefa mecânica.
- Spec 9 (Reliability Audit) depende de resolver os 41 records sem `purificacao` primeiro.

---

## 6. Plano de Ação Sugerido

| Prioridade | Ação | Esforço | Tipo |
|-----------|------|---------|------|
| URGENTE | Verificar/liberar espaço em disco (2.1% livre) | 5 min | Operacional |
| URGENTE | `pip install openai` + atualizar path em vault_health.py + reativar 3 cron jobs | 10 min | Operacional |
| ALTA | Regenerar corpus_dataset.csv com N=328 e re-rodar notebooks 05→06→07→08 | 30-60 min | Análise |
| ALTA | Investigar 41 records sem `purificacao` + 4 duplicate hashes | 30 min | Data quality |
| ALTA | Decidir sobre Reliability Audit (Spec 9) — gargalo científico | Decisão Ana | Decisão |
| MÉDIA | Iniciar scaffold do Atlas v2 (Spec 11) — deadline 15 dias | Decisão Ana | Implementação |
| MÉDIA | Iniciar scaffold do Research Wing (Spec 10) | Decisão Ana | Implementação |
| BAIXA | Verificar fases pendentes do Zettelkasten (Spec 5) | 15 min | Verificação |
| BAIXA | Verificar estado do VAIO para Two-Machine Sync (Spec 3) | Decisão Ana | Verificação |

---

## 7. Arquivos Produzidos

```
/Users/ana/Research/.planning/2026-06-30-brainstorming-retrospective/
├── task_plan.md   — 11 fases com estado verificado, dependências, riscos
├── findings.md    — resumos estruturados de cada spec + análise cross-cutting
└── progress.md    — log completo da sessão + audit-fix pipeline
```

---

## 8. Spec Index (caminhos originais)

| # | Spec | Caminho |
|---|------|---------|
| 1 | Skill Discovery | `/Users/ana/Research/archive/zombies-2026-06-07/Specs/2026-04-14-skill-discovery-design.md` |
| 2 | Cronjob Orchestration | `/Users/ana/Research/archive/zombies-2026-06-07/Specs/2026-04-28-cronjob-orchestration-design.md` |
| 3 | Two-Machine Reconciliation | `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-05-25-two-machine-reconciliation-design.md` |
| 4 | Honcho Memory Activation | `/Users/ana/.hermes/docs/superpowers/specs/2026-06-07-honcho-memory-activation-design.md` |
| 5 | Zettelkasten Triagem | `/Users/ana/Research/docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md` |
| 6 | Corpus Inventory | `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-04-29-corpus-inventory-design.md` |
| 7 | Statistical Analysis 05–07 | `/Users/ana/Research/archive/zombies-2026-06-07/Specs/2026-04-17-new-corpus-analysis-design.md` |
| 8 | IRR Calculation | `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-05-24-irr-calculation-design.md` |
| 9 | Reliability Audit | `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/decisions/2026-06-19-reliability-audit-design.md` |
| 10 | Research Wing | `/Users/ana/Research/apps/iconocracia-research/project-docs/2026-06-23-research-wing-design.md` |
| 11 | Atlas Iconocrático v2 | `/Users/ana/Research/copilot-worktrees/iconocracy-corpus/anavvanzin-legendary-funicular/docs/superpowers/specs/2026-06-24-atlas-v2-design.md` |

---

*Documento gerado em 2026-06-30 por Safo (Hermes Agent) para Ana Vanzin.*