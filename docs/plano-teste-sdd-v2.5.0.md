# Plano de teste e verificação do fluxo `sdd` 2.5.0

> Execução real (Kiro + EWM) de todas as trilhas × modos, no projeto **pab-batch**, com produto isolado em
> `.kiro/planejamento2` e itens do EWM na iteração **Sprint Jandaia** da PA **PAB**. Nada disso é commitado nas
> branches reais nem enviado ao remoto; tudo é apagado no fim (seção 9).

## 1. Objetivo e critério de aprovação

Confirmar, para cada cenário, que **cada passo**:

1. deixa o **estado esperado** — fase do `status.md`, `status` do `backlog.md`, estado da tarefa no EWM;
2. **gera ou atualiza só os artefatos previstos**, com o **conteúdo** previsto (seção 7);
3. **encaminha para a skill certa**, e a skill seguinte **aceita** o estado em que recebeu a fatia (seção 6);
4. termina com `git status` **limpo** na pasta da fatia (regra "estado limpo entre sessões").

Um cenário passa quando todos os passos passam. Qualquer diferença vira um **achado**: id, passo, esperado ×
obtido, arquivo:linha da regra, severidade.

**Testar tudo.** O alvo são as **inconsistências**: uma skill que deixa um estado que a seguinte não aceita, duas
skills que tratam o mesmo caso de jeitos diferentes, um artefato que uma grava e a outra não lê. Por isso nenhuma
combinação fica de fora por "não se aplica": as que o desenho diz que não existem viram **testes de consistência**
(seção 2.1), e o resultado esperado é que **todas** as skills envolvidas recusem do mesmo jeito, com o mesmo
motivo. Toda resposta do Kiro que contradiga este plano é registrada, mesmo que pareça razoável — o plano pode
estar errado, e isso também é achado (do plano ou da skill).

## 2. Matriz de cenários

| Id | Trilha | Modo | Via | Papéis em ação | Observação |
|---|---|---|---|---|---|
| C01 | direta | HITL | skills | P.O., Dev | inclui os pontos de atenção 1 e 2 (seção 10) |
| C01b | direta | AFK | `sdd-loop` e `sdd-desenvolver` | P.O., Dev | consistência: a `sdd-loop` exclui a direta; o que a triagem grava em `modo`, e o que a `sdd-desenvolver` faz com uma direta AFK? |
| C02 | rápida | HITL | skills | P.O., Dev, Revisor, QA | `GATE na trilha rápida = não` → sem GATE do plano mesmo em HITL |
| C03 | rápida | AFK | `sdd-loop` | P.O., Dev (dispara) | só a `[DEV]` no EWM |
| C04 | padrão sem épico | HITL | skills | P.O., Dev, Revisor, QA | com **retrabalho pedido pela REV** |
| C05 | padrão sem épico | AFK | workflows `sdd-planejar-fatia` + `sdd-entregar-fatia` | P.O., Dev (dispara) | sem GATE do plano |
| C06 | épico (especificação) | HITL (sempre) | skills | P.O., Especificador | PRD e backlog nunca são AFK; 2 sessões, em 2 "máquinas" |
| C06b | épico (especificação) | AFK | skills e `sdd-loop` | P.O. | consistência: pedir PRD/fatiamento em modo autônomo (`AUTONOMO=true`) e pôr um `EP-nn` no loop — todos devem recusar |
| C07 | padrão de épico | HITL | skills | Dev, Revisor, QA | fatia do C06; com **retrabalho pedido pela VER** |
| C08 | padrão de épico | AFK | `sdd-loop` | Dev (dispara) | fatia do C06; **mantém o GATE do plano** |
| C09 | atendimento | — (não tem modo) | skills | P.O., quem atende | desdobramento "gerar alteração" → nova triagem com `origem AT-nnn` |
| C09b | atendimento | "AFK" | `sdd-loop`, `sdd-iniciar` | quem atende | consistência: AT no loop e `[ATD]` pelo orquestrador devem recusar; AT nunca vira `status.md` nem branch |
| C10 | hub e fluxo puxado | — | skills | todos | "minha próxima tarefa", triagem em sequência, puxar o topo, Encaixe |
| C11 | virada da sprint | — | `sdd-planejamento` | P.O. | migração, reserva 20% (atendimento + retrabalho), relatório de horas |
| C12 | bordas | — | várias | — | negativos e falhas (seção 8) |

Ordem de execução: **C00 (preparação) → C06 → C06b → C01 → C01b → C02 → C04 → C07 → C03 → C05 → C08 → C09 →
C09b → C10 → C11 → C12 → C13 → limpeza**. O C06 vem primeiro porque produz as fatias de épico do C07 e do C08.

### 2.1 Testes de consistência (combinações que o desenho exclui)

