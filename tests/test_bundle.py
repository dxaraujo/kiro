import os

import pytest

from mcp_okf import bundle

UC = "03-Casos de Uso/2010-uc-cadastrar-cliente.md"
RN = "03-Regras/2001-rn-validar-cpf-do-cliente.md"
LOGIN = "01-Requisitos/10-login-do-cliente.md"


def test_root_requires_absolute_existing_dir(root):
    with pytest.raises(ValueError):
        bundle.root("relativo/bundle")
    with pytest.raises(ValueError):
        bundle.root(os.path.join(root, "nao-existe"))


def test_scan_reads_nested_frontmatter_and_skips_bundle_files(root):
    docs = bundle.scan(root)
    assert set(docs) == {UC, RN, LOGIN}
    uc = docs[UC]
    assert (uc["id"], uc["type"], uc["folder"]) == ("2010", "Caso de Uso", "03-Casos de Uso")
    assert uc["head"]["links"] == {"Vincular A": ["10: Login do cliente", "9999: Fora do bundle"]}
    assert uc["last_modified"] == "2026-01-10T13:05:00Z"


def test_id_falls_back_to_file_name(root):
    with open(os.path.join(root, "01-Requisitos", "77-sem-cabecalho.md"), "w") as f:
        f.write("Texto sem frontmatter.\n")
    doc = bundle.load(root, "01-Requisitos/77-sem-cabecalho.md")
    assert (doc["id"], doc["title"], doc["head"]) == ("77", "77-sem-cabecalho", {})


def test_links_from_frontmatter_body_and_alm_url(root):
    docs = bundle.scan(root)
    ids = bundle.by_id(docs)
    assert bundle.links(docs[UC], docs, ids) == [{"rel": "Vincular A", "path": LOGIN}, {"rel": "cita", "path": RN}]
    assert bundle.links(docs[LOGIN], docs, ids) == [{"rel": "cita", "path": RN}]  # relativo '../03-Regras/...'


def test_resolve_ignores_targets_outside_bundle(root):
    docs = bundle.scan(root)
    assert bundle.resolve(UC, "../../segredo.md", {}, docs) is None
    assert bundle.resolve(UC, "https://example.com/x.md", {}, docs) is None


def test_chunks_by_heading_with_context_prefix(root):
    parts = bundle.chunks(bundle.scan(root)[RN])
    assert [c["section"] for c in parts] == ["Regra", "Mensagem"]
    assert parts[0]["text"].startswith("Regra de Negócio 2001 — RN - Validar CPF do cliente | 03-Regras | Regra\n")


def test_long_section_is_split_by_paragraph():
    body = "\n\n".join("p" * 900 for _ in range(3))
    doc = {"body": body, "type": None, "id": None, "title": "T", "folder": "", "description": None}
    assert len(bundle.chunks(doc)) == 3
