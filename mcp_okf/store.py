"""Índice do bundle: Qdrant local (vetor denso + BM25, fusão RRF) e o estado por bundle (hash, links, enriquecimento).

Estado em <home>/state/<sha1(root)>.json: {path: {hash, indexed_hash, links: [{rel, path}], enrichment}}.
É o que torna a indexação incremental e mantém o enriquecimento entre reindexações. Nada é gravado no bundle."""
from __future__ import annotations

import functools
import hashlib
import json
import os
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from qdrant_client import QdrantClient, models

from . import bundle

COLLECTION = "okf"
DENSE_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
DENSE_DIM = 768
SPARSE_MODEL = "Qdrant/bm25"
_NS = uuid.UUID("5b0f0c6e-2a51-4f43-9d55-0c2c7f1e9a10")
# um lock para tudo: tools síncronas podem rodar em threads e o estado é um JSON
LOCK = threading.RLock()


def home() -> Path:
    if env := os.environ.get("MCP_OKF_HOME"):
        return Path(env)
    if sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "mcp-okf"
    return Path.home() / ".config" / "mcp-okf"


@functools.cache
def client() -> QdrantClient:
    """Qdrant em modo local (a pasta fica travada para um processo só)."""
    path = home() / "qdrant"
    path.mkdir(parents=True, exist_ok=True)
    try:
        qc = QdrantClient(path=str(path))
    except RuntimeError as exc:
        raise RuntimeError(f"Índice em {path} já está aberto por outro processo do mcp-okf: {exc}") from exc
    _ensure(qc)
    return qc


def _ensure(qc: QdrantClient) -> None:
    if qc.collection_exists(COLLECTION):
        return
    qc.create_collection(
        COLLECTION,
        vectors_config={"dense": models.VectorParams(size=DENSE_DIM, distance=models.Distance.COSINE)},
        sparse_vectors_config={"bm25": models.SparseVectorParams(modifier=models.Modifier.IDF)})
    # shortcut: sem índices de payload (o Qdrant local os ignora); criar em bundle/path/folder/type/kind ao migrar
    # para servidor Qdrant


@functools.cache
def _dense():
    from fastembed import TextEmbedding
    return TextEmbedding(DENSE_MODEL)


@functools.cache
def _sparse():
    from fastembed import SparseTextEmbedding
    return SparseTextEmbedding(SPARSE_MODEL, language="portuguese")


def embed_dense(texts: list[str]) -> list[list[float]]:
    return [v.tolist() for v in _dense().embed(texts)]


def embed_sparse(texts: list[str], query: bool = False) -> list[models.SparseVector]:
    fn = _sparse().query_embed if query else _sparse().embed
    return [models.SparseVector(indices=e.indices.tolist(), values=e.values.tolist()) for e in fn(texts)]


# --- estado

def _state_file(root: str) -> Path:
    return home() / "state" / f"{hashlib.sha1(root.encode()).hexdigest()}.json"


def load_state(root: str) -> dict:
    try:
        return json.loads(_state_file(root).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}


def save_state(root: str, state: dict) -> None:
    path = _state_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)  # atômico: estado nunca fica pela metade


def enriched(entry: dict) -> bool:
    return entry.get("enrichment", {}).get("hash") == entry.get("hash")


def indexed(entry: dict) -> bool:
    return entry.get("indexed_hash") == entry.get("hash")


# --- pontos

def _pid(root: str, path: str, n) -> str:
    return str(uuid.uuid5(_NS, f"{root}\n{path}\n{n}"))


def _filter(root: str, **eq) -> models.Filter:
    return models.Filter(must=[models.FieldCondition(key=k, match=models.MatchValue(value=v))
                               for k, v in {"bundle": root, **eq}.items() if v is not None])


def _payload(root: str, doc: dict, kind: str, section: str = "", text: str = "") -> dict:
    return {"bundle": root, "path": doc["path"], "id": doc["id"], "title": doc["title"], "type": doc["type"],
            "folder": doc["folder"], "kind": kind, "section": section, "text": text}


def doc_text(doc: dict, enrichment: dict | None) -> str:
    """Texto do ponto 'doc': cabeçalho + enriquecimento (é ele que casa pergunta em linguagem natural com jargão)."""
    e = enrichment or {}
    parts = [" ".join(filter(None, [doc["type"], doc["id"], "—", doc["title"]])), doc["folder"],
             doc["description"], e.get("summary"), ", ".join(e.get("keywords", [])),
             ", ".join(e.get("entities", [])), "\n".join(e.get("questions", []))]
    return "\n".join(p for p in parts if p)


def _doc_point(root: str, doc: dict, enrichment: dict | None) -> models.PointStruct:
    text = doc_text(doc, enrichment)
    return models.PointStruct(id=_pid(root, doc["path"], "doc"),
                               vector={"dense": embed_dense([text])[0], "bm25": embed_sparse([text])[0]},
                               payload=_payload(root, doc, "doc", text=(enrichment or {}).get("summary") or ""))


def _delete(root: str, path: str) -> None:
    client().delete(COLLECTION, points_selector=models.FilterSelector(filter=_filter(root, path=path)))


def write_doc(root: str, doc: dict, enrichment: dict | None) -> None:
    """Apaga os pontos do documento e grava os chunks + o ponto 'doc'."""
    parts = bundle.chunks(doc)
    texts = [c["text"] for c in parts]
    dense, sparse = embed_dense(texts), embed_sparse(texts)
    points = [models.PointStruct(id=_pid(root, doc["path"], n), vector={"dense": d, "bm25": s},
                                 payload=_payload(root, doc, "chunk", c["section"], c["text"].split("\n", 1)[-1]))
              for n, (c, d, s) in enumerate(zip(parts, dense, sparse))]
    _delete(root, doc["path"])
    client().upsert(COLLECTION, points + [_doc_point(root, doc, enrichment)])


def write_doc_point(root: str, doc: dict, enrichment: dict | None) -> None:
    client().upsert(COLLECTION, [_doc_point(root, doc, enrichment)])


def delete_doc(root: str, path: str) -> None:
    _delete(root, path)


def search(root: str, query: str, limit: int, folder: str | None, type_: str | None) -> list[models.ScoredPoint]:
    flt = _filter(root, folder=folder, type=type_)
    wide = limit * 5
    return client().query_points(
        COLLECTION,
        prefetch=[models.Prefetch(query=embed_dense([query])[0], using="dense", filter=flt, limit=wide),
                  models.Prefetch(query=embed_sparse([query], query=True)[0], using="bm25", filter=flt, limit=wide)],
        query=models.FusionQuery(fusion=models.Fusion.RRF), limit=wide, with_payload=True).points


def similar(root: str, path: str, limit: int) -> list[models.ScoredPoint]:
    """Documentos mais próximos pelo vetor do ponto 'doc' (vazio se o documento não estiver indexado)."""
    found = client().retrieve(COLLECTION, [_pid(root, path, "doc")], with_vectors=["dense"])
    if not found:
        return []
    flt = _filter(root, kind="doc")
    flt.must_not = [models.FieldCondition(key="path", match=models.MatchValue(value=path))]
    return client().query_points(COLLECTION, query=found[0].vector["dense"], using="dense", query_filter=flt,
                                 limit=limit, with_payload=True).points


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
