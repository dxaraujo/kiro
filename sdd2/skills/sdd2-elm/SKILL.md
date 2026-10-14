---
name: sdd2-elm
description: "Alimenta o IBM ELM (sistema de registro da documentação do projeto) a partir dos artefatos do fluxo sdd2, pelo power elm — modo requisitos (histórias, regras e termos do PRD aprovado no DOORS Next, de baixo para cima, idempotente por chave estável e hash, alteração do artefato existente em vez de duplicar), modo backlog (épico e itens de backlog das fatias no EWM, ligados às histórias por implementa/rastreia), modo sprint (iteração, tarefas filhas, responsáveis, virada), modo testes (CT.csv para o ETM e links valida/testado por), modo especificação técnica (ET as-built) e modo conclusão (estados). Sempre mostra a prévia e pede confirmação; o que o MCP não faz vira roteiro manual com pendência registrada. Use em \"publica no ELM\", \"sobe o PRD para o DOORS\", \"cria os itens no EWM\", \"publica a sprint\", \"liga os testes\", \"fecha no ELM\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-elm — O ELM como fonte oficial

Requer o power **`elm`** (MCP `elm`) nesta sessão e as skills dele: **`elm-rm`** (DOORS Next), **`elm-ccm`**
(EWM), **`elm-qm`** (ETM — ler o caso de teste importado para obter a URL), **`elm-gc`** (links) — carregue a skill
da área antes de chamar as tools. Ids da project area:
`.kiro/config/power/elm/pa_*.json`. Tipos, pastas, prefixos e regras do projeto: seção **ELM** do
`.kiro/steering/sdd2-projeto.md`. Mapeamento e limites: [references/mapeamento.md](references/mapeamento.md).

**Sem o MCP `elm` nesta sessão** (agentes, kiro-cli, outra máquina): não publique. Registre `ELM pendente:
<modo> <alvo>` no Histórico do `status.md` (fatia) ou no rodapé do PRD (épico) e siga — o ELM nunca trava o fluxo.
Projeto sem ELM (`sdd2-projeto.md` → ELM: não usa) → nada a fazer.

## Regras de toda publicação

1. **Prévia antes de escrever:** tabela `Ação (criar | atualizar | ligar | sem mudança) | Alvo | Título | Tipo/Pasta`
   e **uma** confirmação para o lote. Nada é escrito sem "sim".
2. **Idempotência:** cada artefato tem uma chave local (`EP-03/HF-01`, `FT-031`). Antes de criar:
   - o repositório já tem o id (frontmatter `elm` do PRD, `backlog.json`, `status.md`) → **atualizar** o mesmo id,
     só se o hash local mudou;
   - não tem → procure pela chave (`rm_search_requirements(text="Chave sdd2: <chave>")`; no EWM, pelo título com
     `[FT-031]`) — achou → grave o id e trate como atualização (publicação anterior interrompida);
   - não achou → criar.
3. **Conflito:** o artefato mudou no ELM depois da nossa última publicação (`rm_list_modified` > `publicado-em`
   gravado) → mostre os dois lados e **pergunte** qual fica. Nunca sobrescreva mudança feita no ELM sem "sim".
4. **Grave de volta** no repositório, a cada item publicado: id, url, hash, `publicado-em`. Commit ao final
   (`<FT|EP> - Publicar no ELM`). Falha no meio → os já publicados ficam registrados; rode de novo (o passo 2
   retoma).
5. Mostre nomes de tipo, pasta e iteração — nunca `FR_`/`OT_`/uuids.
6. Nunca apague nada no ELM. Artefato que deixou de valer → peça à pessoa a marcação de obsoleto/remoção do módulo
   na UI (roteiro manual).

## Modo requisitos (PRD → DOORS Next)

Pré-condição: PRD `aprovado` (ou `fatiado`/`concluido` numa republicação). Publicar **não** muda o status do PRD:
fica registrado no frontmatter `elm`. Ordem **de baixo para cima**, para cada
artefato nascer com os ids dos que ele cita:

