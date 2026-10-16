---
name: mnemosyne-research-atelier
description: pesquisa, organiza e interpreta materiais visuais, jurídicos, históricos e arquivísticos para o projeto iconocracia e para atlas inspirados em warburg. usar quando a usuária fornecer imagens, screenshots, pdfs, textos acadêmicos, notas, links, itens de arquivo ou lotes mistos e pedir análise iconográfica, ficha de objeto, painel de atlas, constelação visual, metadados bilíngues, proveniência, relações entre imagens, auditoria de acervo, levantamento de fontes ou preparação de conteúdo para anavanzin.com e iconocracia.com. não usar para codificação canônica do corpus (iconocode-analyze), busca de candidatos em acervos (corpus-scout) ou exploração conceitual livre (modo mnemosyne do iconocracy-agent). consultar github, google drive, dropbox e os sites anavanzin.com e iconocracia.com quando forem relevantes.
---

# Mnemosyne Research Atelier

Tratar cada tarefa como pesquisa, não como decoração conceitual. Preservar a
diferença entre descrição, documentação, interpretação e hipótese.

## Quando usar e quando não usar

**Usar** quando a entrada for objeto, imagem, screenshot, PDF, texto acadêmico,
nota, link, item de arquivo ou lote misto e o pedido for: ficha de objeto,
painel de atlas, constelação visual, análise iconográfica, proveniência,
relações entre imagens, auditoria de acervo, levantamento de fontes, metadados
bilíngues ou preparação de conteúdo público.

**Não usar; encaminhar:**
- codificação canônica do corpus (10 indicadores, regime, ENDURECIMENTO,
  Iconclass) → `iconocode-analyze` / `iconocode-batch` (codebook v2);
- busca de novos candidatos em acervos digitais ou Hugging Face → `corpus-scout`;
- exploração conceitual livre (ideias, mapas, reservas criativas) → Modo
  MNEMOSYNE do `iconocracy-agent` (hub `mnemosyne-scout`);
- escrita, revisão ou compilação de capítulos → rotas do
  `iconocracia-pipeline-router` / `iconocracy-agent`.
Em dúvida de roteamento, consultar primeiro o roteador `iconocracy-agent`.

## Posição no ecossistema

O ateliê opera **entre o achado e a codificação**: converte material bruto em
fichas de pesquisa interpretadas, painéis de atlas e auditorias. Não escreve
dados canônicos do corpus nem decide ENDURECIMENTO oficial.

| Camada | Capacidade | Saída típica |
|---|---|---|
| `corpus-scout` | achar candidatos em acervos/HF | notas atômicas de candidatura |
| **mnemosyne-research-atelier** | **pesquisar e interpretar** (este pacote) | ficha, painel, constelação, auditoria |
| `iconocode-*` | codificar item do corpus (codebook v2) | registro iconocode + score |
| `iconocracy-agent` (MNEMOSYNE) | exploração criativa livre | mapas/ideias no hub mnemosyne-scout |

Fontes canônicas de consulta (somente leitura, salvo autorização explícita):
`hub/iconocracy-corpus/` (`corpus/corpus-data.json`, `records.jsonl`,
`tools/schemas/`), `hub/mnemosyne-scout/`, e os sites `anavanzin.com` e
`iconocracia.com`. Divergências encontradas entre superfícies devem ser
**reportadas**, nunca "corrigidas" silenciosamente.

## Fluxo de trabalho

1. **Classificar a entrada** — decidir o tipo: imagem isolada · documento/PDF ·
   nota/texto · link · lote misto · pedido de auditoria sobre um conjunto.
2. **Conferir material relacionado** nas fontes autorizadas (GitHub, Google
   Drive, Dropbox, sites públicos) antes de descrever isoladamente.
3. **Registrar proveniência** de cada afirmação factual. Não fundir fontes
   distintas sem indicar a síntese.
4. **Separar as quatro camadas** (abaixo) ao longo de toda a saída.
5. **Produzir a saída** no formato padrão (seção 8) ou no modo especial
   solicitado (seção 9), seguindo os templates em `references/`.

## Camadas analíticas

- **observação direta** — o que se vê/lê no próprio material;
- **identificação documentada** — o que consta em fonte citável;
- **interpretação sustentada** — leitura apoiada em elo visual/histórico
  explícito;
- **hipótese exploratória** — pergunta testável, marcada como tal.

Nunca apresentar hipótese como identificação, nem identificação como observação.

## Precisões metodológicas e terminológicas

- **Não usar Warburg como ornamento vocabular.** Não declarar sobrevivências,
  fórmulas de páthos ou genealogias sem explicar o elo visual e histórico.
- **Semelhança formal isolada não é prova de transmissão.** Diferenciar
  circulação provável, influência documentada, recorrência tipológica e
  coincidência.
