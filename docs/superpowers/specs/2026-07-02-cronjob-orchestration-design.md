# Cronjob Orchestration Design for ICONOCRACY

## Metadata

| | |
|---|---|
| **Date** | 2026-07-02 |
| **Author** | Aurelius (Hermes Agent) for Ana Vanzin |
| **Status** | Spec proposed, awaiting review |
| **Focus** | Multi-platform scheduled automation layer (Hermes + Claude Code) |
| **Target** | Quali Nov/2027 support & operational security |

---

## 1. Context & Motivation

Ana's ICONOCRACY research involves multiple moving parts that require continuous validation, sync checks, and progress tracking. Over time, manual auditing became a bottleneck, leading to drift (e.g., mismatched corpus item counts, silent sync failures, missing packages blocking cron runs). 

To solve this, we are establishing a robust, multi-platform, cost-aware scheduled automation layer. By combining **Hermes cron jobs** (for heavy execution, programmatic validation, and file writing) with **Claude scheduled tasks** (for light reminder prompts and attention-grabbing decision gates), we maintain high-signal rigor with minimal token costs.

---

## 2. Multi-Platform Architecture

```
                      +-----------------------------+
                      |       USER WORKSPACE        |
                      +--------------+--------------+
                                     |
             +-----------------------+-----------------------+
             |                                               |
             v                                               v
+----------------------------+                 +----------------------------+
|      HERMES CRONJOBS       |                 |    CLAUDE SCHEDULED TASKS  |
|   (Heavy Logic / Data)     |                 |  (Light Reminders / Prompts)|
+------------+---------------+                 +------------+---------------+
             |                                               |
             |- Runs Python/Bash scripts                     |- Attention-grabbing prompts
             |- Programmatic file writing                    |- Focuses on writing velocity
             |- Schema validations                           |- Ingest review questions
             |- State-persisted cache                        |- Direct dialog with Ana
             v                                               v
+----------------------------+                 +----------------------------+
|  records.jsonl / DB sync   |                 |    Daily Writing Intent    |
+----------------------------+                 +----------------------------+
```

### Allocation Strategy
- **Hermes Cron Jobs:** Programmatic validations, schema checks, multi-machine git status auditing, Word/PDF compilations, and heavier sync operations.
- **Claude Scheduled Tasks:** Actionable prompts delivered at session start, daily writing intentions, checklist compliance, and lightweight reminders.

---

## 3. Cost-Aware Job Inventory

To prevent token bloating and "alert fatigue," we define three operating tiers based on changes in the workspace. Running daily checks on static files is a waste of tokens, so we implement a **change-detection gate** (hash checking) to make daily jobs return `[SILENT]` if no files were modified.

| ID | Platform | Task Name | Cadence | Est. Tokens / Run | Cost / Month | Fallback / Trigger Condition |
|---|---|---|---|---|---|---|
| **C1** | Hermes | `corpus-validation` | Twice a week (Mon, Thu) | 3K | ~$0.18 | Logs failure to cache, skips release gate. |
| **C2** | Hermes | `thesis-progress` | Weekly (Sunday 20:00) | 2.5K | ~$0.10 | Fallback to last recorded count if draft missing. |
| **C3** | Hermes | `sync-safeguard` | Daily (08:00) | 1.5K | ~$0.45 | Warns via home channel if uncommitted local drift > 24h. |
| **C4** | Hermes | `iconocode-backfill` | Weekly (Friday 02:00) | 15K - 45K | ~$1.20 | [SILENT] if no unanalyzed items present. |
| **T1** | Claude | `daily-writing-prompt` | Session Start | ~1K | $0.00 | Uses Claude attention budget. |
| **T2** | Claude | `gap-analysis-reminder`| Weekly | ~1.5K | $0.00 | Prompt to run bibliographic review. |

---

## 4. Persistent State Cache

To prevent redundant heavy analysis across runs, we introduce a YAML state cache stored at `~/.hermes/cron-cache/iconocracy-jobs.yaml`.

```yaml
jobs:
  corpus-validation:
    last_run: "2026-07-02T08:00:00-03:00"
    last_status: "ok"
    records_hash: "sha256:d5d8b8e0bcf1038a9ed85f42b6bd4d4328e985a884ace863e41"
    item_count: 299

  thesis-progress:
    last_run: "2026-06-28T20:00:00-03:00"
    baseline_words: 45200
    current_words: 46400
    weekly_velocity: 1200
    target_weekly: 1000

  sync-safeguard:
    last_run: "2026-07-02T08:00:00-03:00"
    is_mac_dirty: false
    ssd_synced: true
    last_backup_hash: "sha256:f4a7eb52ede8e6e184bc270a8956cbfa782b870"
```

### State-Saving Implementation Guidelines
- Every script that writes to the cache MUST run `CACHE_YAML.parent.mkdir(parents=True, exist_ok=True)` first to avoid silent `FileNotFoundError` crashes.
- The cache file should be updated atomically using a tempfile.

---

## 5. Error Handling & Fallback Protocol

| Failure Scenario | Mitigation Strategy | Retry Policy |
|---|---|---|
| **Conda Env Missing / Path Resolution** | Never use `conda run`. Run `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python` directly from scripts. | No auto-retry; logs fatal setup alert to terminal. |
| **Offline CDP Port** | Do not hardcode port `9222`. Read port dynamically from `config.yaml` (`browser.cdp_url`) or check port `9223` (Obscura). | Retry once after 5m. |
| **Missing Files / Corpus** | Exit early with clean stderr, write `status: missing_files` to cache, alert home channel. | Do not run again until manually resolved. |
| **No Output generated** | Prevent `(No response generated)` by enclosing the entire script in a `try-except` block that captures traceback and prints it to stdout. | Set alert flag on next session start. |

---

## 6. Testing Strategy

1. **Dry-Run Script Verification:** Run every Python script in foreground mode inside the `iconocracy` environment to confirm it outputs clean JSON/YAML.
2. **First-run Cache Generation:** Pre-create directories and run check scripts to verify the cache state file is generated correctly.
3. **Trigger Testing:** Run jobs on demand (`cronjob action='run'`) to inspect stdout/stderr before turning them on schedule.

---

## 7. Success Criteria

- [ ] All 4 Hermes cron jobs are successfully registered via `cronjob action='create'`.
- [ ] No `(No response generated)` errors during execution.
- [ ] Clear decision trees implemented in LLM prompts with explicit precedence rules to prevent silent failures when suggestions are present.
- [ ] Words, hash baselines, and execution metadata correctly stored in `~/.hermes/cron-cache/iconocracy-jobs.yaml`.

---

## 8. Self-Review

- **Consistency:** Python target path points exactly to the active `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python`.
- **Precedence:** Decision tree prompts are explicitly structured with first-match-wins patterns.
- **Paths:** All script targets utilize absolute paths.
