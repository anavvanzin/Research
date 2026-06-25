---
tags: [meta, decision, architecture, git-physics, multi-harness]
date: 2026-06-25
scope: meta-workspace architecture
status: ACCEPTED
accepted_by: Ana Vanzin
accepted_date: 2026-06-25
supersedes: regra implícita "versionar apenas cowork/, docs/, .claude/AUTOMATION.md" do AGENTS.md prévio
related:
  - ./AGENT-OWNERSHIP.md
  - ../../AGENTS.md
---

# ADR — Multi-harness Git Physics para o workspace ICONOCRACIA

## 1. Enquadramento

O meta-workspace `/Users/ana/Research/` opera hoje com seis harnesses simultâneos
(Codex app, Hermes CLI, Claude CLI, GitHub Copilot, Antigravity 2.0, Claude app),
cada um deixando estado — config, cache, runtime, sessões — em paths do repo raiz.
A regra vigente ("versione apenas `cowork/`, `docs/`, `.claude/AUTOMATION.md`")
é uma cerca que contém o sintoma mas não modela o fenômeno: na prática, ~120
diretórios e arquivos do `.claude/skills/`, `.agents/`, `.codex/`, `.hermes/`,
`.obsidian/`, `.learnings/` continuam untracked, e cada novo harness que entra
precisa negociar exceção.

Este ADR é o **primeiro passo (γ)** de uma migração em três fases:

1. **γ — Este ADR + AGENT-OWNERSHIP.md + extensão cirúrgica do `.gitignore`.**
   Estabelece o modelo sem mover nenhum arquivo.
2. **α — Drain de runtime.** Cada harness ganha bloco próprio no `.gitignore`
   separando "config canônica" (versionada) de "runtime/cache" (ignorada).
3. **β — Extração de sub-repos.** Cada path candidato vira repo independente
   com `.git` próprio, referenciado por symlink (paths pequenos) ou path
   absoluto documentado (paths grandes, ex.: `hub/iconocracy-corpus`).

## 2. Princípios (não-negociáveis)

1. **Repo raiz magro.** Apenas índices, contratos e a sub-árvore
   `docs/decisions/`. Nada mais no meta-repo que não seja
   (a) configuração canônica de harness, ou (b) decisão/documento.
2. **Sub-repo por harness com `.git` próprio.** Sem nested-git. Se A está
   dentro de B e tem `.git`, então A **não pode** ser adicionado em B.
3. **Sub-repo por projeto de pesquisa.** `hub/iconocracy-corpus/` já é.
   `apps/`, `archive/`, `gestao/`, `vida-os/`, `shared/`, `plans/`,
   `iconocracy-editorial-wt/` devem tornar-se.
4. **Decisões entre harnesses via markdown versionado** em `docs/decisions/`.
   Formato: `YYYY-MM-DD-<slug>.md` com frontmatter YAML mínimo
   (`tags`, `date`, `scope`, `status`).
5. **`docs/decisions/` é append-only e livre escrita** desde que siga o
   formato ADR. Qualquer harness pode escrever lá. Conflitos resolvem-se
   por timestamp + linked PR, não por git merge tradicional.
6. **Runtime/cache de harness nunca é versionado.** Só config canônica.
7. **Ownership por path é contrato.** Cada harness tem colunas
   `Owns (versiona)` e `Forbidden` em `AGENT-OWNERSHIP.md`. Violação = hook
   falha o commit.

## 3. Ownership matrix (resumo; canônico em `AGENT-OWNERSHIP.md`)

| Harness           | Owns (paths que pode versionar)                    | Forbidden                                |
|-------------------|---------------------------------------------------|------------------------------------------|
| Codex app         | `.agents/`, `.codex/`, `cowork/codex/`            | `docs/decisions/`-write como único dono, `.hermes/`, `.antigravity/`, `.copilot/` |
| Claude CLI        | `.claude/`, `docs/decisions/`-append              | `.codex/`, `.hermes/`, `.antigravity/`   |
| GitHub Copilot    | `.copilot/`                                       | (todos os outros)                        |
| Antigravity 2.0   | `.antigravity/`                                   | (todos os outros)                        |
| Hermes CLI        | `.hermes/`, `hermes/`                             | `.codex/`, `.claude/`, `.antigravity/`   |
| Claude app        | `.learnings/`, `docs/decisions/`-append           | (paths de harness — escrita só em learnings/decisions) |