| Id | Provocação | Esperado — e o que comparar |
|---|---|---|
| K01 | triar uma direta e responder "AFK" ao modo | a triagem aceita ou recusa? Se aceita, a `sdd-desenvolver`, a `sdd-loop`, o planejamento (tarefas) e a `sdd-elm` precisam concordar no destino da fatia |
| K02 | `sdd-loop` com uma direta AFK no lote | "fica de fora: trilha direta" — e a fatia não pode ficar em estado nenhum |
| K03 | `sdd-prd`/`sdd-fatiar` com `AUTONOMO=true` e `EP-nn` no lote do loop | recusa em todas ("PRD e backlog nunca são AFK") |
| K04 | `AT-nnn` no `sdd-loop` e "[ATD]" pelo `sdd-orquestrador` | recusa; AT nunca ganha branch nem `status.md` |
| K05 | fatia HITL no `sdd-loop` | "fica de fora: HITL" |
| K06 | `[REV]`/`[VER]` de uma fatia AFK pedida no hub | não existem no EWM (Q8): o hub, a `sdd-revisar` e a `sdd-elm` devem dizer o mesmo |
| K07 | workflow `sdd-entregar-fatia` numa fatia HITL | a receita diz que é só AFK; o que ela faz de fato? |
| K08 | mudar o `modo` da fatia no backlog depois de iniciada (HITL → AFK) | o `status.md` copia o modo na criação: quem vence? Registrar a divergência |
| K09 | trilha rápida com `GATE na trilha rápida = sim` em AFK | GATE como no HITL (a trilha decide antes do modo) |
| K10 | mesma pergunta a duas skills (ex.: "qual a fase da FT-001?" ao `sdd-status` e ao hub) | respostas iguais |

## 3. Preparação do ambiente (C00)

### 3.1 Isolamento no git (nada vai para `desenvolvimento`)

| # | Ação | Verificação |
|---|---|---|
| 1 | Commitar antes a atualização 2.5.0 do pab-batch, que está no stage, para começar de árvore limpa | `git status` limpo |
| 2 | `git switch -c sdd-teste/base desenvolvimento` — **branch base de teste**, só local, nunca enviada | `git branch --show-current` |
| 3 | No steering **de teste** (passo 3.3): `Branch base` = `sdd-teste/base`, prefixo `sdd-teste/` | as branches de fatia nascem de `sdd-teste/base` |
| 4 | Push e PR **sempre "não"** nas confirmações; o "merge" é local: `git switch sdd-teste/base && git merge --squash sdd-teste/<ft> && git commit` | nenhum `git push` no histórico do shell |
| 5 | `.kiro/config/power/elm/pa_pab.json`: `ccm.clarity-identifier` = `xxxxxx` (restaurar com `git checkout --` na limpeza) | tarefas novas com Clarity `xxxxxx` |

> "Não commitar" vale para as branches reais. O fluxo **exige** commits (backlog, `status.md`, relatórios), e eles
> ficam só em `sdd-teste/*`, que é apagada no fim.

### 3.2 Produto isolado `.kiro/planejamento2`

| Arquivo | Conteúdo inicial |
|---|---|
| `backlog.md` | formato 2.5.0 vazio: `Próximos ids: EP-01 · FT-001 · AT-001`; `Sustentação:` com os pais de teste (3.4); seções `## Épicos`, `## Fatias — sem épico`, `## Atendimentos` |
| `planejamento/equipe.json` | cópia do real (valida no schema) |
| `planejamento/acordos.md` | cópia do real (cadência, WIP ≤ 2 por revisor, reserva 20%) |
| `planejamento/sprints/sprint-01.md` | `**Situação:** aberta`, iteração **Sprint Jandaia**, meta de teste, reserva calculada |
| `aprendizado/licoes.md` | `# Lições` |

### 3.3 Steering e agentes temporários

O `<produto>` vem do steering, e os agentes só escrevem no `{{PRODUTO}}` que a setup gravou. Para o teste:

| # | Ação | Restaurar no fim |
|---|---|---|
| 1 | `.kiro/steering/sdd.md`: `Pasta do produto` = `.kiro/planejamento2`; `Branch base` = `sdd-teste/base`; prefixo `sdd-teste/` | `git checkout -- .kiro/steering/sdd.md` |
| 2 | `.kiro/agents/sdd-*.json`: trocar `.kiro/planejamento/` por `.kiro/planejamento2/` nas regras de escrita e leitura | `git checkout -- .kiro/agents` |
| 3 | Tipo · pasta no RM: apontar HF, REG, GL e ET para a pasta `14-Lixeira` (só no steering de teste); `Publicar requisitos` = `na-aprovacao` | restaurado no item 1 |

### 3.4 ELM (PA PAB, iteração Sprint Jandaia)

