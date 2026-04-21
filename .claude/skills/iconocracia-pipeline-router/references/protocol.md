---
tipo: protocolo
status: ativo
created: 2026-04-21
source: /Users/ana/Research/docs/academic-pipeline-routing-iconocracia.md
scope: /Users/ana/Research
---

# Protocolo Detalhado

Use este arquivo quando a tarefa exigir o checklist formal do roteador, os
templates completos dos gates, ou a conversao do protocolo em artefatos de
planejamento da tese.

## Ordem Padrao

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

Todo pedido deve ser classificado em uma das rotas abaixo antes de acionar
qualquer pipeline.

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

## Templates de Gates

### Socratic Gate

```markdown
## Research Plan Summary

- Pergunta:
- Tese provisoria:
- Pressupostos:
- Evidencia necessaria:
- Riscos e objecoes:
- Proximo gate:
```

### Santha Gate

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

### Hypothesis Gate

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

### Writing Gate

```markdown
## Plano de Escrita

- Outline:
- Mapa de evidencias:
- Claims por secao:
- Lacunas:
- Word count alvo:
- Entra no artefato:
- Fica fora:
```

### Adversarial Gate

```markdown
## Parecer Adversarial

- Objecoes prioritarias:
- Risco metodologico:
- Risco conceitual:
- Revisao recomendada:
- Itens bloqueantes:
```

### Integrity Gate

```markdown
## Integridade

| Item | Tipo | Status | Acao |
| --- | --- | --- | --- |
|  | claim/citacao/ABNT/corpus | corrigir/verificar/limitar/remover |  |
```

## Cenarios de Teste

- Ideia vaga de capitulo:
  `deep-research socratic`; nenhuma escrita direta.
- Capitulo com argumento mas sem estrutura:
  `academic-paper plan`; gerar outline e mapa de evidencias.
- Artigo quase pronto:
  `academic-paper-reviewer full`, depois `academic-paper revision`.
- Debate sobre originalidade:
  Socratico + Hypothesis Gate + Devil's Advocate, nao pipeline completa.
- Checagem de Cap. 5-6:
  `methodology-focus` + `scientific-critical-thinking`.
- Santha method indefinido:
  preencher Santha Card; nao operar como metodo automatico.

## Defaults

- Horizonte principal: qualificacao 2027.
- Resposta padrao em portugues; termos tecnicos preservados.
- Campo: historia do direito penal e iconografia juridica.
- Evitar deriva antropologica ou sociologica.
- `academic-research` funciona como indice.
- `academic-pipeline` fica restrita a artigos fechados ou capitulos quase
  prontos.
