# 5 ideias de artigos juridicamente críticos

Cada ficha contém os **6 campos obrigatórios**: `Problema`, `Usuário`, `Fluxo argumentativo`, `Risco jurídico`, `Tecnologia analisada`, `Pergunta de debate`. Tom: crítico, anti-solucionista, ancorado em legislação brasileira e em literatura comparada. Cada ficha é um esboço de artigo — não um abstract de capa de revista; serve para preparar submissão a periódico, banca ou disciplina.

---

## A1. Smart contract não é contrato administrativo: o ônus argumentativo da automatização do regime jurídico-administrativo

**Problema.** O discurso de "execução automática" em smart contracts elide as prerrogativas e sujeições que estruturam o regime jurídico do contrato administrativo brasileiro. Súmulas 346 e 473 do STF e art. 53 da Lei 9.784/99 garantem à Administração o poder-dever de anular atos viciados; a Lei 14.133/2021 prevê rescisão e alteração unilaterais, fiscalização contínua e teoria da imprevisão. Tudo isso pressupõe **reversibilidade contextualizada**. A imutabilidade do registro distribuído e a determinismo de uma rotina em Solidity são, nesse contexto, defeitos antes de serem virtudes — exceto quando o uso é restrito a log probatório com governança específica.

**Usuário.** Legisladores que tramitam normas de blockchain pública (ex.: PLs em curso sobre registros e contratações em DLT); órgãos de controle externo (TCU, CGU, MP de Contas); doutrina brasileira de Direito Administrativo crítico (Binenbojm, Marques Neto, Justino de Oliveira); pareceristas de Procuradorias Federais e Estaduais; pesquisadores em Direito Digital.

**Fluxo argumentativo.** (i) Reconstruir dogmaticamente o regime jurídico-administrativo brasileiro com foco em prerrogativas/sujeições e em revisibilidade. (ii) Mapear os usos efetivos de DLT no setor público brasileiro: BNDES PIER, pilotos do TCU, propostas de pregão eletrônico em DLT, registros notariais. (iii) Distinguir três famílias de uso — log probatório, registro de propriedade/título, automação contratual — e mostrar que cada uma exige resposta jurídica distinta. (iv) Formular um teste de admissibilidade: "qual prerrogativa ou sujeição a arquitetura escolhida deixa de absorver?" (v) Diálogo crítico com Pasquale, Hildebrandt e doutrina nacional. (vi) Propostas regulatórias: governança de chaves, multisig com participação de controle, mecanismo de anulação por ordem judicial.

**Risco jurídico.** Anulação de ato viciado em ambiente de imutabilidade técnica; vinculação indevida de Administração futura por *lock-in* de protocolo; transferência de discricionariedade administrativa para *patches* de fornecedor; opacidade da execução (oráculos e dados off-chain).

**Tecnologia analisada.** Hyperledger Fabric e Ethereum (com foco no Solidity como linguagem de execução); oráculos (Chainlink, oráculos centralizados); arquiteturas multisig; *layer-2* e custos de gás como variável administrativa.

**Pergunta de debate.** *"Existe imutabilidade compatível com o art. 37 da CF/88? Em quais condições, sob qual quórum e com qual mecanismo de anulação?"*

---

## A2. Reconhecimento facial municipal: por que o "consentimento" não salva o fundamento legal

**Problema.** Câmeras com reconhecimento facial proliferam em transporte público e policiamento de via no Brasil sem lei específica que satisfaça o art. 4º III da LGPD. O art. 11 trata biometria como dado sensível. Enquanto a "lei específica" para tratamento em segurança pública não é editada, municípios contratam, fornecedores operam, e o cidadão não tem fórum claro de contestação. A literatura empírica brasileira (LAPIN, InternetLab, Coding Rights) documenta impacto desigual em populações negras. O argumento jurídico de "interesse público" abstrato não é base legal suficiente.

**Usuário.** Defensorias Públicas (Estadual, União); Ministério Público com atribuição em direitos humanos e em controle externo; vereadores que tramitam moratórias; advocacia em proteção de dados e direitos humanos; conselhos municipais (de segurança, de direitos humanos); pesquisadores em Direito Urbanístico.

**Fluxo argumentativo.** (i) Mapeamento da legislação municipal e estadual existente sobre uso de RF em via pública. (ii) Análise contratual dos casos paradigmáticos: ViaQuatro/SP, Centro de Operações Rio, projetos de Salvador e Curitiba. (iii) Aplicação do filtro do Estatuto da Cidade (Lei 10.257/2001 art. 2º II e V): a contratação serve à função social ou à otimização para um público específico? (iv) Exame da exigência de Relatório de Impacto à Proteção de Dados Pessoais (LGPD art. 38) e do regime de transparência (LAI). (v) Crítica à racionalidade contratual: o município consegue auditar o sistema que contrata? (vi) Propostas: moratória legislativa, exigência de RIPD público, vedação à coleta para identificação demográfica em transporte público.

