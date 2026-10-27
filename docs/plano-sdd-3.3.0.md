# Plano — sprint fiel ao EWM, sprints por iteração pai e Apoio com categorias (sdd 3.3.0 · mcp-elm 3.3.0)

## Contexto

Três problemas do power `sdd` (`powers/sdd`) e do MCP `elm` (`mcps/elm`):

1. **O que nasce fora do sdd não volta para a sprint.** O sdd publica tudo no EWM (`elm-sprint.md` §1–6), mas
   tarefa criada direto no EWM na iteração da sprint não aparece no `sprint-<nn>.md`: fica fora da capacidade, da
   reserva, dos Números e da review. Não é só Apoio: `[DEV]` e `[ESP]` também surgem por fora (ex.: alguém cria
   a tarefa à mão porque a sessão do agente parou por limite de tokens).
2. **Numeração de sprint sequencial e global** (`sprints/sprint-<nn>.md`). O EWM organiza por iteração pai
   (`<release>` → `2026` → Sprint 1..4; `2027` → Sprint 1..5). O repositório deve espelhar:
   `sprints/2026/sprint-01.md`, `sprints/2027/sprint-01.md`.
3. **"Atendimento" é estreito demais.** Vira uma das categorias de **Apoio**, ao lado de Implantação, Banco de
   dados, Infra, Operação e Apoio a outros times, cada uma com seu prefixo de tarefa. Apoio continua **sem mudança
   no repositório** (mudança de código/config segue pela fatia rápida da triagem).

## Discussões e decisões

Registro do que foi discutido no planejamento, para o time saber por que o desenho é este.

| # | Questão | Opções levantadas | Decisão |
|---|---|---|---|
| 1 | Tarefa criada direto no EWM na iteração da sprint: como entra? | vira item de Apoio · só espelho numa seção "Fora do sdd" · perguntar item a item | **inferir e perguntar o que ela é**: tarefa de papel de uma fatia ou épico (`[DEV]`, `[REV]`, `[VER]`, `[APR]`, `[ESP]`) ou uma categoria de Apoio; com o mesmo id do EWM (nunca recria) e, se for o caso, título renomeado ou com o prefixo |
| 2 | Apoio pode mexer no repositório? | não · sim, por categoria (Infra/Implantação com commit) | **não** — mudança de código/config continua sendo fatia rápida pela triagem |
| 3 | Sprints que já existem | move e renumera · move sem renumerar · não migra | **move e renumera** dentro da iteração pai |
| 4 | Nome do guarda-chuva (D1) | Apoio · Sustentação · Operação · Serviços · Suporte (tabela abaixo) | **Apoio** |
| 5 | Ids e prefixos | tudo muda (`AP-nnn`, `[APO]`) · só o nome muda · novo vale, antigo fica | **não existe item nem tarefa "de Apoio"** (`AP-nnn`, `[APO]`): Apoio é só o guarda-chuva das categorias do D2, cada uma com prefixo e série de ids próprios (`[ATD] AT-nnn`, `[IMPL] IM-nnn`…); os `AT-nnn` existentes seguem válidos, sem migração |
| 6 | "Manutenção" como categoria | manter · trocar | **sai**: é vaga e sinônimo de Sustentação |
| 7 | Chamado aberto pelo cliente | categoria pela natureza · Atendimento = chamados · categoria `Chamado` | chamado **é** atendimento — nada muda, a regra de hoje vale |
| 8 | Pai das tarefas de Apoio no EWM | um IB por categoria · o IB de Sustentação | **o IB de Sustentação** é o pai direto; a categoria vive no prefixo e na Classificação da Tarefa |
| 9 | Nome do IB de Sustentação | `[SUS-<ano>] Sustentação` (hoje) · `Sustentação <produto> - <iteração pai>` | **`Sustentação <produto> - <iteração pai>`** (ex.: `Sustentação <produto> - 2026`): acompanha a iteração pai do item 2, não o ano civil |
| 10 | Skill das categorias | uma por categoria · `sdd-apoiar` · `sdd-atender` + genérica | **`sdd-atender` continua** (só Atendimento: é a única com fluxo próprio); as demais, fluxo mínimo. `sdd-apoiar` e `sdd-tarefa` rejeitados |
| 11 | Onde mora o fluxo mínimo | skill nova · `sdd-iniciar` renomeada (`sdd-tarefas`, `sdd-trabalhar`…) · `sdd-iniciar` com o mesmo nome | **dentro da `sdd-iniciar`, sem renomear**: iniciar a tarefa no ELM, registrar o trabalho, lançar horas e concluir |
| 12 | Versão | major (4.0.0) · minor | **3.3.0** para power, skills e MCP (se a 3.3.0 já existir na hora, 3.4.0) |

