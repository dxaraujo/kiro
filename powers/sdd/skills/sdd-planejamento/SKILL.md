---
name: sdd-planejamento
description: "Planejamento ágil do projeto no fluxo sdd, ajustado a times que trabalham com agentes — roadmap e releases a partir dos épicos, acordos do time (cadência Scrum ou Kanban, Definition of Ready e Done, limites de WIP incluindo a capacidade de revisão humana, que é o gargalo), planejamento da sprint por prioridade, dependências e capacidade (vazão de fatias e pontos, especificação e reserva de atendimento), meta da sprint, acompanhamento, review com as evidências de aceite, retrospectiva com dados e virada de sprint; publica a sprint no EWM pela sdd-elm. Use em \"monta o planejamento\", \"planejar a sprint\", \"roadmap\", \"virada de sprint\", \"fechar a sprint\", \"review da sprint\", \"capacidade do time\", \"acordos do time\", \"encaixe na sprint\"."
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
tamanho parecido e prevê pela **vazão** (fatias concluídas por sprint), mantendo os pontos no EWM para quem os usa.
Toda hora do time cabe numa tarefa da sprint, em cinco frentes: entrega `[DEV]`, revisão `[REV]`, verificação
`[VER]`, especificação `[ESP]` e atendimento `[ATD]`.

Arquivos em `<produto>/planejamento/` (formatos em [references/arquivos.md](references/arquivos.md)):
`equipe.json`, `acordos.md`, `roadmap.md`, `sprints/sprint-<nn>.md`. Fatias: `<produto>/backlog.md`.

Regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar.

## Modo inicial — acordos e roadmap

1. **Equipe** (`equipe.json` ou `equipe.md` existe → mostre e pergunte só o que mudou): pessoas, papel (um só:
   `P.O.`, `Especificador`, `Dev`, `QA` ou `SM`; `Analista` antigo é lido como `Especificador`), login do ELM (de `members` do `pa_*.json`, se houver), horas por
   semana, ausências. Pergunte também, por pessoa, quantas horas por semana vão para **revisar** (planos, PRs) e
   **verificar** — somadas em `horas-revisao-semana` —, para **especificar** (entrevista, PRD, fatiamento:
   `horas-especificacao-semana`; P.O. e Especificador) e quem **atende** demandas (`atende`). Grave no formato
   detectado (`equipe.json` → validado contra `assets/equipe.schema.json`; `equipe.md` → valide só pela presença
   das colunas obrigatórias: Login, Papel, Horas/semana). Se nenhum arquivo existir ainda, prefira `equipe.json`
   (padrão com validação de schema); só use `equipe.md` se o time preferir edição direta em Markdown.

   **equipe.md** (formato Markdown, alternativo): leia pelo parser de tabelas Markdown; as colunas mapeiam 1:1
   para os campos do schema. Não valide contra `equipe.schema.json` neste caso — valide pela presença das colunas
   obrigatórias (Login, Papel, Horas/semana). Formato das tabelas:
   ```
   ## Pessoas
   | Login | Nome | Papel | Horas/semana | Horas revisão/semana | Horas especificação/semana | Atende |
   |---|---|---|---|---|---|---|

   ## Ausências planejadas
   | Login | Início | Fim | Horas ausentes |
   |---|---|---|---|

   ## Histórico de sprints
   | Sprint | Fatias concluídas | Pontos | Horas DEV | Horas REV | Horas VER | Horas ESP | Horas ATD |
   |---|---|---|---|---|---|---|---|
   ```
2. **Acordos** (`acordos.md`) — proponha e ajuste:
   - cadência: **Scrum** (sprints de N semanas, cerimônias, iteração no EWM) ou **Kanban** (fluxo contínuo,
     revisão de backlog semanal); padrão: sprints de 2 semanas com fluxo puxado dentro da sprint;
   - **WIP:** uma fatia por sessão de agente; fatias esperando pessoa (`plano-em-revisao` + `aceita` +
     `pr-aberto`) ≤ capacidade de revisão (ex.: 2 por revisor); PR parado há mais de 1 dia → recomendar destravá-lo
     antes de começar fatia nova (seguir mesmo assim fica registrado: `WIP excedido`);
   - **Definition of Ready** e **Definition of Done** (padrão no `arquivos.md`);
   - tamanho: `P`/`M`/`G` e a tabela de pontos (padrão `2/3/5`);
   - **reserva de atendimento** (padrão 20% das horas de quem atende) — esta reserva cobre **atendimentos novos**
     e **retrabalho da sprint anterior** (fatias migradas que ainda consomem esforço); as fatias migradas consomem
     capacidade **antes** da seleção de novas fatias; e **lançamento de horas** (na conclusão de cada tarefa).
3. **Roadmap** (`roadmap.md`): épicos do `backlog.md` em ordem de valor e risco (maior incerteza mais cedo),
   agrupados em releases com um objetivo cada; épico sem PRD aparece como "a descobrir" (`sdd-prd`).

## Modo sprint — planejar a próxima

1. **Capacidade**, da `equipe.json` (horas da sprint menos ausências):
   - **revisão humana** (horas de revisão e verificação) — o limite principal;
   - **HITL**: fatias HITL consomem horas de dev acompanhando;
   - **vazão**: média de fatias concluídas nas últimas 3 sprints (primeira sprint: comece com 1 fatia por dev
     por semana e ajuste na virada). Em pontos: velocidade média, para o EWM;
   - **especificação**: horas de especificação da sprint (`horas-especificacao-semana`);
   - **reserva de atendimento**: o percentual do `acordos.md` sobre as horas de quem atende, descontado antes de
     selecionar fatias. **Fatias migradas da sprint anterior** consomem capacidade antes das fatias novas — inclua-as
     no cálculo antes de selecionar novos itens.
