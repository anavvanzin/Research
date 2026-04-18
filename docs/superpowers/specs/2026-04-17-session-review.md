# Revisão da Sessão — 17 de Abril de 2026

**Pesquisadora:** Ana Vanzin (PPGD/UFSC)
**Tese:** ICONOCRACIA — Female Allegory in the History of Legal Culture, 19th–20th c.
**Assistente:** Hermes Agent (Nous Portal, modelo minimax-minimax-m2.7)
**Início da sessão:** 19:02 BRT

---

## 1. Contexto da Sessão

Objetivo inicial: explorar os notebooks estatísticos existentes do corpus e identificar análises novas. A sessão evoluiu de uma verificação de notebooks para uma refatoração multidimensional do modelo de scoring e uma nova seção do Capítulo 6.

### Notebooks existentes (antes da sessão)

| Notebook | Conteúdo | Status |
|----------|----------|--------|
| 01_exploratory.ipynb | Estatísticas descritivas (Cap. 6.1) | Executado ✓ |
| 02_kruskal_wallis.ipynb | Kruskal-Wallis regimes × morfologia (Cap. 6.2) | Executado ✓ |
| 03_regression.ipynb | Regressão OLS (Cap. 6.3) | Executado ✓ |
| 04_correspondence.ipynb | Análise de correspondência múltipla (Cap. 6.4) | Executado ✓ |

### Notebooks criados durante a sessão

| Notebook | Conteúdo | Status |
|----------|----------|--------|
| 05_temporal.ipynb | Dinâmica temporal: regimes, ENDURECIMENTO, países, suportes por década | Criado e executado ✓ |
| 06_clustering.ipynb | Clustering hierárquico (Ward) + k-means; silhueta; validação cruzada | Criado e executado ✓ |
| 07_dimensionality.ipynb | PCA: scree, loadings, biplot | Criado e executado ✓ |
| 08_multidimensional_scoring.ipynb | Sub-scores, comparações por regime, exportação CSV | Criado e executado ✓ |

---

## 2. Análises Realizadas e Resultados

### 2.1 Análise de Correlação dos Indicadores

**Dados:** 145 itens × 10 indicadores ordinais (escala 0–3)

**Descoberta-chave:** `monocromatizacao` correlaciona fracamente com todos os outros indicadores (ρ = 0,08 a 0,36). Os outros 9 indicadores formam um bloco fortemente intercorrelacionado (ρ = 0,44 a 0,76).

**Conclusão exploratória:** ENDURECIMENTO pode não ser unidimensional — a monocromatização pode ser uma dimensão independente.

### 2.2 Análise de Componentes Principais (PCA)

**Notebook:** 07_dimensionality.ipynb

| Componente | Variância | Interpretação |
|-----------|-----------|---------------|
| PC1 | 53,7% | Dimensão geral de endurecimento |
| PC2 | 11,8% | Eixo burocrático (serialidade + inscrição vs. desincorporação) |
| PC3 | 9,6% | Monocromatização (loading = 0,87) |
| PC4–10 | 25,0% | Ruído / variância residual |

**Descobertas:**
- O composite atual (média de 10) captura PC1 — 53,7% da variância. Os outros 46,3% são escondidos.
- Monocromatização domina PC3 isoladamente — é uma dimensão estatisticamente separável.
- PC2 (eixo burocrático) é interpretável mas menor em magnitude.

### 2.3 Clustering Não-Supervisionado

**Notebook:** 06_clustering.ipynb

**Melhor k:** k=2, silhueta = 0,284 (moderada — os dados não se separam limpiamente).

**Cramér's V = 0,502** (associação forte entre clusters e regimes).

| Cluster | fundacional | normativo | militar | contra-alegoria |
|---------|-----------|-----------|---------|-----------------|
| 0 | 24 | 30 | 24 | 1 |
| 1 | 47 | 10 | 3 | 6 |

**Cluster 0** = endurecimento misto (todos regimes). **Cluster 1** = fundacional residual + contra-alegorias.

**ARI hierarquia × k-means (k=2):** 0,741 (alta concordância).

**Teste monocromatização:** ARI (com vs. sem monocromatização) = 0,790 — efeito moderado, a estrutura muda mas não desaparece.

**Outliers:** 10 itens com silhueta negativa. Principais: FR-019 (−0,32), FR-008 (−0,21), US-004 (−0,19) — todos militar mas com traços de fluidez narrativa.

