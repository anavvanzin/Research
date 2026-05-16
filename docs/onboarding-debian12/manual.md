# Manual Operacional Integrado — Setup Doutoral em Debian 12

> **Para Ana Vanzin** — PPGD/UFSC, pesquisa *ICONOCRACIA: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)*.
> **Máquina-alvo:** VAIO FE16, AMD Ryzen 7-5825U (Cezanne, 8c/16t), 32 GB DDR4, 512 GB SSD NVMe, Debian 12 (Bookworm), kernel 6.1.
> **Última revisão:** 11 de maio de 2026 · **Versão da Claude Code CLI documentada:** 2.1.89+
> **Fontes:** ver [`refs/fontes-consultadas.md`](refs/fontes-consultadas.md). Toda asserção técnica neste manual está rastreada por âncora `[F-NN]` à fonte correspondente.

---

## Como ler este manual

Comandos vêm marcados com três etiquetas que indicam o grau de confiança e a natureza da decisão:

- **(U) Universal** — funciona em qualquer Debian 12 recém-instalado.
- **(C) Contextual** — pressupõe uma configuração anterior; a dependência é nomeada no próprio bloco.
- **(J) Julgamento** — envolve preferência metodológica; o manual sempre oferece pelo menos uma alternativa.

Texto em primeira pessoa do plural ("instalamos", "configuramos") refere-se ao par autora–pesquisadora; texto em segunda pessoa direta refere-se a comandos que devem ser executados *agora*, com o terminal aberto.

---

## Camada 1 — Claude Code CLI em Debian 12

### 1.1 Por que o *native installer*

A Claude Code CLI é distribuída oficialmente em três canais para Debian 12: instalador nativo (`curl https://claude.ai/install.sh | bash`), repositório `apt` assinado, e pacote `npm` global. Os três produzem o **mesmo binário** [F-01]. A escolha entre eles é uma escolha sobre **quem controla as atualizações**.

| Canal | Atualização | Dependência | Quando preferir |
|---|---|---|---|
| Native installer | automática em *background* | nenhuma | usuária individual, sem política corporativa de versionamento |
| `apt` assinado | manual via `apt upgrade` | repo da Anthropic em `sources.list.d/` | máquina de laboratório com pinning, ou política única de upgrades |
| `npm` global | manual via `npm install -g …@latest` | Node.js ≥ 18 | já há toolchain Node mantida para outros propósitos |

Para o uso doutoral, o instalador nativo é o caminho de menor atrito: liberar a Ana da decisão "preciso atualizar Claude Code esta semana?" e remover Node.js da rota crítica reduz superfície de manutenção. A trilha `apt` permanece registrada na § 1.10 como fallback caso a instalação nativa apresente conflito com o `sandbox-exec` que o Claude Code usa para isolar Bash em alguns workflows [F-01].

### 1.2 Instalação

```bash
# (U) Instalador nativo — método oficial recomendado [F-01]
curl -fsSL https://claude.ai/install.sh | bash
```

Por que `-fsSL`: `-f` faz `curl` retornar erro em HTTP ≥ 400 (em vez de baixar uma página de erro), `-s` silencia barra de progresso, `-S` reintroduz mensagens de erro mesmo em modo silencioso, `-L` segue redirecionamentos. Esta combinação é o idioma seguro para pipe em shell.

O script instala o binário em `~/.local/bin/claude` (sem `sudo`) e adiciona o diretório ao `PATH` editando `~/.bashrc` ou `~/.zshrc` conforme o shell ativo. Para que a alteração tenha efeito, abra um novo terminal **ou** execute:

```bash
# (U) Recarrega configuração do shell sem fechar a sessão
source ~/.bashrc
```

#### Verificação pós-instalação

```bash
# (U) Confere que o binário foi colocado no PATH e responde [F-01]
claude --version

# (U) Diagnóstico completo (PATH, rede, permissões, ripgrep, settings) [F-01]
claude doctor
```

`claude doctor` é o equivalente do `pip check` e do `brew doctor`: ele percorre uma lista de invariantes (binário acessível, `ANTHROPIC_API_KEY` ausente se o login for via OAuth, autoupdate funcional, *search backend* operante) e relata o que está fora do contrato. Documentar a saída na primeira execução — copiar para `~/.claude/diagnostico-inicial-$(date +%F).txt` — facilita comparação se algo quebrar depois.

#### Validação criptográfica (recomendada antes do primeiro uso)

A Anthropic publica `manifest.json` com checksums SHA256 de cada plataforma, assinado por GPG. O *fingerprint* da chave de assinatura é fixo [F-01]:

```
31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
```

Procedimento de verificação:

```bash
# (U) Importa a chave pública oficial
curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import

# (U) Mostra fingerprint para conferência manual contra o valor acima
gpg --fingerprint security@anthropic.com

# (U) Baixa manifest e assinatura da versão instalada
REPO=https://downloads.claude.ai/claude-code-releases
VERSION=$(claude --version | awk '{print $NF}')
curl -fsSLO "$REPO/$VERSION/manifest.json"
curl -fsSLO "$REPO/$VERSION/manifest.json.sig"

# (U) Verifica assinatura
gpg --verify manifest.json.sig manifest.json
```

O resultado esperado contém a linha `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`. Eventual `WARNING: This key is not certified` é esperado em primeira importação e não compromete a verificação criptográfica — o que importa é o `Good signature` casado ao fingerprint conferido manualmente.

### 1.3 Autenticação

A Claude Code CLI exige uma conta **paga**: Pro, Max, Team, Enterprise, ou conta Console com créditos pré-pagos. O plano gratuito Claude.ai **não** dá acesso à CLI [F-02]. A pesquisadora já tem assinatura Pro/Max; portanto:

```bash
# (U) Primeira execução — abre browser para login OAuth
claude
```

Na tela de boas-vindas, digite `/login` e siga o redirect. As credenciais ficam em `~/.claude.json` (modo 600); para trocar de conta depois, basta `/login` novamente.

**Quando usar `ANTHROPIC_API_KEY` em vez de OAuth.** Apenas para automação *headless* (CI/CD, scripts batch). Misturar `ANTHROPIC_API_KEY` com sessão OAuth confunde a cobrança — uso interativo é faturado no plano da assinatura; uso com `ANTHROPIC_API_KEY` é faturado no Console por token. Para a tese, **não** usar a variável de ambiente: mantém o histórico de custo dentro do plano Pro/Max [F-02].

### 1.4 Arquivos de contexto `CLAUDE.md` (sistema de memória)

A Claude Code resolve seu contexto a partir de uma hierarquia de arquivos `CLAUDE.md` [F-03]:

1. `~/.claude/CLAUDE.md` — global do usuário, carregado em toda sessão.
2. `<projeto>/CLAUDE.md` — específico do projeto, carregado quando a sessão é aberta dentro desse diretório.
3. Sub-`CLAUDE.md` em diretórios filhos — carregados quando arquivos daquela pasta entram em contexto.

Para a migração, o procedimento é replicar a hierarquia do Mac no Debian *antes* de iniciar a primeira sessão real. Isto evita que a Claude tente "redescobrir" convenções já estabilizadas (caveman mode, env conda, convenções de citação ABNT, ADRs do projeto).

```bash
# (C) Pressupõe Syncthing já espelhando ~/Research entre Mac e Debian (ver § 2.2)
# Espelhe manualmente o CLAUDE.md global a partir do Mac
mkdir -p ~/.claude
cp ~/Research/.claude/CLAUDE.md ~/.claude/CLAUDE.md   # ou o caminho de origem real
```

