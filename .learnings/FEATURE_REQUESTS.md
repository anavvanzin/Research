# Feature Requests Log

Este arquivo registra solicitações de funcionalidade, melhorias e capacidades novas pedidas pelo usuário ou identificadas durante o trabalho.

## Propósito

- Documentar feature requests explícitos do usuário
- Rastrear ideias de melhoria identificadas durante desenvolvimento
- Priorizar implementações futuras
- Manter histórico de decisões sobre features

## Quando registrar

- Usuário solicita explicitamente uma nova funcionalidade
- Usuário pergunta "como faço X?" e X não existe ainda
- Durante trabalho, identifica-se necessidade de ferramenta/capability nova
- Usuário expressa frustração com limitação atual

## Formato de entry

```markdown
## [FEATURE-YYYYMMDD-NNN] Título breve da feature

**Status**: requested|planned|in_progress|implemented|rejected|deferred
**Priority**: critical|high|medium|low
**Area**: frontend|backend|infra|tests|docs|config|workflow
**Effort**: trivial|small|medium|large|epic
**Tags**: #tag1 #tag2

### Origin

[Quem solicitou: user|identified_during_work]
[Contexto da solicitação ou descoberta]

### Description

[Descrição detalhada da funcionalidade solicitada]
[O que o usuário quer fazer?]
[Qual problema isso resolve?]

### Use Case

[Cenário de uso específico]
[Exemplo concreto de como seria usado]

### Expected Impact

[Como isso melhora o workflow?]
[Quantos casos de uso isso cobre?]
[Qual a frequência de uso esperada?]

### Implementation Notes

[Ideias técnicas de como implementar]
[Ferramentas/libraries necessárias]
[Complexidade estimada]
[Dependências ou blockers]

### Related

- Files: [arquivos que precisariam ser modificados]
- Learnings: [referências a LEARNING-* entries relacionados]
- Issues: [links para issues ou tickets]
```

---

## Template (copiar e preencher para novos requests)

<!--
## [FEATURE-YYYYMMDD-NNN] Título breve

**Status**: requested
**Priority**: medium
**Area**: [área]
**Effort**: [esforço]
**Tags**: #feature-request

### Origin

### Description

### Use Case

### Expected Impact

### Implementation Notes

### Related
- Files: 
- Learnings: 
- Issues: 
-->

---

# Feature Requests registrados

<!-- Adicionar novos requests abaixo desta linha, mais recente primeiro -->

## [FEATURE-20250415-001] Configurar busca web

**Status**: requested
**Priority**: medium
**Area**: workflow
**Effort**: small
**Tags**: #feature-request #ambiguous #needs-clarification

### Origin

User perguntou: **"Como faço pra configurar para que busque na web?"**

Contexto: após configuração de MCP servers e habilitação do Templater no vault Obsidian.

### Description

**AMBIGUIDADE DETECTADA**: A pergunta pode ter três interpretações diferentes:

**1. Busca web via MCP Servers (para Claude usar durante conversas)**
   - Adicionar MCP servers de busca web (`brave-search`, `tavily`, `exa`)
   - Claude poderia buscar informações atualizadas na web durante as conversas
   - Complementaria o `context7` já habilitado (focado em docs técnicas)

**2. Busca web dentro do Obsidian (plugin para usuário buscar)**
   - Instalar plugin de busca web no vault (`Omnisearch`, `Web Search`, ou integração custom)
   - Usuário poderia buscar web diretamente do Obsidian
   - Funcionalidade nativa do Obsidian, não relacionada ao Claude

**3. Busca web para apoiar plano de estudos (usar MCP durante estudo)**
   - Usar MCP `context7` existente para buscar docs técnicas enquanto estuda "The Book of Secret Knowledge"
   - Configuração já disponível, apenas clarificar workflow de uso

### Use Case

**Caso 1 (MCP para Claude)**:
- Durante conversa sobre tecnologia, Claude busca informações atualizadas
- Exemplo: "qual a última versão do Kubernetes?" → busca web via MCP

**Caso 2 (Plugin Obsidian)**:
- Usuário está escrevendo nota e quer buscar referência na web
- Exemplo: atalho no Obsidian abre busca DuckDuckGo/Google inline

**Caso 3 (Apoio ao estudo)**:
- Durante Semana 1 (Shell), usuário pede "busca docs oficiais do fzf"
- Claude usa `context7` para trazer documentação atualizada

### Expected Impact

**Caso 1**: Aumento significativo de accuracy em perguntas sobre estado atual de tecnologias, notícias, versões recentes.

**Caso 2**: Melhoria no workflow de pesquisa dentro do Obsidian, integração mais fluida entre notas e referências web.

**Caso 3**: Workflow de estudo mais eficiente, menos context switching entre terminal/Obsidian/browser.

### Implementation Notes

**Caso 1 - MCP Servers de busca web**:
- Opções disponíveis no catálogo MCP Docker:
  - `brave-search`: busca via API Brave Search
  - `tavily`: busca otimizada para AI/research
  - `exa`: busca neural/semântica
- Comando: `docker mcp add brave-search` (ou tavily/exa)
- Requer API key (configurar via `docker mcp secret set`)
- Depois habilitar: `docker mcp enable brave-search`

**Caso 2 - Plugin Obsidian**:
- Opções:
  - **Omnisearch**: busca fuzzy no vault + integração web (mais popular)
  - **Web Search**: plugin específico para busca DuckDuckGo/Google
  - Custom integration via Templater + curl/fetch
- Instalação: baixar do community plugins ou via GitHub
- Configuração: `.obsidian/plugins/[plugin-id]/` + habilitar em `community-plugins.json`

**Caso 3 - Usar MCP context7 existente**:
- Já configurado e habilitado
- Workflow: usuário pede busca de docs técnicas durante conversa
- Nenhuma configuração adicional necessária

### Related

- Files: 
  - `.obsidian/community-plugins.json` (se Caso 2)
  - MCP config via Docker (se Caso 1)
- Learnings: 
  - `[LEARNING-20250415-001]` (ordem de configuração de plugins Obsidian, relevante se Caso 2)
- Issues: N/A

**AÇÃO NECESSÁRIA**: Aguardando usuário clarificar qual das três interpretações é a correta.
