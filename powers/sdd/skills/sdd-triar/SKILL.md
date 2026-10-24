---
name: sdd-triar
description: "Entrada de todo trabalho novo no fluxo sdd — recebe um pedido em texto, um item do EWM (defeito, item de backlog) ou um lote de itens do EWM, procura duplicados e faz a triagem: épico (várias histórias ou decisão de produto em aberto), padrão (regra de negócio clara, ficha aprovada pelo P.O.), rápida (defeito ou ajuste ≤ 1 dia sem regra nova, inclusive o que cabe numa frase) ou atendimento (consulta ou extração sem mudar o repositório). Registra no backlog.md da base — épico EP-nn, fatia com ficha ou AT-nnn com a tarefa [ATD]; EWM com confirmação — e não começa nada: indica o hub sdd-iniciar e pergunta se há mais itens. Use em \"nova demanda\", \"chegou um pedido\", \"o cliente pediu\", \"nova funcionalidade\", \"registra o defeito 4567\", \"coloca no backlog\", \"triagem\", \"aprova a ficha da FT-040\", \"importar do EWM\", \"triar os defeitos do time\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.0.0"
---

# sdd-triar — Triagem e registro

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-triar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Toda demanda nova entra por aqui. Triar é decidir **se** ela entra, **em que trilha** e **com que informação** —
sem começar nada. O que sai é uma linha no `backlog.md` (e, em toda fatia sem épico, a ficha; no atendimento, o
registro do AT e a `[ATD]`), que o planejamento puxa para a sprint. Começar é pelo hub **`sdd-iniciar`**, que
encaminha o item para a skill do papel.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare. Formato do
backlog e quem escreve cada coluna: [../sdd-fatiar/references/backlog.md](../sdd-fatiar/references/backlog.md).
Ficha da fatia (toda trilha): [references/ficha.md](references/ficha.md).

## Passo 1 — O que chegou

**Antes de tudo** — a triagem lê e escreve na base: itens 1 e 5 do bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) (troca
com "sim", `pull --ff-only`, árvore suja → pare; no fim, oferecer voltar).

| Entrada | Como ler |
|---|---|
| pedido em texto ("nova demanda: …", "corrigir o cálculo de juros") | a própria descrição |
| número do EWM (DF, IB) | `elm_ler_wi(id, comentarios)`; sem o MCP `elm` → peça à pessoa o título, a descrição e o comportamento esperado — nunca invente dado de work item |
| "importar do EWM", "triar os defeitos do time" | **lote** → Passo 5 |
| pedido de cliente sem mudança no repositório ("extrai as contas bloqueadas", "por que o caso X deu Y?") | trilha atendimento (Passo 2) |

**Já existe?** Antes de triar, procure no `backlog.md` da base (ids `FT`/`EP`, colunas `origem` e `elm`, títulos
parecidos, e a seção `## Atendimentos`), no `**Origem:**` dos `<produto>/atendimentos/AT-*.md` e nos `status.md` das branches
(`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`). Achou → mostre a linha e:
- **fatia sem épico que volta para cá** — `backlog` com `falta:`, ficha em `rascunho` ou a aprovar, mudança na
  ficha (pedida pela pessoa ou devolvida pela `sdd-plano` ou pela `sdd-consolidar`) ou trilha que não serve
  (devolvida pela `sdd-desenvolver`) → **retome a triagem dela**: Passo 2 com o mesmo `FT` e
  a ficha que existe; no Passo 3, só atualize a linha (sem id novo). Virou épico → `EP-nn` novo e a fatia
  `cancelada`, com `obs` `substituida-por EP-nn`;
- **épico em `rascunho` com `prd` `—`** que voltou (falta de informação para o PRD, P.O. ou EWM pendentes —
  devolvido pela `sdd-prd`, pela `sdd-especificar` ou pela Definition of Ready) → **complete o registro**: o que
  falta da linha (`po`, descrição mínima, `elm`), sem id novo, e siga para o Passo 4;
