#!/usr/bin/env bash
# usage: sudo bash 02-academic-stack.sh
# Instala Obsidian, Syncthing, GitHub CLI, VS Code, Starship e rclone.
# Zotero 7 e plugins ficam por conta da execução manual (manual.md § 2.3).

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "rode com sudo — vários pacotes vão para /etc e /usr/local" >&2
  exit 2
fi

REAL_USER="${SUDO_USER:-$(logname)}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"

export DEBIAN_FRONTEND=noninteractive

# ---------- Syncthing (repo oficial) ----------------------------------------
echo "→ Syncthing…"
install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://syncthing.net/release-key.gpg -o /etc/apt/keyrings/syncthing-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/syncthing-archive-keyring.gpg] https://apt.syncthing.net/ syncthing stable" \
  > /etc/apt/sources.list.d/syncthing.list

# ---------- GitHub CLI (repo oficial) ---------------------------------------
echo "→ GitHub CLI (gh)…"
wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null
chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  > /etc/apt/sources.list.d/github-cli.list

# ---------- VS Code (repo oficial Microsoft) --------------------------------
echo "→ VS Code…"
install -D -o root -g root -m 644 \
  <(wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor) \
  /etc/apt/keyrings/packages.microsoft.gpg
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" \
  > /etc/apt/sources.list.d/vscode.list

apt update
apt install -y syncthing gh code

# ---------- Obsidian (download manual do .deb mais recente) -----------------
echo "→ Obsidian…"
OBS_TMP="$(mktemp -d)"
cd "$OBS_TMP"
LATEST=$(curl -s https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest \
  | grep -oE '"browser_download_url":\s*"[^"]+_amd64\.deb"' \
  | head -1 \
  | sed 's/.*"\(.*\)"/\1/')
if [[ -n "$LATEST" ]]; then
  wget -O obsidian.deb "$LATEST"
  apt install -y ./obsidian.deb
  echo "✓ Obsidian instalado: $LATEST"
else
  echo "! Não consegui descobrir versão mais recente; instale manualmente de https://obsidian.md/download"
fi
cd /
rm -rf "$OBS_TMP"

# ---------- Starship prompt -------------------------------------------------
echo "→ Starship…"
sudo -u "$REAL_USER" bash -c '
  curl -fsSL https://starship.rs/install.sh | sh -s -- --yes
  if ! grep -q "starship init bash" "$HOME/.bashrc" 2>/dev/null; then
    echo "eval \"\$(starship init bash)\"" >> "$HOME/.bashrc"
  fi
'

# ---------- rclone ----------------------------------------------------------
echo "→ rclone…"
curl -fsSL https://rclone.org/install.sh | bash

# ---------- Habilita Syncthing como user service ----------------------------
echo "→ habilitando Syncthing como serviço do usuário…"
sudo -u "$REAL_USER" XDG_RUNTIME_DIR="/run/user/$(id -u $REAL_USER)" \
  systemctl --user enable syncthing.service || true
sudo -u "$REAL_USER" XDG_RUNTIME_DIR="/run/user/$(id -u $REAL_USER)" \
  systemctl --user start syncthing.service || true

# Extensões VS Code mínimas
echo "→ extensões VS Code essenciais…"
EXT_LIST=(
  ms-python.python
  ms-python.vscode-pylance
  yzhang.markdown-all-in-one
  eamodio.gitlens
  dbaeumer.vscode-eslint
  anthropic.claude-code
)
for ext in "${EXT_LIST[@]}"; do
  sudo -u "$REAL_USER" code --install-extension "$ext" --force >/dev/null 2>&1 || \
    echo "  - falha ao instalar $ext (instale manualmente depois)"
done

echo
echo "✓ Stack acadêmico instalado."
echo "  Próximos passos manuais:"
echo "  - parear Syncthing com o Mac em http://localhost:8384"
echo "  - configurar gh: 'gh auth login' como usuário normal"
echo "  - instalar Zotero 7 manualmente (manual.md § 2.3)"
