# Plano — campos vazios, tabela agrupada e as lacunas que a 3.4.1 deixou na sincronização com o EWM (sdd 3.4.2)

## Contexto

A 3.4.1 (no `main` desde `a1ae8c5`; plano em `docs/plano-sdd-3.4.1.md`) reescreveu o §9
do `powers/sdd/skills/sdd-planejamento/references/elm-sprint.md`. A sincronização passou a comparar as tarefas
conhecidas, além das por fora, numa tabela só, com a solução proposta por linha. As referências de linha abaixo são da
3.4.1 do `main` (`a1ae8c5`).

Na conferência da 3.4.1 contra o que se pediu ao revisar o rascunho dela, sobraram quatro pendências:

1. **Campo que o EWM não traz.** Foi pedido `—` no campo correspondente, sem inferir. A seção Por fora do §9 ainda grava
   `falta: prazo, critério de pronto` na ficha do item de Sustentação que nasce de uma tarefa por fora
   (`elm-sprint.md:494-495`), como na 3.4.0. Nenhuma das decisões 1–25 da 3.4.1 trata disso. O power fica
   incoerente: o lote "importar do EWM" da `sdd-triar` já grava prazo e critério de pronto `—` no mesmo caso
   (`sdd-triar/SKILL.md:235-236`).
2. **Tabela agrupada por tarefa ou IB.** A tabela da 3.4.1 tem uma linha por WI e por campo, sem agrupamento
   (`elm-sprint.md:319-345`). O cabeçalho conta os itens conferidos (`9 divergências · 41 itens conferidos`), não os
   itens com divergência.
3. **Lacunas que continuam abertas:**
   1. **IB ou defeito do backlog alterado no EWM fora da sprint.** Os ids "do backlog" e "terminal de fora" só geram
      linha quando aparecem na listagem da iteração da sprint (`elm-sprint.md:260-307`). Fora dela, nunca são lidos:
      o IB cancelado ou concluído à mão no backlog do EWM segue `nova`/`elegivel` no `backlog.md`. O "importar do
      EWM" da `sdd-triar` exclui todo id conhecido.
   2. **`[DEV]` concluída à mão quando a fatia é retomada.** O §9 acusa (`elm-sprint.md:396`, `manter: o Dev confere`),
      mas a `sdd-desenvolver` retoma e chama `assumir` sem ler o estado (`sdd-desenvolver/SKILL.md:45`, `:65`,
      `:149`). O MCP recusa a tarefa fechada com `precondicao` ("já concluída: reabra antes", `ewm.py:527-528`), e a
      skill não diz o que fazer. A `sdd-atender` (`:50`) e a `sdd-executar` (`:40`) têm o mesmo furo, que a seção 6
      da 3.4.1 só registra.
   3. **Estado de `[REV]`, `[VER]` e `[APR]` em relação à fase do `status.md`.** O §9 lê o `status.md` só pelos ids,
      nunca pela `fase`. As linhas genéricas da tabela Fatia (`elm-sprint.md:398`, `:401`) pegam a tarefa descartada
      e a tarefa aberta depois de `pronta`. Ficam de fora, por exemplo: a `[VER]` concluída com a fatia ainda em
      `implementando`; a `[APR] Aprovar plano` aberta com o plano já aprovado; a `[DEV]` ainda Nova com a fatia
      `iniciada`.
   4. **Fatia com `status.md` numa branch e ainda `planejada` na base.** A linha da tabela Fatia exclui esse caso e o
      deixa para a rede de proteção (`elm-sprint.md:397`), que só roda na pré-condição dos ritos
      (`sdd-planejamento/SKILL.md:258-264`) e depois do §9. Sob pedido, a resposta é "iguais". Nos ritos, se o IB
      foi movido no EWM, o §9 decide "saiu" pela situação do `backlog.md` e propõe "sai da sprint" para uma fatia já
      começada, quando a regra é "de `iniciada` em diante nada volta".
   5. **WI que sumiu do EWM.** A única solução para `nao_encontrado` é `manter: confira na UI do EWM`, com Outras `—`
      (`elm-sprint.md:449`). Como o `manter` volta na próxima sincronização, a linha volta para sempre e a linha
      "iguais" nunca sai.
