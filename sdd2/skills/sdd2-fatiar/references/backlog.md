# Backlog do produto — `.kiro/produto/backlog.json`

Fonte única dos ids locais (`EP-nn`, `FT-nnn`), do estado de alto nível de cada item e do mapeamento com o ELM.
Versionado. `backlog.md` é **gerado** a partir dele (nunca editado à mão). O estado detalhado de uma fatia em
andamento fica no `status.md` da pasta dela; o backlog só muda nas transições marcadas abaixo.

## Formato

```json
{
  "projeto": "Gestão de Acessos",
  "atualizado": "2026-10-13",
  "proximo": { "EP": 4, "FT": 34 },
  "epicos": [
    {
      "id": "EP-03",
      "titulo": "Bloqueio por tentativas de login",
      "status": "fatiado",
      "prioridade": 1,
      "prd": ".kiro/produto/epicos/EP-03-bloqueio-login/prd.md",
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
      "status": "backlog",
      "sprint": null,
      "responsavel": null,
      "spec": null,
      "branch": null,
      "pr": null,
      "elm": null,
      "concluida-em": null
    }
  ]
}
```

| Campo | Valores |
|---|---|
| épico `status` | `rascunho` · `em-revisao` · `aprovado` · `publicado` · `fatiado` · `concluido` · `cancelado` (o mesmo do frontmatter do PRD) |
| fatia `origem` | `null` (veio de um PRD) ou o item que a originou sem PRD: `"DF 4567"`, `"IB 611"`, `"pedido: <resumo>"` (trilha rápida) |
| `cobre` | `HF-nn#c.c` (cenário) e `REG-nn` do PRD do épico; vazio só na trilha rápida |
| `tamanho` | `P` · `M` · `G` |
| `modo` | `AFK` · `HITL` |
| fatia `status` | `backlog` → `pronta` (Definition of Ready ok) → `em-andamento` → `concluida`; desvios `bloqueada`, `dividida` (+ `substituida-por`), `cancelada` (+ `motivo`) |
| `sprint` | número da sprint (`sdd2-planejamento`) ou `null`; no Kanban, `null` |
| `spec` | `.kiro/specs/<ft>-<slug>/` quando a fatia começa |
| `elm` | `null` ou `{ "id", "url", "tarefas": { "<prefixo>": { "id", "url" } } }` (gravado pela `sdd2-elm`) |

## Quem escreve o quê

| Transição | Skill |
|---|---|
| épico criado / status do PRD | `sdd2-prd` |
| fatias criadas, divididas, juntadas, canceladas | `sdd2-fatiar` |
| `sprint`, `responsavel`, prioridade | `sdd2-planejamento` |
| `pronta` (DoR) → `em-andamento`, `spec`, `branch` | `sdd2-iniciar` |
| `pr` | `sdd2-implementar` |
| `concluida`, `concluida-em` | `sdd2-consolidar` |
| `elm` (ids e urls) | `sdd2-elm` |

## Regras

- Ids nunca são reaproveitados nem renumerados; `proximo` só cresce.
- Antes de gravar: `git pull --rebase` (o backlog é compartilhado); depois, commit pequeno só com ele (e o
  `backlog.md`) quando não houver outro artefato junto.
- Conflito no `backlog.json`: mantenha o remoto e reaplique só a sua mudança, campo a campo. Nunca resolva
  descartando o lado remoto.
- `backlog.md` é regenerado: tabela por épico (**FT | Título | Tam. | Modo | Status | Sprint | Responsável | ELM**),
  na ordem de prioridade, seguida das fatias de trilha rápida.
