---
name: sdd2-plano
description: "Planeja uma fatia do fluxo sdd2 no formato de spec do Kiro — pesquisa o código primeiro (sdd2-pesquisar), depois escreve requirements.md (critérios EARS falsificáveis, só o que a fatia cobre) ou bugfix.md (trilha rápida), design.md (pattern grounding, forma do programa: árvore de arquivos, assinaturas e árvore de chamadas, pontos de teste, contrato de pronto da verificação) e tasks.md (uma tarefa por comportamento, teste primeiro, comando de pronto); passa pela análise independente (rubrica L) e pelo GATE do plano, a revisão humana de maior alavanca. Use em \"planeja a FT-031\", \"gera a spec\", \"cria as tasks\", \"aprova o plano\", \"replaneja\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-plano — Decidir o como antes de codar

O plano existe para que as decisões de desenho sejam tomadas **com** uma pessoa, não descobertas por ela no
code review. Ele é curto, concreto e descartável: depois do merge, o que vale é o código, o ELM, o glossário e os
ADRs. Templates: [references/plano-templates.md](references/plano-templates.md).

Entrada: pasta `.kiro/specs/<ft>-<slug>/` criada pela `sdd2-iniciar`, na branch da fatia.
Leia: `status.md`, a fatia no `backlog.json`, o PRD do épico (histórias e regras cobertas) ou o defeito,
`.kiro/steering/sdd2-projeto.md`, o steering de tecnologia/estrutura e `.kiro/steering/sdd2-licoes.md`.

## Passo 1 — Pesquisa

Sem `research.md` → **`sdd2-pesquisar`** (de preferência pelo agente `sdd2-pesquisador`). Trabalhe a partir do
arquivo, não da memória da leitura. Divergência entre o ELM e o código apontada na pesquisa → pergunte antes de
seguir (pode ser defeito, pode ser documentação velha).

## Passo 2 — Decisões em aberto

Lacuna de **negócio** (regra sem valor, exceção sem comportamento) → **pare**: é do P.O. — `sdd2-entrevistar` e,
se mudar o PRD aprovado, `sdd2-prd` (mudança depois de aprovado). Nunca decida regra no plano.
Escolhas **técnicas** com alternativas reais (ex.: onde guardar o contador) → apresente-as à pessoa com a
recomendada (HITL) ou decida e registre (AFK) em "Decisões técnicas".

## Passo 3 — Escrever

0. **`.config.kiro`** (se não existe): `specType` `feature` (padrão) ou `bugfix` (rápida) — é o que faz o painel
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
5. Limite: plano que passa de ~200 linhas no total ou de ~8 tarefas → a fatia está grande: volte à `sdd2-fatiar`
   (dividir) em vez de escrever um plano maior.

`status.md`: fase `planejando` → `plano-em-revisao`.

## Passo 4 — Análise independente

Peça ao agente **`sdd2-revisor`** a rubrica **L** ([../sdd2-revisar/references/rubricas.md](../sdd2-revisar/references/rubricas.md))
— passe só a pasta da fatia e a rodada. Grave como `analise-plano-<N>.md`.
- `ANALISE: OK` → Passo 5.
- `AJUSTAR`: falta **do plano** → corrija e peça nova análise (até 2 rodadas); falta **do PRD** → Passo 2.

## Passo 5 — GATE do plano

```
🧭 Plano FT-<nnn> — <título> · trilha <…> · modo <AFK|HITL>
Requisitos: <n> (<c> critérios) · Tarefas: <n> · Arquivos: <criar n · alterar n>
Análogo: <…> · Pontos de teste: <…> · Decisões técnicas: <lista curta>
Contrato de pronto: <n> cenários, executados por <API | job | browser | carga>
Análise: OK na rodada <N>
Aprovar? Leia de preferência: forma do programa e contrato de pronto.
```

- **HITL** → sempre uma pessoa aprova. Sugira que seja quem vai revisar o PR (alinha antes do código).
- **AFK** → o `sdd2-projeto.md` decide (`Plano AFK: aprovação humana | análise basta`). Com "análise basta", a
  fatia segue com `ANALISE: OK`; a pessoa revisa no PR.
- Aprovado → `fase: implementando`, linha no Histórico (quem aprovou), commit dos arquivos do plano. Próximo:
  **`sdd2-implementar`** — numa sessão nova, de preferência (o plano está no disco; o contexto da pesquisa não é
  mais necessário).

## Replanejar

Implementação descobriu que o plano não serve (esperado × encontrado) → atualize `design.md`/`tasks.md` só no que
mudou, acrescente tarefas (nunca desmarque as prontas), registre o motivo no Histórico e repita os Passos 4–5 para
a parte alterada.

## Modo autônomo

`AUTONOMO=true`: sem perguntas; decisão técnica com alternativas → escolha a recomendada e registre; lacuna de
negócio → `fase: bloqueada` com a pergunta para o P.O.
