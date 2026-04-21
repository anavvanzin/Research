---
name: iconocracia-pipeline-router
description: Route ICONOCRACIA thesis work through the correct academic research pipeline while preserving context. Use when a request concerns thesis research, chapter planning, Socratic inquiry, Santha method, hypothesis generation, academic writing, adversarial review, methodology review, citation integrity, ABNT readiness, publication, or thesis compilation for ICONOCRACIA.
---

# ICONOCRACIA Pipeline Router

Use this skill before calling academic research, writing, review, or integrity
pipelines for Ana Vanzin's ICONOCRACIA thesis. The goal is to choose the
smallest correct pipeline, keep one principal object in context, and prevent
the full academic pipeline from becoming the continuous engine of the thesis.

For the full protocol and templates, read `references/protocol.md` only when
the user asks for the detailed gate outputs, a reusable checklist, or a formal
artifact.

## Operating Rule

Start every execution with a compact state summary:

- request;
- principal object in context;
- selected route;
- gate to run now;
- checkpoint that blocks progress.

Load at most one principal object per round:

- one chapter;
- one article;
- one hypothesis matrix;
- one review report;
- one runbook or protocol.

Large materials enter by summary plus local path, not by copying full text.
If the task needs multiple objects, split the work into rounds.

## Route Triage

Classify the user request before invoking any pipeline.

`research`:
Use when question, contribution, scope, concept, or bibliography is unstable.
Prefer `deep-research socratic`; then use `lit-review`, `fact-check`, or
`systematic-review` only for bounded tasks. Block drafting final text until the
question converges.

`write`:
Use when argument or materials exist, but structure is missing. Prefer
`academic-paper plan`; use `full` only after plan approval. Block full writing
mode as the first step for thesis work.

`review`:
Use when a substantive text needs simulated peer review or banca pressure.
Prefer `academic-paper-reviewer full`, `guided`, or `methodology-focus`.
Critical Devil's Advocate findings block closure.

`integrity`:
Use when text is near qualification or submission readiness. Prefer citation,
claim verification, `abnt-format`, and Zotero/ABNT checks. Block readiness if
claims or citations remain open.

`publish`:
Use for dataset, HF Space, companion app, or public release. Prefer hub scripts
plus release workflow. Block publication before schema, diff, vault status, and
corpus checks.

`compile`:
Use to generate thesis or chapter DOCX/PDF. Prefer `compilar-tese` or
`make -C vault/tese/`. Block final compilation with critical `[VERIFICAR]`
markers.

## Gate Sequence

Default sequence:

```text
Socratic Gate
-> Santha Gate
-> Hypothesis Gate
-> Writing Gate
-> Adversarial Gate
-> Integrity Gate
```

Skip a gate only when its output is already present and current.

### Socratic Gate

Use when question, contribution, method, or scope is uncertain.

Required output:

- research question in one sentence;
- provisional thesis;
- assumptions;
- evidence needed;
- likely risks and objections;
- next gate.

### Santha Gate

Treat the Santha method as a mandatory explication slot, not as an automatic
method, until Ana defines it operationally in the workspace.

Required Santha Card:

```markdown
## Santha Card

- Objetivo:
- Sequencia de operacoes:
- Quando usar:
- Produto final:
- O que o metodo nao decide:
```

If the Santha Card is empty or generic, record the gap. Do not use Santha as a
methodological justification.

### Hypothesis Gate

Use `hypothesis-generation` to convert concepts into testable hypotheses.

Start with four ICONOCRACIA blocks:

- Contrato Sexual Visual;
- Feminilidade de Estado;
- Contrato Racial Visual;
- Purificacao Classica.

Required matrix columns:

- hypothesis;
- prediction;
- expected evidence;
- falsifier;
- destination chapter or article.

### Writing Gate

Use `academic-paper plan` before any integral writing.

Required output:

- outline;
- evidence map;
- claims by section;
- gaps;
- target word count;
- materials included and excluded.

For thesis work, operate by chapter or small artifact. Use `academic-pipeline`
only for closed articles or nearly ready chapters.

### Adversarial Gate

Use `academic-paper-reviewer` or `scientific-critical-thinking`.

Prefer:

- `academic-paper-reviewer full` for substantive drafts and almost-ready
  articles;
- `academic-paper-reviewer methodology-focus` for chapters 5-6, endurecimento,
  IRR, statistics, and indicator validity;
- `scientific-critical-thinking` for circularity, bias, inference validity, and
  evidence-to-conclusion pressure.

Required output:

- priority objections;
- methodological risk;
- conceptual risk;
- recommended revision;
- blocking items.

### Integrity Gate

Use before qualification, submission, or public release.

Check:

- citations and references;
- historical and theoretical claims;
- ABNT NBR 6023:2025;
- consistency among text, corpus, notebooks, and release artifacts;
- traceability for corpus-derived claims.

Classify each issue as:

- correct;
- verify;
- accept as limitation;
- remove.

## ICONOCRACIA Defaults

- Main horizon: qualification 2027.
- Default language: Portuguese; keep code identifiers and skill names in the
  original.
- Field boundary: criminal law history and legal iconography. Avoid drift into
  general anthropology, sociology, or generic visual culture.
- `academic-research` is an index, not the executor.
- `academic-pipeline` is exceptional, not the default.
- For large materials, prefer summary plus local path.

## Scenarios

- Vague chapter idea: run `deep-research socratic`; do not draft directly.
- Chapter with argument but no structure: run `academic-paper plan`.
- Almost-ready article: run `academic-paper-reviewer full`, then revision.
- Originality debate: run Socratic Gate, Hypothesis Gate, and Devil's Advocate.
- Chapters 5-6 check: run `methodology-focus` plus
  `scientific-critical-thinking`.
- Undefined Santha method: fill Santha Card; do not treat it as operational.
