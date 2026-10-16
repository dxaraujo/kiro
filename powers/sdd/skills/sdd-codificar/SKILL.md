---
name: sdd-codificar
description: "Skill do papel Dev no fluxo sdd — começa ou retoma o código de uma fatia já registrada no backlog (FT-031, de épico ou sem épico, em qualquer trilha: padrão, rápida, direta), de um item do EWM que o backlog já conhece (DF, IB) ou da tarefa [DEV] de uma fatia. É o ponto de compromisso: confere a Definition of Ready da trilha, o responsável, se a fatia está na sprint aberta (fora dela, o encaixe é decisão do P.O. pela sdd-planejamento) e os limites de WIP; cria a branch (sugere o nome e aguarda), a pasta da fatia em .kiro/specs/ com o status.md, assume a [DEV] no EWM (sdd-elm modo assumir, com confirmação) e encaminha pela fase: pesquisar → plano → implementar → PR. Pedido novo ou item fora do backlog passa antes pela sdd-triar; [REV], [VER], [ESP] e atendimento têm skill própria (o hub sdd-iniciar encaminha). Use em \"vamos trabalhar na FT-031\", \"pegar a [DEV] da FT-031\", \"corrigir o defeito 4567\", \"próxima fatia\", \"retomar a FT-031\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.5.0"
---

# sdd-codificar — Compromisso e início do código

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-codificar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Começar é um compromisso: daqui em diante a fatia consome a capacidade do time e o lead time corre. Por isso esta
skill só começa o que já está registrado e planejado; a entrada de trabalho novo é da **`sdd-triar`**. É a skill do
papel **Dev**: assume a `[DEV]` da fatia e a leva até o PR. Revisão (`[REV]`), verificação (`[VER]`), especificação
(`[ESP]`) e atendimento (`[ATD]`) têm skill própria; na dúvida sobre o item, o hub **`sdd-iniciar`** diz qual.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — O que chegou

**Ordem de consulta** para qualquer id (`FT-031`, número do EWM) — vale a primeira fonte que achar, e nunca se
inventa dado de work item: (1) `status.md` nas branches (atual, worktrees, remotas); (2) o `backlog.md` da base
(ids locais e as colunas `origem` e `elm`); (3) o EWM pela skill `elm-ccm`, se a sessão tem o power `elm`;
(4) perguntar à pessoa. O EWM e a pessoa só completam dados: id que não está em (1) nem (2) não está registrado →
`sdd-triar`. A `fase` do `status.md` decide se o papel pode começar.

| Entrada | Como ler |
|---|---|
| `FT-nnn` | `<produto>/backlog.md` (+ o PRD do épico ou a ficha da fatia sem épico) |
| número do EWM (DF, IB) | a linha do `backlog.md` com esse id em `origem` ou `elm` |
| tarefa `[DEV] FT-nnn` | a fatia do pai |
| "próxima fatia" | a `pronta` de maior prioridade da sprint aberta sem `status.md` em nenhuma branch (no Kanban, a do topo do backlog) |
| `[REV]`, `[VER]`, `EP-nn`/`[ESP]`, `AT-nnn`/`[ATD]` | não é deste papel → "use `sdd-iniciar <item>`" e pare |
| pedido em texto, ou id que não está no backlog | não está registrado → "use `sdd-triar`" e pare |

