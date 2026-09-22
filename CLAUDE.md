# CLAUDE.md — `/Users/ana/Research`

Meta-workspace root for Ana Vanzin's ICONOCRACIA doctoral research.
This file is for Claude Code sessions; the human-readable counterpart is
[`README.md`](README.md).

> Global config: `~/.claude/CLAUDE.md` (always loaded). This file does **not**
> duplicate it — read it for user profile, environment, harness rules, citation
> defaults, conda env, caveman mode, etc.

## Workspace shape

This is a **meta-workspace, not a monorepo.** It versions only meta files; the canonical
list is in **[`.claude/AUTOMATION.md`](.claude/AUTOMATION.md)** under *Versioned surfaces*
and is deliberately not repeated here. Sub-repos are siblings with their own `.git`. The
tree below shows the workspace's shape, not the set of tracked paths.

```
/Users/ana/Research/      ← THIS REPO (git: anavvanzin/Research)
├── cowork/               ← 85 agentes + 12 integrações + opencode.json
├── docs/                 ← seminários, protótipos
├── .claude/              ← AUTOMATION.md + self-improving-agent + skills
├── .opencode/            ← plans/iconocracy-priority-plan.md
├── hub/
│   ├── iconocracy-corpus/ ← thesis monorepo (git: anavvanzin/iconocracy-corpus)
│   └── mnemosyne-scout/   ← scout staging area (no .git)
├── apps/                  ← iconocracia-companion, iconocracia-db, iconocracia-space
├── vaults/                ← Obsidian vaults (dir410340/346, iconocracy)
├── shared/                ← iconclass-data, the-book-of-secret-knowledge
├── hermes-workspace/      ← own .git
└── labs/                  ← experimental sub-repos
```

> <!-- drift-pin: 2026-09-22 real=`pipelines/` (Atlas, indexing) e
> `deep-memory/` ausentes na raiz; bloco abaixo é o estado alvo, não o atual.
> Repositórios órfãos foram movidos para `archive/` na organização de
> 2026-09-22 (ver docs/organizacao/). -->

```
alvo histórico (não reflete o disco):
├── pipelines/             ← Atlas, indexing (sibling sub-repos)  [ausente]
└── deep-memory/           ← own .git                          [ausente]
```

## Primary surface: the thesis

**`hub/iconocracy-corpus/`** is the canonical thesis monorepo.
Navigate: `cd hub/iconocracy-corpus`

Quick paths (from `hub/iconocracy-corpus/`):

| What | Path |
| --- | --- |
| Capítulos da tese | `tese/manuscrito/` (lar canônico; era `vault/tese/`) |
| Manuscrito + revisões | `tese/{manuscrito,revisoes}/` |
| Entrega mais recente | `tese/Entrega_Orientador_Mar2026_FINAL/` |
| Corpus canônico | `corpus/corpus-data.json` (336 itens; `hub/iconocracy-corpus/data/processed/records.jsonl` = 336 linhas — o drift de 1 item que esta linha descrevia não existe mais; conferido 2026-09-19) |
| Notebooks | `notebooks/` (01–08) |
| Compilação | `make -C vault/tese/` (Makefile permanece em `vault/tese/`; migração de chapters → `tese/manuscrito/` em 2026-06-04 não moveu o pipeline) |

## Sibling repos

- `deep-memory/` — Persistent-memory agent (own `.git`) <!-- drift-pin: 2026-09-22 ausente na raiz -->
- `hermes-workspace/` — Hermes experimental workspace (own `.git`)
- `apps/iconocracia-companion/` · `apps/iconocracia-db/` · `apps/iconocracia-space/`
- `pipelines/Atlas/` · `pipelines/indexing/` <!-- drift-pin: 2026-09-22 pipelines/ ausente na raiz -->
- `vaults/` — Obsidian vaults (see `vaults/CLAUDE.md`)
- `shared/` — shared datasets and reference libraries

## Remote / web sessions

This repo is cloned into remote and web Claude Code sessions (claude.ai/code, GitHub
integrations). Such a session gets **only the tracked meta-repo** — a Linux container at
`/home/user/Research`, not `/Users/ana/Research`. Absent by design:

