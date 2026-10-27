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

### Estado do pré-registro e congelamento do frame

**Sorteio bloqueado: o funil de elegibilidade específico do piloto ainda não
foi aprovado nem versionado.** Este documento fixa o contrato de randomização;
não declara um frame estável nem autoriza produzir uma seleção definitiva.
A seleção de consultas e a elegibilidade de galerias, descritas separadamente,
não substituem o funil de formação do microcorpus.

Antes de mudar `status` de `blocked_pending_frame` para `frozen`, o manifesto
precisa vincular os seguintes artefatos por repositório, commit completo, caminho
e SHA-256 dos bytes (não usar links móveis para `main`):

1. Snapshot de entrada e crosswalk de identidade, com `source_row_id` único,
   estável e rastreável por linha, inclusive quando o ID canônico estiver ausente.
2. Política de elegibilidade aprovada: campos consultados, predicados exatos,
   ordem dos filtros, tratamento de vazios e incertezas, duplicatas/outras vistas,
   escolha de imagem primária e vocabulário de exclusões com precedência quando
   houver mais de um motivo. Registrar responsável, aprovação e versão **antes**
   da avaliação do frame. Esses critérios ainda estão pendentes; não deduzi-los
   dos exemplos de `Suporte`, de títulos ou da disponibilidade de thumbnails.