| Item | Valor |
|---|---|
| PA | PAB · `_NV9GgHBcEeqtJpJfUp9v3A` · `.kiro/config/power/elm/pa_pab.json` |
| Iteração | **Sprint Jandaia** · `_ck8NALeGEfGZGNAHniZkPA` (2026-10-01 → 2026-12-18) |
| Prefixo em **todo** título criado | `[TESTE-SDD]`, para achar e cancelar no fim |
| Pais de teste | épico `[TESTE-SDD] SUS-teste` e IB `[TESTE-SDD] Atendimento` (filho dele), criados no C00 e gravados na linha `Sustentação:` do `backlog.md` de teste |
| DOORS (RM) e ETM | **DOORS:** publicar na pasta **`14-Lixeira`** do RM da PAB (`FR_PBbe9XBeEeqlM7DFIH2SZA`; vazia em 2026-10-16), com os tipos reais HF/REG/GL/ET. **ETM:** o usuário não enxerga área de projeto da PAB no ETM (só Janela Sisben, PA_MASTER, Prova de Vida, RPV e SIBE) → a importação do `CT.csv` **não é testável**; testar o roteiro manual e a pendência, e registrar o achado A-ETM (o steering do pab-batch configura colunas de `CT.csv` para um ETM que não existe para o projeto). Requisito publicado não se apaga pelo fluxo: fica na Lixeira |
| Pessoas | Dev, P.O. e Especificador = `daniel.xavier`. **Revisor e Verificador (QA) = `ricardo.saboia`, simulado**: as sessões de REV e VER rodam aqui, com o login do Daniel, no papel do Ricardo. No planejamento de teste, revisor e verificador das fatias HITL = `ricardo.saboia`, e a `[REV]`/`[VER]` nasce com ele como responsável |
| Simulação do Ricardo (desvios esperados, registrar como **ambiente**, não como achado do fluxo) | (1) *assumir*: a regra grava responsável = quem está na sessão (Daniel); no teste, a tarefa **fica com o Ricardo** — responder "não" à troca de responsável e seguir só com a mudança de estado; se o CCM recusar a mudança de estado por não ser o responsável, registrar e seguir com a fase no `status.md`. (2) **horas não são lançadas** nas tarefas do Ricardo: o esperado é `ELM pendente: lançar <h>h em [REV\|VER] FT-nnn (ricardo.saboia)` no lugar certo. (3) *concluir*: tentar; recusa do CCM → `ELM pendente: concluir …` e seguir. (4) commits do relatório e da fase saem com o autor git do Daniel |
| Clarity (horas fora da apuração da empresa) | no `pa_pab.json`, `ccm.clarity-identifier` = **`xxxxxx`** durante o teste (o campo "ID do Produto (Clarity)" da Tarefa é texto livre e opcional — conferido em 2026-10-16); toda tarefa `[TESTE-SDD]` nasce com ele, e as horas lançadas não entram no produto real `AP1648`. Restaurar na limpeza |

### 3.5 Material de código das fatias

As fatias mexem em código real do pab-batch, mas são **mudanças seguras e descartáveis**, numa branch de teste e
nunca mergeadas em `desenvolvimento`:

| Fatia | Pedido de teste |
|---|---|
| direta | texto de uma mensagem de log de um job |
| rápida | defeito simulado: validação que aceita um valor fora do limite, com o teste que o reproduz |
| padrão sem épico | regra nova pequena num processor (ficha com 2 cenários) |
| de épico | 2 fatias de um épico de teste "Relatório de teste de execução de jobs" (3 cenários) |

## 4. Estados de referência

### 4.1 Fase da fatia (`status.md`, branch da fatia)

| Evento | HITL | AFK |
|---|---|---|
| `sdd-desenvolver` começa | `pesquisando` (direta: `implementando`) | `pesquisando` |
| pesquisa pronta | `planejando` | `planejando` |
| plano escrito, esperando GATE | `plano-em-revisao` (exceto rápida com GATE = não) | só fatia de épico: `plano-em-revisao` |
| GATE aprovado / dispensado | `implementando` | `implementando` |
| Dev termina (PR aberto) | `pr-aberto` · `[DEV]` **concluída** | — |
| revisão por subagente | — | `revisando` |
| verificação por subagente | — | `verificando` → `aceita` |
| PR aberto (AFK) | — | `pronta-para-merge` · `[DEV]` concluída |
| Revisor **inicia** | `em-revisao` · `[REV]` em andamento | — |
| Revisor **aprova** | `em-verificacao` · `[REV]` concluída | — |
| Revisor **reprova** | `retrabalho (de: em-revisao)` · `[REV]` segue em andamento | — |
| Dev retoma o retrabalho | `implementando` · `[DEV]` **reaberta** | — |
| Dev atualiza o PR | `pr-aberto` · `[DEV]` concluída de novo | — |
| Verificador **inicia** (só com `em-verificacao`) | `em-verificacao` (não muda) · `[VER]` em andamento | — |
| Verificador **aceita** | `pronta-para-merge` · `[VER]` concluída | — |
| Verificador **rejeita** | `retrabalho (de: em-verificacao)` · `[VER]` segue em andamento | — |
| PR mergeado + `sdd-consolidar` | `concluida` | `concluida` |
| Bloqueio | `bloqueada (de: <fase>)` + campo Bloqueio | idem |

### 4.2 Linha da fatia no `backlog.md` (base)

`backlog` (falta algo) → `pronta` (DoR) → `concluida` (consolidar, com `concluida-em` e os ids de tarefa). "Em
andamento" **nunca** é gravado no backlog. `sprint` = nn quando prevista ou puxada; fatia puxada recebe `sprint` na
consolidação.

### 4.3 Tarefas no EWM

| Tarefa | Criada por | Assumida (em andamento) | Concluída |
|---|---|---|---|
| `[ESP] EP-nn` | planejamento | `sdd-especificar` (Passo 2) | `sdd-fatiar`, no GATE do backlog |
| `[DEV] FT-nnn` | planejamento ou `sdd-desenvolver` (se faltar) | `sdd-desenvolver` (Passo 4) | `sdd-implementar` Passo 5 (no PR) |
| `[REV] FT-nnn` | idem — **só fatia HITL**, nunca na direta | `sdd-revisar` (Passo 0) | `sdd-revisar`, ao aprovar |
| `[VER] FT-nnn` | idem — **só fatia HITL**, nunca na direta | `sdd-verificar` (Passo 0) | `sdd-verificar`, ao aceitar |
| `[ATD] AT-nnn` | `sdd-triar` (estado inicial) | `sdd-atender` (Passo 2) | `sdd-atender` (Passo 4) |
| IB da fatia | planejamento / `sdd-elm` modo backlog | — | `sdd-consolidar` |

