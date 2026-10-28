# Plano — situações que respondem ao P.O. e ao SM, uma tabela de fatias, Sustentação no lugar de Apoio e só Scrumban (sdd 3.4.0)

## Contexto

Na primeira review, o P.O. e o SM não conseguiram responder pelo `backlog.md` e pelo `sprint-<nn>.md` duas
perguntas: **o que falta fazer no projeto** (backlog) e **o que foi feito em cada sprint** (backlog e sprint) — em
especial, em que pé estavam as fatias mergeadas e ainda não consolidadas. Causas no power `sdd` 3.3.1 (`powers/sdd`):

1. **O andamento não chega à base.** "Em andamento não é gravado: é a fatia que tem `status.md` numa branch"
   (`sdd-fatiar/references/backlog.md:59`); a coluna Status da sprint "espelha o backlog no fechamento; durante a
   sprint, o painel é a fonte" (`sdd-planejamento/references/arquivos.md:203`). Quem lê os arquivos não vê
   iniciada nem mergeada.
2. **Nomes que confundem:** `pronta` quer dizer "passou na DoR" e soa como terminada; `→ sprint <chave>` não se
   explica; a chave `2026/03` parece um mês; prioridade é um número.
3. **Dois vocabulários para a mesma coisa:** a especificação na sprint (`entrevista · PRD · fatiamento · concluida`)
   e o épico no backlog (`rascunho · em-revisao · aprovado · fatiado · concluido`, espelho do frontmatter do PRD).
4. **"Apoio" não casa com o EWM**, onde o pai é a Sustentação; uma tabela só para todas as categorias; as fatias
   espalhadas em uma seção por épico mais a "sem épico".
5. **Duas metodologias** (Scrum ou Kanban, escolhidas nos acordos), quando o sdd inteiro é Scrumban: o ramo Kanban
   só duplica regras.

Resultado esperado: cada transição gravada no `backlog.md` e na sprint por quem a causa; vocabulário curto e
próximo do EWM; Sustentação com a mesma árvore no repositório e no EWM; um fluxo só. O power ainda não tem
usuários: **nada de migração** — e saem as regras de compatibilidade das versões anteriores.

O plano foi conferido por um mapeamento de 68 arquivos (528 trechos) e por três revisões adversariais (máquina de
estados, git e permissões, EWM); os furos achados estão corrigidos abaixo.

## Discussões e decisões

