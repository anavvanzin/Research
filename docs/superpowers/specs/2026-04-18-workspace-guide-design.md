---
title: ICONOCRACIA Workspace Guide — Design Spec
slug: workspace-guide-v1
date: 2026-04-18
author: Ana Vanzin + Claude Opus 4.7
status: approved-for-planning
scope: hub/iconocracy-corpus/docs/GUIDE.md · ~/Research/docs/GUIDE.md · apps/iconocracia-space/AGENTS.md · ~/.claude/skills/iconocracy-agent/SKILL.md
supersedes: ~/Research/docs/skill-upgrade-v2/SKILL.md (draft-source; remains as rascunho)
---

# Spec — Guia Canônico ICONOCRACIA (3 repos)

> Construção de um guia-mestre operacional para o ecossistema ICONOCRACIA,
> servindo dupla audiência (agente-codificador + pesquisadora PhD), com
> convergência explícita dos 3 repos GitHub.

---

## 1. Problema

O ecossistema ICONOCRACIA hoje tem 5+ fontes autorizadas (CLAUDE.md × 2, AGENTS.md, MANUAL.md, WORKFLOW.md, OPERATING_MODEL.md, SKILL.md) mas:

1. **Não existe narrativa que tece a convergência dos 3 repos GitHub**
   (`anavvanzin/Research`, `anavvanzin/iconocracy-corpus`, `anavvanzin/iconocracia-space`).
2. **`SKILL.md` do skill `iconocracy-agent`** está com 532 linhas — router-only,
   duplica conteúdo de CLAUDE.md/MANUAL.md, e **não ensina fluxo**.
3. **HF Space** (`apps/iconocracia-space`) só tem `README.md` de 1K — agente
   caindo ali fica cego sobre o contrato de dados com `warholana/iconocracy-corpus`.
4. **Meta-workspace `~/Research/`** foi originalmente construído como hub-que-redireciona
   pro `iconocracy-corpus`, o que confunde agente-codificador: o remote local
   aponta erradamente pra `iconocracia-space.git` e não pro `anavvanzin/Research.git`
   que já existe.
5. **Session patterns PhD↔agente não estão documentados** — só as atomic tasks.

Resultado: sessões novas gastam tokens/tempo redescobrindo topologia, e Ana
esquece onde atualizar quando a realidade drifta.

## 2. Objetivos

### 2.1 Objetivo primário

Produzir **um guia-mestre denso** em `hub/iconocracy-corpus/docs/GUIDE.md` que:

- Tece os 3 repos num único documento narrativo
- Ensina fluxos de sessão ponta-a-ponta (não só comandos soltos)
- Serve dupla audiência — densidade técnica (agente) + prosa acadêmica (Ana)
- **NÃO duplica** MANUAL.md, WORKFLOW.md, OPERATING_MODEL.md, CLAUDE.md
- Tem política de idioma explícita (PT narrativa / EN contratos)
- Tem metadados anti-drift (`last_verified`, checksums opcionais)

### 2.2 Objetivos secundários

- **Colapsar `SKILL.md`** de 532 → ~180 linhas: terminologia + mode-table enxuta + ponteiro pro GUIDE
- **Criar stubs apertura** em `~/Research/docs/GUIDE.md` e `apps/iconocracia-space/AGENTS.md`
- **Editar mínimos** em CLAUDE.md/README.md dos 3 repos pra apontar pro GUIDE
- **Fixar remote** de `~/Research/` pra `anavvanzin/Research.git`

## 3. Não-objetivos (YAGNI)

- Reescrever MANUAL.md, WORKFLOW.md, OPERATING_MODEL.md — **mantêm-se como estão**.
- Criar documentação per-módulo (ex.: GUIDE-para-webiconocracy.md) — Ana tem outros docs pra isso.
- Gerar site estático novo — GitHub Pages já serve `hub/`, basta fazer GUIDE.md ser renderizado lá.
- Traduzir MANUAL.md inteiro pro PT — mantém bilingue onde já está.
- Build automation (pre-commit hook validando checksums) — nesta v1, verificação manual.

## 4. Arquitetura proposta

### 4.1 Inventário de arquivos

