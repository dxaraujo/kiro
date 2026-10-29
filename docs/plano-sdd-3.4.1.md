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
- `elm_transicao` assume, conclui e **reabre**; cancelar continua manual (`ELM pendente [<id> cancelar]`).
- O agente de produto, onde a sincronização roda, tem tudo isso: `elm-leitura` liberado, `elm-tarefa` e
  `elm_atualizar_wi` com pergunta, e grava `<produto>/**`, fichas de `sustentacao/` inclusive
  (`sdd-setup/assets/agents/papeis.json`). Nenhuma permissão muda.

O plano foi conferido por uma revisão adversarial e por oito verificações independentes dos achados (dois ângulos
por grupo: regras e código, cenário passo a passo). Os onze furos confirmados estão corrigidos abaixo.

## Discussões e decisões

| # | Questão | Opções levantadas | Decisão |
|---|---|---|---|
| 1 | Onde está o defeito | MCP `elm` (filtro da iteração) · desenho do §9 | §9: o MCP está certo |
| 2 | Quem prevalece numa divergência | EWM sempre · arquivo sempre · por tipo de item · perguntar por linha | **nenhum lado prevalece sozinho** (pedido): uma tabela com todas as divergências, cada uma com a solução proposta; a pessoa aprova o lote ("ok") ou ajusta uma ou mais linhas. A solução proposta segue a seção 2: na Sustentação, o arquivo recebe o EWM; na fatia e no épico, o estado não muda pelo EWM (o EWM é corrigido, ou a linha fica com quem resolve) e o dono segue as regras da equipe (decisão 9); na iteração, vale a situação do item |
| 3 | Fatia e épico mudam de situação pelo estado do EWM | sim · não (só avisa) | **não** (proposta do rascunho, mantida): a situação deles só muda pela skill que a causa (`pronta` exige o Passo 6 da `sdd-desenvolver`: `status.md` na base, créditos, lições). Nas linhas de estado da fatia e do épico, o ajuste é `EWM` ou `manter`, nunca `arquivo`. A sincronização só grava a situação de fatia ou de épico numa decisão de escopo do P.O.: a Volta (decisão 7) e o encaixe (decisões 8 e 8a) |
| 4 | Tarefas por fora e divergências | duas tabelas (rascunho) · uma | **uma tabela** (pedido: "todas as divergências"): a tarefa por fora é a linha de Campo `por fora`, com o tipo inferido e o título proposto na solução |
| 5 | Ajuste por linha | — | `<n>: arquivo` (o arquivo recebe o EWM) · `<n>: EWM` (o EWM recebe o arquivo) · `<n>: manter` (nada é gravado, e a linha volta na próxima sincronização) · na por fora, o tipo e o título, como hoje: `9: [EXT]`, `9: só incluir o prefixo`, `9: manter o título` (traz a tarefa sem renomear; o `manter` sozinho não a traz) |
| 6 | Quem aprova mudança de escopo | quem roda · só o P.O. | sair da sprint e o encaixe pedem o "sim" do **P.O.**, como no Encaixe e no Fechamento sem consolidar; sem ele, a linha fica `manter` nesta rodada |
| 7 | Item que saiu da sprint no EWM | — | a saída vale pelo **item** (o IB ou a origem; na Especificação, a `[ESP]`) e só para o que está **aberto** no EWM: o fechado fica na iteração em que fechou (decisão 16). Não iniciado (fatia ou Especificação `planejada`, Sustentação `aberto`) → sai da sprint pela Volta do `backlog.md`, e o IB e as tarefas vão para o backlog do EWM (o sdd não tem sprint futura: a próxima nasce no planejamento). Iniciado → volta para a iteração da sprint (de `iniciada` em diante nada volta). Só uma tarefa fora (ou, na Especificação, só o IB do épico), com o item na sprint → ela volta. A linha com a publicação pendente nunca "sai" (decisão 13) |
| 7a | Tarefa que ficou no backlog do EWM quando o item volta a uma sprint | recriar · mover | **mover**, nunca recriar (a regra do topo do `elm-sprint.md`), com o dono e a estimativa do novo planejamento (`elm_atualizar_wi(ids, iteracao, dono, estimativa_h)`), senão a sincronização seguinte acusaria o dono velho. Só nasce o papel que falta, conferido com `elm_listar_wi(pai = IB)` (não pelo prefixo do título, que a pessoa pode ter mantido). Vale para a publicação (§3–4), o Encaixe, a puxada (`sdd-desenvolver` Passo 4) e a `sdd-especificar`, e cobre também as tarefas que o Encaixe da 3.4.0 já deixa no backlog |
| 8 | Item conhecido que entrou na iteração pelo EWM | — | "entrou" é estar na listagem e ser esperado noutra iteração — a do `**Iteração no EWM:**` da sprint do item, ou o backlog (uma iteração que cobre duas sprints, `sdd-planejamento/SKILL.md:289-291`, não gera linha). **Uma linha por item**, com o IB e as tarefas dele que estão na listagem (citadas, ou por fora com esse pai). Pelo tipo: fatia não iniciada → `encaixe` (decisão 8a); recusado → tudo volta ao backlog do EWM. Épico `novo` ou `elegivel` com a `[ESP]` (citada ou por fora) → a linha da Especificação nasce `planejada`, com `encaixe: trazida do EWM`, e o P.O. confirma (a regra de hoje para a `[ESP]` por fora); só o IB, sem a `[ESP]` → volta ao backlog (a especificação entra pelo planejamento, que dá o responsável e as horas). Item de Sustentação `aberto` → entra na sprint, como a tarefa de Sustentação por fora (reserva estourada → o P.O. decide pelo Encaixe se uma fatia sai). Item terminal → volta para a iteração esperada. IB de estrutura (`Sustentação`, `Manutenção`, categoria) → volta ao backlog |
| 8a | Encaixe da fatia trazida do EWM | na linha, na hora (passo 5 de hoje) · pela seção Encaixe | **pela seção Encaixe**: a linha da fatia precisa de responsável, do modo pela senioridade e, no HITL, de revisor e verificador (com a `[REV]` e a `[VER]`), que o passo 5 de hoje não pede. Vale para o IB que entrou e para a tarefa de papel por fora de uma fatia que não está na sprint; a tarefa que já existe vira a do papel inferido, e só o papel que falta nasce (decisão 7a) |
| 9 | Dono | — | Sustentação e `[ESP]` → o arquivo recebe o dono do EWM. `[REV]` → também, se o novo é Dev Sênior ativo e não implementa (ou é o `revisor único`: o implementador é o único Sênior ativo, `sdd-planejamento/SKILL.md:155-157`). `[VER]` → também, se o novo não implementa. `[DEV]` de fatia `planejada` → o arquivo recebe o novo responsável só se ele é Dev ativo, não é o Verificador da linha nem o Revisor (salvo `revisor único`) e o modo não muda pela senioridade dele: Júnior só em fatia HITL; Sênior em fatia AFK, ou HITL com o motivo já na `obs`; Pleno quando os critérios da `sdd-fatiar` dão o modo atual (`sdd-planejamento/SKILL.md:149`), com a confirmação do P.O. na própria linha. Fora disso, o EWM volta (trocar o responsável com troca de modo é do P.O., e o sdd não tem esse fluxo — seção 6). `[DEV]` de fatia `iniciada` em diante: o EWM volta (só quem iniciou retoma). Tarefa sem dono no EWM → recebe o do arquivo |
| 10 | Estimativa | comparar todas · só onde o arquivo guarda horas | **só onde o arquivo guarda horas** (Especificação: Horas previstas; Sustentação: Horas e `**Estimativa:**`); o arquivo recebe a do EWM, e só nas tarefas abertas. As fatias não guardam horas: nada a comparar |
| 11 | Título sem o prefixo do sdd | comparar · não | **não compara**: a triagem e o §9 aceitam "manter" o título (`sdd-triar/SKILL.md:161`), e não há como distinguir o título mantido do que perdeu o prefixo |
| 12 | `concluida-em` do item concluído no EWM | data da conclusão · data da sincronização | **a data da sincronização** (o MCP não traz a da conclusão), com a Observação `concluído no EWM`; a pessoa corrige pela linha |
| 13 | Pendência já registrada | divergência · não | **não é divergência**: `ELM pendente [<chave>]` sem `ELM feito` já cobre a diferença (ex.: `[AT-012 cancelar]`). A publicação pendente da linha (Tarefa ELM `pendente`, ou o item com `elm` `pendente` ou id sem link: planejamento sem o MCP ou com falha, `sdd-planejamento/SKILL.md:136-137`) cobre a linha inteira: o item e as tarefas ficam fora da comparação de estado e de iteração, e a solução é `EWM: publicar (§3–4)`, nunca "sai da sprint" |
| 14 | Resultado sem divergência | calado (hoje) · sempre uma linha | **sempre uma linha** (pedido): `🔄 <chave> × EWM: iguais — <n> itens conferidos`. O agente nunca diz que "não é preciso sincronizar" sem ter rodado a comparação |
| 15 | Painel da `sdd-status` | sincronização inteira · só a listagem | **só a listagem** (uma chamada, somente leitura). Por fora, estado, dono e entrada contam como divergências. O id da sprint ausente da listagem conta à parte, como `a conferir`, quando a linha dele não tem `migrada de`; o de linha migrada fica só para a sincronização (em geral é tarefa que fechou numa sprint anterior e ficou lá — decisão 16). Nada → `🔄 EWM: sem diferença na listagem (<n> itens)`: o painel não diz "iguais", que é da sincronização. A estimativa fica para a sincronização |
| 16 | Virada (§5) | mover pelos arquivos (hoje) · cruzar com o EWM | **cruzar**: move, entre os abertos na listagem da iteração que fecha, os ids do conjunto "da sprint" (§1, passo 2) que seguem no fluxo — as tarefas e o item das linhas que migram (inclusive os ids que só estão no `status.md`), o IB de todo épico `planejado` ou `iniciado` (mesmo com a linha da Especificação `concluida`, que não migra) e a `[GB]`, se o pai não muda. O que está fechado fica na iteração em que fechou: o que move é o conjunto "da sprint" da próxima, menos o que fechou |
| 17 | MCP `elm` | sem mudança · `elm_listar_wi` com o grupo do estado e a estimativa (mcp-elm 3.4.1) | **sem mudança** (pedido): segue o `mcp-elm ≥ 3.3.5`; a melhoria fica registrada na seção 6 |
| 18 | Versão | 3.4.1 sozinha · junto da próxima rodada | **3.4.1 sozinha** (pedido): o `plugin.json` e as **22** skills. A versão é única, como nas tags `sdd-3.3.1` e `sdd-3.4.0` (o rascunho dizia "skills alteradas"); o `**Power sdd:**` e os créditos gravam o `metadata.version` de quem escreve, e versões misturadas confundiriam essa conta |
| 19 | Migração | — | nenhuma (o power ainda não tem usuários, como na 3.4.0) |
| 20 | Listagem no teto do MCP | confiar no `truncado` · conferir o `total` | **`total` = 1000 → avise e pare** (o `truncado` nunca acusa com `limite 1000`): sem a listagem inteira faltariam por fora e entradas, e a linha "iguais" mentiria. Vale também para o painel e para a virada |
| 21 | Tipo que não é do `pa` (impedimento, retrospectiva…) | linha por fora · fora da comparação | **fora**, quando nenhum arquivo cita o id: conta nos conferidos, sem linha — senão o `manter` o traria de volta em toda rodada e a linha "iguais" nunca sairia. Id citado é comparado qualquer que seja o tipo (a origem de um épico pode ser de outro tipo, `elm-sprint.md:113-114`) |

