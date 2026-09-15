---
tags: [metodologia, microcorpus, retrieval, reprodutibilidade]
date: 2026-09-09
scope: seleção de consultas para comparação HOG/CLIP
status: ACTIVE
related:
  - ./2026-06-19-corpus-ssot-methodology.md
---

# Seleção reprodutível das consultas do microcorpus

**Status:** decisão metodológica obrigatória
**Data:** 2026-09-09
**Artefato canônico:** `hub/iconocracy-corpus/data/queries.csv`

## Decisão

`data/queries.csv` deve ser gerado **imediatamente depois** do congelamento do
microcorpus e **antes** de qualquer cálculo de descritores HOG, embeddings CLIP
ou rankings. Rankings não podem retroagir sobre a escolha das consultas.

A seleção contém exatamente 12 consultas e usa uma segunda seed fixa,
independente da seed empregada para construir ou congelar o microcorpus. O valor
da seed deve ser declarado no README do experimento e persistido como metadado
no CSV. Alterá-la caracteriza uma nova execução, que exige novo congelamento do
artefato e nova hash.

## Regra estratificada

O universo de sorteio é formado somente pelos itens que passam por todas as
validações estáticas da seção seguinte. A seleção não admite curadoria por
interesse, qualidade ou saliência visual.

1. Agrupar os itens elegíveis por `support_stratum`.
2. Se houver no máximo 12 estratos elegíveis, reservar uma vaga para cada
   estrato. Se houver mais de 12, sortear 12 estratos com a segunda seed, antes
   de sortear itens.
3. Distribuir as vagas restantes proporcionalmente ao número de itens elegíveis
   de cada estrato, pelo método dos maiores restos (quota de Hare). Empates nos
   restos são desfeitos por uma ordenação pseudoaleatória produzida pela mesma
   seed fixa.
4. Dentro de cada estrato, ordenar os IDs canônicos antes de aplicar o gerador
   pseudoaleatório e selecionar sem reposição. Essa ordenação torna o resultado
   independente da ordem física das linhas no manifesto.
5. Falhar, sem produzir arquivo parcial, se não houver 12 itens válidos ou se as
   reservas por estrato não puderem ser satisfeitas.

## Validações estáticas obrigatórias

Cada consulta selecionável deve satisfazer, antes do sorteio:

- possuir ao menos cinco candidatos elegíveis cujo `support_stratum` seja
  diferente do estrato da consulta;
- não possuir duplicata nem outra vista do mesmo objeto na galeria, considerando
  tanto o próprio item quanto todos os candidatos;
- ter seu ID canônico presente no manifesto congelado do microcorpus;
- apresentar status de elegibilidade final, e não provisório, pendente ou nulo.

A validação deve terminar com erro não zero e não escrever `queries.csv` quando
qualquer condição for impossível de verificar. Ausência de metadado de
duplicidade, identidade do objeto, estrato ou status é falha — nunca deve ser
interpretada como aprovação implícita.

## Contrato mínimo de `queries.csv`

O arquivo deve conter, no mínimo, as colunas:

| Coluna | Conteúdo |
| --- | --- |
| `query_id` | ID canônico presente no manifesto congelado |
| `support_stratum` | estrato usado na alocação |
| `selection_seed` | segunda seed fixa da seleção |
| `eligibility_status` | status final validado |
| `frozen_manifest_sha256` | SHA-256 do manifesto usado na seleção |
| `eligible_cross_stratum_candidates` | contagem validada, sempre maior ou igual a 5 |

As linhas devem ser ordenadas por `query_id`, usar UTF-8, cabeçalho explícito e
terminador de linha LF. Datas de execução, caminhos absolutos e ordem original
do manifesto não podem influenciar seu conteúdo, para que execuções idênticas
produzam a mesma hash.

## Gate antes dos rankings

Após a escrita atômica do CSV, calcular sua SHA-256 sobre os bytes finais e
registrá-la no README do experimento no formato:

```text
queries.csv SHA-256: <64 caracteres hexadecimais minúsculos>
```

O estágio de HOG/CLIP/ranking deve verificar simultaneamente que o arquivo tem
12 linhas de dados, que a hash recalculada coincide com a registrada no README
e que a hash do manifesto em cada linha coincide com o manifesto congelado. Se
qualquer verificação falhar, o pipeline deve parar antes de carregar imagens ou
calcular descritores.

## Ordem canônica do pipeline

1. finalizar elegibilidade e metadados de duplicidade/outras vistas;
2. congelar o manifesto do microcorpus;
3. validar o universo, alocar os 12 lugares e gerar `data/queries.csv`;
4. registrar no README a SHA-256 de `queries.csv`;
5. verificar os gates de integridade;
6. somente então calcular HOG, CLIP e rankings.
