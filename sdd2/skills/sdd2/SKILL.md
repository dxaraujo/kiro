---
name: sdd2
description: "Guia do fluxo sdd2 — engenharia agêntica orientada a especificação, com o IBM ELM como fonte oficial da documentação e planejamento ágil: trilhas por tamanho (direta, rápida, padrão, épico), fases, gates humanos, artefatos e onde moram, agentes, princípios e qual skill usar para cada pedido. Use para entender ou explicar o fluxo, decidir o próximo passo quando nenhuma outra skill sdd2 se encaixa, e em \"como funciona o sdd2\", \"qual o fluxo\", \"o que eu faço agora com isso\", \"sdd2\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2 — Engenharia agêntica orientada a especificação

O agente escreve muito código rápido; o que limita o resultado é o **alinhamento** antes e a **verificação**
depois. O sdd2 põe as pessoas onde elas têm mais alavanca — decidir o quê, aprovar o como, ler o código — e
deixa o resto com agentes de contexto limpo, presos a feedback automático. O IBM ELM é o registro oficial do que
o sistema faz; o repositório guarda como cada mudança foi feita.

Configuração do projeto: `.kiro/steering/sdd2-projeto.md` (gerado pela **`sdd2-setup`**). Sem ele, comece por
"configurar o sdd2".

## Trilhas (o tamanho decide a cerimônia)

| Trilha | Quando | Caminho |
|---|---|---|
| **direta** | o diff cabe numa frase, sem regra nova | teste que falha → correção → revisão → PR (sem pasta de spec) |
| **rápida** | defeito ou ajuste ≤ 1 dia, comportamento certo já conhecido | `bugfix.md` + `tasks.md` → implementação → revisão → verificação → PR |
| **padrão** | uma fatia do backlog | pesquisa → plano → **GATE do plano** → implementação (TDD) → revisão → verificação → PR → consolidação |
| **épico** | funcionalidade com várias histórias ou decisão de produto em aberto | entrevista → PRD → **GATE do PRD** → ELM → fatias → **GATE do backlog** → planejamento → cada fatia na trilha padrão |

```
PRODUTO       entrevistar ─► PRD ─► GATE PRD ─► ELM (HF/REG/GL) ─► fatiar ─► GATE backlog ─► sprint (EWM)
                                                                                    │
FATIA         iniciar ─► pesquisar ─► plano ─► GATE plano ─► implementar (TDD) ─► revisar ─► verificar ─► PR
                                                                                                         │
DEPOIS        merge (pessoa) ─► consolidar (drift, ELM as-built, CTs, conclusão) ─► aprender (lições)
```

## Gates — sempre de uma pessoa

| Gate | Quem | O que se aprova |
|---|---|---|
| PRD | P.O. | o quê e o porquê: histórias, cenários, regras, fora de escopo |
| Backlog | P.O. + time | as fatias: granularidade, dependências, AFK/HITL |
| Plano | dev (de preferência quem vai revisar o PR) | a forma do programa e o contrato de pronto — maior alavanca |
| PR | quem revisa | o código, lido de verdade, com a evidência de aceite |

Fatia **AFK**: o projeto pode dispensar o GATE do plano (a análise independente basta) — o PR nunca é dispensado.

## Princípios

1. **Alinhar antes de escrever** — entrevista em rodadas, com recomendação; fatos o agente busca, decisões a pessoa toma.
2. **Cerimônia do tamanho do trabalho** — nada de 16 critérios para um ajuste de uma linha.
3. **Fatias verticais** que cabem numa janela de contexto nova e provam algo demonstrável.
4. **Verificação acima de geração** — teste primeiro, backpressure (compilar, testes, lint) a cada passo, aceite
   com evidência, oráculo protegido (teste não se apaga nem se afrouxa).
5. **Gerador ≠ avaliador** — revisão e verificação em contexto limpo, em eixos separados (spec × padrões).
6. **Contexto limpo e estado em disco** — uma fatia por sessão; `status.md`, `research.md` e o plano carregam o fio.
7. **Autonomia gradual** — HITL até o tipo de trabalho provar que anda sozinho; AFK limitado pela capacidade de
   revisão humana.
8. **Documentação ancorada no ELM** — PRD e plano são registros de decisão descartáveis; o ELM, o glossário e os
   ADRs são o que dura; a consolidação fecha o drift.
9. **Aprendizado composto** — cada correção humana muda o ambiente (checagem, regra, skill, glossário), não só o código.
10. **Leia o código** — PRs pequenos, com caminho de leitura e evidência; nada é mergeado sem uma pessoa.

## O que dizer

| Quero… | Skill |
|---|---|
| configurar o fluxo, os agentes e os toolkits no projeto | `sdd2-setup` |
| saber onde parei / o que fazer agora | `sdd2-status` |
| começar qualquer trabalho (fatia, defeito, item do EWM, pedido) | `sdd2-iniciar` |
| alinhar decisões | `sdd2-entrevistar` |
| escrever o PRD de um épico | `sdd2-prd` |
| quebrar o PRD em fatias / refinar o backlog | `sdd2-fatiar` |
| planejar sprint, roadmap, virada, review | `sdd2-planejamento` |
| entender o código antes de planejar | `sdd2-pesquisar` |
| planejar uma fatia (spec do Kiro) | `sdd2-plano` |
| implementar e abrir o PR | `sdd2-implementar` |
| revisar PRD, plano ou código | `sdd2-revisar` |
| verificar o aceite de ponta a ponta | `sdd2-verificar` |
| fechar a fatia depois do merge | `sdd2-consolidar` |
| publicar no ELM (DOORS Next, EWM, ETM) | `sdd2-elm` |
| levar várias fatias AFK até o PR | `sdd2-loop` |
| registrar uma lição / retrospectiva | `sdd2-aprender` |

## Onde as coisas moram (no projeto)

| Caminho | O quê |
|---|---|
| `.kiro/steering/sdd2.md` · `sdd2-projeto.md` · `sdd2-licoes.md` | resumo do fluxo · configuração · regras aprendidas |
| `.kiro/agents/sdd2-*.json` | agentes (criados pela setup, com as skills escolhidas por agente) |
| `.kiro/produto/backlog.json` · `epicos/<EP>-<slug>/` · `planejamento/` | backlog, PRDs, sprints (só na branch base) |
| `.kiro/specs/<ft>-<slug>/` | uma pasta por fatia: `status.md`, `research.md`, spec do Kiro, revisões, verificação |
| glossário · ADRs · bundle do ELM | caminhos na seção Conhecimento do `sdd2-projeto.md` |
| `.kiro/aprendizado/` | lições e casos de avaliação |

## Fronteiras de fase

Ao terminar uma fase, nesta ordem: seguir na mesma sessão se o contexto ainda serve → sessão nova se o contexto
anterior não importa mais (o estado está nos arquivos) → mandar para um agente se a próxima fase pode correr AFK.
Nunca compacte no meio de uma fase.

## Regras de ouro

- Nada inventado: tabela, coluna, regra, id de work item — confirme no código, no banco (somente leitura) ou no ELM.
- Toda escrita no ELM, troca de branch, push e alteração de work item só com "sim" de uma pessoa. Agente nunca faz
  merge nem `--force`.
- Os agentes não têm o MCP do ELM: a escrita no ELM acontece na sessão da pessoa, com o power `elm`; nos agentes
  ela vira pendência registrada.
