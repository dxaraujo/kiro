---
name: sdd-desenvolver
description: "Skill do papel Dev no fluxo sdd — começa ou retoma uma fatia já registrada no backlog (FT-031, DF ou IB que o backlog conhece, tarefa [DEV]), em qualquer trilha. É o ponto de compromisso: confere a Definition of Ready, o responsável, a sprint aberta (fora dela, encaixe pela sdd-planejamento) e o WIP; cria a branch (sugere o nome e aguarda) e a pasta .kiro/specs/ com o status.md, assume a [DEV] no EWM (com confirmação) e encaminha pela fase: pesquisar → plano → implementar → PR. Em pronta-para-merge, faz o merge do PR aprovado, grava as lições da fatia e conclui a [DEV]. Pedido novo vai para a sdd-triar; [REV], [VER], [ESP] e Apoio têm skill própria (o hub sdd-iniciar encaminha). Use em \"vamos trabalhar na FT-031\", \"pegar a [DEV] da FT-031\", \"corrigir o defeito 4567\", \"próxima fatia\", \"retomar a FT-031\", \"mergeia a FT-031\", \"o PR da FT-031 foi aprovado\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.3.1"
---

# sdd-desenvolver — Compromisso e início do código

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-desenvolver/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Começar é um compromisso: daqui em diante a fatia consome a capacidade do time e o lead time corre. Por isso esta
skill só começa o que já está registrado e planejado; a entrada de trabalho novo é da **`sdd-triar`**. É a skill do
papel **Dev**: assume a `[DEV]` da fatia (Passo 4), encaminha cada fase para a skill dela (Passo 5) e encerra a `[DEV]` no merge do PR aprovado (Passo 6). Revisão (`[REV]`), verificação (`[VER]`), especificação
(`[ESP]`) e Apoio (`[ATD]`, `[IMPL]`…) têm skill própria; na dúvida sobre o item, o hub **`sdd-iniciar`** diz qual.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Passo 1 — O que chegou

**Ordem de consulta** para qualquer id (`FT-031`, número do EWM) — vale a primeira fonte que achar, e nunca se
inventa dado de work item: (1) `status.md` nas branches (atual, worktrees, remotas); (2) o `backlog.md` da base
(ids locais e as colunas `origem` e `elm`); (3) o EWM (`elm_ler_wi`), se a sessão tem o MCP `elm`;
(4) perguntar à pessoa. O EWM e a pessoa só completam dados: id que não está em (1) nem (2) não está registrado →
`sdd-triar`. A `fase` do `status.md` decide se o papel pode começar.

| Entrada | Como ler |
|---|---|
| `FT-nnn` | `<produto>/backlog.md` e a ficha da fatia (coluna `ficha`; de épico, também o PRD que ela cobre) |
| número do EWM (DF, IB) | a linha do `backlog.md` com esse id em `origem` ou `elm` |
| tarefa `[DEV] FT-nnn` | a fatia do pai |
| "próxima fatia" | a `pronta` de maior prioridade da sprint aberta sem `status.md` em nenhuma branch; nenhuma → a `pronta` do topo do backlog, também sem `status.md` em branch ou worktree (puxada; no Kanban, sempre esta) |
| `[REV]`, `[VER]`, `EP-nn`/`[ESP]`, item ou tarefa de Apoio (`AT-nnn`/`[ATD]`, `IM-nnn`/`[IMPL]`…) | não é deste papel → "use `sdd-iniciar <item>`" e pare |
| pedido em texto, ou id que não está no backlog | não está registrado → "use `sdd-triar`" e pare |

