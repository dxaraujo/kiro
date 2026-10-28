# Arquivos do planejamento — raiz de `<produto>/`

Todos versionados. Antes de gravar: `git pull --ff-only` (falhou → a branch local divergiu: peça à pessoa que a
atualize); mostre o diff e grave só com "ok".

## `equipe.json`

Formato definido pelo JSON Schema [../assets/equipe.schema.json](../assets/equipe.schema.json) (fonte da verdade).
Ele fica dentro do power instalado, não no projeto: leia-o direto por esse caminho, relativo a esta pasta (busca no
workspace não o acha), e valide o JSON contra ele antes de mostrar. `$schema` é a primeira propriedade e é sempre a
URL abaixo, nunca um caminho local:

```json
{
  "$schema": "https://raw.githubusercontent.com/dxaraujo/kiro/main/powers/sdd/skills/sdd-planejamento/assets/equipe.schema.json",
  "atualizado": "2026-10-13",
  "projeto": {
    "nome": "Gestão de Acessos",
    "cadencia": "scrum",
    "duracao-sprint-semanas": 2,
    "inicio": "2026-10-06",
    "historico": [
      { "sprint": "2026/01", "fatias-concluidas": 5, "lead-time-medio-dias": 3.2, "horas-revisao": 22,
        "horas-lancadas": { "entrega": 120, "revisao": 18, "aprovacao": 4, "verificacao": 6, "especificacao": 24, "apoio": 9 },
        "reserva-apoio": 0.2 }
    ]
  },
  "membros": [
    {
      "nome": "Ana Souza",
      "login": "ana.souza",
      "papeis": ["P.O.", "Especificador"],
      "horas-semana": 10,
      "horas-revisao-semana": 4,
      "horas-especificacao-semana": 4,
      "atende": true,
      "ativo": true,
      "ausencias": [{ "inicio": "2026-12-20", "fim": "2027-01-05", "motivo": "férias" }]
    },
    {
      "nome": "João Lima",
      "login": "joao.lima",
      "papeis": ["Dev"],
      "senioridade": "Sênior",
      "horas-semana": 40,
      "horas-revisao-semana": 6,
      "atende": false,
      "ativo": true,
      "ausencias": []
    }
  ]
}
```

- Chaves em kebab-case, exatamente as do exemplo; nada além delas (o schema recusa `horasSemana`, `capacidade`…).
- `papeis` é uma lista com um ou mais de `P.O.`, `Especificador`, `Dev`, `QA` e `SM` (ex.: `["Dev", "QA"]`); as horas de
  revisão e de especificação já dizem quanto do tempo vai para cada frente. Exatamente **um** membro ativo tem `P.O.`.
- `senioridade` — `Júnior`, `Pleno` ou `Sênior` — é obrigatória em quem tem `Dev` (o schema recusa sem ela) e não
  existe nos demais. Decide o modo das fatias que a pessoa implementa (Júnior: sempre HITL · Pleno: pelos critérios da
  fatia · Sênior: AFK por padrão) e quem revisa PR: a `[REV]` é sempre de um Dev Sênior.
- `horas-revisao-semana` soma revisar (planos, PRs) e verificar (aceite) e é parte de `horas-semana`.
- `horas-especificacao-semana` (entrevista, PRD, fatiamento: tarefas `[ESP]`) também é parte de `horas-semana`;
  ausente = 0. Revisão + especificação nunca passam de `horas-semana`.
- `atende: true` marca quem faz Apoio (toda categoria: responsável sugerido na triagem); a reserva é das horas do time
  inteiro, não só dessas pessoas.
- `historico[].horas-lancadas` e `reserva-apoio` são gravados na virada (histórico antigo com `atendimento` e
  `reserva-atendimento` continua válido), com o relatório de horas ([elm-sprint.md](elm-sprint.md) §5).
- Capacidade da sprint e totais **não** são gravados: calcule na hora. `historico` fica dentro de `projeto`.
- `motivo` da ausência: `férias`, `folga`, `treinamento` ou `outro`.
- Exatamente um P.O. ativo. Quem sai fica `ativo: false` (preserva o histórico).
- Horas de uma sprint = `horas-semana × semanas` − ausências que caem nela (o mesmo para revisão).
- Sem dado pessoal além de nome e login.

## `acordos.md`

