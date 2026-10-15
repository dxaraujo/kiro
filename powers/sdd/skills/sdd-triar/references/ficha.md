# Ficha da fatia sem épico — `<produto>/fatias/FT-<nnn>-<slug>.md`

O que o PRD é para um épico, a ficha é para uma fatia sem épico: o registro do pedido, das decisões e do contrato
de aceite, escrito na triagem (`sdd-triar`) e lido pela pesquisa, pelo plano, pela revisão e pela consolidação.
Artefato de produto: só na branch base. Obrigatória na trilha **padrão**; na **rápida**, só quando a origem não
traz o comportamento esperado escrito (pedido em texto, defeito sem descrição); na **direta**, nunca.

## Formato

```markdown
# FT-040 · Limitar o desconto de pontualidade a 10% da parcela

**Trilha:** padrão · **Origem:** IB 613 · **Pedido por:** área financeira · **Modo:** HITL · **Tamanho:** M
**Situação:** aprovada por ana.souza em 2026-10-15

## Pedido
<o que mudar e por quê, nas palavras de quem pediu>

## Regras
| Regra | Texto | Fonte / decisão | No ELM |
|---|---|---|---|
| R1 · Teto do desconto de pontualidade | O desconto de pontualidade nunca passa de 10% do valor da parcela. | D-01 (ana.souza) | altera 2101 |

## Cenários de aceite
**C1 · Desconto acima do teto é limitado**
Dado uma parcela de R$ 1.000,00 com desconto de pontualidade calculado em R$ 150,00
Quando o pagamento é feito até o vencimento
Então o desconto aplicado é de R$ 100,00

**C2 · Desconto abaixo do teto não muda**
Dado uma parcela de R$ 1.000,00 com desconto de pontualidade calculado em R$ 50,00
Quando o pagamento é feito até o vencimento
Então o desconto aplicado é de R$ 50,00

## Decisões
| D | Pergunta | Decisão | Fonte / quem decidiu | Data | Situação |
|---|---|---|---|---|---|
| D-01 | O teto vale por parcela ou por contrato? | Por parcela | ana.souza (P.O.) | 2026-10-15 | decidida |

## Fora de escopo
- Parcelas já pagas não são recalculadas.
```

## Regras de escrita

- **Situação:** `rascunho` ou `aprovada por <login do P.O.> em <data>`. Regra nova ou alterada só vale aprovada;
  sem isso, a fatia fica `backlog` com `falta: aprovação do P.O.`.
- **Cenários** como na `sdd-prd`: caminho feliz, o que **não** deve ser aceito, repetição, erro em um item — ou por
  que não se aplica; "Então" sempre verificável. Numerados `C1`, `C2`… — são o `cobre` da fatia: o plano, a
  rubrica L e a verificação leem daqui.
- **Regras:** uma por linha, com valores e a fonte (`D-nn` ou id do ELM). Antes de escrever uma regra nova ou
  alterada, a `sdd-elm` modo *similares* (só leitura); "No ELM" = `reusa <id>` · `altera <id>` ·
  `novo (verificado <data>)`. A regra vai para o DOORS Next na consolidação, as-built (`sdd-consolidar`).
- **Rápida:** no lugar de Regras e Cenários, uma seção `## Comportamento` com o atual (e a evidência), o esperado
  (e a fonte) e o que não muda — é o que o `bugfix.md` vai detalhar.
- **Decisões** no formato do `decisoes.md` da `sdd-entrevistar`, aqui dentro (a ficha não tem pasta).
- Termos do glossário em todo o texto; termo novo vai para o glossário (a triagem roda na base).
- Mais de ~3 cenários de comportamentos diferentes, ou mais de uma regra nova independente → não é uma fatia: a
  `sdd-triar` refaz a triagem como épico.