| Not present remotely | Why |
| --- | --- |
| `hub/`, `apps/`, `pipelines/`, `vaults/`, `shared/`, `labs/`, `deep-memory/`, `hermes-workspace/` | Sibling sub-repos with their own `.git`; never tracked here |
| `~/.claude/agents/` (14 agents), `~/.claude/scheduled-tasks/` (13 tasks) | Live in the macOS home dir |
| `.claude/skills/{academic-research-skills,AutoResearchClaw,hegelian-dialectic,playwright}` | Exist on the Mac but were never committed. Canonical list: `.claude/AUTOMATION.md` |
| `.claude/worktrees/`, `Tools/`, `~/.hermes/` | 🖥️ host-only |
| **Plugins** (e.g. `claude-scientific-writer`) | Plugins do not sync to remote containers |

A `/plugin-name:command` that works on the Mac returns **Unknown command** here. That is
the plugin being absent, not a broken skill. When a capability must work everywhere, ship
it as a versioned skill under `.claude/skills/` — see `scientific-writer`.

Surfaces are marked 🖥️ **host-only** in [`.claude/AUTOMATION.md`](.claude/AUTOMATION.md).
Do not try to "restore" one in a remote session, and do not treat its absence as drift.

## Automation

Single index: → **[`.claude/AUTOMATION.md`](.claude/AUTOMATION.md)**

Governance docs are drift-checked in CI by `tests/test_docs_drift.py`.

Wiring ativo (`.claude/settings.json`): hooks do *self-improving-agent* em
PreToolUse Bash, PostToolUse Bash e SessionEnd, gravando em
`.claude/self-improving-agent/memory/`. Os hooks de lock/plano
(`.claude/hooks/*.sh`, estado em `.claude/locks/`) existem mas estão **inertes
por padrão** — só passam a valer se forem explicitamente ligados no
`settings.json`.

## Root-level commands (a raiz TEM verificação)

A raiz não é um codebase, mas tem CI própria e um par de comandos que valem para o
meta-workspace em si. O `AGENTS.md` diz o mesmo desde 2026-09-19 — os dois documentos
concordam.
<!-- drift-pin: 2026-09-19 dizia "ao contrário do que AGENTS.md afirma"; a ressalva
     virou obsoleta quando o AGENTS.md passou a liberar test/lint com escopo. -->

| Tarefa | Comando |
| --- | --- |
| Testes do repo | `pytest tests/` — `test_repo_sanity.py` compila (`py_compile`) todo `.py` versionado; `test_docs_drift.py` é a guarda de drift |
| Lint | `flake8 $(git ls-files '*.py') --select=E9,F63,F7,F82` (erros de sintaxe / nomes indefinidos) |
| Ambiente do CI | `conda env update --file environment.yml` — env `research`, **Python 3.10** |
| Guard de ownership (pre-commit) | `bash scripts/install-hooks.sh` (modo `info`; `enforce` bloqueia) · `python3 scripts/git_physics_guard.py` avulso |
| Statusline | `bash scripts/install-statusline.sh` |

**Derive do índice, não de diretórios:** no Mac a raiz também contém os sub-repos
irmãos, e `flake8 .` desce por eles. Passar `.claude/` também erra — lá vivem as skills
host-only nunca commitadas e as worktrees gitignored. `git ls-files '*.py'` devolve
exatamente o Python versionado. No container remoto o mesmo comando passa porque os
irmãos não estão lá; é comando que só quebra no Mac. O CI pode usar `.` justamente
porque lá só existe o meta-repo.

`.github/workflows/python-package-conda.yml` roda lint + `pytest` a cada push.
O smoke test existe justamente porque `pytest` sem teste coletável sai com
código 5 e quebra o job — não o remova ao adicionar testes reais.

**Dois Pythons, de propósito:** `environment.yml` (env `research`, 3.10) é só
para casar com o `actions/setup-python` do CI desta raiz. O ambiente canônico da
pesquisa continua sendo `iconocracy` (3.11), em `hub/iconocracy-corpus/`. Não
unifique um no outro.

`scripts/git_physics_guard.py` é detector **read-only**: lê
`docs/decisions/AGENT-OWNERSHIP.md` e valida que os caminhos staged pertencem ao
harness ativo (`--harness`, padrão `$HARNESS_ACTIVE` ou `codex-app`; `--mode enforce` para bloquear). Saída 0 = limpo, 1 = violação,
2 = erro do próprio script. Ele materializa a regra de contenção de sub-repos —
ao vê-lo bloquear um commit, o caminho provavelmente pertence a outro repo.

