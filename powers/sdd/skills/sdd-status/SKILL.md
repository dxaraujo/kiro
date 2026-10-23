---
name: sdd-status
description: "Painel do fluxo sdd, somente leitura — onde parei e o que fazer agora: fatias em andamento (nesta branch, nas worktrees e nas branches remotas) com fase, trilha, modo AFK/HITL, progresso do tasks.md, achados abertos e PR; WIP de revisão humana contra o acordo do time; sprint atual e meta, com especificação e atendimento (reserva × consumido); fatias prontas para começar; épicos e PRDs pendentes de aprovação; pendências de ELM; lições propostas; e inconsistências. Também fecha a sessão de trabalho numa fatia (atualiza o status.md, lança as horas da sessão com confirmação, registra os créditos do Kiro, deixa o git pronto para commit e diz como retomar). SEMPRE use esta skill (leia-a antes de responder) em \"onde parei\", \"status\", \"painel\", \"bom dia\", \"o que tem pendente\", \"qual a próxima fatia\", \"como está a sprint\", \"retomar\", \"fechar a sessão\", \"encerrar por hoje\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.0.0"
---

# sdd-status — Onde parei

O painel é somente leitura: não altera arquivo, branch nem ELM. Pedido de **fechar a sessão** → modo da última
seção. Sem `.kiro/steering/sdd.md` → diga que o fluxo não está configurado e ofereça a `sdd-setup`.

## Coleta

1. `git fetch --quiet`. Pastas `.kiro/specs/*/status.md` da branch atual, de cada worktree (`git worktree list`)
   e de cada branch remota (`git for-each-ref --format='%(refname:short)' refs/remotes/origin/`, ignorando
   `HEAD`; `git ls-tree -r --name-only <ref> -- .kiro/specs/` e `git show <ref>:<caminho>`). A pasta da fatia
   costuma existir só na branch dela.
2. De cada `status.md`: fatia, título, trilha, modo, fase, responsável, rodadas, achados abertos, PR, ELM,
   Banco, última linha do Histórico (data) e pendências `ELM pendente [<chave>]:` sem `ELM feito` com a **mesma chave** (pendência antiga, sem chave → liste com "sem chave: confira") (também
   no campo `**ELM:**` dos `AT-*.md` abertos e na coluna "Tarefa ELM" `pendente` da sprint aberta).
   PR das fatias em `pr-aberto`, `em-revisao`, `em-verificacao`, `retrabalho`, `pronta-para-merge` ou `mergeada`:
   `gitlab_listar_mrs(origem=<branch>, estado=all)` (MCP `gitlabpr`, só leitura) — estado, conflitos e link;
   `merged` → próximo passo `sdd-consolidar`, do P.O. ou do SM no agente `sdd-produto` (fase ainda `pronta-para-merge` → o Dev registra `mergeada` e conclui a `[DEV]`); `closed` sem merge → inconsistência. Sem o MCP → o link do `status.md`.
3. De cada `tasks.md`: `[x]`/total e o primeiro item pendente.
4. `<produto>/backlog.md` (da base): épicos por status, fatias `pronta` sem `status.md` em nenhuma branch,
   sprint atual (`<produto>/sprints/` de maior número com `**Situação:** aberta`) e a meta. "Em andamento" = fatia com
   `status.md` numa branch e fase diferente de `concluida`, e não `concluida` na base (a branch mergeada fica em
   `mergeada`; quem fecha é a consolidação, na base); o backlog não guarda isso.
   PRDs (`epicos/*/prd.md`): status e pendências `ELM pendente [<chave>]:` do rodapé.
5. `<produto>/acordos.md`: limites de WIP (sem o arquivo: 2 fatias esperando pessoa, e sugira a
   `sdd-planejamento` modo inicial). Sem `<produto>/equipe.json` → sugira o mesmo modo inicial: sem ele não há
   senioridade (modo da fatia, GATE do plano, quem revisa).
