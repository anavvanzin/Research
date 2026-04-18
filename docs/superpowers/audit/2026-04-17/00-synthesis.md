# 00 — Synthesis: Research Workspace Full 360° Audit

**Data:** 2026-04-17
**Escopo auditado:** `/Users/ana/Research` (meta-workspace ICONOCRACIA completo)
**Agentes executados:** 6 subagentes paralelos em 2 ondas, ~12 min wall-clock, ~22min CPU-time
**Relatórios-fonte:** `1.1-data-engineer-hub.md`, `1.2-code-reviewer-ecosystem.md`, `1.3-academic-content-review.md`, `2.1-frontend-visual.md`, `2.2-architecture.md`, `2.3-notebooks.md`

---

## TL;DR (≤10 linhas)

O workspace tem arquitetura bem pensada no papel (AGENTS.md, contrato canônico records→corpus→HF, 3 regimes iconocráticos) mas **o estado-em-disco diverge criticamente do estado-declarado** em três frentes:

1. **Contrato de dados quebrado:** `records.jsonl` tem 2 linhas enquanto `corpus/corpus-data.json` tem 165 itens (não 145). Há 4 cópias de corpus-data.json com contagens divergentes (165/145/89/165). A cadeia canônica declarada em AGENTS.md não é verificável hoje.
2. **Segurança imediata:** Um `GEMINI_API_KEY` está exposto para inlining no bundle cliente via `vite.config.ts` em iurisvision. A key precisa ser rotacionada mesmo se nunca tiver vazado no runtime.
3. **Consistência terminológica:** 3 misattributions do conceito original "Contrato Sexual Visual" a Pateman, 8+ ocorrências de "hardening" onde deveria ser ENDURECIMENTO, Goodrich 2014 vs 2013 (*Legal Emblems* é 2013), Mondzain citada em 3 edições diferentes. Estes findings comprometem a autoria intelectual da tese.

Zero tests na cadeia canônica. Zero CI na companion. Notebooks 05-08 nunca foram executados apesar de o visual-essay citar `subscores.csv` e `fig_06-fig_18` como produtos deles. `main.jsx` é god-file de 2.422 linhas. Dois arquivos visual-essay são byte-idênticos (perda do snapshot pré-refactor). A boa notícia: framing "index→arquivo" está 100% consistente no refactor, nenhum secret hardcoded no código-fonte, nenhum symlink quebrado, topologia estruturalmente sólida.

---

## 1. Cross-Domain Critical Findings (rankeados por impacto × urgência)

### CRIT-01 · Contrato de dados records↔corpus quebrado
- **Fonte:** 1.1-C01, 2.2-C2, 2.3-m3
- **Diagnóstico:** `records.jsonl` = 2 linhas; `corpus/corpus-data.json` = 165 itens; HF snapshot = 145 itens; archive-legacy = 89 itens; `.claude/worktrees/` = 165 itens. A "ordem de verdade" declarada em AGENTS.md (records → corpus) está invertida no disco — o corpus Gold foi populado independentemente da Bronze/Silver declarada.
- **Impacto:** Inviabiliza a rastreabilidade total (requisito do capítulo de método da tese), quebra a defensibilidade metodológica, torna HF releases não-reprodutíveis.
- **Remediação:** rodar `csv_to_records.py` para regenerar records.jsonl a partir do corpus+csv; adicionar gate `len(records)==len(corpus)` na CI; documentar qual direção é real; reconciliar as 4 cópias (ou declarar arquivo-legacy explicitamente deprecated).
- **Bloqueia:** qualquer release HF novo, defesa metodológica do Capítulo 3, cotutela.

### CRIT-02 · GEMINI_API_KEY exposto em build cliente
- **Fonte:** 1.2-C01, 2.1-C-01 (confirmado)
- **Diagnóstico:** `/Users/ana/Research/labs/iurisvision/vite.config.ts:11` usa `define: { 'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY) }` combinado com `loadEnv(mode, '.', '')` (terceiro arg vazio carrega TODAS as envs). Vite inlineia textualmente no bundle do cliente. O build atual saiu sem valor resolvido apenas porque o shell não exportou a var no último build — o vetor está armado.
- **Impacto:** Qualquer build com a env definida vaza a key no JS servido publicamente. Key extraível via view-source.
- **Remediação:** (1) remover o `define` do vite.config.ts; (2) mover chamadas Gemini para endpoint backend (Cloudflare Worker ou Firebase Function); (3) rotacionar a key imediatamente (assume comprometida).
- **Bloqueia:** qualquer deploy público de iurisvision.

