"""Guarda de drift dos documentos de governança.

O `AGENTS.md` já descreve o *Drift protocol* — a classe de bug dominante do
workspace é "config apontando para uma realidade que mudou". O detector citado
lá (`~/.hermes/skills/research/drift-detector/`) é 🖥️ host-only e não roda em
sessões remotas/web, então a política existia sem nenhuma aplicação dentro do
repo. Este arquivo é essa aplicação.

Verifica apenas afirmações **checáveis dentro deste repo**:

1. caminhos ancorados numa raiz conhecida (versionada ou aposentada) estão **no índice
   do Git**, e link markdown resolve relativo ao próprio documento;
2. a tabela de skills de projeto bate com `git ls-files .claude/skills`;
3. toda contagem declarada de `cowork/` bate com o índice;
4. nenhuma referência sobrou ao nome antigo `find-skill` (o skill é `find-skills`);
5. nenhuma skill é declarada sincronizada **e** host-only ao mesmo tempo.

Cobre os quatro docs de governança em prosa mais `docs/decisions/AGENT-OWNERSHIP.md`,
que é lido por máquina (`scripts/git_physics_guard.py`).

Superfícies que vivem só no Mac de Ana ficam fora: uma linha marcada
`host-only` ou com `<!-- drift-pin: ... -->` é ignorada, e caminhos ancorados
fora da raiz versionada (`hub/`, `Tools/`, `~/...`) nunca são verificados.

Roda junto com `test_repo_sanity.py` no mesmo passo `pytest` do
`.github/workflows/python-package-conda.yml`.
"""
from __future__ import annotations

import itertools
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Documentos de governança sob guarda.
#
# `AGENT-OWNERSHIP.md` entrou em 2026-09-19. Não é prosa como os outros quatro: é o
# contrato que `scripts/git_physics_guard.py` **parseia** para decidir a que harness
# pertence cada path staged. Um caminho podre ali não é um link quebrado, é o guard
# distribuindo permissão sobre superfície inexistente — foi o que a rodada 3 desta PR
# achou à mão. Ver `docs/decisions/2026-09-19-guarda-drift-agent-ownership.md`.
GOVERNANCE_DOCS = (
    "CLAUDE.md",
    "README.md",
    "AGENTS.md",
    ".claude/AUTOMATION.md",
    "docs/decisions/AGENT-OWNERSHIP.md",
)

# Uma linha com qualquer destes marcadores é ignorada por completo.
_ESCAPE_MARKERS = ("host-only", "drift-pin")

# Caracteres que denunciam glob, placeholder ou trecho de comando — não é caminho literal.
_NOT_A_LITERAL_PATH = set("*{}<>|$ ")

# Raízes versionadas deste repo, declaradas **independentemente da existência atual**.
# Ancorar na existência em disco criava um ponto cego: apagar `.opencode/` inteiro faria
# as referências a `.opencode/plans/...` sumirem de _PATH_CASES e o CI passar — justamente
# o drift que este teste existe para pegar. Editar esta constante é deliberado; o
# test_versioned_roots_are_declared avisa quando uma raiz nova é rastreada e falta aqui.
_VERSIONED_ROOTS = frozenset({
    ".claude", ".devcontainer", ".github", ".opencode", ".planning",
    "cowork", "data", "docs", "plans", "scripts", "tests",
})

# Arquivos versionados na raiz. Um token sem "/" só é verificável se estiver aqui:
# nomes soltos aparecem muito na prosa justamente para falar de arquivos que **não**
# existem (`package.json`, `vercel.json`, `nextjs.yml`), então checar todos daria
# falso positivo. Declarados, como as raízes acima, para que renomear ou remover um
# deles com a referência de pé continue falhando.
_VERSIONED_ROOT_FILES = frozenset({
    "AGENTS.md", "CLAUDE.md", "README.md",
    "environment.yml", ".gitignore", ".gitattributes",
})

# Raízes e arquivos **já aposentados**: não são mais versionados, mas continuam no
# vocabulário de detecção. Sem isso, aposentar uma superfície (tirando-a da tabela
# canônica e de `_VERSIONED_ROOTS`) faria toda referência residual a ela deixar de ser
# reconhecida como caminho — e o CI voltaria ao verde justamente no drift que a guarda
# existe para pegar. Ao remover uma superfície, **mova** o nome para cá em vez de apagá-lo.
_RETIRED_ROOTS: frozenset[str] = frozenset()
_RETIRED_ROOT_FILES: frozenset[str] = frozenset()

# O que conta como "token que afirma um caminho deste repo" — atual **ou** aposentado.
_KNOWN_ROOTS = _VERSIONED_ROOTS | _RETIRED_ROOTS
_KNOWN_ROOT_FILES = _VERSIONED_ROOT_FILES | _RETIRED_ROOT_FILES

_BACKTICKED = re.compile(r"`([^`\n]+)`")

