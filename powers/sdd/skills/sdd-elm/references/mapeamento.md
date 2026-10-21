# Mapeamento sdd → IBM ELM

O ELM é o **sistema de registro**: o que o sistema faz (DOORS Next), o que está sendo feito (EWM) e como foi
testado (ETM). O repositório guarda as **propostas de mudança** (PRD, fatias) e o histórico de como cada mudança
foi feita. Os nomes reais de tipos, pastas, campos e links são da project area: vêm do
`.kiro/config/power/elm/pa_<nome>.json` (power `elm`, skill `elm-setup`) e o mapeamento abaixo é confirmado na
`sdd-setup` e gravado na seção **ELM** do `.kiro/steering/sdd.md`.

## Artefatos

| sdd (repositório) | ELM | Tipo padrão (ajustável) | Quando |
|---|---|---|---|
| Épico `EP-nn` | EWM — Épico, ou Item de Backlog pai quando a PA não tem Épico | `Épico` / `com.ibm.team.apt.workItemType.epic` ou `…workItemType.story` | quando o épico entra na sprint (`[ESP]` ou primeira fatia) |
| Sustentação · Atendimento · `[GB]` | EWM — épico `[SUS-<ano>] Sustentação`, IB `Atendimento` e Tarefa `[GB] Gerenciamento do backlog` filhos dele | os mesmos tipos · `task` | primeira sprint do release/ano (ou a triagem, para a `[GB]`, com sprint aberta) |
| História `HF-nn` (conceito OKF em `elm/`) | DOORS Next — artefato | `História de Usuário` (título `HF - <nome>`) | GATE do PRD (`na-aprovacao`) ou merge (`no-merge`) |
| Regra `REG-nn` (conceito OKF em `elm/`) | DOORS Next — artefato | `Regra` (título `REG - <nome>`) | idem, **antes** das histórias (elas embutem as regras) |
| Termo `GL-<termo>` (conceito OKF em `elm/`) | DOORS Next — artefato | `Termos de Glossário` (título = o termo) | idem, antes das regras |
| Fatia `FT-nnn` | EWM — Item de Backlog (story, *plan item*) | `com.ibm.team.apt.workItemType.story` | quando a fatia entra na sprint |
| Tarefas `[DEV]` `[REV]` `[VER]` da fatia | EWM — Tarefa (filha do IB, *execution item*) | `task` | planejamento da sprint (`[REV]` `[VER]` da fatia AFK que troca para HITL: na troca, pela `sdd-planejamento`) |
| Tarefa `[APR]` da fatia (`Aprovar plano` · `Aprovar PR` do AFK) | EWM — Tarefa (mesmo pai das tarefas da fatia), do Dev Sênior que aprova | `task` | no gate (`sdd-plano`, `sdd-implementar` Passo 5, `sdd-loop`), nunca no planejamento |
| Tarefa `[ESP]` do épico | EWM — Tarefa (filha do épico) | `task` | planejamento da sprint |
| Tarefa `[ATD]` do atendimento | EWM — Tarefa (filha de `Atendimento`) | `task` | quando o AT entra na sprint (triagem com sprint aberta, encaixe ou planejamento) |
| Critérios de aceite da fatia | campo de texto rico do IB (ou seção da descrição) | linha do `sdd.md` | publicação do IB |
| Horas | EWM — timesheet da tarefa | `elm-ccm` › lançar horas | a qualquer momento numa tarefa iniciada (padrão: ao fechar cada sessão) ou sob pedido; na conclusão, o saldo |
| ET as-built (opcional) | DOORS Next — artefato | `Especificação Técnica` (título `ET - <fatia>`) | escrita pelo Dev no PR (`sdd-implementar` Passo 5); publicada na consolidação (depois do merge) |
| Cenário verificado | ETM — Caso de Teste | `elm-qm` › criar caso de teste (texto da linha do `CT.csv`; sem permissão → importação manual do `CT.csv`) | consolidação |
| Defeito (trilha rápida) | EWM — Defeito | `defect` | já existe; a fatia referencia |

