# Triagem & Consolidação de Vaults Obsidian — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidar 13 vaults Obsidian em 1 vault canon `~/Zettelkasten/` para conhecimento da tese, arquivando legacy em Dropbox e reconciliando 3 cópias divergentes do corpus iconocracia.

**Architecture:** Filesystem + git operations. Seis fases ordenadas (F1-F6). Snapshot antes de mutação. Pull review com atomização. Vanilla Obsidian (zero plugin novo). Cada task validável independente via comandos shell.

**Tech Stack:** bash 5+, rsync 3+, git, Python 3.12 (env `iconocracy` para diff helper), Obsidian vanilla, Dropbox sync.

**Spec base:** `docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md`

**Estimated total effort:** 8-15h, distribuído em 7-12 sessões.

---

## File Structure

Arquivos a criar (não há código de aplicação — apenas helpers, configs e READMEs):

| Caminho | Responsabilidade |
|---------|------------------|
| `~/Dropbox/vaults-archive-2026-06-05/README.md` | Status geral da triagem, índice |
| `~/Dropbox/vaults-archive-2026-06-05/<source>/README.md` | Por source: origem, data, contagem, status review |
| `~/Zettelkasten/.obsidian/` | Config Obsidian baseline (gerada ao abrir) |
| `~/Zettelkasten/README.md` | Convenções pessoais Z |
| `~/Zettelkasten/_inbox/.gitkeep` | Pasta fleeting notes |
| `~/Zettelkasten/lit/.gitkeep` | Pasta literature notes |
| `~/Zettelkasten/zet/.gitkeep` | Pasta permanent notes |
| `~/Zettelkasten/moc/.gitkeep` | Pasta Maps of Content |
| `~/Zettelkasten/zet/<id>-piloto.md` | Primeira nota Z de teste |
| `~/Research/tools/scripts/diff_corpus_vaults.py` | Diff entre 3 cópias do corpus (helper F2) |

Estrutura informada pelo spec: cada task é self-contained, mutação só após snapshot verificado.

---

## Task 1: F1 — Snapshot Completo das Fontes

**Files:**
- Create: `~/Dropbox/vaults-archive-2026-06-05/` (root)
- Create: `~/Dropbox/vaults-archive-2026-06-05/README.md`
- Create: 8 subfolders + READMEs para cada source

- [ ] **Step 1: Verify Dropbox is running and synced**

Run:
```bash
ls -la ~/Dropbox/.dropbox 2>/dev/null && echo "Dropbox mount OK"
pgrep -fl Dropbox | head -2
```

Expected: Mount visible, processo Dropbox rodando. Se não, abrir Dropbox app antes de prosseguir.

- [ ] **Step 2: Create archive root dir**

Run:
```bash
mkdir -p ~/Dropbox/vaults-archive-2026-06-05/
cd ~/Dropbox/vaults-archive-2026-06-05/
ls -la
```

Expected: Diretório vazio criado.

- [ ] **Step 3: Write archive root README**

Run:
```bash
cat > ~/Dropbox/vaults-archive-2026-06-05/README.md <<'EOF'
# Vaults Archive — Snapshot 2026-06-05

Snapshot dos vaults Obsidian existentes antes de consolidação em ~/Zettelkasten/.
Ver spec: ~/Research/docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md

## Origens

| Source | Path original | Notas | Última mod | Status |
|--------|---------------|-------|------------|--------|
| research-root | ~/Research/ (exclui sub-vaults) | ~5500 | 2026-06-05 | aguardando review F4 |
| documents-linux | ~/Documents/linux/ | 1253 | 2026-05-16 | aguardando review F4 |
| downloads-analise | ~/Downloads/ana 2026 main/ANAlise/ | 1032 | 2026-06-01 | aguardando review F4 |
| iconocracy-wiki-research | ~/Research/hub/iconocracy-corpus/wiki/ | 611 | 2026-06-01 | aguardando review F4 |
| iconocracy-wiki-github | ~/Documents/GitHub/iconocracy-corpus/wiki/ | 648 | 2026-05-30 | aguardando review F4 |
| iconocracy-wiki-projetos | ~/projetos/research/hub/iconocracy-corpus/wiki/ | 611 | 2026-05-20 | aguardando review F4 |
| iconocracy-vault-github | ~/Documents/GitHub/iconocracy-corpus/vault/ | 621 | 2026-05-30 | DIVERGENTE — reconciliar F2 |
| iconocracy-vault-projetos | ~/projetos/research/hub/iconocracy-corpus/vault/ | 611 | 2026-05-24 | DIVERGENTE — reconciliar F2 |

## Retenção

12 meses (até 2027-06-05). Depois disso, revisitar para decidir descarte definitivo
ou retenção indefinida em backup externo.
EOF
echo "README criado"
wc -l ~/Dropbox/vaults-archive-2026-06-05/README.md
```

Expected: README criado, ~25 linhas.

- [ ] **Step 4: Snapshot each source via rsync (parallel-safe, idempotente)**

