# F2 closed — Reconciliar 3 cópias corpus

- Date: 2026-06-05
- Helper: ~/Research/tools/scripts/diff_corpus_vaults.py (com NFC normalize após bug)
- Diff inicial: 16 únicos github (drafts capítulos tese), 133 únicos projetos
- Após NFC normalize: 16 únicos github, **0 únicos projetos** (eram falsos-positivos por unicode)
- Conflitos: 5 (todos resolvidos a favor canon via --ignore-existing)
  - 3 onde canon é mais recente/maior
  - 2 (SBRICCOLI/BATISTA) onde projetos é mais recente mas MENOR — flagged para revisão manual
- Canon: 622 → 638 notas (+16 drafts tese resgatados)
- Commit no corpus repo: ca9b424 (branch reconcile/ssd-scripts-2026-06-04)

## FECHADO em 2026-06-22

- Step 8 executado: os dois diretórios duplicados já não existem no filesystem.
- Archive no Dropbox (`~/Dropbox/vaults-archive-2026-06-05/iconocracy-vault-github/` e
  `iconocracy-vault-projetos/`) está preservado.
- Verificação: `ls` nos caminhos originais retorna "No such file or directory".
- Status: F2 não tem pendências técnicas.
