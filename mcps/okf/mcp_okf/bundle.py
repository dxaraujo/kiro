"""Leitura de um bundle OKF (alm-sync do mcp-alm): documentos, frontmatter, links entre eles e chunks.
Só disco e texto; o índice fica em store.py."""
from __future__ import annotations

import hashlib
import os
import posixpath
import re
from pathlib import Path
from urllib.parse import quote, unquote

import yaml
from markdown_it import MarkdownIt

RESERVED = {"index.md", "log.md"}  # reservados pelo OKF em qualquer pasta, não documentos
SKIP = {"sync.md"}  # relatório da alm-sync na raiz
CHUNK_MAX = 1500
_HEADING = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$", re.M)
_LEADING_ID = re.compile(r"(\d+)(?:[ _:-].*)?")
_LINK_ID = re.compile(r"\s*(\d+)\s*:")  # item de `links`: 'id: título'
_LINK = re.compile(r"\]\((?:<([^>]*)>|([^)\s]*))")  # '](alvo' ou '](<alvo>'
_MD = MarkdownIt()


def root(dest: str) -> str:
    """Raiz do bundle: `dest` tem de ser absoluto (o cwd do MCP não é o bundle)."""
    if not os.path.isabs(dest):
        raise ValueError(f"root precisa ser caminho absoluto: {dest}")
    path = os.path.realpath(dest)
    if not os.path.isdir(path):
        raise ValueError(f"pasta não encontrada: {dest}")
    return path


def read_document(text: str) -> tuple[dict, str]:
    """(frontmatter YAML completo, corpo). Sem cabeçalho ou YAML inválido: ({}, texto)."""
    if not text.startswith("---\n") or (end := text.find("\n---\n", 3)) < 0:
        return {}, text
    try:
        head = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}, text
    return (head, text[end + 5:]) if isinstance(head, dict) else ({}, text)


def _text(value) -> str | None:
    return " ".join(str(value).split()) if value not in (None, "") else None


def load(root_dir: str, path: str) -> dict:
    """Documento pelo caminho relativo (posix) ao root."""
    full = os.path.join(root_dir, *path.split("/"))
    with open(full, "rb") as f:
        raw = f.read()
    head, body = read_document(raw.decode("utf-8"))
    name = posixpath.basename(path)[:-3]
    m = _LEADING_ID.fullmatch(name)
    doc_id = head.get("id") if head.get("id") is not None else (m.group(1) if m else None)
    sources = head.get("sources") if isinstance(head.get("sources"), list) else []
    tags = head.get("tags") if isinstance(head.get("tags"), list) else []
    return {"path": path, "id": str(doc_id) if doc_id is not None else None,
            "title": _text(head.get("title")) or name, "type": _text(head.get("type")),
            "folder": path.split("/")[0] if "/" in path else "", "description": _text(head.get("description")),
            "tags": [str(t) for t in tags], "resource": _text(head.get("resource")),
            "last_modified": next((str(s["last_modified"]) for s in sources
                                   if isinstance(s, dict) and s.get("last_modified")), None),
            "head": head, "body": body, "hash": hashlib.sha256(raw).hexdigest()}


def scan(root_dir: str) -> dict[str, dict]:
    """Todos os .md do bundle (menos index.md/log.md de qualquer pasta e sync.md na raiz), por caminho relativo posix."""
    docs = {}
    for full in sorted(Path(root_dir).rglob("*.md")):
        rel = full.relative_to(root_dir).as_posix()
        if full.name in RESERVED or rel in SKIP or any(part.startswith(".") for part in full.relative_to(root_dir).parts):
            continue
        docs[rel] = load(root_dir, rel)
    return docs


def _targets(markdown: str) -> list[str]:
    """Alvos de link do corpo (markdown-it, inclusive '<alvo com espaço>')."""
    out = []
    for token in _MD.parse(markdown):
        for child in token.children or []:
            if child.type == "link_open" and (href := child.attrGet("href")):
                out.append(str(href))
    return out


def resolve(doc_path: str, target: str, by_id: dict[str, str], docs: dict) -> str | None:
    """Alvo de link -> caminho de documento do bundle; None se estiver fora dele."""
    target = unquote(target).split("#")[0].strip()
    if not target:
        return None
    if "/rm/resources/" in target:  # URL do ALM: só liga se o artefato estiver no bundle
        return next((p for p, d in docs.items() if d["resource"] == target.split("?")[0]), None)
    if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I):
        return None
    base = "" if target.startswith("/") else posixpath.dirname(doc_path)
    path = posixpath.normpath(posixpath.join(base, target.lstrip("/")))
    if path.startswith("..") or path.startswith("/"):
        return None  # fora do bundle
    if path in docs:
        return path
    m = _LEADING_ID.fullmatch(posixpath.basename(path).removesuffix(".md"))
    return by_id.get(m.group(1)) if m else None


def links(doc: dict, docs: dict, by_id: dict[str, str]) -> list[dict]:
    """[{rel, path}] sem repetição: do frontmatter `links {rel: ['id: título']}` e do corpo (rel 'cita')."""
    out: dict[tuple[str, str], dict] = {}
    raw = doc["head"].get("links")
    for rel, items in (raw.items() if isinstance(raw, dict) else []):
        for item in items if isinstance(items, list) else [items]:
            m = _LINK_ID.match(str(item))
            if m and (path := by_id.get(m.group(1))) and path != doc["path"]:
                out[(str(rel), path)] = {"rel": str(rel), "path": path}
    for target in _targets(doc["body"]):
        if (path := resolve(doc["path"], target, by_id, docs)) and path != doc["path"]:
            out.setdefault(("cita", path), {"rel": "cita", "path": path})
    return list(out.values())


def link_body(doc: dict, docs: dict, by_id: dict[str, str]) -> str:
    """Corpo com os links para documentos do bundle trocados por `#doc=<path>` (navegação dentro do okf.html)."""
    def repl(m: re.Match) -> str:
        path = resolve(doc["path"], m.group(1) if m.group(1) is not None else m.group(2), by_id, docs)
        return f"](#doc={quote(path)}" if path else m.group(0)
    return _LINK.sub(repl, doc["body"])


def by_id(docs: dict) -> dict[str, str]:
    return {d["id"]: p for p, d in docs.items() if d["id"]}


def _split(text: str) -> list[str]:
    """Quebra por parágrafo em pedaços de até CHUNK_MAX (parágrafo maior que isso vai inteiro)."""
    parts, cur = [], ""
    for para in re.split(r"\n\s*\n", text):
        if cur and len(cur) + len(para) > CHUNK_MAX:
            parts.append(cur)
            cur = ""
        cur = f"{cur}\n\n{para}" if cur else para
    return parts + ([cur] if cur.strip() else [])


def chunks(doc: dict) -> list[dict]:
    """[{section, text}] por heading (#..###); `text` já com o prefixo de contexto para o embedding."""
    body, sections = doc["body"], []
    marks = list(_HEADING.finditer(body))
    starts = [(0, "")] + [(m.start(), m.group(2)) for m in marks]
    for i, (start, title) in enumerate(starts):
        end = marks[i].start() if i < len(marks) else len(body)
        text = body[start:end].strip()
        if text:
            sections += [(title, part.strip()) for part in _split(text) if part.strip()]
    prefix = " ".join(filter(None, [doc["type"], doc["id"], "—", doc["title"]]))
    return [{"section": s, "text": f"{prefix} | {doc['folder']} | {s}\n{t}"} for s, t in sections] or \
        [{"section": "", "text": f"{prefix} | {doc['folder']}\n{doc['description'] or doc['title']}"}]
