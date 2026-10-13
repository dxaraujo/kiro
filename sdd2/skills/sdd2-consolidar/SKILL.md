---
name: sdd2-consolidar
description: "Fecha uma fatia do fluxo sdd2 depois do merge do PR — confere que o que foi entregue bate com a documentação oficial (drift entre código, plano e ELM), atualiza o que mudou na documentação (as-built) e manda para o ELM pela sdd2-elm (requisitos, especificação técnica se o projeto usa, casos de teste e links), conclui os itens do EWM, marca a fatia como concluída no backlog, registra as lições (sdd2-aprender) e diz o que vem a seguir no épico. Use em \"PR mergeado\", \"fecha a FT-031\", \"consolidar\", \"concluir a fatia\", \"a fatia foi entregue\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-consolidar — Documentação viva depois do merge

O plano da fatia (`research`, `design`, `tasks`) é andaime: cumpriu o papel quando o código chegou à base. O que
fica valendo é a documentação oficial no ELM — e ela tem de descrever o que **foi** construído. Esta skill fecha a
distância entre os dois.

Entrada: fatia em `pr-aberto` cujo PR foi **mergeado** (confira: `git branch -r --merged origin/<base>` ou a
ferramenta de PR; não mergeado → pare).

## Passo 1 — Drift

Compare o entregue com a documentação:

| Fonte | Pergunta |
|---|---|
| `design.md` → Decisões técnicas, achados aceitos da revisão | alguma decisão mudou comportamento visível? |
| `verificacao.md` | algum cenário foi ajustado durante a verificação? |
| `decisoes.md` (épico e fatia) | decisão nova depois do GATE do PRD? |
| PRD (histórias e regras cobertas) × bundle do ELM | o ELM já reflete o PRD aprovado? (publicação pendente?) |

Drift de **negócio** (regra, cenário, valor) → o PRD precisa de nova versão: mostre a diferença e acione a
`sdd2-prd` (mudança depois de aprovado) antes de publicar. Drift só técnico → nada no PRD.

## Passo 2 — ELM (com o power `elm`; senão registre pendências)

Pela **`sdd2-elm`**, numa confirmação só:
- *requisitos* — publicar/atualizar o que ainda não foi (publicação `no-merge` no `sdd2-projeto.md`, ou drift do
  Passo 1);
- *especificação técnica* — se o projeto publica ET: gerar a ET **as-built** da fatia a partir do `design.md` e do
  código final (interfaces, dados, integrações) e publicar;
- *testes* — `CT.csv` pronto para importar no ETM; após a importação, links "valida" com as histórias;
- *backlog* — concluir as tarefas e o item de backlog da fatia no EWM (estado de conclusão da PA).

Sem o MCP `elm` nesta sessão → `ELM pendente: <ação>` no Histórico do `status.md`; o `sdd2-status` lista as
pendências até alguém fazê-las numa sessão com o power.

Bundle do ELM no repositório (`rm.download.path`) → sugira rodar a `elm-sync` para trazer o que foi publicado
(é a base de conhecimento que os agentes leem na próxima pesquisa).

## Passo 3 — Conhecimento que dura

- **ADRs:** decisões técnicas do `design.md` marcadas "Vira ADR? sim" (ou que mudam como o time vai construir daqui
  para a frente) → um ADR curto na pasta de ADRs do `sdd2-projeto.md` (contexto · decisão · consequências ·
  origem FT-nnn). Mostre e grave com "ok".
- **Glossário:** termos que o código novo introduziu ou renomeou estão no glossário? Divergência → corrija o
  glossário (com "ok") ou abra a correção do código como fatia.
- **Lint do conhecimento** (a cada épico concluído, ou quando a pessoa pedir): procure contradições entre
  glossário, ADRs, bundle do ELM e steering — termo com duas definições, ADR superado sem marcação, regra do ELM
  que o código não segue. Liste como achados; cada um vira correção na fonte ou fatia nova.

## Passo 4 — Fechar

- `status.md`: `fase: concluida`, data; `backlog.json`: `status: concluida`, `concluida-em`.
- Todas as fatias do épico concluídas → épico `concluido` (PRD e backlog).
- **`sdd2-aprender`** modo registrar para cada correção humana da fatia (achados da revisão que chegaram à pessoa,
  verificações rejeitadas, mudanças pedidas no PR) — e modo retrospectiva se a pessoa quiser.
- Commit (padrão do `sdd2-projeto.md`) com `status.md`, `backlog.json`/`backlog.md` e o que mudou.

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
- Toda escrita no ELM só com confirmação, pela `sdd2-elm`.
