# Esquema operacional — Airtable do corpus ICONOCRACIA

Este documento especifica a estrutura de dados da base **“Iconocracia — Corpus e Tese”**. A base organiza o corpus como arquivo vivo e auditável; o GitHub recebe documentação versionada e snapshots públicos.

## Princípio de modelagem

- **Itens do Corpus** é a tabela-mãe.
- O campo `ID do corpus` é a chave pública e estável de ligação.
- Os valores brutos não devem ser substituídos silenciosamente por valores normalizados.
- Os campos de codificação são distintos dos campos de descrição e dos campos de interpretação.
- Um registro pode existir no catálogo sem estar validado, codificado ou selecionado para escrita.

## Tabela 1 — Itens do Corpus

| Campo | Tipo sugerido | Uso |
|---|---|---|
| `ID do corpus` | texto, campo primário | Identificador estável e chave de ligação. |
| `Título` | texto | Título preferencial da obra/registro. |
| `Título alternativo` | texto longo | Variações linguísticas, títulos de catálogo e traduções. |
| `Ano` | número | Ano conhecido; não usar para intervalos. |
| `Data textual` | texto | Data original, intervalo ou atribuição incerta. |
| `Período` | seleção única | Normalização histórica para filtros e gráficos. |
| `País` | seleção única | País de produção, emissão ou circulação principal. |
| `Região / circulação` | múltipla seleção | Espaços de circulação, império, colônia ou rede transatlântica. |
| `Criador / emissor` | texto | Artista, instituição, governo, casa da moeda ou impressor. |
| `Meio` | seleção única | Técnica ou medium normalizado. |
| `Suporte` | seleção única | Moeda, selo, cédula, gravura, pintura, monumento etc. |
| `Motivos` | múltipla seleção | Justitia, Marianne, Britannia, República, Liberty, virtudes e correlatos. |
| `Atributos visuais` | múltipla seleção | Venda, espada, balança, tridente, leão, barrete frígio, escudo etc. |
| `Tags analíticas` | múltipla seleção | Colonialidade, guerra, serialidade, pedagogia cívica, judicialização etc. |
| `Descrição` | texto longo | Descrição factual e contextual. |
| `URL da obra` | URL | Página do item na fonte de origem. |
| `URL da imagem` | URL | Reprodução ou thumbnail, quando disponível. |
| `Fonte / arquivo` | vínculo para Fontes e Arquivos | Proveniência institucional ou bibliográfica. |
| `Citação ABNT` | texto longo | Referência pública para uso editorial. |
| `Em escopo` | caixa de seleção | Marca de pertencimento ao corpus definido. |
| `Estado do registro` | seleção única | Fluxo de curadoria e validação. |
| `Observações / QA` | texto longo | Notas de inconsistência, incerteza ou decisão de normalização. |

### Valores controlados: `Estado do registro`

1. `bruto / importado`
2. `validado no ledger`
3. `em escopo`
4. `codificado`
5. `revisado`
6. `selecionado para escrita`
7. `publicado / exibido`
8. `excluído ou duplicado`

## Tabela 2 — Codificação Visual

Cada registro deve vincular-se a exatamente um `ID do corpus`; recodificações ou discordâncias devem ser armazenadas como linhas separadas, não sobrescritas.

| Campo | Tipo sugerido | Uso |
|---|---|---|
| `Registro de codificação` | texto, campo primário | Identificador da rodada de codificação. |
| `Item do Corpus` | vínculo para Itens do Corpus | Obra codificada. |
| `Desincorporação` | número 0–3 | Indicador ordinal. |
| `Rigidez postural` | número 0–3 | Indicador ordinal. |
| `Dessexualização` | número 0–3 | Indicador ordinal. |
| `Uniformização facial` | número 0–3 | Indicador ordinal. |
| `Heraldização` | número 0–3 | Indicador ordinal. |
| `Enquadramento arquitetônico` | número 0–3 | Indicador ordinal. |
| `Apagamento narrativo` | número 0–3 | Indicador ordinal. |
| `Monocromatização` | número 0–3 | Indicador ordinal. |
| `Serialidade` | número 0–3 | Indicador ordinal. |
| `Inscrição estatal` | número 0–3 | Indicador ordinal. |
| `Índice de purificação` | fórmula ou número | Média dos dez indicadores; guardar também o valor exportado quando houver. |
| `Regime iconocrático` | seleção única | Fundacional, normativo, militar ou outra categoria documentada. |
| `Codificador(a)` | colaborador ou texto | Responsável pela codificação. |
| `Data de codificação` | data | Data da rodada. |
| `Validação` | seleção única | Pendente, revisado, divergente, confirmado. |
| `Notas metodológicas` | texto longo | Justificativa da pontuação, limitação ou discordância. |

## Tabela 3 — Casos Argumentativos

