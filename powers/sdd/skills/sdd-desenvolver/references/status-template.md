# FT-<nnn> — <título>

| Campo | Valor |
|---|---|
| Fatia | FT-<nnn> · épico <EP-nn — título \| — (sem épico)> |
| Origem | <PRD EP-nn \| ficha \| DF 4567 \| IB 611 \| pedido: …> |
| Trilha | <padrão \| rápida> (como na coluna `trilha` do backlog) |
| Modo | <AFK \| HITL> (o da fatia no `backlog.md`; vale para todos os papéis) |
| Cobre | <HF-01#1.1, HF-01#1.2, REG-01 \| —> |
| Branch | `<branch>` |
| Fase | pesquisando |
| Responsável | <login \| agente:sdd-orquestrador> |
| Rodadas | revisão do plano 0 · revisão do código 0 · verificação 0 · retrabalho 0 |
| PR | — |
| Bloqueio | — (ou: `<motivo>` · pergunta: `<pergunta exata>` — junto com `Fase: bloqueada (de: <fase>)`) |
| ELM | <IB <id> · [DEV] <id> · [REV] <id> · [VER] <id> (AFK: só [DEV]) · [APR] <id> (criadas nos gates) · CT <ids> (consolidação) \| sem ELM \| pendente> |
| Banco (DDL) | <não se aplica \| pendente \| aplicada em dev \| aplicada em prod> |
| Drift de negócio | — (marcado pela REV e pela VER: `não` \| `sim — <motivo>`) |

<!-- Fases por modo:
     HITL  pesquisando → planejando → [plano-em-revisao: pela senioridade] → implementando → pr-aberto ([DEV] em andamento)
           → em-revisao ([REV] assumida; concluída ao aprovar) → em-verificacao ([VER] assumida; concluída ao
           aceitar) → pronta-para-merge → mergeada (merge pelo Dev, [DEV] concluída) → concluida (consolidação)
           reprovada na REV ou na VER → retrabalho (de: em-revisao | em-verificacao), com a [DEV] ainda aberta
           → implementando → pr-aberto (mesmo PR)
     AFK   pesquisando → planejando → [plano-em-revisao: pela senioridade] → implementando → revisando
           → verificando → aceita → pronta-para-merge (PR aberto; espera a [APR] Aprovar PR de um Dev Sênior)
           mudanças pedidas na [APR] → retrabalho (de: pronta-para-merge) → implementando → … → pronta-para-merge
     AFK → HITL (nunca o contrário): plano com risco → bloqueada (de: planejando), "aguardando troca para HITL",
           [DEV] interrompida (horas lançadas, sem conclusão) → o P.O. troca na base (sdd-planejamento) → o Dev
           retoma pela sdd-desenvolver: Modo HITL, revisor, verificador, fase planejando → GATE pela senioridade
           → mergeada (merge pelo Dev, [DEV] concluída) → concluida (consolidação)
     Entrega (todo papel do HITL): commit → push → conferir no remoto → só então concluir a tarefa e avisar.
     Desvio: `bloqueada (de: <fase>)`, com motivo e a pergunta exata; resolvido, a fatia volta à fase de origem.
     plano-em-revisao = o plano espera a [APR] Aprovar plano de um Dev Sênior; durante a análise independente a fase
     é planejando. GATE pela senioridade de quem implementa: Júnior sempre, Pleno se pedir, Sênior nunca.
     WIP esperando pessoa = plano-em-revisao + pr-aberto + em-revisao + em-verificacao + aceita + pronta-para-merge.
     Quem grava a fase: quem conduz a sessão (a skill da fase) ou, no loop, o orquestrador; o pesquisador nunca
     grava o status.md; o revisor e o verificador só no HITL (a rodada é deles); o Dev Sênior da [APR] na
     aprovação do plano e nas mudanças pedidas no PR (o PR aprovado não ganha commit: o sha não muda).
     Rodadas: incrementadas por quem pede a rodada — sdd-plano (análise), sdd-implementar (revisão e
     verificação) ou, no loop, o orquestrador; nas receitas de workflow, o passo do codificador que vem depois.
     O revisor e o verificador não incrementam — exceto no HITL, em que eles mesmos conduzem a rodada sobre o PR.
     Drift de negócio: a REV (rubrica C: achado aceito ou decisão técnica que muda comportamento visível) e a VER
     (cenário ajustado na verificação) marcam; no AFK o subagente põe a linha no relatório e quem conduz grava aqui.
     Só passa de `não` para `sim`; outro `sim` acrescenta o motivo. A consolidação só lê (sim → nova versão do PRD
     ou da ficha antes de publicar).
     Retrabalho: incrementado por quem reprova (revisor ou verificador, HITL) ou, no AFK, pelo orquestrador ou pelo
     passo do workflow que registra a verificação REJEITADA. -->

## Achados abertos

<!-- Da revisão (plano/código), da verificação e do PR. A sdd-implementar os transforma em tarefas [R<n>] e
     marca a Situação `resolvido — tarefa <n>` quando a tarefa fica verde. -->

| # | Origem | Achado | Situação |
|---|---|---|---|

## Retrabalho

<!-- HITL: uma linha por reprovação na REV ou na VER, gravada por quem reprovou; as horas, pelo codificador ao
     entregar o PR atualizado (a [DEV] segue aberta até o merge). AFK: uma linha por verificação REJEITADA (Papel `verificação (AFK)`), gravada pelo
     orquestrador ou pelo passo registrar_verificacao do workflow; e uma por mudanças pedidas na [APR] Aprovar PR
     (Papel `APR`), gravada por quem aprova; a [DEV] só é concluída no merge, Horas `—`. -->

| # | Papel | Motivo (relatório) | Data | Horas na [DEV] (retrabalho) |
|---|---|---|---|---|

## Histórico

<!-- Só acréscimo, sempre no fim. É o arquivo de progresso: quem retoma a fatia (pessoa, agente, sessão nova)
     começa por aqui. Pendências de ELM: "ELM pendente [<chave>]: <ação>" → depois "ELM feito [<chave>]: <ação>". -->

- <AAAA-MM-DD HH:MM> — fatia iniciada (sdd-desenvolver) · trilha <…> · modo <…>
