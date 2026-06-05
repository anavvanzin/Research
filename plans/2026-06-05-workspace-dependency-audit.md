# Workspace Dependency Audit — 2026-06-05

**Date:** 2026-06-05
**Audited root:** /Users/ana/Research
**Auditor:** Hermes Agent (iconocracy-workspace-dependency-audit)
**Skill version:** 2026-04-25 (with June 4 SSD-consolidation reference)

---

## EXECUTIVE SUMMARY

The ICONOCRACY workspace is in **a clean, well-maintained state**. The April 2026 audit's main remediation items have all been applied: the `~/iconocracy-corpus` top-level symlink exists, the `~/.claude.json` has a single canonical project entry, all five "Caminhos legados" symlinks are present and functional, and the working tree is intact (no `D`eleted-but-tracked files).

The **one material deviation** from the skill's reference doc (`ssd-consolidation-2026-06-04.md`): the SSD is **not currently mounted** at `/Volumes/data`, and the canonical corpus lives on the **internal disk** at `~/Research/hub/iconocracy-corpus`. A `~/Research/iconocracy-corpus` symlink still points to the (unmounted) SSD path and is dangling.

**Severity:** **LOW** — no tools are blocked; the dangling `~/Research/iconocracy-corpus` symlink is not referenced by any active config or script.

**Key issues:**
1. **DANGLING SYMLINK** — `~/Research/iconocracy-corpus` → `/Volumes/data/projetos/research/hub/iconocracy-corpus` (SSD not mounted)
2. **DUPLICATE CLONES** — `~/projetos/research/hub/iconocracy-corpus` (596 MB) and `~/Documents/GitHub/iconocracy-corpus` (575 MB) are independent git repos from May 24 / May 30, both pre-dating the move to `~/Research/hub/`
3. **BRANCH STATE** — canonical repo is on `reconcile/ssd-scripts-2026-06-04` (not `main`); 4 modified + 1 untracked working-tree entries (low-risk Obsidian session churn)

---

## 1. STRUCTURE OVERVIEW

```
/Users/ana/
├── Research/                       ← ACTIVE workspace (case-insensitive alias: research/)
│   ├── hub/
│   │   ├── iconocracy-corpus/      ← CANONICAL THESIS REPO (HEAD: 72d560d, 1.3 GB)
│   │   └── mnemosyne-scout/
│   ├── apps/
│   │   ├── iconocracia-companion/  ← target of legacy symlink
│   │   └── iconocracia-space/      ← target of legacy symlink
│   ├── shared/
│   │   ├── iconclass-data/         ← target of legacy symlink
│   │   └── iconclass-data-avmadrj/ ← target of legacy symlink
│   ├── labs/
│   │   └── iuris-visio-roadmap/    ← target of legacy symlink
│   ├── Paths/                      ← enumerated dependency lists (paths-1.1/1.2/1.3.txt)
│   ├── Plans/                      ← audit reports (this file joins 2026-04-25, 2026-04-30, etc.)
│   ├── docs/, Specs/, gestao/, etc.
│   └── README.md                   ← workspace index
│
├── iconocracy-corpus               ✓ SYMLINK → /Users/ana/research/hub/iconocracy-corpus
├── iconocracia-companion           ✓ SYMLINK → /Users/ana/Research/apps/iconocracia-companion
├── iconocracia-space               ✓ SYMLINK → /Users/ana/Research/apps/iconocracia-space
├── iconclass-data                  ✓ SYMLINK → /Users/ana/Research/shared/iconclass-data
├── iconclass-data-avmadrj          ✓ SYMLINK → /Users/ana/Research/shared/iconclass-data-avmadrj
├── iuris-visio-roadmap             ✓ SYMLINK → /Users/ana/Research/labs/iuris-visio-roadmap
│
├── Research/iconocracy-corpus      ✗ DANGLING SYMLINK → /Volumes/data/projetos/research/hub/iconocracy-corpus (SSD unmounted)
│
├── projetos/research/hub/iconocracy-corpus/   ⚠ STALE CLONE (596 MB, last commit 2026-05-24)
├── Documents/GitHub/iconocracy-corpus/        ⚠ STALE CLONE (575 MB, last commit 2026-05-30)
│
├── .claude.json                    ✓ one canonical entry: /Users/ana/Research/hub/iconocracy-corpus
│
└── Research/united-by-marriage/CLAUDE.md   ✓ line 60: "~/research/hub/iconocracy-corpus/" (correct)
```