- o resto → pare: começar ou retomar é pelo hub **`sdd-iniciar`**; mudar uma fatia de épico é refinamento na
  **`sdd-fatiar`**.

## Passo 2 — Triagem

| Trilha | Quando | O que se registra |
|---|---|---|
| **épico** | funcionalidade nova com várias histórias ou fatias, mais de ~3 dias, mais de um objetivo, ou decisão de produto em aberto | `EP-nn` em `rascunho` → depois `sdd-prd` → `sdd-fatiar` |
| **padrão** | uma fatia (≤ G) que cria ou muda regra de negócio **clara** — o P.O. decide aqui —, sem decisão de produto em aberto | fatia sem épico, com **ficha** (regras, cenários, decisões) aprovada pelo P.O. |
| **rápida** | defeito ou ajuste ≤ 1 dia **sem** regra nova (o comportamento certo já está documentado ou é óbvio) — inclusive o diff que cabe numa frase (texto, configuração, ajuste trivial) | fatia sem épico, com ficha de **comportamento** (atual · esperado · não muda) e como verificar |
| **atendimento** | o cliente pede consulta, extração, explicação ou conferência; nada muda no repositório | `AT-nnn` na seção `## Atendimentos`, com o registro, a sprint sugerida e a `[ATD]` (a triagem registra; quem executa é a **`sdd-atender`**) |

- Fatia de um épico não passa de novo por aqui: o épico foi triado na entrada e as fatias dele vêm da `sdd-fatiar`.
- Diga a trilha e o motivo numa linha; dúvida entre duas → sim/não pela mais leve (rápida, depois padrão, depois épico). Padrão que precisaria de mais de
  ~3 cenários de comportamentos diferentes, ou de mais de uma regra nova independente → é épico.
- **Padrão:** rodadas da `sdd-entrevistar` até as regras e os cenários fecharem, gravando na seção Decisões da
  ficha (ela nasce aqui, com o próximo `FT-nnn` de "Próximos ids"); regra nova ou alterada → [similares](../sdd-prd/references/similares.md) antes de escrevê-la; no fim, o P.O.
  aprova a ficha. Sem a aprovação, a fatia fica `backlog` com `falta: aprovação do P.O.`.
- **Rápida:** **uma** rodada no formato da `sdd-entrevistar` (numerada, cada pergunta com a recomendação,
  "sim" aceita todas) para o que a ficha pede e a origem não traz: atual com evidência, esperado com fonte, o que
  não muda, como verificar.
- Fatos o agente busca (código, bundle do ELM pelas `elm_*_local`, banco só leitura); decisões são da pessoa.
- **Não fazer** (já entregue, fora do produto, recusado pelo P.O.) → nada no backlog; item do EWM → ofereça um
  comentário `sdd: não fazer — <motivo>` (`elm_comentar`, com "sim"), que o tira dos próximos lotes;
  fechar o item é do P.O., na UI.

## Passo 3 — Registrar (na base)

Grava-se na base, conferida no Passo 1. Backlog ainda com a seção antiga `## Fatias — trilha rápida` → renomeie-a
para `## Fatias — sem épico` e acrescente as colunas `trilha` (`rápida` nas linhas que já existem) e `ficha` (`—`),
no mesmo commit.

