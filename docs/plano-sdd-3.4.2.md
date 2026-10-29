# Plano — a sincronização leva o sdd até onde o trabalho chegou (sdd 3.4.2)

## Objetivo

Permitir o desenvolvimento tradicional quando os tokens acabam. A pessoa segue sem agente (código, PR, merge, tarefas
no EWM), e a "sincroniza a sprint" (§9 do `sdd-planejamento/references/elm-sprint.md`) leva o sdd até onde o
trabalho chegou. Toda diferença entre `status.md` e EWM, ou entre `sprint-<nn>.md` e `backlog.md`, vira uma linha da
tabela com uma solução sugerida, e nada é gravado sem o "ok" ou o ajuste da linha.

Exemplo que a 3.4.1 não resolve: o Dev fez o código, o PR e o merge por fora; a `[DEV]` segue iniciada e `[APR]`,
`[REV]` e `[VER]` abertas. Hoje dá `manter` para sempre. Na 3.4.2: fatia `pronta`, `[DEV]` concluída e as outras
três canceladas.

## Decisões

| # | Questão | Opções | Decisão |
|---|---|---|---|
| 0 | Papel da sincronização | conferir EWM × arquivos (3.4.1) · levar o sdd até onde o trabalho chegou | **levar o sdd até onde chegou**, com o git (branch, PR, merge) como evidência. Revê a decisão 3 da 3.4.1 |
| 1 | Campo que o EWM não traz | `falta: …` · `—` | **como hoje** (`falta: prazo, critério de pronto`) |
| 2 | Tabela | uma linha por WI e campo · agrupada | **agrupada por item** (IB e tarefas juntos), numeração corrida; cabeçalho `<n> divergências em <m> itens · <k> conferidos` |
| 3 | IB ou defeito do backlog alterado no EWM fora da sprint | não ver · ler um a um · listar o backlog | **listar o backlog do EWM** numa chamada e comparar estado e dono |
| 4 | Tarefa já fechada quando alguém retoma | deixar falhar · tratar o `precondicao` do `assumir` | **tratar**: PR mergeado → Passo 6 da `sdd-desenvolver`; senão, reabrir. O mesmo na `sdd-atender` e na `sdd-executar` |
| 5 | `[REV]`, `[VER]`, `[APR]` e `[DEV]` × fase do `status.md` | só as linhas genéricas · pela fase | **pela fase** (tabela abaixo) |
| 6 | Fatia com `status.md` numa branch e ainda `planejada` | rede de proteção só nos ritos · no §9 | **no §9**: conta como iniciada e gera `arquivo: iniciada`; nunca "sai da sprint" |
| 7 | WI que sumiu do EWM | `manter` para sempre · pendência | **`manter` registra `ELM pendente [<tipo> <id> sumiu]`**, que tira o id da comparação até o `ELM feito` |
| 8 | MCP `elm` | sem mudança · cancelar · todas as melhorias | **cancelar**: `elm_transicao(<id>, "cancelar")`; as outras melhorias seguem adiadas |
| 8a | Quem grava `pronta` | só a `sdd-desenvolver` · também a sincronização | **também a sincronização**, pela evidência do merge (Créditos e lições `—`) |
| 9 | Versão | — | **3.4.2** para o `plugin.json`, as 22 skills e a mcp-elm, juntos; `plugin.json` exige `mcp-elm ≥ 3.4.2` |
| 10 | Migração | — | nenhuma |

## Casos de desenvolvimento por fora

| Evidência no git | Solução sugerida |
|---|---|
| PR mergeado, fatia antes de `pronta` | `arquivo: pronta` (como o Passo 6) · concluir a `[DEV]` · cancelar `[APR]`, `[REV]` e `[VER]` abertas · depois a `sdd-consolidar` |
| PR mergeado, fatia `pronta` | cancelar as tarefas abertas; concluir a `[DEV]` |
| PR aberto | `arquivo: iniciada` e `status.md` na fase do PR (`pr-aberto` no HITL, `aguardando-aprovacao-pr` no AFK) |
| branch com commits, sem PR | `arquivo: iniciada` e `Fase: implementando` |
| PR fechado sem merge | `manter: o Dev diz` (retomar ou cancelar) |
| `sprint-<nn>.md` × `backlog.md` diferentes | a versão mais adiantada pelas evidências; sem evidência, `manter` com as duas na linha |

