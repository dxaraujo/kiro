# Sprint no EWM

Regras comuns (prévia, um "sim", idempotência, pendências): [../../sdd/references/elm.md](../../sdd/references/elm.md).
**Só nasce no EWM o que entra numa sprint** (exceto a `[GB]`); **todo trabalho tem pai**: épico → IB → tarefa, ou o
épico de Sustentação para o que não vem de PRD. Ordem: épico, IB, tarefa. `iteracao` = a da sprint em tudo.

## 1. Iteração e planos

`elm_iteracao(nome)` acha ou cria a iteração e os planos do time (backlog e sprint) e guarda os ids no `pa`.
Criar exige a permissão de modificar iterações — erro `permissao` → peça a quem administra a PA.

## 2. Sustentação (uma vez por ano, com a linha `Sustentação:` do `backlog.md` vazia)

Épico `[SUS-<ano>] Sustentação` (`tipo: ib` — ou o tipo de épico, se o `pa` tiver), filho dele o IB `Atendimento`
(pai das `[ATD]`) e a tarefa `[GB] Gerenciamento do backlog` (dono = o P.O. ativo do `equipe.json`). Ids na linha:
`Sustentação: SUS <id> · Atendimento <id> · Backlog [GB] <id>`. Sustentação já existe sem a `[GB]` → crie só a `[GB]`.

## 3. Épico e IB (quando entram na sprint)

- **Épico** (pela `[ESP]` ou pela primeira fatia): `elm_criar_wi(tipo ib, "[EP-<nn>] <título>", dono = po da linha,
  descricao_md = problema, quem pede, resultado; depois do GATE, a solução e o link do PRD)`. Item de origem do EWM
  (`origem: <id>` na `obs`): já é do tipo épico → é o épico; senão `elm_atualizar_wi(origem, pai = épico novo)`.
  Histórias publicadas → `elm_ligar(wi = épico, req, tipo rastreia)`.
- **IB da fatia:** `elm_criar_wi(tipo ib, "[FT-<nnn>] <título>", pai = épico — sem épico, a Sustentação; com item
  de origem, não há IB novo —, dono = P.O., descricao_md = modo, bloqueada por, pasta prevista, campos =
  {<campo de critérios do sdd.md>: os cenários Dado/Quando/Então copiados do PRD ou da ficha, com "gerado do PRD — não
  edite aqui"})`. Defeito: `campos` com a categoria de correção da seção ELM do `sdd.md`. Depois `elm_ligar(wi, req)`
  (implementa) para cada história coberta e `elm_ligar(wi, wi_destino, tipo depende)` para cada `bloqueada-por`
  (sem `links.depende` no `pa` → fica na descrição).
- **Fatia dividida:** como a linha do `sdd.md` manda (filhos do IB original, ou fecha o original e cria novos);
  pai errado → `elm_atualizar_wi(id, pai)`.
- Ids na coluna `elm` do `backlog.md`.

## 4. Tarefas da sprint (depois do "ok" da sprint)

Para cada linha do `sprint-<nn>.md`, com a tabela "Tarefas no EWM" de `elm.md`: `elm_criar_wi(tipo tarefa, título,
pai, dono, estimativa_h, iteracao)` (Kanban: a iteração corrente). Fatia **AFK**: só a `[DEV]`. A `[APR]` não nasce aqui. AT da seção Atendimento
sem `elm` → §6. Ids na coluna "Tarefa ELM" (`DEV <id> · REV <id> · VER <id>`) e no `elm` do `backlog.md`.

## 5. Virada

Tarefas, IBs e épicos não concluídos (inclusive Sustentação, Atendimento e `[GB]`) →
`elm_atualizar_wi(ids, iteracao = a nova)` numa chamada (move, nunca recria; o pai não muda). Baseline por sprint, se o
`sdd.md` exigir → roteiro manual. Relatório: `elm_horas(iteracao)` → horas por prefixo e por pessoa, planejadas ×
lançadas, e as tarefas concluídas sem horas.

## 6. Atendimento `[ATD]` (chamado pela `sdd-triar`, pelo encaixe ou aqui)

`elm_criar_wi(tipo tarefa, "[ATD] AT-<nnn> <título>", pai = Atendimento, dono = quem atende, estimativa_h, iteracao
= a da sprint do AT; Kanban: a corrente)`. AT sem sprint não é registrado. Fica no estado inicial.

## 7. Troca AFK → HITL (só pela seção "Troca de modo")

Cria a `[REV]` e a `[VER]` como no §4 (mesmo pai da `[DEV]`), com o revisor e o verificador da decisão. A `[DEV]` não
muda. HITL → AFK não existe.

## 8. `[APR]` no gate (chamada pela `sdd-plano`, `sdd-implementar` Passo 5 ou `sdd-loop`)

`elm_listar_wi(pai = IB, titulo_prefixo "[APR] FT-<nnn> Aprovar <plano|PR>")` → já existe: é ela (volta a ser
aprovada depois de ajustes). Senão `elm_criar_wi(tipo tarefa, "[APR] FT-<nnn> Aprovar <plano|PR>", pai = IB, dono = o
Dev Sênior escolhido, estimativa_h perguntada, iteracao da fatia)`. Fica no estado inicial; o id vai para o campo ELM
do `status.md`.
