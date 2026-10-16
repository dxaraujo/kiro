---
name: sdd-elm
description: "Alimenta o IBM ELM (registro oficial da documentação) a partir dos artefatos do fluxo sdd, sempre pelas skills do power elm, com prévia e confirmação — modos: similares (antes de especificar HF, REG ou GL, busca no bundle e no DOORS Next artefatos iguais, sobrepostos ou relacionados; só leitura), requisitos (conceitos OKF aprovados publicados no DOORS Next, termos → regras → histórias, HF embute REG, idempotente), backlog (épico, Sustentação e itens de backlog das fatias com critérios de aceite e links), sprint (planos e tarefas [ESP] [DEV] [REV] [VER], virada por plannedFor), assumir (o Passo 0 de toda skill de papel: assume e inicia a própria tarefa, sem repetir o que já foi feito), atendimento ([ATD] registrada pela triagem, concluída pela sdd-atender), horas (lançar e relatório), testes (CT.csv no ETM e links), especificação técnica (ET as-built) e conclusão. O que o MCP não faz vira roteiro manual com pendência. Use em \"publica no ELM\", \"sobe o PRD para o DOORS\", \"cria os itens no EWM\", \"publica a sprint\", \"liga os testes\", \"fecha no ELM\", \"lança 4h\", \"relatório de horas\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.5.0"
---

# sdd-elm — O ELM como fonte oficial

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-elm/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Requer o power **`elm`** (MCP `elm`) nesta sessão e as skills dele: **`elm`** (guia do power: regras de uso do
MCP), **`elm-rm`** (DOORS Next), **`elm-ccm`**
(EWM), **`elm-qm`** (ETM — ler o caso de teste importado para obter a URL), **`elm-gc`** (links) — carregue a skill
da área antes de chamar as tools. Ids da project area:
`.kiro/config/power/elm/pa_*.json`. Tipos, pastas, prefixos e regras do projeto: seção **ELM** do
`.kiro/steering/sdd.md`. Mapeamento e limites: [references/mapeamento.md](references/mapeamento.md).

**Sem o MCP `elm` nesta sessão** (revisor, verificador, pesquisador, outra máquina) ou com falha: não publique. Registre `ELM pendente:
<modo> <alvo>` no Histórico do `status.md` (fatia) ou no rodapé do PRD (épico) e siga — o ELM nunca trava o fluxo.
Projeto sem ELM (`sdd.md` → ELM: não usa) → nada a fazer.

## Regras de toda publicação

1. **Prévia antes de escrever:** tabela `Ação (criar | atualizar | ligar | sem mudança) | Alvo | Título | Tipo/Pasta`
   e **uma** confirmação para o lote. Nada é escrito sem "sim".
2. **Idempotência:** cada artefato tem uma identidade no repositório — o conceito OKF em `elm/` (requisitos) ou
   a linha do `backlog.md` (épico, fatia). Antes de criar:
   - o repositório já tem o id (`resource`/`id` do conceito; coluna `elm` do `backlog.md`) → **atualizar** o mesmo id;
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

## Modo similares (antes de especificar — só leitura)

Chamado pela `sdd-prd` (e pela `sdd-triar`, para a regra da ficha de uma fatia padrão sem épico) **antes** de
criar qualquer HF, REG ou GL, e pelo modo requisitos antes de criar um
conceito novo. Só lê: não pede confirmação. Entrada: a lista de artefatos propostos — tipo (`HF` | `REG` | `GL`),
título provisório e 3–6 palavras-chave do domínio (termos do glossário, sinônimos que apareceram na entrevista,
valores e atores centrais).

1. **Bundle** (`<rm.download.path>` do `sdd.md`, se existe): busca de texto do Kiro pelo título e por cada
   palavra-chave. Anote a data do último sincronismo da `elm-sync`.
2. **DOORS Next ao vivo**, pela skill **`elm-rm`**: uma `rm_search_requirements(text=<palavra-chave>)` por palavra-chave
   e pelo título (só `text` — com `folder`/`requirement_type` junto o DOORS Next devolve HTTP 400), filtrando o
   resultado pelos tipos do mapeamento do projeto; e `rm_list_modified` desde o último sincronismo, para ver o que
   outro time criou ou mudou depois da `elm-sync`. Sem o MCP nesta sessão → só o bundle, e a saída diz
   `verificação no ELM ao vivo pendente`.
