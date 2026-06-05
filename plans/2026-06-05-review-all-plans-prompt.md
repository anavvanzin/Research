---
id: P-2026-019
titulo: "Review all plans in a separate session"
dominio: meta
status: rascunho
criado: 2026-06-05
ultimo_update: 2026-06-05
autor: Hermes (com Ana)
uso: "cole no início de uma nova sessão de revisão (Hermes CLI ou outro agente)"
idioma: en
output_formato: "tabela de comparação + nota final de 1 parágrafo"
---

# Review all plans — prompt

## Como usar

Abra uma nova sessão (Hermes CLI, Codex, ou o agente que você preferir). Cole o bloco **PROMPT** abaixo na primeira mensagem. A sessão deve abrir e ler os 8 arquivos de plano do repo `~/Research/plans/` (e o plano de tese em `~/Research/.opencode/plans/iconocracy-priority-plan.md`) e produzir a tabela de comparação + nota de revisão.

## PROMPT (cole a partir daqui)

```
You are reviewing 9 planning documents for Ana Vanzin's doctoral thesis
ICONOCRACIA (PPGD/UFSC, defense Nov 2027). Your job is to surface
contradictions, overlaps, and gaps across the plans — NOT to write a new
plan. The 8 plans in ~/Research/plans/ are operational plans written
across April–June 2026. The 1 plan in ~/Research/.opencode/plans/
(iconocracy-priority-plan.md, dated 2026-04-15) is the long-arc strategy.

## Documents to read (in this order)

1. /Users/ana/.opencode/plans/iconocracy-priority-plan.md
2. /Users/ana/Research/plans/2026-04-14-skill-discovery.md
3. /Users/ana/Research/plans/2026-04-24-hermes-audit-summary.md
4. /Users/ana/Research/plans/2026-04-25-dependencies-audit.md
5. /Users/ana/Research/plans/2026-04-25-workspace-dependency-audit.md
6. /Users/ana/Research/plans/2026-06-05-workspace-dependency-audit.md
7. /Users/ana/Research/plans/2026-06-05-biweekly-imes-cap6.md
8. /Users/ana/Research/plans/2026-06-05-june-plan.md
9. /Users/ana/Research/plans/visual-essay-refactor-plan.md

## Output structure

Produce a comparison table with one row per plan and these columns:
- ID (filename, no path)
- Date (yyyy-mm-dd)
- Type (long-arc strategy | monthly operational | biweekly operational |
  audit | refactor proposal | meta-tooling)
- Scope (1 line: what's covered, what's explicitly excluded)
- Cadence (when in the project timeline)
- Cross-references (which other plans it points to or contradicts)
- Status (active | superseded | historical | scratch)

Then write a "Findings" section with 3 subsections:
1. **Contradictions** — places where 2+ plans disagree on dates, scope,
   scope-inclusions, or numbers. Be specific (file:line if possible).
2. **Gaps** — what is NOT covered anywhere in the 9 plans but probably
   should be (be conservative; flag only if you can defend it).
3. **Duplication** — content that appears in 2+ plans and could be
   deduplicated by reference rather than by copying.

End with a single-paragraph "Reviewer take" that answers: which 2-3
plans should Ana treat as canonical, which 2-3 are historical/archival,
and what is the single most important thing to fix in the planning
surface this week?

## Rules

- Do NOT rewrite any plan. This is a review, not a draft.
- Do NOT propose a new plan or new structure. Surface what exists.
- Use Portuguese/English mixed as Ana does (don't translate the plan
  filenames; do use English for the review prose).
- When you cite a number (dates, word counts, Ns), cite the source
  file:line so Ana can verify.
- If a plan is unclear, say "ambiguous" — don't guess.
- Keep the whole output under 2,000 words. Ana reads in the terminal.
```

## Notas para a Ana

  - **Cole o bloco acima inteiro** a partir da linha que diz `You are
    reviewing 9 planning documents` — não precisa do cabeçalho YAML.
  - A sessão nova pode ser Hermes CLI no terminal, ou Codex, ou
    OpenCode. O prompt é agente-agnóstico.
  - Se você quiser cortar, o **núcleo mínimo** é: ler 1, 7, 8 (a
    estratégia + o biweekly + o june). Os outros 6 são contexto
    histórico; cite-os como contexto, mas a análise principal fica em
    1, 7, 8.
  - O output foi pensado pra caber no terminal. Se a outra sessão
    devolver algo gigante (>2k palavras), peça um resumo.

## Resultado esperado

  - Tabela com 9 linhas, todas as colunas preenchidas.
  - Findings: 0-3 contradições, 0-3 gaps, 0-3 duplicações
    (provavelmente 1-2 de cada, dado o histórico).
  - Reviewer take de 1 parágrafo.
  - Verificável: cada número citado tem referência arquivo:linha.

## Quando rodar

  - Antes da próxima reunião de orientação (vale a pena ter o
    veredito sobre canonização dos planos na mão).
  - Ou depois da Semana 1 do biweekly (06-12), quando der pra comparar
    "o que o plano disse" vs. "o que aconteceu".
  - Não rodar antes de 2026-06-08: o biweekly só entra em vigor nessa
    data e a revisão fica vazia.
