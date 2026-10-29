# Plano — a sincronização com o EWM compara o que mudou nas tarefas conhecidas, não só as tarefas por fora (sdd 3.4.1)

## Contexto

Na review e na retrospectiva, os agentes informaram que "não era preciso sincronizar com o EWM". O MCP `elm` está
certo: `elm_listar_wi` filtra pelo "Planejado para" da iteração (`mcps/elm/mcp_elm/ewm.py:354-379`). O problema é o
desenho do §9 do `powers/sdd/skills/sdd-planejamento/references/elm-sprint.md` ("Trazer o EWM para a sprint"):

- O §9 só procura **tarefas externas**: lista a iteração (`tipo tarefa`), tira os ids conhecidos (`sprint-<nn>.md`,
  `backlog.md`, `status.md`) e, sem sobra, responde "sprint e EWM iguais" e para (passo 2, `elm-sprint.md:204-207`).
- Nada compara **o que mudou no EWM nas tarefas que os arquivos já conhecem**.
- O conjunto das conhecidas é largo demais: é todo id do `backlog.md`, inclusive de item fora da sprint. O IB de uma
  fatia `elegivel` posto na iteração pelo EWM conta como conhecido e não aparece em lugar nenhum.
- A pré-condição dos ritos de fechamento (`sdd-planejamento/SKILL.md:223-224`) diz "sem tarefa por fora, segue
  calado": o agente leu como "não precisa sincronizar", e nada mostra que a comparação rodou. A `sdd-aprender` resume
  a mesma pré-condição só pela consolidação (`sdd-aprender/SKILL.md:84-85`).

### O que não volta do EWM para os arquivos

1. **Estado** — `[ATD]`/`[IMPL]` concluída direto no EWM segue `aberto`/`em-andamento` na `## Sustentação`
   (reserva consumida errada na retrospectiva); `[ESP]` concluída no EWM segue `iniciada` na Especificação e migra
   na virada à toa; tarefa cancelada ou invalidada no EWM segue contando. E a virada (§5) não diz por onde julga as
   "não concluídas": se for pelos arquivos, a tarefa já fechada vai para a iteração seguinte e leva as horas junto,
   porque o `elm_horas(iteracao)` soma pela iteração da tarefa, não pela data do lançamento (`ewm.py:674-675`).
2. **Iteração** — tarefa conhecida movida no EWM para outra sprint ou para o backlog continua na sprint pelos
   arquivos; o §9 lista só a iteração da sprint, então nunca vê que ela saiu, e a virada a traz de volta com
   `elm_atualizar_wi`. No sentido contrário, o item do backlog posto na iteração pelo EWM fica invisível (acima).
3. **Dono e estimativa** — alterados no EWM, o Responsável (e o Revisor e o Verificador) e as horas do
   `sprint-<nn>.md` ficam velhos. A sprint só guarda horas na Especificação (Horas previstas) e na Sustentação
   (Horas, e a `**Estimativa:**` da ficha); nas fatias, a estimativa só existe no EWM.
4. **Contradição interna do §9** — o passo 4 manda listar à parte "item que não é tarefa (IB, defeito) planejado na
   iteração" (`elm-sprint.md:227-229`), mas o passo 1 só busca `tipo tarefa`: IB ou defeito posto na sprint pelo EWM
   nunca aparece.

O contador "tarefas por fora" do painel da `sdd-status` (`skills/sdd-status/SKILL.md:46-48` e `:83`) herda a mesma
limitação.

### O que o MCP entrega (conferido no código; nada muda nele — decisão 17)

- `elm_listar_wi` → por item `{id, tipo, titulo, estado, dono}`, mais `truncado` e `total` (`ewm.py:374-379`). A
  consulta para em 1000 itens (`ewm.py:349-351`, `oslc.py:55`): `total` conta até esse teto, e `truncado` só
  compara com o `limite` pedido. Não traz estimativa, pai nem iteração. Tipo que não é do `pa` vem com o id do tipo
  no servidor (`ewm.py:169-174`); o `pa` só tem `ib`, `tarefa` e `defeito` (`sdd-setup/assets/pa.schema.json:31-37`).
- `elm_ler_wi` → `estado`, `dono`, `pai`, `iteracao` (só o nome: `Backlog`, `Sprint 04`) e `estimativa_h`
  (`ewm.py:335-338`); `comentarios: 0` dispensa os comentários. Não traz a data da conclusão.
- O estado vem pelo nome. O MCP classifica pelo nome quando o servidor não informa o grupo (`GRUPOS` e `_DESCARTE`,
  `ewm.py:55-60`); o §9 usa as mesmas palavras.
- `elm_transicao` assume, conclui e **reabre**; cancelar continua manual (`ELM pendente [<id> cancelar]`). Só o dono
  lança horas numa tarefa (`ewm.py:700-704`).
- O agente de produto, onde a sincronização roda, tem tudo isso: `elm-leitura` liberado, `elm-tarefa` e
  `elm_atualizar_wi` com pergunta, e grava `<produto>/**`, fichas de `sustentacao/` inclusive
  (`sdd-setup/assets/agents/papeis.json`). Nenhuma permissão muda.

O plano foi conferido em rodadas: uma revisão adversarial com oito verificações independentes dos achados (11
confirmados) e quatro revisões seguidas por três ângulos — situações e quem grava, mecânica do EWM e completude —,
cada lista conferida por um cético (18, 13, 7 e 8 confirmados, vários repetidos entre os ângulos; a última, só com
fluxo normal e com as falhas que o power admite), mais conferências focadas no último diff. Os furos estão
corrigidos abaixo.

## Discussões e decisões