3. Harmonização de suportes já aprovada no corpus: versão `1.0.0`, configuração
   [support_harmonization.yaml](https://github.com/anavvanzin/iconocracy-corpus/blob/443018ecbafdd7b97e4ef03d60e80c0ea7c3ae28/config/support_harmonization.yaml)
   e implementação `tools/scripts/support_harmonization.py` no mesmo commit
   `443018ecbafdd7b97e4ef03d60e80c0ea7c3ae28`. Executar a implementação canônica
   (NFKC, trim, casefold); não reimplementar a lista descritiva de transformações
   do YAML em outra ordem. Usar `support_stratum` como `stratum`, nunca a família.
   Preservar `support_raw` e `support_source`; gerar frequências antes/depois,
   inclusive categorias zero. Valores ausentes, proibidos, compostos ou não
   mapeados bloqueiam o lote e exigem adjudicação documentada no corpus. Não
   excluir silenciosamente essas linhas para permitir o sorteio.
4. Frame avaliado com uma linha por entrada, denominadores após cada filtro,
   relatório de rejeições e hash dos bytes finais. Pendências de identidade ou
   suporte impedem congelamento; exclusões finais aprovadas ficam na auditoria.

A implementação canônica, os snapshots e eventuais novos critérios vivem em
`anavvanzin/iconocracy-corpus`, conforme a
[decisão de ownership](../decisions/PR-32-support-harmonization-ownership.md).
O [template documental](sampling-manifest.template.json) permanece em `docs/`;
não é um snapshot, schema validador nem gerador. Não alterar `data/public/`
nesta PR. Critério ou mapeamento alterado exige nova versão, novo frame e nova
hash antes de qualquer sorteio, preservando o histórico.

### Frame e aleatorização

1. Verificar os gates acima. Publicar também as exclusões finais, com
   `exclusion_code`, e as pendências de revisão, sem fingir que são reservas.
   `eligibility_status` distingue `eligible`, `excluded` e `pending`.
2. `canonical_item_id` é exatamente o valor da chave pública `ID do corpus`,
   sem trim, mudança de caixa, remoção de acentos ou normalização Unicode.
   O crosswalk da seção de identidade deve comprovar esse vínculo com a fonte
   canônica; IDs de outros sistemas permanecem em suas colunas. ID ausente,
   vazio, com espaços nas extremidades, U+001F, Unicode inválido ou duplicado
   entre elegíveis bloqueia o sorteio. Corrigir na fonte antes de congelar;
   nunca gerar um ID a partir de título ou número de linha.
3. Ordenar todos os itens `eligible` por sequência de valores escalares Unicode
   de `canonical_item_id`, crescente, sem locale, e numerá-los desde `1` em
   `sampling_frame_order`. Isso inclui estratos com um ou dois elegíveis;
   `STRATUM_LT_3` impede participação, não apaga elegibilidade nem posição.
   Exclusões do funil e pendências não recebem posição no frame.
4. Fixar `sampling_seed = "cv-pilot-0.1"`. O payload SHA-256 é exatamente:

   ```python
   seed.encode("utf-8") + bytes([0x1f]) + stratum.encode("utf-8") + bytes([0x1f]) + canonical_item_id.encode("utf-8")
   ```

   Sem BOM, aspas, espaços extras, newline final ou sequência literal de seis
   caracteres `\u001f`. O separador é um único byte `1f`, U+001F real; no JSON
   sua representação é `"\u001f"` com **uma** barra no arquivo, que o parser
   decodifica para esse caractere. `stratum` não pode conter U+001F.
5. Ordenar por SHA-256 hexadecimal minúsculo de 64 caracteres **crescente**
   (equivalente à ordem lexicográfica dos 32 bytes sem sinal), depois por
   `canonical_item_id` Unicode crescente em caso de colisão hash.
6. Sortear sem reposição: primeiros `n_h` são selecionados; os demais elegíveis
   de estratos participantes são reservas, na mesma ordem, com `reserve_rank`
   desde `1`. Reservas não são excluídas e não substituem automaticamente itens.

Vetores sintéticos de conformidade (não são uma seleção do corpus):

| `stratum` | `canonical_item_id` | Payload em hexadecimal | SHA-256 |
|---|---|---|---|
| moeda | BR-001 | `63762d70696c6f742d302e311f6d6f6564611f42522d303031` | `0eaba708d95bfdb39eb74d8af7d745dcb149b2712a84c64b0f72f9a727996f27` |
| pintura | Á-01 | `63762d70696c6f742d302e311f70696e747572611fc3812d3031` | `4eab12fe49fb87fdb0ada81ad954bb272dd128232796c3ac01ca9c7391d2b45b` |

### Alocação e redistribuição

- Um estrato só pode ser incluído se tiver pelo menos três itens elegíveis
  (`N_h >= 3`). Preservar `stratum_size = N_h`, inclusive 1 e 2. Estratos menores recebem `selection_probability = 0`,
  `selected = false`, `reserve_rank` vazio e o código controlado
  `STRATUM_LT_3`.
- Se houver exatamente seis estratos incluíveis **e todos tiverem pelo menos
  cinco itens elegíveis** (`N_h >= 5` em cada estrato), atribuir cinco itens a
  cada um (`n_h = 5`), totalizando 30. Se qualquer um dos seis tiver
  `3 <= N_h < 5`, aplicar o fallback proporcional limitado abaixo.
- Nos demais casos, procurar um total factível nesta ordem previamente fixada:
  `30, 29, 31, 28, 27, 26, 25, 24`. Cada estrato incluído recebe no mínimo três
  e no máximo `min(6, N_h)` itens. Usar o primeiro total entre 24 e 31 que caiba
  entre a soma desses limites. Se nenhum couber, interromper a seleção e registrar
  a exceção; não alterar estratos nem escolher exemplos manualmente.
- Para o total factível, calcular a cota proporcional ideal
  `q_h = total * N_h / sum(N_h)` somente entre estratos incluíveis.
  Comparar déficits por aritmética racional exata (ou produtos inteiros
  equivalentes), sem arredondamento intermediário. Começar com três itens por estrato e distribuir
  as vagas restantes, uma por iteração (recalculando o déficit após cada vaga), ao estrato com maior déficit
  `q_h - n_h` que ainda não atingiu o teto. Empates são resolvidos pelo nome do
  estrato em ordem Unicode crescente. Essa é a única regra de redistribuição.
- Registrar no manifesto o total pretendido, o total obtido, `N_h`, `n_h`, o
  método de alocação (`balanced_6x5` ou `bounded_proportional`) e, quando o total
  não for 30, uma justificativa objetiva da inviabilidade. É proibido substituir
  manualmente itens sorteados por “melhores exemplos”.

Para cada estrato participante, `selection_probability = n_h / N_h`. Essa é a
probabilidade nominal do desenho sob a ordenação hash, não uma probabilidade
empírica estimada com a seed fixa. Publicar também `allocated_size = n_h` para
permitir reconstruir a razão sem depender do arredondamento decimal. Os itens
selecionados recebem `selected = true` e `reserve_rank` vazio. Os não selecionados
recebem `selected = false` e `reserve_rank = 1, 2, ...` conforme a continuação da
ordem hash dentro do estrato. O manifesto deve publicar
`sampling_frame_order`, `sampling_seed`, `stratum_size`,
`selection_probability`, `selected`, `reserve_rank` e `exclusion_code` para cada
linha.

### Verificação documental

Executar de `docs/airtable/`:

```bash
python3 -m unittest discover -s tests -v
python3 -m json.tool sampling-manifest.template.json > /dev/null
```

Os testes são vetores e um oráculo de alocação sobre dados sintéticos; não são
um pipeline de seleção do piloto e não validam critérios curatoriais pendentes.
Conferir também `git diff --check` e os gates de ownership/drift de `AGENTS.md`.
O template bloqueado usa `actual_size = null`: zero significaria uma execução
concluída sem selecionados. Sem total factível, registrar erro, não emitir seleção
parcial nem converter todos os elegíveis em reservas.

## Elegibilidade de consultas para galerias analíticas

A composição de uma galeria deve ser determinada por critérios verificáveis, e
não por seleção manual posterior. Para cada consulta, aplicar e registrar os
filtros na ordem definida pelo protocolo da análise. Depois de **cada** filtro,
o relatório deve informar o denominador efetivo remanescente, inclusive quando
um filtro não altera a contagem.

Uma consulta só é elegível quando, ao final dos filtros:

- contém `N >= 20` itens válidos;
- registra `eligible_cross_support_candidates >= 10`;
- reúne candidatos de pelo menos três suportes distintos;
- não contém itens duplicados nem mais de uma reprodução do mesmo objeto.

O alvo analítico é **30 itens por consulta**. Resultados com 24–29 itens são
admissíveis, mas ficam abaixo do alvo; resultados com 20–23 itens constituem a
**faixa mínima degradada** e devem ser identificados como tal no relatório.
Resultados abaixo de 20, ou que descumpram qualquer outro critério acima, são
inelegíveis.

Quando uma consulta for inelegível, substituí-la pela próxima consulta ainda
não utilizada da lista de reserva, respeitando estritamente a ordem congelada.
Aplicar à substituta os mesmos filtros, critérios e relatório de denominadores.
Se nenhuma consulta de reserva satisfizer os critérios, declarar a consulta
inelegível; é vedada escolha manual *ad hoc* para completar a galeria.

## Checklist antes de um release público

- [ ] Cada linha possui `ID do corpus` único ou está marcada como duplicata.
- [ ] A contagem do release é declarada no manifesto.
- [ ] O manifesto indica a camada de origem e os critérios de inclusão.
- [ ] O manifesto experimental referencia o crosswalk e declara todas as colunas de identidade (`canonical_item_id`, `registry_id`, `editorial_id`, `hf_row_id`, `bucket_object_key`, `source_record_url`).
- [ ] Cada vínculo informa `link_method` (`existing_crosswalk`, `exact_id`, `canonical_url` ou `manual_review`) e `link_evidence` verificável.
- [ ] `data/processed/id_crosswalk.jsonl` foi incorporado quando disponível e sua proveniência foi preservada.
- [ ] Nenhuma identidade foi confirmada somente por igualdade ou aproximação de título.
- [ ] Colisões de IDs, imagens primárias múltiplas não resolvidas e vínculos apenas por título estão marcados como inelegíveis para a amostra.
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
