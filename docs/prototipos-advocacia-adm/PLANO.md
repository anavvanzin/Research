# Protótipos para escritórios de advocacia em Direito Administrativo

> Plano de produto · 8 protótipos + 1 *moonshot* · foco em escritórios brasileiros que atuam em **políticas públicas, licitações, contratos administrativos, regulatório, improbidade, concessões, PPPs e contencioso especializado** (TCU, CARF, TIT, TCEs).

## Contexto

A advocacia em Direito Administrativo brasileira convive com cinco dores estruturais:

1. **Volume e velocidade.** Editais publicados diariamente (Comprasnet, BEC/SP, BLL, ComprasNet/Estados); súmulas de TCU mudando jurisprudência; mudanças regulatórias setoriais (Anatel, Aneel, ANS, ANTT, ANP, ANAC, ANTAQ, Anvisa).
2. **Captura de oportunidade.** Cláusulas restritivas em edital costumam só serem flagradas quando alguém com tempo as lê linha a linha. A maioria passa.
3. **Cálculo financeiro caro.** Reequilíbrio econômico-financeiro, modelagem de PPP, *stress test* de concessão — feitos em Excel artesanal por consultor sênior, em horas faturadas.
4. **Memória institucional fragmentada.** Cada parecer escrito, cada tese defendida, cada quesito pericial vive em PDF disperso. O escritório não capitaliza o que já produziu.
5. **Defasagem entre prática e tecnologia.** As ferramentas hoje disponíveis (Sajadv, jurimetria genérica, IA generalista) **não são desenhadas para Direito Administrativo brasileiro**. Genéricas demais para o contencioso especializado, opacas demais para o regulatório, juridicamente cegas para o contratual.

Este plano propõe **8 protótipos diferenciados** que respondem a essas dores — mais 1 *moonshot* experimental. Critérios de seleção:

- **(C1) Automatiza tarefa que advogado sênior faz à mão hoje** (não tarefa que ninguém faria nunca);
- **(C2) Usa fonte de dado pública ou contratualmente acessível** (não depende de raspagem ilegal de cliente);
- **(C3) Tem diferencial claro vs. SaaS jurídico de prateleira** (Sajadv, JusBrasil, CASA, Aurum);
- **(C4) Entrega alavanca de honorários** (acelera entrega ou viabiliza serviço novo);
- **(C5) Compatível com LGPD, segredo profissional (art. 7º, II, EOAB) e Provimento 205/2021 da OAB** sobre IA na advocacia;
- **(C6) Demonstrável em 10–15 min para sócio que decide compra**.

---

## Os 8 protótipos

Cada ficha contém: **Problema · Usuário · Fluxo · Risco jurídico tratado · Tecnologia · Diferencial inovador · Modelo de adoção · Esforço para MVP · Pergunta de validação**.

---

### 1. Edital-Radar — *o caça-direcionamento*

**Tagline.** Lê todo edital publicado por um órgão e detecta cláusula restritiva, exigência desproporcional, "carbonização" (cláusula que só passa porque já passou em edital anterior do mesmo órgão).

**Problema.** Triagem manual de edital é o gargalo do contencioso de licitações. A janela para impugnar é curta (Lei 14.133/2021 art. 164: até 3 dias úteis antes da abertura). Cláusulas direcionadoras costumam ser sutis: exigência de atestado em quantidade incompatível, marca específica disfarçada de "similar", certificações redundantes.

**Usuário.** Sócio de licitações; advogado pleno em contencioso administrativo; cliente fornecedor que paga monitoramento.

**Fluxo.** (i) Ingestão diária de editais por órgão monitorado (Comprasnet, BEC, BLL, portais estaduais). (ii) NLP em duas camadas: classificador de cláusulas (objeto, habilitação, técnica, preço) + detector de padrões restritivos (lista de heurísticas + LLM dirigido). (iii) Comparação semântica com base histórica do mesmo órgão — flag se cláusula apareceu em mais de N editais consecutivos sob mesmo objeto (sinal de "carbonização"). (iv) Dashboard com *risk score* + minuta de impugnação pré-redigida com fundamentação na Lei 14.133 e jurisprudência TCU correlata.

**Risco jurídico tratado.** Direcionamento (Lei 14.133 art. 9º), restrição injustificada à competitividade (art. 22 §1º), violação ao princípio da isonomia (CF art. 37 caput).

