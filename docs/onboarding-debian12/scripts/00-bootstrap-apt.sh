#!/usr/bin/env bash
# usage: sudo bash 00-bootstrap-apt.sh
# Pacotes base para Debian 12 — fundação do workstation doutoral.
# Idempotente: pode rodar várias vezes; apt cuida da reentrada.

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "este script precisa de sudo (instala pacotes via apt)" >&2
  exit 2
fi

export DEBIAN_FRONTEND=noninteractive

apt update
apt upgrade -y

apt install -y \
  git curl wget gpg ca-certificates build-essential \
  ripgrep fd-find jq unzip xz-utils make \
  pandoc texlive-xetex texlive-fonts-recommended texlive-fonts-extra \
  texlive-lang-portuguese texlive-luatex \
  python3-pip python3-venv \
  ffmpeg imagemagick poppler-utils \
  htop tmux

# fd é distribuído como fdfind em Debian — criar symlink amigável
if ! command -v fd >/dev/null 2>&1; then
  ln -sf "$(command -v fdfind)" /usr/local/bin/fd
fi

echo
echo "✓ Pacotes base instalados."
echo "  Próximo: scripts/01-claude-code.sh (instala Claude Code CLI)."
