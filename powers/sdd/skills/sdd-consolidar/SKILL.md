---
name: sdd-consolidar
description: "Fecha uma fatia do fluxo sdd depois do merge do PR — processo de produto, do P.O. ou do SM (analista de negócio) no agente sdd-produto, com horas na tarefa [GB] Gerenciamento do backlog: lê o campo Drift de negócio do status.md (marcado pela revisão e pela verificação) e, com drift, leva o PRD ou a ficha a nova versão; manda para o ELM pela sdd-elm, numa confirmação, os requisitos, a regra da ficha as-built, a especificação técnica as-built (gerada aqui, do design.md e do código mergeado), os casos de teste (criados pelo agente no ETM, um por cenário verificado) e a conclusão do item de backlog; leva os ADRs do PR para a pasta de ADRs, corrige o glossário, marca a fatia como concluída no backlog, registra as lições (sdd-aprender) e diz o que vem a seguir no épico. Use em \"PR mergeado\", \"fecha a FT-031\", \"consolidar\", \"concluir a fatia\", \"a fatia foi entregue\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.7.0"
---

# sdd-consolidar — Documentação viva depois do merge

O plano da fatia (`research`, `design`, `tasks`) é andaime: cumpriu o papel quando o código chegou à base. O que
fica valendo é a documentação oficial no ELM — e ela tem de descrever o que **foi** construído. Esta skill fecha a
distância entre os dois.

**Processo de produto:** quem consolida é o **P.O. ou o SM** (analista de negócio), no agente **`sdd-produto`**, e
as horas vão na tarefa **`[GB] Gerenciamento do backlog`** (linha `Sustentação:` do `backlog.md`). A consolidação
não repete a revisão nem a verificação: o drift de negócio já vem marcado por elas no `status.md`; os ADRs já vêm
escritos no PR.

Entrada: fatia em `mergeada` (o Dev responsável mergeou o PR aprovado — Passo 6 da `sdd-implementar`; a fase
está no `status.md` da branch da fatia) — confira que o PR foi mesmo **mergeado** pelo MCP `gitlabpr`
(`gitlab_obter_mr` com o `iid` do link no `status.md`, ou `gitlab_listar_mrs(origem=<branch>, estado=all)`: estado
`merged`); `git branch -r --merged origin/<base>` é só atalho e não enxerga *squash* nem *rebase merge*. Sem PR
(push "não", sem ferramenta, merge local) → pergunte à pessoa se foi mergeado e confira pelo conteúdo: `git diff
<base> <branch> -- <arquivos que a fatia mudou>` vazio (fora a pasta da fatia). Não mergeado → pare. Tudo aqui é
gravado na **base**, pelo bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base) (confirmado o
merge, a troca e o `pull --ff-only` vêm antes de qualquer passo).

## Passo 1 — Drift de negócio

Leia o campo **Drift de negócio** do `status.md` — marcado pela revisão (`sdd-revisar`, rubrica C: achado aceito
ou decisão técnica que muda comportamento visível) e pela verificação (`sdd-verificar`: cenário ajustado). Não
releia o `design.md` nem o `verificacao.md` atrás de drift: isso já foi julgado.

- `sim — <motivo>` → mostre o motivo e leve o PRD a nova versão pela `sdd-prd` (mudança depois de aprovado) — na
  fatia sem épico, a ficha, pela `sdd-triar` — **antes** de publicar (Passo 2).
- `não` → nada no PRD nem na ficha.
- vazio (`—`) → pergunte a quem revisou ou verificou (Histórico) e grave a resposta no campo; não procure você.

## Passo 2 — ELM (com o power `elm`; senão registre pendências)

Pela **`sdd-elm`**, numa confirmação só, nesta ordem (os casos de teste precisam das URLs dos requisitos):
- *requisitos* — publicar/atualizar o que ainda não foi (publicação `no-merge` no `sdd.md`, ou a nova versão do
  Passo 1);
- *regra da ficha* (fatia padrão sem épico com regra nova ou alterada) — gerar o conceito OKF da regra as-built
  em `.kiro/specs/<ft>-<slug>/elm/` (formato do `okf-elm.md` da `sdd-prd`; alteração → a partir do artefato do
  bundle), mostrar e, com o `verified` humano, publicar pelo modo *requisitos*;
- *especificação técnica* — se a linha ET do `sdd.md` diz `as-built no merge`: você gera aqui a ET **as-built** da
  fatia a partir do `design.md` e do **código final já na base** (interfaces, contratos, dados, integrações), com
  o `verified` humano de quem consolida; publicada e ligada ao IB (**implementa**) — modo *especificação técnica*;
- *casos de teste* — um por cenário verificado (`verificacao.md`/`CT.csv`), criados pelo agente no ETM com o link
  **valida** para a história e o **testado por** do IB; ids no `verificacao.md` e no `status.md` — modo *testes*.
  Falha (ex.: HTTP 403, sem permissão de criar no ETM) ou sem o power → `ELM pendente [CT FT-<nnn> criar]` e o
  `CT.csv` como alternativa para importar à mão;