Para inicializar um `CLAUDE.md` novo em projeto sem histórico:

```bash
# (C) Dentro do diretório do projeto, com a sessão Claude aberta
/init
```

O slash command `/init` lê o repositório, infere stack, build commands, convenções, e propõe um `CLAUDE.md`. Revisar **manualmente** antes de salvar — gerar contexto automático tende a inflar com observações triviais.

Para editar memória dentro da sessão sem trocar de janela:

```
/memory
```

Abre um seletor entre `~/.claude/CLAUDE.md`, o `<projeto>/CLAUDE.md` ativo, e `~/.claude/settings.json` (permissões, hooks). Salva ao sair.

### 1.5 Terminais e ergonomia

O GNOME Terminal padrão do Debian 12 funciona sem alterações. Duas alternativas valem o desvio se a Ana for trabalhar diariamente várias horas no terminal:

- **(J) Alacritty** (`sudo apt install alacritty`). GPU-accelerated, latência mínima, configuração via `~/.config/alacritty/alacritty.toml`. Sem abas — combinar com `tmux` ou com o workspace do GNOME.
- **(J) Kitty** (`sudo apt install kitty`). Também GPU-accelerated, suporte nativo a abas e splits, protocolo gráfico próprio (útil para visualizar miniaturas de iconografia direto no terminal via `kitty +kitten icat`).

Para a tese — onde o terminal será usado para `claude`, `git`, `make`, e `python -i` — Kitty oferece mais ergonomia *out-of-the-box*. Configuração mínima recomendada em `~/.config/kitty/kitty.conf`:

```conf
font_family      JetBrains Mono
font_size        12.0
enable_audio_bell no
shell_integration enabled
```

`shell_integration enabled` ativa marcação automática de prompts, permitindo navegação salto-a-salto entre comandos com `Ctrl+Shift+Z`.

### 1.6 Modos de operação

| Modo | Como entrar | O que faz |
|---|---|---|
| **Interativo** | `claude` | Sessão padrão; loop de mensagens; ferramentas pedem permissão a cada uso. |
| **Headless** | `claude -p "consulta"` | Executa uma única consulta, imprime resposta em stdout, encerra. Usado para pipelines. [F-04] |
| **Continue** | `claude -c` | Retoma a *última* conversa cujo cwd era o diretório atual. |
| **Resume** | `claude -r` | Abre um seletor com conversas anteriores; útil quando se mistura projetos. |
| **Plan mode** | Atalho `Shift+Tab` dentro da sessão | Pesquisa antes de editar; bloqueia escritas; encerra com `ExitPlanMode`. Foi o modo desta própria pesquisa. |
| **Accept-edits** | `Shift+Tab` (cicla entre modos) | Aceitação automática de edições; útil quando se está refatorando volume sem necessidade de aprovar cada arquivo. |

O comando `claude -p` é, na prática, a forma mais subutilizada da CLI. Para a tese, vale o reflexo: toda vez que um capítulo termina, gerar um sumário em `tese/manuscrito/<capítulo>/_sumario.md`:

```bash
# (C) Pressupõe sessão Claude já autenticada
claude -p "Em até 200 palavras, sumarize o argumento central de @tese/manuscrito/cap03.md em português acadêmico" \
  > tese/manuscrito/cap03/_sumario.md
```

A sintaxe `@arquivo.md` na consulta força a Claude a abrir aquele arquivo como contexto — sem o `@`, ela responderia "preciso ver o arquivo".

### 1.7 Slash commands essenciais

Lista enxuta — só o que a pesquisadora usará na primeira semana. A referência completa está em `claude --help` e em [F-04].

| Comando | Quando |
|---|---|
| `/clear` | Conversa virou ruído; começar limpo no mesmo diretório sem perder os `CLAUDE.md`. |
| `/compact` | Conversa longa que vale a pena manter mas está pesada: gera sumário e mantém daí pra frente. |
| `/resume` | Recuperar uma sessão de ontem cujo título não bate com o cwd atual. |
| `/agents` | Listar e selecionar subagentes (caso a Ana adote o catálogo de agentes da meta-workspace). |
| `/mcp` | Status dos MCP servers (importa para o Gallica MCP em Node, § 3.6). |
| `/hooks` | Listar hooks ativos; útil quando algo silenciosamente bloqueia uma escrita. |
| `/config` | Configuração rápida (modelo, canal de release, autoupdate). |
| `/memory` | Editar `CLAUDE.md` global ou de projeto sem sair da sessão. |
| `/init` | Gerar `CLAUDE.md` inicial para um repositório sem contexto. |
| `/cost` | Custo acumulado da sessão atual (em USD aproximado). |
| `/login` | Trocar de conta sem encerrar a CLI. |

### 1.8 Claude Code CLI vs Claude.ai web

Diferenças que importam para o fluxo doutoral:

| Capacidade | CLI | Web (`claude.ai/code`) |
|---|---|---|
| Acesso a filesystem real | ✅ | ❌ (sandbox) |
| Execução de Bash | ✅ | ❌ |
| Operações Git locais | ✅ | ❌ |
| Pandoc, LaTeX, `make` | ✅ | ❌ |
| MCP servers locais | ✅ | parcial |
| Auditabilidade (histórico em `~/.claude/projects/`) | ✅ | ❌ |
| Disponível offline (após login) | parcial (algumas operações cacheadas) | ❌ |
| Disponível no celular | ❌ | ✅ |

Regra prática: **CLI como padrão** para qualquer trabalho que toque o monorepo da tese. Web para consultas conceituais quando o notebook está fora de alcance ou para perguntas curtas sobre legislação que não exigem leitura de arquivos.

### 1.9 Gestão de custos

A CLI rastreia custo em USD aproximado, atualizado token-a-token. Ao final de cada sessão, antes de sair:

```
/cost
```

Convenção recomendada para a tese: criar `tese/.cost-log.md` com uma linha por sessão no formato

```
2026-05-16 cap03-revisao-secao-3.2  US$ 1.84  ~32min  notas:obs-arrazoado-tronco-imperial
```

Após dois meses isto produz uma estatística simples: quanto custou cada capítulo, qual seção consumiu mais iteração. Auxilia tanto orçamento quanto autoconsciência metodológica (capítulos muito caros costumam ser capítulos cuja questão central ainda não está clara).

### 1.10 Troubleshooting — padrões comuns 2025-2026

**(a) `claude: command not found` após instalação bem-sucedida.**
Causa típica: shell não recarregou o `PATH`. Fix:

```bash
# (U)
hash -r           # limpa cache do shell
source ~/.bashrc  # ou ~/.zshrc
echo $PATH | tr ':' '\n' | grep -q "\.local/bin" || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

**(b) `claude doctor` reporta search backend ausente.**
O Claude Code embarca `ripgrep` próprio. Em ambientes onde a libc é diferente do esperado (containers Alpine, alguns *userspace* Debian estranhos), o `rg` embutido não roda. Fix:

```bash
# (U)
sudo apt install ripgrep
```

E adicionar a `~/.claude/settings.json`:

```json
{
  "env": { "USE_BUILTIN_RIPGREP": "0" }
}
```

**(c) Autoupdate silenciosamente falha em rede com proxy.**
Sintoma: versão da CLI fica congelada por semanas. Fix em `~/.claude/settings.json`:

```json
{
  "env": {
    "HTTPS_PROXY": "http://proxy.exemplo:8080",
    "HTTP_PROXY":  "http://proxy.exemplo:8080",
    "NO_PROXY":    "localhost,127.0.0.1"
  }
}
```

**(d) Erros de permissão após `sudo npm install -g`.**
A doc oficial **desaconselha explicitamente** [F-01]. Recuperação:

```bash
# (U) Remove a instalação npm com privilégios elevados
sudo npm uninstall -g @anthropic-ai/claude-code
# Reinstala via native installer (sem sudo)
curl -fsSL https://claude.ai/install.sh | bash
```

**(e) Primeira sessão trava na tela de login com browser indisponível (servidor remoto).**
Fix:

```bash
# (U) Força fluxo não-interativo só para autenticar
ANTHROPIC_API_KEY=sk-… claude -p "ping"
```

(Apenas para servidores headless. No notebook pessoal, o login OAuth via browser é o caminho.)

---

## Camada 2 — Stack acadêmico-jurídico em Debian 12

### 2.1 Pacotes base via `apt`

Antes de qualquer outra coisa, a primeira corrida no notebook novo:

```bash
# (U) Atualização inicial — pode levar 10-20 minutos
sudo apt update && sudo apt upgrade -y

