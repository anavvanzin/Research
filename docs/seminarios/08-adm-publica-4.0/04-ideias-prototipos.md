# 5 ideias de protótipos acadêmicos demonstráveis em sala

Cada ficha contém os **6 campos obrigatórios**: `Problema`, `Usuário em sala`, `Fluxo de demo`, `Risco jurídico ilustrado`, `Tecnologia`, `Pergunta de debate`. Critérios comuns: rodável em laptop sem cloud paga; sem dado pessoal real; tempo de setup ≤ 30 min; tempo de demo ≤ 15 min; cada protótipo nomeia o que a tecnologia **não resolve**.

> Atenção ética. Em P4 (reconhecimento facial), todo uso de imagem de pessoa real exige consentimento expresso, escrito, e descarte imediato após a aula. **Não fazer demo de RF com rosto de aluno se houver qualquer dúvida sobre consentimento.** Alternativa segura: galeria multifenótipo de imagens stock CC.

---

## P1. Anula-Bloco — irreversibilidade vs. autotutela administrativa

**Problema.** Mostrar visceralmente que "imutabilidade" do registro distribuído colide com a autotutela administrativa (Súmulas 346 e 473 STF; art. 53 da Lei 9.784/99) e com a rescisão unilateral do art. 137 e ss. da Lei 14.133/2021. O argumento se sustenta sozinho na doutrina; mas em sala, ver na tela um pagamento sendo executado e *não conseguir desfazê-lo* tem peso pedagógico que cinquenta páginas não têm.

**Usuário em sala.** Aluno-A representa "Administração" (assinatura administrativa). Aluno-B representa "Particular". Professor representa autoridade controladora (TCU/Judiciário) que descobre vício superveniente.

**Fluxo de demo (≈ 12 min).**
1. Abrir VS Code com contrato Solidity simples já escrito (`Pagamento.sol`): condicional sobre prazo, valor fixo, beneficiário fixo.
2. Subir Hardhat node local (`npx hardhat node`).
3. Deploy: `npx hardhat run scripts/deploy.js --network localhost`.
4. Aluno-A invoca `aprovarPagamento()` — front-end HTML mínimo dispara transação.
5. Pagamento executa. Mostrar saldo.
6. Professor anuncia: "ato viciado por incompetência relativa, descoberto agora". Pedir à classe: o que fazer?
7. Tentar reverter pelo contrato — não há função `anular()`. Demonstrar.
8. Discussão: o que precisaria existir? Multisig com juiz? Função `pause()` com governance? Oráculo de tutela judicial? Mostrar versão alternativa do contrato com `pause()` e quórum 3 de 5.

**Risco jurídico ilustrado.** Autotutela administrativa; rescisão unilateral; equilíbrio econômico-financeiro; controle externo; reversibilidade do ato administrativo viciado.

**Tecnologia.** Solidity 0.8.x; Hardhat (Node.js 20+); Ethers.js v6; HTML/JS mínimo; rede local (chainId 31337); MetaMask opcional para visual.

**O que a tecnologia *não* resolve.** Não resolve interpretação do vício; não resolve teoria da imprevisão; não resolve o juízo de proporcionalidade que fundamenta a anulação; não resolve responsabilização pessoal do agente.

**Pergunta de debate.** *"É possível desenhar smart contract que respeite autotutela administrativa sem virar contrato comum com etapa cripto inútil?"*

---

## P2. Painel-Sombra LAI — assimetria entre transparência ativa e passiva

**Problema.** Portais oficiais investem em transparência ativa (o que a Administração escolhe mostrar) e pouco em passiva (o que o cidadão pergunta). Demonstrar a assimetria com dado público real, sem precisar de qualquer credencial.

**Usuário em sala.** Toda a turma como observadora. Um aluno voluntário protocola um pedido real via e-SIC (CGU) durante a aula — opcional.

**Fluxo de demo (≈ 10 min).**
1. Abrir Streamlit local (`streamlit run app.py`).
2. Página inicial: tabela com volume de pedidos LAI por órgão federal (CSV público da CGU pré-baixado).
3. Filtros: órgão, ano, status (atendido / parcialmente atendido / negado / não respondido).
4. Mostrar **taxa de negativa por órgão** em mapa de calor; alunos identificam *outliers*.
5. Mostrar **prazo médio de resposta** vs. prazo legal (LAI art. 11: 20 dias prorrogáveis por mais 10).
6. Mostrar **reincidência da mesma pergunta** — sinal de transparência ativa deficiente: se 200 pessoas fazem a mesma pergunta passiva, deveria ser ativa.
7. Opcional: aluno protocola pedido durante a aula. Volta no slide para checar status na próxima semana.

**Risco jurídico ilustrado.** Abuso da exceção do art. 23 da LAI (sigilo); recusa por "trabalho adicional desproporcional"; silêncio administrativo; descumprimento do prazo do art. 11; violação ao princípio da publicidade.

