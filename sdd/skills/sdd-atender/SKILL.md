---
name: sdd-atender
description: "Trilha de atendimento do fluxo sdd — demanda de cliente que não muda o repositório (consulta na base, extração de dados, explicação de regra, conferência de caso): abre o atendimento AT-nnn com entrevista curta e a tarefa [ATD] no EWM na sprint, executa pelo banco (somente leitura) e pelo bundle do ELM, com código só em escopo fechado, guarda extrações fora do git (.kiro/local/atendimentos/), redige a resposta para o \"ok\" da pessoa e conclui lançando as horas na [ATD]; encaminha a saída (defeito → trilha rápida, regra em aberto → entrevista ou PRD, consulta reaproveitável → lição). Use em \"novo atendimento\", \"o cliente pediu\", \"extrai os dados de\", \"consulta na base para o cliente\", \"responde o chamado\", \"conclui o AT-012\", \"atendimentos abertos\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.1.0"
---

# sdd-atender — Atender sem perder o rastro

Atendimento é trabalho real que não vira código: alguém pergunta, o time consulta, responde e segue. Sem trilha,
ele some — não tem tarefa, não consome capacidade e não deixa registro. Aqui cada demanda ganha um número
(`AT-nnn`), uma tarefa `[ATD]` na sprint e um registro versionado **sem dado de cliente**.

Não é atendimento (encaminhe pela `sdd-iniciar`): pedido que muda o comportamento do sistema (fatia, trilha rápida
ou direta) e regra que ninguém decidiu (entrevista ou PRD).

## Arquivos

- `<produto>/atendimentos/README.md` — o próximo número no topo (`Próximo: AT-013`) e a lista dos atendimentos
  (AT · pedido · situação). Número sequencial no projeto, **nunca reaproveitado**.
- `<produto>/atendimentos/AT-<nnn>-<slug>.md` — o registro (formato no fim).
- `.kiro/local/atendimentos/AT-<nnn>/` — extrações, telas e respostas com dado real. Fora do git.
- Linha na seção Atendimento do `sprints/sprint-<nn>.md` aberto (`sdd-planejamento`): consome a reserva.

## 1. Abrir ("novo atendimento: o cliente X pediu …")

1. **Número:** lê o `Próximo` do `README.md` e já o incrementa.
2. **Entrevista curta** — `sdd-entrevistar` modo *atendimento* (uma rodada, com recomendação em cada pergunta):
   o que o cliente precisa receber, origem (chamado, e-mail, DF), prazo, quem responde, critério de pronto.
3. **EWM**, com confirmação — `sdd-elm` modo *atendimento*: tarefa `[ATD] AT-<nnn> <título>`, filha do item
   "Atendimento", `plannedFor` = iteração da sprint aberta (a do `sprint-<nn>.md`; a pessoa pode indicar outra),
   responsável = quem atende, estimativa, estado em andamento.
4. Grava o `AT-<nnn>-<slug>.md`, a linha no `README.md` e a linha no `sprint-<nn>.md`; commit na base (artefato
   de produto). Reserva estourada → avise: o P.O. decide se alguma fatia sai (o atendimento não tira fatia
   sozinho).

## 2. Executar

1. **Fontes, nesta ordem** — subagente `sdd-pesquisador`, se houver: banco pelo MCP de consulta (**somente
   leitura**) e bundle do ELM (`<rm.download.path>` do `sdd.md`). Código só se necessário e em escopo fechado:
   termos ou arquivos indicados e um limite de leitura, para não gastar tokens.
2. **Resultado com dado real** (linhas, telas, planilhas) → `.kiro/local/atendimentos/AT-<nnn>/`. No registro
   ficam só a consulta (SQL), a contagem, o caminho do arquivo e um resumo **sem identificar pessoas**.
3. **Rascunho da resposta** → "ok" da pessoa antes de enviar. Quem envia é a pessoa; o agente não manda e-mail
   nem responde chamado.

## 3. Concluir ("enviei", "conclui o AT-012")

1. Grava no registro a resposta enviada (sem dado de cliente; o texto com dado real fica em `.kiro/local/`).
2. **Horas:** pergunta as horas, descontando o que já foi lançado na `[ATD]` → `sdd-elm` modo *horas* lança e
   conclui a tarefa, com confirmação. Sem MCP ou com falha → `ELM pendente: lançar <h>h em [ATD] AT-<nnn>` no
   registro, e o modo horas lança depois.
3. Atualiza a situação no `README.md` e no `sprint-<nn>.md`; commit na base.
4. **Encaminha a saída:**
   - defeito encontrado → trilha rápida com `origem: AT-<nnn>` (`sdd-iniciar`);
   - regra que ninguém decidiu → `sdd-entrevistar` ou `sdd-prd`;
   - consulta reaproveitável → lição (`sdd-aprender`).

## Registro `AT-<nnn>-<slug>.md`

```markdown
# AT-012 · Extração de contas bloqueadas em setembro

**Origem:** chamado 4521 · **Pedido por:** área de segurança · **Prazo:** 2026-10-16
**Responsável:** joao.lima · **Tarefa ELM:** 669380 · **Situação:** aberto | concluido
**Critério de pronto:** planilha com as contas bloqueadas por tentativas, por dia

## Pedido
<o que o cliente precisa receber, nas palavras dele, sem dado pessoal>

## Consultas
| # | Consulta (SQL) | Resultado |
|---|---|---|
| 1 | `select count(*) from conta where situacao = 'B' and dt_bloqueio between …` | 1.284 contas |

Arquivo: `.kiro/local/atendimentos/AT-012/contas-bloqueadas-2026-09.csv` (fora do git)

## Resposta enviada
<texto, sem dado que identifique pessoas>

## Horas
| Data | Horas |
|---|---|
| 2026-10-14 | 2 |

**ELM:** feito | pendente: <o que falta>
**Saída:** — | FT-040 (defeito) | D-07 em aberto | lição L-015
```

## Regras

- **Dado de cliente nunca vai para o git**: resultado de consulta, extração ou tela com dado real fica em
  `.kiro/local/atendimentos/AT-<nnn>/`. O registro guarda consulta, contagem, caminho e resumo anônimo.
- Banco só em leitura. Pedido que exige escrita na base não é atendimento: vira fatia ou trilha rápida.
- Um `[ATD]` por demanda, sem balde. O que não vira AT fica fora do plano.
- Horas só na conclusão (ou sob pedido, pela `sdd-elm` modo *horas*); nunca no meio do atendimento.
- Toda escrita no EWM e todo envio de resposta pedem confirmação da pessoa.