6. `<produto>/aprendizado/licoes.md`: lições com situação `proposta`.
   Sprint aberta (`sprint-<nn>.md`): seções Especificação e Atendimento (reserva × consumido) e as linhas
   `ELM pendente [<chave>]:`. Atendimentos abertos: as linhas `aberto` e `backlog` de `## Atendimentos` do `backlog.md`
   (backlog antigo, sem a seção: os `AT-*.md` com `**Situação:** aberto`).
7. Lotes autônomos em andamento: `.kiro/local/loop-*.md`.
8. "Minhas" = responsável igual ao login da pessoa: `git config user.name` cruzado com `nome`/`login` do
   `equipe.json`; sem correspondência, pergunte o login uma vez.

## Painel

```
📊 sdd — <projeto> · sprint <nn> (<dias> dias restantes) · meta: <…>

🔨 Em andamento
| FT | Título | Fase | Modo | Tarefas | Achados | PR | Parada há | Próximo passo |

👀 Esperando pessoa (WIP de revisão: <n>/<limite> — plano-em-revisao + pr-aberto + em-revisao + em-verificacao + aceita + pronta-para-merge)
- FT-031 plano-em-revisao há 1 dia → aprovar o plano: [APR] de <Dev Sênior> (sdd-revisar, Aprovação do plano)
- FT-029 pr-aberto há 2 dias → esperando revisão: [REV] de <revisor> (sdd-revisar) <link>
- FT-028 em-verificacao → esperando verificação: [VER] de <verificador> (sdd-verificar)
- FT-027 pronta-para-merge → merge pelo Dev responsável (<login>, sdd-desenvolver Passo 6) <link> · AFK, antes: [APR] Aprovar PR de <Dev Sênior> (sdd-revisar)
- FT-026 bloqueada: aguardando troca para HITL → P.O. (sdd-planejamento, Troca de modo)
- FT-025 mergeada há 1 dia → consolidar: P.O. ou SM (sdd-consolidar, agente sdd-produto, horas na [GB])
- FT-030 aceita (AFK) → abrir o PR (sdd-implementar)
🔁 Retrabalho: FT-026 (de: em-revisao) → o codificador retoma no mesmo PR (sdd-implementar)

✅ Prontas para começar (por prioridade)
| FT | Título | Tam. | Modo | Depende de |

📄 Produto
- EP-04 PRD em-revisao · EP-05 a descobrir
- Especificação na sprint: EP-05 (rita.melo) PRD · 8/16 h

🎧 Reserva (atendimento + retrabalho): <h>h · consumido <h>h (retrabalho <x>h · AT <y>h) · abertos: AT-012 (joao.lima, prazo 2026-10-16)

🏛️ ELM pendente: <n> (lista) · 🔁 Lições propostas: <n>
⚠️ Inconsistências: <lista | nenhuma>

👉 Sugestão: <a ação de maior alavanca agora>
```

**Sugestão** — nesta ordem: desbloquear quem espera uma pessoa (plano ou PR parado, WIP de revisão estourado) →
atendimento com prazo vencendo → terminar a fatia em andamento → começar a próxima pronta (AFK prontas em quantidade → ofereça o `sdd-loop`) →
trabalho de produto (PRD/fatiar) para manter o backlog com fatias prontas.

## Inconsistências a apontar

- fase `pr-aberto` sem PR (nem `PR: texto entregue`), ou com tarefas pendentes no `tasks.md`;
- fatia sem ficha (coluna `ficha` `—` ou arquivo inexistente) marcada `pronta`;
- `ELM pendente` sem chave (formato antigo) — liste à parte, para a pessoa conferir à mão;
- layout antigo do produto: subpasta `<produto>/planejamento/` (o lugar de `equipe.json`, `acordos.md`,
  `roadmap.md` e `sprints/` é a raiz de `<produto>/`) — ofereça a `sdd-setup` para mover (com "ok");
- fatia `concluida` no `status.md` e não no `backlog.md` (ou o contrário);
- fatia em andamento sem commit há mais de 3 dias úteis;
- `concluida` com Banco = `pendente` ou `aplicada em dev` (implantação bloqueada);
- Histórico fora de ordem cronológica ou fase que não bate com a última linha (conflito mal resolvido);
- conceito de `elm/` com `verified` humano e sem `resource` há mais de 1 dia (projeto que publica na aprovação);
- conceito de `elm/` alterado (`generated.at`) depois do último `verified` e ainda `stable` (falta reaprovar);
- `backlog.md` alterado numa branch de fatia (deve mudar só na base);
- reserva de atendimento estourada (consumido > reserva) sem decisão do P.O. registrada no `sprint-<nn>.md`;
- arquivo com dado de cliente versionado (extração, CSV ou evidência fora de `.kiro/local/`).

