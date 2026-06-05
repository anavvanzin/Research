# F2 done (parcial) — Reconciliar 3 cópias corpus

- Date: 2026-06-05
- Helper: ~/Research/tools/scripts/diff_corpus_vaults.py (com NFC normalize após bug)
- Diff inicial: 16 únicos github (drafts capítulos tese), 133 únicos projetos
- Após NFC normalize: 16 únicos github, **0 únicos projetos** (eram falsos-positivos por unicode)
- Conflitos: 5 (todos resolvidos a favor canon via --ignore-existing)
  - 3 onde canon é mais recente/maior
  - 2 (SBRICCOLI/BATISTA) onde projetos é mais recente mas MENOR — flagged para revisão manual
- Canon: 622 → 638 notas (+16 drafts tese resgatados)
- Commit no corpus repo: ca9b424 (branch reconcile/ssd-scripts-2026-06-04)

## NÃO executado (aguardando Dropbox sync verde)

- Step 8: delete ~/Documents/GitHub/iconocracy-corpus/vault/ e ~/projetos/research/hub/iconocracy-corpus/vault/

Critério para prosseguir: Dropbox menu bar mostra ícone VERDE/sincronizado, indicando
que os 8.6 GB de archive (incluindo iconocracy-vault-github/ e iconocracy-vault-projetos/)
estão na cloud.

Comando para confirmar e completar F2:
```
rm -rf ~/Documents/GitHub/iconocracy-corpus/vault/
rm -rf ~/projetos/research/hub/iconocracy-corpus/vault/
```
