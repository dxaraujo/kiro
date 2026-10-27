---
name: sdd-iniciar
description: "Hub de início do fluxo sdd — recebe um work item já registrado (FT-031, EP-03, AT-012, IM-003, DF ou IB que o backlog conhece, tarefa [DEV] [REV] [VER] [ESP] [ATD] [IMPL] [BD] [INF] [OPE] [EXT]) ou \"minha próxima tarefa\", descobre o tipo e diz qual skill de papel usar: sdd-desenvolver (Dev), sdd-revisar (Revisor), sdd-verificar (QA), sdd-especificar (Especificador) ou sdd-atender (Atendimento); pedido novo ou item fora do backlog vai para a sdd-triar. As tarefas de Apoio sem skill própria (Implantação, Banco de dados, Infra, Operação, Apoio a outros times) ficam aqui, no fluxo mínimo: iniciar a tarefa no ELM, registrar o trabalho, lançar horas e concluir. Use em \"iniciar\", \"começar\", \"pegar a task 123\", \"vamos trabalhar na FT-031\", \"iniciar o AT-012\", \"iniciar a [IMPL] 670100\", \"registrar o que fiz no IM-003\", \"lançar horas no IM-003\", \"concluir o IM-003\", \"minha próxima tarefa\", \"o que eu pego agora?\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.3.0"
---

# sdd-iniciar — Hub: qual skill faz este item

