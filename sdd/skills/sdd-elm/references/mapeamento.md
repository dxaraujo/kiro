# Mapeamento sdd → IBM ELM

O ELM é o **sistema de registro**: o que o sistema faz (DOORS Next), o que está sendo feito (EWM) e como foi
testado (ETM). O repositório guarda as **propostas de mudança** (PRD, fatias) e o histórico de como cada mudança
foi feita. Os nomes reais de tipos, pastas, campos e links são da project area: vêm do
`.kiro/config/power/elm/pa_<nome>.json` (power `elm`, skill `elm-setup`) e o mapeamento abaixo é confirmado na
`sdd-setup` e gravado na seção **ELM** do `.kiro/steering/sdd.md`.

## Artefatos

| sdd (repositório) | ELM | Tipo padrão (ajustável) | Quando |
|---|---|---|---|
| Épico `EP-nn` | EWM — Épico (ou Item de Backlog pai) | `Épico` / `com.ibm.team.apt.workItemType.epic` | publicação do backlog |
| História `HF-nn` (conceito OKF em `elm/`) | DOORS Next — artefato | `História de Usuário` (título `HF - <nome>`) | GATE do PRD (`na-aprovacao`) ou merge (`no-merge`) |
| Regra `REG-nn` (conceito OKF em `elm/`) | DOORS Next — artefato | `Regra` (título `REG - <nome>`) | idem, **antes** das histórias (elas embutem as regras) |
| Termo `GL-<termo>` (conceito OKF em `elm/`) | DOORS Next — artefato | `Termos de Glossário` (título = o termo) | idem, antes das regras |
| Fatia `FT-nnn` | EWM — Item de Backlog (story, *plan item*) | `com.ibm.team.apt.workItemType.story` | conforme `backlog no EWM` (seção ELM do `sdd.md`): ao fatiar ou na sprint |
| Tarefas da fatia | EWM — Tarefa (filha do IB, *execution item*) | `task` | planejamento da sprint |
| ET as-built (opcional) | DOORS Next — artefato | `Especificação Técnica` (título `ET - <fatia>`) | consolidação (depois do merge) |
| Cenário verificado | ETM — Caso de Teste | importação do `CT.csv` | consolidação |
| Defeito (trilha rápida) | EWM — Defeito | `defect` | já existe; a fatia referencia |

## Links

| Link | De → Para | Ferramenta (`elm-gc`) | Quando |
|---|---|---|---|
| **implementa** | IB da fatia → cada História (HF) que ela cobre | `link_workitem_and_requirement(…, "implements")` | publicação do IB |
| **rastreia** | Épico → Histórias do PRD | `link_workitem_and_requirement(…, "tracks")` | publicação do épico |
| **afeta** | Defeito → História/Regra que ele viola | `link_workitem_and_requirement(…, "affects")` | trilha rápida |
| **valida** | Caso de Teste → História | `link_testartifact_and_requirement(…, "validates")` | depois da importação do CT |
| **testado por** | IB → Caso de Teste | `link_workitem_and_testartifact(…, "tests")` | depois da importação do CT |
| **pai / filhos** | Épico → IB → Tarefa | `ccm_create_workitem(…, parent=…)` | criação |
| **depende de** | IB → IB (`bloqueada-por` do backlog) | atributo de link do `link-types` do `pa_*.json`, se mapeado | publicação do IB |
| **embutido** | História → Regra (no texto) | `rm_update_requirement(…, embedded=[…])` | publicação da história |

Os links são gravados no lado do work item ou do teste (o DOORS Next mostra o backlink). As tools só
**acrescentam**: antes de ligar, liste os existentes (`list_linked_*`) para não duplicar.

## Pontos e tamanho

O IB é *plan item*: os pontos vão no campo de complexidade/pontos de história do IB (nunca nas tarefas), para o
relatório de velocidade do EWM funcionar. Padrão (ajustável no `sdd.md`): `P = 2`, `M = 3`, `G = 5`.

## O que o MCP `elm` não faz (passos manuais)

Hoje o MCP grava título e texto de requisitos, work items, estados, comentários e links work item/teste ↔
requisito. Não grava: atributos de requisito, links requisito ↔ requisito (*satisfaz*, *restringe*, *elabora*),
módulos, change sets, baselines e casos de teste. Quando o processo do projeto exigir algum deles, a `sdd-elm`
entrega um **roteiro manual** com os ids exatos, e o registra como `ELM pendente: <ação>` até a pessoa confirmar:

| Exigência do projeto (seção ELM do `sdd.md`) | Roteiro manual |
|---|---|
| Change set por publicação | criar o change set `sdd <EP> v<versão>` no DOORS Next **antes** da publicação e entregá-lo depois da revisão na UI |
| Módulo por épico | inserir os artefatos publicados no módulo `<nome>`, na ordem do PRD |
| Regra **restringe** história | criar os links na UI (lista: `REG <id> → HF <id>`) |
| Atributo de situação/aprovação | preencher na UI (lista de ids) |
| Baseline por sprint/release | no fechamento da sprint: baseline do componente RM e baseline global (GC) |
| Caso de teste | importar o `CT.csv` no ETM (Importar → CSV) e informar os ids |

## Identidade e idempotência

Os artefatos do DOORS Next nascem como conceitos **OKF v0.2** na pasta `elm/` do épico (ou da fatia), no mesmo
formato do bundle da `elm-sync` — ver [../../sdd-prd/references/okf-elm.md](../../sdd-prd/references/okf-elm.md):

- a chave estável é o **Concept ID** (o caminho do arquivo dentro de `elm/`), que não muda;
- `resource` ausente = ainda não publicado (criar); `resource` + `id` = publicado (atualizar o mesmo id);
- a entrada do ELM em `sources` guarda o `last_modified` visto na última publicação — base da detecção de
  conflito com mudanças feitas direto no ELM;
- aprovação = `verified` humano (OKF §5.2); sem ele, não publica.

Nada é acrescentado ao texto publicado para identificar o artefato.
