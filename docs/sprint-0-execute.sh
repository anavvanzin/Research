#!/bin/bash
# ========================================================
# SPRINT 0 — EMERGÊNCIA: Backup do trabalho no GitHub
# Rodar no Terminal do Mac (NÃO no Cowork sandbox)
# Data: 2026-04-16
# ========================================================

set -e
echo "🚨 SPRINT 0 — Backup de emergência"
echo "===================================="
echo ""

# ----------------------------
# STEP 1: Push hub (49 commits)
# ----------------------------
echo "📦 [1/4] Pushing hub/iconocracy-corpus (49 commits pendentes)..."
cd ~/Research/hub/iconocracy-corpus
git push origin main
echo "✅ Hub pushed."
echo ""

# ----------------------------
# STEP 2: Commit e push Research meta-workspace
# ----------------------------
echo "📦 [2/4] Committing and pushing Research meta-workspace..."
cd ~/Research
git add AGENTS.md docs/skill-upgrade-v2/ docs/ULTRAPLAN-2026-04-16.md docs/AUTOMATION-RECOMMENDATIONS.md docs/sprint-0-execute.sh
git commit -m "docs: fix AGENTS.md symlinks, add skill v2, ultraplan, and automation recommendations

- Fix reversed symlink descriptions for indexing/ and Atlas/ in AGENTS.md
- Add iconocracy-agent v2 (lightweight orchestrator, 12KB vs 34KB)
- Add ULTRAPLAN diagnostic and action plan
- Add Claude Code automation recommendations
- Add Sprint 0 execution script"
git push origin main
echo "✅ Research pushed."
echo ""

# ----------------------------
# STEP 3: Create remote for companion (if missing)
# ----------------------------
echo "📦 [3/4] Checking companion app remote..."
cd ~/Research/apps/iconocracia-companion
if ! git remote get-url origin &>/dev/null; then
    echo "  Creating GitHub repo for companion..."
    gh repo create anavvanzin/iconocracia-companion --private --source=. --push
    echo "✅ Companion repo created and pushed."
else
    echo "  Remote exists: $(git remote get-url origin)"
    git push origin main 2>/dev/null || git push -u origin main 2>/dev/null || echo "  ⚠️  Push failed — check branch name"
fi
echo ""

# ----------------------------
# STEP 4: Fix iconocracia-space origin
# ----------------------------
echo "📦 [4/4] Checking iconocracia-space remote..."
cd ~/Research/apps/iconocracia-space
current_origin=$(git remote get-url origin 2>/dev/null || echo "none")
if [ "$current_origin" = "https://github.com/anavvanzin/Research.git" ]; then
    echo "  ⚠️  Origin points to Research.git (wrong!)"
    echo "  Creating correct repo..."
    # Check if repo exists first
    if gh repo view anavvanzin/iconocracia-space &>/dev/null; then
        git remote set-url origin https://github.com/anavvanzin/iconocracia-space.git
    else
        gh repo create anavvanzin/iconocracia-space --private --source=. --push
    fi
    echo "✅ Fixed."
else
    echo "  Origin: $current_origin (ok)"
fi
echo ""

# ----------------------------
# STEP 5: Install skill v2
# ----------------------------
echo "📦 [BONUS] Installing iconocracy-agent v2..."
if [ -f ~/Research/docs/skill-upgrade-v2/SKILL.md ]; then
    cp ~/Research/docs/skill-upgrade-v2/SKILL.md ~/.claude/skills/iconocracy-agent/SKILL.md
    echo "✅ Skill v2 installed."
else
    echo "  ⚠️  Source file not found — check ~/Research/docs/skill-upgrade-v2/SKILL.md"
fi
echo ""

# ----------------------------
# SUMMARY
# ----------------------------
echo "===================================="
echo "🏁 Sprint 0 completo!"
echo ""
echo "Verificação:"
echo "  Hub unpushed: $(cd ~/Research/hub/iconocracy-corpus && git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ') commits"
echo "  Research unpushed: $(cd ~/Research && git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ') commits"
echo ""
echo "Próximo: Sprint 1 (triagem dos 64 arquivos soltos no hub)"
