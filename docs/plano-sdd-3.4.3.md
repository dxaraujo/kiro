# Plano — o item do backlog que ficou sem IB chega ao EWM sem esperar a sprint (sdd 3.4.3)

## Por que

O backlog é vivo: o item nasce na triagem, com ou sem sprint aberta, e precisa estar no EWM desde então, porque é de
lá que a diretoria tira os relatórios (demandas atendidas e pendentes, sprints). A 3.4.2 garante isso só para o item
que a triagem registra na hora. O que já estava no `backlog.md` com `elm` `pendente` não tem por onde chegar ao EWM.

## O que o caso de teste mostra

- Itens triados na **3.4.0** (o IB da fatia sem épico só nascia na sprint), todos com `elm` `pendente`, e o MCP
  `elm` ok. No EWM só existem a Sustentação e a `[GB]`.
- A 3.4.2 só tem três saídas para um item `pendente`, e nenhuma serve aqui:
  - **§0, passo 4 (espelhamento):** o passo 1 termina em "Já há `atual` → mostre e confirme; fim", e a `sdd-setup` só
    roda o §0 quando o `pa` não tem `ccm.backlog`. Num projeto que já tem o backlog configurado, o espelhamento
    nunca roda.
  - **§4:** só cobre o item que entra numa sprint.
  - **§9:** a "publicação pendente" só olha as linhas da sprint. O item do backlog com `pendente` não tem id para
    comparar e não gera linha. Sem sprint, a sincronização nem roda.
  - A `sdd-status` conta esses itens em 🏛️ ELM pendente, mas não diz o que fazer.
- **Risco de duplicar a Sustentação:** o `backlog.md` ainda está no formato anterior à 3.4.0 (`## Apoio`,
  `apoio/…`), e o IB se chama `Sustentação - <produto>`. A idempotência do §2 procura o id na linha da
  `## Sustentação` e, se não acha, aceita só o título exato `Sustentação`. Nenhum dos dois casa, e o §2 criaria uma
  segunda Sustentação. O agente do log percebeu a diferença, mas nenhuma regra manda parar.
- **Está certo como está, sem mudança:** nenhuma tarefa nasce sem sprint; a Sustentação fica com sprint sugerida
  `—` e o aviso; as FT-002 a FT-008 seguem `nova` com a ficha em `rascunho`; os critérios de aceite do IB saem
  incompletos até a ficha ser aprovada; a prévia que o agente montou segue o §0.4, o §3 e o §6.

## Decisões

| # | Questão | Opções | Decisão |
|---|---|---|---|
| 1 | Quem leva o `pendente` do backlog ao EWM | só a setup · a triagem · a sincronização · todas | **proposta:** o procedimento continua um só, o §0 passo 4. Quem o chama: a **triagem** (toda sessão, Passo 1), a **sincronização** (§9) e a **setup** (também com o backlog já configurado). Motivo: o backlog do EWM é a fonte dos relatórios e não pode depender de haver sprint |
| 2 | §0, passo 1 com `atual` | `fim` (3.4.2) · seguir para o passo 4 | **proposta:** com `atual` ou sem ele, segue para o passo 4 quando há linha a espelhar |
| 3 | Triagem com itens `pendente` antigos | ignorar · oferecer no início · oferecer no fim | **proposta:** no Passo 1, logo depois de conferir a base: `<n> itens do backlog sem IB no EWM → criar agora?`, com a prévia do §0.4 e um "sim". Os ids entram no commit único do Passo 3. Com "não", a triagem segue e o painel continua contando |
| 4 | §9 com item do backlog `pendente` | fora da comparação (3.4.2) · linha na tabela | **proposta:** linha `EWM: criar no backlog (§0, passo 4)`, agrupada por item como as outras |
| 5 | Título parecido sem id na linha (`Sustentação - x`, `Manutenção - x`, `<Categoria> - x`) | criar outro · perguntar | **proposta:** mostrar e perguntar se é ele. Com "sim", o id vai para a linha, e renomear o título fica pelas opções do §9 (renomear · manter) |
| 6 | Backlog no formato anterior à 3.4.0 (`## Apoio`) | migração no power · correção única no projeto · detectar e parar | **proposta:** sem migração no power (ele ainda não tem usuários; o projeto do caso é de teste). Faz-se uma correção única no projeto, à mão, antes do espelhamento (aceita) |
| 7 | Versão | — | **3.4.3** para o `plugin.json` e as 22 skills. O `mcp-elm` não muda e segue `≥ 3.4.2` |
| 8 | Migração | — | nenhuma |

## O que muda

- **`elm-sprint.md`:**
  - §0: o passo 1 deixa de terminar em `fim` quando há `atual`. O passo 4 passa a dizer quem o chama (triagem, §9,
    setup), além de "backlog já existente".
  - §2: a idempotência pergunta quando o título casa só pelo prefixo (decisão 5). Vale para a Sustentação, a
    Manutenção e as categorias (§3, §6).
  - §9: no passo 2, o item do backlog com `elm` `pendente` ou id sem link sai de "fora da comparação" e vira a
    linha da decisão 4. Entra também na tabela de Soluções propostas.
- **`sdd-triar`:** no Passo 1, a oferta da decisão 3. No Passo 3, os ids do espelhamento entram no commit único. No
  Passo 4, o resumo da sessão mostra o que foi espelhado.
- **`sdd-setup`** (`SKILL.md` e `references/elm-pa.md`): "atualizar a configuração do sdd" roda o §0 também com o
  `pa` que já tem o `ccm.backlog`; nesse caso, só o passo 4.
- **`sdd-status`:** no painel, o ELM pendente de uma linha do backlog leva a indicação "a triagem ou a
  sincronização cria".
- **`sdd-fatiar/references/backlog.md`:** na tabela de quem escreve a coluna `elm`, o espelhamento passa a ser
  feito pela triagem, pela sincronização e pela setup.
- **Versão:** `README.md`, `plugin.json` e as 22 skills em 3.4.3.

## Verificação

- `pa` com `ccm.backlog` e 3 linhas `pendente` → "atualizar a configuração do sdd" oferece o espelhamento (na 3.4.2
  parava no `fim`).
- Triagem com itens antigos `pendente` → o Passo 1 oferece a criação; com "sim", os IBs nascem no backlog, no estado
  Novo, e os ids vão no commit único.
- Sem sprint aberta → a triagem espelha do mesmo jeito.
- §9 com item do backlog `pendente` → linha `EWM: criar no backlog`.
- IB `Sustentação - x` no backlog do EWM, sem id na linha → a skill pergunta e não cria.
- `grep -rn "Já há \`atual\` → mostre e confirme; fim" powers/sdd` → nada; os testes do power passam.
