# Research Workspace Full 360° Audit — Ultraplan

**Data:** 2026-04-17
**Escopo:** `/Users/ana/Research` (meta-workspace completo — hub + apps + pipelines + labs + vaults + shared + docs)
**Estratégia:** delegação paralela multi-agente com subagentes de contexto isolado
**Lentes:** agency-data-engineer · agency-code-reviewer · academic-paper-reviewer · agency-ux-architect · agency-frontend-developer
**Produto final:** relatório consolidado com achados rankeados (critical → suggested), por domínio, com roadmap de remediação
**Modo de execução:** planejamento apenas — nenhuma mudança de código nesta sessão

---

## Ground Truth (reconhecimento realizado 2026-04-17)

### Topologia do workspace

```
/Users/ana/Research/              (meta-workspace, é um git repo próprio)
├── hub/           977M    tese canônica (iconocracy-corpus: 1368 arquivos de código, 36 testes)
│                          + mnemosyne-scout (ideias/handoffs, sem código)
├── apps/          1.1G    iconocracia-companion (Next/Cloudflare), iconocracia-space (HF)
├── pipelines/     269M    Atlas (toolkit), indexing (corpus-scout + gallica-mcp-server)
├── labs/          382M    iurisvision (Vite/Firebase), iuris-visio-roadmap (planning)
├── vaults/           0B   todos symlinks para hub
├── shared/        266M    iconclass-data (2 forks), the-book-of-secret-knowledge
├── docs/          216K    superpowers/ (plans, specs, visual-essays), imported/, runbook
├── archive/       684M    READ-ONLY — legados, duplicatas, retired checkouts
├── Books/         244M    PDFs de referência (bibliografia) — não auditar
├── Cotutela/      232K    admin
└── rotinas/        20K    templates
```

### Repositórios Git independentes (escaneados)

| Repo | Caminho | Tamanho | Código | Testes | Papel |
|---|---|---|---|---|---|
| `Research` (meta) | `/Users/ana/Research` | — | — | — | supervisor git da meta-workspace |
| `hub/iconocracy-corpus` | `hub/` | 977M | 1368 | 36 | **crown jewel** — tese, corpus, pipeline |
| `apps/iconocracia-companion` | `apps/` | 1.1G (maior parte `node_modules`) | 19 | 0 | frontend Next/Cloudflare do corpus |
| `apps/iconocracia-space` | `apps/` | 48K | 1 (app.py) | 0 | Space HuggingFace (Gradio) |
| `pipelines/Atlas` | `pipelines/` | 6.7M | 12 | 0 | toolkit iconográfico + DOCX/PDF output |
| `pipelines/indexing` | `pipelines/` | 262M | 11 | 0 | corpus-scout-agent + gallica-mcp-server (Node/TS) |
| `labs/iurisvision` | `labs/` | 382M (mostly node_modules) | 16 | 0 | lab Vite/TS + Firebase |
| `labs/iuris-visio-roadmap` | `labs/` | 248K | 0 | 0 | só docs |
| `shared/iconclass-data*` (x2) | `shared/` | 266M | — | — | upstream forks Iconclass |
| `shared/the-book-of-secret-knowledge` | `shared/` | — | — | — | ref externa (não auditar) |
| `archive/*` (6 repos) | `archive/` | 684M | — | — | **NÃO AUDITAR** — read-only histórico |

### Instrução files (contratos de governança)

```
/Users/ana/Research/AGENTS.md + CLAUDE.md               — meta-workspace
/Users/ana/Research/hub/iconocracy-corpus/{AGENTS,CLAUDE,SKILL}.md
/Users/ana/Research/apps/iconocracia-companion/{AGENTS,CLAUDE,SKILL}.md
```

### Dados canônicos (cadeia de custódia)

```
records.jsonl  →  corpus/corpus-data.json (145 itens)  →  HF release
                ↓
           companion-data.json  →  apps/iconocracia-companion
                ↓
            vault/candidatos/   →  vaults/* (symlinks)
```

Qualquer auditoria tem que validar este contrato — é a espinha dorsal da tese.

---

## Premissas