**Tecnologia.** Python 3.12 (env `iconocracy`); Streamlit ≥ 1.30; Pandas; Plotly; CSV de dados abertos da CGU (ckan.cgu.gov.br); opcional: requests + parser para o e-SIC.

**O que a tecnologia *não* resolve.** Não responde os pedidos; não obriga transparência ativa; não evita o uso abusivo das exceções; não substitui o trabalho político de pressão por LAI funcional.

**Pergunta de debate.** *"Transparência ativa pode substituir a passiva? Por que não?"*

---

## P3. Caixa-Preta-Tributária — explicação algorítmica que esconde viés (DEMO RECOMENDADA)

**Problema.** SHAP e LIME são vendidos como solução para "explicabilidade" em compliance algorítmico. Mostrar em sala que uma explicação local pode dar verniz técnico a um modelo discriminatório, sem cumprir o dever de motivação do art. 50 da Lei 9.784/99. Útil tanto para Direito Tributário quanto para Direito Administrativo geral.

**Usuário em sala.** Toda a turma. Pode-se chamar um aluno para "rodar o classificador" — efeito participativo aumenta o impacto.

**Fluxo de demo (≈ 12 min).**
1. Abrir Jupyter Lab (`jupyter lab`); notebook `caixa_preta.ipynb` pré-carregado.
2. Mostrar dataset sintético: 5.000 empresas fictícias com `cnae`, `faturamento`, `idade_empresa`, `regiao`, `funcionarios`. Variável-alvo: `risco_fraude` (binária). **Importante: dataset construído com viés territorial deliberado** (ex.: 40 % das empresas marcadas como alto risco em uma região, 5 % nas outras).
3. Treinar XGBoost (`xgb.XGBClassifier`); rodar predição em batch.
4. Mostrar matriz de confusão: acurácia ~ 0.92. Reação: "ótimo modelo".
5. Rodar SHAP: `shap.TreeExplainer + shap.summary_plot`.
6. Feature importance: **`regiao` em primeiro lugar**, com larga vantagem.
7. Discussão: o que isso significa juridicamente? Modelo está discriminando por território — proxy para classe, raça, renda. Apresentar art. 50 da Lei 9.784/99 e art. 20 da LGPD em quadro lateral.
8. Provocação final: "este parecer SHAP, anexado a um auto de infração, cumpre o dever de motivação?"

**Risco jurídico ilustrado.** Motivação insuficiente do ato administrativo (art. 50 Lei 9.784/99); discriminação algorítmica indireta; viés territorial como proxy de raça/classe; presunção operativa de fraude; descumprimento do art. 20 da LGPD na sua leitura substantiva.

**Tecnologia.** Python 3.12; scikit-learn 1.4+; xgboost 2.x; shap 0.45+; jupyter; pandas; matplotlib. Sem GPU. Setup com `pip install` em ≤ 5 min.

**O que a tecnologia *não* resolve.** SHAP não interpreta a decisão para o contribuinte — apenas mostra atribuições aproximadas em torno da predição. Não cumpre, por si só, dever de motivação. Não dispensa contraditório humano qualificado. Não auditoria substantiva do modelo.

**Pergunta de debate.** *"Uma explicação local (SHAP) cumpre o dever de motivação do art. 50 da Lei 9.784/99?"*

---

## P4. Cidade-Vigia — reconhecimento facial com taxa de erro visível por fenótipo

**Problema.** O discurso de "tecnologia neutra" colapsa em sala quando o erro é **estratificado**. A literatura (Buolamwini & Gebru; Tarcizio Silva) já demonstrou. Em sala, demonstrar localmente, com galeria stock, dá impacto pedagógico imediato.

**Usuário em sala.** Galeria stock multifenótipo (recomendado). Alternativa: alunos voluntários **somente com termo de consentimento expresso por escrito e descarte imediato após a aula** — incluindo log do modelo. Em qualquer caso, evitar minorias étnicas locais identificáveis na galeria.

**Fluxo de demo (≈ 10 min).**
1. Subir Flask local (`python app.py`).
2. Carregar galeria de 30 imagens stock CC com diversidade fenotípica/idade/gênero.
3. Cada imagem é embedada (face_recognition lib, baseado em dlib).
4. UI: webcam mostra imagem ao vivo (não persistida); compara com galeria; retorna match + score.
5. Configurar limiar baixo deliberadamente (0.55) para forçar falsos positivos.
6. Mostrar contador de falsos positivos por fenótipo da galeria.
7. Discussão: aceitar 1 falso positivo a cada 100 abordagens é "aceitável"? Quem decide e com que base legal? Mencionar LGPD art. 11; art. 4º III; ausência de regulamentação; ausência de RIPD pública.
8. Encerrar derrubando o app e apagando *embeddings*. Demonstrar o `rm -rf` ao vivo (efeito didático sobre dever de descarte).