# Destino de link markdown: `[texto](caminho)`. A regex de crase nunca pegava isto, então
# renomear um doc linkado deixava o link quebrado e o CI verde — inclusive os ponteiros
# para a lista canônica que esta PR introduziu. Link explícito é inequívoco: quando começa
# com ./ ou ../ é validado relativo ao próprio doc, sem passar pelo filtro de raízes.
_MD_LINK = re.compile(r"\]\(([^)\s]+)\)")

# Cabeçalho de qualquer nível encerra o escape de seção.
_HEADING = re.compile(r"^#{1,6} ")


def _is_escaped(line: str) -> bool:
    return any(marker in line for marker in _ESCAPE_MARKERS)


def _iter_doc_lines(doc: str):
    """Devolve (nº da linha, texto) das linhas verificáveis de `doc`.

    Escapa em dois níveis: uma linha marcada é pulada, e um **cabeçalho**
    marcado silencia a sua seção — útil para tabelas inteiras cujos caminhos são
    relativos a outro repo.

    Um cabeçalho marcado cobre as **subseções** abaixo dele; só um cabeçalho de nível
    igual ou mais raso o encerra. A rodada 12 fazia qualquer cabeçalho encerrar o
    escape, para o link de um ADR numa subseção `###` do `README.md` voltar a ser
    conferido; corrigida a estrutura daquele arquivo, o aninhamento passou a valer.

    Os níveis escapados vivem numa **pilha**, não num inteiro. Com um inteiro, uma
    subseção marcada dentro de uma seção marcada sobrescrevia o nível externo — um
    `###` marcado dentro de um `##` marcado levava o nível de 2 para 3 —, e o próximo
    `###` **sem** marca encerrava o escape inteiro, embora ainda estivesse dentro da
    seção host-only externa. Os caminhos locais dali em diante voltavam a ser
    conferidos e deixavam o CI remoto vermelho.
    """
    escapadas: list[int] = []
    for lineno, line in enumerate((REPO_ROOT / doc).read_text(encoding="utf-8").splitlines(), 1):
        cabecalho = _HEADING.match(line)
        if cabecalho:
            nivel = len(cabecalho.group(0)) - 1
            while escapadas and nivel <= escapadas[-1]:
                escapadas.pop()
            if _is_escaped(line):
                escapadas.append(nivel)
        if escapadas or _is_escaped(line):
            continue
        yield lineno, line


def _candidate_paths(doc: str) -> list[tuple[int, str, bool]]:
    """Tokens que afirmam um caminho deste repo, com a marca de link markdown.

    Só entra o token cujo **primeiro segmento** está em `_KNOWN_ROOTS` — as raízes
    versionadas **mais** as aposentadas. Isso exclui de graça: caminhos absolutos,
    `~/...`, sub-repos irmãos ausentes (`hub/`, `apps/`, `Tools/`) e fragmentos
    relativos a outro diretório (`hooks/post-bash.sh`, relativo a
    `.claude/self-improving-agent/`); e, por ancorar no vocabulário em vez de na
    existência, continua reconhecendo referência a raiz removida — tanto a que
    desapareceu do disco quanto a que foi formalmente aposentada.
    """
    found: list[tuple[int, str, bool]] = []
    for lineno, line in _iter_doc_lines(doc):
        candidates = [(tok, False) for tok in _BACKTICKED.findall(line)]
        candidates += [
            (tok.split("#", 1)[0], True)          # âncora #secao não faz parte do caminho
            for tok in _MD_LINK.findall(line)
        ]
        for token, is_link in candidates:
            if not token or _NOT_A_LITERAL_PATH & set(token):
                continue
            if token.startswith(("/", "~", "http", "mailto:")):
                continue
            if is_link:
                # Link markdown local resolve relativo ao próprio documento, com ou sem
                # `./`. Exigir o prefixo descartava `[ADR](2026-09-19-exemplo.md)` — a
                # sintaxe normal — e também `[x](subdir/arquivo.md)` num doc aninhado,
                # cujo primeiro segmento não é raiz desta raiz. Apagar o alvo deixava o
                # link quebrado com a guarda verde. Os filtros de raiz abaixo valem para
                # o token em crase, que é afirmação de caminho **da raiz**; aqui eles só
                # cegavam.
                found.append((lineno, token, True))
                continue
            if "/" not in token:
                # Nome solto: só conta se for arquivo de raiz versionado e declarado.
                if token not in _KNOWN_ROOT_FILES:
                    continue
            elif token.split("/", 1)[0] not in _KNOWN_ROOTS:
                continue
            found.append((lineno, token, is_link))
    return found


_PATH_CASES = [
    (doc, lineno, token, is_link)
    for doc in GOVERNANCE_DOCS
    for lineno, token, is_link in _candidate_paths(doc)
]