4. **MCP `elm`.** A decisão 17 da 3.4.1 é "sem mudança (pedido)". A seção 6 dela adia melhorias que a sincronização
   usaria:
   - `estimativa_h` e o grupo do estado no `elm_listar_wi`: hoje é um `elm_ler_wi` por id; as "Planejadas" e a
     menor alocação da Troca de modo não têm fonte;
   - a data da conclusão no `elm_ler_wi`: o `concluida-em` recebe a data da sincronização, e a tarefa fechada
     movida não é apontada;
   - o pai na listagem: o pai trocado não é visto, e a duplicata criada no backlog para uma fatia na sprint também
     não;
   - cancelar por `elm_transicao`: hoje o cancelamento é a pendência manual `[<id> cancelar]`;
   - o teto de 1000 itens: a sincronização avisa e para.

## Discussões e decisões

| # | Questão | Opções levantadas | Decisão |
|---|---|---|---|
| 1 | Campo que o EWM não traz (tarefa ou item trazido do EWM) | inferir · `falta: …` · `—` | **`—`** no campo correspondente, nunca inventado (pedido). Na ficha: `**Prazo:** —`, `**Critério de pronto:** —`, `**Pedido por:** —` e `**Estimativa:** —` sem estimativa no EWM. Tarefa sem dono que vira item → `responsavel` `—`. `[ESP]` sem estimativa → Horas previstas `—`. É o marcador de vazio que as tabelas já usam e o que o lote da `sdd-triar` grava |
| 2 | Agrupar a tabela | uma linha por WI e campo (3.4.1) · agrupada por tarefa ou IB | **agrupada** (pedido). Proposta de forma: as linhas de um mesmo item (o IB ou a origem e as tarefas dele) ficam juntas, na ordem da coluna Item; a linha de publicação continua primeiro; numeração corrida, para o ajuste por linha seguir igual. Cabeçalho `<n> divergências em <m> itens · <k> conferidos` |
| 3 | IB ou defeito do backlog alterado no EWM fora da sprint | um `elm_ler_wi` por id do backlog · uma listagem do backlog do EWM (`elm_listar_wi(iteracao = backlog)`) · passo novo no "importar do EWM" · aceitar | **em aberto** — proposta: a listagem do backlog no §9, numa chamada, comparando estado e dono dos ids "do backlog". Título não (decisão 11 da 3.4.1). Prioridade não vai ao EWM (`sdd-fatiar/references/backlog.md`, coluna `prioridade`). A descrição não vem na listagem |
| 4 | `[DEV]` (e tarefa de Sustentação) já fechada quando o trabalho é retomado | ler o estado antes do `assumir` · tratar o `precondicao` do `assumir` · deixar para a sincronização | **em aberto** — proposta: tratar o `precondicao`, sem chamada a mais. Na `sdd-desenvolver`: PR mergeado → Passo 6; senão `elm_transicao(<id>, "reabrir")` com "sim". Na `sdd-atender`/`sdd-executar`: reabrir, ou levar o item a `concluido` como a sincronização faz |
| 5 | Estado de `[REV]`, `[VER]`, `[APR]` e `[DEV]` pela fase do `status.md` | comparar pela fase · só as linhas genéricas (3.4.1) | **em aberto** — proposta: o §9 lê a `fase` (regra A base prevalece) e compara pelo estado esperado da fase (rascunho abaixo), com `manter` quando quem resolve é o papel e `EWM:` quando o EWM está à frente |
| 6 | Fatia com `status.md` numa branch e ainda `planejada` na base | rede de proteção antes do §9 · o §9 trata a fatia como iniciada · como está | **em aberto** — proposta: o passo 2 do §9 olha os `status.md` das branches, como a rede de proteção. Fatia com `status.md` conta como iniciada para "saiu" (o EWM volta, nunca "sai da sprint") e gera a linha `arquivo: iniciada (status.md na branch)`, que grava como a rede de proteção grava. Vale também sob pedido |
| 7 | WI que sumiu do EWM | `manter` (3.4.1) · `arquivo:` o id vira `pendente` e o §3–4 republica · `manter` com pendência registrada | **em aberto** — proposta: a solução continua `manter: confira na UI do EWM`, mas o `manter` dessa linha registra `ELM pendente [<tipo> <id> sumiu]`, que tira o id da comparação até o `ELM feito` (como a decisão 13 da 3.4.1). Em Outras, `arquivo: pendente (republicar)` |
| 8 | MCP `elm` | sem mudança (decisão 17 da 3.4.1) · incluir as melhorias da seção 6 da 3.4.1 | **em aberto** — pela versão única, se mudar, a mcp-elm sobe junto, e o `plugin.json` passa a exigir a nova |
| 9 | Versão | 3.4.2 sozinha | **3.4.2**: `plugin.json`, as 22 skills e o MCP se a decisão 8 o alterar |
| 10 | Migração | — | nenhuma (o power ainda não tem usuários) |

