---
name: sdd-executar
description: "Skill de quem faz as tarefas de Apoio sem fluxo próprio no sdd — Implantação [IMPL], Banco de dados [BD], Infra [INF], Operação [OPE], Apoio a outros times [EXT] (IM-, BD-, IN-, OP-, EX-nnn), já registradas pela sdd-triar (ou trazidas do EWM pela sincronização da sprint). O trabalho acontece fora do repositório (a pessoa executa; o agente não roda script, deploy nem comando em ambiente): aqui só se registra — iniciar a tarefa no ELM, registrar o que foi feito na ficha (sem dado de cliente), lançar horas e concluir. Atendimento (AT-nnn, [ATD]) é da sdd-atender; pedido novo passa pela sdd-triar. Use em \"executar o IM-003\", \"iniciar a [IMPL] 670100\", \"registrar o que fiz no IM-003\", \"lançar horas no IM-003\", \"concluir o IM-003\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.3.1"
---

# sdd-executar — Tarefas de Apoio sem fluxo próprio

Implantação `[IMPL]`, Banco de dados `[BD]`, Infra `[INF]`, Operação `[OPE]`, Apoio a outros times `[EXT]` — e toda
categoria da tabela **Apoio** do `sdd.md` com Skill `sdd-executar`. O trabalho acontece fora do repositório (a
pessoa executa; o agente não roda script, deploy nem comando em ambiente): aqui só se registra. A **`sdd-triar`**
registra o item; esta skill é a de quem **faz**.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — O que chegou

| Entrada | Como ler |
|---|---|
| `IM-`, `BD-`, `IN-`, `OP-`, `EX-nnn`, ou a tarefa `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]` (número do EWM: a linha com esse id em `elm`) | a linha em `## Apoio` do `backlog.md` da base e a ficha `<produto>/apoio/<pasta>/<ID>-<slug>.md` (formato: [`sdd-atender`](../sdd-atender/SKILL.md#registro), com `## O que foi feito`) |
| pedido novo, ou id fora do backlog | não está registrado → "use `sdd-triar`" e pare |
| `AT-nnn`, tarefa `[ATD]` | não é desta skill → "use `sdd-atender <item>`" e pare |
| item `concluido` ou `cancelado` | mostre a situação e pare |

## Passo 2 — Registrar

O passo 1 vem primeiro; com a tarefa já assumida, os demais valem em qualquer ordem e em várias sessões (lançar
horas ou concluir sem a tarefa assumida → o passo 1 antes). Cada escrita no EWM com "sim". Ficha e backlog são gravados
na base (bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base)).

1. **Iniciar a tarefa no ELM:** `elm_transicao(id, "assumir")` (já minha → `ja_estava`; de outra pessoa →
   `conflito`: pergunte e repita com `forcar: true`). Antes de tudo: item em `backlog`, sem linha na seção Apoio do
   `sprint-<nn>.md` aberto (sem sprint, ou fora da reserva na triagem) → a decisão é do P.O. (`sdd-planejamento`,
   Encaixe) e pare; com a linha na sprint, siga (a reserva já foi decidida ali); Kanban (`acordos.md`) → não há sprint nem encaixe: siga
   (a tarefa fica na iteração corrente). Item com `elm` `pendente` → antes de assumir, crie a
   tarefa ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §6) e grave o id na coluna `elm` do
   `backlog.md` e em "Tarefa ELM" da linha da seção Apoio do `sprint-<nn>.md`, no commit da ficha.
2. **Registrar o trabalho:** em `## O que foi feito` da ficha, os passos e a evidência (o que foi executado, onde,
   resultado, link do chamado ou da mudança), **sem dado de cliente** — dado real fica em `.kiro/local/apoio/<pasta>/<ID>/`.
   Comentário ou anexo na própria tarefa (`elm_comentar`, `elm_anexo enviar`), se a pessoa quiser.
3. **Lançar horas:** a qualquer momento, `elm_lancar_horas(id, horas)`; cada lançamento é uma linha na tabela Horas
   da ficha. Lançar **não** conclui.
4. **Concluir:** mostre o já lançado (`elm_horas(id)`), pergunte só o saldo → `elm_lancar_horas`, depois
   `elm_transicao(id, "concluir")`, numa confirmação. `**Situação:** concluido` e os créditos da sessão na ficha
   ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4); no `backlog.md`, `status` `concluido` e
   `concluida-em`; no `sprint-<nn>.md`, a Situação e os Créditos da linha na seção Apoio. Um commit `<ID> concluir`.
   Desdobramento que muda o repositório → `sdd-triar` com `origem` `<ID>`.

Sem o MCP `elm` ou com falha → `ELM pendente [<chave>]: <assumir | lançar <h>h | concluir> <prefixo> <ID>` no campo
`**ELM:**` da ficha, e siga.

## Regras

- O agente não executa o trabalho: script, deploy e comando em ambiente são da pessoa; aqui fica o registro.
- **Dado de cliente nunca vai para o git**: fica em `.kiro/local/apoio/<pasta>/<ID>/`.
- Registrar o item é da `sdd-triar`; esta skill nunca numera nem abre item.
- Lançar horas é registro de empenho, a qualquer momento na tarefa iniciada; concluir é o passo 4, com o saldo.