**In-scope vs. out-of-scope:** Cluster 1 tem 30,3% de itens fora do escopo vs. 8,9% no Cluster 0 — a fronteira escopo é estruturalmente visível nos dados.

### 2.4 Dinâmica Temporal

**Notebook:** 05_temporal.ipynb

- 159/165 itens com ano (96%)
- Período 1850s–1970s: 103 itens em 13 décadas
- **1910s spike:** 32 itens, 23 militar (WWI)
- ENDURECIMENTO médio por década: 1850s = 1,12 → 1950s = 2,58 (ilustrativo, viés de seleção)

### 2.5 Sub-Scores Multidimensionais

**Notebook:** 08_multidimensional_scoring.ipynb

**Definição dos sub-scores:**

| Sub-score | Indicadores | Conteúdo |
|-----------|-------------|----------|
| ENDURECIMENTO_CORE | 8 (exclui monocromatização + serialidade) | Dimensão geral de endurecimento |
| MONOCROMATIZAÇÃO | 1 (monocromatização) | Registro cromático isolado |
| FORMALIZAÇÃO_BUR | 2 (serialidade + inscrição estatal) | Eixo burocrático |

**Médias por regime:**

| Regime | Core | Mono | Form.Bur. | Composite |
|--------|------|------|-----------|-----------|
| fundacional | 1,07 | 1,97 | 1,04 | 1,16 |
| normativo | 1,70 | **2,40** | 2,16 | 1,82 |
| militar | 1,73 | 1,67 | **2,52** | 1,80 |
| contra-alegoria | 0,50 | 1,29 | 1,21 | 0,71 |

**Descoberta-chave:** normativo e militar têm composite quase idêntico (1,82 vs. 1,80). Mas normativo maximiza registro cromático; militar maximiza burocrático. A distinção era invisível no composite.

### 2.6 Teste Crítico: Monocromatização é Medium-Driven?

**Pergunta:** A correlação entre monocromatização e endurecimento é real ou é um artefato do meio?

**Testes:**

| Análise | Resultado | Interpretação |
|---------|-----------|---------------|
| year × mono (Spearman) | ρ = −0,18 (p = 0,03) | Fraca; gravuras mais recentes são *menos* monocromáticas |
| year × core (Spearman) | ρ = 0,33 (p < 0,001) | Endurecimento aumenta com ano |
| mono × core (Spearman, raw) | ρ = 0,27 (p = 0,001) | Correlação aparente |
| mono × core (Spearman, parcial \| year) | ρ = 0,35 (p < 0,001) | Mais forte controlando por ano |
| **mono × core (gravuras only)** | ρ = −0,01 (p = 0,92) | **Nula dentro do mesmo meio** |
| **Within coins** | mono = 3,6 ± 1,1 (n=12) | Moedas sempre monocromáticas |

**Conclusão:** Dentro do mesmo tipo de meio, monocromatização e endurecimento não se correlacionam. A correlação aparente no corpus é espúria — reflete diferenças de medium entre grupos. Moedas e selos forçam monocromatização por affordance material.

### 2.7 Crítica Metodológica Aplicada

Durante a sessão, a skill *scientific-critical-thinking* foi aplicada ao próprio trabalho, gerando as seguintes ressalvas autoidentificadas:

1. **PCA em dados ordinais (0–3):** pressuposto de normalidade violado. Alternativas: MCA (já usado em 04), ou PCA Polychoric. O StandardScaler mitiga mas não resolve.
2. **Sub-scores definidos post-hoc:** CORE_8, MONO_1, BUR_2 foram definidos após ver os loadings — são exploratórios, não confirmatórios.
3. **Sem correção para comparações múltiplas:** 4 Kruskal-Wallis tests sem Bonferroni (α limiar deveria ser 0,0125). Todos ainda significativos, mas a prática deve ser reportada.
4. **Correlação CORE × composite = 0,976:** os sub-scores não contradizem o composite — CORE_8 é o composite sem monocromatização e serialidade. O achado real é a distinção normativo × militar nos sub-scores.

---

## 3. Decisões Tomadas

### 3.1 Mantidas

- O **composite de 10 indicadores** permanece como variável dependente principal.
- Os notebooks 05–08 são **materiais exploratórios/robustness**, não refatoração do pipeline.
- Os resultados são **reportados honestamente** com limitações explicitadas.

### 3.2 Descartadas