### Estado esperado pela fase (rascunho para a decisão 5)

Conferir cada linha com quem grava a fase no `sdd-desenvolver/references/status-template.md` e com os nomes de estado
da PA no `sdd.md`.

| Fase no `status.md` | `[DEV]` | `[REV]` (HITL) | `[VER]` (HITL) | `[APR]` |
|---|---|---|---|---|
| `pesquisando` · `planejando` | em andamento | nova | nova | Aprovar plano: nova ou ausente |
| `aguardando-aprovacao-plano` | em andamento | nova | nova | Aprovar plano: aberta |
| `implementando` · `revisando` | em andamento | nova | nova | Aprovar plano: concluída (com GATE) |
| `pr-aberto` · `em-revisao` | em andamento | aberta | nova | — |
| `aceita` · `verificando` · `em-verificacao` · `verificada` | em andamento | concluída | aberta → concluída | — |
| `aguardando-aprovacao-pr` (AFK) | em andamento | — | — | Aprovar PR: aberta |
| `retrabalho` | em andamento | reaberta quando a volta passa pela revisão | idem | Aprovar PR reaberta (conflito no merge) |
| `pronta` · `concluida` | concluída | concluída | concluída | concluídas |
| `bloqueada (de: <fase>)` | a da fase de origem | idem | idem | idem |

## Mudanças propostas

### `sdd-planejamento/references/elm-sprint.md`

- **Por fora** (`:458-` e `:494-495`): `falta: prazo, critério de pronto` → os campos com `—` (decisão 1). Tarefa
  sem dono → `responsavel` `—`. A `[ESP]` sem estimativa na linha "entrou: épico com a `[ESP]`" (`:452`) → Horas
  previstas `—`.
- **Tabela** (`:319-345`): agrupamento e cabeçalho (decisão 2), atualizando o exemplo.
- **Passo 1 e 2** (`:254-307`): a listagem do backlog e os ids "do backlog" comparados (decisão 3, se aprovada); a
  fatia com `status.md` em branch (decisão 6).
- **Soluções propostas — Fatia** (`:392-406`): as linhas pela fase (decisão 5). A linha `:397` passa a cobrir a
  fatia com `status.md` em branch (decisão 6).
- **Soluções propostas — Iteração** (`:449`): o `sumiu` com a pendência registrada (decisão 7).

### Demais skills

- `sdd-desenvolver/SKILL.md` (`:45`, `:65`, `:149`), `sdd-atender/SKILL.md:50`, `sdd-executar/SKILL.md:40`: o
  `precondicao` do `assumir` (decisão 4). Tirar o item correspondente da seção 6 da 3.4.1.
