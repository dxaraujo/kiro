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
    └── gitlabpr/    #   mcp-gitlabpr
```

## Powers

| Power | O que faz | MCP |
|---|---|---|
| [elk](powers/elk/) | Logs do ELK (Elasticsearch + Kibana): buscar, contar, exportar CSV, diagnosticar incidentes, consultas salvas no Kibana e execução de jobs Spring Batch | [mcp-elk](mcps/elk/) |
| [sdd](powers/sdd/) | Engenharia agêntica orientada a especificação: trilhas por tamanho (inclusive atendimento), PRD, fatias verticais AFK/HITL, plano na spec do Kiro, TDD com backpressure, revisão e verificação independentes, ELM como fonte oficial (work items, horas, requisitos, casos de teste e sincronismo do bundle), planejamento ágil e aprendizado composto | [mcp-elm](mcps/elm/), [mcp-gitlabpr](mcps/gitlabpr/) |

Detalhes e estrutura de um power: [powers/README.md](powers/README.md).

## MCPs

| MCP | Pacote no PyPI | Para quê |
|---|---|---|
| [elm](mcps/elm/) | [`mcp-elm`](https://pypi.org/project/mcp-elm/) | IBM ELM (DOORS Next, EWM, ETM) via OSLC, em operações do fluxo sdd (lê o `pa` do projeto), e busca local no bundle do DOORS Next |
| [elk](mcps/elk/) | [`mcp-elk`](https://pypi.org/project/mcp-elk/) | Elasticsearch/Kibana: busca, contagem, consultas salvas e exportação CSV |
| [gitlabpr](mcps/gitlabpr/) | [`mcp-gitlabpr`](https://pypi.org/project/mcp-gitlabpr/) | GitLab: listar, obter, criar e mesclar merge requests |

Desenvolvimento e publicação: [mcps/README.md](mcps/README.md).

## Como as peças se ligam

- O power declara o MCP no `mcp.json` dele com `uvx <pacote>@latest`: quem instala o power recebe o MCP do
  **PyPI**, não desta pasta. Mudança em `mcps/` só chega aos powers depois de publicada.
- O `sdd` traz os MCPs `elm` e `gitlabpr` (e, nos agentes que ele gera, o MCP de banco do projeto). O próprio `elm`
  indexa e consulta o bundle que a `sdd-sync` baixa (`elm_*_local`).

## Instalação

1. Instale o [uv](https://docs.astral.sh/uv/): os MCPs rodam com `uvx`.
2. No Kiro, adicione o power pelo painel **Powers**, apontando para a pasta dele neste repositório
   (`https://github.com/dxaraujo/kiro/tree/main/powers/<power>`) ou para uma cópia local.
3. Siga o `README.md` do power para credenciais e primeiros passos.

## Licença

[MIT](LICENSE)
