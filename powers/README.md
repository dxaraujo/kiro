# powers

Powers do Kiro. Cada pasta é um power independente, instalado pelo painel **Powers** do Kiro apontando para ela
(`https://github.com/dxaraujo/kiro/tree/main/powers/<power>`) ou para uma cópia local.

| Power | O que faz | Skills | MCP |
|---|---|---|---|
| [elk](elk/) | Logs do ELK: busca, contagem, CSV, diagnóstico, consultas salvas, jobs Spring Batch | `elk-setup`, `elk-logs`, `elk-exportar`, `elk-diagnostico`, `elk-job-logs` | `mcp-elk` |
| [sdd](sdd/) | Fluxo de engenharia agêntica orientada a especificação, com ELM e planejamento ágil | `sdd`, `sdd-setup`, `sdd-triar`, `sdd-iniciar`, `sdd-atender`…, `elm-sync` (21) | `mcp-elm`, `mcp-gitlabpr` |

## Estrutura de um power

```
<power>/
├── plugin.json        # manifesto e keywords de ativação (formato Agent Plugins)
├── mcp.json           # servidor(es) MCP usados pelo power (se houver): uvx <pacote>@latest
├── README.md          # pré-requisitos e primeiros passos
└── skills/<skill>/    # uma pasta por skill: SKILL.md e, se precisar, references/ e assets/
```

- No formato `plugin.json` o Kiro carrega do power só `skills/` e `mcp.json` — `steering/`, agentes e hooks na pasta
  do power são ignorados. As regras do power ficam numa skill-guia (`skills/<power>/`); o que precisa estar sempre
  no contexto, a skill de setup instala em `.kiro/steering/` do projeto.
- Arquivos de uma skill (`references/`, `assets/`) são lidos pelo caminho relativo ao `SKILL.md`, dentro do power
  instalado: o agente não os acha buscando no projeto. Por isso cada skill que os cita diz isso logo abaixo do
  título.
- A configuração de cada projeto fica no projeto, em `.kiro/config/power/<power>/` (gerada pela skill de setup e
  validada pelo schema em `skills/<power>-setup/assets/`).
- Versão: `version` do `plugin.json` e `metadata.version` de cada skill, juntos.