**D1 — Apoio.** Alternativas avaliadas: Sustentação (já é o IB pai; mistura com fatias sem épico e a `[GB]`),
Operação (estranho para Atendimento), Serviços (ambíguo com o código), Suporte (puxa para atendimento). Apoio casa
com o vocabulário da PA (IB `Categoria = Apoio Técnico`, tarefa `Suporte / Apoio Técnico Especializado`).

**D2 — Categorias aprovadas** (a setup grava todas; o projeto pode acrescentar):

| Categoria | O que cobre | Tarefa | Id | Classificação da Tarefa (PA) |
|---|---|---|---|---|
| Atendimento | chamado ou pedido do cliente: consulta, extração, explicação, conferência | `[ATD]` | `AT-nnn` | Suporte / Apoio Técnico Especializado |
| Implantação | preparar e acompanhar a subida de versão: pacote, janela, roteiro, validação pós-implantação | `[IMPL]` | `IM-nnn` | a confirmar na lista da PA (setup) |
| Banco de dados | script de correção ou carga de dados, conferência de base, apoio ao DBA | `[BD]` | `BD-nnn` | a confirmar |
| Infra | ambiente, acesso, certificado, fila, servidor, pedido a outra equipe | `[INF]` | `IN-nnn` | a confirmar |
| Operação | rotina de produção: reprocessar job, acompanhar execução, incidente sem mudança de código | `[OPE]` | `OP-nnn` | a confirmar |
| Apoio a outros times | ajuda técnica a outra equipe ou outro produto | `[EXT]` | `EX-nnn` | a confirmar |

Regra de escolha na triagem: muda o repositório → fatia rápida (não é Apoio); senão, pela natureza do trabalho.

## 1. Tarefas de fora do sdd entram na sprint (só skills; o MCP já basta)

`elm_listar_wi(iteracao, tipo tarefa)`, `elm_ler_wi(id)` (`ewm.py:323`: devolve `pai`, `estimativa_h`, `campos` —
inclusive a Classificação — e `iteracao`) e `elm_atualizar_wi(ids, titulo, pai)` cobrem tudo. Nenhuma tool nova.

**Novo bloco "Trazer o EWM para a sprint"** em `skills/sdd-planejamento/references/elm-sprint.md` (§9):

1. `elm_listar_wi(iteracao = a da sprint, tipo tarefa, limite alto)`.
2. Conhecidas = ids das colunas "Tarefa ELM" do `sprint-<nn>.md`, a `[GB]` da linha `Sustentação` e a coluna `elm`
   da seção Apoio do `backlog.md`. O resto é **externo**.
3. **Inferir** cada externa (`elm_ler_wi`), nesta ordem de pistas: prefixo já no título; pai no EWM (`[FT-nnn]` →
   tarefa de papel da fatia; `[EP-nn]` → `[ESP]` do épico; Sustentação ou sem pai → Apoio); Classificação da Tarefa
   (Desenvolvimento → `[DEV]`/`[REV]`, Testes → `[VER]`, Análise/Especificação → `[ESP]`, demais → categoria do D2
   pela tabela do `sdd.md`); título e descrição.
4. **Perguntar**, numa tabela, o que a pessoa confirma ou corrige por linha:
   ```
   | # | Tarefa | Título atual | Dono | Estado | É (inferido) | De | Título proposto |
   | 1 | 670210 | ajustar job de carga | joao.lima | Em andamento | [DEV] | FT-034 | [DEV] FT-034 ajustar job de carga |
   | 2 | 670215 | subir versão 1.4 | ana.souza | Novo | [IMPL] | — (IM-004) | [IMPL] IM-004 subir versão 1.4 |
   Título: renomear (padrão do sdd) · só incluir o prefixo · manter. Responda por linha ou "ok".
   ```
   Fatia/épico que a inferência não acha → pergunte; item que não está no `backlog.md` → não entra aqui: indique a
   `sdd-triar` ("importar do EWM").
