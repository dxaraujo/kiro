import os

import pytest

UC = "03-Casos de Uso/2010-uc-cadastrar-cliente.md"
RN = "03-Regras/2001-rn-validar-cpf-do-cliente.md"
LOGIN = "01-Requisitos/10-login-do-cliente.md"


def test_index_is_incremental(okf, root):
    assert okf.okf_index(root, limit=2) == {"documentos": 3, "indexados": 2, "removidos": 0, "restantes": 1}
    assert okf.okf_index(root)["indexados"] == 1
    assert okf.okf_index(root)["indexados"] == 0
    with open(os.path.join(root, RN), "a") as f:
        f.write("\nNovo parágrafo.\n")
    assert okf.okf_index(root)["indexados"] == 1
    os.remove(os.path.join(root, LOGIN))
    assert okf.okf_index(root)["removidos"] == 1
    assert {d["path"] for d in okf.okf_list_documents(root)} == {UC, RN}
    assert all(r["path"] != LOGIN for r in okf.okf_search(root, "login portal senha"))
    assert okf.okf_index(root, force=True)["indexados"] == 2


def test_force_keeps_search_while_reindexing(okf, root):
    okf.okf_index(root)
    assert okf.okf_index(root, limit=1, force=True)["restantes"] == 2
    assert okf.okf_search(root, "CPF")  # índice antigo continua respondendo
    assert okf.okf_index(root)["indexados"] == 2


def test_search_and_filters(okf, root):
    okf.okf_index(root)
    hits = okf.okf_search(root, "CPF dígitos verificadores módulo 11")
    assert hits[0]["path"] == RN and hits[0]["trechos"][0]["section"] == "Regra"
    assert hits[0]["trechos"][0]["text"].startswith("## Regra")  # sem o prefixo de contexto
    assert {h["folder"] for h in okf.okf_search(root, "CPF", folder="01-Requisitos")} == {"01-Requisitos"}
    assert okf.okf_search(root, "CPF", type="Caso de Uso")[0]["path"] == UC
    assert okf.okf_search(root, "verificador")[0]["path"] == RN  # FTS por prefixo e sem acento
    assert okf.okf_search(root, 'aspas " e OR') is not None  # sintaxe do FTS5 não vaza da query
    with pytest.raises(ValueError):
        okf.okf_search(root, "  ")


def test_get_document_with_links(okf, root):
    okf.okf_index(root)
    doc = okf.okf_get_document(root, "2001")
    assert doc["path"] == RN and doc["markdown"].startswith("---\ntype: Regra de Negócio")
    assert {(l["rel"], l["path"]) for l in doc["links"]["entrada"]} == {("cita", UC), ("cita", LOGIN)}
    assert doc["links"]["saida"] == []
    assert okf.okf_get_document(root, UC)["links"]["saida"][0] == {
        "rel": "Vincular A", "path": LOGIN, "id": "10", "title": "Login do cliente"}
    with pytest.raises(LookupError):
        okf.okf_get_document(root, "../../etc/passwd")


def test_export_html_renders_bundle(okf, root):
    with open(os.path.join(root, RN), "a") as f:
        f.write("\nTexto com </script><script>alert(1)</script>\n")
    assert okf.okf_export_html(root) == {"arquivo": os.path.join(os.path.realpath(root), "okf.html"),
                                         "documentos": 3, "links": 3}
    html = open(os.path.join(root, "okf.html"), encoding="utf-8").read()
    data = html.split('<script id="data" type="application/json">')[1].split("</script>")[0]
    assert '"rel": "Vincular A"' in data and "<\\/script><script>alert(1)<\\/script>" in data
    assert "(#doc=03-Regras/2001-rn-validar-cpf-do-cliente.md)" in data  # link interno navega no html
    assert "okf.html" not in {d["path"] for d in okf.okf_list_documents(root)}


def test_index_rebuilds_when_db_is_deleted(okf, root):
    from mcp_okf import store
    okf.okf_index(root)
    os.remove(store.db_file(os.path.realpath(root)))
    assert okf.okf_index(root)["indexados"] == 3
    assert okf.okf_search(root, "CPF dígitos verificadores")[0]["path"] == RN


def test_index_stops_at_time_budget(okf, root, monkeypatch):
    monkeypatch.setattr(okf, "TIME_BUDGET", -1)
    assert okf.okf_index(root)["restantes"] == 3


def test_two_connections_on_same_index(okf, root):
    """Dois processos do mcp-okf no mesmo bundle: WAL deixa um ler enquanto o outro grava."""
    from mcp_okf import store
    rd = os.path.realpath(root)
    with store.connect(rd) as a, store.connect(rd) as b:
        okf.okf_index(root)
        assert a.execute("select count(*) from docs").fetchone()[0] == 3
        assert b.execute("select count(*) from chunks").fetchone()[0] > 0