- **Épico:** próximo `EP-nn` de "Próximos ids"; linha em `## Épicos` com `status` `rascunho`, prioridade `—` (quem
  prioriza é o planejamento), `prd` `—` e `po` = o P.O. ativo do `equipe.json` (outro, se a pessoa disser).
  Descrição mínima (a mesma que a Definition of Ready do épico confere): o problema, quem pede e o resultado
  esperado — falta algum → pergunte numa rodada; sem resposta, `rascunho` com `obs` `falta: <o quê>`. Com ELM:
  nada é criado no EWM agora — o épico nasce quando entra numa sprint ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §3); `elm` = `—`. Veio
  de um item do EWM: se ele já é do tipo de épico do `sdd.md`, ele é o épico (grave o id na coluna `elm`) — quando
  esse tipo é o mesmo do item (Item de Backlog pai), pergunte se ele vira o épico ou o filho; filho (ou outro tipo)
  → `obs` `origem: <id>` (a sprint cria o épico e põe o item sob ele).

  **Pasta antecipada:** se o título tem mais de 3 palavras (slug formável), crie
  `<produto>/epicos/<EP>-<slug>/` com:
  - `rascunho.md`: o pedido original (nas palavras de quem pediu, sem dado inventado) + origem (EWM id,
    chamado, texto livre);
  - `decisoes.md`: o formato do Passo 3 da [`sdd-entrevistar`](../sdd-entrevistar/SKILL.md) (título `# Decisões — <EP-nn> <título>` e a tabela vazia).
  A pasta só é criada aqui; o `sdd-prd` completa com `prd.md`, `elm/` e os demais artefatos.
  Inclua o caminho relativo da pasta na coluna `pasta` do `backlog.md` (nova coluna após `prd`):
  `[pasta](epicos/<EP>-<slug>/)` ou `—` se não criada.
- **Fatia sem épico** (padrão, rápida): próximo `FT-nnn`; linha em `## Fatias — sem épico` com:
  - `trilha`; `origem` (`DF 4567`, `IB 611`, `AT-012`, `pedido: <resumo>`); `ficha`
    (`[ficha](fatias/FT-<nnn>-<slug>.md)`, sempre);
  - `tamanho` (padrão `P`/`M`/`G`; rápida `P`/`M`); `modo` proposto — `AFK` quando o esperado e o teste são claros
    e não há dado sensível, senão `HITL` (a fatia ainda não tem responsável: o modo final é gravado pela
    `sdd-planejamento` quando ela ganha um, pela senioridade de quem implementa — Júnior → `HITL` · Pleno → estes
    critérios · Sênior → `AFK` por padrão); prioridade, `sprint` e `responsavel` `—`;
  - `status` `pronta` se passa na Definition of Ready da trilha (formato do backlog — a ficha da trilha completa),
    senão `backlog` com `obs` `falta: <o quê>`.
  - **Ficha** (`<produto>/fatias/FT-<nnn>-<slug>.md`, formato da trilha em [references/ficha.md](references/ficha.md);
    crie a pasta se não existir): sempre.
  - EWM (com ELM): item de origem no EWM → nada a criar (ele será o pai das tarefas). Padrão ou rápida sem item de
    origem → nada agora: o IB `[FT-nnn]` (sob o épico de Sustentação) nasce quando a fatia entra na sprint (o
    planejamento cria).
