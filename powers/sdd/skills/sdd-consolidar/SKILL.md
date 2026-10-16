---
name: sdd-consolidar
description: "Fecha uma fatia do fluxo sdd depois do merge do PR — confere que o que foi entregue bate com a documentação oficial (drift entre código, plano e ELM), atualiza o que mudou na documentação (as-built) e manda para o ELM pela sdd-elm (requisitos, especificação técnica se o projeto usa, casos de teste e links), conclui os itens do EWM, marca a fatia como concluída no backlog, registra as lições (sdd-aprender) e diz o que vem a seguir no épico. Use em \"PR mergeado\", \"fecha a FT-031\", \"consolidar\", \"concluir a fatia\", \"a fatia foi entregue\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.6.2"
---

# sdd-consolidar — Documentação viva depois do merge

O plano da fatia (`research`, `design`, `tasks`) é andaime: cumpriu o papel quando o código chegou à base. O que
fica valendo é a documentação oficial no ELM — e ela tem de descrever o que **foi** construído. Esta skill fecha a
distância entre os dois.

Entrada: fatia em `pronta-para-merge` — ou `pr-aberto` na trilha direta, que não tem verificação; `aceita` no AFK
sem PR autorizado — cujo PR foi **mergeado**: confira pela ferramenta de PR do `sdd.md` (estado `merged`);
`git branch -r --merged origin/<base>` é só atalho e não enxerga *squash* nem *rebase merge*. Sem PR (push "não",
sem ferramenta, merge local) → pergunte à pessoa se foi mergeado e confira pelo conteúdo: `git diff <base>
<branch> -- <arquivos que a fatia mudou>` vazio (fora a pasta da fatia). Não mergeado → pare. Tudo aqui é gravado na **base**, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base)
(confirmado o merge, a troca e o `pull --ff-only` vêm antes de qualquer passo).

Trilha direta: só o *backlog* do Passo 2 e o Passo 4 — não há plano nem cenário para conferir (a ficha de três
linhas foi julgada na revisão).

## Passo 1 — Drift

Compare o entregue com a documentação:

| Fonte | Pergunta |
|---|---|
| `design.md` → Decisões técnicas, achados aceitos da revisão | alguma decisão mudou comportamento visível? |
| `verificacao.md` | algum cenário foi ajustado durante a verificação? |
| `decisoes.md` (épico e fatia) ou a ficha (fatia sem épico) | decisão nova depois do GATE do PRD ou da aprovação da ficha? |
| conceitos de `elm/` (histórias e regras cobertas) × bundle do ELM | o ELM já reflete o aprovado? (conceito `stable` sem `resource` = publicação pendente; corpo do bundle diferente do conceito publicado = alguém mudou no ELM) |

Drift de **negócio** (regra, cenário, valor) → o PRD precisa de nova versão: mostre a diferença e acione a
`sdd-prd` (mudança depois de aprovado) antes de publicar — na fatia sem épico, a ficha, pela `sdd-triar`. Drift só técnico → nada no PRD.

## Passo 2 — ELM (com o power `elm`; senão registre pendências)

Pela **`sdd-elm`**, numa confirmação só:
- *requisitos* — publicar/atualizar o que ainda não foi (publicação `no-merge` no `sdd.md`, ou drift do
  Passo 1);
- *regra da ficha* (fatia padrão sem épico com regra nova ou alterada) — gerar o conceito OKF da regra as-built
  em `.kiro/specs/<ft>-<slug>/elm/` (formato do `okf-elm.md` da `sdd-prd`; alteração → a partir do artefato do
  bundle), mostrar e, com o `verified` humano, publicar pelo modo *requisitos*;
- *especificação técnica* — se o projeto publica ET: gerar a ET **as-built** da fatia a partir do `design.md` e do
  código final (interfaces, dados, integrações) e publicar;
- *testes* — `CT.csv` pronto para importar no ETM; após a importação, links "valida" com as histórias;
- *tarefas* — o merge **não** lança horas nem conclui `[DEV]`, `[REV]` ou `[VER]`: cada skill de papel concluiu
  a sua (a `[DEV]` no PR, a `[REV]` ao aprovar, a `[VER]` ao aceitar; no AFK só existe a `[DEV]`). Tarefa da fatia
  ainda aberta → mostre qual e de quem, e registre `ELM pendente [<chave>]: concluir <tarefa> (<login>)`, que a pessoa faz
  na sessão dela;
