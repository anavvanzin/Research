---
id: P-2026-017
titulo: "Tese — biweekly IMES + Cap.6 (2026-06-08 → 2026-06-19)"
dominio: planejamento
status: rascunho
criado: 2026-06-05
ultimo_update: 2026-06-05
autor: Hermes (com Ana)
espelha_em: "Notion (uni account) — pending mirror"
fonte_estado:
  - /Users/ana/Research/.opencode/plans/iconocracy-priority-plan.md
  - /Users/ana/Research/hub/iconocracy-corpus/docs/superpowers/specs/2026-06-05-imes-pipeline-design.md
  - /Users/ana/Research/hub/iconocracy-corpus/docs/decisions/STATUS-2026-05-30.md
  - /Users/ana/Research/hub/iconocracy-corpus/docs/decisions/IRR-PILOTO-2026-05-30.md
  - /Users/ana/Research/hub/iconocracy-corpus/AGENTS.md
capacidade: 4-5h/dia, 4 dias úteis/semana
meta_longa: qualificação nov/2027
---

# Plano biweekly — ICONOCRACIA

**Janela:** 2026-06-08 (seg) → 2026-06-19 (sex), 2 semanas corridas.
**Cadência diária não-negociável:** 200-300 palavras de prosa acadêmica + 5-10 itens processados no IMES E1.

## Por que este recorte

Três fios abertos competem pelos mesmos 4-5h/dia:

  A. **IMES E1+E2** — design aprovado 2026-06-05. E1 (Pathosformel extraction sobre 265 itens) é o único caminho que destrava a tese quantitativa; E2 (clustering → regimes visuais) é o que gera as pranchas-atlas para o manuscrito.
  B. **Cap.6 (Análise Quantitativa)** — notebooks 01-04 já executados; tarefa é NARRAÇÃO, não pesquisa. 2-3 semanas até 12.000 palavras.
  C. **Limpeza do image-store** — 38% dos arquivos em `binaries/Images` são HTML/PDF salvos como `.jpg` (achado 2026-05-30). Bloqueia qualquer coding visual; protocolo dirigido para subset numismática (Numista/Colnect pipeline bug).

**Decisão de priorização (2026-06-05):** paralelizar A+B com cadência-âncora em B (escrita diária). C é reativa — dispara quando A bate num item não-imagem, não é semana própria.

## Semana 1 (2026-06-08 → 2026-06-12) — IMES E1 + Cap.6 §6.1

### Seg 06-08 · kick-off
  - [ ] **Cap.6** §6.1: 200-300 palavras a partir de `01_exploratory.ipynb`.
  - [ ] Verificar `~/.hermes/skills/research/iconocode-batch/` resolve.
  - [ ] Verificar `tools/scripts/iconocode_batch_runner.py` existe; se não, scaffold mínimo.
  - [ ] Dry-run E1 em 5 itens; revisar schema de `data/processed/pathosformel_index.jsonl`.

### Ter 06-09 · E1 batch 1
  - [ ] Rodar E1 em 50 itens sem `pathosformel` prévio.
  - [ ] **Cap.6** §6.1: +300 palavras. Acumulado ~600.

### Qua 06-10 · E1 batch 2 + triage store
  - [ ] Rodar E1 em mais 75 itens. Acumulado E1: ~125/265.
  - [ ] **Image-store triage (reativa):** confirmar `nao-imagens-store-2026-05-30.json`; subset numismática. NÃO re-adquirir ainda.
  - [ ] **Cap.6** §6.1: +300 palavras. Acumulado ~900.

### Qui 06-11 · E1 batch 3 + nota IRR re-run
  - [ ] Rodar E1 nos itens restantes COM imagem real. Pular os 79 não-imagens (marcar `#no-image`).
  - [ ] Escrever 1-página "IRR re-run design" (referência: `IRR-PILOTO-2026-05-30.md`) — n≥25-30, rater-2 cego, n por indicador estável.
  - [ ] **Cap.6** §6.1: +300 palavras. Acumulado ~1200.

### Sex 06-12 · E1 DoD + §6.1 fechado
  - [ ] `pathosformel_index.jsonl` com 265 linhas (79 com `#no-image`).
  - [ ] `python tools/scripts/validate_schemas.py data/processed/pathosformel_index.jsonl` passa.
  - [ ] **Cap.6** §6.1: 1500 palavras. Iniciar §6.2 se sobrar fôlego.
  - [ ] Atualizar `CHECKLIST-SEMANAL.md` (vault/candidatos/CHECKLIST-SEMANAL.md).