Fatia já iniciada (tem pasta em `.kiro/specs/` nesta branch, em worktrees ou em branches remotas —
`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) → leia o `status.md` e **retome**: Passo 4, item 4
(assumir: já minha e em andamento → `ja_estava`, nada a fazer) e Passo 5, sem repetir o Passo 3. Branch
diferente da atual → pergunte se troca (alterações locais não commitadas → avise e pare; nunca ofereça descartar,
`stash` ou `reset`). **Branch aberta numa worktree** (`git worktree list` mostra `.kiro/local/wt/<ft>` com ela —
fatia do `sdd-loop`): não troque, o `git switch` falha; trabalhe na worktree — comandos com
`cd .kiro/local/wt/<ft> && <comando>`, arquivos pelo caminho `.kiro/local/wt/<ft>/<caminho>` — e passe isso à
próxima skill. Vale para todas as skills de papel que precisam da branch da fatia.

**Troca AFK → HITL** (fatia em `bloqueada (de: <fase>)` com `aguardando troca para HITL`, ou com `Modo: AFK` no
`status.md` e `HITL` no `backlog.md`): leia a base sem trocar de branch — `git fetch` e `git show origin/<base>:<produto>/backlog.md` e
`…/sprints/<pai>/sprint-<nn>.md`. A troca só vale registrada lá pelo P.O. (ou SM): `modo` `HITL` no backlog e a
Observação `modo: AFK → HITL (…)` na linha da fatia. Registrada → mostre e, com "sim", grave no `status.md`
`Modo: HITL`, o revisor e o verificador (Histórico) e os ids da `[REV]` e da `[VER]` (campo ELM, da coluna "Tarefa
ELM"), `Bloqueio: —` e a fase de origem (`planejando`); commit e push. A `[DEV]` é retomada por
`elm_transicao(<id>, "assumir")` (já minha e em andamento → nada a fazer). Siga no HITL: `sdd-plano` Passo 5, com o GATE pela
senioridade. Recusada (Observação `modo: AFK mantido`) → `Bloqueio: —`, fase de origem, segue no AFK. Nenhuma das duas → diga
que a troca é do P.O. (`sdd-planejamento`, Troca de modo) e pare. O Dev não
grava na base nem cria ou cancela tarefa. **HITL → AFK nunca:** `Modo: HITL` no `status.md` e `AFK` no backlog →
avise a divergência ao P.O. e siga no HITL.

## Passo 2 — Trilha

A trilha vem do registro, não de uma triagem nova: fatia de uma seção de épico → **padrão**; da seção
`## Fatias — sem épico` → a da coluna `trilha` (seção antiga `## Fatias — trilha rápida` → **rápida**). Ao ler o
item, a trilha registrada não serve (a "rápida" tem regra de negócio nova)
→ pare e devolva à `sdd-triar` para refazer a triagem.

| Trilha | Caminho depois daqui |
|---|---|
| **padrão** | pesquisa → plano → **GATE do plano** → implementação → revisão → verificação → PR |
| **rápida** | pesquisa curta → `bugfix.md` + `tasks.md` (o teste que reproduz primeiro) → implementação → revisão → verificação → PR |

## Passo 3 — Compromisso

Vale para todas as trilhas. Tudo conferido **antes** de criar branch ou mexer no EWM; falhou um item → diga qual e
o caminho, e não comece.

1. **Definition of Ready** da trilha — a do formato do backlog
   ([../sdd-fatiar/references/backlog.md](../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-pronta),
   mais os itens próprios do `acordos.md`): a fatia está `pronta` ou passa agora.
   - Falhou → `sdd-entrevistar`, `sdd-fatiar` (refinamento) ou `sdd-triar` (retomar a triagem: ficha e `falta:` das
     fatias sem épico).
2. **Responsável.** A coluna `responsavel` do `backlog.md` é outra pessoa → pergunte se ela sabe; trocar é do
   planejamento, não grave aqui. Quem vai implementar é **Júnior** (`senioridade` no `equipe.json`) e a fatia é
   `AFK` → não comece: avise que Júnior implementa sempre em HITL e mande para a **`sdd-planejamento`** (o modo sai
   da senioridade de quem implementa).
3. **Sprint.** Nada começa sem item planejado: é na tarefa da sprint que as horas são lançadas. A
   fatia está na sprint aberta (`sprint` do `backlog.md` = a do `sprint-<nn>.md` com `**Situação:** aberta`)? Não
   está → **puxe** (fluxo puxado, a sprint é cadência): se ela é a `pronta` do topo do backlog — nenhuma `pronta`
   de prioridade maior esperando, dentro ou fora da sprint — e o WIP do item 4 tem folga, ela entra na sprint
   aberta sem cerimônia: `Puxada para a sprint <nn>` no Histórico ao criar o `status.md`, e as tarefas nascem na
   iteração da sprint (Passo 4). Fura a fila ou estoura o WIP → **Encaixe**: a decisão é do P.O., pela
   **`sdd-planejamento`** (seção Encaixe); sem a decisão registrada, não comece. Kanban (`acordos.md`) → não há sprint nem encaixe: as tarefas
   nascem na iteração corrente do EWM ao começar (Passo 4). Nenhuma sprint aberta e nada no
   `acordos.md` (planejamento ainda não feito) → não é encaixe: ofereça a `sdd-planejamento` e não comece.
4. **WIP** (`<produto>/acordos.md`; sem o arquivo, 2 fatias esperando pessoa). Conte as fatias em
   `plano-em-revisao`, `pr-aberto`, `em-revisao`, `em-verificacao`, `aceita` e `pronta-para-merge` nos `status.md`
   das branches, como a `sdd-status`. No limite, ou com PR
   parado há mais tempo que o acordo (padrão 1 dia) → mostre quais e recomende destravar antes (aprovar o plano,
   revisar o PR). A pessoa pode seguir mesmo assim: `WIP excedido: <motivo>` vai no Histórico do `status.md` ao
   criá-lo (Passo 4).
5. **Registro publicado.** A linha da fatia, a ficha e o encaixe já estão em `origin/<base>`
   (`git grep -q '<FT>' origin/<base> -- <produto>/backlog.md`)? Só no local → peça o push
   antes: a branch nasce de `origin/<base>`, e um id que ainda não chegou lá pode mudar. Repositório sem remoto
   (ou base nunca publicada) → não há o que conferir: a branch nasce da base local; diga isso e siga.

## Passo 4 — Branch, pasta e `[DEV]`

1. **Branch** — sugira e **aguarde**:
   ```
   Branch sugerida: <prefixo do sdd.md><ft>-<slug>   (ex.: feature/ft-031-bloquear-conta)
   Confirma, ou informe outro nome:
   ```
   Confirmado → `git fetch` e `git switch -c <branch> origin/<base>`.
2. **Pasta** `.kiro/specs/<ft>-<slug>/` com `status.md` de [references/status-template.md](references/status-template.md)
   e o `.config.kiro` da spec do Kiro (`specType` `feature` na trilha padrão, `bugfix` na rápida — formato em
   [../sdd-plano/references/plano-templates.md](../sdd-plano/references/plano-templates.md)).
3. **Backlog:** não muda aqui (ele só é escrito na base, pela `sdd-triar`, `sdd-fatiar`, `sdd-planejamento` e
   `sdd-consolidar`); a fatia em andamento é a que tem `status.md` numa branch.
4. **Assumir a `[DEV]`** (com o MCP `elm`; nunca sem "sim") — `elm_transicao(<id da [DEV]>, "assumir",
   iniciar_pai: true)`, com `estimativa_h` se faltar (regras: [elm.md](../sdd/references/elm.md)). O item de backlog continua do P.O.
   Tarefa ainda não existe (encaixe aprovado agora, Kanban, ou publicação que falhou no planejamento) → antes, o
   IB (ou o item de origem) sai do backlog do EWM para a iteração da sprint (`elm_atualizar_wi(id, iteracao)`; `elm`
   `pendente` → crie-o) e crie as tarefas da trilha ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3–4; pai sempre definido):

   | Fatia | Tarefas | Pai |
   |---|---|---|
   | de épico (padrão) | `[DEV]` `[REV]` `[VER]` | IB da fatia, filho do épico |
   | sem épico, com item de origem (DF, IB) | `[DEV]` `[REV]` `[VER]` | o próprio item de origem — **sem IB novo** |
   | sem épico, pedido em texto | `[DEV]` `[REV]` `[VER]` | IB `[FT-nnn]`, filho do épico de Sustentação |

   Fatia **AFK**: só a `[DEV]`, em qualquer linha — revisão e verificação são subagentes, sem tarefa. Fatia
   **HITL puxada** (não passou pelo planejamento, sem revisor nem verificador na sprint) → antes de criar `[REV]`
   e `[VER]`, pergunte quem revisa e quem verifica (sugira pelo `equipe.json`: papéis, `senioridade` e
   `horas-revisao-semana`): o revisor é um **Dev Sênior** ativo que não é quem implementa — quem implementa é o
   único Sênior ativo → ele mesmo, com `revisor único`; o verificador nunca é quem implementa. Grave no Histórico ao
   lado de `Puxada para a sprint <nn>`; a `sdd-consolidar` leva para a linha `puxada` do `sprint-<nn>.md`.

   Grave os ids das tarefas no campo ELM do `status.md` — é por ele que as horas acham a tarefa. Chamada daqui, na
   branch da fatia, não grave o `backlog.md` nem o `sprint-<nn>.md`: os ids ficam no `status.md`, e a
   `sdd-consolidar` os leva ao backlog. Sem o MCP `elm`: `ELM pendente [DEV FT-<nnn> assumir]` no `status.md`.
