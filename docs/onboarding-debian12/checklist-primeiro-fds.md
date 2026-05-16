# Checklist — Primeiro Fim de Semana com o Notebook

> **Para imprimir, riscar e arquivar.** Dependências numeradas: cada item `→ N` exige que o item N já esteja concluído. Estimativa de tempo entre parênteses inclui *cooldown* — não vale terminar todos os itens de bloco em 50% do tempo previsto.
>
> **Pré-condição crítica:** revogue a credencial DM-001 (item interno) o mais cedo possível — idealmente na **terça-feira de manhã**, antes mesmo do notebook chegar. Reescrita de histórico vem só no domingo.

---

## Terça (chegada do notebook, ~1h)

- [ ] **T-1 ·** Confirmar BIOS / Secure Boot / dual boot — checar partições do SSD. (15 min)
- [ ] **T-2 ·** Conectar à rede WiFi de casa; testar `ping 1.1.1.1`. (5 min)
- [ ] **T-3 ·** Executar `scripts/00-bootstrap-apt.sh` (`sudo bash scripts/00-bootstrap-apt.sh`). (20 min — sobretudo download)
- [ ] **T-4 ·** Configurar Syncthing (apenas instalação e pareamento com Mac antigo, sem aguardar sync completo). → T-3 (20 min)
- [ ] **T-5 ·** **AÇÃO SEPARADA, NÃO LIGADA AO NOTEBOOK:** revogar token DM-001 no console do provedor. **Faça hoje.** Anote data/hora em papel.

**Não tentar mais nada na terça.** Sync inicial do vault leva horas; deixar rodando à noite.

---

## Quarta a sexta (passivo)

- [ ] Sync Syncthing terminar (verificar `localhost:8384`).
- [ ] Mac antigo continua sendo a máquina primária.
- [ ] Ler `manual.md` § Camada 1 com calma (~1h).
- [ ] Listar credenciais e mirrors antes do sábado: que tokens existem, em quantos lugares.

---

## Sábado de manhã (≈3h)

- [ ] **S1-1 ·** Atualização final: `sudo apt update && sudo apt upgrade -y`. (15 min) → T-3
- [ ] **S1-2 ·** Gerar par SSH para GitHub: `ssh-keygen -t ed25519 -C "ana@vaio-debian-2026" -f ~/.ssh/id_ed25519_github`. (10 min) → S1-1
- [ ] **S1-3 ·** Instalar GitHub CLI; `gh auth login` via SSH; adicionar `id_ed25519_github.pub`. (15 min) → S1-2
- [ ] **S1-4 ·** Clonar monorepo: `git clone git@github.com:anavvanzin/iconocracy-corpus.git ~/iconocracy-corpus`. (30 min — repo grande) → S1-3
- [ ] **S1-5 ·** Confirmar `git status` limpo e branches esperados. → S1-4
- [ ] **S1-6 ·** Configurar `git config --global` (user.name, user.email, signingkey se for o caso). → S1-5

**Café e pausa.** Não pular.

---

## Sábado à tarde (≈3h)

- [ ] **S2-1 ·** Executar `scripts/01-claude-code.sh`. Verificar com `claude --version` e `claude doctor`. (15 min) → S1-1
- [ ] **S2-2 ·** Validar criptograficamente: `gpg --fingerprint security@anthropic.com` deve casar com `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`. (10 min) → S2-1
- [ ] **S2-3 ·** Primeiro `claude` + `/login` via browser. (10 min) → S2-1
- [ ] **S2-4 ·** Copiar `~/.claude/CLAUDE.md` do Mac (via Syncthing) para o Debian. (5 min) → T-4
- [ ] **S2-5 ·** Abrir Claude no diretório do monorepo: `cd ~/iconocracy-corpus && claude`. Conferir que o `CLAUDE.md` do projeto foi carregado. (5 min) → S2-3, S1-4
- [ ] **S2-6 ·** Executar `scripts/03-python-conda.sh`. (40 min — env conda é grande) → S1-4
- [ ] **S2-7 ·** Ativar env: `conda activate iconocracia`; conferir `python -c "import sys; print(sys.version)"` e bibliotecas-chave. (10 min) → S2-6
- [ ] **S2-8 ·** Instalar `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`. (5 min) → S1-1
- [ ] **S2-9 ·** Instalar `nvm` + Node LTS: ver § 2.6 do manual. (15 min) → S1-1