1. **Nenhum subagente escreve código nesta passada.** Saída = relatório. Remediação vem depois, numa segunda onda com plano próprio.
2. **Subagentes não herdam contexto.** Cada um recebe escopo + objetivo + saída esperada auto-contidos.
3. **Paralelismo máximo = 3 subagentes concorrentes** (limite do `delegate_task`).
4. **Rodadas sequenciais** — 3 ondas paralelas + 1 onda de síntese.
5. **Archive é off-limits** — economiza 684M de ruído.
6. **Books/ é off-limits** — é bibliografia, não código.
7. **node_modules, .git, .venv, dist, build, .next, .opencode** são excluídos de toda análise.
8. **Relatórios individuais vão para** `docs/superpowers/audit/2026-04-17/<agent>-<domain>.md`.
9. **Cada relatório usa a mesma schema** para permitir consolidação mecânica.

---

## Riscos conhecidos e mitigações

| Risco | Mitigação |
|---|---|
| Subagente se perde explorando o hub inteiro (1368 arquivos) | Dar lista precisa de caminhos a examinar, não o repo inteiro |
| Subagente escreve no workspace isolado e parent não lê | Exigir retorno em **markdown dentro do summary** + salvar relatório em `docs/superpowers/audit/…` |
| Glob a partir de `/Users/ana/Research` é lento (20s+) | Cada agente trabalha a partir de caminho específico, nunca da raiz |
| Conflito de conclusões entre agentes | Síntese final reconcilia, marcando consensos e disputas |
| Archive gastando tempo | Excluir `archive/`, `Books/`, `node_modules/`, `.venv/`, `dist/`, `.git/` em todos os escopos |
| Sobre-auditoria do hub (já trusted por contrato) | Hub = auditado em 2 vertentes (dados + Python), não 5; foco é o ecossistema |

---

## Schema de Relatório (TODO subagente retorna neste formato)

```markdown
# Audit Report — <domain> — <agent>
Escopo examinado: <paths>
Arquivos analisados: N
Data: 2026-04-17

## Resumo executivo (≤5 linhas)

## Achados — CRITICAL (bloqueante, fix antes de qualquer release)
- [C-01] <título> · `<path>:<linha>` · <diagnóstico> · <remediação proposta>

## Achados — MAJOR (degrada qualidade, deve corrigir no próximo ciclo)
- [M-01] ...

## Achados — MINOR (polimento)
- [m-01] ...

## Pontos fortes (o que NÃO mexer)

## Métricas mensuradas
- métrica: valor

## Dependências inter-domínio (se achado afeta outro agente)
- <achado> depende de / conflita com <outro domínio>

## Recomendações priorizadas (top 5)
```

---

## WAVE 1 — Reconhecimento paralelo (3 agentes concorrentes)

Cada agente produz `docs/superpowers/audit/2026-04-17/<slug>.md` e retorna o summary na resposta.

### Agent 1.1 — Data Engineer Hub (agency-data-engineer lens)

**Escopo:**
- `/Users/ana/Research/hub/iconocracy-corpus/tools/scripts/` (62 scripts Python)
- `/Users/ana/Research/hub/iconocracy-corpus/tools/schemas/` (contratos)
- `/Users/ana/Research/hub/iconocracy-corpus/data/processed/records.jsonl`
- `/Users/ana/Research/hub/iconocracy-corpus/corpus/corpus-data.json`
- `/Users/ana/Research/hub/iconocracy-corpus/notebooks/` (8 notebooks)
- `/Users/ana/Research/hub/iconocracy-corpus/companion-data.json`
- `/Users/ana/Research/hub/iconocracy-corpus/.github/workflows/`

**Goal:**
Auditar o **contrato de dados canônico** da tese pelo prisma data-engineer (Bronze/Silver/Gold, idempotência, quality gates, lineage). Validar que a cadeia records.jsonl → corpus-data.json → companion-data.json → releases HF é:
(a) idempotente
(b) esquema-validada em todos os pontos
(c) testada (os 36 testes cobrem os pontos críticos?)
(d) observável (CI pega regressões?)
(e) reproduzível (notebooks rodam de ponta a ponta com a ENV atual?)

**Toolsets:** `terminal`, `file`, `search`