| Ação | Caminho | Tamanho alvo | Idioma | Papel |
|---|---|---|---|---|
| **CRIAR** | `hub/iconocracy-corpus/docs/GUIDE.md` | 1500–2500 linhas | PT prosa + EN técnico | Guia-mestre canônico |
| **CRIAR** | `~/Research/docs/GUIDE.md` | ~60 linhas | PT | Aperture — aponta pro hub + conteúdo único do meta (Books/, Cotutela/, symlinks) |
| **CRIAR** | `apps/iconocracia-space/AGENTS.md` | ~40 linhas | EN | Contrato HF Space + ponteiro pro hub GUIDE |
| **REESCREVER** | `~/.claude/skills/iconocracy-agent/SKILL.md` | 532 → ~180 linhas | PT | Thin router: terminologia + mode table + delegação |
| **REESCREVER (mirror)** | `~/Research/docs/skill-upgrade-v2/SKILL.md` | idem | PT | Draft-source sincronizado com o skill ativo |
| **EDITAR** | `hub/iconocracy-corpus/CLAUDE.md` | +10 linhas | atual | Link no topo pro GUIDE |
| **EDITAR** | `hub/iconocracy-corpus/README.md` | +5 linhas | atual | Link "Guia canônico: docs/GUIDE.md" |
| **EDITAR** | `~/Research/CLAUDE.md` | +5 linhas | PT/EN misto atual | Link pra aperture doc |
| **EDITAR** | `~/Research/AGENTS.md` | +5 linhas | PT/EN misto atual | Link pra aperture doc |
| **EDITAR** | `apps/iconocracia-space/README.md` | +3 linhas | EN atual | Link pro AGENTS.md |
| **MANTER** | `hub/iconocracy-corpus/docs/MANUAL.md` | sem alteração | atual | GUIDE signposta. **NÃO mexer.** |
| **MANTER** | `hub/iconocracy-corpus/docs/WORKFLOW.md` | sem alteração | atual | GUIDE signposta. **NÃO mexer.** |
| **MANTER** | `hub/iconocracy-corpus/docs/OPERATING_MODEL.md` | sem alteração | atual | GUIDE signposta. **NÃO mexer.** |

**Total:** 3 arquivos novos + 1 reescrito (em 2 locais espelhados) + 5 edições mínimas.

### 4.2 Grafo de ponteiros

```
                         ┌─────────────────────────────────────┐
                         │  hub/iconocracy-corpus/docs/GUIDE.md │
                         │  (canonical — 1500–2500 lines)       │
                         └──┬──────────────┬────────────────┬───┘
                            │              │                │
       apontado por:        │              │                │  signposta pra:
                            │              │                │
   ~/Research/docs/GUIDE.md │              │                │  docs/MANUAL.md
   ~/Research/CLAUDE.md     │              │                │  docs/WORKFLOW.md
   ~/Research/AGENTS.md     │              │                │  docs/OPERATING_MODEL.md
   apps/.../AGENTS.md       │              │                │  CLAUDE.md (hub)
   apps/.../README.md       │              │                │  ICONOCRACIA_MASTER_PROMPT.md
   hub/.../CLAUDE.md        │              │                │  ADR-001 (imagens em Drive)
   hub/.../README.md        │              │                │
   ~/.claude/skills/        │              │                │
      iconocracy-agent/     │              │                │
      SKILL.md              │              │                │
```

## 5. Estrutura do GUIDE.md (hub/docs/GUIDE.md)

13 seções, macro→micro. Densidade calibrada por seção.

### 5.1 Front matter (YAML + badges)

```yaml
---
title: ICONOCRACIA Workspace Guide
version: 1.0
last_verified: 2026-04-18
verified_against:
  - path: hub/iconocracy-corpus/CLAUDE.md
    sha256: <md5-ou-sha256-opcional>
  - path: hub/iconocracy-corpus/docs/MANUAL.md
    sha256: <...>
  - path: ~/Research/CLAUDE.md
    sha256: <...>
audience: [coding-agent, phd-researcher]
language-policy: pt-prose + en-technical
thesis: ICONOCRACIA — Female Allegory in the History of Legal Culture (19–20th c.)
defense: 2026
---
```

Abaixo do YAML: badges shields.io (status, thesis-progress, last-update).

### 5.2 Seções (com densidade estimada)

