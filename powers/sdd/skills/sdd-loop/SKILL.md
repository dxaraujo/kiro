---
name: sdd-loop
description: "Execução autônoma (AFK) de várias fatias do fluxo sdd — pega a fronteira de fatias AFK prontas e desbloqueadas, cria uma worktree e uma branch por fatia (em .kiro/local/wt/) e leva cada uma da pesquisa ao PR pronto, uma fase por subagente de contexto limpo do sdd-orquestrador (pesquisador, codificador, revisor, verificador), com backpressure, até 2 rodadas de revisão, parada em bloqueio e limite de WIP pela capacidade de revisão humana. Retomável pelo log em .kiro/local/. Use em \"roda as fatias AFK\", \"modo AFK\", \"leva a FT-031 e a FT-032 até o PR\", \"trabalha sozinho nas prontas da sprint\", \"retoma o loop\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.3.0"
---

# sdd-loop — Fatias AFK até o PR

Quem executa é o agente **`sdd-orquestrador`** (ou a sessão da pessoa, com os mesmos passos). Ele coordena e
registra; cada fase é feita por um subagente que começa do zero e lê o estado do disco. A pessoa fica **sobre** o
loop, não dentro: aprova o lote no início, um Dev Sênior aprova os planos que pedem GATE e lê cada PR no fim (tarefas
`[APR]`); quem disparou o loop é o Dev responsável e faz o merge de cada PR aprovado (Passo 6 da `sdd-desenvolver`).

Leia antes: `.kiro/steering/sdd.md` (seções Git, banco e autonomia e Comandos) e
`<produto>/acordos.md` (WIP; sem o arquivo, limite 2).

**Quem dispara** tem de ser Dev **Pleno** ou **Sênior** (`senioridade` no `equipe.json` da base): é o responsável
das `[DEV]` do lote. Júnior → diga que Júnior implementa sempre em HITL, uma fatia por vez pela `sdd-desenvolver`,
e pare.

## Passo 0 — Retomar?

Existe `.kiro/local/loop-*.md` com fatias não finalizadas → mostre o estado (fatia, fase, rodada, último resultado)
e pergunte se retoma. Retomar = continuar cada fatia da fase registrada no `status.md` dela.

## Passo 1 — Fronteira e lote

1. Candidatas: as fatias pedidas, ou as `pronta` + `AFK` da sprint atual, em ordem de prioridade — sempre **sem
   `status.md`** em nenhuma branch ou worktree (já em andamento). Fatia pedida fora da sprint aberta → a regra de
   puxar da `sdd-desenvolver` (Passo 3, item 3): é a `pronta` do topo e o WIP tem folga → entra no lote como
   **puxada** (`Puxada para a sprint <nn>` no Histórico); fura a fila → fica de fora até o encaixe
   (`sdd-planejamento`, seção Encaixe). Kanban
   (`acordos.md`): não há sprint nem encaixe — vale a `pronta` do topo do backlog, e as `[DEV]` do lote nascem na
   confirmação ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §4, iteração corrente).
2. Fica de fora (diga o motivo): HITL; `EP-nn`, PRD, fatiamento e `AT-nnn`
   ("PRD, backlog e Apoio nunca são AFK"); Definition of Ready não atendida; `bloqueada-por` não concluída e
   não presente antes no lote; já em andamento (tem `status.md`).
3. **Limite:** paralelismo do `sdd.md` (padrão 1, máximo 3) **e** vagas de WIP de revisão humana (limite
   dos acordos menos as fatias já esperando pessoa: `plano-em-revisao`, `pr-aberto`, `em-revisao`,
   `em-verificacao`, `aceita`, `pronta-para-merge`). PR que ninguém vai
   revisar hoje não deve ser produzido hoje.