---

## Sábado à noite (≈1h)

- [ ] **S3-1 ·** Instalar Obsidian (`.deb`). (10 min) → S1-1
- [ ] **S3-2 ·** Abrir Obsidian; apontar para o vault sincronizado por Syncthing; aceitar plugins essenciais. (20 min) → S3-1, T-4
- [ ] **S3-3 ·** Instalar plugins Tasks, Dataview, Templater, Citations *ou* Zotero Integration. (15 min) → S3-2
- [ ] **S3-4 ·** **Pré-pausa de domingo:** abrir o console do provedor DM-001 e *confirmar* que o token revogado em T-5 retorna `401` num teste manual. (5 min)
- [ ] **S3-5 ·** Dormir. **Domingo é dia denso. Não comece o domingo cansada.**

---

## Domingo de manhã (≈3h)

- [ ] **D1-1 ·** Executar `scripts/02-academic-stack.sh` (Zotero, Syncthing já está pronto, VS Code, gh, Starship). (40 min) → S1-1
- [ ] **D1-2 ·** Configurar Zotero: pasta vinculada `~/Documents/iconocracy-corpus/biblio/`. (10 min) → D1-1
- [ ] **D1-3 ·** Instalar Better BibTeX + ZotMoov; importar biblioteca do Mac (via Syncthing). (30 min) → D1-2
- [ ] **D1-4 ·** Abrir VS Code; instalar extensões mínimas (ver § 2.8 do manual). (10 min) → D1-1
- [ ] **D1-5 ·** Executar `scripts/04-rclone-drive.sh` para instalar e configurar rclone com remote `drive-iconocracy`. (30 min — inclui OAuth) → S1-1
- [ ] **D1-6 ·** Validar acesso: `rclone lsd drive-iconocracy:ICONOCRACIA`. (5 min) → D1-5
- [ ] **D1-7 ·** Dry-run do bisync: `rclone bisync ~/iconocracy-corpus/data/raw/ drive-iconocracy:ICONOCRACIA/data/raw/ --resync --dry-run`. **Não executar sem `--dry-run` ainda.** (10 min) → D1-6

---

## Domingo à tarde (≈3h)

> **Esta é a janela crítica DM-001.** Faça **um trabalho de cada vez**, sem multitarefa.

- [ ] **D2-1 ·** Confirmar **mais uma vez** que o token DM-001 está revogado (`curl` manual com 401). (5 min)
- [ ] **D2-2 ·** Backup defensivo: `tar -czf ~/iconocracy-corpus-backup-$(date +%F).tar.gz ~/iconocracy-corpus/`. (10 min)
- [ ] **D2-3 ·** Mapear segredo no histórico: `git log --all --full-history -S '<prefixo>' --source --remotes`. Anotar commits e arquivos. (15 min)
- [ ] **D2-4 ·** Clonar fresh-mirror para `git-filter-repo`: ver § 3.4 passo 4 do manual. (10 min) → D2-2
- [ ] **D2-5 ·** Executar `scripts/05-secrets-rotation.sh` em modo `--dry-run` primeiro; depois em modo real. (30 min) → D2-4
- [ ] **D2-6 ·** `git push --force --mirror` para o remote real. **Confirme três vezes antes.** (5 min) → D2-5
- [ ] **D2-7 ·** Re-clonar repo limpo em `~/iconocracy-corpus`; renomear o antigo como `~/iconocracy-corpus.preDM001-YYYY-MM-DD`. (15 min) → D2-6
- [ ] **D2-8 ·** Emitir token NOVO no provedor; salvar em `~/.config/iconocracy/.env` (chmod 600). (10 min)
- [ ] **D2-9 ·** Abrir ticket suporte GitHub para purge de caches; anexar evidências. (20 min) → D2-6
- [ ] **D2-10 ·** Atualizar mirror Hugging Face se aplicável (§ 3.5 do manual). (30 min) → D2-7

