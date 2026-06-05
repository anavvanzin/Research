# ICONOCRACY WORKSPACE — DEPENDENCY AUDIT REPORT
**Date:** 2026-04-25  
**Audited root:** /users/ana/  
**Canonical corpus location:** /users/ana/research/hub/iconocracy-corpus  (1,041 MB, 1,084 tracked files)

---

## EXECUTIVE SUMMARY

The `/users/ana/` home directory has several broken dependencies pointing to a non-existent `~/iconocracy-corpus/` path. The actual thesis corpus lives at `~/research/hub/iconocracy-corpus/` (lowercase `research` on macOS case-insensitive FS, aliased as capital `Research/`).

**Severity:** HIGH — broken path references cause tool failures and incorrect documentation.

**Key issues:**
1. Missing top-level symlink `/users/ana/iconocracy-corpus` (expected by multiple configs)
2. Hardcoded broken paths in `.claude.json` and `united-by-marriage/CLAUDE.md`
3. Working tree corruption in the canonical corpus (many tracked files missing from disk)
4. Stale/duplicate corpus copies in `Projects/` and `Downloads/` (29–30 MB each, independent git repos)

---

## 1. STRUCTURE OVERVIEW

```
/users/ana/
├── research/       ← ACTIVE workspace (lowercase; case-insensitive alias: Research/)
│   ├── hub/
│   │   └── iconocracy-corpus/    ← CANONICAL THESIS REPO (1,084 tracked files, 1,041 MB)
│   ├── labs/
│   ├── vaults/
│   ├── pipelines/
│   └── README.md                  ← Defines expected layout
├── iconocracy-corpus  [MISSING — SHOULD BE SYMLINK → research/hub/iconocracy-corpus]
├── .claude.json      ← Claude Desktop config — references MISSING path
├── united-by-marriage/
│   └── CLAUDE.md     ← Says codebase at ~/iconocracy-corpus/ (WRONG)
├── Projects/
│   └── iconocracy-corpus/   ← STALE COPY (29.7 MB, independent git repo)
└── Downloads/
    └── atlas-iconocratico-toolkit/
        └── iconocracy-corpus/   ← STALE COPY (30.3 MB, independent git repo)
```

**Filesystem note:** `research/` and `Research/` are the SAME directory (inode 72484221, macOS case-insensitive FS).

---

## 2. CRITICAL BROKEN DEPENDENCIES

### 2.1 MISSING SYMLINK — `/users/ana/iconocracy-corpus`

**Impact:** High — tools, scripts, and documentation expect the old path.

**What:** The top-level symlink `~/iconocracy-corpus` does NOT exist but is referenced by:
- `.claude.json` (lines 611–620): project config for `/Users/ana/iconocracy-corpus`
- `united-by-marriage/CLAUDE.md` line 60: documentation says codebase at `~/iconocracy-corpus/`
- Various Hermes session logs (historical references)

**Correct target:** `/users/ana/research/hub/iconocracy-corpus`

---

### 2.2 BROKEN PATHS IN `.claude.json`

**File:** `/users/ana/.claude.json`  
**Lines with broken `/Users/ana/iconocracy-corpus` references:** 27, 31, 46–50, 82

**Excerpt of broken references:**

| Line | Context |
|------|---------|
| 27 | `Edit(/Users/ana/iconocracy-corpus)` |
| 31 | `Write(/Users/ana/iconocracy-corpus)` |
| 46–50 | `Bash(rm -rf /Users/ana/iconocracy-corpus*...)` (4 lines) |
| 82 | `validate_schemas.py` hardcoded `cd /Users/ana/iconocracy-corpus && python ...` |

**Contrast:** Line 806 correctly references `/Users/ana/Research/hub/iconocracy-corpus` — the working project config exists alongside a stale broken one.

**Recommended fix:** Either:
- **Option A (preferred):** Create the symlink `~/iconocracy-corpus → ~/research/hub/iconocracy-corpus` so both paths resolve correctly, OR
- **Option B:** Remove the stale entry (lines 611–620) and update broken hooks to use the correct Research/hub path.

---

### 2.3 OUT-OF-DATE DOCUMENTATION

**File:** `/users/ana/united-by-marriage/CLAUDE.md` (line 60)  
**Text:** `- The PhD thesis codebase is at \`~/iconocracy-corpus/\`.`  
**Issue:** Path is stale; should be `~/research/hub/iconocracy-corpus/` or `~/Research/hub/iconocracy-corpus/`

**File:** `/users/ana/Research/README.md` (table at line 40)  
Shows both `/Users/ana/Research/hub/iconocracy-corpus` (correct) AND `/Users/ana/iconocracy-corpus` (should be symlink, not canonical). The README is internally inconsistent.

---

## 3. CORPUS WORKING TREE CORRUPTION

**Location:** `/users/ana/research/hub/iconocracy-corpus`

The git repository has many **tracked but missing** files (marked `D` in `git status`), meaning they were deleted from disk but not committed.

