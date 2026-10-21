---
name: sdd-elm
description: "Alimenta o IBM ELM (registro oficial da documentação) a partir dos artefatos do fluxo sdd, pelas skills do power elm, com prévia e confirmação — modos: similares (antes de especificar HF, REG ou GL, busca artefatos iguais ou relacionados; só leitura), requisitos (conceitos OKF aprovados no DOORS Next, idempotente), backlog (épico, Sustentação e itens de backlog das fatias com critérios de aceite), sprint (planos e tarefas [ESP] [DEV] [REV] [VER], [APR] no gate, troca AFK → HITL, virada), assumir (Passo 0 das skills de papel), atendimento ([ATD]), horas (lançar e relatório), testes (casos de teste criados no ETM, um por cenário verificado, com os links valida e testado por; CT.csv como alternativa manual), especificação técnica (ET as-built) e conclusão. O que o power elm não faz vira roteiro manual com pendência. Use em \"publica no ELM\", \"sobe o PRD para o DOORS\", \"cria os itens no EWM\", \"publica a sprint\", \"liga os testes\", \"fecha no ELM\", \"lança 4h\", \"relatório de horas\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.7.0"
---

# sdd-elm — O ELM como fonte oficial

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-elm/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

**Contrato com o power `elm`:** esta skill decide **quando** e **o quê** registrar; **como** falar com o ELM é do
power `elm`. Ela pede **operações** pelos nomes da seção "Operações" de cada skill `elm-*` (ex.: `elm-ccm` ›
assumir tarefa, lançar horas, anexar) — nunca chama tool direto nem repete regra do EWM (responsável, limites de
horas, estados): essas moram lá.

Requer o power **`elm`** nesta sessão (os agentes o recebem com `includePowers: true`) e as skills dele: **`elm`** (guia do power), **`elm-rm`** (DOORS Next), **`elm-ccm`**
(EWM), **`elm-qm`** (ETM — criar e ler caso de teste), **`elm-gc`** (links) — carregue a skill
da área antes de chamar as tools. Ids da project area:
`.kiro/config/power/elm/pa_*.json`. Tipos, pastas, prefixos e regras do projeto: seção **ELM** do
`.kiro/steering/sdd.md`. Mapeamento e limites: [references/mapeamento.md](references/mapeamento.md).

**Sem o power `elm` nesta sessão** (pesquisador, outra máquina) ou com falha: não publique. Registre `ELM pendente
[<chave>]: <o que falta>` no **lugar único** do artefato e siga — o ELM nunca trava o fluxo. A **chave** identifica
a ação e o alvo, curta e única no artefato (`[DEV 669412 concluir]`, `[IB FT-031 concluir]`, `[REG-01 publicar]`,
`[CT FT-031 criar]`); uma pendência por chave:

| Artefato | Onde mora a pendência |
|---|---|
| fatia | Histórico do `status.md` |
| épico | rodapé do `prd.md` (antes do GATE, o `rascunho.md` da pasta de trabalho) |
| atendimento | campo `**ELM:**` do `AT-<nnn>-<slug>.md` (e `elm` `pendente` na linha do backlog enquanto a `[ATD]` não existe) |
| sprint | coluna "Tarefa ELM" do `sprint-<nn>.md` (`pendente`) |

**Baixar pendências** ("resolve as pendências do ELM"): a `sdd-status` as lista; para cada uma, rode o modo
indicado e acrescente `ELM feito [<chave>]: <o que foi feito> (<data>)` no mesmo lugar, com a **mesma chave** — a
pendência nunca é apagada, só respondida; a `sdd-status` casa as duas pela chave.
Projeto sem ELM (`sdd.md` → ELM: não usa) → nada a fazer.

## Regras de toda publicação

1. **Prévia antes de escrever:** tabela `Ação (criar | atualizar | ligar | sem mudança) | Alvo | Título | Tipo/Pasta`
   e **uma** confirmação para o lote. Nada é escrito sem "sim".
