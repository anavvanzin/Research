# AGENTS.md — `/Users/ana/Research`

Meta-workspace de pesquisa de doutorado (ICONOCRACIA, Ana Vanzin). Este arquivo
orienta agentes de IA; humano: [`README.md`](README.md); Claude Code:
[`CLAUDE.md`](CLAUDE.md); global: `~/.claude/CLAUDE.md`.

## Natureza

**Meta-workspace, NÃO codebase.** A raiz versiona apenas `cowork/`, `docs/`,
`.claude/AUTOMATION.md`, `.gitignore`. Trabalho real vive em sub-repos com
`.git` próprio.

## Constraints de acesso (read-only / proibições)

- Agentes **MUST NOT** rodar `git add` fora de `cowork/` ou `docs/`. Sub-repos
  (`hub/`, `apps/`, `pipelines/`, `vaults/`, `shared/`, `labs/`, `deep-memory/`,
  `hermes-workspace/`) têm `.git` próprio — operar dentro deles.
- Agentes **MUST NOT** executar `build`, `test`, `lint`, `typecheck` na raiz:
  não há `package.json`/`pyproject.toml` aqui. Desça ao sub-repo.
- Agentes **MUST NOT** modificar `.claude/AUTOMATION.md` sem ler integralmente
  antes — é índice canônico de hooks/skills/agents/scheduled tasks.
- Agentes **MUST NOT** criar arquivos novos sem confirmar caminho-alvo (regra
  global `~/.claude/CLAUDE.md` — Project Paths).
- `tese/`, `corpus/`, `vault/` em `hub/iconocracy-corpus/` têm denies globais
  contra `rm -rf` e `git reset --hard` — não tentar contornar.

## Verificação one-shot (quando aplicável)

Não há comandos one-shot **na raiz**. Por sub-repo:

| Tarefa | Comando | Diretório |
|---|---|---|
| Compilar tese | `make -C vault/tese/` (Makefile canônico; chapters foram migrados para `tese/manuscrito/` em 2026-06-04, pipeline ainda não) | `hub/iconocracy-corpus/` |
| Validar corpus | `python tools/scripts/validate_schemas.py` | `hub/iconocracy-corpus/` |
| Build site | `bundle exec jekyll build` | `~/Projects/anavvanzin.github.io/` |
| Agente Hermes | ver `hermes-agent/AGENTS.md` se existir | `hermes-agent/` |

Agentes **MUST NOT** iniciar dev servers, watchers ou crons da raiz.

## Roteamento de tarefas

| Intent | Destino | Notas |
|---|---|---|
| Qualquer trabalho de tese | `hub/iconocracy-corpus/` | Tem `CLAUDE.md` autoritativo — leia-o primeiro |
| Editar capítulos | `hub/iconocracy-corpus/tese/manuscrito/` | Lar canônico de chapters desde 2026-06-04 |
| Compilar tese | `hub/iconocracy-corpus/vault/tese/` | `make docx`/`make pdf` — Makefile permanece aqui (migração pendente) |
| Corpus / dados | `hub/iconocracy-corpus/corpus/corpus-data.json` | Hook protege contra binários crus em `data/raw/` |
| Notebooks análise | `hub/iconocracy-corpus/notebooks/` | conda env `iconocracy` (Python 3.12) |
| Workflows W1–W6 / S1–S5 | `hub/iconocracy-corpus/Specs/WORKFLOW-*.md` | Docs autoritativos de pipeline |
| Agentes / integrações cowork | `cowork/agents/` · `cowork/integrations/` | 85 agentes The Agency; tracked nesta raiz |
| Plano de prioridade | `.opencode/plans/iconocracy-priority-plan.md` | Horizontes + desbloqueios |
| Hooks / automação inventário | `.claude/AUTOMATION.md` | Índice único; atualize ao adicionar |
| Descobrir skill | Invocar skill `find-skill` | NÃO enumerar skills manualmente |

## Convenções herdadas

- Citação: ABNT NBR 6023:2025 (PT), Chicago (EN).
- conda env: `iconocracy` em `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/`.
- Idioma de resposta: português (perfil global). Identificadores de código no original.