| # | Questão | Opções levantadas | Decisão |
|---|---|---|---|
| 1 | Onde está o defeito | MCP `elm` (filtro da iteração) · desenho do §9 | §9: o MCP está certo |
| 2 | Quem prevalece numa divergência | EWM sempre · arquivo sempre · por tipo de item · perguntar por linha | **nenhum lado prevalece sozinho** (pedido): uma tabela com todas as divergências, cada uma com a solução proposta; a pessoa aprova o lote ("ok") ou ajusta uma ou mais linhas. A solução proposta segue a seção 2: na Sustentação, o arquivo recebe o EWM; na fatia e no épico, o estado não muda pelo EWM (o EWM é corrigido, ou a linha fica com quem resolve) e o dono segue as regras da equipe (decisão 9); na iteração, vale a situação do item |
| 3 | Fatia e épico mudam de situação pelo estado do EWM | sim · não (só avisa) | **não** (proposta do rascunho, mantida): a situação deles só muda pela skill que a causa (`pronta` exige o Passo 6 da `sdd-desenvolver`: `status.md` na base, créditos, lições). Nas linhas de estado da fatia e do épico, o ajuste é `EWM` ou `manter`, nunca `arquivo`. A sincronização só grava a situação de fatia ou de épico numa decisão de escopo do P.O.: a Volta (decisão 7) e o encaixe (decisões 8 e 8a) |
| 4 | Tarefas por fora e divergências | duas tabelas (rascunho) · uma | **uma tabela** (pedido: "todas as divergências"): a tarefa por fora é a linha de Campo `por fora`, com o tipo inferido e o título proposto na solução |
| 5 | Ajuste por linha | — | `<n>: arquivo` (o arquivo recebe o EWM) · `<n>: EWM` (o EWM recebe o arquivo) · `<n>: manter` (nada é gravado, e a linha volta na próxima sincronização) · na por fora, o tipo e o título, como hoje: `9: [EXT]`, `9: só incluir o prefixo`, `9: manter o título` (traz a tarefa sem renomear; o `manter` sozinho não a traz) |
| 6 | Quem aprova mudança de escopo | quem roda · só o P.O. | sair da sprint e o encaixe pedem o "sim" do **P.O.**, como no Encaixe e no Fechamento sem consolidar; sem ele, a linha fica `manter` nesta rodada |
| 7 | Item que saiu da sprint no EWM | — | a saída vale pelo **item** (o IB ou a origem; na Especificação, a `[ESP]`) e só para o que está **aberto** no EWM: o fechado fica na iteração em que fechou (decisão 16). Não iniciado (fatia ou Especificação `planejada`, Sustentação `aberto`) → sai da sprint pela Volta do `backlog.md`, e o IB e as tarefas abertas vão para o backlog do EWM, na mesma linha (`· EWM: …`): o sdd não tem sprint futura, a próxima nasce no planejamento. Iniciado → volta para a iteração da sprint (de `iniciada` em diante nada volta). Só uma tarefa fora (ou, na Especificação, só o IB do épico), com o item na sprint → ela volta. A linha com a publicação pendente nunca "sai" (decisão 13) |
| 7a | Tarefa que ficou no backlog do EWM quando o item volta a uma sprint | recriar · mover | **mover**, nunca recriar (a regra do topo do `elm-sprint.md`). Cada tarefa move numa chamada própria, com o dono e a estimativa do papel dela no novo planejamento — `elm_atualizar_wi([id], iteracao, dono, estimativa_h)`: a `[DEV]` com o responsável, a `[REV]` com o revisor, a `[VER]` com o verificador —; o IB e o épico movem só com `iteracao`, na chamada única do §3 (o dono do IB segue o P.O.). Só nasce o papel que falta, conferido com `elm_listar_wi(pai = IB)` (não pelo prefixo do título, que a pessoa pode ter mantido); a tarefa descartada e a que tem pendência de cancelamento aberta não contam — o papel nasce de novo, e a velha segue com a pendência, senão o P.O. cancelaria depois a tarefa em uso. A mesma exclusão vale para a Troca AFK → HITL (§7) e para a busca de idempotência do `elm.md` (pai, prefixo do título). O papel que o novo modo não tem (a fatia HITL que volta AFK, pela senioridade do novo responsável) não move: vira `ELM pendente [<tipo> <id> cancelar]` no rodapé da ficha, e a pendência — aberta ou já com `ELM feito` — a tira da comparação e do `a conferir` (decisão 13); a conferência do papel que falta ignora a tarefa descartada. Vale para a publicação (§3–4), o Encaixe, a puxada (`sdd-desenvolver` Passo 4 e `sdd-loop` Passo 1) e a `sdd-especificar`, e cobre também as tarefas que o Encaixe da 3.4.0 já deixa no backlog |
| 8 | Item conhecido que entrou na iteração pelo EWM | — | "entrou" é estar na listagem e ser esperado noutra iteração — a do `**Iteração no EWM:**` da sprint do item, ou o backlog (uma iteração que cobre duas sprints, `sdd-planejamento/SKILL.md:289-291`, não gera linha). **Uma linha por item**, com o IB e as tarefas dele que estão na listagem (citadas, ou por fora com esse pai). **Toda entrada aceita move junto** o IB (ou a origem, ou o IB do épico) e as tarefas do item que ainda estão fora da iteração da sprint, na mesma linha (`· EWM: …`), senão a sincronização seguinte veria o item sair. Pelo tipo: fatia não iniciada → `encaixe` (decisão 8a); a `nova` passa antes pela DoR, como na Previsão (`sdd-planejamento/SKILL.md:99-103`), e não passando volta ao backlog do EWM, com o `falta:`; recusado o encaixe → tudo volta ao backlog. Épico `novo` ou `elegivel` com a `[ESP]` (citada ou por fora) → a linha da Especificação nasce `planejada`, com `encaixe: trazida do EWM`, e o P.O. confirma (a regra de hoje para a `[ESP]` por fora; o `novo` passa antes pela DoR do épico); só o IB, sem a `[ESP]` → volta ao backlog (a especificação entra pelo planejamento, que dá o responsável e as horas). Item de Sustentação `aberto` → entra na sprint, com a situação pelo estado da tarefa (Novo → `aberto`, Em Andamento → `em-andamento`, concluída → `concluido`), como a tarefa de Sustentação por fora de hoje (reserva estourada → o P.O. decide pelo Encaixe se uma fatia sai). Item terminal → volta para a iteração esperada. IB de estrutura (`Sustentação`, `Manutenção`, categoria) → volta ao backlog |
| 8a | Encaixe da fatia trazida do EWM | na linha, na hora (passo 5 de hoje) · pela seção Encaixe | **pela seção Encaixe**: a linha da fatia precisa de responsável, do modo pela senioridade e, no HITL, de revisor e verificador (com a `[REV]` e a `[VER]`), que o passo 5 de hoje não pede. Vale para o IB que entrou e para a tarefa de papel por fora de uma fatia que não está na sprint; a tarefa que já existe vira a do papel inferido, e só o papel que falta nasce (decisão 7a) |
| 9 | Dono | — | Sustentação e `[ESP]` → o arquivo recebe o dono do EWM. `[REV]` → também, se o novo é Dev Sênior ativo e não implementa (ou é o `revisor único`: o implementador é o único Sênior ativo, `sdd-planejamento/SKILL.md:155-157`). `[VER]` → também, se o novo não implementa. `[DEV]` de fatia `planejada` → o arquivo recebe o novo responsável só se ele é Dev ativo, não é o Verificador da linha nem o Revisor (salvo `revisor único`) e o modo não muda pela senioridade dele: Júnior só em fatia HITL; Sênior em fatia AFK, ou HITL com o motivo já na `obs`; Pleno quando os critérios da `sdd-fatiar` dão o modo atual (`sdd-planejamento/SKILL.md:149`), com a confirmação do P.O. na própria linha. Fora disso, o EWM volta (trocar o responsável com troca de modo é do P.O., e o sdd não tem esse fluxo — seção 6). `[DEV]` de fatia `iniciada` em diante → o dono da `[DEV]` é **quem implementa**: só o dono lança horas (`ewm.py:700-704`), e outro Dev pode retomar a fatia — "trocar é do planejamento" (`sdd-desenvolver/SKILL.md:92-93`), e a sincronização é do planejamento. A referência é o Responsável da linha viva da sprint (decisão 23). O arquivo recebe o dono (esse Responsável e o `responsavel` do backlog, que depois de uma puxada podem diferir) se ele é Dev ativo, não é o Verificador nem o Revisor da linha (salvo `revisor único`) e não é Júnior numa fatia AFK (aí é a Troca de modo, com o P.O.); senão, a `[DEV]` volta para o Responsável da linha viva, e o `responsavel` do backlog passa a ser o mesmo. O dono igual ao Responsável da linha viva e diferente do `responsavel` do backlog (a puxada de quem não era o responsável) → `arquivo: responsavel = <dono>`, só no backlog: o valor velho bloquearia a pessoa como verificadora ou revisora (`sdd-verificar/SKILL.md:30-32`, `sdd-revisar/SKILL.md:29-31`). O Responsável do `status.md` não serve de referência: no GATE do plano ele é o aprovador (`sdd-plano/SKILL.md:112-113`, `sdd-revisar/SKILL.md:123-124`), e o `status.md` da branch é do Dev, não da sincronização. Tarefa sem dono no EWM → recebe o do arquivo |
| 10 | Estimativa | comparar todas · só onde o arquivo guarda horas | **só onde o arquivo guarda horas** (Especificação: Horas previstas; Sustentação: Horas e `**Estimativa:**`); o arquivo recebe a do EWM, e só nas tarefas abertas. As fatias não guardam horas: nada a comparar |
| 11 | Título sem o prefixo do sdd | comparar · não | **não compara**: a triagem e o §9 aceitam "manter" o título (`sdd-triar/SKILL.md:161`), e não há como distinguir o título mantido do que perdeu o prefixo |
| 12 | `concluida-em` do item concluído no EWM | data da conclusão · data da sincronização | **a data da sincronização** (o MCP não traz a da conclusão), com a Observação `concluído no EWM`; a pessoa corrige pela linha |
| 13 | Pendência já registrada | divergência · não | **não é divergência**: `ELM pendente [<chave>]` sem `ELM feito` já cobre a diferença (ex.: `[AT-012 cancelar]`), coletada em todos os lugares da `sdd-status` (Coleta, itens 2 e 4 — o rodapé do `prd.md` ou do `rascunho.md` inclusive, com o `[EP-<nn> concluir]`) e também no Histórico do `status.md` da base das fatias `concluida` da sprint, onde a `sdd-consolidar` e o Passo 6 da `sdd-desenvolver` as deixam (a coleta da `sdd-status` pula essas fatias). Uma falha numa escrita cuja chave já está aberta não grava pendência repetida (uma por chave, `elm.md`). O id com pendência de **cancelamento** (`[<tipo> <id> cancelar]` ou a do item) sai da comparação de vez, aberta ou já com `ELM feito`: cancelar foi decisão registrada, e o cancelado no EWM não é divergência. A publicação pendente da linha — Tarefa ELM `pendente` (ou sem id nenhum, numa linha não iniciada: a sessão parou entre gravar o arquivo e publicar), ou o item com `elm` `pendente` ou id sem link (planejamento sem o MCP ou com falha, `sdd-planejamento/SKILL.md:136-137`), **e** os ids que também faltam no `status.md` da fatia `iniciada` ou `pronta` — cobre a linha inteira: o item e as tarefas ficam fora da comparação de estado e de iteração, e a solução é `EWM: publicar (§1–4)`, nunca "sai da sprint"; a sprint inteira sem iteração no EWM começa pelo §1 (§1 do plano, passo 1). Com os ids no `status.md` (a fatia já começou e publicou), a linha é comparada por eles, e a `sdd-consolidar` os leva aos arquivos, como hoje |
| 14 | Resultado sem divergência | calado (hoje) · sempre uma linha | **sempre uma linha** (pedido): `🔄 <chave> × EWM: iguais — <n> itens conferidos`. O agente nunca diz que "não é preciso sincronizar" sem ter rodado a comparação |
| 15 | Painel da `sdd-status` | sincronização inteira · só a listagem | **só a listagem** (uma chamada, somente leitura). Por fora, estado, dono e entrada contam como divergências. O id da sprint ausente da listagem conta à parte, como `a conferir`, quando a linha dele não tem `migrada de`; o de linha migrada fica só para a sincronização (em geral é tarefa que fechou numa sprint anterior e ficou lá — decisão 16). Pendência registrada não conta (decisão 13), inclusive a do Histórico das fatias `concluida`, que a coleta da `sdd-status` hoje pula — e que passa a entrar também na lista 🏛️ do painel, de toda fatia `concluida` com pendência aberta. Nada → `🔄 EWM: sem diferença na listagem (<n> itens)`: o painel não diz "iguais", que é da sincronização. Sprint com `**Publicação no EWM:** pendente`, ou listagem com `nao_encontrado`/`entrada` → `🔄 EWM: sprint não publicada → sincroniza a sprint`, sem listar nem rodar o §1 (o painel é somente leitura; decisão 24). A estimativa fica para a sincronização |
| 16 | Virada (§5) | mover pelos arquivos (hoje) · cruzar com o EWM | **cruzar**: move, entre os abertos na listagem da iteração que fecha, os ids do conjunto "da sprint" (§1, passo 2) que seguem no fluxo — as tarefas e o item das linhas que migram (inclusive os ids que só estão no `status.md`), o IB de todo épico `planejado` ou `iniciado` (mesmo com a linha da Especificação `concluida`, que não migra) e a `[GB]`, se o pai não muda. O que está fechado fica na iteração em que fechou: o que move é o conjunto "da sprint" da próxima, menos o que fechou. **Ordem**, em toda virada: o §9 da sprint que fecha é o da pré-condição (antes da migração; o §5 não roda outro); depois a migração nos arquivos (passo 3), o replanejamento da próxima (passo 4), o §1 da próxima — a iteração e o plano precisam existir antes do movimento, também com o mesmo pai (com pai novo, o §2 antes, como hoje) —, o movimento do §5, o §3–4 e o §6 das linhas novas e só então o §9 da próxima. Antes do movimento, os itens migrados ainda estão na iteração que fecha e apareceriam como saídos. **Virada pela metade** (sem o MCP, falha no movimento ou sessão parada depois do passo 4): os arquivos seguem, a skill diz que o movimento fica para a sincronização da próxima, e o §9 da próxima reconhece o caso — o marcador `**Publicação no EWM:** pendente` (decisão 24) vira a linha `EWM: criar a iteração e o plano` (§1 passo 1), antes de qualquer listagem; a linha com `migrada de <chave>` cujo id aberto está na iteração de uma sprint da cadeia `migrada de` → `EWM: mover para esta sprint` (só os abertos), nunca "saiu"; e a linha nova ainda sem ids → `EWM: publicar`. O movimento do §5 também leva esses ids da cadeia (não todo id aberto fora da listagem, que desfaria uma saída que espera o P.O.) |
| 17 | MCP `elm` | sem mudança · `elm_listar_wi` com o grupo do estado e a estimativa (mcp-elm 3.4.1) | **sem mudança** (pedido): segue o `mcp-elm ≥ 3.3.5`; a melhoria fica registrada na seção 6 |
| 18 | Versão | 3.4.1 sozinha · junto da próxima rodada | **3.4.1 sozinha** (pedido): o `plugin.json` e as **22** skills. A versão é única, como nas tags `sdd-3.3.1` e `sdd-3.4.0` (o rascunho dizia "skills alteradas"); o `**Power sdd:**` e os créditos gravam o `metadata.version` de quem escreve, e versões misturadas confundiriam essa conta |
| 19 | Migração | — | nenhuma (o power ainda não tem usuários, como na 3.4.0) |
| 20 | Listagem no teto do MCP | confiar no `truncado` · conferir o `total` | **`total` = 1000 → avise e pare** (o `truncado` nunca acusa com `limite 1000`): sem a listagem inteira faltariam por fora e entradas, e a linha "iguais" mentiria. Vale também para o painel e para a virada |
| 21 | Tipo que não é do `pa` (impedimento, retrospectiva…) | linha por fora · fora da comparação | **fora**, quando nenhum arquivo cita o id: conta nos conferidos, sem linha — senão o `manter` o traria de volta em toda rodada e a linha "iguais" nunca sairia. Id citado é comparado qualquer que seja o tipo (a origem de um épico pode ser de outro tipo, `elm-sprint.md:113-114`) |
| 22 | Linha de Sustentação com `saiu da sprint` na reserva | conta · não conta | **não conta** no usado da reserva — na triagem (a soma das estimativas das `### <Categoria>`, `sdd-triar/SKILL.md:146-150`), no painel e no Encaixe: o item saiu da sprint e não a consome. O item que só tem essa linha na sprint é item fora dela para as barreiras da `sdd-atender` e da `sdd-executar` |
| 23 | Item que volta à sprint de onde saiu | reaproveitar a linha · linha nova | **linha nova**, como a puxada já faz (`sdd-desenvolver/SKILL.md:134-136`), em todo caminho de volta (puxada, Encaixe, §9, e a `sdd-especificar`, em que "a linha nasce agora"). A linha com `saiu da sprint` fica como histórico: **nunca é editada e não migra** na virada (senão a próxima sprint teria o item duas vezes). Com duas linhas do mesmo id na sprint aberta, **a viva** — a que se lê e se escreve (Status ou Situação, Tarefa ELM, Responsável, Créditos) — é a sem `saiu da sprint`. A regra fica uma vez no bloco Gravar na base do `backlog.md`, que todo gravador cita, e nas Situações ao vivo do `arquivos.md`; barreiras, reserva, painel e inconsistências da `sdd-status` a seguem |
| 24 | Como saber que a sprint não foi publicada | o `nao_encontrado` da listagem · marcador no cabeçalho | **marcador**: o planejamento e a virada gravam `**Publicação no EWM:** pendente` no cabeçalho do `sprint-<nn>.md` enquanto o §1 não rodou (na virada, o arquivo da próxima nasce no passo 4, antes do §1 — decisão 16), e a publicação o tira no commit dela. A listagem não serve de prova: sem o §1, o MCP procura o caminho pelo nome na PA inteira (`ewm.py:203-212`) e pode achar a sprint homônima de outro produto (cada produto tem a sua linha de base, `elm-sprint.md:50-55`) ou dar `entrada` ("ambígua"); o §1 resolve dentro da linha de base (`ewm.py:916-921`) e guarda o id no `pa`. O painel, com o marcador, não lista: mostra "sprint não publicada". **Nenhuma skill passa a iteração dessa sprint ao MCP** enquanto o marcador está lá (Encaixe, triagem com sprint aberta, `sdd-especificar`, `sdd-atender`, `sdd-executar`, `sdd-desenvolver`, `sdd-loop`): no agente de produto, ela roda o §1 antes, com o mesmo "sim", e tira o marcador no commit dela; nos agentes sem o `elm_iteracao` (codificador, orquestrador), registra o lado do EWM como `ELM pendente [<chave>]` e indica "sincroniza a sprint". A regra fica uma vez no `elm.md`, que toda skill segue — a exposição já existia na 3.4.0 (a primeira sprint de um pai que outro produto da PA já tem) |
| 25 | Falha numa escrita da sincronização no EWM | sempre pendência (`elm.md`) · nunca · pela redetecção | **pela redetecção**: sem pendência quando a próxima sincronização vê a mesma diferença de novo — estado, dono, estimativa ou iteração de item **não terminal** da sprint, que fica nela ou migra —, porque a pendência a esconderia (decisão 13); com `ELM pendente [<chave>]` no lugar do artefato quando não veria: a conclusão do IB ou da tarefa de item terminal (Sustentação no `**ELM:**` da ficha, épico no rodapé do PRD, fatia `concluida` no Histórico do `status.md` da base) e qualquer falha na pré-condição da virada em item que não migra. **Linha que muda o escopo** (entrou — decisão 8 — ou saiu — decisão 7) cujo movimento no EWM falhou: o lado do arquivo **não** é gravado, e a linha volta como estava na próxima (senão a seguinte veria o item sair, ou entrar, ao contrário); só os ids que a linha já criou são gravados de volta (`elm.md`, Regras de toda escrita, item 3). **A por fora** cujo título ou pai falhou: se a linha já criou ids (o IB `[XX-nnn]` do item novo, o IB da categoria), o item entra nos arquivos com eles e a falha vira `ELM pendente` no `**ELM:**` da ficha (título e pai não são comparados de novo); se não criou nada, fica fora dos arquivos e volta como por fora. É a exceção ao "com falha, registre" do `elm.md`, anotada nele |

