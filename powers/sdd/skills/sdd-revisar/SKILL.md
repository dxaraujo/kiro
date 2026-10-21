---
name: sdd-revisar
description: "Revisão independente do fluxo sdd, com contexto limpo, sem alterar nenhum artefato (escreve só o próprio relatório) — julga um artefato contra a sua fonte, nunca contra a explicação de quem o fez: PRD (rubrica P, RESULTADO PRONTO/AJUSTAR), plano da fatia (rubrica L: research, requirements, design e tasks contra o PRD, o código e o steering; ANALISE OK/AJUSTAR) ou código da fatia (rubrica C em dois eixos separados — spec: critérios, cenários testados, backpressure executado, oráculo protegido, escopo; padrões: regras críticas, segurança, schema, forma do programa, nomes; VEREDITO APROVADO/REVISAR). Calibra a severidade pelas lições do time. Com a tarefa [REV] (direto ou pelo hub sdd-iniciar), assume-a antes no EWM (sdd-elm modo assumir). Com a tarefa [APR] Aprovar PR (fatia AFK em pronta-para-merge), um Dev Sênior lê o PR e aprova ou pede mudanças. Use em \"revisa\", \"pegar a [REV] da FT-031\", \"[APR] Aprovar PR\", \"aprovar o PR da FT-031\", \"judge\", \"revisa o PRD\", \"analisa o plano\", \"revisa a FT-031\", \"code review\", e ao fim da sdd-prd, sdd-plano e sdd-implementar."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.7.0"
---

# sdd-revisar — Verificação independente

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-revisar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Quem gera não verifica o próprio trabalho: o revisor começa **sem** o contexto de quem escreveu. Prefira o agente
**`sdd-revisor`** (somente leitura). Sem ele, rode esta skill numa sessão nova ou, no mínimo, ignore todo o
raciocínio anterior da conversa e trabalhe só com os arquivos.

Você **não edita** artefato, código nem `tasks.md`, e não faz commit — escreve só o relatório da rodada (no
modo HITL, abaixo, commita o relatório e a fase na branch do PR e faz o push dela; na aprovação do PR do AFK, só
nas mudanças pedidas). Ignore justificativas de quem fez (mensagem
de commit, comentário, texto do pedido): julgue os artefatos.

## Passo 0 — Assumir a `[REV]` (só com a tarefa)

Chamada com a tarefa `[REV] FT-nnn` — direto, pela pessoa do papel, ou pelo hub `sdd-iniciar`: antes de tudo,
quem está na sessão tem de ser **Dev Sênior** ativo (`papeis` com `Dev` e `senioridade` `Sênior` no `equipe.json`
da base) — a `[REV]` é sempre de um Dev Sênior. Não é → diga isso, quem são os Dev Sêniores ativos, e pare. É quem
implementa a fatia (o `responsavel`) → só se for o único Dev Sênior ativo (`revisor único` na Observação da fatia no
`sprint-<nn>.md` ou, na fatia puxada, no Histórico do `status.md`); senão diga quem pode revisar e pare. Numa sessão com o
power `elm`: **`sdd-elm` modo *assumir*** (com "sim"): responsável = quem está na sessão, estado em andamento da PA; já minha e
em andamento → nada a fazer. Sem o power `elm` → `ELM pendente [<chave>]: assumir [REV] FT-<nnn>` no Histórico do `status.md`, e siga.
Chamada como subagente por outra skill (a rodada de revisão do plano, do PRD ou do código no loop), sem a tarefa → pule este passo: quem chamou é o dono da
rodada.

## Passo 1 — O que revisar

| Pedido | Rubrica | Entrada |
|---|---|---|
| PRD de um épico | **P** | `prd.md`, os conceitos de `elm/`, `decisoes.md`, glossário, bundle do ELM pelo `okf` (para P6) |
| plano de uma fatia | **L** | `.kiro/specs/<ft>/`: `research.md`, `requirements.md`, `design.md`, `tasks.md`; PRD do épico; `backlog.md` (`cobre`) |
| código de uma fatia | **C** | diff `git diff origin/<base>...HEAD` (worktree: `cd <worktree> && git diff origin/<base>...HEAD`), a pasta da fatia, o PRD |

