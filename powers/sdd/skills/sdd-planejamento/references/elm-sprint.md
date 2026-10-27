# Sprint no EWM

Regras comuns (prévia, um "sim", idempotência, pendências): [../../sdd/references/elm.md](../../sdd/references/elm.md).
**O backlog do EWM é a cópia do `backlog.md`:** todo épico, fatia e item de Apoio registrado tem o seu item no EWM.
Nasce com `iteracao = backlog` (o backlog do produto gravado no `pa`, §0) ou, se já entra numa sprint, com a iteração
dela. **Entrar na sprint** = `elm_atualizar_wi(ids, iteracao = a da sprint)` — move, nunca recria; só se cria o
que está `—` ou `pendente` na coluna `elm`. **Todo trabalho tem pai**: épico → IB → tarefa, ou o IB de
Sustentação da iteração pai para o que não vem de PRD. Ordem: épico, IB, tarefa. Tarefas (`[ESP]`, `[DEV]`, `[REV]`,
`[VER]`, `[APR]`, `[GB]`) nascem só na sprint; as únicas tarefas no backlog são as de Apoio que não couberam numa (§6).

## 0. Backlog do produto (na setup ou em "atualizar a configuração do sdd"; uma vez por projeto)

1. `elm_backlog()` → `atual` (o `ccm.backlog` do `pa`) e `candidatos` (planos de backlog da PA). Já há `atual` →
   mostre e confirme; fim.
2. Pergunte se o projeto **já tem** um backlog do produto no EWM — um só pode servir a todas as entregas (ex.:
   PA → `Backlog`, PA → `Entrega 1`, `Entrega 2`… com as sprints dentro), ou cada entrega pode ter o seu. Mostre os
   `candidatos`.
   - **Sim** → a pessoa escolhe um candidato ou cola o link do plano (o da UI web, com `id=_…`) →
     `elm_backlog(plano)`.
   - **Não** → pergunte o nome (padrão `Backlog`) e se a iteração é **filha** de outra (a entrega, a release) ou
     **sem pai** (no topo da timeline) → `elm_backlog(nome, pai?)`, com "sim" (cria a iteração e o plano
     `Backlog <time>`). Erro `permissao` → peça a quem administra a PA.
3. O `pa` passa a ter `ccm.backlog`; daí em diante `iteracao: "backlog"` nas tools é ele. Sem ele, criar no backlog
   falha com `precondicao` — volte a este §0, nunca escolha outra iteração.
4. **Espelhamento** (backlog já existente): linhas do `backlog.md` com `elm` `—` ou `pendente` que não estão
   concluídas nem canceladas → prévia numa tabela (item, tipo, pai, iteração) e um "sim" → §2, §3 e §6 na ordem;
   itens com `elm` que estão fora de sprint e numa iteração antiga → `elm_atualizar_wi(ids, iteracao = backlog)`.

## 1. Iteração e plano da sprint

`elm_iteracao("<pai>/<nome>")` acha ou cria a iteração da sprint **dentro da iteração pai** (o pai que falta nasce
irmão do pai anterior, na mesma release) e o plano da sprint do time, e guarda os ids no `pa` com a chave do caminho
(o backlog do produto não é criado aqui: é o do §0). O caminho tira a ambiguidade de duas `Sprint 1` em pais
diferentes; use-o em toda tool que recebe `iteracao`. Criar exige a permissão de modificar iterações — erro
`permissao` → peça a quem administra a PA.

## 2. Sustentação (uma por iteração pai, com a linha `Sustentação <pai>:` do `backlog.md` vazia ou de outro pai)

IB `Sustentação <produto> - <pai>` (`tipo: ib`; `<produto>` = o nome do produto do `sdd.md`; `<pai>` = a iteração
pai das sprints, ex.: `2026`), com `iteracao = backlog` — nasce no §0, na primeira triagem ou com a primeira sprint
de um pai novo, e **fica no backlog** (não entra em sprint nem move na virada). É o pai dos IBs de categoria do
Apoio (§6), da `[GB]` e das fatias sem épico.
Idempotência: `elm_listar_wi(iteracao = backlog, titulo_prefixo "Sustentação <produto> - <pai>")`. A tarefa
`[GB] Gerenciamento do backlog` (filha da Sustentação, dono = o P.O. ativo do `equipe.json`) nasce na primeira
sprint do pai, com a iteração dela. Ids na linha: `Sustentação <pai>: <id> · Backlog [GB] <id>`, e cada IB de
categoria entra nela quando nasce (`· Operação <id>`; §6). Sustentação já
existe sem a `[GB]` → crie só a `[GB]` (com sprint aberta). **Pai novo** (a sprint nova é `2027/01`): nasce a
Sustentação do pai novo e a `[GB]` dela (os IBs de categoria do pai novo nascem com o primeiro item de cada
uma, §6); a `[GB]` antiga conclui com o saldo de horas (`elm_transicao concluir`); a
linha do `backlog.md` passa a ser a do pai novo. Projeto com a antiga `[SUS-<ano>] Sustentação` e o IB `Atendimento`:
ficam como estão (nada se apaga no EWM) até o primeiro pai novo.