| § | Título | Linhas | Idioma | Função |
|---|---|---|---|---|
| 0 | Preamble (front matter + badges + "como ler este guia") | 40 | PT | Orientação |
| 1 | Para quem é este guia | 60 | PT | Dual audience explicit |
| 2 | Leia primeiro — links canônicos | 40 | PT | O que este guia NÃO é |
| 3 | **Os três repos** (topologia, remotes, escopo) | 200 | PT + EN mixed | — |
| 3.1 | `anavvanzin/Research` (meta-workspace) | 60 | PT | — |
| 3.2 | `anavvanzin/iconocracy-corpus` (hub canônico) | 80 | PT | — |
| 3.3 | `anavvanzin/iconocracia-space` (HF Space) | 60 | PT + EN | — |
| 4 | **Convergência — a joia da coroa** | 300 | PT + EN | Narrativa do contrato |
| 4.1 | Contrato canônico de dados (`records.jsonl` → `corpus-data.json` → HF) | 80 | EN | Pipeline formal |
| 4.2 | Symlinks research↔hub (mapa completo) | 60 | PT | Topologia fs |
| 4.3 | HF dataset `warholana/iconocracy-corpus` como ponte | 60 | EN | Release path |
| 4.4 | Release multi-superfície (local→hub→HF dataset→Space) | 80 | EN | Checklist |
| 4.5 | Anti-drift: como detectar quando divergem | 20 | PT | Sanity check |
| 5 | **Session patterns — PhD↔agente** | 500 | PT predominante | Maior seção |
| 5.1 | Sessão de escrita (redação/revisão de capítulo) | 70 | PT | Pandoc, terminologia |
| 5.2 | Sessão SCOUT (busca em acervos) | 60 | PT + EN | corpus-scout skill |
| 5.3 | Sessão ICONOCODE (codificação visual) | 70 | PT | 3 níveis Panofsky + 10 indicadores |
| 5.4 | Sessão PURIFICAÇÃO (coding ENDURECIMENTO em lote) | 50 | PT | code_purification.py |
| 5.5 | Sessão ZWISCHENRAUM (painel comparativo warburguiano) | 60 | PT | SCOUT+ICONOCODE |
| 5.6 | Sessão DIR410346 (disciplina — aulas e memorial) | 50 | PT | Diego Nunes, Sbriccoli |
| 5.7 | Sessão MNEMOSYNE (exploração criativa) | 40 | PT | hub/mnemosyne-scout |
| 5.8 | Sessão EMERGÊNCIA (bug, release quebrado, pré-orientação) | 50 | PT + EN | Runbook |
| 5.9 | Sessão COMPILE (make thesis → PDF/DOCX) | 30 | EN | Pandoc |
| 5.10 | Sessão VALIDATE + SYNC | 20 | EN | Scripts |
| 6 | Como agentes usam este workspace | 250 | PT + EN | — |
| 6.1 | Ordem de leitura de contexto (CLAUDE→AGENTS→SKILL→GUIDE) | 40 | PT | Loading order |
| 6.2 | Skill routing — mapa dos modos | 80 | PT | Aponta SKILL.md, não duplica |
| 6.3 | Ferramentas MCP disponíveis | 60 | EN | Tabela Gallica, HF Hub, WebSearch |
| 6.4 | Hooks PreToolUse/PostToolUse que disparam | 50 | EN | Segurança + automação |
| 6.5 | Agentes dedicados (abnt-checker, iconocode, thesis-reviewer) | 20 | PT | Pointer |
| 7 | Contrato terminológico | 150 | PT | — |
| 7.1 | 4 conceitos originais (Contrato Sexual Visual, Feminilidade de Estado, Contrato Racial Visual, Purificação Clássica) | 70 | PT | Ordem inegociável |
| 7.2 | ENDURECIMENTO + 10 indicadores (escala 0-3) | 40 | PT + EN | Definição |
| 7.3 | Pathosformel / Warburg / Panofsky | 20 | PT + DE | Manter alemão |
| 7.4 | Proibições lexicais (ciberfeminismo, hardening, 0-4) | 20 | PT | Red lines |
| 8 | Corpus — parâmetros canônicos | 100 | EN + PT | Signposting pra MANUAL §corpus |
| 8.1 | 165 itens, países, suportes, período | 40 | EN | Quick ref |
| 8.2 | Pipeline WebScout → IconoCode | 30 | EN | Pointer |
| 8.3 | Schemas (6) | 30 | EN | Pointer |
| 9 | Tese — manuscrito, compile, 4 originais | 80 | PT | Signposting pra MANUAL §tese |
| 10 | HF Space — app.py, data source, release | 120 | EN | Única seção densa sobre Space |
| 10.1 | Estrutura do app (Gradio tabs) | 40 | EN | — |
| 10.2 | Contrato com `warholana/iconocracy-corpus` | 30 | EN | Como baixa |
| 10.3 | Atualização do Space (sdk_version, deploy) | 30 | EN | — |
| 10.4 | Quando o Space quebra — runbook | 20 | EN | — |
| 11 | Release multi-superfície — checklist canônico | 120 | EN | — |
| 12 | Antipatterns (learned-the-hard-way) | 150 | PT + EN | — |
| 12.1 | Imagens binárias em `data/raw/` | 20 | EN | ADR-001 |
| 12.2 | `sed` em JSON grande | 20 | EN | — |
| 12.3 | System Python em vez de conda `iconocracy` | 20 | EN | — |
| 12.4 | Retry loops em API Europeana/Gallica | 20 | EN | Fall back após 2 falhas |
| 12.5 | `git add -A` em hub (risco: binários) | 20 | EN | — |
| 12.6 | Atribuir conceitos originais a Pateman/Mondzain | 30 | PT | Terminologia |
| 12.7 | Travessões (—) em memorial DIR410346 | 20 | PT | Estilo |
| 13 | Glossário + Índice canônico de docs | 80 | PT + EN | Com datas last-verified |

