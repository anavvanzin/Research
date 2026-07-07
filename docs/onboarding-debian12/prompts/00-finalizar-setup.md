# Prompt-Mestre — Finalização do Setup Debian 12

> **Uso:** abrir Claude Code numa sessão fresh dentro de `~/iconocracy-corpus` (ou `~/Research`), entrar em plan mode (`Shift+Tab` até aparecer "plan mode"), e colar o bloco abaixo na íntegra. **Não** acrescentar texto antes nem depois — o prompt é autocontido.
>
> **Quando usar:** sempre que precisar fechar o ciclo de setup do Debian após mudanças significativas no estado da máquina (formatação, upgrade de release, troca de notebook). O prompt audita o estado real antes de agir, então é seguro rodar várias vezes.
>
> **O que NÃO usar este prompt para:** redigir capítulos de tese, fazer pesquisa bibliográfica, manipular o corpus em massa. É um prompt de *engenharia de plataforma de pesquisa*, não de pesquisa propriamente dita.

---

## Versão do prompt

`00-finalizar-setup` · revisão 2026-05-11 · autora original: parceria Ana ↔ Claude (sessão de planejamento).

---

## Prompt (copiar a partir da linha seguinte até o fim do bloco)

```
Sou Ana Vanzin, doutoranda em Direito (PPGD/UFSC), redigindo a tese
ICONOCRACIA — Alegoria Feminina na História da Cultura Jurídica (Séc. XIX-XX).
Você é o meu copiloto de engenharia de pesquisa nesta sessão.

# MÁQUINA
- VAIO FE16, Ryzen 7-5825U, 32 GB RAM, 512 GB SSD NVMe
- Debian 12 (Bookworm), kernel 6.1
- Já estou logada como usuária regular; o sistema já tem alguma coisa
  configurada — não sei exatamente o quê, descubra antes de agir.

# MISSÃO DESTA SESSÃO
Finalizar o setup da máquina para que eu possa executar com sucesso toda a
tabela "Definition of Done" descrita em docs/onboarding-debian12/manual.md
(se o arquivo existir; caso contrário, trabalhe a partir das instruções
deste prompt e ofereça reconstruí-lo no encerramento).

O setup tem três camadas, conhecidas como:

  Camada 1 — Claude Code CLI + ~/.claude (memory, settings, mcp.json)
  Camada 2 — Stack acadêmica: apt base (git, curl, gpg, pandoc, texlive-*,
             ripgrep, fd-find, poppler-utils, imagemagick), Obsidian (.deb),
             Syncthing, Zotero 7 (tarball oficial), Git/gh, miniforge3
             (env 'iconocracia' a partir do environment.yml), uv (Astral),
             nvm + Node LTS, rclone, VS Code, Starship.
  Camada 3 — Integração GitHub ↔ Google Drive ↔ Notion:
             • clone de github.com/anavvanzin/iconocracy-corpus
             • rclone bisync entre ~/iconocracy-corpus/data/raw/ e
               drive-iconocracy:ICONOCRACIA/data/raw/, com filtro regex
               sobre a convenção {PAÍS}_{SUPORTE}_{ANO}_{ACERVO}_{SEQ}
             • scaffold de tools/scripts/notion_sync.py contra DB1
             • TRACK SEPARADA "DM-001": rotacionar credencial exposta no
               histórico Git via git-filter-repo, com sequência
               estritamente ordenada — revogar → mapear → backup →
               reescrever → force-push → re-emitir → instalar hooks →
               documentar.

# FASE 1 — AUDITORIA  (você está em plan mode; NÃO execute nada destrutivo)

Lance TRÊS subagentes Explore EM PARALELO (uma única mensagem com três
chamadas de ferramenta) com os focos abaixo. Cada subagente deve responder
em até 250 palavras, em tabela | componente | estado | evidência | gap |.

  Subagente A — Camada 1:
    • which claude ; claude --version ; claude doctor   (captura saída)
    • ls -la ~/.claude/ ; ls -la ~/.claude.json
    • test -f ~/.claude/CLAUDE.md && wc -l ~/.claude/CLAUDE.md
    • cat ~/.claude/settings.json   (se existir)
    • verificar ~/.claude/mcp.json ou .mcp.json no projeto
    • gpg --fingerprint security@anthropic.com
      (esperado terminar em 1A7E CACE)

  Subagente B — Camada 2:
    • dpkg -l | grep -E 'pandoc|texlive|ripgrep|fd-find|imagemagick|
       poppler-utils|obsidian|code|syncthing|gh'
    • which conda mamba uv node npm rclone starship zotero
    • node --version ; npm --version ; rclone version ; uv --version
    • test -d ~/.local/opt/miniforge3
    • conda env list   (se conda disponível)
    • systemctl --user status syncthing.service
    • test -d ~/Documents/Obsidian   ou   find ~ -maxdepth 4 -name '.obsidian' -type d
    • rclone listremotes   (procurar 'drive-iconocracy:')

  Subagente C — Camada 3:
    • test -d ~/iconocracy-corpus && cd ~/iconocracy-corpus &&
       git status && git remote -v && git log -1 --oneline
    • ls -la ~/iconocracy-corpus/{data,tools/scripts,schemas,docs} 2>/dev/null
    • test -f ~/iconocracy-corpus/tools/scripts/notion_sync.py &&
       head -20 ~/iconocracy-corpus/tools/scripts/notion_sync.py
    • test -f ~/.config/iconocracy/.env &&
       stat -c '%a %n' ~/.config/iconocracy/.env
       (NÃO leia o conteúdo)
    • test -f ~/iconocracy-corpus/.rclone-filter
    • test -f ~/iconocracy-corpus/.pre-commit-config.yaml
    • git log --all --pretty=format:'%h' | head -1
       (apenas confirma histórico; NÃO faça grep por chaves)
    • test -f ~/iconocracy-corpus/docs/security/DM-001-resolution.md

# FASE 2 — SÍNTESE

Consolide os três relatórios numa tabela única com colunas
[Camada | Item | Estado | Próxima ação | Risco se omitir]. Estado deve ser
exatamente um de: ✅ feito · 🟡 parcial · ❌ ausente · ⚠️ inconsistente.

Em seguida, proponha um plano de execução respeitando:
  • paralelizável: instalações apt, instalações de toolchains, edição de
    arquivos do usuário em ~/.claude, ~/.config/iconocracy
  • sequencial obrigatório: DM-001 — não comece outras tarefas durante a
    janela de rotação, para reduzir risco de erro humano
  • bloqueado por credencial: passos que exigem token novo do Notion,
    OAuth do rclone, ou kicks de browser — marque como "AGUARDA INPUT"
    no plano e siga adiante com o que for possível

# FASE 3 — APROVAÇÃO POR BLOCO

Use a ferramenta AskUserQuestion para confirmar comigo, em UMA chamada com
até quatro perguntas:

  Q1. Aprovar execução PARALELA das Camadas 1 e 2 (operações
      não destrutivas)?  [sim · sim com ajustes · adiar]
  Q2. Aprovar execução da Camada 3 sem ainda mexer no sub-bloco DM-001?
      [sim · adiar · pular Camada 3 hoje]
  Q3. DM-001: você já revogou o token no console do provedor?
      [sim · ainda não · não se aplica]
      — Se "sim", peça-me na pergunta seguinte (ou via texto) o prefixo
      do segredo (mínimo 8 caracteres; NÃO o segredo completo) para o
      git-filter-repo usar como padrão de substituição.
  Q4. Há mirror Hugging Face ativo a ser remediado também?
      [sim · não · não sei]

NÃO chame ExitPlanMode antes de coletar essas respostas. Se eu pedir para
adiar uma camada, registre isso no plano e siga sem ela.

# FASE 4 — EXECUÇÃO

Após aprovação:
  • Saia do plan mode chamando ExitPlanMode com lista explícita de
    allowedPrompts cobrindo: instalações apt, downloads via curl/wget,
    edição de arquivos em $HOME, operações git em ~/iconocracy-corpus,
    chamadas rclone, e (se aprovado) git push --force --mirror.
  • Lance subagentes em PARALELO para Camadas 1 e 2 (independentes).
  • Camada 3 não-DM-001 em SEQUÊNCIA depois (depende de Camada 2 pronta).
  • DM-001 SEMPRE sequencial e supervisionado, com confirmação textual
    minha antes de cada uma das ações abaixo:
        (a) clonar o mirror fresco em /tmp
        (b) rodar git filter-repo com --replace-text ou --path
        (c) git push --force --mirror para o origin
        (d) renomear o clone antigo de trabalho e re-clonar limpo
    Use a "Sequência prescrita" da seção 3.4 do manual.md como contrato
    inviolável. Se algum passo falhar, PARE e me reporte — não tente
    "consertar" por conta própria.

# REGRAS DE SEGURANÇA  (invioláveis, ordenadas por gravidade)

R1. NUNCA imprima nem ecoe segredos. Se um token aparecer em qualquer
    saída de comando, mascare como "<TOKEN_REDACTED>" antes de mostrar.
R2. NUNCA execute `git push --force` ou `git push --force-with-lease`
    sem confirmação explícita textual minha na mensagem imediatamente
    anterior.
R3. NUNCA use `sudo npm install -g` (a doc oficial Anthropic proíbe; é
    causa #1 de permission errors em Linux).
R4. NUNCA grave credenciais em arquivo rastreado pelo git. Tokens vão
    SEMPRE para ~/.config/iconocracy/.env (chmod 600).
R5. Se `claude doctor` reportar warning crítico (binário ausente,
    rede inalcançável, autoupdate falhando), PARE e me reporte antes
    de prosseguir com qualquer outra coisa.
R6. Se `rclone bisync --dry-run` mostrar diferenças que eu não tenha
    aprovado explicitamente, PARE — não execute sem `--dry-run`.
R7. Antes de qualquer `apt upgrade` massivo, mostre quantos pacotes
    serão atualizados (`apt list --upgradable | wc -l`) e espere "ok"
    meu antes de prosseguir.
R8. Se faltar algum dado necessário (token, ID de DB, prefixo de
    segredo, decisão metodológica), pergunte via AskUserQuestion —
    NUNCA invente placeholder e siga.
R9. Se uma ação for irreversível e custar mais do que 5 minutos de
    trabalho desfazer, transforme em ponto de confirmação textual
    explícito mesmo que esteja fora das R1–R8.

# DISCIPLINA DE OUTPUT

  • Antes de cada bloco de trabalho, UMA frase explicando o que vai fazer.
  • Após cada subagente terminar, sumário de 2–3 linhas (nada de despejar
    a saída inteira do subagente no canal principal).
  • Ao final da sessão, rode `/cost` e me reporte o custo total em USD.
  • Atualize (ou crie) docs/onboarding-debian12/checklist-primeiro-fds.md
    marcando itens concluídos com [x]. Se este arquivo não existir,
    gere uma versão enxuta a partir da síntese da Fase 2.
  • No encerramento, escreva
    docs/onboarding-debian12/sessao-finalizacao-YYYY-MM-DD.md  contendo:
        — diff de estado da máquina (antes/depois) em formato tabela
        — comandos efetivamente executados (lista, ordem temporal)
        — credenciais rotacionadas (tipo, provedor, data — NUNCA o valor)
        — decisões pendentes para a próxima sessão
        — custo da sessão em USD aproximado

# GLOSSÁRIO RÁPIDO  (consulte antes de pedir esclarecimento)

  • DM-001: decision memo interna — credencial exposta no histórico Git
    do iconocracy-corpus, ainda não rotacionada.
  • DB1: database Notion "Corpus Iconográfico", chave external_id.
  • Convenção de filename canônica:
        {PAÍS}_{SUPORTE}_{ANO}_{ACERVO}_{SEQ}.{ext}
        exemplo: FR_GRAVURA_1834_BNF_017.jpg
  • Env conda nominal: 'iconocracia' (criado a partir de environment.yml).
  • Mirror público presumido:
        huggingface.co/datasets/anavvanzin/iconocracy-corpus
    (confirmar existência durante a auditoria; se não existir, ignorar).
  • ABNT NBR 6023:2025 é a norma de referência bibliográfica para os
    drafts em português; nada nesta sessão deve quebrar a integração
    Better BibTeX / Pandoc / Citations já configurada.

Comece agora pela Fase 1. Não pule a auditoria, mesmo que pareça óbvio
que determinado componente está ausente — registre a evidência.
```

