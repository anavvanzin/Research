# Encaminhamento do protocolo de harmonização de suportes

O meta-workspace `Research` não é a autoridade para configuração de corpus ou
seleção de imagens. A implementação canônica do protocolo inicialmente proposto
no PR #32 foi movida para `anavvanzin/iconocracy-corpus`, onde vivem os
consumidores executáveis.

- Configuração canônica: `config/support_harmonization.yaml` no corpus.
- Integração e testes: [iconocracy-corpus PR #210](https://github.com/anavvanzin/iconocracy-corpus/pull/210).
- Consumidores auditados: `tools/scripts/select_irr_sample.py`,
  `tools/scripts/irr_sample.py` e `tools/scripts/code_purification.py
  --select-sample`.

Este arquivo registra apenas a decisão de ownership e o encaminhamento entre
repositórios. Ele não replica tabelas, regras ou versões do protocolo; portanto,
não constitui uma segunda fonte de verdade.
