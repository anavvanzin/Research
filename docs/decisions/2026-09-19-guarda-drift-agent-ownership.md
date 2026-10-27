---
tags: [meta, ownership, git-physics, ci, drift]
date: 2026-09-19
scope: meta-workspace path ownership
status: ACTIVE
accepted_by: Ana Vanzin
accepted_date: 2026-09-19
related:
  - ./AGENT-OWNERSHIP.md
  - ./2026-06-25-multi-harness-git-physics.md
  - ./2026-09-09-aposentar-workflows-sample.md
---

# Pôr `AGENT-OWNERSHIP.md` sob a guarda de drift

ADR exigido pela regra do próprio [`AGENT-OWNERSHIP.md`](./AGENT-OWNERSHIP.md):
*"Qualquer mudança aqui = ADR em `docs/decisions/` referenciando este arquivo."*

## Contexto

`tests/test_docs_drift.py` nasceu cobrindo quatro documentos de governança em prosa:
`CLAUDE.md`, `README.md`, `AGENTS.md` e `.claude/AUTOMATION.md`. O
`AGENT-OWNERSHIP.md` ficou de fora, e a razão registrada na PR #28 foi que incluí-lo
exigiria anotar as seções aposentadas — custo sem ganho evidente.

O ganho existe, e é de outra natureza. Os quatro docs originais são lidos por humanos e
por agentes; este é lido por **máquina**. `scripts/git_physics_guard.py` parseia esta
matriz para decidir a que harness pertence cada path staged. Um caminho podre aqui não
produz um link quebrado: produz um guard distribuindo permissão sobre superfície que não
existe. Foi exatamente o que a terceira rodada de revisão da PR #28 encontrou à mão,
depois que a remoção dos dois workflows sample deixou as seções `jekyll-gh-pages` e
`nextjs-deploy` apontando para arquivos apagados.

Uma verificação que só roda quando alguém olha não é verificação.

## Decisão

Acrescentar `docs/decisions/AGENT-OWNERSHIP.md` a `GOVERNANCE_DOCS` em
`tests/test_docs_drift.py`.

A guarda passa a conferir **23** afirmações de caminho neste arquivo. Cinco linhas recebem
`<!-- drift-pin: 2026-09-19 ... -->`, em duas classes distintas, e a distinção importa
mais que a contagem.

### Classe 1 — referência histórica (3 linhas)

`.github/workflows/jekyll-gh-pages.yml` e `.github/workflows/nextjs.yml`, citados nas
duas seções aposentadas para explicar o que o harness versionava antes. Os arquivos
foram removidos de propósito em 2026-08-30. É o mesmo tratamento que
`.claude/AUTOMATION.md` já dá ao registrar a remoção.

### Classe 2 — grant de namespace ainda não materializado (2 linhas)

`cowork/codex/` e `cowork/engineering/drift-detector/`. Na primeira leitura pareciam
drift: paths declarados que não existem em disco. Não são.

A regra de leitura no topo do próprio arquivo diz que a coluna *Owns* lista "paths que o
harness **pode** adicionar (`git add`) e commitar". É concessão de namespace, não
inventário — um diretório que ainda não foi criado é o estado normal de uma concessão
que ninguém exerceu.

Isso expõe um descompasso entre o predicado da guarda (o caminho existe?) e o que a
coluna *Owns* afirma (o caminho é permitido?). A guarda não sabe distinguir os dois, e
não vale ensiná-la: seria uma regra específica de um arquivo dentro de um teste que é
genérico de propósito. O `drift-pin` é o escape previsto justamente para "o doc está
certo e a realidade é que não chegou lá" — o `AGENTS.md` o define nesses termos.

Consequência a assumir: enquanto o pin estiver de pé, essas duas linhas não são
conferidas. Se algum dia um dos dois diretórios for criado, tirar o pin e deixar a
guarda passar a cobri-lo.

## O que isto NÃO entrega

Não valida a semântica da matriz. A guarda confere que um caminho citado existe; não
confere que a atribuição harness→path faz sentido, nem que as colunas *Forbidden* são
coerentes entre si, nem que os 13 `HARNESS_ACTIVE` cobrem os harnesses em uso. Isso
segue sendo leitura humana.

A cobertura efetiva são as 23 afirmações não pinadas — entre elas
`.claude/self-improving-agent/`, `plans/`, `.planning/`, `docs/decisions/`, os arquivos
de raiz e os dois links para o ADR de 2026-09-09. Renomear ou remover qualquer um deles
com a referência de pé passa a falhar o build.

## Verificação

```
pytest tests/                                          → verde
flake8 $(git ls-files '*.py') --select=E9,F63,F7,F82   → 0
python3 scripts/git_physics_guard.py                   → exit 0
```

O ganho desta mudança são **23 casos novos** de `test_documented_path_exists`, ancorados
neste arquivo. O total da suíte de propósito não fica registrado aqui: ele se move a cada
commit que toque qualquer doc de governança, então fixá-lo num ADR é plantar exatamente a
divergência numérica que o *Drift protocol* manda corrigir — foi o que aconteceu com a
primeira versão deste bloco, que dizia 141 quando o head já trazia 145.

Os 13 ids `HARNESS_ACTIVE` seguem sendo parseados após as anotações — os pins são
comentários HTML e não tocam os cabeçalhos `### <nome> (HARNESS_ACTIVE=<id>)` que o
guard casa.

Teste negativo: tirar o pin da linha do `nextjs.yml` faz
`test_documented_path_exists[docs/decisions/AGENT-OWNERSHIP.md:112:.github/workflows/nextjs.yml]`
falhar; recolocado, passa.