3. **Ler e classificar** cada acerto (corpo do bundle pelo `path`, ou `rm_get_requirement` pela `elm-rm`):
   - **igual** — o mesmo comportamento, a mesma regra (com o mesmo valor) ou o mesmo termo;
   - **sobrepõe** — parte do mesmo comportamento, a mesma regra com outro valor, ou o mesmo termo com outra definição;
   - **relacionado** — mesmo assunto, comportamento diferente;
   - acerto só por palavra em comum → descarte.
4. **Saída**, um bloco por artefato proposto:

   ```
   🔎 Similares no ELM — EP-<nn> · bundle de <data> · ao vivo: <sim | pendente>
   | Proposto | No ELM (id · título · tipo · pasta) | Relação | Recomendação |
   |---|---|---|---|
   | HF-01 Bloquear após tentativas | 2034 · HF - Bloquear acesso por senha expirada · História · 02-Histórias | relacionado | criar novo, citando 2034 em ## Relações |
   | REG-01 Limite de tentativas | 2101 · REG - Tentativas de login · Regra · 03-Regras | igual | reutilizar 2101 |
   | GL-tentativa-invalida | — | — | criar novo |
   ```

   Recomendação por relação: **igual → reutilizar** (não cria conceito: HF embute a REG existente, cita a HF
   existente, linka o termo existente pelo id) · **sobrepõe → alterar** o existente (caminho "Alteração" da
   `sdd-prd`) · **relacionado → criar novo**, citando o existente em `## Relações` · **nenhum → criar novo**. A
   decisão é da pessoa; a `sdd-prd` registra.

## Modo requisitos (PRD → DOORS Next)

Entrada: a pasta `elm/` do épico (`<produto>/epicos/<EP>-<slug>/elm/`) ou, na consolidação de uma fatia padrão sem
épico, a da fatia (`.kiro/specs/<ft>-<slug>/elm/`, gerada da ficha) — conceitos OKF v0.2 no
formato de [../sdd-prd/references/okf-elm.md](../sdd-prd/references/okf-elm.md). Publica só conceito
`status: stable` com um `verified` humano (`by: human:…`) **posterior** ao `generated.at`; o resto aparece na prévia
como "aguardando aprovação". Publicar **não** muda o status do PRD.

Ordem **de baixo para cima**, para cada artefato nascer com os ids dos que ele cita: **termos** (`GL-*`) →
**regras** (`REG-*`) → **histórias** (`HF-*`). Para cada conceito:

0. **Similares (conceito novo, sem `resource`):** a coluna "No ELM" do PRD (ou da ficha) tem de dizer `novo (verificado <data>)`.
   Sem isso, ou com `rm_list_modified` mostrando artefato do mesmo tipo criado depois dessa data → rode o **modo
   similares** só para esse conceito. Acerto `igual` ou `sobrepõe` → **não cria**: mostre e devolva para a
   `sdd-prd` decidir (reutilizar ou alterar); o resto do lote segue.
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

## Modo backlog (épicos e fatias → EWM)

**Todo trabalho tem pai:** épico → IB → tarefa para o que vem de PRD; o épico de **Sustentação** (um por release ou
ano) para o resto. Ordem obrigatória de criação: épico, depois IB, depois tarefa. `Planejado para` é obrigatório
em IB e tarefa: use sempre a iteração que a pessoa indicar (no planejamento, a da sprint).

1. **Épico — nasce cedo:** a `sdd-triar` chama este modo ao registrar o `EP-nn` (a `sdd-prd`, se ficou
   `pendente`), para o
   pai existir quando o IB da fatia for criado. Tipo do `sdd.md` (a PA pode não ter "Épico": então é um **Item de
   Backlog pai**), título `[EP-03] <título>`, descrição = problema (e, depois do GATE, solução do PRD + link do
   PRD no repositório). Links **rastreia** → histórias, quando publicadas. Épico que nasce de um item do EWM: se
   o item já é do tipo de épico, ele é o épico; senão o item vira filho do épico novo
   (`ccm_update_workitem(id, parent=<épico>)`).
2. **Sustentação e Atendimento** (uma vez por release/ano, se a linha `Sustentação:` do `backlog.md` estiver
   vazia): épico `[SUS-<ano>] Sustentação` e, filho dele, o IB `Atendimento` (pai das `[ATD]`); ids nessa linha.
