# Scientific Writer — protocol and templates

Loaded on demand. `SKILL.md` is sufficient for routine drafting; read this when the user
asks for gate checklists, a submission template, or a formal artifact.

**Escopo dos gates.** G1→G6 governam um **ciclo completo de escrita** — texto produzido
do zero ou revisado por inteiro. Uma rota direta da triagem (revisar um parágrafo,
padronizar uma referência, iterar um outline) **não passa por eles**: responde na rota
escolhida, sob as Non-negotiables do `SKILL.md`. Mesma regra que a seção *Gates* do
`SKILL.md`; se divergirem, o `SKILL.md` é o resumo e esta é a versão detalhada.

---

## G1 · Sources

Build the working bibliography **before** outlining. A source enters the bibliography only
with a resolvable identifier.

| Type | Required identifier |
|---|---|
| Journal article | DOI, or a stable publisher/repository URL |
| Book / chapter | ISBN **ou** outro identificador resolvível (permalink de catálogo, OCLC, registro de biblioteca) — obra anterior ao ISBN ou edição acadêmica sem ele entra por aí; editora e ano seguem obrigatórios como metadado |
| Archival item | Repository + shelfmark/cote + permalink where digitised |
| Thesis / dissertation | Institution + year + repository handle |
| Legal source | Jurisdiction + instrument + date + official gazette reference |
| Web source | URL + access date (both required under ABNT) |

**Gate output** — a table with: short key · full reference in the target standard ·
identifier · what claim it is expected to support · **resolvido** sim/não · **verificado**
sim/não.

As duas colunas finais medem coisas diferentes e nenhuma substitui a outra:

- **resolvido** — o identificador leva ao registro da obra. É o requisito de *entrada* na
  bibliografia.
- **verificado** — o texto foi aberto e a afirmação foi conferida nele. É o requisito de
  *uso como evidência*.

**Blocks on** qualquer entrada que não resolve: reporte como não resolvida e não a leve
para G2 na esperança de firmar depois.

**Uma entrada `verificado = não` não bloqueia G1, mas bloqueia o uso.** Ela existe na
bibliografia como pendência, e nenhuma afirmação pode se ancorar nela: um DOI ou URL que
resolve sem dar acesso ao texto não autoriza atribuir nada à obra. Até que o conteúdo seja
consultado, a claim que dependia dela é marcada como não verificada — como manda a linha
*a source you could not open is not a source you can cite*, abaixo — ou a fonte é pedida
ao usuário. G4 cobra essa distinção; G3 não deve escrever contra uma chave pendente.

### Source discovery

Prefer, in order: sources the user already has → workspace bibliography → the Consensus,
Scite, Elicit or Scholar Gateway MCP tools when connected → general web search. Record
where each source came from; a source you could not open is not a source you can cite.

---

## G2 · Structure

One row per section. A section with no claim is cut or merged. Uma claim sem entrada G1
volta para G1, salvo a que leva **marca autoral**. A regra é enunciada uma única vez, nas
*Non-negotiables* do `SKILL.md` — não a reformule aqui: foi a reformulação em paralelo que
fez G2 e G4 divergirem duas vezes.

| § | Section | Claim it must carry | G1 keys | Words |
|---|---|---|---|---|

**Gate output** — the completed table, plus the single sentence the whole text argues.
If that sentence cannot be written, the structure is not ready.

---

## G3 · Draft

One section per round. Before drafting a section, restate its claim and its G1 keys.

- Write to the claim in the G2 row — no new claims smuggled in at draft time.
- Mark every borrowed statement with its G1 key inline as you write (`[SILVA2019]`),
  converting to the venue's citation form at G6. Anchoring after the fact is how
  unanchored claims survive.
- Aplique a **marca autoral** aos seus próprios movimentos argumentativos enquanto escreve, para o G4 distingui-los das claims com fonte.
- Keep the author's register. Match the surrounding prose's sentence length and
  vocabulary; do not standardise it.

---

## G4 · Integrity

A separate pass over the finished draft, checked against G1. Not merged into G5.

Checklist:

- [ ] Every informative claim carries a G1 key or the **marca autoral** (*Non-negotiables*, `SKILL.md`).
- [ ] Nenhuma claim se ancora numa entrada G1 com `verificado = não` — identificador que
      resolve não é texto conferido.
- [ ] Every G1 key used in the text exists in the bibliography.
- [ ] Every bibliography entry is actually cited (or deliberately listed as further reading).
- [ ] Every quotation is verbatim and **locatable**: página quando a fonte é paginada; seção, parágrafo, timestamp ou outro localizador estável quando não é (fonte web, documento digital sem paginação). Paráfrases marcadas como paráfrase.
- [ ] No claim attributed to a source that does not make it.
- [ ] Numbers, dates, N-counts and proper names match their sources.
- [ ] No citation invented, inferred, or reconstructed from memory.

**Gate output** — the checklist with each box resolved, plus an explicit list of anything
left unanchored. One unanchored claim blocks G5.

---

## G5 · Review

Adversarial, not confirmatory. Invoke `academic-writing-reviewer`; add
`iconocracy-reviewer` for Portuguese or French text, legal history, or iconology.

Ask the reviewer for: argument structure and logical flow · unsupported assertions ·
terminological inconsistency across sections · bibliographic compliance · prose clarity
without loss of voice.

**Gate output** — findings list, each marked *addressed* / *rejected with reason*.
Unresolved findings block G6.

---

## G6 · Format and submit

- [ ] Reference list in the venue's standard (ABNT NBR 6023:2025 PT / Chicago EN).
- [ ] In-text citation form matches the reference list.
- [ ] Length limits met (words, pages, characters — check which the venue counts).
- [ ] Abstract and keywords in every required language.
- [ ] Figures and tables numbered, captioned, and each cited in the text.
- [ ] Figure sources and permissions recorded.
- [ ] Author metadata, affiliation, ORCID, funding statement.
- [ ] Anonymised version prepared if the venue is double-blind.
- [ ] File format as required — use `docx` / `pdf` / `pptx` for the deliverable.

---

## Reviewer response template

One row per reviewer point. Never mark a point addressed without naming where.

| # | Reviewer point | Response | Change made | Location |
|---|---|---|---|---|

Open with a short thanks and a summary of the substantive changes. Address every point,
including those you decline — a declined point gets a reason, not silence. Quote the
reviewer's wording so the editor can follow without the original to hand.

---

## Grant proposal skeleton

Adjust to the funder's form; the underlying gates are unchanged.

1. **Problem** — what is not known, and why that gap matters now.
2. **State of the art** — G1 sources, positioning the proposal against them.
3. **Hypothesis / research question** — falsifiable, or clearly framed as interpretive.
4. **Method** — what will be done, with what materials, in what order.
5. **Feasibility** — why this team, this infrastructure, this timeframe.
6. **Timeline** — milestones with deliverables.
7. **Expected outcomes and dissemination.**
8. **Budget justification** — each line tied to a method step.
9. **Risks and mitigation** — name the real ones.

Funder review is adversarial: assume every unjustified claim is challenged.

---

## Handing off to the thesis pipeline

When a standalone paper draws on ICONOCRACIA material, this skill stays the owner of the
paper, but:

- corpus figures, item counts, and coding claims come from the thesis repo — never
  restate a corpus number from memory; cite the freeze;
- if the work turns into a thesis chapter, hand the object to
  `iconocracia-pipeline-router` and stop.
