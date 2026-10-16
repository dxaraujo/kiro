# Correções do power `sdd` a partir do teste de fluxos (v2.5.1 → v2.6.0)

> Origem: execução do `docs/plano-teste-sdd-v2.5.0.md` (C00–C13, K01–K10, B01–B17) no pab-batch, 2026-10-16/17.
> 64 achados (A1–A64, A-ETM); o registro completo fica fora do git (`.kiro/local/teste-sdd/resultado.md` do projeto).
> Aqui: o que muda nas skills, por etapa. Achados de dado do projeto, da PA ou do MCP estão no fim.
> **Aplicado** em 2026-10-17: sdd 2.6.0, elm 1.3.1, mcp-elm 1.0.39 (A28). Padrões que a PA exige ("Planejado para",
> "Atendido por") ficam numa linha nova do `sdd.md` — "Padrões do EWM" —, não no `pa_*.json` (que é do power `elm`).

## Decisões do dono

| Achados | Decisão |
|---|---|
| A2 | a tabela Fatias do `sprint-<nn>.md` ganha a coluna **Tarefa ELM** |
| A27, A29, A30 | **toda fatia tem `fatias/FT-nnn-<slug>.md`** (triagem: sem épico · fatiamento: de épico) com **O que fazer**, **Critérios de aceite**, **Como verificar**. Direta: "Pronto quando" + "Como verificar" + "Não muda", uma linha cada (não cabe → não é direta), perguntados numa rodada com recomendação; a revisão C julga contra eles; a evidência do "Como verificar" vai no PR curto. Rápida: atual × esperado × não muda (vira o `bugfix.md`). Padrão sem épico: a ficha de hoje. Padrão de épico: objetivo + links para os cenários do PRD (`cobre`), sem copiar. Coluna `ficha` sempre preenchida; a DoR confere no arquivo. Atendimento fica fora |
| A41 | o GATE do backlog **exige uma fatia ponta a ponta** (do gatilho à saída) — sem ela, o fatiamento não passa |
| A59 | plano que **muda a expectativa de um teste existente** declara isso e **força o GATE** (`plano-em-revisao`), mesmo com `GATE na trilha rápida = não`; a decisão fica no `bugfix.md`/`requirements.md` |
| A35, A36 | **assumir a 1ª `[DEV]` inicia o IB** (estado em andamento da PA; responsável continua o P.O.); a consolidação conclui o IB pelas transições da PA |
| A38 | reabrir no retrabalho = **duas transições** (reabrir → estado inicial; iniciar → em andamento), mesmo onde a PA tem atalho |

## Etapa 1 — Toda fatia tem ficha; direta fecha a `[DEV]` (A2, A3, A23–A27, A29, A30)

| Achado | Correção | Arquivos |
|---|---|---|
| A27/A29/A30 | ficha por trilha (formatos acima); coluna `ficha` obrigatória; DoR de cada trilha confere a ficha | `sdd-triar`, `sdd-triar/references/ficha.md`, `sdd-fatiar` (+ `references/backlog.md`), `sdd-desenvolver` (DoR), `sdd-revisar` (direta contra a ficha), `sdd-implementar` (Trilha direta: PR curto com a evidência do "Como verificar") |
| A24 | a Trilha direta chama o Passo 5, item 4 (conclusão da `[DEV]`) | `sdd-implementar` |
| A23/A25 | sem PR (push "não" ou sem ferramenta): `PR: texto entregue` e a fase segue (`pr-aberto` na direta/HITL); a consolidação aceita `pr-aberto` da direta como estado final antes do merge | `sdd-implementar`, `sdd-consolidar` |
| A26 | squash/merge local sem PR: a consolidação pergunta à pessoa e confere pelo conteúdo (`git diff <base> <branch> -- <arquivos da fatia>` vazio) | `sdd-consolidar` |
| A2/A3 | coluna Tarefa ELM na tabela Fatias; Capacidade com "Reserva (atendimento + retrabalho)" | `sdd-planejamento/references/arquivos.md`, `sdd-elm` (modo sprint grava a coluna) |

## Etapa 2 — Triagem, épico e atendimento (A5, A6, A12–A14, A20, A21, A48, A52, A53)

