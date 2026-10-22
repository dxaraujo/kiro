---
name: sdd-plano
description: "Planeja uma fatia do fluxo sdd no formato de spec do Kiro — pesquisa o código primeiro (sdd-pesquisar), depois escreve requirements.md (critérios EARS falsificáveis, só o que a fatia cobre) ou bugfix.md (trilha rápida), design.md (pattern grounding, forma do programa: árvore de arquivos, assinaturas e árvore de chamadas, pontos de teste, contrato de pronto da verificação) e tasks.md (uma tarefa por comportamento, teste primeiro, comando de pronto); passa pela análise independente (rubrica L), pela sugestão de troca AFK → HITL quando o plano mostra risco e pelo GATE do plano pela senioridade de quem implementa (Júnior sempre, Pleno se pedir, Sênior nunca), aprovado por um Dev Sênior na tarefa [APR], pela sdd-revisar. Use em \"planeja a FT-031\", \"gera a spec\", \"cria as tasks\", \"replaneja\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.8.2"
---

# sdd-plano — Decidir o como antes de codar

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-plano/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

O plano existe para que as decisões de desenho sejam tomadas **com** uma pessoa, não descobertas por ela no
code review. Ele é curto, concreto e descartável: depois do merge, o que vale é o código, o ELM, o glossário e os
ADRs. Templates: [references/plano-templates.md](references/plano-templates.md).

Entrada: pasta `.kiro/specs/<ft>-<slug>/` criada pela `sdd-desenvolver`, na branch da fatia.
Leia: `status.md`, a fatia no `backlog.md`, o PRD do épico (histórias e regras cobertas), a ficha da fatia sem
épico (`<produto>/fatias/`) ou o defeito,
`.kiro/steering/sdd.md` (com as regras aprendidas) e o steering de tecnologia/estrutura.

## Passo 1 — Pesquisa

Sem `research.md` → **`sdd-pesquisar`** (de preferência pelo agente `sdd-pesquisador`). Trabalhe a partir do
arquivo, não da memória da leitura. Divergência entre o ELM e o código apontada na pesquisa → pergunte antes de
seguir (pode ser defeito, pode ser documentação velha).

## Passo 2 — Decisões em aberto

Lacuna de **negócio** (regra sem valor, exceção sem comportamento) → **pare**: é do P.O. — `sdd-entrevistar` e,
se mudar o PRD aprovado, `sdd-prd` (mudança depois de aprovado) — ou a ficha aprovada, `sdd-triar`. Nunca decida regra no plano.
Escolhas **técnicas** com alternativas reais (ex.: onde guardar o contador) → apresente-as à pessoa com a
recomendada (HITL) ou decida e registre (AFK) em "Decisões técnicas".

## Passo 3 — Escrever

0. **`.config.kiro`** (se não existe ou o `specType` não bate com a trilha): `specType` `feature` (padrão) ou `bugfix` (rápida) — é o que faz o painel
   de specs do Kiro reconhecer a pasta.
1. **`requirements.md`** (padrão) ou **`bugfix.md`** (trilha rápida). Cada critério EARS é **falsificável na
   base**: diga a observação que hoje mostra que ele é falso — se ela não existe, o critério já passa e não serve
   como teste.
2. **`design.md`**: pattern grounding (da research), **forma do programa** (árvore de arquivos com ação, assinaturas,
   árvore de chamadas — cada uma é uma decisão que, sem isso, seria tomada implicitamente no code review),
   pontos de teste (o mais alto possível), erros/transação/reexecução, **contrato de pronto** (como cada cenário
   será verificado de ponta a ponta) e decisões técnicas.
3. **`tasks.md`**: uma tarefa por comportamento, teste primeiro, comando de pronto, `_Requirements: N.M_`; a
   última é o checkpoint de validação completa + revisão.
4. Skills do toolkit ligadas ao agente: consulte a da stack para a forma do programa (camadas, nomes, testes).
5. Limite: plano que passa de ~200 linhas no total ou de ~8 tarefas → a fatia está grande: proponha à pessoa
   dividi-la (`sdd-fatiar`, refinamento) em vez de escrever um plano maior. Modo autônomo → `fase: bloqueada (de: planejando)`
   com a proposta de divisão.

`status.md`: fase `planejando` (vale também durante a análise do Passo 4).

## Passo 4 — Análise independente

Incremente "revisão do plano" em Rodadas. Peça ao agente **`sdd-revisor`** (subagente) a rubrica **L**
([../sdd-revisar/references/rubricas.md](../sdd-revisar/references/rubricas.md)) — passe só a pasta da fatia e a
rodada; ele grava o `analise-plano-<N>.md`. Sem subagente disponível (agente sem essa ferramenta, passo de workflow)
→ pare e devolva a quem chamou: "plano pronto para análise".
Assim que o relatório chegar (`OK` ou `AJUSTAR`), commite-o **com o `status.md`** (Rodadas, Histórico) —
mensagem no padrão do `sdd.md`, com o texto `registrar análise do plano <N>`. O GATE e a implementação citam esse
arquivo; ele precisa estar na branch.
- `ANALISE: OK` → Passo 5.
- `AJUSTAR`: falta **do plano** → corrija e peça nova análise (até 2 rodadas); falta **do PRD** → Passo 2.

## Passo 5 — Troca de modo e GATE do plano

### Fatia AFK com risco → sugerir HITL

`Modo: AFK` e o plano mostra risco — regra de negócio sensível, muitos cenários, integração externa, mudança de
dado (diga qual) → **sugira** ao Dev trocar para HITL. A troca é do P.O. (ou do SM), na base; aqui só se para.
**HITL → AFK nunca:** nem sugira nem aceite.