**Sample missing-but-tracked files:**
- `corpus/corpus-data.json`  (canonical corpus source)
- `data/processed/records.jsonl`
- `data/processed/purification.jsonl`  (not even tracked — might be generated)
- `tese/manuscrito/Introducao_rev.md`
- `vault/tese/capitulo-1.md`
- `README.md`

**Status:** `git status` shows ~150+ deleted files. This breaks any tool depending on the corpus being complete.

**Likely cause:** Accidental `git rm` without committing; or a mass-cleanup that removed generated/intermediate files without distinguishing tracked vs untracked.

**Recommended fix:** Run `git restore .` from the corpus root to restore all tracked files from HEAD. Verify before committing anything.

---

## 4. STALE/DUPLICATE COPIES

Two full copies of the corpus exist outside the canonical location. They are **independent git repositories** (~30 MB each) and likely out of sync.

| Location | Size | Git repo? | Status |
|----------|------|-----------|--------|
| `~/Projects/iconocracy-corpus/` | 29.7 MB | YES | Independent repo — probable legacy snapshot |
| `~/Downloads/atlas-iconocratico-toolkit/iconocracy-corpus/` | 30.3 MB | YES | Independent repo — probable toolkit bundle |

**Risk:** Confusion about which copy is authoritative; edits in one won't propagate to others.

**Recommended action:** Decide whether these are intentional backups/toolkits. If not needed, archive them (e.g., tar + gzip) and remove the directories. If they're meant to mirror the main repo, replace them with **symlinks** to `~/research/hub/iconocracy-corpus`.

---

## 5. OTHER SCATTERED REFERENCES

Many files reference `iconocracy-corpus` in text (Hermes session logs, skill snapshots, chat history archives). These are **non-executable** references and don't cause breakage, but indicate historical path usage. No action needed.

---

## 6. MISSING UTILITY SCRIPTS

These files are expected but not found (may be intentional if they're user-created convenience scripts):

- `~/.zshenv` — missing (optional shell init)
- `hermes-setup` — missing (optional Hermes setup script)
- `hermes-setup-tools` — missing (optional Hermes tools script)

---

## 7. PATH EXPECTATIONS FROM RESEARCH/PATHS/

`Research/Paths/paths-1.1.txt` and `paths-1.3.txt` enumerate expected tool locations. All paths point to `/Users/ana/Research/hub/iconocracy-corpus/...` (capital `Research`), which is **the same directory** as lowercase `research/` on this macOS system. No action required — paths resolve correctly once the base directory is addressed.

---

## REMEDIATION PRIORITY

| Priority | Action | File(s) |
|----------|--------|---------|
| **P0 (critical)** | Create symlink `~/iconocracy-corpus → ~/research/hub/iconocracy-corpus` so broken paths resolve | `/users/ana/iconocracy-corpus` |
| **P0** | Restore missing tracked files in corpus (`git restore .`) | `~/research/hub/iconocracy-corpus/` |
| **P1 (high)** | Fix `.claude.json`: remove stale project entry or ensure it points to correct path | `/users/ana/.claude.json` (lines 611–620 and hook lines) |
| **P1** | Correct documentation in `united-by-marriage/CLAUDE.md` | `united-by-marriage/CLAUDE.md` line 60 |
| **P2 (medium)** | Reconcile `Research/README.md` table to show symlink destination consistently | `Research/README.md` |
| **P3** | Archive or delete stale duplicate copies (`Projects/`, `Downloads/atlas-iconocratico-toolkit/`) | `Projects/iconocracy-corpus`, `Downloads/atlas-iconocratico-toolkit/iconocracy-corpus` |
| **P3** | Optionally create missing shell utility scripts if they were intended | `.zshenv`, `hermes-setup`, `hermes-setup-tools` |

---

## ONE-LINE FIX PROPOSAL

To resolve P0+P1 immediately:

```bash
# 1. Create the expected symlink
ln -s /users/ana/research/hub/iconocracy-corpus /users/ana/iconocracy-corpus

# 2. Restore corpus working tree
cd /users/ana/research/hub/iconocracy-corpus && git restore .

# 3. Fix .claude.json — either remove the stale entry or update tool hooks
#    (requires JSON edit; see line references above)

# 4. Fix united-by-marriage doc
sed -i '' "s|~/iconocracy-corpus/|~/research/hub/iconocracy-corpus/|g" united-by-marriage/CLAUDE.md
```

---

## AUDIT METHODOLOGY

- Scanned `/users/ana/` recursively for `iconocracy-corpus` path references (limited to .md, .py, .sh, .json, .yaml, .txt, .conf)
- Verified git status of canonical corpus (`research/hub/iconocracy-corpus`)
- Cross-checked path expectations against `Research/README.md` and `Research/Paths/*.txt`
- Identified duplicate copies via size and `.git` presence
- Confirmed `research/` and `Research/` refer to the same inode on macOS APFS case-insensitive volume.

---

**Report generated by Hermes Agent** — workspace dependency audit session