| # | Questão | Opções levantadas | Decisão |
|---|---|---|---|
| 1 | Situação com que o item nasce no backlog | registrada · triada · nova · cadastrada | **`nova`** (fatia) / **`novo`** (épico) — para o que muda o repositório |
| 2 | Situação de quem passa na DoR (no lugar de `pronta`) | apta · refinada · preparada · elegível | **`elegivel`** — sem acento nos arquivos, como `concluida` |
| 3 | Épico × especificação | (a) `fatiado`, depois `concluido` · (b) `iniciado` até a última fatia · (c) `concluido` no GATE do backlog | **a especificação é uma fase dentro do épico**: épico `novo → elegivel → planejado → iniciado → concluido`; o rascunho (sem informação para o PRD) é a fase inicial (`novo`); a linha da Especificação na sprint vai `planejada → iniciada → concluida`; o épico conclui com a última fatia, como no EWM. O fluxo detalhado fica na Fase do `status.md` do épico (decisão 24) |
| 4 | Onde ficam as fatias sem épico (filhas do IB Manutenção no EWM) | Sustentação › Manutenção no backlog e na sprint · só no backlog · nada muda | **uma tabela só de fatias** no `backlog.md` (somem as seções por épico e a "sem épico"), com a coluna `origem` = `EP-nn` ou `Manutenção`; a origem "veio de um atendimento" vai para a `obs` (`vinculada a [AT-012](…)`, link para a ficha) e vira link `relacionado` no EWM |
| 5 | Títulos do IB do item de Sustentação e da tarefa | IB `[AT-012]` + tarefa `[ATD] AT-012` · IB e tarefa `[ATD-012]` | **IB `[AT-012] <pedido>` + tarefa `[ATD] AT-012 <pedido>`**: o mcp-elm segue classificando e somando horas pelo prefixo `[ATD]` (`ewm.py:303`, `ewm.py:680`) |
| 6 | Fase do AFK com PR aberto esperando a `[APR] Aprovar PR` | `aguardando-aprovacao-pr` · `aceita` também | **`aguardando-aprovacao-pr`** |
| 7 | Pasta das fichas | `sustentacao/<categoria>/` · manter `apoio/` | **`<produto>/sustentacao/<categoria>/`** e `.kiro/local/sustentacao/<categoria>/` |
| 8 | Ciclo do item de Sustentação sem mudança no repositório | `aberto → em-andamento → concluido` · `nova → planejada → em-andamento → concluido` | **`aberto → em-andamento → concluido · cancelado`**, como o EWM; some `backlog` (fora de sprint = coluna `sprint` `—`) |
| 9 | Fases do `status.md` (pedido) | — | `plano-em-revisao` → **`aguardando-aprovacao-plano`**; `pronta-para-merge` → **`aceita`** (HITL); `mergeada` → **`pronta`**, gravada na base; `concluida` na consolidação |
| 10 | O `aceita` do AFK antes do PR (decorre de 6 e 9: `aceita` passa a ser "falta só o merge") | rotear por fase + modo · outro nome | **`verificada`** (AFK: verificação do subagente aceita, PR ainda não aberto): cada fase leva a uma ação só; `aceita` só no HITL. Rotear por modo deixava a fatia HITL `aceita` ser mandada abrir PR (`sdd-desenvolver:157`, `sdd-implementar` Passo 0) |
| 11 | `→ sprint <chave>` | situação própria `migrada` · última situação + Observação | Era "foi para a sprint `<chave>`", gravado na virada no item não concluído. **Some:** a linha da sprint que fecha guarda a última situação e a Observação `migrada para <chave>`; a linha nova, a mesma situação e `migrada de <chave>` |
| 12 | Chave da sprint | caminho da iteração no EWM · `<pai>/Sprint <nn>` do arquivo | **`<pai>/Sprint <nn>`** (`2026/Sprint 03`), do número do arquivo — o nome da iteração no EWM é livre e fica só no `**Iteração no EWM:**` (vale também sem ELM). Cabeçalho `# 2026/Sprint 03 · …`; commit `2026/Sprint 03: planejar` |
| 13 | Prioridade | número · categoria | **`baixa · média · alta · crítica`**; empate → a ordem da linha na tabela (o P.O. ordena); `—` no fim; a fatia herda a do épico ao nascer; não vai ao EWM |
| 14 | Coluna `elm` | id solto · tipo antes do id | **tipo antes de cada id**: `IB [612010](…) · DEV [612011](…)`; `DF` quando o item da fatia é o defeito de origem |
| 15 | Créditos | — | coluna em todas as tabelas de itens (inclusive as novas por categoria); a conclusão grava na sprint e a virada copia para o backlog (regra de hoje) |
| 15a | Créditos do épico | só a especificação · especificação + fatias | **só a especificação** (`[ESP]`), copiados na virada da sprint em que a linha da Especificação ficou `concluida` |
| 16 | Quem grava `iniciada` e `pronta` | o Dev na base · `pronta` na branch antes do merge · só o painel | **o Dev, na base** (`sdd-desenvolver`; no loop, o orquestrador, um commit por lote). `pronta` na branch mudaria o sha aprovado |
| 16a | Push desses commits na base | a pessoa dá o push (comando pronto) · o agente pergunta e dá o push | **o agente pergunta e dá o push** (codificador e orquestrador). Como o Kiro não restringe push por arquivo, a skill confere antes (`git diff --name-only origin/<base>..<base>`) que só sobem `<produto>/backlog.md`, `<produto>/sprints/**` e o `status.md` da fatia — senão para. O agente de produto continua entregando o comando (não foi pedido mudar) |
| 16b | Base protegida no GitLab (Developer sem push) | requisito do sdd · o P.O. registra no lugar do Dev | **requisito**: quem desenvolve tem push na base (a setup avisa). O agente do Dev ganha commit e push na base, perguntando antes de cada um, e sempre `git fetch` + `pull --ff-only` antes de gravar. Push recusado → desfaz só o commit de registro não publicado (`git reset --keep origin/<base>`, com "sim") e para, explicando |
| 17 | Nomes no EWM | com o produto (3.3.1) · sem | **`Sustentação`**, **`Manutenção`**, **`<Categoria>`** sem o produto (pedido); a pergunta do nome curto do produto sai da setup. O §0 recusa um backlog do EWM que já tenha a Sustentação de outro produto |
| 18 | Manutenção consome a reserva? | não, entra pela capacidade · sim | **não**: a reserva (Sustentação + retrabalho) cobre as categorias sem mudança no repositório e o retrabalho; fatia de Manutenção entra pela vazão (puxada ou encaixe), como a de épico |
| 19 | "pronto" em outros nomes (Contrato de pronto, `Pronto quando:`, `RESULTADO: PRONTO`, "critério de pronto") | renomear · manter | **manter** esses nomes: falam de tarefa, plano ou do critério do item, não da situação da fatia. Mas o texto solto que chama a **fatia** de pronta sem ser "mergeada" muda ("as prontas da sprint" → as planejadas; "pronta para a revisão" → aguardando revisão; "PR pronto" → PR aberto; "não está pronto, só está parado" → "não está entregue"); e "tarefa iniciada" (estado do EWM) vira "tarefa assumida", para não colidir com a situação `iniciada` |
| 20 | Versão | 3.4.0 · 4.0.0 | **3.4.0** no power, nas 22 skills e no mcp-elm **se ele for alterado** (pedido). Pelo mapeamento ele não precisa mudar (o `relacionado` já existe, `tests/test_rm_qm.py:89`; `elm_atualizar_wi` já aceita `dono`); se a execução mexer nele (código, docstring ou manual), sobe junto para 3.4.0, com testes, wheel em `dist/` e o `plugin.json` exigindo `mcp-elm >= 3.4.0` |
| 21 | Metodologia | Scrum ou Kanban, escolhida nos acordos (hoje) · uma só | **só Scrumban** (pedido): o sdd já é Scrumban — sprint como cadência (meta, review, retrospectiva, virada) com fluxo puxado e limite de WIP dentro dela. Somem a escolha da cadência e todo ramo "Kanban" (seção 5) |
| 22 | Migração | migrar projetos 3.3.x · nenhuma | **nenhuma** (pedido): nenhum projeto usa o power, ainda em desenvolvimento. Nem migração da 3.4.0 nem leitura de valores antigos; e saem as regras de compatibilidade e migração das versões anteriores (seção 6) |
| 24 | Onde mora o fluxo detalhado do épico (`rascunho → em-revisao → aprovado → fatiado → concluido · cancelado`), hoje no frontmatter do PRD e copiado no backlog | Fase no `status.md` do épico · frontmatter do PRD (como hoje) | **Fase no `status.md` do épico**, como na fatia: o backlog mostra a situação; o `status.md` (que já existe, com início e créditos) guarda a fase. Ele nasce na triagem junto com o `rascunho.md` ("um rascunho é gerado e o status também"); o frontmatter do PRD perde o `status` (fica a versão no rodapé). Um lugar só |
| 23 | Terminal fish (aviso do usuário: comando de bash trava nele) | regra no steering do power · nada no power | **nada muda no power**: o fish é o terminal de quem desenvolve o power (este repositório), não o de quem o usa; a regra "Shell da pessoa" da `sdd-setup` (`SKILL.md:62-64`) continua. Vale para a execução deste plano: comandos rodados ou sugeridos aqui sem sintaxe só de bash, ou em `bash -c '…'` |

## 1. Situações

Valores grafados sem acento, como hoje (`concluida`); fatia no feminino, épico e item de Sustentação no masculino.
Cada escrita no `backlog.md` e na sprint segue o bloco [Gravar na base](powers/sdd/skills/sdd-fatiar/references/backlog.md)
e vai **no mesmo commit** nos dois arquivos.

### Fatia — `status` no backlog · Status na sprint

| Situação | Quando | Quem grava | Onde |
|---|---|---|---|
| `nova` | registrada (triagem, fatiamento) ou DoR que deixou de valer (`obs` `falta: …`) | `sdd-triar` · `sdd-fatiar` | backlog |
| `elegivel` | passou na DoR da trilha | `sdd-triar` · `sdd-fatiar` · `sdd-planejamento` | backlog |
| `planejada` | entrou numa sprint (planejamento, encaixe) | `sdd-planejamento` | backlog (+ `sprint`) · a linha nasce na sprint |
| `iniciada` | a `sdd-desenvolver` começou: grava na base **e então** cria a branch | `sdd-desenvolver` Passo 4 · no loop, o orquestrador | backlog (+ `responsavel`, se `—`) · sprint (puxada: a linha nasce aqui, com `puxada`, revisor, verificador e `revisor único`) |
| `pronta` | PR mergeado | `sdd-desenvolver` Passo 6, na base | backlog · sprint · `status.md` da base |
| `concluida` | consolidada | `sdd-consolidar` | backlog (`concluida-em`) · sprint (Créditos) · `status.md` |
| `dividida` · `cancelada` | desvios (`obs` `substituida-por FT-…` · motivo) | `sdd-fatiar` · `sdd-triar` | backlog e a linha da sprint |

