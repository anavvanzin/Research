# Outline de slides — Seminário 8

20 slides, 16:9, fundo escuro com texto claro (sugestão: `#0E0E12` / `#F2F2F2`, accent `#C4421E`). Tempo médio por slide ≈ 1 min 30 s. Ferramenta-alvo: Google Slides ou PPTX. Conversão automática:

```bash
pandoc 02-slides-outline.md -t pptx -o seminario08.pptx \
  --reference-doc=Tools/pandoc/templates/abnt-slides.pptx  # se existir
```

---

## Slide 1 — Título

**Texto principal**
- Administração Pública 4.0 — uma crítica jurídica
- Big data, blockchain, smart contracts, smart cities no Brasil
- Seminário 8 · Pós-Graduação em Direito · 2026

**Speaker note.** Apresentar-se em uma frase. Anunciar que o seminário é deliberadamente crítico e anti-solucionista, e que vai terminar com uma demo ao vivo. Não pedir desculpas pelo viés crítico — anunciá-lo como método.

---

## Slide 2 — Provocação iconoclasta

**Texto principal**
- "A imagem da Administração 4.0 é uma imagem de poder."
- Mas — **poder de quem?**

**Visual sugerido.** Colagem (1) de um *dashboard* azul-claro genérico, (2) ícone de cadeado em blockchain, (3) cidade vista de cima com pontos de luz conectados. Sobreposto: a frase em branco.

**Speaker note.** Forçar a turma a visualizar o estereótipo antes de desconstruí-lo. Falar a frase em pé. Pausar. Trocar o slide só depois do silêncio. Conectar à tese ICONOCRACIA: imagens de poder não são neutras.

---

## Slide 3 — Roteiro de 30 minutos

**Texto principal**
1. O que é (e o que não é) Adm 4.0
2. Big data público
3. Blockchain e smart contracts
4. Smart cities brasileiras
5. Riscos transversais
6. Três perguntas para o debate
7. Demo ao vivo

**Speaker note.** Dizer "vou cumprir o tempo" com confiança. Avisar que a fala é cadenciada e que aceito perguntas só no debate, exceto para esclarecimento técnico imediato.

---

## Slide 4 — Marco normativo da Adm 4.0 no Brasil

**Texto principal**
- **CF/88 art. 37 caput** — eficiência (EC 19/1998)
- **Decreto 10.332/2020** — Estratégia de Governo Digital
- **Lei 14.129/2021** — Lei do Governo Digital
- **Lei 14.133/2021** — Nova Lei de Licitações
- **LGPD** (Lei 13.709/2018) · **LAI** (Lei 12.527/2011) · **Marco Civil** (Lei 12.965/2014)
- **PL 2338/2023** — marco regulatório de IA (em tramitação)

**Speaker note.** Não memorizar a lista — apontar que cada uma dessas leis foi pensada num momento histórico distinto, e que a Adm 4.0 é a justaposição precária entre elas. Mencionar que o PL 2338 pode mudar a paisagem rapidamente.

---

## Slide 5 — Digitalização vs. algoritmização

**Texto principal**
| Digitalização | Algoritmização |
|---|---|
| Bits substituem papel | Modelo substitui decisão |
| Instrumental | Substantiva |
| Regime jurídico do ato preserva-se | Regime jurídico desloca-se |
| Motivação humana | "Motivação" via SHAP/LIME |
| Art. 50 da Lei 9.784/99 cumprido | Art. 50 sob tensão |

**Speaker note.** Esta é a tese metodológica do seminário. Toda vez que a turma ouvir "Adm 4.0", deve perguntar: digitalização ou algoritmização? O ônus argumentativo é diferente. Falar devagar.

---

## Slide 6 — Big data público: as bases que se cruzam

**Texto principal**
- CADIN · SIAFI · eSocial · RAIS · Sisbacen · CadÚnico
- Sisreg · CNIS · CAGED · Cadastro de Beneficiários do INSS
- **Cruzamento técnico: trivial.**
- **Cruzamento jurídico: nem um pouco trivial.**

**Visual sugerido.** Diagrama de Venn de 4 conjuntos sobrepostos.

**Speaker note.** Lembrar a turma que cada uma dessas bases foi criada para finalidades específicas, sob bases legais distintas. Cruzá-las pode violar o princípio da finalidade da LGPD (art. 6º I) e o devido processo. Não é só "compliance" — é Direito Administrativo.

---