- *backlog* — concluir o item de backlog da fatia no EWM (estado de conclusão da PA). Tarefa concluída sem horas
  não trava: a virada aponta.

Sem o power `elm` nesta sessão ou com falha → `ELM pendente [<chave>]: <ação>` no Histórico do `status.md`; o `sdd-status`
lista as pendências até alguém fazê-las numa sessão com o power `elm`.

Bundle do ELM no repositório (`rm.download.path`) → sugira rodar a `elm-sync` para trazer o que foi publicado
(é a base de conhecimento que os agentes leem na próxima pesquisa).

## Passo 3 — Conhecimento que dura

- **ADRs:** decisões técnicas do `design.md` marcadas "Vira ADR? sim" (ou que mudam como o time vai construir daqui
  para a frente) → um ADR curto na pasta de ADRs do `sdd.md` (contexto · decisão · consequências ·
  origem FT-nnn). Mostre e grave com "ok".
- **Glossário:** termos que o código novo introduziu ou renomeou — e os `termo pendente` do `decisoes.md` da
  fatia — estão no glossário? Faltando ou divergente → corrija o glossário (com "ok") ou abra a correção do código
  como fatia.
- **Lint do conhecimento** (a cada épico concluído, ou quando a pessoa pedir): procure contradições entre
  glossário, ADRs, bundle do ELM e steering — termo com duas definições, ADR superado sem marcação, regra do ELM
  que o código não segue. Liste como achados; cada um vira correção na fonte ou fatia nova.

## Passo 4 — Fechar

- Na **base** (já nela desde a Entrada; direto ou por PR curto, conforme "Artefatos de produto"
  no `sdd.md` — várias fatias podem ir no mesmo PR de consolidação): `status.md` da fatia com
  `fase: concluida` e data; `backlog.md` com `status: concluida`, `concluida-em` e os ids de tarefa do campo ELM
  do `status.md` que a coluna `elm` ainda não tem; ADRs e glossário do Passo 3.
- Fatia puxada (`Puxada para a sprint <nn>` no Histórico): `sprint` = <nn> na linha do `backlog.md` e uma linha na
  seção Fatias do `sprint-<nn>.md` (revisor e verificador do Histórico, Tarefa ELM com os ids do `status.md`), com
  a Observação `puxada` — ela conta na vazão da sprint.
- Todas as fatias do épico concluídas → épico `concluido` (PRD e backlog) e, com ELM, o item do épico no EWM
  concluído (`sdd-elm` modo *conclusão*, na mesma confirmação do Passo 2; sem o power → `ELM pendente
  [EP-<nn> concluir]` no rodapé do PRD).
- Fatia do loop (worktree em `.kiro/local/wt/<ft>`): com "sim", `git worktree remove .kiro/local/wt/<ft>` — **sem
  `--force`**. Falhou por arquivos não rastreados ou alterados → mostre quais (evidência com dado real fica em
  `.kiro/local/verificacao/`, fora da worktree) e deixe a pessoa decidir; nunca force.
- **`sdd-aprender`** modo registrar para cada correção humana da fatia (achados da revisão que chegaram à pessoa,
  verificações rejeitadas, mudanças pedidas no PR) — e modo retrospectiva se a pessoa quiser.
- Commit (padrão do `sdd.md`) com `status.md`, `backlog.md` e o que mudou. Branch da
  fatia: pode ser apagada depois do merge (a pasta da fatia já está na base).

## Passo 5 — Próximo

```
✅ FT-<nnn> concluída — <título>
ELM: <publicado | pendente: …> · Drift: <nenhum | PRD v1.1>
Épico EP-<nn>: <c>/<t> fatias · próxima pronta: FT-<…> (<AFK|HITL>, desbloqueada agora)
Lições: <n> registradas
```

## Regras

- Não apague a pasta da fatia: ela é o registro de como a mudança foi feita (o ELM é o registro do que o sistema
  faz).
- Toda escrita no ELM só com confirmação, pela `sdd-elm`.
