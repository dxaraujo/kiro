# FT-<nnn> — <título>

| Campo | Valor |
|---|---|
| Fatia | FT-<nnn> · épico <EP-nn — título \| — (sem épico)> |
| Origem | <PRD EP-nn \| ficha \| DF 4567 \| IB 611 \| pedido: …> |
| Trilha | <padrão \| rápida \| direta> (como na coluna `trilha` do backlog) |
| Modo | <AFK \| HITL> (o da fatia no `backlog.md`; vale para todos os papéis) |
| Cobre | <HF-01#1.1, HF-01#1.2, REG-01 \| —> |
| Branch | `<branch>` |
| Fase | pesquisando (direta: implementando) |
| Responsável | <login \| agente:sdd-orquestrador> |
| Rodadas | revisão do plano 0 · revisão do código 0 · verificação 0 · retrabalho 0 |
| PR | — |
| Bloqueio | — (ou: `<motivo>` · pergunta: `<pergunta exata>` — junto com `Fase: bloqueada (de: <fase>)`) |
| ELM | <IB <id> · [DEV] <id> · [REV] <id> · [VER] <id> (direta: só [DEV]) \| sem ELM \| pendente> |
| Banco (DDL) | <não se aplica \| pendente \| aplicada em dev \| aplicada em prod> |

<!-- Fases por modo:
     HITL  pesquisando → planejando → plano-em-revisao → implementando → pr-aberto ([DEV] concluída)
           → em-revisao ([REV] assumida) → em-verificacao ([VER] assumida) → pronta-para-merge → concluida
           reprovada na REV ou na VER → retrabalho (de: em-revisao | em-verificacao), [DEV] reaberta
           → implementando → pr-aberto (mesmo PR, [DEV] concluída de novo)
     AFK   pesquisando → planejando → [plano-em-revisao: só fatia de épico] → implementando → revisando
           → verificando → aceita → pronta-para-merge (PR aberto, [DEV] concluída) → concluida
     Desvio: `bloqueada (de: <fase>)`, com motivo e a pergunta exata; resolvido, a fatia volta à fase de origem.
     plano-em-revisao = o plano espera o GATE de uma pessoa; durante a análise independente a fase é planejando,
     e o passo é pulado na fatia AFK sem épico e na trilha rápida com `GATE na trilha rápida = não`.
     WIP esperando pessoa = plano-em-revisao + pr-aberto + em-revisao + em-verificacao + aceita + pronta-para-merge.
     Quem grava a fase: quem conduz a sessão (a skill da fase) ou, no loop, o orquestrador; o pesquisador e o
     revisor nunca gravam o status.md.
     Rodadas: incrementadas por quem pede a rodada — sdd-plano (análise), sdd-implementar (revisão e
     verificação) ou, no loop, o orquestrador; nas receitas de workflow, o passo do codificador que vem depois.
     O revisor e o verificador não incrementam — exceto no HITL, em que eles mesmos conduzem a rodada sobre o PR.
     Retrabalho: incrementado por quem reprova (revisor ou verificador, HITL). -->

## Achados abertos

<!-- Da revisão (plano/código), da verificação e do PR. A sdd-implementar os transforma em tarefas [R<n>] e
     marca a Situação `resolvido — tarefa <n>` quando a tarefa fica verde. -->

| # | Origem | Achado | Situação |
|---|---|---|---|

## Retrabalho

<!-- Só no HITL: uma linha por reprovação na REV ou na VER. Gravada por quem reprovou; as horas, pelo codificador
     ao concluir a [DEV] de novo. -->

| # | Papel | Motivo (relatório) | Data | Horas na [DEV] reaberta |
|---|---|---|---|---|

## Histórico

<!-- Só acréscimo, sempre no fim. É o arquivo de progresso: quem retoma a fatia (pessoa, agente, sessão nova)
     começa por aqui. Pendências de ELM: "ELM pendente: <ação>" → depois "ELM feito: <ação>". -->

- <AAAA-MM-DD HH:MM> — fatia iniciada (sdd-desenvolver) · trilha <…> · modo <…>