Cada tarefa do EWM tem um papel e uma skill dona, que pode ser chamada direto por quem tem o papel. Esta skill
descobre o tipo do item e diz qual é: não confere compromisso, não cria branch e não mexe no EWM — a skill do papel
faz isso, começando por assumir a própria tarefa (`elm_transicao(<id>, "assumir")`). A exceção são as tarefas de
Apoio sem skill própria, que esta skill conduz ([abaixo](#tarefas-de-apoio-sem-skill-própria)).

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — Identificar o item

**Ordem de consulta** — vale a primeira fonte que achar, e nunca se inventa dado de work item: (1) `status.md` nas
branches (atual, worktrees, remotas: `git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`); (2) o `backlog.md`
da base (ids locais e as colunas `origem` e `elm`, inclusive `## Apoio`); (3) o EWM (`elm_ler_wi`), se
a sessão tem o MCP `elm` (o título da tarefa traz o tipo: `[DEV] FT-031 …`); (4) perguntar à pessoa. Id que não
está em (1) nem (2) não está registrado.

## Passo 2 — Encaminhar

| Item informado | Skill | Papel / agente |
|---|---|---|
| pedido em texto, ou id que não está no backlog | **`sdd-triar`** | P.O. / `sdd-produto` |
| `EP-nn`, tarefa `[ESP]` | **`sdd-especificar`** | Especificador / `sdd-produto` |
| `FT-nnn`, DF ou IB do backlog, tarefa `[DEV]`, "próxima fatia" | **`sdd-desenvolver`** | Dev / `sdd-codificador` |
| tarefa `[REV]` | **`sdd-revisar`** (rubrica C sobre o PR) | Revisor / `sdd-revisor` |
| tarefa `[APR] FT-nnn Aprovar plano` | **`sdd-revisar`** (seção "Aprovação do plano — a `[APR]`") | Aprovador (Dev Sênior) / `sdd-revisor` |
| tarefa `[APR] FT-nnn Aprovar PR` | **`sdd-revisar`** (seção "Aprovação do PR — a `[APR]`") | Aprovador (Dev Sênior) / `sdd-revisor` |
| tarefa `[VER]` | **`sdd-verificar`** | Verificador (QA) / `sdd-verificador` |
| `AT-nnn`, tarefa `[ATD]` | **`sdd-atender`** | quem atende / `sdd-produto` |
| `IM-`, `BD-`, `IN-`, `OP-`, `EX-nnn` (outra categoria do Apoio sem skill própria na tabela **Apoio** do `sdd.md`), tarefa `[IMPL]` `[BD]` `[INF]` `[OPE]` `[EXT]` | **esta skill** — [Tarefas de Apoio sem skill própria](#tarefas-de-apoio-sem-skill-própria) | quem faz / `sdd-produto` |
| fatia em `pronta-para-merge` (qualquer item dela, menos a `[APR]`) | **`sdd-desenvolver`** (Passo 6 — merge do PR aprovado) | Dev responsável / `sdd-codificador` |
| fatia em `bloqueada` com `aguardando troca para HITL` | **`sdd-planejamento`** (Troca de modo, na base); feita a troca, o Dev retoma pela **`sdd-desenvolver`** | P.O. ou SM / `sdd-produto` · Dev / `sdd-codificador` |
| fatia em `mergeada` (e não `concluida` na base: `status.md` ou `backlog.md` da base — depois do merge vale a base) | **`sdd-consolidar`** (processo de produto; horas na `[GB]`) | P.O. ou SM / `sdd-produto` |
| tarefa `[GB] Gerenciamento do backlog` | fatias em `mergeada` → **`sdd-consolidar`** (uma por vez); nenhuma → **`sdd-triar`** | P.O. ou SM / `sdd-produto` |

```
🔀 <item> — <título> · <tipo> · <fase do status.md | status do backlog>
Próximo: use `<skill> <item>`   (agente: <agente>)
```

Pedido em texto: `🔀 pedido não registrado — <resumo em uma linha>` · `Próximo: use sdd-triar`.

Responda com a instrução e **pare**: nunca invoque nem simule a skill do papel — ela começa na própria invocação.
Item de Apoio sem skill própria → siga direto na seção abaixo, nesta mesma skill.

## "Minha próxima tarefa"

1. Com o MCP `elm`: `elm_listar_wi(dono: "eu", iteracao: <a da sprint aberta>)`; sem ele: as linhas do
   `sprint-<nn>.md` aberto com `responsavel` = a pessoa (login do `sdd.md` ou `git config user.email`).
2. Mostre as tarefas abertas (não concluídas) de **qualquer tipo**, na ordem de prioridade da sprint — as que já
   estão em andamento primeiro:
   ```
   📋 Suas tarefas na sprint <nn> (<login>)
   | # | Tarefa | Item | Estado | Skill |
   |---|---|---|---|---|
   | 1 | [DEV] 669412 | FT-034 Exportar relatório | Em Desenvolvimento | sdd-desenvolver |
   | 2 | [REV] 669401 | FT-031 Bloquear a conta | Novo | sdd-revisar |
   Qual? (número)
   ```
   Tarefa sem tipo do sdd no título (`[DEV]`, `[REV]`, `[APR]`, `[VER]`, `[ESP]`, `[GB]` e os prefixos do Apoio não aparecem): mostre no fim, com
   Skill `— (fora do sdd)`; escolhida → diga que não é do fluxo e ofereça a `sdd-triar` se ela deve virar trabalho
   do fluxo.
3. A pessoa escolhe → Passo 2 com o item escolhido. Nenhuma tarefa → diga e ofereça "próxima fatia"
   (`sdd-desenvolver`) ou a `sdd-status`.

## Tarefas de Apoio sem skill própria

Implantação `[IMPL]`, Banco de dados `[BD]`, Infra `[INF]`, Operação `[OPE]`, Apoio a outros times `[EXT]` — e toda
categoria da tabela **Apoio** do `sdd.md` com Skill `sdd-iniciar`. O trabalho acontece fora do repositório (a
pessoa executa; o agente não roda script, deploy nem comando em ambiente): aqui só se registra. Item registrado na
seção `## Apoio` do `backlog.md` da base, com a ficha `<produto>/apoio/<ID>-<slug>.md` (formato:
[`sdd-atender`](../sdd-atender/SKILL.md#registro), com `## O que foi feito`); id fora do backlog → `sdd-triar` e
pare; `concluido`/`cancelado` → mostre e pare. Os passos valem em qualquer ordem e em várias sessões; cada escrita
no EWM com "sim". Ficha e backlog são gravados na base (bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base)).

1. **Iniciar a tarefa no ELM:** `elm_transicao(id, "assumir")` (já minha → `ja_estava`; de outra pessoa →
   `conflito`: pergunte e repita com `forcar: true`). Item com `elm` `pendente` → antes, crie a tarefa
   ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §6). Fora da sprint aberta ou fora da reserva → a
   decisão é do P.O. (`sdd-planejamento`, Encaixe) e pare.
2. **Registrar o trabalho:** em `## O que foi feito` da ficha, os passos e a evidência (o que foi executado, onde,
   resultado, link do chamado ou da mudança), **sem dado de cliente** — dado real fica em `.kiro/local/apoio/<ID>/`.
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

- Só encaminha: o compromisso (DoR, sprint, WIP), a branch e o EWM são da skill do papel — menos nas tarefas de
  Apoio sem skill própria, que esta skill conduz.
- Nunca invente dados de work item; na dúvida entre dois tipos, pergunte.
