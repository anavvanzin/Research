# Onboarding Debian 12 — Pacote Operacional

> Material de instalação e migração para o notebook VAIO FE16 (Ryzen 7-5825U, 32 GB RAM, 512 GB SSD) com Debian 12. Destina-se à pesquisa doutoral *ICONOCRACIA — Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)*, PPGD/UFSC.
>
> Autora: Ana Vanzin · Data de redação: 2026-05-11 · Janela de execução prevista: terça (chegada do notebook) → domingo seguinte.

## Como ler este pacote

| Arquivo | Para quê |
|---|---|
| [`manual.md`](manual.md) | Documento operacional principal, três camadas (Claude Code CLI, stack acadêmica, integração GitHub-Drive-Notion). Leitura corrida na primeira passada; consulta indexada depois. |
| [`checklist-primeiro-fds.md`](checklist-primeiro-fds.md) | Roteiro tático sábado-domingo, dependências numeradas, para ser impresso e riscado. |
| [`scripts/`](scripts/) | Scripts Bash idempotentes que automatizam blocos longos do manual. Todos têm cabeçalho `# usage:` e usam `set -euo pipefail`. |
| [`refs/fontes-consultadas.md`](refs/fontes-consultadas.md) | URLs, versões, *fingerprints* de chaves GPG e datas de consulta — referência única para checar drift de informação. |

## Convenção de marcação

Em todo o manual, comandos vêm anotados:

- **(U) — Universal:** funciona em Debian 12 *out-of-the-box*.
- **(C) — Contextual:** depende de configuração prévia descrita em outra seção do manual; a dependência é nomeada.
- **(J) — Julgamento:** envolve escolha metodológica; o manual oferece alternativas com critérios.

## Ordem de execução recomendada

1. Ler `manual.md` § *Frontmatter* e § *Camada 1 — Claude Code CLI* na noite de segunda (antes do notebook chegar).
2. Na terça, **executar apenas** `scripts/00-bootstrap-apt.sh` e configurar Syncthing (etapa do manual § 2.2).
3. Reservar sábado e domingo para o checklist completo.
4. Não pular o item 11 do checklist (revogação imediata da credencial **DM-001**) por nenhum motivo.

## Atualizações

Este pacote é versionado junto da meta-workspace `~/Research/`. Após cada execução de manutenção significativa, atualizar:

- `refs/fontes-consultadas.md` com a data da nova consulta;
- a tabela de verificação (§ *Definition of done* do `manual.md`) refletindo o estado real da máquina.