**Risco jurídico.** Efeito *chilling* sobre direito de reunião (CF art. 5º XVI); falsos positivos com consequências penais; ausência de DPIA pública; opacidade contratual incompatível com o controle externo (CF arts. 70-75); discriminação algorítmica indireta.

**Tecnologia analisada.** CCTV + face matching baseado em redes convolucionais; serviços de fornecedor (AWS Rekognition, OiTV, fornecedores chineses); datasets de treinamento não auditados; arquitetura *edge* vs. *cloud*; integrações com bases policiais (Sinesp, Infoseg).

**Pergunta de debate.** *"Município pode contratar serviço cujos termos técnicos ele não consegue auditar? Em caso negativo, qual a sanção administrativa apropriada?"*

---

## A3. Big data fiscal e devido processo: motivação algorítmica e o art. 20 da LGPD

**Problema.** Autos de infração tributária e bloqueios em sistemas de transferências sociais frequentemente derivam de *risk scoring* algorítmico (ContÁgil, modelos de aprendizado supervisionado em receitas estaduais e federais). A motivação humana formal mascara a causa real. O art. 50 da Lei 9.784/99 exige motivação clara, congruente e suficiente; o art. 20 da LGPD garante revisão de decisões automatizadas — porém com texto que, após o veto presidencial de 2019, não exige revisor humano. O resultado é uma inversão silenciosa da carga probatória: o contribuinte deve provar inocência diante de modelo opaco.

**Usuário.** Contribuintes pessoa física e jurídica (especialmente pequenas e médias empresas); advocacia tributária; CARF e tribunais de contribuintes estaduais; Defensoria Pública (em casos de transferências sociais); pesquisadores em Direito Tributário e em proteção de dados.

**Fluxo argumentativo.** (i) Reconstrução dogmática do dever de motivação no processo administrativo brasileiro (Lei 9.784/99, doutrina de Maria Sylvia Zanella Di Pietro, Diogo de Figueiredo Moreira Neto). (ii) Análise do art. 20 da LGPD em diálogo com o art. 22 do GDPR — a Decisão *SCHUFA* (TJUE, 2023) como referência comparada. (iii) Exame de casos brasileiros: ContÁgil, Sisbacen, sistemas de fiscalização estaduais, modelos de detecção de fraude em INSS. (iv) Discussão sobre o que constitui "explicação suficiente" — local explanations (SHAP, LIME) bastam? (v) Propostas: dever de motivação algorítmica em parecer próprio do auto de infração; direito à intervenção humana qualificada; auditoria contínua dos modelos por órgão de controle.

**Risco jurídico.** Violação ao devido processo administrativo (CF art. 5º LIV/LV); presunção operativa de fraude; viés territorial e setorial; descumprimento do princípio da igualdade material; anulabilidade do auto pela motivação insuficiente.

**Tecnologia analisada.** Aprendizado de máquina supervisionado (gradient boosting, redes profundas); *feature stores* governamentais; pipelines de cruzamento de bases (eSocial, RAIS, CADIN, SIAFI); ferramentas de interpretabilidade (SHAP, LIME, saliency maps); arquiteturas em nuvem federada.

**Pergunta de debate.** *"O direito à explicação algorítmica do art. 20 da LGPD vincula a Receita Federal? Se sim, qual o conteúdo mínimo dessa explicação para satisfazer o art. 50 da Lei 9.784/99?"*

---

## A4. Eficiência como cavalo de Troia: a captura privada do regulamento por API

**Problema.** Desde a EC 19/1998, o princípio da eficiência (CF art. 37 caput) é mobilizado para justificar terceirização decisória. Na Adm 4.0, terceiriza-se a estrutura decisória inteira: a infraestrutura `gov.br`, `ConectaGov`, autenticação federada, integrações via API e armazenamento em cloud privada (AWS, Microsoft, Google) operam sob *Termos de Uso* e *SLA* que jamais passariam pelo Congresso, mas vinculam de fato o cidadão. Sob o *Cloud Act* (EUA, 2018), provedores americanos podem ser compelidos a entregar dados a autoridades dos EUA — em colisão com a LGPD. Quem é o controlador do `gov.br`?

**Usuário.** Doutrina constitucional e administrativa; CGU e TCU em sede de auditoria de governança digital; ANPD; pesquisadores em soberania digital; Procuradorias Federais; Comissões parlamentares de proteção de dados.

