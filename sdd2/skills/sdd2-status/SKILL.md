---
name: sdd2-status
description: "Painel do fluxo sdd2, somente leitura — onde parei e o que fazer agora: fatias em andamento (nesta branch, nas worktrees e nas branches remotas) com fase, trilha, modo AFK/HITL, progresso do tasks.md, achados abertos e PR; WIP de revisão humana contra o acordo do time; sprint atual e meta; fatias prontas para começar; épicos e PRDs pendentes de aprovação; pendências de ELM; lições propostas; e inconsistências. SEMPRE use esta skill (leia-a antes de responder) em \"onde parei\", \"status\", \"painel\", \"bom dia\", \"o que tem pendente\", \"qual a próxima fatia\", \"como está a sprint\", \"retomar\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-status — Onde parei

Somente leitura: não altera arquivo, branch nem ELM. Sem `.kiro/steering/sdd2-projeto.md` → diga que o fluxo
não está configurado e ofereça a `sdd2-setup`.

## Coleta

1. `git fetch --quiet`. Pastas `.kiro/specs/*/status.md` da branch atual, de cada worktree (`git worktree list`)
   e de cada branch remota (`git for-each-ref --format='%(refname:short)' refs/remotes/origin/`, ignorando
   `HEAD`; `git ls-tree -r --name-only <ref> -- .kiro/specs/` e `git show <ref>:<caminho>`). A pasta da fatia
   costuma existir só na branch dela.
2. De cada `status.md`: fatia, título, trilha, modo, fase, responsável, rodadas, achados abertos, PR, ELM,
   Banco, última linha do Histórico (data) e pendências `ELM pendente:` sem `ELM feito:` correspondente.
3. De cada `tasks.md`: `[x]`/total e o primeiro item pendente.
4. `.kiro/produto/backlog.json`: épicos por status, fatias `pronta` sem pasta, sprint atual
   (`planejamento/sprints/` de maior número não fechada) e a meta.
5. `.kiro/produto/planejamento/acordos.md`: limites de WIP.
6. `.kiro/aprendizado/licoes.md`: lições com situação `proposta`.
7. Lotes autônomos em andamento: `.kiro/local/loop-*.md`.
8. "Minhas" = responsável igual ao login da pessoa (`git config user.email`/`user.name` cruzado com
   `equipe.json`; sem correspondência, pergunte uma vez).

## Painel

```
📊 sdd2 — <projeto> · sprint <nn> (<dias> dias restantes) · meta: <…>

🔨 Em andamento
| FT | Título | Fase | Modo | Tarefas | Achados | PR | Parada há | Próximo passo |

👀 Esperando pessoa (WIP de revisão: <n>/<limite>)
- FT-031 plano-em-revisao há 1 dia → aprovar o plano (sdd2-plano)
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
- `concluida` com Banco diferente de `aplicada em prod` (implantação bloqueada);
- Histórico fora de ordem cronológica ou fase que não bate com a última linha (conflito mal resolvido);
- PRD `aprovado` há mais de 1 dia sem publicação no ELM (projeto que publica na aprovação).