# (U) Pacotes base — tudo o que será usado em mais de uma camada
sudo apt install -y \
  git curl wget gpg ca-certificates build-essential \
  ripgrep fd-find jq unzip xz-utils make \
  pandoc texlive-xetex texlive-fonts-recommended texlive-fonts-extra \
  texlive-lang-portuguese texlive-luatex \
  python3-pip python3-venv \
  ffmpeg imagemagick poppler-utils
```

Justificativa rápida por agrupamento:
- `git curl wget gpg ca-certificates build-essential` — universo mínimo para qualquer instalação a partir daqui.
- `ripgrep fd-find` — busca rápida no vault Obsidian e no monorepo (ambos têm milhares de arquivos).
- `pandoc texlive-*` — pipeline `make -C vault/tese/ pdf` do iconocracy-corpus depende deles [F-05]; `texlive-lang-portuguese` cobre hifenização ABNT.
- `python3-pip python3-venv` — bootstrap até miniforge3 entrar (§ 2.6); úteis também para scripts pontuais via venv.
- `ffmpeg imagemagick poppler-utils` — manipulação de imagens iconográficas e PDFs; o `imagemagick` está corrigido em Debian 12 (políticas restritivas já não bloqueiam PDFs por padrão como em Debian 10).

### 2.2 Obsidian

**(J) Recomendação: instalar via `.deb` oficial.**

A página de downloads (`https://obsidian.md/download`) publica `.deb` para arquitetura x86_64 [F-06]. As alternativas:

| Método | Pró | Contra |
|---|---|---|
| `.deb` oficial (recomendado) | atualização via apt; integra-se sem sandbox | é preciso baixar manualmente cada release |
| Flatpak | atualização automática | sandbox bloqueia acesso ao Zotero por padrão; remediação exige `flatpak override` |
| AppImage | portável | nenhuma integração com `update` do sistema; precisa de gerenciador como `appimaged` |

Procedimento:

```bash
# (U) Baixar o .deb mais recente — substitua VERSAO pela atual em obsidian.md/download
cd /tmp
wget https://github.com/obsidianmd/obsidian-releases/releases/download/v<VERSAO>/obsidian_<VERSAO>_amd64.deb
sudo apt install ./obsidian_<VERSAO>_amd64.deb
```

#### Plugins essenciais (instalar no primeiro lançamento)

1. **Tasks** — gestão de TODOs com sintaxe `- [ ]`; filtros por tag, data, projeto.
2. **Dataview** — consultas SQL-like sobre notas; indispensável para gerar índices automáticos por iconclass, por país, por século.
3. **Templater** — templates dinâmicos com JavaScript embutido; usado para criar notas com cabeçalho ABNT pré-preenchido.
4. **Citations** *ou* **Zotero Integration** — ver § 2.3.

#### Sincronização do vault com Syncthing

**Por que Syncthing.** Open-source, P2P (sem servidor de terceiros), sem custo recorrente, conflicts resolvidos por arquivo `.sync-conflict-…`. Para um vault Obsidian onde a Ana é a única autora, é mais simples do que o Obsidian Sync pago.

Instalação:

```bash
# (U) Repositório oficial Syncthing
sudo mkdir -p /etc/apt/keyrings
sudo curl -fsSL https://syncthing.net/release-key.gpg -o /etc/apt/keyrings/syncthing-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable" \
  | sudo tee /etc/apt/sources.list.d/syncthing.list
sudo apt update && sudo apt install syncthing
```

Para rodar como serviço *do usuário* (não systemwide), o Syncthing recomenda *user units* do systemd:

```bash
# (U) Habilita Syncthing para o usuário atual; inicia já
systemctl --user enable syncthing.service
systemctl --user start syncthing.service
```

Pareamento com a máquina antiga:

1. No Mac antigo: abrir `http://localhost:8384`, copiar o *Device ID*.
2. No Debian: abrir `http://localhost:8384`, clicar em **Add Remote Device**, colar o ID, marcar **Auto Accept**.
3. No Mac, aceitar o pareamento de volta.
4. Compartilhar a pasta do vault (`Documents/Obsidian/iconocracy-vault` ou equivalente) do Mac para o Debian.
5. No Debian, escolher o destino como `~/Documents/Obsidian/iconocracy-vault`.

Sync inicial pode levar de minutos a horas conforme tamanho do vault. Durante esse período, **não editar o vault em ambas as máquinas**.

### 2.3 Zotero 7

**Instalação.** A página oficial (`https://www.zotero.org/download/`) distribui Linux x86_64 como tarball `.tar.bz2` [F-07]. Não há `.deb` oficial — usuários experimentaram alternativas comunitárias, mas a recomendação é manter a instalação oficial em `~/.local/opt/`:

```bash
# (U) Download e instalação local (sem sudo)
mkdir -p ~/.local/opt
cd /tmp
wget -O Zotero-7-linux-x86_64.tar.bz2 "https://www.zotero.org/download/client/dl?channel=release&platform=linux-x86_64"
tar -xjf Zotero-7-linux-x86_64.tar.bz2 -C ~/.local/opt/
mv ~/.local/opt/Zotero_linux-x86_64 ~/.local/opt/zotero-7

# Registra atalho .desktop e ícone
~/.local/opt/zotero-7/set_launcher_icon
ln -sf ~/.local/opt/zotero-7/zotero.desktop ~/.local/share/applications/zotero.desktop

# Atalho de comando
mkdir -p ~/.local/bin
ln -sf ~/.local/opt/zotero-7/zotero ~/.local/bin/zotero
```

**Configuração da pasta vinculada.** Em `Edit → Settings → Files and Folders → Linked attachment base directory`, apontar para:

```
~/Documents/iconocracy-corpus/biblio/
```

A escolha deliberada deste path (e não `~/Zotero/storage`) é manter o **mesmo caminho** no Mac e no Debian, o que permite ao Syncthing espelhar o diretório `biblio/` sem reescrever links. Os PDFs ficam fora do `~/Zotero/storage` padrão; o Zotero passa a guardar apenas metadados, e os PDFs ficam livres para serem referenciados também pelo Obsidian.

**Plugins.**

- **Better BibTeX** (`https://github.com/retorquere/zotero-better-bibtex`) — gera chaves estáveis no formato `autor_ano_palavra-chave`; exporta `.bib` que o `pandoc-citeproc` consome. Para tese em português ABNT NBR 6023:2025, configurar `Citation Key Formula` em `Settings → Better BibTeX → Citation Keys` com:
  ```
  authEtAl(2,"_") + "_" + year + "_" + shorttitle(2,2)
  ```