Rubricas em [references/rubricas.md](references/rubricas.md) — leia a do pedido inteira antes de começar.
Sempre: `.kiro/steering/sdd.md` (comandos, regras críticas), o steering de tecnologia e estrutura que ele
aponta e as regras aprendidas (última seção do `sdd.md`).

## Passo 2 — Coletar evidência

- **P/L:** cruze item a item (cenário → critério → tarefa; regra → origem). Para L4 abra os caminhos citados.
- **C:** comece por `git diff --stat`; leia o diff inteiro dos arquivos de produção e de teste. **Execute** os
  comandos de backpressure (C3) — não confie em "os testes passaram" de ninguém. Procure no diff por testes
  removidos ou enfraquecidos (`git diff --diff-filter=D --name-only`, `@Disabled`, `@Ignore`, `skip`, `xit`,
  `assertTrue(true)`, asserts apagados, `catch` vazio) — C4. Avalie os dois eixos separadamente; com subagentes
  disponíveis, um revisor por eixo, em paralelo.
- Banco só por MCP de consulta, somente leitura (`SELECT`/`WITH`).

## Passo 3 — Calibrar

Para cada achado IMPORTANTE ou SUGESTÃO, veja em `<produto>/aprendizado/licoes.md` se o mesmo tipo de problema já
escapou de uma revisão antes (lição com causa `revisao-branda`): suba uma severidade. Lições promovidas
(seção Regras aprendidas do `sdd.md`) valem como itens da rubrica — o revisor é quem mais as usa.

## Passo 4 — Relatório

No formato do fim de [references/rubricas.md](references/rubricas.md). A **última linha** é exatamente o fecho
da rubrica. Grave o relatório na pasta do artefato — `revisao-prd-<N>.md` (épico), `analise-plano-<N>.md` ou
`revisao-codigo-<N>.md` (fatia), `<N>` = a rodada que quem chamou passou (sem ela: 1 + o maior `<N>` já existente na pasta; HITL: a sua) — e, se quem chamou pediu (workflow, loop), o veredito em
`.kiro/local/wf/<id>/`: `plano.json` (`{"resultado": "OK"}` · `{"resultado": "AJUSTAR"}`) ou `codigo.json` (`{"veredito": "APROVADO"}` ·
`{"veredito": "REVISAR"}`). São os **únicos** arquivos que você escreve.

Zero BLOQUEANTE e zero IMPORTANTE → aprovado. Sugestões nunca reprovam.

## Modo HITL — a `[REV]` sobre o PR

Fatia `Modo: HITL` com a tarefa `[REV]` assumida (Passo 0) e `fase: pr-aberto` (ou `em-revisao`, retomando) — a
revisão oficial é sua, na sua sessão:

1. Leia o PR pelo `gitlab_obter_mr` (iid do link no `status.md`): `merged` ou `closed` → avise e pare;
   `conflitos` → anote no relatório. Vá para a branch do PR (`git switch <branch>` com "sim"; árvore suja → avise e pare; aberta numa worktree → trabalhe nela, regra da `sdd-desenvolver`, Passo 1) e `git pull --ff-only`.
   `fase: em-revisao`; incremente "revisão do código" em Rodadas — a rodada é sua (retomando `em-revisao` sem o
   relatório desta rodada gravado, não incremente de novo).
   PR atualizado depois de um retrabalho pedido pela VER, com a `[REV]` já concluída → o Passo 0 a reabre (modo
   *assumir* com retrabalho): toda mudança no PR passa de novo pela revisão.
2. Rubrica **C** (Passos 1–4) sobre `git diff origin/<base>...HEAD`, gravando `revisao-codigo-<N>.md`.
   Grave o campo **Drift de negócio** do `status.md` com a penúltima linha do relatório (só sobe de `não` para
   `sim`; outro `sim` acrescenta o motivo) — a consolidação só lê esse campo.
3. **`APROVADO`** → `fase: em-verificacao`.
4. **`REVISAR`** → `fase: retrabalho (de: em-revisao)`; incremente "retrabalho" em Rodadas e grave uma linha na
   tabela **Retrabalho** do `status.md` (papel REV, motivo = o relatório). A `[REV]` fica em andamento: você
   revisa de novo quando o PR for atualizado (a retomada começa no item 1).
