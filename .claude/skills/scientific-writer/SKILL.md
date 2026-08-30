---
name: scientific-writer
description: Plan, draft, review and prepare standalone scientific and academic texts for submission — artigos, papers, grant proposals, abstracts, resumos expandidos, book chapters, conference submissions, peer-review responses. Use when the user asks to escrever/redigir/estruturar um artigo, montar um paper, preparar submissão, write a paper, draft a grant, build an outline for a manuscript, or respond to reviewers. Enforces ABNT NBR 6023:2025 for Portuguese and Chicago for English, and the rule that every informative claim is traceable to an identifiable source. For ICONOCRACIA thesis chapters use `iconocracia-pipeline-router` instead.
---

# Scientific Writer

Entry point for **standalone** academic writing in Ana Vanzin's workspace: articles,
grant proposals, abstracts, conference papers, book chapters, reviewer responses.

This skill **routes and enforces**; it does not reimplement pipelines that already exist.

## Scope boundary — read first

| Object | Owner |
|---|---|
| ICONOCRACIA thesis chapter, corpus, hypothesis matrix, thesis compile | **`iconocracia-pipeline-router`** — stop here and invoke it |
| Standalone artigo, paper, grant, abstract, chapter for an edited volume, reviewer response | **this skill** |

The two never run together on the same object. If the request names a thesis chapter or
the corpus, hand off to the router and say so in one line. If it names a paper drawn
*from* thesis material, this skill owns it — the paper is the principal object, the thesis
is a source.

## `init` — starting a new writing project

Reproduces what an external scientific-writing plugin would set up. Establish and echo
back, in five lines, before writing anything:

1. **Object** — what is being written (artigo / grant / abstract / chapter / response).
2. **Target** — journal, funder, event, or volume, with its length and format limits.
3. **Language + citation standard** — Portuguese → ABNT NBR 6023:2025; English → Chicago.
   French → follow the target venue.
4. **Working paths** — where the draft and its bibliography live. Confirm the target path
   before creating any file (workspace rule).
5. **Sources on hand** — what already exists vs. what must be found.

Anything unknown after this is a question for the user, not an assumption.

## Operating rule

Start every round with a compact state summary: request · principal object · selected
gate · what blocks progress.

**One principal object per round** — one paper, one proposal, one review response. Large
materials enter by summary plus local path, never by pasting full text. If the task needs
several objects, split it into rounds.

## Route triage

Classify before invoking anything.

| Request | Route |
|---|---|
| "encontre fontes sobre X", literature landscape, state of the art | `academic-pipeline` (research stage) — or the Consensus / Scite / Elicit MCP tools when available |
| "escreva o artigo", "monte o paper", full research→write→review cycle | `academic-pipeline` (all 9 stages) |
| "revise este parágrafo", "está OK?", claim anchoring, argument flow | `academic-writing-reviewer` |
| ABNT formatting, PT/FR review, legal-history and iconology rigor | `iconocracy-reviewer` |
| Outline iteration, hooks, section-by-section feedback | `content-research-writer` |
| Deliverable is `.docx` / `.pdf` / `.pptx` | `docx` / `pdf` / `pptx` |
| Anything touching the thesis | `iconocracia-pipeline-router` |

Pick the **smallest** route that answers the request. A one-paragraph review does not
need the nine-stage pipeline.

## Gates

Run in order. Each gate has an output that blocks the next.

| Gate | Produces | Blocks on |
|---|---|---|
| **G1 · Sources** | Working bibliography, each entry with a resolvable identifier (DOI, ISBN, permalink, archive shelfmark) | Any entry that cannot be resolved |
| **G2 · Structure** | Section outline with the claim each section must carry | A section with no claim, or a claim with no source |
| **G3 · Draft** | Prose, one section per round | — |
| **G4 · Integrity** | Every informative claim mapped to a G1 entry | One unanchored claim |
| **G5 · Review** | Adversarial pass via `academic-writing-reviewer` (+ `iconocracy-reviewer` for PT/FR) | Unresolved finding |
| **G6 · Format** | Reference list in the venue's standard, length and format limits met | Any reference failing the standard |

G4 is not optional and is not merged into G5. Integrity is a separate pass over the
finished draft, checked against G1 — not a reviewer's impression.

## Non-negotiables

- **Never fabricate a citation.** No invented DOI, page range, publisher, year, or
  quotation. An unverified source is reported as unverified, never smoothed into the text.
- **Every informative claim is traceable** to an identifiable source. Claims that are the
  author's own argument are marked as such, not dressed as established fact.
- **Preserve the author's voice.** Improve clarity and structure; do not flatten prose
  into generic academic register, and do not rewrite an argument into a different one.
- **Quotations are exact.** If the source text is not in hand, paraphrase and say so.
- **Portuguese is the response language** (workspace profile); code identifiers stay in
  the original.
- Confirm the target path before creating any file.

## Citation standards

| Language | Standard |
|---|---|
| Portuguese | ABNT NBR 6023:2025 |
| English | Chicago |
| French | Venue's standard; ABNT if the venue is Brazilian |

For ABNT mechanics and worked examples, invoke `iconocracy-reviewer` — it owns the
formatter. Do not re-derive ABNT rules here.

## Deeper protocol

Read `references/protocol.md` only when the user asks for gate checklists, a reusable
submission template, or a formal artifact. Routine drafting does not need it.
