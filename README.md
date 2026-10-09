# mcp-okf

Servidor MCP que transforma um bundle OKF (pasta com `index.md` e um `.md` por documento, como o gerado pela
alm-sync do [mcp-alm](https://github.com/dxaraujo/mcp-alm)) numa base de conhecimento consultável em linguagem natural.

- **Índice vetorial:** Qdrant em modo local (pasta no disco, sem servidor), busca híbrida denso + BM25 com fusão RRF.
- **Embeddings:** fastembed local, `paraphrase-multilingual-mpnet-base-v2` (PT-BR); nada sai da máquina.
- **Enriquecimento:** feito pela própria LLM do cliente (sem chave de API): resumo, palavras-chave/sinônimos,
  entidades e perguntas que o documento responde.
- **Links:** `links` do frontmatter (nomes do DOORS Next), links do corpo para outros arquivos do bundle (`cita`) e
  URL do ALM de artefato que está no bundle; backlinks e documentos semanticamente similares na leitura.

## Instalação

```bash
uv sync
# baixa os modelos uma vez (~1 GB), para a 1ª indexação não estourar o timeout do cliente MCP
uv run python -c "from mcp_okf import store; store.embed_dense(['x']); store.embed_sparse(['x'])"
claude mcp add okf -- uv --directory /caminho/mcp-okf run mcp-okf
```

Dados em `~/.config/mcp-okf/` (`%APPDATA%\mcp-okf` no Windows; ou `MCP_OKF_HOME`): `qdrant/` e
`state/<sha1(root)>.json` (hash, links e enriquecimento de cada documento). Nada é gravado no bundle.
O Qdrant local trava a pasta: só um processo do mcp-okf por vez.

## Tools

`root` é sempre o caminho absoluto do bundle.

| Tool | Parâmetros | Devolve |
|---|---|---|
| `okf_index` | `root`, `limit=200`, `force=False` | `{documentos, indexados, removidos, restantes, a_enriquecer}`; incremental por sha256; chame até `restantes=0` |
| `okf_enrich_next` | `root`, `limit=5` | `{restantes, instrucoes, documentos: [{path, id, type, title, description, body, links}]}` |
| `okf_save_enrichment` | `root`, `items: [{path, summary, keywords, entities, questions}]` | `{gravados, restantes}` |
| `okf_search` | `root`, `query`, `limit=8`, `folder?`, `type?` | `[{path, id, title, type, folder, score, summary, trechos: [{section, text}]}]` |
| `okf_list_documents` | `root`, `folder?`, `type?` | `[{path, id, title, type, folder, description, indexado, enriquecido}]` |
| `okf_get_document` | `root`, `ref` (path ou id) | `{path, markdown, enrichment, links: {saida, entrada, similares}}` |

Fluxo: `okf_index` até `restantes=0` → `okf_enrich_next` / `okf_save_enrichment` até `restantes=0` → perguntas
com `okf_search` e `okf_get_document`. Depois de um novo sincronismo da alm-sync, rode `okf_index` de novo: só o que
mudou é reindexado, e só o que mudou volta para a fila de enriquecimento.

## Como indexa

Cada documento vira pontos `chunk` (corpo dividido por heading `#`..`###`, seções longas por parágrafo; cada chunk
leva o prefixo `<tipo> <id> — <título> | <pasta> | <seção>`) e um ponto `doc` (cabeçalho + enriquecimento). A busca
funde o ranking denso e o BM25 (RRF) e agrupa por documento.

## Testes

```bash
uv run pytest
```
Os testes usam Qdrant em memória e embeddings falsos (não baixam modelo).