1. **Termos** novos do glossário (coluna ELM `—`) → tipo de termo; título = o termo; texto = definição + "Evitar".
2. **Regras** `REG-nn` → título `REG - <nome>`; texto = o bloco da regra.
3. **Histórias** `HF-nn` → título `HF - <nome>`; texto = o bloco da história, com as referências locais trocadas:
   `REG-01` → embed `[<id>](<id>)` (e o id em `embedded`); termos → hyperlink `[<id>](<id>)`.
   História com `Altera: <id>` → **atualização** daquele id: leia-o (`rm_get_requirement`), mostre o diff do corpo
   e mande o texto inteiro novo com o `embedded` correto.
4. Todo texto termina com a linha de chave (formato em `mapeamento.md`).

O texto vai em **Markdown** direto (`rm_create_requirement` / `rm_update_requirement` convertem). Depois:
frontmatter `elm` do PRD com `{id, url, hash, publicado-em}` por chave e o `publicado-em` geral; glossário com o
id na coluna ELM (commits na base, como todo artefato de produto). Roteiro manual se o projeto exigir (change set, módulo, links *restringe*, atributos).
Bundle do ELM no repositório → sugira a `elm-sync` para baixar o que foi publicado.

## Modo backlog (fatias → EWM)

Quando: `Backlog no EWM` = `ao-fatiar` (logo após o GATE do backlog) ou `na-sprint` (só as fatias da sprint, no
modo sprint).

1. **Épico** (se não tem `elm`): tipo do `sdd2-projeto.md`, título `[EP-03] <título>`, descrição = problema +
   solução do PRD + link do PRD no repositório; links **rastreia** → histórias publicadas.
2. **Item de backlog por fatia:** título `[FT-031] <título>`, `parent` = épico, pontos pelo tamanho (tabela do
   `sdd2-projeto.md`), descrição com: cenários cobertos (texto), modo AFK/HITL, `bloqueada por`, pasta prevista;
   responsável = P.O. (o IB é do produto). Links **implementa** → cada história que a fatia cobre; **depende de** →
   IBs das fatias em `bloqueada-por` (se o `link-types` tiver; senão fica na descrição).
3. `backlog.json` (na base): `elm` de cada fatia/épico.

## Modo sprint (planejamento → iteração)

Entrada da `sdd2-planejamento`: número da sprint, iteração, plano e time confirmados, fatias da sprint.

1. Iteração/plano inexistentes → ofereça criá-los pela `elm-setup` (exige a permissão de modificar iterações na
   PA; as tools de criação usam serviços internos do EWM — se falharem, peça a quem administra a PA).
2. Fatias sem IB → modo backlog primeiro. Para cada IB da sprint: `plannedFor` = iteração (o planejamento é de
   quem planeja; o responsável continua o P.O.).
3. **Tarefas** filhas pelo template do `sdd2-projeto.md` (ex.: `[DEV] FT-031 Implementar`, `[VER] FT-031
   Verificar`), com responsável e estimativa em horas se o planejamento informou.
4. **Virada:** IBs/tarefas não concluídos da sprint que fechou → `plannedFor` da nova (move, nunca recria);
   roteiro manual de **baseline** (componente RM + GC) se o projeto exige baseline por sprint.

## Modo testes (verificação → ETM)

1. Entregue o caminho do `CT.csv` de cada fatia: `Importe no ETM (Importar → CSV)`. Pergunte os ids criados.
2. Com os ids: leia cada caso pela `elm-qm` (`get_testartifact`) para obter a URL, depois ligue **valida** (CT →
   história coberta pelo cenário) e **testado por** (IB → CT). `gc_context` se o ETM usar configuração global
   (`elm-gc`).
3. Registre os ids no `verificacao.md` e no `status.md`.

## Modo especificação técnica (opcional, as-built)

Só se o `sdd2-projeto.md` disser `ET: publicar no merge`. Gere `ET - FT-031 <título>` a partir do `design.md` e do
código **final** (interfaces, contratos, dados, integrações, decisões técnicas — nada do que não foi feito),
mostre, publique como os requisitos (chave `FT-031/ET`), e ligue ao IB (**implementa**).

## Modo conclusão

Tarefas e IB da fatia → estado de conclusão da PA (ação de `ccm_list_workitem_states`); épico quando todas as
fatias concluírem. Comentário opcional no IB: PR, pasta e ids publicados.

## Saída

```
🏛️ ELM — <modo> · <EP | FT | Sprint N>
Criados: <n> · Atualizados: <n> · Sem mudança: <n> · Links: <n> · Conflitos: <n resolvidos>
Pendências manuais: <lista | nenhuma>
```