Os workflows `jekyll-gh-pages.yml` e `nextjs.yml` **eram** *samples* do GitHub que
nunca foram adaptados — não há site Jekyll nem app Next.js nesta raiz — e por isso
foram removidos em 2026-08-30; ver a nota em
[`.claude/AUTOMATION.md`](.claude/AUTOMATION.md). Resta apenas
`python-package-conda.yml`, que é deliberado.

## Sibling research repos (fora da árvore local)

Além dos sub-repos siblings listados acima, quatro repositórios da pesquisa vivem
no GitHub da autora e costumam ser clonados lado a lado em sessões remotas —
cada um com seu próprio `CLAUDE.md`:

| Repo | O que é |
| --- | --- |
| `anavvanzin/artigos` | Casa canônica dos artigos prontos + `tools/compilar.sh` e a auditoria transversal `tools/audit_artigos.py` |
| `anavvanzin/biblioteca` | Camada pública dos artigos (gerador estático → GitHub Pages) |
| `anavvanzin/ai-agent-notes` | Artigo sobre construção de agentes (só documentação) |
| `anavvanzin/kant-visao-computacional` | Relatório Kant × visão computacional (só dados; o relatório em si nunca foi commitado) |

A auditoria em `artigos/` assume os repositórios **irmãos no mesmo
diretório-pai**; fora dessa disposição, `--todos` e `--root` não encontram nada.

## Workflow Specifications

> ⚠️ **TODO drift 2026-07-29** — o diretório `hub/iconocracy-corpus/Specs/` não existe no repo atual (verificado). Os arquivos listados abaixo são referências históricas; confirmar se foram movidos (buscar em `docs/` ou `hub/iconocracy-corpus/docs/`) ou se nunca foram criados antes de tratar como autoritativos.

ICONOCRACY pipeline workflows (W1–W6 + S1–S5) *estariam* documentados em `Specs/WORKFLOW-*.md`:

| File | Content |
| --- | --- |
| `Specs/WORKFLOW-REGISTRY.md` | Master index: all workflows, item lifecycle, gate checklist |
| `Specs/WORKFLOW-iconocracy-corpus-acquisition.md` | W1: Gallica → vault → ledger |
| `Specs/WORKFLOW-iconocracy-visual-analysis.md` | W2: Panofsky + ENDURECIMENTO scoring |
| `Specs/WORKFLOW-iconocracy-synchronization.md` | W3: records.jsonl → vault → corpus-data.json → HF |
| `Specs/ZOTERO-MCP-SETUP-STATUS.md` | Zotero MCP troubleshooting (setup broken, use Web API fallback) |

Quando forem localizados/recriados, atualizar esta tabela; até lá, considerar referência quebrada.

## Conventions (workspace-specific)

- **Sub-repo containment.** Do NOT run `git add` on a **sub-repo** path
  (`hub/`, `apps/`, `pipelines/`, `vaults/`, `shared/`, `labs/`, `deep-memory/`,
  `hermes-workspace/`) — each has its own `.git`. The meta surfaces listed under
  *Versioned surfaces* in [`.claude/AUTOMATION.md`](.claude/AUTOMATION.md) are tracked
  here and may be edited normally.
  <!-- drift-pin: 2026-09-09 dizia "only cowork/ and docs/", já falso: tests/,
       scripts/, .github/ e .claude/ eram rastreados antes disso. -->
- **conda env:** `iconocracy` (Python 3.11 — env rebuilt 3.12→3.11 em 2026-06-22; use path version-agnostic `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python`). Never system Python.
- **ABNT NBR 6023:2025** for Portuguese drafts; Chicago for English.
- **Caveman mode** active by default (`~/.caveman-active`); `stop caveman` per session.
- Always confirm path before creating new files.
- **macOS session header.** When starting a session on macOS (primary host), open with
  `> ⚠️ macOS session` so agents avoid Linux-only skills (e.g. `ssd-health`) and use
  `/opt/homebrew/…` paths rather than `/home/ana/…`.
- **Checkpoints in long sessions.** For sessions longer than ~15 tool calls or spanning
  multiple pipeline stages, call `/checkpoint "<label>"` at each stage boundary so
  Code Review and resume have a clean diff story.

## What this file does *not* cover

- User profile, plan tier → `~/.claude/CLAUDE.md`
- Thesis pipeline internals → `hub/iconocracy-corpus/CLAUDE.md`
- Skill catalog → `find-skills` skill
