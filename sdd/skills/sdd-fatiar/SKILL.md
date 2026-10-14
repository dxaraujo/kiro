---
name: sdd2-fatiar
description: "Quebra um PRD aprovado do fluxo sdd2 em fatias verticais (tracer bullets) — cada fatia atravessa todas as camadas, entrega um comportamento verificável de ponta a ponta, cita as histórias e cenários que cobre, as dependências (bloqueada por), o tamanho (P/M/G, nunca maior) e o modo de autonomia (AFK: o agente faz sozinho até o PR · HITL: precisa de uma pessoa no meio). Grava o backlog em <produto>/backlog.json, conduz o GATE do backlog e, com ELM, publica as fatias como itens de backlog no EWM pela sdd2-elm. Use em \"fatiar o PRD\", \"quebrar em histórias\", \"gerar o backlog\", \"criar os itens de backlog\", \"PRD para issues\", \"refinar o backlog\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-fatiar — PRD → fatias verticais

Entrada: PRD `aprovado` (`<produto>/epicos/<EP>-<slug>/prd.md`). Saída: fatias no
`<produto>/backlog.json` (formato em [references/backlog.md](references/backlog.md)) e a visão humana
`<produto>/backlog.md`, regenerada a partir do JSON.

## O que é uma boa fatia

- **Vertical (tracer bullet):** atravessa entrada → regra → dado → saída. "Criar a tabela", "fazer o DAO" ou
  "tela sem backend" **não** são fatias. A primeira fatia de um épico é a mais fina que prova o caminho inteiro
  (um cenário feliz, ponta a ponta); as seguintes engrossam.
- **Verificável sozinha:** tem cenários de aceite do PRD (`HF-01 · 1.1, 1.2`) que passam ao fim dela.
- **Cabe numa janela de contexto nova:** um agente pesquisa, planeja e implementa a fatia sem perder o fio, e uma
  pessoa revisa o PR numa sentada. Tamanho `P` (horas), `M` (≈ 1 dia), `G` (2–3 dias); maior que `G` → divida.
- **Nem fina demais:** doze fatias para uma mudança de três linhas é o erro mais comum. Teste de cada fatia:
  *"o que dá para demonstrar quando ela terminar?"* — se a resposta é "nada visível", junte com a vizinha.
- **Critério falsificável:** cada cenário coberto falha hoje, na base (diga a observação que mostra isso). Cenário
  que já passa não prova nada; cenário que só outra fatia consegue fazer passar está na fatia errada.
- **Preparação antes:** se a mudança exige mexer em código compartilhado, a primeira fatia deixa a mudança fácil
  (prefactoring) e a seguinte faz a mudança. Refatoração larga: expandir → migrar em lotes → contrair.
- **Independente quando der:** dependência só quando uma fatia precisa de algo que outra entrega (`bloqueada-por`).
- **Autonomia declarada:**
  - `AFK` — critérios claros, padrão conhecido no código, backpressure forte (testes e verificação automatizáveis),
    sem decisão de produto ou de UX no caminho: o agente pode ir do plano ao PR sem pessoa (a pessoa revisa o PR).
  - `HITL` — tem decisão de design, UX, integração nova, dado sensível ou risco alto: uma pessoa acompanha o plano e
    a implementação.
  - Tipo de trabalho novo no projeto começa `HITL`; vira `AFK` depois que fatias parecidas chegaram ao PR sem
    correção humana (a `sdd2-aprender` mostra isso na retrospectiva).

## Passo 1 — Rascunho

1. Leia o PRD inteiro e o `decisoes.md`. Releia o código das fatias que mexem
   em módulos existentes (subagente `sdd2-pesquisador`, se houver) — a fatia tem de ser possível no código real.
2. Monte a lista:

```
| FT | Título (comportamento, linguagem do negócio) | Cobre | Bloqueada por | Tam. | Modo |
|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas inválidas | HF-01 · 1.1, 1.2 · REG-01 | — | M | AFK |
| FT-032 | Desbloquear automaticamente após 30 min | HF-01 · 1.3 · REG-02 | FT-031 | P | AFK |
| FT-033 | Avisar o usuário do bloqueio por e-mail | HF-02 · 2.1–2.3 | FT-031 | M | HITL (texto do e-mail) |
```

3. Confira a **cobertura**: todo cenário de todas as histórias do PRD aparece em exatamente uma fatia (cenário
   compartilhado → a primeira que o entrega). Cenário sem fatia ou fatia sem cenário → corrija antes de mostrar.

## Passo 2 — Perguntar à pessoa (uma vez, com a tabela)

```
🍰 EP-<nn> — <n> fatias · <a> AFK · <h> HITL · tamanhos <P/M/G>
<tabela>
Cobertura: <c>/<c> cenários · Primeira fatia (tracer bullet): FT-<…>
- A granularidade está boa? (muito grossa / muito fina)
- As dependências estão certas?
- Alguma fatia deveria ser HITL/AFK ao contrário?
```

Ajuste e repita até "ok". Esse "ok" é o **GATE do backlog** (P.O. ou time no refinamento).

## Passo 3 — Gravar

1. `backlog.json` (na **base** — ver [references/backlog.md](references/backlog.md)): épico com `status: fatiado`;
   uma entrada por fatia com prioridade (ordem da tabela, respeitando dependências), `elm: null` e `status`
   `pronta` se passa na **Definition of Ready** (seção do `backlog.md`) ou `backlog` com o que falta. Ids
   `FT-<nnn>` sequenciais no projeto, **nunca reaproveitados**.
2. Regenere `backlog.md` a partir do JSON.
3. PRD: `status: fatiado`.
4. Commit (padrão do `sdd2.md`): `backlog.json`, `backlog.md`, `prd.md`.

## Passo 4 — Próximos passos (na mesma resposta)

- Com ELM: **`sdd2-elm`** modo *backlog* — cria o épico (se ainda não existe no EWM) e um item de backlog por fatia,
  ligados às histórias do DOORS Next ("implementa") e ao épico (pai), **sem iteração** (backlog do produto).
- **`sdd2-planejamento`** — encaixar as fatias na sprint (ou no fluxo Kanban).
- Para começar uma fatia já: "vamos trabalhar na FT-031" (`sdd2-iniciar`).

## Refinamento (backlog já existe)

"Refinar o backlog", "a FT-033 está grande demais", "faltou uma fatia":
- **Dividir:** a fatia original fica `status: dividida` com `substituida-por: [FT-x, FT-y]`; as novas herdam a
  cobertura (repartida), as dependências e o épico. No EWM, a `sdd2-elm` faz o que diz "Fatia dividida no EWM" no
  `sdd2.md` (filhos do item original, ou fecha o original e cria itens novos).
- **Juntar:** só fatias ainda em `backlog`; a que some fica `status: cancelada` com `motivo`.
- **Nova fatia:** cenário novo exige PRD alterado antes (`sdd2-prd`, mudança depois de aprovado).
- **Definition of Ready:** a cada refinamento, confira as fatias `backlog` e grave `pronta` nas que passam (e
  volte a `backlog` as que deixaram de passar). Critérios na seção do [references/backlog.md](references/backlog.md).

## Regras

- Nunca crie fatia por camada técnica ou por papel ("especificar X", "testar X") — o trabalho de todos os papéis
  na mesma fatia é a mesma fatia.
- Nunca altere fatia `concluida`. Mudança de comportamento entregue = fatia nova.
- Tamanho não é promessa de prazo: é o sinal de que a fatia cabe num PR revisável.
