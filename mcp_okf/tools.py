"""Tools do mcp-okf: indexação, enriquecimento (feito pela LLM do cliente), busca e leitura."""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import TypedDict

from . import bundle, store
from .server import tool

# shortcut: orçamento fixo por chamada; tornar parâmetro se algum cliente tiver timeout menor que ~60 s
TIME_BUDGET = 40
BODY_MAX = 4000  # corpo devolvido para enriquecer: a LLM do cliente lê tudo, então quanto menos, mais rápido
LINKS_MAX = 10
_LINK_TARGET = re.compile(r"\]\((?:<[^>]*>|[^)\s]*)\)")  # '[rótulo](alvo)' -> '[rótulo]': o alvo não ajuda a resumir
SNIPPET_MAX = 800
LIST_MAX, ITEM_MAX, SUMMARY_MAX = 30, 300, 2000
INSTRUCOES = (
    "Para todos os documentos do lote, chame UMA vez okf_save_enrichment com items=[{path, summary, keywords, "
    "entities, questions}], em PT-BR e curto: summary = 1-2 frases do que o documento define; keywords = até 8 termos "
    "de negócio e sinônimos que alguém usaria para procurá-lo (inclusive os que o texto não usa); entities = até 5 "
    "atores/sistemas/dados citados, ou []; questions = até 3 perguntas que ele responde. Use só o documento e os "
    "links; não invente. Não mostre o enriquecimento na conversa: grave e chame okf_enrich_next de novo até "
    "restantes = 0.")


class Enrichment(TypedDict):
    path: str
    summary: str
    keywords: list[str]
    entities: list[str]
    questions: list[str]


def _ref(entry: dict, path: str) -> dict:
    return {"path": path, "id": entry.get("id"), "title": entry.get("title")}


def _pending_enrichment(state: dict) -> list[str]:
    return [p for p, e in state.items() if store.indexed(e) and not store.enriched(e)]


@tool
def okf_index(root: str, limit: int = 200, force: bool = False) -> dict:
    """Indexa o bundle OKF em `root` (caminho absoluto): lê todos os .md, recalcula os links entre documentos, remove
    do índice os arquivos apagados e (re)indexa até `limit` documentos novos ou alterados (sha256 diferente) ou que
    faltam no índice, parando em ~40 s para responder antes do timeout do cliente. Chame até `restantes` = 0. `force=True` (só na 1ª chamada) reindexa tudo, mantendo o enriquecimento.
    Devolve {documentos, indexados, removidos, restantes, a_enriquecer}."""
    with store.LOCK:
        rd = bundle.root(root)
        docs = bundle.scan(rd)
        ids = bundle.by_id(docs)
        state = store.load_state(rd)
        removed = [p for p in state if p not in docs]
        for p in removed:
            store.delete_doc(rd, p)
            del state[p]
        in_index = store.indexed_paths(rd)  # o que o Qdrant tem de fato: estado e índice podem divergir
        for p, d in docs.items():
            e = state.setdefault(p, {})
            e.update(hash=d["hash"], id=d["id"], title=d["title"], type=d["type"], folder=d["folder"],
                     description=d["description"],
                     links=bundle.links(d, docs, ids))
            if force or p not in in_index:
                e.pop("indexed_hash", None)
        pending = [p for p in docs if not store.indexed(state[p])]
        done, deadline = 0, time.monotonic() + TIME_BUDGET
        store.save_state(rd, state)
        for p in pending[:limit]:
            if time.monotonic() > deadline:
                break
            store.write_doc(rd, docs[p], state[p].get("enrichment"))  # enriquecimento antigo vale até o novo
            state[p]["indexed_hash"] = docs[p]["hash"]
            store.save_state(rd, state)  # por documento: reinício do MCP no meio do lote não perde o progresso
            done += 1
        return {"documentos": len(docs), "indexados": done, "removidos": len(removed),
                "restantes": len(pending) - done, "a_enriquecer": len(_pending_enrichment(state))}


