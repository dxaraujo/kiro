---
name: sdd-elm
description: "Alimenta o IBM ELM (sistema de registro da documentação do projeto) a partir dos artefatos do fluxo sdd, pelo power elm — modo requisitos (histórias, regras e termos do épico — conceitos OKF v0.2 na pasta da spec, aprovados com verified humano — publicados no DOORS Next de baixo para cima, HF → REG como embed, idempotente pelo resource/id do conceito, alteração do artefato existente em vez de duplicar), modo backlog (épico e itens de backlog das fatias no EWM, ligados às histórias por implementa/rastreia), modo sprint (iteração, tarefas filhas, responsáveis, virada), modo testes (CT.csv para o ETM e links valida/testado por), modo especificação técnica (ET as-built) e modo conclusão (estados). Sempre mostra a prévia e pede confirmação; o que o MCP não faz vira roteiro manual com pendência registrada. Use em \"publica no ELM\", \"sobe o PRD para o DOORS\", \"cria os itens no EWM\", \"publica a sprint\", \"liga os testes\", \"fecha no ELM\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.0.0"
---

# sdd-elm — O ELM como fonte oficial

Requer o power **`elm`** (MCP `elm`) nesta sessão e as skills dele: **`elm`** (guia do power: regras de uso do
MCP), **`elm-rm`** (DOORS Next), **`elm-ccm`**
(EWM), **`elm-qm`** (ETM — ler o caso de teste importado para obter a URL), **`elm-gc`** (links) — carregue a skill
da área antes de chamar as tools. Ids da project area:
`.kiro/config/power/elm/pa_*.json`. Tipos, pastas, prefixos e regras do projeto: seção **ELM** do
`.kiro/steering/sdd.md`. Mapeamento e limites: [references/mapeamento.md](references/mapeamento.md).

**Sem o MCP `elm` nesta sessão** (agentes, kiro-cli, outra máquina): não publique. Registre `ELM pendente:
<modo> <alvo>` no Histórico do `status.md` (fatia) ou no rodapé do PRD (épico) e siga — o ELM nunca trava o fluxo.
Projeto sem ELM (`sdd.md` → ELM: não usa) → nada a fazer.

## Regras de toda publicação

1. **Prévia antes de escrever:** tabela `Ação (criar | atualizar | ligar | sem mudança) | Alvo | Título | Tipo/Pasta`
   e **uma** confirmação para o lote. Nada é escrito sem "sim".
2. **Idempotência:** cada artefato tem uma identidade no repositório — o conceito OKF em `elm/` (requisitos) ou
   a entrada do `backlog.json` (épico, fatia). Antes de criar:
   - o repositório já tem o id (`resource`/`id` do conceito; `elm` do `backlog.json`) → **atualizar** o mesmo id;
   - não tem → procure no ELM uma publicação interrompida (requisito: `rm_search_requirements(text=<título>)`
     filtrado pelo tipo e pela pasta do conceito; EWM: título com `[FT-031]`) — achou um candidato → mostre e
     pergunte se é ele (sim → grave o id e trate como atualização);
   - não achou → criar.
3. **Conflito:** o artefato mudou no ELM depois da última vez que o vimos (`rm_list_modified` mais novo que o
   `last_modified` da entrada do ELM em `sources` do conceito) → mostre os dois lados e **pergunte** qual fica.
   Nunca sobrescreva mudança feita no ELM sem "sim".
4. **Grave de volta** no repositório, a cada item publicado (requisito: `resource`, `id` e a entrada do ELM em
   `sources` do conceito, mais uma linha no `log.md`; backlog: `elm`). Commit ao final
   (`<FT|EP> - Publicar no ELM`). Falha no meio → os já publicados ficam registrados; rode de novo (o passo 2
   retoma).
5. Mostre nomes de tipo, pasta e iteração — nunca `FR_`/`OT_`/uuids.
6. Nunca apague nada no ELM. Artefato que deixou de valer → peça à pessoa a marcação de obsoleto/remoção do módulo
   na UI (roteiro manual).

## Modo requisitos (PRD → DOORS Next)

Entrada: a pasta `elm/` do épico (`<produto>/epicos/<EP>-<slug>/elm/`) — conceitos OKF v0.2 no
formato de [../sdd-prd/references/okf-elm.md](../sdd-prd/references/okf-elm.md). Publica só conceito
`status: stable` com um `verified` humano (`by: human:…`) **posterior** ao `generated.at`; o resto aparece na prévia
como "aguardando aprovação". Publicar **não** muda o status do PRD.

Ordem **de baixo para cima**, para cada artefato nascer com os ids dos que ele cita: **termos** (`GL-*`) →
**regras** (`REG-*`) → **histórias** (`HF-*`). Para cada conceito:

1. **Tipo e pasta:** `type` → `rm.requirements-types`; `tags[0]` → `rm.folders` (`pa_*.json`). Não casou → pergunte
   uma vez; vale para o lote.
