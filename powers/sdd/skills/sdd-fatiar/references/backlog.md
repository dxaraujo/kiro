# Backlog do produto — `<produto>/backlog.md`

Fonte única dos ids locais (`EP-nn`, `FT-nnn`, `AT-nnn`), do **planejamento** (o que existe, em que ordem, em que sprint) e do
mapeamento com o ELM. Versionado. Só markdown: editado direto, sem arquivo JSON por trás.

**Onde é escrito:** só na **branch base** (direto ou por um PR curto, conforme "Artefatos de produto" no
`sdd.md`) — **nunca numa branch de fatia**, para que fatias em paralelo não disputem o mesmo arquivo. O
andamento de uma fatia (fase, branch, PR) não mora aqui: mora no `status.md` da pasta dela, na branch dela, e o
`sdd-status` o lê de lá.

## Formato

```markdown
# Backlog — Gestão de Acessos

Próximos ids: EP-04 · FT-034 · AT-013
Sustentação: [SUS-2026] [612000](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612000) · Atendimento [612005](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612005)

## Épicos

| id | título | status | prioridade | po | prd | pasta | elm |
|---|---|---|---|---|---|---|---|
| EP-03 | Bloqueio por tentativas de login | fatiado | 1 | ana.souza | [prd](epicos/EP-03-bloqueio-login/prd.md) | [pasta](epicos/EP-03-bloqueio-login/) | [612001](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612001) |

## Fatias — EP-03 Bloqueio por tentativas de login

| id | título | cobre | ficha | bloqueada-por | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas inválidas | HF-01#1.1, HF-01#1.2, REG-01 | [ficha](fatias/FT-031-bloquear-conta.md) | — | M | AFK | 1 | pronta | 3 | joao.lima | — | — | — |

## Fatias — sem épico

| id | título | trilha | origem | ficha | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Atendimentos

| id | título | origem | status | sprint | responsavel | elm | registro | concluida-em |
|---|---|---|---|---|---|---|---|---|
| AT-012 | Extração de contas bloqueadas em setembro | chamado 4521 | aberto | 3 | joao.lima | [ATD] [669380](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/669380) | [AT-012](atendimentos/AT-012-contas-bloqueadas.md) | — |
```

Uma seção `## Fatias — <EP> <título>` por épico, na ordem de prioridade dos épicos, e uma `## Fatias — sem épico`
no fim, e a `## Atendimentos` por último (linhas na ordem dos ids); fatias na ordem de `prioridade`. Célula vazia é `—`. Listas (`cobre`, `bloqueada-por`) separadas por vírgula. Cada fatia é **uma**
linha da tabela — sem quebra de linha nem `|` dentro de célula (troque por `/`).

| Coluna | Valores |
|---|---|
| épico `status` | `rascunho` · `em-revisao` · `aprovado` · `fatiado` · `concluido` · `cancelado` (o mesmo do frontmatter do PRD; publicação no ELM fica no `elm` do PRD, não no status) · `rascunho` com `prd` `—` = registrado pela `sdd-triar`, PRD ainda não escrito ("a descobrir" no roadmap) |
| épico `po` | login do P.O. do épico (padrão: o P.O. ativo do `equipe.json`); é o responsável do épico no EWM e quem aprova o PRD; backlog antigo sem a coluna → a próxima escrita a acrescenta com o P.O. ativo |
| épico `pasta` | `[pasta](epicos/<EP>-<slug>/)` (criada pela `sdd-triar`) ou `—`; backlog antigo sem a coluna → a próxima escrita a acrescenta |
| `trilha` | só nas fatias sem épico: `padrão` · `rápida` · `direta` (fatia de épico é sempre padrão) |
| fatia `origem` | só nas fatias sem épico: o item ou o pedido que a originou — `DF 4567`, `IB 611`, `AT-012`, `pedido: <resumo>` |
| `ficha` | toda fatia: `[ficha](fatias/FT-<nnn>-<slug>.md)` — formato por trilha na `sdd-triar`, `references/ficha.md` (sem épico: escrita pela `sdd-triar`; de épico: pela `sdd-fatiar`). Backlog antigo com `—` ou sem a coluna → a fatia fica `backlog` com `falta: ficha` até alguém escrevê-la |
| `cobre` | `HF-nn#c.c` (cenário) e `REG-nn` do PRD do épico; não existe nas fatias sem épico (os cenários da padrão ficam na ficha, `C<n>`) |
| fatia `obs` | texto livre; convenções: `falta: <…>` (o que impede a Definition of Ready), `substituida-por FT-…`, o motivo do cancelamento |
| `tamanho` | `P` · `M` · `G` |
| `modo` | `AFK` · `HITL` (padrão e rápida) · `—` (direta: feita na sessão da pessoa) |
| fatia `status` | `backlog` → `pronta` (passou na Definition of Ready) → `concluida`; desvios `dividida` (`obs`: `substituida-por FT-…`), `cancelada` (`obs`: motivo). "Em andamento" não é gravado: é a fatia que tem `status.md` numa branch |
| `sprint` | número da sprint (`sdd-planejamento`) ou `—`; no Kanban, `—` |
| `elm` | `—`, `pendente` (registrado sem o power `elm`; a `sdd-elm` cria depois) ou `[<id>](<url>)`; tarefas do EWM em seguida, `<prefixo> [<id>](<url>)`, separadas por ` · ` (gravado pela `sdd-elm`) |
| `concluida-em` | data `AAAA-MM-DD` ou `—` |
| atendimento `status` | `backlog` (sem sprint aberta) · `aberto` (na sprint ou na iteração corrente do Kanban) · `concluido` · `cancelado` |
| atendimento `origem` | chamado, e-mail, `DF 4567`, `IB 615` ou `pedido` |
| atendimento `registro` | `[AT-<nnn>](atendimentos/AT-<nnn>-<slug>.md)` |
| linha `Sustentação:` | épico de Sustentação do ano e o IB `Atendimento` filho dele (pais do que não nasce de PRD); `—` até a `sdd-elm` criá-los |

