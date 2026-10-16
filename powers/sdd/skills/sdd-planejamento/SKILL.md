---
name: sdd-planejamento
description: "Planejamento ágil do projeto no fluxo sdd, ajustado a times que trabalham com agentes — roadmap e releases a partir dos épicos, acordos do time (cadência Scrum ou Kanban, Definition of Ready e Done, limites de WIP incluindo a capacidade de revisão humana, que é o gargalo), planejamento da sprint como cadência — compromisso com a meta, previsão por prioridade, dependências e capacidade (vazão de fatias e lead time, especificação e reserva de atendimento), fluxo puxado dentro da sprint —, acompanhamento, review com as evidências de aceite, retrospectiva com dados e virada de sprint; publica a sprint no EWM pela sdd-elm. Use em \"monta o planejamento\", \"planejar a sprint\", \"roadmap\", \"virada de sprint\", \"fechar a sprint\", \"review da sprint\", \"capacidade do time\", \"acordos do time\", \"encaixe na sprint\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.5.0"
---

# sdd-planejamento — Planejar o fluxo, não só o calendário

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-planejamento/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Com agentes escrevendo código, o que limita a entrega é a **atenção humana**: decidir (P.O.), revisar planos e
PRs, verificar e aceitar. O planejamento do sdd mede e protege essa capacidade, trabalha com fatias pequenas e de
tamanho parecido e prevê pela **vazão** (fatias concluídas por sprint) e pelo **lead time** por fatia — sem pontos
(opcionais só no IB do EWM, para quem usa o relatório de velocidade de lá).

**A sprint é cadência, não contêiner de escopo:** o time se compromete com a **meta**; a seleção do planejamento é
uma **previsão**. Dentro da sprint o fluxo é **puxado** — terminou uma fatia, a `pronta` do topo entra, enquanto o
WIP de revisão humana tiver folga (a `sdd-desenvolver` puxa, sem cerimônia). O Encaixe (abaixo) fica para quem
fura a fila ou estoura o WIP.
Toda hora do time cabe numa tarefa da sprint, em cinco frentes: entrega `[DEV]`, revisão `[REV]`, verificação
`[VER]`, especificação `[ESP]` e atendimento `[ATD]`.

Arquivos na raiz de `<produto>/` (formatos em [references/arquivos.md](references/arquivos.md)):
`equipe.json`, `acordos.md`, `roadmap.md`, `sprints/sprint-<nn>.md`. Fatias: `<produto>/backlog.md`.

Regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar.

## Modo inicial — acordos e roadmap

1. **Equipe** (`equipe.json` ou `equipe.md` existe → mostre e pergunte só o que mudou): nome do projeto, data de
   início da sprint 1 (Kanban: a da primeira revisão de backlog), pessoas (todas `ativo: true`; quem sai fica
   `false`, nunca é apagado), papéis (um ou mais por
   pessoa: `P.O.`, `Especificador`, `Dev`, `QA`, `SM`; exatamente um P.O. ativo), login do ELM (de `members` do `pa_*.json`, se houver), horas por
   semana, ausências. Pergunte também, por pessoa, quantas horas por semana vão para **revisar** (planos, PRs) e
   **verificar** — somadas em `horas-revisao-semana` —, para **especificar** (entrevista, PRD, fatiamento:
   `horas-especificacao-semana`; P.O. e Especificador) e quem **atende** demandas (`atende`). Grave no formato
   detectado — **só depois dos acordos (passo 2)**, que dão `cadencia` e `duracao-sprint-semanas` (antes deles o JSON não valida; Kanban → `duracao-sprint-semanas` = a cadência da revisão de
   backlog, padrão 1), com `atualizado` = hoje, `historico: []` e `ausencias: []` em quem não tem; confirme que há
   **exatamente um** P.O. ativo — (`equipe.json` → validado contra `assets/equipe.schema.json`; `equipe.md` → valide só pela presença
   das colunas obrigatórias: Login, Papéis, Horas/semana). Se nenhum arquivo existir ainda, prefira `equipe.json`
   (padrão com validação de schema); só use `equipe.md` se o time preferir edição direta em Markdown.

   **equipe.md** (formato Markdown, alternativo): o formato é o de
   [assets/equipe-template.md](assets/equipe-template.md) (cabeçalho com cadência, duração, início e pontos; tabelas
   Pessoas — com `Ativo` —, Ausências e Histórico), que mapeia 1:1 para os campos do schema. Não valide contra
   `equipe.schema.json` neste caso — valide pela presença das colunas obrigatórias (Login, Nome, Papéis,
   Horas/semana).
