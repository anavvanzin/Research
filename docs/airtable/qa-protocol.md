# Protocolo de QA e reconciliação — corpus ICONOCRACIA

## Objetivo

Este protocolo controla divergências entre catálogo, ledger, codificação visual, extratos analíticos e seleção editorial. Seu propósito não é reduzir artificialmente o corpus a uma única contagem, mas tornar cada diferença rastreável, justificável e reproduzível.

## Camadas a reconciliar

| Camada | O que registra | Regra de interpretação |
|---|---|---|
| Universo de catálogo | Todos os registros identificados ou importados | Pode conter duplicatas, itens provisórios e registros ainda não verificados. |
| Ledger validado | Registros com ID estável, fonte e escopo verificados | É a referência operacional para status de validação. |
| Codificação visual | Avaliações pelos dez indicadores | Não ser codificado não implica ausência de atributo. |
| Extrato analítico | CSVs e notebooks derivados | É um recorte com finalidade específica, nunca uma definição automática do corpus total. |
| Casos argumentativos | Seleção para escrita e apresentação | É uma escolha interpretativa e editorial. |

## Tabela de divergências no Airtable

Criar uma tabela adicional chamada **Divergências e QA** quando a primeira importação integral for concluída.

| Campo | Tipo sugerido | Finalidade |
|---|---|---|
| `Ocorrência QA` | texto, campo primário | Identificador legível da ocorrência. |
| `Item do Corpus` | vínculo para Itens do Corpus | Registro afetado. |
| `Tipo de problema` | seleção única | Categoria da divergência. |
| `Campo afetado` | texto | Campo ou coluna em disputa. |
| `Valor bruto` | texto longo | Valor recebido na fonte/exportação. |
| `Valor alternativo` | texto longo | Valor conflitante ou normalizado. |
| `Camada de origem` | seleção única | Catálogo, ledger, codificação, extrato, caso argumentativo. |
| `Decisão` | seleção única | Manter, normalizar, dividir, mesclar, excluir, pendente. |
| `Justificativa` | texto longo | Razão histórica, técnica ou metodológica. |
| `Responsável` | texto ou colaborador | Quem tomou ou revisou a decisão. |
| `Data da decisão` | data | Registro da ação. |
| `Resolvido` | caixa de seleção | Fechamento do item. |

### Tipos de problema controlados

- duplicata provável;
- ID ausente ou divergente;
- URL quebrada ou não permanente;
- imagem ausente;
- atribuição incerta;
- data conflitante;
- país ou circulação ambígua;
- meio ou suporte não normalizado;
- motivo iconográfico ambivalente;
- valor de indicador fora da escala 0–3;
- índice composto inconsistente;
- regime iconocrático em revisão;
- item fora de escopo;
- citação ABNT incompleta;
- pendência de direitos ou atribuição.

## Fluxo de decisão

1. **Preservar:** manter o dado bruto e registrar a divergência.
2. **Comparar:** verificar catálogo, fonte institucional, ledger e exportação correspondente.
3. **Classificar:** indicar se o problema é técnico, histórico, iconográfico, bibliográfico ou editorial.
4. **Decidir:** escolher entre manter, normalizar, dividir, mesclar, excluir ou deixar pendente.
5. **Justificar:** redigir uma justificativa breve, pública e auditável.
6. **Versionar:** incluir a decisão no próximo snapshot público quando ela afetar dados publicados.

## Regras específicas para a codificação

- A escala dos dez indicadores é ordinal e limitada a `0`, `1`, `2` e `3`.
- Campo vazio significa **sem codificação**, não zero.
- Uma recodificação deve gerar nova linha em Codificação Visual, preservando a rodada anterior.
- Desacordo entre codificações não deve ser resolvido por sobrescrita; deve receber status `divergente` até haver decisão registrada.
- O `Índice de purificação` deve ser recalculado a partir dos dez indicadores quando todos estiverem presentes; qualquer exceção exige nota metodológica.

## Amostragem pré-registrada do piloto de visão computacional

### Frame e aleatorização

1. Aplicar primeiro o funil de elegibilidade e a normalização de suportes. Manter
   no manifesto também as linhas excluídas, com `exclusion_code` e sem posição no
   frame.