**Tecnologia.** Python + Playwright/Scrapy para ingestão; PostgreSQL + pgvector para histórico; modelo de embeddings (e5, BGE-pt) para similaridade; LLM com *constrained decoding* para minuta; Streamlit/Next.js para UI.

**Diferencial inovador.** A maioria dos monitores de edital é alarmista — manda 200 alertas/dia e o advogado ignora. Edital-Radar **só dispara quando há sinal de direcionamento histórico**. É um detector de padrão, não um *RSS feed*.

**Modelo de adoção.** Licença para escritório (uso interno) + serviço white-label para clientes fornecedores (assinatura por órgão monitorado).

**Esforço para MVP.** 6 semanas, 1 dev sênior + 1 advogado-curador para construir base de heurísticas.

**Pergunta de validação.** *Quantos casos de direcionamento o escritório encontrou nos últimos 12 meses, e em quantos a impugnação foi protocolada dentro do prazo?*

---

### 2. Reequilíbrio-Live — *a calculadora que escreve memorial*

**Tagline.** Recebe o BDI original do contrato, os fatos novos (insumo, câmbio, tributário, regulatório) e devolve **três cenários de reequilíbrio** com memorial argumentativo pronto.

**Problema.** Pleitos de reequilíbrio econômico-financeiro (Lei 14.133 art. 124 e ss.; CF art. 37 XXI) são intensivos em planilha + tese + jurisprudência. Hoje, cada pleito é construído do zero por consultor + advogado, em sequência, em semanas. Resultado é defasado quando entregue.

**Usuário.** Escritórios que assessoram concessionárias, contratadas em obras públicas, fornecedores de bens e serviços continuados.

**Fluxo.** (i) *Upload* da planilha de BDI original + contrato. (ii) Identificação automática dos componentes elásticos (insumos, mão-de-obra, câmbio, tributos, encargos sociais). (iii) *Plug-in* de séries históricas (IBGE, BCB, Sicro, Sinapi). (iv) Cálculo de três alternativas — **revisão**, **repactuação** e **reajuste** — com fundamentação distinta (teoria da imprevisão, fato do príncipe, álea econômica extraordinária). (v) Geração de memorial argumentativo com citação correta a Súmula 480 TCU e Acórdãos pertinentes. (vi) *Side-by-side* das três alternativas para o sócio decidir tese.

**Risco jurídico tratado.** Manutenção do equilíbrio econômico-financeiro (CF art. 37 XXI; Lei 14.133 art. 124); distinção entre álea ordinária e extraordinária; vedação à recomposição retroativa quando o instrumento é reajuste.

**Tecnologia.** Python + Pandas para cálculo; BCB API + IBGE SIDRA + Sicro/Sinapi (ETL); modelo de geração de memorial com *retrieval* sobre base vetorizada de jurisprudência TCU (assinatura cadastrada do escritório); Streamlit ou React para UI.

**Diferencial inovador.** Não é uma calculadora — é uma **decisão estruturada** entre três teses jurídicas, com memorial pronto para revisão humana. O *output* é um documento, não um número.

**Modelo de adoção.** Uso interno; eventualmente SaaS para departamentos jurídicos de empresas concessionárias.

**Esforço para MVP.** 8 semanas; precisa de um economista parceiro para validar o cálculo e um sócio sênior para validar a fundamentação.

**Pergunta de validação.** *Qual o tempo médio do escritório, hoje, entre o pedido do cliente e a entrega da minuta de reequilíbrio? Reduzir esse ciclo para 3 dias úteis vale quanto?*

---

### 3. Improbidade-Filtro — *o classificador pós-Lei 14.230*

**Tagline.** Mapeia o caso à luz do **dolo específico** exigido pela Lei 14.230/2021 e identifica enquadramentos defensáveis, vulneráveis e indefensáveis.

**Problema.** A reforma de improbidade (Lei 14.230/2021) reescreveu o art. 1º §1º da Lei 8.429/92 para exigir dolo específico de "fim ilícito" e modulou retroatividade. Muito caso ajuizado pré-reforma é alvo de defesa pós-reforma — e a triagem manual da peça inicial à luz dos novos requisitos é trabalhosa.

**Usuário.** Sócios de defesa em improbidade, agentes públicos investigados, advogados em ações de ressarcimento.

