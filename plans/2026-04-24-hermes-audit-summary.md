# HERMES AGENT STATE — 2026-04-24

## Workspace roots (canonical)
  ROOT = /Users/ana/Research
  HUB  = /Users/ana/Research/hub/iconocracy-corpus

## Current branch positions
  ~/Research                              → main                     (clean, pushed)
  ~/Research/hub/iconocracy-corpus       → main (ahead 2)           (pushed)
  ~/Research/apps/iconocracia-companion  → main                     (clean, pushed)
  ~/Research/pipelines/indexing          → main (ahead 2)           (NOT pushed — remote missing)

## Alerts
  • Port 9119 (old mxit) — cleared
  • Port 3000 (WhatsApp gateway) — cleared
  • Port 8765 (Artifact Preview) — running, 200 OK
  • Port 9120 (Hermes Dashboard) — running, 200 OK
  • Artifact Preview reachable via curl but not browser — check Brave shields / try 127.0.0.1:8765

## Open todos
  • Fix indexing repo remote or accept local-only state
  • Decide fate of remaining worktrees:
      iconocracy-corpus-hub-consistency
      iconocracy-main-crda-fix
      iconocracy-pr-33-sync
  • NIM_API_KEY placeholder added to ~/.zshrc (lines 97–98) — needs your key value

## Notes
  • chapter_targets.json updated to canonical Research paths in both skill locations
  • Method contract and term gate live in hub; CI validates on every push
  • records.jsonl: 165 records (all valid); purification.jsonl: 154 items (all valid)
  • Traceability: 0% — 457 claims without evidence/gap status (pre-existing)