2. **Texto:** o corpo, sem a seção `## Relações` (ela é só local), com os links relativos trocados:
   - para uma **regra** já publicada → embed `[<id>](<id>)` e o id em `embedded` (HF → REG é sempre embed);
   - para um **termo** já publicado → hyperlink `[<id>](<id>)`;
   - para conceito ainda sem id → só o título, como texto;
   - link do bundle (`../03-Regras/2001-x.md`) ou URL do ELM → como está (o MCP resolve).
   O texto vai em **Markdown** direto (`rm_create_requirement` / `rm_update_requirement` convertem).
3. **Criar** (sem `resource`) → `rm_create_requirement(type, pasta, title, text, embedded)`.
   **Atualizar** (com `id`) → confira o conflito (regra 3), mostre o diff do corpo e mande o texto inteiro com o
   `embedded` correto: `rm_update_requirement(id, title, text, embedded)`.
4. **Grave de volta** no conceito: `resource` = URL devolvida, `id`, e a entrada `{ id: elm, resource: <URL>,
   last_modified: <rm_list_modified> }` em `sources`; `**Publication**` no `log.md`. Termos: o id também na coluna ELM
   do glossário do projeto.

Atributos (aprovação, prioridade) e links requisito ↔ requisito (*restringe*, *satisfaz*) ficam só nos conceitos:
o MCP não os grava. Roteiro manual se o processo do projeto os exigir no ELM (atributo, link, change set, módulo).
Depois: sugira a **`elm-sync`** para baixar ao bundle a versão oficial, que passa a ser a viva; os conceitos de
`elm/` ficam como registro, com `resource` preenchido. Commits na base, como todo artefato de produto.

## Modo backlog (fatias → EWM)

Quando: `backlog no EWM` = `ao-fatiar` (logo após o GATE do backlog) ou `na-sprint` (só as fatias da sprint, no
modo sprint).

1. **Épico** (se não tem `elm`): tipo do `sdd.md`, título `[EP-03] <título>`, descrição = problema +
   solução do PRD + link do PRD no repositório; links **rastreia** → histórias publicadas.
2. **Item de backlog por fatia:** título `[FT-031] <título>`, `parent` = épico, pontos pelo tamanho (tabela do
   `sdd.md`), descrição com: cenários cobertos (texto), modo AFK/HITL, `bloqueada por`, pasta prevista;
   responsável = P.O. (o IB é do produto). Links **implementa** → cada história que a fatia cobre; **depende de** →
   IBs das fatias em `bloqueada-por` (se o `link-types` tiver; senão fica na descrição).
3. `backlog.json` (na base): `elm` de cada fatia/épico.

## Modo sprint (planejamento → iteração)

Entrada da `sdd-planejamento`: número da sprint, iteração, plano e time confirmados, fatias da sprint.

1. Iteração/plano inexistentes → ofereça criá-los pela `elm-setup` (exige a permissão de modificar iterações na
   PA; as tools de criação usam serviços internos do EWM — se falharem, peça a quem administra a PA).
2. Fatias sem IB → modo backlog primeiro. Para cada IB da sprint: `plannedFor` = iteração (o planejamento é de
   quem planeja; o responsável continua o P.O.).
3. **Tarefas** filhas pelo template do `sdd.md` (ex.: `[DEV] FT-031 Implementar`, `[VER] FT-031
   Verificar`), com responsável e estimativa em horas se o planejamento informou.
4. **Virada:** IBs/tarefas não concluídos da sprint que fechou → `plannedFor` da nova (move, nunca recria);
   roteiro manual de **baseline** (componente RM + GC) se o projeto exige baseline por sprint.

## Modo testes (verificação → ETM)

1. Entregue o caminho do `CT.csv` de cada fatia: `Importe no ETM (Importar → CSV)`. Pergunte os ids criados.
2. Com os ids: leia cada caso pela `elm-qm` (`get_testartifact`) para obter a URL, depois ligue **valida** (CT →
   história coberta pelo cenário) e **testado por** (IB → CT). `gc_context` se o ETM usar configuração global
   (`elm-gc`).
3. Registre os ids no `verificacao.md` e no `status.md`.

## Modo especificação técnica (opcional, as-built)

Só se a linha ET da seção ELM do `sdd.md` disser `as-built no merge`. Gere `ET - FT-031 <título>` a partir do `design.md` e do
código **final** (interfaces, contratos, dados, integrações, decisões técnicas — nada do que não foi feito),
grave-a como conceito OKF em `.kiro/specs/<ft>-<slug>/elm/ET-<slug>.md` (mesmo formato; `type` = o tipo de ET do
projeto), mostre, publique como os requisitos depois do `verified` humano, e ligue ao IB (**implementa**).

## Modo conclusão

Tarefas e IB da fatia → estado de conclusão da PA (ação de `ccm_list_workitem_states`); épico quando todas as
fatias concluírem. Comentário opcional no IB: PR, pasta e ids publicados.

## Saída

```
🏛️ ELM — <modo> · <EP | FT | Sprint N>
Criados: <n> · Atualizados: <n> · Sem mudança: <n> · Links: <n> · Conflitos: <n resolvidos>
Pendências manuais: <lista | nenhuma>
```