2. **Acordos** (`acordos.md`) — proponha e ajuste:
   - cadência: **Scrum** (sprints de N semanas, cerimônias, iteração no EWM) ou **Kanban** (fluxo contínuo,
     revisão de backlog semanal); padrão: sprints de 2 semanas com fluxo puxado dentro da sprint;
   - **WIP:** uma fatia por sessão de agente; fatias esperando pessoa (`plano-em-revisao`, `pr-aberto`,
     `em-revisao`, `em-verificacao`, `aceita`, `pronta-para-merge`) ≤ capacidade de revisão (ex.: 2 por revisor); PR parado há mais de 1 dia → recomendar destravá-lo
     antes de começar fatia nova (seguir mesmo assim fica registrado: `WIP excedido`);
   - **Definition of Ready** e **Definition of Done** (padrão no `arquivos.md`);
   - tamanho: `P`/`M`/`G` — só para a Definition of Ready e para saber quando dividir (maior que G → dividir);
     pontos por tamanho, só se o time os quiser no EWM;
   - **reserva de atendimento e retrabalho** (padrão **20% das horas da sprint do time**) — cobre os
     **atendimentos** (`[ATD]`) e o **retrabalho da sprint anterior** (o que falta das fatias migradas); e a **cadência de lançamento de horas** (padrão: ao fechar cada sessão; lançar ≠ concluir).
3. **Roadmap** (`roadmap.md`): épicos do `backlog.md` em ordem de valor e risco (maior incerteza mais cedo),
   agrupados em releases com um objetivo cada; épico sem PRD aparece como "a descobrir" (`sdd-prd`).

## Modo sprint — planejar a próxima

1. **Capacidade**, da `equipe.json` (horas da sprint menos ausências):
   - **revisão humana** (horas de revisão e verificação) — o limite principal;
   - **HITL**: fatias HITL consomem horas de dev acompanhando;
   - **vazão**: média de fatias concluídas nas últimas 3 sprints, incluídas as puxadas (primeira sprint: comece
     com 1 fatia por dev por semana e ajuste na virada), e o lead time médio por fatia;
   - **especificação**: horas de especificação da sprint (`horas-especificacao-semana`); zero no time inteiro e
     épico a especificar no topo → avise antes de seguir (sem horas não há `[ESP]`: alguém ganha horas de
     especificação no `equipe.json`, ou o épico fica para depois);
   - **reserva de atendimento e retrabalho**: o percentual do `acordos.md` sobre as **horas da sprint do time
     inteiro** (todos os ativos, menos ausências), descontado antes de selecionar fatias. Dentro dela entram primeiro
     as **fatias migradas** da sprint anterior (horas que faltam, pela estimativa da `[DEV]` restante); o resto fica
     para os atendimentos da sprint. Migradas que passam da reserva consomem a capacidade das fatias novas.
2. **Especificação:** épicos que entram em entrevista, PRD ou fatiamento nesta sprint (do `roadmap.md`, os "a
   descobrir" do topo, e os `EP` em `rascunho` com `prd` `—` do `backlog.md` que o roadmap ainda não tem —
   proponha a posição deles), um `[ESP]` por épico, com responsável e horas previstas dentro da capacidade de
   especificação.