@pytest.mark.parametrize(
    ("doc", "lineno", "token", "is_link"),
    _PATH_CASES,
    ids=[f"{doc}:{lineno}:{token}" for doc, lineno, token, _ in _PATH_CASES],
)
def test_documented_path_exists(doc: str, lineno: int, token: str, is_link: bool) -> None:
    """Todo caminho ancorado citado num doc de governança precisa estar **no índice**.

    Link markdown resolve **só** relativo ao diretório do próprio documento, como o
    GitHub o resolve. Aceitar também a raiz deixaria `[texto](README.md)` dentro de
    `.claude/AUTOMATION.md` passar por causa do `README.md` da raiz, enquanto o link
    renderizado aponta para `.claude/README.md` e está quebrado. Token em crase é
    afirmação de caminho **da raiz** por construção (o filtro de raízes acima), então
    para ele a raiz é a referência correta.

    A pergunta é *está versionado?*, não *existe em disco?* — e era `Path.exists()` até
    a rodada 18, a sexta vez nesta PR que um mecanismo contra drift consultou o disco.
    Um caminho tirado do índice mas com cópia ignorada ou não rastreada no Mac (sob
    `.claude/`, sobretudo, onde vivem as skills host-only e as worktrees gitignored)
    deixava `pytest tests/` verde na máquina da Ana enquanto o arquivo não viajava no
    clone e o CI remoto quebrava. Era a assimetria que esta guarda existe para eliminar,
    na verificação central dela.

    Só o índice, sem conferir disco junto: `rm` local não commitado é estado sujo de
    quem trabalha, não drift de documento. Caminho real porém gitignored é caso dos
    escapes, e a mensagem abaixo diz isso.
    """
    relative = token.rstrip("/")
    doc_dir = (REPO_ROOT / doc).parent
    base = doc_dir if is_link else REPO_ROOT
    onde = f"link relativo a {base.relative_to(REPO_ROOT)}/" if is_link else "raiz do repo"

    alvo = os.path.normpath(os.path.join(str(base), relative))
    no_repo = os.path.relpath(alvo, str(REPO_ROOT))
    rastreados = _tracked_paths()
    resolved = no_repo in rastreados or any(
        entry.startswith(no_repo + "/") for entry in rastreados
    )
    assert resolved, (
        f"{doc}:{lineno} cita `{token}`, que o Git não rastreia ({onde}). "
        f"Atualize o doc com o valor real (Drift protocol, AGENTS.md); se a superfície "
        f"vive só no Mac — ou existe em disco sem ser versionada —, marque a linha "
        f"(ou o cabeçalho da seção) como host-only, ou anote com <!-- drift-pin: ... -->."
    )