---

## Domingo à noite (≈2h)

- [ ] **D3-1 ·** Primeira sincronização real `rclone bisync --resync` (sem `--dry-run`). (15 min — ou mais se data/raw/ for grande) → D1-7, D2-7
- [ ] **D3-2 ·** Auditoria de nomes: `python tools/scripts/audit_corpus_names.py data/raw/`. Esperado: `OK`. (5 min) → D3-1
- [ ] **D3-3 ·** Configurar integração Notion: criar/conferir DB1; copiar IDs para `~/.config/iconocracy/.env`. (15 min) → D2-8
- [ ] **D3-4 ·** Adicionar scaffold `tools/scripts/notion_sync.py` (do manual); `python tools/scripts/notion_sync.py --dry-run --limit 5`. (15 min) → D2-7, D3-3
- [ ] **D3-5 ·** Validar pipeline tese: `make -C vault/tese/ docx`. (10 min — primeira execução baixa fontes) → S2-7
- [ ] **D3-6 ·** Validar pipeline tese: `make -C vault/tese/ pdf`. (15 min) → D3-5
- [ ] **D3-7 ·** Instalar pre-commit + gitleaks; rodar `pre-commit run --all-files`. (15 min) → D2-7
- [ ] **D3-8 ·** Commit do pacote de onboarding: `git add docs/onboarding-debian12/ && git commit -m "docs: manual de onboarding Debian 12"`. (5 min)
- [ ] **D3-9 ·** Criar `docs/security/DM-001-resolution.md` com timeline da remediação. (15 min) → D2-9
- [ ] **D3-10 ·** `claude /cost`: anotar custo total do fim de semana em `tese/.cost-log.md`. (5 min)

---

## Tabela final — Definition of done

> Antes de fechar o domingo, os comandos abaixo devem todos retornar como esperado. Se algum falhar, **não** declare o setup completo: marque um *follow-up* para a semana.

| # | Verificação | Esperado |
|---|---|---|
| V01 | `claude --version` | ≥ 2.1.89 |
| V02 | `claude doctor` | sem warnings críticos |
| V03 | `gpg --fingerprint security@anthropic.com` | termina em `1A7E CACE` |
| V04 | `conda activate iconocracia && python -V` | `Python 3.10+` |
| V05 | `wc -l ~/iconocracy-corpus/data/processed/records.jsonl` | número esperado de registros |
| V06 | `make -C ~/iconocracy-corpus/vault/tese/ docx` | sem erro |
| V07 | `make -C ~/iconocracy-corpus/vault/tese/ pdf` | sem erro |
| V08 | `rclone lsd drive-iconocracy:ICONOCRACIA` | lista subpastas |
| V09 | `python tools/scripts/audit_corpus_names.py data/raw/` | `OK` |
| V10 | Notion `notion_sync.py --dry-run --limit 5` | 5 linhas, sem `401` |
| V11 | `curl -H "Authorization: Bearer <chave-antiga>" …` | `401` |
| V12 | `git commit -m "test"` com fake key no body | bloqueado pelo gitleaks |
| V13 | `/mcp` na Claude Code | `gallica` em `connected` |
| V14 | Syncthing — criar nota no Mac, conferir aparecer no Debian em <120s | aparece |

---

## Sinais de que **não** está pronto e merece adiar para semana seguinte

- `claude doctor` reporta warning não trivial → § 1.10 do manual.
- `rclone bisync --dry-run` lista mudanças que você não reconhece → investigar antes de executar de verdade.
- Algum `*.sync-conflict-*` apareceu no vault Obsidian → resolver antes de continuar editando.
- Você está cansada e o item D2-6 (`git push --force --mirror`) ainda não foi executado → pare, durma, retome segunda.

**Cansaço é o maior fator de risco do fim de semana. O notebook não vai a lugar nenhum.**