**Fluxo.** (i) *Upload* da peça inicial e principais provas. (ii) Extração de fatos imputados, condutas, agentes, beneficiários, valores. (iii) Classificação contra o tipo objetivo da Lei 8.429/92 atualizada. (iv) Verificação do **elemento subjetivo** (dolo específico) — busca de evidência de finalidade ilícita nos termos do art. 1º §2º. (v) Aplicação da **modulação temporal** (Tema 1199 STF, set. 2022). (vi) Saída: matriz com cada imputação categorizada como **defensável** (carece de dolo específico ou de modulação favorável), **vulnerável** (depende de prova específica) ou **indefensável** (dolo configurado).

**Risco jurídico tratado.** Tipicidade pós-reforma; dolo específico; modulação retroativa (Tema 1199); proporcionalidade da sanção.

**Tecnologia.** Python + LangChain/LlamaIndex para *retrieval*; modelo de extração de entidades jurídicas (NER fine-tuned em peças cíveis brasileiras, ou GPT-4-class com função estruturada); base vetorizada de Tema 1199 + acórdãos STF/STJ pós-2022; Streamlit.

**Diferencial inovador.** Nenhuma ferramenta no mercado faz **matriz de defensibilidade por imputação** — o esforço é sempre artesanal. Aqui, a saída é uma tabela acionável que vira sumário do memorial.

**Modelo de adoção.** Uso interno do escritório; rigorosamente *on-premise* ou cloud privada (sigilo do cliente).

**Esforço para MVP.** 6 semanas + curadoria contínua de jurisprudência STF.

**Pergunta de validação.** *Quanto tempo se perde reescrevendo defesa de improbidade pré-Lei 14.230 para enquadrar requisitos pós-reforma?*

---

### 4. Caderno-de-Quesitos — *o consultor pericial implícito*

**Tagline.** Gera **quesitos periciais** de qualidade técnica a partir do objeto do contrato e do ponto controvertido. Pré-redige quesitos suplementares em audiência de instrução.

**Problema.** Em contencioso de licitações e contratos administrativos, a perícia é decisiva. Quesitos mal formulados perdem causa. Sócio sênior gasta horas escrevendo cada quesito; júnior demora dias e ainda assim entrega genérico.

**Usuário.** Sócio de contencioso administrativo; advogado em audiência de instrução; cliente que precisa entender os quesitos do outro lado.

**Fluxo.** (i) *Upload* do objeto contratual (TR, edital, projeto básico) e da peça que delimita o ponto controvertido. (ii) Identificação do tipo de perícia (engenharia, contábil, ambiental, sistêmica). (iii) Geração de **três blocos** de quesitos: (a) técnicos descritivos, (b) impugnatórios sobre a metodologia do laudo do outro lado, (c) suplementares para audiência. (iv) Cada quesito vem com **justificativa jurídica curta** apontando o que ele tenta provar e qual a tese.

**Risco jurídico tratado.** Ampla defesa (CF art. 5º LV); pertinência e utilidade da prova; preclusão de quesito não formulado.

**Tecnologia.** LLM com *prompt scaffolding* específico por tipo de perícia; base curada de quesitos de boas práticas (sócio sênior aprova lote inicial); UI conversacional.

**Diferencial inovador.** Quesitos não são "geração de texto livre" — são instrumento processual. O protótipo trata cada quesito como uma **micro-hipótese probatória**, não como pergunta solta.

