# Airtable — camada pública do corpus ICONOCRACIA

## Finalidade

A base **“Iconocracia — Corpus e Tese”** é a camada pública de curadoria, revisão e navegação do projeto. Ela permite acompanhar cada imagem, sua proveniência, sua codificação visual e seu uso argumentativo na tese sem substituir o repositório canônico do corpus.

O repositório mantém a documentação, o esquema e os futuros snapshots de exportação. O Airtable continua sendo o ambiente de trabalho vivo; o GitHub registra versões estáveis, decisões metodológicas e dados liberados para consulta pública.

## Regra metodológica central

Não existe um único número que descreva, sozinho, todos os estágios do corpus. O projeto distingue deliberadamente:

1. **Universo de catálogo** — todos os registros descritivos importados ou identificados.
2. **Ledger validado** — registros com identificador estável, proveniência e escopo checados.
3. **Codificação visual** — subconjunto que recebeu avaliação pelos dez indicadores de purificação iconocrática.
4. **Extratos analíticos** — CSVs e notebooks derivados para testes, visualizações e recortes específicos.
5. **Casos argumentativos** — seleção editorial de figuras utilizadas na escrita da tese.

Assim, um CSV analítico com 165 linhas não deve ser tratado como o tamanho integral do corpus. Todo release público deve declarar sua camada, data, critérios de inclusão e contagem efetiva.

## Esquema da base

### 1. Itens do Corpus

Tabela-mãe para identificação e descrição dos objetos visuais.

Campos-chave:

- `ID do corpus` — identificador estável de junção entre todas as tabelas.
- `Título`, `País`, `Ano`, `Período`, `Meio`, `Suporte`.
- `Motivo(s)` — alegorias, figuras e repertórios iconográficos.
- `Regime iconocrático` e `Índice de purificação`.
- `URL da obra`, `URL da imagem`, `Fonte / arquivo`, `Citação ABNT`.
- `Estado de revisão` e `Observações / QA`.

### 2. Codificação Visual

Tabela de auditoria para os dez indicadores de purificação iconocrática:

- desincorporação;
- rigidez postural;
- dessexualização;
- uniformização facial;
- heraldização;
- enquadramento arquitetônico;
- apagamento narrativo;
- monocromatização;
- serialidade;
- inscrição estatal.

Também registra índice composto, regime proposto, codificador, data, validação e notas metodológicas.

### 3. Casos Argumentativos

Tabela editorial para a tese, apresentações e defesa. Cada caso recebe tese interpretativa, capítulo, conceito-chave, evidência visual, prioridade de escrita e referência bibliográfica.

### 4. Fontes e Arquivos

Tabela de proveniência para instituições, catálogos, arquivos, coleções, hemerotecas e obras secundárias. Registra URL, referência ABNT, nível de evidência e observações de proveniência.

## Política de publicação

Os metadados, URLs, reproduções identificadas por fonte, notas de QA, indicadores e textos interpretativos desta camada podem ser públicos. A publicação deve preservar atribuição, URL de origem e referência bibliográfica sempre que disponíveis.

Snapshots públicos devem ser incluídos em `data/public/airtable/` com um arquivo `manifest.json` contendo:

- versão e data de exportação;
- nome da tabela de origem;
- número de registros;
- campos incluídos;
- critérios de inclusão/exclusão;
- referência do commit;
- observações metodológicas relevantes.

## Sincronização recomendada

1. Atualizar e validar registros no Airtable.
2. Exportar cada tabela em CSV ou JSON.
3. Gerar ou atualizar o `manifest.json` com contagens e escopo do snapshot.
4. Revisar divergências no log de QA antes da publicação.
5. Fazer commit com mensagem que indique a camada e a data do release.

## Princípios de QA

- Nunca sobrescrever o valor bruto sem registrar a decisão de normalização.
- Ausência de codificação significa **não codificado**, e não ausência do atributo visual.
- Divergências entre catálogo, ledger e extratos analíticos devem ser registradas, não apagadas.
- `ID do corpus` é a única chave de ligação entre itens, codificação, fontes e casos argumentativos.
- Qualquer mudança em escala, regime ou critério de escopo exige nota de versão.

## Próxima etapa

Após a importação integral do catálogo, o primeiro release público deve incluir o manifesto, a tabela de itens e a tabela de codificação correspondente, sem colapsar o corpus total em um único extrato analítico.