## 1. O §9 novo — "Sincronizar a sprint com o EWM"

O título muda; nenhum link aponta para a âncora (as skills citam "§9"). Roda depois de publicar a sprint (§4), na
pré-condição dos ritos de fechamento e sob pedido ("sincroniza a sprint", "sincronizar com o EWM"). Sem o MCP `elm`
→ "sincronização com o EWM não feita" (sob pedido, pare).

1. **Listar** — `elm_listar_wi(iteracao = "<pai>/<nome>" da sprint, limite 200)`, **sem `tipo`** (tarefas, IBs,
   defeitos e épicos). `truncado` → repita com `limite 1000`. `total` = 1000 → avise e pare (decisão 20).
2. **Onde cada id deveria estar**, pelos arquivos. Cada item entra com **todos** os ids dele: o IB ou a origem e as
   tarefas (a coluna `elm` do `backlog.md`, a "Tarefa ELM" da linha e, na fatia `iniciada` ou `pronta`, o campo ELM do
   `status.md`).
   - **da sprint** (esperado na iteração da sprint): os itens das linhas do `sprint-<nn>.md` aberto, menos as que têm
     `saiu da sprint`, com os ids dos `status.md` das fatias da sprint `iniciada` (na branch, `git show
     origin/<branch>:…`) e `pronta` (na base); a `[GB]` do pai; e o IB de cada épico `planejado` ou `iniciado` (ele
     acompanha as sprints até concluir, §3 e §5);
   - **do backlog** (esperado no backlog do EWM): os IBs `Sustentação`, `Manutenção` e de categoria e os itens não
     terminais fora da sprint (`sprint` `—`), inclusive os que saíram dela, com as tarefas que ficaram no backlog
     (decisão 7a);
   - **terminal de fora**: o item terminal cuja `sprint`, no `backlog.md`, não é esta — esperado na iteração do
     `**Iteração no EWM:**` daquela sprint (`—`: o backlog). O IB do épico terminal fica fora desta conferência: ele
     acompanha as sprints até concluir, e o `backlog.md` não diz em qual concluiu;
   - **por fora**: o id da listagem que nenhum arquivo cita, com `tipo` do `pa` (decisão 21).

   **Publicação pendente** (decisão 13): a linha com Tarefa ELM `pendente`, ou cujo item tem `elm` `pendente` ou id
   sem link, fica fora das comparações abaixo; ela vira a linha `EWM: publicar (§3–4)`.
