# Weekly Audit — 2026-07-13

**Date:** 2026-07-13
**Auditor:** Claude Code (weekly-audit session, remote container)
**Scope:** all 9 ICONOCRACIA workspace repositories
**Branch:** `claude/weekly-audit-46a2jl` (each repo)

> Unlike the April/June *dependency* audits (which inspected the macOS
> symlink/filesystem layout on Ana's Mac), this audit runs in a fresh Linux
> clone. It therefore covers **content and data integrity** — reproducible from
> git — not host-specific filesystem structure.

---

## EXECUTIVE SUMMARY

The workspace is in **good health**. Every repo's audit branch was clean and
even with its default branch at session start. Corpus data passes all schema
validation and is in sync. **One material defect was found and fixed**:
`mnemosyne-viva` had unresolved git merge-conflict markers committed into a
**deployed** landing page.

**Severity:** was **HIGH** for the mnemosyne-viva site (visible corruption on a
live page); **LOW** everywhere else.

**Actions taken this audit:**
1. **Fixed** — removed leftover conflict markers in `mnemosyne-viva/site/index.html`.
2. **Refreshed** — updated the stale "Known Data Issues" snapshot in
   `iconocracy-corpus/CLAUDE.md` (dated 2026-07-02 → 2026-07-13) with verified counts.
3. **Reported** — this document.

---

## 1. `mnemosyne-viva` — CONFLICT MARKERS IN LIVE SITE ✅ FIXED

**Finding (HIGH).** `site/index.html` contained two unresolved diff3-style
conflict blocks (`<<<<<<< HEAD` … `||||||| parent` … `=======` … `>>>>>>>
79200b7`) at lines 159–190. The literal marker text would render on the page.

Ironically the previous commit — `c6ddff4 "fix: resolve merge conflicts in
site/index.html"` — claimed to resolve them but left these two blocks behind.
This is a deployed site (`CNAME`, `vercel.json`, `wrangler.jsonc` present).

**Resolution.** Kept the **HEAD** side of both blocks, which is the coherent
choice on two independent grounds:
- **Style:** HEAD uses `class="label"` — the dominant convention in the file
  (11 uses) and the class defined/aligned by the brand-board work (`#7`,
  `90c0de9`). The `|||||||` ancestor's `class="eyebrow"` is the superseded name.
- **Semantics:** HEAD's panel heading "Quatro regimes iconocráticos" matches the
  four `<strong>Fundacional/Normativo/Militar/Contra-alegoria</strong>`
  paragraphs immediately below it. The redesign side's "Pathosformeln" heading
  would mislabel that same four-regime list.

Verified: `grep` for conflict tokens across `site/`, `scripts/`, `schemas/`
now returns **0**.

---

## 2. `iconocracy-corpus` — DATA INTEGRITY ✅ CLEAN (docs refreshed)

Ran the documented validation pipeline. All green:

| Check | Result |
|---|---|
| `validate_schemas.py` (records) | **328/328 valid** ✓ |
| `validate_schemas.py … purification` | **279/279 valid** ✓ |
| `records_to_corpus.py --diff` | **in sync by URL** (328 ↔ 328) ✓ |
| `code_purification.py --status` | **279/328 coded (85%)**, 49 remaining |
| Duplicate `item_id`s | **0** ✓ |

**Movement since last audit (2026-07-02):**
- Endurecimento coding advanced **236 → 279 items** (+43; now 85% coded). Healthy
  exploratory progress, not drift.
- Placeholder URLs in the ledger dropped **8 → 6**.

**Two low-severity findings (reported, NOT auto-fixed — need Ana's eyes):**
- **Placeholder drift ledger↔export:** `records.jsonl` has **6** placeholder
  `input_url`s but `corpus/corpus-data.json` still surfaces **8** placeholder
  items. Two resolutions haven't propagated. → re-run `records_to_corpus.py`;
  verify remaining 6 against `data/raw/drive-manifest.json`.
- **4 duplicate real `input_url`s** (3× `iconocracy-corpus.local/piloto/` pilot
  rows + 3 real-source pairs). Candidates for `corpus-dedup`; not confirmed dupes.

The `CLAUDE.md` "Known Data Issues" section was refreshed to reflect the above
verified state (it had drifted to the 2026-07-02 numbers).

> Note per repo policy: corpus **N is intentionally non-fixed**. Growing counts
> are expected, not defects.

---

## 3. Cross-repo health scan

| Repo | Tracked files | Commits (14d) | Notes |
|---|---:|---:|---|
| `iconocracy-corpus` | — | active | See §2. Data clean. |
| `mnemosyne-viva` | 50 | 20 | Conflict markers fixed (§1). Otherwise active. |
| `arno-dal-ri-site` | 20 | 11 | Active; recent factual corrections. Clean. |
| `atlas-celeste` | 4 | 4 | Parchment restyle. Clean JSON. |
| `artigos` | 26 | 3 | New article added. Clean. |
| `grupoiusgentium.com.br` | 28 | 0 | Quiet 2 weeks. Open PR #4 pending (§4). |
| `atlaslab` | 95 | 2 | Dependabot merge (#2). Clean. |
| `ai-agent-notes` | 3 | 1 | Single article. Clean. |
| `Research` | — | — | Meta-workspace. This report. |

**Automated checks run across content repos:**
- **JSON validity:** all `*.json` in `mnemosyne-viva`, `atlaslab`, `atlas-celeste`
  parse cleanly — **0 invalid**.
- **Merge-conflict markers:** **0** remaining anywhere after the §1 fix. (Matches
  in `iconocracy-corpus/wiki/.obsidian/plugins/**/main.js` are minified
  third-party plugin code, not real conflicts — ignored.)

---

## 4. Open PR backlog (10 open, scoped repos)

| Repo | PR | Draft | Title |
|---|---|---|---|
| Research | #20 | — | docs: revisão de confluência entre os 9 repositórios |
| grupoiusgentium.com.br | #4 | — | feat: modernize website layout / extract partials |
| iconocracy-corpus | #13 | draft | feat(corpus): integrate gallery research — 43 new items |
| iconocracy-corpus | #82 | — | Apresentação "Do ventre à alegoria" |
| iconocracy-corpus | #118 | — | Feat/alegorias piloto v2 |
| iconocracy-corpus | #119 | — | corpus acquisition orchestrator |
| iconocracy-corpus | #136 | draft | Short paper Malleus/Cajada (ABNT, 10 p.) |
| iconocracy-corpus | #139 | — | feat(tese): fechar painéis do Capítulo 9 |
| iconocracy-corpus | #140 | — | fix(hooks): skip ML stack during SessionStart |
| iconocracy-corpus | #142 | — | docs: iconometria como framework guarda-chuva |

**Observation:** the backlog concentrates in `iconocracy-corpus` (8 open). Several
are long-lived (#13, #82, #118, #119). Recommend a triage pass to merge or close
the stale ones — carrying four+ month-old branches raises rebase/conflict risk
(cf. the mnemosyne-viva conflict this audit just fixed).

---

## 5. Recommendations (for Ana)

1. **iconocracy-corpus:** re-run `records_to_corpus.py` to clear the 6↔8
   placeholder drift; run `corpus-dedup` on the 4 duplicate `input_url`s.
2. **PR triage:** close/merge the four stale iconocracy-corpus PRs (#13, #82,
   #118, #119) to shrink conflict surface.
3. **mnemosyne-viva:** consider a pre-commit / CI grep for conflict markers so a
   `<<<<<<<` never reaches `main` again.

---

*Nothing in this audit blocks ongoing work. Corpus posture remains exploratory;
growing N is expected, not a defect.*
