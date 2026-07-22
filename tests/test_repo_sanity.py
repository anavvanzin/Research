"""Smoke test do meta-workspace.

O CI (`.github/workflows/python-package-conda.yml`) roda `pytest` após o lint.
Sem nenhum teste coletável o pytest sai com código 5 e o job falha; este arquivo
dá ao pytest algo mínimo e útil para coletar: garante que todo `.py` versionado
compila (sintaxe válida), cobrindo os poucos utilitários rastreados no repo.
"""
from __future__ import annotations

import py_compile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Diretórios que não devem entrar na varredura (caches, vendored, VCS).
_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv"}


def _tracked_python_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*.py"):
        if any(part in _SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def test_repo_has_python_files() -> None:
    """A varredura precisa encontrar ao menos este próprio arquivo de teste."""
    assert _tracked_python_files(), "nenhum arquivo .py encontrado no repositório"


@pytest.mark.parametrize("py_file", _tracked_python_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_python_file_compiles(py_file: Path) -> None:
    """Cada arquivo Python versionado deve compilar sem erro de sintaxe."""
    py_compile.compile(str(py_file), doraise=True)