### CRIT-03 · Build HF publica sem gate de qualidade
- **Fonte:** 1.1-C03
- **Diagnóstico:** `build_hf_release.py:208-249` copia arquivos e chama `hf upload` sem validar schema, sem abortar em `corpus_records_delta != 0` (só imprime). `release_tag` default = data de hoje → reexecução no mesmo dia sobrescreve snapshot. Escrita não atômica.
- **Impacto:** Publicação pública de corpus inconsistente é possível com um `enter` errado. Snapshots do mesmo dia são destruídos sem aviso.
- **Remediação:** invocar `validate_schemas.py` no topo de `main()`; abortar em drift; abortar se `snapshot_dir` já existe sem `--force`; gerar `SHA256SUMS`; atomic write.
- **Bloqueia:** próxima release HF.

### CRIT-04 · Misattribution e breach terminológico no corpus acadêmico
- **Fonte:** 1.3-C01/C02/C03/C04/C05
- **Diagnóstico:**
  - "Contrato Sexual Visual" descrito como "transposição da crítica feminista de Pateman" em `Iconocracia_Tropical.md` e `O contrato visual — mapa conceitual.md` — **deve** ser conceito original de Ana Vanzin (2026).
  - 3× "hardening" em `Introducao_rev.md` (incluindo Painel IV do Atlas), 4× em `sumario-iconocracia.md` — **deve** ser ENDURECIMENTO.
  - 10+ "Goodrich 2014" quando `Legal Emblems` é 2013, e a obra que a tese cita (`Imago Decidendi`) é 2017.
  - ~14 citações de Mondzain em edições não-2002 (1996 ou 2005) — **deve** ser 2002 conforme contrato.
  - "Feminilidade de Estado" grafada como "feminilidade estatal" em 2 memorandos.
- **Impacto:** Perda de autoria intelectual nos dois conceitos mais originais da tese. Falhas ABNT em escala. Arriscado se qualquer draft sair para avaliação externa no estado atual.
- **Remediação:** sweep de correção terminológica (pode ser script de patch), começando por `Introducao_rev.md` e `tese/artigos/dessexualization-threshold-draft-v1.md`.
- **Bloqueia:** submissão de qualquer artigo; defesa de qualificação.

### CRIT-05 · dangerouslySetInnerHTML em main.jsx + zero CSP
- **Fonte:** 2.1-C-02/C-03
- **Diagnóstico:** `apps/iconocracia-companion/src/main.jsx:1511` usa `dangerouslySetInnerHTML` com HTML vindo de `/api/corpus` sem sanitização. Nenhuma das 4 surfaces HTML (2 visual-essays + atlas-iconometrico + companion) tem CSP meta. Atlas carrega Babel standalone runtime (vector XSS amplificado).
- **Impacto:** XSS stored se qualquer campo do corpus contiver HTML malicioso (hoje improvável; amanhã com ingest automatizado do Gallica, provável).
- **Remediação:** adicionar DOMPurify na companion; CSP meta em todos os HTMLs servidos; remover Babel standalone do Atlas.
- **Bloqueia:** deploy público da companion em domínio próprio.

### CRIT-06 · Join records↔corpus por URL (não item_id)
- **Fonte:** 1.1-C02
- **Diagnóstico:** `records_to_corpus.py:163-194` junta por `webscout.search_results[0].url`. Corpus tem 4 clusters de URLs duplicadas/vazias (2 None, 6 "", europeana dup, loc.gov dup). Colisões perdem registros silenciosamente. Output não ordenado → idempotência byte-a-byte quebrada.
- **Impacto:** Corrupção silenciosa do corpus em cada run; diff inútil.
- **Remediação:** chave de join = item_id (UUID5 determinístico), sort por item_id antes de escrever, falhar em colisão, atomic write.
- **Bloqueia:** CRIT-01 (não dá para arrumar o contrato sem arrumar o join).

