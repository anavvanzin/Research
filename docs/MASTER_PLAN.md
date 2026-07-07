# Research — Master Development Plan

> **Purpose**: Central tracking document for work items, ideas, bugs, and roadmap across the ICONOCRACIA meta-workspace
> **Last Updated**: 2026-07-03
> **Project Status**: Active

---

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Task Dependency Index](#task-dependency-index) | Prevent multi-instance conflicts |
| [Active Work](#active-work) | Current tasks being worked on |
| [Bug Tracking](#bug-tracking) | Known bugs and fixes |
| [Roadmap](#roadmap) | Planned features by priority |
| [Ideas](#ideas) | Ideas to consider |
| [Known Issues](#known-issues) | Documented limitations |
| [Completed Work](#completed-work) | Archive of finished items |

---

## Task Dependency Index

> **Purpose**: Prevent multiple Claude instances from editing the same files simultaneously.
> Only relevant if you wire the task-lock hooks (see `.claude/hooks/README.md`). For a
> single-instance Cowork workflow this table is just documentation.

| Task ID | Status | Primary Files | Depends On |
|---------|--------|---------------|------------|
| TASK-001 | TODO | `example.md` | - |

**Status Legend**: `TODO` | `IN_PROGRESS` | `REVIEW` | `DONE`

---

## Active Work

### TASK-001: Example task (TODO)

**Description**: Replace this with a real work item. One block per task.

**Priority**: P2-MEDIUM

**Files to Modify**:
- `example.md` — what changes here

**Implementation Steps**:
- [ ] Step 1: Research and planning
- [ ] Step 2: Implementation
- [ ] Step 3: Verification

---

## Bug Tracking

| ID | Bug | Severity | Status | Notes |
|----|-----|----------|--------|-------|
| BUG-001 | Example bug description | P2 | 🔄 IN PROGRESS | Investigating root cause |

---

## Roadmap

### Priority Legend
- **P0**: Critical — fix immediately
- **P1**: High — next sprint
- **P2**: Medium — this quarter
- **P3**: Low — nice to have

| ID | Feature | Priority | Status | Notes |
|----|---------|----------|--------|-------|
| ROAD-001 | Example item | P2 | TODO | Planned |

---

## Ideas

| ID | Idea | Category | Added |
|----|------|----------|-------|
| IDEA-001 | Example idea | Enhancement | 2026-07-03 |

---

## Known Issues

| ID | Issue | Workaround | Status |
|----|-------|------------|--------|
| ISSUE-001 | Example known issue | Workaround description | Acknowledged |

---

## Completed Work

### ~~TASK-000~~: Install dev infrastructure (✅ DONE)
- Completed: 2026-07-03
- Summary: Added MASTER_PLAN tracking + inert task-lock hooks (opt-in) via /dev-setup

---

## Formatting Guide for AI/Automation

### Task Header Format
```markdown
### TASK-XXX: Task Title (STATUS)
### ~~TASK-XXX~~: Completed Task Title (✅ DONE)
```

### Status Keywords (for parser detection)
| Status | Keywords |
|--------|----------|
| Done | `DONE`, `COMPLETE`, `✅`, `~~strikethrough~~` |
| In Progress | `IN PROGRESS`, `IN_PROGRESS`, `🔄`, `ACTIVE` |
| Review | `REVIEW`, `MONITORING`, `👀` |
| Todo | Default (no keyword) |
