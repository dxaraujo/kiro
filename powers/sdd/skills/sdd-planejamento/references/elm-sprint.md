# Sprint no EWM

Regras comuns (prévia, um "sim", idempotência, pendências): [../../sdd/references/elm.md](../../sdd/references/elm.md).
**O backlog do EWM é a cópia do `backlog.md`:** todo épico, fatia e item de Sustentação registrado tem o seu item no
EWM. Nasce com `iteracao = backlog` (o backlog do produto gravado no `pa`, §0) ou, se já entra numa sprint, com a
iteração dela. **Entrar na sprint** = `elm_atualizar_wi(ids, iteracao = a da sprint)` — move, nunca recria; só se
cria o que está `—` ou `pendente` na coluna `elm`. **Todo trabalho tem pai**: épico → IB → tarefa; o que não vem de
épico fica sob o IB `Sustentação` (§2) — a fatia sob a `Manutenção` (§3), o item sob o IB da categoria (§6). Ordem:
épico, IB, tarefa. Tarefas (`[ESP]`, `[DEV]`, `[REV]`, `[VER]`, `[APR]`, `[GB]` e as da Sustentação, §6) nascem só
na sprint; no backlog só ficam as do item que saiu da sprint sem começar (Encaixe ou §9: fatia, `[ESP]`,
Sustentação), até ele voltar a uma.

**Tarefa que já existe** (o item volta a uma sprint — publicação, Encaixe, puxada, `sdd-especificar` — com tarefas
que ficaram no backlog do EWM): **move, nunca recria**. Cada uma numa chamada própria, com o dono e a estimativa do
papel dela no novo planejamento — `elm_atualizar_wi([id], iteracao, dono, estimativa_h)`: a `[DEV]` com o
responsável, a `[REV]` com o revisor, a `[VER]` com o verificador, a da Sustentação com quem faz —; o IB e o épico
movem só com `iteracao`, na chamada única do §3 (o dono do IB segue o P.O.). **Só nasce o papel que falta**,
conferido com `elm_listar_wi(pai = IB)` — não pelo prefixo do título, que a pessoa pode ter mantido; a tarefa
descartada e a que tem pendência de cancelamento aberta não contam (o papel nasce de novo, e a velha segue com a
pendência). O papel que o novo modo não tem (a fatia HITL que volta AFK, pela senioridade do novo responsável) não
move: vira `ELM pendente [<tipo> <id> cancelar]` onde a fatia guarda as pendências (`elm.md`, Pendências: o
rodapé da ficha; na puxada, que já gravou `iniciada`, o Histórico do `status.md`), e a sincronização não o compara
mais (§9).

## Estrutura no EWM (padrão)

Cada sprint é uma **iteração** com o seu plano; o backlog do produto é uma iteração irmã dos pais das sprints. Tudo
fica dentro de uma **linha de base** — a iteração do projeto na timeline:

```
<linha de base>            (ex.: Evolução do produto — sem datas)
├── Backlog                iteração do backlog do produto, com o plano "Backlog" (tipo product backlog)
├── 2026                   iteração pai (o nome é livre: 2026, Entrega 3…)
│   ├── Sprint 01          iteração da sprint, com datas, e o plano "Sprint 01 - <nome curto da meta>"
│   ├── Sprint 02
│   └── …
└── 2027
    └── Sprint 01
```

Por que cada sprint é uma iteração, e não um plano a mais no pai: no EWM o plano mostra os itens cujo "Planejado
para" é a iteração dele (e o time); dois planos na mesma iteração mostram os mesmos itens. O "Planejado para" é o
que diz em que sprint está cada tarefa, o que migra na virada e o que soma as horas da sprint (`elm_horas`).

A linha de base é o **pai da iteração do backlog** (`ccm.backlog` do `pa`). O caminho que as skills passam ao MCP é
relativo a ela: `2026/Sprint 01` é `<linha de base>/2026/Sprint 01` — uma `2026` de outro lugar da PA não confunde.
Nos arquivos do sdd: `sprints/2026/sprint-01.md`, chave `2026/Sprint 01` (do número do arquivo),
`**Iteração no EWM:** 2026/Sprint 01` (o nome da iteração é livre).

## 0. Backlog do produto (na setup ou em "atualizar a configuração do sdd"; uma vez por projeto)

1. `elm_backlog()` → `atual` (o `ccm.backlog` do `pa`) e `candidatos` (planos de backlog da PA). Já há `atual` →
   mostre e confirme; fim.
2. Pergunte a **linha de base** do projeto (a iteração da timeline onde ficam o backlog e os pais das sprints; quem
   administra a PA cria, se não existir) e se ela **já tem** a iteração `Backlog` com o plano. Mostre os
   `candidatos`.
   - **Já tem** → a pessoa escolhe o candidato ou cola o link do plano (o da UI web, com `id=_…`) →
     `elm_backlog(plano)`. Só serve o plano cuja iteração é filha da linha de base (o `pai` de cada candidato e do
     resultado): noutro lugar, avise que a estrutura padrão não se forma e não siga com ele.
   - **Não tem** → `elm_backlog(nome = "Backlog", pai = <linha de base>)`, com "sim": cria `<linha de base>/Backlog`
     e o plano `Backlog` (iteração `Backlog` que já existe na base → só o plano). Erro `entrada` no campo `plano` (o
     time já tem mais de um plano de backlog nela) → recuse a iteração, como abaixo.
   - **Um produto por iteração de backlog** (os títulos `Sustentação`, `Manutenção` e `<Categoria>` não levam o
     produto): gravado o backlog, `elm_listar_wi(iteracao = backlog, tipo ib, titulo_prefixo "Sustentação")`, e só
     os de título exato `Sustentação` (o prefixo também traz demandas). Uma `Sustentação` que este `backlog.md` não
     conhece (id fora da linha da `## Sustentação`) é de outro produto → recuse a iteração: peça a quem administra a PA uma linha de base só deste produto e refaça o §0 com ela. O `pa`
     já gravou o backlog recusado e fica com ele até o `elm_backlog` ser refeito com o plano certo, pelo passo 2 (o 1
     pararia nesse `atual`); até lá, nada nasce no EWM.
   Erro `permissao` → peça a quem administra a PA.
