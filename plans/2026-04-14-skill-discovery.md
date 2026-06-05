# Skill Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Seed curated skill catalogs into four CLAUDE.md files and ship a `find-skill` meta-skill, so Claude prefers the right skill per project and Ana can fuzzy-search by intent.

**Architecture:** Docs-only changes (catalog blocks in four CLAUDE.md) plus one new instructional skill at `~/.claude/skills/find-skill/SKILL.md`. No code scripts, no hooks. Claude uses its own `Grep`/`Read` to execute the finder when the skill is invoked.

**Tech Stack:** Markdown. Claude Code skill system (SKILL.md frontmatter).

**Spec:** `~/Research/docs/superpowers/specs/2026-04-14-skill-discovery-design.md`

---

## File Structure

| File | Role |
| --- | --- |
| `~/.claude/skills/find-skill/SKILL.md` | New instructional skill that scans frontmatter and ranks by intent |
| `~/.claude/CLAUDE.md` | Add global cross-cutting catalog |
| `~/Research/CLAUDE.md` | Add workspace-level catalog |
| `~/Research/hub/iconocracy-corpus/CLAUDE.md` | Add full thesis catalog |
| `~/Research/apps/iconocracia-companion/CLAUDE.md` | Add app-dev catalog |

Each catalog sits at the very end of its file under `## Skills for this workspace`. `find-skill` is a single Markdown file; no scripts, no dependencies.

---

## Task 1: Create `find-skill` skill

**Files:**
- Create: `~/.claude/skills/find-skill/SKILL.md`

- [ ] **Step 1: Confirm no existing `find-skill` skill**

Run: `ls ~/.claude/skills/find-skill/ 2>/dev/null; find ~/.claude -maxdepth 6 -name find-skill 2>/dev/null`
Expected: empty / "No such file or directory".

- [ ] **Step 2: Create skill directory**

Run: `mkdir -p ~/.claude/skills/find-skill`
Expected: no output.

- [ ] **Step 3: Write `SKILL.md`**

Write file `~/.claude/skills/find-skill/SKILL.md` with content:

```markdown
---
name: find-skill
description: Fuzzy-search installed skills by intent and return the top 3 matches. Use when you know a skill probably exists for a task but can't recall its exact name. Input is a natural-language intent string; output is ranked ID + one-liner + why-it-matched. Biased by current working directory against per-project catalogs in CLAUDE.md.
---

# Find Skill

Search installed Claude Code skills by intent when the exact name is unknown.

## Trigger

Invoke when the user:
- Says "is there a skill for X", "find the skill that does X", "which skill...".
- Asks a question where the answer is probably "use skill Y" but Y isn't obvious.
- Types `/find-skill <intent>` directly.

## Procedure

1. **Parse the intent.** Strip filler ("the", "a", "skill that"); keep domain nouns/verbs.
2. **Collect candidates.** Use `Grep` over:
   - `~/.claude/skills/*/SKILL.md`
   - `~/.claude/plugins/cache/**/SKILL.md` (skim, do not exhaustively expand — use `Grep` with frontmatter patterns).
   Only read the frontmatter (lines between the two `---` delimiters).
3. **Score each candidate:**
   - +3 for each intent term that appears in `name`.
   - +1 for each intent term that appears in `description`.
   - +2 if the skill id is listed in the nearest `## Skills for this workspace` catalog (walk up from cwd through `CLAUDE.md` chain to `~/.claude/CLAUDE.md`).
   - -1 if the description starts with "Legacy slash-entry shim" (deprecated).
4. **Select top 3** by score; break ties by shorter skill id.
5. **Return** in this format:

   ```
   1. <skill-id> — <one-line description>
      why: <which intent terms matched + catalog-boost note>
   2. ...
   3. ...
   ```

   If top score < 2, add:
   > No strong match. Nearest candidates above; consider broader search or adding the skill to a catalog.

## Output rules

- Never return more than 3 primary matches. Fallback list may include up to 5 when the threshold fails.
- Do not invoke the matched skill — just report. The user chooses.
- If no candidates are found at all, say so plainly and suggest `~/.claude/skills/` may need seeding.

## Non-goals

