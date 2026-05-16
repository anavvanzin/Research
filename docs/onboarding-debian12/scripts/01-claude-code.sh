#!/usr/bin/env bash
# usage: bash 01-claude-code.sh
# Instala Claude Code CLI via native installer e prepara configuração mínima.
# Não use sudo — o installer recusa execução com privilégios elevados.

set -euo pipefail

if [[ $EUID -eq 0 ]]; then
  echo "rode este script SEM sudo — o native installer recusa root" >&2
  exit 2
fi

EXPECTED_FINGERPRINT="31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE"

echo "→ instalando Claude Code CLI (native installer oficial)…"
curl -fsSL https://claude.ai/install.sh | bash

# Garante que o PATH inclui ~/.local/bin
if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi
export PATH="$HOME/.local/bin:$PATH"

echo
echo "→ versão instalada:"
claude --version

echo
echo "→ diagnóstico (claude doctor):"
claude doctor || true

echo
echo "→ validação criptográfica (importa chave de release e mostra fingerprint)…"
curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import 2>/dev/null
echo
echo "Fingerprint instalado:"
gpg --fingerprint security@anthropic.com 2>/dev/null | grep -E '[A-F0-9]{4}( [A-F0-9]{4}){9}' || true
echo
echo "Fingerprint esperado:"
echo "  $EXPECTED_FINGERPRINT"
echo
echo "→ se os fingerprints coincidem, a verificação passou."

# Estrutura mínima de config
mkdir -p "$HOME/.claude"
if [[ ! -f "$HOME/.claude/settings.json" ]]; then
  cat > "$HOME/.claude/settings.json" <<'EOF'
{
  "autoUpdatesChannel": "stable",
  "env": {
    "USE_BUILTIN_RIPGREP": "1"
  }
}
EOF
  echo "✓ settings.json mínimo criado em ~/.claude/settings.json"
fi

# Snapshot do diagnóstico inicial
DIAG="$HOME/.claude/diagnostico-inicial-$(date +%F).txt"
claude doctor > "$DIAG" 2>&1 || true
echo "✓ snapshot do diagnóstico salvo em $DIAG"

echo
echo "Próximos passos manuais:"
echo "  1. Abra um novo terminal (para recarregar PATH)."
echo "  2. Execute 'claude' e use '/login' para autenticar via browser."
echo "  3. Sincronize ~/.claude/CLAUDE.md do Mac via Syncthing."