3. O `pa` passa a ter `ccm.backlog`; daí em diante `iteracao: "backlog"` nas tools é ele, e o pai dele é a linha de
   base. Sem ele, criar no backlog falha com `precondicao` — peça "atualizar a configuração do sdd" (a `sdd-setup`, na
   sessão padrão, roda este §0; os agentes não têm o `elm_backlog`), nunca escolha outra iteração.
4. **Espelhamento** (backlog já existente): linhas do `backlog.md` que não estão concluídas nem canceladas, com `elm`
   `—`, `pendente` ou id sem link (`DF 4567`: registrado sem o MCP, conta como pendente) → prévia numa tabela (item,
   tipo, pai, iteração) e um "sim" → §2, §3 e §6 na ordem; o id sem link não nasce de novo: recebe o que a triagem
   não fez no EWM (pai, dono, prefixo no título, link relacionado) e a `elm` ganha o link. Itens com `elm` que estão
   fora de sprint e numa iteração antiga → `elm_atualizar_wi(ids, iteracao = backlog)`.

## 1. Iteração e plano da sprint

Depois do "ok" da sprint: `elm_iteracao("<pai>/<nome>", inicio = <início da sprint>, fim = <fim>, plano = <o
**Plano no EWM:** do cabeçalho do `sprint-<nn>.md`>)` — o caminho e o plano vêm do cabeçalho (`**Iteração no EWM:**
2026/Sprint 01`, `**Plano no EWM:** Sprint 01 - Exportar o relatório de contas`), também na publicação feita depois e
na virada. Acha ou cria a iteração da sprint dentro do pai, o pai dentro da linha de base (se faltar) e o plano (o
nome só vale ao criar: o plano que já existe não é renomeado), e guarda os ids no `pa` com a chave do caminho (o backlog
não é criado aqui: é o do §0). **O pai:** a sprint nova herda o da anterior; pai novo só quando a pessoa diz, com o
nome que ela der (`2026`, `Entrega 3`…); primeira sprint do projeto → pergunte. Use o caminho em toda tool que recebe
`iteracao`. Criar exige a permissão de modificar iterações — erro `permissao` → peça a quem administra a PA. Erro
`entrada` "ambígua" (duas iterações com o mesmo nome no mesmo pai) → mostre e peça à pessoa que resolva no EWM;
nunca crie outra.

**Sprint não publicada:** o `sprint-<nn>.md` gravado antes deste § — planejamento sem o MCP ou com falha, sessão
parada antes da publicação, ou o da próxima, que nasce no passo 4 da virada (§5) — leva no cabeçalho
`**Publicação no EWM:** pendente`, e este §, ao rodar, o tira no commit da publicação. Enquanto ele está lá, nenhuma
tool recebe a iteração dessa sprint ([elm.md](../../sdd/references/elm.md), Regras de toda escrita): sem este §, o
MCP procura o caminho pelo nome na PA inteira e pode achar a sprint homônima de outro produto (cada produto tem a sua
linha de base, §0); este § a acha dentro da linha de base e guarda o id no `pa`.

## 2. Sustentação e `[GB]` (a Sustentação: uma por produto, com a linha da `## Sustentação` vazia; a `[GB]`: na primeira sprint de cada pai)

IB `Sustentação` (`tipo: ib`; sem o produto no título: um produto por iteração de backlog, §0), com `iteracao =
backlog` — nasce no §0 ou na primeira triagem e **fica no backlog** (não entra em sprint nem move na virada). É a
raiz do que não vem de épico:

```
IB Sustentação                     um por produto; fica no backlog
├── [GB] Gerenciamento do backlog  uma por pai de sprint, na iteração da sprint
├── IB Manutenção                  nasce com a 1ª fatia sem épico (§3); fica no backlog
│   └── IB [FT-034] … (ou o item de origem, DF 4567) → [DEV] FT-034 … · [REV] · [VER] · [APR]
└── IB <Categoria>                 nasce com o 1º item da categoria (§6); fica no backlog
    └── IB [AT-012] <pedido>       nasce na triagem (dono = P.O.); vai à sprint como o IB da fatia
        └── [ATD] AT-012 <pedido>  nasce quando o item entra numa sprint (dono = quem faz)
```