- **ZotMoov** (`https://github.com/wileyyugioh/zotmoov`) — automatiza relocação dos PDFs anexados para a pasta vinculada com nomeação previsível (`{author}_{year}_{title}.pdf`).

**Integração com Obsidian.**

Dois plugins competem; a escolha depende do estilo de escrita.

- **Citations** (`zotero-plugin/citations`) — leve, gera apenas o citation key Markdown `[@chave]` quando você invoca `Insert Markdown citation`. Bom para quem escreve direto em pandoc-markdown e não quer Obsidian *intermediando* o trabalho do Pandoc.
- **Zotero Integration** (`mgmeyers/obsidian-zotero-integration`) — mais ambicioso: cria *literature notes* automáticas com excerpts dos PDFs, links bidirecionais com a entrada Zotero, templates customizáveis. Bom para quem usa o Obsidian como camada de leitura ativa antes de escrever no Pandoc.

Para a tese em fase avançada (manuscrito sendo redigido em Pandoc com `.bib` externo), **Citations** é o suficiente e adiciona menos pontos de falha.

### 2.4 Git, GitHub CLI, SSH

```bash
# (U) Configuração mínima de identidade
git config --global user.name  "Ana Vanzin"
git config --global user.email "ana@…"   # use o e-mail GitHub
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global rerere.enabled true   # reaproveitar resolução de conflitos
```

**Chave SSH.**

```bash
# (U) Geração de chave ed25519 dedicada à máquina nova
ssh-keygen -t ed25519 -C "ana@vaio-debian-2026" -f ~/.ssh/id_ed25519_github
chmod 600 ~/.ssh/id_ed25519_github

# Configura ssh-agent para uso automático
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github
```

E em `~/.ssh/config`:

```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
```

**GitHub CLI.**

```bash
# (U) Repositório oficial GitHub CLI [F-08]
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
     | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
     | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update \
  && sudo apt install gh -y
```

```bash
# (U) Login interativo
gh auth login
# escolher: GitHub.com → SSH → caminho ~/.ssh/id_ed25519_github → cadastra a chave pública
```

**Clone do monorepo:**

```bash
# (C) Pressupõe SSH configurada acima
mkdir -p ~/iconocracy-corpus
git clone git@github.com:anavvanzin/iconocracy-corpus.git ~/iconocracy-corpus
cd ~/iconocracy-corpus
git status   # deve mostrar 'On branch main, working tree clean'
```

### 2.5 Python — abordagem híbrida conda + uv

**Decisão metodológica registrada.** O repositório `iconocracy-corpus` traz `environment.yml` e `requirements.txt` como fontes da verdade [F-05]. Migrá-los a `pyproject.toml` puro hoje compete com o trabalho de escrita da tese. A recomendação é **híbrida**:

- **conda** (via miniforge3) gerencia o env nominal `iconocracia`, reproduzindo `environment.yml` sem mudanças;
- **uv** passa a ser o gerenciador padrão para scripts novos fora do monorepo (utilitários, *playgrounds*, o próprio `notion_sync.py` enquanto estiver em fase de scaffold).

**Instalação do miniforge3 (conda + mamba sem licenciamento Anaconda).**

```bash
# (U) Instalador oficial conda-forge [F-09]
curl -fsSL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
  -o /tmp/miniforge.sh
bash /tmp/miniforge.sh -b -p ~/.local/opt/miniforge3

# Inicializa para bash
~/.local/opt/miniforge3/bin/conda init bash
# abrir nova sessão de shell, ou:
exec $SHELL
```

**Criação do env do projeto:**

```bash
# (C) Pressupõe miniforge3 inicializado e ~/iconocracy-corpus clonado
cd ~/iconocracy-corpus
conda env create -f environment.yml         # cria env 'iconocracia'
conda activate iconocracia
python -c "import sys; print(sys.version)"  # deve imprimir 3.10+ conforme env
```

**Instalação do `uv` (Astral).**

```bash
# (U) Instalador oficial [F-10]
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc   # ou abrir nova sessão
uv --version
```

**Uso de `uv` para scripts novos** (exemplo do scaffold `notion_sync.py`):

```bash
# (U) Em um diretório fora do monorepo, p.ex. ~/playground/notion-sync/
cd ~/playground/notion-sync
uv init                              # cria pyproject.toml + .python-version
uv add notion-client python-dotenv   # adiciona deps; cria uv.lock
uv run python notion_sync.py --dry-run
```

`uv run` resolve dependências, cria venv embutido em `.venv/`, executa. Tempo de cold-start: ~80 ms em SSD NVMe, ordens de grandeza mais rápido que `python -m venv && pip install`.

### 2.6 Node.js (Gallica MCP e auxiliares)

O monorepo da tese declara um *Gallica MCP server* em Node, rodando na porta 3001 [F-05]. Para gerenciar versões de Node sem amarrar o sistema:

```bash
# (U) Instala nvm — gerenciador de versões Node [F-11]
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc

# Instala LTS atual e fixa como default
nvm install --lts
nvm alias default lts/*

# Verifica
node --version
npm --version
```

Não é necessário Node para a Claude Code CLI (o native installer entrega binário independente). Node é necessário **só** para o Gallica MCP e eventuais scripts auxiliares que a Ana decida escrever em JavaScript.

### 2.7 rclone para Google Drive

```bash
# (U) Instalador oficial [F-12]
curl https://rclone.org/install.sh | sudo bash
rclone version
```

**Configuração do remote `drive-iconocracy`:**

```bash
# (U) Wizard interativo
rclone config
```

Sequência de respostas (ditados pelo wizard):

1. `n` → New remote
2. Name → `drive-iconocracy`
3. Storage → `drive` (Google Drive)
4. `client_id` e `client_secret` → deixar em branco (usa credenciais Anthropic-rclone públicas; aceitável para uso pessoal; para produção, criar projeto próprio em `console.cloud.google.com`)
5. `scope` → `drive` (acesso completo) ou `drive.file` (só arquivos criados pelo rclone) — para esta tese, `drive` para conseguir ler a pasta `ICONOCRACIA` já existente
6. `root_folder_id` → deixar vazio; especificar nas operações
7. `service_account_file` → deixar vazio
8. `Edit advanced config?` → `n`
9. `Use auto config?` → `y` (abre browser para OAuth)
10. Confirmar → `q` para sair

Teste:

```bash
# (C) Pressupõe remote 'drive-iconocracy' configurado
rclone lsd drive-iconocracy:           # lista pastas do Drive
rclone lsd drive-iconocracy:ICONOCRACIA  # confere pasta canônica do projeto
```

**Sync de `data/raw/`.** O comando canônico é `bisync` (preserva mudanças nos dois lados), mas exige *primeira execução* com `--resync` para estabelecer baseline:

```bash
# (C) PRIMEIRA execução APENAS — declara o lado local como autoridade inicial
rclone bisync ~/iconocracy-corpus/data/raw/ drive-iconocracy:ICONOCRACIA/data/raw/ \
  --resync \
  --dry-run                    # rode com --dry-run primeiro, conforme execução real
```

```bash
# (C) Execuções subsequentes — sincronização incremental
rclone bisync ~/iconocracy-corpus/data/raw/ drive-iconocracy:ICONOCRACIA/data/raw/ \
  --conflict-resolve newer \
  --check-access \
  --filter-from ~/iconocracy-corpus/.rclone-filter
```

Arquivo `~/iconocracy-corpus/.rclone-filter` (excluir lixos e validar convenção de nomes):