## 3. Épico e IB (nascem no registro; movem na sprint)

- **Épico** (na triagem, com "sim"; `iteracao = backlog`): `elm_criar_wi(tipo ib, "[EP-<nn>] <título>", dono = po da linha,
  descricao_md = problema, quem pede, resultado; depois do GATE, a solução e o link do PRD)`. Item de origem do EWM
  (`origem: <id>` na `obs`): já é do tipo épico → é o épico; senão `elm_atualizar_wi(origem, pai = épico novo, iteracao = backlog)`.
  Histórias publicadas → `elm_ligar(wi = épico, req, tipo rastreia)`. Épico registrado e não iniciado fica só ele
  no backlog; quando entra numa sprint (a `[ESP]` ou a primeira fatia), move para a iteração dela e a `[ESP]` nasce
  lá (§4).
- **IB da fatia** (no GATE do backlog da `sdd-fatiar`; fatia sem épico, na triagem; `iteracao = backlog` ou a da
  sprint em que já entra): `elm_criar_wi(tipo ib, "[FT-<nnn>] <título>", pai = épico — sem épico, a Sustentação;
  com item de origem, não há IB novo: `elm_atualizar_wi(origem, iteracao = backlog)` —, dono = P.O., descricao_md = modo, bloqueada por, pasta prevista, campos =
  {<campo de critérios do sdd.md>: os cenários Dado/Quando/Então copiados do PRD ou da ficha, com "gerado do PRD — não
  edite aqui"})`. Defeito: `campos` com a categoria de correção da seção ELM do `sdd.md`. Depois `elm_ligar(wi, req)`
  (implementa) para cada história coberta e `elm_ligar(wi, wi_destino, tipo depende)` para cada `bloqueada-por`
  (sem `links.depende` no `pa` → fica na descrição).
- **Fatia dividida:** como a linha do `sdd.md` manda (filhos do IB original, ou fecha o original e cria novos);
  pai errado → `elm_atualizar_wi(id, pai)`.
- Ids na coluna `elm` do `backlog.md`.
- **Na sprint** (depois do "ok"): épicos e IBs das fatias da sprint que já têm `elm` →
  `elm_atualizar_wi(ids, iteracao = a da sprint)` numa chamada; os `—`/`pendente` nascem como acima, já na iteração da
  sprint. Item que sai da sprint sem ter começado volta com `iteracao = backlog`.

## 4. Tarefas da sprint (depois do "ok" da sprint)

Para cada linha do `sprint-<nn>.md`, com a tabela "Tarefas no EWM" de `elm.md`: `elm_criar_wi(tipo tarefa, título,
pai, dono, estimativa_h, iteracao)` (Kanban: a iteração corrente). Fatia **AFK**: só a `[DEV]`. A `[APR]` não nasce aqui. Item da seção Apoio
sem `elm` → §6; com a tarefa no backlog → move (§6). Ids na coluna "Tarefa ELM" (`DEV <id> · REV <id> · VER <id>`) e no `elm` do `backlog.md`.

## 5. Virada

Antes de tudo, §9 (o que nasceu por fora entra nos Números). Próxima sprint em outro pai (`2026/04` → `2027/01`) → §1 com o pai novo e §2 (Sustentação e `[GB]` do pai novo)
antes de mover. Tarefas, IBs e épicos não concluídos da sprint (inclusive a `[GB]`, se o pai não muda; Sustentação e o que está no
backlog ficam onde estão) → `elm_atualizar_wi(ids, iteracao = a nova)` numa chamada (move, nunca recria; o pai não muda). Baseline por sprint, se o
`sdd.md` exigir → roteiro manual. Relatório: `elm_horas(iteracao)` → horas por prefixo e por pessoa, planejadas ×
lançadas, e as tarefas concluídas sem horas.

## 6. Apoio (chamado pela `sdd-triar`, pelo encaixe ou aqui)