2. **Especificação:** épicos que entram em entrevista, PRD ou fatiamento nesta sprint (do `roadmap.md`, os "a
   descobrir" do topo, e os `EP` em `rascunho` com `prd` `—` do `backlog.md` que o roadmap ainda não tem —
   proponha a posição deles), um `[ESP]` por épico, com responsável e horas previstas dentro da capacidade de
   especificação.
3. **Seleção:** confira a Definition of Ready das fatias do topo e grave `pronta` nas que passam (ou `backlog`
   nas que deixaram de passar). Entram as `pronta` — de épico e sem épico, inclusive as diretas (toda hora tem
   tarefa) —, respeitando `bloqueada-por` — a fatia só entra se as
   dependências entram antes ou já estão concluídas. Pare ao atingir a menor das capacidades. Fatia não `pronta` no
   topo → aponte o que falta (decisão, PRD, fatiar) antes de pular para a próxima. Cada fatia ganha **revisor** e
   **verificador** (não quem implementa), e a soma das revisões e verificações cabe nas horas de revisão de cada um.
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
   Atendimento: reserva <h>h (<p>% de <pessoas>)
   Capacidade: revisão <h>h (usa <x>h) · especificação <h>h (usa <x>h) · vazão prevista <n> fatias / <p> pts · HITL <h>h
   Fica de fora (por capacidade): <FT…>
   ```
7. "ok" → grave `sprints/sprint-<nn>.md`, `sprint`, `responsavel` e `status` no `backlog.md`, commit na base
   (artefato de produto) e **chame sempre a `sdd-elm` modo *sprint*** (planos, IBs e tarefas `[DEV]` `[REV]`
   `[VER]` `[ESP]` na iteração escolhida), para a sprint e o EWM ficarem iguais. Sem MCP ou com falha, a
   coluna "Tarefa ELM" fica `pendente` e a `sdd-elm` publica depois.

## Durante a sprint

"Como está a sprint?" → **`sdd-status`** filtrado pela sprint (fase de cada fatia, bloqueios, WIP de revisão,
PRs parados). Fatia que cresceu (passou de `G` no plano) → volte para a `sdd-fatiar` (dividir) em vez de esticar.
Atendimento que estoura a reserva → mostre ao P.O. e ele decide qual fatia sai da sprint; o atendimento nunca tira
fatia sozinho.

**Encaixe** — alguém quer começar uma fatia `pronta` (de qualquer trilha, inclusive a direta) que não está na sprint
aberta; a `sdd-codificar` manda para cá. Atendimento triado quando a reserva estourou é o mesmo encaixe (a
`sdd-triar` manda para cá): a decisão do P.O. vai na linha do AT no `sprint-<nn>.md`. Mostre ao P.O. a fatia (trilha, tamanho, modo, origem), o que sobra da
capacidade (revisão, vazão, HITL) e as opções, com a recomendada:
- **entra na folga** — cabe sem tirar nada;
- **entra no lugar de** `FT-…` — uma ainda não iniciada, que volta para `sprint` `—`;
- **fica para a próxima sprint**.

Com a decisão do P.O. (ou de quem ele delegou): `sprint` e `responsavel` no `backlog.md` (e revisor e verificador,
que não sejam quem implementa — as `[REV]`/`[VER]` precisam deles), uma linha no
`sprint-<nn>.md` com a Observação `encaixe: <decisão> (<quem decidiu>, <data>)`, commit na base e a `sdd-elm` modo
*sprint* para as tarefas da fatia. Na troca, as tarefas da fatia que sai vão
para a próxima iteração (`sdd-elm`, só o `plannedFor`). Depois, volte à `sdd-codificar` (Passo 3, item 4). Sem
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
3. **Fechar:** concluídas contam na vazão e nos pontos; não concluídas — fatias, `[ESP]` e `[ATD]` — **migram**
   para a próxima sprint (no `sprint-<nn>.md` antigo ficam com "→ sprint <nn+1>"; o histórico não é apagado) e
   ele fica com `**Situação:** fechada`. AT migrado → `sprint` = nn+1 na linha de `## Atendimentos` do
   `backlog.md`; AT em `backlog` (triado sem sprint aberta) entra no planejamento da próxima como as fatias.
4. Recalcule vazão média, velocidade e horas por tipo (`equipe.json` → `historico`), recalibre a reserva de
   atendimento pelo consumido e replaneje a próxima pelo modo sprint (migradas consomem capacidade primeiro).
5. **ELM** — `sdd-elm` modo *sprint*, virada: as tarefas não concluídas só mudam o `plannedFor` para a nova
   iteração (o pai não muda) e as novas são publicadas; roteiro manual de baseline, se o projeto exige.

## Regras

- Nunca planeje acima da capacidade de revisão: trabalho que ninguém revisa não está pronto, só está parado.
- Fatia nunca se espalha por sprints para caber; se não cabe, divide.
- Estimativa é do time (pode usar Planning Poker); o agente propõe tamanho com justificativa, a pessoa decide.
- Pontos ficam no IB (plan item), nunca nas tarefas.
- Toda hora planejada tem tarefa: nada de especificação ou atendimento fora da sprint.
