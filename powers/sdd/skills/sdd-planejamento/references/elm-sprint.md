# Sprint no EWM

Regras comuns (prévia, um "sim", idempotência, pendências): [../../sdd/references/elm.md](../../sdd/references/elm.md).
**O backlog do EWM é a cópia do `backlog.md`:** todo épico, fatia e item de Sustentação registrado tem o seu item no
EWM. Nasce com `iteracao = backlog` (o backlog do produto gravado no `pa`, §0) ou, se já entra numa sprint, com a
iteração dela. **Entrar na sprint** = `elm_atualizar_wi(ids, iteracao = a da sprint)` — move, nunca recria; só se
cria o que está `—` ou `pendente` na coluna `elm`. **Todo trabalho tem pai**: épico → IB → tarefa; o que não vem de
épico fica sob o IB `Sustentação` (§2) — a fatia sob a `Manutenção` (§3), o item sob o IB da categoria (§6). Ordem:
épico, IB, tarefa. Tarefas (`[ESP]`, `[DEV]`, `[REV]`, `[VER]`, `[APR]`, `[GB]` e as da Sustentação, §6) nascem só
na sprint; no backlog só ficam as da fatia que saiu da sprint sem começar (Encaixe).

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
  backlog; quando entra numa sprint (`planejado`, com a `[ESP]`, ou com a primeira fatia), move para a iteração dela
  e a `[ESP]` nasce lá (§4).
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
  `elm_atualizar_wi(ids, iteracao = a da sprint)` numa chamada; os `—`/`pendente` nascem como acima, já na iteração da
  sprint. Item que sai da sprint sem ter começado volta com `iteracao = backlog`.

## 4. Tarefas da sprint (depois do "ok" da sprint)

Item da sprint com id sem link na `elm` (`DF 4567`: registrado sem o MCP) é pendente: antes das tarefas, recebe o
que a triagem não fez no EWM e a `elm` ganha o link, como no espelhamento (§0, passo 4).

Para cada linha do `sprint-<nn>.md`, com a tabela "Tarefas no EWM" de `elm.md`: `elm_criar_wi(tipo tarefa, título,
pai, dono, estimativa_h, iteracao)`. Fatia **AFK**: só a `[DEV]`. A `[APR]` não nasce aqui. Item da `## Sustentação`:
o IB dele muda de iteração (sem `elm` → nasce antes) e a tarefa nasce (§6). Ids na coluna "Tarefa ELM"
(`DEV <id> · REV <id> · VER <id>`) e no `elm` do `backlog.md` (`DEV [<id>](<url>)`).

## 5. Virada

Antes de tudo, §9 (o que nasceu por fora entra nos Números). Próxima sprint em outro pai (`2026/Sprint 04` →
`2027/Sprint 01`) → §1 com o pai novo e §2 (`[GB]` do pai novo) antes de mover. Tarefas, IBs (das fatias e dos
itens de Sustentação) e épicos não concluídos da sprint (inclusive a `[GB]`, se o pai não muda; a Sustentação, a
Manutenção, os IBs de categoria e o que está no backlog ficam onde estão) → `elm_atualizar_wi(ids, iteracao = a
nova)` numa chamada (move, nunca recria; o pai não muda). Baseline por sprint, se o `sdd.md` exigir → roteiro manual.
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
`ATD <id>` na "Tarefa ELM" da sprint. Concluir o item é concluir a tarefa **e** o IB dele, na mesma confirmação
(`sdd-atender`, `sdd-executar`).

## 7. Troca AFK → HITL (só pela seção "Troca de modo")

Cria a `[REV]` e a `[VER]` como no §4 (mesmo pai da `[DEV]`), com o revisor e o verificador da decisão. A `[DEV]` não
muda. HITL → AFK não existe.

## 8. `[APR]` no gate (chamada pela `sdd-plano`, `sdd-implementar` Passo 5 ou `sdd-loop`)

`elm_listar_wi(pai = IB, titulo_prefixo "[APR] FT-<nnn> Aprovar <plano|PR>")` → já existe: é ela (volta a ser
aprovada depois de ajustes). Senão `elm_criar_wi(tipo tarefa, "[APR] FT-<nnn> Aprovar <plano|PR>", pai = IB, dono = o
Dev Sênior escolhido, estimativa_h perguntada, iteracao da fatia)`. Fica no estado inicial; o id vai para o campo ELM
do `status.md`.

## 9. Trazer o EWM para a sprint ("sincroniza a sprint")

Tarefa criada direto no EWM na iteração da sprint — à mão, por outra pessoa, ou porque a sessão do agente parou (ex.:
limite de tokens) e alguém abriu a `[DEV]` ou a `[ESP]` por fora — entra na sprint com o **mesmo id** (nunca recria).
Roda depois de publicar a sprint (§4), na pré-condição dos ritos de fechamento e sob pedido.

1. `elm_listar_wi(iteracao = "<pai>/<nome>" da sprint, tipo tarefa, limite 200)`.
2. **Conhecidas:** os ids da coluna "Tarefa ELM" de todas as seções do `sprint-<nn>.md`, a `[GB]` da linha da
   `## Sustentação` e a coluna `elm` do `backlog.md`; e as dos `status.md` das fatias `iniciada` (Histórico e campo
   ELM, `git show origin/<branch>:…`) e `pronta` (o `status.md` da base) — a `sdd-consolidar` ainda não as levou ao
   `backlog.md`. O resto é **externa**. Nenhuma → "sprint e EWM iguais" e fim.
