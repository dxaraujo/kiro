---
name: sdd-iniciar
description: "Hub de início do fluxo sdd — recebe um work item já registrado (FT-031, EP-03, AT-012, DF ou IB que o backlog conhece, tarefa [DEV] [REV] [VER] [ESP] [ATD]) ou \"minha próxima tarefa\", descobre o tipo e diz qual skill de papel usar: sdd-desenvolver (Dev), sdd-revisar (Revisor), sdd-verificar (QA), sdd-especificar (Especificador) ou sdd-atender (atendimento); pedido novo ou item fora do backlog vai para a sdd-triar. Não tem regra própria: cada skill de papel assume a sua tarefa no EWM e confere o compromisso. Use em \"iniciar\", \"começar\", \"pegar a task 123\", \"vamos trabalhar na FT-031\", \"iniciar o AT-012\", \"minha próxima tarefa\", \"o que eu pego agora?\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.9.0"
---

# sdd-iniciar — Hub: qual skill faz este item

Cada tarefa do EWM tem um papel e uma skill dona, que pode ser chamada direto por quem tem o papel. Esta skill só
descobre o tipo do item e diz qual é: não confere compromisso, não cria branch e não mexe no EWM — a skill do papel
faz isso, começando por assumir a própria tarefa (`sdd-elm` modo *assumir*).

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — Identificar o item

**Ordem de consulta** — vale a primeira fonte que achar, e nunca se inventa dado de work item: (1) `status.md` nas
branches (atual, worktrees, remotas: `git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`); (2) o `backlog.md`
da base (ids locais e as colunas `origem` e `elm`, inclusive `## Atendimentos`); (3) o EWM pela skill `elm-ccm`, se
a sessão tem o power `elm` (o título da tarefa traz o tipo: `[DEV] FT-031 …`); (4) perguntar à pessoa. Id que não
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

## "Minha próxima tarefa"

1. Com o power `elm`: `elm-ccm` › **quem sou eu** e **listar itens** (responsável = o login, iteração = a da sprint aberta); sem ele: as linhas do
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
   Tarefa sem tipo do sdd no título (`[DEV]`, `[REV]`, `[APR]`, `[VER]`, `[ESP]`, `[ATD]`, `[GB]` não aparecem): mostre no fim, com
   Skill `— (fora do sdd)`; escolhida → diga que não é do fluxo e ofereça a `sdd-triar` se ela deve virar trabalho
   do fluxo.
3. A pessoa escolhe → Passo 2 com o item escolhido. Nenhuma tarefa → diga e ofereça "próxima fatia"
   (`sdd-desenvolver`) ou a `sdd-status`.

## Regras

- Só encaminha: o compromisso (DoR, sprint, WIP), a branch e o EWM são da skill do papel.
- Nunca invente dados de work item; na dúvida entre dois tipos, pergunte.