3. **Previsão** (não compromisso): confira a Definition of Ready das fatias do topo e grave `pronta` nas que passam (ou `backlog`
   nas que deixaram de passar). Entram as `pronta` — de épico e sem épico, inclusive as diretas (toda hora tem
   tarefa) —, respeitando `bloqueada-por` — a fatia só entra se as
   dependências entram antes ou já estão concluídas. Pare ao atingir a menor das capacidades. Fatia não `pronta` no
   topo → aponte o que falta (decisão, PRD, fatiar) antes de pular para a próxima. Cada fatia **HITL** ganha **revisor**
   e **verificador** (não quem implementa), e a soma das revisões e verificações cabe nas horas de revisão de cada
   um; fatia **AFK** não tem (revisão e verificação por subagente, sem `[REV]`/`[VER]`) — a revisão humana dela é a
   leitura do PR.
4. **Meta da sprint:** uma frase de resultado de negócio que as fatias entregam juntas.
5. **Iteração:** pergunte a iteração do EWM da sprint (de `iterations` do `pa_*.json`); é o `plannedFor` de
   todos os IBs e tarefas desta sprint.
6. **Proposta**, com as três seções:
   ```
   🗓️ Sprint <nn> · <início> → <fim> · iteração <nome> · meta: <…>
   Fatias
   | Prioridade | FT | Título | Tam. | Modo | Depende de | Responsável | Revisor | Verificador |
   Especificação
   | EP | Responsável | Horas previstas |
   Reserva (atendimento + retrabalho): <h>h (<p>% da sprint) · retrabalho migrado <x>h · livre para atendimento <y>h
   Capacidade: revisão <h>h (usa <x>h) · especificação <h>h (usa <x>h) · vazão prevista <n> fatias · lead time médio <d> dias · HITL <h>h
   Próximas a puxar (fora da previsão, na ordem): <FT…>
   ```
7. "ok" → grave `sprints/sprint-<nn>.md`, `sprint`, `responsavel` e `status` no `backlog.md` pelo bloco
   [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) e **chame sempre a `sdd-elm` modo *sprint*** (planos, IBs e tarefas `[DEV]` `[REV]`
   `[VER]` `[ESP]` na iteração escolhida), para a sprint e o EWM ficarem iguais. Sem o power `elm` ou com falha, a
   coluna "Tarefa ELM" fica `pendente` e a `sdd-elm` publica depois.

## Durante a sprint

"Como está a sprint?" → **`sdd-status`** filtrado pela sprint (fase de cada fatia, bloqueios, WIP de revisão,
PRs parados). Fatia que cresceu (passou de `G` no plano) → volte para a `sdd-fatiar` (dividir) em vez de esticar.
Atendimento que estoura a reserva → mostre ao P.O. e ele decide qual fatia sai da sprint; o atendimento nunca tira
fatia sozinho.

**Encaixe** — só quando puxar não basta: a fatia `pronta` que alguém quer começar **não é a do topo** (fura a
fila) ou o **WIP de revisão está no limite** (de qualquer trilha, inclusive a direta); a `sdd-desenvolver` manda para cá. Atendimento triado quando a reserva estourou é o mesmo encaixe (a
`sdd-triar` manda para cá): a decisão do P.O. vai na linha do AT no `sprint-<nn>.md`. Mostre ao P.O. a fatia (trilha, tamanho, modo, origem), o que sobra da
capacidade (revisão, vazão, HITL) e as opções, com a recomendada:
- **entra na folga** — cabe sem tirar nada;
- **entra no lugar de** `FT-…` — uma ainda não iniciada, que volta para `sprint` `—`;
- **fica para a próxima sprint**.

