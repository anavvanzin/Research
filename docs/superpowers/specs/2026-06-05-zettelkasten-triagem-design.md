# Triagem & Consolidação de Vaults Obsidian para Zettelkasten

**Sub-projeto A** do sistema Zettelkasten completo (A → B → C)

| | |
|---|---|
| **Data** | 2026-06-05 |
| **Autora** | Ana Vanzin |
| **Status** | Design aprovado em brainstorming, aguarda implementação |
| **Quali alvo** | Nov/2027 — projeto + Cap 1 vitrine |

---

## Contexto

Diagnóstico em 2026-06-05 identificou **13 diretórios `.obsidian/` no sistema**. Quadro real:

- **9 vaults vivos** (≥1 nota modificada nos últimos 30 dias)
- **3 cópias divergentes do iconocracy-corpus/vault** recebendo edits simultaneamente em paths diferentes (canon ativo hoje, GitHub há 6 dias, projetos há 12 dias)
- **1 vault ativo em ~/Downloads** (1032 notas, modificado há 4 dias — Downloads é zona de trânsito sem backup git)
- **~/Research raiz como vault container** com 6714 notas, abrigando sub-vaults Obsidian aninhados — fonte de divergência silenciosa

A divergência das 3 cópias do corpus invalida a reconciliação SSD completada em 2026-06-04 (ver `project_ssd_reconciliation_20260604`): se continuar editando em 3 lugares, próxima reconciliação volta a ter conflitos.

## Motivação

A usuária quer adotar método Zettelkasten **focado na tese de doutorado** (PPGD/UFSC, História do Direito Penal — alegoria feminina na cultura jurídica séc. XIX-XX), alinhando com quali nov/2027 = projeto + Cap 1 vitrine.

Sistema completo decompõe-se em 3 sub-projetos sequenciais:
- **A** (este doc): Triagem + consolidação dos 13 vaults em 1 vault canon
- **B** (futuro): Método Zettelkasten aplicado — convenções, atomização, MOC structure
- **C** (futuro): Workflow Z → Cap 1 — pipeline notas → outline → draft

Sem A, qualquer adoção de Z herda o caos atual. Daí a ordem.

## Goals