- **Volta.** A DoR que deixou de valer (PRD reaberto, ficha devolvida, decisão em aberto) rebaixa a `nova` só a fatia
  `elegivel` ou `planejada`. A `planejada` que sai da sprint (DoR perdida ou troca do Encaixe) fica `nova` ou
  `elegivel`, com `sprint` `—`, e a linha dela na sprint recebe a mesma situação e `saiu da sprint: <motivo>
  (<quem>, <data>)`. De `iniciada` em diante nada volta: a fatia para em `bloqueada (de: <fase>)` no `status.md`,
  com o motivo, até o P.O. decidir. Juntar só entre fatias não iniciadas (a absorvida: `cancelada` com
  `substituida-por`).
- **Dividida ou cancelada depois de `iniciada`:** a `sdd-fatiar` (ou a `sdd-triar`, na sem épico) conclui as tarefas
  abertas da fatia com as horas lançadas (sem o MCP, `ELM pendente`), avisa o Dev para fechar o PR, e as novas nascem
  `nova` com `obs` `desmembrada de FT-…`. Os leitores ignoram o `status.md` da branch de fatia `dividida` ou
  `cancelada` na base.

### Fases do `status.md` (o detalhe de `iniciada`)

```
HITL  pesquisando → planejando → [aguardando-aprovacao-plano] → implementando → pr-aberto → em-revisao
      → em-verificacao → aceita → (merge) pronta → concluida
AFK   pesquisando → planejando → [aguardando-aprovacao-plano] → implementando → revisando → verificando
      → verificada → aguardando-aprovacao-pr → (merge) pronta → concluida
```

- Desvios de hoje mantidos: `bloqueada (de: …)`, `retrabalho (de: …)`. Novo: **conflito no merge** (Passo 6) →
  `retrabalho (de: aceita | aguardando-aprovacao-pr)`; a `sdd-implementar` aceita essa fase, atualiza a branch e
  segue — HITL volta a `pr-aberto` (nova REV e VER), AFK volta a `revisando` (subagentes) e a `[APR] Aprovar PR`
  é reaberta.
- WIP esperando pessoa: `aguardando-aprovacao-plano` + `pr-aberto` + `em-revisao` + `em-verificacao` + `aceita` +
  `verificada` + `aguardando-aprovacao-pr`.
- Merge (`sdd-desenvolver` Passo 6): HITL em `aceita`; AFK em `aguardando-aprovacao-pr` com a `[APR] Aprovar PR`
  concluída (a aprovação não grava fase: o sha não muda — como hoje).
- **A base prevalece:** `pronta` e `concluida` só existem no `status.md` da base. Para uma fatia, o `status.md` de
  `origin/<base>` em `pronta` ou `concluida` vale sobre o da branch (que fica parado na fase do merge): painel, WIP
  (`sdd-desenvolver`, `sdd-loop`) e roteamento (`sdd-iniciar`, `sdd-desenvolver` Passo 1) leem por essa regra, que
  mora no `status-template.md`.

### Épico — `status` no backlog · Situação da Especificação na sprint

| Épico | Especificação | Quando | Quem grava |
|---|---|---|---|
| `novo` | — | triado; sem informação para o PRD, a pasta antecipada guarda o `rascunho.md` | `sdd-triar` |
| `elegivel` | — | DoR do épico (uma só, no `backlog.md`: o problema, quem pede, o resultado e o `po`) | `sdd-triar` · `sdd-planejamento` |
| `planejado` (+ `sprint`) | `planejada` | `[ESP]` planejada | `sdd-planejamento` |
| `iniciado` | `iniciada` | `[ESP]` assumida (Passo 2): só a situação vai à base; épico não planejado → a linha nasce na sprint aberta, como a puxada | `sdd-especificar` |
| `iniciado` | `concluida` (+ Créditos) | GATE do backlog: a `[ESP]` conclui; o épico segue com as fatias | `sdd-especificar` Passo 6 |
| `concluido` | — | última fatia concluída (backlog, Fase do `status.md` do épico e EWM) | `sdd-consolidar` |
| `cancelado` | `cancelada` | decisão do P.O.: as fatias não iniciadas ficam `cancelada` e a `[ESP]` conclui com as horas lançadas, na mesma gravação | `sdd-fatiar` |

O GATE do PRD grava no backlog só o link `prd` (o épico segue `iniciado`).

### Fases do `status.md` do épico (o detalhe do épico, como o da fatia)

```
rascunho → em-revisao → aprovado → fatiado → concluido · cancelado
```

| Fase | Quando | Quem grava |
|---|---|---|
| `rascunho` | triado (`status.md` nasce na pasta do épico com o `rascunho.md` e o `decisoes.md`; sem pasta antecipada, nasce na pasta de trabalho da `sdd-especificar`) e durante a entrevista e a escrita do PRD | `sdd-triar` · `sdd-especificar` |
| `em-revisao` | PRD na revisão P; também na mudança depois de aprovado | `sdd-prd` |
| `aprovado` | GATE do PRD (a pasta vai à base com o `status.md`) | `sdd-prd` |
| `fatiado` | GATE do backlog | `sdd-fatiar` |
| `concluido` | última fatia concluída | `sdd-consolidar` |
| `cancelado` | decisão do P.O. | `sdd-fatiar` |

- O `status.md` do épico ganha a linha `Fase` (modelo da `sdd-especificar` Passo 3, que a `sdd-triar` passa a usar);
  antes do GATE do PRD ele vive na pasta de trabalho local, como o `prd.md` hoje.