def _tracked_entries(prefix: str = "") -> list[Path]:
    """Caminhos rastreados pelo Git sob `prefix`, relativos a ele.

    O disco mente das duas direções nesta árvore: no Mac ele traz sub-repos irmãos,
    árvores ignoradas e rascunhos nunca commitados que o Git não rastreia, e no
    container remoto não traz o que só existe no Mac. Toda pergunta de "isto ainda é
    versionado?" — e toda contagem que um doc afirma — se responde pelo índice.
    """
    argv = ["git", "ls-files", "-z"]
    if prefix:
        argv += ["--", prefix]
    out = subprocess.run(
        argv, cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    base = Path(prefix) if prefix else None
    entries = [Path(e) for e in out.split("\0") if e]
    return [e.relative_to(base) for e in entries] if base else entries


def _tracked_paths() -> frozenset[str]:
    """Todos os caminhos rastreados, como strings relativas à raiz.

    Memoizado: `test_documented_path_exists` é parametrizado em ~140 casos e um
    `git ls-files` por caso seria desperdício puro.
    """
    global _TRACKED_CACHE
    if _TRACKED_CACHE is None:
        _TRACKED_CACHE = frozenset(e.as_posix() for e in _tracked_entries())
    return _TRACKED_CACHE


_TRACKED_CACHE: frozenset[str] | None = None


def _tracked_top_level() -> tuple[set[str], set[str]]:
    """Diretórios e arquivos de topo **rastreados pelo Git**, não o que há em disco."""
    entries = _tracked_entries()
    dirs = {e.parts[0] for e in entries if len(e.parts) > 1}
    files = {str(e) for e in entries if len(e.parts) == 1}
    return dirs, files


def _versioned_skills() -> set[str]:
    """Skills de projeto **rastreadas pelo Git**, não o conteúdo do diretório.

    No Mac de Ana `.claude/skills/` também contém as entradas host-only nunca
    commitadas; um `iterdir()` as contaria e faria o teste falhar localmente mesmo
    com a tabela correta. Só o que está versionado conta.
    """
    out = subprocess.run(
        ["git", "ls-files", "-z", ".claude/skills"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    # `> 3` e nao `> 2`: exige `.claude/skills/<nome>/<arquivo>`. Com `> 2`, um
    # `.claude/skills/README.md` commitado viraria a "skill" README.md, e a tabela — cuja
    # regex so casa `[a-z0-9-]+` — nunca conseguiria declara-la.
    return {
        Path(entry).parts[2]
        for entry in out.split("\0")
        if entry and len(Path(entry).parts) > 3
    }


def test_project_skill_table_matches_disk() -> None:
    """A tabela de skills de projeto do AUTOMATION.md precisa bater com o disco.

    Regressão do drift original: o doc declarava 6 entradas com apenas 1 versionada.
    """
    automation = (REPO_ROOT / ".claude/AUTOMATION.md").read_text(encoding="utf-8")
    on_disk = _versioned_skills()

    header = re.search(
        r"\*\*Project \(`\.claude/skills/`\)\*\* — (\d+) versioned entries", automation
    )
    assert header, "AUTOMATION.md perdeu o cabeçalho da tabela de skills de projeto"

    declared_count = int(header.group(1))
    assert declared_count == len(on_disk), (
        f"AUTOMATION.md declara {declared_count} skills de projeto versionadas, "
        f"mas o Git rastreia {len(on_disk)}: {sorted(on_disk)}"
    )

    # Colhe as linhas de tabela que seguem o cabeçalho, parando na primeira que não é
    # linha de tabela. Duas versões anteriores cortaram no lugar errado: primeiro na
    # ocorrência de "host-only" (qualquer célula que citasse o marcador truncava a
    # tabela), depois na primeira linha em branco (a linha em branco idiomática entre
    # parágrafo e tabela esvaziava `listed`). O que delimita uma tabela é o "|".
    depois = automation[header.end():].splitlines()
    linhas = list(itertools.dropwhile(lambda l: not l.lstrip().startswith("|"), depois))
    table = "\n".join(itertools.takewhile(lambda l: l.lstrip().startswith("|"), linhas))
    listed = set(re.findall(r"^\| `([a-z0-9-]+)` \|", table, flags=re.MULTILINE))
    assert listed == on_disk, (
        f"tabela de skills de projeto fora de sincronia com o Git — "
        f"listadas mas ausentes: {sorted(listed - on_disk)}; "
        f"no disco mas não listadas: {sorted(on_disk - listed)}"
    )

    # Pelo índice, não por `is_file()`: com o manifesto fora do Git e uma cópia local
    # não rastreada no lugar, a skill continua em `_versioned_skills()` por causa dos
    # outros arquivos dela, o Mac passa, e o clone limpo recebe a skill sem manifesto.
    # Oitava vez nesta PR que uma verificação pergunta ao disco o que só o índice sabe.
    rastreados = _tracked_paths()
    for skill in sorted(on_disk):
        manifesto = f".claude/skills/{skill}/SKILL.md"
        assert manifesto in rastreados, (
            f"skill de projeto `{skill}`: o Git não rastreia `{manifesto}`. Uma cópia "
            f"local não basta — no clone do CI a skill chegaria sem manifesto."
        )


_AGENTES = re.compile(r"(\d+)\s+(?:definições de\s+)?agentes\b")
_INTEGRACOES = re.compile(r"(\d+)\s+integrações\b")


def _cowork_counts() -> tuple[int, int]:
    """Agentes e integrações de `cowork/` **segundo o índice do Git**.

    O filtro de profundidade nas integrações não é enfeite: `cowork/integrations/README.md`
    é rastreado e não é uma integração — sem ele o total daria 13 em vez de 12.
    """
    agentes = len([e for e in _tracked_entries("cowork/agents") if e.suffix == ".md"])
    integracoes = len({
        e.parts[0] for e in _tracked_entries("cowork/integrations") if len(e.parts) > 1
    })
    return agentes, integracoes


@pytest.mark.parametrize("doc", GOVERNANCE_DOCS)
def test_documented_counts_match(doc: str) -> None:
    """**Toda** afirmação numérica sobre `cowork/` num doc de governança tem de bater.

    Antes isto era uma tabela de casos com um `pattern` por documento, e a tabela tinha
    uma linha só: o `README.md`. Bastava atualizar ali para o teste passar, enquanto
    `CLAUDE.md` e `AGENTS.md` seguiam declarando o número antigo — a guarda permitia
    exatamente o drift numérico que existe para detectar, e uma quarta declaração num
    doc novo nasceria fora da cobertura. Agora o teste varre as linhas verificáveis de
    cada doc e confere cada ocorrência; não há lista a manter em sincronia.

    Os números vêm do **documento** e do **índice**, nunca de uma constante aqui nem do
    disco: uma mensagem de falha que contradiga o arquivo aberto pelo leitor é pior que
    nenhuma, e no Mac um rascunho não rastreado sob `cowork/agents/` não pode derrubar
    um build que o clone do CI aprova.

    As afirmações em inglês sobre `~/.claude/agents/` (os 14 agents globais) ficam de
    fora por construção: as regexes são das formas em português, que só o par
    `cowork/agents` + `cowork/integrations` usa.
    """
    agentes, integracoes = _cowork_counts()

    for lineno, line in _iter_doc_lines(doc):
        for declarado in _AGENTES.finditer(line):
            assert int(declarado.group(1)) == agentes, (
                f"{doc}:{lineno} declara {declarado.group(1)} agentes, mas o Git rastreia "
                f"{agentes} sob cowork/agents/. Atualize o doc, ou marque a linha como "
                f"host-only / com <!-- drift-pin: ... --> se o número for histórico."
            )
        for declarado in _INTEGRACOES.finditer(line):
            assert int(declarado.group(1)) == integracoes, (
                f"{doc}:{lineno} declara {declarado.group(1)} integrações, mas o Git "
                f"rastreia {integracoes} diretórios sob cowork/integrations/ "
                f"(o README.md solto lá não conta)."
            )


def test_cowork_counts_are_stated_somewhere() -> None:
    """Apagar a frase não pode ser jeito de calar o teste acima.

    O varredor conferiria zero ocorrências e passaria. Esta é a contraparte: a
    declaração canônica do `README.md` tem de continuar existindo e visível à guarda.
    """
    declaracoes = [
        (lineno, line)
        for lineno, line in _iter_doc_lines("README.md")
        if _AGENTES.search(line) and _INTEGRACOES.search(line)
    ]
    assert declaracoes, (
        "README.md perdeu a linha que declara agentes + integrações de cowork/, ou ela "
        "foi marcada como host-only — sem ela o test_documented_counts_match não tem o "
        "que conferir"
    )


def test_counts_ignore_untracked_drafts(tmp_path: Path) -> None:
    """Um rascunho não rastreado sob `cowork/agents/` não pode mexer na contagem.

    Regressão direta do achado: enquanto a contagem vinha de `rglob`, este arquivo
    levava o total de 85 para 86 e derrubava `test_documented_counts_match` no Mac de
    Ana, com o README e o clone do CI corretos. Irmão de
    `test_never_committed_skills_are_not_versioned`, que é a mesma lição em outra
    superfície.
    """
    del tmp_path  # o caso exige o caminho real dentro do repo, não um tmp isolado
    antes = len([e for e in _tracked_entries("cowork/agents") if e.suffix == ".md"])
    probe = REPO_ROOT / "cowork/agents/_drift_probe.md"
    assert not probe.exists(), f"{probe} já existe; remova antes de rodar"
    try:
        probe.write_text("rascunho de teste\n", encoding="utf-8")
        depois = len([e for e in _tracked_entries("cowork/agents") if e.suffix == ".md"])
    finally:
        probe.unlink(missing_ok=True)
    assert depois == antes, (
        f"a contagem de agentes saiu de {antes} para {depois} por causa de um arquivo "
        f"não rastreado — ela precisa vir de `git ls-files`, não do disco"
    )


@pytest.mark.parametrize("doc", GOVERNANCE_DOCS)
def test_no_stale_find_skill_reference(doc: str) -> None:
    """O skill instalado chama-se `find-skills`; `find-skill` no singular não existe.

    Regressão do bug encontrado em 2026-08-30, quando os quatro docs de governança
    mandavam invocar um skill inexistente.
    """
    stale = [
        lineno
        for lineno, line in _iter_doc_lines(doc)
        if re.search(r"find-skill(?!s)", line)
    ]
    assert not stale, (
        f"{doc} referencia `find-skill` nas linhas {stale}; o skill instalado é "
        f"`find-skills`. Para registrar o nome antigo historicamente, marque a linha "
        f"como host-only ou com <!-- drift-pin: ... -->."
    )


def _canonical_surfaces() -> tuple[set[str], set[str]]:
    """As duas linhas da tabela *Versioned surfaces* do `.claude/AUTOMATION.md`.

    Desde e95b4c6 essa tabela é a **única** enumeração em prosa; AGENTS.md, CLAUDE.md
    e README.md apontam para ela. Sem parseá-la aqui, acrescentar uma raiz só exigiria
    editar a constante e a fonte canônica podia ficar desatualizada — o furo que este
    parser fecha.
    """
    automation = (REPO_ROOT / ".claude/AUTOMATION.md").read_text(encoding="utf-8")

    def row(label: str) -> set[str]:
        m = re.search(rf"^\| {label} \|(.+)\|$", automation, flags=re.MULTILINE)
        assert m, f"tabela canônica perdeu a linha '{label}' em .claude/AUTOMATION.md"
        return set(re.findall(r"`([^`]+)`", m.group(1)))

    dirs = {d.rstrip("/") for d in row("Diretórios")}
    return dirs, row("Arquivos de raiz")


def test_canonical_table_matches_constants() -> None:
    """A tabela canônica e as constantes da guarda precisam dizer a mesma coisa.

    Fecha o furo da revisão de 2026-09-19: bastava acrescentar a raiz nova em
    `_VERSIONED_ROOTS` para o teste passar, deixando a tabela *Versioned surfaces*
    — a fonte única — atrasada.
    """
    table_dirs, table_files = _canonical_surfaces()
    assert table_dirs == set(_VERSIONED_ROOTS), (
        f"tabela canônica × _VERSIONED_ROOTS divergem — "
        f"só na tabela: {sorted(table_dirs - set(_VERSIONED_ROOTS))}; "
        f"só na constante: {sorted(set(_VERSIONED_ROOTS) - table_dirs)}. "
        f"Edite os dois: .claude/AUTOMATION.md (*Versioned surfaces*) e este arquivo."
    )
    assert table_files == set(_VERSIONED_ROOT_FILES), (
        f"tabela canônica × _VERSIONED_ROOT_FILES divergem — "
        f"só na tabela: {sorted(table_files - set(_VERSIONED_ROOT_FILES))}; "
        f"só na constante: {sorted(set(_VERSIONED_ROOT_FILES) - table_files)}."
    )


def test_versioned_roots_are_declared() -> None:
    """Toda raiz de topo rastreada precisa estar em `_VERSIONED_ROOTS`.

    Sem isso, um diretório novo entraria no repo sem que suas referências fossem
    conferidas. O inverso é permitido de propósito: uma raiz já removida continua
    declarada, para que referências órfãs a ela ainda falhem.
    """
    tracked_dirs, tracked_files = _tracked_top_level()

    missing_dirs = tracked_dirs - _VERSIONED_ROOTS
    assert not missing_dirs, (
        f"raízes rastreadas ausentes de _VERSIONED_ROOTS: {sorted(missing_dirs)} — "
        f"acrescente-as em tests/test_docs_drift.py **e** na tabela *Versioned surfaces* de .claude/AUTOMATION.md — o test_canonical_table_matches_constants cobra as duas"
    )

    missing_files = tracked_files - _VERSIONED_ROOT_FILES
    assert not missing_files, (
        f"arquivos de raiz rastreados ausentes de _VERSIONED_ROOT_FILES: "
        f"{sorted(missing_files)} — acrescente-os em tests/test_docs_drift.py **e** na tabela *Versioned surfaces* de .claude/AUTOMATION.md"
    )


def _skill_inventories() -> tuple[set[str], set[str]]:
    """Os dois inventários de skills da seção *Skills* do `.claude/AUTOMATION.md`.

    Um nome só pode estar em um dos dois: ou a skill chega numa sessão remota pela
    conta, ou é 🖥️ host-only. Estar nos dois é a contradição que um operador remoto
    paga com *Unknown command* — foi o que iniciou a PR #28.
    """
    automation = (REPO_ROOT / ".claude/AUTOMATION.md").read_text(encoding="utf-8")

    def names(anchor: str) -> set[str]:
        start = automation.find(anchor)
        assert start != -1, (
            f"seção *Skills* do .claude/AUTOMATION.md perdeu o trecho {anchor!r} — "
            f"se o texto foi reescrito, atualize este parser junto"
        )
        block = automation[start:].split("\n\n", 1)[0]
        return set(re.findall(r"`([^`\n]+)`", block))

    synced = names("Defaults sincronizados relevantes para a tese")
    host_only = names("Nomeadas nos docs mas **ausentes do conjunto sincronizado**")
    return synced, host_only


def test_section_escape_respects_nesting(tmp_path: Path) -> None:
    """Um cabeçalho marcado silencia suas **subseções**; um irmão do mesmo nível encerra.

    A rodada 12 fez qualquer cabeçalho encerrar o escape, para o link de um ADR numa
    subseção `###` do `README.md` voltar a ser conferido. O efeito colateral era que uma
    tabela host-only inteira dependia de nenhum `###` aparecer no meio dela — e o
    `docs/methodology.md`, caminho relativo ao sub-repo, escapava por acidente de posição.

    A estrutura do README foi corrigida (as duas subseções eram irmãs, não filhas, e
    viraram `##`), o que tornou seguro o escape respeitar o aninhamento: `##` marcado
    cobre seus `###`, e só um cabeçalho de nível igual ou superior o encerra.
    """
    linhas = [
        "## Seção host-only",        # abre escape em nível 2
        "`tese/inexistente/`",       # coberto
        "### Subseção sem marca",    # mais fundo: não encerra
        "`corpus/inexistente/`",     # ainda coberto
        "## Seção normal",           # irmão: encerra
        "`docs/`",                   # conferido
    ]
    doc = tmp_path / "nesting.md"
    doc.write_text("\n".join(linhas), encoding="utf-8")
    visiveis = {ln for ln, _ in _iter_doc_lines(str(doc))}

    assert 2 not in visiveis and 4 not in visiveis, (
        "um `###` sem marca encerrou o escape de um `##` marcado: a seção host-only "
        "deixou de cobrir as próprias subseções"
    )
    assert 6 in visiveis, (
        "um `##` irmão sem marca não encerrou o escape: a seção host-only vazou para "
        "a seção seguinte"
    )


def test_nested_escaped_heading_does_not_shorten_the_outer_one(tmp_path: Path) -> None:
    """Uma subseção marcada dentro de uma seção marcada não pode encurtar a de fora.

    Enquanto o nível escapado era um inteiro, o `###` marcado sobrescrevia o `##`
    marcado (2 → 3) e o `###` seguinte, **sem** marca, satisfazia `nivel <= escape_level`
    e encerrava o escape inteiro — ainda dentro da seção host-only externa. Os caminhos
    dali em diante voltavam a ser conferidos e deixavam o CI remoto vermelho. Por isso
    os níveis viram uma pilha.
    """
    linhas = [
        "## Seção host-only",        # abre escape em nível 2
        "`tese/inexistente/`",       # coberto
        "### Subseção host-only",    # marcada também: empilha o nível 3
        "`corpus/inexistente/`",     # coberto
        "### Subseção sem marca",    # desempilha só o 3; o 2 continua de pé
        "`vault/inexistente/`",      # tem de continuar coberto
        "## Seção normal",           # irmão do nível 2: encerra
        "`docs/`",                   # conferido
    ]
    doc = tmp_path / "nesting_dupla.md"
    doc.write_text("\n".join(linhas), encoding="utf-8")
    visiveis = {ln for ln, _ in _iter_doc_lines(str(doc))}

    assert 6 not in visiveis, (
        "a subseção marcada encurtou o escape da seção externa: a linha 6 voltou a ser "
        "conferida embora ainda esteja dentro do `##` host-only"
    )
    assert 8 in visiveis, "o `##` irmão não encerrou o escape depois da pilha esvaziar"


def test_guard_row_is_not_self_escaped() -> None:
    """A linha que documenta esta guarda no `.claude/AUTOMATION.md` tem de ser conferida.

    Quarta recorrência, nesta PR, de mecanismo que não se cobre — e a mais direta: a
    linha da tabela *Tests / CI* que descreve esta guarda explicava também os escapes,
    e por citar "host-only" caía no próprio `_is_escaped`, que casa por substring. Dez
    afirmações de caminho daquela linha deixavam de ser conferidas, entre elas o único
    link verificado para o ADR que a PR acrescenta: renomear o ADR quebrava o link com
    o CI verde.

    A correção foi de prosa — a explicação dos escapes desceu para um parágrafo abaixo
    da tabela —, então é aqui que ela fica presa.
    """
    doc = ".claude/AUTOMATION.md"
    visiveis = {ln for ln, _ in _iter_doc_lines(doc)}
    alvo = [
        ln
        for ln, linha in enumerate((REPO_ROOT / doc).read_text(encoding="utf-8").splitlines(), 1)
        if "Governance-doc drift guard" in linha
    ]
    assert alvo, f"{doc} perdeu a linha da tabela que descreve a guarda de drift"

    escapadas = [ln for ln in alvo if ln not in visiveis]
    assert not escapadas, (
        f"{doc}:{escapadas} descreve a guarda de drift mas está escapada dela — "
        f"a linha caiu em _is_escaped (provavelmente por citar 'host-only' ou "
        f"'drift-pin' ao explicar os escapes). Mantenha a explicação dos escapes no "
        f"parágrafo abaixo da tabela; a célula da tabela só descreve e aponta caminhos."
    )

    conferidos = {tok for ln, tok, _ in _candidate_paths(doc) if ln in alvo}
    assert "tests/test_docs_drift.py" in conferidos, (
        f"a linha da guarda em {doc} deixou de afirmar o caminho do próprio arquivo de "
        f"teste; sem isso este teste não prova que a linha está sendo conferida"
    )


def _never_committed_skills() -> set[str]:
    """A terceira tabela da seção *Skills*: presentes no Mac e nunca commitadas.

    Ela não entra em `_skill_inventories()` porque é tabela, não parágrafo, e porque a
    contradição que ela pode produzir é com o **Git**, não com os outros dois blocos:
    commitar uma destas skills deixa o índice canônico declarando, ao mesmo tempo, que
    ela é versionada e que nunca foi commitada.
    """
    automation = (REPO_ROOT / ".claude/AUTOMATION.md").read_text(encoding="utf-8")
    anchor = "Present in `.claude/skills/` on the Mac but"
    start = automation.find(anchor)
    assert start != -1, (
        "seção *Skills* do .claude/AUTOMATION.md perdeu a tabela de skills nunca "
        "commitadas — se o texto foi reescrito, atualize este parser junto"
    )
    fim = automation.find("\n\nTo make any", start)
    assert fim != -1, (
        "seção *Skills* do .claude/AUTOMATION.md perdeu a frase de fecho "
        "'To make any of these work…' que delimita a tabela — se o texto foi "
        "reescrito, atualize este parser junto"
    )
    table = automation[start:fim]
    return set(re.findall(r"^\| `([A-Za-z0-9_-]+)` \|", table, flags=re.MULTILINE))


def test_never_committed_skills_are_not_versioned() -> None:
    """Nenhuma skill pode ser "nunca commitada" e estar rastreada pelo Git.

    Fecha o furo achado em 2026-09-19: commitar uma skill hoje listada como host-only
    exigia atualizar a tabela de skills de projeto (o test_project_skill_table_matches_disk
    cobra), mas nada obrigava a tirá-la desta terceira tabela — e o
    test_skill_inventories_are_disjoint não a lê. O índice canônico passaria a afirmar
    as duas coisas ao mesmo tempo, com o CI verde.

    A tabela **pode** ficar vazia, e isso não é falha: versionar ou apagar as quatro
    skills que restam ali é o desfecho que o próprio `AUTOMATION.md` recomenda. Havia
    aqui um `assert declared` que derrubaria o CI exatamente nessa hora, obrigando a
    manter uma entrada fictícia ou uma seção morta. O que este teste garante é a
    **interseção** vazia; quem cobra a existência da tabela de skills versionadas é o
    `test_project_skill_table_matches_disk`, que lê o índice e não some com a lista.
    """
    declared = _never_committed_skills()
    contradiction = declared & _versioned_skills()
    assert not contradiction, (
        f"skills declaradas \"nunca commitadas\" mas rastreadas pelo Git: "
        f"{sorted(contradiction)} — ao versionar uma delas, tire a linha da tabela "
        f"host-only de .claude/AUTOMATION.md e acrescente-a à tabela de skills de projeto"
    )


def test_skill_inventories_are_disjoint() -> None:
    """Nenhuma skill pode ser declarada sincronizada **e** host-only.

    Fecha a divergência achada em 2026-09-19: a linha de defaults listava 15 nomes
    como sincronizados quando 12 deles não estavam no conjunto da conta, e um
    (`AutoResearchClaw`) já aparecia como host-only em outro doc.

    Como no teste acima, qualquer um dos dois inventários pode legitimamente esvaziar —
    uma categoria que deixa de existir não é drift. A asserção é sobre a interseção.

    E o bloco host-only é confrontado também com o **índice**. Sem isso, versionar uma
    skill dali (`compilar-tese`, digamos) e acrescentá-la à tabela de projeto passava em
    tudo: o `test_never_committed_skills_are_not_versioned` lê a *terceira* tabela, não
    esta, e o índice canônico ficava declarando a mesma skill portável e exclusiva do
    Mac ao mesmo tempo. É o furo que a rodada 17 fechou, na tabela vizinha.
    """
    synced, host_only = _skill_inventories()
    both = synced & host_only
    assert not both, (
        f"skills declaradas como sincronizadas **e** host-only: {sorted(both)} — "
        f"decida qual conjunto vale e remova do outro, em .claude/AUTOMATION.md"
    )

    versionadas = host_only & _versioned_skills()
    assert not versionadas, (
        f"skills declaradas host-only mas rastreadas pelo Git: {sorted(versionadas)} — "
        f"uma skill versionada viaja com o clone e deixou de ser exclusiva do Mac; "
        f"tire-a do bloco host-only de .claude/AUTOMATION.md"
    )


def test_retired_vocabulary_is_coherent() -> None:
    """O vocabulário aposentado precisa ser disjunto do atual — e de fato aposentado.

    `_RETIRED_ROOTS` existe para que uma superfície removida continue sendo reconhecida
    como caminho, e não para duplicar a lista corrente: um nome nos dois conjuntos
    contradiria a tabela canônica, e um nome aposentado que ainda está rastreado
    significa que a remoção não aconteceu.
    """
    overlap_dirs = _RETIRED_ROOTS & _VERSIONED_ROOTS
    assert not overlap_dirs, (
        f"raízes declaradas aposentadas **e** versionadas: {sorted(overlap_dirs)} — "
        f"ao aposentar uma superfície, mova o nome; não o copie"
    )
    overlap_files = _RETIRED_ROOT_FILES & _VERSIONED_ROOT_FILES
    assert not overlap_files, (
        f"arquivos declarados aposentados **e** versionados: {sorted(overlap_files)}"
    )

    # Pelo índice, não pelo disco: no Mac uma raiz aposentada pode continuar em disco
    # como diretório ignorado ou host-only, e `Path.exists()` a daria como ainda
    # versionada — o teste ficaria vermelho localmente e verde no clone limpo do CI.
    tracked_dirs, tracked_files = _tracked_top_level()
    still_tracked = (_RETIRED_ROOTS | _RETIRED_ROOT_FILES) & (tracked_dirs | tracked_files)
    assert not still_tracked, (
        f"declarados aposentados mas ainda presentes no repo: {sorted(still_tracked)} — "
        f"devolva-os a _VERSIONED_ROOTS/_VERSIONED_ROOT_FILES e à tabela canônica"
    )