2. **Idempotência:** cada artefato tem uma identidade no repositório — o conceito OKF em `elm/` (requisitos) ou
   a linha do `backlog.md` (épico, fatia). Antes de criar:
   - o repositório já tem o id (`resource`/`id` do conceito; coluna `elm` do `backlog.md`) → **atualizar** o mesmo id;
   - não tem → procure no ELM uma publicação interrompida (requisito: `elm-rm` › **buscar requisitos** pelo título
     filtrado pelo tipo e pela pasta do conceito; EWM: item de backlog ou épico pelo título com `[FT-031]`/`[EP-03]`;
     **tarefa** pelo prefixo e o id — `[DEV] FT-031`, `[ESP] EP-03`, `[ATD] AT-012` — **e o mesmo pai**, entre os
     filhos do pai) — achou um candidato → mostre e pergunte se é ele (sim → grave o id e trate como atualização);
   - não achou → criar.
3. **Conflito:** o artefato mudou no ELM depois da última vez que o vimos (`elm-rm` › **última modificação** mais nova que o
   `last_modified` da entrada do ELM em `sources` do conceito) → mostre os dois lados e **pergunte** qual fica.
   Nunca sobrescreva mudança feita no ELM sem "sim".
4. **Grave de volta** no repositório, a cada item publicado (requisito: `resource`, `id` e a entrada do ELM em
   `sources` do conceito, mais uma linha no `log.md`; backlog: `elm`). Commit ao final
   (`<FT|EP> - Publicar no ELM`). Falha no meio → os já publicados ficam registrados; rode de novo (o passo 2
   retoma).
5. Mostre nomes de tipo, pasta e iteração — nunca `FR_`/`OT_`/uuids. Ao gravar, o contrário: enumeração (categoria,
   classificação, OTR, estado) vai pelo **identifier** que a `elm-ccm` lista para o atributo, nunca pelo nome; nome
   do `sdd.md` que não bate exato com nenhum valor → o valor cujo nome **começa** com ele, e diga qual foi usado.
6. **Campos que a PA exige** (os erros 403 "The '<atributo>' attribute needs to be set" dizem quais): a linha
   "Padrões do EWM" da seção ELM do `sdd.md` guarda os valores que o fluxo usa sempre (ex.: "Atendido por" /
   categoria do time na Tarefa; "Planejado para" é sempre a iteração da sprint — nada nasce no EWM fora dela);
   recusa por atributo que falta → mostre o atributo, peça o valor uma vez e ofereça gravá-lo nessa linha.
7. Nunca apague nada no ELM. Artefato que deixou de valer → peça à pessoa a marcação de obsoleto/remoção do módulo
   na UI (roteiro manual).

## Modo similares (antes de especificar — só leitura)

Chamado pela `sdd-prd` (e pela `sdd-triar`, para a regra da ficha de uma fatia padrão sem épico) **antes** de
criar qualquer HF, REG ou GL, e pelo modo requisitos antes de criar um
conceito novo. Só lê: não pede confirmação. Entrada: a lista de artefatos propostos — tipo (`HF` | `REG` | `GL`),
título provisório e 3–6 palavras-chave do domínio (termos do glossário, sinônimos que apareceram na entrevista,
valores e atores centrais).

1. **Bundle** (`rm.download.path` do `pa_*.json`, se existe), pelo MCP `okf`: um `okf_search` pelo título e um por
   palavra-chave (nunca a busca de texto nos arquivos). Anote a data do último sincronismo da `elm-sync`.
2. **DOORS Next ao vivo**, pela skill **`elm-rm`**: uma **buscar requisitos** por palavra-chave
   e pelo título (só `text` — com `folder`/`requirement_type` junto o DOORS Next devolve HTTP 400), filtrando o
   resultado pelos tipos do mapeamento do projeto; e **última modificação** dos já conhecidos desde o último sincronismo, para ver o que
   outro time criou ou mudou depois da `elm-sync`. Sem o power `elm` nesta sessão → só o bundle, e a saída diz
   `verificação no ELM ao vivo pendente`.