**Total estimado:** ~2400 linhas. Escala-se conforme escrita real.

### 5.3 Política de idioma (header inline)

Cada seção abre com badge HTML:
```html
<!-- 🇧🇷 Português (prosa, conceitos, tese) -->
<!-- 🇬🇧 English (CLI, JSON, schemas, code) -->
<!-- 🌐 PT + EN (híbrido) -->
```

Regra: PT pro que Ana pode copiar-colar na tese. EN pro que um agente executa.

### 5.4 Badges de abertura (shields.io ou equivalente)

```html
<p align="center">
  <img alt="Status" src="https://img.shields.io/badge/status-active-success">
  <img alt="Thesis" src="https://img.shields.io/badge/defense-2026-blueviolet">
  <img alt="Python" src="https://img.shields.io/badge/python-3.12-blue">
  <img alt="Corpus" src="https://img.shields.io/badge/corpus-165%20items-orange">
  <img alt="ABNT" src="https://img.shields.io/badge/citations-ABNT%20NBR%206023%3A2025-red">
</p>
```

## 6. SKILL.md colapso — plano detalhado

### 6.1 Seções que **permanecem** no SKILL.md

| § atual | Conteúdo | Decisão |
|---|---|---|
| A. Argumento Central | 3 conceitos originais (EXPANDIR pra 4 — Purificação Clássica) | **MANTER + atualizar** |
| B. Terminologia Obrigatória | Tabela de termos | **MANTER** |
| D. Roteamento de Modos (apenas a tabela enxuta) | Trigger → modo → delegação | **MANTER enxuta** (sem explicações longas) |
| Q. Skills Satélites — catálogo | Tabela de delegação | **MANTER** |
| S. Regras de Comportamento | 14 regras | **MANTER** |

### 6.2 Seções que **saem** do SKILL.md pro GUIDE.md

| § atual | Destino no GUIDE |
|---|---|
| C. Workspace Map | §3 (3 repos) + §4.2 (symlinks) |
| E. Modo ICONOCODE detalhado | §5.3 |
| F. Modo ARGOS | §5.8 (emergência/acquisition no MANUAL) |
| G. Modo PURIFICAÇÃO | §5.4 |
| H. Modo MNEMOSYNE | §5.7 |
| I. Modo COMPILAR | §5.9 (pointer pra MANUAL) |
| J. Modo VALIDAR | §5.10 (pointer pra MANUAL) |
| K. Modo SYNC | §5.10 |
| L. Modo ZWISCHENRAUM | §5.5 |
| M. Modo DIR410346 | §5.6 |
| N. Três Regimes Iconocráticos | §7 |
| O. Corpus parâmetros | §8 |
| P. Scripts disponíveis | MANUAL (já está lá) — remover do SKILL |
| R. Ferramentas MCP | §6.3 |
| T. Documentação de Referência | §13 |

### 6.3 Nova seção terminal do SKILL

```markdown
## ⚓ Entry Point Canônico

Para qualquer modo acima, o **guia canônico é**:

📖 `~/Research/hub/iconocracy-corpus/docs/GUIDE.md`

- **§3** — topologia dos 3 repos
- **§4** — convergência e release multi-superfície
- **§5.X** — session patterns ponta-a-ponta
- **§12** — antipatterns

Este SKILL é router. GUIDE ensina o fluxo.
```