4. Proposta — **uma confirmação para o lote todo**:
   ```
   🤖 Loop AFK — <n> fatias · paralelo <p> · base <branch>
   | FT | Título | Branch | Worktree |
   |---|---|---|---|
   | FT-031 | Bloquear a conta após 3 tentativas | feature/ft-031-bloquear-conta | .kiro/local/wt/ft-031 |
   GATE do plano (senioridade de quem dispara): Sênior → sem GATE (plano do Sênior) · Pleno → quer a aprovação de
   um Dev Sênior nos planos deste lote? (sim: [APR] para <login> | não) — a escolha vale para o lote
   Aprovação dos PRs: [APR] Aprovar PR para <Dev Sênior> (sugestão: outro que não quem dispara; ele mesmo só se
   for o único Dev Sênior ativo)
   Plano com risco (regra sensível, muitos cenários, integração externa, mudança de dado) → a fatia para em
   bloqueada com a sugestão de troca para HITL, o P.O. é avisado e o loop segue com as outras
   Ao fim de cada fatia aprovada e aceita: push + PR? (sim/não)   — nunca merge; só se o sdd.md diz
   "perguntar a cada lote" (com "não — a pessoa abre", omita a linha: o loop para em `aceita`)
   EWM: assumir as [DEV] do lote (responsável: <login de quem dispara>) e colocá-las em andamento; criar cada
   [APR] quando a fatia chegar ao gate — no AFK não há [REV] nem [VER]: revisão e verificação são dos subagentes
   Confirma?
   ```
   Com "sim" e o MCP `elm`: fatia sem `[DEV]` (puxada, ou publicação que falhou) → crie-a ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md)
   §3–4: antes o IB sai do backlog do EWM para a iteração da sprint — `pendente`, crie-o; pai sempre definido —; das tarefas, só a `[DEV]`, AFK); depois `elm_transicao(<id>, "assumir", iniciar_pai: true)` em cada `[DEV]`; sem o MCP `elm` ou com falha → `ELM pendente [<chave>]: assumir a
   tarefa` no `status.md` de cada fatia.
5. Log `.kiro/local/loop-<AAAA-MM-DD-HHMM>.md` (formato no fim).

## Passo 2 — Worktree por fatia

As worktrees ficam **dentro** do workspace, em `.kiro/local/wt/<ft>/` (ignorado pelo git), para que os agentes
alcancem os arquivos com as permissões deles:

```bash
git fetch --quiet
git worktree add .kiro/local/wt/<ft> -b <branch> origin/<base>     # nova
git worktree add .kiro/local/wt/<ft> <branch>                      # já existe
```

Dentro da worktree, faça só os itens 2 e o commit do item 5 do Passo 4 da **`sdd-desenvolver`** (pasta, `status.md`
com `Responsável: agente:sdd-orquestrador`, `.config.kiro`), sem perguntas — o lote já foi confirmado. O EWM
já foi tratado na confirmação do lote (Passo 1) e não há push nesta hora. O `backlog.md` não muda
(ele só é escrito na base).

**Comandos dentro da worktree** — diga isto a cada subagente: git, build e testes com
`cd .kiro/local/wt/<ft> && <comando>` (o `git -C` é bloqueado nos agentes: com ele as regras de permissão não
enxergam o subcomando); arquivos pelo caminho `.kiro/local/wt/<ft>/<caminho>`. Ferramentas que varrem a raiz
(alguns test runners, linters) podem enxergar `.kiro/local/`: se o projeto tiver esse risco, a setup registra a
exclusão.

## Passo 3 — Fases (por fatia; fatias diferentes em paralelo até o limite)

Cada fase é um subagente novo recebendo **só**: `AUTONOMO=true`, id da fatia, o caminho da worktree
(`.kiro/local/wt/<ft>`) e da pasta da fatia dentro dela, como rodar comandos ali (Passo 2) e a rodada. Nunca o
raciocínio de outra fase. Com **Workflows** ligado no Kiro, a delegação a um agente pode virar uma execução em
segundo plano: espere a de cada fase terminar (artefato gravado, `status.md` atualizado) antes de abrir a
seguinte da mesma fatia.