3. **Ler e classificar** cada acerto (corpo do bundle pelo `okf_get_document` com o `path`, ou `elm-rm` › **ler requisito**):
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
   Sem isso, ou com a **última modificação** mostrando artefato do mesmo tipo criado depois dessa data → rode o **modo
   similares** só para esse conceito. Acerto `igual` ou `sobrepõe` → **não cria**: mostre e devolva para a
   `sdd-prd` decidir (reutilizar ou alterar); o resto do lote segue.
1. **Tipo e pasta:** `type` → `rm.requirements-types`; `tags[0]` → `rm.folders` (`pa_*.json`). Não casou → pergunte
   uma vez; vale para o lote.
2. **Texto:** o corpo, sem a seção `## Relações` (ela é só local), com os links relativos trocados:
   - para uma **regra** já publicada → embed `[<id>](<id>)` e o id em `embedded` (HF → REG é sempre embed);
   - para um **termo** já publicado → hyperlink `[<id>](<id>)`;
   - para conceito ainda sem id → só o título, como texto;
   - link do bundle (`../03-Regras/2001-x.md`) ou URL do ELM → como está (o power `elm` resolve).
   O texto vai em **Markdown** direto (**criar/atualizar requisito** convertem).
3. **Criar** (sem `resource`) → `elm-rm` › **criar requisito** (tipo, pasta, título, texto, embutidos).
   **Atualizar** (com `id`) → confira o conflito (regra 3), mostre o diff do corpo e mande o texto inteiro com o
   `embedded` correto: `elm-rm` › **atualizar requisito** (id, título, texto, embutidos).
4. **Grave de volta** no conceito: `resource` = URL devolvida, `id`, e a entrada `{ id: elm, resource: <URL>,
   last_modified: <última modificação> }` em `sources`; `**Publication**` no `log.md`. Termos: o id também na coluna ELM
   do glossário do projeto.

Atributos (aprovação, prioridade) e links requisito ↔ requisito (*restringe*, *satisfaz*) ficam só nos conceitos:
o power `elm` não os grava. Roteiro manual se o processo do projeto os exigir no ELM (atributo, link, change set, módulo).
Depois: sugira a **`elm-sync`** para baixar ao bundle a versão oficial, que passa a ser a viva; os conceitos de
`elm/` ficam como registro, com `resource` preenchido. Commits na base, como todo artefato de produto.

## Modo backlog (épicos e fatias → EWM)

**Só nasce no EWM o que entra numa sprint:** o backlog do produto (épicos, fatias e atendimentos à espera) mora no
`backlog.md`; quem chama este modo é o modo *sprint*, quando o item entra na sprint — nunca a triagem, o PRD ou o
fatiamento. **Todo trabalho tem pai:** épico → IB → tarefa para o que vem de PRD; o épico de **Sustentação** (um por
release ou ano) para o resto. Ordem obrigatória de criação: épico, depois IB, depois tarefa. `Planejado para` = a
iteração da sprint, em todos.

1. **Épico — nasce na primeira sprint dele** (pela `[ESP]` da seção Especificação ou pela primeira fatia), antes
   dos filhos. Tipo do `sdd.md` (a PA pode não ter "Épico": então é um **Item de
   Backlog pai**), título `[EP-03] <título>`, descrição mínima (problema, quem pede, resultado esperado; depois do
   GATE, solução do PRD + link do PRD no repositório), responsável = o `po` da linha do épico e "Planejado para" = a
   iteração da sprint (não concluído na virada → só o `plannedFor` muda). Links **rastreia** → histórias, quando publicadas. Épico que nasce de um item do EWM (`origem: <id>` na
   `obs` da linha do épico): se o item já é do tipo de épico, ele é o épico; senão o item vira filho do épico novo
   (`elm-ccm` › **trocar o pai** para o épico).