| Achado | Correção | Arquivos |
|---|---|---|
| A5/A52 | PA que exige "Planejado para": épico, IB da triagem e `[ATD]` fora da sprint vão para a **iteração de backlog** da linha "Padrões do EWM" do `sdd.md`; sem ela → a `sdd-elm` pergunta e oferece gravar | `sdd-triar`, `sdd-elm`, `sdd-setup`, template do `sdd.md` |
| A6 | commit da triagem: `Task <id do épico de Sustentação>`; épico: o id do épico | `sdd-triar` |
| A12 | DoR do épico e a descrição gravada pela triagem usam o mesmo mínimo (problema + quem pede + resultado esperado) | `sdd-triar`, `sdd-fatiar/references/backlog.md` |
| A13 | `## Épicos` ganha a coluna `po` (padrão: o P.O. ativo do `equipe.json`); o épico nasce no EWM com responsável = P.O. | `sdd-fatiar/references/backlog.md`, `sdd-triar`, `sdd-elm` |
| A14 | a triagem retoma um `EP-nn` em `backlog` (completa o que falta) | `sdd-triar` |
| A20 | `sdd-especificar` atualiza a linha do épico na seção Especificação do `sprint-<nn>.md` | `sdd-especificar` |
| A21 | o modo sprint cria a Sustentação/Atendimento quando a linha `Sustentação:` está vazia (a direta não passa pelo modo backlog) | `sdd-elm` |
| A48 | direta não tem modo: a triagem grava `—`; a coluna `modo` só vale para padrão e rápida | `sdd-triar`, `sdd-fatiar/references/backlog.md` |
| A53 | o registro `AT-nnn` ganha `**Estimativa:**` no cabeçalho | `sdd-atender` |

## Etapa 3 — ELM (A7, A9, A10, A15, A16, A18, A35/A36, A38, A47, A60, A62, A63)

| Achado | Correção | Arquivos |
|---|---|---|
| A7 | enumeração vai pelo identifier (nunca o nome) na operação criar/atualizar item | `elm-ccm` (contrato), `sdd-elm` |
| A9 | "Atendido por" (categoria do time, `filedAgainst`) entra no contrato da `elm-ccm` e na linha "Padrões do EWM" do `sdd.md` | `elm-ccm`, `sdd-elm`, `sdd-setup` |
| A10 | planos criados pelo modo sprint gravam o id em `ccm.iterations[].plans` | `sdd-elm` |
| A15/A16 | `okf-elm.md`: `verified` de quem aprovou (decisão 0.17) e "Onde fica" com as duas pastas (local até o GATE, `<produto>/epicos/<EP>/elm/` depois) | `sdd-prd/references/okf-elm.md` |
| A18 | comparação de datas em UTC; arquivo baixado usa a data do ELM, não o mtime | `sdd-prd` / `elm-sync` (onde compara) |
| A35/A36 | modo assumir: 1ª `[DEV]` iniciada → IB para o estado em andamento (responsável = P.O., gravado se faltar); modo conclusão do IB percorre as transições da PA; recusa sem mudança de estado vira mensagem com a pré-condição | `sdd-elm` |
| A38 | retrabalho: reabrir (→ estado inicial) e iniciar (→ em andamento), duas transições, na mesma confirmação | `sdd-elm` (assumir, linha "concluída") |
| A47 | épico `concluido` → concluir o item do épico no EWM (modo conclusão) | `sdd-consolidar`, `sdd-elm` |
| A60 | fatia HITL puxada: a `sdd-desenvolver` pergunta revisor e verificador (sugere pelo `equipe.json`) antes de criar `[REV]`/`[VER]`; a consolidação grava na linha `puxada` | `sdd-desenvolver` |
| A62 | iteração do EWM mais longa que a sprint: a virada não muda `plannedFor` e o relatório de horas filtra pelas tarefas da sprint (`sprint-<nn>.md`) | `sdd-planejamento`, `sdd-elm` (horas) |
| A63 | pendência com chave: `ELM pendente [<chave>]: …` e `ELM feito [<chave>]: …`; a `sdd-status` casa pela chave | `sdd-status`, `sdd-elm`, `sdd-consolidar`, `status-template.md` |

## Etapa 4 — Plano, revisão e rubricas (A17, A31–A33, A40, A41, A59)

| Achado | Correção | Arquivos |
|---|---|---|
| A40 | L1 e C2: todo valor visível do "Então" do cenário aparece igual no Esperado do contrato de pronto e no teste | `sdd-revisar/references/rubricas.md`, `sdd-plano/references/plano-templates.md` |
| A41 | GATE do backlog: ao menos uma fatia ponta a ponta (gatilho → saída observável); épico só `concluido` com ela concluída | `sdd-fatiar`, `sdd-consolidar` |
| A59 | plano que muda expectativa de teste existente: seção "Testes existentes que mudam" + GATE obrigatório; L3/C4 conferem | `sdd-plano`, `rubricas.md`, `plano-templates.md` |
| A32 | bugfix: o teste do defeito (vermelho) e a correção fecham num ciclo só (um commit verde) | `sdd-implementar`, `plano-templates.md` |
| A33 | o gate de cobertura vale para o que a fatia tocou; falta pré-existente fora do diff vira registro, não tarefa | `sdd-implementar`, `rubricas.md` (C3) |
| A31 | template do `.config.kiro`: só `uuidgen` | `plano-templates.md` |
| A17 | o revisor grava `revisao-prd-<N>.md` em `.kiro/local/especificacao/**` (permissão do agente) | `sdd-setup/assets/agents/sdd-revisor.json`, `sdd-setup/references/agentes.md` |

## Etapa 5 — Loop e workflows (A39, A42–A46, A49–A51, A54–A57)