---

## Notas de uso (para Ana, não para Claude)

1. **Plan mode é mandatório.** Se a sessão entrar em modo normal por engano, encerre, abra de novo e volte ao plan mode antes de colar.
2. **Não acelerar Fase 3.** A tentação é responder "sim, pode tudo" — resista. A pergunta sobre o prefixo do segredo DM-001 é a única forma de Claude conseguir reescrever o histórico sem precisar ver o segredo completo.
3. **Se a Fase 2 mostrar a máquina mais pronta do que eu lembrava**, ótimo: a sessão termina mais rápido. O prompt não força execução desnecessária.
4. **DM-001 pode ser adiada.** Se você ainda não revogou o token no console do provedor (Q3 = "ainda não"), Claude vai pular a faixa DM-001 inteira e seguir com o resto. Volte ao prompt depois de revogar.
5. **Custo esperado da sessão completa:** US$ 0,80–2,50 dependendo de quanto da auditoria detectar tarefas ainda pendentes. Sessões só-auditoria custam ~US$ 0,30.

## Próximos prompts previstos

- `01-rodar-pipeline-corpus.md` — quando o pipeline `data/raw/ → records.jsonl → DB1` for executado em produção pela primeira vez.
- `02-compilar-tese-pdf.md` — entrega de capítulo: rodar `make pdf`, conferir bibliografia, gerar diff vs. versão anterior.
- `03-backup-mensal.md` — snapshot dirigido do vault Obsidian + `data/processed/` para SSD externo.
