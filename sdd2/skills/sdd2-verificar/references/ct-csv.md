# `CT.csv` — casos de teste para importação no ETM

Um caso por cenário **verificado** (aceito com evidência) da fatia. O MCP do power `elm` só lê o ETM: a
importação é pela UI do ETM (Importar → CSV) e o link "valida" com a história é feito depois, pela `sdd2-elm`.

## Arquivo

- `.kiro/specs/<ft>-<slug>/CT.csv` · UTF-8 **com BOM** · quebras de linha **LF** · separador `;`.
- Depois de gravar, garanta LF (`sed -i 's/\r$//' CT.csv`; no macOS `sed -i '' $'s/\r$//' CT.csv`) e o BOM.

## Colunas (nesta ordem)

Valores do ELM vêm do `.kiro/config/power/elm/pa_*.json` (power `elm`) e do `sdd2-projeto.md`; sem ELM, deixe
vazios os que não souber. A ordem e os nomes podem ser trocados na seção **ELM → Testes** do `sdd2-projeto.md`
(o template de importação do ETM do projeto manda).

| # | Coluna | Valor |
|---|---|---|
| 1 | Tipo | tipo de artefato de teste da importação (padrão: Caso de Teste) |
| 2 | Resumo | `<FT-nnn> <título curto> : CT<nn> - <título do cenário>` |
| 3 | Responsável | login do ELM de quem verificou |
| 4 | Status | estado inicial (padrão do projeto) |
| 5 | Categoria | do projeto, se houver |
| 6 | Planejado para | sprint (iteração do EWM), se houver |
| 7 | Descrição | bloco abaixo, entre aspas duplas, com quebras de linha reais |

## Descrição

```
"OBJETIVO:
<o que o caso comprova> (HF-01 · cenário 1.2; REG-01)

PRÉ-CONDIÇÕES:
- <massa: script/fixture e o estado criado>

PASSOS:
1. <executar: requisição, job, tela> com <entradas>
2. <verificar em: consulta, resposta, log, tela>

RESULTADO ESPERADO:
- <o 'Então' do cenário, com valores>

EVIDÊNCIA DA VERIFICAÇÃO (FT-<nnn>, <AAAA-MM-DD>):
- <resumo do obtido>"
```

Aspas duplas dentro do texto são dobradas (`""`), como manda o CSV.
