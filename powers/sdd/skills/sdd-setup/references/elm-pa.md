# ELM — montar o `pa_<nome>.json`, passo a passo

O `pa` decide o que o MCP `elm` grava em cada work item: um valor errado só aparece quando a PA recusa a criação, a
transição ou o lançamento de horas. Por isso aqui **não vale "padrão sem perguntar"**:

- **Só dois lugares de onde vem um valor:** a descoberta (`elm_setup_descobrir`) ou a pessoa. Nunca deduza um nome, um
  `qname`, um time code ou um valor de enumeração; nunca copie de outro projeto nem de um `pa` antigo sem mostrar a
  origem e pedir confirmação daquele valor.
- **Um bloco por mensagem**, na ordem abaixo: mostre as opções que a descoberta trouxe (numeradas), marque a
  recomendada, e espere a escolha. Valor de enumeração só da lista da PA.
- **Formato:** leia [assets/pa.schema.json](../assets/pa.schema.json) antes do bloco 0 e monte o `pa` nele — chaves,
  aninhamento e obrigatórios vêm do schema, não da memória.
- **Cartão de cada bloco** (ícones e peças em [wizard.md](wizard.md)):

  ```
  ### 🧩 ELM · Bloco <n>/10 · <nome do bloco>
  `<●●◉○○○○○○○○>` (11 posições: blocos 0 a 10) <o que este bloco decide, em uma frase>

  | # | Opção | Detalhe | Fonte |
  |---|---|---|---|
  | 1 | <valor> ⭐ (recomendado) | <…> | 🧩 |

  <n> de <n> da descoberta

  > ❓ **<pergunta do bloco>**
  > `<n>` escolhe · `ok` aceita a recomendada · `<n>: <valor>` muda uma linha
  ```

  **Todas** as opções que a descoberta trouxe aparecem na tabela — nunca "os mais prováveis" nem "os relevantes",
  com o resto resumido ou cortado; logo abaixo da tabela, a linha `<n> de <n> da descoberta` (os dois números iguais:
  conte os itens que o MCP devolveu antes de montar a tabela); a recomendada vai primeiro, com ⭐. Lista com mais de 12 opções → tabela em duas colunas
  (`| # | Opção | # | Opção |`). O resultado de um bloco pode abrir a mensagem do bloco seguinte só como a linha
  `✔ Bloco <n> — <valores>`, sem pergunta: dúvida sobre o bloco anterior → fica nele, com a pergunta dele. Resposta que não deixa claro o
  que muda (um "não" no meio de uma linha, "ok" a uma pergunta com duas partes, um formato que não é o do bloco)
  → repita o que entendeu, em tabela, e **pare**: a confirmação é a próxima resposta da pessoa — nunca feche o bloco
  na mesma mensagem em que interpretou; nunca passe ao bloco seguinte com uma pergunta aberta.
- **Nada é gravado** antes da conferência do bloco 10.
- **Modo atualização** (já existe `.kiro/config/sdd/pa_<nome>.json`): mostre o `pa` atual em tabela, bloco a bloco,
  e pergunte só o que muda.

## 0. Credencial e project areas

Não suponha rede: o ELM pode responder sem VPN mesmo quando o GitLab ou o banco não respondem — teste e diga o que
respondeu. `elm_status(projeto=<raiz>)` (sem `pa` ainda, `faltando` vem preenchido — normal): erro `credencial` → peça o `~/.config/mcp-elm/elm.properties` (`server`, `user`,
`password`; você não lê nem grava esse arquivo) e pare. Pergunte um trecho do nome da PA do EWM e se o DOORS Next e o
ETM usam o mesmo nome (ou qual) → `elm_setup_descobrir(ccm, rm?, qm?)`. Mostre as PAs achadas de cada um e confirme
qual é (nenhuma no ETM → sem `qm`: o fluxo não cria caso de teste no ETM, o `CT.csv` fica).

## 1. Time e categoria

Liste os times (`ccm.times`) com as categorias de cada um; recomende o de quem configura. A categoria
(`filedAgainst`) é a do time escolhido.

## 2. Tipos

Confirme o tipo do EWM para `ib` (épico, fatia e atendimento) e `tarefa`, entre os tipos da descoberta, e pergunte
se o projeto registra **defeitos** no EWM: `defeito` é opcional — "não" → o `pa` fica sem ele e os blocos seguintes
não falam de defeito.

| # | Uso no fluxo | Tipo do EWM | Fonte |
|---|---|---|---|
| 1 | `ib` — épico, fatia, atendimento | <Item de Backlog> | 🧩 |
| 2 | `tarefa` — ESP, DEV, REV, VER, APR, ATD, GB | <Tarefa> | 🧩 |
| 3 | `defeito` (opcional) | <Defeito | não usa> | 🧩 |

## 3. Campos de cada tipo

**Um tipo por mensagem** (IB, depois tarefa, depois defeito se houver). Por tipo, **todos** os campos da descoberta
numa tabela `| | # | Campo | Tipo do valor |` com a caixa `[✅]`/`[ ]` (os do fluxo primeiro, já marcados; a
pessoa marca os outros pelo número — `pôr 4,7`), com os que o fluxo usa já marcados: Planejado para, Responsável,
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
campos da chamada. Pergunte, numa tabela com **linhas numeradas** e o valor proposto já preenchido, o valor de cada campo que muda
conforme o item (`<n>: <valor>` muda; `<n>: não usa` tira o prefixo — confirme, porque o fluxo cria esses itens):

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

**Não pergunte**: time code e tipo de trabalho são fixos — grave `"horas": { "time-code": "Horas Diretas",
"work-type": "Tarefa" }` e mostre-os na conferência do bloco 10 como padrão.

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
`por-prefixo`, horas, RM com cada sigla (tipo e pasta), bundle e ETM —, com a origem de cada valor (descoberta, pessoa ou
fixo), e depois o JSON. O JSON mostrado é **o que será gravado, byte a byte**: monte-o no formato do schema
(ids da descoberta inclusos — `ccm.id`, `time.id`, `categoria.id`, `tipos.*.id`, `campos` como `nome → qname`) e
confira contra o [schema](../assets/pa.schema.json) **antes** de mostrar. "ok" → grave `.kiro/config/sdd/pa_<nome>.json` (relativo à raiz, `/`, sem segredos — vai
para o git) e confira com `elm_status(projeto)`: `valido` e `faltando` vazio. A validação pediu mudança → mostre o diff do que
muda e peça "ok" de novo; nunca regrave em silêncio o que a pessoa aprovou.

**Validação** (recomendada; a PA recusa o que o `pa` não cobre): com "sim", `elm_criar_wi` de uma tarefa `[TESTE]
sdd-setup` (pai = um IB que a pessoa indicar), de um IB e de um defeito, `elm_transicao` de cada um até concluir e um
`elm_lancar_horas` na tarefa → cada recusa `precondicao` traz o `campo`: pergunte o valor (bloco 4), ponha-o em
`obrigatorios` e `padroes` e tente de novo. Os itens criados a pessoa cancela na UI; as horas de teste, remova com
`elm_remover_horas`. Outra project area → repita tudo (outro `pa_<nome>.json`) e diga na seção ELM qual é o padrão.
