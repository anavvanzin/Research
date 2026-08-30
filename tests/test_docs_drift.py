"""Guarda de drift dos documentos de governança.

O `AGENTS.md` já descreve o *Drift protocol* — a classe de bug dominante do
workspace é "config apontando para uma realidade que mudou". O detector citado
lá (`~/.hermes/skills/research/drift-detector/`) é 🖥️ host-only e não roda em
sessões remotas/web, então a política existia sem nenhuma aplicação dentro do
repo. Este arquivo é essa aplicação.

Verifica apenas afirmações **checáveis dentro deste repo**:

1. caminhos ancorados numa entrada real da raiz existem de fato;
2. a tabela de skills de projeto bate com `.claude/skills/`;
3. as contagens declaradas de `cowork/` batem com o disco;
4. nenhuma referência sobrou ao nome antigo `find-skill` (o skill é `find-skills`).

Superfícies que vivem só no Mac de Ana ficam fora: uma linha marcada
`host-only` ou com `<!-- drift-pin: ... -->` é ignorada, e caminhos ancorados
fora da raiz versionada (`hub/`, `Tools/`, `~/...`) nunca são verificados.

Roda junto com `test_repo_sanity.py` no mesmo passo `pytest` do
`.github/workflows/python-package-conda.yml`.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Documentos de governança sob guarda.
GOVERNANCE_DOCS = (
    "CLAUDE.md",
    "README.md",
    "AGENTS.md",
    ".claude/AUTOMATION.md",
)

# Uma linha com qualquer destes marcadores é ignorada por completo.
_ESCAPE_MARKERS = ("host-only", "drift-pin")

# Caracteres que denunciam glob, placeholder ou trecho de comando — não é caminho literal.
_NOT_A_LITERAL_PATH = set("*{}<>|$ ")

_BACKTICKED = re.compile(r"`([^`\n]+)`")


def _is_escaped(line: str) -> bool:
    return any(marker in line for marker in _ESCAPE_MARKERS)


def _iter_doc_lines(doc: str):
    """Devolve (nº da linha, texto) das linhas verificáveis de `doc`.

    Escapa em dois níveis: uma linha marcada é pulada, e um **cabeçalho**
    marcado silencia toda a sua seção (até o próximo cabeçalho `##`) — útil
    para tabelas inteiras cujos caminhos são relativos a outro repo.
    """
    section_escaped = False
    for lineno, line in enumerate((REPO_ROOT / doc).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section_escaped = _is_escaped(line)
        if section_escaped or _is_escaped(line):
            continue
        yield lineno, line


def _candidate_paths(doc: str) -> list[tuple[int, str]]:
    """Tokens em crase que afirmam um caminho ancorado na raiz versionada.

    Só entra o token cujo **primeiro segmento** já existe na raiz do repo. Isso
    exclui de graça: caminhos absolutos, `~/...`, sub-repos irmãos ausentes
    (`hub/`, `apps/`, `Tools/`) e fragmentos relativos a outro diretório
    (`hooks/post-bash.sh`, relativo a `.claude/self-improving-agent/`).
    """
    found: list[tuple[int, str]] = []
    for lineno, line in _iter_doc_lines(doc):
        for token in _BACKTICKED.findall(line):
            if "/" not in token:
                continue  # nome solto (`CLAUDE.md`) é ambíguo, não é afirmação de caminho
            if _NOT_A_LITERAL_PATH & set(token):
                continue
            if token.startswith(("/", "~", "http")):
                continue
            first_segment = token.split("/", 1)[0]
            if not first_segment or not (REPO_ROOT / first_segment).exists():
                continue
            found.append((lineno, token))
    return found


_PATH_CASES = [
    (doc, lineno, token)
    for doc in GOVERNANCE_DOCS
    for lineno, token in _candidate_paths(doc)
]


@pytest.mark.parametrize(
    ("doc", "lineno", "token"),
    _PATH_CASES,
    ids=[f"{doc}:{lineno}:{token}" for doc, lineno, token in _PATH_CASES],
)
def test_documented_path_exists(doc: str, lineno: int, token: str) -> None:
    """Todo caminho ancorado citado num doc de governança precisa existir."""
    relative = token.rstrip("/")
    doc_dir = (REPO_ROOT / doc).parent
    resolved = (REPO_ROOT / relative).exists() or (doc_dir / relative).exists()
    assert resolved, (
        f"{doc}:{lineno} cita `{token}`, que não existe no repo. "
        f"Atualize o doc com o valor real (Drift protocol, AGENTS.md); se a superfície "
        f"vive só no Mac, marque a linha (ou o cabeçalho da seção) como host-only, "
        f"ou anote com <!-- drift-pin: ... -->."
    )


def test_project_skill_table_matches_disk() -> None:
    """A tabela de skills de projeto do AUTOMATION.md precisa bater com o disco.

    Regressão do drift original: o doc declarava 6 entradas com apenas 1 versionada.
    """
    automation = (REPO_ROOT / ".claude/AUTOMATION.md").read_text(encoding="utf-8")
    on_disk = {p.name for p in (REPO_ROOT / ".claude/skills").iterdir() if p.is_dir()}

    header = re.search(
        r"\*\*Project \(`\.claude/skills/`\)\*\* — (\d+) versioned entries", automation
    )
    assert header, "AUTOMATION.md perdeu o cabeçalho da tabela de skills de projeto"

    declared_count = int(header.group(1))
    assert declared_count == len(on_disk), (
        f"AUTOMATION.md declara {declared_count} skills de projeto, "
        f"mas `.claude/skills/` tem {len(on_disk)}: {sorted(on_disk)}"
    )

    # Linhas de tabela entre o cabeçalho e o parágrafo de host-only que o sucede.
    table = automation[header.end():automation.index("host-only", header.end())]
    listed = set(re.findall(r"^\| `([a-z0-9-]+)` \|", table, flags=re.MULTILINE))
    assert listed == on_disk, (
        f"tabela de skills de projeto fora de sincronia — "
        f"listadas mas ausentes: {sorted(listed - on_disk)}; "
        f"no disco mas não listadas: {sorted(on_disk - listed)}"
    )

    for skill in sorted(on_disk):
        assert (REPO_ROOT / ".claude/skills" / skill / "SKILL.md").is_file(), (
            f"skill de projeto `{skill}` não tem SKILL.md"
        )


@pytest.mark.parametrize(
    ("doc", "pattern", "actual"),
    [
        (
            "README.md",
            r"85 definições de agentes \+ 12 integrações",
            (
                len(list((REPO_ROOT / "cowork/agents").rglob("*.md"))),
                len([p for p in (REPO_ROOT / "cowork/integrations").iterdir() if p.is_dir()]),
            ),
        ),
    ],
    ids=["README:cowork-counts"],
)
def test_documented_counts_match(doc: str, pattern: str, actual: tuple[int, int]) -> None:
    """As contagens de `cowork/` afirmadas nos docs precisam bater com o disco."""
    text = (REPO_ROOT / doc).read_text(encoding="utf-8")
    assert re.search(pattern, text), f"{doc} perdeu a frase de contagem esperada"
    assert actual == (85, 12), (
        f"{doc} declara 85 agentes + 12 integrações, mas o disco tem "
        f"{actual[0]} agentes + {actual[1]} integrações"
    )


@pytest.mark.parametrize("doc", GOVERNANCE_DOCS)
def test_no_stale_find_skill_reference(doc: str) -> None:
    """O skill instalado chama-se `find-skills`; `find-skill` no singular não existe.

    Regressão do bug encontrado em 2026-08-30, quando os quatro docs de governança
    mandavam invocar um skill inexistente.
    """
    text = (REPO_ROOT / doc).read_text(encoding="utf-8")
    stale = re.findall(r"find-skill(?!s)", text)
    assert not stale, (
        f"{doc} referencia `find-skill` ({len(stale)}×); o skill instalado é `find-skills`"
    )