## Slide 7 — Caso: ContÁgil e o auto de infração algorítmico

**Texto principal**
- Receita Federal — sistema **ContÁgil** + ML supervisionado para *risk scoring*.
- Auto de infração com motivação **humana formal**, causa **algorítmica real**.
- LGPD art. 20 — direito a revisão (sem garantia de revisor humano após veto).
- Art. 50 Lei 9.784/99 — motivação **clara, congruente, suficiente**.
- Resultado: **inversão silenciosa da carga probatória.**

**Speaker note.** Ler o último bullet em voz pausada. É a frase que fica. Notar que esse caso é a porta de entrada para o artigo A3 e o protótipo P3.

---

## Slide 8 — Blockchain: as duas promessas

**Texto principal**
- **Imutabilidade** — registro inalterável.
- **Execução automática** — *smart contract.*
- No Direito Administrativo brasileiro, ambas têm **ônus argumentativo**:
  - Súmulas 346 e 473 STF — autotutela.
  - Lei 9.784/99 art. 53 — anulação.
  - Lei 14.133/2021 — rescisão unilateral, equilíbrio econômico-financeiro.

**Speaker note.** A imutabilidade é juridicamente um defeito até prova em contrário. A automatização é mais grave porque reduz contrato a `if/else`. Falar de Pasquale e Binenbojm.

---

## Slide 9 — Smart contract não é contrato administrativo

**Texto principal**
- Contrato administrativo = **regime**, não cláusulas.
- Prerrogativas: alteração e rescisão unilaterais, fiscalização, retomada.
- Sujeições: equilíbrio econômico-financeiro, motivação, controle externo.
- Tudo isso é **argumentativo, contextual, revisável**.
- Nada disso cabe em Solidity.

**Speaker note.** Apontar que isso não significa "blockchain é inútil para o setor público". Significa que ela só é útil quando o uso é restrito a log probatório, e mesmo aí precisa de governança. Caso BNDES PIER como exemplo de uso defensável.

---

## Slide 10 — Smart cities: definir antes de aplaudir

**Texto principal**
- IBM Smarter Cities (2008) → Sidewalk Labs → Songdo → Brasil.
- Casos BR: **Porto Maravilha** (RJ), **Conecta Recife**, **Centro de Operações Rio**.
- Tecnologias: IoT urbano, RF, sensores de mobilidade, *open data*, *dashboards*.
- Ponto de partida jurídico **não é** Lei 14.129.
- Ponto de partida é **Lei 10.257/2001 — Estatuto da Cidade.**

**Speaker note.** Insistir no Estatuto da Cidade. A maioria das aulas sobre smart city pula direto para LGPD. Isso é um erro de localização normativa: smart city é, antes de tudo, política urbana.

---

## Slide 11 — Estatuto da Cidade como filtro crítico

**Texto principal**
- Art. 2º, II — **gestão democrática** da cidade.
- Art. 2º, V — **oferta de serviços urbanos compatíveis com os interesses e necessidades da população**.
- Pergunta-teste para qualquer projeto smart city:
  - **A coleta serve à função social, ou à otimização para quem já tem acesso?**

**Speaker note.** Esse é o filtro que eu uso para qualquer audiência pública municipal. Se a resposta é "otimização para quem tem acesso", é projeto de exclusão sob nome técnico.

---

## Slide 12 — Reconhecimento facial: três casos

**Texto principal**
- **2019 — Carnaval do Rio.** Mulher abordada por confusão fenotípica.
- **2020 — ViaQuatro/SP.** Câmeras com identificação demográfica sem consentimento.
- **2024 — audiências por moratória municipal.**
- Em alguns estados: **>90% das prisões por RF foram de pessoas negras.**

**Visual.** Foto sobreposta com retângulo de detecção — usar imagem stock CC, não imagem real de qualquer pessoa identificável.

**Speaker note.** Ler o último número devagar. Citar LAPIN, InternetLab, Coding Rights. O ponto é que viés não é acidente — é estrutura.

---

## Slide 13 — RF e LGPD: a zona cinzenta

**Texto principal**
- LGPD art. 5º II — biometria = **dado pessoal sensível**.
- LGPD art. 11 — regime especial.
- LGPD art. 4º III — **exclusão para segurança pública**, com remissão a lei específica que **não foi editada.**
- Resultado prático: município contrata, polícia opera, base legal abstrata, cidadão desprotegido.

**Speaker note.** Esse vácuo legislativo é o coração do problema. Mencionar PL 2338 e propostas de lei estadual.

