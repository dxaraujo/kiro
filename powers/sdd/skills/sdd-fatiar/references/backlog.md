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

## Fatias — trilha rápida

| id | título | origem | tamanho | modo | prioridade | status | sprint | responsavel | elm | concluida-em | obs |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

Uma seção `## Fatias — <EP> <título>` por épico, na ordem de prioridade dos épicos; linhas na ordem de
`prioridade`. Célula vazia é `—`. Listas (`cobre`, `bloqueada-por`) separadas por vírgula. Cada fatia é **uma**
linha da tabela — sem quebra de linha nem `|` dentro de célula (troque por `/`).

| Coluna | Valores |
|---|---|
| épico `status` | `rascunho` · `em-revisao` · `aprovado` · `fatiado` · `concluido` · `cancelado` (o mesmo do frontmatter do PRD; publicação no ELM fica no `elm` do PRD, não no status) |
| fatia `origem` | só na trilha rápida: o item que a originou sem PRD — `DF 4567`, `IB 611`, `pedido: <resumo>` |
| `cobre` | `HF-nn#c.c` (cenário) e `REG-nn` do PRD do épico; não existe na trilha rápida |
| `tamanho` | `P` · `M` · `G` |
| `modo` | `AFK` · `HITL` |
| fatia `status` | `backlog` → `pronta` (passou na Definition of Ready) → `concluida`; desvios `dividida` (`obs`: `substituida-por FT-…`), `cancelada` (`obs`: motivo). "Em andamento" não é gravado: é a fatia que tem `status.md` numa branch |
| `sprint` | número da sprint (`sdd-planejamento`) ou `—`; no Kanban, `—` |
| `elm` | `—` ou `[<id>](<url>)`; tarefas do EWM em seguida, `<prefixo> [<id>](<url>)`, separadas por ` · ` (gravado pela `sdd-elm`) |
| `concluida-em` | data `AAAA-MM-DD` ou `—` |
| linha `Sustentação:` | épico de Sustentação do ano e o IB `Atendimento` filho dele (pais do que não nasce de PRD); `—` até a `sdd-elm` criá-los |

## Quem escreve o quê

| Transição | Skill |
|---|---|
| épico criado / status do PRD | `sdd-prd` |
| fatias criadas, divididas, juntadas, canceladas · `pronta` (DoR conferida) | `sdd-fatiar` |
| `sprint`, `responsavel`, prioridade · `pronta` (DoR conferida de novo no planejamento) | `sdd-planejamento` |
| fatia da trilha rápida (com `origem`, sem épico) | `sdd-iniciar` (antes de criar a branch, na base) |
| `concluida`, `concluida-em` | `sdd-consolidar` (depois do merge, na base) |
| linha `Sustentação:` | `sdd-elm` (modo backlog) |
| `elm` (ids e urls) | `sdd-elm` |

## Definition of Ready (o que faz uma fatia `pronta`)

Cenários de aceite definidos (`cobre`) num PRD `aprovado` (ou `fatiado`) — ou, na trilha rápida, o comportamento
esperado claro; nenhuma decisão bloqueante `em aberto`; dependências concluídas ou planejadas antes; tamanho ≤ G;
modo AFK/HITL declarado. Deixou de valer (PRD reaberto, decisão nova em aberto) → volta a `backlog`.

## Regras

- Ids nunca são reaproveitados nem renumerados; "Próximos ids" só cresce.
- Antes de gravar: `git switch <base>` e `git pull --ff-only`; depois, commit pequeno só com ele quando não houver
  outro artefato de produto junto. Push ou PR curto: com o "sim" da pessoa, como diz "Artefatos de produto" no `sdd.md`.
- Conflito no `backlog.md`: mantenha o remoto e reaplique só a sua mudança, linha a linha (cada fatia é uma linha).
  Nunca resolva descartando o lado remoto.
