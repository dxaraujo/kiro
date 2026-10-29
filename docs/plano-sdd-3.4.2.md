# Plano — sincronização que fecha o trabalho feito por fora do sdd, tabela agrupada e as lacunas que a 3.4.1 deixou (sdd 3.4.2)

## Contexto

A 3.4.1 (no `main` desde `a1ae8c5`; plano em `docs/plano-sdd-3.4.1.md`) reescreveu o §9
do `powers/sdd/skills/sdd-planejamento/references/elm-sprint.md`. A sincronização passou a comparar as tarefas
conhecidas, além das por fora, numa tabela só, com a solução proposta por linha. As referências de linha abaixo são da
3.4.1 do `main` (`a1ae8c5`).

**O intuito da sincronização** (pedido): possibilitar o desenvolvimento da maneira tradicional quando acabarem os
tokens. A pessoa segue sem agente — altera o código, abre o PR, faz o merge, mexe nas tarefas do EWM — e a
sincronização leva o sdd até onde o trabalho chegou. Por isso tudo o que estiver diferente entre o `status.md` e o
EWM, ou entre o `sprint-<nn>.md` e o `backlog.md`, tem de ser tratado: entra na tabela com uma solução sugerida.

A 3.4.1 não faz isso. Exemplo: o Dev alterou o código, abriu o PR e fez o merge por fora do sdd; a `[DEV]` segue
iniciada e a `[APR]`, a `[REV]` e a `[VER]` seguem abertas, mas está tudo feito. Na 3.4.1 a sincronização só
compara o EWM com os arquivos, não olha o git, e a situação da fatia nunca muda por ela (decisão 3 da 3.4.1: nas
linhas de estado da fatia, só `EWM` ou `manter`). O resultado é `manter` em toda rodada.

Na conferência da 3.4.1 contra o que se pediu ao revisar o rascunho dela, sobraram também estas pendências:

1. **Campo que o EWM não traz.** O `—` foi cogitado no lugar do `falta: prazo, critério de pronto` da seção Por fora
   (`elm-sprint.md:494-495`); **fica como é hoje** (decisão 1).
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
| 1 | Campo que o EWM não traz (tarefa ou item trazido do EWM) | inferir · `falta: …` · `—` | **como é hoje** (pedido): a seção Por fora segue com `falta: prazo, critério de pronto` e `**Estimativa:**` a da tarefa (ou `—`) |
| 0 | Para que serve a sincronização | conferir o EWM contra os arquivos (3.4.1) · levar o sdd até onde o trabalho chegou | **levar o sdd até onde o trabalho chegou** (pedido): possibilitar o desenvolvimento tradicional quando acabarem os tokens. Toda diferença entre `status.md` e EWM, ou entre `sprint-<nn>.md` e `backlog.md`, é uma linha da tabela com solução sugerida; o estado do git (branch, PR, merge) entra como evidência. Revê a decisão 3 da 3.4.1 (seção Desenvolvimento por fora do sdd) |
| 2 | Agrupar a tabela | uma linha por WI e campo (3.4.1) · agrupada por tarefa ou IB | **agrupada** (pedido). Proposta de forma: as linhas de um mesmo item (o IB ou a origem e as tarefas dele) ficam juntas, na ordem da coluna Item; a linha de publicação continua primeiro; numeração corrida, para o ajuste por linha seguir igual. Cabeçalho `<n> divergências em <m> itens · <k> conferidos` |
| 3 | IB ou defeito do backlog alterado no EWM fora da sprint | um `elm_ler_wi` por id do backlog · uma listagem do backlog do EWM (`elm_listar_wi(iteracao = backlog)`) · passo novo no "importar do EWM" · aceitar | **em aberto** — proposta: a listagem do backlog no §9, numa chamada, comparando estado e dono dos ids "do backlog". Título não (decisão 11 da 3.4.1). Prioridade não vai ao EWM (`sdd-fatiar/references/backlog.md`, coluna `prioridade`). A descrição não vem na listagem |
| 4 | `[DEV]` (e tarefa de Sustentação) já fechada quando o trabalho é retomado | ler o estado antes do `assumir` · tratar o `precondicao` do `assumir` · deixar para a sincronização | **em aberto** — proposta: tratar o `precondicao`, sem chamada a mais. Na `sdd-desenvolver`: PR mergeado → Passo 6; senão `elm_transicao(<id>, "reabrir")` com "sim". Na `sdd-atender`/`sdd-executar`: reabrir, ou levar o item a `concluido` como a sincronização faz |
| 5 | Estado de `[REV]`, `[VER]`, `[APR]` e `[DEV]` pela fase do `status.md` | comparar pela fase · só as linhas genéricas (3.4.1) | **em aberto** — proposta: o §9 lê a `fase` (regra A base prevalece) e compara pelo estado esperado da fase (rascunho abaixo), com `manter` quando quem resolve é o papel e `EWM:` quando o EWM está à frente |
| 6 | Fatia com `status.md` numa branch e ainda `planejada` na base | rede de proteção antes do §9 · o §9 trata a fatia como iniciada · como está | **em aberto** — proposta: o passo 2 do §9 olha os `status.md` das branches, como a rede de proteção. Fatia com `status.md` conta como iniciada para "saiu" (o EWM volta, nunca "sai da sprint") e gera a linha `arquivo: iniciada (status.md na branch)`, que grava como a rede de proteção grava. Vale também sob pedido |
| 7 | WI que sumiu do EWM | `manter` (3.4.1) · `arquivo:` o id vira `pendente` e o §3–4 republica · `manter` com pendência registrada | **em aberto** — proposta: a solução continua `manter: confira na UI do EWM`, mas o `manter` dessa linha registra `ELM pendente [<tipo> <id> sumiu]`, que tira o id da comparação até o `ELM feito` (como a decisão 13 da 3.4.1). Em Outras, `arquivo: pendente (republicar)` |
| 8 | MCP `elm` | sem mudança (decisão 17 da 3.4.1) · incluir as melhorias da seção 6 da 3.4.1 | **em aberto** — pela versão única, se mudar, a mcp-elm sobe junto, e o `plugin.json` passa a exigir a nova |
| 9 | Versão | 3.4.2 sozinha | **3.4.2**: `plugin.json`, as 22 skills e o MCP se a decisão 8 o alterar |
| 10 | Migração | — | nenhuma (o power ainda não tem usuários) |

