# Design Spec: Creative & Mindful Cronjobs for ICONOCRACY

## Metadata

| | |
|---|---|
| **Date** | 2026-07-02 |
| **Author** | Aurelius (Hermes Agent) for Ana Vanzin |
| **Status** | Spec proposed, awaiting review |
| **Focus** | Creative, literary, and velocity-oriented scheduled tasks (Hermes) |
| **Target** | Academic mindfulness & thesis inspiration |

---

## 1. Context & Concept

To counterbalance the high-rigor mechanical validations of the core ICONOCRACY pipeline, we are designing a secondary layer of **Creative Scheduled Tasks**. These are designed to stimulate new academic insights and maintain emotional resilience (mindfulness) during long writing sprints.

These jobs rely directly on Ana's local **Trechos (Quotes) Database** (containing 1,608 quotes in `~/Projects/anavvanzin.github.io/quotes/forum-data.json`) and her **Thesis Corpus Export** (`hub/iconocracy-corpus/corpus/corpus-data.json`).

---

## 2. Creative Job Suite

### Job 1: The "Trechos" Oracle (`trechos-oracle`)
* **Objective:** Periodically delivers a random literary quote combined with a prompt for personal gratitude or reflection.
* **Cadence:** Every Tuesday and Thursday morning (09:00).
* **Execution Script:** `tools/scripts/cron_trechos_oracle.py` (runs on Hermes).
* **Output Target:** Appends a beautifully styled markdown note to `~/Zettelkasten/_inbox/gratitude-journal.md` or delivers directly to her Telegram Home Channel (`telegram:771120864`).
* **Example Output:**
  ```markdown
  ## Trechos Oracle — 2026-07-02
  
  > "Your great mistake is to act the drama as if you were alone... Alertness is the hidden discipline of familiarity... Everything is waiting for you."
  > — David Whyte, *Everything is Waiting for You*
  
  **Aurelius Nudge:** Where in your thesis today can you ease into the conversation and let the ideas perfect themselves? Take a moment to record one point of gratitude for this writing sprint.
  ```

---

### Job 2: The "Mnemosyne" Associative Engine (`zwischenraum-generator`)
* **Objective:** Generates unexpected, Warburgian juxtapositions (an associative *Zwischenraum*) to inspire thesis drafting.
* **Cadence:** Every Wednesday (08:00).
* **Execution Script:** `tools/scripts/cron_zwischenraum_generator.py` (runs on Hermes).
* **Methodology:**
  1. Reads a random item from the flat corpus export `hub/iconocracy-corpus/corpus/corpus-data.json`.
  2. Reads a random quote from the literary quotes database `forum-data.json`.
  3. Synthesizes a creative tension prompt that bridges the legal iconography (e.g., a 19th-century representation of Justice) and the literary quote.
* **Output Target:** Deposited as an MD file under `~/Zettelkasten/_inbox/zwischenraum-prompt.md`.

---

### Job 3: The "Thesis Compass & Velocity Coach" (`thesis-velocity-coach`)
* **Objective:** Gentle progress tracking on a weekly cadence.
* **Cadence:** Sunday evening (20:00).
* **Execution Script:** `tools/scripts/cron_thesis_progress_coach.py` (runs on Hermes).
* **Methodology:**
  1. Computes the word count in `hub/iconocracy-corpus/tese/manuscrito/*.md`.
  2. Compares it against the last recorded value in `~/.hermes/cron-cache/iconocracy-jobs.yaml`.
  3. Produces a supportive, literary milestone message rather than a cold table (e.g., celebrating writing velocity and suggesting she bake some brownies).

---

## 3. Data Flow & State Caching

```
[forum-data.json] ----+
                      v
[corpus-data.json] -> [Hermes Cron Script] -> [State Cache YAML] -> [Telegram / Zettelkasten]
```

State is managed within the unified cache `~/.hermes/cron-cache/iconocracy-jobs.yaml`:
```yaml
jobs:
  trechos-oracle:
    last_run: "2026-07-02T09:00:00-03:00"
    last_quote_position: 1590
  zwischenraum-generator:
    last_run: "2026-07-02T08:00:00-03:00"
    last_item_id: "FR-013"
  thesis-progress-coach:
    last_run: "2026-06-28T20:00:00-03:00"
    baseline_words: 45200
```

---

## 4. Testing & Verification

1. **Dry-run local execution:** Execute each python script in the terminal manually before turning on schedule.
2. **Channel Delivery Check:** Trigger a test delivery of the Trechos Oracle to verify the integration with the Telegram gateway.
3. **Empty Fallback Verification:** Ensure the scripts handle missing database files gracefully without raising unparsed tracebacks.