Horas: lançadas a qualquer momento (ao fechar a sessão); na conclusão, **só o saldo**. No AFK, só na `[DEV]`.

## 5. Cenários passo a passo

Formato de cada passo: **o que dizer ao Kiro** (e em qual agente) → **estado esperado** → **artefatos** → **próximo**.
Legenda: `sm` = `status.md`; `bk` = `backlog.md`; `sp` = `sprint-01.md`.

### C06 · Épico — especificação (HITL)

| # | Ator · agente · pedido | Estado esperado | Artefatos | Próximo |
|---|---|---|---|---|
| 1 | P.O. · `sdd-produto` · "nova demanda: relatório de teste de execução de jobs com 3 situações…" | `bk` EP-01 `rascunho`, `prd` `—`; EWM épico `[TESTE-SDD] [EP-01]` criado | `bk` (linha + `pasta`), `epicos/EP-01-<slug>/rascunho.md` (pedido original), `decisoes.md` (cabeçalho do formato único); **1 commit** na base de teste após "não" em "mais algum item?" | "use `sdd-iniciar EP-01`" |
| 2 | P.O. · `sdd-produto` · "planejar a sprint" (só a Especificação) | `sp` seção Especificação com EP-01; EWM `[ESP] EP-01` na Jandaia, estado inicial | `sp`; commit | — |
| 3 | Especificador · `sdd-produto` · "iniciar o EP-01" | hub responde `sdd-especificar` e **para** | — | `sdd-especificar` |
| 4 | "especificar o EP-01" | `[ESP]` **em andamento**, responsável = você; pasta local criada a partir da base | `.kiro/local/especificacao/EP-01-<slug>/` (rascunho, decisoes) — **fora do git** | `sdd-prd` |
| 5 | `sdd-prd` · entrevista (2 rodadas) e escrita | `prd.md` `status: rascunho`/`em-revisao` na pasta local; base **sem** mudança | `decisoes.md` (D-01…), `prd.md`, `elm/HF-*`, `REG-*`, `index.md`, `log.md`; `revisao-prd-1.md` | — |
| 6 | "fechar a sessão de especificação" | `[ESP]` com 1 comentário (resumo, D-nn, dúvidas) e **anexos** `.md` (`elm-*` prefixados); horas lançadas, `[ESP]` **não** concluída | nenhum arquivo versionado | — |
| 7 | **Outra máquina** (simular: apagar a pasta local) · "retomar a especificação do EP-01" | pasta local recriada **pelos anexos**; mostra a data do último comentário | pasta local idêntica à do passo 6 | `sdd-prd` |
| 8 | Alterar algo localmente, depois retomar de novo, com a `[ESP]` mais nova | pergunta se baixa os anexos por cima (comparação de datas) | — | — |
| 9 | `sdd-prd` · GATE: "aprova o PRD" · `sdd-elm` modo *requisitos* (similares antes; publicação na `14-Lixeira`) | base: `prd.md` `aprovado` v1.0; conceitos `stable` + `verified` (lista) + `resource`/`id` do DOORS gravados de volta; `bk` EP-01 `aprovado` + link `prd`; repetir a publicação **não** cria duplicado | pasta copiada para `epicos/EP-01-<slug>/` (substitui rascunho e decisões da triagem) + `revisao-prd-1.md`; **1 commit** | `sdd-fatiar` |
| 10 | `sdd-fatiar` · fatiar e GATE do backlog | `bk` FT-001 e FT-002 em `## Fatias — EP-01`, `pronta`, modos HITL e AFK; EP-01 `fatiado`; `[ESP]` **concluída** com o **saldo** de horas; nada criado no EWM (`na-sprint`) | `bk`, `prd.md` (status), commit | `sdd-planejamento` |

### C01 · Direta · HITL

| # | Ator · pedido | Estado esperado | Artefatos | Próximo |
|---|---|---|---|---|
| 1 | P.O. · `sdd-triar` "ajustar a mensagem de log X" | `bk` FT `direta`, `P`, `pronta`, sem ficha | `bk`; commit único no fim da triagem | `sdd-iniciar` |
| 2 | P.O. · planejar (fatia na sprint) | `sp` linha; EWM **só `[DEV]`** (pai = Sustentação de teste) | `sp`, `bk` (`sprint`, `responsavel`) | — |
| 3 | Dev · `sdd-codificador` · "vamos trabalhar na FT-00x" | branch `sdd-teste/ft-…`; `sm` fase `implementando`; **sem** `.config.kiro`; `[DEV]` em andamento | `.kiro/specs/<ft>/status.md`; commit | `sdd-implementar` (Trilha direta) |
| 4 | Dev · `sdd-implementar` | revisão C sobre o diff (relatório **na conversa**); `sm` `pr-aberto` com o texto do PR (push "não") | commit da mudança + `sm` | merge |
| 5 | **Ponto de atenção:** a `[DEV]` é concluída aqui? A seção Trilha direta não diz | registrar o que acontece | — | — |
| 6 | merge local · `sdd-consolidar` | `sm` `concluida`; `bk` `concluida` + data + id da `[DEV]` | base: `sm`, `bk`; commit | `sdd-aprender` |