@tool
def okf_enrich_next(root: str, limit: int = 10) -> dict:
    """Próximos documentos indexados sem enriquecimento (ou alterados depois dele), para a LLM enriquecer e gravar
    com okf_save_enrichment. Devolve {restantes, instrucoes, documentos: [{path, type, title, body, links}]}; body sem
    o alvo dos links e cortado em 4 mil caracteres; links = ['rel: id — título']."""
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        pending = _pending_enrichment(state)
        out = []
        for p in pending[:max(1, limit)]:
            doc = bundle.load(rd, p)
            body = re.sub(r"\n\s*\n+", "\n\n", _LINK_TARGET.sub("]", doc["body"])).strip()
            if doc["description"] and doc["description"] not in body:
                body = f"{doc['description']}\n\n{body}"
            links = [(l["rel"], state.get(l["path"], {})) for l in state[p].get("links", [])]
            out.append({"path": p, "type": doc["type"], "title": f"{doc['id']} — {doc['title']}" if doc["id"]
                        else doc["title"], "body": body[:BODY_MAX],
                        "links": [f"{rel}: {e.get('id')} — {e.get('title')}" for rel, e in links[:LINKS_MAX]]})
        return {"restantes": len(pending), "instrucoes": INSTRUCOES, "documentos": out}


def _strings(item: dict, key: str) -> list[str]:
    value = item.get(key) or []
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ValueError(f"{item.get('path')}: {key} deve ser lista de textos")
    return [" ".join(x.split())[:ITEM_MAX] for x in value if x.strip()][:LIST_MAX]


@tool
def okf_save_enrichment(root: str, items: list[Enrichment]) -> dict:
    """Grava o enriquecimento gerado para os documentos de okf_enrich_next e reindexa o ponto de resumo de cada um.
    items = [{path, summary, keywords[], entities[], questions[]}]. Devolve {gravados, restantes}."""
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        valid = []
        for item in items:  # valida tudo antes de gravar qualquer coisa
            if not isinstance(item, dict) or item.get("path") not in state:
                path = item.get("path") if isinstance(item, dict) else item
                raise ValueError(f"path fora do índice (rode okf_index): {path}")
            summary = item.get("summary")
            if not isinstance(summary, str) or not summary.strip():
                raise ValueError(f"{item['path']}: summary obrigatório")
            valid.append((item["path"], {"summary": " ".join(summary.split())[:SUMMARY_MAX],
                                         **{k: _strings(item, k) for k in ("keywords", "entities", "questions")}}))
        for path, enrichment in valid:
            doc = bundle.load(rd, path)
            entry = state[path]
            entry["enrichment"] = {**enrichment, "hash": doc["hash"], "at": store.now()}
            if store.indexed(entry) and entry["hash"] == doc["hash"]:
                store.write_doc_point(rd, doc, entry["enrichment"])
        store.save_state(rd, state)
        return {"gravados": len(valid), "restantes": len(_pending_enrichment(state))}


@tool
def okf_search(root: str, query: str, limit: int = 8, folder: str | None = None, type: str | None = None) -> list:
    """Busca semântica + palavra-chave (híbrida) no bundle indexado, em linguagem natural. Filtros opcionais: `folder`
    (primeira pasta do path) e `type` (tipo do frontmatter). Devolve até `limit` documentos, do mais relevante:
    [{path, id, title, type, folder, score, summary, trechos: [{section, text}]}]. Leia o documento inteiro com
    okf_get_document quando o trecho não bastar."""
    if not query.strip():
        raise ValueError("query vazia")
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        out: dict[str, dict] = {}
        for hit in store.search(rd, query, max(1, limit), folder, type):
            p = hit.payload
            r = out.get(p["path"])
            if r is None:
                if len(out) >= limit:
                    continue
                r = out[p["path"]] = {
                    "path": p["path"], "id": p["id"], "title": p["title"], "type": p["type"], "folder": p["folder"],
                    "score": round(hit.score, 4),
                    "summary": state.get(p["path"], {}).get("enrichment", {}).get("summary"), "trechos": []}
            if p["kind"] == "chunk" and len(r["trechos"]) < 2:
                r["trechos"].append({"section": p["section"], "text": p["text"][:SNIPPET_MAX]})
        return list(out.values())


