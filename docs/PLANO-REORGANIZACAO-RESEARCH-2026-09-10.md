# Plano de Reorganização — `/Users/ana/Research`

**Data:** 2026-09-10 · **Status:** proposta para aprovação (nada além do Phase 0 executado sem OK)
**Natureza:** não-destrutivo até onde for possível; apagamento só após revisão em quarentena.

---

## 0. Objetivo

Eliminar o caos estrutural do meta-workspace sem perder nenhum trabalho de tese.
O caos tem **3 causas** — e cada uma vira uma frente do plano:

1. **Worktrees de agentes nunca podados** (~57 do repo Research + ~26 do corpus).
2. **Cópias/duplicatas da tese** (`iconocracy-corpus-1`, `iconocracy-corpus-claude-*`, `artifacts 2/3`, pastas de data).
3. **Trabalho não-commitado espalhado** (2 commits locais do Cap. 2 + working tree sujo + ~36 branches com commits não-enviados).

---

## 1. Baseline (já verificado)

| Métrica | Valor |
|---|---|
| Tamanho total | 30 GB |
| Entradas no topo | ~149 |
| Repos git aninhados | ~63 |
| Arquivos soltos no topo | ~50 |

### 1.1 Já executado em 2026-09-10 (reversível, sem commit)

| De | Para | Ação |
|---|---|---|
| `anavanzinparte242/` | `site-anavvanzin/` | renomeio (site anavvanzin.com) |
| `20262/` | `2026-materiais/` | renomeio (corrige typo) |
| `Particular e Compartilhado/` (casca vazia) | `_apagar/` | quarentena |
| `artifacts 2/` e `artifacts 3/` | `_apagar/` | quarentena (duplicatas) |
| `Particular e Compartilhado 2/` | `Particular e Compartilhado/` | promoção (nome limpo p/ conteúdo DIR410350) |

---

## 2. Fato crítico de segurança (ler antes de tudo)

> ⚠️ **CORREÇÃO 2026-09-21 — este bloco era FALSO POSITIVO. Verificado e desmentido.**
> Os dois commits ditos "locais exclusivos" **já estavam publicados** em `origin/main`
> dentro do PR **#203 "Espinha arquitetura c"**. Comparação arquivo por arquivo (hashes
> idênticos a `origin/main`):
>
> | Arquivo | `97d8e1d` vs `origin/main` |
> |---|---|
> | `The-Coin-and-the-Witch-Brazilian-Extension.md` | idêntico |
> | `docs/BRIEFING-GPT-Astra6-espinha-tese.md` | idêntico |
> | `tese/manuscrito/Capitulo2_iconocracia.md` | idêntico |
> | `vault/tese/references.bib` | idêntico |
> | Cap. 2 em `366a2eb` | sha `62e2d0a` idêntico |
>
> **Nenhum trabalho de tese está em risco.** A branch local é rebase/merge cujo conteúdo
> já circulou por outro caminho. Medição de 2026-09-21: **7 commits à frente** de
> `origin/main` = 2 commits de tese **já duplicados no remoto** + 4 `vault backup`
> automáticos + 1 regeneração de corpus (`ac1ca89`). Nada exclusivo.
>
> **Não travar limpeza por este motivo.** O Phase 0 como bloqueio deixa de existir; o que
> resta é decidir o que fazer com o working tree sujo (M: `AutoResearchClaw`,
> `DASHBOARD_CORPUS.html`, `wiki/.obsidian/*`; ?? : `.codex/agents/`,
> `vault/tese/rascunhos-artigos/out-abnt/`), que é questão de higiene, não de segurança.

`hub/iconocracy-corpus` (repo canônico da tese) — ~~bloco original, superado acima~~:

- Branch local `base/main-sync-2026-08-24` está **15 commits atrás** do `origin/main` e **2 à frente**.
- Os **2 commits locais exclusivos** são tese e só existem aqui:
  - `366a2eb` — Cap. 2: regime contra-alegórico + seção Abaporu/antropofagia
  - `97d8e1d` — extensão brasileira do template federiciano + espinha (Arquitetura C)