- No indexing DB, no pre-computed scores — run the grep live each time.
- No cross-session caching.
- Do not edit or reorder skill files.
```

- [ ] **Step 4: Verify skill is discoverable**

Run: `ls ~/.claude/skills/find-skill/SKILL.md && head -5 ~/.claude/skills/find-skill/SKILL.md`
Expected: file exists; first non-empty line is `---` followed by `name: find-skill`.

- [ ] **Step 5: Smoke-test the frontmatter grep pattern**

Use the Claude Code `Grep` tool: pattern `^name: `, path `~/.claude/skills/corpus-scout/SKILL.md`.
Expected: returns the `name:` frontmatter line. Confirms the grep mechanism `find-skill` relies on at runtime works.

- [ ] **Step 6: Commit (if `~/.claude` is versioned)**

Run: `cd ~/.claude && git status -s 2>/dev/null | head -5 && git rev-parse --is-inside-work-tree 2>/dev/null`
If inside a git work tree:
```bash
cd ~/.claude
git add skills/find-skill/SKILL.md
git commit -m "feat(skills): add find-skill meta-skill for intent-based discovery"
```
If not a git repo, skip the commit and note in the session: "~/.claude not versioned; changes live on disk only."

---

## Task 2: Seed global catalog in `~/.claude/CLAUDE.md`

**Files:**
- Modify: `~/.claude/CLAUDE.md` (append new section at end)

- [ ] **Step 1: Read existing file tail**

Run: `tail -20 ~/.claude/CLAUDE.md`
Expected: confirm current ending (ideally last section `## Learnings Log`); capture the exact last line for use in Step 3's `Edit`.

- [ ] **Step 2: Confirm no prior catalog block exists**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/.claude/CLAUDE.md`.
Expected: no match.

- [ ] **Step 3: Append catalog via `Edit`**

Use the `Edit` tool on `~/.claude/CLAUDE.md`:
- `old_string`: the exact final 1–2 lines captured in Step 1.
- `new_string`: those same lines, followed by a blank line, then the block below.

Block to append:

```markdown

## Skills for this workspace

Curated cross-cutting skills Claude should prefer in any session. Global set still available; `find-skill` covers gaps.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `find-skill` | Fuzzy-search installed skills by intent when the exact name is unknown |
| `context7-mcp` | Fetch current library/framework docs before answering code questions |
| `plan` | Task breakdown + implementation planning for non-trivial work |
| `commit` | Structured git commit flow |
| `caveman` | Toggle ultra-compressed response style per session |

### Supporting skills
- `research` · `academic-research-skills` · `self-improvement` · `claude-md`
```

- [ ] **Step 4: Verify one match after edit**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/.claude/CLAUDE.md`, output_mode `count`.
Expected: count = 1.

- [ ] **Step 5: Commit (if versioned)**

Same pattern as Task 1 Step 6 but `git add CLAUDE.md` and message `docs(claude): seed global skill catalog`.

---

## Task 3: Seed workspace catalog in `~/Research/CLAUDE.md`

**Files:**
- Modify: `~/Research/CLAUDE.md` (append new section at end)

- [ ] **Step 1: Confirm no prior block**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/Research/CLAUDE.md`.
Expected: no match.

- [ ] **Step 2: Read last 10 lines to anchor the `Edit`**

Run: `tail -10 ~/Research/CLAUDE.md`
Expected: confirm file ends with the Conventions section's last bullet; capture the exact last line for `old_string`.

- [ ] **Step 3: Append catalog**

Use `Edit` with the anchor from Step 2. Append:

```markdown

## Skills for this workspace

Curated skills Claude should prefer when cwd is under `~/Research/`. Sub-repos add their own catalogs; this one covers the meta-workspace.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `iconocracy-agent` | Default umbrella for thesis research — orchestrates corpus, coding, compile, progress |
| `find-skill` | Fuzzy-search installed skills by intent |
| `academic-research-skills` | 13-agent deep-research suite (lit review, writing, peer review) |
| `literature-review` | Systematic literature reviews across multiple sources |
| `compilar-tese` | Compile thesis chapters to DOCX/PDF via Pandoc |
```

- [ ] **Step 4: Verify**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/Research/CLAUDE.md`, output_mode `count`.
Expected: count = 1.

