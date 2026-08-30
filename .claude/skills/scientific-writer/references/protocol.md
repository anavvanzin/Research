# Scientific Writer — protocol and templates

Loaded on demand. `SKILL.md` is sufficient for routine drafting; read this when the user
asks for gate checklists, a submission template, or a formal artifact.

---

## G1 · Sources

Build the working bibliography **before** outlining. A source enters the bibliography only
with a resolvable identifier.

| Type | Required identifier |
|---|---|
| Journal article | DOI, or a stable publisher/repository URL |
| Book / chapter | ISBN + publisher + year |
| Archival item | Repository + shelfmark/cote + permalink where digitised |
| Thesis / dissertation | Institution + year + repository handle |
| Legal source | Jurisdiction + instrument + date + official gazette reference |
| Web source | URL + access date (both required under ABNT) |

**Gate output** — a table with: short key · full reference in the target standard ·
identifier · what claim it is expected to support · verified yes/no.

**Blocks on** any entry that cannot be resolved. Report it as unresolved; do not carry it
into G2 hoping it will firm up later.

### Source discovery

Prefer, in order: sources the user already has → workspace bibliography → the Consensus,
Scite, Elicit or Scholar Gateway MCP tools when connected → general web search. Record
where each source came from; a source you could not open is not a source you can cite.

---

## G2 · Structure

One row per section. A section with no claim is cut or merged; a claim with no G1 entry
goes back to G1.

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
- Flag your own argumentative moves explicitly so G4 can tell them from sourced claims.
- Keep the author's register. Match the surrounding prose's sentence length and
  vocabulary; do not standardise it.

---

## G4 · Integrity

A separate pass over the finished draft, checked against G1. Not merged into G5.

Checklist:

- [ ] Every informative claim carries a G1 key or is explicitly marked as the author's argument.
- [ ] Every G1 key used in the text exists in the bibliography.
- [ ] Every bibliography entry is actually cited (or deliberately listed as further reading).
- [ ] Every quotation is verbatim and page-located; paraphrases are marked as paraphrase.
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
