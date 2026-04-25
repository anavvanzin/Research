# Research Workspace

Raiz canônica do ecossistema de pesquisa em `/Users/ana/Research`.

## Produção intelectual — acesso direto

O trabalho principal vive dentro do hub, mas estes são os caminhos de acesso rápido:

| O quê | Caminho |
| --- | --- |
| **Capítulos da tese** | `hub/iconocracy-corpus/vault/tese/` (introdução → conclusão) |
| **Manuscrito & revisões** | `hub/iconocracy-corpus/tese/manuscrito/` · `tese/revisoes/` |
| **Entrega mais recente** | `hub/iconocracy-corpus/tese/Entrega_Orientador_Mar2026_FINAL/` |
| **Rascunhos de artigos** | `hub/iconocracy-corpus/vault/tese/rascunhos-artigos/` (6 drafts) |
| **Artigo publicável** | `hub/iconocracy-corpus/tese/artigos/dessexualization-threshold-draft-v1.md` |
| **Notebooks estatísticos** | `hub/iconocracy-corpus/notebooks/` (01–04: exploratória → correspondência) |
| **Notebooks Atlas** | `pipelines/Atlas/notebooks/` (corpus, estatística, kappa) |
| **Corpus canônico** | `hub/iconocracy-corpus/corpus/corpus-data.json` (165 itens) |
| **Método Atlas, não Score** | `hub/iconocracy-corpus/docs/methodology.md` |
| **Propostas de projeto** | `hub/iconocracy-corpus/vault/tese/drafts/` (Max Planck, Justice Vandalized) |
| **Biblioteca de referência** | `Books/` (24 PDFs — Ginzburg, Beccaria, Sbriccoli, Broedel, etc.) |
| **Cotutela** | `Cotutela/` (checklist + resumo) |
| **Automação** | `.claude/AUTOMATION.md` (hooks, skills, agents, scheduled tasks) |
| **Conformidade Claude Code** | `CLAUDE.md` (mapa do meta-workspace para sessões) |

## Contrato de organização

- `hub/`: hub canônico da tese
- `apps/`: interfaces públicas ou semi-públicas
- `pipelines/`: ingestão, indexação e pipelines operacionais
- `labs/`: experimentos e código exploratório
- `vaults/`: superfícies Obsidian separadas por função
- `shared/`: bases e ativos de referência compartilhados
- `archive/`: duplicatas, legados e checkouts aposentados

## Workspace Index

