---
tags: [meta, ownership, contract, git-physics, multi-harness]
date: 2026-06-25
scope: meta-workspace path ownership
status: ACTIVE (companion to 2026-06-25-multi-harness-git-physics.md)
accepted_by: Ana Vanzin
accepted_date: 2026-06-25
supersedes: implicit "versionar apenas cowork/, docs/, .claude/AUTOMATION.md"
related:
  - ./2026-06-25-multi-harness-git-physics.md
---

# AGENT-OWNERSHIP — Matriz canônica de paths por harness

> Este arquivo é o **contrato vivo** de quem pode versionar o quê no
> meta-repo `/Users/ana/Research/`. Qualquer mudança aqui = ADR
> em `docs/decisions/` referenciando este arquivo.
>
> **Regra de leitura**: a coluna "Owns" lista paths que o harness
> pode adicionar (`git add`) e commitar no meta-repo raiz. A coluna
> "Forbidden" lista paths onde adicionar/commit é bloqueado pelo
> pre-commit guard (fase β). "Read" é universal: todo harness pode
> ler qualquer path,respeitando .gitignore.

## Harness owners (6)

### Codex app (`HARNESS_ACTIVE=codex-app`)

| Owns (pode versionar)         | Forbidden                                        | Read |
|-------------------------------|--------------------------------------------------|------|
| `.agents/`                    | `.hermes/`, `.antigravity/`, `.copilot/`         | tudo |
| `.codex/` (config canônica)   | `.claude/skills/`-write, `.learnings/`-write     | tudo |
| `cowork/codex/`               | `docs/decisions/`-write exclusivo                | tudo |

Runtime ignorado: `.codex/cache/`, `.codex/sessions/`.

### Claude CLI (`HARNESS_ACTIVE=claude-cli`)

| Owns                          | Forbidden                                        | Read |
|-------------------------------|--------------------------------------------------|------|
| `.claude/`                    | `.codex/`, `.hermes/`, `.antigravity/`, `.copilot/` | tudo |
| `docs/decisions/`-append      | `.learnings/`-write                              | tudo |

Runtime ignorado: `.claude/skills/*/runtime/`, `.claude/skills/*/.cache/`.

### GitHub Copilot (`HARNESS_ACTIVE=copilot`)

| Owns                          | Forbidden                                        | Read |
|-------------------------------|--------------------------------------------------|------|
| `.copilot/`                   | (todos os outros paths do meta-repo)             | tudo |

Runtime ignorado: `.copilot/cache/`.

### Antigravity 2.0 (`HARNESS_ACTIVE=antigravity`)

| Owns                          | Forbidden                                        | Read |
|-------------------------------|--------------------------------------------------|------|
| `.antigravity/`               | (todos os outros paths do meta-repo)             | tudo |

Runtime ignorado: `.antigravity/cache/`, `.antigravity/sessions/`.

### Hermes CLI (`HARNESS_ACTIVE=hermes-cli`)

| Owns                          | Forbidden                                        | Read |
|-------------------------------|--------------------------------------------------|------|
| `.hermes/`                    | `.codex/`, `.claude/`, `.antigravity/`, `.copilot/` | tudo |
| `hermes/`                     | `.learnings/`-write                              | tudo |

Runtime ignorado: `.hermes/conversations/`, `.hermes/cache/`.

### Claude app (`HARNESS_ACTIVE=claude-app`)

| Owns                          | Forbidden                                        | Read |
|-------------------------------|--------------------------------------------------|------|
| `.learnings/`                 | paths de harness (só config + decisões)          | tudo |
| `docs/decisions/`-append      | `.codex/`, `.hermes/`, `.antigravity/`, `.copilot/` | tudo |

Runtime ignorado: `.learnings/runtime/`.

## Sub-produtores com path canônico próprio (7 confirmados pela Ana)

### The Agency / cowork (`HARNESS_ACTIVE=cowork`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `cowork/` (sub-tree completo) | Sub-repo próprio com `.git`. Symlink ou path    |
|                               | absoluto documentado em fase β.                 |

