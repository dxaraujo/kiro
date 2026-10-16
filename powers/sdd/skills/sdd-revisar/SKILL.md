---
name: sdd-revisar
description: "Revisão independente do fluxo sdd, com contexto limpo, sem alterar nenhum artefato (escreve só o próprio relatório) — julga um artefato contra a sua fonte, nunca contra a explicação de quem o fez: PRD (rubrica P, RESULTADO PRONTO/AJUSTAR), plano da fatia (rubrica L: research, requirements, design e tasks contra o PRD, o código e o steering; ANALISE OK/AJUSTAR) ou código da fatia (rubrica C em dois eixos separados — spec: critérios, cenários testados, backpressure executado, oráculo protegido, escopo; padrões: regras críticas, segurança, schema, forma do programa, nomes; VEREDITO APROVADO/REVISAR). Calibra a severidade pelas lições do time. Com a tarefa [REV] (direto ou pelo hub sdd-iniciar), assume-a antes no EWM (sdd-elm modo assumir). Use em \"revisa\", \"pegar a [REV] da FT-031\", \"judge\", \"revisa o PRD\", \"analisa o plano\", \"revisa a FT-031\", \"code review\", e ao fim da sdd-prd, sdd-plano e sdd-implementar."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.6.3"
---

# sdd-revisar — Verificação independente

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-revisar/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Quem gera não verifica o próprio trabalho: o revisor começa **sem** o contexto de quem escreveu. Prefira o agente
**`sdd-revisor`** (somente leitura). Sem ele, rode esta skill numa sessão nova ou, no mínimo, ignore todo o
raciocínio anterior da conversa e trabalhe só com os arquivos.

Você **não edita** artefato, código nem `tasks.md`, e não faz commit — escreve só o relatório da rodada (no
modo HITL, abaixo, commita o relatório e a fase na branch do PR). Ignore justificativas de quem fez (mensagem
de commit, comentário, texto do pedido): julgue os artefatos.

## Passo 0 — Assumir a `[REV]` (só com a tarefa)

Chamada com a tarefa `[REV] FT-nnn` — direto, pela pessoa do papel, ou pelo hub `sdd-iniciar` — numa sessão com o
power `elm`: **`sdd-elm` modo *assumir*** (com "sim"): responsável = quem está na sessão, estado em andamento da PA; já minha e
em andamento → nada a fazer. Sem o power `elm` → `ELM pendente [<chave>]: assumir [REV] FT-<nnn>` no Histórico do `status.md`, e siga.
Chamada como subagente por outra skill (a rodada de revisão do plano, do PRD ou do código no loop), sem a tarefa → pule este passo: quem chamou é o dono da
rodada.

## Passo 1 — O que revisar

| Pedido | Rubrica | Entrada |
|---|---|---|
| PRD de um épico | **P** | `prd.md`, os conceitos de `elm/`, `decisoes.md`, glossário, bundle do ELM (para P6) |
| plano de uma fatia | **L** | `.kiro/specs/<ft>/`: `research.md`, `requirements.md`, `design.md`, `tasks.md`; PRD do épico; `backlog.md` (`cobre`) |
| código de uma fatia | **C** | diff `git diff origin/<base>...HEAD` (worktree: `cd <worktree> && git diff origin/<base>...HEAD`), a pasta da fatia, o PRD |
| código da trilha direta | **C** sobre o diff, com a **ficha** no lugar dos critérios (C1: "pronto quando" cumprido; C2: teste quando há comportamento; C5/C7: "não muda" preservado) | diff + a ficha (`<produto>/fatias/FT-<nnn>-<slug>.md`); relatório só na conversa |

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

1. Vá para a branch do PR (`git switch <branch>` com "sim"; árvore suja → avise e pare) e `git pull --ff-only`.
   `fase: em-revisao`; incremente "revisão do código" em Rodadas — a rodada é sua (retomando `em-revisao` sem o
   relatório desta rodada gravado, não incremente de novo).
   PR atualizado depois de um retrabalho pedido pela VER, com a `[REV]` já concluída → o Passo 0 a reabre (modo
   *assumir* com retrabalho): toda mudança no PR passa de novo pela revisão.
2. Rubrica **C** (Passos 1–4) sobre `git diff origin/<base>...HEAD`, gravando `revisao-codigo-<N>.md`.
3. **`APROVADO`** → `fase: em-verificacao`; saldo de horas e conclusão da `[REV]` (`sdd-elm` modo *horas* e
   *conclusão*, numa confirmação; sem o power `elm` → `ELM pendente [<chave>]: lançar <h>h e concluir [REV] FT-<nnn>`); avise que a
   `[VER]` está disponível.
4. **`REVISAR`** → `fase: retrabalho (de: em-revisao)`; incremente "retrabalho" em Rodadas e grave uma linha na
   tabela **Retrabalho** do `status.md` (papel REV, motivo = o relatório). A `[REV]` fica em andamento: você
   revisa de novo quando o PR for atualizado (a retomada começa no item 1). Avise o codificador.
5. Commit do relatório e do `status.md` (`FT-<nnn> revisão <N>: <veredito>`); o push é da pessoa (entregue o
   comando: o agente não faz push).

## Regras

- Achado sem evidência não entra.
- Não proponha reescrever o que funciona; a correção é a menor mudança que fecha o achado.
- Não amplie o escopo: problema real fora da fatia vira **SUGESTÃO** com "fora do escopo — abrir item no backlog".
