---
name: sdd
description: "Guia do fluxo sdd — engenharia agêntica orientada a especificação, com o IBM ELM como fonte oficial da documentação e planejamento ágil: trilhas por tamanho (direta, rápida, padrão, épico) e de atendimento, fases, gates humanos, artefatos e onde moram, agentes, princípios e qual skill usar para cada pedido. Use para entender ou explicar o fluxo, decidir o próximo passo quando nenhuma outra skill sdd se encaixa, e em \"como funciona o sdd\", \"qual o fluxo\", \"o que eu faço agora com isso\", \"sdd\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.6.3"
---

# sdd — Engenharia agêntica orientada a especificação

O agente escreve muito código rápido; o que limita o resultado é o **alinhamento** antes e a **verificação**
depois. O sdd põe as pessoas onde elas têm mais alavanca — decidir o quê, aprovar o como, ler o código — e
deixa o resto com agentes de contexto limpo, presos a feedback automático. O IBM ELM é o registro oficial do que
o sistema faz; o repositório guarda como cada mudança foi feita.

Configuração do projeto: `.kiro/steering/sdd.md` (gerado pela **`sdd-setup`**). Sem ele, comece por
"configurar o sdd".

## Trilhas (o tamanho decide a cerimônia)

Toda demanda nova entra pela **`sdd-triar`**: ela decide a trilha e registra o trabalho no backlog — inclusive o
atendimento —, sem começar, e pergunta se há mais algum item. O hub **`sdd-iniciar`** recebe um item registrado e
diz a skill do papel; cada skill de papel assume a própria tarefa no EWM (`sdd-elm` modo *assumir*) e pode ser
chamada direto:

| Papel | Tarefa | Skill |
|---|---|---|
| Especificador | `[ESP]` | `sdd-especificar` (entrevista → PRD → fatias) |
| Dev | `[DEV]` | `sdd-desenvolver` (compromisso, branch) → pesquisar → plano → implementar → PR |
| Revisor | `[REV]` | `sdd-revisar` |
| Verificador (QA) | `[VER]` | `sdd-verificar` |
| quem atende | `[ATD]` | `sdd-atender` |

| Trilha | Quando | Caminho |
|---|---|---|
| **direta** | o diff cabe numa frase, sem regra nova | teste que falha → correção → revisão → PR (sem spec: a pasta tem só o `status.md`) |
| **rápida** | defeito ou ajuste ≤ 1 dia, comportamento certo já conhecido | `bugfix.md` + `tasks.md` → implementação → revisão → verificação → PR |
| **padrão** | uma fatia do backlog: de um épico, ou sem épico com regra clara e ficha aprovada pelo P.O. | pesquisa → plano → **GATE do plano** → implementação (TDD) → revisão → verificação → PR → consolidação |
| **épico** | funcionalidade com várias histórias ou decisão de produto em aberto | entrevista → PRD → **GATE do PRD** → ELM → fatias → **GATE do backlog** → planejamento → cada fatia na trilha padrão |
| **atendimento** | o cliente pede consulta, extração ou explicação; nada muda no repositório | triagem: entrevista curta → `AT-nnn` no backlog, sprint sugerida, `[ATD]` no EWM · `sdd-atender`: assume → banco (só leitura) e bundle → resposta com "ok" → saldo de horas → desdobramentos |

Toda hora trabalhada cabe numa tarefa da sprint: `[ESP]` (especificação do épico), `[DEV]`, `[REV]`, `[VER]` (por
fatia; no AFK só a `[DEV]`) e `[ATD]` (por atendimento). **Lançar ≠ concluir:** lançar horas é registro de
empenho, a qualquer momento numa tarefa iniciada (inclusive antes de um GATE); concluir é da skill do papel quando
o trabalho dela termina, perguntando só o saldo — `[DEV]` no PR, `[REV]` ao aprovar, `[VER]` ao aceitar, `[ESP]`
no GATE do backlog, `[ATD]` ao finalizar.

```
ENTRADA       triar ─► backlog: EP rascunho · FT sem épico (padrão com ficha, rápida, direta) · AT + [ATD] ─► "mais algum?"
                │
HUB           iniciar <item> ─► especificar · desenvolver · revisar · verificar · atender   (cada uma assume a sua tarefa)
                │
PRODUTO       especificar ─► entrevistar ─► PRD ─► GATE PRD ─► ELM (HF/REG/GL) ─► fatiar ─► GATE backlog ─► sprint (EWM)
                                                                                    │
FATIA         desenvolver ─► pesquisar ─► plano ─► GATE plano ─► implementar (TDD) ─► revisar ─► verificar ─► PR
                                                                                                         │
DEPOIS        merge (pessoa) ─► consolidar (drift, ELM as-built, CTs, conclusão) ─► aprender (lições)
```

