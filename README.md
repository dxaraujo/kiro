# kiro

Powers e servidores MCP do [Kiro](https://kiro.dev) mantidos por [@dxaraujo](https://github.com/dxaraujo), num
repositório só: os powers ensinam o agente a trabalhar (skills); os MCPs dão a ele acesso aos sistemas.

```
kiro/
├── powers/          # powers do Kiro: manifesto, skills e a configuração do MCP que usam
│   ├── elk/         #   logs do ELK
│   └── sdd/         #   engenharia agêntica orientada a especificação
└── mcps/            # servidores MCP em Python, publicados no PyPI
    ├── elm/         #   mcp-elm
    ├── elk/         #   mcp-elk
    └── okf/         #   mcp-okf
```

## Powers

| Power | O que faz | MCP |
|---|---|---|
| [elk](powers/elk/) | Logs do ELK (Elasticsearch + Kibana): buscar, contar, exportar CSV, diagnosticar incidentes, consultas salvas no Kibana e execução de jobs Spring Batch | [mcp-elk](mcps/elk/) |
| [sdd](powers/sdd/) | Engenharia agêntica orientada a especificação: trilhas por tamanho (inclusive atendimento), PRD, fatias verticais AFK/HITL, plano na spec do Kiro, TDD com backpressure, revisão e verificação independentes, ELM como fonte oficial (work items, horas, requisitos, casos de teste e sincronismo do bundle), planejamento ágil e aprendizado composto | [mcp-elm](mcps/elm/), [mcp-okf](mcps/okf/), [mcp-gitlabpr](mcps/gitlabpr/) |

Detalhes e estrutura de um power: [powers/README.md](powers/README.md).

## MCPs

| MCP | Pacote no PyPI | Para quê |
|---|---|---|
| [elm](mcps/elm/) | [`mcp-elm`](https://pypi.org/project/mcp-elm/) | IBM ELM (DOORS Next, EWM, ETM) via OSLC, em operações do fluxo sdd (lê o `pa` do projeto) |
| [elk](mcps/elk/) | [`mcp-elk`](https://pypi.org/project/mcp-elk/) | Elasticsearch/Kibana: busca, contagem, consultas salvas e exportação CSV |
| [okf](mcps/okf/) | [`mcp-okf`](https://pypi.org/project/mcp-okf/) | Base de conhecimento sobre bundles OKF: indexação e busca semântica local |

Desenvolvimento e publicação: [mcps/README.md](mcps/README.md).

## Como as peças se ligam

- O power declara o MCP no `mcp.json` dele com `uvx <pacote>@latest`: quem instala o power recebe o MCP do
  **PyPI**, não desta pasta. Mudança em `mcps/` só chega aos powers depois de publicada.
- O `sdd` traz os MCPs `elm`, `okf` e `gitlabpr` (e, nos agentes que ele gera, o MCP de banco do projeto). O `okf` lê o
  bundle que a `elm-sync` grava.

## Instalação

1. Instale o [uv](https://docs.astral.sh/uv/): os MCPs rodam com `uvx`.
2. No Kiro, adicione o power pelo painel **Powers**, apontando para a pasta dele neste repositório
   (`https://github.com/dxaraujo/kiro/tree/main/powers/<power>`) ou para uma cópia local.
3. Siga o `README.md` do power para credenciais e primeiros passos.

## Licença

[MIT](LICENSE)
