# Visual Essay Refactor — Plano para Nova Sessão

**Data:** 2026-04-17
**Status:** aguardando sessão de implementação
**Arquivo atual:** `docs/superpowers/visual-essay-iconocracia.html`
** Problema:** o framing统计学 cautela em vez de insight historiográfico

---

## Problema Central

A versão atual inverte a lógica da tese. ICONOCRACIA é:
**O index iconométrico encontra padrões → O arquivo decide o que significam.**

A versão atual diz:
**O index não consegue determinar → É uma questão de arquivo.**

A diferença é fundamental. Na versão atual, o arquivo rescued os dados da irrelevância. Na tese, os dados são o ponto de partida e o arquivo é a autoridade interpretativa.

---

## O Que Mudar

### 1. Título e framing do essay
- **Antes:** "O que os números escondem"
- **Proposta:** "ICONOCRACIA — Padrões iconométricos e aarchive" ou manter "O que os números escondem" mas mudar o subtítulo para deixar claro que o archive é a conclusão, não a rescue

### 2. Seção monocromia — Reframe total

** ANTES (errado):
"Moedas são monocromáticas porque moedas são monocromáticas..."

** DEPOIS (correto):
"O que a análise encontra: a monocromia estatal varia por meio, por período, por regime — e o padrão não é trivial.
O que a archive revela: para cada item, a resposta sobre escolha estratégica vs. affordance material está nos arquivos de produção, nos catálogos de impressão, nas decisões editoriais.
O que o index não pode fazer sozinho."

### 3. "Archive box" — mudar framing
- **Antes:** "A questão que a quantificação não pode responder"
- **Proposta:** "O que o index não pode fazer sozinho — aarchive como autoridade interpretativa"

### 4. Takeaways — reframe item 3
- **Antes:** "A monocromatização é um problema historiográfico, não estatístico"
- **Proposta:** "Aarchive como autoridade interpretativa — o index encontra padrões, aarchive decide o que significam"

### 5. CSS — não precisa mudar (já está bom)
As cores, tipografia e layout estão OK. Mudar só conteúdo.

---

## Estrutura de Arquivos

```
docs/superpowers/
├── visual-essay-iconocracia.html      # versão atual (descartar)
├── visual-essay-refactored.html       # NOVO — com os cambios
├── plans/
│   └── visual-essay-refactor-plan.md  # este arquivo
```

---

## Tarefas de Implementação

### Passo 1 — Reescrever header
Mudar subtítulo para deixar claro o framing arquivo-first:
```html
<p class="subtitle">Análise multidimensional de 145 alegorias jurídicas — como o arquivo interpreta os padrões que o index encontra</p>
```

### Passo 2 — Reescrever seção monocromia (linhas ~378-418)
- Mudar título de "A armadilha" para "Cromia e materialidade"
- Reescrever os 3 finding cards como "O que o index encontra"
- Reescrever o reveal-box como "O que aarchive decide"
- Mudar o texto "A consequência para a tese:..." para algo como: "Aarchive como autoridade: para os itens com maior divergência core/mono, a pesquisa arquivística vai determinar se houve escolha estratégica ou affordance."

### Passo 3 — Reescrever Brazil note
O Brazil note sobre BR-016 vs BR-005 está bom em si, mas talvez mover para antes da seção de correlação — como exemplo concreto de "o index encontrou padrão, aarchive vai resolver".

### Passo 4 — Reescrever takeaway 3
- Remover "A monocromatização é um problema historiográfico"
- Substituir por: "O index iconométrico levanta a questão; aarchive decide. Para cada item com divergência forte core/mono, o arquivo de produção é o tribunal final."

### Passo 5 — Reescrever archive box
Mudar de "a questão que a quantificação não pode responder" para:
"O circuito: index → padrões → archive → interpretação. Sem o index, aarchive não sabe onde olhar. Sem aarchive, o index não sabe o que看见了."

### Passo 6 — Revisar Chart 2 (correlação)
O chart de correlação mostra bem os dados. Manter, mas mudar a legenda: em vez de "Dentro de gravuras: ρ = −0.01" mudar para "Padrão encontrado — aarchive decide o que significa".

---

## Pergunta em Aberto

"endurecimento doesn" — a mensagem cortou. Se era algo como:
- "endurecimento doesn't need this framing" — talvez o framing do essay inteiro mude
- "endurecimento doesn't make sense in this context" — preciso saber o que foi cortado

**Confirmar com pesquisadora antes de implementar.**

---

## Para a Próxima Sessão

1. Carregar este plano
2. Verificar o que "endurecimento doesn" queria dizer
3. Implementar passos 1-6
4. Testar no browser (servidor já rodando na porta 8899)
5. Salvar como `visual-essay-refactored.html`