**Risco jurídico ilustrado.** LGPD art. 5º II (dado sensível biométrico); art. 11 (regime especial); art. 4º III (vácuo legislativo); art. 38 (ausência de RIPD); CF art. 5º XVI (efeito *chilling*); CF arts. 70-75 (controle externo limitado por opacidade contratual).

**Tecnologia.** Python 3.12; face_recognition (dlib HOG/CNN); Flask; OpenCV; galeria de 30 imagens stock CC (Pexels, Unsplash com licença adequada). Não usar serviço cloud.

**O que a tecnologia *não* resolve.** Não corrige viés de treinamento — apenas o expõe. Não substitui audiência pública, RIPD, lei específica. Não justifica o uso em via pública.

**Pergunta de debate.** *"Um falso positivo a cada 100 abordagens é 'aceitável'? Quem decide e com que base legal?"*

---

## P5. Carômetro Cidadão — simulação do atrito do gov.br para quem não tem smartphone

**Problema.** O discurso de "facilidade" do gov.br só funciona para quem tem dispositivo recente, conexão estável e alfabetização digital. Inverter a experiência: em sala, alunos representam um cidadão em desvantagem técnica e cronometram cada etapa.

**Usuário em sala.** Aluno voluntário "cidadão sem smartphone moderno"; turma observa e cronometra; professor narra o que cada barreira representa juridicamente.

**Fluxo de demo (≈ 12 min).**
1. **Materiais físicos.** 8 cartões em A6 representando etapas reais do cadastro/benefício gov.br: CPF, e-mail, foto do documento, prova de vida por selfie, recuperação de senha, autenticação de dois fatores, comprovante de residência, validação por SMS.
2. Aluno recebe cartões fora de ordem; precisa montar a sequência.
3. **Interface web degradada.** HTML/CSS local simulando navegador antigo; usar DevTools throttling para emular 2G; *form* com timeouts curtos e autocomplete desativado.
4. Aluno tenta avançar; cronômetro começa.
5. Em uma das telas, simular falha por *liveness* — selfie rejeitada por iluminação. Aluno recomeça.
6. Em outra, simular OCR falhando em CPF com hífen.
7. Cronometrar. A maioria dos alunos desiste em 5–7 min. Comentar: e se o benefício fosse o Bolsa Família?
8. Discussão: art. 17 da Lei 14.129/2021 ("preferência" presencial subsidiária); CF art. 5º XXXIV (direito de petição); princípio da continuidade; mínimo existencial.

**Risco jurídico ilustrado.** Lei 14.129/2021 art. 17 lido como "exclusividade" (interpretação a evitar); CF art. 5º XXXIV; descumprimento da continuidade; lesão ao mínimo existencial; discriminação indireta por idade, território, classe, deficiência.

**Tecnologia.** HTML/CSS/JS estáticos; Chrome DevTools Network throttling; cartões físicos impressos; cronômetro web simples. Setup em ≤ 15 min. Não envolve dado pessoal real.

**O que a tecnologia *não* resolve.** Não substitui balcão presencial garantido. Não substitui conexão pública. Não substitui Defensoria. Mostrar o atrito é o ponto — não corrigi-lo no protótipo.

**Pergunta de debate.** *"A digitalização compulsória cria uma nova categoria de incapacidade civil de fato?"*

---

## Matriz de escolha do protótipo para a aula

| Critério | P1 | P2 | P3 ★ | P4 | P5 |
|---|---|---|---|---|---|
| Tempo de setup | 30 min | 15 min | 5 min | 30 min | 15 min |
| Tempo de demo | 12 min | 10 min | 12 min | 10 min | 12 min |
| Densidade jurídica | alta | média | alta | alta | alta |
| Impacto visual | médio | baixo | alto | alto | alto |
| Risco ético em sala | baixo | nenhum | nenhum | **alto** | nenhum |
| Recomendação | boa | boa | **DEMO** | usar com cautela | excelente para encerrar |

★ Recomendação principal de demo na fala dos 30 min — o protótipo P3 entrega a tese metodológica do seminário em 12 min e dialoga diretamente com o art. 50 da Lei 9.784/99 e o art. 20 da LGPD.

## Notas de execução

- Cada subdiretório `prototipos/0X-nome/` no repositório receberá: `README.md` (instalação + demo), `requirements.txt` ou `package.json`, código mínimo executável, **e disclaimer ético** quando aplicável.
- Nenhum protótipo é executado nesta etapa do seminário. Especificações servem como ponto de partida para iteração separada.
- Para dúvidas de propriedade intelectual nas imagens stock (P4): registrar fonte e licença em `prototipos/04-cidade-vigia/CREDITS.md`.