**DoD Semana 1:** E1 completo (§9 DoD #1 do design IMES). §6.1 = 1500 palavras.

## Semana 2 (2026-06-15 → 2026-06-19) — IMES E2 + Cap.6 §6.2-§6.3

### Seg 06-15 · E2 scaffold + seeds
  - [ ] Escrever `tools/scripts/cluster_rv.py` (design §3.6).
  - [ ] Curar 4 seeds manuais com IDs-âncora do corpus: `RV-01` Justitia Monumental · `RV-02` Marianne Republicana · `RV-03` Britannia Imperial · `RV-04` Justitia Hierática.
  - [ ] **Cap.6** §6.2: +300 palavras. Acumulado ~1800.

### Ter 06-16 · E2 first run
  - [ ] Rodar clustering; revisar `regimes_visuais.yaml` (seeds, atribuidos, pool_revisao, nao_classificados).
  - [ ] Se `pool_revisao` > 30: definir mais seeds (mitigação design §10).
  - [ ] **Cap.6** §6.2: +300 palavras. Acumulado ~2100.

### Qua 06-17 · Re-aquisição numismática
  - [ ] Re-resolver URLs Numista/Colnect para o subset numismático (estimativa 30-50 itens, não 79 avulsos).
  - [ ] Itens irrecuperáveis: marcar `#no-image-recovered` + quarentenar E1.
  - [ ] **Cap.6** §6.2: +300 palavras. Acumulado ~2400.

### Qui 06-18 · E2 final + E3 prancha 1
  - [ ] Re-rodar E2 com imagens recuperadas. Target: ≥80% atribuídos, pool ≤20.
  - [ ] Primeira prancha: copiar `templates/prancha-template.yaml` → `docs/pilots/pranchas/rv-01-justitia-monumental.yaml`. Preencher `imagens` (max 6) + `cjv_justificativa` (mín 2 crit/pair).
  - [ ] **Cap.6** §6.3: +300 palavras. Acumulado ~2700.

### Sex 06-19 · E2 DoD + prancha 1 + §6.3 fechado
  - [ ] E2 DoD: 4 seeds + ≥80% corpus atribuído (§9 DoD #2).
  - [ ] E3 DoD parcial: 1 prancha em `status: "rascunho"`. As 3 outras vão para semana 3.
  - [ ] **Cap.6** §6.3: 3000 palavras totais.
  - [ ] Atualizar `CHECKLIST-SEMANAL.md`.

**DoD Semana 2:** E2 completo. E3 começa (1 prancha). §6.3 fechado.

## Decisões pendentes da Ana (responder quando abrir no Notion)

  1. **Cadência-âncora:** confirmar — Cap.6 (200-300 palavras/dia) + E1 (5-10 itens/dia) é o equilíbrio? Ou prefere IMES-pesado (pular Cap.6 nestas 2 semanas) ou Cap.6-pesado (pular E1)?
  2. **Protocolo `#no-image`:** marcar os 79 não-imagens com `#no-image` no E1 output + quarentenar do E2 é o caminho? Ou prefere protocolo diferente (ex.: `#invalid-source` em vez de `#no-image`)?
  3. **Re-aquisição numismática:** 30-50 itens na Qua 06-17 é volume razoável? Ou prefere adiar limpeza do store e quarentenar tudo por enquanto?
  4. **Pranchas E3:** as 3 pranchas restantes (RV-02 Marianne, RV-03 Britannia, RV-04 Justitia Hierática) entram na semana 3 ou ficam para depois?

## Decisões SCOPE-EXCLUDED (não fazer nestas 2 semanas)

  - Sem expansão de Cap.2, sem escrita de Cap.3, sem refatoração Cap.4-5. (Horizonte 2 do priority plan.)
  - Sem merge de `infra/hub-consistency-refactor` (decisão tua, STATUS-2026-05-30 §2).
  - Sem revisão dos 44 SCOUT notes (decisão tua, STATUS-2026-05-30 §3).
  - Sem fix do protobufjs, sem dotfiles, sem submodule (2026-05-25 two-machine sync, ainda pending).
  - Sem push de nada. Push-to-main é gated.

## Métricas de saída (visíveis no `CHECKLIST-SEMANAL.md`)

| Métrica | Semana 1 | Semana 2 |
|---|---|---|
| E1 (pathosformel_index.jsonl linhas) | 265 | 265 |
| E2 (regimes_visuais.yaml atribuídos) | 0% | ≥80% |
| E3 (pranchas rascunho) | 0 | 1 |
| Cap.6 palavras acumuladas | 1500 | 3000 |
| Imagens re-adquiridas | 0 | 30-50 |
| `#no-image` items no E1 | 79 | 79 (estável) |

## Pontos de atenção (a checar diariamente)

  - **Cap.6 §6.1 está narrando o que os notebooks ACHARAM, não o que EU acho.** Risco: vestir teses nos dados. Fix: §6.1 cita tabelas/figuras específicas do notebook, não formulações próprias vagas.
  - **E1 LLM pode ser inconsistente entre batches.** Mitigação: revisar amostra de 10% antes de E2.
  - **Não inventar números no Cap.6.** Toda afirmação quantitativa deve ter footnote com referência ao output do notebook (célula + figura).
  - **Glossário IMES ≠ vocabulário da tese.** Pathosformel aparece na tese (Warburg), mas "Regime Visual" é constructo IMES. Cap.6 não deve "vazar" a nomenclatura interna.

## Para espelhar no Notion (uni account, ana.vanzin@posgrad.ufsc.br)

Estrutura sugerida para a página "Tese — planejamento quinzenal 2026-06-08 → 2026-06-19":

  1. Callout "Por que este recorte" (3 bullets).
  2. Callout "Cadência diária" (1 linha).
  3. Toggle "Semana 1" com checklist de 5 dias.
  4. Toggle "Semana 2" com checklist de 5 dias.
  5. Toggle "Decisões pendentes" (4 perguntas acima).
  6. Database inline "Métricas de saída" (tabela acima).
  7. Link para `Research/plans/2026-06-05-biweekly-imes-cap6.md` no vault (referência canônica local).
