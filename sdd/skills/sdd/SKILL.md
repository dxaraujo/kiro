---
name: sdd
description: "Guia do fluxo sdd — engenharia agêntica orientada a especificação, com o IBM ELM como fonte oficial da documentação e planejamento ágil: trilhas por tamanho (direta, rápida, padrão, épico) e de atendimento, fases, gates humanos, artefatos e onde moram, agentes, princípios e qual skill usar para cada pedido. Use para entender ou explicar o fluxo, decidir o próximo passo quando nenhuma outra skill sdd se encaixa, e em \"como funciona o sdd\", \"qual o fluxo\", \"o que eu faço agora com isso\", \"sdd\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.0.0"
---

# sdd — Engenharia agêntica orientada a especificação

O agente escreve muito código rápido; o que limita o resultado é o **alinhamento** antes e a **verificação**
depois. O sdd põe as pessoas onde elas têm mais alavanca — decidir o quê, aprovar o como, ler o código — e
deixa o resto com agentes de contexto limpo, presos a feedback automático. O IBM ELM é o registro oficial do que
o sistema faz; o repositório guarda como cada mudança foi feita.

Configuração do projeto: `.kiro/steering/sdd.md` (gerado pela **`sdd-setup`**). Sem ele, comece por
"configurar o sdd".

## Trilhas (o tamanho decide a cerimônia)

| Trilha | Quando | Caminho |
|---|---|---|
| **direta** | o diff cabe numa frase, sem regra nova | teste que falha → correção → revisão → PR (sem pasta de spec) |
| **rápida** | defeito ou ajuste ≤ 1 dia, comportamento certo já conhecido | `bugfix.md` + `tasks.md` → implementação → revisão → verificação → PR |
| **padrão** | uma fatia do backlog | pesquisa → plano → **GATE do plano** → implementação (TDD) → revisão → verificação → PR → consolidação |
| **épico** | funcionalidade com várias histórias ou decisão de produto em aberto | entrevista → PRD → **GATE do PRD** → ELM → fatias → **GATE do backlog** → planejamento → cada fatia na trilha padrão |
| **atendimento** | o cliente pede consulta, extração ou explicação; nada muda no repositório | entrevista curta → `[ATD]` no EWM → banco (só leitura) e bundle → resposta com "ok" → horas |

Toda hora trabalhada cabe numa tarefa da sprint: `[ESP]` (especificação do épico), `[DEV]`, `[REV]`, `[VER]` (por
fatia) e `[ATD]` (por atendimento). As horas são lançadas na conclusão de cada tarefa, nunca nos GATEs.

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
| configurar o fluxo, os agentes e os toolkits no projeto | `sdd-setup` |
| saber onde parei / o que fazer agora · fechar a sessão | `sdd-status` |
| começar qualquer trabalho (fatia, defeito, item do EWM, pedido) | `sdd-iniciar` |
| alinhar decisões | `sdd-entrevistar` |
| escrever o PRD de um épico | `sdd-prd` |
| quebrar o PRD em fatias / refinar o backlog | `sdd-fatiar` |
| planejar sprint, roadmap, virada, review | `sdd-planejamento` |
| atender um pedido de cliente (consulta, extração) sem mudar o código | `sdd-atender` |
| lançar horas ou ver o relatório de horas | `sdd-elm` modo *horas* |
| entender o código antes de planejar | `sdd-pesquisar` |
| planejar uma fatia (spec do Kiro) | `sdd-plano` |
| implementar e abrir o PR | `sdd-implementar` |
| revisar PRD, plano ou código | `sdd-revisar` |
| verificar o aceite de ponta a ponta | `sdd-verificar` |
| fechar a fatia depois do merge | `sdd-consolidar` |
| publicar no ELM (DOORS Next, EWM, ETM) | `sdd-elm` |
| levar várias fatias AFK até o PR | `sdd-loop` (com o agente `sdd-orquestrador`) |
| rodar uma receita de workflow numa fatia | você, no chat do Kiro: "rode o workflow `sdd-entregar-fatia` para a FT-031" ou `/workflow-run` (IDE 1.3+) |
| registrar uma lição / retrospectiva | `sdd-aprender` |

## Onde as coisas moram (no projeto)

| Caminho | O quê |
|---|---|
| `.kiro/steering/sdd.md` | o único steering do fluxo: resumo, configuração do projeto e regras aprendidas |
| `.kiro/agents/sdd-*.json` | agentes (criados pela setup, com as skills escolhidas por agente) |
| `<produto>/` — a pasta escolhida na setup (ex.: `docs/pab`), registrada no `sdd.md` | `backlog.md`, `epicos/<EP>-<slug>/` (PRDs), `planejamento/`, `atendimentos/`, `aprendizado/` (só na branch base) |
| `.kiro/specs/<ft>-<slug>/` | uma pasta por fatia: `status.md`, `research.md`, spec do Kiro, revisões, verificação |
| glossário · ADRs · bundle do ELM | caminhos na seção Projeto do `sdd.md` |
| `.kiro/hooks/sdd.json` · `.kiro/workflows/sdd-*` · `.kiro/sdd/http.sh` | opcionais da setup: backpressure por tarefa, receitas, chamada HTTP do verificador |
| `.kiro/local/` (fora do git) | worktrees do loop, vereditos dos workflows, log dos lotes, dados de cliente (extrações, evidências com dado real) |

## Fronteiras de fase

Ao terminar uma fase, nesta ordem: seguir na mesma sessão se o contexto ainda serve → sessão nova se o contexto
anterior não importa mais (o estado está nos arquivos) → mandar para um agente se a próxima fase pode correr AFK.
Nunca compacte no meio de uma fase.

## Regras de ouro

- Nada inventado: tabela, coluna, regra, id de work item — confirme no código, no banco (somente leitura) ou no ELM.
- Toda escrita no ELM, troca de branch, push e alteração de work item só com "sim" de uma pessoa. Agente nunca faz
  merge nem `--force`.
- O MCP do ELM fica nos agentes que conduzem sessão com a pessoa (`sdd-produto`, `sdd-codificador`,
  `sdd-orquestrador`); revisor, verificador e pesquisador não o têm. Sem o MCP ou com falha, a escrita vira
  `ELM pendente` registrada — o ELM nunca trava o fluxo.
- Dado de cliente (resultado de consulta, extração, tela com dado real) nunca vai para o git: fica em
  `.kiro/local/<origem>/<id>/`; o registro versionado guarda consulta, contagem, caminho e resumo sem identificar
  pessoas.
