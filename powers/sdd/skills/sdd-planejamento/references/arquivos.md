# Arquivos do planejamento — `<produto>/planejamento/`

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
      { "sprint": 1, "fatias-concluidas": 5, "lead-time-medio-dias": 3.2, "horas-revisao": 22,
        "horas-lancadas": { "entrega": 120, "revisao": 18, "verificacao": 6, "especificacao": 24, "atendimento": 9 },
        "reserva-atendimento": 0.2 }
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
    }
  ]
}
```

- Chaves em kebab-case, exatamente as do exemplo; nada além delas (o schema recusa `horasSemana`, `capacidade`…).
- `papeis` é uma lista com um ou mais de `P.O.`, `Especificador`, `Dev`, `QA` e `SM` (ex.: `["Dev", "QA"]`); as horas de
  revisão e de especificação já dizem quanto do tempo vai para cada frente. Exatamente **um** membro ativo tem `P.O.`.
- `horas-revisao-semana` soma revisar (planos, PRs) e verificar (aceite) e é parte de `horas-semana`.
- `horas-especificacao-semana` (entrevista, PRD, fatiamento: tarefas `[ESP]`) também é parte de `horas-semana`;
  ausente = 0. Revisão + especificação nunca passam de `horas-semana`.
- `atende: true` marca quem atende demandas (`[ATD]`: responsável sugerido na triagem); a reserva é das horas do time
  inteiro, não só dessas pessoas.
- `historico[].horas-lancadas` e `reserva-atendimento` são gravados na virada, com o relatório da `sdd-elm` modo
  *horas*.
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
| Reserva de atendimento e retrabalho | 20% das horas da sprint do time, para atendimentos e retrabalho da sprint anterior (fatias migradas primeiro); na virada, o P.O. pode mudar o % olhando o consumido (muda aqui, com "ok") |
| Lançamento de horas | Cadência do time (padrão: ao fechar cada sessão de trabalho), em qualquer tarefa iniciada; na conclusão, só o saldo. Lançar não conclui |

## Definition of Ready (fatia)

A do fluxo, por trilha: [../../sdd-fatiar/references/backlog.md](../../sdd-fatiar/references/backlog.md#definition-of-ready-o-que-faz-uma-fatia-pronta).
O time só acrescenta itens próprios aqui (ex.: "massa de teste disponível"), nunca afrouxa os de lá.

## Definition of Done (fatia)
- [ ] Plano aprovado (GATE do plano) e seguido; desvios registrados no design.md
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
| R1 | Bloquear abuso de login | EP-03, EP-04 | sprint 3 (pela vazão média) |
| R2 | … | EP-05 (a descobrir) | — |
```

A previsão vem da vazão: `fatias restantes ÷ vazão média`, arredondando para cima, com a faixa (vazão mínima e
máxima das últimas sprints) quando houver histórico.

## `sprints/sprint-<nn>.md`

```markdown
# Sprint <nn> · <AAAA-MM-DD> → <AAAA-MM-DD>

**Meta:** <resultado de negócio>
**Iteração no EWM:** <nome | —>
**Situação:** <aberta | fechada>   (a virada grava `fechada`; o painel usa a última `aberta`)

## Fatias

| FT | Título | Tam. | Modo | Responsável | Revisor | Verificador | Status | Tarefa ELM | Observação |
|---|---|---|---|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas | M | HITL | joao.lima | ana.souza | ana.souza | concluida | DEV 669401 · REV 669402 · VER 669403 | |
| FT-033 | Avisar o usuário do bloqueio | M | HITL | ana.souza | joao.lima | rita.melo | → sprint <nn+1> | DEV 669410 · REV 669411 · VER 669412 | aguardando texto do e-mail |
| FT-034 | Corrigir o texto do e-mail | P | — | joao.lima | — | — | concluida | DEV 669420 | puxada |

## Especificação

| EP | Responsável | Horas previstas | Situação | Tarefa ELM |
|---|---|---|---|---|
| EP-05 | rita.melo | 16 | PRD | 669377 |

## Atendimento

Reserva (atendimento + retrabalho): <h>h · consumido: <h>h · retrabalho migrado: <h>h

| AT | Pedido | Origem | Responsável | Horas | Tarefa ELM | Situação |
|---|---|---|---|---|---|---|
| AT-012 | Extração de contas bloqueadas em setembro | chamado 4521 | joao.lima | 3 | 669380 | concluido |

## Capacidade
Revisão: <h>h · HITL: <h>h · Especificação: <h>h · Reserva (atendimento + retrabalho): <h>h · Vazão prevista: <n> fatias (previsão; o compromisso é a meta)

## Review
<retorno do P.O. por fatia; pedidos novos → backlog>

## Retrospectiva
| Bom | Melhorar | Ação (dono) |
|---|---|---|

## Números
Concluídas: <n> fatias (<p> previstas · <q> puxadas) · meta: <atingida | não — por quê> · lead time médio <d> dias · rodadas de revisão por fatia <x> · correções humanas <n>

| Tipo | Planejadas (h) | Lançadas (h) |
|---|---|---|
| Entrega `[DEV]` | | |
| Revisão `[REV]` | | |
| Verificação `[VER]` | | |
| Especificação `[ESP]` | | |
| Atendimento `[ATD]` | | |
```

Situação da especificação: `entrevista`, `PRD`, `fatiamento`, `concluida` ou `→ sprint <nn+1>`. Situação do
atendimento: `aberto`, `concluido` ou `→ sprint <nn+1>`. "Tarefa ELM" é o id da tarefa no EWM, ou `pendente`
(nas fatias, as tarefas com prefixo — `DEV <id> · REV <id> · VER <id>`; AFK e direta, só a `DEV`), gravada pela
`sdd-elm` modo *sprint* (e pela `sdd-consolidar` na fatia puxada). Observação: `puxada`, `encaixe: <decisão>
(<quem>, <data>)`, `migrada da sprint <nn>` ou texto livre.

A coluna Status espelha o `backlog.md` do produto no fechamento; durante a sprint, o painel (`sdd-status`) é a fonte.
