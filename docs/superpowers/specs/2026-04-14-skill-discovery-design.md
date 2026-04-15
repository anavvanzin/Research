# Skill Discovery — Path Z (Catalog + Finder)

**Date:** 2026-04-14
**Status:** Design approved, pending implementation plan
**Owner:** Ana Vanzin
**Problem slice:** Claude Code workflow — skills sprawl (B5: discovery).

## Problem

Hundreds of skills are installed across `~/.claude/skills/` and plugin caches. Some are project-scoped (thesis-only), others global. When a task starts, the right skill often exists but is hard to locate in a flat list. User wanted **both** filter-by-project-scope *and* a global query escape hatch (Path Z).

## Goal

Make Claude prefer the right skills per project without hiding the global set, and give the user a fuzzy-search way to find any skill by intent.

## Non-goals

- Hiding skills or disabling plugins.
- Auto-generating catalogs from skill frontmatter.
- ML-based ranking.
- Restructuring where skills live on disk.

## Approach A — Curated catalog in CLAUDE.md + `/find-skill` skill

### Component 1 — Catalog block in CLAUDE.md

Each in-scope `CLAUDE.md` ends with a `## Skills for this workspace` section containing a curated, human-maintained list. Claude reads these as authoritative preference hints; global skills remain available.

Canonical block shape (example: thesis hub):

```markdown
## Skills for this workspace

Curated skills Claude should prefer here. Global + finder still apply.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `iconocracy-agent` | Default umbrella for thesis research |
| `compilar-tese` | Direct thesis compile (DOCX/PDF) |
| `validate-corpus` | Quick schema check after editing `corpus-data.json` |

### Branches (when bypassing the agent)
- `corpus-scout` · `iconocode-analyze` · `iconocode-batch` · `thesis-progress` · `citation-management` · `dir410346`

### Review agents (subagent dispatch)
- `abnt-checker` · `thesis-reviewer` · `chapter-integrity` · `iconclass-reviewer` · `iconocode` · `corpus-dedup`
```

Rules:
- Max ~10 top-table entries per file — forces curation.
- Always last section in CLAUDE.md so it's easy to grep.
- `Skill ID` column uses the exact string passed to the `Skill` tool.
- Entries marked `(agent)` use `Agent` tool dispatch.
- When a primary entry point is an umbrella (like `iconocracy-agent`), list branches as a compact one-liner below; don't duplicate them in the main table.

### Component 2 — `/find-skill` meta-skill

New skill at `~/.claude/skills/find-skill/SKILL.md`.

- **Input:** natural-language intent string. Optional scope tag (`--scope=thesis|dev|writing|global`).
- **Behavior:**
  1. Scan `name` + `description` frontmatter under `~/.claude/skills/` and plugin caches.
  2. Score by term overlap with intent, boosted by cwd heuristic: cwd inside `~/Research/hub` → boost entries already in the hub catalog; cwd inside `~/Research/apps/*` → boost dev/frontend entries; no boost otherwise.
  3. Return top 3 matches: `skill-id` + one-line description + one-line "why it matched".
- **Implementation:** pure ripgrep + simple in-memory scoring, no DB, no ML.
- **Fallback:** if no match scores above threshold, return 5 closest + message "no strong match; these are nearest."

### Component 3 — Catalogs to seed (phase 1)

1. `~/.claude/CLAUDE.md` — cross-cutting always-on skills.
   Proposed entries: `find-skill`, `context7-mcp`, `plan`, `commit`, `caveman`, `research`, `academic-research-skills`, `self-improvement`.
2. `~/Research/CLAUDE.md` — workspace entry points.
   Proposed entries: `iconocracy-agent`, `find-skill`, `academic-research-skills`, `literature-review`, `compilar-tese`.
3. `~/Research/hub/iconocracy-corpus/CLAUDE.md` — full thesis catalog per shape above.
4. `~/Research/apps/iconocracia-companion/CLAUDE.md` — app-dev catalog.
   Proposed entries: `frontend-design`, `context7-mcp`, `playwright`, `code-review`, `find-skill`, plus any firebase-related skills in the inventory.

Other sub-repos (webiconocracy, Atlas, iurisvision, indexing) get catalogs on demand, not now.

## Data flow

```
Session starts at cwd=X
  └─ Claude loads CLAUDE.md chain (X and ancestors, plus user-global)
     └─ "Skills for this workspace" blocks bias skill selection
Ana issues a task
  ├─ Claude picks from catalog if a match exists
  └─ If uncertain → Ana invokes /find-skill "<intent>" → top 3 returned
```

## Error handling

- Catalog lists a skill that no longer exists → the `find-skill` skill, when called, reports the stale entry; Ana prunes manually.
- Two catalogs in the chain list the same skill → no conflict, duplicates ignored.
- `find-skill` returns zero matches → fallback prints nearest 5.

## Testing

Manual acceptance checks, no automated suite:

1. Open session at `~/Research/hub/iconocracy-corpus`. Ask "what skills here?". Expect Claude to cite the catalog.
2. Run `/find-skill "validate corpus"`. Expect `validate-corpus` in top 3.
3. Open session at `~/Research/apps/iconocracia-companion`. Ask for a skill to review a React component. Expect `frontend-design` / `code-review` cited over thesis skills.
4. Edit `~/.claude/CLAUDE.md` catalog, remove a skill, reopen session — verify Claude no longer proposes it first.

## Maintenance

- When a new skill becomes relevant, edit the appropriate CLAUDE.md catalog. Manual, deliberate.
- No sync script, no auto-regen. Drift tolerable because `/find-skill` covers gaps.

## Out of scope (revisit later)

- SessionStart hook to auto-inject recommended skills (Approach B). Re-evaluate if manual curation becomes burdensome.
- Scoping by git branch, not just path.
- Machine-readable skill tags in frontmatter.
