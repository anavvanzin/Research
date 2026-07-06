# Creative Cronjobs Implementation Plan

> **For agentic workers:** Use subagent-driven-development (recommended) or executing-plans to implement task-by-task.

**Goal:** Implement the creative scheduled automation layer for ICONOCRACY, enabling mindful reflection, Warburgian juxtapositions, and progress coaching based on local quotes and corpus datasets.
**Architecture:** Python-based CLI utilities residing under the thesis codebase that interact with static databases (`forum-data.json`, `corpus-data.json`), writing execution and count states to a consolidated YAML cache (`~/.hermes/cron-cache/iconocracy-jobs.yaml`).
**Tech Stack:** Python 3.11.15 (Conda env), PyYAML, Pytest, stdlib (json, random, pathlib).

---

## File Mapping

- **Create:**
  - `hub/iconocracy-corpus/tools/scripts/cron_trechos_oracle.py` (Script for the quotes Oracle)
  - `hub/iconocracy-corpus/tools/scripts/cron_zwischenraum_generator.py` (Script for the visual-literary association)
  - `hub/iconocracy-corpus/tools/scripts/cron_thesis_progress_coach.py` (Script for Sunday progress coaching)
  - `hub/iconocracy-corpus/tests/test_cron_trechos_oracle.py` (Pytest suite)
  - `hub/iconocracy-corpus/tests/test_cron_zwischenraum_generator.py` (Pytest suite)
  - `hub/iconocracy-corpus/tests/test_cron_thesis_progress_coach.py` (Pytest suite)

---

## Tasks

### Task 1: Initialize Unified Cache State & Directory

**Files:**
- Create: `hub/iconocracy-corpus/tools/scripts/init_cron_cache.py`

- [ ] **Step 1: Write initialization script**
  ```python
  import os
  from pathlib import Path
  import yaml

  def main():
      cache_path = Path("~/.hermes/cron-cache/iconocracy-jobs.yaml").expanduser()
      cache_path.parent.mkdir(parents=True, exist_ok=True)
      if not cache_path.exists():
          initial_data = {
              "jobs": {
                  "trechos-oracle": {"last_run": None, "last_quote_position": 0},
                  "zwischenraum-generator": {"last_run": None, "last_item_id": None},
                  "thesis-progress-coach": {"last_run": None, "baseline_words": 0}
              }
          }
          with open(cache_path, "w", encoding="utf-8") as f:
              yaml.safe_dump(initial_data, f, default_flow_style=False, allow_unicode=True)
          print(f"Initialized cache state at: {cache_path}")
      else:
          print("Cache state already exists.")

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 2: Run initialization script**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python hub/iconocracy-corpus/tools/scripts/init_cron_cache.py
  ```

- [ ] **Step 3: Commit**
  ```bash
  git add hub/iconocracy-corpus/tools/scripts/init_cron_cache.py
  git commit -m "feat(automation): initialize unified state cache file"
  ```

---

### Task 2: Implement "Trechos" Oracle Script & Tests

**Files:**
- Create: `hub/iconocracy-corpus/tools/scripts/cron_trechos_oracle.py`
- Create: `hub/iconocracy-corpus/tests/test_cron_trechos_oracle.py`

- [ ] **Step 1: Write tests for Trechos Oracle**
  ```python
  import json
  from pathlib import Path
  from tools.scripts.cron_trechos_oracle import select_random_quote
  
  def test_select_random_quote(tmp_path):
      db_file = tmp_list_file = tmp_path / "forum-data.json"
      db_file.write_text(json.dumps({"posts": [{"bodyText": "“Test Quote”— Author", "position": 1}]}), encoding="utf-8")
      
      quote = select_random_quote(db_file)
      assert "Test" in quote["bodyText"]
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python -m pytest hub/iconocracy-corpus/tests/test_cron_trechos_oracle.py
  ```

- [ ] **Step 3: Write minimal implementation for Trechos Oracle**
  ```python
  import json
  import random
  from pathlib import Path
  import yaml
  
  def select_random_quote(db_path: Path) -> dict:
      with open(db_path, "r", encoding="utf-8") as f:
          data = json.load(f)
      return random.choice(data["posts"])

  def main():
      db_path = Path("~/Projects/anavvanzin.github.io/quotes/forum-data.json").expanduser()
      if not db_path.exists():
          print("Error: Quotes database forum-data.json not found.")
          return
      quote = select_random_quote(db_path)
      print(f"## Trechos Oracle\n\n> {quote['bodyText']}\n")

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 4: Run test to verify it passes**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python -m pytest hub/iconocracy-corpus/tests/test_cron_trechos_oracle.py
  ```

- [ ] **Step 5: Commit**
  ```bash
  git add hub/iconocracy-corpus/tools/scripts/cron_trechos_oracle.py hub/iconocracy-corpus/tests/test_cron_trechos_oracle.py
  git commit -m "feat(automation): implement trechos-oracle script and tests"
  ```