### CRIT-07 · Visual-essay duplicado (perda de snapshot pré-refactor)
- **Fonte:** 1.3-M01, 2.1-major
- **Diagnóstico:** `visual-essay-iconocracia.html` e `visual-essay-refactored.html` são byte-idênticos (MD5 igual). Aconteceu na sessão de refactor quando copiei em vez de preservar. O plano de refactor dizia "salvar como `visual-essay-refactored.html`" mas ambos foram editados.
- **Impacto:** Snapshot pré-refactor perdido — impossível mostrar orientador o antes/depois.
- **Remediação:** recuperar versão pré-refactor via `git log -- docs/superpowers/visual-essay-iconocracia.html` e restaurar o `iconocracia.html` para estado original; ou decidir promover `refactored.html` a canônico e deletar duplicata.
- **Bloqueia:** nada, mas é embaraçoso.

### CRIT-08 · Path hardcoded em script de sync
- **Fonte:** 2.2-C1
- **Diagnóstico:** `scripts/sync-thesis-content.mjs` tem `/Users/ana/Research/hub/...` hardcoded. Quebra portability, CI, containerização, qualquer colaborador.
- **Remediação:** parametrizar via `process.env.RESEARCH_ROOT` com default para `path.resolve(__dirname, '../../..')` ou similar.
- **Bloqueia:** cotutela (outro pesquisador executar o sync).

---

## 2. Matriz de Dependências entre Findings

```
CRIT-01 (contrato records↔corpus)
   ├── depende de: CRIT-06 (join por item_id)
   └── destrava: CRIT-03 (HF release gate), M-03 (lineage tests), 2.3-C2 (notebooks 05-08 rodam)

CRIT-02 (GEMINI key leak)
   └── isolada — pode fixar em paralelo

CRIT-03 (HF release gate)
   └── depende de: CRIT-01 (arrumar o estado antes do gate)

CRIT-04 (misattribution + terminologia)
   ├── depende de: decisão sobre "hardening" em inglês-só-para-dessexualization-threshold (intencional ou não?)
   └── destrava: submissão de qualquer artigo, peer-review da TOP-3 (genealogia já feita, faltam Introducao_rev e Iconocracia_Tropical)

CRIT-05 (XSS via dangerouslySetInnerHTML + CSP ausente)
   └── depende de: saneamento do pipeline de ingest (garantia de que corpus-data não contém HTML)

CRIT-06 (join unsafe)
   └── pré-requisito de CRIT-01

CRIT-07 (visual-essay dup)
   └── isolada — fix trivial (git revert ou rename)

CRIT-08 (path hardcoded)
   └── isolada

Dependências ORDEM GLOBAL de fix:
  Sprint 1: CRIT-02 + CRIT-07 + CRIT-08 (isoladas, cada uma <30min) +
            CRIT-06 → CRIT-01 → CRIT-03 (cadeia canônica) +
            CRIT-04 parcial (Introducao_rev + Iconocracia_Tropical)
  Sprint 2: CRIT-05 + CRIT-04 completo (todos os drafts) + tests/pipeline/ + notebooks
  Sprint 3: refactor main.jsx + design-tokens shared + CI da companion
```

---

## 3. Top-20 Findings Consolidados (CRITICAL + MAJOR)