Run sequentially (rsync stable for these sizes, no parallelism needed):
```bash
ARCH=~/Dropbox/vaults-archive-2026-06-05

# Source 1: Research raiz (cuidado: exclui sub-vaults que serão tratados separados)
rsync -aHp --exclude='hub/iconocracy-corpus/vault' \
            --exclude='hub/iconocracy-corpus/wiki' \
            --exclude='Chaos' \
            --exclude='.git' \
            ~/Research/ $ARCH/research-root/

# Source 2: Documents/linux
rsync -aHp ~/Documents/linux/ $ARCH/documents-linux/

# Source 3: Downloads/ANAlise
rsync -aHp "$HOME/Downloads/ana 2026 main/ANAlise/" $ARCH/downloads-analise/

# Source 4: 3 wikis iconocracy
rsync -aHp ~/Research/hub/iconocracy-corpus/wiki/ $ARCH/iconocracy-wiki-research/
rsync -aHp ~/Documents/GitHub/iconocracy-corpus/wiki/ $ARCH/iconocracy-wiki-github/
rsync -aHp ~/projetos/research/hub/iconocracy-corpus/wiki/ $ARCH/iconocracy-wiki-projetos/

# Source 5: 2 cópias divergentes do corpus vault (canon NÃO precisa archive — já está em git Research)
rsync -aHp ~/Documents/GitHub/iconocracy-corpus/vault/ $ARCH/iconocracy-vault-github/
rsync -aHp ~/projetos/research/hub/iconocracy-corpus/vault/ $ARCH/iconocracy-vault-projetos/

echo "rsync completo"
```

Expected: 8 subfolders preenchidos em ~/Dropbox/vaults-archive-2026-06-05/. Tempo: 1-5 min dependendo de tamanho. rsync sem erros.

- [ ] **Step 5: Verify snapshot counts match originals**

Run:
```bash
ARCH=~/Dropbox/vaults-archive-2026-06-05

# Função para contar .md
count_md() { find "$1" -name "*.md" -type f 2>/dev/null | wc -l | xargs; }

echo "== Verificação contagem .md (original vs archive) =="
echo "research-root:     $(count_md ~/Research) - subvaults vs $(count_md $ARCH/research-root)"
echo "documents-linux:   $(count_md ~/Documents/linux) vs $(count_md $ARCH/documents-linux)"
echo "downloads-analise: $(count_md "$HOME/Downloads/ana 2026 main/ANAlise") vs $(count_md $ARCH/downloads-analise)"
echo "wiki-research:     $(count_md ~/Research/hub/iconocracy-corpus/wiki) vs $(count_md $ARCH/iconocracy-wiki-research)"
echo "wiki-github:       $(count_md ~/Documents/GitHub/iconocracy-corpus/wiki) vs $(count_md $ARCH/iconocracy-wiki-github)"
echo "wiki-projetos:     $(count_md ~/projetos/research/hub/iconocracy-corpus/wiki) vs $(count_md $ARCH/iconocracy-wiki-projetos)"
echo "vault-github:      $(count_md ~/Documents/GitHub/iconocracy-corpus/vault) vs $(count_md $ARCH/iconocracy-vault-github)"
echo "vault-projetos:    $(count_md ~/projetos/research/hub/iconocracy-corpus/vault) vs $(count_md $ARCH/iconocracy-vault-projetos)"
```

Expected: contagens batem (research-root pode ser menor — subvaults excluídos). Se diverge >5%, RE-RUN rsync.

- [ ] **Step 6: Write per-source READMEs**

Run:
```bash
ARCH=~/Dropbox/vaults-archive-2026-06-05
TODAY=$(date +%Y-%m-%d)

for src in research-root documents-linux downloads-analise \
           iconocracy-wiki-research iconocracy-wiki-github iconocracy-wiki-projetos \
           iconocracy-vault-github iconocracy-vault-projetos; do
  count=$(find $ARCH/$src -name "*.md" -type f 2>/dev/null | wc -l | xargs)
  cat > $ARCH/$src/_ARCHIVE_README.md <<EOF
# Archive snapshot: $src

- **Origem**: (ver tabela em ../README.md)
- **Snapshot date**: $TODAY
- **Notas .md no snapshot**: $count
- **Status**: aguardando review F4
- **Sub-projeto**: A (triagem) — ver ~/Research/docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md

## Quando revisar

Marcar status="reviewed $TODAY" neste README ao concluir revisão dessa source.
EOF
done
echo "Per-source READMEs escritos:"
ls -la $ARCH/*/  _ARCHIVE_README.md 2>/dev/null | head -10
```

Expected: 8 arquivos `_ARCHIVE_README.md` criados, um por source folder.

- [ ] **Step 7: Wait for Dropbox sync — verify cloud reflects local**

Run:
```bash
echo "Aguardando sync Dropbox... verifique no menu bar que ícone está VERDE/sincronizado"
echo "Depois rodar:"
echo "  du -sh ~/Dropbox/vaults-archive-2026-06-05/"
du -sh ~/Dropbox/vaults-archive-2026-06-05/
```

Expected: Tamanho total razoável (10-200 MB dependendo de anexos). Ícone Dropbox verde no menu bar. Esta é verificação MANUAL — não prosseguir até confirmar.

- [ ] **Step 8: Commit F1 status no repo Research (rastreabilidade)**

Run:
```bash
cd ~/Research

# Cria nota de progresso, NÃO commita conteúdo do archive (está em Dropbox, não em git)
mkdir -p docs/superpowers/progress/
cat > docs/superpowers/progress/2026-06-05-zettelkasten-A-F1-done.md <<'EOF'
# F1 done — Snapshot Archive

- Date: 2026-06-05
- Output: ~/Dropbox/vaults-archive-2026-06-05/ (8 sources + READMEs)
- All counts verified
- Dropbox sync confirmed
EOF

git add docs/superpowers/progress/2026-06-05-zettelkasten-A-F1-done.md
git commit -m "progress: Zettelkasten sub-projeto A F1 (snapshot archive) done"
```

Expected: Commit feito no main com mensagem indicada.

---

## Task 2: F5 — Descarte de Vaults Vazios (quick win, isolado de F1)

**Files:**
- Delete: `~/Documents/Obsidian Vault/.obsidian/` (vault vazio)
- Delete: `~/Research/Chaos/.obsidian/` ou diretório inteiro (1 nota)
- Delete: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/anavanzinthesis/.obsidian/`
- Delete: Obsidian Sandbox

- [ ] **Step 1: Verify vaults realmente vazios antes de deletar**

Run:
```bash
echo "== ~/Documents/Obsidian Vault =="
find "$HOME/Documents/Obsidian Vault" -name "*.md" -type f 2>/dev/null | head -3
echo "TOTAL: $(find "$HOME/Documents/Obsidian Vault" -name "*.md" 2>/dev/null | wc -l | xargs)"