- Dev não aceita → o GATE abaixo, no AFK.
- Dev aceita → `fase: bloqueada (de: planejando)`, Bloqueio `aguardando troca para HITL` · motivo: `<risco>`, linha
  no Histórico; commit com os artefatos do plano e o `status.md` (`registrar plano`) → push → conferir no remoto
  (itens 1–3 da Entrega do Passo 5 da [`sdd-implementar`](../sdd-implementar/SKILL.md)) → horas da sessão na
  `[DEV]` (`sdd-elm` modo *horas*, com "sim"; sem o power `elm` → `ELM pendente [<chave>]`) — ela fica
  **interrompida**, sem conclusão → avise o P.O. (troca pela `sdd-planejamento`, seção Troca de modo). Não troque
  de branch nem grave na base. A sessão pode ser encerrada: feita a troca, o Dev retoma pela `sdd-iniciar` →
  `sdd-desenvolver`, que sincroniza o `status.md` e devolve a fatia a este Passo 5, já no HITL.

### GATE do plano — pela senioridade de quem implementa

```
🧭 Plano FT-<nnn> — <título> · trilha <…> · modo <AFK|HITL> · Dev <login> (<senioridade>)
Requisitos: <n> (<c> critérios) · Tarefas: <n> · Arquivos: <criar n · alterar n>
Análogo: <…> · Pontos de teste: <…> · Decisões técnicas: <lista curta>
Testes existentes que mudam: <nenhum | lista>
Contrato de pronto: <n> cenários, executados por <API | job | browser | carga>
Análise: OK na rodada <N>
Leia de preferência: forma do programa e contrato de pronto.
```

A `senioridade` de quem implementa (o `Responsável` do `status.md`; no loop, quem disparou) no `equipe.json` da
base decide — trilha e modo não entram:

| Senioridade | GATE |
|---|---|
| **Júnior** | sempre: um Dev Sênior aprova |
| **Pleno** | **pergunte** se ele quer a aprovação de um Dev Sênior (recomende "sim" quando o plano muda a expectativa de um teste existente). Sim → como o Júnior; não → `fase: implementando`, Histórico `Pleno dispensou o GATE do plano` |
| **Sênior** | nunca: ele aprova o próprio plano — `fase: implementando`, Histórico `plano do Sênior` —, inclusive quando o plano muda a expectativa de um teste existente |

**Com GATE** (Júnior, ou Pleno que pediu): pergunte qual Dev Sênior aprova — sugira o que vai revisar o PR (coluna
Revisor do `sprint-<nn>.md` ou Histórico do `status.md`); AFK, sem revisor: um Dev Sênior ativo que não é quem
implementa. Então `fase: plano-em-revisao` (conta no WIP de revisão humana), `Responsável` = quem aprova, e a tarefa
**`[APR] FT-<nnn> Aprovar plano`** para ele (`sdd-elm` modo *sprint*, item 6, com "sim"; o id no campo ELM do
`status.md`; sem o power `elm` → `ELM pendente [APR FT-<nnn> criar]`). Commit com `research.md`, `.config.kiro`,
`requirements.md`/`bugfix.md`, `design.md`, `tasks.md` e `status.md` (`registrar plano`) → push → conferir no remoto
(itens 1–3 da Entrega do Passo 5 da `sdd-implementar`) — quem aprova lê o plano no remoto → horas da sessão na
`[DEV]` (lança, não conclui) → avise o aprovador (`sdd-revisar`, Aprovação do plano).

**Sem GATE** (Sênior, ou Pleno que dispensou): `fase: implementando`, a linha no Histórico e **um commit** com os
mesmos arquivos (`registrar plano`). Próximo: **`sdd-implementar`** — numa sessão nova, de preferência (o plano está
no disco; o contexto da pesquisa não é mais necessário).

Retomando em `plano-em-revisao` sem `[APR]` (receita de workflow, pendência `[APR FT-<nnn> criar]`) → faça agora a
pergunta ao Pleno, ou crie a `[APR]` (Júnior, Pleno que pediu).

### Quem aprova

A aprovação é do Dev Sênior da `[APR]`, na sessão dele, pela **`sdd-revisar`** (seção "Aprovação do plano") —
nunca nesta skill nem na sessão de quem implementa.

## Replanejar

Implementação descobriu que o plano não serve (esperado × encontrado) → atualize `design.md`/`tasks.md` só no que
mudou, acrescente tarefas (nunca desmarque as prontas), registre o motivo no Histórico e repita os Passos 4–5 para
a parte alterada (com GATE e a `[APR]` já concluída → o aprovador a reabre pela `sdd-revisar`: modo *assumir* com retrabalho).

## Modo autônomo

`AUTONOMO=true`: sem perguntas; decisão técnica com alternativas → escolha a recomendada e registre; lacuna de
negócio → `fase: bloqueada (de: planejando)` com a pergunta para o P.O. Passo 5 sem pessoa: fatia AFK com risco →
`fase: bloqueada (de: planejando)`, `aguardando troca para HITL` com o risco (a sugestão vai ao P.O.); GATE → Sênior
segue para `implementando`; Pleno → a escolha do lote que quem chamou passou (sem ela: `plano-em-revisao`, e a
pergunta fica para a sessão dele); nada de ELM (`ELM pendente`).

## Regras

- Não invoque nem simule outra skill do fluxo: termine dizendo a próxima (`sdd-implementar`, o Dev Sênior da `[APR]`
  ou o P.O. na troca de modo) e pare. A `sdd-pesquisar`, o subagente revisor e a `sdd-elm`, que os passos mandam
  chamar, fazem parte desta skill.