**IB da categoria** (tabela **Apoio** do `sdd.md`), um por categoria e iteração pai: a linha `Sustentação <pai>:`
do `backlog.md` sem `<Categoria> <id>` → é o primeiro item da categoria no pai: crie, na mesma confirmação da
tarefa, `elm_criar_wi(tipo ib, "<Categoria> <produto> - <pai>", pai = Sustentação <produto> - <pai>, iteracao =
backlog)` (§2 antes, se a Sustentação faltar; idempotência: `elm_listar_wi(pai = <id da Sustentação>, titulo_prefixo
"<Categoria> <produto> - <pai>")`) e grave `· <Categoria> <id>` na linha. Fica no backlog, como a Sustentação; a
Categoria do IB é a padrão do tipo no `pa`.

**Tarefa:** `elm_criar_wi(tipo tarefa, "<prefixo> <ID> <título>", pai = o IB da categoria, dono = quem faz,
estimativa_h, iteracao = a da sprint do item; Kanban: a corrente; sem sprint ou fora da reserva: backlog)` — prefixo
e série do id pela categoria (tabela **Apoio** do `sdd.md`: `[ATD] AT-012 …`, `[IMPL] IM-003 …`); o `pa` aplica a
Classificação da Tarefa pelo prefixo. Fica no estado inicial. Item do backlog que entra numa sprint →
`elm_atualizar_wi(id, iteracao = a da sprint)`.

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
2. **Conhecidas:** os ids da coluna "Tarefa ELM" de todas as seções do `sprint-<nn>.md`, a `[GB]` da linha
   `Sustentação <pai>:` e a coluna `elm` do `backlog.md`; e as dos `status.md` das fatias em andamento (Histórico e
   campo ELM, `git show origin/<branch>:…` — a `sdd-consolidar` ainda não as levou à base). O resto é **externa**.
   Nenhuma → "sprint e EWM iguais" e fim.
3. **Inferir** cada externa com `elm_ler_wi(id)` (`pai`, `campos`, descrição), nesta ordem de pistas:
   - prefixo do sdd já no título (`[DEV]`, `[ESP]`, `[IMPL]`…) → é ele;
   - pai no EWM: IB `[FT-nnn]` → tarefa de papel da fatia (`[DEV]`, `[REV]`, `[VER]`, `[APR]`); épico `[EP-nn]` →
     `[ESP]` do épico; IB de categoria → a categoria dele; `Sustentação …`, `[SUS-…]` ou sem pai → Apoio;
   - Classificação da Tarefa: Desenvolvimento → `[DEV]` (ou `[REV]`, se o dono é o revisor da fatia); Testes →
     `[VER]`; Análise / Especificação → `[ESP]`; a de uma categoria da tabela **Apoio** do `sdd.md` → ela;
   - título e descrição (chamado → Atendimento; versão, deploy → Implantação; script, carga → Banco de dados…).
   Fatia ou épico sem pista → deixe `?` para a pessoa dizer.
4. **Perguntar**, numa tabela, o que cada uma é e o que fazer com o título:
   ```
   🔄 Sprint <pai>/<nn> × EWM — <n> tarefas fora da sprint
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
     é um encaixe: a linha nasce com `encaixe: trazida do EWM (<quem>, <data>)` e o P.O. confirma. Fatia em
     andamento (`status.md` numa branch) → o `backlog.md` não muda (a `sdd-consolidar` leva os ids); avise o Dev
     para registrar o id no `status.md`;
   - **Apoio** → próximo id da série da categoria; linha em `## Apoio` do `backlog.md` (`origem` `EWM <id>`, `elm` =
     `<prefixo> <id>`, `sprint`, `responsavel` = dono, `status` pelo estado: concluída → `concluido` com
     `concluida-em`), registro mínimo `<produto>/apoio/<pasta>/<ID>-<slug>.md` (o título e a descrição do EWM, sem dado de
     cliente) e linha na seção Apoio do `sprint-<nn>.md` com `trazida do EWM` — consome a reserva (passou → aviso
     ao P.O., como no Encaixe);
   - **EWM:** `elm_atualizar_wi(id, titulo)` pela escolha da linha; sem pai → `pai` = o IB da fatia, o épico ou, no
     Apoio, o IB da categoria (§6: nasce aqui, se for o primeiro da categoria no pai) — todo trabalho tem pai. Pai
     existente, dono e horas não mudam.
   Um commit `sprint <pai>/<nn>: sincronizar com o EWM`, pelo bloco [Gravar na base](../../sdd-fatiar/references/backlog.md#gravar-na-base),
   na `[GB]`. As horas dessas tarefas já entram no relatório da virada (§5): `elm_horas(iteracao)` lista toda tarefa
   da iteração.
