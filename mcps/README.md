# mcps

Servidores MCP em Python, um pacote por pasta, publicados no PyPI e executados com `uvx`. Os powers de
[../powers](../powers/) os usam pelo `mcp.json`; também podem ser configurados direto no Kiro
(`~/.kiro/settings/mcp.json` ou `.kiro/settings/mcp.json` do projeto) ou em outro cliente MCP.

| Pasta | Pacote | Para quê | Credenciais |
|---|---|---|---|
| [elm](elm/) | [`mcp-elm`](https://pypi.org/project/mcp-elm/) | IBM ELM via OSLC: DOORS Next (rm), EWM (ccm), ETM (qm), GC e horas | `~/.config/mcp-elm/elm.properties` |
| [elk](elk/) | [`mcp-elk`](https://pypi.org/project/mcp-elk/) | Elasticsearch/Kibana, sem power: lê `.kiro/config/elk/`, busca, conta e compara, exporta CSV, resume jobs Spring Batch, consultas salvas | `~/.config/mcp-elk/elk.properties` |
| [gitlabpr](gitlabpr/) | [`mcp-gitlabpr`](https://pypi.org/project/mcp-gitlabpr/) | GitLab (API v4, CE 10.8+): listar, obter, criar e mesclar merge requests | `~/.config/mcp-gitlabpr/gitlabpr.properties` |

## Desenvolvimento

Em cada pasta:

```bash
cd mcps/<mcp>
uv sync
uv run pytest
```

- Python ≥ 3.10; dependências e versão no `pyproject.toml` (lock em `uv.lock`).
- Tools agnósticas: nada específico de uma empresa ou projeto no código — o que é do projeto chega por parâmetro
  ou pela configuração do projeto (gravada pela skill de setup do power ou, no `mcp-elk`, pela tool `elk_configurar`).

## Publicação

O power instala `uvx <pacote>@latest`, então uma mudança só chega aos usuários depois de publicada no PyPI:

1. Suba a `version` no `pyproject.toml` (e rode `uv lock`).
2. `uv run pytest` verde.
3. Publique no PyPI a partir da pasta do MCP.