@tool
def okf_list_documents(root: str, folder: str | None = None, type: str | None = None) -> list:
    """Inventário do bundle (sem corpo): [{path, id, title, type, folder, description, indexado, enriquecido}]."""
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        out = []
        for p, d in bundle.scan(rd).items():
            if (folder and d["folder"] != folder) or (type and d["type"] != type):
                continue
            e = {**state.get(p, {}), "hash": d["hash"]}  # compara com o arquivo de agora
            out.append({"path": p, "id": d["id"], "title": d["title"], "type": d["type"], "folder": d["folder"],
                        "description": d["description"], "indexado": store.indexed(e),
                        "enriquecido": store.enriched(e)})
        return out


@tool
def okf_get_document(root: str, ref: str) -> dict:
    """Documento por path (relativo ao root) ou id: {path, markdown (arquivo inteiro), enrichment, links: {saida,
    entrada, similares}}. saida/entrada = [{rel, path, id, title}] (rel = nome do link no DOORS Next ou 'cita' para
    link no texto); similares = documentos mais próximos semanticamente [{path, id, title, score}]."""
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        path = ref if ref in state else next((p for p, e in state.items() if e.get("id") == str(ref)), None)
        if path is None:
            raise LookupError(f"documento não encontrado no índice: {ref} (rode okf_index)")
        with open(f"{rd}/{path}", encoding="utf-8") as f:
            markdown = f.read()
        entry = state[path]
        return {"path": path, "markdown": markdown, "enrichment": entry.get("enrichment"), "links": {
            "saida": [{"rel": l["rel"], **_ref(state.get(l["path"], {}), l["path"])} for l in entry.get("links", [])],
            "entrada": [{"rel": l["rel"], **_ref(e, p)} for p, e in state.items()
                        for l in e.get("links", []) if l["path"] == path],
            "similares": [{"path": h.payload["path"], "id": h.payload["id"], "title": h.payload["title"],
                           "score": round(h.score, 4)} for h in store.similar(rd, path, 5)]}}


REPORT = "okf.html"


@tool
def okf_export_html(root: str) -> dict:
    """Grava `<root>/okf.html`: página para abrir no navegador com o grafo de links entre os documentos indexados
    (cor por pasta; borda grossa = não enriquecido), lista filtrável por texto, pasta e tipo, e o detalhe de cada
    documento (resumo, palavras-chave, entidades, perguntas, links de saída e de entrada). Rode depois de okf_index
    (e do enriquecimento). Devolve {arquivo, documentos, enriquecidos, links}."""
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        docs = [{"path": p, "id": e.get("id"), "title": e.get("title") or p, "type": e.get("type"),
                 "folder": e.get("folder"), "description": e.get("description"),
                 "enrichment": {k: v for k, v in e.get("enrichment", {}).items() if k not in ("hash", "at")},
                 "enriched": store.enriched(e)} for p, e in sorted(state.items())]
        if not docs:
            raise LookupError(f"nenhum documento indexado em {root} (rode okf_index)")
        links = [{"from": p, "to": l["path"], "rel": l["rel"]} for p, e in sorted(state.items())
                 for l in e.get("links", []) if l["path"] in state]
        data = json.dumps({"bundle": os.path.basename(rd), "generated": store.now(), "docs": docs, "links": links},
                          ensure_ascii=False).replace("</", "<\\/")  # texto do documento não fecha o <script>
        html = Path(__file__).with_name("report.html").read_text(encoding="utf-8").replace("__DATA__", data)
        target = os.path.join(rd, REPORT)
        with open(target, "w", encoding="utf-8") as f:
            f.write(html)
        return {"arquivo": target, "documentos": len(docs), "enriquecidos": sum(d["enriched"] for d in docs),
                "links": len(links)}