### 6.4 Espelhamento draft

Ao reescrever, atualizar **também** `~/Research/docs/skill-upgrade-v2/SKILL.md`
(fonte do draft) para ficar idêntico ao skill ativo. Convenção:
skill-upgrade-v2 = fonte rastreada em git; ~/.claude/skills/ = instalação.

## 7. Aperture doc — `~/Research/docs/GUIDE.md` (~60 linhas)

Estrutura:

```markdown
---
title: Research Meta-Workspace — Aperture Guide
last_verified: 2026-04-18
canonical: hub/iconocracy-corpus/docs/GUIDE.md
---

# 🌐 Research Meta-Workspace

> Este doc é um **stub de apertura**. O guia canônico vive no hub.

## 📖 Guia completo

👉 [`hub/iconocracy-corpus/docs/GUIDE.md`](../hub/iconocracy-corpus/docs/GUIDE.md)

Este repo (`anavvanzin/Research`) é o meta-workspace que **agrupa** os 3 repos
sob `hub/`, `apps/`, `pipelines/`, etc. (ver [`../README.md`](../README.md)).

## O que é único do meta-workspace

Conteúdo que NÃO vive no hub e precisa ser documentado aqui:

### 📚 `Books/`
Biblioteca de referência (24 PDFs) — Ginzburg, Beccaria, Sbriccoli, Broedel, etc.
Não rastreada em git (arquivos pesados). Ver `.gitignore`.

### 🎓 `Cotutela/`
Checklist + resumo da cotutela com [instituição parceira].
Atualizar quando houver marco administrativo.

### 🔗 Symlinks críticos
| Path | Aponta pra | Quem edita |
|---|---|---|
| `vaults/iconocracy-vault` | `hub/iconocracy-corpus/vault` | hub |
| `pipelines/iconocracy-ingest` | `hub/iconocracy-corpus/indexing/ingest` | hub |
| `pipelines/indexing` | `hub/iconocracy-corpus/indexing` | hub |
| ... | ... | ... |

### 🎨 `docs/superpowers/`
Specs, plans, auditorias de sessões anteriores. Referenciado pelo hub GUIDE §13.

## Quando editar este stub

Só quando:
- Adicionar novo bucket top-level (novo `labs/`, `archive/` etc.)
- Mudar política de symlinks
- Adicionar conteúdo que NÃO existe no hub

Para tudo mais, editar o hub GUIDE.
```

## 8. Aperture doc — `apps/iconocracia-space/AGENTS.md` (~40 linhas)

```markdown
---
title: iconocracia-space — Agent Guide
last_verified: 2026-04-18
canonical: ../../hub/iconocracy-corpus/docs/GUIDE.md
---

# 🚀 iconocracia-space (HF Space)

> Hugging Face Gradio app for corpus exploration.
> Canonical guide: see §10 in the [hub GUIDE](../../hub/iconocracy-corpus/docs/GUIDE.md).

## Data contract

This Space **reads** `corpus-data.json` from the HF dataset
[`warholana/iconocracy-corpus`](https://huggingface.co/datasets/warholana/iconocracy-corpus)
— not from the GitHub hub directly.

Update flow:
1. Edit corpus in hub → `records.jsonl`
2. `python tools/scripts/records_to_corpus.py` → regenerates `corpus/corpus-data.json`
3. `python tools/scripts/build_hf_release.py` → pushes to `warholana/iconocracy-corpus` dataset
4. This Space auto-refetches on cold start (or manual restart)

**Never** edit `corpus-data.json` directly in this repo. It is not the source of truth.

## Editing the app

- `app.py` — Gradio entrypoint
- `requirements.txt` — Python deps (must match `python_version: 3.10.13` in README frontmatter)
- HF Space SDK version pinned at `4.44.1`

## Runbook — when Space breaks

| Symptom | Check |
|---|---|
| App builds but shows no data | HF dataset `warholana/iconocracy-corpus` unreachable or empty |
| Import error on boot | `requirements.txt` drift vs `app.py` imports |
| Layout broken after upgrade | `sdk_version` mismatch — pin to `4.44.1` |

See hub GUIDE §10.4 for full runbook.
```

## 9. Edits mínimos nos docs existentes