```
- .DS_Store
- Thumbs.db
- *.tmp
+ /[A-Z][A-Z]_*_[0-9][0-9][0-9][0-9]_*_[0-9]*.jpg
+ /[A-Z][A-Z]_*_[0-9][0-9][0-9][0-9]_*_[0-9]*.jpeg
+ /[A-Z][A-Z]_*_[0-9][0-9][0-9][0-9]_*_[0-9]*.png
+ /[A-Z][A-Z]_*_[0-9][0-9][0-9][0-9]_*_[0-9]*.tif
+ /[A-Z][A-Z]_*_[0-9][0-9][0-9][0-9]_*_[0-9]*.tiff
- *
```

A linha final `- *` é o gatekeeper: qualquer arquivo que não case com a convenção `{PAÍS}_{SUPORTE}_{ANO}_{ACERVO}_{SEQ}.<ext>` é silenciosamente ignorado. Isto força disciplina de nomeação.

**Aviso (J):** `rclone bisync` é tecnicamente classificado como "feature complete and reliable" desde a 1.66, mas ainda recebe correções regulares. Para a tese, alternativa mais conservadora é executar `rclone copy` em duas direções com `rclone check` no meio, agendada via cron:

```bash
# (J) Alternativa conservadora — em cron, a cada 30 min
*/30 * * * * cd ~/iconocracy-corpus && \
  /usr/bin/rclone copy data/raw/ drive-iconocracy:ICONOCRACIA/data/raw/ \
    --filter-from .rclone-filter --update >> ~/.rclone.log 2>&1
```

(`--update` evita reescrever versão remota mais nova com uma local mais antiga.)

### 2.8 Editor: VS Code (com Cursor como alternativa)

**(J) Recomendação primária: VS Code via repositório oficial Microsoft.**

```bash
# (U) Importa chave Microsoft e adiciona repo [F-13]
sudo install -D -o root -g root -m 644 \
  <(wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor) \
  /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
  | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
sudo apt update
sudo apt install code
```

Extensões mínimas (instalar pelo CLI ou pela UI):

```bash
# (C) Pressupõe `code` no PATH
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension yzhang.markdown-all-in-one
code --install-extension eamodio.gitlens
code --install-extension dbaeumer.vscode-eslint
code --install-extension anthropic.claude-code        # integração IDE oficial
```

**Cursor (opcional).** Cursor é distribuído como AppImage. Útil como editor secundário se houver fluxos de coding-com-AI alternativos. Não substitui a Claude Code CLI:

```bash
# (J) Opcional — instalar AppImage e marcar executável
mkdir -p ~/.local/opt/cursor
cd ~/.local/opt/cursor
wget -O cursor.AppImage "https://download.cursor.sh/linux/appImage/x64"
chmod +x cursor.AppImage
```

### 2.9 Shell e prompt

**(J) Recomendação balanceada: manter Bash + adicionar Starship.**

O `oh-my-zsh` adiciona surface de manutenção (plugins que quebram em atualizações, tema que conflita com cores do Tmux) sem retorno tangível para o fluxo acadêmico. Starship é um *prompt*, não um shell: roda sobre Bash ou Zsh, escrito em Rust, configuração única em `~/.config/starship.toml`.

```bash
# (U) Instalador oficial [F-14]
curl -fsSL https://starship.rs/install.sh | sh

# Adiciona init ao bashrc
echo 'eval "$(starship init bash)"' >> ~/.bashrc
```

Configuração mínima recomendada em `~/.config/starship.toml`:

```toml
add_newline = false
format = "$directory$git_branch$git_status$python$nodejs$character"

[directory]
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = "🜂 "

[python]
symbol = "py "
format = "[$symbol$version( \\($virtualenv\\))]($style) "
```

Se a Ana preferir Zsh, é trivial trocar: `sudo apt install zsh && chsh -s $(which zsh)` e substituir `init bash` por `init zsh` no rc correspondente. Apêndice ao final do manual cobre essa variação.

### 2.10 Debian 12 vs alternativas — manter Debian

Quatro parágrafos para fechar a Camada 2.

**Debian 12 (Bookworm).** Kernel 6.1 LTS, congelamento de versões com correções de segurança até pelo menos junho de 2028. Ciclo de release previsível (~2 anos). O Ryzen 7-5825U (microarquitetura Cezanne, lançada 2022) é totalmente coberto pelo kernel 6.1; o driver AMDGPU está estável; o controlador WiFi padrão do VAIO FE16 (Realtek/MediaTek conforme variante) tem suporte mainline.

**Ubuntu 24.04 LTS (Noble).** Kernel 6.8, ferramentas mais novas (Python 3.12 default, GCC 13). Para hardware lançado após 2024, faz diferença; para um Cezanne 2022, é ganho marginal. Custo: a Canonical empurra Snaps no lugar de `apt` para várias aplicações (Chromium, Firefox por padrão), o que cria fricção e degrada inicialização. Para uso individual focado em redação, **não** vale a troca.

**Fedora 41.** Bleeding-edge: kernel ~6.11, Python 3.13, atualizações de toolchain a cada 6 meses. Maior compatibilidade com hardware muito recente e com tooling Wayland avançado. Custo: ciclos curtos significam que a Ana terá uma migração completa de sistema a cada 13 meses (suporte de cada release Fedora). Para um fluxo doutoral cujo objetivo é **escrever**, ciclo curto é inimigo. Não trocar.

**Veredicto.** Ficar com Debian 12. A escolha foi correta. O manual segue assumindo esta base.

---

## Camada 3 — Integração GitHub ↔ Drive ↔ Notion

### 3.1 Modelo mental dos três pilares

```
   ┌──────────────┐  rclone bisync   ┌──────────────────┐
   │ Google Drive │ ────────────────▶│ data/raw/ (local)│
   │   (origem)   │ ◀────────────────│   filename canon │
   └──────────────┘                   └────────┬─────────┘
          ▲                                    │
          │                          tools/scripts/*.py
          │                                    │
          │                                    ▼
   ┌──────┴───────┐    notion_sync.py  ┌─────────────────────────┐
   │  Notion DB1  │ ◀──────────────────│ data/processed/         │
   │ (classifica) │    upsert por      │   records.jsonl         │
   └──────────────┘    external_id     └─────────────────────────┘
                                                ▲
                                                │
                                       git push origin main
                                                │
                                                ▼
                                  ┌──────────────────────────┐
                                  │ GitHub: anavvanzin/      │
                                  │   iconocracy-corpus      │
                                  │ (canonical history)      │
                                  └──────────────────────────┘
```

**Princípio:** cada item iconográfico tem um **identificador canônico único** — o `external_id` — propagado nos três sistemas. A convenção declarada no briefing é:

```
{PAÍS}_{SUPORTE}_{ANO}_{ACERVO}_{SEQ}
```

Exemplo concreto: `FR_GRAVURA_1834_BNF_017`. Este string é simultaneamente:
- o nome de arquivo (sem extensão) em `data/raw/`;
- a chave `external_id` em `data/processed/records.jsonl`;
- o valor da propriedade `external_id` (tipo *Text*) no Notion DB1 *Corpus Iconográfico*.

**Nota técnica importante.** A inspeção do `CLAUDE.md` público do repositório (em 2026-05-11) mostrou que a convenção formal documentada para *vault notes* é `XX-NNN Título.md` (ex.: `FR-013`), distinta da convenção `{PAÍS}_{SUPORTE}_{ANO}_{ACERVO}_{SEQ}` usada para os arquivos brutos do corpus. As duas convenções coexistem em escopos diferentes: a primeira é a chave do vault Obsidian (notas curadoriais sobre cada item); a segunda é a chave do filesystem `data/raw/` (binário origem). O manual respeita ambas. Recomendação operacional: confirmar com o `schemas/` real do repo, na primeira execução de validação após a migração, se a regex está alinhada com itens já catalogados.

