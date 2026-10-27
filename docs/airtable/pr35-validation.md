# PR #35 — revisão documental em 2026-10-16

## Escopo e estado

Correção do contrato de amostragem, sem executar seleção do corpus e sem merge
da PR. Seed `cv-pilot-0.1`, alvo 30, limites 3–6, condição 6×5 e ordem dos totais
de fallback preservados. A integração de `main` na branch preserva a política
de crosswalk, as regras de consultas/galerias e os arquivos de outras áreas.
Base conferida: `712bee45b88f3a88cd5cf771fb3022fcf861749a`.

O template de `data/public/airtable/manifest.template.json` fica idêntico à main.
O novo template é apenas documentação em `docs/airtable/`; configurações,
implementação e artefatos experimentais pertencem a `iconocracy-corpus`.

## Verificações

- `cd docs/airtable && python3 -m unittest discover -s tests -v`: 15 testes
  passam. Cobrem vetores UTF-8/byte 1f, leitura do separador JSON, payload
  interpretado do template, ordem hash crescente, colisão com desempate Unicode,
  permutação de entradas, IDs inválidos/duplicados, reservas sem reposição,
  tamanhos 1/2, 6×5, fallback `(3,5,5,5,5,7)`, total 29/24, inviabilidade e
  redistribuição com aritmética racional. São testes sintéticos de conformidade,
  não execução de um algoritmo de produção nem avaliação do frame real.
- Regressões documentais reproduzidas antes da correção: separador literal no
  JSON, direção ausente, vínculo de identidade ausente, fragmento incorreto,
  tamanho apagado e falta de bloqueio explícito do frame.
- `python3 -m json.tool sampling-manifest.template.json`: JSON válido.
- `git diff --check`: sem erros; conflito de QA resolvido preservando ambas as
  seções; delta final contra main restrito a `docs/airtable/`.
- `python3 scripts/git_physics_guard.py --mode info`: exit 0, com WARN de paths
  não listados como Owns. Durante a integração o comando também vê arquivos
  recebidos da main; isso não significa que foram editados nesta correção.
  A matriz de ownership não concede ownership explícito de `docs/airtable/`
  ao `codex-app`, embora AGENTS permita versionar `docs/`. Não se declara gate
  de ownership em enforce aprovado. Avaliação da função canônica do guard sobre
  os seis paths do delta contra main: seis WARN em info e seis BLOCK em enforce.
  Harmonização dessa discrepância segue como
  impedimento de integração. Não se alterou matriz nem identidade do harness.
- Detector exigido por AGENTS:
  `python3 ~/.hermes/skills/research/drift-detector/scripts/detect_drift.py --quiet`
  retorna **exit 2 / arquivo inexistente**. `~/.hermes` está ausente; não foi
  encontrada cópia do detector em `~/.codex/skills` nem neste checkout.
  `find-skill` também não está disponível. Os sub-repositórios e os caminhos
  macOS/conda referidos por AGENTS não existem neste ambiente Linux.
  Não é drift HIGH reproduzido nem aprovação: a verificação obrigatória está
  **indisponível**, precisa ocorrer no ambiente equipado antes de integração.
  As correções são submetidas para revisão com esse impedimento explícito,
  conforme o escopo solicitado; não se substituiu o detector por um simulacro.

## Reavaliação individual das threads anteriores

| Thread | Tema | Resultado |
|---|---|---|
| `PRRT_kwDOSDEvJc6hXCHH` | P1 antigo 6×5 | Já corrigido na branch anterior; condição todos ≥5 preservada e coberta pelo caso `(3,5,5,5,5,7)`. Pode resolver. |
| `PRRT_kwDOSDEvJc6hXCHK` | Tamanho 1/2 | Tamanho real preservado; só alocação/probabilidade zeradas. Pode resolver. |
| `PRRT_kwDOSDEvJc6hXCHQ` | Fragmento | Template documental usa fragmento acentuado real. Pode resolver. |
| `PRRT_kwDOSDEvJc6iouQu` | Separador | Campo JSON decodifica U+001F; vetor confere bytes/hash. Pode resolver. |
| `PRRT_kwDOSDEvJc6iouQ4` | Funil | Mapeamento canônico vinculado por commit; funil completo ainda não aprovado. Bloqueio explícito; manter aberta. |
| `PRRT_kwDOSDEvJc6iouQ8` | Ordem hash | Hex minúsculo crescente, desempate Unicode crescente. Pode resolver. |
| `PRRT_kwDOSDEvJc6iouRB` | Identidade | Equivalência explícita com ID do corpus, comprovada no crosswalk, sem transformar IDs. Pode resolver. |
| `PRRT_kwDOSDEvJc6iouRH` | data/public | Removido integralmente o delta desse path contra main; template em docs. Problema específico corrigido; pode resolver, sem afirmar enforce geral aprovado. |
| `PRRT_kwDOSDEvJc6iouRP` | Drift obrigatório | Detector ausente: manter aberta. |
| `PRRT_kwDOSDEvJc6sn1SY` | Funil (segunda revisão) | Mesma pendência de aprovação; manter aberta. |
| `PRRT_kwDOSDEvJc6sn1S5` | Tamanho (segunda revisão) | Corrigido como acima. Pode resolver. |

## Pendências para integração/execução

1. Aprovar e versionar o funil completo no repositório canônico, com predicados,
   precedência e códigos de exclusão; preencher as referências nulas do template.
2. Validar crosswalk, suportes e metadados do universo inteiro, resolver pendências
   e congelar o frame com hash antes de produzir qualquer seleção definitiva.
3. Executar detector de drift real e resolver o ownership documental sob a matriz.
4. Implementar e validar o seletor no repositório canônico em tarefa própria.
   Aprovação documental desta PR não equivale à implementação ou ao experimento.