### Desenvolvimento por fora do sdd (decisão 0)

Fontes que a sincronização passa a cruzar: o EWM (como na 3.4.1), o `status.md` (da base e da branch, pela regra A
base prevalece), o `sprint-<nn>.md`, o `backlog.md` e o git — a branch da fatia (`git ls-remote`, `git log`) e o PR
(o mesmo dado que a rede de proteção e a `sdd-status` já leem). Toda solução segue a regra da 3.4.1: aparece na
tabela, e nada é gravado sem o "ok" ou o ajuste da linha.

Casos (rascunho — **propostas**, para confirmar):

| Evidência | Arquivos | EWM | Solução sugerida |
|---|---|---|---|
| PR da fatia mergeado na base | fatia `planejada` ou `iniciada` (qualquer fase antes de `pronta`) | `[DEV]` aberta; `[APR]`, `[REV]`, `[VER]` abertas | **concluir no sdd:** `arquivo: pronta (merge <sha> por fora do sdd)` — grava como o Passo 6 da `sdd-desenvolver` (`status.md` da base com `Fase: pronta`, backlog e sprint `pronta`, Créditos `—`, lições `—`) · `EWM: concluir a [DEV]` · `EWM: cancelar` a `[APR]`, a `[REV]` e a `[VER]` que ainda não estão canceladas · depois, `sdd-consolidar` leva a `concluida` |
| PR da fatia mergeado na base | fatia `pronta` | `[APR]`, `[REV]`, `[VER]` abertas | `EWM: cancelar` as abertas (a `[DEV]` aberta → concluir) |
| PR aberto, sem merge | fatia `planejada` (sem `status.md`) ou `status.md` numa fase anterior | `[DEV]` em andamento | `arquivo: iniciada` (se `planejada`) e `Fase: pr-aberto` (HITL) ou `aguardando-aprovacao-pr` (AFK) no `status.md`, criado se faltar |
| branch com commits, sem PR | fatia `planejada` | `[DEV]` em andamento | `arquivo: iniciada` e `status.md` com `Fase: implementando` (o mesmo caso da lacuna 6) |
| PR fechado sem merge | fatia não terminal | — | `manter: o Dev diz` (retomar ou cancelar pela `sdd-fatiar`) |
| `sprint-<nn>.md` × `backlog.md` | situação, responsável ou sprint diferentes na linha viva e no backlog | — | `arquivo:` a mais adiantada pelas evidências acima; sem evidência, `manter` com as duas versões na linha (as inconsistências da `sdd-status` viram linhas da tabela) |