3. **Comparar** — "entrou" e "saiu" só quando a iteração real não é a esperada:
   - da sprint, presente na listagem → estado e dono (seção 2);
   - da sprint, ausente da listagem → `elm_ler_wi(id, comentarios 0)`: aberto noutra iteração → saiu; fechado → fica
     onde fechou (não é divergência de iteração, mas o estado é comparado); `nao_encontrado` → sumiu;
   - tarefa aberta da Especificação e da Sustentação → `elm_ler_wi(id, comentarios 0)`, para a estimativa (a tarefa
     que já foi lida porque saiu não é lida de novo);
   - do backlog ou terminal de fora, presente na listagem e esperado noutra iteração → entrou: **uma linha por
     item**, com o IB e as tarefas dele que estão na listagem — as citadas e as por fora cujo pai é esse item;
   - por fora → a inferência de hoje (o passo 3 atual: `elm_ler_wi` para o pai, os campos e a descrição; prefixo,
     pai, Classificação, título e descrição). A tarefa cujo pai é um item que entrou vai na linha dele; o IB ou
     defeito fora do `backlog.md` vira linha `triar`, o que resolve a contradição do passo 4.

   O que já é pendência — `ELM pendente [<chave>]` sem `ELM feito`, coletadas como na `sdd-status` (Coleta, item 2)
   — não é divergência.
