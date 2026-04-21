---
tipo: protocolo
status: ativo
created: 2026-04-21
scope: "/Users/ana/Research"
tags:
  - iconocracia
  - academic-pipeline
  - roteamento
  - santha
  - socratic
---

# Roteamento das Pipelines Academicas ICONOCRACIA

Este protocolo define como escolher e encadear pipelines academicas na tese
ICONOCRACIA sem estourar contexto, duplicar trabalho ou acionar a pipeline
completa quando um modo menor resolve.

Ordem padrao:

```text
Socratic first
-> Santha slot
-> hipotese testavel
-> plano de escrita
-> revisao adversarial
-> integridade/citacoes
```

O protocolo nao executa pesquisa, nao edita capitulos e nao altera corpus. Ele
decide qual skill usar, qual material carregar, qual produto esperar e qual
checkpoint bloqueia o avanco.

## Regra de Contexto Maximo

Cada rodada deve carregar no maximo um objeto principal:

- um capitulo;
- um artigo;
- uma matriz de hipoteses;
- um parecer;
- um runbook ou protocolo.

Materiais grandes entram por resumo e caminho local, nao por copia integral.
Se um pedido exigir mais de um objeto principal, dividir em rodadas.

## Triage

Todo pedido deve ser classificado em uma das rotas abaixo antes de
acionar qualquer pipeline.

### `research`

- Quando usar: pergunta, conceito, escopo ou bibliografia instavel.
- Skill/modo: `deep-research socratic`, `lit-review` ou `fact-check`.
- Entrada minima: pergunta ou tema + limite de escopo.
- Produto: Research Plan Summary, bibliografia ou verificacao.
- Bloqueio: nao escrever texto final se a pergunta nao convergiu.

### `write`

- Quando usar: ha argumento ou material e falta arquitetura textual.
- Skill/modo: `academic-paper plan`; depois `full` apenas se aprovado.
- Entrada minima: capitulo/artigo + objetivo textual.
- Produto: outline, mapa de evidencias e claims por secao.
- Bloqueio: nao usar `full` antes de `plan` para tese.

### `review`

- Quando usar: texto substantivo precisa de parecer ou banca simulada.
- Skill/modo: `academic-paper-reviewer full`, `guided` ou
  `methodology-focus`.
- Entrada minima: texto + alvo de revisao.
- Produto: objecoes, riscos e roadmap de revisao.
- Bloqueio: Devil's Advocate CRITICAL bloqueia fechamento.

### `integrity`

- Quando usar: texto quase pronto precisa checar citacoes, claims ou ABNT.
- Skill/modo: `citation-management`, `zotero-cite`, `abnt-format` ou
  protocolos de integridade.
- Entrada minima: texto + lista de referencias.
- Produto: lista fechada de correcoes ou limitacoes aceitas.
- Bloqueio: nao marcar como pronto com claims abertos.

### `publish`

- Quando usar: dataset, Space, companion ou release publico.
- Skill/modo: scripts do hub + HF release flow.
- Entrada minima: snapshot local validado.
- Produto: release ou plano de publicacao.
- Bloqueio: nao publicar antes de schema, diff, vault status e purificacao.

### `compile`

- Quando usar: gerar DOCX/PDF da tese ou capitulo.
- Skill/modo: `compilar-tese` ou `make -C vault/tese/`.
- Entrada minima: caminho do texto.
- Produto: DOCX/PDF compilado.
- Bloqueio: nao compilar versao final com `[VERIFICAR]` critico.

## Gates Operacionais

### 1. Socratic Gate

Aplicar quando houver incerteza sobre pergunta, contribuicao, metodo ou escopo.

Saida obrigatoria:

- pergunta de pesquisa em uma frase;
- tese provisoria;
- pressupostos;
- evidencia necessaria;
- riscos e objecoes provaveis;
- proximo gate recomendado.

Use `deep-research socratic` para problema de pesquisa e `academic-paper plan`
quando a pergunta ja existe, mas a estrutura textual ainda nao.

### 2. Santha Gate

O Santha method e metodo local da autora e ainda nao esta formalizado no
workspace. Ate haver definicao operacional, ele deve ser tratado como slot
obrigatorio de explicitacao, nao como metodo automatico.

