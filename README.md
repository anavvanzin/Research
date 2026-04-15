# Research Workspace

Raiz canonica do ecossistema de pesquisa em `/Users/ana/Research`.

## Contrato de organizacao

- `hub/`: hub canonico da tese
- `apps/`: interfaces publicas ou semi-publicas
- `pipelines/`: ingestao, indexacao e pipelines operacionais
- `labs/`: experimentos e codigo exploratorio
- `vaults/`: superficies Obsidian separadas por funcao
- `shared/`: bases e ativos de referencia compartilhados
- `archive/`: duplicatas, legados e checkouts aposentados

## Workspace Index

| Nome | Caminho canonico | Papel | Proposito / responsavel | Status | Caminhos legados |
| --- | --- | --- | --- | --- | --- |
| `iconocracy-corpus` | `/Users/ana/Research/hub/iconocracy-corpus` | Hub da tese | Monorepo canonico da pesquisa ICONOCRACIA | canonical | `/Users/ana/iconocracy-corpus` |
| `iconocracia-companion` | `/Users/ana/Research/apps/iconocracia-companion` | App | Interface publica/operacional do corpus | experimental | `/Users/ana/iconocracia-companion` |
| `iconocracia-space` | `/Users/ana/Research/apps/iconocracia-space` | App | Space/Hugging Face para exploracao do corpus | experimental | `/Users/ana/iconocracia-space` |
| `webiconocracy` | `/Users/ana/Research/apps/webiconocracy` | App | Interface experimental em AI Studio/Gemini | experimental | `/Users/ana/iconocracy-corpus/webiconocracy` |
| `iconocracy-ingest` | `/Users/ana/Research/pipelines/iconocracy-ingest` | Pipeline | Ingestao, OCR e normalizacao de lotes | derived | symlink externo para o diretório rastreado no hub |
| `indexing` | `/Users/ana/Research/pipelines/indexing` | Pipeline | Indexacao, agentes de busca e Gallica MCP | derived | `/Users/ana/iconocracy-corpus/indexing` |
| `Atlas` | `/Users/ana/Research/pipelines/Atlas` | Pipeline/toolkit | Toolkit iconografico e analitico da tese | experimental | `/Users/ana/iconocracy-corpus/Atlas` |
| `iurisvision` | `/Users/ana/Research/labs/iurisvision` | Lab | Laboratorio exploratorio em visao juridica | experimental | symlinks legados em home, `Projects/` e hub |
| `iuris-visio-roadmap` | `/Users/ana/Research/labs/iuris-visio-roadmap` | Lab | Roadmap e planejamento do laboratorio iurisvision | experimental | `/Users/ana/iuris-visio-roadmap` |
| `iconocracy-vault` | `/Users/ana/Research/vaults/iconocracy-vault` | Vault | Superficie canonica de notas da tese | canonical | symlink externo para o vault rastreado no hub |
| `dir410346-vault` | `/Users/ana/Research/vaults/dir410346-vault` | Vault | Materiais da disciplina DIR410346 | experimental | symlink externo para o subdiretório rastreado no vault do hub |
| `dir410340-vault` | `/Users/ana/Research/vaults/dir410340-vault` | Vault | Materiais de disciplina separados do vault da tese | experimental | symlink externo para o subdiretório rastreado no vault do hub |
| `iconclass-data` | `/Users/ana/Research/shared/iconclass-data` | Shared data | Base de referencia Iconclass | canonical | `/Users/ana/iconclass-data` |
| `iconclass-data-avmadrj` | `/Users/ana/Research/shared/iconclass-data-avmadrj` | Shared data | Variante local da base Iconclass | canonical | `/Users/ana/iconclass-data-avmadrj` |
| `js-genai` | `/Users/ana/Research/archive/js-genai` | Archive | Checkout externo mantido apenas por compatibilidade | archived | `/Users/ana/iconocracy-corpus/js-genai` |
| `iconocracy-corpus-legacy` | `/Users/ana/Research/archive/iconocracy-corpus-legacy` | Archive | Repo duplicado legado extraido do hub | archived | antigo nested repo em `iconocracy-corpus/iconocracy-corpus` |
| `iurisvision-home-duplicate` | `/Users/ana/Research/archive/iurisvision-home-duplicate` | Archive | Duplicata antiga do checkout `iurisvision` | archived | antigo `/Users/ana/iurisvision` |
| `iurisvision-projects-duplicate` | `/Users/ana/Research/archive/iurisvision-projects-duplicate` | Archive | Duplicata antiga do checkout `Projects/iurisvision` | archived | antigo `/Users/ana/Projects/iurisvision` |
| `root-vault-legacy` | `/Users/ana/Research/archive/root-vault-legacy` | Archive | Vault legado fora da estrutura canonica | archived | `/Users/ana/vault` |

## Regras de migracao

- Novos repositorios de pesquisa entram apenas em `/Users/ana/Research`.
- Caminhos antigos permanecem como symlinks de compatibilidade enquanto scripts e documentos sao atualizados.
- Na fase git-safe, conteudo rastreado da tese continua versionado dentro do hub; os paths em `Research/pipelines` e `Research/vaults` podem apontar para ele via symlink.
- Excecao: o nested repo legado `iconocracy-corpus/iconocracy-corpus` foi arquivado sem symlink local porque o gitlink antigo quebrava `git status` no hub.
- O contrato canonico da tese permanece: `records.jsonl` -> `corpus-data.json` -> releases publicos.
