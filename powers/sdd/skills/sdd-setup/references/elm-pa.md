# ELM — montar o `pa_<nome>.json`, passo a passo

O `pa` decide o que o MCP `elm` grava em cada work item: um valor errado só aparece quando a PA recusa a criação, a
transição ou o lançamento de horas. Por isso aqui **não vale "padrão sem perguntar"**:

- **Só dois lugares de onde vem um valor:** a descoberta (`elm_setup_descobrir`) ou a pessoa. Nunca deduza um nome, um
  `qname`, um time code ou um valor de enumeração; nunca copie de outro projeto nem de um `pa` antigo sem mostrar a
  origem e pedir confirmação daquele valor.
- **Um bloco por mensagem**, na ordem abaixo: mostre as opções que a descoberta trouxe (numeradas), marque a
  recomendada, e espere a escolha. Valor de enumeração só da lista da PA.
- **Nada é gravado** antes da conferência do bloco 10.
- **Modo atualização** (já existe `.kiro/config/sdd/pa_<nome>.json`): mostre o `pa` atual em tabela, bloco a bloco,
  e pergunte só o que muda.

## 0. Credencial e project areas

`elm_status` (sem `projeto`): erro `credencial` → peça o `~/.config/mcp-elm/elm.properties` (`server`, `user`,
`password`; você não lê nem grava esse arquivo) e pare. Pergunte um trecho do nome da PA do EWM e se o DOORS Next e o
ETM usam o mesmo nome (ou qual) → `elm_setup_descobrir(ccm, rm?, qm?)`. Mostre as PAs achadas de cada um e confirme
qual é (nenhuma no ETM → sem `qm`: o fluxo não cria caso de teste no ETM, o `CT.csv` fica).

## 1. Time e categoria

Liste os times (`ccm.times`) com as categorias de cada um; recomende o de quem configura. A categoria
(`filedAgainst`) é a do time escolhido.

## 2. Tipos

Confirme o tipo do EWM para `ib` (épico, fatia e atendimento), `defeito` e `tarefa`, entre os tipos da descoberta.

## 3. Campos de cada tipo

Por tipo, a lista de campos da descoberta, com os que o fluxo usa já marcados: Planejado para, Responsável,
Estimativa (Tarefa) e, no IB, o de critérios de aceite. Pergunte, por tipo: **"a PA exige mais algum campo para
criar, mudar de estado ou lançar horas?"** — campos de processo não vêm marcados como obrigatórios (ex.: categoria de
integração de horas, OTR, classificação, id do produto). Os que a pessoa indicar entram em `campos` e em
`obrigatorios` do tipo: o MCP os exige já na criação, para nenhuma transição ou lançamento esbarrar neles depois.

## 4. Valores

Chame de novo `elm_setup_descobrir` com `valores_de` = os campos de enumeração escolhidos no bloco 3. Para cada
obrigatório, mostre a lista de valores da PA e pergunte o valor padrão (`padroes`). Campo de texto (ex.: id de
produto) → pergunte o valor. "Planejado para" nunca vai em `padroes`: é sempre a iteração da sprint.

## 5. Valor por item de trabalho

O MCP aplica, na criação: os `padroes` do tipo, depois o `por-prefixo` cujo texto **inicia** o título, depois os
campos da chamada. Pergunte, numa tabela, o valor de cada campo que muda conforme o item (a coluna vazia fica com o
padrão do bloco 4):

| Item | Título começa por | Pergunte |
|---|---|---|
| épico | `[EP-` | categoria do IB |
| fatia | `[FT-` | categoria do IB |
| IB de atendimento | `Atendimento` | categoria do IB |
| épico de Sustentação | `[SUS-` | categoria do IB |
| IB de defeito | — (vai na chamada) | categoria de correção → linha "IB de defeito" do `sdd.md` |
| tarefas | `[ESP]` `[DEV]` `[REV]` `[VER]` `[APR]` `[ATD]` `[GB]` | classificação e o que mais mudar por papel |

O valor mais comum entre os itens vira o padrão do tipo (rede de segurança para título fora dos prefixos); os
diferentes vão em `por-prefixo`.

## 6. Horas

Time code e tipo de trabalho do lançamento **não vêm na descoberta**: pergunte os dois, exatamente como aparecem no
EWM (ex.: o time code das horas do projeto). Nunca use o nome da PA nem um valor de exemplo.

## 7. Links

Não escreva `links`: os padrões do MCP (pai, filhos, implementa, relacionado) são os do EWM. Só `depende`, e só se a
descoberta trouxer um tipo de link de dependência — mostre-o e confirme.

## 8. DOORS Next

Para cada sigla — `HF` (história), `REG` (regra), `GL` (termo de glossário), `ET` (especificação técnica) — pergunte o
tipo de artefato (lista `rm.tipos`) e a pasta (lista `rm.pastas`), com a recomendada pelo nome. Projeto sem uma delas
→ a sigla fica de fora. **Bundle** (`rm.download`): procure no repositório pastas com `index.md` de `okf_version` e
mostre; senão sugira `docs/elm/<nome>` e pergunte.

## 9. ETM

PA do ETM do bloco 0 → `qm` (nome e id). Sem PA → registre "sem casos de teste no ETM".

## 10. Conferência

Mostre o `pa` inteiro numa tabela legível — PA, time e categoria, cada tipo com campos, obrigatórios, padrões e
`por-prefixo`, horas, RM com cada sigla (tipo e pasta), bundle e ETM —, com a origem de cada valor (descoberta ou
pessoa), e depois o JSON. "ok" → grave `.kiro/config/sdd/pa_<nome>.json` (relativo à raiz, `/`, sem segredos — vai
para o git) e confira com `elm_status(projeto)`: `valido` e `faltando` vazio.

**Validação** (recomendada; a PA recusa o que o `pa` não cobre): com "sim", `elm_criar_wi` de uma tarefa `[TESTE]
sdd-setup` (pai = um IB que a pessoa indicar), de um IB e de um defeito, `elm_transicao` de cada um até concluir e um
`elm_lancar_horas` na tarefa → cada recusa `precondicao` traz o `campo`: pergunte o valor (bloco 4), ponha-o em
`obrigatorios` e `padroes` e tente de novo. Os itens criados a pessoa cancela na UI; as horas de teste, remova com
`elm_remover_horas`. Outra project area → repita tudo (outro `pa_<nome>.json`) e diga na seção ELM qual é o padrão.
