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

## Checklist antes de um release público

- [ ] Cada linha possui `ID do corpus` único ou está marcada como duplicata.
- [ ] A contagem do release é declarada no manifesto.
- [ ] O manifesto indica a camada de origem e os critérios de inclusão.
- [ ] Campos vazios foram mantidos como vazios, sem conversão automática para zero.
- [ ] Valores fora da escala foram revisados ou marcados como pendentes.
- [ ] URLs de origem e citações foram preservadas.
- [ ] Notas de QA relevantes foram incluídas ou vinculadas.
- [ ] O commit contém data, versão e descrição de alterações.

## Convenção de versões

Use o padrão `AAAA-MM-DD-camada-vN` nos nomes de release e diretórios. Exemplo:

```text
2026-06-23-catalogo-v1
2026-06-23-codificacao-v1
2026-06-23-casos-argumentativos-v1
```

A primeira linha de cada manifesto deve explicar se o snapshot contém o universo bruto, o ledger validado, a codificação disponível ou um extrato analítico.
