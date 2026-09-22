"""Smoke test do meta-workspace.

O CI (`.github/workflows/python-package-conda.yml`) roda `pytest` após o lint.
Sem nenhum teste coletável o pytest sai com código 5 e o job falha; este arquivo
dá ao pytest algo mínimo e útil para coletar: garante que todo `.py` versionado
compila (sintaxe válida), cobrindo os poucos utilitários rastreados no repo.
"""
from __future__ import annotations

import py_compile
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _tracked_python_files() -> list[Path]:
    """Os `.py` **rastreados pelo Git** — o nome desta função sempre disse isso.

    Até 2026-09-22 o corpo fazia `REPO_ROOT.rglob("*.py")` com uma lista de
    diretórios a pular. No container remoto dá no mesmo, porque lá só existe o
    meta-repo; no Mac da Ana a raiz também contém as skills host-only nunca
    commitadas, as worktrees gitignored de `.claude/worktrees/` e os sub-repos
    irmãos, e a varredura descia por todos eles — Python alheio ao meta-repo
    derrubando `pytest tests/` na máquina de quem trabalha, que é exatamente o que
    a regra de escopo do `AGENTS.md` manda evitar. A blocklist não tinha como
    acompanhar: ela enumerava caches, não árvores de outro repositório.

    O índice enumera sem blocklist: nada de não rastreado aparece nele, e sub-repo
    irmão nunca esteve nele. É a sétima vez nesta PR que um mecanismo criado contra
    uma classe de erro consulta o disco em vez do índice — aqui numa função cujo
    próprio nome já prometia o contrário.

    Se o `git ls-files` falhar, a exceção sobe e a coleta quebra, de propósito: um
    fallback silencioso para o disco reintroduziria o bug justamente onde ninguém
    olharia.
    """
    out = subprocess.run(
        ["git", "ls-files", "-z", "*.py"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return sorted(REPO_ROOT / entry for entry in out.split("\0") if entry)


def test_repo_has_python_files() -> None:
    """O índice precisa listar ao menos este próprio arquivo de teste.

    Não é asserção de lista cheia por acidente: este arquivo é versionado, então
    zero aqui significa `git ls-files` quebrado — e a coleta vazia faria o pytest
    sair com código 5 e o job vermelho sem dizer por quê.
    """
    assert _tracked_python_files(), (
        "git ls-files '*.py' não devolveu nada — nem este arquivo de teste, que é "
        "rastreado; a varredura do smoke test está quebrada"
    )


@pytest.mark.parametrize("py_file", _tracked_python_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_python_file_compiles(py_file: Path) -> None:
    """Cada arquivo Python versionado deve compilar sem erro de sintaxe."""
    py_compile.compile(str(py_file), doraise=True)
