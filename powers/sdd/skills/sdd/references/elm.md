# ELM — como o sdd grava

O ELM é o registro oficial: o que o sistema faz (DOORS Next), o que está sendo feito (EWM) e como foi testado (ETM).
O repositório guarda as propostas de mudança e o histórico. Quem fala com o ELM é o MCP **`elm`** do power: ele lê
o `.kiro/config/sdd/pa_<nome>.json` (um por project area; gravado pela `sdd-setup`) — tipos, campos, padrões,
pastas, ids. **A skill passa só `projeto` (caminho absoluto da raiz do repositório), `pa` (quando o projeto tem
mais de um) e os ids e o conteúdo.** Nunca repasse campos, URLs ou ids do `pa`: o MCP resolve.

Toda tool devolve `{"ok":true,"dados":{…}}` ou `{"ok":false,"erro":{"codigo","detalhe","campo"}}`; `elm_ler_wi` e
`elm_ler_req` devolvem Markdown. Os parâmetros de cada tool estão no schema dela — não os repita aqui.

## Operações

| Operação | Tool |
|---|---|
| conferir conexão e `pa` | `elm_status` |
| ler · listar work items | `elm_ler_wi(id)` · `elm_listar_wi(iteracao, dono, tipo, pai, titulo_prefixo, estado)` |
| criar · atualizar (pai, iteração, campos; vários ids = virada) | `elm_criar_wi` · `elm_atualizar_wi` |
| assumir · concluir · reabrir | `elm_transicao(id, alvo)` |
| comentar · anexos | `elm_comentar` · `elm_anexo(acao)` |
| horas lançadas · relatório da iteração · lançar · remover (lançamento errado) | `elm_horas(id)` · `elm_horas(iteracao)` · `elm_lancar_horas` · `elm_remover_horas(id, data)` |
| ligar (implementa, rastreia, afeta, testado por, valida, depende) | `elm_ligar` |
| buscar · ler · publicar requisito | `elm_buscar_req` · `elm_ler_req` · `elm_publicar_req` |
| criar caso de teste (já ligado) | `elm_criar_ct` |
| iteração e planos | `elm_iteracao` |
| bundle do DOORS Next | `elm_sync` (skill `elm-sync`) |

Erro `config` → o `pa` está incompleto: diga o campo e ofereça a `sdd-setup`. `credencial` → peça a configuração do
`~/.config/mcp-elm/elm.properties` (o agente não lê esse arquivo). `permissao`/`precondicao` → mostre o atributo;
não chute valor. Os campos que a PA exige por regra de processo (criar, mudar de estado, lançar horas) ficam em
`obrigatorios` do tipo no `pa` e são exigidos já na criação (`elm_criar_wi`), para as transições e as horas não
esbarrarem neles — Estimativa → pergunte e passe `estimativa_h`; outro campo sem padrão → ofereça a `sdd-setup`. Item
criado fora do fluxo recusado numa transição → mostre o campo e peça o valor.

## Regras de toda escrita

1. **Prévia e um "sim" por lote:** `Ação (criar | atualizar | ligar | sem mudança) | Alvo | Título`. Nada é escrito
   sem "sim". Mostre nomes, nunca ids internos (`FR_`, `OT_`, `_uuid`).
2. **Idempotência:** o repositório guarda o id (coluna `elm` do `backlog.md`, campo ELM do `status.md`, `resource`
   do conceito). Com id → atualizar o mesmo. Sem id → procure uma publicação interrompida: tarefa ou IB por
   `elm_listar_wi(pai, titulo_prefixo)` (`[DEV] FT-031`, `[FT-031]`, `[EP-03]`); requisito por `elm_buscar_req`
   (título). Achou → mostre e pergunte se é ele. Não achou → criar.
3. **Grave de volta** cada id assim que nasce (falha no meio: o próximo passo 2 retoma). Commit no fim.
4. **Nunca apague** nada no ELM: o que deixou de valer vira roteiro manual (obsoleto/remoção na UI).
5. **Conflito no DOORS Next:** `elm_publicar_req` com `modificado_em` devolve `conflito` se o ELM mudou depois →
   mostre os dois lados e pergunte qual fica.

## Pendências

Sem o MCP `elm` nesta sessão (pesquisador, outra máquina) ou com falha: não grave; registre
`ELM pendente [<chave>]: <o que falta>` no lugar único do artefato e siga — o ELM nunca trava o fluxo. A chave
identifica ação e alvo (`[DEV 669412 concluir]`, `[IB FT-031 concluir]`, `[REG-01 publicar]`, `[CT FT-031 criar]`,
`[DEV FT-031 horas]`); uma pendência por chave.

| Artefato | Onde mora |
|---|---|
| fatia | Histórico do `status.md` |
| épico | rodapé do `prd.md` (antes do GATE, o `rascunho.md`) |
| atendimento | campo `**ELM:**` do `AT-<nnn>-<slug>.md` |
| sprint | coluna "Tarefa ELM" do `sprint-<nn>.md` (`pendente`) |

Resolver ("resolve as pendências do ELM"): a `sdd-status` lista; para cada uma, faça a operação e acrescente
`ELM feito [<mesma chave>]: <o que foi feito> (<data>)` no mesmo lugar — a pendência nunca é apagada.

## Tarefas no EWM (quem, quando)

| Tarefa | Pai | Responsável | Nasce | Conclui |
|---|---|---|---|---|
| `[ESP] EP-<nn> Especificação` | épico | quem especifica | planejamento | GATE do backlog |
| `[DEV] FT-<nnn> Implementar` | IB da fatia | Dev | planejamento | merge |
| `[REV] FT-<nnn> Revisar` · `[VER] FT-<nnn> Verificar` | IB | revisor · verificador (só HITL) | planejamento ou troca AFK→HITL | aprovar · aceitar (depois do push) |
| `[APR] FT-<nnn> Aprovar plano` · `Aprovar PR` | IB | Dev Sênior | no gate | na aprovação |
| `[ATD] AT-<nnn> <pedido>` | IB `Atendimento` | quem atende | quando o AT entra na sprint | ao finalizar |
| `[GB] Gerenciamento do backlog` | épico de Sustentação | P.O. | 1ª sprint do ano | não conclui (move na virada) |

O `pa` aplica os campos que a PA exige (categoria, campos exigidos por processo, classificação por prefixo); `iteracao` é sempre a
da sprint. Assumir = `elm_transicao(id, "assumir")`; concluir = saldo de horas e `elm_transicao(id, "concluir")`.

## O que o MCP não grava (roteiro manual)

Atributos de requisito, links requisito ↔ requisito (*satisfaz*, *restringe*), módulos, change sets e baselines.
Quando o processo do projeto exigir (seção ELM do `sdd.md`), entregue o roteiro com os ids exatos e registre
`ELM pendente [<chave>]` até a pessoa confirmar.