| Nome | Caminho canônico | Papel | Propósito / responsável | Status | Caminhos legados |
| --- | --- | --- | --- | --- | --- |
| `iconocracy-corpus` | `/Users/ana/Research/hub/iconocracy-corpus` | Hub da tese | Monorepo canônico da pesquisa ICONOCRACIA | canonical | `/Users/ana/iconocracy-corpus` |
| `iconocracia-companion` | `/Users/ana/Research/apps/iconocracia-companion` | App | Interface pública/operacional do corpus | experimental | `/Users/ana/iconocracia-companion` |
| `iconocracia-space` | `/Users/ana/Research/apps/iconocracia-space` | App | Space/Hugging Face para exploração do corpus | experimental | `/Users/ana/iconocracia-space` |
| `iconocracia-db` | `/Users/ana/Research/apps/iconocracia-db` | App | Banco/interface experimental associado ao ecossistema ICONOCRACY | experimental | — |
| `iconocracy-ingest` | `/Users/ana/Research/pipelines/iconocracy-ingest` | Pipeline | Ingestão, OCR e normalização de lotes | derived | symlink externo para o diretório rastreado no hub |
| `indexing` | `/Users/ana/Research/pipelines/indexing` | Pipeline | Indexação, agentes de busca e Gallica MCP | derived | `/Users/ana/iconocracy-corpus/indexing` |
| `Atlas` | `/Users/ana/Research/pipelines/Atlas` | Pipeline/toolkit | Toolkit iconográfico e analítico da tese | experimental | `/Users/ana/iconocracy-corpus/Atlas` |
| `iurisvision` | `/Users/ana/Research/labs/iurisvision` | Lab | Laboratório exploratório em visão jurídica | experimental | symlinks legados em home, `Projects/` e hub |
| `iuris-visio-roadmap` | `/Users/ana/Research/labs/iuris-visio-roadmap` | Lab | Roadmap e planejamento do laboratório iurisvision | experimental | `/Users/ana/iuris-visio-roadmap` |
| `browser-harness` | `/Users/ana/Research/labs/browser-harness` | Lab | Harness experimental de automação/browser para pesquisa e QA | experimental | — |
| `iconocracy-vault` | `/Users/ana/Research/vaults/iconocracy-vault` | Vault | Superfície canônica de notas da tese | canonical | symlink externo para o vault rastreado no hub |
| `dir410346-vault` | `/Users/ana/Research/vaults/dir410346-vault` | Vault | Materiais da disciplina DIR410346 | experimental | symlink externo para o subdiretório rastreado no vault do hub |
| `dir410340-vault` | `/Users/ana/Research/vaults/dir410340-vault` | Vault | Materiais de disciplina separados do vault da tese | experimental | symlink externo para o subdiretório rastreado no vault do hub |
| `iconclass-data` | `/Users/ana/Research/shared/iconclass-data` | Shared data | Base de referência Iconclass | canonical | `/Users/ana/iconclass-data` |
| `iconclass-data-avmadrj` | `/Users/ana/Research/shared/iconclass-data-avmadrj` | Shared data | Variante local da base Iconclass | canonical | `/Users/ana/iconclass-data-avmadrj` |
| `mnemosyne-scout` | `/Users/ana/Research/hub/mnemosyne-scout` | Hub criativo | Exploração conceitual, mapas, sessões e handoffs da tese | active | — |
| `the-book-of-secret-knowledge` | `/Users/ana/Research/shared/the-book-of-secret-knowledge` | Shared data | Base de referência externa (curadoria de ferramentas e recursos) | reference | — |
| `cowork` | `/Users/ana/Research/cowork` | Tooling | Área de agentes, integrações e tooling Node/OpenCode associado | active | antigo tooling solto na raiz |
| `Books` | `/Users/ana/Research/Books` | Biblioteca | PDFs de referência (Ginzburg, Beccaria, Sbriccoli, Broedel, grammars, etc.) | active | — |
| `Cotutela` | `/Users/ana/Research/Cotutela` | Admin | Checklist e resumo para cotutela | active | — |
| `.claude/AUTOMATION.md` | `/Users/ana/Research/.claude/AUTOMATION.md` | Automação | Índice único de hooks, skills, agents, scheduled tasks, worktrees | canonical | superseded `docs/AUTOMATION-RECOMMENDATIONS.md`, `docs/self-improving-agent-summary.md` |

### Entradas arquivadas removidas do índice ativo

Checkouts aposentados que não existem mais em disco não aparecem como linhas ativas do Workspace Index. Se uma entrada arquivada precisar ser restaurada, recrie primeiro o diretório sob `/Users/ana/Research/archive/` e então reintroduza a linha no índice.

## Regras de migração

- Novos repositórios de pesquisa entram apenas em `/Users/ana/Research`.
- Caminhos antigos permanecem como symlinks de compatibilidade enquanto scripts e documentos são atualizados.
- Na fase git-safe, conteúdo rastreado da tese continua versionado dentro do hub; os paths em `Research/pipelines` e `Research/vaults` podem apontar para ele via symlink.
- Exceção: o nested repo legado `iconocracy-corpus/iconocracy-corpus` foi arquivado sem symlink local porque o gitlink antigo quebrava `git status` no hub.
- Tooling Node/OpenCode de apoio vive em `cowork/`; a raiz do meta-workspace não deve funcionar como projeto npm.
- O contrato canônico da tese permanece: `records.jsonl` -> `corpus-data.json` -> releases públicos.
