# Backlog do produto — `<produto>/backlog.json`

Fonte única dos ids locais (`EP-nn`, `FT-nnn`), do **planejamento** (o que existe, em que ordem, em que sprint) e do
mapeamento com o ELM. Versionado. `backlog.md` é **gerado** a partir dele (nunca editado à mão).

**Onde é escrito:** só na **branch base** (direto ou por um PR curto, conforme "Artefatos de produto" no
`sdd2.md`) — **nunca numa branch de fatia**, para que fatias em paralelo não disputem o mesmo arquivo. O
andamento de uma fatia (fase, branch, PR) não mora aqui: mora no `status.md` da pasta dela, na branch dela, e o
`sdd2-status` o lê de lá.

## Formato

```json
{
  "projeto": "Gestão de Acessos",
  "proximo": { "EP": 4, "FT": 34 },
  "epicos": [
    {
      "id": "EP-03",
      "titulo": "Bloqueio por tentativas de login",
      "status": "fatiado",
      "prioridade": 1,
      "prd": "<produto>/epicos/EP-03-bloqueio-login/prd.md",
      "elm": { "id": "612001", "url": "https://elm.exemplo/ccm/resource/itemName/com.ibm.team.workitem.WorkItem/612001" }
    }
  ],
  "fatias": [
    {
      "id": "FT-031",
      "epico": "EP-03",
      "origem": null,
      "titulo": "Bloquear a conta após 3 tentativas inválidas",
      "cobre": ["HF-01#1.1", "HF-01#1.2", "REG-01"],
      "bloqueada-por": [],
      "tamanho": "M",
      "modo": "AFK",
      "prioridade": 1,
      "status": "pronta",
      "sprint": 3,
      "responsavel": "joao.lima",
      "elm": null,
      "concluida-em": null
    }
  ]
}
```

| Campo | Valores |
|---|---|
| épico `status` | `rascunho` · `em-revisao` · `aprovado` · `fatiado` · `concluido` · `cancelado` (o mesmo do frontmatter do PRD; publicação no ELM fica no `elm` do PRD, não no status) |
| fatia `origem` | `null` (veio de um PRD) ou o item que a originou sem PRD: `"DF 4567"`, `"IB 611"`, `"pedido: <resumo>"` (trilha rápida) |
| `cobre` | `HF-nn#c.c` (cenário) e `REG-nn` do PRD do épico; vazio só na trilha rápida |
| `tamanho` | `P` · `M` · `G` |
| `modo` | `AFK` · `HITL` |
| fatia `status` | `backlog` → `pronta` (passou na Definition of Ready) → `concluida`; desvios `dividida` (+ `substituida-por`), `cancelada` (+ `motivo`). "Em andamento" não é gravado: é a fatia que tem `status.md` numa branch |
| `sprint` | número da sprint (`sdd2-planejamento`) ou `null`; no Kanban, `null` |
| `elm` | `null` ou `{ "id", "url", "tarefas": { "<prefixo>": { "id", "url" } } }` (gravado pela `sdd2-elm`) |

## Quem escreve o quê

| Transição | Skill |
|---|---|
| épico criado / status do PRD | `sdd2-prd` |
| fatias criadas, divididas, juntadas, canceladas · `pronta` (DoR conferida) | `sdd2-fatiar` |
| `sprint`, `responsavel`, prioridade · `pronta` (DoR conferida de novo no planejamento) | `sdd2-planejamento` |
| `concluida`, `concluida-em` | `sdd2-consolidar` (depois do merge, na base) |
| `elm` (ids e urls) | `sdd2-elm` |

## Definition of Ready (o que faz uma fatia `pronta`)

Cenários de aceite definidos (`cobre`) num PRD `aprovado` (ou `fatiado`) — ou, na trilha rápida, o comportamento
esperado claro; nenhuma decisão bloqueante `em aberto`; dependências concluídas ou planejadas antes; tamanho ≤ G;
modo AFK/HITL declarado. Deixou de valer (PRD reaberto, decisão nova em aberto) → volta a `backlog`.

## Regras

- Ids nunca são reaproveitados nem renumerados; `proximo` só cresce.
- Antes de gravar: `git switch <base>` e `git pull --ff-only`; depois, commit pequeno só com ele (e o
  `backlog.md`) quando não houver outro artefato de produto junto.
- Conflito no `backlog.json`: mantenha o remoto e reaplique só a sua mudança, campo a campo. Nunca resolva
  descartando o lado remoto.
- `backlog.md` é regenerado: tabela por épico (**FT | Título | Tam. | Modo | Status | Sprint | Responsável | ELM**),
  na ordem de prioridade, seguida das fatias de trilha rápida.