- **Atendimento:**
  - **Entrevista curta:** `sdd-entrevistar` modo *atendimento* (uma rodada: o que o cliente precisa receber,
    origem, prazo, quem atende, critério de pronto). Regra de negócio em aberto → não é atendimento: volte ao
    Passo 2.
  - Próximo `AT-nnn` de "Próximos ids" (backlog antigo, sem `AT-`: regra de migração no formato do backlog).
  - **Sprint sugerida:** a aberta (`sprint-<nn>.md` com `**Situação:** aberta`), pela regra da reserva — a reserva
    (atendimento + retrabalho) está na seção Atendimento do `sprint-<nn>.md`; o usado é o retrabalho migrado mais a
    soma das estimativas dos AT dela; cabe com a
    estimativa deste (A-6) → quem triou confirma; estourou → `status` `backlog`, sem `[ATD]` (nasce quando o AT
    entrar numa sprint), e a decisão é do P.O. pelo Encaixe da
    `sdd-planejamento` (o atendimento não tira fatia sozinho).
    Kanban (`acordos.md`) → a iteração corrente. Sem sprint aberta → `status` `backlog` e o aviso "sem sprint
    aberta: o AT entra no próximo planejamento". Responsável sugerido: quem tem `atende: true` no `equipe.json`.
  - Linha em `## Atendimentos` (`aberto` na sprint, `backlog` sem ela); `<produto>/atendimentos/AT-<nnn>-<slug>.md`
    no formato da [`sdd-atender`](../sdd-atender/SKILL.md), com as respostas da entrevista no cabeçalho (A-6 em
    `**Estimativa:**`) e `**Situação:** aberto`; na sprint, a linha na seção Atendimento do `sprint-<nn>.md`.
  - EWM (com ELM), só com o AT na sprint: [elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §6, com "sim"; o id vai para a
    coluna `elm`. AT em `backlog` → nada agora (o encaixe ou o planejamento registram). Sem o MCP `elm` → `elm` =
    `pendente` (a `sdd-atender` registra antes de assumir).

Atualize "Próximos ids". O commit é **um só, no fim da sessão de triagem** (Passo 4, resposta "não"), com o
`backlog.md`, as fichas, os registros de AT e a linha de créditos da sessão na seção **Créditos de gestão** do `sprint-<nn>.md` aberto (Atividade `triagem`;
([`sdd-status`](../sdd-status/SKILL.md#fechar-a-sessão), item 4); sem sprint aberta, não há onde gravar) (padrão de commit do `sdd.md`). A triagem não tem tarefa própria e os
itens triados só nascem no EWM na sprint: o padrão é a tarefa **`[GB] Gerenciamento do backlog`** da linha
`Sustentação:` do `backlog.md` — mostre-a e confirme (a pessoa pode indicar outra). Linha sem `[GB]` → sugira
criá-la ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §2; só com sprint aberta, que dá a
iteração) ou pergunte a tarefa. Sem tarefa, não commite: deixe os arquivos e o comando pronto; push direto na base com o "sim" da pessoa
(no agente `sdd-produto`, que não faz push, entregue o comando pronto
— a pessoa executa). **Conflito de id** no push (outra
pessoa registrou o mesmo número antes): o agente não faz merge nem rebase — peça à pessoa `git pull --rebase`; no
conflito do `backlog.md`, mantenha o remoto e, **antes de renumerar**, confira de novo a `origem` (DF, IB, AT, pedido):
já está numa linha do remoto → a outra pessoa triou o mesmo item; descarte a sua linha e a sua ficha, mostre a
que existe e pare. Senão, pegue o próximo id livre para a sua linha (e para o nome
da ficha) e, se o item já foi criado no EWM, troque o `[FT-nnn]`/`[EP-nn]` do título (`elm_atualizar_wi`, com
"sim"). Id que ainda não chegou à base pode mudar; o que já chegou, nunca.

## Passo 4 — Encaminhar

```
📥 <FT-nnn | EP-nn | AT-nnn> — <título> · trilha <…> · <pronta | backlog: falta … | aberto na sprint <nn>> · modo <AFK | HITL>
Origem: <DF 4567 | IB 611 | chamado | pedido> · Ficha: <caminho | —> · EWM: <id | criado <id> | pendente | sem ELM>
Registrado. Para começar: use `sdd-iniciar <id>` (o hub encaminha para a skill do papel; épico e AT
precisam estar na sprint; a fatia fora dela a `sdd-desenvolver` puxa, Passo 3). AT fora da reserva → use `sdd-planejamento` (Encaixe) antes.
Mais algum item para triar?
```

- **"sim"** → volte ao Passo 1 com o novo item, na mesma sessão e na base (sem novo `switch` nem `pull`).
- **"não"** → mostre o resumo da sessão (ids, trilhas, pendências `falta:` e `ELM pendente`), faça o commit único
  do Passo 3 e encerre; se a triagem trocou de branch no Passo 1, ofereça voltar à anterior.

A triagem termina aqui. **Nunca invoque nem simule outra skill** (nem `sdd-iniciar`, nem a do papel): responda com
a instrução acima e pare. Recomeçar a própria triagem com o próximo item não é invocar outra skill.

## Passo 5 — Lote do EWM

"Importar do EWM", "triar os defeitos do time" — precisa do MCP `elm` nesta sessão; sem ele → diga isso e pare.

1. **Filtro**, com padrão e uma confirmação: o `pa` (vários → pergunte qual), tipos Defeito e Item de
   Backlog, estado `Novo` (o nome do estado inicial na PA; a pessoa troca). `elm_listar_wi(tipo, estado)`, por tipo.
2. **Fora do lote:** item cujo id já está no `backlog.md` (colunas `origem` e `elm`) ou no `**Origem:**` de um
   `<produto>/atendimentos/AT-*.md`, item criado pelo próprio fluxo (título com `[EP-`, `[FT-`, `[SUS-`, `[ESP]`,
   `[DEV]`, `[REV]`, `[VER]`, `[ATD]`), tarefas e, depois de ler o item (item 3), o que tem pai do fluxo (`[EP-`,
   `[SUS-`) ou o comentário `sdd: não fazer`. Mais de 15
   itens → mostre a contagem e peça um filtro mais fino.
3. Leia cada item (`elm_ler_wi(id, comentarios)`) e proponha a triagem numa tabela, com **uma
   confirmação para o lote**:
   ```
   📥 Lote EWM — <time> · <tipos> · estado <…> · <n> itens novos (<m> já no backlog)
   | Item | Tipo | Título | Trilha | Status | Motivo |
   |---|---|---|---|---|---|
   | DF 4567 | Defeito | Juros calculados em dobro no atraso | rápida | pronta | comportamento certo na REG 2101 |
   | IB 611 | Item de Backlog | Portal de renegociação de dívidas | épico | rascunho | várias histórias, decisões de produto |
   | IB 613 | Item de Backlog | Limitar o desconto de pontualidade a 10% | padrão | backlog | regra nova clara; falta: ficha |
   | DF 4570 | Defeito | Erro ao consultar CPF sem máscara | rápida | backlog | falta: como reproduzir |
   | IB 615 | Item de Backlog | Relação de contas bloqueadas para a auditoria | atendimento | aberto · sprint 3 | extração, sem mudança |
   "sim" registra tudo · ou ajuste por linha (ex.: "DF 4570: não fazer")
   ```
4. Com "sim": o Passo 3 para cada linha, com um commit para o lote e o EWM numa confirmação só. Padrão
   no lote → ficha em `rascunho` só com o Pedido e `falta: regras, cenários e aprovação do P.O.`; rápida
   sem o que a ficha da trilha pede → `backlog` com `falta: <o quê>` (a entrevista é uma a uma, depois). Atendimento no lote → registrado como no Passo 3, sem a entrevista curta (o item é o pedido;
   prazo e critério de pronto ficam `—`), com a sprint e o responsável da tabela e a `[ATD]` na mesma confirmação.
5. Saída: a tabela com os ids criados e o que ficou pendente — e **"Mais algum item para triar?"** (Passo 4).

## Regras

- Triar não começa: nunca cria branch, pasta de spec nem `status.md`, e nunca assume tarefa no EWM.
- O `backlog.md` e as fichas só são escritos na base; ids nunca são reaproveitados ("Próximos ids" só cresce).
- Ficha aprovada só muda por pedido explícito: volta a `rascunho`, mostre a diferença e peça a aprovação de novo;
  fatia já iniciada que dependa da mudança → avise quem a conduz.
- Nunca invente dado de work item, regra ou comportamento esperado: sem fonte e sem pessoa, fica `falta: …`.
- Toda escrita no EWM só com "sim"; sem o MCP `elm` ou com falha → `pendente` ([pendências](../sdd/references/elm.md#pendências)), e o fluxo segue.