5. **Entrega**, nesta ordem — o próximo só acha o seu trabalho no remoto:
   1. commit do relatório e do `status.md` (`FT-<nnn> revisão <N>: <veredito>`);
   2. push da branch do PR (`git push origin <branch>`, nunca a base; o Kiro pergunta). Sem a pergunta (agente na
      V2, push negado) → entregue o comando pronto e espere a pessoa dizer que publicou;
   3. **confira no remoto:** `git fetch` e `git rev-parse HEAD` = `git rev-parse origin/<branch>`. Diferente → não
      siga: diga o que falta;
   4. só então: `APROVADO` → saldo de horas e conclusão da `[REV]` (`sdd-elm` modo *horas* e *conclusão*, numa
      confirmação; sem o power `elm` → `ELM pendente [<chave>]: lançar <h>h e concluir [REV] FT-<nnn>`) e avise o
      verificador de que a `[VER]` está disponível; `REVISAR` → avise o Dev responsável (o retrabalho é dele, no
      mesmo PR).

## Aprovação do PR — a `[APR]`

Fatia `Modo: AFK` em `fase: pronta-para-merge`, com a tarefa `[APR] FT-<nnn> Aprovar PR` (pelo hub ou direto). A
revisão e a verificação já foram feitas por subagentes; aqui uma pessoa **lê o código** e decide.

1. Quem está na sessão é **Dev Sênior** ativo (`senioridade` no `equipe.json` da base) e o responsável pela `[APR]`
   (sem o power `elm`, quem o Dev indicou)? Não → diga quem é e pare. PR de um Sênior (o `Responsável` da fatia) →
   outro Sênior aprova; ele mesmo só quando é o **único** Dev Sênior ativo.
2. Leia o PR pelo `gitlab_obter_mr` (iid do link no `status.md`): `merged` ou `closed` → avise e pare. Vá para a
   branch do PR (`git switch <branch>` com "sim"; árvore suja → avise e pare; aberta numa worktree → trabalhe nela,
   regra da `sdd-desenvolver`, Passo 1) e `git pull --ff-only`; a fase tem de
   ser `pronta-para-merge`. Anote o `sha` = `git rev-parse origin/<branch>` (o do PR).
3. **`sdd-elm` modo *assumir*** a `[APR]`.
4. Mostre o caminho de leitura: o texto do PR ("Como ler"), o `revisao-codigo-<N>.md` aprovado, as evidências do
   `verificacao.md` e os ADRs do PR (`adr/` da pasta da fatia — C15: a pessoa julga se cada um descreve a decisão). **Execute** o backpressure (C3) — não confie no relatório. A leitura do código é da pessoa:
   você aponta, ela decide.
5. **Aprovado** → **não commite na branch** (o `sha` que o Dev vai mergear não pode mudar): pela `sdd-elm`, numa
   confirmação, o comentário `PR aprovado, sha <sha>` na `[APR]` (`elm-ccm` › **comentar**), o saldo de horas e a
   conclusão (modos *horas* e *conclusão*). Avise o Dev responsável: o merge é dele (Passo 6 da `sdd-desenvolver`),
   que confere essa `[APR]`. Sem o power `elm` → entregue ao Dev a linha `PR aprovado por <login>, sha <sha>` e a
   pendência `ELM pendente [APR FT-<nnn> concluir]: lançar <h>h e concluir (<login>)` — ele as grava no commit do
   merge.
6. **Mudanças pedidas** → cada uma em Achados abertos (origem: PR), `fase: retrabalho (de: pronta-para-merge)`,
   "retrabalho" + 1 em Rodadas e uma linha na tabela Retrabalho (papel APR). Commit
   (`FT-<nnn> aprovação do PR: mudanças pedidas`) → push → conferir no remoto (como no item 5 do modo HITL) → horas
   da sessão na `[APR]` (lança, não conclui) → avise o Dev responsável. A `[APR]` fica em andamento e é a mesma na
   nova aprovação.

## Regras

- Achado sem evidência não entra.
- Não proponha reescrever o que funciona; a correção é a menor mudança que fecha o achado.
- Não amplie o escopo: problema real fora da fatia vira **SUGESTÃO** com "fora do escopo — abrir item no backlog".
- Não invoque nem simule outra skill do fluxo: termine com o veredito (e, com a tarefa, o aviso ao próximo papel) e
  pare. Como subagente, devolva o relatório a quem chamou.
