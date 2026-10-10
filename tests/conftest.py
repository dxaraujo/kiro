"""Bundle de exemplo copiado para tmp, Qdrant em memória e embeddings falsos (sem baixar modelo)."""
import re
import zlib

import pytest
from qdrant_client import QdrantClient, models

from mcp_okf import store

# bundle OKF no formato da alm-sync: {caminho relativo: conteúdo}
BUNDLE = {
    '01-Requisitos/10-login-do-cliente.md': '---\ntype: Requisito\ntitle: Login do cliente\ndescription: "Acesso ao portal com CPF e senha."\nresource: "https://alm.example.com/rm/resources/TX_10"\ntags:\n  - "01-Requisitos"\nsources:\n  - id: doors-next\n    resource: "https://alm.example.com/rm/resources/TX_10"\n    last_modified: "2026-01-10T13:05:00Z"\nid: 10\n---\nO cliente acessa o portal informando CPF e senha. O CPF é validado conforme [2001 RN - Validar CPF do cliente](../03-Regras/2001-rn-validar-cpf-do-cliente.md).\n',
    '03-Casos de Uso/2010-uc-cadastrar-cliente.md': '---\ntype: Caso de Uso\ntitle: UC - Cadastrar cliente\nresource: "https://alm.example.com/rm/resources/TX_2010"\ntags:\n  - "03-Casos de Uso"\nsources:\n  - id: doors-next\n    resource: "https://alm.example.com/rm/resources/TX_2010"\n    author: "human:ana.souza"\n    last_modified: "2026-01-10T13:05:00Z"\ngenerated:\n  by: "process:alm-mcp/1.0.14"\n  at: "2026-01-11T19:20:00Z"\nid: 2010\nlinks:\n  Vincular A:\n    - "10: Login do cliente"\n    - "9999: Fora do bundle"\n---\n## Fluxo Básico\n\n1. O usuário informa os dados do cliente.\n2. O sistema valida o documento: [2001 RN - Validar CPF do cliente](https://alm.example.com/rm/resources/TX_2001)\n3. Ver também [manual](https://example.com/manual.pdf) e [fora](../../segredo.md).\n',
    '03-Regras/2001-rn-validar-cpf-do-cliente.md': '---\ntype: Regra de Negócio\ntitle: RN - Validar CPF do cliente\nresource: "https://alm.example.com/rm/resources/TX_2001"\ntags:\n  - "03-Regras"\nid: 2001\n---\n## Regra\n\nO CPF deve ter 11 dígitos e dígitos verificadores válidos (módulo 11). CPFs com todos os dígitos iguais são rejeitados.\n\n## Mensagem\n\nExibir "CPF inválido" e bloquear o envio do formulário.\n',
    'index.md': '---\nokf_version: "0.2"\n---\n\n# 01-Requisitos\n\n* [10 — Login do cliente](</01-Requisitos/10-login-do-cliente.md>) - Acesso ao portal com CPF e senha.\n\n# 03-Casos de Uso\n\n* [2010 — UC - Cadastrar cliente](</03-Casos de Uso/2010-uc-cadastrar-cliente.md>)\n\n# 03-Regras\n\n* [2001 — RN - Validar CPF do cliente](</03-Regras/2001-rn-validar-cpf-do-cliente.md>)\n\n# Bundle\n\n* [Sincronismo ALM → OKF](/sync.md) - Situação de cada artefato do DOORS Next baixado neste bundle.\n',
    'sync.md': '---\ntype: Relatório de Sincronismo\ntitle: Sincronismo ALM → OKF\n---\n| Artefato | Pasta | Última atualização ALM | Hash | Status |\n|---|---|---|---|---|\n',
}


def _words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def fake_dense(texts):
    out = []
    for t in texts:
        v = [0.0] * store.DENSE_DIM
        for w in _words(t):
            v[zlib.crc32(w.encode()) % store.DENSE_DIM] += 1.0
        out.append(v if any(v) else [1.0] + [0.0] * (store.DENSE_DIM - 1))
    return out


def fake_sparse(texts, query=False):
    out = []
    for t in texts:
        idx = sorted({zlib.crc32(w.encode()) % 100_000 for w in _words(t)})
        out.append(models.SparseVector(indices=idx, values=[1.0] * len(idx)))
    return out


@pytest.fixture
def root(tmp_path):
    dest = tmp_path / "bundle"
    for rel, text in BUNDLE.items():
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_text(text, encoding="utf-8")
    return str(dest)


REAL_CLIENT = store.client  # Qdrant em disco, antes do monkeypatch


@pytest.fixture
def okf(tmp_path, monkeypatch):
    monkeypatch.setenv("MCP_OKF_HOME", str(tmp_path / "home"))
    qc = QdrantClient(":memory:")
    store._ensure(qc)
    monkeypatch.setattr(store, "client", lambda: qc)
    monkeypatch.setattr(store, "embed_dense", fake_dense)
    monkeypatch.setattr(store, "embed_sparse", fake_sparse)
    from mcp_okf import tools
    return tools