### 3.2 rclone bisync com preservação da convenção de nomes

O arquivo de filtro `~/iconocracy-corpus/.rclone-filter` apresentado na § 2.7 cumpre função dupla: exclui artefatos do sistema operacional (`.DS_Store`, `Thumbs.db`) e *valida estruturalmente* cada arquivo via regex. Qualquer arquivo introduzido na pasta com nome fora da convenção é silenciosamente ignorado pelo `bisync`, o que cria pressão por disciplina (o arquivo "some" para a pesquisadora até ser renomeado).

Para *auditoria* periódica do que está em `data/raw/` mas não foi sincronizado por violar a regex, o manual entrega um script complementar (a salvar em `tools/scripts/audit_corpus_names.py`):

```python
#!/usr/bin/env python3
"""
usage: python audit_corpus_names.py [DIR]
Default DIR: data/raw/

Percorre o diretório e reporta arquivos cujo nome não respeita a convenção
{PAÍS}_{SUPORTE}_{ANO}_{ACERVO}_{SEQ}.{ext}.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r"^[A-Z]{2,3}"           # país (FR, DE, BR, USA…)
    r"_[A-Z]+"               # suporte (GRAVURA, ESTAMPA, OLEO…)
    r"_[0-9]{4}"             # ano YYYY
    r"_[A-Z0-9-]+"           # acervo (BNF, LOC, MNBA…)
    r"_[0-9]{3,}"            # seq numérico (≥3 dígitos)
    r"\.(?:jpe?g|png|tiff?)$",
    re.IGNORECASE,
)

def main(target: str = "data/raw/") -> int:
    root = Path(target)
    if not root.is_dir():
        print(f"diretório não encontrado: {root}", file=sys.stderr)
        return 2
    offenders = sorted(
        p.name
        for p in root.iterdir()
        if p.is_file() and not PATTERN.match(p.name)
    )
    if offenders:
        print(f"{len(offenders)} arquivo(s) fora da convenção:")
        for name in offenders:
            print(f"  {name}")
        return 1
    print("OK — todos os arquivos respeitam a convenção.")
    return 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
```

Execução periódica recomendada (semanal, manualmente, antes do `rclone bisync` em massa):

```bash
# (C) Pressupõe env 'iconocracia' ativo
cd ~/iconocracy-corpus
python tools/scripts/audit_corpus_names.py data/raw/
```

### 3.3 Notion: API e o script `notion_sync.py`

**Pré-requisitos no Notion (web).**

1. Acessar `https://www.notion.so/my-integrations` → **+ New integration**.
2. Nome: `iconocracia-corpus-sync`; tipo: *Internal*; capacidades: **Read content**, **Update content**, **Insert content** (não habilitar *User information* a menos que necessário).
3. Copiar o **Internal Integration Token** (`secret_…`).
4. Na database **DB1 Corpus Iconográfico**, abrir `…` → **Connections** → **Connect to** → selecionar `iconocracia-corpus-sync`.
5. Copiar o ID da database (na URL: `notion.so/<workspace>/<db_id>?v=…`; o `db_id` é o substring de 32 hex chars).

**Armazenamento das credenciais.**

```bash
# (U) Cria diretório de config com permissões restritivas
mkdir -p ~/.config/iconocracy
chmod 700 ~/.config/iconocracy
touch ~/.config/iconocracy/.env
chmod 600 ~/.config/iconocracy/.env
```

Conteúdo do `~/.config/iconocracy/.env` (preencher após gerar os valores no Notion):