2. Ordenar todos os itens elegíveis por `canonical_item_id` em ordem Unicode
   crescente e numerá-los a partir de `1` em `sampling_frame_order`. IDs devem ser
   únicos e não nulos; empate ou duplicata bloqueia o sorteio.
3. Fixar `sampling_seed = "cv-pilot-0.1"`. Para obter uma ordem reproduzível
   dentro de cada estrato, ordenar pelo SHA-256, representado em hexadecimal, da
   cadeia UTF-8
   `cv-pilot-0.1\u001f<stratum>\u001f<canonical_item_id>`; usar
   `canonical_item_id` como desempate. Assim, a seed textual não depende do
   gerador pseudoaleatório de uma linguagem específica.
4. Sortear sem reposição: os primeiros `n_h` itens dessa ordem são a amostra
   principal do estrato; os demais constituem a reserva, na mesma ordem.

### Alocação e redistribuição

- Um estrato só pode ser incluído se tiver pelo menos três itens elegíveis
  (`N_h >= 3`). Estratos menores recebem `selection_probability = 0`,
  `selected = false`, `reserve_rank` vazio e o código controlado
  `STRATUM_LT_3`.
- Se houver exatamente seis estratos incluíveis, atribuir cinco itens a cada um
  (`n_h = 5`), totalizando 30.
- Nos demais casos, procurar um total factível nesta ordem previamente fixada:
  `30, 29, 31, 28, 27, 26, 25, 24`. Cada estrato incluído recebe no mínimo três
  e no máximo `min(6, N_h)` itens. Usar o primeiro total entre 24 e 31 que caiba
  entre a soma desses limites. Se nenhum couber, interromper a seleção e registrar
  a exceção; não alterar estratos nem escolher exemplos manualmente.
- Para o total factível, calcular a cota proporcional ideal
  `q_h = total * N_h / sum(N_h)`. Começar com três itens por estrato e distribuir
  as vagas restantes, uma por rodada, ao estrato com maior déficit
  `q_h - n_h` que ainda não atingiu o teto. Empates são resolvidos pelo nome do
  estrato em ordem Unicode crescente. Essa é a única regra de redistribuição.
- Registrar no manifesto o total pretendido, o total obtido, `N_h`, `n_h`, o
  método de alocação (`balanced_6x5` ou `bounded_proportional`) e, quando o total
  não for 30, uma justificativa objetiva da inviabilidade. É proibido substituir
  manualmente itens sorteados por “melhores exemplos”.

Para cada estrato participante, `selection_probability = n_h / N_h`. Os itens
selecionados recebem `selected = true` e `reserve_rank` vazio. Os não selecionados
recebem `selected = false` e `reserve_rank = 1, 2, ...` conforme a continuação da
ordem hash dentro do estrato. O manifesto deve publicar
`sampling_frame_order`, `sampling_seed`, `stratum_size`,
`selection_probability`, `selected`, `reserve_rank` e `exclusion_code` para cada
linha.

## Checklist antes de um release público

- [ ] Cada linha possui `ID do corpus` único ou está marcada como duplicata.
- [ ] A contagem do release é declarada no manifesto.
- [ ] O manifesto indica a camada de origem e os critérios de inclusão.
- [ ] Campos vazios foram mantidos como vazios, sem conversão automática para zero.
- [ ] Valores fora da escala foram revisados ou marcados como pendentes.
- [ ] URLs de origem e citações foram preservadas.
- [ ] Notas de QA relevantes foram incluídas ou vinculadas.
- [ ] O frame de amostragem está ordenado, a seed confere e todos os campos de seleção e reserva foram publicados.
- [ ] Cada estrato incluído respeita mínimo 3 e máximo 6; qualquer total diferente de 30 está justificado no manifesto.
- [ ] O commit contém data, versão e descrição de alterações.

## Convenção de versões

Use o padrão `AAAA-MM-DD-camada-vN` nos nomes de release e diretórios. Exemplo:

```text
2026-06-23-catalogo-v1
2026-06-23-codificacao-v1
2026-06-23-casos-argumentativos-v1
```

A primeira linha de cada manifesto deve explicar se o snapshot contém o universo bruto, o ledger validado, a codificação disponível ou um extrato analítico.
