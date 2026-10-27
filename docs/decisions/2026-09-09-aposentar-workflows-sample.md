---
tags: [meta, ci, ownership, git-physics]
date: 2026-09-09
scope: meta-workspace CI surfaces
status: ACTIVE
accepted_by: Ana Vanzin
accepted_date: 2026-09-09
related:
  - ./AGENT-OWNERSHIP.md
  - ./2026-06-25-multi-harness-git-physics.md
---

# Aposentar os workflows sample de deploy (`jekyll-gh-pages`, `nextjs`)

ADR exigido pela regra do próprio [`AGENT-OWNERSHIP.md`](./AGENT-OWNERSHIP.md):
*"Qualquer mudança aqui = ADR em `docs/decisions/` referenciando este arquivo."*

## Contexto

`.github/workflows/jekyll-gh-pages.yml` e `.github/workflows/nextjs.yml` eram
templates de exemplo do GitHub, adicionados sem adaptação. Esta raiz não tem
`_config.yml`, nem `package.json`, nem app Next.js — nenhum dos dois podia
produzir um deploy real. Ambos disparavam a cada push para `main` e disputavam o
mesmo grupo de concorrência `pages`.

Foram removidos em 2026-08-30 (PR #28). A matriz de ownership, porém, continuou
atribuindo esses paths a dois harnesses, e o resumo em
[`2026-06-25-multi-harness-git-physics.md`](./2026-06-25-multi-harness-git-physics.md)
repetia a mesma configuração. Como `scripts/git_physics_guard.py` lê a matriz
como contrato canônico, operadores e o guard continuavam reconhecendo superfícies
de deploy que não existem mais.

## Decisão

1. As seções `jekyll-gh-pages` e `Next.js deploy` em `AGENT-OWNERSHIP.md` ficam
   marcadas como **APOSENTADAS**, com a coluna `Owns` esvaziada nesta raiz.
2. As seções **não são removidas**. O guard casa harnesses pelo cabeçalho
   `### <nome> (\`HARNESS_ACTIVE=<id>\`)`; apagá-las faria um `HARNESS_ACTIVE`
   legado ainda exportado no shell de alguém cair em "harness desconhecido".
   Mantê-las vazias é degradação suave.
3. O ADR de 2026-06-25 recebe apenas uma nota de rodapé apontando para cá — é
   registro histórico e descreve corretamente o estado daquela data; não se
   reescreve o passado.

## Consequências

- Nenhum harness versiona `.github/workflows/*` de deploy nesta raiz.
- `python-package-conda.yml` continua sendo o único workflow, e é deliberado:
  roda `flake8` + `pytest` a cada push, com `tests/test_repo_sanity.py` e
  `tests/test_docs_drift.py`.
- Se um site Jekyll ou app Next.js voltar a viver **nesta raiz** (hoje não é o
  caso — ambos vivem em sub-repos), reativar exige novo ADR e repovoar a coluna
  `Owns` correspondente.

## Alternativas descartadas

- **Apagar as seções.** Quebraria um `HARNESS_ACTIVE` legado, conforme acima.
- **Deixar como estava.** Mantinha a matriz canônica descrevendo arquivos
  inexistentes — exatamente a classe de bug que o *Drift protocol* do
  [`AGENTS.md`](../../AGENTS.md) existe para impedir.
