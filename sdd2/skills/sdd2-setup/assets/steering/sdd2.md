---
inclusion: always
---

# sdd2 — <nome do projeto>

Este repositório usa o fluxo **sdd2** (power `sdd2`): alinhar antes de escrever, fatias verticais pequenas, plano
aprovado por uma pessoa, teste primeiro com backpressure, revisão e verificação independentes, PR lido por uma
pessoa, e o IBM ELM como registro oficial da documentação. Como funciona: skill `sdd2`. Começar: `sdd2-iniciar`.
Onde parei ou fechar a sessão: `sdd2-status`.

- Nada inventado (confirme no código, no banco — só leitura — ou no ELM). Nunca apague nem afrouxe teste.
- Push, troca de branch e escrita no ELM só com "sim" de uma pessoa. Agente nunca faz merge nem `--force`.
- Estado em disco: cada fatia em `.kiro/specs/<ft>-<slug>/` (comece pelo `status.md`); produto na pasta abaixo.

> Gerado pela `sdd2-setup` (power `sdd2` <x.y.z>) em <AAAA-MM-DD>. Para mudar: "atualizar a configuração do sdd2".
> As skills e os agentes `sdd2-*` leem os valores daqui.

## Projeto

| Item | Valor |
|---|---|
| Pasta do produto (`<produto>` nas skills) | `<docs/<produto>>` — backlog, épicos e PRDs, planejamento, aprendizado |
| Tipos · stack · módulos | `<batch>` · <Java 21, Spring Batch 5, Oracle> · <módulo único | lista> |
| Toolkits | <nome (origem) | nenhum> |
| Steering | produto `<product.md>` · tecnologia `<tech.md>` · estrutura `<structure.md>` · extras `<… | nenhum>` |
| Glossário · ADRs | `<docs/glossario.md>` · `<docs/adr | não há>` |
| Bundle do ELM (OKF da `elm-sync`) | `<docs/elm/<pa>> | não há` |

**Regras críticas** (BLOQUEANTE na revisão):
- <ex.: escrita em lote sempre idempotente por chave de negócio>

## Comandos (backpressure)

Uma coluna por módulo quando houver mais de um; a fatia usa a do módulo que altera (o `design.md` diz qual).
Na worktree do `sdd2-loop`: `cd .kiro/local/wt/<ft> && <comando>`. Falha de ambiente → `AMBIENTE`, nunca consertar.

| Ação | `<módulo>` |
|---|---|
| Compilar | `<…>` |
| Testes · teste único (`{alvo}`) | `<…>` · `<…>` |
| Lint · cobertura e gate | `<… | não há>` · `<comando> · <gate | sem gate>` |

## Verificação de aceite

| Item | `<módulo>` |
|---|---|
| Executar · exercitar um cenário | `<comando | job + parâmetros>` · <HTTP | job | browser | carga> |
| Onde verificar · massa de teste | <resposta, banco, log> · `<pasta e convenção>` |
| Ambiente · chamada HTTP | <local | dev — nunca produção> · `<sh .kiro/sdd2/http.sh — <url> | curl com confirmação | não se aplica>` |

## Git, banco e autonomia

| Item | Valor |
|---|---|
| Branch base · prefixo · commit | `<develop>` · `<feature/>` · `<FT-<nnn> <verbo> <descrição> | Task <id> - …>` |
| Abrir PR | `<gh pr create … | glab mr create … | entregar título e descrição>` |
| Pasta do produto, glossário, ADRs, consolidação | `<direto na branch base | PR curto para a base>` — nunca em branch de fatia |
| MCP de banco | `<@servidor/tool | não há>` — **somente leitura** (`SELECT`/`WITH`), exceto os scripts de massa; DDL fora do fluxo |
| Plano AFK · GATE na trilha rápida · paralelo no loop | `<aprovação humana | análise basta>` · `<sim | não>` · `<1>` (máx. 3) |
| Push e PR no loop | `<perguntar a cada lote (o Kiro confirma cada um) | não — a pessoa abre>` |
| Instalados | hook `<sdd2-backpressure | nenhum>` · workflows `<sdd2-planejar-fatia, sdd2-entregar-fatia | nenhum>` (disparados pela pessoa) |

## ELM

| Item | Valor |
|---|---|
| Usa ELM | `<sim — <caminho do pa_*.json> | não>` (agentes `sdd2-*` não têm o MCP do ELM: a sessão da pessoa usa o power `elm`) |
| Publicar requisitos · backlog no EWM · ET | `<na-aprovacao | no-merge>` · `<ao-fatiar | na-sprint>` · `<não publica | as-built no merge>` |
| Manual no DOORS Next | `<change set, módulo, links restringe, baseline | nada>` |
| Tipo · pasta no RM | HF `<História de Usuário>` `<pasta>` · REG `<Regra>` `<pasta>` · GL `<Termos de Glossário>` `<pasta>` · ET `<… | —>` |
| Tipo no EWM · pontos P/M/G | épico `<Épico>` · fatia `<Item de Backlog>` · `<2 · 3 · 5>` |
| Tarefas por fatia na sprint | `<[DEV] FT-<nnn> Implementar>` (quem implementa) · `<[VER] FT-<nnn> Verificar>` (quem verifica) |
| `CT.csv` (colunas na ordem do template do ETM) | `<Tipo=Caso de Teste · Resumo · Responsável · Status=<inicial> · Categoria · Planejado para · Descrição>` |

## Agentes

| Agente | Skills extras | Oferecidas e recusadas | MCP | Modelo | Subagentes |
|---|---|---|---|---|---|
| `sdd2-produto` | <…> | <…> | <…> | <padrão> | `sdd2-pesquisador`, `sdd2-revisor` |
| `sdd2-pesquisador` | <…> | <…> | <…> | <padrão> | — |
| `sdd2-codificador` | <…> | <…> | <…> | <padrão> | `sdd2-pesquisador`, `sdd2-revisor` <+ do projeto> |
| `sdd2-revisor` | <…> | <…> | <…> | <padrão> | — |
| `sdd2-verificador` | <…> | <…> | <…> | <padrão> | — |
| `sdd2-orquestrador` | <…> | <…> | — | <padrão> | os `sdd2-*` <+ do projeto> |

## Regras aprendidas

Regras de **julgamento** promovidas pela `sdd2-aprender` (lições em `<produto>/aprendizado/licoes.md`). O revisor
as cobra como itens da rubrica; o plano as respeita. Erro mecânico não entra aqui: vira lint, teste, hook ou CI.
Formato: `### R-<nn> · <título> · aplica a: <codificador | revisor | plano | PRD | todos> · <BLOQUEANTE | IMPORTANTE>`,
a regra em 1–2 frases imperativas, `- ✅ <certo> · ❌ <errado>`, `- Origem: L-<nnn>`.

<!-- Nenhuma regra promovida ainda. -->