- [ ] **Step 5: Commit if versioned**

Run: `cd ~/Research && git rev-parse --is-inside-work-tree 2>/dev/null`
If yes: `git add CLAUDE.md && git commit -m "docs(claude): seed workspace skill catalog"`.
Else: note uncommitted and move on.

---

## Task 4: Seed thesis catalog in `~/Research/hub/iconocracy-corpus/CLAUDE.md`

**Files:**
- Modify: `~/Research/hub/iconocracy-corpus/CLAUDE.md` (append)

- [ ] **Step 1: Confirm no prior block**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/Research/hub/iconocracy-corpus/CLAUDE.md`.
Expected: no match.

- [ ] **Step 2: Read file tail to anchor edit**

Run: `tail -20 ~/Research/hub/iconocracy-corpus/CLAUDE.md`
Expected: capture the exact last line for `old_string` in Step 3.

- [ ] **Step 3: Append catalog**

Use `Edit`. Append:

```markdown

## Skills for this workspace

Curated skills Claude should prefer inside the thesis hub. Global + `find-skill` still apply.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `iconocracy-agent` | Default umbrella — orchestrates corpus research, coding, compile, progress |
| `compilar-tese` | Direct thesis compile (DOCX/PDF) when bypassing the agent |
| `validate-corpus` | Quick schema check after editing `corpus/corpus-data.json` |

### Branches (when bypassing the agent)
- `corpus-scout` · `iconocode-analyze` · `iconocode-batch` · `thesis-progress` · `citation-management` · `dir410346`

### Review agents (subagent dispatch)
- `abnt-checker` · `thesis-reviewer` · `chapter-integrity` · `iconclass-reviewer` · `iconocode` · `corpus-dedup`
```

- [ ] **Step 4: Verify**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/Research/hub/iconocracy-corpus/CLAUDE.md`, output_mode `count`.
Expected: count = 1.

- [ ] **Step 5: Commit**

```bash
cd ~/Research/hub/iconocracy-corpus
git add CLAUDE.md
git commit -m "docs(claude): seed thesis-hub skill catalog"
```

---

## Task 5: Seed app catalog in `~/Research/apps/iconocracia-companion/CLAUDE.md`

**Files:**
- Modify: `~/Research/apps/iconocracia-companion/CLAUDE.md` (append)

- [ ] **Step 1: Confirm no prior block**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/Research/apps/iconocracia-companion/CLAUDE.md`.
Expected: no match.

- [ ] **Step 2: Spot-check candidate skills exist**

For each of `frontend-design`, `context7-mcp`, `playwright`, `code-review`, run a Claude Code `Grep`:
- pattern: `^name: <skill-id>$`
- path: `~/.claude` (let ripgrep walk; use glob `**/SKILL.md`)
- output_mode: `files_with_matches`

Expected: each returns at least one match. If any returns zero, drop that row from the catalog in Step 3 and note it in the commit message.

- [ ] **Step 3: Read file tail to anchor edit**

Run: `tail -20 ~/Research/apps/iconocracia-companion/CLAUDE.md`
Expected: capture the exact last line for `old_string`.

- [ ] **Step 4: Append catalog (trim rows whose skill failed Step 2)**

Use `Edit`. Append:

```markdown

## Skills for this workspace

Curated skills Claude should prefer in the companion app. Global + `find-skill` still apply.

