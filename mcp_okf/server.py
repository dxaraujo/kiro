"""Servidor MCP de base de conhecimento sobre bundles OKF (alm-sync do mcp-alm).

As tools ficam em tools.py, registradas com `@tool`; leitura do bundle em bundle.py e índice em store.py.
"""
from __future__ import annotations

import functools

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer(
    "okf",
    instructions=(
        "Base de conhecimento sobre um bundle OKF (pasta com index.md e um .md por documento, como o gerado pela "
        "alm-sync). `root` é sempre o caminho absoluto da pasta. Preparar: okf_index até restantes=0; depois "
        "okf_enrich_next -> gere o enriquecimento de cada documento -> okf_save_enrichment, até restantes=0. "
        "Consultar: okf_search (pergunta em linguagem natural), okf_get_document (documento inteiro + links de "
        "saída, de entrada e similares), okf_list_documents (inventário). A busca funciona sem enriquecimento, mas "
        "fica melhor com ele. Cite os documentos pelo path/id."
    ),
)



def tool(fn):
    """Registra `fn` como tool e devolve `fn` intacta (testes veem as exceções originais).

    O MCP SDK 2.x esconde o texto de exceções que não são ToolError ("Error executing tool"); aqui toda falha vira
    ToolError com tipo e mensagem, para o cliente (e quem lê o log dele) ver a causa."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            raise ToolError(f"{type(exc).__name__}: {exc}") from exc

    mcp.tool()(wrapper)
    return fn


# importado depois de `tool` existir: o módulo registra as tools ao ser carregado
from . import tools  # noqa: E402,F401


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
