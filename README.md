# Research — Meta-workspace ICONOCRACIA

Meta-workspace da pesquisa de doutorado ICONOCRACIA (Ana Vanzin, UFSC).
Versiona apenas arquivos de configuração e documentação. Os repositórios
de produção vivem fora deste repo, com seu próprio `.git`.

## O que existe aqui

| O quê | Caminho | Descrição |
| --- | --- | --- |
| **Tese** | `hub/iconocracy-corpus/` | Monorepo canônico (264 itens de corpus, 265 registros, manuscrito, 69 scripts Python, 7 schemas JSON, notebooks Jupyter 01–08) |
| **Agentes** | `cowork/agents/` | 85 definições de agentes + 12 integrações de ferramentas |
| **Documentação** | `docs/` | Pacotes de seminários, planos de protótipos |
| **Automação** | `.claude/AUTOMATION.md` | Índice único de hooks, skills, agents, scheduled tasks |
| **Planos** | `.opencode/plans/` | Planos prioritários e roadmaps |

## Acesso rápido à tese

Caminhos a partir de `hub/iconocracy-corpus/`:

| O quê | Caminho |
| --- | --- |
| Capítulos da tese | `vault/tese/` |
| Manuscrito e revisões | `tese/manuscrito/` · `tese/revisoes/` |
| Entrega mais recente | `tese/Entrega_Orientador_Mar2026_FINAL/` |
| Corpus canônico | `corpus/corpus-data.json` (264 itens) |
| Notebooks | `notebooks/` (01–08) |
| Schemas JSON | `tools/schemas/` (7 schemas) |
| Método | `docs/methodology.md` |

## Projetos irmãos

- `deep-memory/` — agente de memória persistente (`.git` próprio)
- `hermes-workspace/` — workspace experimental Hermes (`.git` próprio)

## Convenções

- **Contenção de sub-repos.** Apenas `cowork/` e `docs/` são rastreados neste repo.
- **Ambiente conda:** `iconocracy` (Python 3.12). Nunca usar Python do sistema.
- **Citação:** ABNT NBR 6023:2025 para português; Chicago para inglês.
- **Automação:** Consulte `.claude/AUTOMATION.md` antes de adicionar hooks, skills ou agents.
- **Navegação para a tese:** `cd hub/iconocracy-corpus/` e leia o `CLAUDE.md` de lá.