2. **Sustentação e Atendimento** (uma vez por release/ano, se a linha `Sustentação:` do `backlog.md` estiver
   vazia): épico `[SUS-<ano>] Sustentação` e, filho dele, o IB `Atendimento` (pai das `[ATD]`); ids nessa linha.
   Junto, a tarefa **`[GB] Gerenciamento do backlog`**, filha do épico de Sustentação, responsável = o P.O. ativo
   do `equipe.json`, `plannedFor` = a iteração da sprint: recebe os commits do que não tem tarefa
   própria (a triagem); id na mesma linha (`· Backlog [GB] <id>`). Na virada, como as demais, só o `plannedFor` muda.
3. **Item de backlog por fatia** (quando a fatia entra na sprint):
   título `[FT-031] <título>`, `parent` = épico (fatia sem épico sem item de origem: o épico de
   Sustentação; com item de origem não há IB novo), pontos pelo tamanho só se o `sdd.md` tiver a tabela de pontos (opcional), descrição com modo
   AFK/HITL, `bloqueada por` e pasta prevista; responsável = P.O. (o IB é do produto; sem responsável a PA pode
   recusar qualquer mudança de estado depois); "Planejado para" = a iteração da sprint. **Critérios de aceite:** os
   cenários que a fatia cobre (`cobre`), em Dado / Quando / Então, copiados do PRD (fatia sem épico: da ficha —
   cenários ou comportamento esperado, conforme a trilha), no campo da linha "Critérios
   de aceite no IB" do `sdd.md` (Markdown; o power `elm` grava como texto rico) — sem o campo, numa seção "Critérios de
   aceite" da descrição. Fonte única é o PRD: o campo é cópia gerada, com o aviso "gerado do PRD — não edite
   aqui"; atualize quando a fatia for refinada ou a `sdd-consolidar` registrar mudança as-built. Links
   **implementa** → cada história que a fatia cobre; **depende de** → IBs das fatias em `bloqueada-por` (se o
   `link-types` tiver; senão fica na descrição).
4. **Fatia dividida:** conforme a linha do `sdd.md` — IBs novos filhos do IB original (que segue filho do épico),
   ou fecha o original e cria novos. Pai errado → `elm-ccm` › **trocar o pai**.
5. `backlog.md` (na base): `elm` de cada fatia/épico.

## Modo sprint (planejamento → iteração)

Entrada da `sdd-planejamento` (sempre chamada depois do "ok" da sprint): número da sprint, iteração, time e as três
seções do `sprint-<nn>.md` (fatias com responsável, revisor e verificador; especificação; reserva de atendimento).

1. **Planos**, por iteração e time — os dois tipos que o fluxo usa: **plano de backlog**
   (`com.ibm.team.apt.plantype.product.backlog`: épicos, IBs, Sustentação e "Atendimento") e **plano da sprint**
   (`com.ibm.team.apt.plantype.default`: as tarefas). Procure a iteração e os planos nesta
   ordem: (a) `ccm.iterations` do `pa_*.json`; (b) não estão lá → no EWM (`elm-setup` › **buscar iteração · listar
   planos**, pelo nome) — achou → grave em `ccm.iterations[<iteração>]` (com os planos) do `pa_*.json`, na
   confirmação do lote; (c) só o que não existe no EWM → proponha criar (`elm-setup` › **criar iteração · criar
   plano**; exige a permissão de modificar iterações — se falhar, peça a quem administra a PA). Plano criado → grave o
   id em `ccm.iterations[<iteração>].plans` do `pa_*.json` (com a confirmação do lote), para a próxima sprint achá-lo.
