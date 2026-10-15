"""Índice do bundle: um SQLite por bundle em <home>/<sha1(root)>.db, com documentos, links, chunks (vetor denso
float32 normalizado) e FTS5 (BM25). Busca híbrida: cosseno por força bruta (numpy) + FTS5, fusão RRF.

SQLite em WAL: vários processos do mcp-okf podem abrir o mesmo índice. Nada é gravado no bundle."""
from __future__ import annotations

import contextlib
import functools
import hashlib
import os
import re
import sqlite3
import sys
from pathlib import Path

import numpy as np

from . import bundle

MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
RRF_K = 60
SCHEMA = """
create table if not exists docs(path text primary key, hash text, id text, title text, type text, folder text,
                                description text);
create index if not exists docs_id on docs(id);
create table if not exists links(src text, rel text, dst text);
create index if not exists links_src on links(src);
create index if not exists links_dst on links(dst);
create table if not exists chunks(cid integer primary key, path text, section text, text text, vec blob);
create index if not exists chunks_path on chunks(path);
create virtual table if not exists chunks_fts using fts5(text, tokenize='unicode61 remove_diacritics 2');
"""


def home() -> Path:
    if env := os.environ.get("MCP_OKF_HOME"):
        return Path(env)
    if sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "mcp-okf"
    return Path.home() / ".config" / "mcp-okf"


def db_file(root: str) -> Path:
    return home() / f"{hashlib.sha1(root.encode()).hexdigest()}.db"


@contextlib.contextmanager
def connect(root: str):
    """Conexão ao índice do bundle; commit ao sair sem erro."""
    path = db_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path, timeout=30)
    try:
        con.execute("pragma journal_mode=wal")
        con.executescript(SCHEMA)
        yield con
        con.commit()
    finally:
        con.close()


@functools.cache
def _model():
    from fastembed import TextEmbedding
    return TextEmbedding(MODEL)


def embed(texts: list[str]) -> np.ndarray:
    """(n, dim) float32 com norma 1: produto escalar = cosseno."""
    v = np.array(list(_model().embed(texts)), dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True).clip(1e-9)


def delete_doc(con: sqlite3.Connection, path: str) -> None:
    con.execute("delete from chunks_fts where rowid in (select cid from chunks where path = ?)", (path,))
    con.execute("delete from chunks where path = ?", (path,))
    con.execute("delete from docs where path = ?", (path,))


def write_doc(con: sqlite3.Connection, doc: dict) -> None:
    """Troca os chunks do documento e grava a linha em `docs` (com o hash: marca como indexado)."""
    parts = bundle.chunks(doc)
    vecs = embed([c["text"] for c in parts])  # antes de apagar: falha no modelo não deixa o documento sem chunks
    delete_doc(con, doc["path"])
    con.execute("insert into docs values (?, ?, ?, ?, ?, ?, ?)", tuple(doc[k] for k in (
        "path", "hash", "id", "title", "type", "folder", "description")))
    for c, v in zip(parts, vecs):
        cid = con.execute("insert into chunks(path, section, text, vec) values (?, ?, ?, ?)",
                          (doc["path"], c["section"], c["text"], v.tobytes())).lastrowid
        con.execute("insert into chunks_fts(rowid, text) values (?, ?)", (cid, c["text"]))


def set_links(con: sqlite3.Connection, links: dict[str, list[dict]]) -> None:
    con.execute("delete from links")
    con.executemany("insert into links values (?, ?, ?)",
                    [(src, l["rel"], l["path"]) for src, ls in links.items() for l in ls])


def search(con: sqlite3.Connection, query: str, wide: int, folder: str | None, type_: str | None) -> list[dict]:
    """Até `wide` chunks, do mais relevante: [{path, section, text, id, title, type, folder, score}]."""
    where, args = "1 = 1", []
    for col, value in (("folder", folder), ("type", type_)):
        if value is not None:
            where += f" and d.{col} = ?"
            args.append(value)
    # shortcut: vetores lidos a cada consulta; cachear a matriz se o bundle passar de ~50k chunks
    rows = con.execute(f"select c.cid, c.vec from chunks c join docs d on d.path = c.path where {where}",
                       args).fetchall()
    dense = []
    if rows:
        scores = np.frombuffer(b"".join(r[1] for r in rows), dtype=np.float32).reshape(len(rows), -1) \
            @ embed([query])[0]
        dense = [rows[i][0] for i in np.argsort(-scores)[:wide]]
    # shortcut: FTS5 sem stemming PT (prefixo * cobre plurais); tokenizer próprio se o recall lexical cair
    terms = re.findall(r"\w+", query)
    lexical = [r[0] for r in con.execute(
        f"select f.rowid from chunks_fts f join chunks c on c.cid = f.rowid join docs d on d.path = c.path "
        f"where chunks_fts match ? and {where} order by bm25(chunks_fts) limit ?",
        [" OR ".join(f'"{t}"*' for t in terms), *args, wide])] if terms else []
    rrf: dict[int, float] = {}
    for ranking in (dense, lexical):
        for rank, cid in enumerate(ranking):
            rrf[cid] = rrf.get(cid, 0) + 1 / (RRF_K + rank + 1)
    best = sorted(rrf, key=rrf.get, reverse=True)[:wide]
    found = {r[0]: r for r in con.execute(
        f"select c.cid, c.path, c.section, c.text, d.id, d.title, d.type, d.folder from chunks c "
        f"join docs d on d.path = c.path where c.cid in ({','.join('?' * len(best))})", best)}
    return [dict(zip(("path", "section", "text", "id", "title", "type", "folder"), found[cid][1:]),
                 score=rrf[cid]) for cid in best]