**Cadência:** a sprint é ritmo de inspeção (meta, review, retro), não escopo congelado. O compromisso é a meta; a
seleção é previsão, e dentro da sprint o fluxo é puxado (a `pronta` do topo entra quando o WIP de revisão tem
folga). Previsão pela vazão e pelo lead time, sem pontos.

## Gates — sempre de uma pessoa

| Gate | Quem | O que se aprova |
|---|---|---|
| PRD | P.O. | o quê e o porquê: histórias, cenários, regras, fora de escopo |
| Backlog | P.O. + time | as fatias: granularidade, dependências, AFK/HITL |
| Ficha | P.O. | a fatia padrão sem épico: regras e cenários |
| Plano | dev (de preferência quem vai revisar o PR) | a forma do programa e o contrato de pronto — maior alavanca |
| PR | quem revisa | o código, lido de verdade, com a evidência de aceite |

GATE do plano: sempre no HITL; no AFK, só na fatia de épico (a fatia AFK sem épico segue com a análise
independente); na trilha rápida, `GATE na trilha rápida` do `sdd.md` decide antes do modo. PRD e backlog nunca são
AFK. O PR e o merge nunca são dispensados.

## Modos — o `modo` da fatia vale para todos os papéis

| | **HITL** — pessoas nos papéis, subfluxos assíncronos | **AFK** — a IA coordena, um fluxo só |
|---|---|---|
| Quem roda | cada pessoa, a skill do seu papel | `sdd-loop` (`sdd-orquestrador` + subagentes) |
| Codificador | revisão automática (rubrica C, subagente) → PR → `[DEV]` concluída | o loop leva a fatia até o PR |
| Revisão | o revisor assume a `[REV]` e revisa o PR: aprova → VER; reprova → retrabalho | subagente, até 2 rodadas |
| Verificação | o verificador assume a `[VER]` (só depois da REV): aceita → `pronta-para-merge`; rejeita → retrabalho | subagente |
| Retrabalho | a `[DEV]` é reaberta e o codificador corrige no mesmo PR, que passa de novo pela REV | volta à implementação |
| Tarefas no EWM | `[DEV]` `[REV]` `[VER]`, cada uma da sua pessoa | só a `[DEV]`, de quem disparou |

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
| registrar qualquer demanda nova — pedido, defeito, ajuste, pedido de cliente, item ou lote do EWM (triagem) | `sdd-triar` |
| começar um item registrado, ou "minha próxima tarefa" (o hub diz a skill do papel) | `sdd-iniciar` |
| especificar um épico (`[ESP]`) e registrar cada sessão com o cliente na tarefa | `sdd-especificar` |
| começar ou retomar o código de uma fatia (`[DEV]`) | `sdd-desenvolver` |
| alinhar decisões | `sdd-entrevistar` |
| escrever o PRD de um épico | `sdd-prd` |
| quebrar o PRD em fatias / refinar o backlog | `sdd-fatiar` |
| planejar sprint, roadmap, virada, review | `sdd-planejamento` |
| executar um atendimento já triado (`AT-nnn`, `[ATD]`) | `sdd-atender` |
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
| `<produto>/` — a pasta escolhida na setup (padrão `.kiro/planejamento`), registrada no `sdd.md` | `backlog.md`, `epicos/<EP>-<slug>/` (PRDs), `equipe.json`, `acordos.md`, `roadmap.md`, `sprints/`, `atendimentos/`, `aprendizado/` (só na branch base) |
| `.kiro/specs/<ft>-<slug>/` | uma pasta por fatia: `status.md`, `research.md`, spec do Kiro, revisões, verificação |
| glossário · ADRs · bundle do ELM | caminhos na seção Projeto do `sdd.md` |
| `.kiro/hooks/sdd.json` · `.kiro/workflows/sdd-*` · `.kiro/sdd/http.sh` | opcionais da setup: backpressure por tarefa, receitas, chamada HTTP do verificador |
| `.kiro/local/` (fora do git) | worktrees do loop, vereditos dos workflows, log dos lotes, dados de cliente (extrações, evidências com dado real), especificação em andamento (`especificacao/<EP>/`, até o GATE do PRD) |

