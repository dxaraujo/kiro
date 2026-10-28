# Backlog do produto — `<produto>/backlog.md`

Fonte única dos ids locais (`EP-nn`, `FT-nnn` e os de Apoio — `AT-nnn`, `IM-nnn`… uma série por categoria), do **planejamento** (o que existe, em que ordem, em que sprint) e do
mapeamento com o ELM. Versionado. Só markdown: editado direto, sem arquivo JSON por trás.

**Onde é escrito:** só na **branch base**, com commit direto nela — **nunca numa branch de fatia**, para que fatias em paralelo não disputem o mesmo arquivo. O
andamento de uma fatia (fase, branch, PR) não mora aqui: mora no `status.md` da pasta dela, na branch dela, e o
`sdd-status` o lê de lá.

## Formato

```markdown
# Backlog — Gestão de Acessos

Próximos ids: EP-04 · FT-034 · AT-013 · IM-004 · BD-001 · IN-002 · OP-001 · EX-001
Sustentação: [612000](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612000) · Backlog [GB] [612006](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612006)

## Épicos

| id | título | status | prioridade | po | prd | pasta | elm | creditos |
|---|---|---|---|---|---|---|---|---|
| EP-03 | Bloqueio por tentativas de login | fatiado | 1 | ana.souza | [prd](epicos/EP-03-bloqueio-login/prd.md) | [pasta](epicos/EP-03-bloqueio-login/) | [612001](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612001) | 18.40 |

## Fatias — EP-03 Bloqueio por tentativas de login

| id | título | cobre | ficha | bloqueada-por | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | creditos | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas inválidas | HF-01#1.1, HF-01#1.2, REG-01 | [ficha](fatias/FT-031-bloquear-conta.md) | — | M | AFK | 1 | pronta | 2026/03 | joao.lima | [612010](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612010) · DEV [612011](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612011) | — | — | — |

## Fatias — sem épico

| id | título | trilha | origem | ficha | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | creditos | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Apoio

| id | categoria | título | origem | status | sprint | responsavel | elm | registro | concluida-em | creditos |
|---|---|---|---|---|---|---|---|---|---|---|
| AT-012 | Atendimento | Extração de contas bloqueadas em setembro | chamado 4521 | aberto | 2026/03 | joao.lima | [ATD] [669380](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/669380) | [AT-012](apoio/atendimento/AT-012-contas-bloqueadas.md) | — | — |
| IM-003 | Implantação | Subir a versão 1.4 em produção | pedido | aberto | 2026/03 | ana.souza | [IMPL] [669390](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/669390) | [IM-003](apoio/implantacao/IM-003-versao-1-4.md) | — | — |
```

Uma seção `## Fatias — <EP> <título>` por épico, na ordem de prioridade dos épicos, e uma `## Fatias — sem épico`
no fim, e a `## Apoio` por último (linhas na ordem dos ids, agrupadas por categoria); fatias na ordem de `prioridade`. Célula vazia é `—`. Listas (`cobre`, `bloqueada-por`) separadas por vírgula. Cada fatia é **uma**
linha da tabela — sem quebra de linha nem `|` dentro de célula (troque por `/`).

