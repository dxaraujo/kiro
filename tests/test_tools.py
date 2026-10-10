import os

import pytest

UC = "03-Casos de Uso/2010-uc-cadastrar-cliente.md"
RN = "03-Regras/2001-rn-validar-cpf-do-cliente.md"
LOGIN = "01-Requisitos/10-login-do-cliente.md"


def test_index_is_incremental(okf, root):
    assert okf.okf_index(root, limit=2) == {"documentos": 3, "indexados": 2, "removidos": 0, "restantes": 1,
                                            "a_enriquecer": 2}
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


def test_enrichment_round_trip(okf, root):
    okf.okf_index(root)
    batch = okf.okf_enrich_next(root, limit=1)
    assert batch["restantes"] == 3 and len(batch["documentos"]) == 1 and "summary" in batch["instrucoes"]
    uc = okf.okf_enrich_next(root, limit=5)["documentos"]
    doc = next(d for d in uc if d["path"] == UC)
    assert "Vincular A: 10 — Login do cliente" in doc["links"] and doc["title"] == "2010 — UC - Cadastrar cliente"
    assert "[2001 RN - Validar CPF do cliente]" in doc["body"] and "TX_2001" not in doc["body"]
    items = [{"path": d["path"], "summary": f"Resumo {d['title']}", "keywords": ["onboarding"], "entities": [],
              "questions": []} for d in uc]
    assert okf.okf_save_enrichment(root, items) == {"gravados": 3, "restantes": 0}
    assert okf.okf_enrich_next(root)["documentos"] == []
    assert okf.okf_index(root)["a_enriquecer"] == 0
    # keyword que só existe no enriquecimento já acha o documento
    assert okf.okf_search(root, "onboarding", limit=3)[0]["summary"].startswith("Resumo")
    with open(os.path.join(root, RN), "a") as f:
        f.write("\nMudou.\n")
    assert okf.okf_index(root)["a_enriquecer"] == 1


def test_save_enrichment_validates_before_writing(okf, root):
    okf.okf_index(root)
    ok = {"path": RN, "summary": "x", "keywords": [], "entities": [], "questions": []}
    with pytest.raises(ValueError):
        okf.okf_save_enrichment(root, [ok, {**ok, "path": "../fora.md"}])
    with pytest.raises(ValueError):
        okf.okf_save_enrichment(root, [{**ok, "keywords": "não é lista"}])
    assert okf.okf_enrich_next(root)["restantes"] == 3


def test_search_and_filters(okf, root):
    okf.okf_index(root)
    hits = okf.okf_search(root, "CPF dígitos verificadores módulo 11")
    assert hits[0]["path"] == RN and hits[0]["trechos"][0]["section"] == "Regra"
    assert {h["folder"] for h in okf.okf_search(root, "CPF", folder="01-Requisitos")} == {"01-Requisitos"}
    assert okf.okf_search(root, "CPF", type="Caso de Uso")[0]["path"] == UC


def test_get_document_links_backlinks_and_similar(okf, root):
    okf.okf_index(root)
    doc = okf.okf_get_document(root, "2001")
    assert doc["path"] == RN and doc["markdown"].startswith("---\ntype: Regra de Negócio")
    assert {(l["rel"], l["path"]) for l in doc["links"]["entrada"]} == {("cita", UC), ("cita", LOGIN)}
    assert doc["links"]["saida"] == []
    assert RN not in {s["path"] for s in doc["links"]["similares"]} and doc["links"]["similares"]
    assert okf.okf_get_document(root, UC)["links"]["saida"][0] == {
        "rel": "Vincular A", "path": LOGIN, "id": "10", "title": "Login do cliente"}
    with pytest.raises(LookupError):
        okf.okf_get_document(root, "../../etc/passwd")


def test_export_html_writes_report_in_bundle_root(okf, root):
    with pytest.raises(LookupError):
        okf.okf_export_html(root)
    with open(os.path.join(root, RN), "a") as f:
        f.write("\nTexto com </script><script>alert(1)</script>\n")
    okf.okf_index(root)
    okf.okf_save_enrichment(root, [{"path": RN, "summary": "Valida CPF </script>", "keywords": ["cpf"],
                                    "entities": [], "questions": []}])
    assert okf.okf_export_html(root) == {"arquivo": os.path.join(os.path.realpath(root), "okf.html"),
                                         "documentos": 3, "enriquecidos": 1, "links": 3}
    html = open(os.path.join(root, "okf.html"), encoding="utf-8").read()
    data = html.split('<script id="data" type="application/json">')[1].split("</script>")[0]
    assert '"rel": "Vincular A"' in data and "Valida CPF <\\/script>" in data
    assert "okf.html" not in {d["path"] for d in okf.okf_list_documents(root)}


def test_index_heals_points_missing_from_qdrant(okf, root):
    from mcp_okf import store
    okf.okf_index(root)
    store.delete_doc(os.path.realpath(root), RN)  # estado diz indexado, Qdrant não tem
    assert okf.okf_index(root)["indexados"] == 1
    assert okf.okf_search(root, "CPF dígitos verificadores")[0]["path"] == RN


def test_index_stops_at_time_budget(okf, root, monkeypatch):
    monkeypatch.setattr(okf, "TIME_BUDGET", -1)
    assert okf.okf_index(root)["restantes"] == 3
