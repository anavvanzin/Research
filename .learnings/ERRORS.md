# Errors Log

Este arquivo registra erros técnicos, falhas de execução e bugs encontrados durante o desenvolvimento do projeto.

## Propósito

- Documentar erros inesperados, stack traces e contexto de falha
- Facilitar debugging e troubleshooting futuro
- Identificar padrões de erro recorrentes
- Servir como base de conhecimento para prevenção

## Quando registrar

- Comandos que falharam inesperadamente
- Erros de execução de código (Python, TypeScript, Shell)
- Falhas de integração com APIs externas
- Problemas de configuração que causaram falha
- Bugs descobertos em código ou ferramentas

## Formato de entry

```markdown
## [ERROR-YYYYMMDD-HHMMSS] Título breve do erro

**Status**: open|investigating|resolved|wontfix
**Priority**: critical|high|medium|low
**Area**: frontend|backend|infra|tests|docs|config
**Severity**: blocking|major|minor|cosmetic
**Tags**: #tag1 #tag2

### Context

[Descrição do que estava sendo feito quando o erro ocorreu]
[Estado do sistema antes do erro]

### Error Details

**Command/Operation:**
```
[comando exato ou operação que falhou]
```

**Error Output:**
```
[stack trace completo ou mensagem de erro]
```

**Environment:**
- OS: [sistema operacional]
- Tool/Language: [ferramenta e versão]
- Working directory: [diretório de trabalho]
- Related files: [arquivos envolvidos]

### Root Cause

[Análise da causa raiz do erro]
[Por que o erro ocorreu?]

### Solution

[Solução aplicada ou steps para resolver]
[Comandos executados para fix]

### Prevention

[Como evitar este erro no futuro]
[Mudanças de processo, validações, checks]

### Related

- Files: [lista de arquivos modificados para resolver]
- Learnings: [referências a LEARNING-* entries relacionados]
- Issues: [links para issues ou tickets]
```

---

## Template (copiar e preencher para novos errors)

<!--
## [ERROR-YYYYMMDD-HHMMSS] Título breve

**Status**: open
**Priority**: medium
**Area**: [área]
**Severity**: [severidade]
**Tags**: #error

### Context

### Error Details

**Command/Operation:**
```

```

**Error Output:**
```

```

**Environment:**
- OS: 
- Tool/Language: 
- Working directory: 
- Related files: 

### Root Cause

### Solution

### Prevention

### Related
- Files: 
- Learnings: 
- Issues: 
-->

---

# Errors registrados

<!-- Adicionar novos errors abaixo desta linha, mais recente primeiro -->
