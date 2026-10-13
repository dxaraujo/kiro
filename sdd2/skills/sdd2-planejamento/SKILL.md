---
name: sdd2-planejamento
description: "Planejamento ágil do projeto no fluxo sdd2, ajustado a times que trabalham com agentes — roadmap e releases a partir dos épicos, acordos do time (cadência Scrum ou Kanban, Definition of Ready e Done, limites de WIP incluindo a capacidade de revisão humana, que é o gargalo), planejamento da sprint por prioridade, dependências e capacidade (vazão de fatias e pontos), meta da sprint, acompanhamento, review com as evidências de aceite, retrospectiva com dados e virada de sprint; publica a sprint no EWM pela sdd2-elm. Use em \"monta o planejamento\", \"planejar a sprint\", \"roadmap\", \"virada de sprint\", \"fechar a sprint\", \"review da sprint\", \"capacidade do time\", \"acordos do time\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-planejamento — Planejar o fluxo, não só o calendário

Com agentes escrevendo código, o que limita a entrega é a **atenção humana**: decidir (P.O.), revisar planos e
PRs, verificar e aceitar. O planejamento do sdd2 mede e protege essa capacidade, trabalha com fatias pequenas e de
tamanho parecido e prevê pela **vazão** (fatias concluídas por sprint), mantendo os pontos no EWM para quem os usa.

Arquivos em `.kiro/produto/planejamento/` (formatos em [references/arquivos.md](references/arquivos.md)):
`equipe.json`, `acordos.md`, `roadmap.md`, `sprints/sprint-<nn>.md`. Fatias: `.kiro/produto/backlog.json`.

Regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar.

## Modo inicial — acordos e roadmap

1. **Equipe** (`equipe.json` existe → mostre e pergunte só o que mudou): pessoas, papel (P.O., dev, QA, SM),
   login do ELM (de `members` do `pa_*.json`, se houver), horas por semana, ausências. Pergunte também, por pessoa,
   quantas horas por semana vão para **revisar** (planos, PRs) e **verificar**.
2. **Acordos** (`acordos.md`) — proponha e ajuste:
   - cadência: **Scrum** (sprints de N semanas, cerimônias, iteração no EWM) ou **Kanban** (fluxo contínuo,
     revisão de backlog semanal); padrão: sprints de 2 semanas com fluxo puxado dentro da sprint;
   - **WIP:** uma fatia por sessão de agente; fatias em `revisando` + `pr-aberto` ≤ capacidade de revisão (ex.: 2
     por revisor); nenhuma fatia nova começa com PR parado há mais de 1 dia;
   - **Definition of Ready** e **Definition of Done** (padrão no `arquivos.md`);
   - tamanho: `P`/`M`/`G` e a tabela de pontos (padrão `2/3/5`).
3. **Roadmap** (`roadmap.md`): épicos do `backlog.json` em ordem de valor e risco (maior incerteza mais cedo),
   agrupados em releases com um objetivo cada; épico sem PRD aparece como "a descobrir" (`sdd2-prd`).

## Modo sprint — planejar a próxima

1. **Capacidade**, da `equipe.json` (horas da sprint menos ausências):
   - **revisão humana** (horas de revisão e verificação) — o limite principal;
   - **HITL**: fatias HITL consomem horas de dev acompanhando;
   - **vazão**: média de fatias concluídas nas últimas 3 sprints (primeira sprint: comece com 1 fatia por dev
     por semana e ajuste na virada). Em pontos: velocidade média, para o EWM.
2. **Seleção:** fatias `pronta` (Definition of Ready) do topo do backlog, respeitando `bloqueada-por` — a fatia só
   entra se as dependências entram antes ou já estão concluídas. Pare ao atingir a menor das capacidades. Fatia
   não `pronta` no topo → aponte o que falta (decisão, PRD, fatiar) antes de pular para a próxima.
3. **Meta da sprint:** uma frase de resultado de negócio que as fatias entregam juntas.
4. **Proposta:**
   ```
   🗓️ Sprint <nn> · <início> → <fim> · meta: <…>
   | Prioridade | FT | Título | Tam. | Modo | Depende de | Responsável |
   Capacidade: revisão <h>h (usa <x>h) · vazão prevista <n> fatias / <p> pts · HITL <h>h
   Fica de fora (por capacidade): <FT…>
   ```
5. "ok" → grave `sprints/sprint-<nn>.md`, `sprint` e `responsavel` no `backlog.json`, commit; ofereça a
   **`sdd2-elm`** modo *sprint* (iteração, IBs, tarefas).

## Durante a sprint

"Como está a sprint?" → **`sdd2-status`** filtrado pela sprint (fase de cada fatia, bloqueios, WIP de revisão,
PRs parados). Fatia que cresceu (passou de `G` no plano) → volte para a `sdd2-fatiar` (dividir) em vez de esticar.

## Review

Para cada fatia concluída: o cenário entregue e a **evidência** do `verificacao.md` (resposta, contagem,
screenshot). Registre o retorno do P.O. no `sprint-<nn>.md`; pedido novo vira cenário/fatia nova pela `sdd2-prd`/
`sdd2-fatiar` — não reabre fatia concluída.

## Retrospectiva e virada

1. **Retrospectiva com dados** — `sdd2-aprender` modo retrospectiva (vazão, lead time, rodadas de revisão,
   correções humanas por causa, AFK que chegaram ao PR sozinhas). Registre no `sprint-<nn>.md`: bom · melhorar ·
   ações (cada ação com dono).
2. **Fechar:** concluídas contam na vazão e nos pontos; não concluídas **migram** para a próxima sprint (no
   `sprint-<nn>.md` antigo ficam com "→ sprint <nn+1>"; o histórico não é apagado).
3. Recalcule vazão média e velocidade (`equipe.json` → `historico`), replaneje a próxima pelo modo sprint
   (migradas consomem capacidade primeiro).
4. **ELM** — `sdd2-elm` modo *sprint*, virada: move as não concluídas para a nova iteração e publica as novas;
   roteiro manual de baseline, se o projeto exige.

## Regras

- Nunca planeje acima da capacidade de revisão: trabalho que ninguém revisa não está pronto, só está parado.
- Fatia nunca se espalha por sprints para caber; se não cabe, divide.
- Estimativa é do time (pode usar Planning Poker); o agente propõe tamanho com justificativa, a pessoa decide.
- Pontos ficam no IB (plan item), nunca nas tarefas.
