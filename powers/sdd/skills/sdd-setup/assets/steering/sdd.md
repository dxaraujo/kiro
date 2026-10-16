---
inclusion: always
---

# sdd — <nome do projeto>

Este repositório usa o fluxo **sdd** (power `sdd`): alinhar antes de escrever, fatias verticais pequenas, plano
aprovado por uma pessoa, teste primeiro com backpressure, revisão e verificação independentes, PR lido por uma
pessoa, e o IBM ELM como registro oficial da documentação. Como funciona: skill `sdd`. Toda demanda nova: `sdd-triar`.
Começar um item registrado: hub `sdd-iniciar` (diz a skill do papel: `sdd-especificar`, `sdd-desenvolver`,
`sdd-revisar`, `sdd-verificar`, `sdd-atender`). Onde parei ou fechar a sessão: `sdd-status`.

- Nada inventado (confirme no código, no banco — só leitura — ou no ELM). Nunca apague nem afrouxe teste.
- **Falha de escrita:** pasta inexistente → crie; permissão negada ou confirmação recusada → `fase: bloqueada (de:
  <fase>)` com o caminho e o que faltou (fora de fatia: diga e pare); gravação parcial → o próximo passo retoma pelo
  que está no disco. Nunca siga como se tivesse gravado.
- Estado limpo entre sessões: quem grava um passo na pasta da fatia commita o que gravou **com o `status.md`**,
  antes de seguir. AFK: quem pede a rodada (plano, implementação, loop) commita o relatório do subagente assim que o
  recebe — revisor, verificador e pesquisador como subagentes não commitam. HITL: cada papel commita o seu
  relatório e a fase na branch do PR; o push é da pessoa.
- Push, troca de branch e escrita no ELM só com "sim" de uma pessoa. Agente nunca faz merge nem `--force`.
- Dado de cliente (consulta, extração, tela com dado real) nunca vai para o git: fica em `.kiro/local/<origem>/<id>/`;
  o versionado guarda consulta, contagem, caminho e resumo sem identificar pessoas.
- Toda hora tem tarefa (`[ESP]` `[DEV]` `[REV]` `[VER]` `[ATD]`; no AFK, só a `[DEV]`). Lançar horas é registro de
  empenho, a qualquer momento na tarefa iniciada; concluir é da skill do papel, com o saldo: `[DEV]` no PR, `[REV]`
  ao aprovar, `[VER]` ao aceitar, `[ESP]` no GATE do backlog, `[ATD]` ao finalizar.
- Estado em disco: cada fatia em `.kiro/specs/<ft>-<slug>/` (comece pelo `status.md`); produto na pasta abaixo.

> Gerado pela `sdd-setup` (power `sdd` <x.y.z>) em <AAAA-MM-DD>. Para mudar: "atualizar a configuração do sdd".
> As skills e os agentes `sdd-*` leem os valores daqui.

## Projeto

| Item | Valor |
|---|---|
| Pasta do produto (`<produto>` nas skills) | `<.kiro/planejamento>` — backlog, épicos e PRDs, planejamento, aprendizado |
| Tipos · stack · módulos | `<batch>` · <Java 21, Spring Batch 5, Oracle> · <módulo único | lista> |
| Toolkits | <nome (origem) | nenhum> |
| Steering | produto `<product.md>` · tecnologia `<tech.md>` · estrutura `<structure.md>` · extras `<… | nenhum>` |
| Glossário · ADRs | `<docs/glossario.md>` · `<docs/adr | não há>` |
| Bundle do ELM (OKF da `elm-sync`) | `<docs/elm/<pa>> | não há` |

**Regras críticas** (BLOQUEANTE na revisão):
- <ex.: escrita em lote sempre idempotente por chave de negócio>

## Comandos (backpressure)

Uma coluna por módulo quando houver mais de um; a fatia usa a do módulo que altera (o `design.md` diz qual).
Na worktree do `sdd-loop`: `cd .kiro/local/wt/<ft> && <comando>`. Falha de ambiente → `AMBIENTE`, nunca consertar.

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
| Ambiente · chamada HTTP | <local | dev — nunca produção> · `<sh .kiro/sdd/http.sh — <url> | curl com confirmação | não se aplica>` |

## Git, banco e autonomia