echo "== ~/Research/Chaos =="
ls -la ~/Research/Chaos 2>/dev/null
find ~/Research/Chaos -name "*.md" -type f 2>/dev/null

echo "== iCloud anavanzinthesis =="
ICL="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/anavanzinthesis"
[ -d "$ICL" ] && find "$ICL" -name "*.md" | wc -l | xargs echo "notas:"
```

Expected: Documents/Obsidian Vault = 0 .md. iCloud = 0 .md. Research/Chaos = 1 .md (já snapshotado em F1? Verificar — se não, skipar e archive antes).

- [ ] **Step 2: Archive Chaos (única nota) antes de deletar**

Run:
```bash
if [ -d ~/Research/Chaos ] && [ "$(find ~/Research/Chaos -name '*.md' | wc -l)" -gt 0 ]; then
  mkdir -p ~/Dropbox/vaults-archive-2026-06-05/research-chaos/
  rsync -aHp ~/Research/Chaos/ ~/Dropbox/vaults-archive-2026-06-05/research-chaos/
  echo "Chaos archived. Verifying sync..."
  du -sh ~/Dropbox/vaults-archive-2026-06-05/research-chaos/
fi
```

Expected: Chaos arquivado em Dropbox. Verificar sync verde.

- [ ] **Step 3: Delete vaults vazios — Documents/Obsidian Vault**

Run:
```bash
rm -rf "$HOME/Documents/Obsidian Vault"
ls -la "$HOME/Documents/Obsidian Vault" 2>&1 | head -2
```

Expected: "No such file or directory" — confirmação de remoção.

- [ ] **Step 4: Delete iCloud anavanzinthesis .obsidian/ órfão**

Run:
```bash
ICL="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/anavanzinthesis"
if [ -d "$ICL" ]; then
  rm -rf "$ICL/.obsidian"
  echo "Removido .obsidian/ órfão; pasta pai preservada (pode haver outros arquivos)"
  ls -la "$ICL" 2>&1 | head -5
fi
```

Expected: .obsidian/ deletado. Pasta pai pode permanecer vazia ou com outros arquivos não-vault.

- [ ] **Step 5: Delete Obsidian Sandbox (test vault interno)**

Run:
```bash
SBX="$HOME/Library/Application Support/obsidian/Obsidian Sandbox"
if [ -d "$SBX" ]; then
  rm -rf "$SBX"
  echo "Sandbox removido"
fi
```

Expected: Sandbox path desaparece. Obsidian recria se ela acessar Help > Open Sandbox vault no futuro — comportamento esperado, sem impacto.

- [ ] **Step 6: Delete ~/Research/Chaos completamente (já archived)**

Run:
```bash
if [ -d ~/Research/Chaos ]; then
  rm -rf ~/Research/Chaos
  echo "Chaos removido. Backup em ~/Dropbox/vaults-archive-2026-06-05/research-chaos/"
fi
```

Expected: ~/Research/Chaos não existe mais. Archive preserva conteúdo.

- [ ] **Step 7: Re-verify all vaults**

Run:
```bash
find ~ -name ".obsidian" -type d -maxdepth 6 2>/dev/null | sort
```

Expected: Lista reduzida — desapareceram Documents/Obsidian Vault, iCloud anavanzinthesis, Sandbox, Research/Chaos.

- [ ] **Step 8: Commit F5 progress**

Run:
```bash
cd ~/Research
cat > docs/superpowers/progress/2026-06-05-zettelkasten-A-F5-done.md <<'EOF'
# F5 done — Descarte vaults vazios

- Date: 2026-06-05
- Deletados: Documents/Obsidian Vault, iCloud anavanzinthesis/.obsidian, Obsidian Sandbox, Research/Chaos
- Research/Chaos archived em Dropbox antes do delete
EOF

git add docs/superpowers/progress/2026-06-05-zettelkasten-A-F5-done.md
git commit -m "progress: Zettelkasten sub-projeto A F5 (descarte vaults vazios) done"
```

Expected: Commit feito.

---

## Task 3: F3 — Scaffold ~/Zettelkasten/

**Files:**
- Create: `~/Zettelkasten/` (root)
- Create: `~/Zettelkasten/README.md`
- Create: `~/Zettelkasten/_inbox/.gitkeep`
- Create: `~/Zettelkasten/lit/.gitkeep`
- Create: `~/Zettelkasten/zet/.gitkeep`
- Create: `~/Zettelkasten/moc/.gitkeep`
- Create: `~/Zettelkasten/zet/<id>-piloto.md`

- [ ] **Step 1: Verify path libre**

Run:
```bash
[ -d ~/Zettelkasten ] && echo "JÁ EXISTE — abortar" || echo "OK criar"
```

Expected: "OK criar". Se já existe, abortar e investigar.

- [ ] **Step 2: Create directory tree**

Run:
```bash
mkdir -p ~/Zettelkasten/{_inbox,lit,zet,moc}
touch ~/Zettelkasten/_inbox/.gitkeep
touch ~/Zettelkasten/lit/.gitkeep
touch ~/Zettelkasten/zet/.gitkeep
touch ~/Zettelkasten/moc/.gitkeep
ls -la ~/Zettelkasten/
```

Expected: 4 subfolders criados com .gitkeep cada.

- [ ] **Step 3: Write vault README com convenções Z**

Run:
```bash
cat > ~/Zettelkasten/README.md <<'EOF'
# Zettelkasten — Tese Iconocracia

