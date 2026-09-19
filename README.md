# Research — Meta-workspace ICONOCRACIA

Meta-workspace da pesquisa de doutorado ICONOCRACIA (Ana Vanzin, UFSC).
Versiona apenas arquivos de configuração e documentação. Os repositórios
de produção vivem fora deste repo, com seu próprio `.git`.

## O que existe aqui

| O quê | Caminho | Descrição |
| --- | --- | --- |
| **Tese** | `hub/iconocracy-corpus/` | Monorepo canônico (336 itens de corpus, 336 registros no ledger, manuscrito, 319 arquivos Python rastreados — 115 deles em `tools/scripts/` —, 9 schemas JSON, notebooks Jupyter 01–08). Conferido em 2026-09-19; ver a nota de contagens abaixo. |
| **Agentes** | `cowork/agents/` | 85 definições de agentes + 12 integrações de ferramentas |
| **Documentação** | `docs/` | Pacotes de seminários, planos de protótipos |
| **Automação** | `.claude/AUTOMATION.md` | Índice único de hooks, skills, agents, scheduled tasks |
| **Planos** | `.opencode/plans/` | Planos prioritários e roadmaps |

## Acesso rápido à tese — 🖥️ host-only

Caminhos relativos a `hub/iconocracy-corpus/`, um sub-repo irmão com `.git`
próprio. Não existe em sessões remotas/web — ver **Remote / web sessions** em
[`CLAUDE.md`](CLAUDE.md).

| O quê | Caminho |
| --- | --- |
| Capítulos da tese | `tese/manuscrito/` (lar canônico desde 2026-06-04; era `vault/tese/`) |
| Revisões | `tese/revisoes/` |
| Compilação | `make -C vault/tese/` (Makefile permanece aqui; migração pendente) |
| Entrega mais recente | `tese/Entrega_Orientador_Mar2026_FINAL/` |
| Corpus canônico | `corpus/corpus-data.json` (336 itens) |
| Notebooks | `notebooks/` (01–08) |
| Schemas JSON | `tools/schemas/` (7 schemas) |
| Método | `docs/methodology.md` |

### Protocolo de consultas do microcorpus

A seleção das 12 consultas para comparação HOG/CLIP é regida pela decisão de
[seleção reprodutível das consultas do microcorpus](docs/decisions/2026-09-09-selecao-consultas-microcorpus.md).
Ela exige sorteio estratificado com uma segunda seed fixa, validações estáticas
e registro da SHA-256 de `hub/iconocracy-corpus/data/queries.csv` — o artefato canônico
nomeado pelo ADR, no sub-repo da tese, não nesta raiz — antes da geração dos rankings.

### Contagens da tese — 🖥️ host-only, fora da guarda

Os números acima descrevem `hub/iconocracy-corpus/`, **sub-repo irmão com `.git` próprio**.
`tests/test_docs_drift.py` não os alcança: numa sessão remota o diretório não existe, e a
guarda só confere o que está nesta árvore. São, portanto, a classe de afirmação que mais
apodrece aqui — o par 264/265 sobreviveu neste README enquanto o corpus ia a 336.

Duas regras para quem editar:

- **Denominador junto do número.** "69 scripts Python" apodreceu invisível porque ninguém
  sabia o que contava. Hoje: 319 arquivos `.py` rastreados por `git ls-files` no sub-repo,
  115 deles em `tools/scripts/` e 114 em `archive/code-legacy/`.
- **Data da conferência junto do valor.** Quem reconferir, atualiza as duas coisas.

**336 é inventário, não N de estatística.** O campo `support` dos 336 itens está longe de
harmonizado, e é o gate de `iconocracy-corpus#210` que decide o que pode ser amostrado por
estrato. Contado contra o clone em 2026-09-19, com o gate corrigido:

| Classe | N | O que é |
| --- | --- | --- |
| inventário operacional | **336** | tudo que está em `corpus/corpus-data.json` |
| estrato limpo (amostrável hoje) | **152** | `moeda` 85 · `cartaz` 26 · `selo` 12 · `pintura` 8 · `papel-moeda` 7 · outros |
| composto, aguarda adjudicação | **90** | `estampa/gravura` 61 · `monumento/escultura` 22 · outros |
| não mapeado, aguarda adjudicação | **11** | `medalha` 3 · `cerâmica` 2 · `vitral` · outros |
| pendente (`?` ou vazio) | **83** | `?` 76 · vazio 7 |

Os 184 das três últimas linhas não entram em estatística nenhuma até alguém decidir o que
são — e se `estampa/gravura` é um estrato ou dois é decisão de pesquisa, não de script.

Última conferência: **2026-09-19**, contra o clone de `anavvanzin/iconocracy-corpus`
(`corpus/corpus-data.json` = 336 entradas; `hub/iconocracy-corpus/data/processed/records.jsonl`
= 336 linhas).

## Projetos irmãos

- `deep-memory/` — agente de memória persistente (`.git` próprio)
- `hermes-workspace/` — workspace experimental Hermes (`.git` próprio)

## Convenções

- **Contenção de sub-repos.** Não rode `git add` em caminho de sub-repo (cada um tem
  seu `.git`). As superfícies-meta versionadas aqui estão listadas em
  [`.claude/AUTOMATION.md`](.claude/AUTOMATION.md) (*Versioned surfaces*).
- **Ambiente conda:** `iconocracy` (Python 3.11 — rebuild 3.12→3.11 em 2026-06-22).  
- **Citação:** ABNT NBR 6023:2025 para português; Chicago para inglês.
- **Automação:** Consulte `.claude/AUTOMATION.md` antes de adicionar hooks, skills ou agents.
- **Navegação para a tese:** `cd hub/iconocracy-corpus/` e leia o `CLAUDE.md` de lá.