| # | Severidade | Domínio | Título | Fonte |
|---|---|---|---|---|
| 1 | CRITICAL | data | Contrato records↔corpus quebrado (2 vs 165) | 1.1-C01 |
| 2 | CRITICAL | security | GEMINI_API_KEY leak em vite.config.ts | 1.2-C01/2.1-C-01 |
| 3 | CRITICAL | academic | Misattribution de Contrato Sexual Visual a Pateman | 1.3-C02 |
| 4 | CRITICAL | academic | "hardening" no Introducao_rev + sumário | 1.3-C01/C05 |
| 5 | CRITICAL | data | HF release publica sem gate | 1.1-C03 |
| 6 | CRITICAL | data | Join por URL (não item_id) | 1.1-C02 |
| 7 | CRITICAL | data | 0 atomic writes na cadeia canônica | 1.1-C04 |
| 8 | CRITICAL | arch | 4 cópias de corpus-data.json divergentes | 2.2-C2 |
| 9 | CRITICAL | arch | Path hardcoded em sync-thesis-content.mjs | 2.2-C1 |
| 10 | CRITICAL | arch | companion sem .gitignore, sem CI, sem AGENTS.md próprio | 1.2-C03/2.2-C3 |
| 11 | CRITICAL | security | dangerouslySetInnerHTML sem sanitize + zero CSP | 2.1-C-02/C-03 |
| 12 | CRITICAL | data | Notebooks 05-08 nunca executados; subscores.csv órfão | 2.3-C2 |
| 13 | CRITICAL | data | environment.yml incompleto | 2.3-C3 |
| 14 | CRITICAL | viz | Visual-essay duplicado (perda de snapshot) | 1.3-M01/2.1-major |
| 15 | CRITICAL | academic | Goodrich 2014 vs 2013 (10+ ocorrências) | 1.3-C03 |
| 16 | CRITICAL | academic | Mondzain citada em 1996/2005 (~14×) quando contrato fixa 2002 | 1.3-C04 |
| 17 | MAJOR | data | 54/165 itens sem citation_abnt (33%) | 1.1-M05 |
| 18 | MAJOR | data | 19/165 sem panofsky; 19/165 sem indicadores | 1.1-M05 |
| 19 | MAJOR | data | Zero testes na cadeia canônica (11 scripts sem test) | 1.1-M03 |
| 20 | MAJOR | code | `pipelines/Atlas/atlas_iconocratico/*` duplicado em companion (MD5 divergente) | 1.2-C02 |

---

## 4. Pontos Fortes (NÃO MEXER)

1. **csv_to_records.py** usa UUID5 NAMESPACE_URL → padrão-ouro de idempotência.
2. **Schemas JSON com `additionalProperties: false`** → drift de campos bloqueado.
3. **Pre-commit hook bloqueando binários em `data/raw/`** → defense-in-depth funcional.
4. **Zero `@ts-ignore`, zero `catch {}` vazio, zero `eslint-disable` nos TS/JS repos** → higiene estática exemplar.
5. **Zero hardcoded secrets no código-fonte** (todos via `process.env`).
6. **corpus-scout-agent e gallica-mcp-server com `strict: true` no tsconfig.**
7. **gallica-mcp-server com decomposição modular exemplar** (modelo para outros repos).
8. **Topologia de symlinks estruturalmente sólida** (zero quebrados, zero circulares).
9. **Framing refactor do visual-essay 100% consistente** (13/13 pontos auditados OK).
10. **tests/argos/ é bem organizado** (12 testes + fixtures, modelo replicável para tests/pipeline/).

---

## 5. Observações Não-Quantitativas

- A dissonância entre documentação (AGENTS.md robusto, contrato explícito) e estado-no-disco sugere que a documentação foi escrita para projetar o futuro desejado do workspace — não para descrever o presente. Isso é uma escolha legítima de pesquisadora, mas cria um risco: quem entra no projeto (cotutela, orientador, banca) lê o contrato e espera encontrá-lo operativo.
- O refactor do visual-essay desta sessão produziu um resultado de alta qualidade de framing mas com 2 falhas operacionais (duplicata + não houve preservação do antes). Indica que um skill `visual-essay-refactor` com step de preservação snapshot seria valioso.
- Os 6 rascunhos-artigos não competem entre si (overlap <60%), o que é saudável. Mas a ausência de rascunho para os Capítulos 4, 5 e 8 da tese sugere que o pipeline artigos-da-tese precisa de um passe de balanceamento.
- A separação hub/apps/pipelines/labs é sólida em teoria, mas na prática: apps depende de paths absolutos do hub (CRIT-08), pipelines/Atlas é duplicado fora do sync (CRIT-02 do 1.2), labs/iurisvision roda Gemini direto no cliente (CRIT-02). O modelo funciona mas a execução cumpriu só a arquitetura macro, não a micro.

---

## 6. Roadmap de Remediação em 3 Sprints

### Sprint 1 — "Stop the bleeding" (1 semana, efetivamente 3-4 dias de trabalho)

**Objetivos:** segurança + integridade de dados. Nada público vazando, contrato canônico restaurado.