Tarefa concluída **sem horas lançadas** não é apontada aqui: só no fechamento da sprint (`sdd-planejamento`,
virada).

## Fechar a sessão

Ao encerrar uma sessão numa fatia, para que a próxima — sua, de outra pessoa ou de um agente — retome sem perder o
fio:

1. Acrescente ao Histórico do `status.md` da fatia o que foi feito, o **próximo passo exato** e as decisões desta
   sessão.
2. Marque no `tasks.md` só o que está realmente pronto e verde.
3. **Horas da sessão** (com ELM): "Quanto tempo nesta sessão em `<tarefa>`?" — a tarefa do papel de quem fecha,
   pelo campo ELM do `status.md` → `elm_horas(<id>)` → desconte → `elm_lancar_horas(<id>, <h>)`, com "sim" (lança, não conclui).
   Sem o MCP `elm` → `ELM pendente [<DEV|REV|VER|APR> FT-<nnn> horas]: lançar <h>h (<data>)` no Histórico.
4. **Créditos da sessão** (sempre, com ou sem ELM) — o Kiro grava o consumo de cada turno só na máquina de quem
   conversou (`~/.kiro`), por isso é quem fecha que registra, aqui, e o número chega aos outros pelo commit. O
   Kiro só grava o consumo de um turno quando ele **termina**: leia sempre **na resposta a uma pergunta** — primeiro
   `💳 Registrar os créditos desta sessão? (sim)` (nas entregas das skills de papel, antes do commit:
   `💳 Registrar os créditos e entregar? (sim)`), e só na resposta rode o script; assim o turno do trabalho já
   está gravado. Rode
   o script `scripts/creditos.py` desta skill (fica no power instalado: caminho relativo a esta pasta; busca no
   workspace não o acha): `uv run --no-project python <caminho>/creditos.py --pasta <cada pasta do git worktree
   list> --desde <Data da sua última linha onde vai gravar | início do item>`. Sai uma linha por sessão do Kiro
   com consumo, a mais recente primeiro — é a atual; as outras são sessões que ninguém fechou: mostre-as com o
   título e pergunte quais são deste item (nenhuma é atribuída sem "sim").
   ```
   💳 Créditos — FT-<nnn> · power sdd <metadata.version desta skill>
   Esta sessão: <id> · <x.xx> créditos (até <ate>)
   Sem registro: <id> "<título>" · <x.xx> — é desta fatia? (sim/não)
   Gravar? (sim)
   ```
   Com "sim", uma linha por sessão na seção **Créditos** do `status.md`: `| <ate> | <papel> | <login> | <id> |
   <versão> | <x.xx> |` — Data é o `ate` do script (o `--desde` da próxima vez). Sessão com várias fatias (loop)
   → rateio igual entre elas, Sessão `<id> (rateio 1/<n>)`. Script sem sessão (código 1, outro editor) → pergunte
   o número que o Kiro mostra, Sessão `informado`; nunca estime. Sobra só o turno do próprio registro, pequeno: o
   próximo fechamento do item o pega pelo `--desde`.

   O mesmo vale fora da fatia, mudando só onde a linha vai: atendimento → seção Créditos da ficha `AT-<nnn>`;
   especificação → `status.md` do épico (`sdd-especificar`); gestão (triagem, consolidação, planejamento,
   retrospectiva, horas na `[GB]`) → seção **Créditos de gestão** do `sprint-<nn>.md` aberto, com Atividade no
   lugar de Papel.
5. Mostre o `git status` e proponha o commit do que está pronto (padrão do `sdd.md`); grave só com "ok" e nunca
   faça push.
6. Termine com a frase para retomar numa sessão nova (ex.: "vamos trabalhar na FT-031").