## Estado esperado pela fase (decisão 5)

Conferir na implementação com o `sdd-desenvolver/references/status-template.md`.

| Fase | `[DEV]` | `[REV]` | `[VER]` | `[APR]` |
|---|---|---|---|---|
| `pesquisando` · `planejando` | em andamento | nova | nova | plano: nova ou ausente |
| `aguardando-aprovacao-plano` | em andamento | nova | nova | plano: aberta |
| `implementando` · `revisando` | em andamento | nova | nova | plano: concluída |
| `pr-aberto` · `em-revisao` | em andamento | aberta | nova | — |
| `aceita` · `verificando` · `verificada` | em andamento | concluída | aberta → concluída | — |
| `aguardando-aprovacao-pr` (AFK) | em andamento | — | — | PR: aberta |
| `pronta` · `concluida` | concluída | concluída | concluída | concluídas |
| `retrabalho` · `bloqueada` | a da fase de origem | idem | idem | idem |

## O que muda

- **`elm-sprint.md` §9:** fontes novas (git, PR, `sprint-<nn>.md` × `backlog.md`, backlog do EWM, fase do
  `status.md`); tabela agrupada; soluções novas (casos acima, fase, `status.md` em branch, `sumiu`); exceção à regra
  "linha de estado da fatia não tem `arquivo`" quando há evidência do git.
- **`sdd-desenvolver`, `sdd-atender`, `sdd-executar`:** tratar o `precondicao` do `assumir`.
- **`sdd-planejamento`:** a rede de proteção entra no §9.
- **`sdd-fatiar/references/backlog.md`:** a sincronização também grava `pronta`.
- **Cancelamento:** onde hoje há pendência porque "o MCP não cancela" (`elm.md`, `sdd-triar`, `sdd-fatiar`,
  `sdd-planejamento`, `sdd-desenvolver`, `sdd-loop`), passa a ser `elm_transicao(<id>, "cancelar")` com "sim"; a
  pendência fica só para a falha.
- **`sdd-status`:** o painel conta as divergências novas que a listagem mostra.
- **`mcps/elm`:** alvo `cancelar` em `ewm.py` e `server.py` (só ações que levam a um estado de descarte; já cancelada
  → `ja_estava`; concluída ou workflow sem descarte → `precondicao`), testes, manual e `pyproject.toml` em 3.4.2.
- **Versão:** `README.md`, `plugin.json` e as 22 skills.
- **Permissões:** nenhuma muda (o agente de produto já lê git e MR; `cancelar` entra em `elm-tarefa`, com pergunta).

## Verificação

- PR mergeado por fora com `[DEV]`, `[APR]`, `[REV]` e `[VER]` abertas → a tabela propõe `pronta`, concluir e
  cancelar; com o "ok", a `sdd-consolidar` aceita a fatia.
- PR aberto por fora, fatia `planejada` sem `status.md` → propõe `iniciada` e a fase do PR.
- IB `elegivel` cancelado no backlog do EWM → linha na tabela, sem a fatia estar na sprint.
- `[DEV]` concluída à mão e fatia retomada → a skill oferece o Passo 6 ou reabrir.
- `[VER]` concluída com a fatia em `implementando` → `EWM: reabrir a [VER]`.
- WI sumido com `manter` → não volta enquanto a pendência `sumiu` estiver aberta.
- `cancelar` no fake do MCP: Novo e Em Andamento → cancelado; cancelado → `ja_estava`; concluído → `precondicao`.
- `grep -rn "o MCP não cancela" powers/sdd` → nada; testes do power e pytest do MCP passam.

## Fica para a revisão da 3.4.1

- O "sim" do P.O. nas linhas de escopo (decisão 6 da 3.4.1), onde se pediu que o "ok" aprovasse tudo.
- "Encaminhar à skill dona" só existe para a `[DEV]`; `[ESP]` e IB concluídos antes da hora só têm `EWM: reabrir`.
- A `sdd-iniciar` trata a tarefa com o título mantido como fora da sprint.
- O piloto da seção 7 da 3.4.1.
