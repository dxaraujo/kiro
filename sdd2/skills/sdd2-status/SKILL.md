---
name: sdd2-status
description: "Painel do fluxo sdd2, somente leitura — onde parei e o que fazer agora: fatias em andamento (nesta branch, nas worktrees e nas branches remotas) com fase, trilha, modo AFK/HITL, progresso do tasks.md, achados abertos e PR; WIP de revisão humana contra o acordo do time; sprint atual e meta; fatias prontas para começar; épicos e PRDs pendentes de aprovação; pendências de ELM; lições propostas; e inconsistências. Também fecha a sessão de trabalho numa fatia (atualiza o status.md, deixa o git pronto para commit e diz como retomar). SEMPRE use esta skill (leia-a antes de responder) em \"onde parei\", \"status\", \"painel\", \"bom dia\", \"o que tem pendente\", \"qual a próxima fatia\", \"como está a sprint\", \"retomar\", \"fechar a sessão\", \"encerrar por hoje\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-status — Onde parei

O painel é somente leitura: não altera arquivo, branch nem ELM. Pedido de **fechar a sessão** → modo da última
seção. Sem `.kiro/steering/sdd2.md` → diga que o fluxo não está configurado e ofereça a `sdd2-setup`.

## Coleta

1. `git fetch --quiet`. Pastas `.kiro/specs/*/status.md` da branch atual, de cada worktree (`git worktree list`)
   e de cada branch remota (`git for-each-ref --format='%(refname:short)' refs/remotes/origin/`, ignorando
   `HEAD`; `git ls-tree -r --name-only <ref> -- .kiro/specs/` e `git show <ref>:<caminho>`). A pasta da fatia
   costuma existir só na branch dela.
2. De cada `status.md`: fatia, título, trilha, modo, fase, responsável, rodadas, achados abertos, PR, ELM,
   Banco, última linha do Histórico (data) e pendências `ELM pendente:` sem `ELM feito:` correspondente.
3. De cada `tasks.md`: `[x]`/total e o primeiro item pendente.
4. `<produto>/backlog.json` (da base): épicos por status, fatias `pronta` sem `status.md` em nenhuma branch,
   sprint atual (`planejamento/sprints/` de maior número não fechada) e a meta. "Em andamento" = fatia com
   `status.md` numa branch e fase diferente de `concluida`; o backlog não guarda isso.
   PRDs (`epicos/*/prd.md`): status e pendências `ELM pendente:` do rodapé.
5. `<produto>/planejamento/acordos.md`: limites de WIP.
6. `<produto>/aprendizado/licoes.md`: lições com situação `proposta`.
7. Lotes autônomos em andamento: `.kiro/local/loop-*.md`.
8. "Minhas" = responsável igual ao login da pessoa: `git config user.name` cruzado com `nome`/`login` do
   `equipe.json`; sem correspondência, pergunte o login uma vez.

## Painel

```
📊 sdd2 — <projeto> · sprint <nn> (<dias> dias restantes) · meta: <…>

🔨 Em andamento
| FT | Título | Fase | Modo | Tarefas | Achados | PR | Parada há | Próximo passo |

👀 Esperando pessoa (WIP de revisão: <n>/<limite> — plano-em-revisao + aceita + pr-aberto)
- FT-031 plano-em-revisao há 1 dia → aprovar o plano (sdd2-plano)
- FT-030 aceita → abrir o PR (sdd2-implementar)
- FT-029 pr-aberto há 2 dias → revisar o PR <link>

✅ Prontas para começar (por prioridade)
| FT | Título | Tam. | Modo | Depende de |

📄 Produto
- EP-04 PRD em-revisao · EP-05 a descobrir

🏛️ ELM pendente: <n> (lista) · 🔁 Lições propostas: <n>
⚠️ Inconsistências: <lista | nenhuma>

👉 Sugestão: <a ação de maior alavanca agora>
```

**Sugestão** — nesta ordem: desbloquear quem espera uma pessoa (plano ou PR parado, WIP de revisão estourado) →
terminar a fatia em andamento → começar a próxima pronta (AFK prontas em quantidade → ofereça o `sdd2-loop`) →
trabalho de produto (PRD/fatiar) para manter o backlog com fatias prontas.

## Inconsistências a apontar

- fase `pr-aberto` sem PR, ou com tarefas pendentes no `tasks.md`;
- fatia `concluida` no `status.md` e não no `backlog.json` (ou o contrário);
- fatia em andamento sem commit há mais de 3 dias úteis;
- `concluida` com Banco = `pendente` ou `aplicada em dev` (implantação bloqueada);
- Histórico fora de ordem cronológica ou fase que não bate com a última linha (conflito mal resolvido);
- conceito de `elm/` com `verified` humano e sem `resource` há mais de 1 dia (projeto que publica na aprovação);
- conceito de `elm/` alterado (`generated.at`) depois do último `verified` e ainda `stable` (falta reaprovar);
- `backlog.json` alterado numa branch de fatia (deve mudar só na base).

## Fechar a sessão

Ao encerrar uma sessão numa fatia, para que a próxima — sua, de outra pessoa ou de um agente — retome sem perder o
fio:

1. Acrescente ao Histórico do `status.md` da fatia o que foi feito, o **próximo passo exato** e as decisões desta
   sessão.
2. Marque no `tasks.md` só o que está realmente pronto e verde.
3. Mostre o `git status` e proponha o commit do que está pronto (padrão do `sdd2.md`); grave só com "ok" e nunca
   faça push.
4. Termine com a frase para retomar numa sessão nova (ex.: "vamos trabalhar na FT-031").