## Quem escreve o quê

| Transição | Skill |
|---|---|
| épico registrado (`rascunho`, `prd` `—`, `po`, `pasta`) | `sdd-triar` |
| épico `aprovado` e `prd` (no GATE do PRD; antes, o estado mora no `prd.md` da pasta de trabalho) | `sdd-prd` |
| épico `fatiado` (GATE do backlog) | `sdd-fatiar` |
| épico `concluido` (última fatia concluída) | `sdd-consolidar` |
| épico `cancelado` | o P.O., pela `sdd-fatiar` (refinamento) |
| fatias criadas, divididas, juntadas, canceladas, fichas das fatias de épico · `pronta` (DoR conferida) | `sdd-fatiar` |
| `sprint`, `responsavel`, prioridade · `pronta` (DoR conferida de novo no planejamento) · encaixe durante a sprint | `sdd-planejamento` |
| fatia sem épico (padrão, rápida, direta), ficha e `falta:` em `obs` | `sdd-triar` (na base) |
| atendimento registrado (`AT-nnn`, `backlog`/`aberto`, `sprint`, `responsavel`, registro) | `sdd-triar` (na base) |
| atendimento `concluido`, `concluida-em` | `sdd-atender` (na base) |
| `concluida`, `concluida-em` | `sdd-consolidar` (depois do merge, na base) |
| linha `Sustentação:` | `sdd-elm` (modo backlog) |
| `elm` (ids e urls) | `sdd-elm` |

## Definition of Ready (o que faz uma fatia `pronta`)

A única do fluxo — triagem, fatiamento, planejamento e `sdd-desenvolver` conferem por aqui.

| Trilha | Pronta quando |
|---|---|
| épico (para a `sdd-prd`) | descrição mínima — o problema, quem pede, o resultado esperado — e `po` preenchido |
| padrão de épico | ficha com Objetivo, Cobre e Como verificar; cenários de aceite em `cobre` num PRD `aprovado`/`fatiado`; `bloqueada-por` concluídas, ou planejadas na mesma sprint antes dela (ela só **começa** quando o que precisa está na base) |
| padrão sem épico | ficha `aprovada por` o P.O., com cenários `C<n>` |
| rápida | ficha com o atual (com evidência), o esperado (com fonte), o que não muda e como verificar; sem regra nova; tamanho ≤ M |
| direta | ficha com pronto quando, como verificar e não muda — uma linha cada; sem regra nova; tamanho P |
| todas | a ficha existe no caminho da coluna `ficha`; nenhuma decisão bloqueante `em aberto` (`decisoes.md` ou ficha); tamanho ≤ G; modo declarado (AFK/HITL; direta `—`); cabe numa janela de contexto |

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
4. **Publicar:** push direto ou PR curto, conforme "Artefatos de produto" no `sdd.md`, com o "sim" da pessoa
   (agente sem push → entregue o comando pronto; PR curto → diga o nome da branch e o link). Conflito de id no
   push → a regra de conflito abaixo.
5. Ao terminar, ofereça voltar à branch anterior.

## Regras

- Ids nunca são reaproveitados nem renumerados; "Próximos ids" só cresce.
- Backlog sem `AT-` em "Próximos ids" (antes da 2.5.0): o próximo é o maior entre o `Próximo:` do antigo
  `<produto>/atendimentos/README.md` e os `AT-*.md` existentes, mais um; a próxima escrita da `sdd-triar` acrescenta
  o `AT-` e a seção `## Atendimentos` (com os AT abertos do README) e deixa de gravar no README.
- Backlog com a seção antiga `## Fatias — trilha rápida` (antes da 2.3.0): leia as linhas como `trilha` `rápida` e
  `ficha` `—`; a próxima escrita da `sdd-triar` renomeia a seção e acrescenta as colunas, sem perder linha.
- Antes de gravar: `git switch <base>` e `git pull --ff-only`; depois, commit pequeno só com ele quando não houver
  outro artefato de produto junto. Push ou PR curto: com o "sim" da pessoa, como diz "Artefatos de produto" no `sdd.md`.
- Conflito no `backlog.md`: mantenha o remoto e reaplique só a sua mudança, linha a linha (cada fatia é uma linha).
  Nunca resolva descartando o lado remoto.