### 9.1 `hub/iconocracy-corpus/CLAUDE.md` (+10 linhas no topo)

Adicionar logo abaixo do H1:

```markdown
> **📖 Guia canônico para esta pesquisa:** [`docs/GUIDE.md`](docs/GUIDE.md)
>
> Este CLAUDE.md é reference técnico-operacional. GUIDE.md ensina fluxo e
> convergência com os outros 2 repos (`anavvanzin/Research`, `iconocracia-space`).
```

### 9.2 `hub/iconocracy-corpus/README.md` (+5 linhas)

Adicionar seção "Canonical guide" abaixo do abstract:

```markdown
## 📖 Canonical Guide

**Start here:** [`docs/GUIDE.md`](docs/GUIDE.md) — comprehensive workflow
+ convergence with `anavvanzin/Research` and `anavvanzin/iconocracia-space`.
```

### 9.3 `~/Research/CLAUDE.md` (+5 linhas) e `~/Research/AGENTS.md` (+5 linhas)

Adicionar no topo (abaixo do H1):

```markdown
> **📖 Canonical guide:** [`hub/iconocracy-corpus/docs/GUIDE.md`](hub/iconocracy-corpus/docs/GUIDE.md)
>
> Aperture doc for this meta-workspace: [`docs/GUIDE.md`](docs/GUIDE.md).
```

### 9.4 `apps/iconocracia-space/README.md` (+3 linhas)

Adicionar antes do último parágrafo:

```markdown
**For agents & contributors:** see [`AGENTS.md`](AGENTS.md) and the
[hub GUIDE](../../hub/iconocracy-corpus/docs/GUIDE.md) §10.
```

## 10. Sprint 0 — Pré-requisitos infra (antes de escrever GUIDE)

```bash
# 1. Fix remote de ~/Research/
git -C /Users/ana/Research remote set-url origin https://github.com/anavvanzin/Research.git
git -C /Users/ana/Research remote -v   # confirmar

# 2. Confirmar branch e fetch
git -C /Users/ana/Research fetch origin
git -C /Users/ana/Research branch -vv

# 3. Verificar se há divergência com remote
git -C /Users/ana/Research log origin/main..HEAD --oneline
git -C /Users/ana/Research log HEAD..origin/main --oneline

# 4. Se OK, continuar. Se houver conflito, parar e diagnosticar.
```

**Se Sprint 0 falha:** parar, reportar, não prosseguir com o GUIDE. Guia em repo
órfão não cumpre seu papel.

## 11. Critérios de aceitação

### 11.1 GUIDE.md deve

- [ ] Render corretamente em GitHub (preview markdown)
- [ ] Ter todas 13 seções populadas (não stub)
- [ ] Ter badges shields.io funcionais
- [ ] Ter front matter YAML válido (passa `python3 -c "import yaml; yaml.safe_load(open('front matter'))"`)
- [ ] Ter headers declarando idioma em cada seção
- [ ] Não duplicar > 10% de nenhum dos 3 docs existentes (MANUAL/WORKFLOW/OPERATING_MODEL) — verificar com `diff -y` resumo
- [ ] Linkar **todos** os docs mencionados com path relativo válido (rodar um link-checker markdown)
- [ ] §4 (convergência) e §5 (session patterns) representam juntas ≥50% do volume

### 11.2 SKILL.md colapsado deve

- [ ] ≤200 linhas
- [ ] Manter 4 originais, terminologia, mode-table, regras de comportamento
- [ ] Apontar pro GUIDE.md em seção terminal
- [ ] Estar espelhado entre `~/.claude/skills/iconocracy-agent/SKILL.md` e `~/Research/docs/skill-upgrade-v2/SKILL.md`

### 11.3 Stubs devem

- [ ] `~/Research/docs/GUIDE.md` em ~60 linhas, aponta pro hub
- [ ] `apps/iconocracia-space/AGENTS.md` em ~40 linhas, contrato HF + ponteiro

### 11.4 Edições devem

- [ ] Adicionar blockquote canônico no topo de: hub CLAUDE.md, hub README.md, Research CLAUDE.md, Research AGENTS.md, space README.md
- [ ] Nenhum doc existente **modificado além** desse blockquote (zero risco regressão)

### 11.5 Sprint 0

- [ ] Remote de `~/Research/` aponta pra `https://github.com/anavvanzin/Research.git`
- [ ] `git push` bem-sucedido em cada um dos 3 repos
- [ ] `git log origin/main..HEAD` vazio nos 3