**Context passado:**
- AGENTS.md do workspace e do hub (conteúdo literal injetado no prompt)
- README.md do hub
- Conda env: `iconocracy`, Python 3.12 em `/Users/ana/.venvs/iconocracy/bin/python3.12`
- Lista explícita dos 62 scripts e 8 notebooks (produzida via `find` antes do dispatch)
- Instrução: NÃO executar `validate_schemas.py` em modo destrutivo — só leitura e `--dry-run` se existir
- Instrução: NÃO tocar em `data/raw/` (hook bloqueia binários)

**Saída esperada:**
1. Relatório no schema acima salvo em `docs/superpowers/audit/2026-04-17/1.1-data-engineer-hub.md`
2. Resumo no return value da chamada (copia do relatório)
3. Contagem: # scripts sem header/docstring, # notebooks sem fig inicial, # schemas sem version, # breakage de contrato detectado entre records.jsonl e corpus-data.json

### Agent 1.2 — Code Reviewer Ecossistema (agency-code-reviewer lens)

**Escopo:**
- `/Users/ana/Research/apps/iconocracia-companion/src/` (19 arquivos TS/TSX)
- `/Users/ana/Research/apps/iconocracia-companion/scripts/`
- `/Users/ana/Research/apps/iconocracia-space/app.py`
- `/Users/ana/Research/pipelines/Atlas/main.py` + `/Users/ana/Research/pipelines/Atlas/atlas_iconocratico/`
- `/Users/ana/Research/pipelines/indexing/corpus-scout-agent/`
- `/Users/ana/Research/pipelines/indexing/gallica-mcp-server/` (TypeScript MCP — auditar dist vs src)
- `/Users/ana/Research/labs/iurisvision/src/`

**Goal:**
Code review cross-repo focado em:
(a) consistência de estilo e convenções (PT vs EN em identifiers, naming, imports)
(b) duplicação de lógica entre apps/pipelines (ex: corpus-data.json é lido em N lugares com N parsers diferentes?)
(c) uso de `any`, `@ts-ignore`, try/catch vazio, console.log esquecido
(d) gestão de segredos (API keys, Firebase config, Gallica credentials) — há vazamentos em src?
(e) dependências desatualizadas ou duplicadas entre repos
(f) ausência de testes — cada repo tem 0 testes exceto hub; quais são os pontos críticos que deveriam ter?

**Toolsets:** `terminal`, `file`, `search`

**Context passado:**
- Lista dos repos e seus caminhos exatos
- AGENTS.md de cada repo (inline)
- Instrução explícita: NÃO escrever código, NÃO executar `npm install`, NÃO rodar builds. Apenas leitura e análise estática.
- Instrução: flagear mas NÃO corrigir — corrigir é wave futura.

**Saída esperada:**
1. Relatório `docs/superpowers/audit/2026-04-17/1.2-code-reviewer-ecosystem.md`
2. Contagens: # arquivos com `any`, # `@ts-ignore`, # try/catch vazios, # console.log, # secrets em src, # TODOs sem dono
3. Matriz de duplicação: qual lógica aparece em quantos repos

### Agent 1.3 — Academic Content Reviewer (academic-paper-reviewer lens)

**Escopo:**
- `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/rascunhos-artigos/` (6 drafts identificados)
- `/Users/ana/Research/hub/iconocracy-corpus/tese/artigos/dessexualization-threshold-draft-v1.md`
- `/Users/ana/Research/hub/iconocracy-corpus/tese/manuscrito/` (capítulos da tese — apenas os `*_rev`, não `*_original`)
- `/Users/ana/Research/hub/iconocracy-corpus/vault/tese/drafts/` (propostas Max Planck, Justice Vandalized)
- `/Users/ana/Research/hub/mnemosyne-scout/ideas/` (mapas conceituais)
- `/Users/ana/Research/docs/superpowers/visual-essay-iconocracia.html` e `visual-essay-refactored.html`

**Goal:**
Auditoria rápida (não full-review como em genealogia-alegoria-feminina) de:
(a) **inventário**: quais drafts existem, estado (early / mid / late / submitted), tamanho em palavras
(b) **consistência terminológica** entre drafts e vault/tese — ENDURECIMENTO, Contrato Sexual Visual, Feminilidade de Estado são usados coerentemente? Alguma atribuição incorreta a Pateman/Mondzain escapando em algum draft?
(c) **duplicação/overlap**: os 6 rascunhos de artigo competem entre si ou mapeiam porções complementares da tese?
(d) **cobertura da tese pelos artigos**: quais seções da tese não têm rascunho de artigo correspondente?
(e) **riscos ABNT**: citações inconsistentes (Mondzain sem edição 2002, Goodrich 2014 vs 2017, etc.)

