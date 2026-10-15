---
name: sdd-iniciar
description: "Começa ou retoma, no fluxo sdd, um trabalho já registrado no backlog — uma fatia (FT-031) de épico ou sem épico, em qualquer trilha (padrão, rápida, direta), ou um item do EWM que o backlog já conhece (com o power elm); pedido novo ou item fora do backlog passa antes pela sdd-triar. É o ponto de compromisso: confere a Definition of Ready da trilha, o responsável, se a fatia está na sprint aberta (nada começa sem item planejado, nem a direta; fora da sprint, o encaixe é decisão do P.O. pela sdd-planejamento) e os limites de WIP do time; cria a pasta da fatia em .kiro/specs/ e a branch (sugere o nome e aguarda), assume a tarefa no EWM com confirmação e encaminha para a próxima skill pela fase. Use em \"vamos trabalhar na FT-031\", \"pegar a task 123\", \"corrigir o defeito 4567\", \"começar\", \"próxima fatia\", \"retomar a FT-031\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.4.0"
---

# sdd-iniciar — Compromisso e início

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-iniciar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Começar é um compromisso: daqui em diante a fatia consome a capacidade do time e o lead time corre. Por isso esta
skill só começa o que já está registrado e planejado; a entrada de trabalho novo é da **`sdd-triar`**.

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
| tarefa `[DEV] FT-nnn` | a fatia do pai → fluxo normal de início/retomada |
| tarefa `[REV] FT-nnn` (recebida por esta pessoa) | identifica a fatia pai → assume `[REV]` no EWM (responsável = `whoami`, inicia) com "sim" → encaminha para **`sdd-revisar`** (rubrica C), passando: fatia, pasta spec, branch, rodada atual (lida do `status.md`) |
| tarefa `[VER] FT-nnn` (recebida por esta pessoa) | identifica a fatia pai → assume `[VER]` no EWM (responsável = `whoami`, inicia) com "sim" → encaminha para **`sdd-verificar`**, passando: fatia, pasta spec, branch |
| "próxima fatia" | a `pronta` de maior prioridade da sprint aberta sem `status.md` em nenhuma branch (no Kanban, a do topo do backlog) |
| `EP-nn` sem `[ESP]` assumida | não é fatia: **`sdd-prd`** (se PRD ainda não existe) ou **`sdd-fatiar`** (se PRD aprovado) |
| `EP-nn` com tarefa `[ESP]` no EWM (estado: `Novo` ou `Em andamento`) | fluxo [ESP] → Passo 4a |
| pedido em texto, ou id que não está no backlog | não está registrado → carregue a **`sdd-triar`**: ela registra e, se a pessoa quiser começar agora, volta aqui com o id |

Para tarefas `[REV]` e `[VER]`: não cria branch nova (a branch da fatia já existe); não repete o Passo 3
(compromisso); vai diretamente para `sdd-revisar` ou `sdd-verificar` após assumir no EWM. Sem o MCP → `ELM
pendente: assumir [REV|VER] FT-<nnn>` e encaminha da mesma forma.

Fatia já iniciada (tem pasta em `.kiro/specs/` nesta branch, em worktrees ou em branches remotas —
`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) → leia o `status.md` e **retome** pela fase (Passo 5),
sem repetir o Passo 3. Branch diferente da atual → pergunte se troca (alterações locais não commitadas → avise e
pare; nunca ofereça descartar, `stash` ou `reset`).

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

## Passo 4 — Pasta, branch e item

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
4. **EWM** (com power `elm`, pergunta única; nunca sem "sim"): assumir a **tarefa** de quem implementa (ex.:
   `[DEV]`; o item de backlog continua do P.O.) com responsável = `whoami`, iniciá-la (ação de
   `ccm_list_workitem_states`), estimativa se faltar. Tarefa ainda não existe (encaixe aprovado agora, Kanban, ou
   publicação que falhou no planejamento) → `sdd-elm` modo *sprint* cria as da trilha (pai sempre definido):

   | Fatia | Tarefas | Pai |
   |---|---|---|
   | de épico (padrão) | `[DEV]` `[REV]` `[VER]` | IB da fatia, filho do épico |
   | sem épico, com item de origem (DF, IB) | `[DEV]` `[REV]` `[VER]` — direta: só a `[DEV]` | o próprio item de origem — **sem IB novo** |
   | sem épico, pedido em texto | `[DEV]` `[REV]` `[VER]` — direta: só a `[DEV]` | IB `[FT-nnn]`, filho do épico de Sustentação — direta: o épico de Sustentação |

   Grave os ids das tarefas no campo ELM do `status.md` — é por ele que as horas acham a tarefa. Chamada daqui, na
   branch da fatia, a `sdd-elm` não grava o `backlog.md` nem o `sprint-<nn>.md`: os ids ficam no `status.md`, e a
   `sdd-consolidar` os leva ao backlog. Sem o MCP: `ELM pendente` no `status.md`.
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

## Passo 4a — Fluxo [ESP] (tarefa de especificação de épico)

Para `EP-nn` com tarefa `[ESP]` detectada no Passo 1:

1. **DoR mínima do épico:** título (>5 palavras), descrição do problema (>2 frases), P.O. definido no `backlog.md`
   ou no EWM. Faltando → liste e pare: a `sdd-triar` completa o registro antes de começar.
2. **Pasta do épico:** verifique se `<produto>/epicos/<EP>-<slug>/` existe; se não → crie com `decisoes.md`
   (só o cabeçalho da tabela `D | Pergunta | Decisão | Fonte | Data | Situação`) e `rascunho.md` (título e
   descrição do item EWM, sem dado inventado).
3. **Assumir:** pela `sdd-elm` modo *sprint* — assuma a `[ESP]` com responsável = `whoami` e inicie-a
   (`ccm_list_workitem_states`), com confirmação ("sim"). Sem MCP → `ELM pendente: assumir [ESP] EP-<nn>` na
   pasta do épico.
4. **Encaminhar:**
   ```
   🚦 EP-<nn> — <título> · [ESP] assumida · fase: especificando
   Pasta: <produto>/epicos/<EP>-<slug>/
   Próximo: sdd-pesquisar (ler código e bundle do ELM) → sdd-entrevistar → sdd-prd
   ```
   **NÃO** cria branch de fatia. **NÃO** cria `status.md` de fatia. **NÃO** registra em sprint de fatia.
   O trabalho de especificação é feito na branch base; as horas são lançadas na `[ESP]` ao concluir.

## Regras

- Só começa o que está registrado e planejado: pedido novo ou item fora do backlog vai para a `sdd-triar`; fatia
  fora da sprint, para o encaixe.
- O EWM (ou a pessoa) é a fonte dos dados do item; o código, do comportamento atual; o `status.md`, da fase.
- Toda troca/criação de branch e toda alteração no EWM só com "sim".
- Nunca invente dados de work item.