**Filesystem notes:**
- macOS APFS case-insensitive: `research/` and `Research/` resolve to inode **72484221** (same directory)
- Always use lowercase `research/` in scripts (portable to Linux)
- SSD at `/Volumes/data` is **NOT** currently mounted; corpus lives on internal disk
- 5 legacy top-level symlinks + 1 main corpus symlink = all 6 functional

---

## 2. CRITICAL BROKEN DEPENDENCIES

### 2.1 DANGLING `~/Research/iconocracy-corpus` SYMLINK

**Impact:** Low — nothing actively references this path. The functional symlink at `~/iconocracy-corpus` is the one used.

**What:** A symlink `~/Research/iconocracy-corpus` was created on 2026-06-04 22:29 pointing to `/Volumes/data/projetos/research/hub/iconocracy-corpus` (per the June 4 SSD-consolidation effort). The SSD is not currently mounted, so the symlink dangles.

**Verification:** No active config, script, or doc references `/Users/ana/Research/iconocracy-corpus` as a literal path. Active references go through `hub/iconocracy-corpus` (the real directory) or `~/iconocracy-corpus` (the working top-level symlink).

**Recommendation:**
- **Option A (do nothing now):** wait for SSD to remount, or wait for the SSD-consolidation to complete
- **Option B (re-point the symlink):** `rm ~/Research/iconocracy-corpus && ln -s /Users/ana/Research/hub/iconocracy-corpus /Users/ana/Research/iconocracy-corpus` — keeps the dual-symlink topology the June 4 plan envisioned, but redirects to the live location
- **Option C (defer to user):** surface this finding and let Ana decide. Per memory: "Push-to-main is gated — always get explicit user OK"

### 2.2 NO STALE `.claude.json` PROJECT ENTRY

**File:** `/Users/ana/.claude.json` (84 KB)

**Findings:**
- Line **851**: `"/Users/ana/Research/hub/iconocracy-corpus": { ... }` — **single canonical entry, correct path**
- Line **2206–2207**: `anavvanzin/iconocracy-corpus` (GitHub remote) → `/Users/ana/Research/hub/iconocracy-corpus` — also correct
- **No** stale `"/Users/ana/iconocracy-corpus": { ... }` block
- **No** dangerous `rm -rf /Users/ana/iconocracy-corpus*` or `cd /Users/ana/iconocracy-corpus` patterns in hooks (verified across `.claude.json` and `.hermes/.skills_prompt_snapshot.json`)

**Status:** Clean. The April 2026 audit's P0 `.claude.json` issue has been resolved.

### 2.3 NO STALE DOCUMENTATION REFERENCES

**Files checked:**
- `~/Research/README.md` — references `hub/iconocracy-corpus/` (correct)
- `~/Research/CLAUDE.md` — references `hub/iconocracy-corpus/` (correct)
- `~/Research/united-by-marriage/CLAUDE.md` line 60 — "The PhD thesis codebase is at `~/research/hub/iconocracy-corpus/`" (correct, lowercase `research`)
- `~/Research/hub/iconocracy-corpus/CLAUDE.md` line 13 — refers to `~/Documents/projetos/research/CLAUDE.md` (a *meta-workspace* reference, unrelated to the corpus path itself; not stale)
- `~/Research/hub/iconocracy-corpus/README.md` — only canonical references (HF dataset name, GitHub repo name)

**Status:** Clean.

---

## 3. CORPUS WORKING TREE CORRUPTION

**Location:** `/Users/ana/Research/hub/iconocracy-corpus`

**`git status` output:**
```
 M corpus/DASHBOARD_CORPUS.html
 M vault/.makemd/fileCache.mdc
 M vault/.makemd/superstate.mdc
 M vault/.space/context.mdb
?? "vault/Untitled Kanban.md"
```

- **0** `D`eleted-but-tracked files
- **4** modified files (Obsidian/MakeMD caches, dashboard HTML — all benign)
- **1** untracked file (transient Kanban note)
- **Branch:** `reconcile/ssd-scripts-2026-06-04` (NOT `main`)
- **HEAD:** `72d560d vault backup: 2026-06-05 01:30:42`

**Critical files present (8/8):**
- `corpus/corpus-data.json` ✓
- `data/processed/records.jsonl` ✓
- `data/processed/purification.jsonl` ✓
- `tese/manuscrito/Introducao_rev.md` ✓
- `README.md` ✓
- `AGENTS.md` ✓
- `CLAUDE.md` ✓
- `data/raw/drive-manifest.json` ✓