## Fronteiras de fase

Ao terminar uma fase, nesta ordem: seguir na mesma sessão se o contexto ainda serve → sessão nova se o contexto
anterior não importa mais (o estado está nos arquivos) → mandar para um agente se a próxima fase pode correr AFK.
Nunca compacte no meio de uma fase.

## Regras de ouro

- **Falha de escrita:** pasta inexistente → crie; permissão negada ou confirmação recusada → `fase: bloqueada (de:
  <fase>)` com o caminho e o que faltou (fora de fatia: diga e pare); gravação parcial → o próximo passo retoma pelo
  que está no disco. Nunca siga como se tivesse gravado.
- Nada inventado: tabela, coluna, regra, id de work item — confirme no código, no banco (somente leitura) ou no ELM.
- Toda escrita no ELM, troca de branch, push e alteração de work item só com "sim" de uma pessoa. Agente nunca faz
  merge nem `--force`.
- O ELM é do **power `elm`**: o `sdd` decide quando e o quê, e pede **operações** às skills `elm-*` (nunca chama
  tool direto). Os agentes que conduzem sessão (`sdd-produto`, `sdd-codificador`, `sdd-orquestrador`) e o revisor e
  o verificador (só para a própria tarefa) recebem o power com `includePowers: true`; o pesquisador também o recebe (pelo `okf`), mas não pede nada ao ELM. Sem o
  power ou com falha, a escrita vira
  `ELM pendente` registrada — o ELM nunca trava o fluxo.
- **Bundle do ELM e PR, só pelos MCPs do power:** a documentação baixada pela `elm-sync` (`<rm.download.path>`) —
  cópia local, em Markdown, dos artefatos do ELM, válida até o último sincronismo (o ELM ao vivo é pela `elm-rm`) — é
  consultada pelo **`okf`** — `okf_search` para achar, `okf_get_document` para ler um artefato, `okf_list_documents`
  para listar uma pasta (`root` = caminho absoluto de `rm.download.path` do `pa_*.json` (o da linha "Usa ELM"): raiz do repositório + o `path`, a mesma `dest` da `elm-sync`; `okf_index` antes da primeira busca da sessão) —, nunca
  lendo ou buscando os arquivos (os agentes nem têm leitura nessa pasta). PR é o merge request do GitLab, pelo
  **`gitlabpr`**: `gitlab_listar_mrs`, `gitlab_obter_mr` e `gitlab_criar_mr` (com o "sim" da pessoa; `origem` e
  `destino` sempre explícitos, porque o MCP roda no checkout principal, não na worktree) — nunca `gh` nem `glab`.
  MCP indisponível → diga e siga sem ele: bundle → o ELM ao vivo pela `elm-rm`; PR → título e descrição entregues.
- Dado de cliente (resultado de consulta, extração, tela com dado real) nunca vai para o git: fica em
  `.kiro/local/<origem>/<id>/`; o registro versionado guarda consulta, contagem, caminho e resumo sem identificar
  pessoas.
- **Skills sem agente exclusivo:** `sdd-setup`, `sdd-consolidar` e `sdd-aprender` rodam na **sessão padrão** (com
  o power carregado), não em agentes específicos: gravam onde nenhum agente pode (steering, agentes, ET *as-built*,
  remoção de worktree). **O que os agentes não fazem:** push (exceto o orquestrador no loop, com `ask`) — a
  skill entrega o comando pronto e a pessoa executa; com a branch no remoto, o PR é aberto pela `gitlab_criar_mr`,
  que o Kiro confirma (`ask` no codificador, no produto e no orquestrador; negada aos demais); merge (exceto a
  `gitlab_mesclar_mr` no codificador, com `ask`), `--force`, `worktree remove` — nunca. O hub `sdd-iniciar` está em todos os agentes de papel, e a `sdd-status`
  em todos os agentes, menos o `sdd-pesquisador`; os dois também funcionam na sessão padrão. Nenhuma skill depende de um agente para operar: o agente apenas recebe a skill
  pré-carregada para conveniência.
- **Nenhuma skill cria branch ou `.kiro/specs/<ft>/status.md`** sem passar pelos Passos 3–4 da `sdd-desenvolver`
  (DoR, sprint, WIP, branch, commit). O `sdd-loop` é a única exceção (opera em worktree como orquestrador).
