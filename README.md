# kiro

> **Arquivado.** O power `sdd` virou o **Saíra** e continua em [dxaraujo/saira](https://github.com/dxaraujo/saira). Este
> repositório fica só para consulta, congelado no sdd 3.4.4 (que usa o `mcp-elm` 3.4.2). Os MCPs estão no PyPI, e os
> schemas públicos em [dxaraujo/mcps](https://github.com/dxaraujo/mcps).

Powers do [Kiro](https://kiro.dev) mantidos por [@dxaraujo](https://github.com/dxaraujo): os powers ensinam o
agente a trabalhar (skills); os MCPs, cada um no seu repositório e publicados no PyPI, dão a ele acesso aos sistemas.

```
kiro/
└── powers/          # powers do Kiro: manifesto, skills e a configuração do MCP que usam
    └── sdd/         #   engenharia agêntica orientada a especificação
```

## Powers

| Power | O que faz | MCP |
|---|---|---|
| [sdd](powers/sdd/) | Engenharia agêntica orientada a especificação: trilhas por tamanho (inclusive atendimento), PRD, fatias verticais AFK/HITL, plano na spec do Kiro, TDD com backpressure, revisão e verificação independentes, ELM como fonte oficial (work items, horas, requisitos, casos de teste e sincronismo do bundle), planejamento ágil e aprendizado composto | [mcp-elm](https://pypi.org/project/mcp-elm/), [mcp-gitlabpr](https://pypi.org/project/mcp-gitlabpr/) |

Detalhes e estrutura de um power: [powers/README.md](powers/README.md).

## MCPs

| Repositório | Pacote no PyPI | Para quê |
|---|---|---|
| `dxaraujo/mcp-elm` | [`mcp-elm`](https://pypi.org/project/mcp-elm/) | IBM ELM (DOORS Next, EWM, ETM) via OSLC, em operações do fluxo sdd (lê o `pa` do projeto), e busca local no bundle do DOORS Next |
| `dxaraujo/mcp-elk` | [`mcp-elk`](https://pypi.org/project/mcp-elk/) | Logs do ELK sem power: lê a config do projeto, conta e compara, exporta CSV, resume execução de job Spring Batch e salva consultas no Kibana |
| `dxaraujo/mcp-gitlabpr` | [`mcp-gitlabpr`](https://pypi.org/project/mcp-gitlabpr/) | GitLab: listar, obter, criar e mesclar merge requests |

Desenvolvimento e publicação: no README de cada repositório (privados).

## Como as peças se ligam

- O power declara o MCP no `mcp.json` dele com `uvx <pacote>@latest`: quem instala o power recebe o MCP do
  **PyPI**. Mudança num MCP só chega aos powers depois de publicada.
- O `mcp-elk` não tem power: instale-o direto no `mcp.json` do Kiro (`uvx mcp-elk@latest`); as regras de uso
  vão nas `instructions` do próprio MCP.
- O `sdd` traz os MCPs `elm` e `gitlabpr` (e, nos agentes que ele gera, o MCP de banco do projeto). O próprio `elm`
  indexa e consulta o bundle que a `sdd-sync` baixa (`elm_*_local`).

## Instalação

1. Instale o [uv](https://docs.astral.sh/uv/): os MCPs rodam com `uvx`.
2. No Kiro, adicione o power pelo painel **Powers**, apontando para a pasta dele neste repositório
   (`https://github.com/dxaraujo/kiro/tree/main/powers/<power>`) ou para uma cópia local.
3. Siga o `README.md` do power para credenciais e primeiros passos.

## Licença

[MIT](LICENSE)