**Toolsets:** `file`, `search`

**Context passado:**
- Revisão prévia do `genealogia-alegoria-feminina.json` (injetada como referência de qualidade/estilo)
- Lista dos 10 conceitos-chave que devem ser verificados em cada draft
- Instrução: NÃO fazer full peer-review de cada draft. Só inventário + checagem de consistência.

**Saída esperada:**
1. Relatório `docs/superpowers/audit/2026-04-17/1.3-academic-content-review.md`
2. Tabela-inventário: draft, estado, palavras, status terminológico, gaps
3. Top-3 drafts que precisam de full peer-review em onda futura (com justificativa)

---

## WAVE 2 — Análise especializada (3 agentes concorrentes, após Wave 1)

Wave 2 tem contexto de síntese parcial — cada agente recebe os 3 relatórios da Wave 1 como input além do próprio escopo.

### Agent 2.1 — Frontend/Visual-Essay Architect (agency-frontend-developer + agency-ux-architect lens)

**Escopo:**
- `/Users/ana/Research/docs/superpowers/visual-essay-*.html` (2 arquivos)
- `/Users/ana/Research/apps/iconocracia-companion/src/` (se Wave 1.2 flageou issues de UX)
- `/Users/ana/Research/pipelines/Atlas/atlas-iconometrico.html`
- `/Users/ana/Research/labs/iurisvision/src/` (se Wave 1.2 flageou issues)

**Goal:**
Auditar as superfícies visuais da tese (essays HTML, companion app, Atlas iconométrico):
(a) acessibilidade (contraste, ARIA, keyboard nav, alt em charts)
(b) performance (Chart.js pesado, CDN blocking, bundle size)
(c) consistência visual entre superfícies (tipografia, paleta, gramática de UI)
(d) responsividade (testar em 375/768/1440 — o visual-essay-refactored funciona em mobile?)
(e) conformidade com o framing "index→arquivo" que acabamos de estabelecer no refactor

**Toolsets:** `file`, `search`, `browser` (para testar HTMLs localmente), `terminal`

**Saída esperada:**
1. `docs/superpowers/audit/2026-04-17/2.1-frontend-visual.md`
2. Screenshots de viewport quebrados se houver
3. Lista de issues de acessibilidade por nível WCAG

### Agent 2.2 — Architecture Auditor (agency-software-architect lens)

**Escopo:** workspace inteiro, visão arquitetural (não arquivo-por-arquivo)

**Goal:**
(a) **Validar a arquitetura declarada** em AGENTS.md — os symlinks `pipelines/iconocracy-ingest → hub/...`, `hub/Atlas → pipelines/Atlas`, etc. estão consistentes? Há symlinks quebrados?
(b) **Circular deps**: hub importa de pipelines que importa de hub? Há ciclos?
(c) **Drift de contratos**: `corpus-data.json` tem mesma schema em todos os consumidores?
(d) **Zombie code**: quais repos/subdiretórios em archive/ ainda têm referências ativas no hub ou apps? (se sim, archive → active)
(e) **Orfãos**: há diretórios no hub que não são referenciados por nenhum script, notebook, CI, ou AGENTS.md? (candidatos a archive)
(f) **CI coverage**: qual % dos repos tem CI funcionando? O .github/workflows do hub cobre o quê?

**Toolsets:** `terminal`, `file`, `search`

**Context passado:** relatórios 1.1 e 1.2

**Saída esperada:**
1. `docs/superpowers/audit/2026-04-17/2.2-architecture.md`
2. Diagrama atualizado da topologia real (vs. declarada em AGENTS.md)
3. Lista de symlinks quebrados, orfãos, e zombies

### Agent 2.3 — Notebook & Reproducibility (agency-data-engineer lens, subescopo)