| Achado | Correção | Arquivos |
|---|---|---|
| A39 | o loop segue a regra de puxar da `sdd-desenvolver` (topo + WIP) e cria a `[DEV]` que faltar (modo sprint) | `sdd-loop` |
| A42 | "próxima fatia" e o loop pulam fatia com `status.md` em qualquer branch/worktree | `sdd-desenvolver`, `sdd-loop` |
| A43 | horas e conclusão no fim do lote valem para toda fatia que chegou a `aceita` | `sdd-loop` |
| A44 | `plano-em-revisao`: `Responsável` = quem aprova (sugestão: o revisor do PR; épico: P.O. ou revisor) | `sdd-loop`, `sdd-plano` |
| A45 | AFK: tabela Retrabalho no `status.md`; REJEITADO → implementação → **nova revisão C** → verificação | `sdd-loop`, workflow entregar |
| A46 | `CT.csv` no AFK: responsável = quem disparou | `sdd-verificar` |
| A49 | workflow planejar: o passo `plano` commita o plano ("registrar plano (rascunho)") antes da análise | `sdd-planejar-fatia.workflow.json` |
| A50 | a descrição das receitas pede a fatia sempre com a mesma grafia (o `stopCondition` lê `{{fatia}}` como digitada; o motor não normaliza, então a pasta não pode ser forçada para minúsculas) | os dois workflows |
| A51 | workflow entregar: `implementar` também lê os cenários REJEITADO do último `verificacao.md` | `sdd-entregar-fatia.workflow.json` |
| A54 | workflow entregar: 1º passo confere `Modo: AFK` e para se HITL | `sdd-entregar-fatia.workflow.json` |
| A55 | modo mudado depois de iniciada: vale o `backlog.md`; a `sdd-desenvolver` atualiza o `status.md` e cria/cancela `[REV]`/`[VER]` com "sim" | `sdd-desenvolver` |
| A56 | ordem da regra do GATE em todos os lugares: trilha rápida primeiro (`GATE na trilha rápida`), depois o modo | `sdd-loop`, workflow planejar, template do `sdd.md` (`sdd-setup`) |
| A57 | recusa explícita: EP/AT no loop ("PRD, backlog e atendimento nunca são AFK") | `sdd-loop`, `sdd-prd`, `sdd-fatiar` |

## Etapa 6 — Hub, painel e planejamento (A1, A4, A11, A22, A58, A61)

| Achado | Correção | Arquivos |
|---|---|---|
| A58 | "minha próxima tarefa": tarefa sem tipo do sdd aparece como "fora do sdd" (sem skill) | `sdd-iniciar` |
| A61 | reserva: o % é o dos acordos; a virada mostra o consumido e **propõe** novo % ao P.O. (muda o acordo só com "ok") | `sdd-planejamento` |
| A4/A22 | base sem upstream: `git fetch` basta; "registro publicado" sem remoto → pula e avisa | `sdd-desenvolver`, `sdd-fatiar/references/backlog.md` (Gravar na base) |
| A11 | planejamento: ninguém com horas de especificação e épico a especificar → avisa antes de planejar `[ESP]` | `sdd-planejamento` |
| A1 | `sdd-status`/`sdd-setup`: layout antigo (arquivos na raiz de `<produto>/planejamento/`) → oferece mover | `sdd-setup`, `sdd-status` |

## Fora das skills

| Achado | Onde | Ação |
|---|---|---|
| A8, A19, A-ETM | dados do pab-batch | A19 feito (`b65813f11`); A8: classificação por prefixo no `pa_pab.json`; A-ETM: pedir acesso ao ETM da PAB |
| A28 | mcp-elm `ccm_list_timesheet` | feito no 1.0.39: `total_hours` com −1 ms ("sem horas") vira 0, com teste — publicar no PyPI |
| A34 | mcp-elm `rm_count_folder` | sem bug: atraso de índice do servidor logo após criar — conferido em 2026-10-17, `rm_count_folder` e `rm_list_folder` dão 12 e 12 na `14-Lixeira`, com os itens do teste |
| A37 | mcp-elm | corrigido no 1.0.38 |
| A64 | PA PAB | 3 tarefas filhas de IB cancelado não mudam de estado — cancelar na UI |

## Pós-correção (2026-10-17)

- Descrições da `sdd-elm` e da `sdd-triar` passavam de 1024 caracteres (já antes desta rodada) e o Kiro pulava as
  duas skills: encurtadas (`116e375`); as 33 skills com frontmatter válido.
- pab-batch (`desenvolvimento`, sem commit): `sdd.md` com a linha "Padrões do EWM" (Atendido por `Manutenção-CE`,
  iteração de backlog a definir) e o texto novo do GATE; `sdd-revisor.json` com a permissão da revisão do PRD local.
  As 3 fatias do backlog real já têm ficha. O layout é o antigo (A1): `acordos.md`, `equipe.json` e `sprints/` na
  raiz de `.kiro/planejamento/` — a `sdd-setup` oferece mover.