5. Commit pequeno do `status.md` e do `.config.kiro` e, com "sim", push da branch — é o sinal para o time de que a fatia começou.

## Passo 5 — Encaminhar

```
🚦 FT-<nnn> — <título>   ·   trilha <…> · modo <AFK|HITL> · fase <…>
Épico: <EP — título | — (sem épico)> · Cobre: <… | ficha C1–Cn | origem …> · Branch: <…> · Pasta: .kiro/specs/<ft>-<slug>/
Próximo: <skill>
```

| Fase | Próxima skill |
|---|---|
| `pesquisando`, `planejando`, `plano-em-revisao` | `sdd-plano` (que começa pela `sdd-pesquisar`) |
| `implementando`, `revisando`, `retrabalho (de: …)` | `sdd-implementar` |
| `verificando` | `sdd-verificar` (AFK) |
| `aceita` | `sdd-implementar` (Passo 5 — abrir o PR) |
| `pr-aberto`, `em-revisao` | HITL: com o revisor — `[REV]` pela `sdd-revisar` |
| `em-verificacao` | HITL: com o verificador — `[VER]` pela `sdd-verificar` |
| `pronta-para-merge` | Dev: **Passo 6** desta skill (merge do PR aprovado e conclusão da `[DEV]`) |
| `mergeada` | nada para o Dev: a consolidação é do P.O. ou do SM — `sdd-consolidar` (agente `sdd-produto`) |
| `bloqueada (de: <fase>)` | mostre o motivo e a pergunta; resolvido → volta à skill da fase de origem. `aguardando troca para HITL` → a troca é do P.O. (`sdd-planejamento`, Troca de modo); registrada, a Troca AFK → HITL do Passo 1 |

