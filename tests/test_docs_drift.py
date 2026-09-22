"""Guarda de drift dos documentos de governança.

O `AGENTS.md` já descreve o *Drift protocol* — a classe de bug dominante do
workspace é "config apontando para uma realidade que mudou". O detector citado
lá (`~/.hermes/skills/research/drift-detector/`) é 🖥️ host-only e não roda em
sessões remotas/web, então a política existia sem nenhuma aplicação dentro do
repo. Este arquivo é essa aplicação.

Verifica apenas afirmações **checáveis dentro deste repo**:

1. caminhos ancorados numa raiz conhecida (versionada ou aposentada) existem de fato,
   e link markdown resolve relativo ao próprio documento;
2. a tabela de skills de projeto bate com `.claude/skills/`;
3. as contagens declaradas de `cowork/` batem com o disco;
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

    O escape vale até o **próximo cabeçalho de qualquer nível**, não só até o
    próximo `##`. Antes, um `##` marcado host-only engolia também os `###` abaixo
    dele: o link do ADR em `README.md`, acrescentado pelo main sob a seção da tese,
    ficava sem verificação mesmo apontando para um caminho **deste** repo. Apagar o
    ADR deixaria o link quebrado e o CI verde.
    """
    section_escaped = False
    for lineno, line in enumerate((REPO_ROOT / doc).read_text(encoding="utf-8").splitlines(), 1):
        if _HEADING.match(line):
            section_escaped = _is_escaped(line)
        if section_escaped or _is_escaped(line):
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
            if is_link and token.startswith(("./", "../")):
                found.append((lineno, token, True))  # link relativo explícito: sempre checável
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
    """Todo caminho ancorado citado num doc de governança precisa existir.

    Link markdown resolve **só** relativo ao diretório do próprio documento, como o
    GitHub o resolve. Aceitar também a raiz deixaria `[texto](README.md)` dentro de
    `.claude/AUTOMATION.md` passar por causa do `README.md` da raiz, enquanto o link
    renderizado aponta para `.claude/README.md` e está quebrado. Token em crase é
    afirmação de caminho **da raiz** por construção (o filtro de raízes acima), então
    para ele a raiz é a referência correta.
    """
    relative = token.rstrip("/")
    doc_dir = (REPO_ROOT / doc).parent
    base = doc_dir if is_link else REPO_ROOT
    onde = f"link relativo a {base.relative_to(REPO_ROOT)}/" if is_link else "raiz do repo"
    resolved = (base / relative).exists()
    assert resolved, (
        f"{doc}:{lineno} cita `{token}`, que não existe ({onde}). "
        f"Atualize o doc com o valor real (Drift protocol, AGENTS.md); se a superfície "
        f"vive só no Mac, marque a linha (ou o cabeçalho da seção) como host-only, "
        f"ou anote com <!-- drift-pin: ... -->."
    )


def _tracked_top_level() -> tuple[set[str], set[str]]:
    """Diretórios e arquivos de topo **rastreados pelo Git**, não o que há em disco.

    O disco mente das duas direções nesta árvore: no Mac ele traz sub-repos irmãos e
    árvores ignoradas que o Git não rastreia, e no container remoto não traz o que só
    existe no Mac. Toda pergunta de "isto ainda é versionado?" se responde pelo índice —
    é a mesma lição que já obrigou `_versioned_skills()` a trocar `iterdir()` por
    `git ls-files`.
    """
    out = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    entries = [e for e in out.split("\0") if e]
    dirs = {Path(e).parts[0] for e in entries if len(Path(e).parts) > 1}
    files = {e for e in entries if len(Path(e).parts) == 1}
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

    for skill in sorted(on_disk):
        assert (REPO_ROOT / ".claude/skills" / skill / "SKILL.md").is_file(), (
            f"skill de projeto `{skill}` não tem SKILL.md"
        )


@pytest.mark.parametrize(
    ("doc", "pattern"),
    [("README.md", r"(\d+) definições de agentes \+ (\d+) integrações")],
    ids=["README:cowork-counts"],
)
def test_documented_counts_match(doc: str, pattern: str) -> None:
    """As contagens de `cowork/` afirmadas nos docs precisam bater com o disco.

    O número vem do **documento**, capturado pela regex, e não de uma constante no
    teste. Antes o `assert` comparava com um `(85, 12)` fixo: corrigir a contagem no
    README **e** no `pattern` ainda deixava o build vermelho, com uma mensagem que
    contradizia o arquivo que o leitor tinha aberto.

    A varredura de disco também roda aqui, no corpo, e não no `@parametrize`. Lá ela
    era executada em tempo de import, e um `cowork/integrations/` ausente derrubava a
    coleta do módulo inteiro — as outras ~145 asserções nunca chegavam a rodar.
    """
    text = (REPO_ROOT / doc).read_text(encoding="utf-8")
    declarado = re.search(pattern, text)
    assert declarado, f"{doc} perdeu a frase de contagem esperada"

    agentes = len(list((REPO_ROOT / "cowork/agents").rglob("*.md")))
    integracoes = len([p for p in (REPO_ROOT / "cowork/integrations").iterdir() if p.is_dir()])

    assert (int(declarado.group(1)), int(declarado.group(2))) == (agentes, integracoes), (
        f"{doc} declara {declarado.group(1)} agentes + {declarado.group(2)} integrações, "
        f"mas o disco tem {agentes} agentes + {integracoes} integrações"
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
    """
    declared = _never_committed_skills()
    assert declared, "a tabela de skills nunca commitadas ficou vazia"

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
    """
    synced, host_only = _skill_inventories()

    assert synced, "o inventário de skills sincronizadas ficou vazio"
    assert host_only, "o inventário de skills host-only ficou vazio"

    both = synced & host_only
    assert not both, (
        f"skills declaradas como sincronizadas **e** host-only: {sorted(both)} — "
        f"decida qual conjunto vale e remova do outro, em .claude/AUTOMATION.md"
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
