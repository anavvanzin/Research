# Revisão de Confluência entre Repositórios — ICONOCRACIA

**Data:** 2026-07-13 · **Escopo:** 9 repositórios `anavvanzin/*` da constelação de pesquisa · **Fonte canônica:** `iconocracy-corpus`

> Objetivo: mapear onde os repositórios *convergem* (mesmos dados, conceitos e fatos)
> e onde *divergem*, para que as superfícies públicas não contradigam a tese nem
> umas às outras. Esta revisão **não altera dados canônicos** — apenas diagnostica.

---

## 1. Mapa da constelação

| Repositório | Papel | Registro | Fonte de dados |
|---|---|---|---|
| **iconocracy-corpus** | Monorepo canônico da tese (corpus, manuscrito, notebooks, tools) | acadêmico | **canônico** (`records.jsonl`) |
| **Research** | Meta-workspace (agentes, docs, automação, planos) | operacional | — |
| **atlaslab** | Site público *Iuris Memoria* — Atlas da Pesquisa + Atlas Lab | público/divulgação | amostra própria (`data.js`, `corpus.jsonld`) |
| **mnemosyne-viva** | `iconocracia.com` — casa editorial do acervo | público/acervo | export enriquecido (`corpus-data-enriched.json`) |
| **atlas-celeste** | Quadro-jogo interno "O Grande Jogo das Alegorias" (Julho/2026) | planejamento interno | referencia o N do corpus |
| **artigos** | Artigos derivados (bruxa/*Malleus*; réplica involuntária) | acadêmico | reusa corpus + apparatus |
| **arno-dal-ri-site** | Sítio do orientador (Prof. Arno Dal Ri Jr.) | institucional | — |
| **grupoiusgentium.com.br** | Site do Grupo Ius Gentium (UFSC) | institucional | — |
| **ai-agent-notes** | Notas sobre construção de agentes de IA | técnico/lateral | — |

**Três anéis de confluência:**
1. **Anel da tese** — `iconocracy-corpus` (núcleo) → `atlaslab`, `mnemosyne-viva`, `atlas-celeste`, `artigos` (derivados que consomem corpus + apparatus).
2. **Anel institucional** — `arno-dal-ri-site` ↔ `grupoiusgentium.com.br` (mesmas pessoas, grupo, ORCID, UFSC/PPGD).
3. **Anel de método/tooling** — `Research` + `ai-agent-notes` (infra e automação, sem dado de corpus).

---

## 2. O que converge bem (confluência saudável)

- **Método iconométrico** — os **10 indicadores de endurecimento** (ordinais 0–3) aparecem idênticos em todas as superfícies (desincorporação, rigidez postural, dessexualização, uniformização facial, heraldicização, enquadramento arquitetônico, apagamento narrativo, monocromatização, serialidade, inscrição estatal).
- **Regimes iconocráticos** — `fundacional → normativo → militar (+ contra-alegoria)` consistentes em `mnemosyne/stats.json`, `atlaslab` e canônico.
- **Terminologia central** — *ENDURECIMENTO* mantido em português/maiúsculas; os 3 conceitos autorais de superfície (*Contrato Sexual Visual*, *Feminilidade de Estado*, *Purificação Clássica*) presentes em `atlaslab` e `mnemosyne`. Sem vazamento de "embrutecimento".
- **Institucional** — `arno-dal-ri-site` e `grupoiusgentium.com.br` convergem em pessoas, Grupo Ius Gentium, UFSC/PPGD e ORCID `0000-0002-7734-0404` (143 menções cruzadas a Arno Dal Ri, sem contradição factual detectada).
- **Arquitetura de domínios** — coerente e sem colisão: `iconocracia.com` (mnemosyne), `anavvanzin.github.io/iconocracia` (atlaslab), `www.grupoiusgentium.com.br` (grupo), `atlas-celeste` (Cloudflare, interno).

---

## 3. Onde diverge (a corrigir / conciliar)

> Sintoma dominante: **conceitos estáveis, números instáveis.** Cada superfície fixou
> um N/período/país diferente em momentos diferentes do corpus em expansão.

### 3.1 N do corpus — divergência crítica

| Superfície | N declarado | Situação |
|---|---|---|
| `records.jsonl` (canônico) | **328** | ✅ referência |
| `corpus/corpus-data.json` | **328** | ✅ sincronizado |
| `mnemosyne/site/data/stats.json` | **328** | ✅ concorda |
| `atlas-celeste` (jogo) | **328** | ✅ concorda |
| `mnemosyne/…/corpus-data-enriched.json` e `acervo.json` | **95** | ⚠️ export parcial (34 % do corpus no ar) |
| `companion-data.json` (raiz) | **277** | ⚠️ desatualizado |
| `companion-data.json` (`corpus/`) | **165** | ⚠️ divergente |
| `companion-data.json` (`Other/`) | **145** | ⚠️ cópia stale |
| `atlaslab` (README "27" / `data.js` 30) | **27–30** | ✅ amostra demonstrativa (esperado) — mas README ≠ data |
| `Research/README.md` | **264 / 265** | ⚠️ muito desatualizado |

**Nota de postura:** por decisão de 2026-06-24, **N é intencionalmente não-fixo** (corpus em expansão até a defesa). Portanto a recomendação **não** é "congelar 328", e sim: (a) sincronizar/aposentar as cópias `companion-data.json`; (b) atualizar `Research/README.md`; (c) alinhar README×data no `atlaslab`; (d) descrever o corpus **provisoriamente** ("amostra analisada", "instantâneo") nas prosas públicas em vez de cravar número.

### 3.2 Período — três faixas em conflito

| Fonte | Faixa | Observação |
|---|---|---|
| `iconocracy-corpus/CLAUDE.md` | **1800–2000** | doc canônico |
| `atlaslab` (README) | **1789–2000** | superfície pública |
| `mnemosyne/stats.json` (dados reais) | **1707–1981** | derivado do corpus atual |

Os dados reais **estouram** ambos os limites de prosa (itens < 1789 e nenhum chegando a 2000). Conciliar: ou tratar 1800–2000 como *janela de prioridade* (não gate) e descrever a faixa observada, ou revisar itens-outlier pré-1789.

### 3.3 Países — "seis nações" vs. 17

- `atlaslab` enquadra a tese como **"seis nações — FR, UK, DE, US, BE, BR"**.
- `mnemosyne/stats.json` conta **17 países** (inclui IT 20, PT 11, NL 10, ES 7, AT 4, CL/DK/MX 3…).
- Isso contradiz a **decisão de 2026-06-22**: país deixou de ser critério de inclusão (a alegoria "universal" é transnacional — base do *Contrato Racial Visual*).

**Recomendação:** ajustar a moldura do `atlaslab` de "seis nações" para "núcleo de seis + expansão transnacional", coerente com o *Contrato Racial Visual*.

### 3.4 Painéis warburguianos — 8 vs. 21 vs. 18

| Fonte | Painéis |
|---|---|
| `atlaslab` (README) | **8** |
| `companion-data.json` (raiz e `corpus/`) | **21** |
| `companion-data.json` (`Other/`) | **18** |

Definir o número canônico de painéis Zwischenraum e propagá-lo (provável: os 8 são a curadoria pública do atlas; os 21 são o inventário operacional — vale **explicitar essa relação**, não deixá-la como contradição).

### 3.5 Conceito ausente do público — *Contrato Racial Visual*

O **conceito autoral #3** (Cap. 3; 188 arquivos no canônico) **não aparece em nenhuma superfície pública** (`atlaslab`=0, `mnemosyne`=0, `grupoiusgentium`=0, `artigos`=0), enquanto os outros três circulam. Lacuna de divulgação de um dos quatro pilares originais.

### 3.6 Derivas internas menores

- `purification.jsonl` tem **279** registros, mas `iconocracy-corpus/CLAUDE.md` afirma **236** (doc stale).
- `atlaslab`: README diz "27 espécimes", `atlas/data.js` tem **30** entradas.
- "hardening" aparece como *glosa inglesa* de ENDURECIMENTO em `artigos/…/replica-involuntaria` e numa string de UI inglesa do `atlas-lab`. Aceitável em texto inglês (a regra "nunca hardening" é para o manuscrito PT), mas convém **padronizar**: manter ENDURECIMENTO em maiúsculas + glosa entre parênteses, nunca substituir.

---

## 4. Recomendações priorizadas

| # | Ação | Repo(s) | Prioridade |
|---|---|---|---|
| 1 | Sincronizar ou aposentar as 3 cópias de `companion-data.json` (277/165/145) | iconocracy-corpus | **Alta** |
| 2 | Alinhar molduras públicas de N/período/países à *postura exploratória* (prosa provisória, não número cravado) | atlaslab, mnemosyne | **Alta** |
| 3 | Atualizar `Research/README.md` (264/265 → estado atual) e `CLAUDE.md` (purification 236→279) | Research, iconocracy-corpus | Média |
| 4 | Reenquadrar "seis nações" → "núcleo + expansão transnacional" | atlaslab | Média |
| 5 | Explicitar relação 8 (curadoria) × 21 (inventário) de painéis | atlaslab, companion-data | Média |
| 6 | Superficializar *Contrato Racial Visual* em ao menos uma superfície pública | mnemosyne / atlaslab | Média |
| 7 | Ampliar o export público do `mnemosyne` (95 → cobertura maior do corpus) | mnemosyne | Baixa |
| 8 | Corrigir README×data do `atlaslab` (27 vs 30) e padronizar glosa "hardening" | atlaslab, artigos | Baixa |

---

## 5. Observações de escopo

- Revisão **apenas diagnóstica**; nenhum dado canônico foi tocado.
- `grupoiusgentium.com.br` e `arno-dal-ri-site` não carregam apparatus da tese (registro institucional distinto) — **esperado**, não é divergência.
- `ai-agent-notes` está fora do anel de dados; sem interseção factual a auditar.