Sub-produtores com path canônico próprio (também donos):

| Sub-produtor        | Owns                              |
|---------------------|-----------------------------------|
| The Agency / cowork | `cowork/` (sub-tree completo)     |
| Obsidian vault cfg  | `.obsidian/`                      |
| jekyll-gh-pages     | `.github/workflows/jekyll-*.yml` + `anavvanzin.github.io/` |
| Next.js deploy      | `.github/workflows/nextjs.yml`    |
| self-improving-agent | `.claude/self-improving-agent/`  |
| drift-detector      | `cowork/engineering/drift-detector/` + `.hermes/skills/` |
| iconocracy-companion | `iconocracia-companion/` (symlink → sub-repo) |

## 4. Path contracts (regras por path)

- `cowork/`: shared, qualquer harness com code review do owner.
- `docs/decisions/`: append-only, formato ADR, qualquer harness.
- `plans/`: livre, qualquer harness.
- `.claude/`, `.codex/`, `.hermes/`, `.antigravity/`, `.copilot/`:
  dono único (ver matriz).
- `.learnings/`: write por Claude app; read por todos.

## 5. Runtime drain (`.gitignore` por harness)

Bloco por harness separa "config canônica" (trackeada) de "runtime" (ignorada).
Exemplo (esqueleto — versão final em commit γ.3):

```
# Codex app runtime (config canônica é .agents/, .codex/config/)
.codex/cache/
.codex/sessions/

# Hermes CLI runtime
.hermes/conversations/
.hermes/cache/

# Claude CLI runtime (skills config trackeada; runtime ignorado)
.claude/skills/*/runtime/
.claude/skills/*/.cache/

# Antigravity runtime
.antigravity/cache/
.antigravity/sessions/

# Copilot runtime
.copilot/cache/

# Binários soltos
*.dmg
*.zip
*.bak-*/

# Worktree dumps
.worktree-salvage-*/

# Rascunhos de plano não versionados (resolve Q3)
iconocracia_junho*/
"ICONOCRACIA — Trajetória"/
```

## 6. Pre-commit ownership guard (script)

Localização: `cowork/engineering/git-physics-guard.sh` (no sub-repo
`cowork/`, que tem `.git` próprio). No meta-repo raiz, hook chama
o script como referência externa:

```bash
#!/usr/bin/env bash
# Falha se algum path staged está fora da ownership matrix.
# Lê docs/decisions/AGENT-OWNERSHIP.md e bloqueia.
set -euo pipefail
ACTIVE_HARNESS="${HARNESS_ACTIVE:-codex-app}"
OWNERSHIP="docs/decisions/AGENT-OWNERSHIP.md"
# ... (implementação na fase α)
```

O guard vira **obrigatório** no meta-repo raiz a partir da fase β. Antes,
fica como `info` (warning, não bloqueia).

## 7. Migration plan (fases, não datas)

- **γ (hoje, 2026-06-25)**: este ADR + `AGENT-OWNERSHIP.md` + `.gitignore`
  estendido. Nenhum `git add` de paths novos. Decisão pendente de assinatura.
- **α (próxima sessão)**: implementar o runtime drain (`.gitignore` por
  harness), wired como hook `info`. Validar com `git status` limpo em
  cada harness ativo.
- **β (depois de α estável)**: extrair `apps/`, `archive/`, `gestao/`,
  `vida-os/`, `shared/`, `plans/`, `iconocracy-editorial-wt/` para
  sub-repos com `.git` próprio. Symlink para paths pequenos; path
  absoluto documentado para paths grandes. Hook guard vira `enforce`.
- **γ+ (manutenção)**: cada novo harness que entrar preenche sua linha
  na matriz **antes** de criar qualquer arquivo no repo.

## 8. Decisões tomadas nesta sessão

- **D1**: Todos os 6 harnesses podem versionar artefatos. Sem distinção
  produtor/consumidor.