3. **Item de backlog por fatia** (`backlog no EWM` = `ao-fatiar`, logo após o GATE do backlog — na fatia sem épico,
   ao registrar na `sdd-triar` —, ou `na-sprint`):
   título `[FT-031] <título>`, `parent` = épico (fatia sem épico sem item de origem: o épico de
   Sustentação; com item de origem não há IB novo; direta: sem IB), pontos pelo tamanho (tabela do `sdd.md`), descrição com modo
   AFK/HITL, `bloqueada por` e pasta prevista; responsável = P.O. (o IB é do produto). **Critérios de aceite:** os
   cenários que a fatia cobre (`cobre`), em Dado / Quando / Então, copiados do PRD (fatia sem épico: da ficha), no campo da linha "Critérios
   de aceite no IB" do `sdd.md` (Markdown; o MCP grava como texto rico) — sem o campo, numa seção "Critérios de
   aceite" da descrição. Fonte única é o PRD: o campo é cópia gerada, com o aviso "gerado do PRD — não edite
   aqui"; atualize quando a fatia for refinada ou a `sdd-consolidar` registrar mudança as-built. Links
   **implementa** → cada história que a fatia cobre; **depende de** → IBs das fatias em `bloqueada-por` (se o
   `link-types` tiver; senão fica na descrição).
4. **Fatia dividida:** conforme a linha do `sdd.md` — IBs novos filhos do IB original (que segue filho do épico),
   ou fecha o original e cria novos. Pai errado → `ccm_update_workitem(id, parent=<novo pai>)`.
5. `backlog.md` (na base): `elm` de cada fatia/épico.

## Modo sprint (planejamento → iteração)

Entrada da `sdd-planejamento` (sempre chamada depois do "ok" da sprint): número da sprint, iteração, time e as três
seções do `sprint-<nn>.md` (fatias com responsável, revisor e verificador; especificação; reserva de atendimento).

1. **Planos**, por iteração e time — os dois tipos que o fluxo usa: **plano de backlog**
   (`com.ibm.team.apt.plantype.product.backlog`: épicos, IBs, Sustentação e "Atendimento") e **plano da sprint**
   (`com.ibm.team.apt.plantype.default`: as tarefas). Faltou algum (ou a iteração) → crie pela `elm-setup`
   (`ccm_create_iteration` / `ccm_create_iteration_plan`; exige a permissão de modificar iterações — se falhar,
   peça a quem administra a PA).
2. Fatias sem IB e épicos com `elm` `pendente` ou `—` (projeto com ELM) → modo backlog primeiro (a `[ESP]` nunca nasce sem pai). Para cada IB da sprint: `plannedFor` = iteração (o responsável
   continua o P.O.).
3. **Tarefas**, com os títulos da linha "Tarefas" do `sdd.md`, responsável, estimativa em horas e `plannedFor` =
   iteração:

   | Tarefa | Uma por | Responsável | Pai |
   |---|---|---|---|
   | `[ESP] EP-05 Especificação` | épico na seção Especificação | quem especifica | o épico |
   | `[DEV] FT-031 Implementar` | fatia | responsável da fatia | IB da fatia |
   | `[REV] FT-031 Revisar` | fatia **HITL** | revisor | IB da fatia |
   | `[VER] FT-031 Verificar` | fatia **HITL** | verificador | IB da fatia |

   Fatia **AFK** (`modo` do `backlog.md`): só a `[DEV]` — revisão e verificação são subagentes, sem tarefa nem
   horas.

   Fatia sem épico com item de origem → pai = o item (sem IB novo); direta → só a `[DEV] FT-<nnn> <pedido>`, pai = item de
   origem ou Sustentação. Campos obrigatórios da Tarefa (categoria de horas, OTR, classificação, Clarity) pela
   `elm-ccm` (Criar) e pela linha "Classificação da tarefa" do `sdd.md`. Grave os ids na coluna "Tarefa ELM" do
   `sprint-<nn>.md` e no `elm` do `backlog.md`.
4. **Virada:** tarefas não concluídas (inclusive `[ESP]` e `[ATD]`) e IBs não concluídos → só o `plannedFor`
   muda para a nova iteração (o pai não muda; move, nunca recria); roteiro manual de **baseline** (componente RM +
   GC) se o projeto exige baseline por sprint.

## Modo assumir (Passo 0 das skills de papel)

Chamado pela skill do papel antes de trabalhar: `sdd-desenvolver` (`[DEV]`), `sdd-especificar` (`[ESP]`),
`sdd-revisar` (`[REV]`), `sdd-verificar` (`[VER]`) e `sdd-atender` (`[ATD]`). A regra mora só aqui.

