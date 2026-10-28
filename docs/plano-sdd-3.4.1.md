# Plano — a sincronização com o EWM compara o que mudou nas tarefas conhecidas, não só as tarefas por fora (sdd 3.4.1)

## Contexto

Na review e na retrospectiva, os agentes informaram que "não era preciso sincronizar com o EWM". O MCP `elm` está
certo (`elm_listar_wi` filtra pelo "Planejado para" da iteração, `mcps/elm/mcp_elm/ewm.py` `listar_wi`); o problema
é o desenho do §9 do `powers/sdd/skills/sdd-planejamento/references/elm-sprint.md` ("Trazer o EWM para a sprint"):

- O §9 só procura **tarefas externas**: lista a iteração (`tipo tarefa`), tira os ids conhecidos (`sprint-<nn>.md`,
  `backlog.md`, `status.md`) e, sem sobra, responde "sprint e EWM iguais" e para (passo 2).
- A pré-condição dos ritos de fechamento (`sdd-planejamento/SKILL.md`, seção Review) diz "sem tarefa por fora,
  segue calado" — o agente lê como "não precisa sincronizar".
- Nada compara **o que mudou no EWM nas tarefas que os arquivos já conhecem**.

### O que não volta do EWM para os arquivos

1. **Estado** — `[ATD]`/`[IMPL]` concluída direto no EWM segue `aberto`/`em-andamento` na `## Sustentação`
   (reserva consumida errada na retrospectiva); `[ESP]` concluída no EWM segue `iniciada` na Especificação e migra
   na virada à toa; tarefa cancelada/invalidada no EWM segue contando.
2. **Iteração** — tarefa conhecida movida no EWM para outra sprint ou para o backlog continua na sprint pelos
   arquivos; o §9 lista só a iteração da sprint, então nunca vê que ela saiu, e a virada (§5) a move de volta com
   `elm_atualizar_wi`.
3. **Dono e estimativa** — alterados no EWM, o Responsável e as horas previstas do `sprint-<nn>.md` ficam velhos; o
   relatório de horas (§5, `elm_horas(iteracao)`) lê o EWM e não bate com os "Números" do arquivo.
4. **Contradição interna do §9** — o passo 4 manda listar à parte "item que não é tarefa (IB, defeito) planejado na
   iteração", mas o passo 1 só busca `tipo tarefa`: IB ou defeito posto na sprint pelo EWM nunca aparece.

O contador "tarefas por fora" do painel da `sdd-status` (`skills/sdd-status/SKILL.md`, item 6 da Coleta) herda a
mesma limitação.

## Discussões e decisões

| Questão | Opções levantadas | Decisão |
|---|---|---|
| Onde está o defeito | MCP `elm` (filtro da iteração) · desenho do §9 | §9: o MCP está certo |
| Quem prevalece numa divergência | EWM sempre · arquivo sempre · perguntar por linha | **em aberto** — proposta: EWM prevalece em estado, iteração, dono e estimativa, com prévia e um "sim" |
| Fatia pode mudar de situação pela via do EWM | sim · não (só avisa) | **em aberto** — proposta: não; `iniciada`/`pronta`/`concluida` seguem do Dev e da `sdd-consolidar` |
| Versão | 3.4.1 sozinha · junto da próxima rodada | **em aberto** — pela regra da versão única, power + skills sobem juntos |

## Mudanças propostas

### `sdd-planejamento/references/elm-sprint.md` §9

1. **Passo 1** — `elm_listar_wi(iteracao da sprint, limite 200)` sem filtro de tipo; separar tarefas de IB/defeito.
2. **Passo novo (entre 2 e 3): divergências das conhecidas** — para cada id conhecido da sprint:
   - na listagem → comparar estado e dono com o arquivo;
   - fora da listagem → `elm_ler_wi(id)` para ver a iteração (saiu da sprint) ou se sumiu/foi invalidada;
   - tarefas abertas → `elm_ler_wi` para a estimativa, comparada com as horas previstas.
3. **Prévia** — tabela única "arquivo × EWM" com a ação proposta por linha, ao lado da das externas:
   ```
   🔄 <pai>/Sprint <nn> × EWM — <n> divergências
   | # | Tarefa | Item | Campo | Arquivo | EWM | Ação proposta |
   | 1 | 670301 | AT-012 | estado | aberto | Concluído | concluido + concluida-em |
   | 2 | 670188 | EP-04 [ESP] | iteração | 2026/Sprint 03 | Backlog | sai da sprint (Observação) |
   | 3 | 669402 | FT-031 [DEV] | estado | iniciada | Concluído | só aviso — Dev/sdd-consolidar |
   ```
4. **Gravar** com um "sim" para o lote, pelo bloco Gravar na base, no mesmo commit
   `<pai>/Sprint <nn>: sincronizar com o EWM`.

### `sdd-planejamento/SKILL.md`

- Pré-condição dos ritos: "sem tarefa por fora **nem divergência**, segue calado"; o agente nunca declara "não é
  preciso sincronizar" sem ter rodado a comparação.
- "Sincronizar com o EWM" (Durante a sprint): citar as divergências, além das tarefas por fora.

### `sdd-status/SKILL.md`

- Item 6 da Coleta e linha `🔄 EWM` do painel: contar também as divergências (só conta, não grava).

### Demais

- `README.md` do power (nota da versão), `plugin.json`/`metadata.version` das skills alteradas — versão única.
- Conferir `sdd-fatiar/references/backlog.md` (tabela de quem grava `concluido`/`concluida-em`): incluir o §9 de
  divergência como gravador do item de Sustentação concluído no EWM.

## Verificação

- Ler o §9 novo de ponta a ponta com os quatro casos do Contexto e conferir que cada um gera linha na prévia.
- `grep -rn "por fora" powers/sdd` — toda menção cobre também as divergências.
- Testes do power (`test_gerar_agentes.py`, `test_creditos.py`) seguem passando.