### C02 · Rápida · HITL (`GATE na trilha rápida = não`)

| # | Ator · pedido | Estado esperado | Artefatos | Próximo |
|---|---|---|---|---|
| 1 | P.O. · triar defeito simulado | `bk` FT `rápida`, `M`, HITL, `pronta` (ficha só se faltar o comportamento esperado) | `bk` (± ficha) | — |
| 2 | planejar | EWM `[DEV]`, `[REV]`, `[VER]` (HITL); `sp` com revisor e verificador ≠ dev | `sp`, `bk` | — |
| 3 | Dev · `sdd-desenvolver` | `sm` `pesquisando`; `.config.kiro` `specType: bugfix`; `[DEV]` em andamento | `sm`, `.config.kiro`; 1 commit | `sdd-plano` |
| 4 | `sdd-plano` | `research.md`; `bugfix.md` + `design.md` + `tasks.md` (teste que reproduz primeiro); `analise-plano-1.md` commitado com `sm`; **sem GATE** → `implementando`, Histórico "rápida sem GATE" | commit "registrar análise do plano 1" + commit "registrar plano" | `sdd-implementar` |
| 5 | `sdd-implementar` | 1 commit por tarefa (código, teste, `tasks.md`, `sm`); revisão automática **sem** arquivo; PR (texto); `[DEV]` horas + concluída; `sm` `pr-aberto` | — | Revisor |
| 6 | Revisor · `sdd-revisor` · "[REV] FT-…" | `[REV]` em andamento; `sm` `em-revisao`, Rodadas revisão = 1; `revisao-codigo-1.md` APROVADO; `sm` `em-verificacao`; `[REV]` concluída | relatório + `sm`, commitados pelo revisor | Verificador |
| 7 | Verificador · `sdd-verificador` · "[VER] FT-…" | `[VER]` em andamento; `sm` **continua** `em-verificacao`; ACEITO → `pronta-para-merge`; `[VER]` concluída | `verificacao.md`, `CT.csv`, `evidencias/`, `massa/`, `sm`; commit | merge |
| 8 | merge local · consolidar | `concluida`; IB/defeito de teste concluído | base: `sm`, `bk` | — |

### C04 · Padrão sem épico · HITL, com retrabalho pela REV

Igual ao C02, com estas diferenças:

| # | Diferença | Estado esperado |
|---|---|---|
| 1 | triagem | entrevista até fechar a ficha; **P.O. aprova a ficha** → `pronta`; ficha `aprovada por` |
| 4 | plano | `requirements.md` EARS; **GATE** → `plano-em-revisao` + commit; "aprovado" → `implementando` + Histórico com quem aprovou |
| 6 | Revisor **reprova** | `retrabalho (de: em-revisao)`; Rodadas retrabalho = 1; linha na tabela **Retrabalho** (REV, motivo); `[REV]` **segue em andamento**; commit |
| 6a | Dev · `sdd-desenvolver`/`sdd-implementar` | `[DEV]` **reaberta** (em andamento); achados viram tarefas `[R1]…`; `implementando` → PR atualizado → `pr-aberto`; horas do retrabalho na tabela; `[DEV]` concluída de novo |
| 6b | Revisor revê | Rodadas revisão = 2; APROVADO → `em-verificacao`; `[REV]` concluída |

### C07 · Padrão de épico · HITL, com retrabalho pela VER

Fatia FT-001 do C06. Diferenças em relação ao C04:

