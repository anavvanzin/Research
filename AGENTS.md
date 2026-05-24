# AGENTS.md — Research Meta-Workspace

Meta-workspace da pesquisa de doutorado ICONOCRACIA (Ana Vanzin).
Guia compacto para agentes **OpenCode**.

## Natureza

**Meta-workspace, não uma codebase.** Versiona apenas arquivos de configuração
(README, CLAUDE.md, .gitignore, docs/). O trabalho real da tese vive em
sub-repos com seu próprio `.git`.

## Superfície primária

**`hub/iconocracy-corpus/`** — monorepo canônico da tese ICONOCRACIA
(dados, código, notebooks, manuscrito, vault). Possui `CLAUDE.md`
autoritativo próprio — consulte-o para qualquer trabalho na tese.

## Planos

**`.opencode/plans/`** — planos de prioridade e cronograma da tese:
- `iconocracy-priority-plan.md` — horizontes, desbloqueios e projeções

## Agentes

**`cowork/agents/`** — 85 agentes (The Agency) em `academic/`, `design/`,
`engineering/`, `specialized/`. **`cowork/integrations/`** — tools.

## Automação

**`.claude/AUTOMATION.md`** — índice canônico de hooks, skills, agents,
scheduled tasks e worktrees. Leia antes de modificar qualquer automação.

## Regras

- Sub-repos (`hub/`, `apps/`, `pipelines/`, `labs/`, `vaults/`, `shared/`)
  têm `.git` próprio e NÃO devem ser rastreados neste repositório.
- Para a tese, abra `hub/iconocracy-corpus/` como workspace separado.
- Tooling em `cowork/`; a raiz não é um projeto npm.
- Docs: [`README.md`](README.md) (humano), [`CLAUDE.md`](CLAUDE.md) (Claude Code).
