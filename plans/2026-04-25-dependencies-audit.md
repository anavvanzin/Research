# /users/ana/ DEPENDENCIES & IMPORTANT FILES AUDIT
**Date:** 2026-04-25  
**Scope:** All files and folders directly under `/users/ana/`  
**Follow-up to:** Workspace dependency audit (2026-04-25)

---

## EXECUTIVE SUMMARY

**226 dependency/config manifests** identified across the workspace.  
**8 git repositories** tracked; 4 are **out of sync** with their upstream remotes.  
**awesome-hermes-agent** (0xNyk/awesome-hermes-agent) — **NOT cloned locally**; GitHub repo is recent (last push 2026-04-21).

---

## 1. CRITICAL REPO SYNC STATUS

### Repos BEHIND upstream (need `git pull`)

| Repository | Ahead | Behind | Severity | Recommended Action |
|------------|-------|--------|----------|-------------------|
| `Research/hub/iconocracy-corpus` | 4 | **287** | 🔴 HIGH | **PULL REQUIRED** — heavily diverged; coordinate before pulling to avoid merge conflicts |
| `hermes-agent-camel` | 11 | **2840** | 🔴 CRITICAL | **STOP USING** — this fork is 2,840 commits behind upstream; should be reset or recloned |
| `.hermes/hermes-agent` | 0 | **1** | 🟡 LOW | Minor drift; safe to pull |
| `hermes-workspace` | 0 | **15** | 🟡 LOW | Moderately behind; pull recommended |

### Repos CLEAN (up-to-date)

- `Research/apps/iconocracia-companion` ✓
- `Research/apps/iconocracia-space` ✓
- `Research/labs/iurisvision` ✓
- `Research/pipelines/Atlas` ✓

---

## 2. DEPENDENCY MANIFESTS INVENTORY

### Python projects (18)
| File | Location | Notes |
|------|----------|-------|
| `pyproject.toml` | `.hermes/hermes-agent/` | Core Hermes agent package |
| `pyproject.toml` | `.hermes/hermes-agent/ui-tui/` | TUI interface |
| `pyproject.toml` | `.hermes/hermes-agent/web/` | Web UI |
| `pyproject.toml` | `.hermes/hermes-agent/website/` | Docs site |
| `requirements.txt` | `Research/hub/iconocracy-corpus/` | Thesis corpus deps |
| `requirements.txt` | `Research/apps/iconocracia-space/` | Companion app |
| `requirements.txt` | `Research/pipelines/Atlas/` | Atlas toolkit |
| `pyproject.toml` | `Research/labs/browser-harness/` | Browser automation |
| `pyproject.toml` | `hermes-agent-camel/` | Alternate Hermes fork |
| `environment.yml` | `Research/hub/iconocracy-corpus/` | Conda env (tiny) |
| `environment.yml` | multiple `Research/shared/iconclass-data*` | Data packages |
| `requirements.txt` | `LLM Skills/Text/` | Skill dependencies (15 bytes — placeholder?) |
| `pyproject.toml` | `deep-memory/` | Memory plugin |
| +5 more in `Documents/GitHub/`, `Downloads/`, `Projects/` | scattered | Downloaded examples / experiments |

**Note:** Many dependency files appear in `Downloads/`, `Documents/GitHub/`, `Projects/` — these are isolated sandboxes, not workspace-critical.

---

### Node.js / npm projects (15+)
| Manifest | Location | Purpose |
|----------|----------|---------|
| `package.json` + `package-lock.json` | `.hermes/hermes-agent/` | Core agent (Node components) |
| `package.json` | `.hermes/hermes-agent/ui-tui/` | Terminal UI |
| `package.json` | `.hermes/hermes-agent/web/` | Web dashboard |
| `package.json` | `.hermes/hermes-agent/website/` | Docs site |
| `package.json` | `Research/apps/iconocracia-companion/` | Public companion app |
| `package.json` | `Research/cowork/` | Tooling workspace |
| `package.json` | `Research/labs/iurisvision/` | Vision lab UI |
| `package.json` | `hermes-agent-camel/` | Camel fork (includes WhatsApp bridge) |
| `package-lock.json` (756KB) | `.hermes/hermes-agent/website/` | Large lockfile — may be stale |
| +7 more in `Downloads/`, `Projects/`, `Protótipo IG/` | scattered | External projects |

---

