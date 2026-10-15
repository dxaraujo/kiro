# Backlog do produto — `<produto>/backlog.md`

Fonte única dos ids locais (`EP-nn`, `FT-nnn`), do **planejamento** (o que existe, em que ordem, em que sprint) e do
mapeamento com o ELM. Versionado. Só markdown: editado direto, sem arquivo JSON por trás.

**Onde é escrito:** só na **branch base** (direto ou por um PR curto, conforme "Artefatos de produto" no
`sdd.md`) — **nunca numa branch de fatia**, para que fatias em paralelo não disputem o mesmo arquivo. O
andamento de uma fatia (fase, branch, PR) não mora aqui: mora no `status.md` da pasta dela, na branch dela, e o
`sdd-status` o lê de lá.

## Formato

```markdown
# Backlog — Gestão de Acessos

Próximos ids: EP-04 · FT-034
Sustentação: [SUS-2026] [612000](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612000) · Atendimento [612005](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612005)

## Épicos

| id | título | status | prioridade | prd | elm |
|---|---|---|---|---|---|
| EP-03 | Bloqueio por tentativas de login | fatiado | 1 | [prd](epicos/EP-03-bloqueio-login/prd.md) | [612001](https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612001) |

## Fatias — EP-03 Bloqueio por tentativas de login

| id | título | cobre | bloqueada-por | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas inválidas | HF-01#1.1, HF-01#1.2, REG-01 | — | M | AFK | 1 | pronta | 3 | joao.lima | — | — | — |

## Fatias — sem épico

| id | título | trilha | origem | ficha | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

Uma seção `## Fatias — <EP> <título>` por épico, na ordem de prioridade dos épicos, e uma `## Fatias — sem épico`
no fim; linhas na ordem de `prioridade`. Célula vazia é `—`. Listas (`cobre`, `bloqueada-por`) separadas por vírgula. Cada fatia é **uma**
linha da tabela — sem quebra de linha nem `|` dentro de célula (troque por `/`).

| Coluna | Valores |
|---|---|
| épico `status` | `rascunho` · `em-revisao` · `aprovado` · `fatiado` · `concluido` · `cancelado` (o mesmo do frontmatter do PRD; publicação no ELM fica no `elm` do PRD, não no status) · `rascunho` com `prd` `—` = registrado pela `sdd-triar`, PRD ainda não escrito ("a descobrir" no roadmap) |
| `trilha` | só nas fatias sem épico: `padrão` · `rápida` · `direta` (fatia de épico é sempre padrão) |
| fatia `origem` | só nas fatias sem épico: o item ou o pedido que a originou — `DF 4567`, `IB 611`, `AT-012`, `pedido: <resumo>` |
| `ficha` | só nas fatias sem épico: `[ficha](fatias/FT-<nnn>-<slug>.md)` ou `—` — obrigatória na padrão (formato na `sdd-triar`, `references/ficha.md`) |
| `cobre` | `HF-nn#c.c` (cenário) e `REG-nn` do PRD do épico; não existe nas fatias sem épico (os cenários da padrão ficam na ficha, `C<n>`) |
| fatia `obs` | texto livre; convenções: `falta: <…>` (o que impede a Definition of Ready), `substituida-por FT-…`, o motivo do cancelamento |
| `tamanho` | `P` · `M` · `G` |
| `modo` | `AFK` · `HITL` |
| fatia `status` | `backlog` → `pronta` (passou na Definition of Ready) → `concluida`; desvios `dividida` (`obs`: `substituida-por FT-…`), `cancelada` (`obs`: motivo). "Em andamento" não é gravado: é a fatia que tem `status.md` numa branch |
| `sprint` | número da sprint (`sdd-planejamento`) ou `—`; no Kanban, `—` |
| `elm` | `—`, `pendente` (registrado sem o MCP; a `sdd-elm` cria depois) ou `[<id>](<url>)`; tarefas do EWM em seguida, `<prefixo> [<id>](<url>)`, separadas por ` · ` (gravado pela `sdd-elm`) |
| `concluida-em` | data `AAAA-MM-DD` ou `—` |
| linha `Sustentação:` | épico de Sustentação do ano e o IB `Atendimento` filho dele (pais do que não nasce de PRD); `—` até a `sdd-elm` criá-los |

## Quem escreve o quê

| Transição | Skill |
|---|---|
| épico registrado (`rascunho`, `prd` `—`) | `sdd-triar` |
| status do PRD | `sdd-prd` |
| fatias criadas, divididas, juntadas, canceladas · `pronta` (DoR conferida) | `sdd-fatiar` |
| `sprint`, `responsavel`, prioridade · `pronta` (DoR conferida de novo no planejamento) · encaixe durante a sprint | `sdd-planejamento` |
| fatia sem épico (padrão, rápida, direta), ficha e `falta:` em `obs` | `sdd-triar` (na base) |
| `concluida`, `concluida-em` | `sdd-consolidar` (depois do merge, na base) |
| linha `Sustentação:` | `sdd-elm` (modo backlog) |
| `elm` (ids e urls) | `sdd-elm` |

## Definition of Ready (o que faz uma fatia `pronta`)

Cenários de aceite definidos (`cobre`) num PRD `aprovado` (ou `fatiado`) — ou, na fatia sem épico: padrão com a
ficha aprovada pelo P.O.; rápida com o comportamento esperado claro, sem regra nova e tamanho ≤ M; direta com o
pedido numa frase e tamanho P; nenhuma decisão bloqueante `em aberto`; dependências concluídas ou planejadas antes; tamanho ≤ G;
modo AFK/HITL declarado. Deixou de valer (PRD reaberto, decisão nova em aberto) → volta a `backlog`.

## Regras

- Ids nunca são reaproveitados nem renumerados; "Próximos ids" só cresce.
- Backlog com a seção antiga `## Fatias — trilha rápida` (antes da 2.3.0): leia as linhas como `trilha` `rápida` e
  `ficha` `—`; a próxima escrita da `sdd-triar` renomeia a seção e acrescenta as colunas, sem perder linha.
- Antes de gravar: `git switch <base>` e `git pull --ff-only`; depois, commit pequeno só com ele quando não houver
  outro artefato de produto junto. Push ou PR curto: com o "sim" da pessoa, como diz "Artefatos de produto" no `sdd.md`.
- Conflito no `backlog.md`: mantenha o remoto e reaplique só a sua mudança, linha a linha (cada fatia é uma linha).
  Nunca resolva descartando o lado remoto.