**Escopo:**
- `/Users/ana/Research/hub/iconocracy-corpus/notebooks/*.ipynb` (8 notebooks)
- `/Users/ana/Research/pipelines/Atlas/notebooks/` (se existe)
- `/Users/ana/Research/hub/iconocracy-corpus/environment.yml`
- `/Users/ana/Research/hub/iconocracy-corpus/requirements*.txt` (se existe)

**Goal:**
(a) cada notebook roda end-to-end em conda `iconocracy`? (inspeção estática — não executar)
(b) outputs armazenados ou limpos? (versionamento de outputs é anti-pattern)
(c) paths hardcoded vs. relativos? (absolute `/Users/ana/...` é pegadinha)
(d) notebooks 01-08 narram uma sequência coerente? (sequencialidade)
(e) cells com erro armazenado?

**Saída esperada:** `docs/superpowers/audit/2026-04-17/2.3-notebooks.md`

---

## WAVE 3 — Síntese (executada pelo orquestrador, NÃO subagente)

Após Wave 1 e 2, o parent agent (esta sessão ou próxima) faz:

1. **Ler os 6 relatórios** em `docs/superpowers/audit/2026-04-17/`
2. **Consolidar** em `docs/superpowers/audit/2026-04-17/00-synthesis.md` com:
   - Top-10 findings CRITICAL (cross-domain)
   - Matriz de dependência entre findings (fix X destrava Y)
   - Roadmap de remediação em 3 sprints (1 semana cada)
   - Estimate de esforço por sprint
3. **Produzir** `docs/superpowers/plans/2026-04-XX-remediation-wave-1.md` — plano executável para o primeiro sprint

---

## Caminhos de arquivos que serão criados

```
Research/docs/superpowers/audit/2026-04-17/
├── 1.1-data-engineer-hub.md              (Wave 1, Agent 1.1)
├── 1.2-code-reviewer-ecosystem.md        (Wave 1, Agent 1.2)
├── 1.3-academic-content-review.md        (Wave 1, Agent 1.3)
├── 2.1-frontend-visual.md                (Wave 2, Agent 2.1)
├── 2.2-architecture.md                   (Wave 2, Agent 2.2)
├── 2.3-notebooks.md                      (Wave 2, Agent 2.3)
└── 00-synthesis.md                       (Wave 3, orquestrador)

Research/docs/superpowers/plans/
├── 2026-04-17-research-workspace-full-audit.md   (este arquivo)
└── 2026-04-XX-remediation-wave-1.md              (produto de Wave 3)
```

---

## Métricas de sucesso da ultraplan

- Wave 1 completa em ≤ 10 min (3 agents paralelos, max_iterations=25 cada)
- Wave 2 completa em ≤ 10 min (3 agents paralelos)
- Wave 3 síntese em ≤ 15 min de trabalho do orquestrador
- **Total: ≤ 35 min de wall-clock para audit 360° completo**
- Cada relatório segue o schema, permitindo merge mecânico
- Pelo menos 20 findings CRITICAL+MAJOR identificados (se forem menos, algo não foi coberto)
- Zero findings duplicados entre agentes (o escopo é particionado sem overlap — exceto companion/iurisvision que aparecem em 1.2 e 2.1 por design)

---

## Open questions / calls do orquestrador

1. **O usuário quer executar esta wave agora ou revisar o plano primeiro?**
2. **Delegar os 3 da Wave 1 imediatamente em paralelo ou rodar um como pilot primeiro?**
3. **Produto final: relatório em PT ou EN?** (convenção do workspace é PT, mas Opus funciona melhor em EN para análise técnica — eu recomendo PT no sumário executivo e EN nos achados técnicos)
4. **Onde delivery? Aqui na sessão, em arquivo salvo, ou ambos?** (default: ambos)
5. **Alguma zona quente a proteger?** (ex: não mexer em `tese/manuscrito/*_rev`, não tocar em vault durante audit?)

---

## Próximo passo

Se aprovado:
1. Criar `docs/superpowers/audit/2026-04-17/` (diretório)
2. Pré-gerar listas de caminhos que cada agente vai receber (via `find`, salvas como `.txt`)
3. Dispatch paralelo Wave 1 via `delegate_task` com `tasks=[…]`
4. Aguardar retornos, dispatch paralelo Wave 2
5. Síntese

Se rejeitado: revisar escopo com base no feedback.