4. **Prévia** — uma tabela só, com a solução proposta em cada linha (seção 3).
5. **Gravar** com o "ok", ou depois dos ajustes:
   - **EWM** primeiro, com o mesmo "ok" (é a prévia de `elm.md`, Regras de toda escrita): `elm_atualizar_wi` para
     iteração, dono, estimativa e, na por fora, título e pai; `elm_transicao` para concluir o IB do item de
     Sustentação concluído e reabrir a `[ESP]`, a `[GB]` ou um IB; a publicação pendente pelo §3–4. A tarefa só nasce
     para o papel que o item não tem (decisão 7a). Uma falha → `ELM pendente [<chave>]` no lugar do artefato
     ([Pendências](../powers/sdd/skills/sdd/references/elm.md#pendências)); o lado do arquivo segue;
   - **arquivos** (`backlog.md`, `sprint-<nn>.md` e as fichas de `sustentacao/**`) pelo bloco
     [Gravar na base](../powers/sdd/skills/sdd-fatiar/references/backlog.md#gravar-na-base), num commit
     `<pai>/Sprint <nn>: sincronizar com o EWM` (já está no `sdd.md`), com as horas na `[GB]`;
   - as linhas `encaixe` seguem depois, uma a uma, para a seção Encaixe da `sdd-planejamento` (decisão 8a).
   As regras de hoje para gravar a por fora (passo 5 atual: Tarefa ELM da linha, `trazida do EWM`, o épico que entra
   pela `[ESP]`, a tarefa de Sustentação que vira item, IB `[XX-nnn]`, reserva estourada → Encaixe) continuam; só a
   fatia que ainda não está na sprint passa a ir para o Encaixe.
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
| `concluido` · `cancelado` | tarefa aberta (reaberta) | manter: situação terminal não volta, e trabalho novo é item novo (`sdd-triar`) | EWM: concluir de novo |
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
| `iniciada` em diante | `[DEV]` com outro dono | EWM: o dono volta (só quem iniciou retoma) | — |
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
| publicação pendente | EWM: publicar a linha (§3–4) | — |
| saiu (aberto), item não iniciado | arquivo: sai da sprint (P.O.) — fatia `elegivel` (ou `nova`, pela DoR), épico `elegivel`, Sustentação `aberto`, com `sprint` `—`; a linha da sprint fica com a mesma situação e `saiu da sprint: movida no EWM para <iteração> (<P.O.>, <data>)`; o IB e as tarefas vão para o backlog do EWM | EWM: volta para a sprint |
| saiu (aberto), item iniciado | EWM: volta para a iteração da sprint | — |
| só uma tarefa aberta saiu (ou só o IB do épico), com o item na sprint | EWM: volta | — |
| fechado e fora da listagem | não é divergência: fica onde fechou | — |
| sumiu (`nao_encontrado`) | manter: confira na UI do EWM | — |
| entrou: fatia não iniciada fora da sprint (o IB, tarefas dela, ou os dois) | encaixe (P.O., seção Encaixe; a tarefa que já existe é a do papel) — recusado, EWM: tudo volta ao backlog | EWM: volta ao backlog |
| entrou: épico `novo` ou `elegivel`, com a `[ESP]` | arquivo: Especificação `planejada` e épico `planejado`, com `encaixe: trazida do EWM (<P.O.>, <data>)`; Responsável e Horas previstas pelo dono e pela estimativa da `[ESP]` | EWM: volta ao backlog |
| entrou: épico `novo` ou `elegivel`, só o IB | EWM: volta ao backlog (a especificação entra pelo planejamento) | — |
| entrou: item de Sustentação `aberto` (o IB, a tarefa, ou os dois) | arquivo: entra na sprint (linha `aberto` com `trazida do EWM`); a tarefa que já existe é a dele, e só sem ela a tarefa nasce (§6), com o `responsavel` e a `**Estimativa:**` da ficha, ou os que a pessoa der na linha | EWM: volta ao backlog |
| entrou: item terminal | EWM: volta para a iteração esperada | — |
| entrou: IB de estrutura | EWM: volta ao backlog | — |

**Por fora:** a tarefa segue a inferência e as soluções de hoje (a da fatia fora da sprint, pelo Encaixe — decisão
8a); o IB ou defeito fora do `backlog.md` → triar (`sdd-triar`, "importar do EWM"), com a outra solução "EWM: volta
ao backlog".

## 3. A tabela

```
🔄 2026/Sprint 03 × EWM — 9 divergências · 41 itens conferidos
| # | Item | No EWM | Campo | Arquivo | EWM | Solução proposta |
|---|---|---|---|---|---|---|
| 1 | AT-012 | ATD 670301 | estado | em-andamento | Concluído | arquivo: concluido, concluida-em 2026-10-28 (concluído no EWM) · EWM: concluir o IB 669379 |
| 2 | IM-003 | IMPL 670215 | dono | ana.souza | rita.melo | arquivo: responsável rita.melo |
| 3 | IM-003 | IMPL 670215 | estimativa | 4 h | 6 h | arquivo: Horas 6 |
| 4 | FT-036 | IB 670188 | iteração | 2026/Sprint 03 | Backlog | arquivo: sai da sprint — elegivel, sprint — (P.O.) |
| 5 | FT-031 | DEV 669401 | iteração | 2026/Sprint 03 | Sprint 04 | EWM: volta para 2026/Sprint 03 (fatia iniciada) |
| 6 | FT-033 | DEV 669410 | estado | iniciada | Concluído | manter: o Dev confere — PR mergeado → sdd-desenvolver Passo 6; senão, reabrir |
| 7 | EP-05 | ESP 669377 | estado | iniciada | Concluído | EWM: reabrir a [ESP] (fecha no GATE do backlog) |
| 8 | FT-040 | IB 670400 · DEV 670401 | iteração | backlog (elegivel) | 2026/Sprint 03 | encaixe (P.O.; a DEV 670401 é a da fatia) — recusado: volta ao backlog |
| 9 | — | 670210 | por fora | — | "ajustar job de carga" · joao.lima · Em Andamento | [DEV] de FT-034 → Tarefa ELM dela · título "[DEV] FT-034 ajustar job de carga" |
"ok" aplica tudo como proposto · ou ajuste uma ou mais linhas: "4: EWM", "6: EWM", "2: manter", "9: só incluir o prefixo"
```

- **No EWM** é o tipo e o id (o item que entrou leva os ids dele na mesma linha, 8); **Campo**: `estado` · `dono` ·
  `estimativa` · `iteração` · `sumiu` · `por fora` · `publicação`.
- A solução diz onde grava: `arquivo:` (o arquivo recebe o EWM), `EWM:` (o EWM recebe o arquivo), `manter:` (nada é
  gravado; diz quem resolve), `encaixe` ou `triar` (encaminha). Linha com as duas partes (1) grava as duas.
- Na por fora, o título segue as opções de hoje (renomear · só incluir o prefixo · manter o título); `manter`
  sozinho deixa a tarefa fora da sprint.
- As linhas que mudam o escopo (4 e 8) esperam o "sim" do P.O. (decisão 6).
- O cabeçalho conta as divergências e os itens conferidos; nada diverge → só a linha do passo 6.

## 4. Mudanças por arquivo

| Arquivo (em `powers/sdd/skills/`, salvo indicação) | O que muda |
|---|---|
| `sdd-planejamento/references/elm-sprint.md` | **§9** reescrito pelas seções 1–3 (título "Sincronizar a sprint com o EWM"). **Topo** (`:9-10`): no backlog ficam também as tarefas do item que saiu da sprint sem começar — pelo Encaixe ou pelo §9 (fatia, `[ESP]`, Sustentação) — e elas movem quando ele volta (decisão 7a). **§3** (`:115-117`): o épico `novo` ou `elegivel` pode ter a `[ESP]` no backlog, que move ao entrar; "Na sprint" (`:137-139`): movem o IB e as tarefas que já existem, com o dono e a estimativa do planejamento, e o item que sai sem ter começado — pelo Encaixe ou pelo §9 — volta com `iteracao = backlog`, com as tarefas. **§4** (`:146-149`) e **§6** (`:178-183`): a tarefa só nasce para o papel que o item não tem (`elm_listar_wi(pai = IB)`). **§5** (`:153-158`): "Antes de tudo, §9 (o que nasceu por fora e o que mudou nas conhecidas)", a lista do que move pela decisão 16 e o `total` = 1000 (decisão 20) |
| `sdd-planejamento/SKILL.md` | passo 7 do modo sprint (`:137-138`): sincronizar também compara as conhecidas; **Sincronizar com o EWM** (`:170-174`): por fora e divergências, numa tabela com a solução proposta, "ok" ou ajuste por linha, e o "sim" do P.O. no escopo; **Encaixe** (`:176-196`): a fatia que entrou pelo EWM (o IB, ou uma tarefa de papel por fora) chega aqui como `encaixe` (decisão 8a), com a Observação `encaixe: trazida do EWM — <decisão> (<quem decidiu>, <data>)`, e a tarefa que já existe move em vez de nascer (decisão 7a); **pré-condição** (`:223-224`): sempre a linha de resultado, "sem tarefa por fora nem divergência", e nunca "não é preciso sincronizar" sem a comparação; `description`: + "sincronizar com o EWM" (a `sdd-sync`, do bundle, atende "sincroniza o ELM") |
| `sdd-status/SKILL.md` | Coleta, item 6 (`:46-48`): a listagem sem `tipo`, com as regras de `total` e de tipo (decisões 20 e 21), e as divergências que ela mostra, pela seção 2 (decisão 15); painel (`:83`): `🔄 EWM: <n> por fora · <m> divergências · <k> a conferir (<ids>) → sincroniza a sprint (sdd-planejamento)`; nada → `🔄 EWM: sem diferença na listagem (<n> itens)`; sem o MCP → `🔄 EWM: não conferido (sem o MCP elm)` |
| `sdd-fatiar/references/backlog.md` | **Volta** (`:102-106`): a `planejada` que sai da sprint também por movimento no EWM (§9), com as tarefas no backlog do EWM até ela voltar; **Épico** (`:117-137`): `elegivel` também do `planejado` que saiu da sprint; **Sustentação** (`:139-148`): `em-andamento`, `concluido` e `cancelado` também pela sincronização (tarefa conhecida que mudou de estado no EWM), e o item `aberto` que sai da sprint (`sprint` `—`, a linha com `saiu da sprint`); **Quem escreve o quê** (`:159`, `:162-163`): `status`, `sprint`, `responsavel` e `concluida-em` pela sincronização (§9) |
| `sdd-planejamento/references/arquivos.md` | Situações ao vivo (`:204-211`): a linha da Especificação que sai da sprint fica `elegivel`, e a da Sustentação fica `aberto`, as duas com `saiu da sprint`, como a da fatia; Observações (`:216-219`): `concluído no EWM`, `cancelado no EWM` e o motivo `movida no EWM para <iteração>` em `saiu da sprint` |
| `sdd-desenvolver/SKILL.md` | Passo 4, item 5 (`:151-155`): a fatia que saiu de uma sprint sem começar tem o IB e as tarefas no backlog do EWM — eles movem para a iteração da sprint antes do `assumir`, com o dono e a estimativa atuais, e só nasce o papel que falta (decisão 7a) |
| `sdd-especificar/SKILL.md` | Passo 1 (`:35-38`) e Passo 2 (`:45-48`): o épico `elegivel` pode ter a `[ESP]` no backlog do EWM (saiu de uma sprint sem começar): ela é a `[ESP]` da linha e move para a iteração da sprint, em vez de o épico contar como "sem `[ESP]`" |
| `sdd-atender/SKILL.md` · `sdd-executar/SKILL.md` | barreira do Passo 2 (`sdd-atender:42-44`) e do passo 1 (`sdd-executar:34-36`): a linha com `saiu da sprint` é item fora da sprint |
| `sdd-aprender/SKILL.md` | retrospectiva de sprint (`:84-85`): a pré-condição inteira — sincronização com o EWM e consolidação |
| `sdd/SKILL.md` | "Quero…" (`:148`): "trazer para a sprint o que mudou no EWM — tarefas por fora e divergências das conhecidas ('sincroniza a sprint')" |
| `sdd-setup/assets/steering/sdd.md` | `:52-53`: a sincronização traz a tarefa criada no EWM e compara as conhecidas (estado, iteração, dono, estimativa) |
| as 22 `*/SKILL.md` | `metadata.version` → `3.4.1` |
| `powers/sdd/plugin.json` | `version` → `3.4.1`; keyword `sincronizar com o ewm` |
| `powers/sdd/README.md` | entrada "Na **3.4.1**": a sincronização compara as conhecidas, a tabela única com a solução proposta, a linha de resultado nos ritos e no painel, a virada que move só o que está aberto no EWM e as tarefas que movem, em vez de nascer de novo, quando o item volta a uma sprint. Requer o `mcp-elm ≥ 3.3.5` (sem mudança no MCP) |

Não mudam: `mcps/elm` (decisão 17), `papeis.json` e os agentes, `sdd-iniciar` (a "minha próxima tarefa" já indica
a "sincroniza a sprint"), `sdd/references/elm.md` e `powers/README.md` (continuam 22 skills).

## 5. Ordem de execução e versões

1. `elm-sprint.md` §9, topo, §3, §4, §5 e §6 — a fonte das demais.
2. `backlog.md` e `arquivos.md`.
3. `sdd-planejamento/SKILL.md`, `sdd-status/SKILL.md`, `sdd-desenvolver/SKILL.md`, `sdd-especificar/SKILL.md`,
   `sdd-atender/SKILL.md`, `sdd-executar/SKILL.md`, `sdd-aprender/SKILL.md`, `sdd/SKILL.md` e
   `assets/steering/sdd.md`.
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
- **Título sem o prefixo** (decisão 11): o `elm_horas` classifica as horas pelo prefixo do título, então a tarefa
  com o título mantido sai sem prefixo no relatório — custo já aceito na 3.3.0.
- **`sdd-atender` e `sdd-executar` com a tarefa já concluída no EWM:** o `assumir` falha com `precondicao` ("já
  concluída: reabra antes", `ewm.py:527-528`), e a skill não diz o que fazer.
- **Troca de responsável da fatia com troca de modo:** não há fluxo (decisão 9).
- O mapa do GitHub Pages (branch `gh-pages`) está na 3.3.1, e o `mcps/elm/docs/manual-mcp-elm.md:96-107` segue atrás
  da mcp-elm 3.3.5 (já apontado na 3.4.0).

## 7. Verificação

- **Ensaio de mesa** do §9 novo, um caso por linha da seção 2, com a linha da tabela que cada um gera:
  - Sustentação: (a) `[ATD]` concluída com o AT `em-andamento`; (b) `[IMPL]` em andamento com o IM `aberto`;
    (c) `[ATD]` invalidada, e o `ELM pendente [AT-… cancelar]` quando o IB segue aberto; (d) `[IMPL]` com outro dono
    e outra estimativa → duas linhas;
  - estado de fatia e de épico: (e) `[ESP]` concluída com a Especificação `iniciada`; (f) `[DEV]` concluída com a
    fatia `iniciada`, nas duas soluções;
  - dono: (g) `[REV]` com um dono que não é Dev Sênior → o dono volta; (h) `[DEV]` de fatia AFK de um Sênior passada a
    um Júnior → o dono volta; (i) `[DEV]` de fatia HITL passada ao verificador dela → o dono volta;
  - saída: (j) IB de fatia `planejada` movido para o Backlog → sai da sprint com o P.O., e o IB e as tarefas no
    backlog do EWM; (k) `[DEV]` de fatia `iniciada` movida para outra sprint → volta; (l) só a `[REV]` de uma fatia
    `planejada` movida → a tarefa volta; (m) linha com Tarefa ELM `pendente` (planejamento sem o MCP) → `EWM:
    publicar`, nunca "sai da sprint";
  - entrada: (n) IB de fatia `elegivel` posto na iteração, com uma `[DEV]` feita à mão → uma linha só, encaixe, e a
    `[DEV]` não nasce de novo; recusado, tudo volta ao backlog; (o) IB de AT `aberto` sem sprint posto na iteração,
    com a `[ATD]` feita à mão → uma linha, e nenhuma `[ATD]` nova; (p) épico `elegivel` cuja `[ESP]` ficou no backlog
    (saiu de uma sprint) e volta → a `[ESP]` move, não nasce; (q) duas sprints numa iteração do EWM → nenhuma linha
    "entrou" para o que fechou na primeira;
  - listagem: (r) defeito na iteração e fora do `backlog.md` → triar; (s) impedimento na iteração → nenhuma linha;
    (t) tarefa por fora na mesma tabela; (u) pendência registrada não aparece; (v) `total` = 1000 → para;
  - ritos, virada e painel: (w) nada diverge → a linha de resultado na pré-condição da review, da retrospectiva
    (também pela `sdd-aprender`) e da virada; (x) virada com uma tarefa fechada no EWM, que fica, uma aberta, que
    muda de iteração, e o IB de um épico `iniciado` com a Especificação `concluida`, que também muda; (y) painel na
    sprint seguinte, com uma fatia migrada cuja `[REV]` fechou na anterior → nenhuma divergência; (z) painel com por
    fora e divergências, e "não conferido" sem o MCP.
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
- **Piloto:** a sprint de ensaio com os casos (a), (j), (n) e (x) feitos de verdade no EWM.