- O working tree tem **mais alterações não-commitadas** (7 M, 2 D, 22 ??): manuscrito Maria/Marianne, `conselho_revisoes/`, `corpus/exemplares/`, `docs/contra-alegoria-abaporu…`, `rascunhos de artigos/`.

**~~Consequência~~ (superada pela correção acima):** nenhuma limpeza pode tocar o canônico antes de resolver esses 2 commits + working tree. Isso é o **Phase 0**, e é pré-requisito de tudo. **Falso** — ver correção de 2026-09-21.

---

## 3. Fases

### Phase 0 — Travar a segurança do canônico *(PRÉ-REQUISITO, decide tudo)*

| # | Ação | Risco | Autorização |
|---|---|---|---|
| 0.1 | Snapshot do working tree (`git diff` exportado + lista de untracked) | zero | não precisa |
| 0.2 | Reconciliar os 2 commits locais com `origin/main` (merge ou rebase) | médio — pode dar conflito | **precisa** |
| 0.3 | Commit do working tree sujo (ou descartar/estacionar por decisão) | médio | **precisa** |
| 0.4 | Push para `origin` | alto (publica) | **precisa** |

**Decisões de Ana (Phase 0):**
- D0a. Como reconciliar: `merge` (conservador, cria merge commit) vs `rebase` (histórico linear, reescreve os 2 commits) — **recomendo merge**.
- D0b. O working tree sujo: commitar como está, ou separar por tema, ou `stash` para decidir depois — **recomendo commitar como está** com mensagem clara, pois é trabalho real.

### Phase 1 — Resgatar conteúdo único de `iconocracy-corpus-1/`

Clone stale (787 MB, 2 meses atrás) com **3 itens que não existem no canônico**:

| Item | O que é | Destino proposto |
|---|---|---|
| `adasdsa/` | pacote apresentação *Malleus Maleficarum* (PPTX 13 MB + handout + roteiro) | `hub/iconocracy-corpus/vault/` ou pasta de aulas |
| `vault/projeto/review-phase0.5-data-purist.json` | veredito de revisão | `hub/iconocracy-corpus/vault/projeto/` |
| `vault/projeto/review-phase0.5-writing-first.json` | veredito de revisão | idem |

Após resgate: arquivar/apagar o clone. **Decisão:** D1 = destino do pacote Malleus.

### Phase 2 — Higiene git (worktrees + branches)