## 12. Plano de implementação (ordem)

1. **Sprint 0** — fix remote (bash, confirmação humana antes de push)
2. **Fase 1 — GUIDE skeleton** — criar `hub/docs/GUIDE.md` com front matter + badges + H2 de todas 13 seções + "TODO" em cada
3. **Fase 2 — GUIDE conteúdo §3 §4 §5** — as 3 seções maiores, escrita substantiva
4. **Fase 3 — GUIDE conteúdo §6 §7 §10 §11 §12** — densas mas menores
5. **Fase 4 — GUIDE conteúdo §0 §1 §2 §8 §9 §13** — signposting
6. **Fase 5 — SKILL.md colapso** — reescrever em ambos os locais espelhados
7. **Fase 6 — Stubs** — Research aperture + Space AGENTS
8. **Fase 7 — Edits mínimos** — 5 blockquotes canônicos
9. **Fase 8 — Validação** — rodar critérios §11 como checklist
10. **Fase 9 — Commit + push** — 1 commit por fase, push nos 3 repos

## 13. Riscos & mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| GUIDE duplica MANUAL silenciosamente | Média | Drift em 6 meses | Checklist §11.1 — diff resumo |
| Sprint 0 falha (remote Research confuso) | Média | Bloqueia tudo | Parar e reportar; não escrever em repo quebrado |
| SKILL colapsa conteúdo que era usado ativamente | Baixa | Agente perde capability | Mode-table permanece exaustiva; só as explicações longas migram |
| Edição do hub CLAUDE.md quebra gateguard | Baixa | PreToolUse bloqueia | Usar blockquote simples, sem mudanças estruturais |
| HF Space AGENTS.md deploya como parte do Space | Baixa | Quebra Gradio? | Gradio ignora `AGENTS.md`; confirmar com `sdk`: só lê `app.py`+requirements+README |
| Ana esquece de atualizar `last_verified` | Alta | Metadata drifta | Aceitar — é manual v1; automação fica pra v2 |
| Portuguese/English split drifta | Média | Memorial e guia se cruzam | Política explícita §5.3 + badge HTML em cada seção |

## 14. Métricas de sucesso

- Uma sessão nova do agente-codificador localiza o guia em ≤2 lookups
- Ana consegue apontar pra GUIDE.md em lugar de explicar oralmente
- GUIDE é referenciado pelo memorial de qualificação (se aplicável)
- Release multi-superfície roda com checklist de §11 sem memória oral
- Zero conflito entre GUIDE e MANUAL/WORKFLOW/OPERATING_MODEL após 3 meses
- `last_verified` atualiza ao menos 1×/mês

## 15. Decisões tomadas (council synthesis)

| Decisão | Voz dominante | Racional |
|---|---|---|
| GUIDE vive em `hub/docs/` | Pragmatist | Path diário de Ana; hub tem Pages; menos drift |
| Escopo apertado — só gap | Skeptic | MANUAL já cobre 85%; não duplicar |
| Sprint 0 obrigatório | Critic | Remote quebrado torna doc órfão |
| Language-per-section | Critic | PT/EN mistura gera mess impublicável |
| SKILL colapsa pra ~180 linhas | Architect + Pragmatist | Router não precisa ter conteúdo duplicado |
| Stubs em Research + Space | Pragmatist + Critic | Discoverability sem triplo-maintenance |

## 16. Open questions (resolver durante implementação)

- **Q1:** Incluir checksums SHA256 em `verified_against` ou só paths + datas? **Default:** só paths+datas (v1 manual); automação fica pra v2.
- **Q2:** Badges custom ou shields.io? **Default:** shields.io (sem infra).
- **Q3:** Glossário §13 replicado ou puro índice? **Default:** puro índice (definições ficam em MANUAL e ICONOCRACIA_MASTER_PROMPT).
- **Q4:** MCP list §6.3 inclui Notion legado? **Default:** sim, marcado como legacy/on-demand (já foi demotion em commit a1f1d73).
- **Q5:** AGENTS.md do space fica rastreado pelo HF Space deploy? **Checar:** rodar `git check-ignore` + confirmar HF Space ignora arquivos não-executáveis (README + app + requirements).

---

**Status:** aprovado pelo user em 2026-04-18. Próximo passo: invocar `writing-plans` skill para gerar plano de implementação detalhado por fase.