2. Linha `Sustentação:` vazia → crie a Sustentação e o Atendimento antes (item 2 do modo backlog): o
   atendimento depende deles e não passa pelo modo backlog. Fatias sem IB e épicos com `elm` `pendente` ou `—`
   (projeto com ELM) → modo backlog primeiro (a `[ESP]` nunca nasce sem pai). Para cada IB da sprint: `plannedFor` = iteração (o responsável
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
   horas. **`[APR]` não nasce aqui:** nasce no gate, pelo item 6, quando a fatia chega a ele (gate dispensado não
   deixa tarefa vazia).

   Fatia sem épico com item de origem → pai = o item (sem IB novo). Campos obrigatórios da Tarefa (categoria de horas, OTR, classificação, Clarity) pela
   `elm-ccm` (Criar), pela linha "Classificação da tarefa" do `sdd.md` e pela linha "Padrões do EWM" do `sdd.md` (regra 6).
   Grave os ids na coluna "Tarefa ELM" do `sprint-<nn>.md` (fatias: `DEV <id> · REV <id> · VER <id>`) e no `elm`
   do `backlog.md`. AT da seção Atendimento sem `elm` → modo *atendimento* (Registrar), no mesmo lote.
4. **Virada:** tarefas não concluídas (inclusive `[ESP]` e `[ATD]`), IBs e épicos não concluídos (inclusive
   Sustentação e Atendimento) → só o `plannedFor`
   muda para a nova iteração (o pai não muda; move, nunca recria); roteiro manual de **baseline** (componente RM +
   GC) se o projeto exige baseline por sprint.
5. **Troca AFK → HITL** (só chamada pela seção "Troca de modo" da `sdd-planejamento`, na base, com a decisão do P.O.
   ou do SM já registrada): cria a `[REV]` e a `[VER]` da fatia como no item 3 (mesmo pai da `[DEV]`, `plannedFor` =
   a iteração da sprint), com o revisor e o verificador da decisão; ids na coluna "Tarefa ELM" do `sprint-<nn>.md`
   e no `elm` do `backlog.md`. A `[DEV]` não muda. **HITL → AFK não existe:** nenhuma tarefa é cancelada por troca de
   modo.
6. **Aprovação `[APR]`** (chamada pela skill que abre o gate, quando a fatia chega a ele — nunca no planejamento):
   uma tarefa por gate humano que não tem tarefa de papel — `[APR] FT-<nnn> Aprovar plano` (GATE do plano:
   `sdd-plano` Passo 5, ou o `sdd-loop` na fase 4) e `[APR] FT-<nnn> Aprovar PR` (PR da fatia AFK: `sdd-implementar`
   Passo 5, ou o `sdd-loop` na fase 8). Responsável = o **Dev Sênior** que vai aprovar (quem chamou já escolheu),
   estimativa (pergunte), `plannedFor` = a iteração da sprint da fatia, o mesmo pai das outras tarefas da fatia (item
   3). Fica no estado inicial: quem aprova a assume (modo *assumir*), lança as horas e a conclui na aprovação. Já
   existe (prefixo, id e mesmo pai — regra 2) → não crie outra: depois de um ajuste ou de mudanças pedidas, a mesma
   `[APR]` volta a ser aprovada. Chamada da branch da fatia: o id vai para o campo ELM do `status.md` (a
   `sdd-consolidar` o leva ao `backlog.md` e ao `sprint-<nn>.md`).

## Modo assumir (Passo 0 das skills de papel)

Chamado pela skill do papel antes de trabalhar: `sdd-desenvolver` (`[DEV]`), `sdd-especificar` (`[ESP]`),
`sdd-revisar` (`[REV]` e `[APR]` do PR), `sdd-verificar` (`[VER]`), `sdd-plano` (`[APR]` do plano) e `sdd-atender`
(`[ATD]`). A regra mora só aqui.

1. **Tarefa:** a informada; senão pelo item — coluna `elm` do `backlog.md`, campo ELM do `status.md` da fatia ou
   coluna "Tarefa ELM" do `sprint-<nn>.md`. Não achou → a skill que chamou diz como criar (modo *sprint* ou
   *atendimento*); nunca crie tarefa por aqui.
2. **Leia** (`elm-ccm` › **ler item**) o responsável e o estado, e decida:

   | Situação | Ação |
   |---|---|
   | minha (`elm-ccm` › **quem sou eu**) e em andamento | **nada a fazer** — diga "já assumida" e siga |
   | sem responsável, ou minha e não iniciada | `elm-ccm` › **assumir tarefa** (responsável = quem sou eu, estado em andamento da PA, ex.: *Em Desenvolvimento*; estimativa se faltar — pergunte) |
   | de outra pessoa | mostre quem é e pergunte se assume no lugar dela; sem "sim", pare; com "sim", **assumir tarefa** como na linha acima |
   | concluída | `[DEV]`: só é concluída no merge — a fatia já foi mergeada: avise e pare (retrabalho não reabre a `[DEV]`, que segue em andamento até o merge). Outra tarefa (ex.: a `[REV]` que volta à revisão depois de um retrabalho pedido pela VER, a `[APR]` do plano num replanejamento): só se quem chamou disse **retrabalho**: duas transições, na mesma confirmação — `elm-ccm` › **reabrir tarefa** (ação que leva ao estado inicial da PA, ex.: *Novo*) e **assumir tarefa** (estado em andamento), mesmo que a PA tenha uma ação direta de concluída para em andamento (sem ação de reabertura → `ELM pendente [<tarefa> reabrir]` e aviso); fora disso → avise e pare |

3. **Uma** confirmação com o que muda (responsável, estado, estimativa); **atualizar item** com os campos e o
   `state` na mesma chamada.
   **`[DEV]` e o item de backlog:** ao iniciar a `[DEV]` de uma fatia com IB, leia o IB; ainda no estado inicial →
   na mesma confirmação, leve-o ao estado em andamento da PA (responsável continua o P.O.; sem responsável, grave o
   `po`/P.O. — a PA recusa mudança de estado sem ele). Assim a consolidação o encontra pronto para concluir.
4. Sem o power `elm` nesta sessão ou com falha → `ELM pendente [<tarefa> assumir]` onde a skill que chamou indicar, e siga.

## Modo atendimento

- **Registrar** (chamado pela `sdd-triar`): `[ATD] AT-<nnn> <título>`, filha do IB "Atendimento" (linha
  `Sustentação:` do `backlog.md`), `plannedFor` = a iteração da sprint em que o AT entrou (Kanban → a iteração corrente). AT
  sem sprint (`backlog`) não é registrado: a `[ATD]` nasce quando a triagem, o encaixe ou o planejamento o põe numa
  sprint. Responsável = quem vai atender, estimativa. Fica no
  estado inicial: quem atende a assume (modo *assumir*) ao executar.
- **Concluir** (chamado pela `sdd-atender`): depois do saldo de horas (modo horas), estado de conclusão da PA.

## Modo horas

**Lançar** é registro de empenho, não conclusão: a qualquer momento numa tarefa iniciada — ao fechar a sessão
(`sdd-status`), numa fronteira de fase, sob pedido ("lança 4h", "lança 6h de ontem") — e, na conclusão, só o saldo
(chamado pela skill do papel):
1. Tarefa: a informada; senão a atual — o `status.md` da branch dá a `[DEV]`, `[REV]`, `[VER]` ou `[APR]` do papel
   de quem pede; o AT aberto dá a `[ATD]`; a `[ESP]` vem do `sprint-<nn>.md`; a triagem e a consolidação (P.O. ou
   SM) lançam na `[GB]` da linha `Sustentação:` do `backlog.md`. Dúvida → pergunte.
2. `elm-ccm` › **horas lançadas** → mostre e desconte. Uma linha por data.
3. Confirme e `elm-ccm` › **lançar horas** (as regras do EWM — quem pode lançar, limite por dia, time code — são
   da `elm-ccm`; recusa dela → mostre o motivo e registre a pendência). Lançar não conclui a tarefa (tarefa de vários dias); concluir é
   do modo conclusão ou da skill que chamou.
4. Sem o power `elm` ou com falha → `ELM pendente [<chave>]: lançar <h>h em <tarefa> (<data>)` no `status.md`, no registro do AT ou no
   `sprint-<nn>.md`; este modo lança depois.

**Relatório** (virada ou sob pedido): **horas lançadas** das tarefas da sprint → horas por tipo (`[ESP]`
`[DEV]` `[REV]` `[VER]` `[APR]` `[ATD]`) e por pessoa, planejadas × lançadas, e as tarefas concluídas **sem horas** (só no
fechamento). Alimenta a retrospectiva e a recalibração da reserva de atendimento.

## Modo testes (cenários verificados → ETM)

Chamado pela `sdd-consolidar`, depois do merge e dos requisitos (as histórias já têm URL). Um caso de teste por
cenário **verificado** (`✅ aceito` no `verificacao.md`); o texto vem da linha dele no `CT.csv`.

1. Para cada cenário: título = o Resumo; descrição = a Descrição (sem as aspas do CSV); requisitos validados = a
   URL (`resource`) de cada história que o cenário cobre (fatia sem épico: a da regra da ficha). Idempotência: id já ao lado do cenário no
   `verificacao.md` → sem mudança (cada id é gravado assim que o caso nasce — passo 3).
2. Prévia e **uma** confirmação para o lote → `elm-qm` › **criar caso de teste** (o link **valida** vai na criação)
   → `elm-gc` › ligar item a caso de teste (**testado por**: IB → CT). `gc_context` se o ETM usar configuração
   global (`elm-gc`).
3. A cada caso criado, grave o id ao lado do cenário no `verificacao.md` e no campo ELM do `status.md`
   (`CT <id>, …`) — falha no meio: os já criados ficam registrados e o passo 1 retoma.
4. Falha (HTTP 403 sem permissão de criar no ETM, área sem criação de caso de teste por OSLC) ou sem o power →
   `ELM pendente [CT FT-<nnn> criar]: <cenários sem caso>` e o `CT.csv` como alternativa: `Importe no ETM (Importar
   → CSV)`; com os ids que a pessoa informar, `elm-qm` › **ler caso de teste** (URL), os links **valida** e
   **testado por**, os ids como no passo 3 e `ELM feito [CT FT-<nnn> criar]`.

## Modo especificação técnica (opcional, as-built)

Só se a linha ET da seção ELM do `sdd.md` disser `as-built no merge`, e **só chamado pela `sdd-consolidar`** —
pelo P.O. ou SM que consolida, no agente `sdd-produto` (que lê o código e grava em `.kiro/specs/*/elm/`); pedido
direto → "use a `sdd-consolidar`". Gere `ET - FT-031 <título>` a partir do `design.md` e do código **final, já
mergeado na base** (interfaces, contratos, dados, integrações, decisões técnicas — nada do que não foi feito),
grave-a como conceito OKF em `.kiro/specs/<ft>-<slug>/elm/ET-<slug>.md` (mesmo formato; `type` = o tipo de ET do
projeto), mostre, publique como os requisitos depois do `verified` humano de quem consolida, e ligue ao IB
(**implementa**).

## Modo conclusão

Uma tarefa por vez, chamada pela skill do papel que terminou (`[DEV]` no merge, `[REV]` ao aprovar, `[VER]` ao
aceitar — as duas depois do push conferido no remoto —, `[APR]` na aprovação do plano (depois do push) ou do PR
(antes, o comentário `PR aprovado, sha <sha>` pela `elm-ccm` › **comentar**: é ele que o merge confere), `[ESP]` no GATE do backlog, `[ATD]` ao finalizar) → estado de conclusão da PA (ação de
`elm-ccm` › **concluir tarefa**), depois do saldo de horas (modo horas). O IB da fatia, pela `sdd-consolidar` depois do
merge, e o épico quando todas as fatias concluírem: leia os estados e as ações do item e percorra as transições até
o estado de conclusão (ex.: *Em Desenvolvimento* → *Pronto*; ainda no inicial → passe pelo em andamento antes),
numa confirmação. O servidor aceitou e o estado não mudou, ou recusou por atributo → mostre a pré-condição (ex.:
responsável vazio) e registre `ELM pendente [IB FT-<nnn> concluir]` com ela. Na mesma confirmação, o comentário no IB
(`elm-ccm` › **comentar**): PR, pasta da fatia e ids publicados (requisitos, ET, casos de teste).

## Saída

```
🏛️ ELM — <modo> · <EP | FT | Sprint N>
Criados: <n> · Atualizados: <n> · Sem mudança: <n> · Links: <n> · Conflitos: <n resolvidos>
Pendências manuais: <lista | nenhuma>
```
