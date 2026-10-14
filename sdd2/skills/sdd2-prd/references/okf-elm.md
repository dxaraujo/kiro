# Artefatos do ELM em OKF v0.2

Cada artefato que vai para o DOORS Next — história (HF), regra (REG), termo (GL) — nasce como **um conceito OKF
v0.2** (Open Knowledge Format, [SPEC.md](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md),
versão 0.2) **na pasta da spec**, até ser aprovado e publicado. É o mesmo formato do bundle que a `elm-sync` mantém
no repositório, então o rascunho e a versão oficial se leem do mesmo jeito.

## Onde fica

| Origem | Pasta (um bundle OKF pequeno) |
|---|---|
| épico (PRD) | `.kiro/produto/epicos/<EP>-<slug>/elm/` |
| fatia de trilha rápida que muda documentação | `.kiro/specs/<ft>-<slug>/elm/` |

```
elm/
  index.md                       # catálogo (OKF §8), com okf_version: "0.2"
  log.md                         # histórico (OKF §9), entradas mais novas primeiro
  GL-tentativa-de-login.md
  REG-01-bloqueio-apos-3-tentativas.md
  HF-01-bloquear-conta.md
```

- **Nunca dentro do bundle da `elm-sync`** (`<rm.download.path>`): lá só o MCP grava, e um sincronismo regravaria
  ou apagaria o rascunho.
- O **Concept ID** do OKF (o caminho do arquivo dentro de `elm/`, sem `.md`) é a chave estável do artefato. Ele não
  muda depois de criado; o id do ELM fica em `resource`/`id`.
- Nome do arquivo: `HF-nn-<slug>.md`, `REG-nn-<slug>.md`, `GL-<termo-kebab>.md` — o rótulo local (`HF-01`) é o
  mesmo que o PRD e o backlog (`cobre`) usam.

## Frontmatter — só campos do OKF v0.2

```yaml
---
type: Regra                                   # REQUIRED (§4.1): o tipo do artefato no DOORS Next
title: REG - Bloqueio após 3 tentativas       # título no ELM
description: Após 3 tentativas inválidas em 15 minutos, a conta fica Bloqueada por 30 minutos.
tags: ["03-Regras"]                           # pasta de destino no RM — o mesmo uso que o bundle faz
status: draft                                 # §5.4: draft → stable (aprovado) → deprecated (obsoleto)
sources:                                      # §5.1: de onde o conteúdo veio
  - id: prd
    resource: ../prd.md
    title: PRD EP-03 — Bloqueio por tentativas de login
  - id: d-02
    resource: ../decisoes.md
    title: Decisão D-02
generated: { by: sdd2/0.1.0, at: 2026-10-14T13:00:00Z }   # §5.2: quem escreveu e quando mudou por último
---
```

| Campo (OKF v0.2) | Uso no sdd2 |
|---|---|
| `type` (obrigatório) | nome do tipo no DOORS Next — a chave em `rm.requirements-types` do `pa_*.json` (ex.: `História de Usuário`, `Regra`, `Termos de Glossário`) |
| `title` | título no ELM: `HF - <nome>`, `REG - <nome>`, o termo |
| `description` | uma frase; vai para o `index.md` |
| `tags` | `[<pasta do RM>]` — a chave em `rm.folders` |
| `resource` | **ausente até publicar**; depois, a URI do artefato no ELM. Decide criar × atualizar |
| `sources` | o PRD, as decisões e, numa alteração, o próprio artefato do ELM (`resource` = URI, `last_modified` = última modificação no ELM vista por nós) |
| `generated` | `by: sdd2/<versão do power>` (ator `<producer>/<version>`, §7); `at` = última mudança de conteúdo |
| `verified` | **aprovação no GATE**: `{ by: human:<login do P.O.>, at: <instante> }` (§5.2). Sem `verified` humano o conceito é *unverified* (§5.3) e **não é publicado** |
| `status` | `draft` enquanto não aprovado (obrigatório escrever: no OKF, ausência = `stable`), `stable` depois do GATE, `deprecated` quando deixa de valer |

**Uma extensão só** (OKF §4.1 permite chaves do produtor): `id` — o id numérico do DOORS Next, gravado na
publicação. É a mesma chave que o mcp-elm já grava no bundle, e a tool de atualização a exige. Copiado do bundle,
o arquivo mantém também as extensões que vierem dele (`created`, `links`): o OKF manda preservar chaves
desconhecidas. Nenhuma outra chave é inventada.

Mudou o conteúdo depois da aprovação → `generated.at` novo e `status: draft`. Só volta a publicar com um
`verified` humano **posterior** ao `generated.at` (a lista `verified` acumula as aprovações).

## Corpo e relações

O corpo é Markdown estrutural (§4.2). A relação entre conceitos é um **link Markdown** e o tipo da relação vem da
prosa (§6.1):

