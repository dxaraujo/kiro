# Arquivos do planejamento — `<produto>/planejamento/`

Todos versionados. Antes de gravar: `git pull --ff-only` (falhou → a branch local divergiu: peça à pessoa que a
atualize); mostre o diff e grave só com "ok".

## `equipe.json`

```json
{
  "atualizado": "2026-10-13",
  "projeto": {
    "nome": "Gestão de Acessos",
    "cadencia": "scrum",
    "duracao-sprint-semanas": 2,
    "inicio": "2026-10-06",
    "pontos-por-tamanho": { "P": 2, "M": 3, "G": 5 },
    "historico": [
      { "sprint": 1, "fatias-concluidas": 5, "pontos": 15, "lead-time-medio-dias": 3.2, "horas-revisao": 22 }
    ]
  },
  "membros": [
    {
      "nome": "Ana Souza",
      "login": "ana.souza",
      "papel": "P.O.",
      "horas-semana": 10,
      "horas-revisao-semana": 4,
      "ativo": true,
      "ausencias": [{ "inicio": "2026-12-20", "fim": "2027-01-05", "motivo": "férias" }]
    }
  ]
}
```

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
| WIP | 1 fatia por sessão de agente · revisão + PR aberto ≤ 2 por revisor · PR parado > 1 dia trava fatia nova |
| Tamanhos | P (horas) = 2 pts · M (≈ 1 dia) = 3 pts · G (2–3 dias) = 5 pts · maior → dividir |

## Definition of Ready (fatia)
- [ ] Cenários de aceite definidos no PRD aprovado (ou defeito com comportamento esperado claro)
- [ ] Nenhuma decisão bloqueante em aberto
- [ ] Dependências concluídas ou na mesma sprint antes dela
- [ ] Tamanho ≤ G · modo AFK/HITL declarado
- [ ] Cabe em uma janela de contexto: o agente consegue pesquisar, planejar e implementar sem perder o fio

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

| FT | Título | Tam. | Modo | Responsável | Status | Observação |
|---|---|---|---|---|---|---|
| FT-031 | Bloquear a conta após 3 tentativas | M | AFK | joao.lima | concluida | |
| FT-033 | Avisar o usuário do bloqueio | M | HITL | ana.souza | → sprint <nn+1> | aguardando texto do e-mail |

## Capacidade
Revisão: <h>h · HITL: <h>h · Vazão prevista: <n> fatias / <p> pts

## Review
<retorno do P.O. por fatia; pedidos novos → backlog>

## Retrospectiva
| Bom | Melhorar | Ação (dono) |
|---|---|---|

## Números
Concluídas: <n> fatias / <p> pts · lead time médio <d> dias · rodadas de revisão por fatia <x> · correções humanas <n>
```

A coluna Status espelha o `backlog.json` no fechamento; durante a sprint, o painel (`sdd-status`) é a fonte.