5. **Gravar** (um "sim" para o lote; nunca recria):
   - **Tarefa de papel** → o id entra na coluna "Tarefa ELM" da linha da fatia/épico no `sprint-<nn>.md` (pode haver
     duas: `DEV 669401 · DEV 670210`), Observação `trazida do EWM`. Fatia em andamento (`status.md` numa branch)
     não mexe no `backlog.md` — a `sdd-consolidar` leva os ids (regra de hoje); o Dev é avisado para registrar no
     `status.md`.
   - **Categoria de Apoio** → próximo id da série dela; linha na seção Apoio do `backlog.md` (`origem: EWM <id>`,
     `elm` = id, `sprint`, `responsavel` = dono, `status` pelo estado), ficha mínima em `<produto>/apoio/<ID>-<slug>.md`
     e linha na seção Apoio do `sprint-<nn>.md` com `trazida do EWM`. Consome a reserva (passou → aviso ao P.O.).
   - **EWM:** `elm_atualizar_wi(id, titulo)` conforme a escolha da linha; sem pai → `pai` = o IB da fatia, o épico
     ou a Sustentação (regra "todo trabalho tem pai"); pai existente não muda.

**Onde roda:** `sdd-planejamento` depois de publicar a sprint e na [pré-condição dos ritos de
fechamento](skills/sdd-planejamento/SKILL.md) (antes da review, retro e virada); `sdd-status` só **conta** e avisa
no painel ("3 tarefas do EWM fora da sprint → sincroniza a sprint"); `sdd-iniciar` em "minha próxima tarefa" oferece
o mesmo para tarefa sem prefixo do sdd (hoje oferece a triagem); sob pedido ("sincroniza a sprint", gatilho novo na
`description` da `sdd-planejamento`). Os Números já pegam essas horas: `elm_horas(iteracao)` lista toda tarefa da
iteração (`ewm.py:662`).

## 2. Sprints por iteração pai

**Chave da sprint:** `<pai>/<nn>` (ex.: `2026/03`), `nn` reinicia em `01` em cada pai. Arquivo
`sprints/<pai>/sprint-<nn>.md`; cabeçalho `# Sprint <pai>/<nn> · …`; `**Iteração no EWM:** <pai>/<nome>`.

**MCP `elm`** — `mcps/elm/mcp_elm/ewm.py`:
- `iteracao_id` e `iteracao()` aceitam caminho `"2026/Sprint 1"`: resolve o pai pelo nome e o filho dentro dele
  (hoje `_por_nome` acusa ambiguidade com dois "Sprint 1"). Nome sem `/` continua como hoje.
- `iteracao()` com caminho cujo pai não existe → cria o pai como irmão do pai da última iteração do cache (mesma
  release), reaproveitando `_criar_iteracao`; a sprint nasce filha dele. Devolve também `pai` (nome).
- Cache do `pa` (`ccm.iteracoes`) com a chave = caminho; `pa.schema.json` só muda a descrição.
- Testes em `mcps/elm/tests/test_ewm.py` com o `elm_fake.py`: dois "Sprint 1" em pais diferentes; pai novo criado.

**Skills** (padrão: trocar `sprint-<nn>.md` por `sprints/<pai>/sprint-<nn>.md` e `sprint <nn+1>` pela chave):
- `sdd-planejamento` passo 5: propõe o pai (o da sprint anterior; se o fim do pai no EWM é antes do início da nova
  → o próximo, ex.: `2027`) e a próxima `nn` dentro dele; virada migra `2026/04 → 2027/01`.
- `arquivos.md` (formato), `sdd-status` (sprint atual = a `aberta` de maior `(pai, nn)`), `backlog.md` (coluna
  `sprint` = chave), `sdd-triar`, `sdd-atender`, `sdd-consolidar`, `sdd-desenvolver`, `sdd-especificar`,
  `sdd-iniciar`, `sdd-revisar`, `sdd-verificar`, `sdd-plano`, `sdd-aprender`, `sdd-prd`, `sdd/SKILL.md`,
  `sdd/references/elm.md`, `README.md`.