Vault de notas atômicas para tese de doutorado: **alegoria feminina na cultura jurídica
séc. XIX-XX** (PPGD/UFSC, orient. Diego Nunes).

## Escopo

Apenas notas que servem para a tese (Cap 1 + projeto quali, nov/2027). Notas de OAB,
advocacia, iuris-ops, código, pessoal — NÃO entram aqui (ficam em
~/Dropbox/vaults-archive-2026-06-05/, recuperáveis).

## Convenções

### IDs

Formato: `YYMMDDHHMMSS-slug-curto.md`
- Timestamp: garante unicidade técnica
- Slug: legibilidade humana

Exemplo: `260605143027-codificacao-pombalina.md`

Gera ID via: `date +%y%m%d%H%M%S`

### Tipos de nota

- **_inbox/**: fleeting notes. Rascunhos brutos. Processar para lit/ ou zet/ — ou descartar — em até 7 dias.
- **lit/**: literature notes. 1 nota por fonte lida. Sumário PRÓPRIO da fonte
  (parafrasear, não citar literal). Frontmatter com `source: [@bibtex-key]`.
- **zet/**: permanent notes. Atômicas. 1 ideia = 1 nota. 100-400 palavras típico,
  raramente >800. Cada uma tem ≥1 link saindo.
- **moc/**: Maps of Content. Pontos de entrada temáticos. Estilo Luhmann: texto narrativo
  conectando zet/, NÃO listas bullet. Ex: moc/alegoria-feminina.md, moc/codificacao.md.

### Links e citações

- `[[YYMMDDHHMMSS-slug]]` para conexão entre notas Z
- `[@bibtex-key]` para citação ABNT (resolvida em pandoc no compile)
- `#lit`, `#zet`, `#moc` tags para tipo (apenas — sem tags temáticas)

### Frontmatter mínimo

```yaml
---
title: <título da nota>
created: 2026-06-05
type: lit | zet | moc
source: [@bibtex-key]  # apenas em lit/
---
```

### Hard rule até quali

**Vanilla Obsidian. Sem plugins community.** Justificativa: `feedback_no_new_tooling_until_quali`
em ~/.claude/projects/-Users-ana/memory/MEMORY.md. Revisitar pós-quali.

## Roadmap

- A (este vault): triagem ~10k notas legacy → core curado. Em andamento.
- B (próximo): refinamento do método aplicado — MOCs maduros, templates próprios.
- C (final): pipeline Z → outline Cap 1 → draft via pandoc + abnt-format.

Spec completa: ~/Research/docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md
EOF

wc -l ~/Zettelkasten/README.md
```

Expected: README ~60 linhas criado.

- [ ] **Step 4: Write nota piloto para testar workflow**

Run:
```bash
ID=$(date +%y%m%d%H%M%S)
cat > ~/Zettelkasten/zet/${ID}-piloto-zettelkasten.md <<EOF
---
title: Piloto — primeiro teste do Zettelkasten
created: 2026-06-05
type: zet
---

# Piloto — primeiro teste do Zettelkasten

Esta é a primeira nota Z deste vault. Existe para validar:

1. **Convenção de ID** (YYMMDDHHMMSS-slug) — ver [[README]]
2. **Atomicidade** — esta nota fala de UMA coisa só: validação inicial do vault
3. **Link de saída** — qualquer nota Z deve ter ≥1 link. Aqui linka para README.

Se você está lendo isto e ainda não há outras notas Z conectadas, está tudo bem —
F4 (Pull review) começa depois desta task. As primeiras 10 notas Z surgem ao
revisar archive em ~/Dropbox/vaults-archive-2026-06-05/.

## Próximo passo

Abrir Obsidian apontando para ~/Zettelkasten/, confirmar que renderiza link [[README]],
e que .obsidian/ é criado vanilla pelo próprio app.
EOF

ls -la ~/Zettelkasten/zet/
```

Expected: 1 .md piloto + .gitkeep em zet/.

- [ ] **Step 5: Abrir Obsidian para gerar .obsidian/ vanilla**

Manual step:
- Abrir app Obsidian (não via terminal — UI)
- "Open folder as vault" → escolher `~/Zettelkasten/`
- Aguardar Obsidian criar `.obsidian/` config
- Verificar que nota piloto renderiza corretamente (link [[README]] aparece como link)

Run para verificar:
```bash
ls -la ~/Zettelkasten/.obsidian/ 2>&1 | head -5
```

Expected: .obsidian/ existe com workspace.json, app.json, etc. Se não aparecer, abrir Obsidian manualmente até gerar.

- [ ] **Step 6: Commit F3 progress**

Run:
```bash
cd ~/Research
cat > docs/superpowers/progress/2026-06-05-zettelkasten-A-F3-done.md <<'EOF'
# F3 done — Scaffold ~/Zettelkasten/

- Date: 2026-06-05
- Output: ~/Zettelkasten/ (não tracked em git Research — vault próprio)
- Estrutura: _inbox/ lit/ zet/ moc/ + README + 1 nota piloto
- Obsidian vanilla aberto, .obsidian/ gerado
EOF

git add docs/superpowers/progress/2026-06-05-zettelkasten-A-F3-done.md
git commit -m "progress: Zettelkasten sub-projeto A F3 (scaffold) done"
```

Expected: Commit.

---

## Task 4: F2 — Reconciliar 3 Cópias Divergentes do Corpus

**Files:**
- Create: `~/Research/tools/scripts/diff_corpus_vaults.py` (helper)
- Modify: `~/Research/hub/iconocracy-corpus/vault/` (canon — recebe merges únicos)
- Delete: `~/Documents/GitHub/iconocracy-corpus/vault/`
- Delete: `~/projetos/research/hub/iconocracy-corpus/vault/`

**Pre-req**: Task 1 (F1) concluído, com `iconocracy-vault-github/` e `iconocracy-vault-projetos/` snapshot em Dropbox.

- [ ] **Step 1: Write helper Python para diff**

Run:
```bash
mkdir -p ~/Research/tools/scripts/

cat > ~/Research/tools/scripts/diff_corpus_vaults.py <<'PYEOF'
#!/usr/bin/env python3
"""Diff 3 cópias do iconocracy-corpus/vault.

Saída:
  - Notas só no canon
  - Notas só em github (candidatos a merge)
  - Notas só em projetos (candidatos a merge)
  - Notas em todos os 3 mas com hash diferente (conflitos a resolver)

Uso: python diff_corpus_vaults.py
"""
from __future__ import annotations

import hashlib
from pathlib import Path

CANON = Path.home() / "Research" / "hub" / "iconocracy-corpus" / "vault"
GITHUB = Path.home() / "Documents" / "GitHub" / "iconocracy-corpus" / "vault"
PROJETOS = Path.home() / "projetos" / "research" / "hub" / "iconocracy-corpus" / "vault"


def index(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in root.rglob("*.md"):
        rel = p.relative_to(root).as_posix()
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:12]
        out[rel] = h
    return out


def main() -> None:
    if not CANON.exists():
        raise SystemExit(f"Canon path missing: {CANON}")

    a = index(CANON)
    b = index(GITHUB) if GITHUB.exists() else {}
    c = index(PROJETOS) if PROJETOS.exists() else {}

    only_canon = set(a) - set(b) - set(c)
    only_github = set(b) - set(a)
    only_projetos = set(c) - set(a)
    conflicts: list[tuple[str, str, str, str]] = []
    for rel in set(a) & set(b):
        if a[rel] != b[rel]:
            conflicts.append((rel, a[rel], b[rel], c.get(rel, "-")))
    for rel in set(a) & set(c):
        if a[rel] != c[rel] and rel not in {x[0] for x in conflicts}:
            conflicts.append((rel, a[rel], b.get(rel, "-"), c[rel]))

    print(f"Canon ({CANON}): {len(a)} notas")
    print(f"GitHub ({GITHUB}): {len(b)} notas")
    print(f"Projetos ({PROJETOS}): {len(c)} notas")
    print()
    print(f"Only canon: {len(only_canon)}")
    print(f"Only github (CANDIDATOS A MERGE): {len(only_github)}")
    print(f"Only projetos (CANDIDATOS A MERGE): {len(only_projetos)}")
    print(f"Conflitos (mesmo path, hash diferente): {len(conflicts)}")
    print()

    if only_github:
        print("=== ONLY GITHUB (review e decidir merge) ===")
        for rel in sorted(only_github)[:50]:
            print(f"  {rel}")
        if len(only_github) > 50:
            print(f"  ... e mais {len(only_github) - 50}")
        print()

    if only_projetos:
        print("=== ONLY PROJETOS (review e decidir merge) ===")
        for rel in sorted(only_projetos)[:50]:
            print(f"  {rel}")
        if len(only_projetos) > 50:
            print(f"  ... e mais {len(only_projetos) - 50}")
        print()

    if conflicts:
        print("=== CONFLITOS (hash diferente entre cópias) ===")
        for rel, hc, hg, hp in conflicts[:50]:
            print(f"  {rel}  canon={hc}  github={hg}  projetos={hp}")


if __name__ == "__main__":
    main()
PYEOF

chmod +x ~/Research/tools/scripts/diff_corpus_vaults.py
ls -la ~/Research/tools/scripts/diff_corpus_vaults.py
```

Expected: Script criado executável.

- [ ] **Step 2: Run helper para inventário**

Run:
```bash
cd ~/Research
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python tools/scripts/diff_corpus_vaults.py
```

Expected: Saída listando counts, only-github, only-projetos, conflicts. Salvar output para referência:
```bash
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python tools/scripts/diff_corpus_vaults.py \
  > docs/superpowers/progress/2026-06-05-corpus-diff.txt
```

- [ ] **Step 3: Dry-run rsync merge das únicas de github e projetos para canon**

Run:
```bash
echo "=== DRY RUN: github → canon ==="
rsync -aHpn ~/Documents/GitHub/iconocracy-corpus/vault/ \
            ~/Research/hub/iconocracy-corpus/vault/ \
  --ignore-existing 2>&1 | head -30

echo ""
echo "=== DRY RUN: projetos → canon ==="
rsync -aHpn ~/projetos/research/hub/iconocracy-corpus/vault/ \
            ~/Research/hub/iconocracy-corpus/vault/ \
  --ignore-existing 2>&1 | head -30
```

Expected: Lista de arquivos QUE seriam copiados (sem mover ainda). Confere com lista de "only github" e "only projetos" do diff script.

- [ ] **Step 4: Resolver conflitos manualmente (se houver)**

If `diff_corpus_vaults.py` reportou conflitos:
- Para cada path em conflito, abrir as 3 versões lado a lado
- Decidir qual mantém em canon (usualmente a mais recente por timestamp do file, OU a com mais conteúdo)
- Editar manualmente em `~/Research/hub/iconocracy-corpus/vault/<path>` antes do merge

If sem conflitos: pular para Step 5.

- [ ] **Step 5: Execute merge real (sem --ignore-existing apenas para únicas)**

Run:
```bash
# Merge: copia apenas notas que NÃO existem em canon (--ignore-existing)
rsync -aHp --ignore-existing \
  ~/Documents/GitHub/iconocracy-corpus/vault/ \
  ~/Research/hub/iconocracy-corpus/vault/

rsync -aHp --ignore-existing \
  ~/projetos/research/hub/iconocracy-corpus/vault/ \
  ~/Research/hub/iconocracy-corpus/vault/

# Conta final
find ~/Research/hub/iconocracy-corpus/vault -name "*.md" | wc -l | xargs echo "Canon agora:"
```

Expected: Canon recebeu únicas das outras 2 cópias. Count deve refletir: canon_inicial + only_github + only_projetos.

- [ ] **Step 6: Validar canon com schema validation (hook existente)**

Run:
```bash
cd ~/iconocracy-corpus
/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python tools/scripts/validate_schemas.py 2>&1 | tail -10
```

Expected: Validation pass. Se falhar, há .jsonl quebrado entre merges — investigar antes de Step 7.

- [ ] **Step 7: Commit canon merged**

Run:
```bash
cd ~/Research
git add hub/iconocracy-corpus/vault/
git status --short | head -20
git commit -m "fix: reconciliar 3 cópias iconocracy-corpus/vault em canon

Merge --ignore-existing de:
  - ~/Documents/GitHub/iconocracy-corpus/vault/  (divergente 6d)
  - ~/projetos/research/hub/iconocracy-corpus/vault/  (divergente 12d)

Backup das 2 cópias em ~/Dropbox/vaults-archive-2026-06-05/ (F1).
Schema validation pass."
```

Expected: Commit feito refletindo merges.

- [ ] **Step 8: Delete 2 cópias divergentes (Dropbox archive já tem)**

Run:
```bash
# Triple-check archive existe antes
ls -la ~/Dropbox/vaults-archive-2026-06-05/iconocracy-vault-github/ | head -3
ls -la ~/Dropbox/vaults-archive-2026-06-05/iconocracy-vault-projetos/ | head -3

# Se OK, deletar
rm -rf ~/Documents/GitHub/iconocracy-corpus/vault/
rm -rf ~/projetos/research/hub/iconocracy-corpus/vault/

# Verify
[ ! -d ~/Documents/GitHub/iconocracy-corpus/vault ] && echo "GitHub copy: gone"
[ ! -d ~/projetos/research/hub/iconocracy-corpus/vault ] && echo "Projetos copy: gone"
```

Expected: 2 paths não existem mais. Archive Dropbox permanece.

- [ ] **Step 9: Commit F2 progress**

Run:
```bash
cd ~/Research
cat > docs/superpowers/progress/2026-06-05-zettelkasten-A-F2-done.md <<'EOF'
# F2 done — Reconciliar 3 cópias corpus

- Date: 2026-06-05
- Merges: únicas de github e projetos para canon
- Conflicts: resolvidos manualmente (se houver, listados no Step 4)
- Schema validation: passou
- Deleted: ~/Documents/GitHub/iconocracy-corpus/vault, ~/projetos/.../vault
- Backup: ~/Dropbox/vaults-archive-2026-06-05/iconocracy-vault-{github,projetos}/
EOF

git add docs/superpowers/progress/2026-06-05-zettelkasten-A-F2-done.md tools/scripts/diff_corpus_vaults.py
git commit -m "progress: Zettelkasten sub-projeto A F2 (reconcile corpus) done"
```

Expected: Commit.

---

## Task 5: F4 — Pull Review por Source (iterativo, 5-10 sessões)

**Files:**
- Modify: `~/Zettelkasten/zet/<new-ids>.md` (notas Z migradas, conforme review)
- Modify: `~/Zettelkasten/lit/<new-ids>.md` (literature notes migradas)
- Modify: `~/Zettelkasten/moc/<new-ids>.md` (MOCs criadas conforme tópicos emergem)
- Modify: `~/Dropbox/vaults-archive-2026-06-05/<source>/_ARCHIVE_README.md` (status="reviewed YYYY-MM-DD")

**Pre-req**: Tasks 1, 3 concluídos. Task 4 (F2) idealmente concluído antes de wikis (Sources 4-6).

**Estratégia**: 1 source por sessão. Ordem sugerida (mais valioso primeiro):
1. iconocracy-wiki-research (4d antiga, conteúdo curado)
2. downloads-analise (risco resolvido por F1, mas conteúdo provavelmente alto valor tese)
3. research-root (volume alto, exclui já-migrado)
4. iconocracy-wiki-github + iconocracy-wiki-projetos (dedup vs wiki-research)
5. documents-linux (fóssil, baixa prioridade)

**Procedure template (aplicar a cada source)**:

- [ ] **Step 1: Ler _ARCHIVE_README.md da source**

Run:
```bash
SRC=iconocracy-wiki-research  # ← MUDAR conforme source da sessão
cat ~/Dropbox/vaults-archive-2026-06-05/$SRC/_ARCHIVE_README.md
```

Expected: Visualizar origem, count, status.

- [ ] **Step 2: Inventariar clusters (top-level dirs ou groups de filenames)**

Run:
```bash
SRC=iconocracy-wiki-research
ls -la ~/Dropbox/vaults-archive-2026-06-05/$SRC/ | head -30
find ~/Dropbox/vaults-archive-2026-06-05/$SRC/ -maxdepth 2 -type d | head -20
```

Expected: Lista de subpastas e arquivos top-level. Identificar 3-5 clusters temáticos visualmente.

- [ ] **Step 3: Para cada cluster, decidir destino**

Manual. Para cada cluster identificado, aplicar critério do README do vault Z:
- ✓ MIGRA — fonte primária / conceito-chave / fragmento tese / corpus
- ✗ NÃO MIGRA — OAB, advocacia, código, pessoal
- ? CASO DUVIDOSO — metodológicas, DIR410346

Anotar decisão em rascunho local (e.g., scratch file no $CLAUDE_JOB_DIR).

- [ ] **Step 4: Para clusters MIGRA — criar notas Z atomizadas**

Para cada nota legacy que merece migrar:

```bash
# Gerar ID
ID=$(date +%y%m%d%H%M%S)

# Identificar tipo (lit | zet | moc)
TYPE=lit  # exemplo: nota sobre fonte lida

# Slug curto descrevendo conceito atômico
SLUG=hespanha-cultura-juridica

# Criar nota nova com frontmatter
cat > ~/Zettelkasten/$TYPE/${ID}-${SLUG}.md <<'EOF'
---
title: <título>
created: 2026-06-05
type: lit
source: [@hespanha2003]
---

# <título>

<conteúdo atômico, parafraseado, com ≥1 [[link]] saindo>
EOF
```

**IMPORTANTE**: nota Z NÃO é copy-paste literal. É reescrita guiada por critério tese — atomizada (1 ideia), com slug humano, com ≥1 link saindo. Esta é a parte intelectual demorada.

- [ ] **Step 5: Self-check de qualidade Z**

Para cada nota recém-criada, verificar:
- [ ] Tem ID timestamp único
- [ ] Frontmatter completo (title, created, type, source se lit)
- [ ] É 1 ideia só (não 3 misturadas)
- [ ] Tem ≥1 link saindo (`[[id]]` ou `[@bibtex]`)
- [ ] Está no folder certo (lit/zet/moc)
- [ ] 100-400 palavras (raramente >800)

Se falhar qualquer item: refatorar a nota antes de prosseguir.

- [ ] **Step 6: Marcar source como reviewed**

Run:
```bash
SRC=iconocracy-wiki-research  # ← mesma source do Step 1
TODAY=$(date +%Y-%m-%d)
README=~/Dropbox/vaults-archive-2026-06-05/$SRC/_ARCHIVE_README.md

# Update status linha
sed -i.bak "s/Status\*\*: aguardando review F4/Status**: reviewed $TODAY/" $README
grep "Status" $README
rm $README.bak
```

Expected: Status do README mudou de "aguardando review F4" para "reviewed YYYY-MM-DD".

- [ ] **Step 7: Contar notas Z criadas nesta sessão**

Run:
```bash
echo "Notas Z criadas hoje:"
find ~/Zettelkasten/{lit,zet,moc} -name "*.md" -newer ~/Zettelkasten/README.md | wc -l | xargs
find ~/Zettelkasten/{lit,zet,moc} -name "*.md" -newer ~/Zettelkasten/README.md
```

Expected: N notas criadas — anotar para tracking de progresso ao critério "A done" (≥10).

- [ ] **Step 8: Commit do progresso da sessão**

Run:
```bash
cd ~/Research
DATE=$(date +%Y-%m-%d)
SRC=iconocracy-wiki-research  # ← source dessa sessão
cat > docs/superpowers/progress/${DATE}-zettelkasten-A-F4-${SRC}.md <<EOF
# F4 progress — $SRC reviewed

- Date: $DATE
- Source: $SRC
- Notas migradas: <preencher>
- Decisões por cluster: <preencher>
- Status archive: reviewed
EOF

git add docs/superpowers/progress/${DATE}-zettelkasten-A-F4-${SRC}.md
git commit -m "progress: F4 review $SRC"
```

Expected: Commit por source-session.

**Repetir Tasks 5 Steps 1-8 para cada source** até todas 6 sources Prioridade 3 (Source list em Task 1 step 3) estarem com status="reviewed".

---

## Task 6: F6 — Decidir Destino do ~/Research como Vault

**Files:**
- Delete (optional): `~/Research/.obsidian/`
- Modify: `~/Research/.gitignore` (se manter .obsidian para outro uso)

**Pre-req**: Task 5 (F4) com todas Prioridade 3 reviewed.

- [ ] **Step 1: Confirm nothing in ~/Research raiz precisa de vault**

Run:
```bash
# Listar todos .md em ~/Research raiz (excluindo sub-vaults migrados)
find ~/Research -maxdepth 3 -name "*.md" \
  -not -path "*/hub/iconocracy-corpus/*" \
  -not -path "*/.git/*" 2>/dev/null | head -20

echo "---"
echo "Total: $(find ~/Research -maxdepth 3 -name "*.md" \
  -not -path "*/hub/iconocracy-corpus/*" \
  -not -path "*/.git/*" 2>/dev/null | wc -l | xargs)"
```

Expected: Se baixo (<50) e todos já reviewed em F4, .obsidian raiz pode sair. Se ainda há .md significativos não-revisados, F4 não está done para Research raiz — voltar.

- [ ] **Step 2: Decidir e executar**

Decisão binária:
- (a) Fechar Research como vault: remover .obsidian/ raiz
- (b) Manter Research como vault separado (não-Z): documentar no CLAUDE.md repo

Run para (a):
```bash
rm -rf ~/Research/.obsidian
ls -la ~/Research/.obsidian 2>&1 | head -2
```

Expected: ".obsidian: No such file or directory"

OR run para (b):
```bash
echo "Mantendo ~/Research/.obsidian como vault legacy não-Z" >> ~/Research/README.md
```

- [ ] **Step 3: Commit F6 progress**

Run:
```bash
cd ~/Research
cat > docs/superpowers/progress/2026-06-05-zettelkasten-A-F6-done.md <<EOF
# F6 done — Research raiz vault decision

- Date: $(date +%Y-%m-%d)
- Decisão: <(a) ou (b)>
- Estado: <descrição>
EOF

git add docs/superpowers/progress/2026-06-05-zettelkasten-A-F6-done.md
[ -d .obsidian ] && git add -u .obsidian || true
git commit -m "progress: Zettelkasten sub-projeto A F6 (Research vault decision) done"
```

Expected: Commit.

---

## Task 7: A Done Checkpoint

**Files:** —

- [ ] **Step 1: Verify all "A done" criteria**

Run:
```bash
echo "== A done criteria check =="

# 1. ~/Zettelkasten/ ≥10 notas Z
COUNT_Z=$(find ~/Zettelkasten/{lit,zet,moc} -name "*.md" 2>/dev/null | wc -l | xargs)
echo "[1] Notas Z: $COUNT_Z (esperado ≥10)"

# 2. Fontes legacy snapshot em Dropbox com README
COUNT_SOURCES=$(ls ~/Dropbox/vaults-archive-2026-06-05/ | wc -l | xargs)
echo "[2] Sources arquivadas: $COUNT_SOURCES"

# 3. 3 cópias corpus → 1 canon
[ -d ~/Documents/GitHub/iconocracy-corpus/vault ] && echo "[3] FAIL: github copy ainda existe"
[ -d ~/projetos/research/hub/iconocracy-corpus/vault ] && echo "[3] FAIL: projetos copy ainda existe"
[ -d ~/Research/hub/iconocracy-corpus/vault ] && echo "[3] OK: apenas canon resta"

# 4. ~/Downloads sem vaults
find ~/Downloads -name ".obsidian" -type d 2>/dev/null | head -3 || echo "[4] OK: sem vaults em Downloads"

# 5. Vaults vazios deletados
find ~ -name ".obsidian" -type d -maxdepth 6 2>/dev/null | sort
echo "(Deve ter apenas: ~/Zettelkasten/.obsidian, ~/Research/hub/iconocracy-corpus/vault/.obsidian,"
echo " ~/Research/hub/iconocracy-corpus/wiki/.obsidian — ou menos se F6 fechou Research raiz)"

# 6. F6 decisão registrada
ls ~/Research/docs/superpowers/progress/2026-06-05-zettelkasten-A-F6-done.md && echo "[6] OK: F6 doc existe"
```

Expected: Todos critérios validam. Se algum falha, voltar à fase relevante.

- [ ] **Step 2: Atualizar memória persistente**

Run:
```bash
cat > ~/.claude/projects/-Users-ana/memory/project_zettelkasten_A_done.md <<'EOF'
---
name: zettelkasten-A-done
description: Sub-projeto A (triagem vaults para Zettelkasten) concluído; ~/Zettelkasten/ vault canon ativo, archive em ~/Dropbox/vaults-archive-2026-06-05/, 3 cópias corpus reconciliadas
metadata:
  type: project
---

## Sub-projeto A concluído

**Data**: <preencher>
**Spec**: ~/Research/docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md
**Plan**: ~/Research/docs/superpowers/plans/2026-06-05-zettelkasten-triagem-implementation.md

### Estado final

- ~/Zettelkasten/ : vault canon Z com N notas Z migradas
- ~/Dropbox/vaults-archive-2026-06-05/ : 8 sources com READMEs status="reviewed"
- ~/Research/hub/iconocracy-corpus/vault/ : canon único (2 divergentes deletadas)
- Vaults vazios removidos

### Próximo

Quando Z tiver ~50-100 notas, abrir brainstorming sub-projeto B (método Z aplicado).

**Why**: parte 1/3 do sistema Z completo. Pré-requisito de B e C.
**How to apply**: para questões sobre vault, default é ~/Zettelkasten/. Para corpus
iconográfico, default é ~/Research/hub/iconocracy-corpus/vault/. Archive read-only,
puxar se necessário.
EOF

# Adicionar ao MEMORY.md
echo "- [Zettelkasten A done](project_zettelkasten_A_done.md) — $(date +%Y-%m-%d) — Sub-projeto A concluído; ~/Zettelkasten/ ativo, archive Dropbox, 3 cópias corpus reconciliadas" >> ~/.claude/projects/-Users-ana/memory/MEMORY.md

cat ~/.claude/projects/-Users-ana/memory/MEMORY.md | tail -3
```

Expected: Memory file criada e MEMORY.md atualizado.

- [ ] **Step 3: Final commit**

Run:
```bash
cd ~/Research
cat > docs/superpowers/progress/2026-06-05-zettelkasten-A-DONE.md <<EOF
# Sub-projeto A — DONE

- Date: $(date +%Y-%m-%d)
- Spec: docs/superpowers/specs/2026-06-05-zettelkasten-triagem-design.md
- Plan: docs/superpowers/plans/2026-06-05-zettelkasten-triagem-implementation.md
- Critério done validado via Task 7 Step 1
- Memória persistente atualizada

## Próximo

Brainstorming sub-projeto B quando ~/Zettelkasten/ tiver ~50-100 notas Z e workflow rodando.
EOF

git add docs/superpowers/progress/2026-06-05-zettelkasten-A-DONE.md
git commit -m "done: Zettelkasten sub-projeto A (triagem)"
```

Expected: Commit final do sub-projeto.

---

## Self-Review (completed inline)

**Spec coverage check** — todas as seções do spec endereçadas:
- Arquitetura target (~/Zettelkasten/) → Task 3 ✓
- Archive Dropbox → Task 1 ✓
- Critério "serve para tese?" → Task 3 Step 3 (README) + Task 5 Step 3 ✓
- Convenções Z (IDs, links, frontmatter) → Task 3 Step 3 ✓
- Procedimento archive → Task 1 Steps 4-6 ✓
- Procedimento review → Task 5 Steps 3-5 ✓
- Reconciliação corpus → Task 4 ✓
- Critério "A done" → Task 7 ✓
- Riscos & mitigações → embutidos em verify steps

**Placeholder scan**: Sem TBD/TODO no flow principal. `<preencher>` em campos de progress doc é esperado (preenchido durante execução, não no plano).

**Type/path consistency**: paths absolutos consistentes (~/Zettelkasten/, ~/Dropbox/vaults-archive-2026-06-05/, ~/Research/...). Bash variable names (ARCH, SRC, ID, TYPE, SLUG) consistentes entre steps que os reusam.