```markdown
# Acordos do time

| Item | Acordo |
|---|---|
| Cadência | Scrum, sprints de 2 semanas, fluxo puxado dentro da sprint |
| Cerimônias | planejamento (seg, 1h) · review (última qui, 30 min) · retrospectiva (última qui, 30 min) |
| WIP | 1 fatia por sessão de agente · revisão + PR aberto ≤ 2 por revisor · PR parado > 1 dia: destravar antes de fatia nova (exceção fica registrada: `WIP excedido`) |
| Tamanhos | P (horas) · M (≈ 1 dia) · G (2–3 dias) · maior → dividir (sem pontos; a previsão é pela vazão) |
| Reserva de apoio e retrabalho | 20% das horas da sprint do time, para o Apoio (toda categoria) e o retrabalho da sprint anterior (fatias migradas primeiro); na virada, o P.O. pode mudar o % olhando o consumido (muda aqui, com "ok") |
| Lançamento de horas | Cadência do time (padrão: ao fechar cada sessão de trabalho), em qualquer tarefa iniciada; na conclusão, só o saldo. Lançar não conclui |

## Definition of Ready (fatia)

A do fluxo, por trilha: [../../sdd-fatiar/references/backlog.md](../../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-pronta).
O time só acrescenta itens próprios aqui (ex.: "massa de teste disponível"), nunca afrouxa os de lá.

## Definition of Done (fatia)
- [ ] Plano aprovado (GATE do plano pela senioridade, ou plano do Sênior / Pleno que dispensou) e seguido; desvios registrados no design.md
- [ ] Backpressure verde: compilar, testes, lint, cobertura (gate do projeto)
- [ ] Revisão independente APROVADO
- [ ] Verificação de aceite ACEITO com evidência por cenário
- [ ] PR revisado e mergeado por uma pessoa
- [ ] ELM atualizado (requisitos, IB concluído, CTs ligados) ou pendência registrada
- [ ] Lições registradas
```

## `roadmap.md`

```markdown
# Roadmap — <projeto>

| Release | Objetivo | Épicos | Previsão |
|---|---|---|---|
| R1 | Bloquear abuso de login | EP-03, EP-04 | sprint 2026/03 (pela vazão média) |
| R2 | … | EP-05 (a descobrir) | — |
```

A previsão vem da vazão: `fatias restantes ÷ vazão média`, arredondando para cima, com a faixa (vazão mínima e
máxima das últimas sprints) quando houver histórico.

## `sprints/<pai>/sprint-<nn>.md`