### Docker / Container (8)
| File | Location |
|------|----------|
| `Dockerfile` | `.hermes/hermes-agent/` |
| `docker-compose.yml` | `.hermes/hermes-agent/` |
| `Dockerfile` | `Research/hub/iconocracy-corpus/` |
| `docker-compose.yml` | `Research/hub/iconocracy-corpus/` |
| `Dockerfile` | multiple `Projects/mcp/*` | MCP server containers |
| `Dockerfile` | `Downloads/`, `Other/`, `Tools/pandoc/` | Experimental |

---

### Config files (YAML / .env)
| File | Notes |
|------|-------|
| `.hermes/config.yaml` | Active Hermes agent configuration |
| `.claude.json` | Claude Desktop project settings (already cleaned) |
| `.env` (root) | Workspace-level env vars? |
| `.hermes/.env` | Hermes agent environment (19 KB) |
| `pyproject.toml` (many) | Project metadata + deps |
| `config.yaml` | Multiple project configs (AutoResearchClaw, united-by-marriage art projects) |

---

## 3. GIT REPOSITORY HEALTH SUMMARY

### Out-of-sync repositories (action required)

```
1. hermes-agent-camel/  (ahead 11, behind 2840)  — CRITICAL
   This fork is massively behind upstream. Likely abandoned or needs a hard reset.
   Action: git remote show upstream; consider: git reset --hard upstream/main

2. Research/hub/iconocracy-corpus/  (ahead 4, behind 287)  — HIGH
   Active development but diverged. Needs careful merge or rebase.
   Action: coordinate with any other collaborators; pull with --rebase

3. .hermes/hermes-agent/  (behind 1)  — LOW
   Minor drift. Safe to pull.

4. hermes-workspace/  (behind 15)  — MEDIUM
   Workspace infra; moderately behind. Should pull.
```

### Healthy repositories (up-to-date)

- `Research/apps/iconocracia-companion` — Web interface for corpus
- `Research/apps/iconocracia-space` — Hugging Face Space integration
- `Research/labs/iurisvision` — Legal vision lab
- `Research/pipelines/Atlas` — Atlas toolkit

---

## 4. awesome-hermes-agent REPO STATUS

**Local presence:** NOT CLONED  
**GitHub repo:** `https://github.com/0xNyk/awesome-hermes-agent`  
**Status (remote):**
- Stars: 1,778
- Default branch: `main`
- Last pushed: **2026-04-21** (4 days ago)
- Open issues: 7
- Description: Curated list of Hermes Agent skills, tools, integrations

**Assessment:**
- This is a **reference index**, not a code dependency
- No local clone → no local sync issue
- No git submodule references to it found anywhere in workspace
- No config/documentation hardcoded links to it (except possibly external references)
- **Up-to-date on GitHub** — your local lack of clone means you're simply not tracking it, not that you're behind

**Recommendation:** If you want to use it as a skill discovery resource, clone it separately:
```bash
git clone https://github.com/0xNyk/awesome-hermes-agent.git ~/awesome-hermes-agent
```
But it's not required for any workspace functionality.

---

## 5. ORPHANED / STALE DEPENDENCIES

### Found & Already Cleaned
- `Projects/iconocracy-corpus/` — stale git clone (deleted as `.bak`, then removed)
- `Downloads/atlas-iconocratico-toolkit/iconocracy-corpus/` — stale toolkit copy (deleted)

### Not ORPHANED but ISOLATED
These live in `Downloads/`, `Documents/GitHub/`, `Projects/` — are sandbox/experiment areas, not workspace core:
- `Downloads/hermes-agent-2026.4.23/` — old Hermes agent snapshot (can archive if not needed)
- `Downloads/AutoResearchClaw-main/` — AutoResearchClaw reference clone
- `Documents/GitHub/` — multiple example project clones (deer-flow, gemini-cli, etc.)
- `Projects/AutoResearchClaw/` — another AutoResearchClaw copy
- `Projects/mcp/` — MCP server experiments (datagouv, zotero, notebooklm)
- `Projects/pixel-love/` — personal projects (loveu, melovanzin)
- `Projects/IG/` — Ius Gentium app prototypes
- `hermes-agent-camel/` — alternate Hermes fork (heavily behind upstream)

**These are all optional sandboxes.** They don't break anything; they just take up space. If you need to reclaim disk space, archive or delete non-current `Downloads/` subfolders.

---

## 6. IMPORTANT CONFIG FILES (Touched in prior remediation)