- **2a.** Podar worktrees `prunable` do repo Research (26 codex + 5 gemini) — zero risco.
- **2b.** Remover os 5 worktrees `iconocracy-corpus-claude-*` (0 commits únicos) via `git worktree remove`/`prune` (inscrição aponta pra `Documents/GitHub`, está `locked`).
- **2c.** Revisão branch-a-branch dos **~36 branches locais** do corpus. Método por branch: `git log origin/main..<branch> --oneline` + `git diff --stat origin/main...<branch>`, classificar em:
  - ✅ já incorporado ao `origin/main` → **apagar branch**
  - 🔶 trabalho único (ex.: `feat/alegorias-piloto-v2` 22, `reconcile/ssd-scripts` 37, `v0.2-thumbnail-recovery` 10, `debug-mpc-agent-introspection` 13, `worktree-e1-fable5-recode` 22, `harness/hookify-python-path-rule` 14) → **resgatar/cherry-pick ou push**
  - 🗑️ superseded por trabalho posterior (incl. *spring cleaning #196*) → **apagar**

**Decisão:** D2 = aprovar push dos branches resgatados (exige autorização).

### Phase 3 — Finalizar duplicatas de pasta

- `_apagar/` (3 itens) → apagar de vez após revisão.
- `iconocracy-corpus-1/` → arquivar/apagar após Phase 1.
- `Documents/` (4,2 GB) e `Downloads/` (74 MB) internos → investigar se duplicam o `~/` real.
- `2026-materiais/iconocracia_sessao_2026-07-24/` vs top-level `iconocracia_sessao_2026-07-24/` → confirmar duplicata.
- Symlinks iCloud/Documents (16 GB) → fora do escopo (já tratado no `disco-2026-08-28.md §10.6`).

### Phase 4 — Triagem de arquivos soltos (~50 no topo)

| Categoria | Arquivos | Destino |
|---|---|---|
| Jurídico/pessoal | `Peticao_Inicial_JEF_TCG_Cards.txt`, `Requerimento_Restituicao_II_eCAC.txt`, `Roteiro_Pratico_TCG_Cards.md` | `Particular e Compartilhado/` |
| Visão computacional | `curso-visao-computacional-moodle.pdf` (16 MB), `Plano_piloto_visao_computacional_*.docx` (×2), `relatoriokantvisaocomputacional.md` | `docs/` ou `2026-materiais/` |
| Metodologia/tese | `DECISAO-METODOLOGICA-aparato-minimo.md`, `pesquisa-padrao-metodologico-iconografia-juridica.md`, `Metodologia em História do Direito…html` + `_files/`, `Elicit - The Coin and the Witch…prospectus.md` | `docs/` |
| Scripts/scholar | `tmp_*.py` (3), `edit_halperin.py`, `scholar_*.{csv,json}` (8), `iconocracia_cv_env.py`, `rewrite-home-repo.sh` | `scripts/` ou apagar |
| DB de agente | `acc.db` + `-shm` + `-wal` | investigar origem → apagar |
| Zips | `iconocracia_docs.zip` + `(1).zip` (22 B, corrompidos → apagar); `artifacts.zip`, `abnt-6023.zip`(+pasta), `pacote-tese-iconocracia.zip`, `notion-export.zip`(+pasta), `5ac5851e…ExportBlock….zip` | conferir conteúdo → extrair ou `_apagar/` |
| PDF grande | `Caderno antigo de Historia da Cultura Juridica mestrado.pdf` (5,6 MB) | `2026-materiais/` |
| Relatórios de agente | `agent_cost_spike_report.md`, `agenttrace-overview.md`, `agenttrace-session-recovery-report.md`, `document_instructions_to_agent.md` | `_apagar/` ou `docs/` |
| SBHCJ | `Logos SBHCJ.dc.html` | `sbhcj-press-kit/` |
| Imagem | `desktop-ref-antigravity.png` | `imagens/` |
| Config/meta | `Claude.mobileconfig`, `github-app.yml`, `payload.json`, `environment.yml`, `CLAUDE.md` (0 B), `BOOT-EXTERNO-CHECKPOINT-2026-09-10.md` | revisar 1 a 1 |

### Phase 5 — Repos aninhados (63) — baixa prioridade

Não limpar. Manter o mapa vivo (CONFLUENCIA-REPOSITORIOS doc). Apenas verificar clones redundantes pontuais (ex.: `site-anavvanzin/` vs `apps/anavanzin-pages/`).

---

## 4. Pontos de decisão (resumo)

| ID | Decisão | Recomendação |
|---|---|---|
| D0a | merge vs rebase dos 2 commits | **merge** |
| D0b | o que fazer com o working tree sujo | **commitar como está** |
| D0c | autorizar push do Phase 0 | **sim** (é o maior risco de perda) |
| D1 | destino do pacote Malleus | `hub/iconocracy-corpus/vault/` |
| D2 | aprovar push de branches resgatados (2c) | após eu apresentar a lista |
| D3 | apagar `_apagar/` agora ou depois | **depois** da sua revisão |

---

## 5. Riscos e reversibilidade

| Fase | Risco | Mitigação |
|---|---|---|
| 0 | perder 2 commits / conflito de merge | snapshot antes; merge não reescreve histórico |
| 1 | mover Malleus pro lugar errado | copiar (não mover) até você validar destino |
| 2 | apagar branch com trabalho único | só apagar após classificar ✅/🗑️ com diff |
| 3–4 | apagar algo útil | tudo passa por `_apagar/` antes de `rm` |
| — | qualquer commit/push | exige autorização explícita sua |

**Regra geral:** nada é apagado permanentemente sem antes passar por quarentena ou confirmação sua.
