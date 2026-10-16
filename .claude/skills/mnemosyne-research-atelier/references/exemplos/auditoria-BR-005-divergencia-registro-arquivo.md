# Auditoria — BR-005: divergência registro × arquivo de imagem

**Modo:** auditoria de acervo (exemplar). **Data:** 2026-09-08.
**Objeto auditado:** registro `BR-005` em
`hub/iconocracy-corpus/corpus/corpus-data-enriched.json`
("Alegoria da República (Décio Villares)", c. 1900).

## Divergências encontradas (evidência)

1. **Metadados do registro × página do arquivo indicado.**
   - Registro: óleo sobre tela, "sketch", **97 × 77 cm**, **Museu Histórico
     Nacional**, c. 1900, barrete frígio inscrito "Ordem e Progresso".
   - Arquivo referido (thumbnail_url do registro): hash inexistente
     (`.../commons/thumb/4/4b/...` → erro 404 no Wikimedia).
   - Arquivo real localizado por busca direta (mesmo título de arquivo,
     `.../commons/2/27/Décio_Villares_-_A_República.jpg`): página estruturada do
     Commons indica obra **"A República", 1919, óleo, 55 × 45 cm, acervo do
     Senado Federal (Brasília)**, fonte: catálogo do acervo do Senado.
   - Conclusão preliminar: dois quadros distintos (esboço do MHN vs. tela do
     Senado) colidem sob o título genérico "A República"; o registro BR-005
     parece mesclar metadados de um com a URL de outro.

2. **Leitura visual preliminar (observador, baixa resolução 503×616; marcar
   como hipótese, não como identificação).** A imagem do arquivo 2/27 não
   apresenta, à resolução disponível, barrete frígio, bandeira, espada ou a
   inscrição "Ordem e Progresso": vê-se figura feminina de perfil com cabeça
   coberta por tecido verde-escuro, fundo ocre/dourado; assinatura lida como
   "D. Volkoff 1912" (leitura incerta — pode ser má leitura de "D. Villares";
   exige conferência em resolução maior).

## Recomendação

- Não usar BR-005 como se o arquivo 2/27 fosse o esboço do MHN.
- Conferir em alta resolução: (a) a tela do Senado (catálogo do acervo do
  Senado Federal, PDF citado na página do Commons); (b) eventuais arquivos
  irmãos — "Décio Villares (1851–1931). República, ost, 60 × 49 cm" e
  "Décio Villares - A República (MR).jpg" — para identificar qual corresponde
  ao esboço do MHN (97 × 77 cm) descrito no registro.
- Corrigir no corpus canônico (competência do `iconocracy-corpus`, fora do
  ateliê): apontar o thumbnail para arquivo existente e desambiguar o título.

## Lacunas

Cadeia de custódia do arquivo 2/27 (upload 2013, usuário Dornicke, fonte =
catálogo do Senado); sem confirmação independente da autoria/identidade visual
em alta resolução.