A sprint acompanha a iteração do EWM de que ela é filha (estrutura padrão: `<linha de base>` → `2026` → `Sprint 01`, `Sprint 02`…;
`2027` → `Sprint 01`… — [elm-sprint.md](elm-sprint.md#estrutura-no-ewm-padrão)): `<pai>` é o nome da iteração pai (`2026`) e `<nn>` recomeça em `01` em cada pai — `sprints/2026/sprint-01.md`,
`sprints/2027/sprint-01.md`. A **chave** da sprint é `<pai>/<nn>` (`2026/03`): é ela que vai na coluna `sprint` do
`backlog.md`, em `historico[].sprint` do `equipe.json`, em `→ sprint <chave>` e `migrada da sprint <chave>`. Nas
skills, `sprint-<nn>.md` abrevia `sprints/<pai>/sprint-<nn>.md` e "sprint `<nn>`", a chave. A ordem das sprints é a
da data de início do cabeçalho (o nome do pai é livre e não ordena) — a do `historico`, que cruza pais na vazão. Kanban: o mesmo, com a iteração corrente.

```markdown
# Sprint <pai>/<nn> · <AAAA-MM-DD> → <AAAA-MM-DD>

**Meta:** <resultado de negócio>
**Iteração no EWM:** <pai>/<nome> | —   (o caminho que o `elm_iteracao` recebe: `2026/Sprint 03`)
**Plano no EWM:** <nome> - <nome curto da meta>   (o `plano` do `elm_iteracao`: `Sprint 03 - Exportar o relatório de contas`)
**Power sdd:** <versões usadas, crescente: 2.9.0 · 2.9.1>   (o planejamento grava a da abertura; a virada acrescenta as das linhas de créditos)
**Situação:** <aberta | fechada>   (a virada grava `fechada`; o painel usa a última `aberta`)
**Fechamento sem consolidar:** <FT-… (<P.O.>, <data>)>   (só quando o P.O. decide fechar com fatia mergeada sem consolidação)

## Fatias

| FT | Título | Tam. | Modo | Responsável | Revisor | Verificador | Status | Tarefa ELM | Créditos | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas | M | AFK | joao.lima | — | — | concluida | DEV 669401 | 41.20 | |
| FT-033 | Avisar o usuário do bloqueio | M | HITL | ana.souza | joao.lima | rita.melo | → sprint <próxima chave> | DEV 669410 · REV 669411 · VER 669412 | — | aguardando texto do e-mail |
| FT-034 | Corrigir o texto do e-mail | P | — | joao.lima | — | — | concluida | DEV 669420 | 6.75 | puxada |

## Especificação

| EP | Responsável | Horas previstas | Situação | Tarefa ELM | Créditos |
|---|---|---|---|---|---|
| EP-05 | rita.melo | 16 | PRD | 669377 | — |

## Apoio

Reserva (apoio + retrabalho): <h>h · consumido: <h>h · retrabalho migrado: <h>h

| Id | Categoria | Pedido | Origem | Responsável | Horas | Tarefa ELM | Situação | Créditos | Observação |
|---|---|---|---|---|---|---|---|---|---|
| AT-012 | Atendimento | Extração de contas bloqueadas em setembro | chamado 4521 | joao.lima | 3 | ATD 669380 | concluido | 3.12 | |
| IM-003 | Implantação | Subir a versão 1.4 em produção | EWM 670215 | ana.souza | 4 | IMPL 670215 | aberto | — | trazida do EWM |

## Créditos de gestão

| Data | Atividade | Login | Sessão Kiro | Power sdd | Créditos |
|---|---|---|---|---|---|
| 2026-10-06T10:41:12 | planejamento | ana.souza | 9ec1dcaa | 2.9.0 | 2.40 |

## Capacidade
Revisão: <h>h · HITL: <h>h · Especificação: <h>h · Reserva (apoio + retrabalho): <h>h · Vazão prevista: <n> fatias (previsão; o compromisso é a meta)

## Review
<retorno do P.O. por fatia; pedidos novos → backlog>

## Retrospectiva
| Bom | Melhorar | Ação (dono) |
|---|---|---|

## Números
Concluídas: <n> fatias (<p> previstas · <q> puxadas) · meta: <atingida | não — por quê> · lead time médio <d> dias · rodadas de revisão por fatia <x> · correções humanas <n>

| Tipo | Planejadas (h) | Lançadas (h) | Créditos |
|---|---|---|---|
| Entrega `[DEV]` | | | <Fatias: todos os papéis> |
| Revisão `[REV]` | | | ↑ |
| Aprovação `[APR]` | | | ↑ |
| Verificação `[VER]` | | | ↑ |
| Especificação `[ESP]` | | | |
| Apoio — Atendimento `[ATD]` | | | |
| Apoio — <categoria> `<prefixo>` (uma linha por categoria com horas) | | | |
| Gestão `[GB]` | — | | |
| **Total** | | | |

Créditos por fatia concluída: <média> · por versão do power sdd: <versão> <x> · …
```

Situação da especificação: `entrevista`, `PRD`, `fatiamento`, `concluida` ou `→ sprint <próxima chave>`. Situação do
Apoio: `aberto`, `concluido` ou `→ sprint <próxima chave>`. "Tarefa ELM" é o id da tarefa no EWM, ou `pendente`
(nas fatias, as tarefas com prefixo — `DEV <id> · REV <id> · VER <id>`, mais `APR <id>` das aprovações criadas no
gate; AFK, a `DEV` e as `APR`), gravada na publicação da sprint ([elm-sprint.md](elm-sprint.md) §4; e pela `sdd-consolidar` na fatia puxada). Observação: `puxada`, `encaixe: <decisão>
(<quem>, <data>)`, `modo: AFK → HITL (<quem>, <data>, <motivo>)`, `modo: AFK mantido (<quem>, <data>)`, `migrada da sprint <chave>`, `trazida do EWM`, `não consolidada` ou texto livre.

Créditos (do Kiro): nas Fatias, Especificação e Apoio, a soma das linhas de créditos do item, gravada na
conclusão dele (`sdd-consolidar`, `sdd-especificar`, `sdd-atender`, `sdd-executar`), `—` antes; em Créditos de gestão, uma linha por
sessão de triagem, consolidação, planejamento ou retrospectiva (`sdd-status`, Fechar a sessão, item 4).

A coluna Status espelha o `backlog.md` do produto no fechamento; durante a sprint, o painel (`sdd-status`) é a fonte.
