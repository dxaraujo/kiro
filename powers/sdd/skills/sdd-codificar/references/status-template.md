# FT-<nnn> — <título>

| Campo | Valor |
|---|---|
| Fatia | FT-<nnn> · épico <EP-nn — título \| — (sem épico)> |
| Origem | <PRD EP-nn \| ficha \| DF 4567 \| IB 611 \| pedido: …> |
| Trilha | <padrao \| rapida \| direta> |
| Modo | <AFK \| HITL> |
| Cobre | <HF-01#1.1, HF-01#1.2, REG-01 \| —> |
| Branch | `<branch>` |
| Fase | pesquisando (direta: implementando) |
| Responsável | <login \| agente:sdd-orquestrador> |
| Rodadas | revisão do plano 0 · revisão do código 0 · verificação 0 |
| PR | — |
| ELM | <IB <id> · [DEV] <id> · [REV] <id> · [VER] <id> (direta: só [DEV]) \| sem ELM \| pendente> |
| Banco (DDL) | <não se aplica \| pendente \| aplicada em dev \| aplicada em prod> |

<!-- Fases: pesquisando → planejando → plano-em-revisao → implementando → revisando → verificando → aceita
     → pr-aberto → concluida · desvio: `bloqueada (de: <fase>)`, com motivo e a pergunta exata; resolvido, a fatia
     volta à fase de origem.
     plano-em-revisao = o plano espera o GATE de uma pessoa; durante a análise independente a fase é planejando,
     e o passo é pulado quando o sdd.md permitir (AFK com "análise basta"; trilha rápida sem GATE).
     Quem grava a fase: quem conduz a sessão (a skill da fase) ou, no loop, o orquestrador; o pesquisador e o
     revisor nunca gravam o status.md.
     Rodadas: incrementadas por quem pede a rodada — sdd-plano (análise), sdd-implementar (revisão e
     verificação) ou, no loop, o orquestrador; nas receitas de workflow, o passo do codificador que vem depois.
     O revisor e o verificador não incrementam. -->

## Achados abertos

<!-- Da revisão (plano/código), da verificação e do PR. A sdd-implementar os transforma em tarefas [R<n>] e
     marca a Situação `resolvido — tarefa <n>` quando a tarefa fica verde. -->

| # | Origem | Achado | Situação |
|---|---|---|---|

## Histórico

<!-- Só acréscimo, sempre no fim. É o arquivo de progresso: quem retoma a fatia (pessoa, agente, sessão nova)
     começa por aqui. Pendências de ELM: "ELM pendente: <ação>" → depois "ELM feito: <ação>". -->

- <AAAA-MM-DD HH:MM> — fatia iniciada (sdd-codificar) · trilha <…> · modo <…>