| # | Fase | Subagente | Sai quando |
|---|---|---|---|
| 1 | pesquisa | `sdd-pesquisador` (`sdd-pesquisar`) | `research.md` gravado |
| 2 | plano | `sdd-codificador` (`sdd-plano`, Passos 2–3) | spec do Kiro gravada · ou `bloqueada` |
| 3 | análise do plano | `sdd-revisor` (rubrica L) → `sdd-codificador` corrige | `ANALISE: OK` · 2 rodadas sem OK → `bloqueada` |
| 4 | troca e GATE do plano | você | o Passo 5 da `sdd-plano`, sem pessoa: plano com risco → `fase: bloqueada (de: planejando)`, `aguardando troca para HITL` com o risco, commit, horas da sessão na `[DEV]` no fim do lote, o P.O. avisado no resumo, e siga com as outras · GATE pela escolha do lote: Sênior, ou Pleno que dispensou → `fase: implementando` (Histórico `plano do Sênior` · `Pleno dispensou o GATE do plano`) e siga · Pleno que pediu → `fase: plano-em-revisao` (`Responsável` = o Dev Sênior do lote), a `[APR] FT-<nnn> Aprovar plano` ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §8), commit do plano e, com push autorizado no lote, push e conferência; **pare esta fatia** e siga com as outras (retoma depois do GATE) |
| 5 | implementação | `sdd-codificador` (`sdd-implementar`, Passos 0–2) | tarefas `[x]` e backpressure verde · ou `bloqueada` |
| 6 | revisão do código | `sdd-revisor` (rubrica C) → volta à 5 com os achados | `VEREDITO: APROVADO` · 2ª reprovação → `bloqueada` |
| 7 | verificação | `sdd-verificador` (`sdd-verificar`) | `ACEITO` · `REJEITADO` → volta à 5 com os cenários rejeitados (retrabalho: linha na tabela Retrabalho do `status.md`, Rodadas `retrabalho` + 1) e **passa de novo pela 6** antes da 7; de novo rejeitado → `bloqueada` |
| 8 | entrega | você | `fase: aceita`; commit do que faltar; push, conferência no remoto (`git rev-parse HEAD` = `git rev-parse origin/<branch>`, na worktree) e PR se autorizado no lote (ADRs, texto e `gitlab_criar_mr` do Passo 5 da `sdd-implementar`, com `origem` = a branch da worktree — o MCP roda no checkout principal e não a enxerga; o Kiro ainda pode pedir confirmação a cada push e a cada PR, conforme as permissões) → a `[APR] FT-<nnn> Aprovar PR` para o Dev Sênior do lote ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §8) → `fase: pronta-para-merge` com o link do PR no `status.md`, commit, push e conferência (item 3 do Passo 5 da `sdd-implementar`); a `[DEV]` fica em andamento; sem PR autorizado → fica `aceita` |

Depois de cada fase: grave a fase seguinte (`planejando` depois da pesquisa, `revisando` antes da revisão do
código), atualize o log, as Rodadas e o Histórico do `status.md` — nas fases 6 e 7, também o campo **Drift de
negócio** com a linha do relatório (só sobe de `não` para `sim`); **commite imediatamente** na worktree os
relatórios que chegaram nesta fase — `analise-plano-<N>.md` (fase 3), `revisao-codigo-<N>.md` (fase 6),
`verificacao.md`, `CT.csv`, `evidencias/` e `massa/` (fase 7) — antes de iniciar a fase seguinte. Esses arquivos não são commitados
pelos subagentes que os geram; o orquestrador é o responsável pelo commit deles.

**Aprovação de plano pausado:** é do Dev Sênior da `[APR]`, na sessão dele, pela `sdd-revisar` (Aprovação do plano)
(no mesmo checkout do loop, ele trabalha na worktree — `cd .kiro/local/wt/<ft>` — em vez do `git switch`; sem push
autorizado, só assim). Ao retomar: `git pull --ff-only` na worktree (com upstream) e leia a fase — `implementando` →
fase 5 (Passo 0); `planejando` com o ajuste pedido → codificador (`sdd-plano`, replanejar), nova análise e fase 4.
Aprovação dita nesta sessão não vale.