| Coluna | Valores |
|---|---|
| épico `status` | `rascunho` · `em-revisao` · `aprovado` · `fatiado` · `concluido` · `cancelado` (o mesmo do frontmatter do PRD; publicação no ELM fica no `elm` do PRD, não no status) · `rascunho` com `prd` `—` = registrado pela `sdd-triar`, PRD ainda não escrito ("a descobrir" no roadmap) |
| épico `po` | login do P.O. do épico (padrão: o P.O. ativo do `equipe.json`); é o responsável do épico no EWM e quem aprova o PRD |
| épico `pasta` | `[pasta](epicos/<EP>-<slug>/)` (criada pela `sdd-triar`) ou `—` |
| `trilha` | só nas fatias sem épico: `padrão` · `rápida` (fatia de épico é sempre padrão) |
| fatia `origem` | só nas fatias sem épico: o item ou o pedido que a originou — `DF 4567`, `IB 611`, `AT-012`, `pedido: <resumo>` |
| `ficha` | toda fatia: `[ficha](fatias/FT-<nnn>-<slug>.md)` — formato por trilha na `sdd-triar`, `references/ficha.md` (sem épico: escrita pela `sdd-triar`; de épico: pela `sdd-fatiar`) |
| `cobre` | `HF-nn#c.c` (cenário) e `REG-nn` do PRD do épico; não existe nas fatias sem épico (os cenários da padrão ficam na ficha, `C<n>`) |
| fatia `obs` | texto livre; convenções: `falta: <…>` (o que impede a Definition of Ready), `substituida-por FT-…`, o motivo do cancelamento |
| `tamanho` | `P` · `M` · `G` |
| `modo` | `AFK` · `HITL` — proposto na triagem ou no fatiamento (critérios da `sdd-fatiar`); o modo final é gravado pela `sdd-planejamento` quando a fatia ganha responsável, pela senioridade dele (Júnior → `HITL` · Pleno → os critérios · Sênior → `AFK` por padrão) |
| fatia `status` | `backlog` → `pronta` (passou na Definition of Ready) → `concluida`; desvios `dividida` (`obs`: `substituida-por FT-…`), `cancelada` (`obs`: motivo). "Em andamento" não é gravado: é a fatia que tem `status.md` numa branch |
| `creditos` | créditos do Kiro do item: soma das linhas de créditos do `status.md` da fatia, do `status.md` do épico (a `[ESP]`) ou da ficha do AT, copiada do `sprint-<nn>.md` na virada da sprint (`sdd-planejamento`; a conclusão grava só na sprint); `—` antes |
| `sprint` | chave da sprint `<pai>/<nn>` (`2026/03`: iteração pai do EWM e número dentro dela — [arquivos.md](../../sdd-planejamento/references/arquivos.md#sprintspaisprint-nnmd)) (`sdd-planejamento`) ou `—`; no Kanban, `—` |
| `elm` | o item no EWM — o backlog do EWM é a cópia deste arquivo: nasce no backlog do produto ao registrar (triagem, GATE do backlog) e muda de iteração ao entrar na sprint ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md)) —: `[<id>](<url>)`, `pendente` (registrado sem o MCP `elm`; criado depois) ou `—` (sem ELM); tarefas do EWM em seguida, `<prefixo> [<id>](<url>)`, separadas por ` · ` (gravadas na publicação da sprint, §4) |
| `concluida-em` | data `AAAA-MM-DD` ou `—` |
| apoio `categoria` | uma das categorias da tabela **Apoio** do `sdd.md` (padrão: Atendimento `[ATD]` `AT-` · Implantação `[IMPL]` `IM-` · Banco de dados `[BD]` `BD-` · Infra `[INF]` `IN-` · Operação `[OPE]` `OP-` · Apoio a outros times `[EXT]` `EX-`); o id é da série da categoria. Não existe item nem tarefa "de Apoio" genérica: Apoio é só o nome do conjunto |
| apoio `status` | `backlog` (sem sprint aberta) · `aberto` (na sprint ou na iteração corrente do Kanban) · `concluido` · `cancelado` |
| apoio `origem` | chamado, e-mail, `DF 4567`, `IB 615`, `pedido` ou `EWM <id>` (tarefa criada direto no EWM e trazida para a sprint — [elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §9) |
| apoio `registro` | `[<ID>](apoio/<pasta>/<ID>-<slug>.md)` — a ficha do item, na pasta da categoria (tabela **Apoio** do `sdd.md`) (formato na [`sdd-atender`](../../sdd-atender/SKILL.md#registro); o mesmo para toda categoria) |
| linha `Sustentação:` | o IB `Sustentação - <produto>`, um por produto (pai dos IBs de categoria do Apoio e do que não nasce de PRD), a tarefa `[GB] Gerenciamento do backlog` da iteração pai atual (commits da triagem) e os IBs de categoria, cada um gravado quando nasce com o primeiro item da categoria (`Sustentação: <id> · Backlog [GB] <id> · Atendimento <id> · Operação <id>`); `—` até a primeira triagem (ou a configuração do backlog do EWM) criar o IB, que fica no backlog do EWM; a `[GB]` nasce na primeira sprint de cada pai. Pai novo (virada para `2027`) → só a `[GB]` é trocada pela do pai novo ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §2) |

## Quem escreve o quê

| Transição | Skill |
|---|---|
| épico registrado (`rascunho`, `prd` `—`, `po`, `pasta`) | `sdd-triar` |
| épico `aprovado` e `prd` (no GATE do PRD; antes, o estado mora no `prd.md` da pasta de trabalho) | `sdd-prd` |
| épico `fatiado` (GATE do backlog) | `sdd-fatiar` |
| épico `concluido` (última fatia concluída) | `sdd-consolidar` |
| épico `cancelado` | o P.O., pela `sdd-fatiar` (refinamento) |
| fatias criadas, divididas, juntadas, canceladas, fichas das fatias de épico · `pronta` (DoR conferida) | `sdd-fatiar` |
| `sprint`, `responsavel`, `modo` final (pela senioridade), prioridade · `pronta` (DoR conferida de novo no planejamento) · encaixe durante a sprint | `sdd-planejamento` |
| fatia sem épico (padrão, rápida), ficha e `falta:` em `obs` | `sdd-triar` (na base) |
| apoio registrado (id da categoria, `backlog`/`aberto`, `sprint`, `responsavel`, registro) | `sdd-triar` (na base); tarefa trazida do EWM: `sdd-planejamento` (§9 do `elm-sprint.md`) |
| apoio `concluido`, `concluida-em` | `sdd-atender` (Atendimento) · `sdd-executar` (demais categorias) (na base) |
| `concluida`, `concluida-em` | `sdd-consolidar` (depois do merge, na base) |
| linha `Sustentação:` | `sdd-triar` ou a setup (o IB), publicação da sprint (`[GB]`, inclusive a do pai novo) ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §2); o IB de categoria: quem cria o primeiro item dela pelo §6 (`sdd-triar`, sincroniza a sprint, Encaixe, publicação da sprint, ou `sdd-atender`/`sdd-executar` com o item `pendente`) |
| `elm` (ids e urls) | `sdd-triar` (épico, fatia sem épico, tarefas de Apoio), `sdd-fatiar` (IB das fatias de épico), publicação da sprint (tarefas e o que estava `pendente`), `sdd-atender`/`sdd-executar` (a tarefa de Apoio criada a partir de `pendente`) ([elm-sprint.md](../../sdd-planejamento/references/elm-sprint.md) §2–6) |

## Definition of Ready (o que faz uma fatia `pronta`)

A única do fluxo — triagem, fatiamento, planejamento e `sdd-desenvolver` conferem por aqui.

| Trilha | Pronta quando |
|---|---|
| épico (para a `sdd-prd`) | descrição mínima — o problema, quem pede, o resultado esperado — e `po` preenchido |
| padrão de épico | ficha com Objetivo, Cobre e Como verificar; cenários de aceite em `cobre` num PRD `aprovado`/`fatiado`; `bloqueada-por` concluídas, ou planejadas na mesma sprint antes dela (ela só **começa** quando o que precisa está na base) |
| padrão sem épico | ficha `aprovada por` o P.O., com cenários `C<n>` |
| rápida | ficha com o atual (com evidência), o esperado (com fonte), o que não muda e como verificar; sem regra nova; tamanho ≤ M |
| todas | a ficha existe no caminho da coluna `ficha`; nenhuma decisão bloqueante `em aberto` (`decisoes.md` ou ficha); tamanho ≤ G; modo declarado (AFK/HITL); cabe numa janela de contexto |

Deixou de valer (PRD reaberto, decisão nova em aberto) → volta a `backlog`.

## Gravar na base

O bloco único para todo artefato de produto (`backlog.md`, fichas, PRD, `sprint-<nn>.md`, registro de AT, glossário,
ADRs, lições, `sdd.md` Regras aprendidas). As skills citam este bloco em vez de repetir:

1. **Base:** fora dela → "Troco para `<base>`? (sim)" — sem "sim", pare; árvore com alterações não commitadas →
   avise e pare (nunca ofereça descartar, `stash` ou `reset`). Na base: `git pull --ff-only`; falhou (divergiu) →
   avise e pare, sem merge nem rebase. Base sem upstream (repositório só local, ou branch nunca publicada) →
   `git fetch` basta, e diga que o registro fica só local até alguém publicar.
2. **Grave** só o que a skill manda.
3. **Commit** pequeno, só com o que gravou, mensagem no padrão do `sdd.md`.
4. **Publicar:** push direto na base, com o "sim" da pessoa (agente sem push → entregue o comando pronto).
   Conflito de id no push → a regra de conflito abaixo.
5. Ao terminar, ofereça voltar à branch anterior.

## Regras

- Ids nunca são reaproveitados nem renumerados; "Próximos ids" só cresce.
- Antes de gravar: `git switch <base>` e `git pull --ff-only`; depois, commit pequeno só com ele quando não houver
  outro artefato de produto junto. Push: com o "sim" da pessoa.
- Conflito no `backlog.md`: mantenha o remoto e reaplique só a sua mudança, linha a linha (cada fatia é uma linha).
  Nunca resolva descartando o lado remoto.
