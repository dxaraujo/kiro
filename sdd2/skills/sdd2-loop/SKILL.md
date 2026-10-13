---
name: sdd2-loop
description: "Execução autônoma (AFK) de várias fatias do fluxo sdd2 — pega a fronteira de fatias AFK prontas e desbloqueadas, cria uma worktree e uma branch por fatia e leva cada uma da pesquisa ao PR pronto, uma fase por sessão de contexto limpo (pesquisador, codificador, revisor, verificador — por subagentes do sdd2-orquestrador ou pelos Kiro Workflows instalados), com backpressure, até 2 rodadas de revisão, parada em bloqueio e limite de WIP pela capacidade de revisão humana. Retomável pelo log em .kiro/local/. Use em \"roda as fatias AFK\", \"modo AFK\", \"leva a FT-031 e a FT-032 até o PR\", \"trabalha sozinho nas prontas da sprint\", \"retoma o loop\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-loop — Fatias AFK até o PR

Quem executa é o agente **`sdd2-orquestrador`** (ou a sessão da pessoa, com os mesmos passos). Ele coordena e
registra; cada fase é feita por um subagente que começa do zero e lê o estado do disco. A pessoa fica **sobre** o
loop, não dentro: aprova o lote no início e lê os PRs no fim.

Leia antes: `.kiro/steering/sdd2-projeto.md` (seção Autonomia, comandos, git) e
`.kiro/produto/planejamento/acordos.md` (WIP).

## Passo 0 — Retomar?

Existe `.kiro/local/loop-*.md` com fatias não finalizadas → mostre o estado (fatia, fase, rodada, último resultado)
e pergunte se retoma. Retomar = continuar cada fatia da fase registrada no `status.md` dela.

## Passo 1 — Fronteira e lote

1. Candidatas: as fatias pedidas, ou as `pronta` + `AFK` da sprint atual, em ordem de prioridade.
2. Fica de fora (diga o motivo): HITL; Definition of Ready não atendida; `bloqueada-por` não concluída e não
   presente antes no lote; já em andamento com outra pessoa.
3. **Limite:** paralelismo do `sdd2-projeto.md` (padrão 1, máximo 3) **e** vagas de WIP de revisão (limite dos
   acordos menos fatias já em `revisando`/`pr-aberto`). PR que ninguém vai revisar hoje não deve ser produzido hoje.
4. Proposta — **uma confirmação para o lote todo**:
   ```
   🤖 Loop AFK — <n> fatias · paralelo <p> · base <branch> · motor <subagentes | Kiro Workflows>
   | FT | Título | Branch | Worktree |
   |---|---|---|---|
   | FT-031 | Bloquear a conta após 3 tentativas | feature/ft-031-bloquear-conta | ../<repo>-wt-ft-031 |
   Plano AFK: <aprovação humana → o loop para no GATE do plano | análise basta → segue até o PR>
   Ao fim de cada fatia aprovada e aceita: push + PR? (sim/não)   — nunca merge
   Confirma?
   ```
5. Log `.kiro/local/loop-<AAAA-MM-DD-HHMM>.md` (formato no fim).

## Passo 2 — Worktree por fatia

```bash
git fetch --quiet
git worktree add ../<repo>-wt-<ft> -b <branch> origin/<base>     # nova
git worktree add ../<repo>-wt-<ft> <branch>                      # já existe
```

Dentro da worktree, faça o que a **`sdd2-iniciar`** faz no Passo 4 (pasta, `status.md` com `Responsável:
agente:sdd2-orquestrador`, `.config.kiro`, backlog `em-andamento`), sem perguntas — o lote já foi confirmado.

## Passo 3 — Fases (por fatia; fatias diferentes em paralelo até o limite)

Cada fase é um subagente novo recebendo **só**: `AUTONOMO=true`, id da fatia, caminho absoluto da worktree e da
pasta da fatia, e a rodada. Nunca o raciocínio de outra fase.

| # | Fase | Subagente | Sai quando |
|---|---|---|---|
| 1 | pesquisa | `sdd2-pesquisador` (`sdd2-pesquisar`) | `research.md` gravado |
| 2 | plano | `sdd2-codificador` (`sdd2-plano`, Passos 2–3) | spec do Kiro gravada · ou `bloqueada` |
| 3 | análise do plano | `sdd2-revisor` (rubrica L) → `sdd2-codificador` corrige | `ANALISE: OK` · 2 rodadas sem OK → `bloqueada` |
| 4 | GATE do plano | — | Plano AFK = aprovação humana → **pare esta fatia** em `plano-em-revisao` e siga com as outras |
| 5 | implementação | `sdd2-codificador` (`sdd2-implementar`, Passos 0–2) | tarefas `[x]` e backpressure verde · ou `bloqueada` |
| 6 | revisão do código | `sdd2-revisor` (rubrica C) → volta à 5 com os achados | `VEREDITO: APROVADO` · 2ª reprovação → `bloqueada` |
| 7 | verificação | `sdd2-verificador` (`sdd2-verificar`) | `ACEITO` · `REJEITADO` → volta à 5 uma vez; de novo → `bloqueada` |
| 8 | entrega | você | commit do que faltar; push + PR se autorizado no lote (texto do Passo 5 da `sdd2-implementar`) |

Com **Kiro Workflows** instalados (`.kiro/workflows/sdd2-planejar-fatia` e `sdd2-entregar-fatia`), as fases 1–3 e
5–7 podem rodar pelas receitas, uma execução por fatia (`fatia` = id). Os resultados ficam em
`.kiro/local/wf/<ft>/` (`plano.json`, `codigo.json`, `aceite.json`); você lê esses arquivos para decidir o
próximo passo.

Depois de cada fase: atualize o log e o Histórico do `status.md`; commits pequenos na worktree.

## Passo 4 — Parada

- **Fatia bloqueada** (lacuna de negócio, divergência com o plano, 2 reprovações, verificação rejeitada duas
  vezes) → registre o motivo e a pergunta exata no `status.md`; siga com as outras.
- **Problema sistêmico** (build quebrado na base, ambiente fora do ar, mesmo erro em duas fatias) → **pare o lote
  inteiro**: o loop não conserta ambiente.
- Ao fim, o resumo:
  ```
  🤖 Loop AFK — resultado
  | FT | Resultado | PR | Rodadas (plano/código/aceite) | Observação |
  Aguardando pessoa: <planos para aprovar · PRs para revisar · bloqueios com pergunta>
  ELM pendente: <ações para a sessão com o power elm>
  Lições para registrar: <correções que o loop precisou — sdd2-aprender>
  ```
- Worktrees ficam até o merge; remova depois (`git worktree remove ../<repo>-wt-<ft>`).

## Log `.kiro/local/loop-<data>.md`

```markdown
# Loop AFK <data> — paralelo <p> · motor <…> · push/PR: <sim|não>
| FT | Worktree | Branch | Fase | Rodada | Último resultado | Atualizado |
|---|---|---|---|---|---|---|
```

## Regras

- Nunca merge, nunca `--force`, nunca push sem a autorização do lote.
- Nunca escreva no ELM: pendências vão para o `status.md` (`ELM pendente: …`).
- Nunca relaxe um gate para o loop andar: bloqueio é informação, não falha.
- Tipo de fatia que bloqueia com frequência → sugira na retrospectiva tratá-lo como HITL.
