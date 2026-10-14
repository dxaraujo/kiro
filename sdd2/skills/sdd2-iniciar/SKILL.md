---
name: sdd2-iniciar
description: "Porta de entrada do fluxo sdd2 para qualquer trabalho — recebe uma fatia (FT-031), um item do EWM (IB, defeito, tarefa — com o power elm), um épico ou um pedido em texto; faz a triagem pelo tamanho (trilha direta quando o diff cabe numa frase, rápida para defeito pequeno com bugfix spec, padrão para uma fatia, épico quando precisa de PRD), confere a Definition of Ready, cria a pasta da fatia em .kiro/specs/ e a branch (sugere o nome e aguarda), assume o item no EWM com confirmação e encaminha para a próxima skill. Use em \"vamos trabalhar na FT-031\", \"pegar a task 123\", \"corrigir o defeito 4567\", \"nova demanda\", \"começar\", \"próxima fatia\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-iniciar — Triagem e entrada

Leia antes: `.kiro/steering/sdd2-projeto.md`. Sem ele → ofereça a **`sdd2-setup`** ("configurar o sdd2") e pare.

## Passo 1 — O que chegou

**Ordem de consulta** para qualquer id (`FT-031`, número do EWM, `EP-03`) — vale a primeira fonte que achar, e
nunca se inventa dado de work item: (1) `status.md` nas branches (atual, worktrees, remotas); (2) o
`backlog.json` da base (ids locais e o campo `elm`); (3) o EWM pela skill `elm-ccm`, se a sessão tem o power `elm`;
(4) perguntar à pessoa. A `fase` do `status.md` decide se o papel pode começar.

| Entrada | Como ler |
|---|---|
| `FT-nnn` | `.kiro/produto/backlog.json` (+ PRD do épico) |
| `EP-nn` ou "nova demanda" | é trabalho de produto → **`sdd2-prd`** (ou `sdd2-fatiar`, se o PRD já está aprovado) |
| número do EWM (IB, DF, tarefa) | skill `elm-ccm` do power `elm`; o item pode já estar no `backlog.json` (campo `elm`) — procure primeiro lá |
| texto ("corrigir o cálculo de juros") | a própria descrição; pergunte só o que faltar para a triagem |

Fatia já iniciada (tem pasta em `.kiro/specs/` nesta branch, em worktrees ou em branches remotas —
`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) → leia o `status.md` e **retome** pela fase
(Passo 5). Branch diferente da atual → pergunte se troca (alterações locais não commitadas → avise e pare; nunca
ofereça descartar, `stash` ou `reset`).

## Passo 2 — Triagem

| Trilha | Quando | Caminho |
|---|---|---|
| **épico** | funcionalidade nova ou mudança com várias regras/histórias; mais de ~3 dias de trabalho; decisão de produto em aberto | `sdd2-prd` → `sdd2-fatiar` → cada fatia volta aqui |
| **padrão** | uma fatia do backlog (`FT-nnn`) ou mudança pequena **com** regra de negócio clara | pesquisa → plano → **GATE do plano** → implementação → revisão → verificação → PR |
| **rápida** | defeito ou ajuste ≤ 1 dia **sem** regra de negócio nova (comportamento correto já documentado ou óbvio) | pesquisa curta → `bugfix.md` + `tasks.md` (o teste que reproduz primeiro) → implementação → revisão → verificação → PR |
| **direta** | o diff cabe numa frase (texto, configuração, ajuste trivial), sem regra nova e sem risco de dado | sem pasta de spec: teste que falha (quando houver comportamento) → mudança → backpressure → revisão (`sdd2-revisar`, rubrica C sobre o diff, com o pedido no lugar dos critérios) → PR |

Diga a trilha e o motivo; dúvida entre duas → sim/não pela mais leve.
- **Direta** não cria pasta nem entrada no backlog: o pedido e o id do item (se houver) vão no commit e no PR.
- **Rápida** cria a fatia no `backlog.json` com `origem` (ex.: `"DF 4567"`) e sem épico. Regra de negócio nova
  descoberta nela → vira padrão (e, se mudar documentação, o PRD do épico ou um PRD curto).

## Passo 3 — Definition of Ready (trilha padrão)

- a fatia está `pronta` no `backlog.json` — ou confira agora: cenários de aceite definidos (`cobre` preenchido) e
  PRD `aprovado`/`fatiado`;
- nenhuma decisão bloqueante `em aberto` (`decisoes.md`);
- dependências (`bloqueada-por`) concluídas ou com o que a fatia precisa já na base;
- tamanho ≤ G e modo AFK/HITL declarado.

Falhou um item → diga qual e o caminho (`sdd2-entrevistar`, `sdd2-fatiar` refinamento); não comece.

## Passo 4 — Pasta, branch e item

1. **Branch** — sugira e **aguarde**:
   ```
   Branch sugerida: <prefixo do sdd2-projeto.md><ft>-<slug>   (ex.: feature/ft-031-bloquear-conta)
   Confirma, ou informe outro nome:
   ```
   Confirmado → `git fetch` e `git switch -c <branch> origin/<base>`.
2. **Pasta** `.kiro/specs/<ft>-<slug>/` com `status.md` de [references/status-template.md](references/status-template.md)
   e o `.config.kiro` da spec do Kiro (`specType` `feature` na trilha padrão, `bugfix` na rápida — formato em
   [../sdd2-plano/references/plano-templates.md](../sdd2-plano/references/plano-templates.md)).
3. **Backlog:** não muda aqui (ele só é escrito na base); a fatia em andamento é a que tem `status.md` numa branch.
   Fatia de trilha rápida sem id → crie-a no `backlog.json` **na base** antes de criar a branch.
4. **EWM** (com power `elm`, pergunta única; nunca sem "sim"): assumir a **tarefa** de quem implementa (ex.:
   `[DEV]`; o item de backlog continua do P.O.) com responsável = `whoami`, iniciá-la (ação de
   `ccm_list_workitem_states`), estimativa se faltar. Sem o power: só o `status.md`.
5. Commit pequeno do `status.md` e, com "sim", push da branch — é o sinal para o time de que a fatia começou.

## Passo 5 — Encaminhar

```
🚦 FT-<nnn> — <título>   ·   trilha <…> · modo <AFK|HITL> · fase <…>
Épico: <EP — título | —> · Cobre: <…> · Branch: <…> · Pasta: .kiro/specs/<ft>-<slug>/
Próximo: <skill>
```

| Fase | Próxima skill |
|---|---|
| `pesquisando`, `planejando`, `plano-em-revisao` | `sdd2-plano` (que começa pela `sdd2-pesquisar`) |
| `implementando`, `revisando` | `sdd2-implementar` |
| `verificando` | `sdd2-verificar` |
| `aceita` | `sdd2-implementar` (Passo 5 — abrir o PR) |
| `pr-aberto` | aguardar o merge; mergeado → `sdd2-consolidar` |
| `bloqueada` | mostre o motivo; a pessoa decide |

Trilha direta → `sdd2-implementar` (seção Trilha direta), sem pasta. Modo AFK e várias fatias prontas → ofereça
o **`sdd2-loop`** (o agente leva cada uma até o PR).

## Regras

- O EWM (ou a pessoa) é a fonte dos dados do item; o código, do comportamento atual; o `status.md`, da fase.
- Toda troca/criação de branch e toda alteração no EWM só com "sim".
- Nunca invente dados de work item.
