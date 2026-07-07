#!/usr/bin/env bash
# usage: bash 03-python-conda.sh [CAMINHO_DO_ENVIRONMENT_YML]
# default: ~/iconocracy-corpus/environment.yml
#
# Instala miniforge3 em ~/.local/opt e cria o env conda 'iconocracia' a partir
# do environment.yml do monorepo. Rode SEM sudo (instalação por-usuário).

set -euo pipefail

if [[ $EUID -eq 0 ]]; then
  echo "rode SEM sudo — miniforge3 é instalação por usuário" >&2
  exit 2
fi

ENV_YML="${1:-$HOME/iconocracy-corpus/environment.yml}"
FORGE_DIR="$HOME/.local/opt/miniforge3"

if [[ ! -f "$ENV_YML" ]]; then
  echo "environment.yml não encontrado em $ENV_YML" >&2
  echo "passe o caminho como primeiro argumento, p.ex.: bash $0 ~/projeto/environment.yml" >&2
  exit 2
fi

if [[ ! -d "$FORGE_DIR" ]]; then
  echo "→ baixando e instalando miniforge3 em $FORGE_DIR…"
  TMP_INSTALLER="$(mktemp /tmp/miniforge.XXXXXX.sh)"
  curl -fsSL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
    -o "$TMP_INSTALLER"
  bash "$TMP_INSTALLER" -b -p "$FORGE_DIR"
  rm -f "$TMP_INSTALLER"
else
  echo "→ miniforge3 já existe em $FORGE_DIR (reuso)"
fi

# Inicializa para bash se ainda não estiver
"$FORGE_DIR/bin/conda" init bash >/dev/null
# Recarrega contexto conda na shell atual
# shellcheck disable=SC1091
source "$FORGE_DIR/etc/profile.d/conda.sh"

echo "→ criando env 'iconocracia' a partir de $ENV_YML…"
if conda env list | awk '{print $1}' | grep -qx "iconocracia"; then
  echo "  env 'iconocracia' já existe; usando 'conda env update' para sincronizar"
  conda env update --name iconocracia --file "$ENV_YML" --prune
else
  conda env create --name iconocracia --file "$ENV_YML"
fi

echo
echo "✓ env conda 'iconocracia' pronto."
echo "  Para ativar em nova shell: conda activate iconocracia"
echo
echo "→ snapshot do ambiente:"
# Usa arquivo temporário para evitar que SIGPIPE do `head` propague sob
# `set -o pipefail` e faça o script sair com status != 0 após tudo dar certo.
SNAPSHOT="$(mktemp)"
conda env export --name iconocracia > "$SNAPSHOT"
head -30 "$SNAPSHOT"
rm -f "$SNAPSHOT"
echo "  (truncado em 30 linhas; export completo em conda env export --name iconocracia)"