- **D2**: Repo magro na raiz + sub-repos. Consistente com
  `hub/iconocracy-corpus` que já é sub-repo.
- **D3**: Decisões como markdown versionado, não git objects.
  Apendável, legível, sem tooling extra.
- **D4**: Symlink para sub-repos pequenos (`.codex/`, `.hermes/`,
  `.antigravity/`, `.copilot/`); path absoluto documentado para os
  grandes (`hub/iconocracy-corpus`).
- **D5**: `docs/decisions/` é livre-escrita por qualquer harness desde
  que siga formato ADR (frontmatter YAML + slug kebab-case).
- **D6**: ADR escrito em português para consistência com `AGENTS.md`
  raiz. ADR técnico pode usar inglês em body, mas frontmatter é PT.

## 9. Open questions (para próximas sessões)

- **Q1**: Path reference para sub-repos grandes usa symlink resolvido ou
  path absoluto hard-coded em `AGENT-OWNERSHIP.md`? Symlink é mais
  portável; path absoluto é mais robusto contra move acidental.
- **Q2**: Como resolver conflito quando dois harnesses editam o mesmo
  ADR simultaneamente? (Proposta: timestamp + linked PR + ADR de
  "resolução" que supersede.)
- **Q3 [RESOLVIDA 2026-06-25]**: `iconocracia_junho2026 2/` é
  **rascunho de plano, não repo**. Tratamento: ignorar via
  `.gitignore` (padrão `iconocracia_junho*`); quando o plano virar
  ADR/capítulo, conteúdo migra para `docs/decisions/` ou `plans/` e
  diretório morre.
- **Q4**: `.worktree-salvage-20260530/` é recuperável ou purgar?
- **Q5**: Copilot não versiona nada — manter assim ou forçar mínimo
  canônico (`.copilot/README.md` declarando intenção)?
- **Q6 [nova 2026-06-25]**: Dividir o `Research/` por meses/trimestres
  (`2026-Q2/`, `2026-Q3/`, ...) é desejável para sazonalidade de
  trabalho, ou atrapalha buscas cross-quarter e continuidade do
  `AGENTS.md`? Avaliar **depois** de γ/α/β estabilizarem, com 1-2 meses
  de evidência sobre sub-repos em uso.

## 10. Riscos do modelo

- **R1**: Hook guard muito estrito trava trabalho legítimo. Mitigação:
  começar como `info` (warning) por uma semana antes de virar `enforce`.
- **R2**: Symlinks quebram em clones bare / CI sem resolução de
  symlinks, e em sync via cloud (Dropbox/iCloud) que pode duplicar
  paths. Mitigação: paths críticos grandes (`hub/iconocracy-corpus`)
  ficam como **path absoluto em `AGENT-OWNERSHIP.md`**, não symlink.
  Symlinks só para sub-repos pequenos e efêmeros.
- **R3**: Owner de harness muda (ex.: trocar Antigravity por outra
  ferramenta). Mitigação: ADR de substituição, atualizar matriz,
  arquivar `.antigravity/` como `archive/.antigravity-<data>/`.
- **R4**: Frontmatter YAML drift entre ADRs. Mitigação: schema em
  `docs/decisions/SCHEMA.md` (a criar em γ+).

## 11. Recomendação operacional para esta sessão

**Parar aqui após γ.** Não commitar nada até a Ana assinar este ADR
(✓ status: ACCEPTED em 2026-06-25). Próximo passo é γ.3 (extensão
do `.gitignore`) como commit único e atômico, antes de qualquer
`git add` de paths novos.

## 12. Aceite

Aceito por **Ana Vanzin** em **2026-06-25**, durante sessão Codex app
no meta-repo `/Users/ana/Research/`. Sub-produtores confirmados:
The Agency / cowork, Obsidian vault cfg, jekyll-gh-pages,
Next.js deploy, self-improving-agent, drift-detector,
iconocracia-companion. Q3 resolvida (rascunho, não repo).
Q6 registrada para avaliação pós-β.

Próximo passo autorizado: γ.3 (extensão cirúrgica do `.gitignore`)
como commit único, sem `git add` de paths novos.
