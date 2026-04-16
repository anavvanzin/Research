# ULTRAPLAN — Infraestrutura ICONOCRACIA

> Diagnóstico + plano de ação para resolver a fragmentação do workspace.
> Data: 2026-04-16 · Ana Vanzin · PPGD/UFSC

---

## 1. DIAGNÓSTICO: O que está quebrado

### 1.1 GitHub — nada está atualizado

| Repo | Commits locais não-pushed | Problema |
|------|--------------------------|----------|
| `hub/iconocracy-corpus` | **49 commits** atrás do remote | Todo trabalho recente (capítulos, IRR, ARGOS, configs) existe **só no Mac** |
| `Research` (meta-workspace) | 0 pendentes (mas AGENTS.md modificado e docs/ não commitados) | Docs novos (skill-upgrade-v2, dashboard) não versionados |
| `pipelines/Atlas` | 1 commit, remote existe | Provavelmente ok, mas verificar |
| `apps/iconocracia-companion` | **sem remote** | Nenhum backup no GitHub |
| `apps/iconocracia-space` | aponta para `Research.git` | Origin errado — não tem repo próprio |
| `pipelines/indexing` | remote `avmadrj/indexing` | Funcional, conta alternativa |

**Risco real:** se o Mac ou o SSD falhar, **49 commits de trabalho de tese se perdem**. Não há backup remoto do trabalho mais importante.

### 1.2 Arquivos soltos no hub (64 untracked)

O hub tem 64 arquivos/pastas não rastreados, incluindo:

- **Pastas legadas soltas:** `"Bibliografia - Uso simbólico/"`, `"Notas e Textos/"`, `"Esquema antigo .md"`, `"random outputs/"` — detritos que nunca foram organizados
- **Arquivos binários proibidos:** `"dissertacao de mestrado.pdf"`, `"Plan Linux.pdf"`, `corpus/infografico_gemini.png` — violam ADR-001 (binários → Drive, não git)
- **Artefatos de deploy não-commitados:** `docker-compose.yml`, `deploy/docker/`, `.postman/`
- **Notas de aula não-commitadas:** 5 arquivos em `vault/obsidian-dir410346/aulas/`
- **Templates e guias Obsidian:** `vault/_templates/`, `vault/meta/`
- **Skills locais do Claude:** 8 skills em `.claude/skills/` que podem ter valor

### 1.3 Documentação fragmentada

| Problema | Onde |
|----------|------|
| CLAUDE.md do hub dizia "26 scripts" (são 50+) | **Corrigido hoje** |
| AGENTS.md tinha symlinks invertidos | **Corrigido hoje** |
| Escala de indicadores ambígua (0–4 vs 0–3) | **Corrigido hoje** |
| `ICONOCRACY_MASTER_PROMPT.md` — referenciado mas pode estar desatualizado | hub/ — verificar |
| `docs/OPERATING_MODEL.md` — referenciado no hub CLAUDE.md | existência e atualidade? |
| Notion databases (4 IDs) — sincronização inexistente | `notion_sync.py` nunca foi criado |
| Google Doc "Mapa de Coerência" — última atualização? | ID: `1PpxzlHLBDPX8...` |
| `.learnings/LEARNINGS.md` vs hub docs vs Research docs | sobreposição, sem curadoria |

### 1.4 Decisões metodológicas abertas

- **DM-001:** chave API exposta em GitHub Actions → CRÍTICO se push acontecer
- **DM-002:** status de `feminist_network_48C51_pt.json` — usar ou não?
- **DM-003:** arquitetura PostgreSQL SPEC-1 não documentada

---

## 2. PLANO DE AÇÃO — 4 Sprints

### Sprint 0: EMERGÊNCIA (hoje, ~30 min)

**Objetivo:** backup remoto do trabalho existente.

- [ ] **0.1** Auditar se DM-001 (chave API) está em algum commit pendente:
  ```bash
  cd hub/iconocracy-corpus
  git log --all -p | grep -i "api.key\|ANTHROPIC_API\|sk-ant\|OPENAI_API" | head -20
  ```
  Se encontrar: `git filter-repo` ou BFG Cleaner ANTES de pushar.

- [ ] **0.2** Push hub/iconocracy-corpus (49 commits):
  ```bash
  cd hub/iconocracy-corpus
  git push origin main
  ```

- [ ] **0.3** Commit e push Research meta-workspace:
  ```bash
  cd ~/Research
  git add AGENTS.md docs/skill-upgrade-v2/ docs/ULTRAPLAN-2026-04-16.md
  git commit -m "docs: fix AGENTS.md symlinks, add skill v2 and ultraplan"
  git push origin main
  ```

- [ ] **0.4** Verificar/criar remote para `apps/iconocracia-companion`:
  ```bash
  cd apps/iconocracia-companion
  # Se não tem remote:
  gh repo create anavvanzin/iconocracia-companion --private --source=.
  git push -u origin main
  ```

### Sprint 1: HIGIENE (esta semana, ~2h)

**Objetivo:** limpar os 64 arquivos soltos e organizar o .gitignore.