- *tarefas* — a consolidação **não** lança horas nem conclui `[DEV]`, `[REV]`, `[VER]` ou `[APR]`: cada skill de
  papel concluiu a sua (a `[DEV]` no merge, a `[REV]` ao aprovar, a `[VER]` ao aceitar, a `[APR]` na aprovação do
  plano ou do PR; no AFK não há `[REV]` nem `[VER]`). Tarefa da fatia ainda aberta → mostre qual e de quem, e
  registre `ELM pendente [<chave>]: concluir <tarefa> (<login>)`, que a pessoa faz na sessão dela;
- *backlog* — concluir o item de backlog da fatia no EWM (estado de conclusão da PA; e o do épico, na última
  fatia — Passo 4) e comentar no IB o PR, a pasta da fatia e os ids publicados (modo *conclusão*). Tarefa
  concluída sem horas não trava: a virada aponta;
- *horas* — as da consolidação na `[GB] Gerenciamento do backlog` (modo *horas*: lança, não conclui — a `[GB]` é
  contínua). Linha `Sustentação:` sem `[GB]` → como na `sdd-triar` (sugira criá-la ou pergunte a tarefa).

Sem o power `elm` nesta sessão ou com falha → `ELM pendente [<chave>]: <ação>` no Histórico do `status.md`; o
`sdd-status` lista as pendências até alguém fazê-las numa sessão com o power `elm`.

Bundle do ELM no repositório (`rm.download.path`) → sugira rodar a `elm-sync` para trazer o que foi publicado
(é a base de conhecimento que os agentes consultam pelo `okf` na próxima pesquisa; depois dela, `okf_index`
reindexa só o que mudou).

## Passo 3 — Conhecimento que dura

- **ADRs:** o Dev os escreveu no PR (`.kiro/specs/<ft>-<slug>/adr/`, uma por decisão "Vira ADR? sim" do
  `design.md`) e o Dev Sênior os julgou na revisão ou na `[APR]`. Leve cada um para a pasta de ADRs do `sdd.md`
  (próximo número da pasta, `origem FT-<nnn>`), sem reescrever o conteúdo; a cópia da pasta da fatia fica como
  registro do PR. Pasta de ADRs "não há" → ficam só na pasta da fatia.
- **Glossário:** termos que o código novo introduziu ou renomeou — e os `termo pendente` do `decisoes.md` da
  fatia — estão no glossário? Faltando ou divergente → corrija o glossário (com "ok") ou abra a correção do código
  como fatia.

O lint do conhecimento (contradições entre glossário, ADRs, bundle e steering) não é por fatia: é da
retrospectiva do épico ou da sprint (`sdd-aprender`).

## Passo 4 — Fechar

- Na **base** (já nela desde a Entrada; direto ou por PR curto, conforme "Artefatos de produto"
  no `sdd.md` — várias fatias podem ir no mesmo PR de consolidação): `status.md` da fatia com
  `fase: concluida` e data; `backlog.md` com `status: concluida`, `concluida-em` e os ids de tarefa do campo ELM
  do `status.md` que a coluna `elm` ainda não tem; ADRs e glossário do Passo 3.
- Fatia puxada (`Puxada para a sprint <nn>` no Histórico): `sprint` = <nn> na linha do `backlog.md` e uma linha na
  seção Fatias do `sprint-<nn>.md` (revisor e verificador do Histórico, Tarefa ELM com os ids do `status.md`), com
  a Observação `puxada` (e `revisor único`, se o Histórico o tiver) — ela conta na vazão da sprint.
- Todas as fatias do épico concluídas → épico `concluido` (PRD e backlog) e, com ELM, o item do épico no EWM
  concluído (`sdd-elm` modo *conclusão*, na mesma confirmação do Passo 2; sem o power → `ELM pendente
  [EP-<nn> concluir]` no rodapé do PRD); sugira a retrospectiva do épico (`sdd-aprender`), com o lint do
  conhecimento.
- **`sdd-aprender`** modo registrar para cada correção humana da fatia (achados da revisão que chegaram à pessoa,
  verificações rejeitadas, mudanças pedidas no PR).
- Commit (padrão do `sdd.md`, `<id> consolidar`) com `status.md`, `backlog.md` e o que mudou. Branch da fatia: pode
  ser apagada depois do merge (a pasta da fatia já está na base).

## Passo 5 — Próximo

```
✅ FT-<nnn> concluída — <título>
ELM: <publicado (requisitos · ET · CT <ids>) | pendente: …> · Drift de negócio: <não | PRD v1.1 | ficha v2>
Épico EP-<nn>: <c>/<t> fatias · próxima pronta: FT-<…> (<AFK|HITL>, desbloqueada agora)
Lições: <n> registradas
```

## Regras

- Não apague a pasta da fatia: ela é o registro de como a mudança foi feita (o ELM é o registro do que o sistema
  faz).
- Toda escrita no ELM só com confirmação, pela `sdd-elm`.
- Não escreve código: a correção que o glossário ou o drift pedirem no código vira fatia.
