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
| Corpus / dados | `hub/iconocracy-corpus/corpus/corpus-data.json` | Hook protege contra binários crus em `hub/iconocracy-corpus/data/raw/` |
| Notebooks análise | `hub/iconocracy-corpus/notebooks/` | conda env `iconocracy` (Python 3.11 — rebuild 3.12→3.11 em 2026-06-22) |
| Workflows W1–W6 / S1–S5 | `hub/iconocracy-corpus/Specs/WORKFLOW-*.md` (**TODO drift 2026-07-29**: diretório `Specs/` ausente no repo; verificar se foi movido ou nunca criado) | Docs autoritativos de pipeline (referência quebrada) |
| Agentes / integrações cowork | `cowork/agents/` · `cowork/integrations/` | 85 agentes The Agency; tracked nesta raiz |
| Plano de prioridade | `.opencode/plans/iconocracy-priority-plan.md` | Horizontes + desbloqueios |
| Hooks / automação inventário | `.claude/AUTOMATION.md` | Índice único; atualize ao adicionar |
| Descobrir skill | Invocar skill `find-skills` | NÃO enumerar skills manualmente |

## Convenções herdadas

- Citação: ABNT NBR 6023:2025 (PT), Chicago (EN).
- conda env: `iconocracy` em `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/`.
- Idioma de resposta: português (perfil global). Identificadores de código no original.

## Cron jobs (regra)

- Todo cron job que usa LLM **DEVE** ser criado com `model` explícito (provider + model)
  para evitar drift quando o provider global mudar. Ex.: `model: {provider: "google", model: "gemini-3.1-pro-preview"}`.
- Após qualquer `hermes model` ou troca de provider global, rodar verificação de saúde:
  ```bash
  hermes cron list 2>&1 | grep -i "error\|drift\|skipped"
  ```
- Jobs com script Python que falham por drift **DEVEM** ser pinados imediatamente —
  não acumular. Cada job quebrado é pipeline de pesquisa silenciosamente parada.
- Jobs LLM-driven (sem `no_agent=true`) devem ser testados com `cronjob action='run'`
  após alteração de prompt ou troca de modelo, antes do próximo agendamento.

## Descoberta de skills (regra)

- **Nunca** enumerar skills manualmente. Usar `find-skills`:
  - `find-skills <intent>` para busca semântica
  - Se `find-skills` não achar, usar `hermes skills list <category>` com filtro
  - Só como último recurso: `skills_list` e busca visual
- 594 skills instaladas (Jul/2026). A maioria é ruído para o workflow ICONOCRACY.
  Confiar no `find-skills`, não na memória.

## Drift protocol (anti-classe-de-bug)

A classe de bug dominante em jun-2026 foi **config apontando para uma
realidade que mudou**: `python3.12` hardcoded vs 3.11 real, vault Obsidian
em path inexistente, corpus N=314 vs 265 reais, validação ajv em draft-07
mascarando schema 2020-12, email `warholana@msn.com` em commit local
rejeitado pelo GitHub. Cada fix foi one-off; este protocolo torna a classe
detectável.

### Antes de qualquer commit que mencione path / env / N / schema

```bash
# 1. Rodar o detector (skill drift-detector)
python3 ~/.hermes/skills/research/drift-detector/scripts/detect_drift.py --quiet
# exit 1 = HIGH drift detectado → PARE e atualize o doc primeiro
# exit 0 = OK prossiga

# 2. Conferências manuais para os pontos quentes
ls -d ~/Research/hub/iconocracy-corpus                  # canonical repo
ls -d ~/Obsidian/vida-os                                # vault real
ls -d /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy   # conda env
ls ~/Research/hub/iconocracy-corpus/vault/candidatos/SCOUT-*.md 2>/dev/null \
  | grep -v SCOUT-ZW- | grep -v SCOUT-SESSION- | grep -v SCOUT-NC- | wc -l   # N regular
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python --version   # python real
```

### Se drift detectado

1. **Atualize o doc com o valor real, NÃO o valor declarado.** O doc é
   o que está errado. "Fix" silencioso em código sem atualizar doc só
   esconde a classe de bug.
2. Commite o doc no mesmo commit do fix (atomicidade).
3. Memory `~/.hermes/memories/MEMORY.md` ganha entrada curta descrevendo
   o drift detectado e onde o fix foi aplicado.

### Quando o doc é a verdade e o sistema precisa ser corrigido

(Ex.: path mudou e o doc ainda aponta pro antigo mas você quer preservar
a nomenclatura do doc.) Marque o trecho do doc com data:

```markdown
Python 3.12 <!-- drift-pin: 2026-06-23 real=3.11.15, fix tracked in commit X -->
```

O detector não tem heurística para ler HTML comments ainda, mas isso
impede o próximo leitor de propagar o número errado.

## Coding Tasks

Ao spawnar sessões Claude Code para trabalho de coding, diga à sessão para usar
as skills do gstack (instalado em `~/.claude/skills/gstack`). Exemplos de prompt
para a sessão spawnada:

- **security audit:** `Load gstack. Run /cso`
- **code review:** `Load gstack. Run /review`
- **QA test a URL:** `Load gstack. Run /qa https://...`
- **build a feature end-to-end:** `Load gstack. Run /autoplan, implement the plan, then run /ship`
- **plan before building:** `Load gstack. Run /office-hours then /autoplan. Save the plan, don't implement.`