| Campo | Tipo sugerido | Uso |
|---|---|---|
| `Caso argumentativo` | texto, campo primário | Nome editorial do caso. |
| `Item do Corpus` | vínculo para Itens do Corpus | Figura/obra de referência. |
| `Capítulo` | seleção única | Destino principal na tese. |
| `Pergunta ou hipótese` | texto longo | Problema que o caso ajuda a responder. |
| `Tese interpretativa` | texto longo | Afirmação analítica concisa e defensável. |
| `Evidência visual` | texto longo | Detalhes formais e materiais que sustentam a tese. |
| `Conceitos-chave` | múltipla seleção | Iconocracia, colonialidade, alegoria, serialidade etc. |
| `Prioridade de escrita` | seleção única | Agora, depois, arquivo. |
| `Imagem / figura` | anexo ou URL | Reprodução para escrita e apresentação. |
| `Legenda de trabalho` | texto longo | Legenda editorial em construção. |
| `Citação ABNT` | texto longo | Referência pronta para uso. |
| `Frase de uso` | texto longo | Formulação reaproveitável no capítulo ou apresentação. |

## Tabela 4 — Fontes e Arquivos

| Campo | Tipo sugerido | Uso |
|---|---|---|
| `Fonte / arquivo` | texto, campo primário | Nome da instituição, catálogo ou referência. |
| `Tipo de fonte` | seleção única | Museu, arquivo, biblioteca, hemeroteca, catálogo, obra secundária. |
| `Instituição` | texto | Titular ou responsável pela coleção. |
| `País` | seleção única | Localização institucional. |
| `URL` | URL | Link de acesso ou catálogo. |
| `Referência ABNT` | texto longo | Citação bibliográfica. |
| `Nível de evidência` | seleção única | Primária, institucional, secundária, provisória. |
| `Direitos / atribuição` | texto longo | Informação pública de atribuição e uso. |
| `Notas de proveniência` | texto longo | Lacunas, versões, mediações e advertências. |

## Convenções de dados

- Use `sem data`, `aproximado` ou intervalo apenas no campo `Data textual`; mantenha `Ano` vazio quando o dado não for pontual.
- Registre múltiplas identificações iconográficas no campo `Motivos`, sem forçar uma categoria única quando a imagem for ambivalente.
- Não use `0` para significar “não codificado”. `0` significa ausência do indicador; ausência de dado permanece vazia.
- Valores fora de 0–3 devem ser enviados para a tabela de divergências antes de qualquer normalização.
- Use URLs permanentes ou de catálogo quando houver; URLs de thumbnails são auxiliares e não substituem a referência da obra.

## Manifesto experimental e crosswalk de identidade

Todo extrato experimental deve publicar, ao lado do manifesto, um crosswalk
linha a linha que mantenha separados os identificadores de cada sistema. O
arquivo deve conter obrigatoriamente as seguintes colunas, sem reutilizar uma
como substituta de outra:

| Coluna | Conteúdo |
|---|---|
| `canonical_item_id` | Identificador canônico do item no corpus. |
| `registry_id` | Identificador do registro no catálogo ou ledger de origem. |
| `editorial_id` | Identificador usado na seleção ou camada editorial. |
| `hf_row_id` | Identificador estável da linha no dataset Hugging Face. |
| `bucket_object_key` | Chave completa do objeto no bucket, não apenas o nome do arquivo. |
| `source_record_url` | URL canônica do registro na fonte. |
| `link_method` | Método controlado de vínculo. |
| `link_evidence` | Evidência verificável que justificou o vínculo. |
| `review_status` | Estado da revisão humana, quando necessária. |
| `sample_eligible` | Booleano que controla a entrada na amostra. |
| `exclusion_reason` | Motivo controlado do bloqueio, quando houver. |

### Construção e precedência

O crosswalk deve ser construído a partir dos artefatos existentes, preservando
a proveniência de cada valor. Quando existir,
`data/processed/id_crosswalk.jsonl` é uma entrada prioritária, mas não dispensa
a validação de unicidade e de evidência. A ordem de resolução é:

1. vínculo documentado em crosswalk existente (`existing_crosswalk`);
2. igualdade de identificador emitido pelo mesmo sistema (`exact_id`);
3. igualdade de URL após normalização estritamente sintática (`canonical_url`);
4. decisão humana documentada (`manual_review`).

Cada linha deve registrar em `link_evidence` o artefato e o campo consultados
(e, quando aplicável, a decisão de revisão). Título não é chave: igualdade ou
similaridade de título pode somente abrir uma revisão e jamais confirmar a
identidade automaticamente.

### Bloqueios de amostragem

Antes da seleção experimental, `sample_eligible` deve ser `false` e
`exclusion_reason` deve registrar um dos motivos abaixo sempre que houver:

- `id_collision`: um identificador aponta para mais de um item ou dois itens
  reivindicam o mesmo identificador no mesmo sistema;
- `unresolved_multiple_primary_images`: há mais de uma imagem marcada como
  primária e nenhuma decisão documentada resolve a ambiguidade;
- `approximate_title_only`: o único sinal de correspondência é título exato ou
  aproximado, sem ID, URL canônica ou revisão humana conclusiva.

Campos ausentes permanecem vazios; não devem ser preenchidos por inferência.
Uma linha bloqueada pode permanecer no crosswalk para auditoria, mas não pode
entrar na amostra até a resolução explícita e registrada do problema.