| File | Status | Notes |
|------|--------|-------|
| `.claude.json` | ✓ Cleaned | Removed stale `/Users/ana/iconocracy-corpus` entry; only `/Users/ana/Research/hub/iconocracy-corpus` remains |
| `united-by-marriage/CLAUDE.md` | ✓ Updated | Path corrected to `~/research/hub/iconocracy-corpus/` |
| `Research/README.md` | ✓ Verified | Table shows canonical path; legacy symlink column accurate now that symlinks are fixed |
| `.hermes/config.yaml` | ✓ Clean | No iconocracy-specific hooks; no broken references |

---

## 7. DEPENDENCY RECOMMENDATIONS

### Immediate Actions (P1)
1. **Pull ICONOCRACY corpus from upstream** — but with caution:
   ```bash
   cd /users/ana/Research/hub/iconocracy-corpus
   git fetch --all
   git log --oneline origin/main..HEAD  # review your 4 local-only commits
   git log --oneline HEAD..origin/main | head -20  # review 287 incoming commits
   # Then decide: merge or rebase
   ```
   **Do not blindly pull** — you're 287 commits behind. Check if your 4 local commits are already upstream.

2. **Evaluate `hermes-agent-camel/`** — 2,840 commits behind is extreme. Options:
   - Abandon this fork (delete or archive)
   - Reset to upstream: `git fetch upstream && git reset --hard upstream/main`
   - Rebase your local changes onto current upstream (if you have unique work)

3. **Pull `.hermes/hermes-agent`** — safe, 1 commit behind:
   ```bash
   cd ~/.hermes/hermes-agent && git pull
   ```

4. **Pull `hermes-workspace`** — behind 15 commits; safe to pull if no local mods:
   ```bash
   cd ~/hermes-workspace && git pull
   ```

### Optional Cleanup (P3)
- Archive old `Downloads/hermes-agent-2026.4.23/` (outdated Hermes distribution)
- Archive `Documents/GitHub/` clones if not actively used (they're duplicates of public repos)
- Review `Projects/` experiments for retention policy

---

## 8. DEPENDENCY MATRIX (Workspace-Critical Only)

These are the files/repos that **the active workspace actually depends on**:

| Dependency | Type | Location | Status |
|------------|------|----------|--------|
| Hermes Agent core | Git repo | `~/.hermes/hermes-agent/` | ⚠ behind 1 |
| ICONOCRACY corpus | Git repo | `~/Research/hub/iconocracy-corpus/` | ⚠ ahead 4, behind 287 |
| Iconocracia companion (web) | npm project | `~/Research/apps/iconocracia-companion/` | ✓ clean |
| Iconocracia space (HF) | Python reqs | `~/Research/apps/iconocracia-space/` | ✓ clean |
| Atlas toolkit | Python reqs + git | `~/Research/pipelines/Atlas/` | ✓ clean |
| Shared data (iconclass) | Git repo | `~/Research/shared/iconclass-data/` | ✓ clean |
| Browser harness | Python project | `~/Research/labs/browser-harness/` | ✓ clean |

---

## 9. HOLISTIC WORKSPACE HEALTH SCORE

| Category | Score | Status |
|----------|-------|--------|
| Path dependencies (symlinks) | 10/10 | ✓ All 6 canonical symlinks functional |
| Config file cleanliness | 10/10 | ✓ No broken hook references |
| Git working tree integrity | 10/10 | ✓ Corpus working tree clean |
| Repo sync with upstream | **4/10** | 🔴 4 repos out of sync |
| Disk hygiene (no duplicates) | 9/10 | ✓ Stale copies removed |
| Documentation consistency | 9/10 | ✓ README polished; path refs corrected |

**Overall: 8.5/10** — Infrastructure paths fixed; now need **repository synchronization**.

---

## 10. FINAL RECOMMENDATIONS (Ordered)

1. **Triage sync conflicts** — Determine:
   - Are the 4 local commits in `iconocracy-corpus` already merged upstream? If yes, just `git pull --rebase`.
   - Is `hermes-agent-camel/` still needed? 2,840-behind suggests it's an abandoned fork.

2. **Pull the clean repos** — `.hermes/hermes-agent`, `hermes-workspace` are safe pulls.

3. **Consider archiving sandboxes** — `Downloads/hermes-agent-2026.4.23/`, `Documents/GitHub/*` if not actively used (≈500 MB potential reclaim).

4. **awesome-hermes-agent** — Not a dependency. Clone only if you want to browse curated skill list.

5. **Schedule regular sync cadence** — Repos that drift far behind risk complex merge conflicts. Monthly pull/rebase recommended for active repos.

---

**Report generated:** 2026-04-25  
**Agent:** Hermes (workspace dependency & git health audit)