Pontos para decidir com estes casos:

- **Cancelar no EWM:** o MCP não cancela (`elm_transicao` só assume, conclui e reabre). Sem mudança no MCP, o
  "cancelar" vira `ELM pendente [<tipo> <id> cancelar]` para a pessoa fazer na UI — o que pesa a favor da decisão 8.
- **Quem grava `pronta`:** a 3.4.1 só deixa a `sdd-desenvolver` gravar (`pronta` exige `status.md` na base, créditos
  e lições). A proposta é a sincronização gravar com a evidência do merge, com Créditos e lições `—`.
- **O agente de produto** (onde a sincronização roda) precisa ler o git e o PR — conferir as permissões em
  `sdd-setup/assets/agents/papeis.json`.

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

- **Topo do §9 e passos 1–3** (`:244-307`): o intuito (decisão 0), as fontes novas (git, PR, `sprint-<nn>.md` ×
  `backlog.md`) e os casos da seção Desenvolvimento por fora do sdd.
- **Soluções propostas** (`:372-`): a tabela nova de desenvolvimento por fora; a regra "nas linhas de estado da fatia
  não há `arquivo`" (`:342-343`) passa a ter a exceção da evidência do git.
- **Tabela** (`:319-345`): agrupamento e cabeçalho (decisão 2), atualizando o exemplo.
- **Passo 1 e 2** (`:254-307`): a listagem do backlog e os ids "do backlog" comparados (decisão 3, se aprovada); a
  fatia com `status.md` em branch (decisão 6).
- **Soluções propostas — Fatia** (`:392-406`): as linhas pela fase (decisão 5). A linha `:397` passa a cobrir a
  fatia com `status.md` em branch (decisão 6).
- **Soluções propostas — Iteração** (`:449`): o `sumiu` com a pendência registrada (decisão 7).

### Demais skills

- `sdd-desenvolver/SKILL.md` (`:45`, `:65`, `:149`), `sdd-atender/SKILL.md:50`, `sdd-executar/SKILL.md:40`: o
  `precondicao` do `assumir` (decisão 4). Tirar o item correspondente da seção 6 da 3.4.1.
- `sdd-planejamento/SKILL.md` (pré-condição, `:250-264`): a rede de proteção entra no §9 (decisões 0 e 6).
- `sdd-desenvolver/SKILL.md` (Passo 6) e `sdd-fatiar/references/backlog.md` (Situações, quem grava `pronta`): a
  sincronização como gravador de `pronta` pela evidência do merge (decisão 0).
- `sdd-setup/assets/agents/papeis.json`: o agente de produto lê o git e o PR, se ainda não lê.
- `sdd-status/SKILL.md`: o painel conta as divergências novas que a listagem já mostra. As que exigem `elm_ler_wi`
  ou a fase ficam para a sincronização, como a estimativa na 3.4.1.
- `sdd/references/elm.md`: a chave `[<tipo> <id> sumiu]` na tabela de pendências (decisão 7).
- `README.md` (nota da 3.4.2), `plugin.json` e o `metadata.version` das 22 skills.
- `mcps/elm`, se a decisão 8 o incluir.

## Para a revisão final da 3.4.1

Achados da conferência da 3.4.1 que não são pendências desta versão, mas pesam na revisão dela:

- **Diferenças do que foi pedido no rascunho:**
  - a decisão 3 (a situação da fatia nunca muda pela sincronização) é revista pela decisão 0 desta versão;
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

- Desenvolvimento por fora: fatia `iniciada` em `implementando`, PR mergeado por fora, `[DEV]` em andamento,
  `[APR]`, `[REV]` e `[VER]` abertas → a tabela propõe `pronta` no sdd, concluir a `[DEV]` e cancelar as outras três
  (ou as pendências de cancelamento, sem o MCP); com o "ok", o `status.md` da base fica em `pronta` e a
  `sdd-consolidar` aceita a fatia.
- PR aberto por fora com a fatia `planejada` e sem `status.md` → a tabela propõe `iniciada` e o `status.md` na fase do
  PR.
- `sprint-<nn>.md` e `backlog.md` com situações diferentes → linha na tabela, com a solução pela evidência.
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