**Modelo de adoção.** Uso interno; eventualmente módulo dentro do produto Reequilíbrio-Live (#2) quando há perícia contábil.

**Esforço para MVP.** 4 semanas; mais 2 semanas de validação por sócio sênior em casos reais (com sigilo).

**Pergunta de validação.** *Em quantas audiências dos últimos 12 meses o escritório saiu sem ter formulado um quesito suplementar que poderia ter feito diferença?*

---

### 5. PPP-Stress-Test — *o simulador Monte Carlo de concessão*

**Tagline.** Roda 10.000 cenários sobre uma PPP/concessão variando demanda, câmbio, inflação, inadimplência. Identifica gatilhos contratuais e estima probabilidade de litígio por cláusula.

**Problema.** Concessões e PPPs envolvem cláusulas complexas: revisão ordinária, extraordinária, fato do príncipe, *force majeure*, equilíbrio. Quando o cliente é poder concedente ou concessionário, simular cenários pré-litígio é diferencial competitivo. Hoje isso é feito caso a caso por consultoria financeira terceirizada.

**Usuário.** Escritórios full-service em infraestrutura; áreas de M&A com componente regulatório; departamentos jurídicos de concessionárias e poder concedente.

**Fluxo.** (i) Modelagem do contrato em DSL própria — cláusulas gatilho com condições matemáticas (ex.: "se variação cambial > 30 % em 12 meses, então revisão extraordinária"). (ii) Definição das variáveis exógenas e suas distribuições (histórica + cenário do cliente). (iii) Simulação Monte Carlo com 10.000 trajetórias. (iv) Saída: probabilidade de cada gatilho disparar; probabilidade de litígio (calibrada com base em precedentes setoriais); valor esperado de cada cenário.

**Risco jurídico tratado.** Cláusulas de revisão (Lei 8.987/95; Lei 11.079/04); teoria da imprevisão; matriz de riscos (art. 22 da Lei 11.079/04 c/c arts. 102-104 Lei 14.133/21); fato do príncipe.

**Tecnologia.** Python (NumPy/Pandas/SciPy) para simulação; pgmpy para inferência probabilística; D3.js ou Plotly para visualização; armazenamento on-premise.

**Diferencial inovador.** Liga **modelagem financeira** + **estrutura jurídica do contrato** + **dados de litígio** numa simulação única. Não existe ferramenta brasileira que faça isso integrado para PPP/concessão.

**Modelo de adoção.** Serviço *premium* — não SaaS. Licença para escritório com componente de consultoria.

**Esforço para MVP.** 12 semanas; precisa de quant + advogado de infra + sócio.

**Pergunta de validação.** *Quantos litígios em PPPs do escritório nos últimos 5 anos teriam sido antecipados com simulação pré-litígio?*

---

### 6. Multa-Doppler — *o detector de perseguição administrativa*

**Tagline.** Para um cliente fornecedor recorrente, detecta **padrão de multas em série** aplicadas pelo mesmo órgão e identifica se há sinal de perseguição administrativa ou erro sistemático de fiscalização.

**Problema.** Multas administrativas (regulatórias, contratuais, tributárias) frequentemente vêm em série. Cada uma é tratada isoladamente pelo júnior do escritório. O *padrão* — que é a tese de defesa mais forte — nunca é construído.

**Usuário.** Sócios de regulatório (Anatel, Aneel, ANS); contencioso administrativo; cliente fornecedor com volume.

**Fluxo.** (i) Cliente alimenta carteira de multas recebidas (CSV com órgão, data, valor, fundamento, fato gerador). (ii) Análise temporal — séries por órgão, fiscal, tipo. (iii) Detecção de padrão: aglomeração temporal, sazonalidade, fiscal repetido, fundamento idêntico. (iv) Saída: relatório com **tese de defesa transversal** (não específica de uma multa, mas do conjunto), invocando *desvio de finalidade*, *isonomia*, *proporcionalidade*. (v) Fundamentação com Súmulas TCU e jurisprudência STJ pertinente.

**Risco jurídico tratado.** Desvio de finalidade administrativa (Lei 4.717/65 art. 2º "e"); isonomia; razoabilidade; controle judicial do ato sancionatório.

**Tecnologia.** Python + Pandas para análise temporal; algoritmos de detecção de anomalia (DBSCAN, isolation forest); LLM para gerar a tese transversal a partir do padrão detectado.

**Diferencial inovador.** **Inversão do olhar** — não defende multa por multa, defende contra o padrão. É um produto que só faz sentido quando o escritório tem **carteira recorrente**, e por isso fideliza cliente.

**Modelo de adoção.** Módulo de *retainer* mensal (assinatura para grandes clientes); ou venda como projeto único de auditoria.

**Esforço para MVP.** 4 semanas; precisa de carteira histórica de pelo menos um cliente piloto.

**Pergunta de validação.** *O escritório tem cliente que recebeu mais de 20 multas do mesmo órgão nos últimos 3 anos? Já se tentou tese conjunta?*

---

### 7. Política-Pública-Mapper — *o mapa visual para litígio estratégico*

**Tagline.** Em ACPs, ADIs, recomendações ministeriais e amici curiae, gera **mapa visual** de uma política pública: atores, fluxo orçamentário, cadeia normativa, decisões judiciais relevantes, gargalos.

**Problema.** Litígio estratégico em política pública (judicialização da saúde, educação, assistência social, política penitenciária, ambiental) exige domínio de fluxo administrativo + financeiro + normativo. Hoje, montar esse contexto consome 60 % do esforço; a tese ocupa 40 %. O ideal é inverter.

**Usuário.** Defensorias Públicas; MPs; escritórios em direito da saúde, educação e ambiental; ONGs; clínicas universitárias.

**Fluxo.** (i) Tema (ex.: "medicamento órfão para doença rara X"). (ii) Coleta automática: portarias do Ministério da Saúde, Resoluções da Anvisa, atos da Conitec, decisões do STF (RE 657.718, ADI 5.501), execução orçamentária no SIOP/SIAFI. (iii) Construção de **grafo**: nó-ator, nó-norma, nó-decisão, aresta de dependência. (iv) Visualização interativa com filtros temporais. (v) Geração de **sumário narrativo** servível como introdução de petição inicial em ACP.

**Risco jurídico tratado.** Mínimo existencial; reserva do possível; controle judicial de política pública (STF RE 684.612); separação de poderes.

**Tecnologia.** Python + Neo4j ou networkx para grafo; APIs de dados abertos (gov.br, Senado, STF); D3.js para visualização; LLM para sumário narrativo.

**Diferencial inovador.** É o oposto do *legal research* genérico: parte do **mapa institucional** da política, não da busca por jurisprudência. Útil para construir tese antes de redigir peça.

**Modelo de adoção.** Pode virar **bem público** (open source, em parceria com defensoria/MP/clínica universitária) — alavanca reputacional + cumpre função social.

**Esforço para MVP.** 8 semanas; primeiro mapa montado para 1 política piloto (ex.: medicamento de alto custo).

**Pergunta de validação.** *Em quantas peças de litígio estratégico o escritório investiu mais de 40 horas só montando contexto factual?*

---

### 8. Regulador-Tropos — *a análise retórica de mudança jurisprudencial*

**Tagline.** Analisa pareceres normativos e decisões de agência reguladora ao longo do tempo para detectar **mudança de orientação interpretativa** — antes que ela vire surpresa para o cliente.

**Problema.** Agências reguladoras (Anatel, Aneel, ANS, ANTT, ANP, Anvisa) mudam orientação por mudança de retórica antes de mudar por mudança formal. Quem monitora atos formais perde a curva de tendência. Quem lê todo parecer normativo gasta tempo desproporcional.

**Usuário.** Sócios de regulatório setorial; departamentos jurídicos de concessionárias e operadoras; associações setoriais.

**Fluxo.** (i) Ingestão contínua de pareceres normativos, votos relatores e decisões de plenário da agência. (ii) Análise de *frequência de termos*, *tropos retóricos* e *citação cruzada*. (iii) Detecção de novos *tropos* (ex.: agência começa a citar "interesse difuso" onde antes usava "interesse coletivo"; mudança em "razoabilidade econômica" para "razoabilidade regulatória"). (iv) Alerta de mudança incipiente, com diff visual. (v) Memorando curto explicando o que essa mudança pode antecipar regulatoriamente.

**Risco jurídico tratado.** Segurança jurídica regulatória; vedação à mudança abrupta de orientação (Lei 13.655/2018 — alterações da LINDB, art. 23); proteção da confiança legítima.

**Tecnologia.** NLP — *topic modeling* (BERTopic), *keyword shift detection*, *embedding drift*; *time series* sobre vetores de embeddings; LLM para narrar a mudança detectada.

**Diferencial inovador.** Aplica **linguística computacional** a **fontes regulatórias setoriais** brasileiras. Nenhum produto faz isso hoje em português.

**Modelo de adoção.** SaaS por agência monitorada (assinatura mensal por setor regulatório).

**Esforço para MVP.** 10 semanas; piloto em 1 agência (sugiro Anvisa ou Aneel pelo volume e estabilidade do corpus).

**Pergunta de validação.** *Quantas vezes em 2024-2025 o escritório foi pego de surpresa por uma mudança de orientação regulatória que, retroativamente, era detectável em pareceres anteriores?*

---

## Moonshot — Contrato-Living

**Tagline.** Versão "viva" do contrato administrativo: cada cláusula anotada com jurisprudência atualizada, dependências normativas e alertas quando a base legal muda. Como GitHub para contrato.

**Problema.** Gestão contratual em órgãos públicos e em fornecedores recorrentes é fragmentada: o contrato vive como PDF estático, e o "estado do mundo" ao redor dele muda. Quando o sócio precisa opinar em pleito, ele lê o PDF e refaz a pesquisa. Toda vez.

**Fluxo conceitual.** (i) *Parser* do contrato em árvore de cláusulas. (ii) Cada cláusula vinculada por *anchor* a artigos de lei, súmulas e acórdãos. (iii) Watch contínuo nas fontes: muda artigo? Cláusula é marcada como "exposta". (iv) Painel para o gestor com cláusulas "verdes" (estáveis), "amarelas" (em movimento) e "vermelhas" (impactadas). (v) Cada movimento gera nota explicativa para o sócio decidir intervenção.

**Risco/diferencial.** Inverte a relação contrato↔jurisprudência. Hoje a jurisprudência é caçada quando há litígio; aqui ela vigia o contrato preventivamente. **É um produto novo, não uma melhoria de produto existente.**

**Por que é moonshot.** Exige *parsing* robusto de contrato, ontologia jurídica brasileira, integração contínua com fontes oficiais. Esforço: 6+ meses, 2-3 devs, advogado especialista. Mas pode virar diferencial estratégico do escritório por uma década.

---

## Roadmap proposto (4 trimestres)

| Trimestre | Foco | Protótipos | Por quê primeiro |
|---|---|---|---|
| Q1 | Honorários rápidos | #4 Caderno-de-Quesitos · #6 Multa-Doppler | MVP barato, retorno rápido em fidelização |
| Q2 | Diferencial visível | #1 Edital-Radar · #3 Improbidade-Filtro | Demonstráveis para sócio em 15 min; alavanca de marketing |
| Q3 | Vertical premium | #2 Reequilíbrio-Live · #5 PPP-Stress-Test | Maior margem por hora; diferencial competitivo em infra |
| Q4 | Posicionamento institucional | #7 Política-Pública-Mapper · #8 Regulador-Tropos | Reputacional; oportunidade de open-source parcial |
| Cont. | Moonshot | Contrato-Living | Investimento estratégico paralelo |

## Considerações de governança

**Sigilo profissional (EOAB art. 7º II).** Todo protótipo que processa dado de cliente deve rodar **on-premise** ou em **cloud privada brasileira**. Vedado uso de API de LLM cloud sem isolamento contratual claro. Para Improbidade-Filtro, Reequilíbrio-Live, PPP-Stress-Test e Multa-Doppler: on-premise obrigatório.

**LGPD (Lei 13.709/2018).** Quando o cliente é pessoa natural ou há dado pessoal de servidor (improbidade, contencioso disciplinar), tratamento sob hipótese do art. 7º VI (exercício regular de direitos em processo) e art. 11 II "d". RIPD para Multa-Doppler e Improbidade-Filtro.

**Provimento 205/2021 da OAB.** IA é ferramenta auxiliar; o ato privativo da advocacia (parecer, peça) tem assinatura humana. Os protótipos geram **rascunho**, nunca peça final. Cada um deles deve ter *banner* nesse sentido na UI.

**Conflito de interesses.** Edital-Radar não pode ser usado simultaneamente para impugnar e para preparar proposta no mesmo edital — **muralha técnica** entre módulos.

**Modelo de monetização.** Três tracks compatíveis:
- **Interno** (sem cliente): protótipos #2, #3, #4, #5, #6 — ganho em produtividade do próprio escritório.
- **SaaS para cliente** (B2B): #1 Edital-Radar, #6 Multa-Doppler, #8 Regulador-Tropos.
- **Bem público / open-source**: #7 Política-Pública-Mapper — ganho reputacional, parceria com Defensoria/MP/clínica universitária.

## Critério de descontinuação

Cada protótipo tem critério explícito de descontinuação após 6 meses de uso:

- Caso #4 e #6: se a taxa de adoção do sócio sênior < 30 %, descontinuar.
- Caso #1, #2, #3, #5: se ROI calculado em horas economizadas / horas de manutenção < 3x, descontinuar.
- Caso #7: se nenhuma instituição parceira adotar em 6 meses, descontinuar.
- Caso #8 e Moonshot: avaliação semestral por comitê de inovação do escritório.

## Próximo passo recomendado

1. Apresentar este plano ao comitê de inovação / gestão do escritório.
2. Selecionar **2 protótipos** para piloto Q1 — recomendação: **#4 Caderno-de-Quesitos** (esforço baixo, retorno rápido) + **#1 Edital-Radar** (alto impacto visível e diferencial competitivo).
3. Definir advogado-curador interno para cada protótipo (validação jurídica é o gargalo, não o desenvolvimento).
4. Construir baseline mensurável: horas atuais por tarefa, taxa de êxito, satisfação de cliente. Sem baseline, não há como provar ganho.