**Status:** Clean. No remediation needed. (Per skill pitfall #7: do not run `git restore .` blindly — the working tree has intentional Obsidian session churn.)

**Branch state note:** The active branch is `reconcile/ssd-scripts-2026-06-04`, not `main`. If the user is about to push, confirm which branch should receive the work. Per memory: "Push-to-main is gated."

---

## 4. STALE/DUPLICATE COPIES

| Location | Size | Last commit | Git remote | Status |
|----------|------|-------------|-----------|--------|
| `~/Research/hub/iconocracy-corpus/` (CANONICAL) | 1.3 GB (905 MB non-git) | `72d560d` 2026-06-05 01:30 | `ssd-mirror` only (no `origin` — intentional, see below) | Active |
| `~/projetos/research/hub/iconocracy-corpus/` | **596 MB** | `9be98bb` 2026-05-24 20:54 | `git@github.com:anavvanzin/iconocracy-corpus.git` | **Stale clone, pre-reorganization** |
| `~/Documents/GitHub/iconocracy-corpus/` | **575 MB** | `cc094f4` 2026-05-30 17:17 | `https://github.com/anavvanzin/iconocracy-corpus.git` | **Stale clone, GitHub Desktop** |
| `~/Projects/iconocracy-corpus/` | — | — | — | **Does not exist** (already cleaned up since April audit) |
| `~/Downloads/atlas-iconocratico-toolkit/iconocracy-corpus/` | — | — | — | **Does not exist** (already cleaned up since April audit) |
| `~/.gemini/{history,tmp}/iconocracy-corpus` | 120K / 92K | — | — | Tool runtime caches, not real repos |
| `~/.claude/ck/contexts/iconocracy-corpus` | 8 KB | — | — | Tool runtime cache |
| `~/.hermes/plugins/iconocracy-corpus` | 32 KB | — | — | Hermes plugin metadata |

**Note on canonical repo remotes:** `git remote -v` shows only `ssd-mirror` (push/fetch to `/Volumes/ICONOCRACIA/git-mirrors/iconocracy-corpus.git`), no `origin`. The two duplicate clones have `origin` pointing to GitHub. The canonical was deliberately reconfigured to push to the local mirror, not GitHub. This is consistent with the SSD-consolidation plan but should be re-verified if/when the SSD is back online.

**Risk:** Confusion about authoritative copy; ~1.17 GB of wasted disk space. Neither duplicate is referenced by active configs.

**Recommendation:** Archive or delete both duplicates after confirming no local work is in them. Per skill pitfall #5: check their README first to confirm they're snapshots, not standalone toolkits.

```bash
# Verify they're snapshots, not work-in-progress:
cd ~/projetos/research/hub/iconocracy-corpus && git log --oneline | head -3
cd ~/Documents/GitHub/iconocracy-corpus && git log --oneline | head -3

# If both are confirmed stale (no unique commits beyond what's in canonical):
tar -czf ~/archive/dup-iconocracy-corpus-projetos-$(date +%Y%m%d).tar.gz -C ~/projetos/research/hub iconocracy-corpus
tar -czf ~/archive/dup-iconocracy-corpus-gh-$(date +%Y%m%d).tar.gz -C ~/Documents/GitHub iconocracy-corpus
rm -rf ~/projetos/research/hub/iconocracy-corpus
rm -rf ~/Documents/GitHub/iconocracy-corpus
```

**Decision:** defer to user — this is a destructive cleanup.

---

## 5. OTHER SCATTERED REFERENCES

**Historical (informational only — no action required):**

These are in archived documents and are expected to exist as audit/sprint history:

- `Research/doc1s/ULTRAPLAN-2026-04-16.md` and `doc1s/superpowers/audit/2026-04-17/2.2-architecture.md` — pre-reorganization architecture notes (correctly state old path; kept for historical accuracy)
- `Research/LLM Skills/Text/memory.md` lines 21, 23, 24 — pre-reorganization knowledge architecture (still has `~/iconocracy-corpus/` form); this is a snapshot file, not active config
- `Research/LLM Skills/Text/ARGOS_*` — prompt audit trails from April
- `Research/Plans/2026-04-25-workspace-dependency-audit.md` — the April 2026 audit report itself (references old state)
- `Research/Research/2026-04-17-research-workspace-full-audit.md`, `Research/Research/2026-04-23-research-audit-remediation.md` — earlier audit records

**Status:** All in archived/historical directories; no live tool depends on these paths. **No action required.**

---

## 6. PATH EXPECTATIONS FROM RESEARCH/PATHS/

`Research/Paths/paths-1.1.txt` (70 lines), `paths-1.2.txt` (53 lines), `paths-1.3.txt` (44 lines) enumerate expected tool locations. **All paths point to `/Users/ana/Research/hub/iconocracy-corpus/...`** which resolves correctly.

**Sample validation (25 of 167 total):** 25/25 present. No action required.

---

## REMEDIATION PRIORITY

| Priority | Action | File(s) / Location | Notes |
|----------|--------|-------------------|-------|
| **P3 (low)** | Resolve dangling `~/Research/iconocracy-corpus` symlink | `~/Research/iconocracy-corpus` | Either remove it, re-point to internal-disk canonical, or wait for SSD remount. **Ask user.** |
| **P3 (low)** | Archive/delete stale duplicate clones | `~/projetos/research/hub/iconocracy-corpus` (596 MB), `~/Documents/GitHub/iconocracy-corpus` (575 MB) | Verify no unique commits first; ~1.17 GB recoverable. **Ask user.** |
| **P3 (low)** | Confirm canonical repo remotes after SSD remount | `~/Research/hub/iconocracy-corpus` | When `/Volumes/ICONOCRACIA` returns, verify `ssd-mirror` is still wired. If not, decide whether `origin` (GitHub) should be re-added. |
| **P3 (low)** | Note active branch in any push workflow | `~/Research/hub/iconocracy-corpus` | Currently on `reconcile/ssd-scripts-2026-06-04`, not `main`. Pushes to main are gated; confirm target branch before any commit/push. |

**No P0/P1/P2 issues found.** The April 2026 audit's P0 (`~/iconocracy-corpus` symlink, `.claude.json` stale entry) and P1 (documentation paths) have all been resolved.

---

## ONE-LINE FIX PROPOSAL

```bash
# OPTIONAL cleanup — ask user before running:

# 1. Resolve the dangling SSD symlink (3 options):
#    a) remove it:
rm /Users/ana/Research/iconocracy-corpus
#    b) re-point to the live canonical:
rm /Users/ana/Research/iconocracy-corpus && ln -s /Users/ana/Research/hub/iconocracy-corpus /Users/ana/Research/iconocracy-corpus
#    c) leave it for SSD remount

# 2. Archive stale duplicate clones (verify first, then archive):
mkdir -p /Users/ana/archive/dup-corpus-2026-06-05
tar -czf /Users/ana/archive/dup-corpus-2026-06-05/projetos-$(date +%Y%m%d).tar.gz -C /Users/ana/projetos/research/hub iconocracy-corpus
tar -czf /Users/ana/archive/dup-corpus-2026-06-05/github-$(date +%Y%m%d).tar.gz -C /Users/ana/Documents/GitHub iconocracy-corpus
# (only remove after confirming archives)
```

---

## AUDIT METHODOLOGY

- Ran six phases per the skill spec: structure discovery, symlink/path audit, cross-reference validation, duplicate detection, legacy symlink completion, working-tree integrity check
- Verified symlink resolution with `readlink` and `[ -L ... ]` checks
- Cross-checked `.claude.json` for stale project entries and dangerous hook patterns
- Inspected `git status` and `git remote -v` on canonical and duplicate repos
- Validated 25/167 paths in `Research/Paths/paths-1.1.txt` (representative sample)
- Excluded `node_modules/`, `.git/`, `.venv/`, `Library/`, `markitdown/`, `hermes-agent/`, `hermes-workspace/`, `.hermes/sessions/` from recursive content scans (per skill pitfall #6)
- Did not modify any files; this audit is observational

**Limitations:**
- Skipped networked home directories (`~/Library/CloudStorage/GoogleDrive*`) and `.hermes/sessions/*.json` archives (read-only history)
- One `find` command timed out at 60s; switched to targeted `grep` calls for active-config checks
- Did not validate binary files or compiled artifacts

**Date verification:** Conversation started 2026-06-05. Reference doc `ssd-consolidation-2026-06-04.md` describes state as of June 4 — current state matches the plan's intent for the on-disk canonical, but the SSD consolidation is **not currently live** (volume unmounted).

---

**Report generated by Hermes Agent** — iconocracy-workspace-dependency-audit session, 2026-06-05
