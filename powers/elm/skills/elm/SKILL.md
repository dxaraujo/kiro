---
name: "elm"
description: "Usage rules and map of the IBM ELM power (`elm` MCP): which skill covers each application (elm-ccm, elm-rm, elm-sync, elm-qm, elm-gc, elm-setup), pa_*.json before the server, how to proceed without setup (ask once, pick by name from numbered lists, keep choices in the conversation), list and answer format, write confirmation and credentials. Read it before the first `elm` MCP call of a conversation, together with the area skill, and when the user asks what the power does or how to use it: \"o que o power elm faz\", \"como usar o ELM\", \"usar o ELM sem setup\", IBM ELM, EWM, RTC, DOORS Next, ETM, RQM, OSLC, Jazz."
license: "MIT"
metadata:
  author: "Daniel Xavier Araújo"
  version: "1.0.0"
---

# ELM Power

Este power dá acesso ao **IBM Engineering Lifecycle Management (ELM)** via OSLC, pelo MCP `elm`
(`uvx mcp-elm@latest`). **O MCP fornece as capacidades; as skills fornecem o conhecimento** (quais tools, em que
ordem, de onde vem cada parâmetro).

## O que ele cobre

| Aplicação | O que faz | Skill |
|---|---|---|
| **EWM/RTC (CCM)** | Listar, ler, criar, atualizar, mudar estado, comentar work items (IB, TR, DF, DT, IMP, RSC, REU); itens de sprint, iteração ou plano; **lançar horas trabalhadas (timesheet)** | `elm-ccm` |
| **DOORS Next (RM)** | Buscar, ler, criar e atualizar requisitos (REQ, HU, UC, RN, MSG, ET...), atributos, links entre requisitos e artefatos embutidos | `elm-rm` |
| **Documentação RM** | Baixar os artefatos do DOORS Next para o repositório em OKF (`rm.download.path`) e sincronizar só o que mudou (`sync.md`) | `elm-sync` |
| **ETM/RQM (QM)** | Consultar artefatos de teste (CT, PT, ST, SCT, TER, RT) — só leitura | `elm-qm` |
| **Comum / GC** | Quem sou eu, usuários, project areas, configuração global e rastreabilidade entre work item, requisito e teste | `elm-gc` |
| **Configuração** | Criar/atualizar `.kiro/config/power/elm/pa_<nome>.json`; criar iterações e planos | `elm-setup` |

## Como usar

1. **Carregue a skill da área** antes de chamar as tools.
2. **elm.json primeiro, servidor depois.** `.kiro/config/power/elm/pa_*.json` (gerado pela `elm-setup`) resolve nomes → identifiers
   sem chamadas de descoberta. Com o arquivo, nada muda: use-o.
3. **Sem setup.** Sem o arquivo (ou faltando a seção/nome que o pedido precisa), pergunte **uma vez**: rodar a
   `elm-setup` (grava para as próximas vezes) ou **seguir sem setup**. Seguindo sem setup:
   - pergunte só o que **este** pedido precisa (a lista "Sem setup" de cada skill), uma pergunta por vez;
   - descubra os identifiers com as mesmas tools da `elm-setup` (tabelas da etapa 3 dela), mostrando só **nomes** em
     lista numerada para o usuário escolher — nunca peça uuid, `FR_`, `OT_` ou attribute. Uma opção só (ex.: a
     busca por trecho achou uma project area) → use direto e diga qual; lista só com 2 ou mais;
   - project area: `list_project_areas(app_type=<CCM|RM|QM>, search_name=<trecho que o usuário disser>)`; não liste
     todas sem trecho;
   - guarde as escolhas **na conversa** e reaproveite nos pedidos seguintes (não pergunte de novo); não grave
     arquivo nenhum;
   - no fim, se o usuário for repetir pedidos desse projeto, ofereça gravar o que já foi escolhido com a `elm-setup`.
   Usuário recusou a setup → não ofereça de novo na mesma conversa.
4. **Prefira as tools de skill** (`ccm_*`, `rm_*`): saída enxuta e leitura em Markdown + YAML. As genéricas do IBM
   AI Hub ficam no `reference.md` de cada skill, para o que as de skill não cobrem.
5. **Siglas** ("ib 123", "hu 45", "ct 7") indicam o tipo; o número é o id web.
6. **Listas** saem como tabela que começa por **Código | Título**. Leitura de um item começa por
   `**<código>** — <título>`.
7. **Confirme toda escrita** (criar, atualizar, mudar estado, comentar, ligar) com um resumo por nomes: é visível
   ao time e o MCP não desfaz. Erros do MCP dizem o que corrigir (valores válidos, estados): use-os, sem tentativas
   às cegas.

## Credenciais

Ficam em `~/.config/mcp-elm/elm.properties` (Windows: `%APPDATA%\mcp-elm\elm.properties`, ou `MCP_ELM_CONFIG`).
**Nunca leia nem mostre esse arquivo**: ele tem a senha. Em erro de login (HTTP 401), peça ao usuário que o corrija.