- [S1-01] Rotacionar GEMINI_API_KEY, remover `define` do vite.config.ts, mover chamadas Gemini para Cloudflare Worker proxy. **[CRIT-02]**
- [S1-02] Fix atômico em `records_to_corpus.py`: join por item_id, sort, atomic write via `tempfile + os.replace`. **[CRIT-06]**
- [S1-03] Regenerar `records.jsonl` a partir de `corpus_dataset.csv` via `csv_to_records.py`; commit reconciliação. **[CRIT-01]**
- [S1-04] Decidir canonicalização entre corpus-data.json cópias (hub=165 vs HF=145). Opções: (a) HF errado e precisa update; (b) hub precisa poda para 145. Cotar com orientador antes de agir. **[CRIT-01 parte 2]**
- [S1-05] Gate CI: adicionar steps em `validate.yml` para `len(records)==len(corpus)`, diff, trace_evidence ≥90%, ABNT ≥90%, zero URL duplicada. **[M-02]**
- [S1-06] Fix `build_hf_release.py`: validate no topo, abort em drift, abort em overwrite, SHA256SUMS. **[CRIT-03]**
- [S1-07] Resolver duplicata visual-essay: `git log -- docs/superpowers/visual-essay-iconocracia.html` → restore pré-refactor OU promover refactored a canônico e deletar duplicata. **[CRIT-07]**
- [S1-08] Fix path hardcoded em `sync-thesis-content.mjs`. **[CRIT-08]**
- [S1-09] Criar `apps/iconocracia-companion/.gitignore` (node_modules, .env, dist, .next, .wrangler). **[CRIT-10 parte 1]**
- [S1-10] Sweep terminológico parcial: `Introducao_rev.md` e `Iconocracia_Tropical.md` — todas as ocorrências de hardening→ENDURECIMENTO, Pateman→Vanzin para Contrato Sexual Visual, Goodrich 2014→2013/2017, Mondzain → 2002. **[CRIT-04 parte 1]**

**Critério de aceitação Sprint 1:**
- CI passa verde e inclui os novos gates.
- `git grep -E 'hardening|GEMINI_API_KEY|/Users/ana/'` no Introducao_rev retorna zero.
- HF release dry-run falha deterministicamente se contract breaks.

### Sprint 2 — "Tests and terminology sweep" (1 semana)

- [S2-01] Criar `tests/pipeline/` com 5 golden tests: idempotência records→corpus, UUID5 estável, schema happy/sad, roundtrip purification, aborto por drift. **[M-03]**
- [S2-02] Sweep terminológico completo: todos os 6 drafts rascunhos-artigos + `dessexualization-threshold-draft-v1.md` + `vault/tese/drafts/*.md`. **[CRIT-04 completo]**
- [S2-03] Completar ABNT em 54 itens sem `citation_abnt` (priorizar os que já estão em peer-review queue). **[M-05]**
- [S2-04] Peer-review full dos TOP-3 identificados por 1.3: `Introducao_rev.md`, `dessexualization-threshold-draft-v1.md`, `Iconocracia_Tropical.md`.
- [S2-05] Fix `environment.yml` (adicionar pandas, scipy, seaborn, statsmodels, sklearn, prince, scikit-posthocs) + executar notebooks 05-08 + commit outputs. **[2.3-C3, 2.3-C2]**
- [S2-06] Resolver colisão `fig_06-fig_10` (dois notebooks diferentes produzem fig_06). **[2.3-C1]**
- [S2-07] Adicionar DOMPurify em main.jsx:1511 + CSP meta em todos os HTMLs. **[CRIT-05]**
- [S2-08] Migrar `jsonschema.RefResolver` → `referencing.Registry`. **[M-04]**

**Critério de aceitação Sprint 2:**
- `pytest tests/pipeline/` verde.
- Zero ocorrência de "hardening" em qualquer .md da tese.
- Notebook 05-08 re-run produz subscores.csv idêntico ao do visual-essay.

### Sprint 3 — "Refactor and deduplication" (2 semanas)