**Categoria** (o campo do IB no EWM, que o `pa` aplica na criação —
[`elm-pa.md`](../../sdd-setup/references/elm-pa.md#modelo-do-sdd-obrigatórios-e-valores-por-item)): o IB do item
(`[AT-012]`…) recebe a da Sustentação, pelo `por-prefixo`; a Manutenção, a que a setup perguntou; os IBs de
categoria (`Atendimento`…), a padrão do tipo.

Idempotência: o id gravado no `backlog.md`; sem ele, `elm_listar_wi(iteracao = backlog, tipo ib, titulo_prefixo
"Sustentação")` e, do resultado, só o de título exato `Sustentação` (o prefixo também traz demandas que começam pela
palavra), aceito só se for o único. A tarefa `[GB] Gerenciamento do backlog` (filha da Sustentação, dono = o
P.O. ativo do `equipe.json`) nasce na primeira sprint de cada iteração pai, com a iteração dela. Ids na primeira
linha da `## Sustentação` do `backlog.md`: `IB [<id>](<url>) · GB [<id>](<url>) · Manutenção IB [<id>](<url>)` (a
Manutenção entra quando nasce, §3; o IB de cada categoria abre a `### <Categoria>` dele, §6). Sustentação já existe
sem a `[GB]` → crie só a `[GB]` (com sprint aberta). **Pai novo** (a sprint nova é `2027/Sprint 01`): nasce a `[GB]`
do pai novo e a antiga conclui com o saldo de horas (`elm_transicao concluir`) e sai da linha; a Sustentação, a
Manutenção e os IBs de categoria não mudam.

## 3. Épico e IB (nascem no registro; movem na sprint)

- **Épico** (na triagem, com "sim"; `iteracao = backlog`): `elm_criar_wi(tipo ib, "[EP-<nn>] <título>", dono = po da linha,
  descricao_md = problema, quem pede, resultado; depois do GATE, a solução e o link do PRD)`. Item de origem do EWM
  (`origem: <id>` na `obs`): já é do tipo épico → é o épico; senão `elm_atualizar_wi(origem, pai = épico novo, iteracao = backlog)`.
  Histórias publicadas → `elm_ligar(wi = épico, req, tipo rastreia)`. Épico `novo` ou `elegivel` fica só ele no
  backlog (com a `[ESP]`, se ela saiu de uma sprint sem começar); quando entra numa sprint (`planejado`, com a
  `[ESP]`, ou com a primeira fatia), move para a iteração dela e a `[ESP]` nasce lá (§4) — ou move, se já existe
  (topo).
- **IB da fatia** (no GATE do backlog da `sdd-fatiar`; fatia sem épico, na triagem; `iteracao = backlog` ou a da
  sprint em que já entra): `elm_criar_wi(tipo ib, "[FT-<nnn>] <título>", pai = épico — sem épico, a Manutenção —,
  dono = P.O., descricao_md = modo, bloqueada por, pasta prevista, campos =
  {<campo de critérios do sdd.md>: os cenários Dado/Quando/Então copiados do PRD ou da ficha, com "gerado do PRD — não
  edite aqui"})`. Defeito: `campos` com a categoria de correção da seção ELM do `sdd.md`. Depois `elm_ligar(wi, req)`
  (implementa) para cada história coberta e `elm_ligar(wi, wi_destino, tipo depende)` para cada `bloqueada-por`
  (sem `links.depende` no `pa` → fica na descrição).
- **Fatia sem épico** (origem `Manutenção`): o pai é o IB `Manutenção`, filho da Sustentação, que nasce com a
  primeira delas, na mesma confirmação (`elm_criar_wi(tipo ib, "Manutenção", pai = Sustentação, iteracao =
  backlog)`; idempotência: `elm_listar_wi(pai = <id da Sustentação>, titulo_prefixo "Manutenção")`), com o id na
  linha da `## Sustentação` do `backlog.md`. Com item de origem (DF, IB), não há IB novo:
  `elm_atualizar_wi(origem, iteracao = backlog)`, com `pai = Manutenção` se ele não tem pai (outro pai: mantém e
  avisa) e `dono = P.O.` se ele não tem dono — o `assumir` da `[DEV]` com `iniciar_pai` exige dono no pai. Fatia
  vinculada a um item de Sustentação (`obs` `vinculada a [AT-012](…)`) → `elm_ligar(wi = item da fatia, wi_destino =
  IB do item, tipo relacionado)`.
- **Fatia dividida:** como a linha do `sdd.md` manda (filhos do IB original, ou fecha o original e cria novos); sem
  épico, sob a Manutenção, direto ou pelo item original; pai errado → `elm_atualizar_wi(id, pai)`.
- Ids na coluna `elm` do `backlog.md`, com o tipo antes de cada id: `IB [612010](…) · DEV [612011](…)`; o item de
  origem, `DF [4567](…)` (sem o MCP, `DF 4567`).
- **Na sprint** (depois do "ok"): épicos, IBs das fatias e IBs dos itens de Sustentação da sprint que já têm `elm` →
  `elm_atualizar_wi(ids, iteracao = a da sprint)` numa chamada, só com a iteração; as tarefas que já existem movem
  cada uma na chamada dela, com o dono e a estimativa do papel (topo); os `—`/`pendente` nascem como acima, já na
  iteração da sprint. Item que sai da sprint sem ter começado (Encaixe ou §9) volta com `iteracao = backlog`, com as
  tarefas abertas.

## 4. Tarefas da sprint (depois do "ok" da sprint)

Item da sprint com id sem link na `elm` (`DF 4567`: registrado sem o MCP) é pendente: antes das tarefas, recebe o
que a triagem não fez no EWM e a `elm` ganha o link, como no espelhamento (§0, passo 4).

Para cada linha do `sprint-<nn>.md`, com a tabela "Tarefas no EWM" de `elm.md`: `elm_criar_wi(tipo tarefa, título,
pai, dono, estimativa_h, iteracao)` — só para o papel que o item não tem; a que já existe move (topo). Fatia
**AFK**: só a `[DEV]`. A `[APR]` não nasce aqui. Item da `## Sustentação`:
o IB dele muda de iteração (sem `elm` → nasce antes) e a tarefa nasce (§6). Ids na coluna "Tarefa ELM"
(`DEV <id> · REV <id> · VER <id>`) e no `elm` do `backlog.md` (`DEV [<id>](<url>)`).

## 5. Virada

**Ordem**, em toda virada: o §9 da sprint que fecha é o da pré-condição dos ritos (antes da migração nos arquivos;
este § não roda outro, que veria os itens já migrados) → a migração nos arquivos (passo 3 da virada) → o
replanejamento da próxima (passo 4: o arquivo dela nasce com `**Publicação no EWM:** pendente`, §1) → o §1 da
próxima, também com o mesmo pai (próxima em outro pai, `2026/Sprint 04` → `2027/Sprint 01`: também o §2, com a
`[GB]` do pai novo) → o **movimento** → o §3–4 e o §6 das linhas novas → o §9 da próxima. Antes do movimento, os itens
migrados ainda estão na iteração que fecha, e o §9 da próxima os veria sair.

**Movimento:** `elm_atualizar_wi(ids, iteracao = a nova)` numa chamada (move, nunca recria; o pai não muda), com os
ids do conjunto "da sprint" (§9, passo 2) que seguem no fluxo e estão **abertos** na listagem da iteração que fecha —
as tarefas e o item das linhas que migram (inclusive os ids que só estão no `status.md`), o IB de todo épico
`planejado` ou `iniciado` (mesmo com a linha da Especificação `concluida`, que não migra) e a `[GB]`, se o pai não
muda; a Sustentação, a Manutenção, os IBs de categoria e o que está no backlog ficam onde estão. O que está fechado
fica na iteração em que fechou: as horas dele são desta sprint (`elm_horas` soma pela iteração da tarefa). Leva
também os ids abertos de linha migrada que ainda estão numa sprint anterior da cadeia `migrada de` (virada pela
metade, abaixo) — não todo id aberto fora da listagem, que desfaria uma saída que espera o P.O. Listagem com `total` =
1000 → avise e pare (§9, passo 1). Baseline por sprint, se o `sdd.md` exigir → roteiro manual.

**Virada pela metade** (sem o MCP, falha no movimento ou sessão parada depois do passo 4): os arquivos seguem; diga
que o movimento fica para a sincronização da próxima, que o reconhece (§9: a sprint não publicada, a linha `migrada
de` ainda na iteração de origem, a linha nova sem ids).

Relatório: `elm_horas(iteracao)` → horas por prefixo e por pessoa, planejadas × lançadas, e as tarefas concluídas
sem horas.

## 6. Sustentação (chamado pela `sdd-triar`, pelo encaixe ou aqui)

Item sem mudança no repositório, de uma categoria da tabela **Sustentação** do `sdd.md` (a Manutenção é o §3).

**IB da categoria**, um por categoria: a `## Sustentação` do `backlog.md` sem a `### <Categoria>` → é o primeiro
item dela: crie, na mesma confirmação do IB do item, `elm_criar_wi(tipo ib, "<Categoria>", pai = Sustentação,
iteracao = backlog)` (§2 antes, se a Sustentação faltar; idempotência: `elm_listar_wi(pai = <id da Sustentação>,
titulo_prefixo "<Categoria>")`); o id abre a `### <Categoria>` (`IB [<id>](<url>)`). Fica no backlog, como a
Sustentação; a Categoria dele é a padrão do tipo no `pa` (§2).

**IB do item** (na triagem; `iteracao = backlog` ou a da sprint em que já entra): `elm_criar_wi(tipo ib,
"[AT-012] <pedido>", pai = o IB da categoria, dono = o P.O.)` — série do id pela categoria; idempotência:
`elm_listar_wi(pai = <IB da categoria>, titulo_prefixo "[AT-012]")`. Item triado a partir de um IB ou DF do EWM: ele
é o IB do item (sem IB novo, como na fatia), sob o IB da categoria se não tiver pai (outro pai: mantém e avisa), e o
título ganha o `[AT-012]` pelas opções do §9 (renomear · só incluir o prefixo · manter). Entra na sprint e muda de
iteração na virada como o IB da fatia (§3, §5).

**Tarefa** (só quando o item entra numa sprint — triagem com sprint aberta e reserva, planejamento, Encaixe ou §9):
`elm_criar_wi(tipo tarefa, "[ATD] AT-012 <pedido>", pai = o IB do item, dono = quem faz, estimativa_h, iteracao = a
da sprint)` — prefixo pela categoria (`[ATD] AT-012 …`, `[IMPL] IM-003 …`); o `pa` aplica a Classificação da Tarefa
pelo prefixo. Fica no estado inicial. Ids: `IB [<id>](<url>) · ATD [<id>](<url>)` na coluna `elm` do `backlog.md`,
`ATD <id>` na "Tarefa ELM" da sprint. A que já existe (o item saiu de uma sprint sem começar) move em vez de nascer
(topo). Concluir o item é concluir a tarefa **e** o IB dele, na mesma confirmação (`sdd-atender`, `sdd-executar`).

## 7. Troca AFK → HITL (só pela seção "Troca de modo")

Cria a `[REV]` e a `[VER]` como no §4 (mesmo pai da `[DEV]`), com o revisor e o verificador da decisão — só o papel
que falta: a que já existe move, e a que tem pendência de cancelamento não conta (topo). A `[DEV]` não muda. HITL →
AFK não existe.

## 8. `[APR]` no gate (chamada pela `sdd-plano`, `sdd-implementar` Passo 5 ou `sdd-loop`)

`elm_listar_wi(pai = IB, titulo_prefixo "[APR] FT-<nnn> Aprovar <plano|PR>")` → já existe: é ela (volta a ser
aprovada depois de ajustes). Senão `elm_criar_wi(tipo tarefa, "[APR] FT-<nnn> Aprovar <plano|PR>", pai = IB, dono = o
Dev Sênior escolhido, estimativa_h perguntada, iteracao da fatia)`. Fica no estado inicial; o id vai para o campo ELM
do `status.md`.

## 9. Sincronizar a sprint com o EWM ("sincroniza a sprint")

Compara a sprint com a iteração dela no EWM nos dois sentidos: o que nasceu **por fora** — tarefa criada direto no
EWM, à mão, por outra pessoa, ou porque a sessão do agente parou (ex.: limite de tokens) e alguém abriu a `[DEV]` ou
a `[ESP]` por fora; entra com o **mesmo id**, nunca recriada — e **o que mudou no EWM nos itens que os arquivos já
conhecem**: estado, iteração, dono e estimativa. Roda depois de publicar a sprint (§4; na virada, a da próxima só
depois do movimento, §5), na pré-condição dos ritos de fechamento e sob pedido ("sincroniza a sprint", "sincronizar
com o EWM"). Sem o MCP `elm` → "sincronização com o EWM não feita" (sob pedido, pare). Nunca diga que "não é preciso
sincronizar" sem ter rodado a comparação: o resultado é sempre a tabela do passo 4 ou a linha do passo 6.

1. **Listar.** Cabeçalho com `**Publicação no EWM:** pendente` (§1) → **não liste ainda**: a tabela abre com a linha
   `EWM: criar a iteração e o plano (§1; com pai novo, também o §2)`, e a listagem vem depois do "ok". Senão,
   `elm_listar_wi(iteracao = "<pai>/<nome>" da sprint, limite 200)`, **sem `tipo`** (tarefas, IBs, defeitos e
   épicos); erro `nao_encontrado` ou `entrada` ("ambígua") → como o marcador. `truncado` → de novo com `limite 1000`;
   `total` = 1000 (o teto da consulta no MCP) → avise e pare: a listagem pode estar incompleta, e a linha "iguais"
   mentiria.
2. **Onde cada id deveria estar**, pelos arquivos. Cada item entra com **todos** os ids dele — o IB ou a origem e as
   tarefas: a coluna `elm` do `backlog.md`, a "Tarefa ELM" da linha e, na fatia `iniciada` ou `pronta`, o campo ELM do
   `status.md`, lido pela regra A base prevalece (o de `origin/<base>` quando existe, senão o da branch, `git show
   origin/<branch>:…`).
   - **da sprint** (esperado na iteração dela): os itens das linhas do `sprint-<nn>.md` aberto, menos as que têm
     `saiu da sprint`; a `[GB]` do pai; e o IB de cada épico `planejado` ou `iniciado` (ele acompanha as sprints até
     concluir, §5);
   - **do backlog** (esperado no backlog do EWM): os IBs `Sustentação`, `Manutenção` e de categoria e os itens não
     terminais fora da sprint (`sprint` `—`), com as tarefas que ficaram no backlog (topo);
   - **terminal de fora**: o item terminal cuja `sprint` não é esta — esperado na `**Iteração no EWM:**` daquela sprint
     (`—`: o backlog); uma iteração que cobre duas sprints não gera linha. O IB do épico terminal fica fora da
     conferência de iteração (o `backlog.md` não diz em que sprint ele concluiu), mas o estado dele é comparado;
   - **por fora**: o id da listagem que nenhum arquivo cita, de `tipo` do `pa` (`ib`, `tarefa`, `defeito`); o de outro
     tipo (impedimento, retrospectiva…) fica fora, só contado nos conferidos. O id citado é comparado qualquer que seja
     o tipo.

   Ficam **fora da comparação**:
   - a **publicação pendente** — a linha com Tarefa ELM `pendente` (ou sem id nenhum, numa linha não iniciada: a
     sessão parou entre gravar o arquivo e publicar), ou cujo item tem `elm` `pendente` ou id sem link, e sem os ids
     no `status.md` —, que vira a linha `EWM: publicar (§1–4)`, nunca "sai da sprint"; a puxada `iniciada` tem Tarefa
     ELM `—` de propósito: os ids dela estão no `status.md`;
   - a **pendência registrada** — `ELM pendente [<chave>]` sem `ELM feito`, coletada como na `sdd-status` (Coleta,
     itens 2 e 4) e no Histórico do `status.md` da base das fatias `concluida` —, que já cobre a diferença;
   - de vez, o id com pendência de **cancelamento** (`[<tipo> <id> cancelar]` ou a do item), aberta ou já com
     `ELM feito`: cancelar foi decisão registrada.
3. **Comparar** — "entrou" e "saiu" só quando a iteração real não é a esperada:
   - da sprint, na listagem → estado e dono ([Soluções propostas](#soluções-propostas));
   - da sprint, fora da listagem → `elm_ler_wi(id, comentarios 0)`: **aberto** noutra iteração → saiu — salvo na linha
     com `migrada de <chave>` cujo id aberto está na iteração de uma sprint da cadeia (`<chave>`, a de onde ela migrou
     antes, e assim por diante, pelos `migrada de` dos arquivos fechados): a virada não moveu, e a linha é `EWM: mover
     para esta sprint`; **fechado** → fica onde fechou (sem divergência de iteração; o estado é comparado);
     `nao_encontrado` → sumiu;
   - tarefa aberta da Especificação e da Sustentação → `elm_ler_wi(id, comentarios 0)` para a estimativa (a que já foi
     lida não é lida de novo); as fatias não guardam horas no arquivo;
   - IB de épico citado no `backlog.md` e na listagem → o estado, qualquer que seja a situação do épico;
   - do backlog ou terminal de fora, na listagem → **entrou**: uma linha por item, com o IB e as tarefas dele que
     estão na listagem (as citadas e as por fora cujo pai é ele);
   - por fora → [Por fora](#por-fora).

   **Estados do EWM**, pelo nome, com as palavras que o MCP usa:

   | Grupo | Nomes |
   |---|---|
   | nova | o estado inicial da PA (Novo…) |
   | em andamento | andamento, progresso, desenvolvimento, execução, implementação, trabalho, teste, revisão, verificação |
   | concluída | concluído, resolvido, fechado, finalizado, pronto, done, completo |
   | descartada | cancelado, inválido ou invalidado, rejeitado, duplicado, descartado |

   Nome fora da tabela → `?` na linha, e a pessoa diz o grupo.
4. **Tabela** — uma só, com todas as divergências e as por fora, e a solução proposta em cada linha:
   ```
   🔄 2026/Sprint 03 × EWM — 9 divergências · 41 itens conferidos
   | # | Item | No EWM | Campo | Arquivo | EWM | Solução proposta |
   | 1 | AT-012 | ATD 670301 | estado | em-andamento | Concluído | arquivo: concluido, concluida-em 2026-10-28 (concluído no EWM) · EWM: concluir o IB 669379 |
   | 2 | IM-003 | IMPL 670215 | dono | ana.souza | rita.melo | arquivo: responsável rita.melo |
   | 3 | IM-003 | IMPL 670215 | estimativa | 4 h | 6 h | arquivo: Horas 6 |
   | 4 | FT-036 | IB 670188 | iteração | 2026/Sprint 03 | Backlog | arquivo: sai da sprint — elegivel, sprint — (P.O.) · EWM: DEV, REV e VER de FT-036 → backlog |
   | 5 | FT-031 | DEV 669401 | iteração | 2026/Sprint 03 | Sprint 04 | EWM: volta para 2026/Sprint 03 (fatia iniciada) |
   | 6 | FT-033 | DEV 669410 | estado | iniciada | Concluído | manter: o Dev confere — PR mergeado → sdd-desenvolver Passo 6; senão, reabrir |
   | 7 | EP-05 | ESP 669377 | estado | iniciada | Concluído | EWM: reabrir a [ESP] (fecha no GATE do backlog) |
   | 8 | FT-040 | IB 670400 · DEV 670401 | iteração | backlog (elegivel) | 2026/Sprint 03 | encaixe (P.O.; a DEV 670401 é a da fatia) — recusado: volta ao backlog |
   | 9 | — | 670210 | por fora | — | "ajustar job de carga" · joao.lima · Em Andamento | [DEV] de FT-034 → Tarefa ELM dela · título "[DEV] FT-034 ajustar job de carga" |
   "ok" aplica tudo como proposto · ou ajuste uma ou mais linhas: "4: EWM", "6: EWM", "2: manter", "9: só incluir o prefixo"
   ```
   - **No EWM**: o tipo e o id (o item que entrou leva os ids dele na mesma linha); **Campo**: `estado` · `dono` ·
     `estimativa` · `iteração` · `sumiu` · `por fora` · `publicação` (a linha que cria a iteração da sprint não
     publicada vem primeiro).
   - A solução diz onde grava: `arquivo:` (o arquivo recebe o EWM) · `EWM:` (o EWM recebe o arquivo) · `manter:`
     (nada é gravado; diz quem resolve) · `encaixe` ou `triar` (encaminha). Linha com as duas partes grava as duas;
     toda escrita no EWM aparece na linha.
   - **Ajuste por linha:** `<n>: arquivo` · `<n>: EWM` · `<n>: manter` (a linha volta na próxima sincronização); na
     por fora, o tipo e o título (`9: [EXT]`, `9: só incluir o prefixo`, `9: manter o título` — traz sem renomear; o
     `manter` sozinho não a traz). Nas linhas de estado da fatia e do épico não há `arquivo`: a situação deles só muda
     pela skill que a causa.
   - As linhas que mudam o escopo (sai da sprint, encaixe) esperam o "sim" do **P.O.**; sem ele, ficam `manter` nesta
     rodada.
5. **Gravar** com o "ok", ou depois dos ajustes:
   - **EWM** primeiro (é a prévia de [`elm.md`](../../sdd/references/elm.md), Regras de toda escrita):
     `elm_atualizar_wi` — iteração (o item que entra ou sai leva o IB e as tarefas abertas junto; a que já existe move
     com o dono e a estimativa do papel, topo), dono, estimativa e, na por fora, título e pai; `elm_transicao` pelo
     que a linha diz — concluir (o IB da fatia, do épico ou do item de Sustentação; a tarefa reaberta, no "concluir de
     novo", com as horas já lançadas) ou reabrir (tarefa, IB, `[ESP]`, `[GB]`); a sprint não publicada e a publicação
     pendente pelo §1–4. **Falha:** sem pendência quando a próxima sincronização vê a mesma diferença de novo —
     estado, dono, estimativa ou iteração de item não terminal da sprint, que fica nela ou migra —, porque a pendência
     a esconderia; com `ELM pendente [<chave>]` no lugar do artefato (`elm.md`, Pendências) quando não veria: a
     conclusão do IB ou da tarefa de item terminal (Sustentação no `**ELM:**` da ficha, épico no rodapé do PRD, fatia
     `concluida` no Histórico do `status.md` da base) e a falha na pré-condição da virada em item que não migra. A
     linha que muda o escopo cujo movimento falhou **não grava o lado do arquivo** e volta como estava (só os ids que
     ela já criou são gravados de volta). A por fora cujo título ou pai falhou entra nos arquivos só se a linha já
     criou ids (o IB do item novo), com a falha em `ELM pendente` no `**ELM:**` da ficha; sem id criado, fica fora e
     volta como por fora;
   - **arquivos** — `backlog.md`, `sprint-<nn>.md` e as fichas de `sustentacao/**` (e, para uma pendência, o rodapé
     do `prd.md` e o `status.md` da base da fatia `concluida`) — pelo bloco
     [Gravar na base](../../sdd-fatiar/references/backlog.md#gravar-na-base), num commit `<pai>/Sprint <nn>:
     sincronizar com o EWM`, com as horas na `[GB]`. As horas das tarefas trazidas já entram no relatório da virada
     (§5): `elm_horas(iteracao)` lista toda tarefa da iteração;
   - as linhas `encaixe` seguem depois, uma a uma, para o Encaixe ([Durante a sprint](../SKILL.md#durante-a-sprint)).
6. **Nada diverge** → `🔄 <chave> × EWM: iguais — <n> itens conferidos` (os da listagem mais os da sprint que não
   estão nela).

### Soluções propostas

A solução proposta vem primeiro; "outras" são os ajustes que a linha aceita, além de `manter`.

**Sustentação sem mudança no repositório** (a tarefa `[ATD]`, `[IMPL]`… e o IB do item) — o ciclo dela vive no EWM:

| Arquivo | EWM | Solução proposta | Outras |
|---|---|---|---|
| `aberto` | tarefa em andamento | arquivo: `em-andamento` (backlog, sprint e `**Situação:**` da ficha) | — |
| `aberto` · `em-andamento` | tarefa concluída | arquivo: `concluido`, `concluida-em` = a data da sincronização, Observação `concluído no EWM`, `**Situação:** concluido` na ficha (Créditos `—`: ninguém fechou a sessão, e a virada aponta) · EWM: concluir o IB do item, se aberto | EWM: reabrir a tarefa |
| não terminal | tarefa descartada | arquivo: `cancelado`, Observação `cancelado no EWM`, ficha · IB aberto → `ELM pendente [<ID> cancelar]` no `**ELM:**` da ficha | EWM: reabrir a tarefa |
| `em-andamento` | tarefa nova | manter: quem faz assume na próxima sessão (`sdd-atender`, `sdd-executar`) | — |
| `concluido` · `cancelado` | tarefa aberta (reaberta) | manter: situação terminal não volta, e trabalho novo é item novo (`sdd-triar`) | EWM: concluir de novo, com as horas já lançadas |
| `concluido` | IB do item aberto | EWM: concluir o IB | — |
| — | tarefa com outro dono | arquivo: `responsavel` (backlog), Responsável (sprint) e `**Responsável:**` (ficha) | EWM: o dono volta |
| — | tarefa sem dono | EWM: dono = o responsável do arquivo | — |
| tarefa aberta | outra estimativa | arquivo: Horas (sprint) e `**Estimativa:**` (ficha) | EWM: a estimativa volta |

**Fatia** (as tarefas de papel e o IB ou a origem) — a situação só muda pela skill do papel:

| Arquivo | EWM | Solução proposta | Outras |
|---|---|---|---|
| `planejada` · `iniciada` | `[DEV]` concluída | manter: o Dev confere — PR mergeado → `sdd-desenvolver` Passo 6; senão, reabrir | EWM: reabrir a `[DEV]` |
| `planejada`, sem `status.md` em branch | `[DEV]` em andamento | manter: a fatia começa pela `sdd-desenvolver` (com `status.md` numa branch, quem corrige é a rede de proteção da [pré-condição](../SKILL.md#pré-condição-dos-ritos-de-fechamento)) | — |
| não terminal | tarefa ou IB descartado | manter: dividir ou cancelar é da `sdd-fatiar` (P.O.) | EWM: reabrir |
| antes de `concluida` | IB concluído | EWM: reabrir o IB (ele fecha na `sdd-consolidar`) | — |
| `concluida` | IB aberto | EWM: concluir o IB | — |
| `pronta` · `concluida` | tarefa aberta | manter: a tarefa é de `<dono>`, que a conclui na sessão dele | — |
| `planejada` | `[DEV]` com outro dono | arquivo: responsável = o novo, quando a regra do dono (abaixo) deixa; senão, EWM: o dono volta | EWM: o dono volta |
| `iniciada` em diante | `[DEV]` com outro dono | arquivo: `responsavel` e Responsável = o dono, quando a regra do dono deixa (quem retomou a fatia); senão, EWM: a `[DEV]` volta para o Responsável da linha viva (e o backlog acompanha) | EWM: a `[DEV]` volta para o Responsável da linha viva |
| `iniciada` em diante | dono da `[DEV]` = Responsável da linha viva ≠ `responsavel` do backlog | arquivo: `responsavel` = o dono, só no backlog | — |
| HITL | `[REV]` com outro dono | arquivo: Revisor = o novo, se é Dev Sênior ativo e não implementa (ou é o `revisor único`); senão, EWM: o dono volta | EWM: o dono volta |
| HITL | `[VER]` com outro dono | arquivo: Verificador = o novo, se não implementa; senão, EWM: o dono volta | EWM: o dono volta |

**Regra do dono da `[DEV]`.** Fatia `planejada`: o arquivo recebe o novo responsável só se ele é Dev ativo, não é o
Verificador da linha nem o Revisor (salvo `revisor único`) e o modo não muda pela
[senioridade](../SKILL.md#modo-pela-senioridade) dele — Júnior só em fatia HITL; Sênior em fatia AFK, ou HITL com o
motivo já na `obs`; Pleno quando os critérios da `sdd-fatiar` dão o modo atual, com a confirmação do P.O. na linha;
fora disso, o dono volta (trocar o responsável com troca de modo é do P.O.). Fatia `iniciada` em diante: o dono da
`[DEV]` é **quem implementa** — só o dono lança horas, e outro Dev pode retomar a fatia (trocar o responsável é do
planejamento, e esta sincronização é dele). A referência é o Responsável da **linha viva** da sprint (a sem `saiu da
sprint`): o arquivo recebe o dono (esse Responsável e o `responsavel` do backlog, que depois de uma puxada podem
diferir) se ele é Dev ativo, não é o Verificador nem o Revisor da linha (salvo `revisor único`) e não é Júnior numa
fatia AFK (aí é a [Troca de modo](../SKILL.md#troca-de-modo-afk--hitl), com o P.O.); senão, a `[DEV]` volta para o
Responsável da linha viva, e o `responsavel` do backlog passa a ser o mesmo. Dono igual ao Responsável da linha viva e
diferente do `responsavel` do backlog (a puxada de quem não era o responsável) → `arquivo: responsavel = <dono>`, só
no backlog: o valor velho bloquearia a pessoa como verificadora ou revisora. O Responsável do `status.md` não serve de
referência: no GATE do plano ele é o aprovador. Tarefa sem dono no EWM → recebe o do arquivo.

**Especificação** (a `[ESP]` e o IB do épico):

| Arquivo | EWM | Solução proposta | Outras |
|---|---|---|---|
| `planejada` · `iniciada` | `[ESP]` concluída | EWM: reabrir a `[ESP]` (ela fecha no GATE do backlog, `sdd-especificar` Passo 6) | — |
| `planejada` | `[ESP]` em andamento | manter: a especificação começa pela `sdd-especificar` (o Passo 2 grava `iniciada`) | — |
| não terminal | `[ESP]` descartada | manter: cancelar o épico é da `sdd-fatiar` | EWM: reabrir |
| épico `planejado` · `iniciado` | IB do épico concluído | EWM: reabrir o IB | — |
| épico `concluido` | IB do épico aberto | EWM: concluir o IB | — |
| — | `[ESP]` com outro dono | arquivo: Responsável (sprint) | EWM: o dono volta |
| `[ESP]` aberta | outra estimativa | arquivo: Horas previstas | EWM: a estimativa volta |

**`[GB]`:** concluída fora da troca de pai → `EWM: reabrir`.

**Iteração** (qualquer item):

| Caso | Solução proposta | Outras |
|---|---|---|
| sprint não publicada (passo 1) | EWM: criar a iteração e o plano (§1; com pai novo, também o §2), e só então listar | — |
| publicação pendente (passo 2) | EWM: publicar a linha (§1–4) | — |
| migrada (`migrada de <chave>`), aberta ainda na iteração de uma sprint da cadeia | EWM: mover para esta sprint (a virada não moveu, §5) | — |
| saiu (aberto), item não iniciado | arquivo: sai da sprint (P.O.) — fatia `elegivel` (ou `nova`, pela DoR), épico `elegivel`, Sustentação `aberto`, com `sprint` `—`; a linha da sprint fica com a mesma situação e `saiu da sprint: movida no EWM para <iteração> (<P.O.>, <data>)` · EWM: o IB e as tarefas abertas que não estão no backlog (onde estiverem, outra sprint inclusive) → backlog | EWM: o que saiu volta para a sprint |
| saiu (aberto), item iniciado | EWM: volta para a iteração da sprint (de `iniciada` em diante nada volta) | — |
| só uma tarefa aberta saiu (na Especificação, também só o IB do épico), com o item na sprint | EWM: volta | — |
| fechado e fora da listagem | não é divergência: fica onde fechou | — |
| sumiu (`nao_encontrado`) | manter: confira na UI do EWM | — |
| entrou: fatia `elegivel` fora da sprint (o IB, tarefas dela, ou os dois) | encaixe (P.O., Encaixe da `sdd-planejamento`; a tarefa que já existe é a do papel, e o IB e as tarefas que faltam vêm para a sprint) — recusado, EWM: tudo volta ao backlog | EWM: volta ao backlog |
| entrou: fatia `nova` | a DoR primeiro, como na Previsão: passa → `elegivel` e encaixe, como acima; não passa → EWM: volta ao backlog, com o `falta:` na `obs` | — |
| entrou: épico `novo` ou `elegivel`, com a `[ESP]` | arquivo: Especificação `planejada` e épico `planejado`, com `encaixe: trazida do EWM (<P.O.>, <data>)`; Responsável e Horas previstas pelo dono e pela estimativa da `[ESP]` · EWM: o IB do épico → sprint (o `novo` passa antes pela DoR do épico) | EWM: volta ao backlog |
| entrou: épico `novo` ou `elegivel`, só o IB | EWM: volta ao backlog (a especificação entra pelo planejamento, que dá o responsável e as horas) | — |
| entrou: item de Sustentação `aberto` (o IB, a tarefa, ou os dois) | arquivo: entra na sprint, com a situação pelo estado da tarefa (Novo → `aberto`, Em Andamento → `em-andamento`, concluída → `concluido`) e `trazida do EWM`; a tarefa que já existe é a dele, e só sem ela a tarefa nasce (§6), com o `responsavel` e a `**Estimativa:**` da ficha, ou os que a pessoa der na linha · EWM: o IB e a tarefa → sprint, e, com a tarefa concluída, concluir o IB (reserva estourada → o item fica, e o P.O. decide pelo Encaixe se uma fatia sai) | EWM: volta ao backlog |
| entrou: item terminal | EWM: volta para a iteração esperada | — |
| entrou: IB de estrutura (`Sustentação`, `Manutenção`, categoria) | EWM: volta ao backlog | — |

### Por fora

Tarefa (ou IB, defeito) da listagem que nenhum arquivo cita. **Inferir** com `elm_ler_wi(id)` (`pai`, `campos`,
descrição), nesta ordem de pistas:
- prefixo do sdd já no título (`[DEV]`, `[ESP]`, `[IMPL]`…) → é ele;
- pai no EWM: IB `[FT-nnn]` (ou o item de origem da fatia) → tarefa de papel da fatia (`[DEV]`, `[REV]`, `[VER]`,
  `[APR]`); épico `[EP-nn]` → `[ESP]` do épico; IB de item (`[AT-012]`, `[IM-003]`…) → a tarefa dele; IB de
  categoria → item novo dela; `Sustentação` ou sem pai → item novo de Sustentação;
- Classificação da Tarefa: Desenvolvimento → `[DEV]` (ou `[REV]`, se o dono é o revisor da fatia); Testes →
  `[VER]`; Análise / Especificação → `[ESP]`; a de uma categoria da tabela **Sustentação** do `sdd.md` → ela;
- título e descrição (chamado → Atendimento; versão, deploy → Implantação; script, carga → Banco de dados…).

Fatia ou épico sem pista → `?` na linha, para a pessoa dizer. A tarefa cujo pai é um item que entrou vai na linha
dele (passo 3). Título: renomear (padrão do sdd) · só incluir o prefixo · manter o título. Soluções:

- **tarefa de papel** de fatia ou épico com linha na sprint → o id entra na "Tarefa ELM" da linha (`DEV 669401 ·
  DEV 670210`), com a Observação `trazida do EWM`; fatia `iniciada` → o `backlog.md` não muda (a `sdd-consolidar`
  leva os ids); avise o Dev para registrar o id no `status.md`. Fatia fora da sprint → `encaixe` (a `nova` passa antes
  pela DoR; a tarefa é a do papel inferido). `[ESP]` de épico fora da sprint → a linha da Especificação nasce
  `planejada` (o épico `novo` ou `elegivel` fica `planejado` — o `novo` depois da DoR do épico —; o `iniciado` não muda
  e a linha nasce `iniciada`), com `encaixe: trazida do EWM (<quem>, <data>)`, Responsável e Horas previstas pelo dono
  e pela estimativa dela, e o IB do épico vem para a sprint; o P.O. confirma. Fatia ou épico fora do `backlog.md` →
  `triar` (`sdd-triar`, "importar do EWM") para o IB;
- **Sustentação** → tarefa de um item (pai IB `[AT-012]`) → o id vai para o `elm` dele e para a "Tarefa ELM" da linha
  dele na sprint; sem linha, o item entra na sprint como em "entrou: item de Sustentação" (acima), com o IB movido
  junto. Senão, a linha da `### <Categoria>` do `backlog.md` com `elm` `pendente` que seja o mesmo pedido (triado sem o
  MCP e aberto à mão no EWM) → proponha ligar (sem id nem ficha novos). Nenhuma → a tarefa **vira item**: registre pelas
  regras da Sustentação da [`sdd-triar`](../../sdd-triar/SKILL.md#passo-3--registrar-na-base) (categoria confirmada,
  próximo id da série, duplicado pelo `**Origem:**` das fichas de `sustentacao/**`), com `origem` `EWM <id>`, `sprint`
  = a desta, `responsavel` = o dono no EWM e o `status` pelo estado (Novo → `aberto`, Em Andamento → `em-andamento`,
  concluída → `concluido` com `concluida-em`); a ficha leva o título e a descrição do EWM (sem dado de cliente),
  `**Estimativa:**` a da tarefa (ou `—`) e `falta: prazo, critério de pronto` no que o EWM não traz. Ligado ou novo, o
  item sem IB ganha o IB `[XX-nnn] <pedido>` (§6; a `### <Categoria>` nasce se for a primeira) e a tarefa passa a
  filha dele — com a tarefa concluída, o IB conclui na mesma linha; linha na `## Sustentação` do `sprint-<nn>.md` com
  `trazida do EWM`. Reserva estourada → o item fica na sprint e o P.O. decide pelo Encaixe
  ([Durante a sprint](../SKILL.md#durante-a-sprint));
- **IB ou defeito** fora do `backlog.md` → `triar` (`sdd-triar`, "importar do EWM"); outra: `EWM: volta ao backlog`;
- **EWM:** `elm_atualizar_wi(id, titulo)` pela escolha da linha; sem pai → `pai` = o IB da fatia ou o épico; na
  Sustentação, o IB do item (também quando o pai era a `Sustentação` ou o IB da categoria) — todo trabalho tem pai.
  Outro pai, dono e horas não mudam.