Modo AFK e várias fatias padrão ou rápida prontas na sprint → ofereça o **`sdd-loop`** (o agente leva cada uma até
o PR). Uma fatia só, com as receitas instaladas (`.kiro/workflows/sdd-*`) → diga que a pessoa pode dispará-las no
chat ("rode o workflow `sdd-planejar-fatia` com fatia FT-<nnn>"; AFK, depois `sdd-entregar-fatia`) — quem dispara
receita é sempre a pessoa, nunca uma skill ou agente.

Diga a próxima e **pare**: nunca invoque nem simule a skill da fase — ela começa na própria invocação. A
exceção é `pronta-para-merge`: o Passo 6 é desta skill.

## Passo 6 — Encerrar a `[DEV]`: merge do PR aprovado

A fatia chegou a `pronta-para-merge`: o merge e a conclusão da `[DEV]` são do Dev responsável, aqui. Vale a aprovação
**registrada**, nunca a dita na conversa ("o PR foi aprovado", "pode mergear"; o P.O. não aprova PR):
- **HITL:** revisão `APROVADO` e verificação `ACEITO` registradas (é o que leva a fatia a `pronta-para-merge`);
- **AFK:** a `[APR] FT-<nnn> Aprovar PR` está **concluída** e tem o comentário `PR aprovado, sha <sha>` (`elm_ler_wi(<id>,
  comentarios: true)`, só leitura). Sem o MCP `elm` → a linha `PR aprovado por <login>, sha <sha>` que o
  aprovador entregou. Sem a aprovação → avise que o PR espera a leitura do Dev Sênior e pare.

1. **Leia o PR:** `gitlab_obter_mr` pelo `iid` do link no `status.md`. Tem de estar aberto, sem WIP/Draft e sem
   conflito. `merged` → vá ao item 5; `closed`, WIP ou conflito → avise e pare (conflito: atualize a branch pelo
   item 1 do Passo 5 da [`sdd-implementar`](../sdd-implementar/SKILL.md), e a mudança passa de novo pela revisão).
2. **Commit aprovado:** o `sha` do PR = `git rev-parse origin/<branch>` e é o commit que foi aprovado — HITL: o da
   entrega da verificação (o último commit que mudou o `verificacao.md`, `git log -1 --format=%H -- <pasta da fatia>/verificacao.md`, e nele o veredito `ACEITO` — não depende do padrão de mensagem do projeto); AFK: o `sha` do
   comentário da `[APR]`. Commit depois da aprovação → não mergeie:
   a mudança volta à revisão.
