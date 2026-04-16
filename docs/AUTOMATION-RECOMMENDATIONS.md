# Recomendações de Automação Claude Code — ICONOCRACIA

> Análise: 2026-04-16 · Workspace: `~/Research/hub/iconocracy-corpus`

---

## Perfil do Workspace

- **Tipo:** Monorepo acadêmico (Python 3.12 + Pandoc + React/Vite)
- **Hooks existentes:** 13 (2 SessionStart, 2 PreToolUse, 8 PostToolUse, 1 PreCompact) — **maduro**
- **Skills locais:** 11 no hub (compilar-tese, sync-corpus, release-gate, etc.)
- **Skills Cowork:** 8 satélites (corpus-scout, iconocracy-reviewer, etc.)
- **MCP no hub:** **nenhum configurado** (mcpServers: {})
- **CI:** 7 workflows GitHub Actions (validate, deploy, claude-code-review, codeql, etc.)
- **Estado Git:** 49 commits não-pushed, 64 arquivos untracked

---

## Recomendações por Categoria

### 1. MCP Servers (PRIORIDADE ALTA — nenhum configurado no hub)

O hub tem `mcpServers: {}` no settings.json. Os MCPs que você já usa no Cowork (Gallica, Notion, HF Hub) **não estão disponíveis quando trabalha no Claude Code CLI** dentro do hub. Isso é um gap importante.

#### 1.1 Gallica MCP (já existe em `indexing/gallica-mcp-server`)

**Por quê:** Você já tem o servidor construído localmente mas ele não está registrado no settings.json do hub. Todo SCOUT e pesquisa iconográfica se beneficia.

**Configurar em** `.claude/settings.json`:
```json
{
  "mcpServers": {
    "gallica": {
      "command": "npm",
      "args": ["run", "dev"],
      "cwd": "indexing/gallica-mcp-server"
    }
  }
}
```

#### 1.2 Notion MCP

**Por quê:** 4 databases Notion (Corpus, Glossário, Decisões Metodológicas) são referenciadas mas não há sync. Com MCP, o futuro `notion_sync.py` pode usar tools nativos.

**Instalar:** `claude mcp add notion` (requer integration token)

---

### 2. Hooks — Recomendações Adicionais

Seus hooks atuais são bons (protegem manuscrito, validam naming, auto-stage vault notes). Faltam dois:

#### 2.1 Hook: Bloquear binários em `data/raw/` (ADR-001)

**Por quê:** O CI já rejeita binários, mas o hook PreToolUse pode bloquear **antes** do commit, evitando o ciclo push → fail → fix.

```json
{
  "matcher": "Write",
  "hooks": [{
    "type": "command",
    "command": "jq -r '.tool_input.file_path' | { read -r f; echo \"$f\" | grep -q 'data/raw/' && file --mime-type -b \"$f\" 2>/dev/null | grep -qvE 'text/|application/json' && echo '{\"decision\":\"block\",\"reason\":\"ADR-001: binarios pertencem ao Google Drive, nao a data/raw/.\"}'; } || true",
    "statusMessage": "Checking ADR-001..."
  }]
}
```

#### 2.2 Hook: Auto-push após commit (resolve o problema dos 49 commits)

**Por quê:** O gap atual (49 commits locais) é causado por nunca pushar. Um hook PostToolUse async no `Bash(git commit*)` resolveria.

```json
{
  "matcher": "Bash",
  "hooks": [{
    "type": "command",
    "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git commit' && git push origin main 2>/dev/null || true",
    "async": true
  }]
}
```

**Nota:** Este hook é agressivo. Alternativa menos invasiva: SessionStart hook que avisa quantos commits estão pendentes.

---

### 3. Skills — Reorganização

#### Estado atual: 11 skills locais no hub + 8 skills Cowork

Muitos dos skills locais do hub parecem redundantes com os skills Cowork ou com o iconocracy-agent v2 que acabamos de criar:

| Skill local | Status | Ação recomendada |
|-------------|--------|-----------------|
| `compilar-tese` | **Manter** — usado diretamente | Manter como está |
| `sync-corpus` | **Avaliar** — coberto pelo modo SYNC do agent v2 | Provavelmente redundante |
| `release-gate` | **Manter** — proteção de release | Manter como está |
| `abnt-precommit` | **Manter** — validação de citações | Manter como está |
| `scout-dedupe` | **Avaliar** — coberto pelo corpus-scout? | Verificar sobreposição |
| `ssd-health` | **Manter** — checagem de hardware | Manter como está |
| `pandoc-fix` | **Manter** — troubleshooting de compilação | Manter como está |
| `zotero-cite` | **Manter** — integração Zotero | Manter como está |
| `archive-fallback` | **Avaliar** — o que faz exatamente? | Revisar |
| `ecc-iconocracy-guide` | **Avaliar** — pode ser redundante com agent v2 | Provavelmente redundante |
| `foreveryh-claude-skills-tutorial-translator` | **Remover** — parece genérico/externo | Não pertence ao hub |

#### Skill novo recomendado: `git-push-all`

**Por quê:** O workspace tem ~10 sub-repos. Um skill que faz push de todos de uma vez resolve o problema de backup.

```yaml
---
name: git-push-all
description: Push all sub-repos under ~/Research/ to their remotes
---

Iterar por todos os sub-repos e executar git push:
```bash
for d in hub/* apps/* pipelines/* labs/* shared/*; do
  [ -d "$d/.git" ] && echo "=== $d ===" && (cd "$d" && git push 2>&1) || true
done
```

---

### 4. Subagents — Não prioritário agora

O workspace já tem o iconocracy-agent v2 como orquestrador e 8 skills satélites que funcionam como subagents de fato (corpus-scout, iconocracy-reviewer, etc.). Não recomendo adicionar subagents formais neste momento — o overhead não vale para um workspace acadêmico de uma pessoa.

**Exceção futura:** quando o corpus passar de 200 itens, um subagent `corpus-validator` que roda validação completa em background após edits pode ser útil.

---

### 5. Plugins — Já instalados

Os plugins necessários já estão no Cowork (ECC, Gallica, data, productivity). Nenhum plugin adicional recomendado.

---

## Resumo de Ações

| # | Ação | Impacto | Esforço |
|---|------|---------|---------|
| 1 | Registrar Gallica MCP no hub settings.json | Alto — habilita SCOUT no CLI | 5 min |
| 2 | Adicionar hook ADR-001 (bloquear binários) | Médio — previne erros no CI | 10 min |
| 3 | Adicionar hook ou script de auto-push | Alto — resolve gap de 49 commits | 10 min |
| 4 | Limpar skills redundantes (3 candidatos) | Baixo — reduz ruído | 15 min |
| 5 | Configurar Notion MCP (quando notion_sync.py for criado) | Médio — unifica dados | 30 min |

**Quer mais recomendações para alguma categoria específica?** Posso detalhar hooks, skills, ou MCP servers individualmente.