1. Criar **~/Zettelkasten/** como vault canon único para conhecimento tese
2. Arquivar fontes legacy em **~/Dropbox/vaults-archive-2026-06-05/** (sync automático, não-deleção)
3. Reconciliar 3 cópias do iconocracy-corpus/vault em 1 canon (parar divergência)
4. Eliminar vault em ~/Downloads (risco de perda)
5. Deletar vaults vazios/triviais (.obsidian/ órfão)
6. Manter `[[feedback_no_new_tooling_until_quali]]`: sem plugins novos, sem software adicional

## Non-goals (explicit out-of-scope)

- Definir método Z em detalhe (templates, plugins, atalhos) — vai para sub-projeto B
- Escrever Cap 1 a partir do Z — vai para sub-projeto C
- Migrar notas de OAB / advocacia / iuris-ops / pessoais / código — não cabem no Z só-tese
- Refatorar corpus iconocracia em si (dataset com schema, hooks de validação — fica como está)

---

## Arquitetura

### Target final

```
~/Zettelkasten/              # vault canon único, novo, local
├── .obsidian/               # config Obsidian baseline (vanilla)
├── README.md                # convenções pessoais (IDs, links, tipos)
├── _inbox/                  # fleeting notes: rascunhos, processar/descartar em até 7d
├── lit/                     # literature notes: 1 nota por fonte lida (sumário próprio)
├── zet/                     # permanent notes: atômicas, ID timestamp, com links cruzados
└── moc/                     # Maps of Content: índices temáticos navegáveis
```

### Archive de fontes legacy

```
~/Dropbox/vaults-archive-2026-06-05/    # sync automático Dropbox
├── README.md                            # status geral da triagem
├── research-root/                       # de ~/Research/ (notas exclusivas, sem sub-vaults)
├── documents-linux/                     # de ~/Documents/linux/
├── downloads-analise/                   # de ~/Downloads/ana 2026 main/ANAlise/
├── iconocracy-wiki-research/            # de ~/Research/hub/iconocracy-corpus/wiki/
├── iconocracy-wiki-github/              # de ~/Documents/GitHub/iconocracy-corpus/wiki/
├── iconocracy-wiki-projetos/            # de ~/projetos/.../wiki/
├── iconocracy-vault-github/             # de ~/Documents/GitHub/iconocracy-corpus/vault/
└── iconocracy-vault-projetos/           # de ~/projetos/.../vault/
```

Cada subpasta carrega `README.md` com origem, data do snapshot, status de revisão.

### Inventário de fontes (em 2026-06-05)

| Fonte | Notas | Última mod | Prioridade | Destino |
|-------|-------|------------|-----------|---------|
| ~/Research/hub/iconocracy-corpus/vault | 623 | hoje | **1** | **CANON** (mantém, dataset) |
| ~/Documents/GitHub/iconocracy-corpus/vault | 621 | 6d | 1 | Archive + delete cópia divergente |
| ~/projetos/research/hub/iconocracy-corpus/vault | 611 | 12d | 1 | Archive + delete cópia divergente |
| ~/Downloads/ana 2026 main/ANAlise | 1032 | 4d | **2** | Archive + review para Z |
| ~/Research (raiz, exclui sub-vaults) | ~5500 | hoje | **3** | Archive + review pasta-por-pasta |
| ~/Documents/linux | 1253 | 20d | 3 | Archive + review pasta-por-pasta |
| ~/Research/hub/iconocracy-corpus/wiki | 611 | 4d | 3 | Archive + dedup vs outras 2 wikis + review |
| ~/Documents/GitHub/iconocracy-corpus/wiki | 648 | 6d | 3 | Archive + dedup |
| ~/projetos/research/hub/iconocracy-corpus/wiki | 611 | 16d | 3 | Archive + dedup |
| ~/Documents/Obsidian Vault | 0 | — | **4** | rm -rf (.obsidian/ órfão) |
| ~/Research/Chaos | 1 | hoje | 4 | Archive + delete |
| iCloud anavanzinthesis | 0 | — | 4 | rm -rf .obsidian/ órfão |
| Obsidian Sandbox | — | — | 4 | rm -rf |

---

## Componentes & Critério Z

### Critério operacional "serve para tese?"

Aplicado durante review de cada nota legacy:

**✓ MIGRA** (vira nota Z atomic):
- Fonte primária da tese (Sbriccoli, Hespanha, Foucault, Nilo Batista, IKV-ICW, Diego Nunes, etc.)
- Conceito-chave (alegoria feminina, codificação, escola positiva, justiça criminal histórica, iconologia jurídica)
- Fragmento textual reaproveitável em Cap 1 ou projeto quali
- Notas sobre objeto iconográfico (em conexão com corpus)

**✗ NÃO MIGRA** (fica em archive, recuperável se mudar de ideia):
- OAB, leis brasileiras contemporâneas
- Advocacia, iuris-ops, Estúdio Vanzin
- Código, configuração, infraestrutura
- Pessoal não-acadêmico
- Screenshots/anexos sem texto próprio

**? CASO DUVIDOSO**:
- Metodológicas (Iconclass, ABNT, history methodology) → migra SE com aplicação direta à tese, descarta se genérico
- Disciplina DIR410346 (memoriais, fichamentos) → migra (alinha com Cap 1 e dialoga com tese)

### Convenções Z (no README do vault)

- **ID**: `YYMMDDHHMMSS-slug-curto.md`. Timestamp para unicidade técnica + slug humano para legibilidade.
- **Atomicidade**: uma nota = uma ideia. 100-400 palavras típico, raramente >800.
- **Links**: `[[id]]` para conexões internas, `[@bibtex-key]` para citações ABNT, `#tag` apenas para tipo (`#lit`, `#zet`, `#moc`).
- **MOCs**: pontos de entrada narrativos. `moc/alegoria-feminina.md` lista as `zet/` relevantes em texto, não bullet (estilo Luhmann).
- **Frontmatter**: `title`, `created`, `type` (lit|zet|moc), `source` (se literature note).

### Procedimento de archive (Fase 1)

```bash
# Para cada fonte:
mkdir -p ~/Dropbox/vaults-archive-2026-06-05/<nome>/
rsync -aHp <fonte>/ ~/Dropbox/vaults-archive-2026-06-05/<nome>/
# Cria README.md com: origem-original, data-snapshot, contagem-notas, status="aguardando review"
# AGUARDA Dropbox sync (ícone verde) ANTES de prosseguir
```

### Procedimento de review (Fase 4)

Por pasta de fonte:
1. `ls` top-level → identifica clusters temáticos
2. Para cada cluster:
   - migra todo cluster (raro)
   - migra notas específicas (comum)
   - descarta cluster (comum)
3. Notas a migrar: **cria nota Z nova** (não copy-paste literal). Atomiza (1 ideia = 1 nota), atribui ID timestamp, conecta a MOC.
4. Marca pasta original no README do archive como `reviewed YYYY-MM-DD`.

---

## Execução

### Fases ordenadas

| Fase | O que | Esforço | Bloqueia? |
|------|-------|---------|-----------|
| **F1** Snapshot Archive | rsync TODAS fontes → ~/Dropbox/vaults-archive-2026-06-05/. README em cada subpasta. Aguarda sync. | ~30 min | — |
| **F2** Reconciliar 3 cópias corpus | Diff canon vs GitHub vs projetos; merge únicas em canon; delete 2 cópias divergentes (só após archive Dropbox confirmado). | ~1 h | F1 |
| **F3** Scaffold ~/Zettelkasten/ | mkdir + README + 4 subfolders + 1 nota piloto. | ~15 min | — |
| **F4** Pull por fonte | Review pasta-por-pasta de cada Prioridade 3. Decisão por cluster. Migração com atomização. | 30-60 min × 5-10 sessões | F3 |
| **F5** Descarte fáceis | rm -rf .obsidian/ dos vaults vazios. | ~10 min | F1 |
| **F6** Limpeza Research raiz | Decidir destino de .obsidian em ~/Research (fechar como vault? manter como repo só código?). | ~20 min | F4 |

**Total estimado**: 8-15 horas, distribuídas em 10-15 sessões curtas. F1+F2+F3+F5 podem fazer em 1 dia (~2h). F4 é o longo.

### Critério "A done"

- [ ] ~/Zettelkasten/ existe com ≥10 notas Z genuinely atomic (não copy-paste)
- [ ] Todas fontes legacy snapshot em ~/Dropbox/vaults-archive-2026-06-05/ com README de proveniência
- [ ] 3 cópias do corpus iconocracia reconciliadas → 1 canon
- [ ] ~/Downloads/ sem nenhum vault ativo
- [ ] Vaults vazios deletados (.obsidian/ removido)
- [ ] Decisão registrada sobre ~/Research raiz (vault/não-vault)

### Transição para sub-projeto B

Não precisa esperar todas as fases. **Quando Z tiver ~50-100 notas migradas e workflow rodando consistentemente**, abre brainstorming de B (método Z aplicado: refinamento convenções, MOC structure, templates Obsidian, atalhos).

---

## Riscos & Mitigações

| Risco | Mitigação |
|-------|-----------|
| Perda de notas durante migração | F1 (snapshot) acontece ANTES de qualquer remoção. Rollback é `cp` de volta. |
| Reconciliação corpus quebra canon | F2 usa `rsync --dry-run` primeiro. Commit por etapa no git Research. |
| ~/Dropbox sync incompleto antes de remover fontes | Verificação manual: ícone verde + listagem remota antes de F2/F5. |
| Migração vira copy-paste literal (não atomização) | F4 procedure exige "cria nota Z nova", não copy. Self-check: a nota tem 1 ideia? Tem ID timestamp? Tem ≥1 link saindo? |
| F4 se arrasta indefinidamente | Abre B com Z=50-100 notas mesmo que F4 não esteja concluído. Resto de F4 vira backlog. |
| Adoção de plugin novo "porque seria útil" | Hard rule: vanilla Obsidian até quali. README do Z documenta esta regra. |

---

## Out of scope (explicit)

- Método Z em si (atomic note guidelines detalhadas, MOC patterns, refactoring de notas Z) — sub-projeto B
- Workflow Z → outline → Cap 1 draft — sub-projeto C
- Plugins Obsidian community (Dataview, Templater, Excalidraw, etc.) — bloqueado por [[feedback_no_new_tooling_until_quali]]
- Sync Obsidian paid — não considerado
- Migração de notas não-tese (OAB, advocacia, iuris-ops, pessoal, código) — fica em archive, recuperável

---

## Referências

- [[feedback_no_new_tooling_until_quali]] — freeze de tooling até nov/2027
- [[feedback_challenge_more_ready]] — critério tese-only alinha
- [[project_quali_2027_deliverable]] — quali = projeto + Cap 1 vitrine
- [[project_workspace_canonical]] — ~/Research é repo canon
- [[project_ssd_reconciliation_20260604]] — base para reconciliação F2
- [[project_corpus_decision_20260530]] — corpus N=265, validity-stratum
- [[user_cloud_redundancy]] — Dropbox sincronizado, justifica archive lá
- [[project_harness_prune_20260605]] — prune do harness feito antes; mesma filosofia de "redução vai bem com freeze"
