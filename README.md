# kiro-powers

Powers do [Kiro](https://kiro.dev) mantidos por [@dxaraujo](https://github.com/dxaraujo). Cada pasta é um power
independente, com manifesto (`plugin.json`), skills e, quando usa, servidor MCP (`mcp.json`).

## Powers

| Power | O que faz | MCP |
|---|---|---|
| [elm](elm/) | IBM Engineering Lifecycle Management (ELM) via OSLC: work items do EWM/RTC, requisitos do DOORS Next, testes do ETM, configuração global, rastreabilidade, lançamento de horas e sincronização da documentação do RM (OKF) | [mcp-elm](https://github.com/dxaraujo/mcp-elm) |
| [elk](elk/) | Logs do ELK (Elasticsearch + Kibana): buscar, contar, exportar CSV, diagnosticar incidentes, salvar consultas no Kibana e logs de execução de jobs Spring Batch | [mcp-elk](https://github.com/dxaraujo/mcp-elk) |
| [sdd2](sdd2/) | Engenharia agêntica orientada a especificação: trilhas por tamanho, entrevista de alinhamento, PRD, fatias verticais AFK/HITL, plano na spec do Kiro, TDD com backpressure, revisão e verificação independentes, consolidação no ELM (fonte oficial), planejamento ágil e aprendizado composto; a `sdd2-setup` cria os agentes e liga as skills dos toolkits de stack escolhidas por agente | — (usa o `elm`, se instalado) |

## Instalação

1. Para powers com MCP, instale o [uv](https://docs.astral.sh/uv/): os servidores MCP rodam com `uvx`.
2. No Kiro, adicione o power pelo painel **Powers**, apontando para a pasta do power neste repositório
   (ex.: `https://github.com/dxaraujo/kiro-powers/elm`) ou para uma cópia local dela.
3. Siga o `README.md` da pasta do power para credenciais e primeiros passos.

## Estrutura de um power

```
<power>/
├── plugin.json        # manifesto e keywords de ativação (formato Agent Plugins)
├── mcp.json           # servidor(es) MCP usados pelo power (se houver)
├── README.md          # pré-requisitos e primeiros passos
└── skills/<skill>/    # uma pasta por skill, com SKILL.md
```

No formato `plugin.json` o Kiro carrega do power só `skills/` e `mcp.json` — `steering/`, agentes e hooks na pasta
do power são ignorados. As regras do power ficam numa skill-guia (`skills/<power>/`); o que precisa estar sempre no
contexto, a skill de setup instala em `.kiro/steering/` do projeto.

## Licença

[MIT](LICENSE)