### Primary entry points
| Skill ID | When to use |
| --- | --- |
| `frontend-design` | Production-grade UI work, component design, visual polish |
| `context7-mcp` | Fetch current library/framework docs before coding |
| `playwright` | Browser automation for testing or flows |
| `code-review` | Review changes for correctness/security/perf |
| `find-skill` | Fuzzy-search installed skills by intent |
```

- [ ] **Step 5: Verify**

Use Claude Code `Grep`: pattern `Skills for this workspace`, path `~/Research/apps/iconocracia-companion/CLAUDE.md`, output_mode `count`.
Expected: count = 1.

- [ ] **Step 6: Commit**

```bash
cd ~/Research/apps/iconocracia-companion
git add CLAUDE.md
git commit -m "docs(claude): seed companion-app skill catalog"
```

---

## Task 6: End-to-end acceptance

**Files:** none (manual verification).

- [ ] **Step 1: Confirm all four catalogs are in place**

Use Claude Code `Grep`: pattern `Skills for this workspace`, output_mode `files_with_matches`, across these four paths individually:
- `~/.claude/CLAUDE.md`
- `~/Research/CLAUDE.md`
- `~/Research/hub/iconocracy-corpus/CLAUDE.md`
- `~/Research/apps/iconocracia-companion/CLAUDE.md`

Expected: every path returns a match.

- [ ] **Step 2: Confirm `find-skill` skill present**

Run: `ls ~/.claude/skills/find-skill/SKILL.md`
Expected: file exists.

- [ ] **Step 3: Acceptance test 1 — thesis hub lookup**

Open a fresh Claude Code session with cwd `~/Research/hub/iconocracy-corpus`. Prompt: `/find-skill validate corpus schema`.
Expected: top result is `validate-corpus`; `why:` line mentions catalog-boost.

- [ ] **Step 4: Acceptance test 2 — app scope boost**

Open a fresh session with cwd `~/Research/apps/iconocracia-companion`. Prompt: `/find-skill review a react component`.
Expected: top 3 include `code-review` and/or `frontend-design`; no thesis-specific skill (e.g. `validate-corpus`, `iconocode-batch`) in top 3.

- [ ] **Step 5: Acceptance test 3 — no-match fallback**

Prompt: `/find-skill make coffee`.
Expected: top score < 2; finder returns fallback message "No strong match" plus up to 5 nearest candidates.

- [ ] **Step 6: Stale-entry behavior test**

Use `Edit` to temporarily add `totally-fake-skill` as a row under Primary entry points in `~/Research/CLAUDE.md`. Run `/find-skill totally fake`.
Expected: finder does not crash; reports that the catalog entry has no matching SKILL.md.
Revert the edit with a second `Edit` (new_string = the inserted row, old_string = empty row representation is not valid — use the reverse: old_string = the added row, new_string = ""). Re-verify the revert with `Grep` for `totally-fake-skill` returning zero matches.

---

## Self-Review

- **Spec coverage:**
  - Component 1 (catalog block) → Tasks 2–5 each append one catalog; shape matches spec exactly.
  - Component 2 (`/find-skill`) → Task 1 scaffolds skill with SKILL.md body matching spec's behavior and output rules.
  - Component 3 (four seed catalogs) → Tasks 2 (global), 3 (workspace), 4 (hub), 5 (companion).
  - Data flow → catalog-reading happens naturally via CLAUDE.md chain-load; finder executes via Step 3–5 in Task 6.
  - Error handling → zero-match fallback encoded in Task 1 SKILL.md; stale entry covered in Task 6 Step 6; duplicate handling is implicit (grep dedup).
  - Testing → Task 6 mirrors the four acceptance checks in the spec.
  - Maintenance → no automation introduced, aligns with spec's "manual, deliberate".
  - Out-of-scope items (SessionStart hook, git-branch scoping, machine-readable tags) intentionally excluded.

- **Placeholder scan:** no "TBD", "TODO", "implement later". Every code/catalog block is complete and verbatim.

- **Type consistency:** skill IDs (`iconocracy-agent`, `validate-corpus`, `find-skill`, `compilar-tese`, `corpus-scout`, `iconocode-analyze`, `iconocode-batch`, `thesis-progress`, `citation-management`, `dir410346`, `abnt-checker`, `thesis-reviewer`, `chapter-integrity`, `iconclass-reviewer`, `iconocode`, `corpus-dedup`, `frontend-design`, `context7-mcp`, `playwright`, `code-review`, `research`, `academic-research-skills`, `self-improvement`, `claude-md`, `plan`, `commit`, `caveman`, `literature-review`) spelled identically across tasks and spec.

---

## Execution Handoff

Plan complete and saved to `~/Research/docs/superpowers/plans/2026-04-14-skill-discovery.md`. Two execution options:

1. **Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
