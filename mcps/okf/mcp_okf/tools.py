"""Tools do mcp-okf: indexação, busca, leitura e exportação HTML."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from . import bundle, store
from .server import tool

# shortcut: orçamento fixo por chamada; tornar parâmetro se algum cliente tiver timeout menor que ~60 s
TIME_BUDGET = 40
SNIPPET_MAX = 800
REPORT = "okf.html"


@tool
def okf_index(root: str, limit: int = 200, force: bool = False) -> dict:
    """Indexa o bundle OKF em `root` (caminho absoluto): lê todos os .md, recalcula os links entre documentos, remove
    do índice os arquivos apagados e (re)indexa até `limit` documentos novos ou alterados (sha256 diferente),
    parando em ~40 s para responder antes do timeout do cliente. Chame até `restantes` = 0. `force=True` (só na 1ª
    chamada) marca tudo para reindexar. Devolve {documentos, indexados, removidos, restantes}."""
    rd = bundle.root(root)
    docs = bundle.scan(rd)
    ids = bundle.by_id(docs)
    with store.connect(rd) as con:
        if force:
            con.execute("update docs set hash = ''")  # continua buscável enquanto reindexa
        indexed = dict(con.execute("select path, hash from docs"))
        removed = [p for p in indexed if p not in docs]
        for p in removed:
            store.delete_doc(con, p)
        store.set_links(con, {p: bundle.links(d, docs, ids) for p, d in docs.items()})
        con.commit()
        pending = [p for p, d in docs.items() if indexed.get(p) != d["hash"]]
        done, deadline = 0, time.monotonic() + TIME_BUDGET
        for p in pending[:limit]:
            if time.monotonic() > deadline:
                break
            store.write_doc(con, docs[p])
            con.commit()  # por documento: reinício do MCP no meio do lote não perde o progresso
            done += 1
    return {"documentos": len(docs), "indexados": done, "removidos": len(removed), "restantes": len(pending) - done}


@tool
def okf_search(root: str, query: str, limit: int = 8, folder: str | None = None, type: str | None = None) -> list:
    """Busca semântica + palavra-chave (híbrida) no bundle indexado, em linguagem natural. Filtros opcionais: `folder`
    (primeira pasta do path) e `type` (tipo do frontmatter). Devolve até `limit` documentos, do mais relevante:
    [{path, id, title, type, folder, score, trechos: [{section, text}]}]. Leia o documento inteiro com
    okf_get_document quando o trecho não bastar."""
    if not query.strip():
        raise ValueError("query vazia")
    limit = max(1, limit)
    with store.connect(bundle.root(root)) as con:
        hits = store.search(con, query, limit * 5, folder, type)
    out: dict[str, dict] = {}
    for h in hits:
        r = out.get(h["path"])
        if r is None:
            if len(out) >= limit:
                continue
            r = out[h["path"]] = {k: h[k] for k in ("path", "id", "title", "type", "folder")}
            r.update(score=round(h["score"], 4), trechos=[])
        if len(r["trechos"]) < 2:
            r["trechos"].append({"section": h["section"], "text": h["text"].split("\n", 1)[-1][:SNIPPET_MAX]})
    return list(out.values())


@tool
def okf_list_documents(root: str, folder: str | None = None, type: str | None = None) -> list:
    """Inventário do bundle (sem corpo): [{path, id, title, type, folder, description, indexado}]."""
    rd = bundle.root(root)
    with store.connect(rd) as con:
        indexed = dict(con.execute("select path, hash from docs"))
    return [{"path": p, "id": d["id"], "title": d["title"], "type": d["type"], "folder": d["folder"],
             "description": d["description"], "indexado": indexed.get(p) == d["hash"]}
            for p, d in bundle.scan(rd).items()
            if (not folder or d["folder"] == folder) and (not type or d["type"] == type)]


@tool
def okf_get_document(root: str, ref: str) -> dict:
    """Documento indexado por path (relativo ao root) ou id: {path, markdown (arquivo inteiro), links: {saida,
    entrada}}. saida/entrada = [{rel, path, id, title}] (rel = nome do link no DOORS Next ou 'cita' para link no
    texto)."""
    rd = bundle.root(root)
    with store.connect(rd) as con:
        row = con.execute("select path from docs where path = ? or id = ? order by path = ? desc limit 1",
                          (ref, str(ref), ref)).fetchone()
        if row is None:
            raise LookupError(f"documento não encontrado no índice: {ref} (rode okf_index)")
        path = row[0]

        def links(sql: str) -> list[dict]:
            return [dict(zip(("rel", "path", "id", "title"), r)) for r in con.execute(sql, (path,))]
        saida = links("select l.rel, l.dst, d.id, d.title from links l left join docs d on d.path = l.dst "
                      "where l.src = ? order by l.rowid")
        entrada = links("select l.rel, l.src, d.id, d.title from links l left join docs d on d.path = l.src "
                        "where l.dst = ? order by l.rowid")
    with open(os.path.join(rd, *path.split("/")), encoding="utf-8") as f:
        markdown = f.read()
    return {"path": path, "markdown": markdown, "links": {"saida": saida, "entrada": entrada}}


@tool
def okf_export_html(root: str) -> dict:
    """Grava `<root>/okf.html`: página para abrir no navegador com o grafo 3D de links entre os documentos do bundle
    (cor por pasta, tamanho pelo número de links), lista filtrável por texto, pasta e tipo, e cada documento
    renderizado (markdown formatado, links internos navegáveis, links de saída e de entrada). Não depende do índice.
    Devolve {arquivo, documentos, links}."""
    rd = bundle.root(root)
    docs = bundle.scan(rd)
    if not docs:
        raise LookupError(f"nenhum documento .md em {root}")
    ids = bundle.by_id(docs)
    links = [{"from": p, "to": l["path"], "rel": l["rel"]} for p, d in docs.items() for l in bundle.links(d, docs, ids)]
    data = json.dumps({"bundle": os.path.basename(rd), "generated": time.strftime("%Y-%m-%d %H:%M"),
                       "docs": [{"path": p, "id": d["id"], "title": d["title"], "type": d["type"],
                                 "folder": d["folder"], "description": d["description"],
                                 "body": bundle.link_body(d, docs, ids)} for p, d in docs.items()],
                       "links": links}, ensure_ascii=False).replace("</", "<\\/")  # texto não fecha o <script>
    html = Path(__file__).with_name("report.html").read_text(encoding="utf-8").replace("__DATA__", data)
    target = os.path.join(rd, REPORT)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)
    return {"arquivo": target, "documentos": len(docs), "links": len(links)}