- [ ] **1.1** Triagem dos 64 untracked — decisão por item:

  | Ação | Arquivos |
  |------|----------|
  | **Git add** (pertencem ao repo) | `vault/obsidian-dir410346/aulas/*`, `vault/_templates/*`, `vault/meta/*`, `tools/scripts/compare_*.py`, `tools/scripts/reconcile_*.py`, `tools/scripts/run_*.py`, `tools/ROADMAP-automation.md` |
  | **Mover para Drive/SSD** | `dissertacao de mestrado.pdf`, `Plan Linux.pdf`, `corpus/infografico_gemini.png`, `vault/assets/*.docx` |
  | **Mover para archive/** | `"Bibliografia - Uso simbólico/"`, `"Notas e Textos/"`, `"Esquema antigo .md"`, `"random outputs/"`, `corpus/iconocracy-corpus-66items.json` |
  | **Adicionar ao .gitignore** | `.claude/settings.local.json`, `corpus/agent-runs.lock`, `corpus/*.bak-*`, `.postman/`, `.dockerignore`, `docker-compose*.yml`, `deploy/docker/`, `js-genai`, `iurisvision`, `postman/`, `tests/training/` |
  | **Avaliar** | `.claude/skills/*` (8 skills locais — valor?) |

- [ ] **1.2** Atualizar `.gitignore` do hub com as exclusões acima.

- [ ] **1.3** Commit de limpeza:
  ```bash
  git add -A  # após triagem completa
  git commit -m "chore: triage 64 untracked files, update .gitignore"
  git push
  ```

### Sprint 2: DOCUMENTAÇÃO UNIFICADA (esta semana, ~3h)

**Objetivo:** um ponto de entrada confiável, sem redundância.

- [ ] **2.1** Verificar se `ICONOCRACY_MASTER_PROMPT.md` existe e está atualizado:
  ```bash
  ls -la hub/iconocracy-corpus/ICONOCRACY_MASTER_PROMPT.md
  ```
  Se desatualizado, alinhar com as correções feitas hoje (escala 0–3, terminologia).

- [ ] **2.2** Verificar `docs/OPERATING_MODEL.md`:
  ```bash
  ls -la hub/iconocracy-corpus/docs/OPERATING_MODEL.md
  ```
  Se não existe, criar com o release gate do hub CLAUDE.md.

- [ ] **2.3** Instalar o iconocracy-agent v2:
  ```bash
  cp ~/Research/docs/skill-upgrade-v2/SKILL.md ~/.claude/skills/iconocracy-agent/SKILL.md
  ```

- [ ] **2.4** Consolidar `.learnings/` — migrar aprendizados relevantes para:
  - Hub CLAUDE.md (se são regras permanentes)
  - Auto-memory (se são contexto pessoal)
  - Deletar o que é redundante

- [ ] **2.5** Atualizar TASKS.md com estado real (incluir este plano).

### Sprint 3: ELOS FRACOS (próxima semana, ~4h)

**Objetivo:** resolver os elos de infraestrutura que bloqueiam o trabalho.

- [ ] **3.1** `notion_sync.py` — criar script mínimo:
  ```
  records.jsonl → Notion DB1 (id: 68ba778cec304d11bc9ce369612a7e67)
  ```
  Usar Notion MCP disponível. Não precisa ser bidirerecional — push only é suficiente por agora.

- [ ] **3.2** Resolver DM-001 (chave API):
  - Rotacionar a chave comprometida
  - Usar GitHub Secrets para Actions
  - Verificar que `.env` está no `.gitignore`

- [ ] **3.3** Resolver DM-002 (`feminist_network_48C51_pt.json`):
  - Decisão binária: incorporar ao corpus pipeline ou arquivar

- [ ] **3.4** Corrigir origin de `apps/iconocracia-space`:
  ```bash
  cd apps/iconocracia-space
  git remote set-url origin https://github.com/anavvanzin/iconocracia-space.git
  # ou criar o repo se não existe
  ```

- [ ] **3.5** Automatizar backup semanal:
  ```bash
  # Cron ou hook: push all sub-repos
  for d in hub/* apps/* pipelines/* labs/*; do
    (cd "$d" && git push 2>/dev/null) || true
  done
  ```

---

## 3. PRIORIDADE REAL

A tese defende em **2026**. A infraestrutura é meio, não fim. Ordem de prioridade:

1. **Sprint 0** — HOJE. 49 commits sem backup é inaceitável.
2. **Sprint 2.3** — Instalar o skill v2 (já pronto, cópia de 1 arquivo).
3. **Sprint 1** — Higiene. Mas NÃO deixar virar armadilha de procrastinação.
4. **Sprint 3** — Elos fracos. Fazer conforme bloqueiam trabalho real.
5. **Sprint 2** — Docs. Importante mas não urgente.

> **Regra de ouro:** se uma tarefa de infraestrutura não desbloqueia
> um capítulo da tese, ela pode esperar.

---

## 4. MÉTRICAS DE SUCESSO

| Métrica | Agora | Meta |
|---------|-------|------|
| Commits não-pushed no hub | 49 | 0 |
| Arquivos untracked no hub | 64 | < 5 |
| Repos sem remote | 1 (companion) | 0 |
| Repos com origin errado | 1 (space) | 0 |
| Skills desatualizados | 1 (iconocracy-agent) | 0 |
| Documentos com escala errada | 0 (corrigido hoje) | 0 |
| `notion_sync.py` existe | não | sim |
| Backup automático | não | sim (cron semanal) |

---

*Plano gerado em 2026-04-16 por Claude, validado contra o estado real do filesystem.*
