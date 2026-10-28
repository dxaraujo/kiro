---
name: sdd-planejamento
description: "Planejamento ágil do projeto no fluxo sdd, ajustado a times que trabalham com agentes — roadmap e releases a partir dos épicos, acordos do time (cadência Scrum ou Kanban, Definition of Ready e Done, limites de WIP incluindo a capacidade de revisão humana, que é o gargalo), planejamento da sprint como cadência — compromisso com a meta, previsão por prioridade, dependências e capacidade (vazão de fatias e lead time, especificação e reserva de apoio), fluxo puxado dentro da sprint —, acompanhamento, review com as evidências de aceite, retrospectiva com dados e virada de sprint, troca AFK → HITL e relatório de horas; publica a sprint no EWM pelo MCP elm. Use em \"monta o planejamento\", \"planejar a sprint\", \"roadmap\", \"virada de sprint\", \"fechar a sprint\", \"review da sprint\", \"capacidade do time\", \"acordos do time\", \"encaixe na sprint\", \"sincroniza a sprint\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.3.1"
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
Toda hora do time cabe numa tarefa da sprint, em seis frentes: entrega `[DEV]`, revisão `[REV]`, aprovação `[APR]`
(do Dev Sênior, nos gates sem tarefa de papel: plano e PR do AFK), verificação `[VER]`, especificação `[ESP]` e
Apoio (`[ATD]`, `[IMPL]`, `[BD]`, `[INF]`, `[OPE]`, `[EXT]` — tabela **Apoio** do `sdd.md`).

Arquivos na raiz de `<produto>/` (formatos em [references/arquivos.md](references/arquivos.md)):
`equipe.json`, `acordos.md`, `roadmap.md`, `sprints/<pai>/sprint-<nn>.md` (a sprint segue a iteração pai do EWM:
`2026/03`). Fatias: `<produto>/backlog.md`.

Regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar.

## Modo inicial — acordos e roadmap