```dotenv
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DB1_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Scaffold do `notion_sync.py`** (a salvar em `tools/scripts/notion_sync.py` após inspeção do `schemas/` real para confirmar mapeamento exato):

```python
#!/usr/bin/env python3
"""
usage:
  python notion_sync.py [--dry-run] [--since YYYY-MM-DD] [--limit N]

Lê data/processed/records.jsonl e faz upsert idempotente na database DB1 do
Notion. Identificador canônico: external_id (= filename canônico sem extensão).

Variáveis de ambiente esperadas (de ~/.config/iconocracy/.env):
  NOTION_TOKEN     token da integração interna
  NOTION_DB1_ID    id da database 'Corpus Iconográfico'
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError

load_dotenv(Path.home() / ".config" / "iconocracy" / ".env")
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DB1 = os.environ["NOTION_DB1_ID"]
notion = Client(auth=NOTION_TOKEN)

# ---- Mapeamento JSONL → Notion ---------------------------------------------
# CONFIRMAR contra schemas/notion-db1.schema.json antes de promover este script
# para produção. Os tipos do Notion são: title, rich_text, number, select,
# multi_select, date, files, checkbox, url, email, phone_number, relation,
# rollup, formula. As propriedades abaixo são uma minuta de boa-fé.

def to_notion_properties(rec: dict) -> dict:
    return {
        # title — a coluna obrigatória; usamos external_id como título
        "Nome": {
            "title": [{"text": {"content": rec["external_id"]}}],
        },
        "external_id": {
            "rich_text": [{"text": {"content": rec["external_id"]}}],
        },
        "país": {"select": {"name": rec.get("pais", "—")}},
        "suporte": {"select": {"name": rec.get("suporte", "—")}},
        "ano": {"number": rec.get("ano")},
        "acervo": {"select": {"name": rec.get("acervo", "—")}},
        "iconclass": {
            "multi_select": [
                {"name": code} for code in rec.get("iconclass", [])
            ],
        },
        "titulo_obra": {
            "rich_text": [
                {"text": {"content": rec.get("titulo", "")}}
            ],
        },
        "autor": {
            "rich_text": [
                {"text": {"content": rec.get("autor", "")}}
            ],
        },
        "drive_url": {"url": rec.get("drive_url")} if rec.get("drive_url") else None,
        "checksum_sha256": {
            "rich_text": [
                {"text": {"content": rec.get("sha256", "")}}
            ],
        },
    }


def find_existing(external_id: str) -> str | None:
    """Retorna o page_id existente para um external_id, ou None."""
    res = notion.databases.query(
        database_id=DB1,
        filter={
            "property": "external_id",
            "rich_text": {"equals": external_id},
        },
        page_size=1,
    )
    results = res.get("results", [])
    return results[0]["id"] if results else None


def upsert(rec: dict, *, dry_run: bool) -> str:
    properties = {k: v for k, v in to_notion_properties(rec).items() if v is not None}
    existing_id = find_existing(rec["external_id"])
    if dry_run:
        return "WOULD-UPDATE" if existing_id else "WOULD-CREATE"
    if existing_id:
        notion.pages.update(page_id=existing_id, properties=properties)
        return "UPDATED"
    notion.pages.create(parent={"database_id": DB1}, properties=properties)
    return "CREATED"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--since", type=date.fromisoformat, default=None,
                   help="processa apenas registros com 'updated_at' >= YYYY-MM-DD")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--input", type=Path,
                   default=Path("data/processed/records.jsonl"))
    args = p.parse_args()

    if not args.input.exists():
        print(f"input não encontrado: {args.input}", file=sys.stderr)
        return 2

    counts = {"CREATED": 0, "UPDATED": 0, "WOULD-CREATE": 0, "WOULD-UPDATE": 0, "ERROR": 0}
    with args.input.open() as fh:
        for i, line in enumerate(fh):
            if not line.strip():
                continue
            rec = json.loads(line)
            if args.since and rec.get("updated_at", "9999-99-99") < args.since.isoformat():
                continue
            if args.limit and sum(counts.values()) >= args.limit:
                break
            try:
                outcome = upsert(rec, dry_run=args.dry_run)
                counts[outcome] += 1
                print(f"{outcome:<14} {rec['external_id']}")
            except APIResponseError as exc:
                counts["ERROR"] += 1
                print(f"ERROR          {rec.get('external_id', '?')}: {exc}",
                      file=sys.stderr)
    print("---", counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Primeira execução prudente (dry-run, limitado, contra Notion real):**

```bash
# (C) Pressupõe env 'iconocracia' ativo e ~/.config/iconocracy/.env preenchido
cd ~/iconocracy-corpus
pip install notion-client python-dotenv   # ou: uv add ... se for caso de uv puro
python tools/scripts/notion_sync.py --dry-run --limit 5
```

Saída esperada (algo como):

```
WOULD-CREATE   FR_GRAVURA_1834_BNF_017
WOULD-CREATE   FR_GRAVURA_1834_BNF_018
WOULD-UPDATE   IT_OLEO_1881_UFFIZI_004
WOULD-CREATE   DE_ESTAMPA_1902_BSB_023
WOULD-CREATE   FR_GRAVURA_1834_BNF_019
--- {'CREATED': 0, 'UPDATED': 0, 'WOULD-CREATE': 4, 'WOULD-UPDATE': 1, 'WOULD-CREATE': 0, 'ERROR': 0}
```

Erros típicos e fix:
- `APIResponseError: Could not find database` → DB1 ainda não tem a integração conectada (§ 3.3, passo 4).
- `APIResponseError: property "external_id" does not exist` → criar a propriedade na DB1 antes (tipo *Text*).
- `APIResponseError: validation_error … select option` → o valor de `país`, `suporte` ou `acervo` não existe nas opções da DB1; opções *select* não são auto-criadas em algumas variantes da API; usar `multi_select` ou pré-criar as opções no Notion.

### 3.4 Rotação e remoção da credencial exposta (DM-001)

> **Esta seção é a mais sensível do manual.** Não há margem para hesitação na ordem dos passos. Leia toda a seção antes de executar qualquer comando.

**Lacunas explícitas a preencher antes de começar.**

A inspeção pública do repositório, em 2026-05-11, não localizou um documento `DM-001` no `README` nem no `CLAUDE.md` acessíveis; o arquivo `SECURITY.md` é mencionado mas seu conteúdo não foi inspecionado por este manual. Antes de executar a sequência abaixo, a pesquisadora precisa preencher (uma vez, no notebook, em arquivo local):

- [ ] **Que credencial está exposta?** (Notion `secret_…`? Anthropic `sk-ant-…`? Google API key? OAuth client_secret? Token Hugging Face? Outra?)
- [ ] **Em que commit e arquivo?** (`git log --all -S '<prefixo-do-segredo>' --source --remotes` para mapear.)
- [ ] **Algum colaborador externo já clonou o repo?** (Force-push obriga rebase deles.)
- [ ] **Há mirror público em HF Hub ou Zenodo com o segredo?** (Cada mirror é uma cópia que precisa ser remediada à parte.)

**Sequência prescrita.** Os passos *não* podem ser reordenados.

#### Passo 1 — REVOGAR antes de reescrever

Ir ao console do provedor (Notion → *My integrations*, Anthropic → *API keys*, Google → *Credentials*, etc.) e **invalidar o token agora**. Antes da revogação, reescrever histórico apenas torna o segredo mais difícil de encontrar — não impede uso até que o cache Git/CDN sirva ainda a versão antiga. **Revogação no provedor é a única ação que torna o segredo inerte.**

#### Passo 2 — Mapear localização exata

```bash
# (C) Pressupõe ~/iconocracy-corpus clonado; trabalhar a partir dele
cd ~/iconocracy-corpus

# Encontra commits que adicionaram OU removeram o segredo (substring)
git log --all --full-history -S '<PREFIXO_DO_SEGREDO>' --source --remotes \
  --pretty=format:'%h %ai %s'

# Confere o arquivo afetado em cada commit listado
git show <hash>:<caminho-suspeito> | head -50
```

#### Passo 3 — Backup defensivo

```bash
# (C)
cd ~
tar -czf iconocracy-corpus-backup-$(date +%F).tar.gz iconocracy-corpus/
```

#### Passo 4 — Reescrever histórico com `git-filter-repo`

`git-filter-repo` é o substituto oficialmente recomendado para `git filter-branch` (que está obsoleto há anos) e para BFG (que ainda funciona mas é menos preciso para *replace text*).

```bash
# (U) Instala git-filter-repo
sudo apt install git-filter-repo

# Clone fresh-mirror — git-filter-repo recusa rodar em repo com remotes default
cd /tmp
git clone --mirror git@github.com:anavvanzin/iconocracy-corpus.git
cd iconocracy-corpus.git
```

Há duas operações possíveis. Escolher uma delas:

**Opção A — apagar substring sensível em todo o histórico, mantendo arquivos:**

```bash
# (C) Substitua PADRAO pelo prefixo único do segredo (mínimo 8 caracteres)
echo 'PADRAO==>REMOVED' > /tmp/replacements.txt
git filter-repo --replace-text /tmp/replacements.txt
```

**Opção B — eliminar arquivo inteiro de todo o histórico:**

```bash
# (C) Se o segredo está em um arquivo específico (p.ex. tools/scripts/.env)
git filter-repo --path tools/scripts/.env --invert-paths
```

Em muitos casos a sequência correta é fazer **as duas** (B primeiro, A depois — segredos têm vida própria; podem ter sido copiados para README de exemplo em algum commit).

#### Passo 5 — Force push (irreversível)

Antes de executar, conferir três vezes que:
- O Passo 1 (revogação) foi feito e o provedor confirmou.
- O Passo 3 (backup) está em local seguro fora do diretório do projeto.
- Não há *pull requests* abertos sem patches já mergeados para a HEAD nova.

```bash
# (C) Restaurar remote no mirror, então force-push
cd /tmp/iconocracy-corpus.git
git remote add origin-anavvanzin git@github.com:anavvanzin/iconocracy-corpus.git
git push --force --mirror origin-anavvanzin
```

Em paralelo, eliminar o clone original de trabalho (que ainda contém o histórico antigo) e re-clonar:

```bash
# (C) No diretório de trabalho real
cd ~
mv iconocracy-corpus iconocracy-corpus.preDM001-$(date +%F)
git clone git@github.com:anavvanzin/iconocracy-corpus.git
```

#### Passo 6 — Invalidar caches do GitHub

GitHub mantém *forks*, *pull requests* e *API responses* cacheados após force-push. Para um repo público com credencial exposta, abrir solicitação de suporte:

1. Em `https://support.github.com/contact/personal-data` selecionar **Sensitive Data Removal**.
2. Listar URLs específicas de blobs antigos (`/raw/<sha>/<path>`), commits (`/commit/<sha>`) e API responses (`/api/v3/repos/.../contents/<path>?ref=<sha>`).
3. Anexar evidência de revogação (e-mail do provedor + screenshot da página *Audit log* mostrando revogação).
4. Arquivar a resposta do GitHub em `docs/security/DM-001-resolution.md` no próprio repositório.

#### Passo 7 — Re-emitir credencial nova; armazenar com discrição

```bash
# (C) Nova credencial vai apenas no .env local, modo 600
echo "NOTION_TOKEN=secret_NOVA_CHAVE_AQUI" >> ~/.config/iconocracy/.env
chmod 600 ~/.config/iconocracy/.env

# Confirma que o repo NÃO referencia .env de forma rastreada
cd ~/iconocracy-corpus
grep -r "secret_" --include="*.py" --include="*.md" .   # deve retornar 0 hits
```

#### Passo 8 — Pre-commit hook anti-segredos (prevenção)

Instalar `pre-commit` e configurar com `gitleaks`:

```bash
# (U) Instalação via uv (mais rápido que pip)
uv tool install pre-commit

# Em ~/iconocracy-corpus
cd ~/iconocracy-corpus
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
EOF

pre-commit install
pre-commit run --all-files   # primeiro scan completo
```

A partir daqui, qualquer commit que contenha string parecida com chave de API é bloqueado localmente — antes mesmo de chegar ao GitHub.

#### Passo 9 — Documentar a resolução

Criar `docs/security/DM-001-resolution.md` com:

```markdown
# DM-001 — Resolução

**Data da revogação:** 2026-05-DD HH:MM (UTC)
**Credencial:** <tipo de chave, prefixo apenas, nunca o valor completo>
**Provedor:** <Notion / Anthropic / Google / outro>
**Commits afetados:** <lista de hashes pré-rewrite>
**Comando filter-repo:** `git filter-repo --replace-text /tmp/replacements.txt`
**Confirmação do provedor:** anexo `email-revogacao-2026-05-DD.eml`
**Caches GitHub:** ticket #<número> aberto em <data>; resposta em <data>
**Hook preventivo:** gitleaks via pre-commit, instalado em 2026-05-DD

## Lições aprendidas
- …
```

### 3.5 Mirror Hugging Face (após o force-push)

Se o `iconocracy-corpus` é replicado para Hugging Face Hub como *snapshot* público, é preciso recriar o mirror com o histórico limpo. O token HF anterior, se estava no mesmo `.env` afetado, **também precisa ser rotacionado**.

```bash
# (U) Instala CLI Hugging Face
uv tool install huggingface_hub
huggingface-cli login        # cole o token NOVO

# (C) Pressupõe repo HF já existe
cd ~/iconocracy-corpus
# limpar refs antigas e re-push (estratégia simples — ver doc HF para casos complexos)
huggingface-cli upload anavvanzin/iconocracy-corpus . --repo-type dataset --revision main
```

### 3.6 Gallica MCP server

O monorepo da tese declara um servidor MCP em Node para acesso programático à Gallica/BnF, rodando em `localhost:3001` [F-05]. Setup no Debian:

```bash
# (C) Pressupõe nvm + Node LTS instalados (§ 2.6)
cd ~/iconocracy-corpus/<caminho-do-gallica-mcp>
npm ci                       # instalação determinística por package-lock.json
node server.js               # ou o comando declarado no package.json scripts.start
```

Para tornar o servidor disponível à Claude Code CLI, registrar como MCP em `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "gallica": {
      "command": "node",
      "args": ["/home/ana/iconocracy-corpus/<caminho>/server.js"],
      "env": {}
    }
  }
}
```

Verificar no Claude:

```
/mcp
```

A entrada `gallica` deve aparecer como `connected`.

---

## Definition of done — verificação ponta-a-ponta

Após executar o checklist completo, esta tabela deve passar 100%:

| Verificação | Comando | Esperado |
|---|---|---|
| Claude Code instalado | `claude --version` | versão ≥ 2.1.89 |
| Diagnóstico Claude Code | `claude doctor` | nenhum warning crítico |
| GPG fingerprint conferido | `gpg --fingerprint security@anthropic.com` | `31DD DE24 … 1A7E CACE` |
| Env Python | `conda activate iconocracia && python -c "import sys; print(sys.version)"` | `3.10+` |
| Volume do corpus | `wc -l ~/iconocracy-corpus/data/processed/records.jsonl` | `165` (ou número atualizado) |
| Pandoc disponível | `pandoc --version` | `pandoc 2.x` ou `3.x` |
| Build tese DOCX | `make -C ~/iconocracy-corpus/vault/tese/ docx` | gera `.docx` sem erro |
| Build tese PDF | `make -C ~/iconocracy-corpus/vault/tese/ pdf` | gera `.pdf` sem erro |
| rclone OK | `rclone lsd drive-iconocracy:ICONOCRACIA` | lista subpastas |
| Auditoria de nomes | `python tools/scripts/audit_corpus_names.py data/raw/` | `OK — todos os arquivos respeitam a convenção.` |
| Vault Obsidian sincronizado | criar nota teste em uma máquina, conferir aparecimento em outra em < 120 s | OK |
| Notion auth | `python tools/scripts/notion_sync.py --dry-run --limit 5` | 5 linhas `WOULD-CREATE` ou `WOULD-UPDATE`, sem `401` |
| DM-001 revogada | `curl -H "Authorization: Bearer <chave-antiga>" https://api.<provedor>/...` | resposta `401 Unauthorized` |
| Gitleaks ativo | criar commit com fake-key no body | hook bloqueia o commit |
| Gallica MCP | em Claude: `/mcp` | linha `gallica` em estado `connected` |

---

## Apêndice A — Variação Zsh

Para a Ana que decidir migrar para Zsh:

```bash
# (U) Instala zsh e troca shell de login
sudo apt install zsh
chsh -s $(which zsh)
# faça logout/login para tomar efeito

# (U) Starship init para Zsh
echo 'eval "$(starship init zsh)"' >> ~/.zshrc

# (J) Opcional — zsh-autosuggestions, sem oh-my-zsh
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/zsh-autosuggestions
echo 'source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh' >> ~/.zshrc

# (J) Opcional — zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting ~/.zsh/zsh-syntax-highlighting
echo 'source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh' >> ~/.zshrc
```

Esta variação dá ~90% do valor de `oh-my-zsh` com ~5% da superfície de manutenção.

## Apêndice B — Alternativa Python `uv` puro

Caso a recomendação híbrida da § 2.5 seja rejeitada e a Ana decida migrar o monorepo para `uv` puro:

```bash
# (U) Converte environment.yml para pyproject.toml/requirements.txt
# Não há conversor oficial; o procedimento é manual:
# 1. Listar pacotes de environment.yml (campos `dependencies:` e `pip:`)
# 2. Criar pyproject.toml com [project] e [project.optional-dependencies]
# 3. uv pip compile pyproject.toml -o requirements.lock
# 4. uv sync --frozen para validar reprodutibilidade

# (C) Após pyproject.toml em ~/iconocracy-corpus
cd ~/iconocracy-corpus
uv venv --python 3.10
uv sync
```

O custo da migração inclui: revisar `tools/scripts/` em busca de imports condicionais (e.g. `try: import GDAL`), confirmar que pacotes binários *não-Python* (TeX, pandoc, ImageMagick) continuam vindo do `apt`, e atualizar `make` targets se algum referencia `conda activate`.

## Apêndice C — Comandos de emergência

| Sintoma | Comando |
|---|---|
| Claude trava sessão | `Ctrl+C` (uma vez para cancelar tool em curso; duas para sair) |
| Vault Obsidian em conflito | `find ~/Documents/Obsidian -name '*.sync-conflict-*' | head` |
| `rclone bisync` travado em "abort" | `rclone bisync ... --resync` (recria baseline; cuidado: assume estado atual como verdade) |
| Git refusing to commit (.env staged) | `git restore --staged .env && git rm --cached .env` |
| Perdeu acesso ao token Notion | Notion → Settings → My connections → revogar e recriar |
| Erro 503 na Anthropic | `status.anthropic.com`; aguardar; usar Claude web em offline temporário |

---

*Fim do manual. Para o roteiro tático sábado-domingo, ver [`checklist-primeiro-fds.md`](checklist-primeiro-fds.md).*
