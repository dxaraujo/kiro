---
name: sdd-atender
description: "Skill de quem atende no fluxo sdd — executa um atendimento já registrado pela sdd-triar (AT-nnn, tarefa [ATD]): assume a [ATD] no EWM (sdd-elm modo assumir), consulta o banco (somente leitura) e o bundle do ELM, com código só em escopo fechado, guarda extrações fora do git (.kiro/local/atendimentos/), redige a resposta para o \"ok\" da pessoa e finaliza — registra a resposta, lança o saldo de horas, conclui a [ATD] e pergunta os desdobramentos (arquivar · alteração pela sdd-triar · regra pela sdd-entrevistar · lição pela sdd-aprender). Pedido novo não abre aqui: passa pela sdd-triar. Use em \"atender o AT-012\", \"pegar a [ATD] 669380\", \"extrai os dados do AT-012\", \"enviei a resposta\", \"conclui o AT-012\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.7.0"
---

# sdd-atender — Atender sem perder o rastro

Atendimento é trabalho real que não vira código: alguém pergunta, o time consulta, responde e segue. A
**`sdd-triar`** registra a demanda (`AT-nnn`, linha no `backlog.md`, tarefa `[ATD]` na sprint); esta skill é a de
quem **atende**: assume a `[ATD]`, executa e finaliza, deixando um registro versionado **sem dado de cliente**.

Leia antes: `.kiro/steering/sdd.md`. Sem ele → ofereça a **`sdd-setup`** ("configurar o sdd") e pare.

## Arquivos

- `<produto>/atendimentos/AT-<nnn>-<slug>.md` — o registro (formato no fim), criado pela triagem.
- Linha do AT em `## Atendimentos` do `backlog.md` e na seção Atendimento do `sprints/sprint-<nn>.md`.
- `.kiro/local/atendimentos/AT-<nnn>/` — extrações, telas e respostas com dado real. Fora do git.

## Passo 1 — O que chegou

| Entrada | Como ler |
|---|---|
| `AT-nnn` ou `[ATD] AT-nnn` | a linha em `## Atendimentos` do `backlog.md` e o `AT-<nnn>-<slug>.md`, na base (itens 1 e 5 do bloco [Gravar na base](../sdd-fatiar/references/backlog.md#gravar-na-base): o registro é gravado ali durante todo o atendimento) |
| número do EWM de uma `[ATD]` | a linha do `backlog.md` com esse id em `elm` |
| pedido novo ("o cliente pediu …"), ou AT fora do backlog | não está registrado → "use `sdd-triar`" e pare — nunca abra AT aqui |
| AT `concluido` ou `cancelado` | mostre a situação e pare; reabrir é um AT novo pela triagem |

Não é atendimento (pedido que muda o comportamento do sistema, ou regra que ninguém decidiu) → devolva à
`sdd-triar` para refazer a triagem e pare.

## Passo 2 — Assumir a `[ATD]`

**`sdd-elm` modo *assumir*** (com "sim"): responsável = quem está na sessão, estado em andamento da PA (ex.: *Em
Desenvolvimento*); já minha e em andamento → nada a fazer. AT com `elm` `pendente` (registrado sem o power `elm`) → antes,
`sdd-elm` modo *atendimento* (Registrar). Sem o power `elm` → `ELM pendente [<chave>]: assumir [ATD] AT-<nnn>` no registro do AT, e
siga.

## Passo 3 — Executar

1. **Fontes, nesta ordem** — subagente `sdd-pesquisador`, se houver: banco pelo MCP de consulta (**somente
   leitura**) e bundle do ELM pelo MCP `okf` (`okf_search`, `okf_get_document`). Código só se necessário e em escopo fechado:
   termos ou arquivos indicados e um limite de leitura, para não gastar tokens. Se a demanda envolver lógica de
   negócio complexa (regras de cálculo, fluxos condicionais, comportamentos do sistema) — e não for uma extração
   simples de dados — considere acionar o **`sdd-pesquisar`** antes das consultas SQL para entender o contexto
   do código; nesse caso, registre no AT: `"análise baseada em pesquisa de código"`. Sem tempo para pesquisa:
   registre `"resposta baseada apenas no bundle do ELM e no banco"` na seção Consultas do AT.
2. **Resultado com dado real** (linhas, telas, planilhas) → `.kiro/local/atendimentos/AT-<nnn>/`. No registro
   ficam só a consulta (SQL), a contagem, o caminho do arquivo e um resumo **sem identificar pessoas**.
3. **Rascunho da resposta** → "ok" da pessoa antes de enviar. Quem envia é a pessoa; o agente não manda e-mail
   nem responde chamado.
4. **Horas** podem ser lançadas a qualquer momento (`sdd-elm` modo *horas*, com "sim"): lançar não conclui a
   `[ATD]`.

## Passo 4 — Finalizar ("enviei", "conclui o AT-012")

1. Grava no registro a resposta enviada (sem dado de cliente; o texto com dado real fica em `.kiro/local/`).
2. **Saldo de horas:** mostre o que já foi lançado na `[ATD]` (`elm-ccm` › horas lançadas) e pergunte só o que falta →
   `sdd-elm` modo *horas*; depois `sdd-elm` modo *atendimento* (Concluir), com uma confirmação. Cada lançamento
   ganha uma linha na tabela Horas do registro. Sem o power `elm` ou com
   falha → `ELM pendente [<chave>]: lançar <h>h e concluir [ATD] AT-<nnn>` no registro.
3. `**Situação:** concluido` no registro; na linha do AT no `backlog.md`, `status` `concluido` e `concluida-em`;
   a situação no `sprint-<nn>.md`. O commit é **um só**, no fim do Passo 5 (com a Saída), pelos itens 3 e 4 do
   bloco Gravar na base.

## Passo 5 — Desdobramentos

Pergunte o que mais sai do atendimento e registre a resposta em **Saída** no registro:

```
✅ AT-<nnn> concluído. Algum desdobramento?
  1. arquivar — nada mais a fazer
  2. gerar alteração (defeito ou mudança) → use `sdd-triar` com origem AT-<nnn>
  3. regra que ninguém decidiu → use `sdd-entrevistar`
  4. consulta reaproveitável → lição pela `sdd-aprender`
```

Grave a resposta em **Saída** e faça agora o commit único do Passo 4, item 3 (registro, backlog e sprint). Só
instrui e para: **nunca invoque nem simule outra skill**.

## Registro `AT-<nnn>-<slug>.md`

```markdown
# AT-012 · Extração de contas bloqueadas em setembro

**Origem:** chamado 4521 · **Pedido por:** área de segurança · **Prazo:** 2026-10-16
**Responsável:** joao.lima · **Tarefa ELM:** 669380 · **Situação:** aberto | concluido
**Critério de pronto:** planilha com as contas bloqueadas por tentativas, por dia · **Estimativa:** 3 h

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
- Um `[ATD]` por demanda, sem balde. Registrar o AT é da `sdd-triar`; esta skill nunca numera nem abre AT.
- Lançar horas é registro de empenho, a qualquer momento na `[ATD]` iniciada; concluir é o Passo 4, com o saldo.
- Toda escrita no EWM e todo envio de resposta pedem confirmação da pessoa.