1. **Equipe** (`equipe.json` ou `equipe.md` existe → mostre e pergunte só o que mudou): nome do projeto, data de
   início da sprint 1 (Kanban: a da primeira revisão de backlog), pessoas (todas `ativo: true`; quem sai fica
   `false`, nunca é apagado), papéis (um ou mais por
   pessoa: `P.O.`, `Especificador`, `Dev`, `QA`, `SM`; exatamente um P.O. ativo), **senioridade** de quem é Dev
   (`Júnior`, `Pleno` ou `Sênior` — decide o modo das fatias da pessoa e quem revisa PR: [Modo pela
   senioridade](#modo-pela-senioridade); arquivo existente com Dev sem ela → pergunte só isso, para cada um; nenhum Dev
   Sênior ativo → avise: nenhum PR teria quem o revise), login do ELM, horas por
   semana, ausências. Pergunte também, por pessoa, quantas horas por semana vão para **revisar** (planos, PRs) e
   **verificar** — somadas em `horas-revisao-semana` —, para **especificar** (entrevista, PRD, fatiamento:
   `horas-especificacao-semana`; P.O. e Especificador) e quem faz **Apoio** (`atende`). Grave no formato
   detectado — **só depois dos acordos (passo 2)**, que dão `cadencia` e `duracao-sprint-semanas` (antes deles o JSON não valida; Kanban → `duracao-sprint-semanas` = a cadência da revisão de
   backlog, padrão 1), com `atualizado` = hoje, `historico: []` e `ausencias: []` em quem não tem; confirme que há
   **exatamente um** P.O. ativo — (`equipe.json` → validado contra `assets/equipe.schema.json`; `equipe.md` → valide só pela presença
   das colunas obrigatórias: Login, Papéis, Horas/semana e, para Dev, Senioridade). Se nenhum arquivo existir ainda, prefira `equipe.json`
   (padrão com validação de schema); só use `equipe.md` se o time preferir edição direta em Markdown.

   **equipe.md** (formato Markdown, alternativo): o formato é o de
   [assets/equipe-template.md](assets/equipe-template.md) (cabeçalho com cadência, duração, início e pontos; tabelas
   Pessoas — com `Ativo` —, Ausências e Histórico), que mapeia 1:1 para os campos do schema. Não valide contra
   `equipe.schema.json` neste caso — valide pela presença das colunas obrigatórias (Login, Nome, Papéis,
   Horas/semana e, para Dev, Senioridade).
2. **Acordos** (`acordos.md`) — proponha e ajuste:
   - cadência: **Scrum** (sprints de N semanas, cerimônias, iteração no EWM) ou **Kanban** (fluxo contínuo,
     revisão de backlog semanal); padrão: sprints de 2 semanas com fluxo puxado dentro da sprint;
   - **WIP:** uma fatia por sessão de agente; fatias esperando pessoa (`plano-em-revisao`, `pr-aberto`,
     `em-revisao`, `em-verificacao`, `aceita`, `pronta-para-merge`) ≤ capacidade de revisão (ex.: 2 por revisor); PR parado há mais de 1 dia → recomendar destravá-lo
     antes de começar fatia nova (seguir mesmo assim fica registrado: `WIP excedido`);
   - **Definition of Ready** e **Definition of Done** (padrão no `arquivos.md`);
   - tamanho: `P`/`M`/`G` — só para a Definition of Ready e para saber quando dividir (maior que G → dividir);
     pontos por tamanho, só se o time os quiser no EWM;
   - **reserva de apoio e retrabalho** (padrão **20% das horas da sprint do time**) — cobre o
     **Apoio** (toda categoria: `[ATD]`, `[IMPL]`…) e o **retrabalho da sprint anterior** (o que falta das fatias migradas); e a **cadência de lançamento de horas** (padrão: ao fechar cada sessão; lançar ≠ concluir).
3. **Roadmap** (`roadmap.md`): épicos do `backlog.md` em ordem de valor e risco (maior incerteza mais cedo),
   agrupados em releases com um objetivo cada; épico sem PRD aparece como "a descobrir" (`sdd-prd`).

## Modo sprint — planejar a próxima

0. **Senioridade:** Dev ativo sem `senioridade` no `equipe.json` (ou na coluna do `equipe.md`) → pergunte só isso,
   para cada um, e grave antes de seguir. Nenhum **Dev Sênior** ativo → avise antes de planejar: nenhum PR teria quem
   o revise (a `[REV]` é sempre de um Dev Sênior); o time decide se alguém passa a Sênior ou se a sprint segue assim,
   com as fatias HITL paradas em `pr-aberto`.
1. **Capacidade**, da `equipe.json` (horas da sprint menos ausências):
   - **revisão humana** (horas de revisão e verificação) — o limite principal;
   - **HITL**: fatias HITL consomem horas de dev acompanhando;
   - **vazão**: média de fatias concluídas nas últimas 3 sprints, incluídas as puxadas (primeira sprint: comece
     com 1 fatia por dev por semana e ajuste na virada), e o lead time médio por fatia;
   - **especificação**: horas de especificação da sprint (`horas-especificacao-semana`); zero no time inteiro e
     épico a especificar no topo → avise antes de seguir (sem horas não há `[ESP]`: alguém ganha horas de
     especificação no `equipe.json`, ou o épico fica para depois);
   - **reserva de apoio e retrabalho**: o percentual do `acordos.md` sobre as **horas da sprint do time
     inteiro** (todos os ativos, menos ausências), descontado antes de selecionar fatias. Dentro dela entram primeiro
     as **fatias migradas** da sprint anterior (horas que faltam, pela estimativa da `[DEV]` restante); o resto fica
     para o Apoio da sprint. Migradas que passam da reserva consomem a capacidade das fatias novas.
2. **Especificação:** épicos que entram em entrevista, PRD ou fatiamento nesta sprint (do `roadmap.md`, os "a
   descobrir" do topo, e os `EP` em `rascunho` com `prd` `—` do `backlog.md` que o roadmap ainda não tem —
   proponha a posição deles), um `[ESP]` por épico, com responsável e horas previstas dentro da capacidade de
   especificação.
3. **Previsão** (não compromisso): confira a Definition of Ready das fatias do topo e grave `pronta` nas que passam (ou `backlog`
   nas que deixaram de passar). Entram as `pronta` — de épico e sem épico —, respeitando `bloqueada-por` — a fatia só entra se as
   dependências entram antes ou já estão concluídas. Pare ao atingir a menor das capacidades. Fatia não `pronta` no
   topo → aponte o que falta (decisão, PRD, fatiar) antes de pular para a próxima. Cada fatia ganha **responsável**,
   e o modo final sai da senioridade dele ([Modo pela senioridade](#modo-pela-senioridade)). Cada fatia **HITL** ganha
   **revisor** — um **Dev Sênior**, pela [regra do revisor](#modo-pela-senioridade) — e **verificador** (não quem
   implementa), e a soma das revisões e verificações cabe nas horas de revisão de cada um; fatia **AFK** não tem
   (revisão e verificação por subagente, sem `[REV]`/`[VER]`) — a revisão humana dela é a leitura do PR. As
   **aprovações previstas** também consomem as horas de revisão dos Dev Sêniores: o plano de cada fatia de Júnior
   (e de Pleno que costuma pedir o GATE) e o PR de cada fatia AFK. A `[APR]` não nasce aqui — nasce no gate.
4. **Meta da sprint:** uma frase de resultado de negócio que as fatias entregam juntas, e o **nome curto** dela
   (até ~6 palavras: `Exportar o relatório de contas`), que vai no nome do plano no EWM.
5. **Iteração e número:** o **pai** é o da sprint anterior (a nova herda); pai novo só quando a pessoa diz, com o
   nome que ela der (`2026`, `Entrega 3`…); primeira sprint do projeto → pergunte o nome. A `<nn>` é a próxima
   dentro do pai (pai novo → `01`). Proponha o nome da iteração no EWM (padrão `Sprint <nn>`) e o do plano
   (`<nome> - <nome curto da meta>`: `Sprint 01 - Exportar o relatório de contas`); nada é criado no EWM antes do
   "ok" — a iteração, o pai que faltar e o plano nascem na publicação (passo 7;
   [references/elm-sprint.md](references/elm-sprint.md) §1), com as datas da sprint. A iteração é o `plannedFor` de
   todos os IBs e tarefas desta sprint — os que estão no backlog do EWM só mudam de iteração (§3). Pai novo → a
   `[GB]` dele (§2).
6. **Proposta**, com as três seções:
   ```
   🗓️ Sprint <pai>/<nn> · <início> → <fim> · iteração <pai>/<nome> · plano <nome> - <nome curto da meta> · meta: <…>
   Fatias
   | Prioridade | FT | Título | Tam. | Modo | Depende de | Responsável | Revisor | Verificador |
   Especificação
   | EP | Responsável | Horas previstas |
   Reserva (apoio + retrabalho): <h>h (<p>% da sprint) · retrabalho migrado <x>h · livre para apoio <y>h
   Capacidade: revisão <h>h (usa <x>h) · especificação <h>h (usa <x>h) · vazão prevista <n> fatias · lead time médio <d> dias · HITL <h>h
   Próximas a puxar (fora da previsão, na ordem): <FT…>
   ```
7. "ok" → grave `sprints/<pai>/sprint-<nn>.md` (com `**Power sdd:**` = o `metadata.version` desta skill), `sprint`, `responsavel`, `status` e o `modo` final no `backlog.md` pelo bloco
   [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) e **publique sempre no EWM** ([references/elm-sprint.md](references/elm-sprint.md) §1–4), para a sprint e o EWM ficarem iguais. Sem o MCP `elm` ou com
   falha, a coluna "Tarefa ELM" fica `pendente` e é publicada depois. Publicada, **sincronize** (abaixo): o que já
   estava na iteração por fora entra na sprint.

## Modo pela senioridade

O `modo` que a triagem ou o fatiamento gravaram é a proposta para a **fatia** (critérios da `sdd-fatiar`). O modo
final sai quando a fatia ganha responsável — na seleção da sprint ou no encaixe —, pela `senioridade` de quem
implementa no `equipe.json`:

| Senioridade | Modo da fatia |
|---|---|
| `Júnior` | sempre `HITL` |
| `Pleno` | o sdd aplica os critérios da `sdd-fatiar` (inclusive "tipo de trabalho novo começa `HITL`") e propõe; a pessoa confirma |
| `Sênior` | `AFK` por padrão; `HITL` só com motivo forte da fatia — decisão de produto ou de UX no caminho, dado sensível, risco alto (diga qual) |

Modo final diferente do backlog → grave-o com `obs` `modo pela senioridade (<login>)`; o `HITL` do Sênior leva o
motivo: `modo pela senioridade (<login>): HITL — <motivo>`.

**Revisor** (fatia HITL): a `[REV]` é sempre de um **Dev Sênior** ativo — o Sênior revisa os PRs do Pleno e do
Júnior. PR de um Sênior → outro Sênior; se ele for o **único** Sênior ativo, ele mesmo, com `revisor único` na
Observação da linha da fatia no `sprint-<nn>.md`. Conte essas revisões, e as aprovações (`[APR]`), nas horas de
revisão dos Sêniores. A senioridade também decide o GATE do plano (Júnior sempre, Pleno se pedir, Sênior nunca —
`sdd-plano` Passo 5).

Fatia já iniciada (com `status.md`) só troca de **AFK para HITL**, pela [Troca de modo](#troca-de-modo-afk--hitl);
**HITL → AFK nunca** — nem sugerido nem aceito.

## Durante a sprint

"Como está a sprint?" → **`sdd-status`** filtrado pela sprint (fase de cada fatia, bloqueios, WIP de revisão,
PRs parados). Fatia que cresceu (passou de `G` no plano) → volte para a `sdd-fatiar` (dividir) em vez de esticar.
Apoio que estoura a reserva → mostre ao P.O. e ele decide qual fatia sai da sprint; o Apoio nunca tira
fatia sozinho.

**Sincronizar com o EWM** ("sincroniza a sprint"; o painel da `sdd-status` avisa quando há tarefa por fora) — tarefa
criada direto no EWM na iteração da sprint (Apoio, ou uma `[DEV]`/`[ESP]` aberta à mão quando a sessão do agente
parou) entra na sprint com o mesmo id: o sdd infere o que ela é, pergunta e, se for o caso, renomeia o título ou
inclui o prefixo ([references/elm-sprint.md](references/elm-sprint.md) §9). Sem o MCP `elm` → diga que não há como
comparar e pare.

**Encaixe** — só quando puxar não basta: a fatia `pronta` que alguém quer começar **não é a do topo** (fura a
fila) ou o **WIP de revisão está no limite** (de qualquer trilha); a `sdd-desenvolver` manda para cá. Apoio triado quando a reserva estourou é o mesmo encaixe (a
`sdd-triar` manda para cá): a decisão do P.O. vai na linha do item na seção Apoio do `sprint-<nn>.md`. Mostre ao P.O. a fatia (trilha, tamanho, modo, origem), o que sobra da
capacidade (revisão, vazão, HITL) e as opções, com a recomendada:
- **entra na folga** — cabe sem tirar nada;
- **entra no lugar de** `FT-…` — uma ainda não iniciada, que volta para `sprint` `—`;
- **fica para a próxima sprint**.

Com a decisão do P.O. (ou de quem ele delegou): `sprint`, `responsavel` e o modo final pela
[senioridade](#modo-pela-senioridade) no `backlog.md` (e, na fatia HITL, revisor — Dev Sênior, pela [regra do
revisor](#modo-pela-senioridade) — e verificador, que não seja quem implementa — as `[REV]`/`[VER]` precisam deles), uma linha no
`sprint-<nn>.md` com a Observação `encaixe: <decisão> (<quem decidiu>, <data>)`, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base), e no EWM o IB da fatia
passa do backlog para a iteração da sprint e as tarefas nascem ([references/elm-sprint.md](references/elm-sprint.md) §3–4; Apoio: §6). Na troca, a fatia que
sai volta para `sprint` `—`: o IB dela e as tarefas voltam ao backlog do EWM
(`elm_atualizar_wi(ids, iteracao = backlog)`; [references/elm-sprint.md](references/elm-sprint.md) §3). Depois, volte à `sdd-desenvolver` (Passo 3, item 4). Sem
decisão, a fatia não começa; urgência acelera a decisão, não a dispensa.

## Troca de modo (AFK → HITL)

O plano de uma fatia AFK mostrou risco e o Dev aceitou a sugestão (`sdd-plano` Passo 5), ou o loop parou a fatia:
ela está em `bloqueada (de: planejando)` com `aguardando troca para HITL` e o motivo. A decisão é do P.O. (ou do
SM), aqui, na base:

1. Mostre a fatia, o motivo (Histórico do `status.md` da branch, por `git show origin/<branch>:…`) e a sugestão de
   **revisor** (Dev Sênior ativo, pela [regra do revisor](#modo-pela-senioridade)) e de **verificador** (não quem
   implementa), cada um o de **menor alocação** na sprint: a soma das horas estimadas das tarefas abertas de cada
   pessoa na iteração da sprint no EWM (`elm_listar_wi(iteracao, dono)`); sem ELM, a contagem
   de fatias de cada um no `sprint-<nn>.md`.
2. "ok" → `modo: HITL` na linha da fatia no `backlog.md`; no `sprint-<nn>.md`, Modo `HITL`, Revisor, Verificador e a
   Observação `modo: AFK → HITL (<quem>, <data>, <motivo>)` — pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base).
   Com o "ok", crie a `[REV]` e a `[VER]` ([references/elm-sprint.md](references/elm-sprint.md) §7) e grave os ids na coluna "Tarefa ELM".
3. Avise o Dev: ele retoma pela `sdd-iniciar` → `sdd-desenvolver`, que sincroniza o `status.md` com a troca.

Não troca → Observação `modo: AFK mantido (<quem>, <data>)` no `sprint-<nn>.md` e avise o Dev, que retoma no AFK
(`sdd-plano` Passo 5, GATE). **HITL → AFK nunca.**

## Review

### Pré-condição dos ritos de fechamento

Antes da review, da retrospectiva da sprint e da virada — **em cada um** —, **sincronize com o EWM** (§9 do
[elm-sprint.md](references/elm-sprint.md); sem tarefa por fora, segue calado; sem o MCP `elm` → avise "sincronização com o EWM não feita" e siga) e levante as fatias da sprint aberta que
esperam só a consolidação, como a [`sdd-status`](../sdd-status/SKILL.md) (Coleta, itens 1–2: `status.md` nas
branches remotas e o PR pelo `gitlab_listar_mrs`): fase `mergeada`, ou `pronta-para-merge` com o PR `merged` (antes,
o Dev registra `mergeada` e conclui a `[DEV]` — `sdd-desenvolver` Passo 6). Nenhuma → siga o rito. Alguma →
**pare** e mostre:

```
⛔ Consolidação antes do fechamento da sprint <nn>
| FT | Fase | PR | Falta |
| FT-031 | mergeada | <link> | sdd-consolidar (P.O. ou SM, agente sdd-produto) |
Consolide todas antes da review, da retrospectiva e da virada: só fatia consolidada conta na vazão, entra na
review e fecha no EWM. Seguir mesmo assim? (decisão do P.O.)
```

Segue só com o "sim" do **P.O.** (outra pessoa → peça a decisão a ele), gravado no cabeçalho do `sprint-<nn>.md`:
`**Fechamento sem consolidar:** FT-… (<P.O.>, <data>)`. A decisão vale para essas fatias nos ritos seguintes da
mesma sprint (não pergunte de novo); elas migram como as não concluídas, com a Observação `não consolidada`. Fatia
sem merge (`pr-aberto`, `em-revisao`…) não entra aqui: migra, como sempre.

### Rito

Para cada fatia concluída: o cenário entregue e a **evidência** do `verificacao.md` (resposta, contagem,
screenshot). Registre o retorno do P.O. no `sprint-<nn>.md`; pedido novo vira cenário/fatia nova pela `sdd-prd`/
`sdd-fatiar` — não reabre fatia concluída.

## Retrospectiva e virada

0. **Pré-condição** — a [dos ritos de fechamento](#pré-condição-dos-ritos-de-fechamento), antes da retrospectiva
   e de novo antes da virada.
1. **Retrospectiva com dados** — `sdd-aprender` modo retrospectiva (vazão, lead time, rodadas de revisão,
   correções humanas por causa, AFK que chegaram ao PR sozinhas). Registre no `sprint-<nn>.md`: bom · melhorar ·
   ações (cada ação com dono).
2. **Horas:** relatório da sprint por tipo e por pessoa ([references/elm-sprint.md](references/elm-sprint.md) §5). Preencha "Números"
   (planejadas × lançadas) e aponte as tarefas concluídas sem horas lançadas — só aqui, no fechamento.
   **Créditos** (só do git, nunca do `~/.kiro`): a coluna Créditos dos Números soma as colunas Créditos das seções
   Fatias, Especificação e Apoio e a seção Créditos de gestão; `**Power sdd:**` ganha as versões que
   aparecem nessas linhas e nos `status.md`/fichas dos itens concluídos, em ordem crescente; aponte fatia, item de Apoio ou
   `[ESP]` concluída com Créditos `—` (ninguém fechou a sessão). Fatia migrada leva os créditos para a sprint em
   que for consolidada. **`backlog.md`:** a coluna `creditos` de cada fatia, item de Apoio e épico concluído na sprint recebe
   o valor da coluna Créditos dele no `sprint-<nn>.md` — só aqui, no commit da virada (bloco Gravar na base).
3. **Fechar:** concluídas — previstas e puxadas — contam na vazão e no lead time; a meta é avaliada (atingida ou
   não, e por quê); não concluídas — fatias (inclusive as do `**Fechamento sem consolidar:**`, com `não consolidada`), `[ESP]` e
   Apoio — **migram**
   para a próxima sprint (no `sprint-<nn>.md` antigo ficam com "→ sprint <próxima chave>" — `2026/04` → `2027/01`
   na troca de pai; o histórico não é apagado) e ele fica com `**Situação:** fechada`; no arquivo da próxima, cada item migrado ganha a sua linha (seção
   Fatias, Especificação ou Apoio) com a Observação `migrada da sprint <chave>`. Fatia ou item de Apoio migrado → `sprint` = a próxima chave na linha do `backlog.md` (fatias e
   `## Apoio`), pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base). Item de Apoio em `backlog` (triado sem sprint aberta) entra no planejamento da próxima como as fatias.
4. Recalcule vazão média, lead time médio e horas por tipo (`equipe.json` → `historico`). Reserva (apoio +
   retrabalho): o % é o do `acordos.md`; mostre o consumido da sprint (horas das tarefas de Apoio + retrabalho) contra ela
   e, se ficou muito acima ou abaixo, **proponha** um novo % ao P.O. — muda o acordo só com "ok". Replaneje a
   próxima pelo modo sprint (migradas consomem capacidade primeiro).
5. **ELM** — virada ([references/elm-sprint.md](references/elm-sprint.md) §5): as não concluídas só mudam de iteração e as novas são publicadas (§4). Iteração do
   EWM mais longa que a sprint (a mesma cobre as duas) → nada muda no EWM; diga isso, e o relatório de horas da
   sprint conta só as tarefas listadas no `sprint-<nn>.md`, não a iteração inteira.

## Regras

- Créditos do Kiro: toda sessão desta skill que grava na base (planejamento, encaixe, troca de modo, virada) põe,
  no mesmo commit, a linha de créditos dela na seção **Créditos de gestão** do `sprint-<nn>.md` aberto (Atividade = o modo;
  ([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4)).

- Nunca planeje acima da capacidade de revisão: trabalho que ninguém revisa não está pronto, só está parado.
- Fatia nunca se espalha por sprints para caber; se não cabe, divide.
- Tamanho é do time; o agente propõe P/M/G com justificativa, a pessoa decide. Nada de Planning Poker em pontos: a
  previsão é pela vazão.
- Pontos, se o time os usar no EWM, ficam só no IB (plan item), nunca nas tarefas, e não entram no planejamento.
- O compromisso da sprint é a meta: fatia prevista que não entrou não é falha; meta não atingida vai para a retro.
- Toda hora planejada tem tarefa: nada de especificação ou Apoio fora da sprint.