## 1. O §9 novo — "Sincronizar a sprint com o EWM"

O título muda; nenhum link aponta para a âncora (as skills citam "§9"). Roda depois de publicar a sprint (§4; na
virada, a da próxima só depois do movimento do §5 — decisão 16), na pré-condição dos ritos de fechamento e sob
pedido ("sincroniza a sprint", "sincronizar com o EWM"). Sem o MCP `elm` → "sincronização com o EWM não feita" (sob
pedido, pare).

1. **Listar** — `elm_listar_wi(iteracao = "<pai>/<nome>" da sprint, limite 200)`, **sem `tipo`** (tarefas, IBs,
   defeitos e épicos). `truncado` → repita com `limite 1000`. `total` = 1000 → avise e pare (decisão 20).
   **Sprint não publicada** (decisão 24): com `**Publicação no EWM:** pendente` no cabeçalho do `sprint-<nn>.md` —
   planejamento ou virada sem o MCP, ou sessão parada antes do §1 —, **não liste ainda**: a tabela abre com a linha
   `EWM: criar a iteração e o plano (§1; com pai novo, também o §2 — a [GB] nova nasce, e a antiga conclui e sai da
   linha)`, e a listagem vem depois do "ok". Sem o marcador, a listagem que volta `nao_encontrado` ou `entrada`
   ("ambígua") na iteração da sprint é tratada do mesmo jeito.