## Links

| Link | De → Para | Ferramenta (`elm-gc`) | Quando |
|---|---|---|---|
| **implementa** | IB da fatia → cada História (HF) que ela cobre | `elm-gc` › ligar item a requisito (implementa) | publicação do IB |
| **rastreia** | Épico → Histórias do PRD | `elm-gc` › ligar item a requisito (rastreia) | publicação do épico |
| **afeta** | Defeito → História/Regra que ele viola | `elm-gc` › ligar item a requisito (afeta) | trilha rápida |
| **valida** | Caso de Teste → História | na criação (`elm-qm` › criar caso de teste); CT importado à mão: `elm-gc` › ligar caso de teste a requisito (valida) | consolidação |
| **testado por** | IB → Caso de Teste | `elm-gc` › ligar item a caso de teste (testado por) | consolidação, depois da criação do CT |
| **pai / filhos** | Épico → IB → Tarefa (`[APR]` inclusive); Épico → `[ESP]`; Atendimento → `[ATD]` | `elm-ccm` › criar item (com pai); troca: trocar o pai | criação |
| **depende de** | IB → IB (`bloqueada-por` do backlog) | atributo de link do `link-types` do `pa_*.json`, se mapeado | publicação do IB |
| **embutido** | História → Regra (no texto) | `elm-rm` › atualizar requisito (embutidos) | publicação da história |

Os links são gravados no lado do work item ou do teste (o DOORS Next mostra o backlink). As tools só
**acrescentam**: antes de ligar, liste os existentes (`list_linked_*`) para não duplicar.

## Pontos e tamanho

Opcional: o fluxo prevê pela vazão, não por pontos. Se o `sdd.md` tiver a tabela de pontos (para o relatório de
velocidade do EWM), eles vão no campo de complexidade/pontos de história do IB (*plan item*), nunca nas tarefas.
Sem a tabela → o campo fica vazio.

## O que o power `elm` não faz (passos manuais)

Hoje o power `elm` grava título e texto de requisitos, work items (inclusive troca de pai e `plannedFor`), estados,
comentários, horas, casos de teste (criação, com o link *valida*) e links work item/teste ↔ requisito. Não grava:
atributos de requisito, links requisito ↔ requisito (*satisfaz*, *restringe*, *elabora*), módulos, change sets e
baselines. Quando o processo do projeto exigir algum deles, a `sdd-elm`
entrega um **roteiro manual** com os ids exatos, e o registra como `ELM pendente [<chave>]: <ação>` até a pessoa confirmar:

| Exigência do projeto (seção ELM do `sdd.md`) | Roteiro manual |
|---|---|
| Change set por publicação | criar o change set `sdd <EP> v<versão>` no DOORS Next **antes** da publicação e entregá-lo depois da revisão na UI |
| Módulo por épico | inserir os artefatos publicados no módulo `<nome>`, na ordem do PRD |
| Regra **restringe** história | criar os links na UI (lista: `REG <id> → HF <id>`) |
| Atributo de situação/aprovação | preencher na UI (lista de ids) |
| Baseline por sprint/release | no fechamento da sprint: baseline do componente RM e baseline global (GC) |

## Identidade e idempotência

Os artefatos do DOORS Next nascem como conceitos **OKF v0.2** na pasta `elm/` do épico (ou da fatia), no mesmo
formato do bundle da `elm-sync` — ver [../../sdd-prd/references/okf-elm.md](../../sdd-prd/references/okf-elm.md):

- a chave estável é o **Concept ID** (o caminho do arquivo dentro de `elm/`), que não muda;
- `resource` ausente = ainda não publicado (criar); `resource` + `id` = publicado (atualizar o mesmo id);
- a entrada do ELM em `sources` guarda o `last_modified` visto na última publicação — base da detecção de
  conflito com mudanças feitas direto no ELM;
- aprovação = `verified` humano (OKF §5.2); sem ele, não publica.

Nada é acrescentado ao texto publicado para identificar o artefato.