Com a decisão do P.O. (ou de quem ele delegou): `sprint` e `responsavel` no `backlog.md` (e, na fatia HITL, revisor e
verificador, que não sejam quem implementa — as `[REV]`/`[VER]` precisam deles), uma linha no
`sprint-<nn>.md` com a Observação `encaixe: <decisão> (<quem decidiu>, <data>)`, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base), e a `sdd-elm` modo
*sprint* para as tarefas da fatia (AT: modo *atendimento*, Registrar). Na troca, as tarefas da fatia que sai vão
para a próxima iteração (`sdd-elm`, só o `plannedFor`). Depois, volte à `sdd-desenvolver` (Passo 3, item 4). Sem
decisão, a fatia não começa; urgência acelera a decisão, não a dispensa.

## Review

Para cada fatia concluída: o cenário entregue e a **evidência** do `verificacao.md` (resposta, contagem,
screenshot). Registre o retorno do P.O. no `sprint-<nn>.md`; pedido novo vira cenário/fatia nova pela `sdd-prd`/
`sdd-fatiar` — não reabre fatia concluída.

## Retrospectiva e virada

1. **Retrospectiva com dados** — `sdd-aprender` modo retrospectiva (vazão, lead time, rodadas de revisão,
   correções humanas por causa, AFK que chegaram ao PR sozinhas). Registre no `sprint-<nn>.md`: bom · melhorar ·
   ações (cada ação com dono).
2. **Horas:** `sdd-elm` modo *horas*, relatório da sprint por tipo e por pessoa. Preencha "Números"
   (planejadas × lançadas) e aponte as tarefas concluídas sem horas lançadas — só aqui, no fechamento.
3. **Fechar:** concluídas — previstas e puxadas — contam na vazão e no lead time; a meta é avaliada (atingida ou
   não, e por quê); não concluídas — fatias, `[ESP]` e `[ATD]` — **migram**
   para a próxima sprint (no `sprint-<nn>.md` antigo ficam com "→ sprint <nn+1>"; o histórico não é apagado) e
   ele fica com `**Situação:** fechada`; no `sprint-<nn+1>.md` novo, cada item migrado ganha a sua linha (seção
   Fatias, Especificação ou Atendimento) com a Observação `migrada da sprint <nn>`. Fatia ou AT migrado → `sprint` = nn+1 na linha do `backlog.md` (fatias e
   `## Atendimentos`), pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base). AT em `backlog` (triado sem sprint aberta) entra no planejamento da próxima como as fatias.
4. Recalcule vazão média, lead time médio e horas por tipo (`equipe.json` → `historico`). Reserva (atendimento +
   retrabalho): o % é o do `acordos.md`; mostre o consumido da sprint (horas das `[ATD]` + retrabalho) contra ela
   e, se ficou muito acima ou abaixo, **proponha** um novo % ao P.O. — muda o acordo só com "ok". Replaneje a
   próxima pelo modo sprint (migradas consomem capacidade primeiro).
5. **ELM** — `sdd-elm` modo *sprint*, virada: as tarefas não concluídas só mudam o `plannedFor` para a nova
   iteração (o pai não muda) e as novas são publicadas; roteiro manual de baseline, se o projeto exige. Iteração do
   EWM mais longa que a sprint (a mesma cobre as duas) → nada muda no EWM; diga isso, e o relatório de horas da
   sprint conta só as tarefas listadas no `sprint-<nn>.md`, não a iteração inteira.

## Regras

- Nunca planeje acima da capacidade de revisão: trabalho que ninguém revisa não está pronto, só está parado.
- Fatia nunca se espalha por sprints para caber; se não cabe, divide.
- Tamanho é do time; o agente propõe P/M/G com justificativa, a pessoa decide. Nada de Planning Poker em pontos: a
  previsão é pela vazão.
- Pontos, se o time os usar no EWM, ficam só no IB (plan item), nunca nas tarefas, e não entram no planejamento.
- O compromisso da sprint é a meta: fatia prevista que não entrou não é falha; meta não atingida vai para a retro.
- Toda hora planejada tem tarefa: nada de especificação ou atendimento fora da sprint.