2. **Onde cada id deveria estar**, pelos arquivos. Cada item entra com **todos** os ids dele: o IB ou a origem e as
   tarefas (a coluna `elm` do `backlog.md`, a "Tarefa ELM" da linha e, na fatia `iniciada` ou `pronta`, o campo ELM do
   `status.md`).
   - **da sprint** (esperado na iteração da sprint): os itens das linhas do `sprint-<nn>.md` aberto, menos as que têm
     `saiu da sprint`, com os ids dos `status.md` das fatias da sprint `iniciada` e `pronta`, lidos pela regra A base
     prevalece (o de `origin/<base>` quando existe, senão o da branch, `git show origin/<branch>:…` — como a
     `sdd-status`, Coleta, item 1: depois de um merge pela UI do GitLab a branch some); a `[GB]` do pai; e o IB de
     cada épico `planejado` ou `iniciado` (ele acompanha as sprints até concluir, §3 e §5);
   - **do backlog** (esperado no backlog do EWM): os IBs `Sustentação`, `Manutenção` e de categoria e os itens não
     terminais fora da sprint (`sprint` `—`), inclusive os que saíram dela, com as tarefas que ficaram no backlog
     (decisão 7a);
   - **terminal de fora**: o item terminal cuja `sprint`, no `backlog.md`, não é esta — esperado na iteração do
     `**Iteração no EWM:**` daquela sprint (`—`: o backlog). O IB do épico terminal fica fora da conferência de
     iteração (ele acompanha as sprints até concluir, e o `backlog.md` não diz em qual concluiu), mas o estado dele é
     comparado quando está na listagem;
   - **por fora**: o id da listagem que nenhum arquivo cita, com `tipo` do `pa` (decisão 21).

   **Publicação pendente** (decisão 13): a linha com Tarefa ELM `pendente` — ou sem id nenhum, numa linha não
   iniciada (a sessão parou entre gravar o arquivo e publicar) —, ou cujo item tem `elm` `pendente` ou id sem link,
   e sem os ids no `status.md` da fatia, fica fora das comparações abaixo; ela vira a linha `EWM: publicar (§1–4)`. A
   puxada `iniciada` tem Tarefa ELM `—` de propósito: os ids dela estão no `status.md`.
3. **Comparar** — "entrou" e "saiu" só quando a iteração real não é a esperada:
   - da sprint, presente na listagem → estado e dono (seção 2);
   - da sprint, ausente da listagem → `elm_ler_wi(id, comentarios 0)`: aberto noutra iteração → saiu — salvo na linha
     com `migrada de <chave>` cujo id aberto está na iteração de uma sprint da cadeia (`<chave>`, a de onde ela
     migrou antes, e assim por diante, pelos `migrada de` dos arquivos fechados): o movimento da virada não rodou, e a
     linha é `EWM: mover para esta sprint` (decisão 16); fechado → fica onde fechou (não é divergência de iteração,
     mas o estado é comparado); `nao_encontrado` → sumiu;
   - tarefa aberta da Especificação e da Sustentação → `elm_ler_wi(id, comentarios 0)`, para a estimativa (a tarefa
     que já foi lida porque saiu não é lida de novo);
   - IB de épico citado no `backlog.md` e presente na listagem → o estado, qualquer que seja a situação do épico;
   - do backlog ou terminal de fora, presente na listagem e esperado noutra iteração → entrou: **uma linha por
     item**, com o IB e as tarefas dele que estão na listagem — as citadas e as por fora cujo pai é esse item;
   - por fora → a inferência de hoje (o passo 3 atual: `elm_ler_wi` para o pai, os campos e a descrição; prefixo,
     pai, Classificação, título e descrição). A tarefa cujo pai é um item que entrou vai na linha dele; o IB ou
     defeito fora do `backlog.md` vira linha `triar`, o que resolve a contradição do passo 4.

   O que já é pendência — `ELM pendente [<chave>]` sem `ELM feito`, coletadas como na `sdd-status` (Coleta, itens 2
   e 4) e no Histórico do `status.md` da base das fatias `concluida` da sprint — não é divergência; o id com
   pendência de cancelamento sai da comparação de vez (decisão 13).
