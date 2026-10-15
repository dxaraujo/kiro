# mcp-okf

Servidor MCP que transforma um bundle OKF (pasta com `index.md` e um `.md` por documento, como o gerado pela
elm-sync do [mcp-elm](https://github.com/dxaraujo/kiro/tree/main/mcps/elm)) numa base de conhecimento consultável em linguagem natural.

- **Índice:** um arquivo SQLite por bundle (sem servidor, vários processos podem abrir): FTS5 (BM25) + vetores
  densos com cosseno por força bruta (numpy), fusão RRF.
- **Embeddings:** fastembed local, `paraphrase-multilingual-MiniLM-L12-v2` (PT-BR, ~220 MB); nada sai da máquina.
- **Links:** `links` do frontmatter (nomes do DOORS Next), links do corpo para outros arquivos do bundle (`cita`) e
  URL do ALM de artefato que está no bundle; saída e entrada na leitura.
- **Visualização:** `okf_export_html` grava `okf.html` no bundle: grafo 3D dos links, lista filtrável e cada
  documento renderizado (markdown formatado, links internos navegáveis).

## Instalação

Requer o [uv](https://docs.astral.sh/uv/). Baixe o modelo uma vez, para a 1ª indexação não estourar o timeout do
cliente MCP:

```bash
uvx --from mcp-okf python -c "from mcp_okf import store; store.embed(['x'])"
```

Configuração do cliente MCP (Kiro: `~/.kiro/settings/mcp.json` ou `.kiro/settings/mcp.json` do projeto):

```json
{
  "mcpServers": {
    "okf": {
      "command": "uvx",
      "args": ["mcp-okf@latest"],
      "env": { "UV_SYSTEM_CERTS": "true" }
    }
  }
}
```

Claude Code: `claude mcp add okf -- uvx mcp-okf@latest`.

Dados em `~/.config/mcp-okf/` (`%APPDATA%\mcp-okf` no Windows; ou `MCP_OKF_HOME`): `<sha1(root)>.db` por bundle.
Nada é gravado no bundle, exceto o `okf.html` quando pedido. Vindo da 0.2: pode apagar `qdrant/` e `state/` dessa
pasta (o enriquecimento pela LLM saiu; reindexe com `okf_index`).

## Tools

`root` é sempre o caminho absoluto do bundle.

| Tool | Parâmetros | Devolve |
|---|---|---|
| `okf_index` | `root`, `limit=200`, `force=False` | `{documentos, indexados, removidos, restantes}`; incremental por sha256; chame até `restantes=0` |
| `okf_search` | `root`, `query`, `limit=8`, `folder?`, `type?` | `[{path, id, title, type, folder, score, trechos: [{section, text}]}]` |
| `okf_list_documents` | `root`, `folder?`, `type?` | `[{path, id, title, type, folder, description, indexado}]` |
| `okf_get_document` | `root`, `ref` (path ou id) | `{path, markdown, links: {saida, entrada}}` |
| `okf_export_html` | `root` | `{arquivo, documentos, links}`; grava `<root>/okf.html` (bibliotecas via CDN) |

Fluxo: `okf_index` até `restantes=0` → perguntas com `okf_search` e `okf_get_document`. Depois de um novo
sincronismo da alm-sync, rode `okf_index` de novo: só o que mudou é reindexado.

## Como indexa

Cada documento vira chunks (corpo dividido por heading `#`..`###`, seções longas por parágrafo; cada chunk leva o
prefixo `<tipo> <id> — <título> | <pasta> | <seção>`), gravados com o vetor e no FTS5. A busca funde o ranking
denso e o BM25 (RRF) e agrupa por documento.

## Testes

```bash
uv run pytest
```
Os testes usam um SQLite temporário e embeddings falsos (não baixam modelo).