3. **Resumo e confirmação:**
   ```
   🔀 Merge FT-<nnn> — <título>
   PR !<iid> <origem> → <destino> · sha <curto> · aprovado: <REV APROVADO + VER ACEITO | por <login>>
   Mergear? (sim/não)
   ```
4. **Merge:** `gitlab_mesclar_mr(iid, sha=<sha aprovado>, remover_origem=false)` — o Kiro também confirma; a branch
   fica até a consolidação (guarda o `status.md` com `mergeada`). Sem o MCP, sem permissão de merge ou recusa do
   GitLab → a pessoa faz o merge na UI do GitLab e diz "mergeado".
5. **Confira:** `gitlab_obter_mr(iid)` (ou `gitlab_listar_mrs(origem=<branch>, estado=merged)`) com estado `merged`
   — inclusive no merge pela UI. Sem o MCP → `git fetch` e `git diff origin/<base> origin/<branch> -- <arquivos que
   a fatia mudou>` vazio. Não mergeado → pare.
6. **Lições da fatia** — antes de fechar a `[DEV]`: liste as correções humanas que a fatia recebeu (tabela
   Retrabalho; Achados abertos de origem PR ou GATE do plano; bloqueio resolvido por uma pessoa; "não é assim" no
   Histórico) e, com a pessoa, grave uma linha por correção na seção **Lições candidatas** do `status.md`: feito ×
   certo, onde estava o certo e a causa proposta (tabela de causas da [`sdd-aprender`](../sdd-aprender/SKILL.md)).
   Correção sem lição (ambiente, digitação) → causa `—`; nenhuma correção → `nenhuma`. O `licoes.md` é da base:
   quem o grava é a consolidação. Depois, `status.md` (na branch da fatia): `fase: mergeada`; no Histórico, `merge do PR <link> por <login>` (AFK: antes,
   `PR aprovado por <login>`). **Créditos** na seção Créditos ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4): os desta sessão; no AFK, a linha
   da `[APR]` que veio no comentário `PR aprovado` (ou que o aprovador entregou); e a sessão do loop, que só fecha o
   consumo no fim do turno — o script a lista como sem registro: com o "sim", `rateio 1/<n>` pelas fatias do lote.
   Commit (com as Lições e os créditos), push e conferência como nos itens 1–3 da Entrega do Passo 5 da `sdd-implementar`. É
   depois do merge: um commit antes dele mudaria o `sha` aprovado.
7. **Conclusão da `[DEV]`:** mostre as horas já lançadas (`elm_horas(<id>)`) e pergunte só o saldo →
   `elm_lancar_horas(<id>, <saldo>)` e `elm_transicao(<id>, "concluir")`, numa confirmação. Sem o MCP `elm` → `ELM pendente
   [<chave>]: lançar <h>h e concluir [DEV] FT-<nnn>` no Histórico (commit e push), junto com a pendência da `[APR]`
   que o aprovador entregou (AFK).
8. **Worktree do loop** (`.kiro/local/wt/<ft>`): depois do merge, `git worktree remove .kiro/local/wt/<ft>` —
   **sem `--force`**; os agentes não podem (negado a todos): entregue o comando e a pessoa o roda. Falhou por arquivos
   não rastreados ou alterados → mostre quais (evidência com dado real fica em `.kiro/local/verificacao/`, fora da
   worktree) e deixe a pessoa decidir; nunca force.
9. **Avise o P.O. ou o SM** de que a fatia está pronta para a consolidação (**`sdd-consolidar`**, no agente
   `sdd-produto`, com horas na `[GB]`) e **pare**: a consolidação não é do Dev — o `sdd-codificador` nem grava na pasta do
   produto.

## Regras

- Só começa o que está registrado e planejado: pedido novo ou item fora do backlog vai para a `sdd-triar`; fatia
  fora da sprint, para o encaixe.
- O EWM (ou a pessoa) é a fonte dos dados do item; o código, do comportamento atual; o `status.md`, da fase.
- Toda troca/criação de branch e toda alteração no EWM só com "sim".
- Nunca invente dados de work item.
- Não invoque nem simule outra skill do fluxo: diga a próxima (Passo 5) e pare.