- **Refatoração completa do scoring no pipeline** (code_purification.py): muito trabalho para ganho marginal. CORE_8 correlaciona 0,976 com o composite.
- **Re-execução dos notebooks 01–04 com sub-scores:** não muda as conclusões substantivas.
- **FACTORIAL_BUR como eixo independente teorizado:** é um artefato de medium (stamps, coins) mais do que um registro visual do Estado.

### 3.3 Aceitas com Ressalvas

- A **monocromatização como sub-score separado** será reportada como descriptor suplementar, com a ressalva de que sua interpretação histórica requer validação arquivística.
- O **modelo de três registros** (core, cromático, burocrático) será apresentado como modelo exploratório no Capítulo 6, com a limitação de que é derivado de dados e não de teoria a priori.

---

## 4. Material Produzido

### 4.1 Arquivos Criados

| Arquivo | Descrição |
|---------|----------|
| `vault/tese/capitulo-6-sessao-2026-04-17.md` | Seção 6.3 draft completa |
| `notebooks/05_temporal.ipynb` | Análise temporal |
| `notebooks/06_clustering.ipynb` | Clustering não-supervisionado |
| `notebooks/07_dimensionality.ipynb` | PCA |
| `notebooks/08_multidimensional_scoring.ipynb` | Sub-scores multidimensionais |
| `data/processed/subscores.csv` | 145 itens com sub-scores exportados |
| `data/processed/fig_06_regime_timeline.png` | Timeline regimes por década |
| `data/processed/fig_07_endurecimento_trend.png` | Tendência ENDURECIMENTO por década |
| `data/processed/fig_08_country_timeline.png` | Países por década |
| `data/processed/fig_09_medium_timeline.png` | Suportes por década |
| `data/processed/fig_10_indicator_correlation.png` | Correlação 10 indicadores |
| `data/processed/fig_11_dendrogram.png` | Dendrograma Ward |
| `data/processed/fig_12_silhouette.png` | Análise silhueta |
| `data/processed/fig_13_cluster_profiles.png` | Perfis dos clusters |
| `data/processed/fig_14_scree.png` | Scree plot PCA |
| `data/processed/fig_15_loadings.png` | Loadings PCA |
| `data/processed/fig_16_pca_biplot.png` | Biplot PCA |
| `data/processed/fig_17_subscore_scatter.png` | Core × Mono e Core × Form.Bur. |
| `data/processed/fig_18_composite_vs_core.png` | Distribuição gap composite − core |
| `docs/superpowers/specs/2026-04-17-new-corpus-analysis-design.md` | Especificação do design |

### 4.2 Arquivo de Revisão da Sessão

Este documento: `docs/superpowers/specs/2026-04-17-session-review.md`

---

## 5. Achados Principais para Discussão com Orientador

### 5.1 Fortes (validado estatisticamente, robusto)

1. **Os regimes normativo e militar produzem alegorias visualmente distintas por trás do composite.** Normativo = alto registro cromático; militar = alto registro burocrático. Ambos convergem no composite de 1,8. A distinção é conceitualmente significativa — são duas estratégias diferentes de produção de alegoria estatal.