```markdown
**Como** usuário, **quero** ser avisado do bloqueio, **para** saber quando tentar de novo.

## Cenários
1.1 Bloquear após a terceira falha
**Dado que** …
**Conforme** a regra [REG-01 Bloqueio após 3 tentativas](REG-01-bloqueio-apos-3-tentativas.md)

## Regras
- [REG-01 Bloqueio após 3 tentativas](REG-01-bloqueio-apos-3-tentativas.md)

## Relações
- Satisfaz a necessidade [DV 1800 — Segurança de acesso](https://elm.exemplo/rm/resources/TX_…).
```

| Relação | No rascunho | Na publicação |
|---|---|---|
| HF → REG | link relativo para o arquivo da REG | **embed**: `[<id>](<id>)` e o id em `embedded` |
| HF/REG → termo | link relativo para o `GL-*.md` | hyperlink `[<id>](<id>)` |
| restringe, satisfaz, elabora (requisito ↔ requisito) | prosa + link na seção `## Relações` | **não sobe** (o MCP não cria esse link): fica no arquivo como registro |
| atributos (aprovação, prioridade) | `verified`, `status` | **não sobem** (o MCP não grava atributo) |
| conceito ainda sem id | link relativo | texto simples com o título |

A seção `## Relações` é só local. O resto do corpo é o texto publicado.

### Corpo por tipo

**História (HF)** — um comportamento observável:

```markdown
**Como** <ator>, **quero** <capacidade>, **para** <benefício>.

**Gatilho:** <ação na tela | chamada de API | agendamento | evento> · **Entradas:** <…> · **Pré-condições:** <…>

## Cenários
1.1 <caminho feliz>
**Dado que** <estado antes>
**Quando** <o ator faz X>
**Então** <efeito verificável: valor gravado, resposta, mensagem, contagem>
**Conforme** a regra [REG-01 <nome>](REG-01-<slug>.md)

1.2 <o que NÃO deve ser aceito/processado>
1.3 <repetição / reexecução: rodar de novo não duplica nem corrompe>
1.4 <erro em um item: a operação continua? o que fica registrado?>

## Regras
- [REG-01 <nome>](REG-01-<slug>.md)

## Relações
- <restringe / satisfaz / elabora, com link — só local>
```

**Regra (REG)** — um enunciado testável, com valores ("Após **3** tentativas inválidas em **15 minutos**, a conta
fica **Bloqueada** por **30 minutos**."), a origem como nota de rodapé ligada ao `sources` (`[^d-02]`) e, se
houver, `## Relações`.

**Termo (GL)** — a definição; `**Evitar:**` com os sinônimos que não devem ser usados.

## Ciclo de vida

| Momento | O que acontece |
|---|---|
| Rascunho | `sdd2-prd` (ou a fatia) cria o conceito com `status: draft`, `sources`, `generated` |
| GATE do PRD | a pessoa aprova → cada conceito recebe `verified` humano e `status: stable` |
| Publicação | `sdd2-elm` publica de baixo para cima (GL → REG → HF), grava `resource` e `id`, e acrescenta ao `sources` a entrada do ELM com o `last_modified` |
| Depois | a `elm-sync` baixa a versão oficial para o bundle, que passa a ser a versão viva; o rascunho fica como registro histórico, com `resource` preenchido |
| Alteração de artefato existente | copie o arquivo do bundle para `elm/`, mantendo `resource`, `id` e o `sources` do ELM; `status: draft`, `generated` novo; edite. Na publicação, `rm_list_modified` mais novo que o `last_modified` desse `sources` = alguém mudou no ELM no meio-tempo → **conflito**: a pessoa decide |
| Obsoleto | `status: deprecated`; a remoção ou a marcação no ELM é passo manual na UI |

## `index.md` e `log.md`

```markdown
---
okf_version: "0.2"
---
# Histórias
* [HF - Bloquear a conta após 3 tentativas](HF-01-bloquear-conta.md) - <description>

# Regras
* [REG - Bloqueio após 3 tentativas](REG-01-bloqueio-apos-3-tentativas.md) - <description>

# Termos
* [Tentativa de login](GL-tentativa-de-login.md) - <description>
```

`log.md`: `# Directory Update Log`, seções `## AAAA-MM-DD` (mais nova primeiro), itens `* **Creation**: …`,
`* **Update**: …`, `* **Publication**: … (ELM <id>)`, `* **Deprecation**: …`.

## Conformidade (conferida pela rubrica P, item P11)

1. Todo `.md` de `elm/` (fora `index.md` e `log.md`) tem frontmatter YAML que faz parse, com `type` não vazio.
2. Só chaves do OKF v0.2, mais `id` (e as que vieram do bundle numa cópia).
3. `status` presente; `draft` antes do GATE.
4. `type` e `tags` existem no mapeamento do projeto (`pa_*.json`, seção ELM do `sdd2-projeto.md`).
5. Toda HF tem cenários e liga as suas REGs; todo link relativo aponta para um arquivo que existe.
6. `index.md` lista todos os conceitos; `log.md` com datas `AAAA-MM-DD`.