Preencher o Santha Card:

```markdown
## Santha Card

- Objetivo:
- Sequencia de operacoes:
- Quando usar:
- Produto final:
- O que o metodo nao decide:
```

Regra: nao invocar o Santha method como justificativa se o Santha Card estiver
vazio ou generico. Nesse caso, registrar a lacuna e seguir para hipotese apenas
com a ressalva explicita.

### 3. Hypothesis Gate

Converter conceitos da tese em hipoteses testaveis. Para ICONOCRACIA, comecar
pelos quatro blocos:

- Contrato Sexual Visual;
- Feminilidade de Estado;
- Contrato Racial Visual;
- Purificacao Classica.

Saida obrigatoria:

```markdown
## Matriz de hipoteses

### Contrato Sexual Visual
- Hipotese:
- Predicao:
- Evidencia esperada:
- Falsificador:
- Destino: Cap. 1 / artigo

### Feminilidade de Estado
- Hipotese:
- Predicao:
- Evidencia esperada:
- Falsificador:
- Destino: Cap. 2

### Contrato Racial Visual
- Hipotese:
- Predicao:
- Evidencia esperada:
- Falsificador:
- Destino: Cap. 3

### Purificacao Classica
- Hipotese:
- Predicao:
- Evidencia esperada:
- Falsificador:
- Destino: Caps. 5-6
```

Use `hypothesis-generation` para montar a matriz. Para a tese, esquematicos
visuais sao opcionais salvo se a rodada pedir um relatorio completo.

### 4. Writing Gate

Usar `academic-paper plan` antes de qualquer escrita integral.

Saida obrigatoria:

- outline;
- mapa de evidencias;
- claims por secao;
- lacunas;
- word count alvo;
- material que entra e material que fica fora.

Para tese, trabalhar por capitulo ou artefato pequeno. A pipeline completa nao
deve ser usada como motor continuo da tese.

### 5. Adversarial Gate

Usar `academic-paper-reviewer` ou `scientific-critical-thinking`.

Preferencias:

- `academic-paper-reviewer full`: texto substantivo ou artigo quase pronto;
- `academic-paper-reviewer methodology-focus`: Cap. 5-6, endurecimento, IRR,
  estatistica e validade dos indicadores;
- `scientific-critical-thinking`: circularidade, vies, validade inferencial,
  relacao entre evidencia e conclusao.

Saida obrigatoria:

- objecoes prioritarias;
- risco metodologico;
- risco conceitual;
- revisao recomendada;
- itens bloqueantes.

### 6. Integrity Gate

Aplicar antes de qualificação, submissao ou release publico.

Checar:

- citacoes e referencias;
- claims historicos e teoricos;
- ABNT NBR 6023:2025;
- consistencia entre texto, corpus e notebooks;
- rastreabilidade quando houver dado do corpus.

Saida obrigatoria:

- corrigir;
- verificar;
- aceitar como limitacao;
- remover.

## Cenarios de Teste

- Ideia vaga de capitulo:
  `deep-research socratic`; nenhuma escrita direta.
- Capitulo com argumento mas sem estrutura:
  `academic-paper plan`; outline e mapa de evidencias.
- Artigo quase pronto:
  `academic-paper-reviewer full`; depois `academic-paper revision`.
- Debate sobre originalidade:
  Socratico + Hypothesis Gate + Devil's Advocate, nao pipeline completa.
- Checagem de Cap. 5-6:
  `methodology-focus` + `scientific-critical-thinking`.
- Santha method indefinido:
  preencher Santha Card; nao operar como metodo automatico.

## Defaults ICONOCRACIA

- Horizonte principal: qualificacao 2027.
- Lingua de resposta e tese: portugues; identificadores de codigo permanecem no
  original.
- Campo: historia do direito penal e iconografia juridica. Evitar deriva
  antropologica ou sociologica.
- `academic-research` e indice, nao executor principal.
- `academic-pipeline` so para artigos fechados ou capitulos quase prontos.
- `deep-research` resolve pesquisa; `academic-paper` resolve escrita;
  `academic-paper-reviewer` resolve revisao; integridade/citacoes fecham o ciclo.
