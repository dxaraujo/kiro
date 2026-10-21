---
name: sdd-loop
description: "Execução autônoma (AFK) de várias fatias do fluxo sdd — pega a fronteira de fatias AFK prontas e desbloqueadas, cria uma worktree e uma branch por fatia (em .kiro/local/wt/) e leva cada uma da pesquisa ao PR pronto, uma fase por subagente de contexto limpo do sdd-orquestrador (pesquisador, codificador, revisor, verificador), com backpressure, até 2 rodadas de revisão, parada em bloqueio e limite de WIP pela capacidade de revisão humana. Retomável pelo log em .kiro/local/. Use em \"roda as fatias AFK\", \"modo AFK\", \"leva a FT-031 e a FT-032 até o PR\", \"trabalha sozinho nas prontas da sprint\", \"retoma o loop\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.6.3"
---

# sdd-loop — Fatias AFK até o PR

Quem executa é o agente **`sdd-orquestrador`** (ou a sessão da pessoa, com os mesmos passos). Ele coordena e
registra; cada fase é feita por um subagente que começa do zero e lê o estado do disco. A pessoa fica **sobre** o
loop, não dentro: aprova o lote no início e lê os PRs no fim.

Leia antes: `.kiro/steering/sdd.md` (seções Git, banco e autonomia e Comandos) e
`<produto>/acordos.md` (WIP; sem o arquivo, limite 2).

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
   confirmação (`sdd-elm` modo *sprint*, iteração corrente).
2. Fica de fora (diga o motivo): HITL; trilha direta (é da sessão da pessoa); `EP-nn`, PRD, fatiamento e `AT-nnn`
   ("PRD, backlog e atendimento nunca são AFK"); Definition of Ready não atendida; `bloqueada-por` não concluída e
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
   GATE do plano: fatias sem épico seguem com a análise L · fatias de épico param no GATE (uma pessoa aprova)
   Ao fim de cada fatia aprovada e aceita: push + PR? (sim/não)   — nunca merge; só se o sdd.md diz
   "perguntar a cada lote" (com "não — a pessoa abre", omita a linha: o loop para em `aceita`)
   EWM: assumir as [DEV] do lote (responsável: <login de quem dispara>) e colocá-las em andamento — no AFK não
   há [REV] nem [VER]: revisão e verificação são dos subagentes
   Confirma?
   ```
   Com "sim" e o power `elm`: fatia sem `[DEV]` (puxada, ou publicação que falhou) → `sdd-elm` modo *sprint* cria
   (só a `[DEV]`, AFK); depois assuma as `[DEV]` (`sdd-elm` modo *assumir*, que também inicia o IB); sem o power `elm` ou com falha → `ELM pendente [<chave>]: assumir a
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
| 4 | GATE do plano | você | a regra do Passo 5 da `sdd-plano`, na ordem dela (teste existente que muda → rápida com `GATE na trilha rápida` → épico): pede pessoa → commit do plano na worktree, **pare esta fatia** em `plano-em-revisao` (`Responsável` = quem aprova) e siga com as outras (retoma depois do GATE) · não pede → grave `fase: implementando` e siga |
| 5 | implementação | `sdd-codificador` (`sdd-implementar`, Passos 0–2) | tarefas `[x]` e backpressure verde · ou `bloqueada` |
| 6 | revisão do código | `sdd-revisor` (rubrica C) → volta à 5 com os achados | `VEREDITO: APROVADO` · 2ª reprovação → `bloqueada` |
| 7 | verificação | `sdd-verificador` (`sdd-verificar`) | `ACEITO` · `REJEITADO` → volta à 5 com os cenários rejeitados (retrabalho: linha na tabela Retrabalho do `status.md`, Rodadas `retrabalho` + 1) e **passa de novo pela 6** antes da 7; de novo rejeitado → `bloqueada` |
| 8 | entrega | você | `fase: aceita`; commit do que faltar; push + PR se autorizado no lote (texto e `gitlab_criar_mr` do Passo 5 da `sdd-implementar`, com `origem` = a branch da worktree — o MCP roda no checkout principal e não a enxerga; o Kiro ainda pode pedir confirmação a cada push e a cada PR, conforme as permissões) → `fase: pronta-para-merge` com o link do PR no `status.md`, commit e push (item 4 do Passo 5 da `sdd-implementar`); sem PR autorizado → fica `aceita` |

Depois de cada fase: grave a fase seguinte (`planejando` depois da pesquisa, `revisando` antes da revisão do
código), atualize o log, as Rodadas e o Histórico do `status.md`; **commite imediatamente** na worktree os
relatórios que chegaram nesta fase — `analise-plano-<N>.md` (fase 3), `revisao-codigo-<N>.md` (fase 6),
`verificacao.md`, `CT.csv`, `evidencias/` e `massa/` (fase 7) — antes de iniciar a fase seguinte. Esses arquivos não são commitados
pelos subagentes que os geram; o orquestrador é o responsável pelo commit deles.

**Aprovação de plano pausado:** a pessoa lê o plano em `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/` (ou na branch,
se o push foi autorizado) e diz "aprovo o plano da FT-031" → grave `fase: implementando` e retome a fatia na fase 5
(Passo 0). Pediu ajuste → codificador (`sdd-plano`, replanejar) e nova análise.

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
  Aguardando pessoa: <planos para aprovar · PRs para revisar · bloqueios com pergunta>
  ELM pendente [<chave>]: <o que falhou ou ficou sem o power `elm`>
  Lições para registrar: <correções que o loop precisou — sdd-aprender>
  ```
- **Horas e conclusão, numa pergunta só** (com o power `elm`): uma tabela `tarefa | horas sugeridas` com as `[DEV]`
  das fatias que chegaram a `aceita` (com ou sem PR aberto); a pessoa ajusta e confirma de uma vez → `sdd-elm` modo *horas* e modo
  *conclusão* da `[DEV]`. No AFK as horas só vão para a `[DEV]`, ao concluir: revisão e verificação por subagente
  não têm tarefa nem horas.
- Worktrees ficam até o merge; quem as remove é a **`sdd-consolidar`** (sessão padrão), depois do merge — os
  agentes não podem (`git worktree remove` é negado a todos).

## Log `.kiro/local/loop-<data>.md`

```markdown
# Loop AFK <data> — paralelo <p> · push/PR: <sim|não>
| FT | Worktree | Branch | Fase | Rodada | Último resultado | Atualizado |
|---|---|---|---|---|---|---|
```

## Regras

- Nunca merge, nunca `--force`, nunca push sem a autorização do lote.
- ELM só pelo que o lote confirmou (assumir `[DEV]`, estados) e pelas horas do fim; nada mais. Sem o power `elm` ou com
  falha → `ELM pendente [<chave>]: …` no `status.md`.
- Nunca relaxe um gate para o loop andar: bloqueio é informação, não falha.
- Tipo de fatia que bloqueia com frequência → sugira na retrospectiva tratá-lo como HITL.