**Aprovação do PR:** é do Dev Sênior da `[APR]`, pela `sdd-revisar` (Aprovação do PR). Mudanças pedidas →
`retrabalho (de: pronta-para-merge)`: a fatia volta à fase 5 com os achados (retome-a num lote, ou o Dev pela
`sdd-implementar`).

Os **Kiro Workflows** do sdd (se instalados) não fazem parte do loop: são receitas que a pessoa dispara para
**uma** fatia, na branch dela, no checkout principal.

## Passo 4 — Parada

- **Fatia bloqueada** (lacuna de negócio, divergência com o plano, 2 reprovações, verificação rejeitada duas
  vezes) → registre o motivo e a pergunta exata no `status.md`; siga com as outras.
- **Problema sistêmico** (build quebrado na base, o mesmo `⚠️ ambiente` ou o mesmo erro em **duas** fatias) →
  **pare o lote inteiro**: o loop não conserta ambiente. `⚠️ ambiente` numa fatia só → ela fica `bloqueada (de:
  verificando)` e o lote segue com as outras.
- Ao fim, o resumo:
  ```
  🤖 Loop AFK — resultado
  | FT | Resultado | PR | Rodadas (plano/código/aceite) | Observação |
  Aguardando pessoa: <planos para aprovar ([APR] de <login>) · PRs para ler e aprovar ([APR] de <login>) · trocas
  para HITL (P.O., `sdd-planejamento`) · bloqueios com pergunta>
  Merge: cada PR com a [APR] concluída → você, pela `sdd-desenvolver` Passo 6 ("mergeia a FT-<nnn>")
  ELM pendente [<chave>]: <o que falhou ou ficou sem o MCP `elm`>
  Lições para registrar: <correções que o loop precisou — sdd-aprender>
  ```
- **Horas, numa pergunta só** (com o MCP `elm`): uma tabela `tarefa | horas sugeridas` com as `[DEV]` das
  fatias que chegaram a `aceita` (com ou sem PR aberto) ou pararam para a troca para HITL; a pessoa ajusta e confirma de uma vez → `elm_horas(<id>)` →
  desconte → `elm_lancar_horas` (lança, não conclui). A conclusão da `[DEV]` é no merge de cada fatia (Passo 6 da `sdd-desenvolver`), com
  o saldo. No AFK, revisão e verificação por subagente não têm tarefa nem horas; as das `[APR]` são lançadas por
  quem aprova, na sessão dele.
- **Créditos:** o Kiro grava o consumo do turno só quando ele termina, por isso o lote não os registra: no resumo,
  `Créditos: no merge de cada fatia, rateio 1/<n> desta sessão (<FT…>)` — o Dev grava a parte de cada fatia no
  Passo 6 da `sdd-desenvolver` ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4).
- Worktrees ficam até o merge; quem conduz o merge as remove logo depois (item 8 do Passo 6 da
  `sdd-desenvolver`), sem `--force` — os agentes não podem (`git worktree remove` é negado a todos): entregam o
  comando e a pessoa o roda.

## Log `.kiro/local/loop-<data>.md`

```markdown
# Loop AFK <data> — paralelo <p> · push/PR: <sim|não>
| FT | Worktree | Branch | Fase | Rodada | Último resultado | Atualizado |
|---|---|---|---|---|---|---|
```

## Regras

- O orquestrador nunca faz merge (é de quem disparou o loop, depois da aprovação do PR), nunca `--force`, nunca
  push sem a autorização do lote; todo push é conferido no remoto antes do PR.
- ELM só pelo que o lote confirmou (assumir `[DEV]`, estados, criar as `[APR]` nos gates) e pelas horas do fim; nada mais (a conclusão da `[DEV]` é no merge). Sem o MCP `elm` ou com
  falha → `ELM pendente [<chave>]: …` no `status.md`.
- Nunca relaxe um gate para o loop andar: bloqueio é informação, não falha.
- Tipo de fatia que bloqueia com frequência → sugira na retrospectiva tratá-lo como HITL.