Fatia já iniciada (tem pasta em `.kiro/specs/` nesta branch, em worktrees ou em branches remotas —
`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) → leia o `status.md` e **retome**: Passo 4, item 4
(assumir: a `sdd-elm` modo *assumir* não repete o que já foi feito) e Passo 5, sem repetir o Passo 3. Branch
diferente da atual → pergunte se troca (alterações locais não commitadas → avise e pare; nunca ofereça descartar,
`stash` ou `reset`).

## Passo 2 — Trilha

A trilha vem do registro, não de uma triagem nova: fatia de uma seção de épico → **padrão**; da seção
`## Fatias — sem épico` → a da coluna `trilha` (seção antiga `## Fatias — trilha rápida` → **rápida**). Ao ler o
item, a trilha registrada não serve (a "rápida" tem regra de negócio nova, a "direta" tem mais de um comportamento)
→ pare e devolva à `sdd-triar` para refazer a triagem.

| Trilha | Caminho depois daqui |
|---|---|
| **padrão** | pesquisa → plano → **GATE do plano** → implementação → revisão → verificação → PR |
| **rápida** | pesquisa curta → `bugfix.md` + `tasks.md` (o teste que reproduz primeiro) → implementação → revisão → verificação → PR |
| **direta** | pasta só com o `status.md`, sem spec: teste que falha (quando houver comportamento) → mudança → backpressure → revisão (`sdd-revisar`, rubrica C sobre o diff, com o pedido no lugar dos critérios) → PR |

## Passo 3 — Compromisso

Vale para todas as trilhas. Tudo conferido **antes** de criar branch ou mexer no EWM; falhou um item → diga qual e
o caminho, e não comece.

1. **Definition of Ready.**
   - Padrão de épico: a fatia está `pronta` no `backlog.md` ou passa agora — cenários de aceite em `cobre`, PRD
     `aprovado`/`fatiado`, nenhuma decisão bloqueante `em aberto` (`decisoes.md`), `bloqueada-por` concluídas ou com
     o que a fatia precisa já na base, tamanho ≤ G, modo AFK/HITL declarado.
   - Padrão sem épico: ficha `aprovada por` o P.O., com cenários `C<n>` e nenhuma decisão `em aberto`, tamanho ≤ G,
     modo declarado.
   - Rápida: comportamento esperado claro, sem regra nova, tamanho ≤ M, modo declarado.
   - Direta: o pedido cabe numa frase, sem regra nova, tamanho P.
   - Falhou → `sdd-entrevistar`, `sdd-fatiar` (refinamento) ou `sdd-triar` (retomar a triagem: ficha e `falta:` das
     fatias sem épico).
2. **Responsável.** A coluna `responsavel` do `backlog.md` é outra pessoa → pergunte se ela sabe; trocar é do
   planejamento, não grave aqui.
3. **Sprint.** Nada começa sem item planejado, nem a direta: é na tarefa da sprint que as horas são lançadas. A
   fatia está na sprint aberta (`sprint` do `backlog.md` = a do `sprint-<nn>.md` com `**Situação:** aberta`)? Não
   está → **Encaixe**: a decisão é do P.O., pela **`sdd-planejamento`** (seção Encaixe);
   sem a decisão registrada, não comece. Kanban (`acordos.md`) → não há sprint nem encaixe: a `sdd-elm` modo
   *sprint* põe as tarefas na iteração corrente do EWM ao começar (Passo 4). Nenhuma sprint aberta e nada no
   `acordos.md` (planejamento ainda não feito) → não é encaixe: ofereça a `sdd-planejamento` e não comece.
4. **WIP** (`<produto>/planejamento/acordos.md`; sem o arquivo, 2 fatias esperando pessoa). Conte as fatias em
   `plano-em-revisao`, `aceita` e `pr-aberto` nos `status.md` das branches, como a `sdd-status`. No limite, ou com PR
   parado há mais tempo que o acordo (padrão 1 dia) → mostre quais e recomende destravar antes (aprovar o plano,
   revisar o PR). A pessoa pode seguir mesmo assim: `WIP excedido: <motivo>` vai no Histórico do `status.md` ao
   criá-lo (Passo 4).
5. **Registro publicado.** A linha da fatia, a ficha e o encaixe já estão em `origin/<base>`
   (`git grep -q '<FT>' origin/<base> -- <produto>/backlog.md`)? Só no local → peça o push (ou o merge do PR curto)
   antes: a branch nasce de `origin/<base>`, e um id que ainda não chegou lá pode mudar.

## Passo 4 — Branch, pasta e `[DEV]`

1. **Branch** — sugira e **aguarde**:
   ```
   Branch sugerida: <prefixo do sdd.md><ft>-<slug>   (ex.: feature/ft-031-bloquear-conta)
   Confirma, ou informe outro nome:
   ```
   Confirmado → `git fetch` e `git switch -c <branch> origin/<base>`.
2. **Pasta** `.kiro/specs/<ft>-<slug>/` com `status.md` de [references/status-template.md](references/status-template.md)
   e o `.config.kiro` da spec do Kiro (`specType` `feature` na trilha padrão, `bugfix` na rápida — formato em
   [../sdd-plano/references/plano-templates.md](../sdd-plano/references/plano-templates.md)). Trilha direta: só o
   `status.md` (fase `implementando`), sem `.config.kiro`.
3. **Backlog:** não muda aqui (ele só é escrito na base, pela `sdd-triar`, `sdd-fatiar`, `sdd-planejamento` e
   `sdd-consolidar`); a fatia em andamento é a que tem `status.md` numa branch.
4. **Assumir a `[DEV]`** (com power `elm`; nunca sem "sim") — **`sdd-elm` modo *assumir***: responsável =
   `whoami`, estado em andamento da PA, estimativa se faltar; já minha e em andamento → nada a fazer. O item de
   backlog continua do P.O. Tarefa ainda não existe (encaixe aprovado agora, Kanban, ou publicação que falhou no
   planejamento) → antes, `sdd-elm` modo *sprint* cria as da trilha (pai sempre definido):

   | Fatia | Tarefas | Pai |
   |---|---|---|
   | de épico (padrão) | `[DEV]` `[REV]` `[VER]` | IB da fatia, filho do épico |
   | sem épico, com item de origem (DF, IB) | `[DEV]` `[REV]` `[VER]` — direta: só a `[DEV]` | o próprio item de origem — **sem IB novo** |
   | sem épico, pedido em texto | `[DEV]` `[REV]` `[VER]` — direta: só a `[DEV]` | IB `[FT-nnn]`, filho do épico de Sustentação — direta: o épico de Sustentação |

   Grave os ids das tarefas no campo ELM do `status.md` — é por ele que as horas acham a tarefa. Chamada daqui, na
   branch da fatia, a `sdd-elm` não grava o `backlog.md` nem o `sprint-<nn>.md`: os ids ficam no `status.md`, e a
   `sdd-consolidar` os leva ao backlog. Sem o MCP: `ELM pendente: assumir [DEV] FT-<nnn>` no `status.md`.
5. Commit pequeno do `status.md` e, com "sim", push da branch — é o sinal para o time de que a fatia começou.

## Passo 5 — Encaminhar

```
🚦 FT-<nnn> — <título>   ·   trilha <…> · modo <AFK|HITL> · fase <…>
Épico: <EP — título | — (sem épico)> · Cobre: <… | ficha C1–Cn | origem …> · Branch: <…> · Pasta: .kiro/specs/<ft>-<slug>/
Próximo: <skill>
```

| Fase | Próxima skill |
|---|---|
| `pesquisando`, `planejando`, `plano-em-revisao` | `sdd-plano` (que começa pela `sdd-pesquisar`) |
| `implementando`, `revisando` | `sdd-implementar` (trilha direta: a seção Trilha direta) |
| `verificando` | `sdd-verificar` |
| `aceita` | `sdd-implementar` (Passo 5 — abrir o PR) |
| `pr-aberto` | aguardar o merge; mergeado → `sdd-consolidar` |
| `bloqueada (de: <fase>)` | mostre o motivo e a pergunta; resolvido → volta à skill da fase de origem |

Modo AFK e várias fatias padrão ou rápida prontas na sprint → ofereça o **`sdd-loop`** (o agente leva cada uma até
o PR).

## Regras

- Só começa o que está registrado e planejado: pedido novo ou item fora do backlog vai para a `sdd-triar`; fatia
  fora da sprint, para o encaixe.
- O EWM (ou a pessoa) é a fonte dos dados do item; o código, do comportamento atual; o `status.md`, da fase.
- Toda troca/criação de branch e toda alteração no EWM só com "sim".
- Nunca invente dados de work item.
