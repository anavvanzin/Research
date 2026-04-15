# Learnings Log

Registro estruturado de aprendizados técnicos capturados durante o desenvolvimento. Este arquivo documenta padrões, técnicas, insights e convenções descobertas que devem ser aplicadas em trabalhos futuros.

## Propósito

- Capturar conhecimento técnico adquirido durante desenvolvimento
- Documentar padrões e antipadrões identificados
- Preservar insights sobre ferramentas, APIs e fluxos de trabalho
- Criar base de conhecimento pesquisável para referência futura
- Evitar reaprender as mesmas lições repetidamente

## Quando registrar

- Descoberta de um padrão ou técnica que funciona bem
- Identificação de um antipadrão que deve ser evitado
- Insight sobre comportamento de ferramenta, API ou sistema
- Convenção útil que melhora produtividade ou qualidade
- Correção de conhecimento incorreto ou desatualizado
- Técnica de debugging que resolveu problema difícil

## Formato de entry

Cada learning deve seguir este formato:

```markdown
## [YYYY-MM-DD] Título descritivo do aprendizado

**ID**: LEARN-XXX
**Status**: draft|validated|applied|obsolete
**Category**: pattern|antipattern|technique|insight|convention
**Area**: frontend|backend|infra|tests|docs|config|process|tools
**Impact**: high|medium|low
**Tags**: #tag1 #tag2

### Context

O que estava sendo feito quando o aprendizado foi identificado.
Qual problema estava sendo resolvido ou tarefa sendo executada.

### Learning

Descrição clara e concisa do aprendizado.
O que foi descoberto, entendido ou validado.

### Evidence

Exemplos concretos, código, comandos ou resultados que demonstram o aprendizado.

```código ou exemplo```

### Application

Como aplicar este aprendizado no futuro.
Em quais situações ele é relevante.
Checklist ou passos práticos se aplicável.

### Related

- **Files**: arquivos relevantes
- **Errors**: ERRORS.md entries relacionados (ERROR-XXX)
- **Features**: FEATURE_REQUESTS.md entries relacionados
- **Docs**: documentação externa relevante
```

## Valores de campos

### Status
- `draft`: aprendizado recém-capturado, ainda não validado
- `validated`: confirmado como correto e útil
- `applied`: já sendo usado ativamente no trabalho
- `obsolete`: não mais relevante (ferramenta mudou, contexto diferente)

### Category
- `pattern`: abordagem que funciona bem e deve ser repetida
- `antipattern`: abordagem que causa problemas e deve ser evitada
- `technique`: método específico para realizar uma tarefa
- `insight`: entendimento sobre como algo funciona
- `convention`: acordo ou padrão a seguir para consistência

### Area
- `frontend`: UI, componentes, CSS, frameworks front-end
- `backend`: APIs, servidores, lógica de negócio
- `infra`: deploy, CI/CD, containers, cloud
- `tests`: testes unitários, integração, e2e
- `docs`: documentação, comentários, READMEs
- `config`: configuração de ferramentas e ambientes
- `process`: fluxos de trabalho, metodologias
- `tools`: CLIs, editores, utilitários

### Impact
- `high`: afeta significativamente produtividade ou qualidade
- `medium`: melhoria notável mas não crítica
- `low`: otimização menor ou caso de borda

<!--
================================================================================
TEMPLATE PARA COPIAR (remover este bloco de comentário ao usar)
================================================================================

## [YYYY-MM-DD] Título do aprendizado

**ID**: LEARN-XXX
**Status**: draft
**Category**: pattern|antipattern|technique|insight|convention
**Area**: frontend|backend|infra|tests|docs|config|process|tools
**Impact**: high|medium|low
**Tags**: #tag1 #tag2

### Context

[Descrever o contexto em que o aprendizado foi identificado]

### Learning

[Descrever o aprendizado de forma clara e concisa]

### Evidence

```
[Código, comandos ou exemplos que demonstram o aprendizado]
```

### Application

[Como aplicar este aprendizado no futuro]

### Related

- **Files**: 
- **Errors**: 
- **Features**: 
- **Docs**: 

================================================================================
-->

---

# Learnings registrados

<!-- Adicionar novos learnings abaixo desta linha, mais recente primeiro -->