- O frontmatter do `prd.md` perde o `status` (`prd-template.md`); versão e aprovação seguem no rodapé.
- Quem roteava pelo `status` do PRD passa a ler a Fase: `sdd-especificar` Passo 4, `sdd-prd` ("PRD
  `aprovado`/`fatiado` só muda por pedido explícito"), `sdd-fatiar`, `sdd-status` (PRDs pendentes).

### Item de Sustentação sem mudança no repositório — `status` no backlog · Situação na sprint

| Situação | Quando | Quem grava |
|---|---|---|
| `aberto` | triado (na sprint ou fora dela: `sprint` `—`) | `sdd-triar` · `sdd-planejamento` §9 |
| `em-andamento` | tarefa assumida — antes, cria o IB e a tarefa que faltarem; commit `<ID> iniciar` (concluído na mesma sessão → um commit só) | `sdd-atender` · `sdd-executar` |
| `concluido` | tarefa e IB do item concluídos (+ Créditos na sprint; backlog na virada) | `sdd-atender` · `sdd-executar` |
| `cancelado` | correção do registro; cancelar o IB e a tarefa é na UI do EWM (`ELM pendente [<ID> cancelar]`: o MCP não cancela) | `sdd-triar` |

### Virada

Migra só o que não está em situação terminal (`concluida`, `dividida`, `cancelada`, `concluido`, `cancelado`) e
cuja `sprint` no backlog é a que fecha. A linha da sprint que fecha guarda a última situação e ganha `migrada para
<chave>`; na sprint nova, a linha nasce com a mesma situação e `migrada de <chave>`; no backlog só muda a `sprint`.
Fatia `pronta` sem consolidação, com a decisão do P.O.: igual, mais `não consolidada`. Créditos do épico: copiados
quando a linha dele na Especificação ficou `concluida` nesta sprint. A review abre pelo resumo da coluna Status
(concluídas · prontas sem consolidar · iniciadas e planejadas que migram) — é a pergunta que ficou sem resposta.

## 2. Formatos

`backlog.md` (`sdd-fatiar/references/backlog.md`):

```markdown
# Backlog — Gestão de Acessos

Próximos ids: EP-04 · FT-034 · AT-013 · IM-004 · BD-001 · IN-002 · OP-001 · EX-001

## Épicos
| id | título | status | prioridade | po | sprint | prd | pasta | elm | creditos | obs |
| EP-03 | Bloqueio por tentativas de login | iniciado | alta | ana.souza | 2026/Sprint 02 | [prd](…) | [pasta](…) | IB [612001](…) · ESP [669377](…) | 18.40 | — |

## Fatias
| id | título | origem | trilha | cobre | ficha | bloqueada-por | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | creditos | obs |
| FT-031 | Bloquear a conta após 3 tentativas | EP-03 | padrão | HF-01#1.1, REG-01 | [ficha](…) | — | M | AFK | alta | iniciada | 2026/Sprint 03 | joao.lima | IB [612010](…) · DEV [612011](…) | — | — | — |
| FT-034 | Corrigir juros no atraso | Manutenção | rápida | — | [ficha](…) | — | P | AFK | crítica | elegivel | — | — | DF [4567](…) | — | — | vinculada a [AT-012](sustentacao/atendimento/AT-012-contas-bloqueadas.md) |

## Sustentação
IB [612000](…) · GB [612006](…) · Manutenção IB [612030](…)

### Atendimento
IB [612020](…)
| id | título | origem | status | sprint | responsavel | elm | registro | concluida-em | creditos |
| AT-012 | Extração de contas bloqueadas em setembro | chamado 4521 | em-andamento | 2026/Sprint 03 | joao.lima | IB [669379](…) · ATD [669380](…) | [AT-012](sustentacao/atendimento/AT-012-contas-bloqueadas.md) | — | — |
```

- `## Fatias`: uma tabela, ordem por prioridade (crítica → baixa, `—` no fim) e, no empate, a ordem da linha.
  `origem` = `EP-nn` ou `Manutenção`; dividida → a das originais, com `obs` `desmembrada de FT-…`. O item do EWM de
  origem fica na coluna `elm` com o id — `DF [4567](…)`, ou `DF 4567` sem link quando não há o MCP (o id já é
  conhecido; nunca `pendente`); o `pedido: …` fica na ficha. `cobre` e `bloqueada-por` valem para todas (`—` quando
  não há).
- `## Sustentação`: a linha da Sustentação (hoje é a `Sustentação:` do topo) e uma `### <Categoria>` por categoria,
  na ordem da tabela do `sdd.md`, **criada quando o primeiro item dela é triado** (junto com o IB da categoria, cujo
  id abre a seção). Sem a coluna `categoria` (a seção diz).
- Épicos ganham as colunas `sprint` (a da `[ESP]`) e `obs` (`falta: …` e `origem: <id>`, que a triagem e o
  `elm-sprint.md` §3 já gravam sem ter coluna). A fatia criada pela `sdd-fatiar` herda a prioridade do épico.

`sprint-<nn>.md` (`sdd-planejamento/references/arquivos.md`): cabeçalho `# 2026/Sprint 03 · <início> → <fim>`;
`## Fatias` ganha a coluna Origem; `## Especificação` ganha Observação; `## Apoio` vira `## Sustentação`, com a
linha da reserva (Sustentação + retrabalho) e **só as `### <Categoria>` com itens na sprint**. Status e Situações
pela seção 1, gravados durante a sprint (some "espelha o backlog no fechamento").

## 3. EWM

```
<linha de base>/Backlog
├── IB Sustentação                     um por produto; fica no backlog
│   ├── [GB] Gerenciamento do backlog  uma por pai de sprint
│   ├── IB Manutenção                  nasce com a 1ª fatia sem épico
│   │   └── IB [FT-034] … | DF 4567 (item de origem sem pai) → [DEV] FT-034 … · [REV] · [VER] · [APR]
│   └── IB Atendimento                 nasce com o 1º item da categoria
│       └── IB [AT-012] <pedido>       nasce na triagem (dono = P.O.); vai à sprint como o IB da fatia
│           └── [ATD] AT-012 <pedido>  nasce quando o item entra numa sprint (dono = quem faz)
└── IB [EP-03] … → IB [FT-031] … → [ESP] / [DEV] …
```

- `elm-sprint.md` §2 e §6: títulos sem o produto; idempotência pelo id gravado no `backlog.md` e, sem id, por
  `titulo_prefixo` com escopo (`Sustentação` no backlog, tipo IB, aceita só se for única; `Manutenção` e
  `<Categoria>` com `pai` = Sustentação; `[AT-012]` com `pai` = IB da categoria). §0: recusa a iteração de backlog
  que já tem uma `Sustentação` que este `backlog.md` não conhece (outro produto) ou mais de um plano de backlog do
  time. Tarefa de Sustentação só nasce na sprint (some "no backlog só ficam as tarefas de Apoio sem sprint"). A
  `sdd-atender`/`sdd-executar` concluem a tarefa **e** o IB do item na mesma confirmação.
- Fatia sem épico: IB `[FT-nnn]` ou item de origem sob a Manutenção, direto ou pelo item original quando dividida.
  O item de origem sem pai vai para a Manutenção e, sem dono, recebe o P.O. (`elm_atualizar_wi(origem, pai,
  iteracao = backlog, dono)`): o `assumir` da `[DEV]` com `iniciar_pai` exige dono no pai (`ewm.py:532-536`), e a
  `sdd-desenvolver` confere isso no Passo 3, antes de gravar `iniciada`. Com outro pai: mantém e avisa. Fatia
  vinculada a atendimento: `elm_ligar(wi = item da fatia, wi_destino = IB do AT, tipo relacionado)`.
- Item de Sustentação triado a partir de um IB ou DF do EWM: esse item é o IB do item (sem IB novo, como na fatia),
  sob o IB da categoria se não tiver pai (com outro pai: mantém e avisa); o título ganha o `[AT-nnn]` pelas opções
  do §9 (renomear · só incluir o prefixo · manter).
- **Sustentação no `sdd.md`** passa a ser "o que não vem de épico": a Manutenção (fatias: mudam o repositório, são do
  Dev, podem ser AFK) e as categorias sem mudança no repositório (Atendimento…). As regras que hoje dizem "Apoio não
  é deste papel" (`sdd-desenvolver:37`) e "nunca AFK" (`sdd-loop:38-39`) valem pelo tipo de id (`AT-`, `IM-`…), não
  pelo nome Sustentação; a Manutenção não entra na tabela de categorias (não tem prefixo de tarefa, série nem pasta
  próprios).
- §9 "sincroniza a sprint": tarefa por fora sem pai, ou com pai Sustentação ou categoria → vira item (id novo, IB
  `[XX-nnn]`, a tarefa passa a filha dele, a `### <Categoria>` nasce se for a primeira); reserva estourada → fica na
  sprint e o P.O. decide pelo Encaixe (some "volta ao backlog do EWM").
- `pa` (`sdd-setup/references/elm-pa.md`): `por-prefixo` `Sustentação ` → `Sustentação`; os IBs de item (`[AT-`,
  `[IM-`…) com a Categoria da Sustentação; a Manutenção com a Categoria que a setup pergunta.
- **Lote da triagem** (`sdd-triar` Passo 5): hoje não roda — o MCP recusa `elm_listar_wi(tipo, estado)` sem
  iteração, dono ou pai (`ewm.py:356`). O filtro passa a pedir a iteração (padrão: o backlog do produto). Ficam fora
  os itens do fluxo por **id** (todo id do `backlog.md`) e por **título exato** (`Sustentação`, `Manutenção`,
  `<Categoria>`), nunca pela palavra inicial — "Infra: certificado vencido" é demanda.

## 4. Quem grava na base — Dev, loop e permissões

- **Requisito** (decisão 16b): quem desenvolve tem push na branch base; a setup avisa (cartão Git do wizard).
- **Gravar na base, para o Dev** (`backlog.md`, bloco Gravar na base): `git fetch` → `git switch <base>` →
  `git pull --ff-only` → grava → commit (pergunta antes) → confere os arquivos (decisão 16a) → push (pergunta) →
  `git fetch` e `git rev-parse <base>` = `git rev-parse origin/<base>`. Push recusado (base protegida, outro Dev
  antes) → `git reset --keep origin/<base>` só desse commit de registro, com "sim" (exceção explícita ao "nunca
  ofereça reset"), e para.
- **`sdd-desenvolver` Passo 4**, nesta ordem: conferências do Passo 3 (inclusive o dono do item pai) → (puxada HITL)
  revisor e verificador → `iniciada` na base com o push conferido → branch de `origin/<base>` → pasta e `status.md` →
  EWM (assumir a `[DEV]`; tarefas que nascem aqui vão ao campo ELM do `status.md`, e a consolidação as leva à linha
  do backlog e à Tarefa ELM da sprint, como hoje). Item 3 ("Backlog: não muda aqui") sai.
- **Dois Devs na mesma fatia:** o push do segundo é recusado e ele vê a fatia `iniciada` na base. A "próxima fatia"
  e as candidatas do loop excluem as `iniciada` e mantêm o filtro "sem `status.md` em branch".
- **Retomada:** a `iniciada` grava o `responsavel` (se estava `—`); só ele retoma uma `iniciada` sem `status.md` em
  branch (sessão interrompida), pelo Passo 4. Outra pessoa vê "iniciada por <login> em <data>, sem branch publicada"
  e para. O painel lista essas fatias; a pré-condição e o Encaixe não as tratam como "não iniciadas".
- **`sdd-desenvolver` Passo 6:** começa conferindo se a base já tem `Fase: pronta` (já registrado → nada a fazer).
  Depois do merge conferido, na base: o `status.md` (agora na base) com `Fase: pronta`, as Lições candidatas, os
  Créditos e o Histórico; `pronta` no backlog e na sprint; commit `<FT> registrar merge`; push. Some o commit
  pós-merge na branch; o merge passa `remover_origem=true` (a branch não guarda mais nada).
- **`sdd-consolidar`:** entrada = `Fase: pronta` no `status.md` da base; lê dali as Lições candidatas e os Créditos;
  deixa de criar a linha da puxada e de gravar a `sprint` dela (já foram gravadas no `iniciar`) — só completa a
  Tarefa ELM dessa linha com os ids do `status.md`.
- **`sdd-loop`:** o orquestrador grava a `iniciada` do lote num commit na base no fim do Passo 1, depois do "sim"
  do lote — só se o checkout principal já está na base e limpo (outra sessão pode estar trabalhando nele);
  senão, pede à pessoa que troque antes das worktrees.
- **Rede de proteção** (pré-condição dos ritos de fechamento, `sdd-planejamento`): corrige só a `iniciada` que
  ficou para trás, lendo os `status.md` das branches. Fatia com PR mergeado e sem `Fase: pronta` na base é listada
  para o Dev fazer o Passo 6 (ninguém mais grava `pronta`).
- **`sdd-status` › Fechar a sessão:** fatia com PR mergeado grava os Créditos no `status.md` da base, pelo Gravar na
  base, nunca na branch.
- **Branch desatualizada** (`sdd-implementar` Passo 5, item 1): ignora só os commits da base que mexem em
  `<produto>/backlog.md`, `<produto>/sprints/**` e `.kiro/specs/<outras fatias>/**`, conferidos de uma vez por
  `git diff --name-only HEAD...origin/<base>` (PRD e ficha novos continuam exigindo a atualização). Pelo mesmo
  critério, atualizar a branch depois da aprovação, quando a base só trouxe esses caminhos, não invalida a aprovação
  (`sdd-desenvolver` Passo 6, item 2) — é o que acontece em projeto com merge fast-forward ou semi-linear no GitLab.
- **`sdd-especificar` Passo 2** e **`sdd-atender`/`sdd-executar`** ao assumir: gravam só a situação na base (exceção
  explícita ao "nada vai à base antes do GATE do PRD").
- **Agentes** (`sdd-setup/assets/agents/papeis.json`, `scripts/gerar_agentes.py`, `scripts/test_gerar_agentes.py`):
  - codificador: `{{PRODUTO}}/**` segue negado; liberar só `{{PRODUTO}}/backlog.md` e `{{PRODUTO}}/sprints/**` — com
    `exclude` no `fs_write` se o Kiro V3 aceitar (conferir com `agent validate`, como em `agentes.md:83`); senão, pela
    lista dos caminhos negados, com teste que falha se `equipe.json`, `acordos.md`, `roadmap.md`, `epicos/`,
    `fatias/`, `sustentacao/` ou `aprendizado/` ficarem graváveis. O orquestrador ganha os mesmos dois caminhos.
  - push da base sai do `push-perigoso` e pergunta, nos dois; passam a ser negados o `git push` sem branch,
    `git push origin`, `*git push* HEAD*` e `*git push* @*` (as skills sempre nomeiam a branch);
    `git reset --keep origin/*` liberado com pergunta.
  - produto: `.kiro/local/sustentacao/**` no lugar de `.kiro/local/apoio/**` e `.kiro/local/atendimentos/**`.
  - `sdd-codificador.md`, `sdd-orquestrador.md`, `sdd-produto.md`, `references/agentes.md`, o wizard ("🔴 nunca … para
    a base | 📐 fixo") e o `sdd.md` ("push nunca para a base", "o Dev não grava na base") passam a dizer: push da
    base só dos registros de situação, com "sim" e a conferência dos arquivos.

## 5. Uma metodologia — Scrumban

O que o sdd chama de "Scrum" já é Scrumban (`sdd.md`: "Sprint é cadência, não contêiner de escopo… fluxo puxado";
`sdd-planejamento`: "A sprint é cadência… Dentro da sprint o fluxo é puxado"). O ramo Kanban só duplica regras
("não há sprint nem encaixe", "a iteração corrente"). Fica um fluxo:

- **Acordos** (`sdd-planejamento` modo inicial, `arquivos.md`): sai a pergunta Scrum × Kanban; o acordo vira
  `Cadência | Scrumban: sprints de <n> semanas (planejamento, review, retrospectiva, virada), fluxo puxado dentro da
  sprint, WIP limitado`. Pergunta-se só a duração (padrão 2 semanas) e o início da sprint 1.
- **`equipe.json`:** sai a chave `cadencia` (`equipe.schema.json`: do `required` e das `properties`; exemplo do
  `arquivos.md`; cabeçalho do `equipe-template.md`).
- **Ramos que somem** ("Kanban → …"): `sdd-desenvolver` (Passo 1 "próxima fatia", Passo 3 item 3, Passo 4 item 4),
  `sdd-triar` (sprint sugerida), `sdd-atender` e `sdd-executar` (assumir sem sprint), `sdd-loop` (Passo 1),
  `sdd-fatiar` ("ou no fluxo Kanban"), `elm-sprint.md` §4 e §6 ("a iteração corrente"), `backlog.md` (colunas
  `sprint` e status do apoio), `arquivos.md` ("Kanban: o mesmo, com a iteração corrente"), `sdd-setup` (cadência na
  pergunta da equipe), descrição da `sdd-planejamento` e `README.md` do power.

## 6. Sem migração — regras antigas que saem

Nenhum projeto usa o power: a 3.4.0 não traz migração nem tabela de compatibilidade (fases antigas no `status.md`,
`2026/03`, `## Apoio`…), e saem as regras de versões anteriores, que só servem a projetos que não existem:

| Onde | O que sai |
|---|---|
| `sdd-fatiar/references/backlog.md` | "backlog antigo sem a coluna → a próxima escrita a acrescenta" (`po`, `pasta`, `ficha`, `creditos`, número solto na `sprint`); as Regras "sem `AT-` (antes da 2.5.0)", "`## Atendimentos` (antes da 3.3.0)" e "`## Fatias — trilha rápida` (antes da 2.3.0)" |
| `sdd-planejamento/assets/equipe.schema.json` · `arquivos.md:66` | `historico[].sprint` inteiro, `horas-lancadas.atendimento`, `reserva-atendimento` (antes da 3.3.0) |
| `sdd-setup/SKILL.md` · `references/wizard.md` | projeto configurado antes da 3.0.0, layout `planejamento/` (2.6.0), `sdd2`/v1, migração das sprints para `sprints/<pai>/` (3.3.0) |
| `sdd-setup/references/elm-pa.md:81` · `sdd-triar` (lote) | `por-prefixo` e filtro `[SUS-` (Sustentação de antes da 3.3.0) |
| `sdd-status/SKILL.md` | backlog de antes da 3.3.0 e `AT-*.md` soltos (Coleta 6); inconsistências "layout antigo", "sprints na raiz", "`## Atendimentos`" e "`ELM pendente` sem chave" |
| `sdd-triar/SKILL.md` | renomear `## Fatias — trilha rápida`; "Backlog com `## Atendimentos` → antes, a migração" |
| `sdd-desenvolver/SKILL.md:64` | seção antiga `## Fatias — trilha rápida` |
| `sdd-consolidar/SKILL.md:98,108` | número solto de `status.md` anterior à migração das sprints; "seção ausente (fatia anterior a esta regra)" |

O histórico de versões do `README.md` do power fica (é registro); só ganha a entrada da 3.4.0.

## 7. Mudanças por arquivo

Cada linha aplica as seções 1–6 ao arquivo.

| Arquivo (em `powers/sdd/skills/`, salvo indicação) | O que muda |
|---|---|
| `sdd-fatiar/references/backlog.md` | formato (seção 2), situações e "Quem escreve o quê" (seção 1), DoR com `elegivel` (âncora nova, DoR única do épico), prioridade, `elm` com rótulo, Gravar na base do Dev (seção 4), regras antigas saem |
| `sdd-planejamento/SKILL.md` | descrição e acordos Scrumban; Previsão (`elegivel`, prioridade + ordem da linha); `planejada`/`planejado` no "ok"; Encaixe (`saiu da sprint`); pré-condição (rede de proteção, `pronta` sem consolidar); review pelo resumo do Status; virada (seção 1); reserva Sustentação + retrabalho; chave; "não está pronto" → "não está entregue" |
| `sdd-planejamento/references/arquivos.md` | formato da sprint (cabeçalho, Origem, Observação, `## Sustentação`, situações ao vivo); acordos Scrumban; `equipe.json` sem `cadencia`; chave; "tarefa assumida" |
| `sdd-planejamento/references/elm-sprint.md` | §0 (Sustentação de outro produto), §2 (títulos, idempotência), §3 (origem sob a Manutenção, com dono), §4, §6 (IB por item; tarefa só na sprint), §9 (tarefa por fora vira item; reserva → Encaixe); Kanban sai |
| `sdd-planejamento/assets/equipe.schema.json` · `equipe-template.md` | sem `cadencia`; chave `<pai>/Sprint <nn>`; `sustentacao` e `reserva-sustentacao`; chaves antigas saem |
| `sdd-desenvolver/SKILL.md` | Passo 1 (DF/IB pela `elm`, base prevalece, retomada pelo responsável, Sustentação por tipo de id); Passo 2 (trilha pela coluna); Passo 3 (`elegivel`/`planejada`, dono do pai, WIP novo); Passo 4 (ordem e base); Passo 5 (roteamento novo); Passo 6 (seção 4, conflito → retrabalho); Kanban sai |
| `sdd-desenvolver/references/status-template.md` | fases HITL/AFK, WIP, conflito no merge, regra "a base prevalece", ELM com rótulos |
| `sdd-implementar/SKILL.md` | Passo 0 (`verificada`, `retrabalho (de: aceita…)`); Passo 5 (branch desatualizada estreita; AFK → `aguardando-aprovacao-pr`); mensagens ("aguardando revisão") |
| `sdd-plano/SKILL.md` · `sdd-revisar/SKILL.md` · `sdd-verificar/SKILL.md` | `aguardando-aprovacao-plano`, `aceita` (HITL), `verificada` (AFK); revisor e verificador da puxada lidos da linha da sprint (o Histórico deixa de ser a fonte) |
| `sdd-loop/SKILL.md` | candidatas `planejada`/`elegivel` não iniciadas; `iniciada` do lote na base; fases 4 e 8 com os nomes novos; WIP; Sustentação por tipo de id; Kanban sai |
| `sdd-consolidar/SKILL.md` · `references/elm-publicar.md` | entrada `pronta` na base; Lições e Créditos da base; sem a linha da puxada; épico `concluido` na última fatia (backlog e Fase do `status.md` do épico, não mais o PRD); "próxima pronta" → próxima planejada; regras antigas saem |
| `sdd-especificar/SKILL.md` | Passo 2 (situação na base; linha nasce se não planejada); Passo 3 (modelo do `status.md` do épico com a Fase); Passo 4 (roteamento pela Fase); Passo 6 (`concluida` + créditos); DoR do épico pela do `backlog.md` |
| `sdd-prd/SKILL.md` · `references/prd-template.md` | Fase `em-revisao`/`aprovado` no `status.md` do épico; GATE do PRD grava no backlog só o `prd`; frontmatter sem `status`; mudança depois de aprovado pela Fase; `elm` com rótulo |
| `sdd-fatiar/SKILL.md` | fatias nascem `nova`/`elegivel` com `origem` e prioridade herdada; Fase `fatiado` no `status.md` do épico (sai o `status: fatiado` do PRD e do backlog); dividir, juntar e cancelar (seção 1); épico cancelado (Fase `cancelado`, Especificação `cancelada`) |
| `sdd-triar/SKILL.md` · `references/ficha.md` | trilha sustentação e categoria; IB por item; `nova`/`elegivel`; épico: `status.md` com Fase `rascunho` na pasta antecipada; `obs` `vinculada a` + `relacionado`; `DF 4567` sem MCP; lote (seção 3); `[GB]` na linha nova da Sustentação; `cancelado`; regras antigas saem |
| `sdd-atender/SKILL.md` · `sdd-executar/SKILL.md` | `em-andamento` ao assumir; IB e tarefa que faltem; concluir tarefa e IB; `sustentacao/`; Kanban sai |
| `sdd-status/SKILL.md` | coleta com a base prevalecendo; painel (elegíveis, iniciadas sem branch, prontas esperando consolidação, WIP novo, Sustentação por categoria, épicos pela Fase do `status.md`); Fechar a sessão depois do merge; inconsistências antigas saem |
| `sdd-iniciar/SKILL.md` | roteamento pelas situações novas e pelo tipo de id; Sustentação |
| `sdd/SKILL.md` · `sdd/references/elm.md` | visão do fluxo e diagramas; tabela "Tarefas no EWM" (IB por item, Manutenção, `[GB]`); vocabulário; "tarefa assumida" |
| `sdd-setup/SKILL.md` · `references/wizard.md` · `references/elm-pa.md` | requisito do push na base (cartão Git); sai a pergunta do produto e a de Scrum × Kanban; tabela Sustentação; `por-prefixo` e Categoria da Manutenção; regras antigas saem |
| `sdd-setup/assets/steering/sdd.md` | seção Sustentação (Manutenção + categorias, regras por tipo de id); Dev na base; vocabulário; commit `2026/Sprint 03: …`; "tarefa assumida" |
| `sdd-setup/assets/agents/*` · `references/agentes.md` · `scripts/gerar_agentes.py` · `scripts/test_gerar_agentes.py` | permissões (seção 4); `elm_backlog` entra no catálogo `elm` do `papeis.json` (hoje escapa das regras dos agentes); textos dos agentes |
| `sdd-setup/assets/workflows/*.workflow.json` · `references/automacoes.md` | fases novas (`verificada`, `aguardando-aprovacao-pr`) |
| `sdd-aprender/SKILL.md` · `sdd-verificar/references/ct-csv.md` · `sdd-entrevistar/SKILL.md` | chave da sprint; créditos; Sustentação |
| `powers/sdd/README.md` · `powers/sdd/plugin.json` · `powers/README.md` | histórico 3.4.0 e textos; descrição; "(21)" skills → 22 |

Fora do escopo (achado de passagem): `mcps/elm/docs/manual-mcp-elm.md:96-107` está atrás da mcp-elm 3.3.5 (nomes de
plano, `Backlog`, linha de base).

## 8. Ordem de execução e versões

1. Formatos (fonte das demais): `backlog.md`, `arquivos.md`, `status-template.md`, `elm-sprint.md`,
   `sdd/references/elm.md`, `assets/steering/sdd.md`, `equipe.schema.json`.
2. Skills pelo fluxo: `sdd-triar`, `sdd-fatiar`, `sdd-planejamento`, `sdd-desenvolver`, `sdd-plano`,
   `sdd-implementar`, `sdd-revisar`, `sdd-verificar`, `sdd-loop`, `sdd-consolidar`, `sdd-especificar`, `sdd-prd`,
   `sdd-atender`, `sdd-executar`, `sdd-status`, `sdd-iniciar`, `sdd`, `sdd-aprender`.
3. `sdd-setup`: `papeis.json` + gerador + teste, `wizard.md`, `elm-pa.md`, agentes, workflows.
4. Remoção das regras antigas (seção 6), num commit próprio.
5. Versão 3.4.0: `metadata.version` das 22 skills, `plugin.json`, `README.md` do power (histórico) e
   `powers/README.md`; o mcp-elm só se for alterado (decisão 20) — aí `pyproject.toml`, manual, wheel e o
   `requires` do `plugin.json`, num commit `mcp-elm 3.4.0: …`.
6. Este documento, com o plano e as discussões (como o da 3.3.0).
7. Commits por área (`sdd 3.4.0: …`), sem trailer de coautoria; exemplos só com nomes genéricos.

## 9. Verificação

- `uv run --with pytest pytest powers/sdd/skills/sdd-setup/scripts`: o codificador e o orquestrador gravam
  `backlog.md` e `sprints/**` e não gravam `equipe.json`, `acordos.md`, `roadmap.md`, `epicos/`, `fatias/`,
  `sustentacao/` nem `aprendizado/`; push da base pergunta; `git push` sem branch, `HEAD` e `@` negados;
  `git reset --keep origin/*` pergunta; `elm_backlog` no catálogo. E `powers/sdd/skills/sdd-status/scripts`
  (créditos, sem mudança).
- Agentes gerados validados no Kiro (`agent validate`, como em `agentes.md:83`) — é o que decide entre `exclude` e
  lista no `fs_write`.
- Validar o `equipe.json` do `arquivos.md` contra o `equipe.schema.json` (`uv run --with jsonschema …`): chave
  `2026/Sprint 03`, sem `cadencia`; e um com `cadencia` ou chave `2026/03` recusado.
- `cd mcps/elm && uv run pytest` — sanidade; se o mcp-elm for alterado (decisão 20), com os casos novos.
- Varredura sem nenhuma ocorrência (fora o histórico do `README.md`):
  `grep -rn "pronta-para-merge\|plano-em-revisao\|mergeada\|→ sprint\|## Apoio\|reserva de apoio\|apoio/\|- <produto>\|Fatias — sem épico\|Kanban\|kanban\|cadencia\|antes da [0-9]\|\[SUS-" powers/sdd`;
  `pronta` só como "mergeada" (e os nomes da decisão 19).
- Ensaio num projeto piloto novo: (a) fatia HITL de `nova` a `concluida` — `iniciada` na base com o push
  confirmado antes da branch, `pronta` na base depois do merge, créditos e lições lidos da base na consolidação —
  e uma AFK por `verificada → aguardando-aprovacao-pr`; (b) push da base recusado (branch protegida) → o commit
  de registro é desfeito e a skill para; (c) dois Devs pedindo a mesma fatia; (d) conflito na hora do merge →
  `retrabalho`; (e) atendimento: IB `[AT-nnn]` na triagem, `[ATD]` ao entrar na sprint, `em-andamento`,
  `concluido` com créditos e o IB concluído; (f) fatia vinculada a atendimento (obs + link `relacionado`);
  (f2) épico: `status.md` com Fase `rascunho` na triagem, `aprovado` no GATE do PRD (pasta na base), `fatiado` no
  GATE do backlog e `concluido` na última fatia, com o backlog indo de `novo` a `concluido` e o PRD sem `status`;
  (g) lote da triagem com a iteração do backlog; (h) virada com item migrado (`migrada para 2026/Sprint 04`) e
  créditos copiados para o backlog; (i) painel e review mostrando elegíveis, iniciadas e prontas.

## 10. Decisões tomadas na execução

Lacunas que a primeira passada pelos arquivos mostrou e que o plano não fechava, resolvidas pelo desenho acima:

| Lacuna | Decisão |
|---|---|
| Virada do épico depois da especificação | a linha da Especificação migra só se não estiver `concluida` ou `cancelada`; a coluna `sprint` do épico acompanha essa linha (épico `iniciado` com a Especificação `concluida` não migra) |
| Épico cancelado com fatia já iniciada | a `sdd-fatiar` não cancela a fatia iniciada sozinha (mostra ao P.O.); a consolidação da última fatia não conclui um épico `cancelado` |
| Cancelar IB ou tarefa no EWM | é manual (o MCP só assume, conclui e reabre): `ELM pendente [<id> cancelar]`, no rodapé da ficha da fatia (não iniciada, dividida ou cancelada) ou no campo ELM da ficha do item de Sustentação |
| Item registrado sem o MCP | a coluna `elm` leva o id sem link (`DF 4567`); o espelhamento e a publicação da sprint tratam "id sem link" como `pendente` |
| Loop sem push ("Push e PR no loop: não") | a `iniciada` do lote é commitada na base e o push vai como comando pronto; o loop espera a publicação antes das worktrees |
| Branch atualizada por rebase (botão do GitLab) | o sha aprovado some e a mudança volta à revisão; o sdd atualiza a branch por merge da base |
| Épico assumido sem sprint aberta | a `sdd-especificar` oferece a `sdd-planejamento` e não começa |
| Coluna `pasta` do épico sem pasta antecipada | o GATE do PRD a preenche no mesmo commit do link `prd` |
| Mensagens de commit | `<id> iniciar` para fatia, épico e item de Sustentação (lote do loop: `FT-031, FT-032 iniciar`; a rede de proteção usa a mesma) e `<FT> registrar merge` |
| `bloqueada-por` na DoR | a dependência em `pronta` ou `concluida` (já na base) ou planejada antes na mesma sprint |
| Permissão do codificador em `<produto>/` | `{{PRODUTO}}/**` negado com `exclude` de `backlog.md` e `sprints/**`, conforme o motor V3 do Kiro; o `agent validate` não confere `permissions`, então a confirmação fica para o ensaio no piloto |