---

### Task 3: Implement "Mnemosyne" Associative Engine

**Files:**
- Create: `hub/iconocracy-corpus/tools/scripts/cron_zwischenraum_generator.py`
- Create: `hub/iconocracy-corpus/tests/test_cron_zwischenraum_generator.py`

- [ ] **Step 1: Write tests for Associative Engine**
  ```python
  import json
  from pathlib import Path
  from tools.scripts.cron_zwischenraum_generator import pair_quote_with_record

  def test_pair_quote_with_record(tmp_path):
      corpus_file = tmp_path / "corpus-data.json"
      corpus_file.write_text(json.dumps([{"id": "FR-013", "title": "Declaration"}]), encoding="utf-8")
      quotes_file = tmp_path / "forum-data.json"
      quotes_file.write_text(json.dumps({"posts": [{"bodyText": "“Silence”", "position": 1}]}), encoding="utf-8")
      
      record, quote = pair_quote_with_record(corpus_file, quotes_file)
      assert record["id"] == "FR-013"
      assert "Silence" in quote["bodyText"]
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python -m pytest hub/iconocracy-corpus/tests/test_cron_zwischenraum_generator.py
  ```

- [ ] **Step 3: Write implementation**
  ```python
  import json
  import random
  from pathlib import Path

  def pair_quote_with_record(corpus_path: Path, quotes_path: Path):
      with open(corpus_path, "r", encoding="utf-8") as f:
          corpus = json.load(f)
      with open(quotes_path, "r", encoding="utf-8") as f:
          quotes = json.load(f)
      
      return random.choice(corpus), random.choice(quotes["posts"])

  def main():
      corpus_path = Path("hub/iconocracy-corpus/corpus/corpus-data.json")
      quotes_path = Path("~/Projects/anavvanzin.github.io/quotes/forum-data.json").expanduser()
      if not (corpus_path.exists() and quotes_path.exists()):
          print("Error: Missing corpus or quotes dataset.")
          return
      record, quote = pair_quote_with_record(corpus_path, quotes_path)
      print(f"## Mnemosyne Associative Prompt\n\nPairing item: **{record['id']}** with literary fragment:\n> {quote['bodyText']}\n")

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 4: Run tests**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python -m pytest hub/iconocracy-corpus/tests/test_cron_zwischenraum_generator.py
  ```

- [ ] **Step 5: Commit**
  ```bash
  git add hub/iconocracy-corpus/tools/scripts/cron_zwischenraum_generator.py hub/iconocracy-corpus/tests/test_cron_zwischenraum_generator.py
  git commit -m "feat(automation): implement zwischenraum-generator script and tests"
  ```

---

### Task 4: Implement "Thesis Compass" Coach

**Files:**
- Create: `hub/iconocracy-corpus/tools/scripts/cron_thesis_progress_coach.py`
- Create: `hub/iconocracy-corpus/tests/test_cron_thesis_progress_coach.py`

- [ ] **Step 1: Write test for progress coach**
  ```python
  from pathlib import Path
  from tools.scripts.cron_thesis_progress_coach import count_manuscript_words

  def test_count_manuscript_words(tmp_path):
      manuscript_dir = tmp_path / "manuscrito"
      manuscript_dir.mkdir()
      (manuscript_dir / "chapter1.md").write_text("This has exactly five words.", encoding="utf-8")
      
      count = count_manuscript_words(manuscript_dir)
      assert count == 5
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python -m pytest hub/iconocracy-corpus/tests/test_cron_thesis_progress_coach.py
  ```

- [ ] **Step 3: Write implementation**
  ```python
  import sys
  from pathlib import Path
  import yaml

  def count_manuscript_words(manuscript_path: Path) -> int:
      count = 0
      for md_file in manuscript_path.glob("*.md"):
          words = md_file.read_text(encoding="utf-8", errors="ignore").split()
          count += len(words)
      return count

  def main():
      manuscript_path = Path("hub/iconocracy-corpus/tese/manuscrito")
      if not manuscript_path.exists():
          print("Error: tese/manuscrito/ not found.")
          return
      words = count_manuscript_words(manuscript_path)
      print(f"## Weekly Thesis Velocity: {words} words counted.")

  if __name__ == "__main__":
      main()
  ```

- [ ] **Step 4: Run tests**
  ```bash
  /opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python -m pytest hub/iconocracy-corpus/tests/test_cron_thesis_progress_coach.py
  ```

- [ ] **Step 5: Commit**
  ```bash
  git add hub/iconocracy-corpus/tools/scripts/cron_thesis_progress_coach.py hub/iconocracy-corpus/tests/test_cron_thesis_progress_coach.py
  git commit -m "feat(automation): implement thesis-progress-coach script and tests"
  ```