- `equipe.schema.json`: `historico[].sprint` aceita a chave `"2026/03"` (inteiro antigo continua válido até a
  migração). Vazão "últimas 3 sprints" segue a ordem do `historico`, cruzando pais.

**Migração (move e renumera)** — oferecida pela `sdd-status` ao achar `sprints/sprint-*.md` na raiz (como já faz com
o `planejamento/` antigo, `sdd-status/SKILL.md:88`) e executada pela `sdd-setup` com "ok":
1. Para cada arquivo, o pai pela `**Iteração no EWM:**` (`elm_iteracao(nome)` → `pai`); sem EWM ou `—` → pergunta o
   pai para o lote.
2. Renumera por pai na ordem atual (`01`, `02`…); prévia `sprint-07 → 2026/sprint-03` e "ok".
3. `git mv`, e reescreve as referências: coluna `sprint` do `backlog.md`, `historico[].sprint`, `→ sprint <nn>` e
   `migrada da sprint <nn>` nos próprios arquivos. Um commit (`sprint: migrar para sprints/<pai>/`).
4. Nomes das iterações no EWM **não** mudam (o cabeçalho guarda o nome real); renomear é roteiro manual opcional.

## 3. Apoio com categorias

**Estrutura:** IB `Sustentação <produto> - <iteração pai>` → tarefas `[ATD] AT-nnn <pedido>`, `[IMPL] IM-nnn
<pedido>`… direto, sem IB por categoria (decisões 8 e 9). O IB `Atendimento` intermediário de hoje deixa de nascer:
os `[ATD]` já criados ficam onde estão (nada se apaga no EWM); os novos nascem filhos da Sustentação.