- `sdd-planejamento/SKILL.md` (pré-condição, `:250-264`): a rede de proteção deixa de ser a única a ver o
  `status.md` em branch (decisão 6).
- `sdd-status/SKILL.md`: o painel conta as divergências novas que a listagem já mostra. As que exigem `elm_ler_wi`
  ou a fase ficam para a sincronização, como a estimativa na 3.4.1.
- `sdd/references/elm.md`: a chave `[<tipo> <id> sumiu]` na tabela de pendências (decisão 7).
- `README.md` (nota da 3.4.2), `plugin.json` e o `metadata.version` das 22 skills.
- `mcps/elm`, se a decisão 8 o incluir.

## Para a revisão final da 3.4.1

Achados da conferência da 3.4.1 que não são pendências desta versão, mas pesam na revisão dela:

- **Diferenças do que foi pedido no rascunho:**
  - a decisão 6 pede o "sim" do P.O. nas linhas de escopo, onde se pediu que o "ok" aprovasse tudo;
  - as decisões 3, 7 e 8 gravam a situação da fatia na Volta e no encaixe;
  - o "encaminhar à skill dona" existe só para a `[DEV]` concluída (`elm-sprint.md:396`). `[ESP]` concluída e IB
    da fatia ou do épico concluído antes da hora só têm `EWM: reabrir` (`:399`, `:427`, `:430`).
- **Inconsistências internas que seguem:**
  - a `sdd-iniciar` (`:83-86`) trata a tarefa sem prefixo do sdd como fora da sprint, mas a decisão 11 deixa
    "manter o título": a tarefa trazida assim já está na sprint;
  - na sprint não publicada, não está escrito que as divergências achadas depois da publicação voltam numa tabela
    nova, à espera de outro "ok".
- **Já resolvidas na 3.4.1 final** (seção 8 do plano dela): a pendência de cancelamento da puxada vai para o
  Histórico do `status.md` (o texto da decisão 7a ainda diz "rodapé da ficha"); a "minha próxima tarefa" da
  `sdd-iniciar` lê a sprint pelos arquivos enquanto há `**Publicação no EWM:** pendente`; o ensaio de mesa foi feito.
- **A fazer:** o piloto da seção 7 da 3.4.1.

## Verificação

- Tarefa de Sustentação por fora, sem dono, sem estimativa e sem prazo → o item nasce com `responsavel`,
  `**Estimativa:**`, `**Prazo:**`, `**Critério de pronto:**` e `**Pedido por:**` em `—`, e nenhum `falta:`.
  `grep -rn "falta: prazo" powers/sdd` → nada.
- Tabela com divergências em três itens, um deles com IB e duas tarefas → as linhas de cada item juntas, numeração
  corrida, o cabeçalho com `em 3 itens`, e o ajuste `<n>: …` aplicado à linha certa.
- IB de fatia `elegivel` cancelado no backlog do EWM → linha na sincronização, sem a fatia estar na sprint
  (decisão 3).
- Fatia `iniciada` com a `[DEV]` concluída à mão e retomada pela `sdd-desenvolver` → a skill mostra o estado e
  oferece o Passo 6 ou reabrir, nunca um `assumir` que falha calado. O mesmo na `sdd-atender` e na `sdd-executar`.
- Fatia em `implementando` com a `[VER]` concluída → linha `EWM: reabrir a [VER]` (decisão 5).
- Fatia `planejada` na base com `status.md` numa branch e IB movido para o backlog → a sincronização sob pedido
  mostra a linha; nos ritos, a solução nunca é "sai da sprint".
- WI `nao_encontrado` com `manter` → na sincronização seguinte, não volta enquanto a pendência `sumiu` estiver
  aberta.
- Testes do power (`test_gerar_agentes.py`, `test_creditos.py`) e, se o MCP mudar, o pytest dele.