| # | Diferença | Estado esperado |
|---|---|---|
| 2 | planejamento | `sdd-elm` modo backlog cria o IB `[TESTE-SDD] [FT-001]` sob o épico (por causa do `na-sprint`); tarefas com pai = IB |
| 7 | Verificador **rejeita** | `retrabalho (de: em-verificacao)`; linha na tabela Retrabalho (VER); `[VER]` segue em andamento |
| 7a | Dev corrige | `[DEV]` reaberta → `pr-aberto` |
| 7b | Revisor | o PR mudou → a `[REV]` **já concluída é reaberta** (modo *assumir* com retrabalho) → revisão 2 → `em-verificacao` |
| 7c | Verificador | rodada 2 → ACEITO → `pronta-para-merge` |
| 8 | consolidar | ET *as-built* gerada e publicada na `14-Lixeira` (sessão padrão); `CT.csv`: sem ETM da PAB → roteiro manual + `ELM pendente: importar CT FT-001`, links **valida**/**testado por** pendentes (conferir que o fluxo diz isso em vez de travar) |

### C03 · Rápida · AFK (`sdd-loop`)

| # | Ator · pedido | Estado esperado | Artefatos |
|---|---|---|---|
| 1 | triar + planejar | EWM **só `[DEV]`** (sem `[REV]`/`[VER]`); `sp` sem revisor/verificador | `bk`, `sp` |
| 2 | Dev · `sdd-orquestrador` · "loop AFK" | confirmação única do lote; `[DEV]` assumida pelo responsável = quem disparou; worktree `.kiro/local/wt/<ft>` | `loop-<data>.md`, `sm` com `Responsável: agente:sdd-orquestrador` |
| 3 | fases do loop | `pesquisando` → `planejando` → `implementando` (sem GATE) → `revisando` → `verificando` → `aceita` | cada relatório commitado pelo orquestrador **antes** da fase seguinte (inclui `evidencias/`, `massa/`) |
| 4 | entrega (push/PR "não") | fica `aceita`; com PR autorizado seria `pronta-para-merge` + link | — |
| 5 | horas | tabela única com a `[DEV]` → horas + **conclusão** da `[DEV]` | — |
| 6 | consolidar | remove a worktree (sem `--force`) com "sim" | `git worktree list` sem a fatia |

### C05 · Padrão sem épico · AFK (workflows)

| # | Ação | Estado esperado |
|---|---|---|
| 1 | "rode o workflow `sdd-planejar-fatia` com fatia FT-…" | `research.md`, plano, `analise-plano-N.md` commitados; passo `registrar` → `implementando` (AFK sem épico) + commit "registrar plano" |
| 2 | "rode o workflow `sdd-entregar-fatia` com fatia FT-…" | REVISAR → `registrar_revisao` incrementa e commita, fase `implementando`; APROVADO → `verificando`; `registrar_verificacao` commita; ACEITO → `aceita` |
| 3 | `sdd-implementar` Passo 5 | PR (texto), `pronta-para-merge`, `[DEV]` concluída |

### C08 · Padrão de épico · AFK (`sdd-loop`)

| # | Diferença | Estado esperado |
|---|---|---|
| 3 | fase 4 do loop | fatia de épico **para** em `plano-em-revisao` (commit do plano); o lote segue com as outras |
| 3a | pessoa aprova o plano | o loop retoma a fatia até `aceita`/`pronta-para-merge` |

### C09 · Atendimento

| # | Ator · pedido | Estado esperado | Artefatos | Próximo |
|---|---|---|---|---|
| 1 | P.O. · `sdd-triar` "o cliente pediu a relação de X" | entrevista curta com **A-6 estimativa**; `bk` `## Atendimentos` AT-001 `aberto`, sprint 01; EWM `[TESTE-SDD] [ATD] AT-001` **no estado inicial**, filha do IB Atendimento de teste, na Jandaia | `atendimentos/AT-001-<slug>.md` (`Situação: aberto`, cabeçalho com A-1…A-6), linha na seção Atendimento do `sp`; commit único no fim | "mais algum item?" |
| 2 | "sim" + outro atendimento com estimativa acima da reserva | `status` `backlog`, `[ATD]` **sem** `plannedFor`; instrução "use `sdd-planejamento` (Encaixe)" | — | — |
| 3 | quem atende · `sdd-produto` · "atender o AT-001" | `[ATD]` em andamento; trabalho na base | registro (Consultas); extração em `.kiro/local/atendimentos/AT-001/` (**fora do git**) | — |
| 4 | "enviei a resposta" | saldo de horas → `[ATD]` **concluída**; tabela Horas do registro; `bk` `concluido` + data; `sp` | **1 commit** depois do Passo 5 (com a Saída) | desdobramentos |
| 5 | desdobramento "gerar alteração" | instrução "use `sdd-triar` com origem AT-001" | — | `sdd-triar` → FT com `origem` `AT-001` |
| 6 | negativo: pedido novo direto na `sdd-atender` | "use `sdd-triar`" e para | nada gravado | — |

### C10 · Hub, triagem em sequência e fluxo puxado

| # | Pedido | Esperado |
|---|---|---|
| 1 | `sdd-iniciar` "minha próxima tarefa" | lista **todas** as tarefas abertas da pessoa na Jandaia, **em andamento primeiro**, com a skill de cada uma |
| 2 | `sdd-iniciar` com `[REV]`, `[VER]`, `AT-nnn`, `EP-nn`, texto | encaminha para `sdd-revisar`, `sdd-verificar`, `sdd-atender`, `sdd-especificar`, `sdd-triar` e **para** |
| 3 | triar 3 itens seguidos ("sim", "sim", "não") | **1 commit** só, no "não"; resumo com ids, trilhas e pendências |
| 4 | fatia `pronta` no **topo** do backlog, fora da sprint, WIP com folga | `sdd-desenvolver` **puxa**: Histórico `Puxada para a sprint 01`; tarefas na Jandaia; na consolidação, `bk` `sprint` = 01 e linha `puxada` no `sp` |
| 5 | fatia que **não** é do topo, ou com o WIP no limite | Encaixe pela `sdd-planejamento` (decisão do P.O. registrada no `sp`) |

### C11 · Virada da sprint

| # | Pedido | Esperado |
|---|---|---|
| 1 | "fechar a sprint" com 1 fatia e 1 AT abertos | migram: "→ sprint 02" no `sp` antigo, linha `migrada da sprint 01` no `sprint-02.md`, `bk` `sprint` = 02; EWM só muda o `plannedFor` (aqui, a Jandaia continua: registrar) |
| 2 | reserva da sprint 02 | 20% das horas do time; o retrabalho migrado entra primeiro; o resto fica para atendimento |
| 3 | relatório de horas | por tipo e por pessoa; vazão (previstas + puxadas), lead time, meta atingida ou não |
| 4 | `equipe.json` → `historico` | entrada da sprint 01 **sem pontos**; valida no schema |

## 6. Integração entre skills (passagens)

Para cada linha: a skill A termina → a instrução aponta para B → B, chamada nesse estado, **aceita**. Se recusar
ou exigir outro estado, é achado.

| De → para | Estado na passagem | B deve |
|---|---|---|
| triar → iniciar | `bk` `pronta` | encaminhar ao papel |
| iniciar → desenvolver / revisar / verificar / especificar / atender | item registrado | assumir a própria tarefa e seguir |
| desenvolver → plano | `pesquisando` | começar pela `sdd-pesquisar` |
| plano → implementar | `implementando` (+ plano commitado) | Passo 0 com árvore limpa |
| implementar (HITL) → revisar | `pr-aberto`, `[DEV]` concluída | assumir `[REV]`, ir a `em-revisao` |
| revisar (aprova) → verificar | `em-verificacao` | assumir `[VER]`; com `pr-aberto` deve **recusar sem assumir** |
| revisar/verificar (reprova) → implementar | `retrabalho (de: …)` | reabrir `[DEV]` e corrigir |
| verificar (aceita) → consolidar | `pronta-para-merge` + merge | aceitar (e também `pr-aberto`/`aceita` de versões antigas) |
| implementar (AFK) → consolidar | `pronta-para-merge` | idem |
| especificar → prd | pasta local montada | trabalhar na pasta local, não na base |
| prd (GATE) → fatiar | `aprovado` na base | fatiar e concluir a `[ESP]` no GATE do backlog |
| triar (AT) → atender | AT `aberto`, `[ATD]` estado inicial | assumir a `[ATD]` |
| atender → triar | desdobramento "alteração" | nova FT com `origem AT-nnn` |
| status (fechar sessão) | qualquer fase | perguntar horas da sessão, propor commit, frase de retomada |

## 7. Validação de conteúdo dos artefatos

| Artefato | Conferir |
|---|---|
| `backlog.md` | `Próximos ids` só cresce (EP, FT, AT); uma linha por item; colunas na ordem do formato; `—` nas vazias; `pasta` nos épicos; `## Atendimentos`; sem "em andamento"; sem `\|` dentro de célula |
| ficha `FT-nnn-<slug>.md` | cenários `C<n>`; Decisões no formato do `decisoes.md`; `aprovada por <P.O.> em <data>` |
| `decisoes.md` | título `# Decisões — <id> <título>`; tabela `D \| Pergunta \| Decisão \| Fonte / quem decidiu \| Data \| Situação`; só acréscimo |
| `prd.md` + `elm/*.md` | frontmatter `status`; versão; conceito OKF com `status: stable` e `verified` em **lista** com `by: human:<login de quem aprovou>`; `index.md` e `log.md` atualizados |
| `status.md` | campos Fatia, Origem, Trilha (com acento), Modo (= backlog), Cobre, Branch, Fase, Responsável, Rodadas (4 contadores), PR, Bloqueio, ELM (ids das tarefas), Banco; Histórico só acréscimo, com data; tabela Retrabalho no HITL |
| `research.md` | só fatos com `arquivo:linha`; seção "Não encontrado"; ≤ ~150 linhas |
| `requirements.md` / `bugfix.md` | EARS falsificável; só o que a fatia cobre |
| `design.md` | forma do programa, pontos de teste, **contrato de pronto** |
| `tasks.md` | `_Requirements: N.M_`; corretiva começa pelo teste que reproduz; `[x]` só com backpressure verde |
| `analise-plano-N.md` / `revisao-codigo-N.md` | `<N>` = a rodada passada; última linha = fecho da rubrica (`ANALISE: OK`, `VEREDITO: APROVADO`); eixos spec e padrões separados |
| `verificacao.md` + `evidencias/` | um bloco por cenário (massa, executar, esperado, verificar em) + evidência; dado real só em `.kiro/local/verificacao/` |
| `CT.csv` | colunas na ordem do steering (Tipo · Resumo · Responsável · Status · Categoria · Planejado para · Descrição); um caso por cenário aceito |
| `AT-nnn-<slug>.md` | cabeçalho A-1…A-6; Consultas sem dado pessoal; Resposta enviada; tabela Horas; `ELM:`; `Saída:` |
| `sprint-01.md` | seções Fatias, Especificação, Atendimento; reserva (atendimento + retrabalho) e consumido; Observações `puxada` / `encaixe` / `migrada` |
| `equipe.json` | valida no schema; um P.O. ativo; `papeis` em lista |
| EWM | títulos `[TESTE-SDD] [DEV] FT-nnn …`; pai certo; `plannedFor` = Jandaia; classificação e campos obrigatórios da PA; horas por data; comentários e anexos da `[ESP]` |
| Mensagens de commit | no padrão `Task <id> - …` com o texto do fluxo (`registrar plano`, `registrar revisão <N>` …) |

## 8. Bordas e negativos (C12)

| Id | Situação provocada | Esperado |
|---|---|---|
| B01 | DoR falha (ficha não aprovada) e "vamos trabalhar" | `sdd-desenvolver` não começa e aponta o que falta |
| B02 | WIP no limite | mostra as fatias paradas, recomenda destravar; seguir mesmo assim → `WIP excedido` no Histórico |
| B03 | 2ª reprovação seguida (AFK) | `bloqueada (de: revisando)` com as 3 opções |
| B04 | 2ª rejeição seguida da verificação (AFK e workflow) | `bloqueada (de: verificando)` |
| B05 | verificador chamado com `pr-aberto` (REV não aprovou) | recusa **antes** de assumir a `[VER]` |
| B06 | `[REV]` atribuída a outra pessoa | mostra quem é; assume só com "sim" |
| B07 | power `elm` desligado na sessão | todas as escritas no ELM viram `ELM pendente` no lugar certo; `sdd-status` lista; depois "resolve as pendências do ELM" baixa com `ELM feito:` |
| B08 | publicação interrompida: criar a `[DEV]` e apagar o id do `sm` | o modo *sprint* acha pela busca (prefixo + id + pai) e **não duplica** |
| B09 | falha de escrita: tirar a permissão de uma pasta | `bloqueada (de: <fase>)` com o caminho |
| B10 | `⚠️ ambiente` (banco fora) em 1 fatia do loop; depois em 2 | 1 → só ela bloqueada; 2 → para o lote |
| B11 | árvore suja no Passo 0 só com Histórico | commita primeiro e segue |
| B12 | squash merge na consolidação | merge confirmado; `--merged` não basta |
| B13 | pedido de ET dentro do `sdd-produto` | "use a `sdd-consolidar`" |
| B14 | setup dentro de um agente `sdd-*` | pede a sessão padrão e para |

| B15 | sessão sem o power `sdd` (agente sem `includePowers` e sem `resources`) | o agente não acha as skills: o que ele diz? |
| B16 | duas pessoas triando ao mesmo tempo (mesmo `FT-nnn`) | conflito de id no push: regra do backlog (mantém o remoto, pega o próximo id, troca o título no EWM) |
| B17 | `sdd-status` em cada fase de cada cenário | painel coerente com o `status.md` (fase, WIP, esperando revisão/verificação, retrabalho, pendências de ELM) |

## 8.1 C13 · Varredura de consistência ao fim de cada cenário

Depois do último passo de cada cenário, sem pedir nada ao fluxo, conferir **por fora**:

| Checagem | Como |
|---|---|
| fase do `sm` × status do `bk` × estados no EWM contam a mesma história | ler os três e cruzar (tabela da seção 4) |
| todo id citado no `sm` (campo ELM) existe no EWM com o título, o pai e a iteração certos | `elm-ccm` › ler item |
| todo arquivo citado num relatório ou no texto do PR existe na branch (`git ls-files`) | — |
| Rodadas no `sm` = quantidade de `analise-plano-*`, `revisao-codigo-*` e rodadas de verificação | contar |
| horas lançadas no EWM = linhas da tabela Horas (AT) e da tabela Retrabalho | `elm-ccm` › horas lançadas |
| `git status` limpo e `git log` com as mensagens do fluxo | — |
| nada fora do lugar: dado real fora de `.kiro/local/`, `backlog.md` alterado numa branch de fatia, commit em `desenvolvimento` | `git log desenvolvimento`, `git diff sdd-teste/base…<ft> -- .kiro/planejamento2` vazio |

## 9. Limpeza (obrigatória)

| # | Ação | Verificação |
|---|---|---|
| 1 | `git switch desenvolvimento`; restaurar `.kiro/steering/sdd.md`, `.kiro/agents/` e `.kiro/config/power/elm/pa_pab.json` (`git checkout --`) | `git diff` vazio; `clarity-identifier` de volta a `AP1648` |
| 2 | remover worktrees `.kiro/local/wt/*` (`git worktree remove`, sem `--force`) | `git worktree list` |
| 3 | apagar as branches `sdd-teste/*` (`git branch -D`, pela pessoa) | `git branch --list 'sdd-teste/*'` vazio |
| 4 | apagar `.kiro/planejamento2/`, `.kiro/local/especificacao/`, `.kiro/local/atendimentos/AT-*` e `.kiro/local/verificacao/` de teste | `ls` |
| 5 | EWM: todos os itens `[TESTE-SDD]` → estado **Cancelado** (as horas lançadas neles ficam no EWM, mas com Clarity `xxxxxx`) (o fluxo nunca apaga; cancelar pela `elm-ccm`, com "sim", ou na UI) | busca por `[TESTE-SDD]` na PA PAB só com cancelados |
| 5a | DOORS: os requisitos de teste ficam na `14-Lixeira`; se o time quiser, a pessoa os remove na UI | `14-Lixeira` só com itens `[TESTE-SDD]` |
| 6 | conferir que nada foi enviado: `git log origin/desenvolvimento..desenvolvimento` vazio; nenhum PR aberto | — |

## 10. Registro de resultados

Uma linha por passo executado (planilha ou `.kiro/local/teste-sdd/resultado.md`, fora do git):

| Cenário · passo | Data | Estado obtido (sm · bk · EWM) | Artefatos conferidos | Próxima skill indicada | Resultado | Achado (esperado × obtido · regra arquivo:linha · severidade) |
|---|---|---|---|---|---|---|

**Pontos de atenção já conhecidos** (testar de propósito):
0. Toda tarefa criada no teste tem "ID do Produto (Clarity)" = `xxxxxx` (conferir no EWM antes do primeiro lançamento de horas); se alguma nascer com `AP1648`, pare e corrija antes de lançar.
1. Trilha direta: quando a `[DEV]` é concluída (a seção Trilha direta não chama o Passo 5, item 4).
2. Direta HITL termina em `pr-aberto` e vai direto ao merge, sem `pronta-para-merge`.
3. `includePowers: true`: o agente recebe o MCP do `elm`? Toda tool pede confirmação (nenhuma em `allowedTools`)?
4. Sprint Jandaia dura 11 semanas e a sprint de teste é de 2: a virada (C11) mantém a mesma iteração no EWM.