---

## Slide 14 — Tecnocracia e captura por API

**Texto principal**
- Eficiência (EC 19/98) usada como justificativa para terceirização decisória.
- *Termos de Uso, SLA, API* viram **fonte normativa de fato**.
- gov.br · ConectaGov · cloud federada (AWS/Microsoft/Google).
- **Cloud Act (EUA, 2018) × LGPD** — quem é o controlador?

**Speaker note.** Frase-chave: "política pública informal é o nome contemporâneo da tecnocracia". Conectar a Marques Neto e a Hübner Mendes.

---

## Slide 15 — Exclusão digital reversa

**Texto principal**
- Lei 14.129/2021 art. 17 — atendimento presencial **subsidiário**.
- INSS prova de vida por app · CadÚnico com selfie · Bolsa Família via gov.br.
- Idosos · indígenas · ribeirinhos · pop. de rua · pessoas sem smartphone.
- **Nova categoria de incapacidade civil de fato.**

**Speaker note.** Enfatizar que "preferência" no art. 17 não é "exclusividade". Há margem dogmática para construir direito subjetivo ao atendimento humano. Mencionar mínimo existencial, art. 5º XXXIV.

---

## Slide 16 — Transparência ativa vs. passiva: a assimetria

**Texto principal**
- **Ativa** (LAI art. 8º) — Administração escolhe o que mostrar.
- **Passiva** (LAI art. 10) — cidadão pergunta, Administração responde.
- Investimento em portais ≠ investimento em respostas.
- Abuso do art. 23 (sigilo) e da figura "trabalho adicional desproporcional".
- **Silêncio administrativo virou estratégia.**

**Speaker note.** Conectar ao protótipo P2 (Painel-Sombra LAI). Citar relatórios anuais da CGU sobre prazo médio de resposta.

---

## Slide 17 — Três perguntas para o debate

**Texto principal**
1. Existe imutabilidade compatível com o art. 37 CF/88?
2. O art. 20 LGPD vincula a Receita Federal?
3. Existe direito subjetivo ao atendimento humano? Sob que fundamento?

**Speaker note.** Ler em ritmo lento. Não responder. Avisar que o protótipo a seguir aprofunda a pergunta 2.

---

## Slide 18 — Demo: Caixa-Preta-Tributária

**Texto principal**
- Notebook Jupyter · dataset sintético · XGBoost · SHAP.
- O que vamos ver:
  - modelo classifica empresas por "risco de fraude";
  - SHAP "explica" a decisão;
  - **a feature dominante é REGIÃO.**

**Speaker note.** Antes de rodar: avisar que o dataset é sintético e que o ponto não é o modelo, é o que ele revela sobre o argumento da explicabilidade. Rodar. Esperar reação. Comentar.

---

## Slide 19 — A explicabilidade não é motivação

**Texto principal**
- Art. 50 Lei 9.784/99: motivação **clara, congruente, suficiente**.
- SHAP entrega **clara**.
- SHAP **não entrega congruente nem suficiente.**
- Verniz técnico ≠ devido processo administrativo.

**Speaker note.** Esse é o slide que fecha o argumento da apresentação inteira. Repetir a frase: "verniz técnico não é devido processo". Pausar.

---

## Slide 20 — Encerramento

**Texto principal**
- Pacote completo (roteiro, fichas de artigo, fichas de protótipo, bibliografia ABNT) em `docs/seminarios/08-adm-publica-4.0/`.
- 5 ideias de artigo · 5 ideias de protótipo · referências em `05-bibliografia.md`.
- **Pergunta de partida para o debate:** de qual das três deslocações vocês ouviram falar mais — motivação, autotutela ou atendimento? E por quê?

**Visual.** QR-code para o repositório (gerar antes; placeholder por ora).

**Speaker note.** Agradecer. Convidar para escolher uma ficha e voltar com pergunta. Cuidar do tempo: parar a fala em até 30 minutos cravados, mesmo que falte conteúdo. O debate vale mais.

---

## Notas técnicas para conversão

- Para Google Slides: copiar slide a slide, manter contraste mínimo 7:1.
- Para PPTX via pandoc: usar `--slide-level=2` se preferir agrupar.
- Imagens: usar apenas com licença CC ou domínio público; cite a fonte no rodapé do slide.
- Não usar imagens de rostos identificáveis em RF (slide 12) — substituir por silhueta ou retângulo de detecção sobre stock.