- [S3-01] Refatorar `main.jsx` (2.422 LOC) em 6+ módulos coerentes. **[1.2-MAJOR]**
- [S3-02] Criar `shared/design-tokens/regimes.css` canônico; consumir em visual-essays, companion, atlas-iconometrico. **[2.1-MAJOR]**
- [S3-03] Decidir destino de `apps/iconocracia-companion/atlas-iconocratico-toolkit/atlas_iconocratico/`: deletar e consumir via symlink para `pipelines/Atlas/...` OU assumir fork oficial e documentar divergência. **[CRIT-20 da tabela / 1.2-C02]**
- [S3-04] Deletar IIFE de 371 linhas em `apps/iconocracia-companion/Atlas Iconocrático/app.js` OU mover para archive. **[1.2-C04]**
- [S3-05] Criar AGENTS.md correto para companion (não copy-paste do scout-agent). **[2.2-MAJOR]**
- [S3-06] Adicionar CI básica para companion e iurisvision (typecheck + build + artifact size). **[2.2-CRIT-04]**
- [S3-07] Mover orphans do hub para archive ou documentar: `hub/postman/` (55MB), `hub/gallery/`, `hub/concepts/`, `hub/entities/`, `hub/biblio/`, `hub/PHD/`. **[2.2-MINOR]**
- [S3-08] Seed discipline: adicionar `np.random.seed(42)` em notebooks 03 e 08. **[2.3-M3]**
- [S3-09] nbstripout + Makefile `make notebooks` para regeneração fim-a-fim. **[2.3-MAJOR]**

**Critério de aceitação Sprint 3:**
- `wc -l main.jsx` < 500.
- Apenas 1 cópia ativa de `atlas_iconocratico/` no workspace.
- CI ativa em todos os repos de código.

---

## 7. Entregáveis da Ultraplan (status)

| Artefato | Status | Caminho |
|---|---|---|
| Plano mestre | ✅ | `docs/superpowers/plans/2026-04-17-research-workspace-full-audit.md` |
| Relatório 1.1 Data Engineer Hub | ✅ | `docs/superpowers/audit/2026-04-17/1.1-data-engineer-hub.md` |
| Relatório 1.2 Code Reviewer Ecosystem | ✅ | `docs/superpowers/audit/2026-04-17/1.2-code-reviewer-ecosystem.md` |
| Relatório 1.3 Academic Content | ✅ | `docs/superpowers/audit/2026-04-17/1.3-academic-content-review.md` |
| Relatório 2.1 Frontend Visual | ✅ | `docs/superpowers/audit/2026-04-17/2.1-frontend-visual.md` |
| Relatório 2.2 Architecture | ✅ | `docs/superpowers/audit/2026-04-17/2.2-architecture.md` |
| Relatório 2.3 Notebooks | ✅ | `docs/superpowers/audit/2026-04-17/2.3-notebooks.md` |
| **Síntese** | ✅ | `docs/superpowers/audit/2026-04-17/00-synthesis.md` (este arquivo) |
| Plano Sprint 1 | pendente | `docs/superpowers/plans/2026-04-XX-remediation-sprint-1.md` (gerar sob demanda) |

---

## 8. Métricas Finais da Auditoria

- **Tempo wall-clock:** ~12 min (Wave 1: 5:30, Wave 2: 5:30, Síntese: 2-3 min)
- **Custo de iterações:** 76 tool calls distribuídas em 6 agentes (vs. ~300+ que seria preciso single-threaded)
- **Arquivos analisados:** 51 scripts Python + 7 schemas + 4 package.json + 8 notebooks + ~38 arquivos JS/TS + ~32 drafts acadêmicos + 4 HTMLs = **~144 artefatos auditados**
- **Findings produzidos:** 16 CRITICAL + 21 MAJOR + 35+ MINOR = **~72 findings**, zero duplicados entre agentes
- **Domínios cobertos:** 5 lentes (data-engineer, code-reviewer, academic, frontend, architecture)
- **Pontos fortes identificados:** 10 (usados como guardrails do que NÃO mexer)

---

## 9. Próximo passo sugerido

Três caminhos:

1. **Gerar Sprint 1 executável** — um plano `writing-plans`-compliant com código exato, comandos exatos, testes, commits, para cada S1-01 até S1-10. Entrega: novo arquivo `docs/superpowers/plans/2026-04-18-remediation-sprint-1.md`.
2. **Começar execução Sprint 1 agora** — ir direto para S1-01 (GEMINI key) ou S1-07 (visual-essay dedup), mais simples e isolados.
3. **Reunir com orientador** — o CRIT-01 parte 2 (hub=165 vs HF=145) envolve decisão editorial que não deveria ser feita sozinha.

Recomendação: (2) para os isolados (CRIT-02, CRIT-07, CRIT-08), porque são quick wins sem risco, depois (1) para o núcleo de dados (CRIT-01 + CRIT-03 + CRIT-06), depois (3) para o CRIT-04 acadêmico que precisa do olho da autora.