4. **Prévia** — uma tabela só, com a solução proposta em cada linha (seção 3).
5. **Gravar** com o "ok", ou depois dos ajustes:
   - **EWM** primeiro, com o mesmo "ok" (é a prévia de `elm.md`, Regras de toda escrita): `elm_atualizar_wi` para
     iteração (o item que entra ou sai leva o IB e as tarefas abertas junto — decisões 7 e 8), dono, estimativa e, na
     por fora, título e pai; `elm_transicao` pelo que a linha diz — concluir (o IB da fatia, do épico ou do item de
     Sustentação; a tarefa reaberta, no "concluir de novo", com as horas já lançadas, como a `sdd-fatiar` conclui as
     da fatia cancelada) ou reabrir (tarefa, IB, `[ESP]`, `[GB]`); a publicação pendente pelo §3–4. A tarefa só nasce
     para o papel que o item não tem, e a que já existe move com o dono e a estimativa do papel dela (decisão 7a).
     Uma falha no EWM segue a decisão 25: sem pendência quando a próxima sincronização vê a mesma diferença de novo;
     com `ELM pendente [<chave>]` no lugar do artefato
     ([Pendências](../powers/sdd/skills/sdd/references/elm.md#pendências)) quando não veria; a linha que muda o
     escopo e falhou no movimento não grava o lado do arquivo; e a por fora cujo título ou pai falhou entra só se já
     criou ids (com a pendência na ficha) — senão volta como por fora. Fora esses casos, o lado do arquivo segue;
   - **arquivos** (`backlog.md`, `sprint-<nn>.md` e as fichas de `sustentacao/**`; para a pendência da decisão 25,
     também o rodapé do `prd.md` e o `status.md` da base da fatia `concluida`) pelo bloco
     [Gravar na base](../powers/sdd/skills/sdd-fatiar/references/backlog.md#gravar-na-base), num commit
     `<pai>/Sprint <nn>: sincronizar com o EWM` (já está no `sdd.md`), com as horas na `[GB]`;
   - as linhas `encaixe` seguem depois, uma a uma, para a seção Encaixe da `sdd-planejamento` (decisão 8a).
   As regras de hoje para gravar a por fora (passo 5 atual: Tarefa ELM da linha, `trazida do EWM`, o épico que entra
   pela `[ESP]`, a tarefa de Sustentação que vira item, IB `[XX-nnn]`, reserva estourada → Encaixe) continuam; muda
   só a fatia que ainda não está na sprint, que vai para o Encaixe, e o IB do item que entra, que move junto.
6. **Nada diverge** → a linha `🔄 <chave> × EWM: iguais — <n> itens conferidos` (os da listagem mais os da sprint
   que não estão nela).

**Estados do EWM**, pelo nome e com as palavras do MCP:

| Grupo | Nomes |
|---|---|
| nova | o estado inicial da PA (Novo…) |
| em andamento | andamento, progresso, desenvolvimento, execução, implementação, trabalho, teste, revisão, verificação |
| concluída | concluído, resolvido, fechado, finalizado, pronto, done, completo |
| descartada | cancelado, inválido ou invalidado, rejeitado, duplicado, descartado |

Nome fora da tabela → `?` na linha, e a pessoa diz o grupo.

## 2. Divergências e solução proposta

A solução proposta vem primeiro; "outras" são os ajustes que a linha aceita, além de `manter`.

**Sustentação sem mudança no repositório** (a tarefa `[ATD]`, `[IMPL]`… e o IB do item): o ciclo dele vive no EWM.

| Arquivo | EWM | Solução proposta | Outras |
|---|---|---|---|
| `aberto` | tarefa em andamento | arquivo: `em-andamento` (backlog, sprint e `**Situação:**` da ficha) | — |
| `aberto` · `em-andamento` | tarefa concluída | arquivo: `concluido`, `concluida-em` = a data da sincronização, Observação `concluído no EWM`, `**Situação:** concluido` na ficha (Créditos `—`: ninguém fechou a sessão, e a virada aponta) · EWM: concluir o IB do item, se aberto | EWM: reabrir a tarefa |
| não terminal | tarefa descartada | arquivo: `cancelado`, Observação `cancelado no EWM`, ficha · IB aberto → `ELM pendente [<ID> cancelar]` no `**ELM:**` da ficha | EWM: reabrir a tarefa |
| `em-andamento` | tarefa nova | manter: quem faz assume na próxima sessão (`sdd-atender`, `sdd-executar`) | — |
| `concluido` · `cancelado` | tarefa aberta (reaberta) | manter: situação terminal não volta, e trabalho novo é item novo (`sdd-triar`) | EWM: concluir de novo, com as horas já lançadas |
| `concluido` | IB do item aberto | EWM: concluir o IB | — |
| — | tarefa com outro dono | arquivo: `responsavel` (backlog), Responsável (sprint) e `**Responsável:**` (ficha) | EWM: o dono volta |
| — | tarefa sem dono | EWM: dono = o responsável do arquivo | — |
| tarefa aberta | outra estimativa | arquivo: Horas (sprint) e `**Estimativa:**` (ficha) | EWM: a estimativa volta |

**Fatia** (tarefas de papel e o IB ou a origem): a situação não muda pelo estado do EWM (decisão 3).

| Arquivo | EWM | Solução proposta | Outras |
|---|---|---|---|
| `planejada` · `iniciada` | `[DEV]` concluída | manter: o Dev confere — PR mergeado → `sdd-desenvolver` Passo 6; senão, reabrir | EWM: reabrir a `[DEV]` |
| `planejada`, sem `status.md` em branch | `[DEV]` em andamento | manter: a fatia começa pela `sdd-desenvolver` (com `status.md` numa branch, quem corrige é a rede de proteção da pré-condição) | — |
| não terminal | tarefa ou IB descartado | manter: dividir ou cancelar é da `sdd-fatiar` (P.O.) | EWM: reabrir |
| antes de `concluida` | IB concluído | EWM: reabrir o IB (ele fecha na `sdd-consolidar`) | — |
| `concluida` | IB aberto | EWM: concluir o IB | — |
| `pronta` · `concluida` | tarefa aberta | manter: a tarefa é de `<dono>`, que a conclui na sessão dele | — |
| `planejada` | `[DEV]` com outro dono | arquivo: responsável = o novo, quando a decisão 9 deixa; senão, EWM: o dono volta | EWM: o dono volta |
| `iniciada` em diante | `[DEV]` com outro dono | arquivo: `responsavel` e Responsável = o dono, quando a decisão 9 deixa (quem retomou a fatia); senão, EWM: a `[DEV]` volta para o Responsável da linha viva (e o backlog acompanha) | EWM: a `[DEV]` volta para o Responsável da linha viva |
| `iniciada` em diante | dono da `[DEV]` = Responsável da linha viva ≠ `responsavel` do backlog | arquivo: `responsavel` = o dono, só no backlog (decisão 9) | — |
| HITL | `[REV]` com outro dono | arquivo: Revisor = o novo, se é Dev Sênior ativo e não implementa (ou é o `revisor único`); senão, EWM: o dono volta | EWM: o dono volta |
| HITL | `[VER]` com outro dono | arquivo: Verificador = o novo, se não implementa; senão, EWM: o dono volta | EWM: o dono volta |

**Especificação** (a `[ESP]` e o IB do épico):

| Arquivo | EWM | Solução proposta | Outras |
|---|---|---|---|
| `planejada` · `iniciada` | `[ESP]` concluída | EWM: reabrir a `[ESP]` (ela fecha no GATE do backlog, `sdd-especificar` Passo 6) | — |
| `planejada` | `[ESP]` em andamento | manter: a especificação começa pela `sdd-especificar` (o Passo 2 grava `iniciada`) | — |
| não terminal | `[ESP]` descartada | manter: cancelar o épico é da `sdd-fatiar` | EWM: reabrir |
| épico `planejado` · `iniciado` | IB do épico concluído | EWM: reabrir o IB | — |
| épico `concluido` | IB do épico aberto | EWM: concluir o IB | — |
| — | `[ESP]` com outro dono | arquivo: Responsável (sprint) | EWM: o dono volta |
| `[ESP]` aberta | outra estimativa | arquivo: Horas previstas | EWM: a estimativa volta |

**`[GB]`:** concluída fora da troca de pai → EWM: reabrir.

**Iteração** (qualquer item, decisões 7, 7a, 8 e 13):

| Caso | Solução proposta | Outras |
|---|---|---|
| sprint não publicada (`**Publicação no EWM:** pendente`, ou a listagem com `nao_encontrado`/`entrada`) | EWM: criar a iteração e o plano (§1; com pai novo, também o §2), e só então listar | — |
| publicação pendente | EWM: publicar a linha (§1–4) | — |
| migrada (`migrada de <chave>`), aberta ainda na iteração de uma sprint da cadeia | EWM: mover para esta sprint (a virada não moveu — decisão 16) | — |
| saiu (aberto), item não iniciado | arquivo: sai da sprint (P.O.) — fatia `elegivel` (ou `nova`, pela DoR), épico `elegivel`, Sustentação `aberto`, com `sprint` `—`; a linha da sprint fica com a mesma situação e `saiu da sprint: movida no EWM para <iteração> (<P.O.>, <data>)` · EWM: o IB e as tarefas abertas que não estão no backlog (onde estiverem, outra sprint inclusive) → backlog | EWM: o que saiu volta para a sprint |
| saiu (aberto), item iniciado | EWM: volta para a iteração da sprint | — |
| só uma tarefa aberta saiu (ou só o IB do épico), com o item na sprint | EWM: volta | — |
| fechado e fora da listagem | não é divergência: fica onde fechou | — |
| sumiu (`nao_encontrado`) | manter: confira na UI do EWM | — |
| entrou: fatia `elegivel` fora da sprint (o IB, tarefas dela, ou os dois) | encaixe (P.O., seção Encaixe; a tarefa que já existe é a do papel, e o IB e as tarefas que faltam vêm para a sprint) — recusado, EWM: tudo volta ao backlog | EWM: volta ao backlog |
| entrou: fatia `nova` | a DoR primeiro: passa → `elegivel` e encaixe, como acima; não passa → EWM: volta ao backlog, com o `falta:` na `obs` | — |
| entrou: épico `novo` ou `elegivel`, com a `[ESP]` | arquivo: Especificação `planejada` e épico `planejado`, com `encaixe: trazida do EWM (<P.O.>, <data>)`; Responsável e Horas previstas pelo dono e pela estimativa da `[ESP]` · EWM: o IB do épico → sprint (o `novo` passa antes pela DoR do épico) | EWM: volta ao backlog |
| entrou: épico `novo` ou `elegivel`, só o IB | EWM: volta ao backlog (a especificação entra pelo planejamento) | — |
| entrou: item de Sustentação `aberto` (o IB, a tarefa, ou os dois) | arquivo: entra na sprint, com a situação pelo estado da tarefa e `trazida do EWM`; a tarefa que já existe é a dele, e só sem ela a tarefa nasce (§6), com o `responsavel` e a `**Estimativa:**` da ficha, ou os que a pessoa der na linha · EWM: o IB e a tarefa → sprint, e, com a tarefa concluída, concluir o IB (como na linha "tarefa concluída") | EWM: volta ao backlog |
| entrou: item terminal | EWM: volta para a iteração esperada | — |
| entrou: IB de estrutura | EWM: volta ao backlog | — |

**Por fora:** a tarefa segue a inferência e as soluções de hoje (a da fatia fora da sprint, pelo Encaixe — decisão
8a; a de um item de Sustentação fora da sprint, com o IB dele movido junto — decisão 8; a tarefa concluída que vira
item `concluido` deixa o IB `[XX-nnn]` concluído na mesma linha); o IB ou defeito fora do `backlog.md` → triar
(`sdd-triar`, "importar do EWM"), com a outra solução "EWM: volta ao backlog".

## 3. A tabela

```
🔄 2026/Sprint 03 × EWM — 9 divergências · 41 itens conferidos
| # | Item | No EWM | Campo | Arquivo | EWM | Solução proposta |
|---|---|---|---|---|---|---|
| 1 | AT-012 | ATD 670301 | estado | em-andamento | Concluído | arquivo: concluido, concluida-em 2026-10-28 (concluído no EWM) · EWM: concluir o IB 669379 |
| 2 | IM-003 | IMPL 670215 | dono | ana.souza | rita.melo | arquivo: responsável rita.melo |
| 3 | IM-003 | IMPL 670215 | estimativa | 4 h | 6 h | arquivo: Horas 6 |
| 4 | FT-036 | IB 670188 | iteração | 2026/Sprint 03 | Backlog | arquivo: sai da sprint — elegivel, sprint — (P.O.) · EWM: DEV, REV e VER de FT-036 → backlog |
| 5 | FT-031 | DEV 669401 | iteração | 2026/Sprint 03 | Sprint 04 | EWM: volta para 2026/Sprint 03 (fatia iniciada) |
| 6 | FT-033 | DEV 669410 | estado | iniciada | Concluído | manter: o Dev confere — PR mergeado → sdd-desenvolver Passo 6; senão, reabrir |
| 7 | EP-05 | ESP 669377 | estado | iniciada | Concluído | EWM: reabrir a [ESP] (fecha no GATE do backlog) |
| 8 | FT-040 | IB 670400 · DEV 670401 | iteração | backlog (elegivel) | 2026/Sprint 03 | encaixe (P.O.; a DEV 670401 é a da fatia) — recusado: volta ao backlog |
| 9 | — | 670210 | por fora | — | "ajustar job de carga" · joao.lima · Em Andamento | [DEV] de FT-034 → Tarefa ELM dela · título "[DEV] FT-034 ajustar job de carga" |
"ok" aplica tudo como proposto · ou ajuste uma ou mais linhas: "4: EWM", "6: EWM", "2: manter", "9: só incluir o prefixo"
```

- **No EWM** é o tipo e o id (o item que entrou leva os ids dele na mesma linha, 8); **Campo**: `estado` · `dono` ·
  `estimativa` · `iteração` · `sumiu` · `por fora` · `publicação` (a linha que cria a iteração da sprint não
  publicada, quando houver, vem primeiro).
- A solução diz onde grava: `arquivo:` (o arquivo recebe o EWM), `EWM:` (o EWM recebe o arquivo), `manter:` (nada é
  gravado; diz quem resolve), `encaixe` ou `triar` (encaminha). Linha com as duas partes (1, 4) grava as duas; toda
  escrita no EWM aparece na linha, como a prévia de `elm.md` pede.
- Na por fora, o título segue as opções de hoje (renomear · só incluir o prefixo · manter o título); `manter`
  sozinho deixa a tarefa fora da sprint.
- As linhas que mudam o escopo (4 e 8) esperam o "sim" do P.O. (decisão 6).
- O cabeçalho conta as divergências e os itens conferidos; nada diverge → só a linha do passo 6.

## 4. Mudanças por arquivo

| Arquivo (em `powers/sdd/skills/`, salvo indicação) | O que muda |
|---|---|
| `sdd-planejamento/references/elm-sprint.md` | **§9** reescrito pelas seções 1–3 (título "Sincronizar a sprint com o EWM"). **§1** (`:66-77`): ao rodar, tira o `**Publicação no EWM:** pendente` do cabeçalho (decisão 24). **Topo** (`:9-10`): no backlog ficam também as tarefas do item que saiu da sprint sem começar — pelo Encaixe ou pelo §9 (fatia, `[ESP]`, Sustentação) — e elas movem quando ele volta (decisão 7a). **§3** (`:115-117`): o épico `novo` ou `elegivel` pode ter a `[ESP]` no backlog, que move ao entrar; "Na sprint" (`:137-139`): o IB e o épico movem na chamada única, só com `iteracao`; cada tarefa que já existe move na chamada dela, com o dono e a estimativa do papel; o item que sai sem ter começado — pelo Encaixe ou pelo §9 — volta com `iteracao = backlog`, com as tarefas. **§4** (`:146-149`), **§6** (`:178-183`) e **§7** (`:187-188`, Troca AFK → HITL): a tarefa só nasce para o papel que o item não tem (`elm_listar_wi(pai = IB)`, sem contar a descartada nem a que tem pendência de cancelamento — decisão 7a). **§5** (`:153-158`): o §9 é o da pré-condição da virada (sai o "Antes de tudo, §9", que rodaria depois da migração); o §1 da próxima antes do movimento, em toda virada; a lista do que move, a ordem e a virada pela metade pela decisão 16; e o `total` = 1000 (decisão 20) |
| `sdd-planejamento/SKILL.md` | passo 7 do modo sprint (`:133-138`): sincronizar também compara as conhecidas; na virada, a publicação e a sincronização da próxima vêm depois do §5; o arquivo da sprint que é gravado antes do §1 (sem o MCP, com falha, ou o da próxima, no passo 4 da virada) leva `**Publicação no EWM:** pendente`, que a publicação tira (decisão 24). **Sincronizar com o EWM** (`:170-174`): por fora e divergências, numa tabela com a solução proposta, "ok" ou ajuste por linha, e o "sim" do P.O. no escopo. **Encaixe** (`:176-196`): a fatia que entrou pelo EWM (o IB, ou uma tarefa de papel por fora) chega aqui como `encaixe` (decisão 8a), com a Observação `encaixe: trazida do EWM — <decisão> (<quem decidiu>, <data>)`; a tarefa que já existe move em vez de nascer (decisão 7a); a linha de Sustentação com `saiu da sprint` não conta na reserva (decisão 22). **Pré-condição** (`:223-224`): sempre a linha de resultado, "sem tarefa por fora nem divergência", e nunca "não é preciso sincronizar" sem a comparação. **Retrospectiva e virada**: no passo 3 (`:275-284`), a linha com `saiu da sprint` não migra (decisão 23); nos passos 4–5 (`:285-291`), a ordem da decisão 16 — o §1 da próxima e o movimento do §5 antes da publicação dela e do §9 dela. `description`: + "sincronizar com o EWM" (a `sdd-sync`, do bundle, atende "sincroniza o ELM") |
| `sdd-status/SKILL.md` | Coleta, item 2 (`:24-31`): também as pendências sem `ELM feito` do Histórico do `status.md` da base de toda fatia `concluida` com pendência aberta, para a lista 🏛️ e para a contagem. Coleta, item 6 (`:44-48`): o marcador `**Publicação no EWM:** pendente` (sem listar — decisão 24) e a listagem sem `tipo`, com as regras de `total` e de tipo (decisões 20 e 21), e as divergências que ela mostra, pela seção 2 (decisão 15); a reserva × consumido sem as linhas com `saiu da sprint` (decisão 22, também na inconsistência de `:114`); a inconsistência "situação diferente" (`:106-107`) pela linha sem `saiu da sprint` (decisão 23); as pendências dos itens 2 e 4 e as do Histórico do `status.md` da base das fatias `concluida` da sprint fora da contagem (decisão 13). Painel (`:80`, `:83`): `🔄 EWM: <n> por fora · <m> divergências · <k> a conferir (<ids>) → sincroniza a sprint (sdd-planejamento)`; nada → `🔄 EWM: sem diferença na listagem (<n> itens)`; iteração inexistente → `🔄 EWM: sprint não publicada → sincroniza a sprint`; sem o MCP → `🔄 EWM: não conferido (sem o MCP elm)` |
| `sdd-fatiar/references/backlog.md` | **Volta** (`:102-106`): a `planejada` que sai da sprint também por movimento no EWM (§9), com as tarefas no backlog do EWM até ela voltar; **Épico** (`:117-137`): `elegivel` também do `planejado` que saiu da sprint; **Sustentação** (`:139-148`): `em-andamento`, `concluido` e `cancelado` também pela sincronização (tarefa conhecida que mudou de estado no EWM), e o item `aberto` que sai da sprint (`sprint` `—`, a linha com `saiu da sprint`); **Quem escreve o quê** (`:159`, `:162-163`): `status`, `sprint`, `responsavel` e `concluida-em` pela sincronização (§9); **Gravar na base** (`:181-211`): a regra da linha viva — com duas linhas do mesmo id na sprint aberta, lê-se e escreve-se a sem `saiu da sprint`, e a outra nunca é editada (decisão 23) |
| `sdd-planejamento/references/arquivos.md` | Cabeçalho (`:128-135`): a linha opcional `**Publicação no EWM:** pendente` (decisão 24), como a `**Fechamento sem consolidar:**`. Situações ao vivo (`:204-211`): a linha da Especificação que sai da sprint fica `elegivel`, e a da Sustentação fica `aberto`, as duas com `saiu da sprint`, como a da fatia; o item que volta à sprint de onde saiu ganha linha nova, e a com `saiu da sprint` fica como histórico, nunca editada e sem migrar; a viva é a sem `saiu da sprint` (decisão 23). Observações (`:216-219`): `concluído no EWM`, `cancelado no EWM` e o motivo `movida no EWM para <iteração>` em `saiu da sprint` |
| `sdd-desenvolver/SKILL.md` | Passo 4, item 5 (`:151-155`): a fatia que saiu de uma sprint sem começar tem o IB e as tarefas no backlog do EWM — o IB move (só `iteracao`) e cada tarefa move na chamada dela, com o dono e a estimativa do papel, antes do `assumir`; só nasce o papel que falta (decisão 7a) |
| `sdd-loop/SKILL.md` | Passo 1, item 4 (`:75-77`): a mesma regra para a puxada do lote — "fatia sem `[DEV]`" passa a ser conferida com `elm_listar_wi(pai = IB)`; o IB e as tarefas que já existem movem para a iteração da sprint antes do `assumir` (a `[DEV]` com quem dispara), e só a que falta nasce |
| `sdd-especificar/SKILL.md` | Passo 1 (`:35-38`) e Passo 2 (`:45-48`): o épico `elegivel` pode ter a `[ESP]` no backlog do EWM (saiu de uma sprint sem começar): ela é a `[ESP]` da linha e move para a iteração da sprint **com o IB do épico**, em vez de o épico contar como "sem `[ESP]`" |
| `sdd-atender/SKILL.md` · `sdd-executar/SKILL.md` | barreira do Passo 2 (`sdd-atender:42-44`) e do passo 1 (`sdd-executar:34-36`): o item que só tem, na sprint, a linha com `saiu da sprint` é item fora dela (decisões 22 e 23) |
| `sdd/references/elm.md` | Regras de toda escrita, item 2 (`:55-60`): a busca de idempotência por pai e prefixo não conta a tarefa descartada nem a que tem pendência de cancelamento aberta (decisão 7a). Pendências (`:65-68`): a exceção da sincronização — a falha que a próxima comparação vê de novo não grava pendência, e a linha que muda o escopo não grava o arquivo quando o movimento falha (decisão 25). Regra nova: sprint com `**Publicação no EWM:** pendente` — nenhuma tool recebe a iteração dela antes do §1 (decisão 24) |
| `sdd-triar/SKILL.md` | Sprint sugerida (`:146-150`): o usado da reserva não soma as linhas com `saiu da sprint` (decisão 22) |
| `sdd-aprender/SKILL.md` | retrospectiva de sprint (`:84-85`): a pré-condição inteira — sincronização com o EWM e consolidação |
| `sdd/SKILL.md` | "Quero…" (`:148`): "trazer para a sprint o que mudou no EWM — tarefas por fora e divergências das conhecidas ('sincroniza a sprint')" |
| `sdd-setup/assets/steering/sdd.md` | `:52-53`: a sincronização traz a tarefa criada no EWM e compara as conhecidas (estado, iteração, dono, estimativa) |
| as 22 `*/SKILL.md` | `metadata.version` → `3.4.1` |
| `powers/sdd/plugin.json` | `version` → `3.4.1`; keyword `sincronizar com o ewm` |
| `powers/sdd/README.md` | entrada "Na **3.4.1**": a sincronização compara as conhecidas, a tabela única com a solução proposta, a linha de resultado nos ritos e no painel, a virada que move só o que está aberto no EWM (antes da publicação da próxima) e as tarefas que movem, em vez de nascer de novo, quando o item volta a uma sprint. Requer o `mcp-elm ≥ 3.3.5` (sem mudança no MCP) |

Não mudam: `mcps/elm` (decisão 17), `papeis.json` e os agentes, `sdd-iniciar` (a "minha próxima tarefa" já indica
a "sincroniza a sprint") e `powers/README.md` (continuam 22 skills). Os demais gravadores da sprint
(`sdd-desenvolver` Passos 4 e 6, `sdd-consolidar` Passo 4, `sdd-especificar` Passos 2 e 6, `sdd-atender`,
`sdd-executar`, Troca de modo e o passo 2 da virada) seguem a regra da linha viva pelo bloco Gravar na base que já
citam, sem mudança no texto deles.

## 5. Ordem de execução e versões

1. `elm-sprint.md` §9, topo, §3, §4, §5 e §6 — a fonte das demais.
2. `backlog.md` e `arquivos.md`.
3. `sdd-planejamento/SKILL.md`, `sdd-status/SKILL.md`, `sdd-desenvolver/SKILL.md`, `sdd-loop/SKILL.md`,
   `sdd-especificar/SKILL.md`, `sdd-atender/SKILL.md`, `sdd-executar/SKILL.md`, `sdd-triar/SKILL.md`,
   `sdd-aprender/SKILL.md`, `sdd/SKILL.md` e `assets/steering/sdd.md`.
4. Versão 3.4.1: `metadata.version` das 22 skills, `plugin.json` e o histórico do `README.md` do power.
5. Commits por área (`sdd 3.4.1: …`), sem trailer de coautoria; exemplos só com nomes genéricos.

## 6. Fora do escopo (achados de passagem)

- **"Planejadas" sem fonte nas fatias:** o `elm_horas(iteracao)` não traz estimativa (`ewm.py:665-688`), e a sprint
  não guarda as horas das fatias; a coluna "Planejadas (h)" dos Números (`arquivos.md:186`) não tem de onde vir
  para `[DEV]`, `[REV]`, `[VER]` e `[APR]`.
- **Troca de modo:** a "menor alocação" (`sdd-planejamento/SKILL.md:207-208`) soma estimativas pelo
  `elm_listar_wi(iteracao, dono)`, que não devolve estimativa.
- Os dois se resolvem com a mudança do MCP adiada na decisão 17 (`estimativa_h` e o grupo do estado no
  `elm_listar_wi`), numa próxima versão.
- **Pai trocado no EWM:** a listagem não traz o pai; compará-lo exigiria um `elm_ler_wi` por id.
- **Tarefa fechada movida à mão para outra iteração:** não é apontada quando sai da listagem (decisão 7), porque o
  MCP não traz a data da conclusão para saber onde ela fechou; as horas dela contam na iteração para onde foi.
- **IB de épico concluído reaberto depois da sprint em que concluiu:** fica na iteração daquela sprint e não aparece
  na listagem da atual; só é visto se for reaberto ainda nela.
- **Título sem o prefixo** (decisão 11): o `elm_horas` classifica as horas pelo prefixo do título, então a tarefa
  com o título mantido sai sem prefixo no relatório — custo já aceito na 3.3.0.
- **`sdd-atender` e `sdd-executar` com a tarefa já concluída no EWM:** o `assumir` falha com `precondicao` ("já
  concluída: reabra antes", `ewm.py:527-528`), e a skill não diz o que fazer.
- **Troca de responsável da fatia com troca de modo:** não há fluxo (decisão 9). E o `responsavel` do backlog não
  acompanha quem inicia uma puxada ou retoma a fatia (`sdd-desenvolver/SKILL.md:133-136` só o grava se estava `—`);
  a sincronização o acerta pelo dono da `[DEV]` (decisão 9), mas a regra da puxada fica como está, e o Responsável do
  `status.md` da branch, que é do Dev, também.
- O mapa do GitHub Pages (branch `gh-pages`) está na 3.3.1, e o `mcps/elm/docs/manual-mcp-elm.md:96-107` segue atrás
  da mcp-elm 3.3.5 (já apontado na 3.4.0).

## 7. Verificação

- **Ensaio de mesa** do §9 novo: **um caso por linha das tabelas da seção 2**, com a linha da tabela da seção 3 que
  cada um gera e o que a gravação escreve nos arquivos e no EWM. Além deles, os casos que cruzam regras:
  - (a) linha com Tarefa ELM `pendente` (planejamento sem o MCP) → `EWM: publicar`, nunca "sai da sprint"; e a mesma
    fatia, já iniciada com os ids no `status.md` → comparada por eles; a sprint planejada inteira sem o MCP (com
    `**Publicação no EWM:** pendente`) → a primeira linha cria a iteração e o plano, e a listagem vem depois — também
    numa PA com outro produto que tem a mesma `2026/Sprint <nn>`, que a listagem pelo nome acharia; e um Encaixe com
    o marcador → o §1 roda antes, e nada vai para a sprint do outro produto; uma escrita que falha no EWM → sem
    pendência no dono de uma tarefa aberta (a linha volta na sincronização seguinte), com pendência no "concluir o IB"
    de um AT concluído na pré-condição da virada; a entrada de um AT cujo IB não moveu → o arquivo não muda, e a
    linha volta como entrada (nunca como "saiu"); a por fora que virou item, com o IB `[AT-nnn]` criado e o renomear
    falhando → o item entra com o IB e a pendência na ficha; a por fora de papel cujo renomear falhou → fica fora dos
    arquivos e volta como por fora;
  - (b) IB de AT `aberto` sem sprint e uma `[ATD]` feita à mão na iteração → uma linha só, nenhuma `[ATD]` nova, o IB
    vai para a sprint, e a sincronização seguinte não mostra o AT saindo;
  - (c) IB de fatia `elegivel` com uma `[DEV]` feita à mão → um encaixe só, e a `[DEV]` não nasce de novo; fatia
    `nova` na mesma situação → a DoR antes;
  - (d) fatia `planejada` com o IB movido para a `Sprint 04` do EWM → sai da sprint com o P.O., e a linha leva o IB e
    as tarefas para o backlog do EWM; ela volta noutra sprint → cada tarefa move com o dono e a estimativa do papel, e
    a HITL que volta AFK deixa a `[REV]` e a `[VER]` como `ELM pendente [<tipo> <id> cancelar]` — e, depois de o
    P.O. cancelar no EWM e gravar o `ELM feito`, nenhuma sincronização nem o painel as mostram; e, se antes disso a
    fatia trocar para HITL (§7), a `[REV]` e a `[VER]` nascem de novo, sem reaproveitar as que esperam o
    cancelamento;
  - (e) a mesma fatia puxada pelo `sdd-loop` e pela `sdd-desenvolver` → o IB e a `[DEV]` movem antes do `assumir`;
    e, se a puxada é na sprint de onde ela saiu, a linha nova é a viva — o `iniciada`, o `pronta`, a consolidação e
    os créditos caem nela, a com `saiu da sprint` não muda e não migra na virada; o mesmo com um AT que sai e volta
    pelo Encaixe (duas linhas `aberto`: a `sdd-atender` grava na viva);
  - (f) épico `elegivel` cuja `[ESP]` ficou no backlog volta pela `sdd-especificar` → a `[ESP]` e o IB do épico
    movem, sem `[ESP]` nova;
  - (g) fatia retomada por outro Dev, ou puxada por quem não era o `responsavel`, sincronizada durante o GATE do
    plano (o Responsável do `status.md` é o aprovador) → a `[DEV]` fica com quem implementa e o arquivo o registra;
    passada ao verificador da fatia → volta para o Responsável da linha viva, e o backlog acompanha; e a puxada em
    que o dono é o Responsável da linha viva, mas o `responsavel` do backlog ficou com o planejado → o backlog passa
    a ter o dono, e o planejado pode verificar a fatia;
  - (h) duas sprints numa iteração do EWM → nenhuma linha "entrou" para o que fechou na primeira;
  - (i) impedimento na iteração → nenhuma linha; `total` = 1000 → para; pendência registrada não aparece, inclusive
    a `[EP-<nn> concluir]` do rodapé do PRD e a `[VER <id> concluir]` do Histórico de uma fatia `concluida`; fatia
    `iniciada` mergeada pela UI do GitLab (sem a branch) → os ids vêm do `status.md` da base, sem linha por fora;
  - (j) linha de Sustentação com `saiu da sprint` → fora do usado da reserva na triagem, no painel e no Encaixe, e
    as barreiras da `sdd-atender` e da `sdd-executar` a tratam como fora da sprint;
  - (k) épico `concluido` com o IB reaberto na mesma sprint → `EWM: concluir o IB`; AT `aberto` sem sprint cuja
    `[ATD]` foi feita e concluída à mão na iteração → entra `concluido`, com o IB movido e concluído na mesma linha;
  - (l) virada com o mesmo pai e com pai novo: o §9 da pré-condição, a migração, o replanejamento, o §1 da próxima
    (a iteração nasce antes do movimento), o movimento — uma tarefa fechada fica, uma aberta muda de iteração, e o
    IB de um épico `iniciado` com a Especificação `concluida` também muda —, depois a publicação da próxima e o §9
    dela, sem nenhuma saída falsa; e a virada pela metade (sem o MCP) → a sincronização da próxima cria a iteração,
    propõe `EWM: mover para esta sprint` para as linhas migradas e `EWM: publicar` para as novas, nunca "saiu";
    parada depois do §1 e antes do §3–4 → as linhas novas sem ids saem como `EWM: publicar`; duas viradas seguidas
    sem o MCP → o id que ficou duas sprints atrás é reconhecido pela cadeia `migrada de`;
  - (m) painel na sprint seguinte, com uma fatia migrada cuja `[REV]` fechou na anterior → nenhuma divergência nem
    `a conferir`; fatia `concluida` com a `[DEV]` aberta e a pendência no Histórico → nenhuma divergência; painel com
    por fora e divergências, "sprint não publicada" com a iteração inexistente, e "não conferido" sem o MCP;
  - (n) nada diverge → a linha de resultado na pré-condição da review, da retrospectiva (também pela `sdd-aprender`)
    e da virada.
- **Varreduras**, uma por linha, a partir da raiz (rodam no fish):

  ```
  grep -rn "por fora" powers/sdd
  grep -rn "segue calado\|sprint e EWM iguais" powers/sdd
  grep -L 'version: "3.4.1"' powers/sdd/skills/*/SKILL.md
  ```

  Toda menção a "por fora" cobre também as divergências, menos o histórico do `README.md` e o "PR já mergeado por
  fora" da `sdd-desenvolver` (outro assunto); a segunda e a terceira não acham nada.
- **Testes** (sanidade: nenhum script muda): `uv run --with pytest pytest powers/sdd/skills/sdd-setup/scripts
  powers/sdd/skills/sdd-status/scripts -q` (15 passam hoje) e `cd mcps/elm && uv run pytest -q` (49 passam hoje).
- **Revisão:** a seção 11 do [plano da 3.4.0](plano-sdd-3.4.0.md#11-como-revisar-de-novo-depois-de-uma-alteração),
  com este documento como especificação e os três ângulos voltados ao §9: (1) situações e quem grava (a
  sincronização nunca grava situação de fatia nem de épico a partir do estado do EWM; só a Volta e o encaixe, com o
  "sim" do P.O.; Sustentação pela seção 2); (2) formatos (a tabela, as Observações novas, a Especificação `elegivel`
  e a Sustentação com `saiu da sprint`, citações "§n" e "Passo N"); (3) EWM e permissões (só tools e parâmetros que
  existem em `mcps/elm/mcp_elm/server.py`, o agente de produto com cada uma, e a tarefa que move em vez de nascer).
- **Piloto:** a sprint de ensaio com os casos (b), (d), (l) e a linha "tarefa concluída" da Sustentação feitos de
  verdade no EWM.
