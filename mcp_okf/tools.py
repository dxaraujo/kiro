"""Tools do mcp-okf: indexação, enriquecimento (feito pela LLM do cliente), busca e leitura."""
from __future__ import annotations

from typing import TypedDict

from . import bundle, store
from .server import tool

BODY_MAX = 12000  # corpo devolvido para enriquecer: limita o contexto gasto por documento
SNIPPET_MAX = 800
LIST_MAX, ITEM_MAX, SUMMARY_MAX = 30, 300, 2000
INSTRUCOES = (
    "Para cada documento, gere em PT-BR e chame okf_save_enrichment com items=[{path, summary, keywords, entities, "
    "questions}]: summary = 2-3 frases do que o documento define; keywords = termos de negócio e sinônimos que uma "
    "pessoa usaria para procurá-lo (inclusive os que o texto não usa literalmente); entities = atores, sistemas, "
    "regras e dados citados; questions = 3-5 perguntas que o documento responde. Use só o que está no documento e "
    "nos links; não invente.")


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
    do índice os arquivos apagados e (re)indexa até `limit` documentos novos ou alterados (sha256 diferente).
    Chame até `restantes` = 0. `force=True` (só na 1ª chamada) reindexa tudo, mantendo o enriquecimento.
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
        for p, d in docs.items():
            e = state.setdefault(p, {})
            e.update(hash=d["hash"], id=d["id"], title=d["title"], type=d["type"], folder=d["folder"],
                     links=bundle.links(d, docs, ids))
            if force:
                e.pop("indexed_hash", None)
        pending = [p for p in docs if not store.indexed(state[p])]
        done = 0
        try:
            for p in pending[:limit]:
                store.write_doc(rd, docs[p], state[p].get("enrichment"))  # enriquecimento antigo vale até o novo
                state[p]["indexed_hash"] = docs[p]["hash"]
                done += 1
        finally:
            store.save_state(rd, state)  # progresso salvo mesmo se um documento falhar
        return {"documentos": len(docs), "indexados": done, "removidos": len(removed),
                "restantes": len(pending) - done, "a_enriquecer": len(_pending_enrichment(state))}


@tool
def okf_enrich_next(root: str, limit: int = 5) -> dict:
    """Próximos documentos indexados sem enriquecimento (ou alterados depois dele), para a LLM enriquecer e gravar
    com okf_save_enrichment. Devolve {restantes, instrucoes, documentos: [{path, id, type, title, body, links}]}."""
    with store.LOCK:
        rd = bundle.root(root)
        state = store.load_state(rd)
        pending = _pending_enrichment(state)
        out = []
        for p in pending[:max(1, limit)]:
            doc = bundle.load(rd, p)
            out.append({"path": p, "id": doc["id"], "type": doc["type"], "title": doc["title"],
                        "description": doc["description"], "body": doc["body"][:BODY_MAX],
                        "links": [{"rel": l["rel"], **_ref(state.get(l["path"], {}), l["path"])}
                                  for l in state[p].get("links", [])]})
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