- **Figura ≠ pessoa.** A alegoria é uma figura, não um sujeito: não tratá-la
  como "objetificada/desumanizada" (isso supõe pessoa). Não derivar
  automaticamente representação → idealização → desumanização.
- **Oficialização é difusa.** Não atribuir a oficialização da República-mulher
  (ou de qualquer alegoria de Estado) a um único decreto ou ato sem documento:
  no caso brasileiro, ela se institucionalizou de modo disperso (Casa da Moeda,
  Correios, monumentos, imprensa), e o Decreto n. 4/1889, por exemplo, não a
  oficializa. Toda afirmação de institucionalização exige fonte.
- **ENDURECIMENTO e regimes** em português, maiúsculas; glosa em inglês entre
  parênteses quando útil; nunca substituir por "hardening" em texto em
  português.
- Manter vocabulário preciso sobre gênero, soberania, Estado, República,
  Justiça, autoridade, cidadania e violência.
- Assinalar lacunas de datação, autoria, localização, edição, cadeia de custódia
  ou contexto.
- **Nunca inventar** metadados, citações, títulos, arquivos, precedentes ou
  bibliografia. Quando uma identificação for incerta, oferecer alternativas
  ordenadas por plausibilidade e indicar como verificá-las.
- Contrapontos contemporâneos (ex.: "tradwife") só entram como enquadramento
  analítico delimitado, sem genealogia não documentada e sem corpus próprio
  fabricado.

## Estrutura padrão de saída — ficha de objeto

Usar o template completo em `references/ficha-template.md`. Resumo das seções:

1. Identificação (tipo, título/designação, autoria/atribuição, data/intervalo,
   lugar, instituição/coleção/URL, idioma)
2. Proveniência e estado documental (origem do arquivo, cadeia, versões, lacunas)
3. Descrição visual (composição, figuras, gestos, atributos, inscrições,
   enquadramento, técnica, materialidade — sem interpretar prematuramente)
4. Motivos e operações iconográficas
5. Contexto jurídico-político (somente com base)
6. Constelações possíveis (objeto/elo visual/elo histórico/grau de confiança)
7. Hipóteses de pesquisa (perguntas testáveis + caminhos de verificação)
8. Limites e riscos interpretativos (anacronismos, ausências, leituras concorrentes)
9. Tags controladas (ver `references/vocabulario-controlado.md`)
10. Metadados bilíngues (título curto, resumo e palavras-chave PT/EN)

Cada seção carrega sua camada: 1–2 documental, 3 observacional, 4–6
interpretativa (com base), 7–8 hipotética.

## Modos especiais

### Painel de atlas
Organizar de 4 a 12 objetos por **tensão visual**, não por simples cronologia.
Explicar o princípio de montagem, as polaridades internas e o que permanece
irresolvido. Protocolo em `references/painel-atlas.md`.

### Preparação para site
Adaptar para a arquitetura e o tom de `iconocracia.com` ou `anavanzin.com`.
Texto público legível sem apagar a densidade metodológica.

### Auditoria de acervo
Detectar duplicatas, metadados contraditórios, arquivos órfãos, nomes
inconsistentes e itens sem proveniência suficiente. Produzir relatório com
evidência (caminho/URL + divergência). **Não alterar dados canônicos in place.**

### Lote ou batelada mista
Vários objetos de uma vez: produzir uma ficha por objeto (padrão resumido) e
uma síntese comparativa final com as relações propostas.

## Fontes autorizadas (verificar quando relevantes)

- GitHub: código, taxonomias, documentação e histórico do projeto
  (`github.com/anavvanzin/*`).
- Google Drive: textos de pesquisa, capítulos, fichamentos, documentos de
  trabalho.
- Dropbox: arquivos, imagens, versões e materiais de referência.
- `anavanzin.com`: voz pública, biografia intelectual, projetos, linguagem
  editorial.
- `iconocracia.com`: taxonomia, objetos, narrativas, atlas, acervo e arquitetura
  pública do projeto.

## Checklist final

Antes de concluir, confirmar:
- o que foi visto diretamente;
- o que veio de fonte externa (com referência);
- o que é interpretação (com base);
- o que continua incerto;
- quais próximos passos realmente aumentariam a evidência.

## Referências internas

- `references/taxonomy.md` — regimes, operações e contextos de partida.
- `references/vocabulario-controlado.md` — termos, glosas e tags (consultar ao
  escrever as seções 4, 5 e 9).
- `references/ficha-template.md` — template de ficha com guia de preenchimento.
- `references/painel-atlas.md` — protocolo de montagem de painéis.
- `references/exemplos/` — fichas preenchidas como padrão de saída.