**Fluxo argumentativo.** (i) Reconstruir a história do princípio da eficiência no Brasil: do PDRAE de Bresser-Pereira à Lei 14.129/2021. (ii) Mapear as camadas técnicas do `gov.br`: identidade, autenticação, integrações, armazenamento, processamento, disponibilidade. (iii) Identificar onde o poder normativo de fato reside — *Terms of Service*, *SLA*, *patch notes*, *deprecation cycles*. (iv) Crítica em diálogo com Morozov (anti-solucionismo), Zuboff (capitalismo de vigilância), Marques Neto (captura regulatória), Hübner Mendes (tecnocracia). (v) Análise jurídica do conflito Cloud Act × LGPD à luz da soberania jurisdicional. (vi) Propostas: vedação a *vendor lock-in*, exigência de portabilidade técnica, governança aberta de APIs, cláusulas contratuais de salvaguarda jurisdicional.

**Risco jurídico.** Discricionariedade administrativa sequestrada por ToS; jurisdição estrangeira sobre dados públicos brasileiros; descontinuidade do serviço por decisão privada; violação ao princípio da publicidade e da continuidade.

**Tecnologia analisada.** Cloud federada (AWS, Microsoft Azure, Google Cloud); OpenID Connect e OAuth 2.0; APIs governamentais (gov.br, BR-CIDADÃO, ConectaGov); padrões de identidade digital (e-CPF, Pix); arquitetura SaaS aplicada ao setor público.

**Pergunta de debate.** *"Quem é o controlador de dados do gov.br à luz do conflito Cloud Act × LGPD? Há solução contratual ou apenas legislativa?"*

---

## A5. Inclusão digital reversa: o silenciamento do cidadão analógico e o art. 17 da Lei 14.129/2021

**Problema.** A Lei 14.129/2021 estabelece a "preferência" pelo digital e descreve o atendimento presencial como subsidiário (art. 17). Na prática administrativa, "preferência" tem sido lida como "exclusividade": INSS exige prova de vida por aplicativo; Bolsa Família e Auxílio operam via `gov.br`; CadÚnico exige selfie em locais com sinal. Idosos, indígenas, ribeirinhos, população em situação de rua, pessoas com deficiência visual ou cognitiva e qualquer pessoa sem *smartphone* atualizado são silenciadas. A digitalização compulsória produz uma **nova categoria de incapacidade civil de fato** — pessoas juridicamente capazes, mas administrativamente invisíveis.

**Usuário.** Defensorias Públicas; Ministério Público; Conselhos de Direitos (idoso, indígena, pessoa com deficiência); CRAS e CREAS; Congresso Nacional (subcomissões de inclusão); Tribunais de Justiça; pesquisadores em Direitos Humanos e Direito Constitucional.

**Fluxo argumentativo.** (i) Mapear as barreiras concretas: idade, conexão, biometria, alfabetização digital, custo do dispositivo, acessibilidade. (ii) Análise sistemática da Lei 14.129/2021 — em particular dos arts. 3º (princípios), 17 (atendimento) e 18 (acessibilidade). (iii) Diálogo com a doutrina do mínimo existencial (Ricardo Lobo Torres, Ana Paula de Barcellos) e com o direito de petição (CF art. 5º XXXIV "a"). (iv) Casuística: ADIs e Ações Civis Públicas em curso; recomendações de Defensoria; relatórios da ENAP e do IBGE. (v) Construção do **direito subjetivo ao atendimento humano**: fundamentação dogmática em mínimo existencial, princípio da continuidade e dignidade. (vi) Propostas: balcão garantido, prazo razoável de atendimento presencial, vedação a exigência exclusivamente digital para benefício essencial.

**Risco jurídico.** Violação ao mínimo existencial; descumprimento da continuidade do serviço público; lesão a direito de petição; discriminação indireta por idade, território e classe; anulabilidade de atos que extinguem benefício por barreira técnica.

**Tecnologia analisada.** Aplicativo `gov.br` (autenticação, prova de vida, biometria); selfie como autenticação biométrica; integrações federadas; arquitetura *mobile-first*; portais com requisitos de acessibilidade WCAG não cumpridos; modelos de detecção de *liveness*.

**Pergunta de debate.** *"Existe direito subjetivo ao atendimento humano? Em qual fundamento — mínimo existencial, continuidade, dignidade — essa construção é mais robusta?"*

---

## Como escolher uma ficha para virar artigo

| Critério | A1 | A2 | A3 | A4 | A5 |
|---|---|---|---|---|---|
| Disponibilidade de jurisprudência | média | crescente | alta | baixa | crescente |
| Disponibilidade de dado empírico | baixa | alta | média | média | alta |
| Apetite editorial em revistas BR (2026) | alto | alto | médio | médio | alto |
| Diálogo com a tese ICONOCRACIA | direto | direto | médio | direto | médio |
| Esforço estimado de campo | baixo | alto | médio | médio | alto |