- **Sustentação por iteração pai** (`elm-sprint.md` §2): nasce com a primeira sprint de um pai novo (não mais "uma vez
  por ano"); `<produto>` = o nome do produto do `sdd.md` (a setup pergunta, se faltar). Idempotência por
  `elm_listar_wi(iteracao = backlog, titulo_prefixo "Sustentação <produto> - <pai>")`. A `[GB]` nasce junto; na
  troca de pai, a `[GB]` antiga conclui com o saldo e a nova nasce sob a Sustentação nova. `pa`: o `por-prefixo`
  `[SUS-` vira `Sustentação ` (mesma Categoria Apoio Técnico). Linha do `backlog.md`:
  `Sustentação 2026: <id> · Backlog [GB] <id>`. A antiga `[SUS-<ano>]` fica como está.
- **Configuração** (`sdd-setup`, `assets/steering/sdd.md` + `references/elm-pa.md`): tabela D2 no `sdd.md`; no
  `pa`, uma linha `por-prefixo` por tarefa (`[IMPL]` → Classificação…) — o MCP já aplica classificação por prefixo,
  sem código novo; sai a linha do "IB de atendimento". Projetos existentes: "atualizar a configuração do sdd"
  acrescenta as categorias; `Atendimento` já está lá.
- **`elm-sprint.md` §6** vira "Apoio": `elm_criar_wi(tipo tarefa, "<prefixo> <ID> <pedido>", pai = Sustentação, …)`.
  `elm.md` (tabela "Tarefas no EWM"): uma linha por categoria, pai = Sustentação.
- **`backlog.md`** (`sdd-fatiar/references/backlog.md`): `## Atendimentos` → `## Apoio`, com a coluna `categoria`;
  "Próximos ids" com uma série por categoria. Backlog antigo → a próxima escrita renomeia a seção e preenche
  `categoria = Atendimento` (regra de migração no formato, como as já existentes).
- **Pasta:** `<produto>/atendimentos/` → `<produto>/apoio/` (fichas `AT-012-…`, `IM-003-…`); local
  `.kiro/local/apoio/<ID>/`. Migração por `git mv` junto com a da seção.
- **`sdd-triar`:** trilha "atendimento" → "apoio"; a categoria é proposta pelo pedido e confirmada na entrevista
  curta. Continua: nada muda no repositório, senão é fatia rápida.
- **`sdd-atender` continua**, só para Atendimento: fluxo atual; ajusta só o caminho da ficha (`apoio/`), a seção
  `## Apoio` e o pai da `[ATD]` (Sustentação).
- **`sdd-iniciar` (mesmo nome) ganha a seção "Tarefas de Apoio sem skill própria"** (`[IMPL]` `[BD]` `[INF]`
  `[OPE]` `[EXT]`), quatro passos, cada escrita com "sim":
  1. **Iniciar:** `elm_transicao(id, "assumir")` (já minha → `ja_estava`; de outra pessoa → `conflito`, pergunta).
  2. **Registrar o trabalho:** na ficha `<produto>/apoio/<ID>-<slug>.md`, o que foi feito fora do repo (passos,
     evidência sem dado de cliente); comentário/anexo na própria tarefa, se a pessoa quiser.
  3. **Lançar horas:** `elm_lancar_horas(id, horas)` a qualquer momento — lançar não conclui.
  4. **Concluir:** saldo de horas, `elm_transicao(id, "concluir")`, `status concluido` + `concluida-em` no
     `backlog.md` e a Situação na seção Apoio da sprint, créditos da sessão na ficha; um commit `<ID> concluir`.
  Sem o MCP `elm` → `ELM pendente [<chave>]` na ficha, como na `sdd-atender`. O encaminhamento das demais tarefas
  não muda; a regra "não mexe no EWM" vale para tudo, menos esta seção. `description` ganha os gatilhos "iniciar a
  [IMPL] 670100", "lançar horas no IM-003", "concluir o IM-003".
- **Planejamento:** "reserva de atendimento e retrabalho" → "reserva de apoio e retrabalho" (`acordos.md`,
  `sdd-planejamento`, `sdd-status`, `sdd-triar`); seção `## Apoio` no `sprint-<nn>.md` com coluna Categoria;
  Números com uma linha por categoria (horas pelo prefixo em `elm_horas`).
- **`equipe.schema.json`:** `horas-lancadas.apoio` (soma das categorias) e `reserva-apoio`; as chaves
  `atendimento`/`reserva-atendimento` continuam aceitas no histórico antigo; `atende` mantém o nome e passa a
  significar "faz apoio".
- **Agentes** (`sdd-setup/assets/agents/papeis.json`, `sdd-produto.md`): textos de "atendimento" → "apoio" onde
  for o guarda-chuva; nomes de skill não mudam.

## Ordem de execução e versões

1. `mcp-elm 3.3.0` — iteração por caminho + testes + `docs/manual-mcp-elm.md` + wheel em `dist/`.
2. `sdd 3.3.0` — itens 3, 2 e 1, nessa ordem (o 1 grava na seção Apoio e na sprint nova); `metadata.version` de
   todas as skills, `plugin.json`, histórico no `README.md`. Se a 3.3.0 já existir na hora, 3.4.0 em tudo.
3. Commits separados por item, no padrão do repo (`sdd 3.3.0: …`, `mcp-elm 3.3.0: …`), sem trailer de coautoria.
4. Exemplos e docs só com nomes genéricos (`<produto>`, `<release>`, `2026`) — nada de projeto ou cliente real.

## Verificação

- `cd mcps/elm && uv run pytest` — verde, com os casos novos de iteração por caminho.
- `grep -rn "sprint-<nn>.md\|## Atendimentos\|atendimentos/\|\[SUS-" powers/sdd` — só nas regras de migração.
- Validar o `equipe.json` de exemplo do `arquivos.md` contra o `equipe.schema.json` novo (com chave `"2026/03"` e
  com inteiro antigo).
- Ensaio num projeto piloto: (a) migração das sprints e da seção de Atendimentos com prévia e um commit; (b) criar
  à mão no EWM, na iteração da sprint, uma `[DEV]` sem prefixo sob o IB de uma fatia e uma tarefa de implantação
  sem pai, rodar "sincroniza a sprint" → a primeira vai para a linha da fatia com o título renomeado, a segunda vira
  `IM-001` filha da Sustentação; as duas aparecem no painel e nos Números; (c) planejar a sprint seguinte com troca
  de pai (`2026/04 → 2027/01`) e conferir a iteração e a `Sustentação <produto> - 2027` criadas no EWM.