### Obsidian vault config (`HARNESS_ACTIVE=obsidian`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `.obsidian/`                  | Só config do vault, não o vault inteiro.        |

### jekyll-gh-pages (`HARNESS_ACTIVE=jekyll-gh-pages`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `.github/workflows/jekyll-*.yml` | Sub-repo em `~/Projects/anavvanzin.github.io/` |
|                               | apontado por path absoluto.                     |

### Next.js deploy (`HARNESS_ACTIVE=nextjs-deploy`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `.github/workflows/nextjs.yml` | CI-only; app vive em sub-repo separado.        |

### self-improving-agent (`HARNESS_ACTIVE=self-improving-agent`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `.claude/self-improving-agent/` | Runtime memory em sub-path ignorado;         |
|                               | config/skill trackeada.                         |

### drift-detector (`HARNESS_ACTIVE=drift-detector`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `cowork/engineering/drift-detector/` | Skill instalada em `.hermes/skills/`       |
|                               | e `~/.codex/skills/`.                            |

### iconocracia-companion (`HARNESS_ACTIVE=iconocracia-companion`)

| Owns                          | Notes                                            |
|-------------------------------|--------------------------------------------------|
| `iconocracia-companion/` (symlink → sub-repo externo) | Sub-repo separado; symlink na raiz. |

## Paths compartilhados (qualquer harness, com regra)

| Path                  | Regra                                                       |
|-----------------------|-------------------------------------------------------------|
| `docs/decisions/`     | Append-only, formato ADR (frontmatter YAML + slug kebab).   |
| `plans/`              | Livre, qualquer harness.                                    |
| `AGENTS.md`           | Read por todos; write só via PR + review da Ana.           |
| `CLAUDE.md`           | Read por todos; write só via PR + review da Ana.           |
| `README.md`           | Idem.                                                       |
| `.gitignore`          | Idem; mudanças = ADR.                                       |

## Paths reservados (nenhum harness toca)

- `hub/` — sub-repos do `iconocracy-corpus` (já tem `.git` próprio).
- `labs/` — reservado, ainda não populado.
- `.worktree-salvage-*/` — dumps temporários, ignorados pelo `.gitignore`.
- `*.(dmg|zip|bak-*)` — binários soltos, ignorados.

## Paths de rascunho / working (Q3 resolvida)

- `iconocracia_junho*/` — **rascunhos de plano, NÃO repo**.
  Padrão ignorado pelo `.gitignore`. Quando o plano virar
  ADR/capítulo, conteúdo migra para `docs/decisions/` ou `plans/`
  e diretório morre.
- `"ICONOCRACIA — Trajetória"/` — idem, padrão ignored.
- `.planning/` — working de plan; ignorar runtime, trackear config.

## Avaliação pendente: divisão temporal por mês/trimestre (Q6)

A Ana cogitou dividir o repo por meses (`2026-Q2/`, `2026-Q3/`, ...).
**Decisão adiada** até γ/α/β estabilizarem e haver 1-2 meses de
uso real dos sub-repos. Próxima revisão: quando o primeiro commit
β estiver em produção.

## Procedimento para adicionar novo harness

1. Criar ADR em `docs/decisions/YYYY-MM-DD-<harness>-onboarding.md`.
2. Adicionar linha na seção "Harness owners (N)" deste arquivo.
3. Atualizar `.gitignore` com bloco runtime do novo harness.
4. Wirear `HARNESS_ACTIVE=<harness>` no pre-commit guard.
5. PR + review da Ana antes do primeiro commit.

## Procedimento para deprecar harness

1. Criar ADR `YYYY-MM-DD-<harness>-deprecation.md`.
2. Mover `.git/` do sub-repo para `archive/<harness>-<data>/` (manter histórico).
3. Remover linha da matriz.
4. Remover bloco do `.gitignore`.
5. PR + review.