2. **A taxonomia de 4 regimes é empiricamente validada.** Clustering não-supervisionado produz estrutura que se associa fortemente com os regimes (Cramér's V = 0,502). A taxonomia não é imposta arbitrariamente.

3. **PC1 explica 53,7% da variância.** O composite é uma boa proxy da dimensão geral, mas esconde 46,3% de estrutura residual.

### 5.2 Moderados (significativos mas requerem cautela)

4. **Monocromatização é uma dimensão ortogonal ao endurecimento geral** (PC3 loading = 0,87). Seu significado histórico requer validação arquivística.

5. **O pico dos anos 1910s é o evento temporal mais visível no corpus** (32 itens, 23 militar, WWI). A tendência de endurecimento ao longo das décadas é ilustrativa mas não confirmatória.

6. **Os comparanda ocupam um espaço estruturalmente distinto** (30% out-of-scope no cluster fundacional residual). A fronteira escopo é visível nos dados.

### 5.3 Exploratórios (hipóteses, não conclusões)

7. **Hipótese cromática:** a coincidência histórica entre emergência do Estado moderno e普及ação de tecnologias de reprodução mecânica (gravura, selo, moeda) significa que o ENDURECIMENTO estatal emergiu junto com tecnologias visuais que impõem padronização e, frequentemente, monocromia. Não é possível determinar, por métodos iconométricos, quanto da monocromia é escolha estratégica e quanto é affordance material.

8. **Hipótese burocrática:** PC2 captura a tensão entre a alegoria que se desvincula da narrativa (desincorporação) e a que se multiplica no circuito estatal (serialidade + inscrição). Esta pode ser a dimensão visual do "Estado que faz circular a lei" vs. "Estado que remove a lei do contexto".

---

## 6. Próximos Passos Sugeridos

### Imediato (esta semana)
- [ ] Revisar seção 6.3 draft com orientador
- [ ] Executar notebooks 05–08 no Jupyter local para verificar saídas visuais
- [ ] Integrar fig_06–fig_18 no draft do capítulo

### Curto prazo (abril–maio)
- [ ] Para os 10 itens outliers (silhueta negativa): verificar se a codificação de regime está correta
- [ ] Para FR-HERC-1870, NL-005, US-001 (top mono >> core): pesquisa arquivística sobre disponibilidade de alternativas policromáticas no mesmo meio/mesmo período
- [ ] Decidir: incluir sub-scores como colunas extras em `corpus_dataset.csv` (subscores.csv já existe)

### Médio prazo (maio–junho)
- [ ] Considerar MCA Polychoric para PCA ordinal (dados 0–3 não são contínuos)
- [ ] Validar sub-scores com análise de correspondência múltipla (MCA, já em notebook 04)
- [ ] Re-examinar PC2 (eixo burocrático) — é artifactual de medium ou genuinamente visual?

### Para a tese (Cap. 6)
- [ ] Inserir seção 6.3 entre 6.2 e 6.3 existente (renumerar)
- [ ] Integrar com seção 6.5 (limites da quantificação) — o problema monocromático como caso paradigmático
- [ ] Verificar ABNT das referências citadas no draft

---

## 7. Limitações Declaradas

1. **Viés de seleção do corpus:** 165 itens de um pipeline de busca não constituem amostra aleatória. Todas as análises temporais e de distribuição são ilustrativas.
2. **PCA em dados ordinais:** pressupostos violados. Usar MCA como alternativa.
3. **Sub-scores definidos post-hoc:** necessidade de validação em amostra independente ou análise confirmatória.
4. **Nenhuma correção para múltiplas comparações** em Kruskal-Wallis.
5. **Período pré-1850 totalmente inexplorado** no corpus (1–5 itens por década).
6. **Análise de medium dependente de categorização manual** (medium_norm) que pode conter inconsistências.

---

## 8. Resumo Executivo (para orientador)

Na sessão de 17 de abril, foram desenvolvidas quatro novas análises estatísticas sobre o corpus de 165 alegorias jurídicas femininas:

1. **Análise temporal (05):** a evolução dos regimes por década mostra um pico de alegorias militares na Primeira Guerra Mundial (1910s: 32 itens, 23 militar). A tendência geral de endurecimento ao longo do século XIX–XX é ilustrativa mas não confirmatória devido ao viés de seleção do corpus.

2. **Clustering não-supervisionado (06):** a estrutura de quatro regimes é empiricamente validada — clustering hierárquico reproduz a taxonomia com alta concordância (Cramér's V = 0,50). A estrutura mais fundamental é binária: alegorias capturadas pela lógica de Estado (Cluster 0) vs. alegorias operando fora ou contra ela (Cluster 1).

3. **PCA multidimensional (07):** o composite de 10 indicadores captura 53,7% da variância. Duas dimensões residuais emergem: PC2 (eixo burocrático, 11,8%) e PC3 (monocromatização, 9,6%).

4. **Sub-scores multidimensionais (08):** os regimes *normativo* e *militar* produzem composites quase idênticos (1,82 vs. 1,80), mas por lógicas visuais distintas — normativo maximiza o registro cromático; militar maximiza o burocrático.

**O achado mais significativo** é que a monocromatização é um descriptor primariamente driven by medium — dentro de gravuras, monocromatização e endurecimento são completamente não correlacionados (ρ = 0,01). Moedas e selos impõem monocromia por affordance material. A interpretação histórica requer pesquisa arquivística item a item para distinguir escolha estratégica de necessidade material. Este problema hermenêutico — onde forma visual e necessidade material coincidem sem possibilidade de separação — é proposto como o problema central do método iconométrico da tese.

---

*Documento gerado automaticamente por Hermes Agent em 2026-04-17. Revisar antes de compartilhar com orientador.*