1. **Tarefa:** a informada; senão pelo item — coluna `elm` do `backlog.md`, campo ELM do `status.md` da fatia ou
   coluna "Tarefa ELM" do `sprint-<nn>.md`. Não achou → a skill que chamou diz como criar (modo *sprint* ou
   *atendimento*); nunca crie tarefa por aqui.
2. **Leia** (`ccm_get_workitem`) o responsável e o estado, e decida:

   | Situação | Ação |
   |---|---|
   | minha (`whoami`) e em andamento | **nada a fazer** — diga "já assumida" e siga |
   | sem responsável, ou minha e não iniciada | responsável = `whoami`; ação para o estado em andamento da PA (`ccm_list_workitem_states`; ex.: *Em Desenvolvimento*); estimativa se faltar (pergunte) |
   | de outra pessoa | mostre quem é e pergunte se assume no lugar dela; sem "sim", pare |
   | concluída | só se quem chamou disse **retrabalho**: ação de reabertura da PA (sem ação de reabertura → `ELM pendente: reabrir <tarefa>` e aviso); fora disso → avise e pare |

3. **Uma** confirmação com o que muda (responsável, estado, estimativa); `ccm_update_workitem` com os campos e o
   `state` na mesma chamada.
4. Sem MCP nesta sessão ou com falha → `ELM pendente: assumir <tarefa>` onde a skill que chamou indicar, e siga.

## Modo atendimento

- **Registrar** (chamado pela `sdd-triar`): `[ATD] AT-<nnn> <título>`, filha do IB "Atendimento" (linha
  `Sustentação:` do `backlog.md`), `plannedFor` = a iteração que a triagem confirmou (sprint aberta; Kanban → a
  iteração corrente; sem sprint aberta → sem `plannedFor`), responsável = quem vai atender, estimativa. Fica no
  estado inicial: quem atende a assume (modo *assumir*) ao executar.
- **Concluir** (chamado pela `sdd-atender`): depois do saldo de horas (modo horas), estado de conclusão da PA.

## Modo horas

**Lançar** — na conclusão de uma tarefa (chamado pela skill que conclui) ou sob pedido ("lança 4h", "lança 6h de
ontem"):
1. Tarefa: a informada; senão a atual — o `status.md` da branch dá a `[DEV]`, `[REV]` ou `[VER]` do papel de quem
   pede; o AT aberto dá a `[ATD]`; a `[ESP]` vem do `sprint-<nn>.md`. Dúvida → pergunte.
2. Horas já lançadas (`ccm_list_timesheet`) → mostre e desconte. Uma linha por data; data futura não.
3. Regras do EWM: só o responsável lança; máximo 16 h por dia; time code e work type de `timesheet` no
   `pa_*.json`. Confirme e `ccm_add_timesheet`. Lançar não conclui a tarefa (tarefa de vários dias); concluir é
   do modo conclusão ou da skill que chamou.
4. Sem MCP ou com falha → `ELM pendente: lançar <h>h em <tarefa> (<data>)` no `status.md`, no registro do AT ou no
   `sprint-<nn>.md`; este modo lança depois.

**Relatório** (virada ou sob pedido): `ccm_list_timesheet` das tarefas da sprint → horas por tipo (`[ESP]`
`[DEV]` `[REV]` `[VER]` `[ATD]`) e por pessoa, planejadas × lançadas, e as tarefas concluídas **sem horas** (só no
fechamento). Alimenta a retrospectiva e a recalibração da reserva de atendimento.

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

Uma tarefa por vez, chamada pela skill do papel que terminou (`[DEV]` no PR, `[REV]` ao aprovar, `[VER]` ao
aceitar, `[ESP]` no GATE do backlog, `[ATD]` ao finalizar) → estado de conclusão da PA (ação de
`ccm_list_workitem_states`), depois do saldo de horas (modo horas). O IB da fatia, pela `sdd-consolidar` depois do
merge; o épico quando todas as fatias concluírem. Comentário opcional no IB: PR, pasta e ids publicados.

## Saída

```
🏛️ ELM — <modo> · <EP | FT | Sprint N>
Criados: <n> · Atualizados: <n> · Sem mudança: <n> · Links: <n> · Conflitos: <n resolvidos>
Pendências manuais: <lista | nenhuma>
```