| Item | Valor |
|---|---|
| Branch base · prefixo · commit | `<develop>` · `<feature/>` · `<FT-<nnn> <verbo> <descrição> | Task <id> - …>` |
| Abrir PR | `<gh pr create … | glab mr create … | entregar título e descrição>` |
| Artefatos de produto (pasta do produto, glossário, ADRs, consolidação) | `<direto na branch base | PR curto para a base>` — nunca em branch de fatia; push ou PR com o "sim" da pessoa (o agente `sdd-produto` não faz push: entrega o comando) |
| MCP de banco | `<@servidor/tool | não há>` — **somente leitura** (`SELECT`/`WITH`), exceto os scripts de massa; DDL fora do fluxo |
| GATE na trilha rápida · paralelo no loop | `<sim | não>` · `<1>` (máx. 3) — GATE do plano: HITL sempre; AFK só na fatia de épico |
| Push e PR no loop | `<perguntar a cada lote (o Kiro confirma cada um) | não — a pessoa abre>` |
| Instalados | hook `<sdd-backpressure | nenhum>` · workflows `<sdd-planejar-fatia, sdd-entregar-fatia | nenhum>` (disparados pela pessoa) |

## ELM

| Item | Valor |
|---|---|
| Usa ELM | `<sim — <caminho do pa_*.json> | não>` (MCP `elm` nos agentes `sdd-produto`, `sdd-codificador` e `sdd-orquestrador`; nos demais, a escrita vira `ELM pendente`) |
| Publicar requisitos · backlog no EWM · ET | `<na-aprovacao | no-merge>` · `<ao-fatiar | na-sprint>` · `<não publica | as-built no merge>` |
| Manual no DOORS Next | `<change set, módulo, links restringe, baseline | nada>` |
| Fatia dividida no EWM | `<itens novos como filhos do item original | fecha o original e cria itens novos>` |
| Tipo · pasta no RM | HF `<História de Usuário>` `<pasta>` · REG `<Regra>` `<pasta>` · GL `<Termos de Glossário>` `<pasta>` · ET `<… | —>` |
| Tipo no EWM · pontos P/M/G | épico `<Épico | Item de Backlog (pai)>` · fatia `<Item de Backlog>` · `<2 · 3 · 5>` |
| Critérios de aceite no IB | `<nome do campo em workitem-types[IB].fields do pa_*.json | descrição>` |
| Tarefas (títulos padrão; editáveis à mão) | `[ESP] EP-<nn> Especificação` · `[DEV] FT-<nnn> Implementar` · `[REV] FT-<nnn> Revisar` · `[VER] FT-<nnn> Verificar` · `[ATD] AT-<nnn> <pedido>` |
| Classificação da tarefa | `<[ESP] Análise / Especificação · [DEV] Desenvolvimento · [REV] Outra - Não listada · [VER] Testes de Homologação · [ATD] Suporte / Apoio Técnico Especializado | a PA não tem>` |
| `CT.csv` (colunas na ordem do template do ETM) | `<Tipo=Caso de Teste · Resumo · Responsável · Status=<inicial> · Categoria · Planejado para · Descrição>` |

## Agentes

| Agente | Skills extras | Oferecidas e recusadas | MCP | Modelo | Subagentes |
|---|---|---|---|---|---|
| `sdd-produto` | <…> | <…> | <…> | <padrão> | `sdd-pesquisador`, `sdd-revisor` |
| `sdd-pesquisador` | <…> | <…> | <…> | <padrão> | — |
| `sdd-codificador` | <…> | <…> | <…> | <padrão> | `sdd-pesquisador`, `sdd-revisor` <+ do projeto> |
| `sdd-revisor` | <…> | <…> | <…> | <padrão> | — |
| `sdd-verificador` | <…> | <…> | <…> | <padrão> | — |
| `sdd-orquestrador` | <…> | <…> | — | <padrão> | os `sdd-*` <+ do projeto> |

## Regras aprendidas

Regras de **julgamento** promovidas pela `sdd-aprender` (lições em `<produto>/aprendizado/licoes.md`). O revisor
as cobra como itens da rubrica; o plano as respeita. Erro mecânico não entra aqui: vira lint, teste, hook ou CI.
Formato: `### R-<nn> · <título> · aplica a: <codificador | revisor | plano | PRD | todos> · severidade: <BLOQUEANTE | IMPORTANTE>`,
a regra em 1–2 frases imperativas, `- ✅ <certo> · ❌ <errado>`, `- Origem: L-<nnn>`.

<!-- Nenhuma regra promovida ainda. -->