3. **Inferir** cada externa com `elm_ler_wi(id)` (`pai`, `campos`, descrição), nesta ordem de pistas:
   - prefixo do sdd já no título (`[DEV]`, `[ESP]`, `[IMPL]`…) → é ele;
   - pai no EWM: IB `[FT-nnn]` (ou o item de origem da fatia) → tarefa de papel da fatia (`[DEV]`, `[REV]`, `[VER]`,
     `[APR]`); épico `[EP-nn]` → `[ESP]` do épico; IB de item (`[AT-012]`, `[IM-003]`…) → a tarefa dele; IB de
     categoria → item novo dela; `Sustentação` ou sem pai → item novo de Sustentação;
   - Classificação da Tarefa: Desenvolvimento → `[DEV]` (ou `[REV]`, se o dono é o revisor da fatia); Testes →
     `[VER]`; Análise / Especificação → `[ESP]`; a de uma categoria da tabela **Sustentação** do `sdd.md` → ela;
   - título e descrição (chamado → Atendimento; versão, deploy → Implantação; script, carga → Banco de dados…).
   Fatia ou épico sem pista → deixe `?` para a pessoa dizer.
4. **Perguntar**, numa tabela, o que cada uma é e o que fazer com o título:
   ```
   🔄 <pai>/Sprint <nn> × EWM — <n> tarefas fora da sprint
   | # | Tarefa | Título atual | Dono | Estado | É (inferido) | De | Título proposto |
   | 1 | 670210 | ajustar job de carga | joao.lima | Em Andamento | [DEV] | FT-034 | [DEV] FT-034 ajustar job de carga |
   | 2 | 670215 | subir versão 1.4 | ana.souza | Novo | [IMPL] | — (IM-004) | [IMPL] IM-004 subir versão 1.4 |
   | 3 | 670220 | reunião com a área | rita.melo | Novo | ? | ? | — |
   Título: renomear (padrão do sdd) · só incluir o prefixo · manter. Responda por linha ("3: [EXT]", "1: manter")
   ou "ok" para tudo como proposto.
   ```
   Tarefa de papel cuja fatia ou épico não está no `backlog.md` → não entra: indique a `sdd-triar` ("importar do
   EWM") para o IB e pare só nessa linha. Item que não é tarefa (IB, defeito) planejado na iteração e fora do
   `backlog.md` → liste à parte, com a mesma indicação.
5. **Gravar**, com um "sim" para o lote:
   - **tarefa de papel** → o id entra na coluna "Tarefa ELM" da linha da fatia ou do épico no `sprint-<nn>.md`
     (`DEV 669401 · DEV 670210`), com a Observação `trazida do EWM`; fatia ou épico que ainda não está na sprint →
     é um encaixe: a linha nasce `planejada` (o épico `novo` ou `elegivel` fica `planejado`; o `iniciado` não muda e
     a linha nasce `iniciada`) com `encaixe: trazida do EWM (<quem>, <data>)` e o P.O. confirma. Fatia `iniciada` → o `backlog.md` não muda (a `sdd-consolidar` leva os ids); avise
     o Dev para registrar o id no `status.md`;
   - **Sustentação** → tarefa de um item (pai IB `[AT-012]`) → o id vai para o `elm` dele e para a "Tarefa ELM" da
     linha dele na sprint (sem linha → o item entra na sprint, como abaixo). Senão, a linha da `### <Categoria>` do
     `backlog.md` com `elm` `pendente` que seja o mesmo pedido (triado sem o MCP e aberto à mão no EWM) → proponha
     ligar (sem id nem ficha novos). Nenhuma → a tarefa **vira item**: registre pelas regras da Sustentação da
     [`sdd-triar`](../../sdd-triar/SKILL.md#passo-3--registrar-na-base) (categoria confirmada, próximo id da série,
     duplicado pelo `**Origem:**` das fichas de `sustentacao/**`), com `origem` `EWM <id>`, `sprint` = a desta,
     `responsavel` = o dono no EWM e o `status` pelo estado (Novo → `aberto`, Em Andamento → `em-andamento`,
     concluída → `concluido` com `concluida-em`); a ficha leva o título e a descrição do EWM (sem dado de cliente),
     `**Estimativa:**` a da tarefa (ou `—`) e `falta: prazo, critério de pronto` no que o EWM não traz. Ligado ou
     novo, o item sem IB ganha o IB `[XX-nnn] <pedido>` (§6; a `### <Categoria>` nasce se for a primeira) e a tarefa
     passa a filha dele; linha na `## Sustentação` do `sprint-<nn>.md` com `trazida do EWM`. Reserva estourada → o
     item fica na sprint e o P.O. decide pelo Encaixe ([Durante a sprint](../SKILL.md#durante-a-sprint));
   - **EWM:** `elm_atualizar_wi(id, titulo)` pela escolha da linha; sem pai → `pai` = o IB da fatia ou o épico; na
     Sustentação, o IB do item (também quando o pai era a `Sustentação` ou o IB da categoria) — todo trabalho tem
     pai. Outro pai, dono e horas não mudam.
   Um commit `<pai>/Sprint <nn>: sincronizar com o EWM`, pelo bloco [Gravar na base](../../sdd-fatiar/references/backlog.md#gravar-na-base),
   na `[GB]`. As horas dessas tarefas já entram no relatório da virada (§5): `elm_horas(iteracao)` lista toda tarefa
   da iteração.
