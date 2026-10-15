# Validação e verificação das skills do power `sdd` (v2.3.0)

> Gerado em 2026-10-15 sobre o commit `3b727bd` de `powers/sdd/` (19 skills `sdd-*`). Só leitura: nada no
> power foi alterado.

## Objetivo

Validar se o fluxo de desenvolvimento proposto pelo power `sdd` é coeso, com fluxos bem definidos, e se a execução
literal das regras produz o que foi proposto, inclusive os arquivos que cada fluxo grava.

## Método

| Parte | Quem executou | Entrada | Saída |
|---|---|---|---|
| 1 · Mapeamento dos fluxos | orquestrador (Opus) | README, guia `sdd`, os 19 `SKILL.md`, templates de agentes | mapa macro, handoffs, máquinas de estado, achados transversais (O1–O6) |
| 2 · Plano do fluxo esperado | 5 agentes Sonnet, um por grupo de skills | `SKILL.md` + `references/` + `assets/` | um item por fluxo: gatilho → processamento → resultado, com lacunas |
| 3 · Teste do Quarto Chinês | 5 agentes Haiku, executor mecânico | o plano da Parte 2 + o texto das regras, sem conhecimento externo | por fluxo: input exato → regra aplicada (arquivo:linha) → output, com veredito |
| 4 · Persistência e artefatos | 5 agentes Sonnet | Partes 2 e 3 + templates, schemas e permissões dos agentes | por arquivo: diretório, formato, estrutura, sucesso, diretório inacessível; confirma ou refuta a Parte 3 |
| 5 · Consolidação | orquestrador (Opus) | Partes 1–4 + conferência na fonte | matriz por skill, achados priorizados e verificados |

Grupos: G1 = S01 `sdd`, S02 `sdd-setup`, S03 `sdd-status` · G2 = S04 `sdd-triar`, S05 `sdd-iniciar`,
S06 `sdd-atender`, S07 `sdd-entrevistar` · G3 = S08 `sdd-prd`, S09 `sdd-fatiar`, S10 `sdd-planejamento`,
S11 `sdd-elm` · G4 = S12 `sdd-pesquisar`, S13 `sdd-plano`, S14 `sdd-implementar`, S15 `sdd-revisar` ·
G5 = S16 `sdd-verificar`, S17 `sdd-consolidar`, S18 `sdd-aprender`, S19 `sdd-loop`.

**Vereditos da Parte 3:** `DETERMINÍSTICO` (uma só saída possível) · `AMBÍGUO` (a regra admite duas leituras) ·
`SEM REGRA` (o input não tem regra que o trate) · `CONFLITO` (duas regras mandam coisas diferentes).
**Vereditos da Parte 4:** `OK` · `DIVERGENTE` · `NÃO ESPECIFICADO`.

**Como ler as citações:** `arquivo:linha` relativo a `powers/sdd/skills/`. Os agentes abreviam alguns nomes
(ex.: `SV` = `sdd-verificar/SKILL.md`, `tmpl` = `sdd-iniciar/references/status-template.md`); cada grupo traz a
legenda no Anexo A.

**Limites:** é uma simulação sobre o texto. Nenhuma conversa real com o Kiro foi executada, e nenhum ELM, banco ou
repositório de projeto foi tocado. O executor da Parte 3 (Haiku) erra às vezes. A Parte 4 refuta esses erros, e
os achados da Parte 5 marcados **CONFIRMADO** foram conferidos pelo orquestrador direto na fonte.

> Nota de execução: a primeira rodada da Parte 2 foi interrompida por limite de uso. Os grupos G1, G2, G3 e G5
> já tinham gravado o arquivo completo, e o G4 foi retomado do ponto em que parou. Nenhum conteúdo foi perdido.

## Parte 1 — Mapeamento dos fluxos de trabalho (orquestrador · Opus)

### 1.1 Mapa macro

```
             ┌──────────── configuração (uma vez) ────────────┐
             │ S02 sdd-setup → .kiro/steering/sdd.md, agentes,│
             │ hook, workflows, http.sh, pasta do produto     │
             └────────────────────────┬───────────────────────┘
                                      ▼   (toda skill: "sem sdd.md → ofereça a sdd-setup e pare")
ENTRADA   S04 sdd-triar ──┬─ épico ─────────► EP-nn rascunho ──► S08 sdd-prd
          (base, não      ├─ padrão s/ épico ► FT + ficha (P.O. aprova)  ┐
           começa nada)   ├─ rápida/direta ──► FT sem épico              ├─► backlog.md (base)
                          ├─ não fazer ──────► comentário no EWM         │
                          └─ atendimento ────► S06 sdd-atender ──► AT-nnn, [ATD], resposta, horas
PRODUTO   S08 sdd-prd ─(S07 entrevistar, S11 elm similares, S15 revisar P)─► GATE PRD
            └► S11 elm requisitos (na-aprovacao) ─► S09 sdd-fatiar ─► GATE backlog ─► [ESP] horas
          S10 sdd-planejamento: inicial (equipe/acordos/roadmap) · sprint · encaixe · review · virada
FATIA     S05 sdd-iniciar (DoR, sprint/encaixe, WIP, branch, status.md, [DEV] no EWM)
            ├─ padrão/rápida: S12 pesquisar → S13 plano (S15 revisar L) → GATE plano
            │                  → S14 implementar (TDD, S15 revisar C) → S16 verificar → PR
            └─ direta: S14 "Trilha direta" (teste→mudança→S15 C sobre o diff→PR curto)
          S19 sdd-loop: o mesmo, por subagentes, para lotes AFK em worktrees (.kiro/local/wt/<ft>)
DEPOIS    merge (pessoa) → S17 sdd-consolidar (drift, ELM as-built, CT→ETM, horas, ADR, glossário,
            backlog concluida) → S18 sdd-aprender (lições, regras, retrospectiva)
TRANSVERSAL  S03 sdd-status (painel / fechar sessão) · S11 sdd-elm (9 modos) · S01 sdd (guia/roteador)
```

### 1.2 Catálogo das skills (numeração usada no documento)

| # | Skill | Raia | Agente que a carrega (template da setup) | Escreve em |
|---|---|---|---|---|
| S01 | `sdd` | guia | nenhum (sessão padrão) | — |
| S02 | `sdd-setup` | configuração | nenhum (sessão padrão) | `.kiro/steering`, `.kiro/agents`, `.kiro/hooks`, `.kiro/workflows`, `.kiro/sdd`, `<produto>/` |
| S03 | `sdd-status` | transversal | `sdd-orquestrador` | só `status.md`/`tasks.md` ao fechar sessão |
| S04 | `sdd-triar` | entrada | `sdd-produto` | `backlog.md`, `fatias/FT-*.md` (base) |
| S05 | `sdd-iniciar` | fatia | `sdd-orquestrador` | branch, `.kiro/specs/<ft>-<slug>/status.md`, `.config.kiro` |
| S06 | `sdd-atender` | entrada | `sdd-produto` | `atendimentos/`, `sprint-<nn>.md` (base); `.kiro/local/atendimentos/` |
| S07 | `sdd-entrevistar` | produto | `sdd-produto` | `decisoes.md`, ficha (Decisões), glossário (base) |
| S08 | `sdd-prd` | produto | `sdd-produto` | `epicos/<EP>-<slug>/` (`prd.md`, `decisoes.md`, `elm/`) |
| S09 | `sdd-fatiar` | produto | `sdd-produto` | `backlog.md`, `prd.md` |
| S10 | `sdd-planejamento` | produto | `sdd-produto` | `planejamento/` (`equipe.json`, `acordos.md`, `roadmap.md`, `sprints/`) |
| S11 | `sdd-elm` | transversal | `sdd-produto`, `sdd-codificador`, `sdd-orquestrador` | ELM + write-back em `elm/`, `backlog.md`, `status.md` |
| S12 | `sdd-pesquisar` | fatia | `sdd-pesquisador` | `research.md` |
| S13 | `sdd-plano` | fatia | `sdd-codificador` | `requirements.md`/`bugfix.md`, `design.md`, `tasks.md` |
| S14 | `sdd-implementar` | fatia | `sdd-codificador` | código, testes, `tasks.md`, `status.md`, PR |
| S15 | `sdd-revisar` | fatia/produto | `sdd-revisor` | `revisao-prd-<N>.md`, `analise-plano-<N>.md`, `revisao-codigo-<N>.md`, `.kiro/local/wf/<id>/*.json` |
| S16 | `sdd-verificar` | fatia | `sdd-verificador` | `verificacao.md`, `CT.csv`, `massa/`, `evidencias/` |
| S17 | `sdd-consolidar` | depois | **nenhum** (sessão padrão) | ADRs, glossário, `backlog.md`, `status.md` (base) |
| S18 | `sdd-aprender` | depois | **nenhum** (sessão padrão) | `aprendizado/licoes.md`, `sdd.md` (Regras aprendidas), `aprendizado/avaliacoes/` |
| S19 | `sdd-loop` | fatia (lote) | `sdd-orquestrador` | `.kiro/local/loop-<data>.md`, worktrees |

### 1.3 Passagens (handoffs) entre skills

| De | Para | Gatilho | O que passa (em disco) |
|---|---|---|---|
| S04 triar | S08 prd | trilha épico + "especificar agora" | linha `EP-nn rascunho`, `prd —` |
| S04 triar | S05 iniciar | fatia `pronta` + "começar agora" | linha `FT-nnn` + ficha (na base, publicada) |
| S04 triar | S06 atender | trilha atendimento | o pedido (nada gravado) |
| S06 atender | S04 triar | defeito encontrado | `origem AT-nnn` |
| S08 prd | S07 entrevistar | Passo 2 | `decisoes.md` do épico |
| S08 prd | S11 elm *similares* → *requisitos* | Passo 3.1 · após o GATE | conceitos OKF `elm/*.md` com `verified` humano |
| S08 prd | S09 fatiar | após o GATE | `prd.md status: aprovado` |
| S09 fatiar | S10 planejamento | GATE do backlog | fatias `pronta` |
| S05 iniciar | S10 planejamento (Encaixe) | fatia fora da sprint aberta | decisão do P.O. no `sprint-<nn>.md` |
| S05 iniciar | S13 plano / S14 / S16 | pela `fase` do `status.md` | pasta da fatia |
| S13 plano | S12 pesquisar | sem `research.md` | `research.md` |
| S13 plano | S15 revisar (L) | Passo 4 | `analise-plano-<N>.md` → `ANALISE: OK/AJUSTAR` |
| S13 plano | S14 implementar | GATE do plano | `fase: implementando` |
| S14 implementar | S15 revisar (C) | Passo 3 | `revisao-codigo-<N>.md` → `VEREDITO` |
| S14 implementar | S16 verificar | Passo 4 | `verificacao.md` → `ACEITO/REJEITADO` |
| S16 verificar | S14 implementar | ACEITO (abrir PR) · REJEITADO (achados) | `fase: aceita` · achados no `status.md` |
| S14 implementar | S17 consolidar | PR mergeado (pessoa) | `fase: pr-aberto` + merge |
| S17 consolidar | S18 aprender | correções humanas da fatia | `licoes.md` |
| S13/S14/S17 | S04 triar · S08 prd | lacuna/drift de negócio | ficha (sem épico) · PRD nova versão |
| S19 loop | S12–S16 (subagentes) | `AUTONOMO=true` por fase | worktree + `status.md` |

### 1.4 Máquinas de estado (fonte: templates e `references/`)

```
Fatia (status.md, branch da fatia)
  pesquisando → planejando → plano-em-revisao → implementando → revisando → verificando → aceita → pr-aberto → concluida
  direta: implementando → … → pr-aberto       desvio: bloqueada (de: <fase>) → volta à fase de origem
  WIP de revisão humana = plano-em-revisao + aceita + pr-aberto

Fatia (backlog.md, base)       backlog ⇄ pronta → concluida   ·  dividida (substituida-por) · cancelada
Épico / PRD                    rascunho → em-revisao → aprovado → fatiado → concluido · cancelado
Ficha (sem épico)              rascunho → aprovada por <P.O.> em <data>   (mudança → volta a rascunho)
Conceito OKF (elm/*.md)        draft → stable + verified humano → publicado (resource/id gravados)
Atendimento (AT-nnn)           aberto → concluido
Sprint (sprint-<nn>.md)        aberta → fechada (não concluídas migram "→ sprint <nn+1>")
```

### 1.5 Gates humanos e onde ficam

| Gate | Skill | Pode ser dispensado? |
|---|---|---|
| PRD | S08 Passo 5 | não |
| Backlog | S09 Passo 2 | não |
| Ficha | S04 Passo 2 (padrão) | não |
| Plano | S13 Passo 5 | AFK com "análise basta"; rápida com `GATE na trilha rápida = não` |
| PR | humano (merge) | nunca |
| Escrita no ELM / push / troca de branch | todas | nunca ("sim" de uma pessoa) |

### 1.6 Onde se escreve (três territórios)

| Território | Quem escreve | Regra |
|---|---|---|
| **Base** (`<produto>/`, glossário, ADRs, `sdd.md` Regras aprendidas) | S04, S06, S07 (glossário), S08, S09, S10, S17, S18 | `git switch <base>` + `pull --ff-only`; árvore suja → avise e pare; push/PR curto com "sim" |
| **Branch da fatia** (`.kiro/specs/<ft>-<slug>/`) | S05, S12–S16, S19 | `backlog.md` nunca muda aqui; revisor/pesquisador não gravam `status.md` |
| **Local, fora do git** (`.kiro/local/`) | S06 (dados de cliente), S16 (evidência com dado real), S19 (worktrees, log), S15 (vereditos `wf/`) | dado de cliente nunca vai para o git |

### 1.7 Achados de coesão do orquestrador (visão transversal)

| # | Severidade | Achado | Evidência |
|---|---|---|---|
| O1 | Alta | **Skills sem agente.** `sdd-consolidar` e `sdd-aprender` não estão em nenhum agente; `sdd-iniciar` e `sdd-status` só no `sdd-orquestrador`. Quem trabalha dentro do `sdd-produto` recebe da `sdd-triar` a oferta "começar agora (`sdd-iniciar`)" e não tem a skill; quem trabalha no `sdd-codificador` termina o PR e não tem a `sdd-consolidar`. E mesmo no orquestrador a `sdd-iniciar` fora do loop não roda: a lista de comandos dele não tem `git switch` nem `git pull --ff-only` (Passo 4 da iniciar: `git switch -c <branch> origin/<base>`). Na prática, iniciar, consolidar e aprender só funcionam na sessão padrão (com o power carregado). | `sdd-setup/assets/agents/*.json` (resources); `sdd-setup/SKILL.md` Passo 6 (tabela "Já tem"); `sdd-orquestrador.json` `toolsSettings.shell.allowedCommands` |
| O2 | Alta | **`[VER]` concluída antes do PR.** A `sdd-verificar` lança as horas e conclui a `[VER]` no ACEITO, antes da leitura humana do PR; mudança pedida no PR exige nova verificação com a tarefa já fechada. No loop/agente verificador (sem MCP) a `[VER]` vira `ELM pendente` e nenhuma skill a recolhe depois (a consolidação só trata `[DEV]`/`[REV]`). | `sdd-verificar/SKILL.md` Passo 4; `sdd-consolidar/SKILL.md` Passo 2 (*horas*) |
| O3 | Baixa | **Trilha rápida e `design.md`.** README, guia e `sdd-iniciar` resumem a rápida como `bugfix.md` + `tasks.md`; os templates da `sdd-plano` têm um `design.md` curto para a rápida (causa raiz, correção, estratégia de teste), e `sdd-implementar`/`sdd-verificar` o leem. O comportamento está definido; só os resumos omitem o arquivo. | `README.md` tabela de trilhas; `sdd-iniciar` Passo 2; `sdd-plano/references/plano-templates.md:145` |
| O4 | Média | **Escritas na base sem o preâmbulo de base.** `sdd-triar`, `sdd-consolidar`, `sdd-aprender` e `backlog.md` (regras) dizem "troque para a base, `pull --ff-only`, árvore suja → pare"; `sdd-atender` (Abrir/Concluir) e `sdd-planejamento` (gravar sprint/encaixe) só dizem "commit na base". | `sdd-atender` §1.4 e §3.3; `sdd-planejamento` Modo sprint 7 e Encaixe |
| O5 | Média | **Atendimento sem sprint aberta / Kanban.** A `sdd-atender` grava linha no `sprint-<nn>.md` aberto e usa a iteração dele; não há regra para Kanban nem para "nenhuma sprint aberta" (a `sdd-iniciar` tem as duas). | `sdd-atender` Arquivos e §1.3 |
| O6 | Baixa | **Número do AT reservado antes da confirmação.** "lê o `Próximo` do `README.md` e já o incrementa" antes da entrevista e da confirmação no EWM; desistência no meio queima o número sem registro. | `sdd-atender` §1.1 |

Os achados O1–O6 são do orquestrador; os achados por skill estão nas Partes 2–4 e são consolidados na Parte 5.


## Resultados por skill (Partes 2, 3 e 4)

Para cada skill: o plano dos fluxos (Parte 2), o teste cego (Parte 3) e a verificação dos arquivos (Parte 4). As afirmações do executor mecânico (Haiku) foram conferidas e, quando erradas, corrigidas pela Parte 4 (veja a seção de confirmações e refutações de cada grupo no Anexo A).

## S01 · sdd (guia do fluxo)

### Parte 2 — Plano do fluxo esperado (Sonnet)


Skill sem script e sem `references/`/`assets/`: é só um guia (127 linhas). Não grava nada, não chama outra skill; o
resultado é sempre uma explicação ou um encaminhamento. Gatilhos da description (`sdd/SKILL.md:3`): "como funciona o
sdd", "qual o fluxo", "o que eu faço agora com isso", "sdd"; e "decidir o próximo passo quando nenhuma outra skill sdd
se encaixa".

#### S01-F1 · Explicar o fluxo (visão geral)
- **Gatilho:** "como funciona o sdd", "qual o fluxo", "sdd" (`sdd/SKILL.md:3`); pessoa nova no projeto/power.
- **Pré-condições / lidos:** só o próprio `SKILL.md`. Verifica (implicitamente) se há `.kiro/steering/sdd.md`
  (`sdd/SKILL.md:17-18`); a skill não manda *ler* o arquivo, só o cita.
- **Processamento:**
  1. Abre com a tese (alinhamento antes, verificação depois; pessoas decidem o quê/aprovam o como/leem o código;
     ELM = registro oficial, repositório = como foi feito) (`:12-15`).
  2. Apresenta as **5 trilhas** e quando cada uma vale: direta, rápida, padrão, épico, atendimento (`:25-31`), com o
     princípio "o tamanho decide a cerimônia" (`:20`, `:61`).
  3. Mostra o diagrama ENTRADA → PRODUTO → FATIA → DEPOIS (`:36-44`), incluindo que toda demanda nova entra pela
     `sdd-triar` e que `sdd-iniciar` só começa o que já está registrado e planejado (`:22-23`).
  4. Lista os **5 gates humanos** (PRD, Backlog, Ficha, Plano, PR) e a exceção AFK (`:46-56`) e, se pedido, os 10
     princípios (`:58-72`).
  5. Regra das horas: toda hora cabe numa tarefa `[ESP]/[DEV]/[REV]/[VER]/[ATD]`, lançada na conclusão da tarefa,
     nunca nos gates (`:33-34`).
  6. Se não houver `.kiro/steering/sdd.md` → "comece por 'configurar o sdd'" (`:17-18`).
- **Resultado:** explicação em texto (sem arquivos). Próximo passo: `sdd-setup` se não configurado; senão `sdd-triar`
  ("nova demanda: …") ou `sdd-iniciar` ("vamos trabalhar na FT-…") — via tabela `:76-97`.
- **Lacunas:** ver S01-G1 a S01-G4 abaixo.

#### S01-F2 · Rotear / decidir o próximo passo ("o que eu faço agora com isso")
- **Gatilho:** "o que eu faço agora com isso" (`sdd/SKILL.md:3`) ou pedido que não casa com nenhuma outra skill sdd.
- **Pré-condições / lidos:** pedido da pessoa; tabela "O que dizer" (`:74-97`). Nenhum arquivo do projeto é lido pela
  skill (não manda ler `status.md`/`backlog.md`).
- **Processamento:**
  1. Classifica a intenção na tabela "Quero… → Skill" (`:76-97`): configurar → `sdd-setup`; onde parei/fechar sessão
     → `sdd-status`; demanda nova/defeito/lote EWM → `sdd-triar`; começar/retomar → `sdd-iniciar`; alinhar →
     `sdd-entrevistar`; PRD → `sdd-prd`; fatiar → `sdd-fatiar`; sprint/roadmap/virada/review → `sdd-planejamento`;
     cliente → `sdd-atender`; horas → `sdd-elm` modo *horas*; pesquisar → `sdd-pesquisar`; plano → `sdd-plano`;
     implementar/PR → `sdd-implementar`; revisar → `sdd-revisar`; verificar → `sdd-verificar`; pós-merge →
     `sdd-consolidar`; ELM → `sdd-elm`; AFK em lote → `sdd-loop` (agente `sdd-orquestrador`); workflow →
     chat do Kiro ("rode o workflow `sdd-entregar-fatia` para a FT-031" ou `/workflow-run`); lição → `sdd-aprender`.
  2. Se a pessoa está no meio de uma fase → aplica as **fronteiras de fase** (`:111-115`): seguir na mesma sessão se o
     contexto serve → sessão nova se não importa mais → mandar a agente se puder correr AFK; "nunca compacte no meio
     de uma fase".
  3. Se "o que eu faço agora" for sobre estado real do projeto (qual fatia, o que está parado) → a tabela manda para
     `sdd-status` (`:79`); a skill `sdd` sozinha não tem como saber o estado (não lê arquivos).
- **Resultado:** indica a skill (e a frase-gatilho dela) e, quando cabe, a fronteira de fase. Sem arquivos. Handoff:
  a skill indicada.
- **Lacunas:** S01-G1 (sobreposição de gatilho com `sdd-status`), S01-G2 (workflow sem skill), S01-G4.

#### S01-F3 · Consulta de referência (gates, trilhas, onde moram os arquivos, regras de ouro)
- **Gatilho:** perguntas pontuais após a visão geral: "quem aprova o plano?", "onde fica o status.md?", "o MCP do
  ELM vai em qual agente?", "pode subir dado de cliente no git?".
- **Pré-condições / lidos:** `sdd/SKILL.md:46-56` (gates), `:99-109` (onde moram), `:117-127` (regras de ouro).
- **Processamento:**
  1. Gates: PRD=P.O.; Backlog=P.O.+time; Ficha=P.O.; Plano=dev (de preferência quem revisa o PR); PR=quem revisa
     (`:48-54`); AFK pode dispensar só o gate do plano, nunca o PR (`:56`).
  2. Onde moram: `.kiro/steering/sdd.md`, `.kiro/agents/sdd-*.json`, `<produto>/` (backlog, épicos, planejamento,
     atendimentos, aprendizado — só na base), `.kiro/specs/<ft>-<slug>/`, glossário/ADRs/bundle (caminhos no `sdd.md`),
     opcionais da setup (`hooks/sdd.json`, `workflows/sdd-*`, `sdd/http.sh`), `.kiro/local/` (fora do git) (`:101-109`).
  3. Regras de ouro: nada inventado; escrita no ELM/troca de branch/push/alteração de work item só com "sim"; agente
     nunca faz merge nem `--force`; MCP do ELM só em `sdd-produto`, `sdd-codificador`, `sdd-orquestrador`; sem MCP →
     `ELM pendente`; dado de cliente só em `.kiro/local/<origem>/<id>/` (`:119-127`).
  4. Se a resposta depende dos valores do projeto (pasta do produto, glossário, comandos) → remete ao
     `.kiro/steering/sdd.md` (`:103`, `:105`, `:107`).
- **Resultado:** resposta em texto; sem arquivos.
- **Lacunas:** S01-G3.

#### Lacunas observadas — S01
- **S01-G1 · Sobreposição de gatilhos com `sdd-status`.** `sdd/SKILL.md:3` dispara em "o que eu faço agora com isso"
  e `sdd-status/SKILL.md:3` em "o que tem pendente", "qual a próxima fatia", "retomar". O texto da `sdd` não diz como
  desempatar: `sdd` afirma ser para "quando nenhuma outra skill sdd se encaixa", mas a pergunta mais comum
  ("o que faço agora?") é exatamente o painel. Sem regra explícita "pergunta sobre estado real → `sdd-status`".
- **S01-G2 · Workflow sem dona.** `sdd/SKILL.md:96` manda "rodar uma receita de workflow" para a pessoa no chat do Kiro
  (sem skill). Os workflows só existem se `sdd-setup` os instalou (`sdd-setup/SKILL.md:225-227`); a `sdd` não diz o
  que fazer quando a pasta `.kiro/workflows/` não existe (apontar `sdd-setup` modo atualização).
- **S01-G3 · Caminhos incompletos na tabela "Onde moram".** `sdd/SKILL.md:105` omite `<produto>/fatias/FT-<nnn>-<slug>.md`
  (ficha da fatia sem épico, `sdd-triar/SKILL.md:92`), `<produto>/roadmap.md`, `planejamento/equipe.json`,
  `acordos.md` e `sprints/` (`sdd-planejamento/SKILL.md:23`), e `<produto>/planejamento/` aparece só como "planejamento/".
  Também omite `.kiro/local/wf/` (vereditos de workflow, citado em `:109`) como pasta e `.kiro/local/loop-*.md`.
- **S01-G4 · Sem verificação de configuração.** `:17-18` diz "sem `sdd.md`, comece por configurar", mas nenhuma frase
  manda a skill checar se o arquivo existe antes de rotear para skills que dependem dele; fica a cargo de cada skill
  (ex.: `sdd-iniciar/SKILL.md:19`).
- **S01-G5 (menor) · Tabela de trilhas vs. frase de status.** `:29` diz que a trilha padrão serve a "uma fatia do
  backlog: de um épico, ou sem épico com regra clara e ficha aprovada"; o gate "Ficha" (`:52`) aparece só em "Gates" e
  não no diagrama (`:36-44`, que só tem GATE PRD/backlog/plano) — o diagrama não mostra onde a ficha é aprovada.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S01-F1 · Explicar o fluxo (visão geral)
1. INPUT EXATO: "como funciona o sdd"
   ESTADO: repositório git; .kiro/steering/sdd.md AUSENTE; nenhuma fatia em andamento.
2. REGRA APLICADA:
   - SE o pedido casa com a description ("como funciona o sdd") ENTÃO usa a skill sdd — sdd/SKILL.md:3
   - SE o pedido é explicar o fluxo ENTÃO abre com a tese (alinhar antes, verificar depois; ELM = oficial; repo = como) — sdd/SKILL.md:12-15
   - ENTÃO apresenta as 5 trilhas e quando cada uma vale — sdd/SKILL.md:25-31
   - ENTÃO mostra o diagrama ENTRADA → PRODUTO → FATIA → DEPOIS — sdd/SKILL.md:36-44
   - ENTÃO lista os 5 gates e a exceção AFK — sdd/SKILL.md:46-56
   - SE sdd.md ausente ENTÃO diz "comece por configurar o sdd" — sdd/SKILL.md:17-18 (a skill não prescreve como checar a ausência)
   - Princípios (1–10) — sdd/SKILL.md:58-72: a skill não diz em que caso incluir; sem condição escrita.
3. OUTPUT GERADO: explicação em texto livre com as seções acima e a frase "comece por configurar o sdd".
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO (a) profundidade e inclusão dos princípios: sdd/SKILL.md:58-72 não tem condição; (b) a checagem
   de sdd.md (sdd/SKILL.md:17-18) não tem ação prescrita, então o executor não sabe se deve ler o arquivo.

S01-F2 · Rotear / decidir o próximo passo ("o que eu faço agora com isso")
1. INPUT EXATO: "o que eu faço agora com isso"
   ESTADO: .kiro/steering/sdd.md PRESENTE; backlog com FT-031 "em andamento" (a skill não lê arquivos).
2. REGRA APLICADA:
   - SE o pedido casa com o gatilho ("o que eu faço agora com isso") ENTÃO usa a skill sdd — sdd/SKILL.md:3
   - SE o pedido é "o que fazer agora" ENTÃO indica sdd-status (linha "saber onde parei / o que fazer agora · fechar a sessão") — sdd/SKILL.md:79
     (sdd-status/SKILL.md:3 também cita "o que fazer agora" na description: mesmo destino)
3. OUTPUT GERADO: "Próximo passo: sdd-status (onde parei / o que fazer agora)."
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO (destino único: sdd-status).

S01-F3 · Consulta de referência (gates, trilhas, onde moram, regras de ouro)
1. INPUT EXATO: "quem aprova o plano?"
   ESTADO: .kiro/steering/sdd.md PRESENTE.
2. REGRA APLICADA:
   - SE o pedido casa um gatilho literal ("como funciona", "qual o fluxo", "o que eu faço agora com isso", "sdd") ENTÃO usa
     a skill — sdd/SKILL.md:3 → "quem aprova o plano?" NÃO casa.
   - SE o pedido é "entender ou explicar o fluxo" ENTÃO usa a skill — sdd/SKILL.md:3 (description, texto livre) → pode casar.
   - SE a pergunta é sobre o gate Plano ENTÃO responde "dev (de preferência quem vai revisar o PR)" — sdd/SKILL.md:53
3. OUTPUT GERADO: "O plano é aprovado pelo dev, de preferência quem vai revisar o PR (GATE do plano)."
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO (ativação): "quem aprova" não está nos gatilhos literais de sdd/SKILL.md:3; só o texto
   livre "entender ou explicar o fluxo" pode cobrir a pergunta, e a skill não diz se perguntas pontuais entram.

S01-E1 · Borda: pedido que casa duas linhas da tabela "O que dizer"
1. INPUT EXATO: "o que eu faço agora com isso: o cliente reclamou que o relatório X sai com total errado"
   ESTADO: .kiro/steering/sdd.md PRESENTE.
2. REGRA APLICADA:
   - SE o pedido é "o que fazer agora" ENTÃO sdd-status — sdd/SKILL.md:79
   - SE o pedido é um defeito ("registrar qualquer demanda nova — pedido, defeito…") ENTÃO sdd-triar — sdd/SKILL.md:80
3. OUTPUT GERADO: duas indicações de skill para o mesmo input (sdd-status e sdd-triar); nenhuma prioridade escrita.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (sdd/SKILL.md:79 × sdd/SKILL.md:80): a mesma frase casa duas linhas da tabela, com destinos diferentes.

S01-E2 · Pré-condição ausente: pedido de trabalho com sdd.md ausente
1. INPUT EXATO: "vamos trabalhar na FT-031"
   ESTADO: .kiro/steering/sdd.md AUSENTE.
2. REGRA APLICADA:
   - SE sdd.md ausente ENTÃO "comece por configurar o sdd" — sdd/SKILL.md:17-18
   - SE o pedido é "começar ou retomar um trabalho já registrado" ENTÃO sdd-iniciar — sdd/SKILL.md:81
3. OUTPUT GERADO: duas saídas possíveis: "configurar o sdd" (sdd-setup) ou "sdd-iniciar". Nenhuma prioridade escrita.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (sdd/SKILL.md:17-18 × sdd/SKILL.md:81): uma regra manda configurar antes; a outra manda
   iniciar a fatia.

S01-E3 · Negativo: pergunta de referência com resposta "não"
1. INPUT EXATO: "pode subir o extrato de clientes no git?"
   ESTADO: .kiro/steering/sdd.md PRESENTE.
2. REGRA APLICADA:
   - SE o pedido é sobre dado de cliente ENTÃO não vai para o git: fica em .kiro/local/<origem>/<id>/ — sdd/SKILL.md:125-127
   - (o registro versionado guarda consulta, contagem, caminho e resumo sem identificar pessoas) — sdd/SKILL.md:125-127
3. OUTPUT GERADO: "Não. Dado de cliente nunca vai para o git: fica em .kiro/local/<origem>/<id>/; o versionado guarda
   consulta, contagem, caminho e resumo sem identificar pessoas."
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S01-F1 Explicar o fluxo | AMBÍGUO | Princípios sem condição (:58-72); checagem de sdd.md sem ação prescrita (:17-18) |
| S01-F2 Rotear "o que eu faço agora" | DETERMINÍSTICO | Destino único sdd-status (:79) |
| S01-F3 Consulta de referência | AMBÍGUO | "Quem aprova o plano" não casa gatilho literal (:3); só o texto livre "entender o fluxo" cobre |
| S01-E1 Demanda + "o que faço agora" | CONFLITO | :79 (sdd-status) × :80 (sdd-triar) para o mesmo input |
| S01-E2 Trabalho com sdd.md ausente | CONFLITO | :17-18 (configurar primeiro) × :81 (sdd-iniciar) |
| S01-E3 Dado de cliente no git | DETERMINÍSTICO | Negativa direta (:125-127) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


Sem escrita: S01-F1 (explicar o fluxo) · S01-F2 (rotear) · S01-F3 (consulta de referência) · S01-E1 · S01-E2 · S01-E3. A skill não tem `references/` nem
`assets/`, nunca grava, nunca commita (`sdd/SKILL.md` inteiro). Confirmo as afirmações "ARQUIVOS ESCRITOS: nenhum" da Parte 3.
Única observação de persistência: a tabela "Onde as coisas moram" (`sdd/SKILL.md:101-109`) é a referência de caminhos do power inteiro e está incompleta
(ver achados).

---


## S02 · sdd-setup

### Parte 2 — Plano do fluxo esperado (Sonnet)


Arquivos lidos: `sdd-setup/SKILL.md` (303 l.), `references/toolkits.md`, `references/automacoes.md`,
`references/agentes.md`, `assets/steering/sdd.md`, `assets/hooks/sdd.json`, `assets/scripts/http.sh`,
`assets/workflows/*.json`, `assets/toolkit.schema.json`, `assets/agents/*.json` (amostra: produto, codificador,
orquestrador). Regras gerais (valem em todos os fluxos): "padrão primeiro" — padrões aplicados em tabela por bloco,
uma confirmação ("ok" ou a linha que muda); pergunta só o que não tem padrão nem dá para detectar, uma por vez;
não achou algo → pergunta, nunca conclui "não há" sozinha; **nada é gravado antes do resumo do Passo 8 e do "ok"**;
nunca lê credenciais (`sdd-setup/SKILL.md:20-27`). Os arquivos da skill ficam no power instalado, não no projeto
(`:12-14`).

#### S02-F1 · Primeira configuração (projeto sem sdd)
- **Gatilho:** "configurar o sdd", "setup do sdd", "criar os agentes do sdd" (`sdd-setup/SKILL.md:3`); ou handoff de
  outra skill sem `.kiro/steering/sdd.md` (`sdd-iniciar/SKILL.md:19`; `sdd-status/SKILL.md:13`; `sdd/SKILL.md:17`).
- **Pré-condições / lidos:** repositório (idealmente git); power `sdd` instalado em `~/.kiro/powers/installed/sdd/`;
  nenhum `.kiro/steering/sdd.md` nem `.kiro/agents/sdd-*.json`; opcionais: power `elm`, `pa_*.json`, toolkits, mcp.json.
- **Processamento:**
  1. **Passo 0 — onde estou** (`:29-43`): `git rev-parse --show-toplevel` (sem git → avisa que o fluxo depende de
     branches e PRs); acha o power (`~/.kiro/powers/installed/sdd/skills/sdd-setup/SKILL.md`; senão `find ~/.kiro/powers`;
     senão pergunta); `KIRO_HOME` definida → procura em `$KIRO_HOME/powers/installed/sdd/`, fora do home → avisa que só
     vale nesta máquina e pede "ok" para caminho absoluto. Todos os caminhos gravados são relativos (projeto → raiz;
     power/usuário → `~/…`; `/` como separador; nunca `/home/…`, `C:\…`, variáveis). Detecta modo: não existe
     steering/agentes → modo **novo** (F1). Existe → F2 (`:44-48`); `sdd2` → F3; `sdd-projeto.md` sem `sdd.md` → F4.
  2. **Passo 1 — entender o projeto** (`:67-90`): lê `README*`, `AGENTS.md`, `CONTRIBUTING*`, `.kiro/steering/*.md`,
     builds (`pom.xml`, `build.gradle*`, `package.json`, `pyproject.toml`, `go.mod`, `*.csproj`, `Cargo.toml`,
     `Makefile`), árvore 2–3 níveis, `git log --oneline -20`. Propõe numa mensagem "🔎 Entendi assim" (tipos, stack,
     testes, steering ✅/❌) → "Está certo? (sim / corrija)". Tipos pela tabela do `toolkits.md:24-32`
     (backend, batch, frontend, mobile, dados, biblioteca, infra). Steering product/tech/structure: confirma o padrão
     do Kiro; faltando → pergunta **um papel por vez** (qual `.md` faz o papel, ou oferecer "Generate Steering Docs";
     "nenhum" vale). Regras críticas: propõe a partir do steering tech/structure; pessoa confirma/edita/"nenhuma".
  3. **Passo 2 — backpressure** (`:92-104`): propõe comandos (compilar, testes, teste único, lint, cobertura+gate,
     executar app, exercitar cenário, massa de teste) do build/steering/README/`comandos` do toolkit e **oferece rodá-los
     uma vez**. Falhou → mostra erro; pessoa decide (corrigir, seguir assim, parar).
  4. **Passo 3 — git, PR e banco** (`:106-115`), por detecção: branch base (`git symbolic-ref refs/remotes/origin/HEAD`),
     prefixo (branches remotas; padrão `feature/`), padrão de commit (`git log`), **abrir PR pelo host do `origin`**
     (github → `gh pr create`; gitlab → `glab mr create`; outro host → "entregar título e descrição"; ferramenta
     ausente/não autenticada → "entregar título e descrição" com aviso de como instalar; nunca `gh` p/ GitLab nem `glab`
     p/ GitHub), MCP de banco (em `.kiro/settings/mcp.json` e `~/.kiro/settings/mcp.json`; qual tool só consulta; ou
     "não há"; recomenda usuário somente leitura), artefatos de produto (padrão `PR curto para a base`).
  5. **Passo 4 — produto, conhecimento, ELM** (`:117-157`): (a) pasta do produto: a do `backlog.md` já existente senão
     `.kiro/planejamento`; (b) glossário `docs/glossario.md` e ADRs `docs/adr` — usa os existentes, senão padrão criar;
     recusados → "não há" e remove `{{GLOSSARIO}}`/`{{ADR}}` dos agentes; (c) **ELM**: power `elm` instalado e
     `.kiro/config/power/elm/pa_*.json`? Sem power, confirmado → `Usa ELM: não`; com power sem `pa_*.json` → oferece
     rodar `elm-setup` antes; com `pa_*.json` → sem perguntas, tabela "ELM — padrões aplicados" (tipos/pastas por
     proximidade de nome, publicar requisitos `na-aprovacao`, backlog no EWM `na-sprint`, ET `não publica`, manual
     DOORS `nada`, pontos `2·3·5`, fatia dividida = filhos do original, colunas do `CT.csv`); pergunta só tipo/pasta sem
     nome parecido; também sem perguntar: títulos de tarefas, tipo do épico, campo de aceite, classificação das
     tarefas. Sustentação/Atendimento não são perguntados (criados pela `sdd-elm` na primeira sprint). (d) MCP do ELM
     nos agentes: servidor `mcp-elm` precisa estar no `mcp.json` do workspace ou do usuário; não está → oferece
     acrescentar no do usuário (com "ok"). (e) Bundle do RM (`rm.download.path`, pastas com `index.md` `okf_version`):
     mostra e confirma; nada achado → pergunta; registra na seção Projeto.
  6. **Passo 5 — inventário** (`:159-167`): procura toolkits (`.kiro/toolkits/*/toolkit.json`,
     `~/.kiro/toolkits/*/toolkit.json`, `~/.kiro/powers/installed/*/toolkit.json`, skills com `metadata.toolkit` —
     `toolkits.md:34-47`) e skills avulsas de `.kiro/skills`, `~/.kiro/skills`, powers instalados, **exceto** `sdd`,
     `sdd-*`, `sdd2`, `sdd2-*`, `elm`, `elm-*`. Toolkit cujo `deteccao` (arquivo existe **e** `contem` aparece) casa →
     "detectado". Sem toolkit → diz uma vez, registra `Toolkits: nenhum — <tipo>`, sugere criar skills em
     `.kiro/skills/` (`toolkits.md:119-124`).
  7. **Passo 6 — agentes, um por vez** (`:169-219`): ordem produto → pesquisador → codificador → revisor → verificador →
     orquestrador. Uma mensagem por agente com a proposta completa já marcada (skills agrupadas por toolkit/origem,
     MCPs, modelo, subagentes) e **uma** confirmação ("ok" ou o que muda). Padrões: skills marcadas só de toolkits
     detectados com o papel do agente; MCP de banco só leitura (`@servidor/tool` de consulta) em pesquisador,
     codificador, revisor, verificador; browser/Playwright no verificador em `frontend`; MCP `elm` marcado em
     produto/codificador/orquestrador (leitura `allow`, escrita `ask`) e nunca em revisor/verificador/pesquisador;
     modelo = padrão do Kiro sem perguntar; subagentes só em codificador e orquestrador (`sdd-*` marcados; agentes do
     projeto desmarcados; agente com campo `hooks` fica desmarcado com aviso). Registra skills oferecidas e recusadas.
     Depois, **autonomia** por padrões aplicados: plano AFK com aprovação humana; trilha rápida sem GATE do plano;
     paralelismo do loop `1`; push/PR no loop "perguntar a cada lote" (`ask`; "não — a pessoa abre" → `deny`); script
     `.kiro/sdd/http.sh` se a verificação for por HTTP (única pergunta: **URL base do ambiente de teste** quando não está
     no repo; nunca produção; "nenhum" → cada `curl` pede confirmação).
  8. **Passo 7 — hook e workflows** (`:221-227`; `automacoes.md`): hook `sdd-backpressure` ligado quando há compilar+testes;
     receitas de workflow instaladas só se `kiroAgent.workflows.enabled`/`chat.enableWorkflows` já está habilitado;
     diz na tabela que quem dispara é a pessoa e que ambos exigem IDE ou engine V3.
  9. **Passo 8 — montar, mostrar, gravar** (`:229-262`): em memória monta `.kiro/steering/sdd.md` (de
     `assets/steering/sdd.md`, sem `<…>` sobrando), `.kiro/agents/sdd-<agente>.json` ×6 (placeholders, skills, MCPs,
     comandos e caminhos nos **dois blocos** V2/V3 em espelho; nunca regenerar `permissions` pelo `kiro-cli`),
     hook/workflows/`http.sh` (`{{URL_TESTE}}` sem barra final), `<produto>/` (só o que falta: `backlog.md` mínimo,
     `planejamento/`, `aprendizado/licoes.md`, `atendimentos/README.md`), `.gitignore` (+`.kiro/local/`). Mostra o
     resumo "⚙️ sdd — …" e pede "Gravar? ("ok")". Avisa que o Kiro pede confirmação por arquivo em `.kiro/agents/`,
     `.kiro/hooks/`, `.kiro/workflows/`. Só grava com "ok".
  10. **Passo 9 — validar** (`:264-289`): parse dos JSON; `name` = nome do arquivo; nenhum `{{…}}`; `includeMcpJson: true`
      e regra `mcp` coerente (leitura em `allowedTools`, escrita fora); MCP do ELM só nos 3 agentes e servidor existe no
      `mcp.json`; `.kiro/steering/` só com `sdd.md`; todo `skill://`/`file://` existe e é relativo; ferramentas que varrem
      a raiz ignoram `.kiro/local/` (senão acrescenta exclusão com "ok" ou registra no `sdd.md` que o loop não deve ser
      usado); `validate_workflow` (se Workflows ligado); `kiro-cli agent validate --path …` por agente, `kiro-cli agent list`,
      `kiro-cli agent upgrade --dry-run` (esperado "out of sync (not rebuilt)"); herança de recursos (oferece
      `kiro-cli settings --workspace chat.disableInheritingDefaultResources true`); workspace não confiável → avisa.
  11. Sugere o commit (lista de caminhos) — só com confirmação — e fecha com o próximo passo (`:291-295`).
- **Resultado:** arquivos criados (caminho exato): `.kiro/steering/sdd.md`; `.kiro/agents/sdd-produto.json`,
  `sdd-pesquisador.json`, `sdd-codificador.json`, `sdd-revisor.json`, `sdd-verificador.json`, `sdd-orquestrador.json`;
  opcionais `.kiro/hooks/sdd.json`, `.kiro/workflows/sdd-planejar-fatia.workflow.json`,
  `.kiro/workflows/sdd-entregar-fatia.workflow.json`, `.kiro/sdd/http.sh`; `<produto>/backlog.md`,
  `<produto>/planejamento/`, `<produto>/aprendizado/licoes.md`, `<produto>/atendimentos/README.md`; `.gitignore`
  (+`.kiro/local/`); glossário/ADRs só se a pessoa pediu criar. Resposta: resumo "⚙️ sdd — …" + resultado da validação
  + proposta de commit. **Handoff** (`:293-295`): "nova demanda: …" → `sdd-triar` (épico → `sdd-prd`); "vamos trabalhar
  na <id>" → `sdd-iniciar`; "onde parei?" → `sdd-status`.
- **Lacunas:** S02-G1, S02-G2, S02-G3, S02-G4, S02-G6, S02-G7, S02-G8, S02-G9, S02-G10 (abaixo).

#### S02-F2 · Atualização da configuração (modo atualização)
- **Gatilho:** "atualizar os agentes do sdd", "atualizar a configuração do sdd" (`sdd-setup/SKILL.md:3`); README
  `README.md:102-104` ("depois de atualizar o power ou um toolkit … na 2.3.0 é obrigatório: o `sdd-produto` passa a
  carregar a `sdd-triar`"); também `sdd-setup/SKILL.md:208-209` (skills novas).
- **Pré-condições / lidos:** `.kiro/steering/sdd.md` e/ou `.kiro/agents/sdd-*.json` existentes (`:44`); o `sdd.md`
  atual (tabela Agentes com colunas "Skills extras" e "Oferecidas e recusadas", `assets/steering/sdd.md:84-91`); power
  novo instalado; inventário atual de skills/toolkits.
- **Processamento:**
  1. Passo 0 itens 1–3 como em F1 (raiz, power, caminhos relativos).
  2. **Modo atualização** (`:44-48`): mostra a configuração atual numa tabela e pergunta o que mudar, com a opção
     "nada — só regenerar os agentes". Refaz só o que mudou nas respostas, **mas agentes, hook e workflows sempre a
     partir dos templates atuais** (com os valores do projeto), mesmo os que já têm o nome certo; mostra o diff de cada um.
  3. Skills: compara o inventário atual com `sdd.md`; pergunta só sobre as skills **novas** (não presentes nas colunas
     "Skills extras" nem "Oferecidas e recusadas"); skill que sumiu sai do agente com aviso (`toolkits.md:126-130`;
     `SKILL.md:208-209`).
  4. Passo 8 em atualização: `sdd.md` regenerado **preservando a seção Regras aprendidas** (nunca apagar regras
     promovidas) (`:233-234`); `<produto>/` só acrescenta o que falta, nunca recria (`:244-245`); agente editado à mão →
     mostra diff e pergunta antes de sobrescrever (`:261`); resumo + diff de cada arquivo que muda + "Gravar?".
  5. Passo 9 validação (igual a F1).
- **Resultado:** `.kiro/steering/sdd.md` (com a data/versão do power atualizadas e Regras aprendidas intactas),
  `.kiro/agents/sdd-*.json`, `.kiro/hooks/sdd.json`, `.kiro/workflows/sdd-*.workflow.json`, `.kiro/sdd/http.sh`
  regenerados dos templates; diff de cada um mostrado. Handoff: commit sugerido (só com confirmação) e o mesmo próximo
  passo de F1.
- **Lacunas:** S02-G5 (quais passos reexecutam em atualização), S02-G3, S02-G8, S02-G11.

#### S02-F3 · Migração do `sdd2` para o `sdd` (layout antigo)
- **Gatilho:** modo atualização com projeto "configurado com o nome `sdd2`" (`.kiro/steering/sdd2*.md`,
  `.kiro/agents/sdd2-*.json`) (`sdd-setup/SKILL.md:49-59`); README `:102-106` ("atualizar a configuração do sdd").
- **Pré-condições / lidos:** `.kiro/steering/sdd2.md`, `sdd2-projeto.md`, `sdd2-licoes.md`, `sdd2-fechar-sessao.md`;
  `.kiro/agents/sdd2-*.json`; `.kiro/hooks/sdd2.json`; `.kiro/workflows/sdd2-*.workflow.json`; `.kiro/sdd2/http.sh`;
  `.kiro/produto/`; `.kiro/aprendizado/`.
- **Processamento:**
  1. Propõe a migração com o **plano numa só mensagem** e pede "ok" (`:50`).
  2. Mapeamento (`:51-58`): `sdd2.md` + `sdd2-projeto.md` → valores vão para as seções do novo `sdd.md`;
     `sdd2-licoes.md` → regras promovidas vão para "Regras aprendidas" sem perder nenhuma; `sdd2-fechar-sessao.md` →
     removido (agora é da `sdd-status`); `.kiro/agents/sdd2-*.json` → removidos; `.kiro/hooks/sdd2.json` →
     `.kiro/hooks/sdd.json`; `.kiro/workflows/sdd2-*.workflow.json` → `.kiro/workflows/sdd-*.workflow.json`;
     `.kiro/sdd2/http.sh` → `.kiro/sdd/http.sh`; `.kiro/produto/` → pasta do produto (Passo 4);
     `.kiro/aprendizado/` → `<produto>/aprendizado/`.
  3. Execução com `git mv`/`git rm` (arquivo não versionado → `mv`/`rm`), **sem mudar o conteúdo dos movidos**; avisa que
     as fatias em andamento (`.kiro/specs/`) não mudam.
  4. Em seguida segue como F2 (agentes `sdd-*` gerados de novo pelo Passo 8; Passo 9 confere que não sobrou `sdd2*`).
  5. Item "Passo 5" de inventário ignora skills `sdd2`/`sdd2-*` de instalação antiga (`:164`).
- **Resultado:** layout novo no repositório (caminhos acima), `.kiro/steering/sdd.md` único, agentes `sdd-*` novos;
  commit sugerido incluindo "o que a migração moveu ou removeu" (`:291-292`). Próximo passo: o de F1.
- **Lacunas:** S02-G3 (ordem "ok" da migração × "ok" de gravação), S02-G12 (hook/workflow movidos "sem mudar o conteúdo"
  × "sempre a partir dos templates atuais"; e `.kiro/sdd2/http.sh` tem `{{URL_TESTE}}` já resolvido).

#### S02-F4 · Migração da v1 do `sdd` (steering `sdd-projeto.md`)
- **Gatilho:** existe `.kiro/steering/sdd-projeto.md` e **não** existe `.kiro/steering/sdd.md` (`sdd-setup/SKILL.md:60`);
  README `:102-106`.
- **Pré-condições / lidos:** `.kiro/steering/sdd-projeto.md`; agentes v1 `sdd-codificador`, `sdd-revisor`,
  `sdd-orquestrador` (mesmo nome dos novos); `.kiro/agents/sdd-especificador.json`; `.kiro/agents/prompts/sdd-*.md`.
- **Processamento:**
  1. **Oferece** reaproveitar do `sdd-projeto.md`: steering, branch base, prefixo, padrão de commit, ferramenta de PR,
     comandos, gate de cobertura, banco, testes funcionais, ELM e skills por agente (`:60-63`).
  2. Segue o fluxo F1 (Passos 1–7) usando esses valores como padrões detectados.
  3. No Passo 8: os 3 agentes homônimos da v1 são **substituídos** (mostra o diff) (`:63-64`).
  4. O que só a v1 tinha sai com `git rm` e "ok": `.kiro/agents/sdd-especificador.json`,
     `.kiro/agents/prompts/sdd-*.md`, `.kiro/steering/sdd-projeto.md` (`:64-65`). Passo 9 confirma que `sdd-projeto.md`
     não sobrou (`:269-270`).
- **Resultado:** igual a F1 + remoções acima. Próximo passo: o de F1.
- **Lacunas:** S02-G13 (v1 com `.kiro/produto/`/`.kiro/aprendizado/`: o item 5 não diz se a migração de pastas do
  item 4 também vale; README `:105-106` diz que sim para "v1 ou sdd2").

#### S02-F5 · Ligar/atualizar toolkit (skills novas de um toolkit)
- **Gatilho:** "ligar o toolkit" (`sdd-setup/SKILL.md:3`); "toolkit novo ou atualizado → 'atualizar os agentes do sdd'"
  (`toolkits.md:126-130`).
- **Pré-condições / lidos:** `sdd.md` existente (coluna "Oferecidas e recusadas"); toolkit(s) em
  `.kiro/toolkits/*/toolkit.json`, `~/.kiro/toolkits/*/toolkit.json`, `~/.kiro/powers/installed/*/toolkit.json`, ou skills
  com `metadata.toolkit`; formato `toolkit.schema.json`.
- **Processamento:**
  1. Entra em modo atualização (F2). Refaz o inventário (Passo 5) e a detecção (`deteccao.arquivos` existe e algum
     `contem` aparece) (`toolkits.md:87-94`).
  2. Para cada agente, monta proposta agrupada por toolkit, pré-marcando só skills de toolkits **detectados** com o
     papel do agente (`papeis`) (`toolkits.md:96-117`; `SKILL.md:183-206`). Toolkit nunca é ligado sem o "sim" da pessoa,
     agente por agente (`:303`).
  3. `steering[]` do toolkit vira `file://` nos agentes dos papéis indicados (`toolkits.md:92`); `comandos` do toolkit
     só como **proposta** da seção Comandos do `sdd.md` (`toolkits.md:93`); `verificacao` vira texto da seção
     Verificação de aceite (`toolkits.md:94`).
  4. Passo 8–9 como em F2; registra no `sdd.md` o toolkit na linha "Toolkits" e as skills aceitas/recusadas.
- **Resultado:** `.kiro/agents/sdd-*.json` com `skill://` novos (nos dois blocos e, se fora do projeto/power, a leitura
  em `fs_read`/`read.allowedPaths`) e `.kiro/steering/sdd.md` atualizado; handoff como F2.
- **Lacunas:** S02-G5, S02-G14 (`toolkits.md:41-43`: "toolkit implícito" por `metadata.toolkit` — sem `deteccao`, então
  nunca é "detectado" e nunca pré-marcado).

#### Lacunas observadas — S02
- **S02-G1 · Escrita antes do "ok" final.** `sdd-setup/SKILL.md:26` ("Nada é gravado antes do resumo do Passo 8 e do
  'ok'") contradiz: (a) `:152-153` acrescenta entrada no `~/.kiro/settings/mcp.json` do usuário "com ok" ainda no Passo 4;
  (b) `:130` oferece rodar a `elm-setup` (outra skill que grava `pa_*.json`) antes de continuar; (c) `:50-58` executa
  `git mv/git rm` da migração com um "ok" do Passo 0; (d) Passo 2 manda **rodar** build/testes (`:92-104`), que podem
  gerar artefatos; (e) `:286-287` e `:272-273` oferecem alterar configuração fora do que a skill gera
  (`kiro-cli settings --workspace …`, exclusão de `.kiro/local/` em tsconfig/jest/lint "com ok").
- **S02-G2 · "Regras" proíbem o que o fluxo faz.** `:299-300`: "Não altere nada fora de `.kiro/`, da pasta do produto,
  do glossário/ADRs … e do `.gitignore`". Mas `:152-153` escreve em `~/.kiro/settings/mcp.json`, `:272-273` altera config de
  test runners/linters (arquivos fora de `.kiro/`) e `:286-287` grava `.kiro/settings`/config do CLI. Exceções não declaradas
  na regra.
- **S02-G3 · Dois "ok" para a migração.** `:50` pede "ok" ao plano de migração (Passo 0) e `:246`/`:258` incluem a
  migração no resumo "Gravar? ('ok')". Não está dito se a migração (`git mv`/`git rm`) ocorre logo após o primeiro "ok"
  (antes de qualquer leitura/pergunta dos Passos 1–7) ou só na gravação do Passo 8. Idem `:64-65` ("sai com `git rm` e 'ok'").
- **S02-G4 · Subagentes do `sdd-produto`.** `:204` diz "Só codificador e orquestrador: subagentes", porém o template
  `assets/steering/sdd.md:86` lista `sdd-produto` com subagentes `sdd-pesquisador`, `sdd-revisor` e
  `assets/agents/sdd-produto.json:8-9` já traz `subagent/sdd-pesquisador` e `subagent/sdd-revisor` (e o prompt manda
  usá-los, `:4`). A proposta do Passo 6 (`:174-181`) não mostra subagentes de produto, então a pessoa não consegue
  desmarcá-los/estendê-los.
- **S02-G5 · O que reexecuta em modo atualização.** `:44-48` define "refaça só o que mudou nas respostas" mas não diz
  quais dos Passos 1–7 rodam de novo: relê o repositório (Passo 1)? reroda comandos (Passo 2)? reconfirma Git/ELM?
  "nada — só regenerar" pula tudo até o Passo 8? Também falta dizer de onde vêm as "respostas" (lê-se o `sdd.md` atual
  como fonte, mas não há instrução de parsear o `sdd.md`). O `toolkits.md:128-129` ("pergunta só sobre as skills novas")
  e a regra "uma mensagem por agente" (`SKILL.md:183`) não se compõem explicitamente.
- **S02-G6 · Placeholders de comandos sem marcador.** `agentes.md:51` diz que a setup preenche "comandos" (codificador,
  revisor, verificador, orquestrador), mas os templates (`assets/agents/sdd-codificador.json:52-76`) não têm
  placeholder para isso (só `{{POWER}}`, `{{PRODUTO}}`, `{{GLOSSARIO}}`, `{{ADR}}`, `{{SKILLS_EXTRAS}}`, `{{SUBAGENTES}}`):
  não há âncora definida de onde inserir `mvn *` etc. nem a regra para virar regex (V2) × glob (V3) senão a nota genérica
  em `agentes.md:29`. O Passo 9 (`:266`) valida "nenhum `{{…}}` sobrando", mas não valida que os comandos entraram.
  `{{COMPILAR}}`/`{{TESTES}}` (hook) e `{{URL_TESTE}}` (`http.sh`) são citados em `automacoes.md:10` e `SKILL.md:239`
  mas não em `agentes.md`.
- **S02-G7 · Versão e data do `sdd.md`.** O template (`assets/steering/sdd.md:19`) pede "power `sdd` <x.y.z>" e
  "<AAAA-MM-DD>", mas a skill não diz de onde ler a versão (`plugin.json`? `metadata.version`?) nem como obter a data.
- **S02-G8 · Caminho do power e portabilidade.** `:31-43` manda gravar `~/.kiro/powers/installed/sdd` relativo ao home,
  mas `skill://~/…` depende de o Kiro expandir `~` (README/`agentes.md` não citam fonte); `KIRO_HOME` fora do home →
  "pede ok para caminho absoluto", em conflito direto com a regra `:40-43` "nunca absolutos". Exceção declarada só pela
  metade.
- **S02-G9 · Pergunta "uma por vez" × bloco "Padrões aplicados".** `:21-24` diz: perguntar uma coisa por vez, nunca o que
  só confirma um padrão. Mas o Passo 1 (`:73-82`) faz uma confirmação ("Está certo? (sim / corrija)") do que foi
  detectado e o Passo 4/ELM (`:131-149`) faz uma tabela; a fronteira entre "confirmar detecção" e "confirmar padrão" não está
  definida (Passo 1 não aparece como bloco com "Padrões aplicados" apesar de a regra geral listar "projeto").
- **S02-G10 · `sdd-orquestrador` e `sdd-produto`: skills.** Os agentes não recebem a skill `sdd` (guia) nem `sdd-status`
  (exceto orquestrador, `assets/agents/sdd-orquestrador.json:19`), `sdd-triar` está só em produto,
  `sdd-consolidar`/`sdd-aprender`/`sdd-revisar`… ver tabela `:174-181`: **`sdd-consolidar`, `sdd-aprender` e `sdd-status` não
  estão em nenhum agente** (exceto status/orquestrador), logo "fechar a sessão" (S03-F4) e "consolidar" não têm agente
  dono. A tabela do Passo 6 também não lista `sdd-consolidar` nem `sdd-aprender` para nenhum agente (README `:67-82` as lista
  como skills do power). Sessão com o agente padrão do Kiro carrega skills do power (`includePowers` aplica só aos agentes
  customizados), então funciona; mas fica implícito.
- **S02-G11 · Hook com `{{COMPILAR}} && {{TESTES}}` e multi-módulo.** `assets/hooks/sdd.json:10` / `automacoes.md:10`:
  um único par de comandos; o `sdd.md` admite "uma coluna por módulo" (`assets/steering/sdd.md:38`). Não está definido qual
  módulo o hook usa (nem o caso "suíte lenta → sugira o conjunto rápido", sem dizer quem escolhe).
- **S02-G12 · Migração × templates.** `:47-48` (agentes/hook/workflows "sempre a partir dos templates atuais") e `:55-56`
  (`git mv` dos arquivos `sdd2` "sem mudar o conteúdo") se contradizem se o hook/workflow movido também é regenerado:
  precisa decidir se o mv é só histórico git e o conteúdo é regerado do template.
- **S02-G13 · Migração v1 × layout de pastas.** v1 (`sdd-projeto.md`, `:60-65`) só trata steering e agentes; as
  pastas `.kiro/produto/`/`.kiro/aprendizado/` aparecem só no bloco `sdd2` (`:57`), enquanto o README (`:104-106`) diz que
  "projeto configurado com … a v1 do `sdd`" também move `.kiro/produto/` e `.kiro/aprendizado/`.
- **S02-G14 · Toolkit implícito.** `toolkits.md:40-43` cria toolkit sem manifesto por `metadata.toolkit`, mas "detectado"
  (`:90`) e `comandos`/`verificacao`/`steering` só existem em `toolkit.json`. Sem `deteccao`, nenhuma skill implícita fica
  pré-marcada (`SKILL.md:196`); a skill não diz isso.
- **S02-G15 · Backlog mínimo.** `:241-243` cria `backlog.md` só com a tabela `## Épicos`; o formato do `sdd-fatiar`
  (`sdd-fatiar/references/backlog.md:15-36`) também prevê `## Fatias — sem épico` (necessária à `sdd-triar`). Não é erro
  (triar cria), mas o painel e a triagem dependem de seção que a setup não cria. `planejamento/` vazio não vai ao git
  (git não versiona pasta vazia) — a skill não diz para criar `.gitkeep`.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S02-F1 · Primeira configuração (projeto sem sdd)
1. INPUT EXATO: "configurar o sdd"
   ESTADO: repositório git com origin = github.com; KIRO_HOME não definida; power instalado em
   ~/.kiro/powers/installed/sdd/ (com skills/sdd-setup/SKILL.md); SEM .kiro/steering/sdd.md, SEM .kiro/agents/sdd-*.json,
   SEM sdd2*/sdd-projeto.md; pom.xml com Java 21 e spring-batch-core; steering: product.md ✅, tech.md ✅, structure.md ❌;
   SEM docs/glossario.md e SEM docs/adr; SEM power elm e SEM pa_*.json; SEM backlog.md; gh instalado e autenticado;
   mcp.json sem servidor de banco; SEM .kiro/toolkits/; SEM toolkit em ~/.kiro/toolkits.
2. REGRA APLICADA (na ordem em que disparam):
   - SE o pedido é "configurar o sdd" ENTÃO ativa sdd-setup — sdd-setup/SKILL.md:3
   - SE há git ENTÃO raiz = git rev-parse --show-toplevel — :31
   - SE o power está em ~/.kiro/powers/installed/sdd/ com skills/sdd-setup/SKILL.md ENTÃO caminho relativo ao home — :32-35
   - SE KIRO_HOME não definida ENTÃO nenhuma ação extra — :37-39 (ramo só para KIRO_HOME definida)
   - SE sdd.md e sdd-*.json ausentes ENTÃO modo NOVO (complemento implícito de :44) — :44
   - SE sdd2 / sdd-projeto.md ausentes ENTÃO sem migração — :49, :60 (não disparam)
   - Regra geral: padrões decididos sem perguntar, tabela "Padrões aplicados" ao fim de cada bloco, uma confirmação — :20-22
   - Regra geral: pergunta só o que não tem padrão nem dá para detectar — :22-24; não achou → pergunte onde está; nunca "não há"
     sem confirmação — :25-26
   - Passo 1: lê README/AGENTS/build/git log e propõe "🔎 Entendi assim" numa mensagem, com confirmação — :69-82
   - SE sinal de batch (spring-batch-core) ENTÃO tipo "batch" — sdd-setup/references/toolkits.md:27
   - SE structure.md ausente ENTÃO pergunta, um papel por vez, qual arquivo faz o papel (ou oferecer gerar) — :86-88
   - Passo 2: propõe comandos do build e oferece rodá-los uma vez — :94-95
   - Passo 3: branch base via symbolic-ref — :110; prefixo padrão feature/ — :111; PR via gh (origin github) — :113;
     MCP de banco "não há" — :114; artefatos "PR curto para a base" — :115
   - Passo 4.1: sem backlog.md ENTÃO pasta .kiro/planejamento — :120-121
   - Passo 4.2: glossário ausente ENTÃO "o padrão é criá-lo (Padrões aplicados)" — :123-124
   - Passo 4.2 (conflito): glossário ausente = "não achou" ENTÃO pergunte onde está; nunca conclua "não há" — :25-26
   - Passo 4.3: power elm ausente e pa_*.json ausente ENTÃO procura e pergunta qual vale ou se não usa ELM — :126-128
   - Passo 5: sem toolkit ENTÃO diz uma vez e registra "Toolkits: nenhum — <tipo>" — toolkits.md:121-122
3. OUTPUT GERADO (resposta imediata: Passo 1, template literal de :76-81, preenchido):
     🔎 Entendi assim — <projeto>
     Tipos: batch (spring-batch-core em pom.xml)
     Stack: Java 21 · Spring Batch 5
     Testes: JUnit 5
     Steering: product.md ✅ · tech.md ✅ · structure.md ❌
     Está certo? (sim / corrija)
   + pergunta do papel "estrutura" (qual arquivo faz o papel, ou gerar) — ordem em relação ao "Está certo?" não definida.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (no Passo 4.2, quando a pessoa confirmar o Passo 1): sdd-setup/SKILL.md:25-26 ("não achou →
   pergunte onde está") × sdd-setup/SKILL.md:123-124 ("não existindo, o padrão é criá-lo"). O mesmo arquivo ausente leva a
   duas ações diferentes.
   Também, na resposta imediata: AMBÍGUO no formato (:21-22 manda a tabela "Padrões aplicados" ao fim do bloco "projeto"; :81
   pede "Está certo?"). Outros conflitos do fluxo: :26 ("nada é gravado antes do Passo 8 e do ok") × :152-153 (acrescenta ao
   ~/.kiro/settings/mcp.json "com ok" no Passo 4); :299-300 (não altere nada fora de .kiro/…) × :152-153 (mesma escrita).
```

```text
S02-F2 · Atualização da configuração (modo atualização)
1. INPUT EXATO: "atualizar a configuração do sdd"
   ESTADO: .kiro/steering/sdd.md e .kiro/agents/sdd-*.json PRESENTES (versão anterior); sem sdd2*/sdd-projeto.md; power novo
   instalado; sem skills novas.
2. REGRA APLICADA:
   - SE o pedido casa com o gatilho ("atualizar a configuração do sdd") ENTÃO sdd-setup — sdd-setup/SKILL.md:3
   - SE sdd.md OU sdd-*.json existe ENTÃO modo atualização: mostra a configuração atual numa tabela e pergunta o que mudar,
     com a opção "nada — só regenerar os agentes" — :44-46
   - Passo 0 itens 1–3 (raiz, power, caminhos relativos) — :31-43
   - Agentes, hook e workflows SEMPRE a partir dos templates atuais, mesmo os de nome certo — :46-48
   - Mostra o diff de cada arquivo — :48
3. OUTPUT GERADO: tabela "configuração atual" (a skill não define colunas) + pergunta "o que mudar? ('nada — só regenerar os agentes')".
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO. (a) As colunas da tabela não são definidas. (b) Depois da resposta, não há mapa de quais
   passos 1–7 reexecutam: :45-46 manda "refaça só o que mudou nas respostas" sem dizer se relê o repositório (Passo 1),
   reroda comandos (Passo 2) ou reconfirma Git/ELM. Duas leituras dão saídas diferentes.
```

```text
S02-F3 · Migração do sdd2 para o sdd (layout antigo)
1. INPUT EXATO: "atualizar a configuração do sdd"
   ESTADO: PRESENTES .kiro/steering/sdd2.md, sdd2-projeto.md, sdd2-licoes.md, sdd2-fechar-sessao.md; .kiro/agents/sdd2-*.json
   (6); .kiro/hooks/sdd2.json; .kiro/workflows/sdd2-*.workflow.json; .kiro/sdd2/http.sh; .kiro/produto/; .kiro/aprendizado/.
   AUSENTES: sdd.md.
2. REGRA APLICADA:
   - SE o pedido casa o gatilho ENTÃO sdd-setup — :3
   - SE configurado com o nome sdd2 ENTÃO propõe a migração, com o plano numa só mensagem e "ok" — :49-50
   - SE sdd2.md / sdd2-projeto.md ENTÃO valores vão para as seções do novo sdd.md; sdd2-licoes.md → Regras aprendidas — :51-52
   - SE sdd2-fechar-sessao.md ENTÃO removido — :53
   - SE sdd2-*.json ENTÃO removidos (os sdd-*.json são gerados de novo no Passo 8) — :54
   - SE hook/workflows/http.sh sdd2 ENTÃO renomeados para sdd — :55-56
   - SE .kiro/produto e .kiro/aprendizado ENTÃO para a pasta do produto e <produto>/aprendizado — :57
   - Tudo com git mv/git rm, "sem mudar o conteúdo dos movidos" — :58
   - Agentes, hook e workflows SEMPRE a partir dos templates — :47-48 (conflita com :58 só se o hook movido não for regenerado)
   - Nada gravado antes do resumo do Passo 8 e do ok — :26
3. OUTPUT GERADO: mensagem única com o plano de migração (lista de :51-58 preenchida com os arquivos do estado) + "ok?";
   e a tabela de configuração do modo atualização (:44-46).
   ARQUIVOS ESCRITOS: nenhum nesta resposta
4. VEREDITO MECÂNICO: AMBÍGUO. Não se sabe se os git mv/git rm rodam logo após o "ok" do plano (:50, Passo 0) ou só no
   Passo 8. A leitura literal de :26 exige o Passo 8; :50 e :58 não dizem o momento. Subsidiário: :47-48 × :55-56 e :58
   ("sem mudar o conteúdo") são compatíveis só se o hook/workflow movido for regenerado depois.
```

```text
S02-F4 · Migração da v1 do sdd (steering sdd-projeto.md)
1. INPUT EXATO: "configurar o sdd"
   ESTADO: PRESENTE .kiro/steering/sdd-projeto.md; AUSENTE sdd.md; PRESENTES agentes v1 sdd-codificador.json, sdd-revisor.json,
   sdd-orquestrador.json, sdd-especificador.json, .kiro/agents/prompts/sdd-*.md; SEM .kiro/produto/.
2. REGRA APLICADA:
   - SE o pedido é "configurar o sdd" ENTÃO sdd-setup — :3
   - SE sdd-projeto.md existe e sdd.md não ENTÃO OFERECE reaproveitar: steering, branch base, prefixo, padrão de commit,
     ferramenta de PR, comandos, cobertura, banco, testes funcionais, ELM, skills por agente — :60-62
   - Agentes homônimos da v1 (codificador, revisor, orquestrador) ENTÃO substituídos no Passo 8, com diff — :62-64
   - O que só a v1 tinha ENTÃO sai com git rm e "ok": sdd-especificador.json, prompts/sdd-*.md, sdd-projeto.md — :64-65
   - Regra geral: nada gravado antes do resumo do Passo 8 e do ok — :26
3. OUTPUT GERADO: oferta única com a lista de :61-62 ("reaproveitar estes valores do sdd-projeto.md?").
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO. (a) :64-65 diz que a remoção sai "com git rm e 'ok'" sem dizer em que momento; :26 proíbe
   gravar antes do Passo 8, então o "ok" pode ser o do Passo 8 ou um anterior. (b) A seção só diz "ofereça"; não diz que
   depois da oferta o fluxo segue pelos Passos 1–7 (é implícito).
```

```text
S02-F5 · Ligar/atualizar toolkit (skills novas de um toolkit)
1. INPUT EXATO: "ligar o toolkit"
   ESTADO: sdd.md PRESENTE, com coluna "Oferecidas e recusadas" vazia; .kiro/toolkits/spring-batch/toolkit.json com
   tipos-de-projeto ["batch"], deteccao.arquivos ["pom.xml"], deteccao.contem ["spring-batch-core"]; pom.xml CONTÉM
   spring-batch-core; skills spring-batch-job (papeis codificador, revisor), spring-batch-teste (codificador, verificador),
   java (codificador, revisor, pesquisador); sdd-*.json PRESENTES.
2. REGRA APLICADA:
   - SE o pedido é "ligar o toolkit" ENTÃO sdd-setup — :3
   - SE sdd.md existe ENTÃO modo atualização — :44
   - Passo 5: toolkit cujo deteccao casa (arquivo existe E contem aparece) ENTÃO "detectado" — toolkits.md:90; SKILL :166-167
   - Passo 6: para cada agente, nesta ordem (produto primeiro), uma mensagem com a proposta completa — :171, :183-184
   - Pré-marcadas só as skills de toolkits detectados cujo papel inclui o do agente — :196; toolkits.md:98-101
   - Modo atualização: pergunta só sobre as skills NOVAS — toolkits.md:128-130
   - Toolkit nunca é ligado sem o sim, agente por agente — :303
3. OUTPUT GERADO: proposta de sdd-produto: "🤖 sdd-produto — já tem: triar, entrevistar, prd, fatiar, planejamento, atender";
   skills do toolkit spring-batch listadas DESMARCADAS (papel "produto" não está nos papeis); MCPs: nenhum; Modelo: padrão
   do Kiro; "ok?"
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO (escopo da proposta em atualização): sdd-setup/SKILL.md:183-184 pede a proposta completa de
   cada agente × toolkits.md:128-130 pergunta só sobre as skills novas. Leitura compatível: mostra tudo e pergunta só as
   novas; leitura incompatível: mostra só as novas.
```

```text
S02-E1 · Borda: ferramenta de PR ausente
1. INPUT EXATO: (resposta da setup no Passo 3) origin = github.com; "gh" NÃO está no PATH.
   ESTADO: repositório com origin github.com; gh ausente.
2. REGRA APLICADA:
   - SE origin é GitHub ENTÃO abrir PR com gh pr create — sdd-setup/SKILL.md:113
   - SE a ferramenta certa não está no PATH ENTÃO padrão "entregar título e descrição", COM O AVISO de como instalar — :113
     (o exemplo de aviso dado é só para GitLab: "brew install glab" e "glab auth login"; não há texto para GitHub)
3. OUTPUT GERADO: "Abrir PR: entregar título e descrição." + aviso de instalação — o texto do aviso para GitHub não é definido.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO (sdd-setup/SKILL.md:113): a ação é determinada, mas o conteúdo do aviso para GitHub não tem regra.
```

```text
S02-E2 · Negativo: resposta "nada — só regenerar os agentes"
1. INPUT EXATO: "nada — só regenerar os agentes" (resposta à pergunta do modo atualização)
   ESTADO: sdd.md e agentes PRESENTES; versão do power instalado e data de hoje NÃO fornecidas à skill.
2. REGRA APLICADA:
   - SE "nada" ENTÃO refaz só o que mudou nas respostas (nenhum), agentes/hook/workflows a partir dos templates — :45-48
   - Passo 8.1: sdd.md ← template com as respostas; "nada de <…> sobrando" — :232
   - O template do sdd.md traz "Gerado pela sdd-setup (power sdd <x.y.z>) em <AAAA-MM-DD>" — assets/steering/sdd.md:19
   - Passo 8: resumo + diff + "Gravar? ('ok')" — :248-258
3. OUTPUT GERADO: resumo "⚙️ sdd — …" + diff + "Gravar? ('ok')", com <x.y.z> e <AAAA-MM-DD> sem valor.
   ARQUIVOS ESCRITOS: nenhum antes do ok
4. VEREDITO MECÂNICO: SEM REGRA: nenhum trecho diz de onde sair a versão do power (x.y.z) nem a data, e :232 exige que nada
   de "<…>" fique no arquivo. Subsidiário: não está dito se o sdd.md é regenerado quando a resposta é "nada" (:45-46).
```

```text
S02-E3 · Negativo: pessoa recusa o glossário
1. INPUT EXATO: "glossário: não tenho, não quero criar"
   ESTADO: docs/glossario.md AUSENTE; docs/adr AUSENTE; pergunta do Passo 4.2 já feita.
2. REGRA APLICADA:
   - SE a pessoa recusou na tabela ENTÃO registra "não há" e remove {{GLOSSARIO}}/{{ADR}} das regras e linhas dos agentes — :124-125
   - (a pergunta foi feita, então o "não há" tem confirmação — :25-26 satisfeito)
3. OUTPUT GERADO: "Glossário · ADRs: não há" na seção Projeto (template assets/steering/sdd.md:30); linhas com {{GLOSSARIO}}/{{ADR}}
   removidas dos agentes na montagem.
   ARQUIVOS ESCRITOS: nenhum antes do Passo 8 e do ok
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S02-E4 · Borda: KIRO_HOME definida fora do home
1. INPUT EXATO: "configurar o sdd"
   ESTADO: KIRO_HOME=/opt/kiro; power em /opt/kiro/powers/installed/sdd/ (com skills/sdd-setup/SKILL.md).
2. REGRA APLICADA:
   - SE KIRO_HOME definida ENTÃO procura em $KIRO_HOME/powers/installed/sdd/ — sdd-setup/SKILL.md:37-38
   - SE fora do home ENTÃO avisa que os agentes só valem nesta máquina e PEDE "ok" para usar o CAMINHO ABSOLUTO — :38-39
   - SEMPRE caminhos relativos, NUNCA absolutos (ex.: nunca /home/…, /Users/…, variáveis) — :40-43
3. OUTPUT GERADO: pedido de "ok" para caminho absoluto (:38-39) que a regra :40-43 proíbe. Não há saída única.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (sdd-setup/SKILL.md:38-39 × :40-43): o mesmo caso pede um caminho absoluto e proíbe caminho absoluto.
```

```text
S02-E5 · Borda: toolkit implícito (metadata.toolkit sem deteccao)
1. INPUT EXATO: "ligar o toolkit"
   ESTADO: ~/.kiro/skills/acme-java/SKILL.md com metadata.toolkit "acme-java" e papeis ["codificador"]; NENHUM toolkit.json
   ou deteccao; sdd.md presente.
2. REGRA APLICADA:
   - SE skills com metadata.toolkit formam toolkit implícito — sdd-setup/references/toolkits.md:40-43
   - SE o toolkit não tem deteccao ENTÃO não é "detectado" (só deteccao casa e vira detectado) — toolkits.md:90
   - SE o toolkit não está detectado ENTÃO aparece desmarcado — toolkits.md:98-101; sdd-setup/SKILL.md:196
3. OUTPUT GERADO: proposta do sdd-codificador com acme-java [ ] desmarcada.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S02-F1 Primeira configuração | CONFLITO | Glossário ausente: "pergunte onde está" (:25-26) × "criar o padrão" (:123); e :26 × :152-153 |
| S02-F2 Atualização | AMBÍGUO | Colunas da tabela não definidas; não há mapa de quais passos reexecutam (:45-46) |
| S02-F3 Migração sdd2 | AMBÍGUO | git mv/rm após o ok do Passo 0 (:50) ou só no Passo 8 (:26); momento não dito (:58) |
| S02-F4 Migração v1 | AMBÍGUO | "sai com git rm e ok" (:64-65) sem momento; oferta não encadeia os Passos 1–7 |
| S02-F5 Ligar toolkit | AMBÍGUO | Proposta completa por agente (:183) × só skills novas (toolkits.md:128-130) |
| S02-E1 gh ausente | AMBÍGUO | Aviso de instalação só escrito para GitLab (:113) |
| S02-E2 "nada — só regenerar" | SEM REGRA | Versão do power e data (assets/steering/sdd.md:19) sem fonte; :232 proíbe "<…>" |
| S02-E3 Recusa do glossário | DETERMINÍSTICO | Regra explícita "não há" (:124-125) |
| S02-E4 KIRO_HOME fora do home | CONFLITO | Pede "ok" para caminho absoluto (:38-39) × nunca absoluto (:40-43) |
| S02-E5 Toolkit implícito | DETERMINÍSTICO | Sem deteccao nunca é detectado; fica desmarcado (toolkits.md:90, :98-101) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado: commit? quem grava?) | Diretório inacessível / sem permissão / não existe — a skill diz o quê? | Veredito |
|---|---|---|---|---|---|---|---|
| F1, F2, F5 | `.kiro/steering/sdd.md` (SETUP:232; TPL-steering) | Sim: relativo à raiz do repo; P3 não escreveu nada (correto, SETUP:26). Único steering do fluxo (SETUP:269-270) | `.md`, frontmatter `inclusion: always` (TPL-steering:1-3) | Parcial. Seções do template: Projeto, Comandos, Verificação de aceite, Git/banco/autonomia, ELM, Agentes, Regras aprendidas. **Regra "nada de `<…>` sobrando" (SETUP:232) é inexequível**: o template tem `<…>` fixos legítimos (`<origem>/<id>`, `<ft>-<slug>`, `<ft>`, `FT-<nnn>`, `<nn>`, `L-<nnn>`, TPL-steering:14,17,39,78,97,98). `<x.y.z>` e `<AAAA-MM-DD>` (TPL-steering:19) sem fonte indicada (a versão existe em `plugin.json` e `metadata.version`, mas a skill não manda lê-los). Linha do orquestrador na tabela Agentes traz MCP `—` fixo (TPL-steering:91) mas SETUP:199-200 e TPL-steering:71 põem o MCP `elm` nele. Linha do `sdd-produto` traz subagentes `sdd-pesquisador`, `sdd-revisor` (TPL-steering:86) e SETUP:204 diz "só codificador e orquestrador". Tabela-resumo do Passo 8 (`Agente \| Skills extras \| MCPs \| Modelo`, SETUP:254) tem menos colunas que a do template (`… \| Oferecidas e recusadas \| MCP \| Modelo \| Subagentes`) | Quem grava: o agente padrão, com "ok". Em atualização preserva "Regras aprendidas" (SETUP:233-234). Commit: só sugerido (SETUP:291). **Branch do commit NÃO ESPECIFICADA**; push não citado | NÃO ESPECIFICADO (geral). `.kiro/steering/` inexistente: criação implícita, não dita. Arquivo existente editado à mão: só o diff mostrado em atualização (SETUP:248); sobrescrita pergunta só para agentes (SETUP:261) | DIVERGENTE (`<…>` inexequível; MCP do orquestrador `—` × ELM; subagentes do produto; versão/data sem fonte) |
| F1, F2, F4, F5 | `.kiro/agents/sdd-produto.json` · `sdd-pesquisador.json` · `sdd-codificador.json` · `sdd-revisor.json` · `sdd-verificador.json` · `sdd-orquestrador.json` (SETUP:235; `name` = arquivo, SETUP:266) | Sim, relativo à raiz. `{{POWER}}` → `~/.kiro/powers/installed/sdd` (relativo ao home, SETUP:35, 40-43) | `.json`, formato universal V2+V3 em espelho (agentes.md:3-9) | Confere: os 6 templates fazem parse e V2 = V3 em `fs_write`. Placeholders de comandos (compilar/testes/lint/cobertura, SETUP:236 e agentes.md:51) **não têm âncora** nos templates; só `{{POWER}} {{PRODUTO}} {{GLOSSARIO}} {{ADR}} {{SKILLS_EXTRAS}} {{SUBAGENTES}}` existem. Regex (V2) × glob (V3) só tem a nota genérica agentes.md:29. Remover `{{GLOSSARIO}}`/`{{ADR}}` (SETUP:124-125) deixa array JSON com vírgula pendente se for o último item; Passo 9 só pega depois. Texto de comando com `"` ou `\` (Windows) precisa de escape JSON: não dito | Quem grava: agente padrão, com "ok" + uma confirmação do Kiro por arquivo (avisa antes, SETUP:261). Commit sugerido (SETUP:291). Agente existente editado à mão → mostra diff e pergunta (SETUP:261). Permissão do executor: `sdd-codificador` nega `**/.kiro/agents/**`; nenhum agente `sdd-*` tem a setup | NÃO ESPECIFICADO (geral). Pessoa nega a confirmação de um dos 6 → fica configuração parcial; sem regra de recuperação | DIVERGENTE (sem âncora de comandos; escape JSON; regex×glob) |
| F1, F2 | `.kiro/hooks/sdd.json` (SETUP:223-227; automacoes.md:8) | Sim. Só se há compilar+testes (SETUP:223) | `.json` (`{"version":"v1","hooks":[…]}`); valida OK | Confere com o asset: `PostTaskExec`, `timeout 900`, `enabled true`. `({{COMPILAR}} && {{TESTES}}) 1>&2` (hooks/sdd.json:10); multi-módulo sem regra (um par só; automacoes.md:10 "suíte lenta → sugira o conjunto rápido" sem dizer quem decide). Windows: `cmd /c "…"` dentro de JSON exige escape, não dito | Mesmo que acima; Kiro confirma por arquivo em `.kiro/hooks/` (SETUP:262). Commit sugerido | NÃO ESPECIFICADO (geral); IDE/V3 ausente: só avisa que exige IDE ou engine V3 (SETUP:226-227) | OK (sintaxe) com NÃO ESPECIFICADO (multi-módulo, escape) |
| F1, F2 | `.kiro/workflows/sdd-planejar-fatia.workflow.json` e `sdd-entregar-fatia.workflow.json` (SETUP:223-227; automacoes.md:21) | Sim. Só se `kiroAgent.workflows.enabled`/`chat.enableWorkflows` já ligado (SETUP:224-225) | `.json` (`*.workflow.json`); valida OK | Confere. Agentes citados existem no conjunto gerado (`sdd-codificador/revisor/verificador/pesquisador`). Contêm `{{fatia}}` **legítimo** (entrada da receita, minúsculo): uma varredura literal por `{{…}}` (SETUP:266) acusaria falso positivo se aplicada aos workflows; o texto restringe a "JSON de cada agente", mas o resumo diz "nenhum `{{…}}` sobrando" sem escopo | Mesmo que acima; Passo 9 manda `validate_workflow` e, com erro, oferece remover o arquivo (SETUP:276-278) | Parcialmente: erro de validação → oferece remover (SETUP:277-278). Escrita negada/inexistente: NÃO ESPECIFICADO | OK (sintaxe) com ressalva de escopo do `{{…}}` |
| F1, F2 | `.kiro/sdd/http.sh` (SETUP:215-217, 238-240) | Sim. Só se a verificação for por HTTP; o script cita o próprio caminho (`http.sh:3,8,16`) | `.sh` POSIX (`#!/bin/sh`); `sh -n` OK; roda com `sh <arquivo>`, sem `chmod` | Confere: `BASE='{{URL_TESTE}}'` (http.sh:12) é o único placeholder; SETUP:239-240 "sem barra no fim". URL com `'` quebraria o literal (não tratado). Corpo só em `.kiro/specs/*/massa/*` ou `.kiro/local/wt/*/.kiro/specs/*/massa/*` (http.sh:33), coerente com o `fs_write` do verificador | Agente padrão grava; nenhum agente pode alterá-lo (codificador nega `**/.kiro/sdd/**`; orquestrador nega na worktree). Commit sugerido (`.kiro/sdd/`, SETUP:291). Kiro NÃO pede confirmação nessa pasta (SETUP:261-262 não a lista) | URL de teste desconhecida: pergunta (SETUP:217-218); "nenhum" → não instala. Escrita negada: NÃO ESPECIFICADO | OK |
| F1, F2, F5 | `<produto>/backlog.md` (SETUP:241-242). `<produto>` = pasta do `backlog.md` existente, senão `.kiro/planejamento` (SETUP:119-122) | Sim | `.md` | **Diverge do formato real**: SETUP:241-242 cria só `# Backlog — <nome>`, `Próximos ids: EP-01 · FT-001`, `Sustentação: —` e a tabela `## Épicos` vazia. `sdd-fatiar/references/backlog.md:13-35` define também `## Fatias — sem épico` (tabela de 14 colunas), da qual `sdd-triar` e o painel dependem. O cabeçalho da tabela `## Épicos` (`id \| título \| status \| prioridade \| prd \| elm`, backlog.md:21) não é repetido na setup ("tabela vazia") | Agente padrão grava; "só o que não existir" (SETUP:241). **Conflito de branch**: o backlog "só é escrito na base, nunca numa branch de fatia" (`sdd-fatiar/references/backlog.md:6-9`; TPL-steering:61), mas a setup roda na branch em que a pessoa estiver e só "sugere" o commit, sem exigir estar na base nem passar pelo "PR curto para a base" | Pasta do produto inexistente: criada (implícito). Sem permissão: NÃO ESPECIFICADO | DIVERGENTE (backlog mínimo sem `## Fatias — sem épico` nem cabeçalho de colunas; branch de gravação) |
| F1, F2 | `<produto>/planejamento/` (SETUP:243, "`planejamento/`") | Sim | diretório vazio, sem arquivo | Sem estrutura prescrita (os arquivos `acordos.md`, `equipe.json`, `sprints/` são do `sdd-planejamento`) | **Pasta vazia não entra no git** e a skill não manda `.gitkeep`; a sugestão de commit (SETUP:291) lista `<produto>/` mas a pasta some no clone | NÃO ESPECIFICADO | NÃO ESPECIFICADO (pasta vazia não persiste) |
| F1, F2 | `<produto>/aprendizado/licoes.md` (SETUP:243) | Sim; `sdd-aprender` lê o mesmo caminho (`sdd-aprender/SKILL.md:15`) | `.md`, só `# Lições` | Confere com o consumidor: log "só acréscimo" (sdd-aprender:15, 48-54) | Agente padrão grava; branch idem acima | NÃO ESPECIFICADO (geral) | OK |
| F1, F2 | `<produto>/atendimentos/README.md` (SETUP:243-245) | Sim; `sdd-atender` usa `<produto>/atendimentos/README.md` (`sdd-atender/SKILL.md:21,32,38`) | `.md`: `# Atendimentos`, `Próximo: AT-001`, tabela `\| AT \| Pedido \| Situação \|` | Confere com o consumidor (campo `Próximo:`, SKILL sdd-atender:32) | Agente padrão grava; branch idem | NÃO ESPECIFICADO (geral) | OK |
| F1, F2, F5 | `.gitignore` (+ `.kiro/local/`) (SETUP:246) | Sim, raiz | texto | Só acrescenta uma linha "se faltar" | Agente padrão; entra no commit sugerido | `.gitignore` inexistente: NÃO ESPECIFICADO (criar?). Em worktree, `--show-toplevel` aponta para a worktree | NÃO ESPECIFICADO (arquivo ausente) |
| F1 (opcional) | `docs/glossario.md` · `docs/adr/` (SETUP:123-125) | Sim, padrões. P3 S02-E3 correto: recusa → "não há" e remove `{{GLOSSARIO}}`/`{{ADR}}` | `.md` / pasta | **Nenhuma regra diz o que criar** (conteúdo inicial do glossário/ADR), embora o padrão seja "criá-los" (SETUP:124); o Passo 8 (SETUP:231-246) não lista esses arquivos nem como gerados, e SETUP:299 só autoriza "glossário/ADRs que a pessoa pediu para criar" | Sem regra de commit | NÃO ESPECIFICADO | NÃO ESPECIFICADO (criação sem conteúdo nem passo de gravação); também conflito SETUP:25-26 × 123-124 já apontado na P3 |
| F1 | `~/.kiro/settings/mcp.json` (SETUP:152-153) — entrada do `mcp-elm` | **Fora do repo** e fora do que SETUP:299-300 autoriza ("nada fora de `.kiro/`, produto, glossário/ADRs, `.gitignore`"); acontece no Passo 4, **antes** do "ok" do Passo 8 (SETUP:26) | `.json` | Cópia da entrada do `mcp.json` do power `elm`; credenciais ficam em `~/.config/mcp-elm/` (SETUP:153); nenhuma estrutura é especificada | Com "ok" da pessoa (SETUP:152); não versionado (fora do repo) | Arquivo inexistente/inválido/sem permissão: NÃO ESPECIFICADO | DIVERGENTE (SETUP:26 e 299-300 proíbem o que SETUP:152-153 faz; confirma o achado transversal da P3) |
| F1, F2 | Efeitos fora dos arquivos gerados: `kiro-cli settings --workspace chat.disableInheritingDefaultResources true` (SETUP:286-287); exclusão de `.kiro/local/` em tsconfig/jest/lint (SETUP:271-273); `elm-setup` gravando `pa_*.json` (SETUP:130); execução de build/testes (SETUP:94-95) | Fora de `.kiro/` e fora do que SETUP:299-300 lista; Passo 2 e 4 acontecem antes do "Gravar?" | variados | Sem estrutura prescrita | Com "ok" individual (SETUP:272-273, 286-287); o Passo 8 e a sugestão de commit (SETUP:291-292) não os incluem | Falha/sem permissão: NÃO ESPECIFICADO; "registra no `sdd.md` que o loop não deve ser usado" (SETUP:273) é a única saída prevista | DIVERGENTE (SETUP:299-300 × 272-273, 286-287; "nada é gravado antes" × 94-95, 130) |
| F3 (sdd2) | Movidos/removidos: `.kiro/steering/sdd2.md`, `sdd2-projeto.md`, `sdd2-licoes.md`, `sdd2-fechar-sessao.md` → removidos; `.kiro/agents/sdd2-*.json` → removidos; `.kiro/hooks/sdd2.json` → `.kiro/hooks/sdd.json`; `.kiro/workflows/sdd2-*.workflow.json` → `.kiro/workflows/sdd-*.workflow.json`; `.kiro/sdd2/http.sh` → `.kiro/sdd/http.sh`; `.kiro/produto/` → `<produto>/`; `.kiro/aprendizado/` → `<produto>/aprendizado/` (SETUP:51-59) | Sim, relativos à raiz; P3 correta ao não registrar escrita | `git mv`/`git rm` (`mv`/`rm` se não versionado), "sem mudar o conteúdo dos movidos" (SETUP:58) | **Conteúdo movido fica errado**: o workflow `sdd2-*` cita agentes `sdd2-*` (removidos) e o `http.sh` antigo carrega caminhos `sdd2`; SETUP:47-48 manda gerar hook/workflows/http.sh "sempre dos templates atuais" — as duas regras só convivem se o conteúdo for regerado depois do `git mv` (não dito). `.kiro/produto/` → pasta do produto: se já existe `.kiro/produto/backlog.md`, SETUP:119-121 elege essa própria pasta como `<produto>`, e o `git mv` vira auto-movimento ou colisão (não tratado). Passo 9 confere que não sobrou `sdd2*` (SETUP:269-270) mas **não** que os workflows resolvam agentes `sdd-*` além de SETUP:276-277 (confere "agentes citados"; ok) | "ok" ao plano (SETUP:50), mas o **momento** de executar `git mv`/`git rm` não é dito (antes dos Passos 1-7 ou só no Passo 8, SETUP:26). Commit sugerido incluindo "o que a migração moveu ou removeu" (SETUP:291-292); branch não dita | **Árvore suja / arquivos modificados dos que serão movidos**: NÃO ESPECIFICADO. Destino já existente: NÃO ESPECIFICADO. Falha no meio da migração (estado parcial): NÃO ESPECIFICADO | DIVERGENTE (mv "sem mudar conteúdo" × regerar; auto-colisão da pasta do produto) e NÃO ESPECIFICADO (momento, árvore suja, destino existente) |
| F4 (v1) | Removidos: `.kiro/agents/sdd-especificador.json`, `.kiro/agents/prompts/sdd-*.md`, `.kiro/steering/sdd-projeto.md` (SETUP:64-65); substituídos: `sdd-codificador/revisor/orquestrador.json` (SETUP:62-64) | Sim | `git rm` + "ok" | Sem estrutura nova; valores reaproveitados de `sdd-projeto.md` sem formato de origem descrito (SETUP:60-62) | "ok" para `git rm`; momento e branch não ditos | Sem permissão/árvore suja/ausente: NÃO ESPECIFICADO. Pastas `.kiro/produto/` e `.kiro/aprendizado/` da v1: SETUP:60-65 não as migra, mas o README (:104-106) diz que sim | NÃO ESPECIFICADO (momento do `git rm`, pastas da v1) |
| F5 | `.kiro/agents/sdd-*.json` com novos `skill://` e leitura da pasta de skill fora do projeto/power (`~/.kiro/skills/<skill>/**`, `~/.kiro/powers/installed/<toolkit>/**`, agentes.md:50) e `.kiro/steering/sdd.md` (linha Toolkits; colunas "Oferecidas e recusadas") (SETUP:208-209; toolkits.md:126-130) | Sim | `.json` / `.md` | Confere em V2 e V3 se espelhados (agentes.md:9). `steering[]` do toolkit vira `file://` (toolkits.md:92). Para as skills do power `elm`, agentes.md:54 põe `skill://<pasta do power elm>/skills/elm-ccm/SKILL.md` em `resources`, mas a lista de leitura (agentes.md:50) cita só pastas de toolkit/skill, não a do power `elm`: o agente pode listar a skill sem permissão de leitura do arquivo (não verificável aqui) | Agente padrão grava com "ok" por agente (SETUP:303) | Toolkit/skill ausente depois: "skill que sumiu sai do agente com aviso" (toolkits.md:126-130) | OK, com NÃO ESPECIFICADO (leitura da pasta do power `elm`) |

**Atualização (F2)** adiciona: agentes, hook, workflows e `http.sh` sempre regerados dos templates, com diff de cada (SETUP:46-48); `sdd.md` preserva "Regras aprendidas" (SETUP:233-234); `<produto>/` só acrescenta (SETUP:245); sdd.md/agentes editados à mão: o diff é mostrado, mas só os agentes têm "pergunte antes de sobrescrever" (SETUP:261).

---


## S03 · sdd-status

### Parte 2 — Plano do fluxo esperado (Sonnet)


Arquivos lidos: `sdd-status/SKILL.md` (96 l.); sem `references/` nem `assets/`. Cruzados:
`sdd-iniciar/references/status-template.md` (campos/fases do `status.md`),
`sdd-fatiar/references/backlog.md`, `sdd-planejamento/references/arquivos.md`, `sdd-planejamento/SKILL.md:84-92`,
`sdd-iniciar/SKILL.md:19,79`, `sdd-loop/SKILL.md:21,49,122`, `sdd-consolidar/SKILL.md:55,77`.

#### S03-F1 · Painel "onde parei" (somente leitura)
- **Gatilho:** "onde parei", "status", "painel", "bom dia", "o que tem pendente", "qual a próxima fatia",
  "como está a sprint", "retomar" (`sdd-status/SKILL.md:3`: "SEMPRE use esta skill (leia-a antes de responder)").
  Também chamada por outras skills: `sdd-planejamento/SKILL.md:88` ("como está a sprint?"), e a sugestão final de
  `sdd-setup/SKILL.md:295`.
- **Pré-condições / lidos:** `.kiro/steering/sdd.md` (existência, pasta do produto, padrão de commit) (`:12-13`);
  `git fetch --quiet`; `.kiro/specs/*/status.md` da branch atual, de cada worktree (`git worktree list`) e de cada
  branch remota (`git for-each-ref … refs/remotes/origin/`, ignora `HEAD`; `git ls-tree -r --name-only <ref> --
  .kiro/specs/`; `git show <ref>:<caminho>`) (`:17-20`); `tasks.md` de cada fatia (`:23`); `<produto>/backlog.md`
  (da base) (`:24`); `<produto>/planejamento/sprints/sprint-<nn>.md` de maior número com `**Situação:** aberta` (`:25`,
  `:31`); `<produto>/epicos/*/prd.md` (status e `ELM pendente:` do rodapé) (`:27`); `<produto>/planejamento/acordos.md`
  (`:28`); `<produto>/aprendizado/licoes.md` (`:30`); `<produto>/atendimentos/README.md` e `AT-*.md` com
  `**Situação:** aberto` (`:32-33`); `.kiro/local/loop-*.md` (`:34`); `git config user.name` + `equipe.json` (`:35-36`).
- **Processamento:**
  1. Se não existe `.kiro/steering/sdd.md` → vai para S03-F3 (`:13`).
  2. **Coleta** (`:15-36`): como acima. De cada `status.md` extrai fatia, título, trilha, modo, fase, responsável,
     rodadas, achados abertos, PR, ELM, Banco, data da última linha do Histórico e pendências `ELM pendente:` sem
     `ELM feito:` (`:21-22`). De cada `tasks.md`, `[x]`/total e primeiro item pendente (`:23`). Do backlog: épicos por
     status, fatias `pronta` sem `status.md` em nenhuma branch, sprint atual e meta; "em andamento" = fatia com
     `status.md` numa branch e fase ≠ `concluida` (o backlog não guarda isso) (`:24-27`). `acordos.md` ausente → WIP padrão
     "2 fatias esperando pessoa" e sugere `sdd-planejamento` modo inicial (`:28-29`; modo existe em
     `sdd-planejamento/SKILL.md:27`). "Minhas" = responsável igual ao login (`git config user.name` cruzado com
     `nome`/`login` do `equipe.json`); sem correspondência → pergunta o login **uma vez** (`:35-36`).
  3. **Monta o painel** (`:40-64`): cabeçalho (projeto · sprint nn · dias restantes · meta); 🔨 Em andamento (tabela
     FT/Título/Fase/Modo/Tarefas/Achados/PR/Parada há/Próximo passo); 👀 Esperando pessoa (WIP de revisão `<n>/<limite>`
     = `plano-em-revisao` + `aceita` + `pr-aberto`, cada um com a ação e a skill: aprovar o plano (`sdd-plano`), abrir o
     PR (`sdd-implementar`), revisar o PR); ✅ Prontas para começar (por prioridade; Tam./Modo/Depende de); 📄 Produto
     (épicos/PRDs pendentes, especificação na sprint — horas); 🎧 Atendimento (reserva × consumido, abertos);
     🏛️ ELM pendente + 🔁 Lições propostas; ⚠️ Inconsistências; 👉 Sugestão.
  4. **Sugestão** — ordem de prioridade (`:66-68`): (1) desbloquear quem espera pessoa (plano/PR parado, WIP estourado)
     → (2) atendimento com prazo vencendo → (3) terminar a fatia em andamento → (4) começar a próxima pronta (várias AFK
     prontas → oferece `sdd-loop`) → (5) trabalho de produto (PRD/fatiar) para manter o backlog com fatias prontas.
  5. **Inconsistências** (`:70-81`), 10 regras: `pr-aberto` sem PR ou com tarefas pendentes; `concluida` só no
     `status.md` ou só no backlog; fatia em andamento sem commit > 3 dias úteis; `concluida` com Banco `pendente` ou
     `aplicada em dev`; Histórico fora de ordem/fase não bate com a última linha; conceito `elm/` com `verified` humano sem
     `resource` > 1 dia; conceito `elm/` alterado depois do último `verified` ainda `stable`; `backlog.md` alterado numa
     branch de fatia; reserva de atendimento estourada sem decisão do P.O. no `sprint-<nn>.md`; arquivo com dado de
     cliente versionado fora de `.kiro/local/`. Tarefa concluída sem horas **não** é apontada aqui (só na virada da sprint,
     `:83-84`).
- **Resultado:** painel em texto no formato `:40-64`; **nenhum arquivo, branch ou ELM é alterado** (`:12`). Handoff: a
  linha "👉 Sugestão" aponta a skill da próxima ação (sdd-plano/sdd-implementar/sdd-iniciar/sdd-loop/sdd-prd/sdd-fatiar/
  sdd-planejamento).
- **Lacunas:** S03-G1 a S03-G9 (abaixo).

#### S03-F2 · Painel filtrado (sprint / próxima fatia / pendências)
- **Gatilho:** "como está a sprint" (`sdd-status/SKILL.md:3`; `sdd-planejamento/SKILL.md:88`: "`sdd-status` filtrado pela
  sprint (fase de cada fatia, bloqueios, WIP de revisão, PRs parados)"); "qual a próxima fatia"; "o que tem pendente".
- **Pré-condições / lidos:** os mesmos de F1 (a coleta é única); recorte feito na apresentação.
- **Processamento:**
  1. Executa a Coleta inteira (`:15-36`).
  2. Recorta: "como está a sprint" → só fatias com `sprint = <nn atual>` no backlog (fase de cada, bloqueios, WIP, PRs
     parados), mais seções Especificação/Atendimento (reserva × consumido) do `sprint-<nn>.md` aberto;
     "qual a próxima fatia" → a primeira de "✅ Prontas para começar" + sugestão; "o que tem pendente" → 👀 Esperando
     pessoa + 🏛️ ELM pendente + 🔁 Lições + ⚠️ Inconsistências.
  3. Mantém a regra de **Sugestão** (`:66-68`).
- **Resultado:** painel parcial, mesma forma/emoji de F1, somente leitura; handoff igual ao de F1.
- **Lacunas:** S03-G2 (o recorte "filtrado pela sprint" não é definido em `sdd-status`; descrição só diz que a skill
  responde a "como está a sprint"), S03-G3.

#### S03-F3 · Projeto não configurado
- **Gatilho:** qualquer gatilho de S03-F1/F2/F4 sem `.kiro/steering/sdd.md` (`sdd-status/SKILL.md:12-13`).
- **Pré-condições / lidos:** existência de `.kiro/steering/sdd.md`.
- **Processamento:** (1) não existe → (2) "diga que o fluxo não está configurado e ofereça a `sdd-setup`" (`:13`);
  não faz coleta nem painel.
- **Resultado:** mensagem curta + oferta de "configurar o sdd" → `sdd-setup` (S02-F1). Nada gravado.
- **Lacunas:** S03-G10 (o texto não diz o que fazer quando há `sdd-projeto.md`/`sdd2*.md` mas não `sdd.md` — a setup
  trata como migração, `sdd-setup/SKILL.md:49-65`; o status só diz "não está configurado").

#### S03-F4 · Fechar a sessão numa fatia
- **Gatilho:** "fechar a sessão", "encerrar por hoje" (`sdd-status/SKILL.md:3`, `:12`, `:86`).
- **Pré-condições / lidos:** `.kiro/steering/sdd.md` (padrão de commit, `:94`); `.kiro/specs/<ft>-<slug>/status.md` e
  `tasks.md` da fatia da sessão (na branch/worktree atual); `git status`.
- **Processamento:**
  1. **Modo de escrita** (diferente do painel): diz que a sessão fecha para a próxima — "sua, de outra pessoa ou de um
     agente" — retomar sem perder o fio (`:88-89`).
  2. Acrescenta ao **Histórico do `status.md`** o que foi feito, o **próximo passo exato** e as decisões da sessão (`:91-92`;
     histórico é só acréscimo, `status-template.md:39-42`).
  3. Marca no `tasks.md` **só** o que está realmente pronto e verde (`:93`).
  4. Mostra `git status` e **propõe** o commit do que está pronto (mensagem no padrão do `sdd.md`); grava só com "ok";
     **nunca faz push** (`:94-95`).
  5. Termina com a frase para retomar numa sessão nova (ex.: "vamos trabalhar na FT-031") (`:96`) → `sdd-iniciar` retoma pela
     fase (`sdd-iniciar/SKILL.md:38`).
- **Resultado:** `status.md` (Histórico) e `tasks.md` alterados na pasta `.kiro/specs/<ft>-<slug>/`; commit local só com
  "ok"; sem push; resposta com a frase de retomada. Handoff: `sdd-iniciar` na próxima sessão.
- **Lacunas:** S03-G4 a S03-G8 (abaixo).

#### Lacunas observadas — S03
- **S03-G1 · Fase `bloqueada` ignorada.** O `status-template.md:18-20` define `bloqueada (de: <fase>)` com motivo e
  pergunta exata, e o `sdd-planejamento/SKILL.md:88` promete "bloqueios" no painel; mas `sdd-status/SKILL.md:40-64` não tem
  seção/coluna para bloqueadas (nem entram em "Esperando pessoa" `:46`, que só soma 3 fases, nem em "Inconsistências"
  `:70-81`). Uma fatia bloqueada pelo loop (`sdd-codificador.json:4`: "bloqueio → `fase: bloqueada`") só aparece como linha
  de "Em andamento" sem destaque/pergunta pendente.
- **S03-G2 · Filtro "como está a sprint" não definido.** `sdd-planejamento/SKILL.md:88` chama o painel "filtrado pela
  sprint"; `sdd-status/SKILL.md` não descreve esse modo (apenas lista o gatilho no `:3`). Falta dizer qual sprint (a atual
  `aberta`, `:25`), e se inclui fatias `→ sprint <nn+1>`.
- **S03-G3 · Kanban / sem sprint / "dias restantes".** O cabeçalho (`:41`) assume "sprint <nn> (<dias> dias restantes)",
  mas em Kanban (`sdd-iniciar/SKILL.md:75`, `sdd-loop/SKILL.md:28`) não há sprint e em projeto sem planejamento
  (`acordos.md` ausente, `:28-29`) também não; o texto não diz como imprimir. Também não diz de onde vêm os "dias
  restantes" (o cabeçalho do `sprint-<nn>.md` traz `<início> → <fim>`, `sdd-planejamento/references/arquivos.md:106`).
- **S03-G4 · Fechar sessão: qual fatia?** Texto fala em "o `status.md` da fatia" (`:91`) sem dizer como achá-la: branch
  atual? se há várias pastas em `.kiro/specs/`? e se a sessão está na branch base, numa sessão de produto/atendimento
  (sem `status.md`, p.ex. `sdd-prd`, `sdd-atender`, `sdd-triar`), ou numa worktree do loop? Trilha **direta** não tem
  `tasks.md` ("pasta tem só o `status.md`", `sdd/SKILL.md:27`; `sdd-iniciar/SKILL.md:53`), então o passo 2 (`:93`) fica sem
  alvo e não é dito para ignorá-lo.
- **S03-G5 · Agente dono do "fechar a sessão".** A skill escreve arquivos e faz commit, mas só `sdd-orquestrador` a carrega
  (`sdd-setup/assets/agents/sdd-orquestrador.json:19`); `sdd-codificador` (quem conduz a sessão da fatia,
  `assets/agents/sdd-codificador.json:15-17`) e `sdd-produto` **não** a têm, e o prompt do codificador não menciona
  "fechar sessão". O `sdd.md` gerado diz "fechar a sessão: `sdd-status`" (`assets/steering/sdd.md:10`). Em sessão com o
  agente `sdd-codificador` do projeto, o comando "encerrar por hoje" pode não achar a skill. (Além disso, o orquestrador
  usa o painel para decidir o lote, mas nunca fecha sessão de pessoa.)
- **S03-G6 · "Somente leitura" × escrita.** `:12` ("não altera arquivo, branch nem ELM") e a description
  ("somente leitura") coexistem com o modo que grava; é declarado como exceção ("Pedido de fechar a sessão → modo da última
  seção"), mas a description não avisa que a skill pode gravar `status.md`/`tasks.md` e fazer `git add/commit` — o
  agente com permissão de leitura pode ser carregado só para "painel". Conflito com princípio "grave só com ok".
- **S03-G7 · Fechar a sessão não cobre o que a fase exige.** Não manda atualizar a **Fase** do `status.md` (só Histórico),
  nem registrar `ELM pendente:` da sessão (`status-template.md:39-40`), nem as Rodadas; não diz o que fazer com achados
  abertos em tabela `## Achados abertos`; não cita a regra "commit pequeno do `status.md`" nem em qual branch (branch da fatia;
  `status.md` na base seria "inconsistência", `:79`). Também não diz que, em fatia `plano-em-revisao`/`aceita`, o "próximo
  passo exato" é de outra pessoa (e a quem avisar).
- **S03-G8 · Commit sem política de escopo.** `:94` "propõe o commit do que está pronto (padrão do `sdd.md`)": o padrão
  (`assets/steering/sdd.md:59`, ex.: `FT-<nnn> <verbo> <descrição>`) existe, mas não diz como tratar mudanças não prontas
  no `git status` (stash é negado nos agentes `agentes.md:80-81`; `git add .*` permitido) nem se o commit do `status.md`
  deve ir separado do código (compare `sdd-implementar/SKILL.md:22`: "registrar revisão/verificação" em commit próprio).
- **S03-G9 · Fatia presente em várias refs.** A coleta (`:17-20`) lê `status.md` da branch atual + worktrees + remotas,
  mas não define a regra quando a **mesma fatia** aparece em várias (branch local, `origin/<branch>`, worktree) com fases
  diferentes, nem quando a branch da fatia ficou remota após o merge com `fase: pr-aberto` e a base já tem `concluida`
  (`sdd-consolidar/SKILL.md:77` grava `concluida` na base depois do merge): vira falso "em andamento"/"esperando pessoa".
  Também "Histórico fora de ordem … (conflito mal resolvido)" (`:76`) não diz qual ref comparar.
- **S03-G10 · Fichas, gates e fatias não prontas fora do painel.** O fluxo tem gate de Ficha (`sdd/SKILL.md:52`) e GATE do
  backlog (`:51`), e o backlog guarda fatias `backlog` com `falta:` (`sdd-fatiar/references/backlog.md:49,51`) e épicos
  `aprovado` aguardando fatiar; o painel só lista PRDs `em-revisao`/"a descobrir" (`:55`) e fatias `pronta` (`:51-52`): não
  mostra fichas aguardando aprovação do P.O., fatias sem épico em `backlog` com `falta:`, épicos `aprovado` sem fatiar, nem
  `AT` triados não iniciados. A "Sugestão" (`:66-68`) cobre "PRD/fatiar" só genericamente.
- **S03-G11 · "Minhas" sem uso.** `:35-36` define "minhas" (cruza `git config user.name` com `equipe.json`), mas o formato do
  painel (`:40-64`) não usa a noção (nenhuma coluna/filtro/destaque), e o caminho do `equipe.json`
  (`<produto>/planejamento/equipe.json`, `sdd-planejamento/SKILL.md:23`) não é citado em `sdd-status`. Além disso
  `equipe.json` ausente é tratado apenas por "sem correspondência, pergunte o login".
- **S03-G12 · Colunas do painel sem fonte clara.** "Parada há" é a data da última linha do Histórico (`:22`), mas a
  inconsistência "sem commit há mais de 3 dias úteis" (`:74`) usa commit (fonte distinta e não coletada em `:15-36`).
  "Depende de" (`:52`) vem de `bloqueada-por`, mas a tabela "sem épico" do backlog **não tem** essa coluna
  (`sdd-fatiar/references/backlog.md:33`). "Tam." só existe no backlog.
- **S03-G13 · Permissões dos agentes para a coleta.** A coleta usa `git fetch`, `git worktree list`,
  `git for-each-ref`, `git ls-tree`, `git show <ref>:…` e `git config user.name` — todos presentes no `sdd-orquestrador`
  (`assets/agents/sdd-orquestrador.json:58-80`) e no codificador (`:57-75`), mas `git fetch` altera refs locais, o que
  conflita com a frase "não altera … branch" (`sdd-status/SKILL.md:12`) na leitura literal.

### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S03-F1 · Painel "onde parei" (somente leitura)
1. INPUT EXATO: "onde parei?"
   ESTADO: branch main; worktrees: só a principal; .kiro/steering/sdd.md PRESENTE (pasta do produto .kiro/planejamento);
   branches remotas com status.md: feature/FT-031-cadastro (fase "implementar", responsável ana, tarefas 4/9);
   feature/FT-030-relatorio (fase "aceita"); feature/FT-029-export (fase "pr-aberto", PR com link, tarefas 7/7).
   Backlog: FT-031 em andamento; sprint-03 aberta com meta; acordos.md com WIP 2; licoes.md com 1 lição "proposta";
   sem atendimentos; sem .kiro/local/loop-*.md; git config user.name = "ana"; equipe.json com login "ana".
2. REGRA APLICADA:
   - SE o pedido é "onde parei" (gatilho) ENTÃO usa sdd-status — sdd-status/SKILL.md:3
   - SE sdd.md ausente ENTÃO "não configurado" — :12-13 (não dispara: sdd.md presente)
   - SE não é fechar a sessão ENTÃO painel somente leitura — :12
   - git fetch --quiet — :17
   - Coleta de status.md na branch atual, nas worktrees e nas branches remotas — :17-20
   - De cada status.md: fatia, título, trilha, modo, fase, responsável, rodadas, achados, PR, ELM, Banco, data do Histórico — :21-22
     (o formato do status.md não é citado por esta skill: o parse depende de convenção não escrita)
   - De cada tasks.md: [x]/total e primeiro pendente — :23
   - backlog: épicos, fatias pronta sem status.md, sprint aberta de maior número, meta — :24-25
   - acordos.md: limite de WIP = 2 — :28
   - licoes.md: lições "proposta" — :30
   - Sprint aberta: ELM pendente — :31
   - "Minhas": git config user.name cruzado com equipe.json — :35-36 → "ana" casa
   - Painel no formato de :40-64
   - Esperando pessoa: aceita → "abrir o PR (sdd-implementar)" — :48 (exemplo); pr-aberto → "revisar o PR <link>" — :49 (exemplo, SEM skill)
   - WIP de revisão = plano-em-revisao + aceita + pr-aberto = 2 (limite 2) — :46
   - Sugestão: (1) desbloquear quem espera pessoa (plano ou PR parado) — :66-67
   - Inconsistências: nenhuma (FT-029 pr-aberto com PR e tarefas 7/7) — :70-81
3. OUTPUT GERADO: painel no formato de :40-64, com "sprint 03 (<dias> dias restantes)"; "Esperando pessoa (WIP 2/2)":
   "- FT-030 aceita → abrir o PR (sdd-implementar)" e "- FT-029 pr-aberto há 2 dias → revisar o PR <link>";
   "👉 Sugestão: abrir o PR da FT-030 (sdd-implementar)".
   ARQUIVOS ESCRITOS: nenhum (somente leitura; git fetch atualiza só refs remotas)
4. VEREDITO MECÂNICO: SEM REGRA: (a) "revisar o PR" não tem skill indicada (:49; a skill só aparece nos exemplos :47-48);
   (b) "<dias> dias restantes" não tem fonte no SKILL (:41); (c) "PR parado" (:66) não tem limiar. Subsidiário: :12
   ("não altera … branch") × :17 (git fetch atualiza refs/remotes/origin/*), que é leitura de ref, não alteração de branch local.
```

```text
S03-F2 · Painel filtrado (sprint / próxima fatia / pendências)
1. INPUT EXATO: "como está a sprint?"
   ESTADO: o mesmo de S03-F1.
2. REGRA APLICADA:
   - SE o pedido casa o gatilho "como está a sprint" ENTÃO usa sdd-status — sdd-status/SKILL.md:3
   - SE há um modo de recorte pela sprint ENTÃO aplica o recorte — NÃO HÁ regra: sdd-status só define o painel completo (:40-64)
     e a Sugestão (:66-68)
3. OUTPUT GERADO: leitura A: painel completo (única forma definida em :40-64). Leitura B: recorte só das fatias da sprint
   (não definido). ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO: sdd-status/SKILL.md:3 lista "como está a sprint" como gatilho, mas sem modo filtrado. Duas leituras
   (painel inteiro × recorte) geram saídas diferentes.
```

```text
S03-F3 · Projeto não configurado
1. INPUT EXATO: "onde parei?"
   ESTADO: .kiro/steering/sdd.md AUSENTE; nenhum .kiro/agents/sdd-*.json.
2. REGRA APLICADA:
   - SE o pedido é "onde parei" ENTÃO usa sdd-status — :3
   - SE sdd.md ausente ENTÃO "diga que o fluxo não está configurado e ofereça sdd-setup"; não faz coleta nem painel — :12-13
3. OUTPUT GERADO: "O fluxo sdd não está configurado neste projeto. Quer que eu configure com a sdd-setup?"
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S03-F4 · Fechar a sessão numa fatia
1. INPUT EXATO: "fechar a sessão"
   ESTADO: branch feature/FT-031-cadastro (worktree principal); .kiro/steering/sdd.md PRESENTE, com padrão de commit
   "FT-<nnn> <verbo> <descrição>"; .kiro/specs/FT-031-cadastro/ com status.md (fase implementar) e tasks.md (4 de 9
   marcadas); a sessão fez o endpoint de cadastro e os testes do item 5 passaram; git status com 2 arquivos modificados e 1 novo.
   Esta é a ÚNICA pasta de spec na branch atual.
2. REGRA APLICADA:
   - SE o pedido é "fechar a sessão" ENTÃO modo de escrita (exceção à regra "somente leitura") — :12, :88-89
   - Passo 1: acrescenta ao Histórico do status.md da fatia: o que foi feito, próximo passo exato, decisões — :91-92
     (a fatia é a única pasta da branch atual; a regra de escolha da fatia não está escrita)
   - Passo 2: marca no tasks.md só o que está "realmente pronto e verde" — :93
   - Passo 3: mostra git status; propõe commit no padrão do sdd.md; grava só com "ok"; nunca faz push — :94-95
   - Passo 4: termina com a frase para retomar — ex.: "vamos trabalhar na FT-031" — :96
3. OUTPUT GERADO: Histórico do status.md acrescido; tasks.md com itens marcados; git status; "Proposta de commit:
   FT-031 <verbo> <descrição>. Grava? (ok)"; "Para retomar: vamos trabalhar na FT-031".
   ARQUIVOS ESCRITOS: .kiro/specs/FT-031-cadastro/status.md · Histórico (acréscimo) · markdown; .kiro/specs/FT-031-cadastro/tasks.md ·
   checkboxes · markdown. O commit só depois do "ok" (não há commit sem ok).
4. VEREDITO MECÂNICO: AMBÍGUO: "realmente pronto e verde" (:93) não diz como verificar o verde (nenhum comando de teste é
   citado nesta skill; sdd.md não é lido em outro ponto). Leitura A: confirmar pelo teste; leitura B: confiar no relato da
   sessão. Saídas diferentes em tasks.md.
```

```text
S03-E1 · Pré-condição: sdd2 presente e sdd.md ausente
1. INPUT EXATO: "onde parei?"
   ESTADO: .kiro/steering/sdd2.md PRESENTE; .kiro/steering/sdd.md AUSENTE.
2. REGRA APLICADA:
   - SE sdd.md ausente ENTÃO "não está configurado"; ofereça sdd-setup — sdd-status/SKILL.md:12-13
3. OUTPUT GERADO: "O fluxo sdd não está configurado neste projeto. Quer que eu configure com a sdd-setup?"
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO (a regra não distingue sdd2 de ausência total; a migração é tratada pela sdd-setup).
```

```text
S03-E2 · Borda: fechar a sessão em branch base sem fatia
1. INPUT EXATO: "fechar a sessão"
   ESTADO: branch main; .kiro/steering/sdd.md PRESENTE; nenhuma pasta .kiro/specs/*/ na branch atual; a sessão foi de produto
   (escreveu o PRD do EP-04 em <produto>/epicos/EP-04-…/prd.md).
2. REGRA APLICADA:
   - SE o pedido é "fechar a sessão" ENTÃO modo de escrita — :12, :88
   - "Ao encerrar uma sessão numa fatia" ... — :88 (pressupõe fatia)
   - Passo 1 pede "o status.md da fatia" — :91 (sem regra para achar a fatia quando não há nenhuma)
3. OUTPUT GERADO: nenhum output definido.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: SEM REGRA: a skill não trata sessão sem fatia (produto ou branch base). Não há ramo para o caso.
```

```text
S03-E3 · Negativo: pedido de push junto com o fechamento
1. INPUT EXATO: "fecha a sessão e já dá push"
   ESTADO: igual a S03-F4.
2. REGRA APLICADA:
   - SE o pedido é "fechar a sessão" ENTÃO modo de escrita — :12, :88
   - SE há pedido de push ENTÃO nunca faz push; grava só com "ok" — :94-95
3. OUTPUT GERADO: o fechamento de S03-F4 sem push; a resposta diz que o push não é feito pelo agente.
   ARQUIVOS ESCRITOS: como em S03-F4 (status.md, tasks.md); commit só com "ok"; nenhum push
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S03-E4 · Borda: "retomar" nos dois gatilhos
1. INPUT EXATO: "retomar a FT-031"
   ESTADO: .kiro/steering/sdd.md PRESENTE; FT-031 em andamento.
2. REGRA APLICADA:
   - SE o pedido contém "retomar" ENTÃO "SEMPRE use esta skill" (sdd-status) — sdd-status/SKILL.md:3
   - SE o pedido é "começar ou retomar um trabalho já registrado" ENTÃO sdd-iniciar — sdd/SKILL.md:81
     (sdd-status não cita sdd/SKILL.md; o conflito vem de duas descrições do mesmo power)
3. OUTPUT GERADO: duas skills possíveis (painel de status ou sdd-iniciar). Nenhuma prioridade escrita.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (sdd-status/SKILL.md:3 × sdd/SKILL.md:81).
```

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S03-F1 Painel "onde parei" | SEM REGRA | "Revisar o PR" sem skill (:49); "dias restantes" sem fonte (:41); "PR parado" sem limiar (:66) |
| S03-F2 Painel "como está a sprint" | AMBÍGUO | Modo filtrado citado em :3 mas não definido; só o painel completo existe |
| S03-F3 Projeto não configurado | DETERMINÍSTICO | Regra explícita (:12-13) |
| S03-F4 Fechar a sessão | AMBÍGUO | "Pronto e verde" (:93) sem critério; fatia-alvo sem regra de escolha |
| S03-E1 sdd2 sem sdd.md | DETERMINÍSTICO | Mesma regra de ausência (:12-13) |
| S03-E2 Fechar sessão sem fatia | SEM REGRA | Só trata "numa fatia" (:88); nada para sessão de produto |
| S03-E3 Pedido de push | DETERMINÍSTICO | Negativa explícita (:94-95) |
| S03-E4 "Retomar a FT-031" | CONFLITO | sdd-status:3 ("SEMPRE use" retomar) × sdd:81 (retomar → sdd-iniciar) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


Sem escrita: S03-F1 (painel), S03-F2 (painel filtrado), S03-F3 (não configurado), S03-E1, S03-E4. Todas as três usam `git fetch --quiet` (STATUS:17), que
escreve em `.git` (`refs/remotes/origin/*`, `FETCH_HEAD`, objetos) embora STATUS:12 diga "não altera arquivo, branch nem ELM". A P3 registra "nenhum
(git fetch atualiza só refs remotas)": correto em substância, mas o "nenhum" é literalmente falso (ver achados). Permissão do agente que carrega a skill
(`sdd-orquestrador`): `git fetch*` está em `shell allow` (orquestrador.json:79, V3 :172), `git show`, `git ls-tree`, `git for-each-ref`, `git worktree list`
também; leitura de `./**` liberada, `.env/.pem/.key` negados.

| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado: commit? quem grava?) | Diretório inacessível / sem permissão / não existe — a skill diz o quê? | Veredito |
|---|---|---|---|---|---|---|---|
| F4 (S03-F4, S03-E3) | `.kiro/specs/<ft>-<slug>/status.md` (STATUS:91). Acréscimo no **Histórico** | **P3 escreveu `.kiro/specs/FT-031-cadastro/` (maiúsculo): não confere.** A convenção do power é `<ft>` minúsculo: branch `feature/ft-031-…` (`sdd-iniciar/SKILL.md:91`), pasta localizada por "id em minúsculas (ex.: ft-031-…)" (`workflows/sdd-planejar-fatia.workflow.json`, passo `pesquisa`), exemplo `.kiro/specs/ft-031-saldo/massa/…` (`http.sh:8`). STATUS não define `<ft>`; escolha da fatia (branch atual? várias pastas? worktree do loop `.kiro/local/wt/<ft>/.kiro/specs/…`?) **NÃO ESPECIFICADA** (STATUS:91). Caminho relativo à raiz do checkout/worktree atual | `.md`. Formato da linha: o template é `- <AAAA-MM-DD HH:MM> — <texto>` (`sdd-iniciar/references/status-template.md:42`; `sdd-implementar/SKILL.md:47`), mas STATUS **não o cita** | Parcial. STATUS:91-92 manda registrar "o que foi feito, próximo passo exato, decisões", mas não manda tocar na **Fase**, **Rodadas**, tabela "Achados abertos" nem `ELM pendente:` (status-template.md:18-27, 29-40), nem diz que histórico é "só acréscimo, sempre no fim" (status-template.md:39) | Quem grava: o agente da sessão; **só o `sdd-orquestrador` carrega a skill** (orquestrador.json:19). Permissões do orquestrador: `.kiro/specs/**` e `.kiro/local/wt/*/.kiro/specs/**` liberados (fs_write allow, V2 e V3). `sdd-codificador` (quem conduz a fatia) escreve em `./**` mas não tem a skill; `sdd-produto` só grava `decisoes.md` em `.kiro/specs/*/` (não `status.md`). Commit: "propõe" e grava só com "ok", **nunca push** (STATUS:94-95); mensagem no padrão do `sdd.md`. **Branch: NÃO ESPECIFICADA** (a de `sdd-iniciar:115` é a da fatia; `backlog.md`/`status.md` na base é inconsistência, STATUS:79); commit do `status.md` separado do código: não dito (`sdd-implementar` registra em commit próprio) | `status.md` inexistente (branch base, sessão de produto/atendimento, `.kiro/specs/` ausente) → **NÃO ESPECIFICADO** (P3 S03-E2 correto: SEM REGRA). Árvore suja, hook/pré-commit recusando, `git add .*` que pega arquivo indevido: NÃO ESPECIFICADO. Permissão negada (ex.: sessão com `sdd-produto`): NÃO ESPECIFICADO | DIVERGENTE (P3 usou caminho maiúsculo) e NÃO ESPECIFICADO (fatia-alvo, branch do commit, ausência do arquivo, formato da linha) |
| F4 | `.kiro/specs/<ft>-<slug>/tasks.md` (STATUS:93): só marca `[x]` do que está pronto e verde | Idem `status.md` | `.md` com checkboxes | Confere: marca/desmarca checkbox, não cria tarefas. **Trilha direta não tem `tasks.md`** (`sdd-iniciar/SKILL.md:53,98`; `sdd-implementar/SKILL.md:123`) e STATUS:93 não diz para pular; tarefas `[R<n>]` de achados também moram aqui (sdd-implementar:26) | Mesmo executor e commit que `status.md`; permissões idênticas | `tasks.md` ausente: NÃO ESPECIFICADO (direta). "Pronto e verde" sem comando para conferir (STATUS:93) | NÃO ESPECIFICADO (direta; critério de "verde") |
| F4 | Commit local na branch atual (sem arquivo novo) (STATUS:94-95) | Sim | objeto git | Padrão do `sdd.md` seção "Branch base · prefixo · commit" (TPL-steering:59) | `git add`/`git commit` liberados no orquestrador (`git add .*`, `git commit .*`, orquestrador.json:77-78) e no codificador; push é `ask` no orquestrador (`git push *`, V3) e **negado** nos demais: STATUS diz "nunca" (mais restritivo que o agente) | Ver acima | OK (confirma P3 S03-E3: sem push) |

---


## S04 · sdd-triar

### Parte 2 — Plano do fluxo esperado (Sonnet)


Leituras comuns a todos os fluxos: `.kiro/steering/sdd.md` (sem ele → oferece `sdd-setup` e para, triar:20); formato do
backlog (`../sdd-fatiar/references/backlog.md`, triar:21); `references/ficha.md` (triar:22). Antes de tudo: estar na base,
`git pull --ff-only`, árvore limpa (triar:26-28).

#### S04-F1 · Triagem de entrada única (pedido em texto ou número do EWM) + checagem de duplicado
- **Gatilho:** "nova demanda", "chegou um pedido", "o cliente pediu", "nova funcionalidade", "registra o defeito 4567",
  "coloca no backlog", "triagem" (triar:3). Também evento: chamada pela `sdd-iniciar` com pedido/id fora do backlog
  (iniciar:35), pela `sdd-atender` (atender:29), pelo `sdd-implementar` (melhoria vista no caminho → item de backlog).
- **Pré-condições / lê:** `sdd.md`; base atualizada; `backlog.md`; `<produto>/atendimentos/AT-*.md` (`**Origem:**`);
  `status.md` de todas as branches (`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`) (triar:37-39); para número
  do EWM, skill `elm-ccm` (`ccm_get_workitem`, com descrição e comentários); sem o power → pede título, descrição e
  comportamento esperado, nunca inventa (triar:33).
- **Processamento:**
  1. Passo 1: fora da base → "Troco para `<base>` para triar? (sim)" e, no fim, oferece voltar; `git pull --ff-only`;
     alterações locais não commitadas → avisa e **para** (nunca stash/reset/descartar) (triar:26-28).
  2. Lê a entrada (tabela triar:30-35). "importar do EWM"/"triar os defeitos do time" → vai para **S04-F9**; pedido de
     cliente sem mudança no repositório → trilha atendimento (**S04-F7**).
  3. "Já existe?" — procura por `FT`/`EP`, colunas `origem`/`elm`, títulos parecidos, `**Origem:**` dos AT e `status.md`
     das branches (triar:37-39). Achou → mostra a linha e: fatia sem épico que volta para cá → **S04-F2**; qualquer outro
     caso → para e manda para `sdd-iniciar` (começar/retomar) ou `sdd-fatiar` (mudar fatia de épico) (triar:45-46).
  4. Passo 2: classifica (tabela triar:50-56) e diz "trilha + motivo numa linha"; dúvida entre duas → pergunta sim/não
     pela mais leve; padrão com > ~3 cenários de comportamentos diferentes ou > 1 regra nova independente → épico
     (triar:59-60). Fatia de épico não passa por aqui (triar:58). Segue para **S04-F3/F4/F5/F6/F7/F8**.
  5. Passo 3 (registrar) e Passo 4 (encaminhar) conforme a trilha.
- **Resultado:** bloco `📥 <FT-nnn|EP-nn|AT> — título · trilha · pronta|backlog: falta … · modo …` / `Origem … · Ficha … ·
  EWM …` / `Próximo: …` (triar:110-114) + pergunta "começa agora?" (triar:123).
- **Lacunas:** ver S04-F2 (ordem retomada × iniciada). Triar:26-28 exige trocar de base e árvore limpa mesmo quando nada
  será escrito (atendimento, "não fazer"): bloqueia a pessoa que está no meio de uma fatia com árvore suja só para uma
  triagem somente-leitura.

#### S04-F2 · Retomada da triagem de fatia sem épico que volta para cá
- **Gatilho:** "aprova a ficha da FT-040" (triar:3), "retomar a triagem", ou evento: fatia `backlog` com `falta:`,
  ficha `rascunho`/a aprovar, mudança pedida na ficha, ficha devolvida pela `sdd-plano`/`sdd-consolidar`, trilha que não
  serve devolvida pela `sdd-iniciar` (iniciar:46-47) ou `sdd-implementar` (trilha direta, implementar "Trilha direta").
- **Pré-condições:** linha existente em `## Fatias — sem épico`; ficha `<produto>/fatias/FT-<nnn>-<slug>.md`.
- **Processamento (triar:40-44):**
  1. Reabre o Passo 2 **com o mesmo FT** e a ficha existente; reavalia trilha.
  2. Entrevista/aprovação conforme a trilha (F4/F5/F6) sobre a ficha que já existe.
  3. Passo 3: **só atualiza a linha** (sem id novo; "Próximos ids" não cresce).
  4. Virou épico → `EP-nn` novo (Passo 3 épico), a fatia vira `cancelada` com `obs` `substituida-por EP-nn` (triar:43-44).
  5. Regra de ficha aprovada: só muda por pedido explícito → volta a `rascunho`, mostra a diferença, pede nova aprovação;
     fatia já iniciada que dependa da mudança → avisa quem a conduz (triar:160-161).
- **Resultado:** linha do backlog atualizada (`status` `pronta` se a ficha ficou aprovada; senão `backlog`/`falta:`), ficha
  atualizada (`Situação: aprovada por <login> em <data>`), commit pequeno na base; bloco 📥 e "Próximo" (triar:116-121).
- **Lacunas:**
  - **Ordem ambígua** triar:40-46: uma fatia com `status.md` em branch (já iniciada) cujo ficha precisa mudar casa ao mesmo
    tempo com "volta para cá → retome" (41-44) e com "o resto → pare: começar ou retomar é na sdd-iniciar" (45-46);
    triar:160-161 supõe o caso mas o Passo 1 não diz como detectá-lo nem o que fazer com `status.md`/PR já existentes.
  - **Aprovação sem procedimento:** o gatilho "aprova a ficha da FT-040" (triar:3) não tem passo próprio; ninguém define como
    o agente descobre o `<login do P.O.>` (ficha:46) nem como confirma que quem fala é o P.O. (steer não traz papel/P.O.;
    `sdd-status:36` usa `git config user.name` × `equipe.json` só para "minhas"). Risco de ficha "aprovada" pelo próprio dev.
  - Fatia cancelada por virar épico: `backlog:48` só prevê `substituida-por FT-…` (aqui `EP-nn`); destino da ficha e do IB
    já criado no EWM (triar:95-98) não é dito (fica órfão).

#### S04-F3 · Trilha épico
- **Gatilho:** triagem (F1) conclui "funcionalidade nova com várias histórias/fatias, > ~3 dias, mais de um objetivo ou
  decisão de produto em aberto" (triar:52). Frase típica: "nova funcionalidade …".
- **Pré-condições:** base limpa; "Próximos ids" do `backlog.md`; ELM: `sdd.md` → `Usa ELM`, tipo de épico (`épico <Épico | Item
  de Backlog (pai)>`, steer:76).
- **Processamento (triar:77-83):**
  1. Próximo `EP-nn`; linha em `## Épicos`: `status` `rascunho`, prioridade `—`, `prd` `—`.
  2. Com ELM: `sdd-elm` modo *backlog*, só o épico (`[EP-nn] <título>`, descrição = o problema), **com confirmação**; id na coluna `elm`.
  3. Se veio de um item do EWM: se ele já é do tipo de épico do `sdd.md` → ele é o épico (grava o id, não cria outro);
     quando esse tipo é o mesmo do item (Item de Backlog pai) → **pergunta** se vira o épico ou o filho; senão cria o épico
     e o item de origem vira filho, na mesma confirmação.
  4. Sem MCP → `elm` = `pendente`.
  5. "Próximos ids"; commit pequeno só com o `backlog.md`; push/PR com "sim"; conflito de id → **S04-F11**.
- **Resultado:** linha `EP-nn` `rascunho` no `<produto>/backlog.md`; bloco 📥 com `EWM: <id|criado|pendente|sem ELM>`;
  `Próximo`: "especificar agora (`sdd-prd` com o `EP-nn`) ou deixar para o planejamento (seção Especificação da sprint)" (triar:118).
- **Lacunas:** no lote (S04-F9) a pergunta "épico ou filho" (triar:81) contradiz "uma confirmação para o lote" (triar:137-138);
  nenhum item de EWM tem o título `[EP-` antes do fluxo, então a regra "fora do lote: título com `[EP-`" (triar:133) não pega
  épicos criados à mão no EWM com tipo Épico — não bloqueante.

#### S04-F4 · Trilha padrão (fatia sem épico, com ficha aprovada pelo P.O.)
- **Gatilho:** triagem conclui "uma fatia (≤ G) que cria ou muda regra de negócio **clara**, sem decisão de produto em aberto"
  (triar:53); também "aprova a ficha da FT-040" (F2).
- **Pré-condições:** lê glossário, bundle do ELM (para o `sdd-elm` *similares*), "Próximos ids"; `sdd-entrevistar` carregada.
- **Processamento (triar:61-63, 84-98):**
  1. Reserva o próximo `FT-nnn`; cria a ficha `<produto>/fatias/FT-<nnn>-<slug>.md` (cria a pasta `fatias/` se faltar) no formato
     de `ficha.md`; `Situação: rascunho`.
  2. Rodadas da `sdd-entrevistar` até regras e cenários fecharem; decisões vão para a seção **Decisões da própria ficha**
     (entrev:18-20; ficha:56). Termo novo → glossário (a triagem roda na base — ficha:57).
  3. Regra nova/alterada → `sdd-elm` modo *similares* (só leitura) **antes** de escrevê-la; coluna "No ELM" =
     `reusa <id>` | `altera <id>` | `novo (verificado <data>)` (ficha:51-53).
  4. Cenários `C1…Cn` (feliz, "não deve ser aceito", repetição, erro em um item, com "Então" verificável — ficha:48-50).
  5. >3 cenários de comportamentos diferentes / >1 regra independente → refaz como épico (ficha:58-59; triar:59-60).
  6. P.O. aprova a ficha → `Situação: aprovada por <login> em <data>`. Sem aprovação → fica `backlog`, `falta: aprovação do P.O.` (triar:62-63).
  7. Passo 3: linha em `## Fatias — sem épico`: `trilha` padrão; `origem`; `ficha` `[ficha](fatias/FT-<nnn>-<slug>.md)`; `tamanho` P/M/G;
     `modo` AFK (esperado e teste claros, sem dado sensível) senão HITL; prioridade/`sprint`/`responsavel` `—`;
     `status` `pronta` (ficha aprovada) ou `backlog` + `obs` `falta: …` (triar:84-91).
  8. EWM (com ELM): item de origem no EWM → nada a criar (será pai das tarefas); sem item de origem e `backlog no EWM` =
     `ao-fatiar` → `sdd-elm` *backlog* cria o IB `[FT-nnn]` sob o épico de Sustentação (com confirmação); `na-sprint` → o
     planejamento cria (triar:95-98). Backlog com seção antiga `## Fatias — trilha rápida` → renomeia e acrescenta colunas
     `trilha`/`ficha` no mesmo commit (triar:73-75).
  9. "Próximos ids"; commit com `backlog.md` + ficha (padrão de commit do `sdd.md`, `steer:59`); push/PR com "sim".
- **Resultado:** `fatias/FT-<nnn>-<slug>.md` (+ `Decisões`), linha em `## Fatias — sem épico`, glossário atualizado se houve termo
  novo, IB no EWM quando aplicável; bloco 📥; `Próximo`: se `pronta` → "começar agora (`sdd-iniciar`: precisa estar na
  sprint aberta ou entrar por encaixe) ou deixar para o planejamento"; se `backlog` → "o que falta e quem responde" (triar:119-120).
- **Lacunas:**
  - `tamanho` e `modo` são gravados na triagem (triar:87-88) sem dizer que o time/pessoa confirma; `plan` Regras: "estimativa é
    do time, o agente propõe, a pessoa decide" — a triagem não tem esse passo.
  - O `FT-nnn` é reservado e a ficha nasce em `rascunho` durante as rodadas (triar:62), mas só é commitada no Passo 3 (triar:101):
    sessão interrompida perde decisões; e dois devs podem reservar o mesmo FT antes do push (só tratado em F11).
  - `ficha:46` ("regra nova ou alterada só vale aprovada") × DoR da rápida: se a rápida tiver ficha de `## Comportamento`, ela
    precisa de aprovação? Não dito.

#### S04-F5 · Trilha rápida (defeito ou ajuste ≤ 1 dia, sem regra nova)
- **Gatilho:** "registra o defeito 4567", "corrigir o cálculo de juros" (triar:32), item de EWM do tipo Defeito (triar:54).
- **Pré-condições:** descrição do item (EWM via `elm-ccm`, ou pessoa); `sdd-elm` *similares* não é exigido (sem regra nova).
- **Processamento (triar:54, 64-66, 84-98):**
  1. Falta informação (comportamento esperado, onde, como reproduzir) → **uma** rodada no formato da `sdd-entrevistar`
     (numerada, com recomendação, "sim" aceita todas). Fatos o agente busca (código, bundle, banco só leitura).
  2. Cria ficha **só se** a origem não traz o comportamento esperado escrito; nesse caso a ficha usa `## Comportamento` (atual +
     evidência, esperado + fonte, o que não muda) no lugar de Regras e Cenários (ficha:54-55; triar:92-94).
  3. Linha em `## Fatias — sem épico`: `trilha` rápida, `origem` `DF 4567`/`pedido: …`, `tamanho` P/M, `modo`, `status` `pronta` se
     comportamento esperado claro + sem regra nova + tamanho ≤ M, senão `backlog` com `falta: <o quê>` (triar:89-91).
  4. IB: item de origem → nada; sem origem e `ao-fatiar` → `sdd-elm` *backlog* cria `[FT-nnn]` sob Sustentação (triar:95-98).
  5. Commit/push como em F4. Regra nova descoberta no caminho → refaz como padrão (iniciar:46-47 devolve a triagem).
- **Resultado:** linha da fatia; ficha opcional; bloco 📥; `Próximo`: começar (`sdd-iniciar`) ou planejamento / o que falta.
- **Lacunas:** a rodada única da rápida/direta (triar:64-65) usa "o formato" da entrevistar, mas a `sdd-entrevistar` não tem esse
  modo nem destino: sem ficha e sem `decisoes.md`, onde as respostas ficam registradas? (entrev:18-20 só prevê épico, fatia,
  ficha). Idem a interação "atendimento"/"autônomo" (entrev:108-132).

#### S04-F6 · Trilha direta (diff cabe numa frase)
- **Gatilho:** triagem conclui "texto, configuração, ajuste trivial, sem regra nova, sem risco de dado" (triar:55).
- **Processamento:** como F5, com: tamanho `P`; **nunca** ficha (triar:94; ficha:6); `status` `pronta` se "o pedido cabe numa frase"
  (triar:89-91); EWM: **sem IB** (a `[DEV]` nasce no planejamento ou no encaixe — triar:97-98); falta informação → uma rodada (triar:64-65).
- **Resultado:** linha em `## Fatias — sem épico` com `trilha` direta, `ficha` `—`; bloco 📥; `Próximo`: iniciar/planejamento.
- **Lacunas:** a direta exige `[DEV]` planejada para lançar horas (triar:55) e `sdd-iniciar:72-77` não deixa começar fora da sprint;
  o caminho "direta urgente" sempre passa por encaixe do P.O. (plan:93-105) — consistente, mas torna "corrigir um typo" caro; sem
  exceção documentada (README:152-154 vende "corrigir o defeito 4567 → registra e começa").

#### S04-F7 · Trilha atendimento (encaminhamento)
- **Gatilho:** pedido de cliente sem mudança no repositório ("extrai as contas bloqueadas", "por que o caso X deu Y?" — triar:35) ou
  item do EWM classificado assim (triar:56).
- **Processamento:** classifica (Passo 2) e **não escreve nada** (triar:99): `sdd-atender` numera, registra e abre a `[ATD]`.
- **Resultado:** bloco 📥 com `<AT>`, `Origem`, `Próximo: sdd-atender` (triar:121); nenhum arquivo.
- **Lacunas:** o bloco 📥 usa `<FT-nnn | EP-nn | AT>` sem id (triar:111); a `sdd-atender` precisa receber a origem (id do DF/IB) e
  gravá-la em `**Origem:**` — o que a triagem do lote presume (triar:132-133, 153), mas `atender:69` e `entrev:117` só
  falam de "chamado" (ver S06-F1).

#### S04-F8 · "Não fazer" (já entregue, fora do produto, recusado pelo P.O.)
- **Gatilho:** triagem conclui que o item não entra (triar:67).
- **Processamento:** nada no backlog; item do EWM → **oferece** comentário `sdd: não fazer — <motivo>` (`add_comment_to_workitem`, com "sim"), que o tira
  dos próximos lotes; fechar o item é do P.O., na UI (triar:67-69).
- **Resultado:** resposta explicando o motivo; opcional comentário no EWM; nenhum arquivo.
- **Lacunas:** sem MCP, o item continua aparecendo em todo lote (o filtro do lote depende do comentário, triar:135); não há marca local.

#### S04-F9 · Lote do EWM ("importar do EWM", "triar os defeitos do time")
- **Gatilho:** "importar do EWM", "triar os defeitos do time" (triar:3, 34).
- **Pré-condições:** power `elm` e MCP na sessão; sem eles → "a importação precisa do MCP" e para (triar:127-128); `pa_*.json`; backlog; AT-*.
- **Processamento (triar:130-154):**
  1. Filtro com padrão e **uma** confirmação: time do `pa_*.json` (vários → pergunta), tipos Defeito + Item de Backlog, estado `Novo`
     (nome do estado inicial na PA; a pessoa troca); `ccm_list_workitems` por tipo.
  2. Remove do lote: id já em `backlog.md` (`origem`/`elm`) ou em `**Origem:**` de AT; itens criados pelo fluxo (`[EP-`,`[FT-`,
     `[SUS-`,`[ESP]`,`[DEV]`,`[REV]`,`[VER]`,`[ATD]`); tarefas; e, após ler o item, os que têm pai do fluxo ou comentário `sdd: não fazer`.
     > 15 itens → mostra a contagem e pede filtro mais fino.
  3. `ccm_get_workitem` de cada um (com descrição e comentários); monta a tabela `📥 Lote EWM` com Trilha/Status/Motivo e **uma
     confirmação** ("sim" ou ajuste por linha, ex. "DF 4570: não fazer").
  4. Com "sim": Passo 3 para cada linha, **um commit** para o lote e o EWM numa confirmação só (`sdd-elm`); padrão no lote → ficha
     `rascunho` só com o Pedido e `falta: regras, cenários e aprovação do P.O.` (entrevista uma a uma, depois = S04-F2/F4);
     atendimentos **não são abertos**: ficam listados e voltam a cada lote até virarem AT.
  5. Saída: tabela com ids criados e pendências.
- **Resultado:** N linhas no `backlog.md` (épicos `rascunho`, fatias sem épico), fichas `rascunho` das padrão, IBs/épicos no EWM
  conforme F3/F4, um commit; tabela final. `Próximo` por linha (começar ou planejamento / entrevista da ficha / `sdd-atender`).
- **Lacunas:**
  - Pergunta "épico ou filho" (triar:81) dentro do lote quebra a "uma confirmação" (137-138).
  - Rápida `backlog` com `falta:` no lote não recebe rodada de perguntas (triar:64 só vale no fluxo unitário); não dito se é depois.
  - Atendimento do lote só deixa de reaparecer quando o `**Origem:**` do AT contém o id (triar:132-133,153), mas a `sdd-atender`
    não manda gravar esse id (S06-F1). Itens atendimento ficam `Novo` no EWM e sem comentário para filtrá-los.
  - Tamanho e AFK/HITL decididos pelo agente para N itens sem confirmação individual de estimativa.

#### S04-F10 · Mudança em ficha já aprovada (pedido explícito)
- **Gatilho:** pedido da pessoa para alterar regra/cenário de ficha aprovada (triar:160-161), ou ficha devolvida por `sdd-plano:34`/`sdd-consolidar:31`.
- **Processamento:** tratado como F2: ficha volta a `rascunho`, mostra a **diferença**, pede aprovação do P.O. de novo; fatia já iniciada
  que dependa dela → avisa quem a conduz (o `status.md`/Responsável); `status` da fatia no backlog volta a `backlog` com
  `falta: aprovação do P.O.` (backlog:75 "deixou de valer → volta a backlog").
- **Resultado:** ficha e linha atualizadas, commit na base; aviso ao responsável.
- **Lacunas:** não há instrução de como "avisar" (o agente não tem canal além da conversa); e se a fatia está em `pr-aberto`/`implementando`
  não se diz quem decide continuar ou refazer (ver S04-F2).

#### S04-F11 · Conflito de id no push (corrida entre duas pessoas)
- **Gatilho:** push/PR curto rejeitado porque outra pessoa registrou o mesmo número (triar:102-106).
- **Processamento:** o agente **não** faz merge/rebase; pede à pessoa `git pull --rebase`; no conflito do `backlog.md` mantém o remoto, pega o
  próximo id livre para a sua linha **e** para o nome da ficha; se o item já foi criado no EWM, troca `[FT-nnn]`/`[EP-nn]` do título
  (`ccm_update_workitem`, com "sim"). Id que ainda não chegou à base pode mudar; o que já chegou, nunca.
- **Resultado:** linha/ficha renumeradas, título no EWM corrigido, commit novo.
- **Lacunas:** a ficha renomeada também tem o `# FT-nnn` no cabeçalho e links `[ficha](fatias/FT-<nnn>-…)` na linha — a skill só cita "nome da ficha".
  O `sdd-produto` não faz push (steer:61: "entrega o comando"), então quem executa push/rebase é a pessoa; triar:101-102 não diz isso.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**Estado comum S04:** base `main`; `.kiro/steering/sdd.md` presente (Usa ELM = sim; backlog no EWM = `ao-fatiar`; tipo de épico = `Épico`; prefixo `feature/`); `backlog.md` com `Próximos ids: EP-04 · FT-034`; sem AT-* e sem `status.md` em branch; árvore limpa; MCP `elm` presente, salvo onde indicado.

#### S04-F1 · Triagem de entrada única (pedido em texto)

```text
S04-F1 · Triagem de entrada única (pedido em texto)
1. INPUT EXATO: "nova demanda: limitar o desconto de pontualidade a 10% da parcela"
   ESTADO: estado comum S04; nenhuma linha, AT ou status.md com o tema.
2. REGRAS:
   SE sdd.md existe ENTÃO segue — triar:20
   SE está na base ENTÃO git pull --ff-only; árvore limpa → segue — triar:26-28
   SE entrada é pedido em texto ENTÃO lê a própria descrição — triar:32
   SE busca em backlog/AT/status.md não acha nada ENTÃO Passo 2 — triar:37-39
   SE muda regra de negócio, uma fatia, sem decisão de produto em aberto ENTÃO trilha PADRÃO ("regra de negócio clara") — triar:53
   SE dúvida entre duas trilhas ENTÃO pergunta sim/não pela mais leve — triar:59
   SE padrão ENTÃO rodadas da sdd-entrevistar; ficha FT-034 nasce em rascunho — triar:61-62
   SE regra nova ENTÃO sdd-elm modo similares antes de escrevê-la — triar:62
   SE padrão, sem item de origem, backlog no EWM = ao-fatiar ENTÃO sdd-elm modo backlog cria IB [FT-034] sob Sustentação, com confirmação — triar:95-98
3. OUTPUT GERADO: imediato: "Trilha padrão — <motivo em uma linha>." + Rodada 1 no formato de entrev:40-53 (Contexto e Recomendo por pergunta; "sim" aceita todas). O bloco 📥 (triar:111) só sai depois da entrevista.
   ARQUIVOS ESCRITOS: <produto>/fatias/FT-034-<slug>.md · ficha em rascunho, sem commit até o Passo 3 (triar:101) | backlog.md só no Passo 3
4. VEREDITO MECÂNICO: AMBÍGUO (triar:53 "regra de negócio clara — o P.O. decide aqui" × triar:59 "diga a trilha e o motivo": não se diz se a clareza é julgada pelo agente ou pelo P.O.; não há critério de "clara")
```

#### S04-F2 · Retomada: "aprova a ficha da FT-040"

```text
S04-F2 · Retomada da triagem de fatia sem épico ("aprova a ficha da FT-040")
1. INPUT EXATO: "aprova a ficha da FT-040"
   ESTADO: FT-040 em "## Fatias — sem épico": trilha padrão, status backlog, obs "falta: aprovação do P.O."; fatias/FT-040-desconto.md com Situação rascunho e C1–C2; nenhum status.md em branch; main limpa.
2. REGRAS:
   SE gatilho "aprova a ficha da FT-040" ENTÃO a skill entra — triar:3
   SE base e árvore limpa ENTÃO segue — triar:26-28
   SE "já existe?" acha FT-040 em fatia sem épico com falta/ficha a aprovar ENTÃO retoma o Passo 2 com o mesmo FT — triar:40-42
   SE P.O. aprova a ficha ENTÃO Situação: aprovada por <login> em <data> — triar:62-63; ficha:46
   SE retoma a triagem ENTÃO Passo 2 com o mesmo FT; no Passo 3 só atualiza a linha (sem id novo) — triar:42-43
   SE ficha aprovada e cenários completos ENTÃO status pronta — triar:89-91
   SE valor de <login> ENTÃO ??? — nenhuma regra define de onde vem o login, nem como confirmar que quem fala é o P.O. (ficha:46; triar:62-63; steer não traz papel de P.O.)
3. OUTPUT GERADO: sem regra para o passo de aprovação. A saída imediata não tem template: a skill não manda perguntar quem aprova nem qual login gravar. Se o agente pergunta à pessoa, a pergunta não está escrita em lugar nenhum.
   ARQUIVOS ESCRITOS: nenhum até a aprovação; depois fatias/FT-040-desconto.md (Situação) e backlog.md (linha FT-040, status pronta) · commit pequeno
4. VEREDITO MECÂNICO: SEM REGRA (valor de <login do P.O.> e identificação de quem aprova: ficha:46 pede o login, nenhuma regra diz como obtê-lo)
```

#### S04-F3 · Trilha épico

```text
S04-F3 · Trilha épico ("nova funcionalidade …")
1. INPUT EXATO: "nova funcionalidade: portal de renegociação de dívidas com simulação, boleto e acordo para o cliente"
   ESTADO: estado comum S04; EP-03 existe; sdd.md: tipo de épico = Épico; MCP elm presente; entrada de texto (sem item de EWM).
2. REGRAS:
   SE funcionalidade nova com várias histórias/fatias ENTÃO trilha ÉPICO — triar:52
   SE épico ENTÃO próximo EP-nn de "Próximos ids" = EP-04 — triar:77
   SE épico ENTÃO linha em ## Épicos com status rascunho, prioridade —, prd — — triar:77; backlog:43
   SE Usa ELM = sim ENTÃO sdd-elm modo backlog, só o épico, com confirmação — triar:78; elm:120-126
   SE tipo do sdd.md = Épico ENTÃO o item é do tipo Épico, título [EP-04] <título> — elm:126-128
   SE confirmado ENTÃO o id do EWM vai para a coluna elm — triar:78
   SE épico ENTÃO Próximos ids passa a EP-05 · FT-034; commit pequeno só com o backlog.md; push com "sim" — triar:101; backlog:82-83
   SE épico registrado ENTÃO Próximo: "especificar agora (sdd-prd com EP-04) ou deixar para o planejamento" — triar:118
   SE há pergunta de próximo passo ENTÃO "Pergunte; não comece sozinho" — triar:123
3. OUTPUT GERADO: prévia do EWM (elm:29): "Criar | EP-04 | [EP-04] Portal de renegociação de dívidas | Épico" + "sim" para o lote. Depois:
   📥 EP-04 — Portal de renegociação de dívidas · trilha épico · rascunho · modo —
   Origem: pedido: portal de renegociação · Ficha: — · EWM: <id criado após o sim>
   Próximo: especificar agora (sdd-prd) ou deixar para o planejamento
   ARQUIVOS ESCRITOS: <produto>/backlog.md · linha EP-04 em ## Épicos + Próximos ids · commit
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S04-F4 · Trilha padrão com ficha e similares

```text
S04-F4 · Trilha padrão (fatia sem épico com ficha)
1. INPUT EXATO: "nova demanda: bloquear o pagamento por Pix quando o CPF estiver em análise"
   ESTADO: estado comum S04; MCP elm presente; a busca no bundle não acha regra igual (similares: novo).
2. REGRAS:
   SE regra nova ENTÃO trilha PADRÃO (uma fatia, uma regra, 2 cenários) — triar:53, 58-60
   SE padrão ENTÃO FT-034 reservado; ficha fatias/FT-034-<slug>.md em rascunho — triar:61; ficha:44 (formato)
   SE padrão ENTÃO rodadas da sdd-entrevistar até regras e cenários fecharem; decisões na seção Decisões da ficha — triar:61; entrev:18-20; ficha:56
   SE regra nova ENTÃO sdd-elm modo similares (só leitura) antes de escrever — triar:62; elm:49-51
   SE similares sem acerto ENTÃO coluna "No ELM" = novo (verificado <data>) — ficha:52-53; elm:96
   SE cenários ENTÃO C1…Cn (feliz, não aceito, repetição, erro) com "Então" verificável — ficha:48-50
   SE mais de ~3 cenários de comportamentos diferentes ENTÃO refaz como épico — triar:58-60; ficha:58-59 (aqui: 2 cenários, não se aplica)
   SE P.O. aprova ENTÃO Situação: aprovada por <login> em <data> — triar:62-63; ficha:46
   SE valor de <login> ENTÃO ??? — ficha:46 pede o login; nenhuma regra diz como obtê-lo
   SE padrão ENTÃO linha em ## Fatias — sem épico: trilha padrão; origem "pedido: …"; ficha link; tamanho P/M/G; modo; status pronta se aprovada — triar:84-91
   SE padrão, sem item de origem, backlog no EWM = ao-fatiar ENTÃO sdd-elm modo backlog cria IB [FT-034] sob Sustentação, com confirmação — triar:95-98; elm:135-138
3. OUTPUT GERADO: imediato: "Trilha padrão — regra nova com dois cenários." + Rodada 1 (entrev:40-53). Depois da rodada, bloco de similares (elm:69-78) com "novo (verificado 2026-10-15)". Ao fim: 📥 FT-034 — … · trilha padrão · pronta ou backlog: falta: aprovação do P.O. · modo …
   ARQUIVOS ESCRITOS: fatias/FT-034-<slug>.md (rascunho, depois aprovada) · backlog.md (linha FT-034 + Próximos ids) · commit com a ficha; IB no EWM com "sim"
4. VEREDITO MECÂNICO: SEM REGRA (valor de <login do P.O.> em "aprovada por", ficha:46; o tamanho P/M/G (triar:87) não tem critério de escolha)
```

#### S04-F5 · Trilha rápida (defeito do EWM)

```text
S04-F5 · Trilha rápida ("registra o defeito 4567")
1. INPUT EXATO: "registra o defeito 4567"
   ESTADO: estado comum S04; MCP elm presente; DF 4567 = "Juros calculados em dobro no atraso" (sem comportamento esperado e sem passos para reproduzir); o bundle documenta a regra de juros simples em REG 2101 (fato encontrado pelo agente); DF 4567 não está no backlog.
2. REGRAS:
   SE número do EWM ENTÃO lê o item com elm-ccm (ccm_get_workitem, com descrição e comentários) — triar:32-33
   SE defeito e comportamento certo já documentado ENTÃO trilha RÁPIDA — triar:54; triar:66 (fato do bundle)
   SE falta comportamento esperado ou como reproduzir ENTÃO UMA rodada no formato da sdd-entrevistar — triar:64-65
   SE origem não traz o comportamento esperado escrito ENTÃO ficha com seção ## Comportamento (atual, esperado + fonte, o que não muda) — triar:92-94; ficha:54-55
   SE rápida ENTÃO linha em ## Fatias — sem épico: trilha rápida; origem DF 4567; tamanho P/M; modo; status pronta só se comportamento esperado claro, sem regra nova e tamanho ≤ M — triar:87-91
   SE origem é o DF ENTÃO sem IB novo — triar:95
3. OUTPUT GERADO: imediato: "Trilha rápida — defeito; comportamento certo documentado na REG 2101." + rodada única:
   "D-1 · Como reproduzir? Recomendo: <…>. "sim" aceita." Bloco 📥 depois da resposta.
   ARQUIVOS ESCRITOS: fatias/FT-034-<slug>.md com ## Comportamento · backlog.md (linha FT-034) · commit
4. VEREDITO MECÂNICO: AMBÍGUO (tamanho P/M não tem critério em dias ou pontos: triar:54 fala em "≤ 1 dia", triar:87 pede P/M, e o status pronta depende de "tamanho ≤ M" — triar:91)
```

#### S04-F6 · Trilha direta (diff cabe numa frase)

```text
S04-F6 · Trilha direta ("trocar o texto do rodapé")
1. INPUT EXATO: "nova demanda: trocar o texto do rodapé do boleto para 'Central: 0800 123 4567'"
   ESTADO: estado comum S04; MCP elm presente; sem regra nova, sem dado sensível.
2. REGRAS:
   SE o diff cabe numa frase, sem regra nova e sem risco de dado ENTÃO trilha DIRETA — triar:55
   SE direta ENTÃO tamanho P; ficha nunca — triar:55, 94; ficha:6
   SE pedido cabe numa frase ENTÃO status pronta — triar:89-91
   SE direta ENTÃO sem IB no EWM; a [DEV] nasce no planejamento ou no encaixe — triar:97-98
   SE modo AFK quando "o esperado e o teste são claros", senão HITL — triar:87-88
   SE "teste claro" para texto sem comportamento ENTÃO ??? — iniciar:53 diz "teste que falha (quando houver comportamento)"; triar:87-88 exige teste claro
   SE falta informação ENTÃO uma rodada — triar:64-65 (aqui não falta: não dispara)
   SE padrão de Passo 4 ENTÃO Próximo: começar agora (sdd-iniciar, precisa de sprint aberta ou encaixe) ou planejamento — triar:119
3. OUTPUT GERADO: "Trilha direta — pedido cabe numa frase, sem regra nova." + 📥 FT-035 — trocar texto do rodapé do boleto · trilha direta · pronta · modo <AFK | HITL>
   Origem: pedido: trocar texto do rodapé · Ficha: — · EWM: — (sem IB)
   Próximo: sdd-iniciar (precisa de sprint aberta ou encaixe) ou planejamento
   ARQUIVOS ESCRITOS: backlog.md (linha FT-035, tamanho P, trilha direta, ficha —) · commit
4. VEREDITO MECÂNICO: AMBÍGUO (modo AFK × HITL: triar:87-88 pede "teste claro", mas para direta sem comportamento (iniciar:53) não há teste; a regra não diz qual modo usar)
```

#### S04-F7 · Trilha atendimento

```text
S04-F7 · Trilha atendimento ("extrai as contas bloqueadas de setembro")
1. INPUT EXATO: "extrai as contas bloqueadas de setembro para a auditoria, o cliente pediu"
   ESTADO: estado comum S04; sprint 3 aberta; nenhuma mudança no repositório pedida.
2. REGRAS:
   SE pedido de cliente sem mudança no repositório (extração) ENTÃO trilha ATENDIMENTO — triar:35, 56
   SE atendimento ENTÃO nada se escreve na triagem; sdd-atender numera e registra — triar:56, 99
   SE atendimento ENTÃO Próximo: sdd-atender — triar:121
   SE Próximo ENTÃO bloco 📥 <FT-nnn | EP-nn | AT> — triar:111 (o AT ainda não tem número)
   SE triagem termina ENTÃO "Pergunte; não comece sozinho" — triar:123
   SE sdd-atender for chamada ENTÃO sprint aberta é pré-requisito (atender:25); sem sprint aberta não há regra — ver veredito
3. OUTPUT GERADO: "Trilha atendimento — extração, nada muda no repositório."
   📥 AT — Extração das contas bloqueadas de setembro · trilha atendimento · <status ???> · modo <???>
   Origem: pedido: extração contas bloqueadas · Ficha: — · EWM: pendente/sem ELM
   Próximo: sdd-atender. Abro o atendimento agora?
   ARQUIVOS ESCRITOS: nenhum (triar:99)
4. VEREDITO MECÂNICO: AMBÍGUO (o modelo do bloco 📥 (triar:111) pede "pronta | backlog: falta" e "modo" para toda entrada; para atendimento não há status nem modo definidos, e o id é só "AT")
```

#### S04-F8 · Não fazer (item do EWM)

```text
S04-F8 · "Não fazer" com item do EWM
1. INPUT EXATO: "DF 4570: já foi entregue na versão 4.2, não fazer"
   ESTADO: estado comum S04; MCP elm presente; DF 4570 = "Erro ao consultar CPF sem máscara" existe no EWM; nada no backlog.
2. REGRAS:
   SE a triagem conclui que o item não entra (já entregue) ENTÃO nada vai para o backlog — triar:67
   SE item do EWM ENTÃO oferece comentário "sdd: não fazer — <motivo>" via add_comment_to_workitem, com "sim" — triar:68
   SE comentário enviado ENTÃO o item sai dos próximos lotes — triar:68, 135
   SE fechar o item ENTÃO é do P.O., na UI (não é o agente) — triar:69
3. OUTPUT GERADO: "Não entra: DF 4570 — já entregue na versão 4.2. Comento no DF 4570 com 'sdd: não fazer — já entregue na versão 4.2'? (sim)"
   ARQUIVOS ESCRITOS: nenhum · comentário no EWM só com "sim"
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S04-F9 · Lote do EWM ("triar os defeitos do time")

```text
S04-F9 · Lote do EWM ("triar os defeitos do time")
1. INPUT EXATO: "triar os defeitos do time Cobrança"
   ESTADO: estado comum S04; MCP elm presente; pa_*.json com um só time (Cobrança); tipo do épico = Item de Backlog (pai), ou seja, IB 611 é do tipo de épico; backlog já tem a origem DF 4567; ccm_list_workitems em estado Novo: DF 4567 (já no backlog), DF 4570, DF 4571, IB 611 (Portal de renegociação), IB 613 (limitar desconto), IB 615 (extração de contas bloqueadas), e uma tarefa [DEV] 900. Total: 7 itens.
2. REGRAS:
   SE "triar os defeitos do time" ENTÃO lote — triar:34
   SE MCP do power elm presente ENTÃO segue; senão "a importação precisa do MCP" e para — triar:127-128
   SE lote ENTÃO filtro: time, tipos Defeito + Item de Backlog, estado Novo, numa só confirmação — triar:130-131
   SE id no backlog (origem) ou tarefa ([DEV]) ENTÃO fora do lote — triar:132, 134 → sai DF 4567 e [DEV] 900
   SE mais de 15 itens ENTÃO pede filtro mais fino — triar:135 (aqui 6, não se aplica)
   SE lote ENTÃO ccm_get_workitem de cada item — triar:137
   SE IB 611 é do tipo de épico ENTÃO PERGUNTA se vira épico ou filho — triar:80-81
   SE lote ENTÃO tabela com "uma confirmação para o lote" — triar:137-138
   SE padrão no lote ENTÃO ficha rascunho só com Pedido e falta: aprovação do P.O. — triar:150-151
   SE atendimento no lote ENTÃO não abre: fica listado — triar:152
3. OUTPUT GERADO:
   📥 Lote EWM — Cobrança · tipos Defeito, Item de Backlog · estado Novo · 5 itens novos (1 já no backlog)
   | Item | Tipo | Título | Trilha | Status | Motivo |  (uma linha por item; IB 611 = épico)
   IB 611: vira épico ou filho? (pergunta da regra de épico)
   "sim" registra tudo · ou ajuste por linha
   ARQUIVOS ESCRITOS: nenhum até "sim"
4. VEREDITO MECÂNICO: CONFLITO (triar:80-81 "pergunte se vira o épico ou o filho" para o IB 611, dentro do lote, × triar:137-138 "proponha a triagem numa tabela, com uma confirmação para o lote"; a regra de pergunta por item quebra a de confirmação única)
```

#### S04-F10 · Mudança em ficha já aprovada

```text
S04-F10 · Mudança em ficha aprovada ("muda a regra da FT-040: o teto passa a ser 12%")
1. INPUT EXATO: "muda a regra da FT-040: o teto do desconto de pontualidade passa a ser 12% da parcela"
   ESTADO: estado comum S04; fatias/FT-040-desconto.md Situação: aprovada por ana.souza em 2026-10-14; FT-040 status pronta; nenhum status.md em branch (fatia não iniciada); MCP elm presente.
2. REGRAS:
   SE pedido explícito de mudar regra de ficha aprovada ENTÃO volta a rascunho; mostra a diferença; pede aprovação de novo — triar:160; ficha:46
   SE regra alterada ENTÃO sdd-elm modo similares antes de escrever (coluna No ELM = altera <id>) — triar:62; ficha:51-53; elm:81-82
   SE ficha volta a rascunho ENTÃO a linha do backlog volta a backlog com falta: aprovação do P.O. — backlog:75
   SE fatia já iniciada depende da mudança ENTÃO avisa quem a conduz — triar:161 (não se aplica: nenhum status.md)
   SE alteração gravada ENTÃO commit na base — triar:101
3. OUTPUT GERADO: "FT-040: teto muda de 10% para 12% da parcela. Diferença: <linha antiga> → <linha nova>. Ficha volta a rascunho; FT-040 volta a backlog (falta: aprovação do P.O.). Aprova de novo?" + bloco similares (elm:69-78).
   ARQUIVOS ESCRITOS: fatias/FT-040-desconto.md (Situação rascunho; regra R1 atualizada) · backlog.md (linha FT-040: status backlog, obs falta: aprovação do P.O.) · commit
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S04-F11 · Conflito de id no push

```text
S04-F11 · Conflito de id no push
1. INPUT EXATO: "dá o push do backlog com a FT-034"
   ESTADO: commit local com FT-034 (linha em backlog.md, ficha fatias/FT-034-cobranca-pix.md) e IB [FT-034] já criado no EWM; origin/main já tem FT-034 "Relatório de inadimplência" (registrado por outra pessoa); push rejeitado.
2. REGRAS:
   SE push rejeitado porque o id já existe ENTÃO conflito de id — triar:101-102
   SE conflito de id ENTÃO o agente não faz merge nem rebase; pede à pessoa git pull --rebase — triar:102-103
   SE conflito no backlog.md ENTÃO mantém o remoto e pega o próximo id livre para a linha e para o nome da ficha — triar:103-105 (FT-035)
   SE o item já foi criado no EWM ENTÃO troca [FT-034] por [FT-035] no título com ccm_update_workitem, com "sim" — triar:105-106
   SE id já chegou à base ENTÃO não muda (FT-034 remoto) — triar:106
   SE ficha renumerada ENTÃO renomeia o arquivo para FT-035-… — triar:104-105 ("nome da ficha")
3. OUTPUT GERADO: "Push rejeitado: FT-034 já existe em origin/main. Não faço merge nem rebase. Rode git pull --rebase e me avise." Depois do pull:
   "Renumero para FT-035 (linha e ficha). Troco o título do IB [FT-034] para [FT-035]? (sim)"
   ARQUIVOS ESCRITOS: backlog.md (linha FT-035, Próximos ids) · fatias/FT-035-<slug>.md · commit novo
4. VEREDITO MECÂNICO: AMBÍGUO (a renumeração cita só o "nome da ficha" (triar:104-105); o cabeçalho "# FT-nnn" da ficha (ficha:11) e os links [ficha](fatias/FT-<nnn>-…) da linha (backlog:46) não são citados)
```

#### S04-X1 · Borda: pré-condição, árvore suja em outra branch

```text
S04-X1 · Borda: triagem pedida com alterações locais em feature/ft-031
1. INPUT EXATO: "nova demanda: corrigir o rótulo do botão de pagamento"
   ESTADO: branch atual feature/ft-031-bloquear-conta (não é a base main); árvore com alterações não commitadas.
2. REGRAS:
   SE está fora da base ENTÃO pergunta "Troco para main para triar? (sim)" — triar:26
   SE alterações locais não commitadas ENTÃO avisa e PARA; nunca oferece descartar, stash ou reset — triar:27-28
3. OUTPUT GERADO: "Você está em feature/ft-031-bloquear-conta com alterações não commitadas. Não troco de base e não faço pull. Commit ou guarde por conta própria e me chame de novo."
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO (a ordem "pergunta a troca" antes do aviso não muda o desfecho: a triagem para)
```

#### S04-X2 · Borda: "aprova a ficha" de fatia que já tem status.md em branch

```text
S04-X2 · Borda: aprovação de ficha de fatia já iniciada
1. INPUT EXATO: "aprova a ficha da FT-040"
   ESTADO: FT-040 com ficha rascunho e linha backlog com falta: aprovação do P.O.; existe feature/ft-040-desconto com .kiro/specs/ft-040-desconto/status.md, fase implementando (já iniciada).
2. REGRAS:
   SE fatia sem épico volta para cá (ficha a aprovar) ENTÃO retoma a triagem (Passo 2, mesmo FT) — triar:40-42
   SE qualquer outro caso ENTÃO para e manda para sdd-iniciar (começar ou retomar) — triar:45-46
   SE a fatia já tem status.md em branch ENTÃO quem decide mudar a ficha é quem a conduz, avisa — triar:160-161 (não diz como detectar nem quem decide)
3. OUTPUT GERADO: nenhum template de saída define o caso. Os dois ramos produzem resultados diferentes: retomar (aprovar a ficha) ou parar (mandar à sdd-iniciar).
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: AMBÍGUO (triar:40-41 manda retomar "fatia sem épico … ficha a aprovar" sem excluir fatia já iniciada; triar:45-46 e 160-161 mandam parar e avisar quem conduz; qual regra vale com status.md presente não está escrito)
```

#### S04-X4 · Borda: sem MCP elm, padrão com regra nova

```text
S04-X4 · Borda: MCP elm ausente numa fatia padrão com regra nova
1. INPUT EXATO: "nova demanda: bloquear o pagamento por Pix quando o CPF estiver em análise"
   ESTADO: igual a S04-F4, mas o MCP elm NÃO está na sessão.
2. REGRAS:
   SE regra nova ENTÃO sdd-elm modo similares antes de escrevê-la — triar:62
   SE sdd-elm exige o MCP elm nesta sessão ENTÃO "Requer o power elm (MCP elm) nesta sessão" — elm:16-17
   SE sem MCP ENTÃO similares só com o bundle e a saída diz "verificação no ELM ao vivo pendente" — elm:62-63
   SE similares sem verificação ao vivo ENTÃO coluna No ELM só aceita reusa | altera | novo (verificado <data>) — ficha:52-53; elm:96
3. OUTPUT GERADO: não há valor definido para a coluna No ELM quando a verificação ao vivo ficou pendente. A saída imediata pode ser "verificação ao vivo pendente" (elm:63), mas o campo do ficha não aceita esse valor.
   ARQUIVOS ESCRITOS: fatias/FT-034-<slug>.md com No ELM ??? (rascunho) · sem commit
4. VEREDITO MECÂNICO: CONFLITO (elm:16-17 "requer o MCP nesta sessão" × elm:62-63 "sem o MCP, só o bundle"; e ficha:52-53 × elm:62-63: o campo só aceita "novo (verificado <data>)", que exige checagem ao vivo que ficou pendente)
```

#### S04-X8 · Borda: "não fazer" sem MCP elm

```text
S04-X8 · Borda: "não fazer" de item do EWM sem MCP elm
1. INPUT EXATO: "registra o defeito 4570: já foi entregue na 4.2, não fazer"
   ESTADO: MCP elm NÃO está na sessão; o número 4570 é de um item do EWM.
2. REGRAS:
   SE sem o power ou MCP ENTÃO pede título, descrição e comportamento esperado; nunca inventa dado do work item — triar:33
   SE a triagem conclui "não entra" ENTÃO nada no backlog — triar:67
   SE item do EWM ENTÃO oferece comentário "sdd: não fazer" via add_comment_to_workitem — triar:68
   SE sem MCP ENTÃO não há como comentar; nenhuma regra manda registrar o "não fazer" em outro lugar — (sem regra)
   SE item sem comentário "sdd: não fazer" ENTÃO continua em todo lote — triar:135, 67-69 (plan: lacuna)
3. OUTPUT GERADO: "Não entra: já entregue na 4.2. Não consigo comentar no EWM (sem MCP elm). O item vai continuar aparecendo nos lotes até alguém comentar ou fechar na UI." (a última frase não tem regra de origem; é o que sobra)
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: SEM REGRA (o "não fazer" de item do EWM sem MCP não tem registro definido: triar:68 depende do MCP e nenhuma regra manda gravar a decisão na base)
```

#### Tabela-resumo S04

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S04-F1 | AMBÍGUO | "regra de negócio clara" (triar:53) × "diga a trilha" (triar:59): quem julga a clareza? |
| S04-F2 | SEM REGRA | login do P.O. e forma de confirmar o aprovador (ficha:46; triar:62-63) |
| S04-F3 | DETERMINÍSTICO | épico com tipo Épico, prévia e confirmação no EWM |
| S04-F4 | SEM REGRA | login do P.O. para "aprovada por"; tamanho P/M/G sem critério |
| S04-F5 | AMBÍGUO | tamanho P/M sem critério em dias (triar:54 × triar:87-91) |
| S04-F6 | AMBÍGUO | modo AFK × HITL sem teste para trocar texto (triar:87-88 × iniciar:53) |
| S04-F7 | AMBÍGUO | bloco 📥 sem status nem modo para atendimento; AT sem id (triar:111) |
| S04-F8 | DETERMINÍSTICO | comentário "não fazer" no EWM com "sim" |
| S04-F9 | CONFLITO | pergunta épico × filho dentro do lote (triar:80-81) × confirmação única (triar:137-138) |
| S04-F10 | DETERMINÍSTICO | ficha volta a rascunho e linha volta a backlog (triar:160; backlog:75) |
| S04-F11 | AMBÍGUO | renumeração não cita cabeçalho da ficha nem links da linha (ficha:11; backlog:46) |
| S04-X1 | DETERMINÍSTICO | árvore suja: para (triar:27-28) |
| S04-X2 | AMBÍGUO | fatia com status.md em branch: retomar (triar:40-41) × parar (triar:45-46) |
| S04-X4 | CONFLITO | sem MCP: sdd-elm requer MCP (elm:16-17) × similares só com bundle (elm:62-63); coluna No ELM sem valor pendente |
| S04-X8 | SEM REGRA | "não fazer" de item do EWM sem MCP não tem registro |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F3 épico | `<produto>/backlog.md` — linha em `## Épicos` + `Próximos ids` (triar:77, 101) | Sim, `<produto>/backlog.md` (backlog:1). P3 escreve `<produto>/backlog.md` — confere | `.md`, tabela | Colunas `id·título·status·prioridade·prd·elm` (backlog:21); `status` `rascunho`, prioridade `—`, `prd` `—` (triar:77-78 × backlog:43). Confere. `elm`: id gravado pela `sdd-elm` (backlog:53,67), não dito se no mesmo commit | `sdd-produto` grava e faz `git commit` (prod.json:70-71); commit pequeno só do backlog; **push/PR com "sim" mas o agente NÃO pode `git push`** (prod.json:112; steer:61 entrega o comando) — triar:101-102 omite isso; P3 F3 "push com sim" está incompleto. Se o EWM falha no meio → `elm` `pendente`, "Próximos ids" já cresceu (triar:82, 163) | Fora da base → troca com "sim" (triar:26); árvore suja → para (triar:27-28). `backlog.md`/`<produto>` inexistente: **NÃO ESPECIFICADO** (triar só lê o `sdd.md`, triar:20; setup cria o mínimo, setup:243) | DIVERGENTE (push que o agente não executa) · NÃO ESPECIFICADO (backlog.md ausente) |
| F4/F5/F6 fatia sem épico | `<produto>/backlog.md` — linha em `## Fatias — sem épico` + `Próximos ids` | Sim. P3 usa `backlog.md` sem prefixo `<produto>/` em F4, F5, F6, F10 e F2 (só F1/F3 têm) — imprecisão da P3, regra é `<produto>/backlog.md` | `.md` | 14 colunas na ordem backlog:33 (`id·título·trilha·origem·ficha·tamanho·modo·prioridade·status·sprint·responsavel·elm·concluida-em·obs`); triar:84-91 cobre todas, sem inventar. Valores de `trilha` com acento (`padrão·rápida·direta`, backlog:44) — confere com triar. **Coluna `elm` quando o item de origem já existe (DF/IB): NÃO ESPECIFICADO** (`—`? id da origem?) — iniciar:32 procura o id em `origem` **ou** `elm`, então funciona, mas não é dito | Commit com `backlog.md` + ficha (triar:101). Padrão de commit do `sdd.md` é `FT-<nnn> <verbo> …` (steer:59): aplicável a FT; épico, lote e renumeração sem padrão. Push: mesma restrição (agente não faz) | Backlog antigo com `## Fatias — trilha rápida` → renomeia no mesmo commit (triar:73-75) ✔; seção `## Fatias — sem épico` ausente em backlog mínimo do setup (setup:243 cria só `## Épicos`) → **NÃO ESPECIFICADO** criar a seção | NÃO ESPECIFICADO (coluna `elm` com origem existente; seção sem épico inexistente) |
| F4 padrão (F1, F2) | `<produto>/fatias/FT-<nnn>-<slug>.md` (ficha) | Sim (triar:92; ficha:1). P3 escreve `fatias/FT-034-<slug>.md` sem `<produto>/` (F1 traz o prefixo, F4 não). Maiúsculas `FT-` na ficha × `ft-` minúsculo na pasta de spec (iniciar:91, tmpl) — dois padrões de grafia, `<slug>` sem regra | `.md` | Template ficha:10-42: cabeçalho `# FT-nnn · título`; linha `**Trilha:** padrão · **Origem:** … · **Pedido por:** … · **Modo:** … · **Tamanho:** …`; `**Situação:**`; seções `Pedido, Regras (4 col), Cenários de aceite (C1…), Decisões (6 col), Fora de escopo`. **`Pedido por` (ficha:13) sem regra de preenchimento** (nem triar nem entrevistar). `Trilha:` com acento na ficha × `padrao/rapida` no status.md (tmpl:7) → DIVERGENTE entre arquivos. `Situação` só `rascunho` ou `aprovada por <login> em <data>` (ficha:46); **login do P.O. sem regra** (P3 F2/F4 confirmado). `Modo`/`Tamanho` duplicam o backlog (dois lugares) | A ficha nasce em `rascunho` **durante as rodadas** (triar:62) mas só é commitada no Passo 3 (triar:101): se a sessão cai, fica **arquivo não rastreado** com FT-nnn "reservado" que "Próximos ids" (não gravado ainda) ainda mostra livre → próxima triagem para por **árvore suja** (triar:27) sem instrução do que fazer com a ficha órfã → **NÃO ESPECIFICADO** | Pasta `fatias/` inexistente: "crie a pasta se não existir" (triar:92-93) ✔; `sdd-produto` grava `{{PRODUTO}}/**` ✔ | DIVERGENTE (grafia trilha, `Pedido por`) · NÃO ESPECIFICADO (ficha órfã após queda) |
| F5 rápida | `<produto>/fatias/FT-<nnn>-<slug>.md` só quando a origem não traz o esperado | Sim | `.md` | No lugar de Regras/Cenários: `## Comportamento` (ficha:54-55) — **subestrutura da seção (atual+evidência / esperado+fonte / não muda) sem template de exemplo** (só prosa). `Situação` da ficha rápida (precisa de aprovação do P.O.?): **NÃO ESPECIFICADO** — ficha:46 vale para "regra nova ou alterada", e a rápida não tem regra nova; triar:89-91 faz `pronta` sem aprovação | Idem F4 | Idem F4 | NÃO ESPECIFICADO (Situação/aprovação da ficha rápida; modelo de `## Comportamento`) |
| F6 direta | nenhum arquivo além do backlog | n/a | n/a | `ficha` = `—` (triar:94; ficha:6) — P3 confere | Idem F4 | — | OK |
| F4 (S07-F4 via triagem) | glossário (`<glossário do sdd.md>`, padrão `docs/glossario.md`) | Sim, caminho do `sdd.md` (entrev:21; ficha:57). P3 usa `docs/glossario.md` (default) — ok | `.md`, tabela `Termo·Definição·Evitar·Fonte·ELM` (entrev:88) | Confere | **triar:101 manda commitar só "backlog.md e a ficha"**: o glossário alterado pela triagem (ficha:57) fica **fora do commit** → árvore suja na próxima triagem (triar:27 para). steer:61 inclui glossário em "artefatos de produto", mas triar não | Glossário "não há" (setup:123-125 remove `{{GLOSSARIO}}` dos agentes → `sdd-produto` sem permissão de escrita) e triar/entrevistar **não dizem o que fazer**; arquivo inexistente com default "criar" (setup:123) mas o passo de gravação do setup (setup:243-246) **não lista** o glossário → **NÃO ESPECIFICADO** | DIVERGENTE (commit omite glossário) · NÃO ESPECIFICADO (glossário "não há"/inexistente) |
| F2 / F10 retomada e mudança em ficha aprovada | `<produto>/fatias/FT-<nnn>-<slug>.md` + linha do backlog | Sim (mesmos caminhos) | idem | Volta `Situação: rascunho`, "mostra a diferença" (triar:160) — onde a diferença é registrada? só na conversa; sem seção "Histórico/Revisão" no template (ficha:10-42) → a mudança fica só no diff do git. Backlog: `status` volta `backlog` + `obs` `falta: aprovação do P.O.` (backlog:75) ✔; `sprint`/`responsavel` já preenchidos pelo planejamento permanecem? **NÃO ESPECIFICADO** | commit pequeno na base (triar:101) ✔. Fatia `cancelada` por virar épico: `obs` `substituida-por EP-nn` (triar:43-44) × convenção só `substituida-por FT-…` (backlog:48,51); **destino da ficha** (Situação `cancelada`? não existe em ficha:46) e do IB já criado: NÃO ESPECIFICADO | Fatia já iniciada (status.md em branch): triar:45-46 × 160-161 — sem passo para detectar; a ficha na base muda enquanto a branch da fatia tem a cópia antiga → divergência de persistência não tratada (P3 S04-X2 confirmado) | NÃO ESPECIFICADO (ficha de fatia já iniciada; Situação da ficha cancelada) |
| F9 lote | `<produto>/backlog.md` (N linhas) + N fichas `rascunho` das padrão, um commit (triar:150-151) | Sim | `.md` | Ficha de lote "só com o Pedido" (triar:151): quais seções permanecem (Regras/Cenários/Decisões vazias? omitidas?) e `Pedido por`/`Tamanho`/`Modo` **NÃO ESPECIFICADO** — o formato ficha:10-42 exige o conjunto | Um commit para o lote ✔; EWM numa confirmação (triar:150). Se o EWM falha no meio do lote → `pendente` por linha (triar:163) ✔; "Próximos ids" cresce com todas | Idem F4. Mais de 15 itens → filtro (triar:135-136) | NÃO ESPECIFICADO (forma da ficha parcial) |
| F11 conflito de id | `backlog.md` (linha renumerada), `fatias/FT-<novo>-<slug>.md` (renomeada) | Sim | `.md` | Renomear arquivo não basta: `# FT-nnn` no cabeçalho (ficha:11), link `[ficha](fatias/FT-<nnn>-…)` na linha (backlog:46) e título do IB `[FT-nnn]` precisam mudar — triar:104-105 cita só "nome da ficha" (P3 S04-F11 confirmado). **backlog:79 diz "ids nunca são … renumerados"** × triar:104-106 renumera id que ainda não chegou à base → conflito normativo (ressalva só em triar:106) | Quem faz `git pull --rebase`: a pessoa (prod.json nega rebase/pull --rebase) ✔ coerente; commit novo pelo agente ✔; push de novo é da pessoa | Conflito de rebase no `backlog.md`: "mantenha o remoto, reaplique só a sua mudança" (backlog:84) ✔ | DIVERGENTE (backlog:79 × triar:106; renumeração incompleta) |
| F1 (Passo 1) | — (pré-condição de gravação) | Base: `<base>` do `sdd.md` (steer:59) ✔ | — | — | `git pull --ff-only` (permitido prod.json:73) ✔; troca de base com "sim", volta no fim (triar:26-27) ✔; **exige base e árvore limpa mesmo nos fluxos sem escrita (F7/F8)** — P2 já apontou | Árvore suja → avisa e para (triar:27-28) ✔ determinístico (P3 S04-X1 confere). `git switch` permitido em `sdd-produto` ✔ | OK (com lacuna de rigidez em fluxos somente-leitura) |

sem escrita: F7 (atendimento, triar:99), F8 (não fazer; só comentário EWM, triar:67-69), F9 antes do "sim", F1 até o Passo 3.

#### Achados de persistência — S04
- triar:101 × ficha:57 / steer:61: o commit "backlog.md e a ficha" não inclui o glossário alterado na triagem; sobra árvore suja e a triagem seguinte para (triar:27).
- triar:62 × triar:101: a ficha em `rascunho` existe em disco desde as rodadas mas só é commitada no Passo 3; "Próximos ids" só avança no Passo 3. Queda no meio deixa ficha órfã + FT-nnn aparentemente livre; nada diz como retomar (a retomada de triar:40-44 só procura **linha do backlog**, não ficha solta).
- triar:101-102 × prod.json:112 / steer:61: "push ou PR curto com o sim" não é executável por `sdd-produto` (`git push` e `gh/glab` não estão na lista; push negado); o texto da skill não diz "entregue o comando".
- backlog:79 × triar:104-106: ids "nunca renumerados" × renumeração antes da base; e a renumeração omite cabeçalho `# FT-nnn` (ficha:11) e link da coluna `ficha` (backlog:46).
- triar:150-151 × ficha:10-42: ficha de lote sem formato definido.
- ficha:13 `**Pedido por:**` sem regra de origem do valor; ficha:13 `padrão` × tmpl:7 `padrao`.
- P3 usa `backlog.md`/`fatias/…` sem `<produto>/` em vários blocos (F2, F4, F5, F6, F10, F11): caminho prescrito é `<produto>/…`.

---


## S05 · sdd-iniciar

### Parte 2 — Plano do fluxo esperado (Sonnet)


**Núcleo comum (N1–N8)** — usado pelos fluxos F1–F6:
- N1. Lê `.kiro/steering/sdd.md` (sem ele → `sdd-setup` e para — iniciar:19).
- N2. Passo 1: ordem de consulta do id: (1) `status.md` nas branches (atual, worktrees, remotas), (2) `backlog.md` da base, (3) EWM via `elm-ccm`, (4) pessoa; EWM e
  pessoa só completam (iniciar:23-27).
- N3. Passo 2: trilha vem do registro (seção de épico → padrão; `## Fatias — sem épico` → coluna `trilha`; seção antiga → rápida); se a trilha não serve → **S05-F12** (iniciar:44-47).
- N4. Passo 3 (tudo conferido **antes** de criar branch ou tocar o EWM; falhou → diz qual e o caminho, e não começa — iniciar:57-58): (1) DoR, (2) Responsável, (3) Sprint/encaixe/Kanban, (4) WIP, (5) registro publicado em `origin/<base>`.
- N5. Passo 4.1: sugere `<prefixo><ft>-<slug>` e **aguarda** confirmação; `git fetch` + `git switch -c <branch> origin/<base>` (iniciar:89-94).
- N6. Passo 4.2: `.kiro/specs/<ft>-<slug>/status.md` (de `tmpl`) + `.config.kiro` (`feature` na padrão, `bugfix` na rápida; direta sem `.config.kiro`).
- N7. Passo 4.3–4.4: backlog **não** muda; EWM (com power `elm`, pergunta única, só com "sim"): assume `[DEV]` com responsável = `whoami`, inicia (ação de
  `ccm_list_workitem_states`), estimativa se faltar; tarefa inexistente → `sdd-elm` modo *sprint* cria `[DEV][REV][VER]` (direta: só `[DEV]`) com pai conforme tabela
  iniciar:106-110; grava ids no campo ELM do `status.md`; sem MCP → `ELM pendente`.
- N8. Passo 4.5: commit pequeno do `status.md`; com "sim", push da branch (sinal de início). Passo 5: bloco `🚦 FT-<nnn> — título · trilha · modo · fase` / `Épico · Cobre · Branch · Pasta` / `Próximo: <skill>` (iniciar:119-123).

#### S05-F1 · Começar fatia de épico (trilha padrão com PRD)
- **Gatilho:** "vamos trabalhar na FT-031", "começar" (iniciar:3).
- **Pré-condições:** linha da FT em seção `## Fatias — EP-nn …`; PRD do épico; `decisoes.md` do épico; `acordos.md`; sprint aberta.
- **Processamento:** N2 → N3 (seção de épico = padrão) → N4 com DoR "padrão de épico": `pronta` ou passa agora — cenários em `cobre`, PRD `aprovado`/`fatiado`, nenhuma decisão
  bloqueante `em aberto`, `bloqueada-por` concluídas ou já na base, tamanho ≤ G, modo AFK/HITL (iniciar:61-63) → N5–N8 com `specType: feature`, `Fase: pesquisando`, tarefas `[DEV][REV][VER]` filhas do IB da fatia (iniciar:108).
- **Resultado:** branch `feature/ft-031-…` criada; `.kiro/specs/ft-031-<slug>/status.md` + `.config.kiro`; ids ELM no `status.md`; commit (+ push com "sim"); 🚦 com `Próximo: sdd-plano` (que começa pela `sdd-pesquisar`) (iniciar:127); AFK com várias fatias prontas → oferece `sdd-loop` (iniciar:134-135).
- **Lacunas:** ver S05-F3/F9 (Responsável e sprint); o campo `Responsável` do `status.md` (tmpl:12) não tem regra de preenchimento na skill.

#### S05-F2 · Começar fatia sem épico — trilha padrão (ficha)
- **Gatilho:** como F1, para FT da seção `## Fatias — sem épico` com `trilha` padrão.
- **Pré-condições:** ficha `fatias/FT-<nnn>-<slug>.md`.
- **Processamento:** N2–N8; DoR: ficha `aprovada por` o P.O., cenários `C<n>`, nenhuma decisão `em aberto`, tamanho ≤ G, modo declarado (iniciar:64-65); `Origem` no `status.md` = ficha; EWM: pai = item de origem (DF/IB) **sem IB novo**, ou IB `[FT-nnn]` filho do épico de Sustentação se for pedido em texto (iniciar:109-110).
- **Resultado:** igual F1, com `Cobre: ficha C1–Cn` no bloco 🚦 (iniciar:121); `Próximo: sdd-plano`.
- **Lacunas:** `tmpl:9` (campo Cobre) só prevê `HF-…`/`REG-…`/`—`, enquanto iniciar:121 imprime `ficha C1–Cn`; `tmpl:7` grava a trilha sem acento (`padrao|rapida`) e `backlog:44` com acento (`padrão|rápida`) — risco de busca/`sdd-status` divergir. Se a ficha estiver só `rascunho` (lote), falha na DoR e devolve à `sdd-triar` (S04-F2) — correto e fechado.

#### S05-F3 · Começar fatia — trilha rápida
- **Gatilho:** "corrigir o defeito 4567", "pegar a task 123", "começar" (iniciar:3), para fatia/linha de trilha `rápida` registrada.
- **Processamento:** N2–N8; DoR: comportamento esperado claro, sem regra nova, tamanho ≤ M, modo declarado (iniciar:66); `specType: bugfix`; caminho depois: "pesquisa curta → `bugfix.md` + `tasks.md` (teste que reproduz primeiro) → implementação → revisão → verificação → PR" (iniciar:52); `Fase: pesquisando`.
- **Resultado:** igual F1; `Próximo: sdd-plano`.
- **Lacunas:** a tabela de fases (iniciar:127) manda `pesquisando` para `sdd-plano` sem distinguir "pesquisa curta"; o `GATE na trilha rápida` do `sdd.md` (steer:63) não é mencionado no caminho da rápida (iniciar:52) — fica implícito na `sdd-plano`.

#### S05-F4 · Começar fatia — trilha direta
- **Gatilho:** como F3 para linha `trilha` direta.
- **Processamento:** N2–N8; DoR: pedido numa frase, sem regra nova, tamanho P (iniciar:67); pasta só com `status.md` (`Fase: implementando`, sem `.config.kiro`) (iniciar:97-98, tmpl:11); tarefas EWM: só `[DEV]`, pai = item de origem ou épico de Sustentação (iniciar:109-110); caminho: teste que falha (se houver comportamento) → mudança → backpressure → `sdd-revisar` (rubrica C sobre o diff, pedido no lugar dos critérios) → PR (iniciar:53). A direta **também** exige estar na sprint (iniciar:72-73).
- **Resultado:** `status.md` em `implementando`; 🚦 com `Próximo: sdd-implementar` ("Trilha direta") (iniciar:128).
- **Lacunas:** na direta o `Cobre` e as "Rodadas — verificação" do template (tmpl:9,13) não se aplicam; a pasta tem só `status.md`, mas `tmpl` mantém linhas de verificação — cosmético.

#### S05-F5 · Começar por número do EWM (DF, IB, tarefa)
- **Gatilho:** "pegar a task 123", "corrigir o defeito 4567" (iniciar:3).
- **Processamento:** N2; o número é localizado na linha do `backlog.md` com esse id em `origem` ou `elm`; tarefa `[DEV]`/`[REV]`/`[VER]` → a fatia do pai (iniciar:32). Não achou em (1) nem (2) → "não está registrado" → **S05-F8**. Achou → segue F1–F4 conforme a trilha.
- **Resultado:** o da trilha correspondente.
- **Lacunas:** tarefa `[REV]`/`[VER]` pega "a fatia do pai" mas o papel de quem pede não é a `[DEV]`; a skill assume que é para começar a implementação (Passo 4.4: assumir a tarefa "de quem implementa"). Quem pega a `[REV]` de uma fatia já em `revisando` cai em retomada (F7) sem tratamento do papel (iniciar:26-27 "se o papel pode começar" nunca é detalhado).

#### S05-F6 · "Próxima fatia"
- **Gatilho:** "próxima fatia" (iniciar:3, 33).
- **Processamento:** escolhe a `pronta` de maior prioridade da sprint aberta **sem `status.md` em nenhuma branch** (no Kanban: a do topo do backlog) → mostra a candidata → segue N3–N8.
- **Resultado:** o da trilha da fatia escolhida.
- **Lacunas:** não filtra por `responsavel` nem por `bloqueada-por` (só o DoR depois pega); escolher fatia atribuída a outra pessoa só gera a pergunta do item 2 (iniciar:70-71). Sem sprint aberta/sem acordos → cai no ramo "ofereça `sdd-planejamento`" (iniciar:76-77) sem dizer o que "próxima" significa.

#### S05-F7 · Retomar fatia já iniciada pela fase
- **Gatilho:** "retomar a FT-031", "começar"/"vamos trabalhar na FT-031" para fatia que já tem pasta (iniciar:3, 37-40).
- **Pré-condições:** `status.md` da fatia na branch atual, em worktree ou em branch remota (`git grep -l '<id>' <ref> -- '.kiro/specs/*/status.md'`).
- **Processamento:**
  1. Lê o `status.md` (fase, Histórico) e **não repete o Passo 3** (iniciar:38-39).
  2. Branch diferente da atual → pergunta se troca; alterações locais não commitadas → avisa e **para** (nunca stash/reset) (iniciar:39-40).
  3. Encaminha pela tabela de fases (iniciar:125-132): `pesquisando|planejando|plano-em-revisao` → `sdd-plano`; `implementando|revisando` → `sdd-implementar` (direta: seção Trilha direta); `verificando` → `sdd-verificar`; `aceita` → `sdd-implementar` (Passo 5: abrir PR); `pr-aberto` → aguardar merge (mergeado → `sdd-consolidar`); `bloqueada (de: <fase>)` → mostra motivo e a pergunta; resolvido → volta à skill da fase de origem.
- **Resultado:** bloco 🚦 com fase atual e `Próximo`; nenhum arquivo criado (o `status.md` só muda pela skill da fase).
- **Lacunas:** fase `concluida` ou `pr-aberto` já mergeado não têm linha na tabela clara (só texto no `pr-aberto`); fatia só em branch remota: a skill não diz como trazê-la (`git switch --track`). Ver também S05-F11.

#### S05-F8 · Entrada não registrada ou não-fatia (pedido novo, id fora do backlog, EP-nn)
- **Gatilho:** "vamos trabalhar em …" com pedido em texto, ou id (FT/EWM) que não está em `status.md` nem em `backlog.md`; ou `EP-nn` (iniciar:34-35).
- **Processamento:** pedido/id fora do backlog → carrega a **`sdd-triar`**, que registra e, "se a pessoa quiser começar agora, volta aqui com o id"; `EP-nn` → não é fatia: `sdd-prd` (ou `sdd-fatiar`, se o PRD já está aprovado).
- **Resultado:** handoff; nenhum arquivo.
- **Lacunas:** o retorno triar → iniciar quase sempre falha no Passo 3.3 (a fatia recém-triada tem `sprint` `—`) e no 3.5 (registro ainda não publicado): o loop é triar → iniciar → planejamento (encaixe) → iniciar. Fecha, mas sem sinalizar à pessoa logo no 📥 da triagem que "começar agora" exige encaixe (triar:119 menciona).

#### S05-F9 · Fatia fora da sprint aberta → Encaixe (desvio do Passo 3, item 3)
- **Gatilho:** evento: Passo 3.3 acha `sprint` do `backlog.md` ≠ sprint aberta (`**Situação:** aberta`) (iniciar:72-75).
- **Processamento:** não começa; remete à `sdd-planejamento` (seção Encaixe, plan:93-105): P.O. decide (entra na folga | entra no lugar de FT-… | fica para a próxima); grava `sprint`/`responsavel`/revisor/verificador no `backlog.md`, linha no `sprint-<nn>.md` com "encaixe: <decisão> (<quem>, <data>)", commit na base, `sdd-elm` *sprint* para as tarefas; depois volta à `sdd-iniciar`. Sem decisão registrada → não começa.
- **Resultado:** fatia na sprint (ou não) e retorno a iniciar.
- **Lacunas:** **plan:104** diz "volte à `sdd-iniciar` (Passo 3, item 4)" — item 4 é WIP; deveria ser retomar o item 3 e, depois do commit do encaixe na base, o item 5 (publicar). Sem MCP/PA, a criação das tarefas pelo encaixe e o Passo 4.4 da iniciar se sobrepõem (ambas criam `[DEV]` via `sdd-elm` *sprint* — iniciar:103-104 admite "encaixe aprovado agora").

#### S05-F10 · Projeto em Kanban ou sem sprint aberta
- **Gatilho:** `acordos.md` declara Kanban, ou nenhuma sprint aberta (iniciar:75-77).
- **Processamento:** Kanban → não há sprint nem encaixe; `sdd-elm` modo *sprint* põe as tarefas na iteração corrente do EWM ao começar (Passo 4). Nenhuma sprint aberta e nada no `acordos.md` (planejamento ainda não feito) → "não é encaixe": oferece `sdd-planejamento` e **não** começa.
- **Resultado:** começa (Kanban) ou desvia para `sdd-planejamento`.
- **Lacunas:** sprint **fechada** sem a seguinte aberta, mas com `acordos.md` Scrum: caso não cobre (não é Kanban nem "nada no acordos"). `sdd-atender` não trata Kanban (S06).

#### S05-F11 · WIP no limite / PR parado (desvio do Passo 3, item 4)
- **Gatilho:** contagem de fatias em `plano-em-revisao`, `aceita`, `pr-aberto` nos `status.md` das branches ≥ limite de `acordos.md` (sem arquivo: 2), ou PR parado > acordo (padrão 1 dia) (iniciar:78-82).
- **Processamento:** mostra quais e **recomenda** destravar antes (aprovar plano, revisar PR); a pessoa pode seguir: grava `WIP excedido: <motivo>` no Histórico do `status.md` ao criá-lo (Passo 4).
- **Resultado:** começa com a anotação, ou não começa.
- **Lacunas:** nenhuma de fidelidade ao texto; observação: o WIP é lido de branches locais/remotas desatualizadas se não houver `git fetch` antes (o fetch só ocorre em 4.1, depois da checagem).

#### S05-F12 · Trilha registrada não serve / DoR falha (devolução)
- **Gatilho:** ao ler o item, a "rápida" tem regra nova, a "direta" tem mais de um comportamento (iniciar:46-47), ou DoR do Passo 3.1 falha.
- **Processamento:** para, não cria branch/pasta/EWM; devolve: trilha → `sdd-triar` (refazer, S04-F2); DoR → `sdd-entrevistar`, `sdd-fatiar` (refinamento) ou `sdd-triar` (ficha/`falta:` das fatias sem épico) (iniciar:68-69).
- **Resultado:** mensagem com o item que falhou e o caminho; nenhum arquivo.
- **Lacunas:** nenhuma de handoff (fecha com S04-F2); a regra `iniciar:68-69` não diz qual dos três usar para cada falha (ex.: "decisão em aberto" de fatia de épico → `sdd-entrevistar`; "cobre vazio" → `sdd-fatiar`).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**Estado comum S05:** base `main`; `.kiro/steering/sdd.md` presente (prefixo `feature/`, Usa ELM = sim); `sprint-03.md` com `**Situação:** aberta`; `acordos.md` Scrum com WIP = 2; sem `status.md` em branch (salvo indicado); MCP elm presente; a pessoa que pede é `daniel`; `main` limpa.

#### S05-F1 · Começar fatia de épico

```text
S05-F1 · Começar fatia de épico ("vamos trabalhar na FT-031")
1. INPUT EXATO: "vamos trabalhar na FT-031"
   ESTADO: FT-031 em "## Fatias — EP-03": status pronta, sprint 3, responsável daniel, cobre HF-01#1.1, HF-01#1.2, REG-01, tamanho M, modo AFK, bloqueada-por —; EP-03 com PRD fatiado; decisoes.md do épico sem "em aberto"; origin/main tem a linha (git grep).
2. REGRAS:
   SE sdd.md existe ENTÃO segue — iniciar:19
   SE id FT-031 ENTÃO ordem de consulta: (1) status.md em branch: nenhum; (2) backlog.md: achou — iniciar:23-27
   SE seção de épico ENTÃO trilha PADRÃO — iniciar:44
   SE padrão de épico ENTÃO DoR: pronta; cobre preenchido; PRD fatiado; sem decisão em aberto; bloqueada-por —; M ≤ G; modo declarado — iniciar:61-63
   SE responsável é a própria pessoa ENTÃO não pergunta — iniciar:70
   SE sprint do backlog = sprint aberta ENTÃO segue — iniciar:72-74
   SE WIP abaixo do limite (2) ENTÃO segue — iniciar:78-79
   SE linha publicada em origin/main ENTÃO segue — iniciar:83-85
   SE passou no Passo 3 ENTÃO sugere a branch <prefixo><ft>-<slug> e AGUARDA confirmação — iniciar:89-93
3. OUTPUT GERADO: "Branch sugerida: feature/ft-031-<slug>
   Confirma, ou informe outro nome:" (iniciar:90-92)
   ARQUIVOS ESCRITOS: nenhum ainda. Depois do "sim": git switch -c, status.md (tmpl), .config.kiro (specType feature), commit.
4. VEREDITO MECÂNICO: AMBÍGUO (o <slug> da branch não tem regra de formação: iniciar:91 só mostra um exemplo)
```

#### S05-F2 · Começar fatia sem épico, trilha padrão (ficha)

```text
S05-F2 · Começar fatia sem épico, trilha padrão ("vamos trabalhar na FT-040")
1. INPUT EXATO: "vamos trabalhar na FT-040"
   ESTADO: FT-040 em "## Fatias — sem épico": trilha padrão, origem IB 613, ficha aprovada por ana.souza em 2026-10-15 com C1 e C2, decisões todas decididas, tamanho M, modo HITL, status pronta, sprint 3, responsável daniel; origin/main tem a linha e a ficha.
2. REGRAS:
   SE id do backlog ENTÃO ordem: status.md nenhum; backlog achou — iniciar:23-27
   SE seção sem épico ENTÃO trilha da coluna trilha = padrão — iniciar:44-45
   SE padrão sem épico ENTÃO DoR: ficha aprovada por <P.O.>, cenários C<n>, nenhuma decisão em aberto, tamanho ≤ G, modo declarado — iniciar:64-65
   SE sprint aberta, WIP abaixo do limite e linha publicada ENTÃO segue — iniciar:72-74, 78-79, 83-85
   SE padrão ENTÃO sugere branch e aguarda — iniciar:89-93
   SE status.md criado ENTÃO Origem = ficha (tmpl:6) ; Cobre = ??? (ver veredito) — tmpl:9
   SE EWM: item de origem IB 613 ENTÃO tarefas [DEV][REV][VER] filhas do IB 613, sem IB novo — iniciar:103-110 (tabela linha 109)
   SE padrão ENTÃO bloco 🚦 com Cobre: ficha C1–Cn; Próximo: sdd-plano — iniciar:120-121, 127
3. OUTPUT GERADO: "Branch sugerida: feature/ft-040-<slug> — Confirma, ou informe outro nome:"
   Depois do sim, bloco 🚦 FT-040 — <título> · trilha padrão · modo HITL · fase pesquisando
   Épico: — (sem épico) · Cobre: ficha C1–C2 · Branch: … · Pasta: .kiro/specs/ft-040-<slug>/ · Próximo: sdd-plano
   ARQUIVOS ESCRITOS: depois do sim: .kiro/specs/ft-040-<slug>/status.md com Cobre ??? · .config.kiro · commit
4. VEREDITO MECÂNICO: CONFLITO (ficha:49-50 diz que C1…Cn "são o cobre da fatia" e o plano e a verificação leem daí, × tmpl:9 só aceita HF-nn#c.c/REG-nn ou — para o campo Cobre do status.md; iniciar:121 imprime "ficha C1–Cn" no bloco)
```

#### S05-F3 · Começar fatia, trilha rápida

```text
S05-F3 · Começar fatia, trilha rápida ("corrigir o defeito 4567")
1. INPUT EXATO: "corrigir o defeito 4567"
   ESTADO: FT-033 em "## Fatias — sem épico": trilha rápida, origem DF 4567, ficha —, status pronta, tamanho P, modo AFK, sprint 3 aberta; origem DF 4567 com comportamento esperado já escrito; GATE na trilha rápida = não (steering).
2. REGRAS:
   SE número do EWM ENTÃO procura a linha com o id em origem ou elm — iniciar:24, 32
   SE achou a linha FT-033 ENTÃO trilha da coluna trilha = rápida — iniciar:45
   SE rápida ENTÃO DoR: comportamento esperado claro, sem regra nova, tamanho ≤ M, modo declarado — iniciar:66
   SE sprint aberta ENTÃO segue — iniciar:72-74
   SE rápida ENTÃO specType bugfix (.config.kiro); status.md Trilha rapida; Fase pesquisando — iniciar:96; tmpl:7, tmpl:11
   SE rápida ENTÃO caminho: "pesquisa curta → bugfix.md + tasks.md (teste que reproduz primeiro) → implementação …" — iniciar:52
   SE rápida ENTÃO bloco 🚦 com Próximo: sdd-plano (Fase pesquisando) — iniciar:127
3. OUTPUT GERADO: "Branch sugerida: feature/ft-033-<slug> — Confirma, ou informe outro nome:"
   Depois do sim, 🚦 FT-033 · trilha rápida · modo AFK · fase pesquisando · Próximo: sdd-plano
   ARQUIVOS ESCRITOS: .kiro/specs/ft-033-<slug>/status.md (trilha: rapida no tmpl:7; backlog usa rápida, backlog:44) · .config.kiro (bugfix) · commit
4. VEREDITO MECÂNICO: AMBÍGUO (iniciar:52 descreve "pesquisa curta → bugfix.md", mas nenhuma skill citada faz essa pesquisa curta; iniciar:127 manda a fase pesquisando para sdd-plano sem distinguir. Além disso, o valor da trilha no status.md pode ser "rapida" (tmpl:7) ou "rápida" (backlog:44))
```

#### S05-F4 · Começar fatia, trilha direta

```text
S05-F4 · Começar fatia, trilha direta ("vamos trabalhar na FT-036")
1. INPUT EXATO: "vamos trabalhar na FT-036"
   ESTADO: FT-036 em "## Fatias — sem épico": trilha direta, origem pedido: trocar texto do rodapé, sem ficha, status pronta, tamanho P, sprint 3 aberta, responsável daniel.
2. REGRAS:
   SE linha trilha = direta ENTÃO caminho: teste que falha (se houver comportamento) → mudança → backpressure → sdd-revisar → PR — iniciar:53
   SE direta ENTÃO DoR: pedido numa frase, sem regra nova, tamanho P — iniciar:67
   SE direta ENTÃO sprint aberta obrigatória (nem a direta começa fora da sprint) — iniciar:72-73
   SE sprint e WIP ok ENTÃO sugere branch e aguarda — iniciar:89-93
   SE direta ENTÃO pasta só com status.md, Fase implementando, sem .config.kiro — iniciar:97-98; tmpl:11
   SE EWM ENTÃO só [DEV]; pai = épico de Sustentação (origem é pedido em texto) — iniciar:109-110
   SE direta ENTÃO bloco 🚦 Próximo: sdd-implementar (Trilha direta) — iniciar:128
3. OUTPUT GERADO: "Branch sugerida: feature/ft-036-<slug> — Confirma, ou informe outro nome:"
   Depois do sim, 🚦 FT-036 · trilha direta · modo <…> · fase implementando · Próximo: sdd-implementar
   ARQUIVOS ESCRITOS: .kiro/specs/ft-036-<slug>/status.md (Fase implementando) · commit
4. VEREDITO MECÂNICO: AMBÍGUO (só o <slug> da branch, iniciar:91; o restante é determinado)
```

#### S05-F5 · Começar por número do EWM (tarefa [REV])

```text
S05-F5 · Começar por número do EWM ("pegar a task 124", [REV] de FT-031)
1. INPUT EXATO: "pegar a task 124"
   ESTADO: task 124 = [REV] FT-031 Revisar (no EWM, ligada pela coluna elm do backlog); feature/ft-031-bloquear-conta existe (não é a atual), com status.md, fase implementando, responsável joao.lima; a pessoa é daniel.
2. REGRAS:
   SE número do EWM ENTÃO procura a linha do backlog com esse id em origem ou elm — iniciar:32
   SE tarefa [DEV]/[REV]/[VER] ENTÃO a fatia do pai — iniciar:32
   SE achou em status.md de branch ENTÃO retomada pela fase; não repete o Passo 3 — iniciar:37-38
   SE branch diferente da atual ENTÃO pergunta se troca — iniciar:39
   SE fase implementando ENTÃO sdd-implementar — iniciar:127-128
   SE a fase decide se o papel pode começar ENTÃO ??? — iniciar:26-27 diz que a fase decide, sem tabela papel × fase
3. OUTPUT GERADO: "Branch feature/ft-031-bloquear-conta com a fatia em implementando (responsável joao.lima). Troco para ela? (sim)"
   Depois da troca, 🚦 FT-031 · fase implementando · Próximo: sdd-implementar (a [REV] não cabe nesse caminho)
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: SEM REGRA (iniciar:26-27 diz que a fase "decide se o papel pode começar", sem tabela de papel × fase; uma [REV] em fase implementando não tem caminho escrito; iniciar:101-102 só trata a [DEV] como o papel que começa)
```

#### S05-F6 · "Próxima fatia"

```text
S05-F6 · "Próxima fatia"
1. INPUT EXATO: "próxima fatia"
   ESTADO: sprint 3 aberta; FT-031 prioridade 1, pronta, responsável joao.lima, sem status.md; FT-040 prioridade 2, pronta, sprint 3, sem status.md; sem outras fatias na sprint.
2. REGRAS:
   SE gatilho "próxima fatia" ENTÃO escolhe a pronta de MAIOR prioridade da sprint aberta, sem status.md em nenhuma branch — iniciar:33
   SE prioridade é número ENTÃO "maior" = 1 ou = 2? — iniciar:33 e backlog:37 ("linhas na ordem de prioridade") não dizem o sentido
   SE candidata ENTÃO mostra e segue N3–N8 — iniciar:33
   SE responsável é outra pessoa ENTÃO pergunta se ela sabe — iniciar:70-71
3. OUTPUT GERADO: "Candidata: FT-031 — <título> · prioridade 1 · trilha padrão · modo AFK · responsável joao.lima. Ela sabe que vou começar? Sigo?"
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO (sentido de "maior prioridade" com número não definido: se 1 é a maior ou a menor; a tabela de prioridades não diz)
```

#### S05-F7 · Retomar fatia já iniciada pela fase

```text
S05-F7 · Retomar fatia já iniciada ("retomar a FT-031")
1. INPUT EXATO: "retomar a FT-031"
   ESTADO: feature/ft-031-bloquear-conta existe localmente (não é a atual; atual = main limpa); status.md com fase plano-em-revisao e Histórico; sem WIP excedido.
2. REGRAS:
   SE gatilho "retomar" ENTÃO procura status.md nas branches — iniciar:3, 23-24
   SE achou em status.md ENTÃO lê fase e Histórico; não repete o Passo 3 — iniciar:37-38
   SE branch diferente da atual ENTÃO pergunta se troca; árvore limpa, segue — iniciar:39-40
   SE fase plano-em-revisao ENTÃO sdd-plano — iniciar:127
   SE retomada ENTÃO não repete o Passo 3 e não cria arquivo (só o status.md muda pela skill da fase) — iniciar:38-39
3. OUTPUT GERADO: "FT-031 está em plano-em-revisao, na branch feature/ft-031-bloquear-conta. Troco para ela? (sim)" Depois da troca: 🚦 FT-031 · fase plano-em-revisao · Próximo: sdd-plano
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S05-F8 · Entrada não registrada (pedido em texto)

```text
S05-F8 · Entrada não registrada ("vamos trabalhar em: cadastro de chave Pix para o cliente")
1. INPUT EXATO: "vamos trabalhar em: cadastro de chave Pix para o cliente"
   ESTADO: pedido em texto; nada no backlog, nenhum status.md, nenhum AT.
2. REGRAS:
   SE pedido em texto, ou id que não está no backlog ENTÃO não está registrado → carrega sdd-triar — iniciar:35
   SE pessoa quer começar agora ENTÃO a triagem volta aqui com o id — iniciar:35
3. OUTPUT GERADO: "Não está registrado. Carrego a sdd-triar para registrar. Se quiser começar agora, volto com o id."
   ARQUIVOS ESCRITOS: nenhum (triagem é que escreve, depois)
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S05-F9 · Fatia fora da sprint aberta (encaixe)

```text
S05-F9 · Fatia fora da sprint aberta ("vamos trabalhar na FT-050")
1. INPUT EXATO: "vamos trabalhar na FT-050"
   ESTADO: FT-050 pronta, padrão, ficha aprovada, sprint 4 (sprint-04 planejada, não aberta); sprint 3 é a aberta; sem status.md.
2. REGRAS:
   SE DoR ok e sprint do backlog ≠ sprint aberta ENTÃO Encaixe: a decisão é do P.O., pela sdd-planejamento — iniciar:72-75
   SE sem decisão registrada ENTÃO não começa — iniciar:75; planejamento:104-105
   SE encaixe ENTÃO planejamento: P.O. escolhe entre folga | lugar de FT-… | próxima sprint — planejamento:93-98
   SE encaixe decidido ENTÃO grava sprint, responsável, linha no sprint-<nn>.md, commit, sdd-elm modo sprint — planejamento:100-103
   SE encaixe decidido ENTÃO "volte à sdd-iniciar (Passo 3, item 4)" — planejamento:104
   SE volta à sdd-iniciar ENTÃO tudo conferido antes de criar branch, inclusive a sprint (item 3) e o registro publicado (item 5) — iniciar:57-58, 72-74, 83-85
3. OUTPUT GERADO: "FT-050 está na sprint 4; a sprint aberta é a 3. Encaixe: decisão do P.O. pela sdd-planejamento. Opções: entra na folga | entra no lugar de FT-… | fica para a próxima. Não começo."
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (planejamento:104 manda voltar ao Passo 3 item 4 (WIP), pulando a conferência de sprint (item 3) e de registro (item 5), × iniciar:57-58 "tudo conferido antes de criar branch", e iniciar:72-74, 83-85)
```

#### S05-F10 · Kanban ou sem sprint aberta

```text
S05-F10 · Kanban ("começar a FT-060")
1. INPUT EXATO: "começar a FT-060"
   ESTADO: acordos.md declara Kanban; FT-060 pronta, padrão, ficha aprovada, sprint —; EWM disponível; sem sprint aberta.
2. REGRAS:
   SE Kanban (acordos.md) ENTÃO não há sprint nem encaixe — iniciar:75
   SE Kanban ENTÃO sdd-elm modo sprint põe as tarefas na iteração corrente do EWM ao começar — iniciar:75-76
   SE sdd-elm modo sprint ENTÃO entrada = número da sprint, iteração, time e as três seções do sprint-<nn>.md; é chamada depois do "ok" da sprint — elm:150-153
   SE DoR e WIP ok ENTÃO sugere branch e aguarda — iniciar:89-93
3. OUTPUT GERADO: "Kanban: sem sprint nem encaixe. Branch sugerida: feature/ft-060-<slug> — Confirma?"
   Depois do sim: sdd-elm modo sprint para criar [DEV][REV][VER] — o modo pede sprint-<nn>.md, que não existe no Kanban
   ARQUIVOS ESCRITOS: nenhum ainda
4. VEREDITO MECÂNICO: CONFLITO (iniciar:75-76 manda usar sdd-elm modo sprint no Kanban × elm:152-153 exige o número da sprint, as três seções do sprint-<nn>.md e a chamada depois do "ok" da sprint)
```

#### S05-F11 · WIP no limite e PR parado

```text
S05-F11 · WIP no limite ("vamos trabalhar na FT-070")
1. INPUT EXATO: "vamos trabalhar na FT-070"
   ESTADO: acordos.md Scrum, WIP = 2, PR parado = 1 dia (padrão); FT-031 em plano-em-revisao (feature/ft-031); FT-040 em pr-aberto (feature/ft-040) com PR aberto há 3 dias; FT-070 pronta.
2. REGRAS:
   SE conta fatias em plano-em-revisao, aceita, pr-aberto nos status.md das branches ENTÃO conta = 2 — iniciar:78-79
   SE conta ≥ limite ENTÃO mostra quais e recomenda destravar antes — iniciar:80-81
   SE PR parado há mais que o acordo ENTÃO mesma regra — iniciar:80
   SE "há mais tempo que o acordo" ENTÃO medido de quê? (data do PR, último commit, último status.md?) — ??? iniciar:80 não diz a fonte nem a data
   SE a pessoa quer seguir ENTÃO grava WIP excedido: <motivo> no Histórico ao criar o status.md — iniciar:81-82
   SE contagem em branches remotas ENTÃO a leitura não diz se precisa de git fetch antes; o fetch só ocorre no 4.1 — iniciar:78, 4.1 (iniciar:89)
3. OUTPUT GERADO: "WIP no limite (2): FT-031 plano-em-revisao, FT-040 pr-aberto há 3 dias (acordo: 1 dia). Recomendo destravar antes (aprovar o plano da FT-031, revisar o PR da FT-040). Sigo mesmo assim? Se sim, registro WIP excedido: <motivo>."
   ARQUIVOS ESCRITOS: nenhum agora
4. VEREDITO MECÂNICO: SEM REGRA (a regra de PR parado não diz como medir o tempo parado: iniciar:80-81 não tem fonte de data nem de estado do PR)
```

#### S05-F12 · Trilha registrada não serve (regra nova numa rápida)

```text
S05-F12 · Trilha não serve ("vamos trabalhar na FT-045")
1. INPUT EXATO: "vamos trabalhar na FT-045"
   ESTADO: FT-045 em "## Fatias — sem épico": trilha rápida, origem DF 4580, status pronta. Ao ler DF 4580, a descrição nova diz: "juros de mora passam a 2% — regra a definir".
2. REGRAS:
   SE rápida tem regra de negócio nova ENTÃO pare e devolva à sdd-triar para refazer a triagem — iniciar:46-47
   SE DoR da trilha falha ENTÃO devolve: sdd-entrevistar, sdd-fatiar (refinamento) ou sdd-triar (retomar a triagem) — iniciar:68-69
   SE devolve ENTÃO não cria branch, pasta nem item no EWM — iniciar:57-58; (regra de devolução)
3. OUTPUT GERADO: pela linha 46-47: "FT-045 não serve como rápida: tem regra nova. Devolvo à sdd-triar para refazer a triagem."
   pela linha 68-69: "DoR falhou (regra nova). Escolha: sdd-entrevistar, sdd-fatiar ou sdd-triar?"
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: AMBÍGUO (iniciar:46-47 manda à triagem; iniciar:68-69 põe três destinos para a mesma falha, sem critério de escolha: "decisão em aberto" → entrevistar? "cobre vazio" → fatiar? a regra não diz)
```

#### S05-X7 · Borda: fatia só em branch remota

```text
S05-X7 · Borda: "retomar a FT-031" com status.md só em origin/feature/ft-031-bloquear-conta
1. INPUT EXATO: "retomar a FT-031"
   ESTADO: a branch existe só no remoto (origin/feature/ft-031-bloquear-conta); não há cópia local.
2. REGRAS:
   SE status.md em branch remota ENTÃO conta como fatia já iniciada; lê a fase — iniciar:23-24, 37-38
   SE branch diferente da atual ENTÃO pergunta se troca — iniciar:39
   SE troca para branch só remota ENTÃO nenhuma regra diz como trazê-la (ex.: git switch --track) — (sem regra); iniciar:4.1 só cobre branch nova (origin/<base>)
3. OUTPUT GERADO: "FT-031 está em plano-em-revisao, na branch remota origin/feature/ft-031-bloquear-conta. Troco para ela (trazendo a branch)? (sim)"
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: AMBÍGUO (a pergunta de troca (iniciar:39) não define o que a troca faz para branch só remota; o "trazer" da branch não tem passo)
```

#### S05-X8 · Borda: EP-nn (épico, não fatia)

```text
S05-X8 · Borda: "vamos trabalhar no EP-03"
1. INPUT EXATO: "vamos trabalhar no EP-03"
   ESTADO: EP-03 com PRD aprovado; nenhuma fatia do EP-03 foi escrita pela sdd-fatiar ainda (ou elas estão em backlog).
2. REGRAS:
   SE id é EP-nn ENTÃO não é fatia: sdd-prd, ou sdd-fatiar se o PRD já está aprovado — iniciar:34
3. OUTPUT GERADO: "EP-03 é épico, não fatia. Como o PRD está aprovado, o próximo passo é a sdd-fatiar."
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### Tabela-resumo S05

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S05-F1 | AMBÍGUO | <slug> da branch sem regra de formação (iniciar:91) |
| S05-F2 | CONFLITO | Cobre do status.md: tmpl:9 (HF/REG ou —) × ficha:49-50 (C1…Cn são o cobre) |
| S05-F3 | AMBÍGUO | "pesquisa curta" (iniciar:52) sem skill; sdd-plano para pesquisando (iniciar:127); "rapida" × "rápida" |
| S05-F4 | AMBÍGUO | só o <slug> da branch (iniciar:91) |
| S05-F5 | SEM REGRA | papel [REV] × fase implementando: "a fase decide" sem tabela (iniciar:26-27) |
| S05-F6 | AMBÍGUO | "maior prioridade" com número: sentido não definido (iniciar:33; backlog:37) |
| S05-F7 | DETERMINÍSTICO | fase plano-em-revisao → sdd-plano; troca de branch com "sim" |
| S05-F8 | DETERMINÍSTICO | pedido fora do backlog → sdd-triar (iniciar:35) |
| S05-F9 | CONFLITO | planejamento:104 volta ao item 4 (WIP) × iniciar:57-58, 72-74, 83-85 (item 3 e 5 não reconferidos) |
| S05-F10 | CONFLITO | Kanban: iniciar:75-76 usa sdd-elm modo sprint × elm:152-153 exige sprint-<nn>.md e "ok da sprint" |
| S05-F11 | SEM REGRA | PR parado: como medir o tempo parado não está escrito (iniciar:80-81) |
| S05-F12 | AMBÍGUO | DoR falha com regra nova: triar (iniciar:46-47) × triar, entrevistar ou fatiar (iniciar:68-69) |
| S05-X7 | AMBÍGUO | fatia só remota: troca de branch sem passo para trazê-la (iniciar:39) |
| S05-X8 | DETERMINÍSTICO | EP-nn vai para sdd-fatiar com PRD aprovado (iniciar:34) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1–F4 (todas as trilhas) | `.kiro/specs/<ft>-<slug>/status.md` (iniciar:95) — relativo à raiz do projeto, **na branch nova da fatia** (nasce de `origin/<base>`, iniciar:94) | Sim. P3 escreve `.kiro/specs/ft-040-<slug>/status.md` ✔. `<ft>` minúsculo (`ft-040`) enquanto id/ficha são `FT-040`: grafia não definida em iniciar (só o exemplo iniciar:91) | `.md` | tmpl:1-42: título `# FT-<nnn> — <título>`, tabela `Campo·Valor` com 12 campos (Fatia, Origem, Trilha, Modo, Cobre, Branch, Fase, Responsável, Rodadas, PR, ELM, Banco DDL), seções `Achados abertos` e `Histórico` (1ª linha "fatia iniciada (sdd-iniciar) · trilha · modo"). **Trilha `padrao\|rapida\|direta` (tmpl:7) × `padrão\|rápida` no backlog (backlog:44) e na ficha (ficha:13)** (P3 S05-F3 confirmado). **Cobre (tmpl:9) só admite `HF-…/REG-…/—`**; fatia com ficha tem `C1…Cn` (ficha:49-50) e iniciar:121 imprime `ficha C1–Cn` no bloco 🚦 — o valor a gravar no arquivo não existe (P3 S05-F2 confirmado). **Responsável (tmpl:12): sem regra de preenchimento em iniciar**; só o loop define `agente:sdd-orquestrador` (sdd-loop:63); iniciar:102 usa `whoami` para o EWM, enquanto `responsavel` do backlog e `status` usam login do `equipe.json` (sdd-status:35) — três fontes de identidade. Campo ELM para origem DF/IB (tmpl:15 só prevê `IB <id>`) NÃO ESPECIFICADO | Quem grava: **só `sdd-orquestrador`** tem a skill e permissão (`.kiro/specs/**`, orq.json:41). Commit "do status.md" (iniciar:115) na branch da fatia ✔; push só com "sim" (orq.json:232 `ask`) ✔. **`.config.kiro` não é citado no commit** (iniciar:115 diz "status.md") → pode ficar não rastreado; plt:11 diz que a `sdd-plano` o cria "se faltar" (outro `specId`) | Branch nova: `git switch -c <branch> origin/<base>` (iniciar:94) **não está no allowlist de nenhum agente que carrega a skill** (orq.json:57-82 sem `switch`/`pull`; `whoami` idem) → bloqueado/pergunta; **NÃO ESPECIFICADO** como o agente cumpre. Árvore suja ao **criar** branch: só a retomada trata (iniciar:39-40); `switch -c` carrega alterações para a branch nova e `git add *` do commit as incluiria → NÃO ESPECIFICADO. Falha entre criar branch e gravar pasta (permissão/disco): sem reversão | DIVERGENTE (grafia trilha, Cobre) · NÃO ESPECIFICADO (Responsável, commit do `.config.kiro`, `switch -c` sem permissão, árvore suja em branch nova) |
| F1–F3 | `.kiro/specs/<ft>-<slug>/.config.kiro` | Sim (mesma pasta, iniciar:96) | JSON de **uma linha**, sem extensão `.json` (plt:11-16) | `{"specId":"<uuid>","workflowType":"requirements-first","specType":"feature"}`; `specType` `feature` (padrão) / `bugfix` (rápida) (iniciar:96; plt:18). Validado em `tmpl`: JSON ok, `uuidgen` permitido no orquestrador (orq.json:81). `workflowType` fixo `requirements-first` também para `bugfix` (plt:15-16 não distingue) — aceito pela skill, não verificável aqui. P3 cita só "`.config.kiro`" sem conteúdo | Gravado junto da pasta; commit: ver linha acima (omissão) | Idem; glob `.kiro/specs/**` deve casar arquivo oculto — depende do motor do Kiro (não verificável) | OK no formato · DIVERGENTE (fora do commit descrito) |
| F4 direta | `.kiro/specs/<ft>-<slug>/status.md` só, `Fase: implementando`, sem `.config.kiro` (iniciar:97-98; tmpl:11) | Sim | idem | `Cobre` e linhas "Rodadas — verificação" do template não se aplicam (cosmético) | idem | idem | OK |
| F1–F4 EWM | ids no campo ELM do `status.md` (iniciar:112-114); **backlog NÃO muda** (iniciar:99-100) | Confere com backlog:6-9 e steer:61 (backlog só na base) — P3 confirmado | — | Sem MCP → `ELM pendente` (iniciar:114); Histórico `ELM pendente: <ação>` → `ELM feito` (tmpl:40) | A `sdd-consolidar` leva os ids ao backlog (iniciar:113-114): até lá o backlog tem `elm` `—`/IB e o `status.md` tem as tarefas — duas fontes | MCP ausente → `pendente` ✔ | OK (duas fontes temporárias) |
| F11 WIP | linha `WIP excedido: <motivo>` no Histórico do `status.md` (iniciar:81-82) | Sim | append em Histórico (tmpl:39 "só acréscimo") | Formato da linha (data-hora + texto) confere com tmpl:42 | gravada na criação (iniciar:82) ✔ | **iniciar:78-80 lê `status.md` das branches remotas antes do `git fetch` (só em 4.1, iniciar:94)** → contagem sobre refs velhos | DIVERGENTE (fetch depois da leitura) |
| F9 encaixe (atravessa iniciar → planejamento) | `<produto>/backlog.md` (`sprint`, `responsavel`) + `<produto>/planejamento/sprints/sprint-<nn>.md` (linha, Observação `encaixe: <decisão> (<quem>, <data>)`) — escritos pela `sdd-planejamento`, não por iniciar | Sim: `sprints/sprint-<nn>.md` é `<produto>/planejamento/sprints/` (planejamento SKILL:22-23) | `.md` | Linha em `## Fatias` com 9 colunas (arq:112-117) ✔; "revisor e verificador" vão no `sprint-<nn>.md`, e `responsavel` no backlog (planejamento:100-102) | Commit na base e depois "volte à sdd-iniciar (Passo 3, item 4)" (planejamento:104) — item 4 é WIP; o item 5 (publicado em `origin/<base>`, iniciar:83-85) exige **push** que `sdd-produto` não faz → a pessoa precisa publicar; iniciar:83-85 diz "peça o push" ✔ | — | DIVERGENTE (planejamento:104 × iniciar:57-58, 83-85) |
| F5/F6 número / próxima fatia | nenhum | — | — | — | — | — | sem escrita |

sem escrita: F7 retomar (nenhum arquivo; troca de branch só com "sim"; branch só remota sem `--track`, iniciar:39 → NÃO ESPECIFICADO), F8 (handoff à triagem), F12 (devolução), F10 (Kanban/sem sprint: desvia ou começa como F1–F4), F5, F6, X8.

#### Achados de persistência — S05
- sdd-orquestrador.json:57-82 × iniciar:94, 102: a skill só está no agente que não tem `git switch`, `git pull` nem `whoami` no allowlist; a criação de branch prescrita não é executável sem prompt/negação. `sdd-produto` (que oferece "começar agora" a partir da triagem, triar:119) não tem iniciar nem permissão de escrever `status.md` (prod.json:40-47).
- iniciar:115 × plt:11: "commit pequeno do `status.md`" omite o `.config.kiro` (arquivo oculto, fácil de ficar fora).
- tmpl:7 `padrao|rapida` × backlog:44 / ficha:13 `padrão|rápida`; sem regra de normalização (grep: o `status.md` é lido por `sdd-status` só como exibição, sdd-status:21).
- tmpl:9 `Cobre` × ficha:49-50 / iniciar:121: nenhum valor prescrito no arquivo para fatia com ficha.
- tmpl:12 `Responsável` sem regra em iniciar (só sdd-loop:63); iniciar:102 `whoami` ≠ login do `equipe.json` (sdd-status:35).
- iniciar:83-85 `git grep … origin/<base>` roda antes do `git fetch` (iniciar:94): ref remota velha → falso "já publicado"/"só no local". Só confere `backlog.md`, não a ficha (iniciar:83 diz "a ficha" mas o comando não a busca).
- iniciar:39-40 trata árvore suja só na retomada; criação de branch nova com árvore suja não é tratada.
- planejamento:104 manda voltar ao "item 4".

---


## S06 · sdd-atender

### Parte 2 — Plano do fluxo esperado (Sonnet)


Arquivos (atender:19-25): `<produto>/atendimentos/README.md` (topo `Próximo: AT-013` + lista AT·pedido·situação, número nunca reaproveitado); `<produto>/atendimentos/AT-<nnn>-<slug>.md`;
`.kiro/local/atendimentos/AT-<nnn>/` (fora do git); seção Atendimento do `sprints/sprint-<nn>.md` aberto (consome a reserva). Setup cria `atendimentos/README.md` (sdd-setup/SKILL.md:243).

#### S06-F1 · Abrir atendimento
- **Gatilho:** "novo atendimento: o cliente X pediu …" (atender:27), "novo atendimento", "responde o chamado" (frases da description); evento: handoff da `sdd-triar` (S04-F7) ou lote com item de atendimento (triar:152-153).
- **Pré-condições:** `sdd.md`; sprint aberta; `README.md` de atendimentos; `equipe.json` (`atende: true`, entrev:119); power `elm` (opcional).
- **Processamento:**
  1. Chegou direto, sem triar → faz **antes** os Passos 1–2 da `sdd-triar` (já existe? é atendimento mesmo?) (atender:29-30). Não é atendimento (muda comportamento → fatia/rápida/direta; regra que ninguém decidiu → entrevista/PRD) → devolve à `sdd-triar` (atender:16-17; **S06-F5**).
  2. Número: lê `Próximo` do `README.md` e **já o incrementa** (atender:32).
  3. Entrevista curta — `sdd-entrevistar` modo atendimento (**S07-F2**): o que o cliente precisa receber, origem, prazo, quem responde, critério de pronto (atender:33-34).
  4. EWM, com confirmação — `sdd-elm` modo *atendimento*: `[ATD] AT-<nnn> <título>`, filha do item "Atendimento", `plannedFor` = iteração da sprint aberta (ou a indicada), responsável = quem atende, estimativa, estado em andamento (atender:35-37; elm:180-184).
  5. Grava `AT-<nnn>-<slug>.md` (formato atender:66-93), a linha no `README.md` e a linha na seção Atendimento do `sprint-<nn>.md`; commit na base (atender:38-39).
  6. Reserva estourada → avisa: o P.O. decide se alguma fatia sai; o atendimento não tira fatia sozinho (atender:39-40; plan:90-91).
- **Resultado:** `<produto>/atendimentos/AT-<nnn>-<slug>.md` (Situação `aberto`), linha no `README.md` (e `Próximo` incrementado), linha em `sprints/sprint-<nn>.md`, tarefa `[ATD]` no EWM (ou `ELM pendente`); próximo passo: **Executar** (S06-F2).
- **Lacunas:**
  - **Origem do EWM não é carregada:** quando o atendimento vem do lote (IB 615, triar:147) a `[ATD]` é filha do item "Atendimento" (atender:36), a entrevista recomenda "chamado" (entrev:117) e `atender:69` não manda gravar `DF/IB` em `**Origem:**`. Mas o lote só descarta o item se o id estiver em `**Origem:**` de um AT (triar:132-133,153) — o item volta em todo lote e continua `Novo` no EWM.
  - Não há passo de **verificar a base, `git pull --ff-only`, árvore limpa** nem de push/PR (triar:26-28,101-102; steer:61) — "commit na base" é tudo (atender:38).
  - Número incrementado antes da confirmação/commit: dois atendentes podem pegar o mesmo AT (não há tratamento de conflito de id como triar:102-106).
  - Sem sprint aberta / Kanban (iniciar:75-77 trata; atender:25,36-38 não): onde grava a linha e qual `plannedFor`?
  - Triar:56 diz que a `sdd-atender` "abre e já atende, na reserva da sprint"; atender não diz o que fazer se a reserva é 0 ou o `sprint-<nn>.md` não tem a seção Atendimento.

#### S06-F2 · Executar atendimento (consulta, extração, explicação)
- **Gatilho:** "extrai os dados de", "consulta na base para o cliente", "responde o chamado" (frases da description); continuação de F1.
- **Pré-condições:** AT aberto; MCP de banco (somente leitura) declarado no `sdd.md` (steer:62); bundle do ELM (`<rm.download.path>`); subagente `sdd-pesquisador`.
- **Processamento (atender:42-50):**
  1. Fontes, em ordem: banco pelo MCP (**somente leitura**) e bundle do ELM, via `sdd-pesquisador` "se houver"; código só se necessário e em escopo fechado (termos/arquivos indicados e limite de leitura).
  2. Resultado com dado real (linhas, telas, planilhas) → `.kiro/local/atendimentos/AT-<nnn>/` (fora do git; `.gitignore` por sdd-setup:246). No registro versionado: só SQL, contagem, caminho e resumo sem identificar pessoas (seção Consultas).
  3. Pedido que exige escrita no banco → não é atendimento: vira fatia/rápida (atender:99; **S06-F5**).
  4. Rascunho da resposta → **"ok" da pessoa**; quem envia é a pessoa; o agente não manda e-mail nem responde chamado.
- **Resultado:** arquivos em `.kiro/local/atendimentos/AT-<nnn>/…` (não versionados); tabela `## Consultas` no `AT-<nnn>-<slug>.md`; rascunho de resposta na conversa; próximo: Concluir (S06-F3).
- **Lacunas:** sem MCP de banco (`não há`, steer:62) ou sem bundle: não há alternativa nem aviso definidos; o modo de **retomar** um atendimento aberto numa sessão nova ("continuar o AT-012") não tem gatilho/passo; o agente `sdd-produto` tem permissão de escrita em `.kiro/local/atendimentos/**` (sdd-produto.json:46,237) mas não há instrução sobre confirmar que o arquivo está no `.gitignore` antes de gravar dado real.

#### S06-F3 · Concluir atendimento ("enviei", "conclui o AT-012")
- **Gatilho:** "enviei", "conclui o AT-012" (atender:52; description).
- **Pré-condições:** AT `aberto` com resposta aprovada pela pessoa e enviada por ela; `[ATD]` no EWM (ou `pendente`).
- **Processamento (atender:52-62):**
  1. Grava no registro a resposta enviada (sem dado de cliente; texto com dado real fica em `.kiro/local/`).
  2. Horas: pergunta as horas, **descontando o já lançado** na `[ATD]` → `sdd-elm` modo *horas* lança e conclui a tarefa, com confirmação (`elm:190-196`). Sem MCP/falha → `ELM pendente: lançar <h>h em [ATD] AT-<nnn>` no registro; o modo horas lança depois.
  3. Atualiza a situação (`concluido`) no `README.md` e no `sprint-<nn>.md`; commit na base.
  4. Encaminha a saída (→ **S06-F4**): defeito → `sdd-triar` (rápida, `origem` `AT-<nnn>`; começar → `sdd-iniciar`); regra que ninguém decidiu → `sdd-entrevistar` ou `sdd-prd`; consulta reaproveitável → lição (`sdd-aprender`).
- **Resultado:** `AT-<nnn>-<slug>.md` com `## Resposta enviada`, `## Horas`, `**ELM:** feito|pendente`, `**Saída:**`; `README.md`/`sprint-<nn>.md` atualizados; `[ATD]` concluída; commit na base.
- **Lacunas:**
  - **Contradição com `sdd-elm`:** atender:56 diz que o modo horas "lança e conclui a tarefa"; elm:194-195 diz "Lançar não conclui a tarefa; concluir é do modo conclusão ou da skill que chamou" e elm:184 põe a conclusão no modo atendimento ("depois do lançamento das horas"). Quem conclui a `[ATD]`?
  - O "consumido" da reserva (`## Atendimento — Reserva: <h>h · consumido: <h>h`, planejamento/references/arquivos.md:128) nunca é atualizado por atender:58 (só "situação").
  - Atualização do `sprint-<nn>.md` e do `README.md` só na base: mesma lacuna de F1 (troca de branch, push).

#### S06-F4 · Encaminhar a saída do atendimento
- **Gatilho:** passo 4 de F3 (atender:59-62).
- **Processamento:** (a) defeito → registra `**Saída:** FT-<nnn> (defeito)` após a `sdd-triar` criar a rápida com `origem` `AT-<nnn>` (começar → `sdd-iniciar`); (b) regra em aberto → `sdd-entrevistar`/`sdd-prd`; (c) consulta reaproveitável → lição (`sdd-aprender`), `**Saída:** lição L-nnn`.
- **Resultado:** campo `**Saída:**` do AT preenchido (`—` | `FT-040 (defeito)` | `D-07 em aberto` | `lição L-015`) e handoff.
- **Lacunas:** **(a)** atender:16-17 manda devolver à `sdd-triar` "regra que ninguém decidiu (entrevista ou PRD)"; atender:61 manda direto para `sdd-entrevistar`/`sdd-prd` — contradição e destino indefinido (entrev:18-20 exige `decisoes.md` de épico/fatia/ficha; sdd-prd:40 exige `EP-nn` registrado pela triagem). O correto seria triar. **(b)** O AT é commitado antes de o `FT-nnn`/`D-nn`/`L-nnn` existirem; não há passo para voltar e gravar a `Saída` depois.

#### S06-F5 · Devolução: "não é atendimento"
- **Gatilho:** pedido muda comportamento do sistema, exige escrita no banco, ou envolve regra não decidida (atender:16-17, 99).
- **Processamento:** não abre AT (ou, se já aberto, encerra como devolvido); devolve à `sdd-triar` (fatia/rápida/direta) — escrita no banco "vira fatia ou trilha rápida".
- **Resultado:** orientação ao usuário + handoff à triagem; nenhum arquivo novo (número do AT, se já incrementado, é queimado — "nunca reaproveitado", atender:21-22).
- **Lacunas:** não diz o que fazer com um AT **já aberto** que descobre no meio da execução que precisa de escrita (situação do registro? `[ATD]` a cancelar?). Só existem `aberto | concluido` (atender:70).

#### S06-F6 · Listar atendimentos abertos
- **Gatilho:** "atendimentos abertos" (description, atender:3).
- **Processamento:** a SKILL **não descreve** passo para isso; o que existe é `sdd-status:31-32` (lê `README.md` e os `AT-*.md` com `**Situação:** aberto`).
- **Resultado esperado (inferido de sdd-status):** lista AT · pedido · situação · prazo.
- **Lacunas:** gatilho declarado na description sem fluxo no corpo; sobreposição com `sdd-status` — risco de roteamento.

#### S06-F7 · Lançar horas sob pedido durante o atendimento
- **Gatilho:** "lança 2h no AT-012" no meio do atendimento.
- **Processamento:** atender:101 diz "Horas só na conclusão (ou sob pedido, pela `sdd-elm` modo *horas*); nunca no meio" — a sob-pedido é feita pela `sdd-elm` (elm:190-196, o AT aberto dá a `[ATD]`).
- **Resultado:** horas lançadas e, no `AT-…md`, tabela `## Horas`.
- **Lacunas:** a frase é contraditória ("sob pedido" × "nunca no meio"); não diz quem grava a tabela `## Horas` do registro.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**Estado comum S06:** sprint-03 aberta com reserva de atendimento de 16 h e 0 h consumidas; `atendimentos/README.md` com `Próximo: AT-013`; `equipe.json` com joao.lima `atende: true`; `Sustentação:` preenchida com IB Atendimento (612005); MCP elm presente; `sdd.md` com MCP de banco `@db/consulta` (somente leitura); bundle do ELM presente; subagente `sdd-pesquisador` disponível.

#### S06-F1 · Abrir atendimento

```text
S06-F1 · Abrir atendimento ("novo atendimento: o cliente Banco Norte pediu …")
1. INPUT EXATO: "novo atendimento: o cliente Banco Norte pediu a lista de contas bloqueadas em setembro para a auditoria (chamado 4521)"
   ESTADO: estado comum S06; nenhuma linha no backlog para o pedido.
2. REGRAS:
   SE "novo atendimento" ENTÃO abre — atender:27
   SE chegou direto ENTÃO faz antes os Passos 1–2 da triagem (já existe? é atendimento?) — atender:29-30
   SE Passos 1–2 da triagem ENTÃO busca em backlog, AT e status.md; classifica como atendimento (extração, sem mudança) — triar:37-39, 56
   SE Número ENTÃO lê Próximo do README (AT-013) e já o incrementa — atender:32
   SE abrir ENTÃO entrevista curta, sdd-entrevistar modo atendimento (uma rodada, A-1…A-5, com recomendação) — atender:33-34; entrev:108-119
   SE respostas ENTÃO vão para o cabeçalho do AT-013 — entrev:122
   SE Usa EWM ENTÃO sdd-elm modo atendimento: [ATD] AT-013, filha do IB 612005, plannedFor sprint 3, responsável joao.lima (quem atende), em andamento; com confirmação — atender:35-37; elm:180-184
   SE criou ENTÃO grava AT-013-<slug>.md, linha no README e no sprint-03.md; commit na base — atender:38
   SE reserva ENTÃO estourada? 16 h, consumo 0 → não — atender:39-40
3. OUTPUT GERADO: imediato:
   "Atendimento AT-013 · 5 perguntas"
   "A-1 · O que o cliente precisa receber? Recomendo: lista de contas bloqueadas em setembro."
   "A-2 · Origem? Recomendo: chamado 4521."
   "A-3 · Prazo? Recomendo: <data>." "A-4 · Quem responde? Recomendo: joao.lima." "A-5 · Critério de pronto? Recomendo: <…>."
   "sim aceita tudo"
   ARQUIVOS ESCRITOS: depois das respostas e do sim: atendimentos/AT-013-<slug>.md (Situação aberto) · README.md (Próximo: AT-014 + linha) · sprints/sprint-03.md (linha Atendimento) · commit
4. VEREDITO MECÂNICO: AMBÍGUO ("Pedido por" está no cabeçalho do AT (atender:69), mas nenhuma pergunta de A-1…A-5 nem regra de preenchimento o cobre (atender:33-34; entrev:115-119))
```

#### S06-F2 · Executar atendimento (extração)

```text
S06-F2 · Executar atendimento ("extrai os dados de contas bloqueadas de setembro do AT-013")
1. INPUT EXATO: "extrai os dados de contas bloqueadas de setembro do AT-013"
   ESTADO: AT-013 aberto; MCP de banco declarado (somente leitura); bundle presente; sdd-pesquisador disponível; a skill não confirma que .kiro/local/ está no .gitignore (ver veredito).
2. REGRAS:
   SE executar ENTÃO fontes nesta ordem: sdd-pesquisador → banco pelo MCP (somente leitura) → bundle do ELM — atender:44-45
   SE código ENTÃO só se necessário e em escopo fechado — atender:45-46 (aqui não se aplica)
   SE resultado com dado real ENTÃO vai para .kiro/local/atendimentos/AT-013/ (fora do git) — atender:47
   SE registro versionado ENTÃO só SQL, contagem, caminho e resumo SEM identificar pessoas — atender:48; atender:97-98
   SE pedido exige escrita no banco ENTÃO não é atendimento — atender:99 (não se aplica: consulta)
   SE rascunho da resposta ENTÃO "ok" da pessoa antes de enviar; o agente não envia — atender:49-50
3. OUTPUT GERADO: "Consulta executada: 1.284 contas. Arquivo: .kiro/local/atendimentos/AT-013/contas-bloqueadas-2026-09.csv (fora do git). No registro: SQL, contagem, caminho e resumo anônimo. Rascunho da resposta: <texto>. Você aprova antes de enviar?"
   ARQUIVOS ESCRITOS: .kiro/local/atendimentos/AT-013/*.csv (local) · atendimentos/AT-013-<slug>.md (seção Consultas) · commit só do registro
4. VEREDITO MECÂNICO: AMBÍGUO (o "resumo sem identificar pessoas" (atender:48) não tem critério: o que é identificador? A skill também não manda verificar o .gitignore de .kiro/local/, só assume "fora do git")
```

#### S06-F3 · Concluir atendimento ("enviei, conclui o AT-013")

```text
S06-F3 · Concluir atendimento ("enviei a resposta do AT-013 e conclui; foram 3 h")
1. INPUT EXATO: "enviei a resposta do AT-013 e conclui; foram 3 horas"
   ESTADO: AT-013 aberto; resposta aprovada e enviada pela pessoa; [ATD] 669380 existe no EWM; horas lançadas na [ATD]: 0; MCP elm presente.
2. REGRAS:
   SE "enviei" / "conclui" ENTÃO fluxo de conclusão — atender:52-53
   SE conclusão ENTÃO grava a resposta enviada (sem dado de cliente) — atender:54
   SE conclusão ENTÃO pergunta as horas, descontando o já lançado (0 h) → sdd-elm modo horas — atender:55; elm:190-193
   SE modo horas ENTÃO "lança e conclui a tarefa, com confirmação" — atender:56
   SE modo horas ENTÃO "lançar não conclui a tarefa; concluir é do modo conclusão ou da skill que chamou" — elm:194-195
   SE modo atendimento ENTÃO concluir depois do lançamento das horas (estado de conclusão) — elm:184
   SE conclusão ENTÃO atualiza situação em README e sprint-03.md; commit — atender:58
3. OUTPUT GERADO: "Horas: 3 h a lançar na [ATD] 669380 (AT-013, 2026-10-15), descontado 0 h. Confirma o lançamento? (sim)"
   Depois do sim: "Concluo também a [ATD]?" (a regra não diz quem conclui; ver veredito)
   ARQUIVOS ESCRITOS: AT-013-<slug>.md (## Resposta enviada, ## Horas, Situação concluido) · README.md · sprint-03.md · commit · EWM: horas com "sim"
4. VEREDITO MECÂNICO: CONFLITO (atender:56 diz que o modo horas "lança e conclui a tarefa" × elm:194-195 diz que lançar não conclui e que a conclusão é de outro modo; elm:184 põe a conclusão depois do lançamento no modo atendimento)
```

#### S06-F4 · Encaminhar saída (defeito)

```text
S06-F4 · Encaminhar saída: defeito encontrado ("AT-013 concluído; o saldo de contas bloqueadas está errado")
1. INPUT EXATO: "o AT-013 está concluído; a resposta mostra que o saldo de contas bloqueadas está errado no sistema"
   ESTADO: AT-013 concluído (commit feito); ainda sem Saída preenchida.
2. REGRAS:
   SE saída é defeito ENTÃO sdd-triar registra a rápida com origem AT-013 (começar → sdd-iniciar) — atender:60
   SE triagem criou a rápida ENTÃO registra **Saída:** FT-<nnn> (defeito) — atender:92; atender:60 — ver veredito
   SE triagem ENTÃO origem AT-013 vai para a coluna origem — triar:85 (exemplo AT-012)
3. OUTPUT GERADO: "Defeito: encaminho à sdd-triar (trilha rápida, origem AT-013)." Depois da triagem: "Saída do AT-013: FT-<nnn> (defeito)"
   ARQUIVOS ESCRITOS: depois da triagem, AT-013-<slug>.md campo Saída — mas a skill não tem passo para voltar ao AT depois do commit
4. VEREDITO MECÂNICO: AMBÍGUO (quando e onde gravar **Saída:** com o FT-nnn criado depois: atender:54-58 já fez o commit do AT e não há passo de retorno)
```

#### S06-F5 · Devolução: "não é atendimento"

```text
S06-F5 · Não é atendimento ("novo atendimento: o cliente quer que a consulta de CPF aceite CPF sem máscara")
1. INPUT EXATO: "novo atendimento: o cliente quer que a consulta de CPF aceite CPF sem máscara"
   ESTADO: estado comum S06; nenhum AT aberto para o pedido; o próximo número é AT-013.
2. REGRAS:
   SE "novo atendimento" ENTÃO passos 1–2 da triagem antes (já existe? é atendimento?) — atender:29-30
   SE triagem: muda comportamento do sistema ENTÃO não é atendimento; fatia, rápida ou direta — triar:56 (contraste) e atender:16-17
   SE não é atendimento ENTÃO devolve à sdd-triar — atender:16-17
   SE devolve antes do Passo 2 do atendimento ENTÃO o número não é lido nem incrementado (atender:32 vem depois) — atender:32
3. OUTPUT GERADO: "Não é atendimento: muda o comportamento do sistema (consulta de CPF). Devolvo à sdd-triar: fatia, rápida ou direta."
   ARQUIVOS ESCRITOS: nenhum · AT-013 não é reservado
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S06-F6 · Listar atendimentos abertos

```text
S06-F6 · Listar atendimentos abertos ("atendimentos abertos")
1. INPUT EXATO: "atendimentos abertos"
   ESTADO: README com AT-012 aberto e AT-013 aberto.
2. REGRAS:
   SE gatilho "atendimentos abertos" ENTÃO a description da skill tem o gatilho — atender:3
   SE no corpo ENTÃO há passos para abrir, executar e concluir; não há passo para listar — atender:27-62 (nenhum passo de listagem)
3. OUTPUT GERADO: nenhum formato definido na skill
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: SEM REGRA (a description promete o gatilho e o corpo não tem passo de listagem nem formato de saída)
```

#### S06-F7 · Lançar horas sob pedido durante o atendimento

```text
S06-F7 · Lançar horas sob pedido ("lança 2 h no AT-013")
1. INPUT EXATO: "lança 2h no AT-013"
   ESTADO: AT-013 aberto; [ATD] 669380; horas lançadas 0; MCP elm presente.
2. REGRAS:
   SE horas ENTÃO "Horas só na conclusão (ou sob pedido, pela sdd-elm modo horas); nunca no meio do atendimento" — atender:101 (a mesma frase tem as duas partes)
   SE pedido explícito de lançar ENTÃO sdd-elm modo horas — elm:188-189 ("sob pedido ('lança 4h')")
   SE modo horas ENTÃO tarefa = [ATD] do AT aberto; desconta o já lançado; data não futura; com confirmação; ccm_add_timesheet; não conclui — elm:190-195
   SE lançou ENTÃO tabela ## Horas do AT — atender:86-89 (quem grava não está dito)
3. OUTPUT GERADO: "Lanço 2 h na [ATD] 669380 (AT-013, 2026-10-15). Confirma? (sim)"
   ARQUIVOS ESCRITOS: depois do sim, AT-013-<slug>.md (## Horas) — quem grava não está definido
4. VEREDITO MECÂNICO: AMBÍGUO (atender:101 diz "sob pedido" e "nunca no meio" na mesma regra; elm:188 aceita o pedido, atender:101 proíbe no meio; a tabela ## Horas (atender:86-89) não tem autor)
```

#### S06-X1 · Borda: Kanban / sem sprint aberta

```text
S06-X1 · Borda: "novo atendimento: o cliente pediu o extrato de setembro" em Kanban (sem sprint aberta)
1. INPUT EXATO: "novo atendimento: o cliente pediu o extrato de setembro"
   ESTADO: acordos.md declara Kanban; nenhuma sprint aberta; README com Próximo: AT-013.
2. REGRAS:
   SE abrir ENTÃO lê Próximo e incrementa — atender:32
   SE abrir ENTÃO registra a linha na seção Atendimento do sprint-<nn>.md aberto; consome a reserva — atender:25, 38
   SE abrir ENTÃO [ATD] com plannedFor = iteração da sprint aberta — atender:36; elm:182
   SE não há sprint aberta ENTÃO nenhuma regra em atender — (sem regra); só iniciar:75-77 trata o Kanban
3. OUTPUT GERADO: nenhum: a skill não diz onde gravar a linha nem qual plannedFor usar
4. VEREDITO MECÂNICO: SEM REGRA (o atendimento exige sprint aberta e a reserva, sem fallback para Kanban ou sprint fechada)
```

#### S06-X2 · Borda: MCP de banco ausente (`não há`)

```text
S06-X2 · Borda: extração com MCP de banco "não há" (sdd.md)
1. INPUT EXATO: "extrai as contas bloqueadas de setembro do AT-013"
   ESTADO: sdd.md: MCP de banco = não há; bundle presente; sem sdd-pesquisador disponível.
2. REGRAS:
   SE executar ENTÃO fontes: sdd-pesquisador (se houver) → banco pelo MCP → bundle — atender:44-45
   SE sem banco ENTÃO nenhuma regra manda outra fonte (código só em escopo fechado: não serve para extrair dado) — atender:45-46
   SE a extração não tem fonte ENTÃO nenhuma regra diz o que fazer (sem resultado, sem aviso, sem AT devolvido)
3. OUTPUT GERADO: nenhum formato definido
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: SEM REGRA (ausência de banco na execução: a skill não tem caminho alternativo nem aviso)
```

#### S06-X4 · Borda: regra não decidida no encaminhamento

```text
S06-X4 · Borda: encaminhamento do AT-013 concluído com regra não decidida
1. INPUT EXATO: "o AT-013 está concluído; o cliente pergunta se o desconto de 10% vale para parcelas renegociadas — ninguém decidiu isso"
   ESTADO: AT-013 concluído; a pergunta é regra de negócio sem decisão.
2. REGRAS:
   SE regra que ninguém decidiu ENTÃO não é atendimento: devolve à sdd-triar — atender:16-17
   SE pedido que muda comportamento ou regra não decidida ENTÃO não é atendimento — atender:99
   SE saída é regra que ninguém decidiu ENTÃO sdd-entrevistar ou sdd-prd — atender:61
3. OUTPUT GERADO: duas saídas possíveis: "devolvo à sdd-triar" (atender:16-17) ou "sdd-entrevistar ou sdd-prd" (atender:61)
   ARQUIVOS ESCRITOS: AT-013 Saída: a definir
4. VEREDITO MECÂNICO: CONFLITO (atender:16-17 e 99 mandam devolver à sdd-triar × atender:61 manda direto para sdd-entrevistar ou sdd-prd; entrev:18-20 exige decisoes.md de épico/fatia/ficha e prd:40 exige EP-nn registrado pela triagem, então o destino direto não tem onde gravar)
```

#### S06-X5 · Borda: AT já aberto descobre que precisa de escrita

```text
S06-X5 · Borda: AT-013 aberto, a pessoa pede escrita no banco no meio da execução
1. INPUT EXATO: "agora também precisa gravar a faixa de bloqueio no banco de dev"
   ESTADO: AT-013 aberto; resposta ainda não enviada; [ATD] em andamento.
2. REGRAS:
   SE pedido exige escrita no banco ENTÃO não é atendimento; vira fatia ou trilha rápida — atender:99
   SE não é atendimento ENTÃO devolve à sdd-triar — atender:16-17
   SE AT já aberto ENTÃO a Situação só admite aberto | concluido — atender:70; nenhum estado para "devolvido"
   SE AT já aberto ENTÃO a [ATD] fica em andamento ou é cancelada? — nenhuma regra
3. OUTPUT GERADO: "A parte de escrita não é atendimento: devolvo à sdd-triar. O AT-013 fica como?" (sem resposta definida)
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA (o AT já aberto que vira escrita não tem situação nem destino na skill)
```

#### Tabela-resumo S06

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S06-F1 | AMBÍGUO | "Pedido por" no cabeçalho sem pergunta nem regra de preenchimento (atender:69; atender:33-34) |
| S06-F2 | AMBÍGUO | "resumo sem identificar pessoas" sem critério; .gitignore não verificado (atender:48) |
| S06-F3 | CONFLITO | modo horas "lança e conclui" (atender:56) × "lançar não conclui" (elm:194-195) |
| S06-F4 | AMBÍGUO | **Saída:** com o FT-nnn criado depois do commit do AT; sem passo de retorno (atender:54-58, 92) |
| S06-F5 | DETERMINÍSTICO | pedido que muda comportamento: devolve à triagem antes do número (atender:16-17, 29-30) |
| S06-F6 | SEM REGRA | gatilho "atendimentos abertos" na description, nenhum passo no corpo (atender:3) |
| S06-F7 | AMBÍGUO | "sob pedido" × "nunca no meio" na mesma regra (atender:101); tabela ## Horas sem autor (atender:86-89) |
| S06-X1 | SEM REGRA | Kanban / sem sprint aberta: sem onde gravar nem plannedFor (atender:25, 36) |
| S06-X2 | SEM REGRA | sem MCP de banco: sem caminho alternativo nem aviso (atender:44-46) |
| S06-X4 | CONFLITO | regra não decidida: devolver à triagem (atender:16-17, 99) × entrevista ou PRD direto (atender:61) |
| S06-X5 | SEM REGRA | AT já aberto que precisa de escrita: sem situação nem destino (atender:70, 99) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1 abrir | `<produto>/atendimentos/AT-<nnn>-<slug>.md` (atender:23) | Sim. P3 escreve `atendimentos/AT-013-<slug>.md` sem `<produto>/` — imprecisão | `.md` | Template atender:66-93: título `# AT-nnn · título`; cabeçalho `Origem·Pedido por·Prazo` / `Responsável·Tarefa ELM·Situação` / `Critério de pronto`; seções `Pedido, Consultas, Resposta enviada, Horas`, `ELM`, `Saída`. Mapeamento do modo atendimento: A-2→Origem, A-3→Prazo, A-4→Responsável, A-5→Critério (entrev:122); **A-1 ("o que receber") → `## Pedido` (atender:73-74), não cabeçalho (entrev:122 diz cabeçalho)**; **`Pedido por` sem pergunta nem regra** (P3 S06-F1/S07-F2 confirmado); `Tarefa ELM` quando o EWM falha na abertura: **NÃO ESPECIFICADO** (atender só trata `ELM pendente` na conclusão, atender:56; o sprint-nn admite `pendente`, arq:157) | **Quem/onde**: `sdd-produto` grava (`{{PRODUTO}}/**`) e commita "na base" (atender:38). **Nenhum passo para checar/trocar para a base, `git pull --ff-only` nem árvore limpa** (triar:26-28 tem; atender não) → pode gravar em branch de fatia (viola backlog:6-7 / steer:61). Push/PR: **não citado**; `sdd-produto` não pode `git push` | Pasta `atendimentos/` inexistente (setup cria o README, setup:243-244; em projeto sem setup recente): **NÃO ESPECIFICADO** | DIVERGENTE (base/pull/árvore) · NÃO ESPECIFICADO (`Tarefa ELM` pendente na abertura) |
| F1 | `<produto>/atendimentos/README.md` — `Próximo: AT-013` + tabela `\| AT \| Pedido \| Situação \|` | Sim (atender:21; setup:243-244) | `.md` | Formato do setup (`# Atendimentos`, `Próximo: AT-001`, tabela vazia) ✔. P3: "`Próximo: AT-014` + linha" ✔ | **"Lê o Próximo e já o incrementa" (atender:32) — mas só grava no passo 4 (atender:38)**: se EWM (passo 3) ou gravação falhar, número fica reservado só na memória; o `[ATD]` pode existir no EWM com `AT-013` enquanto o README continua `Próximo: AT-013` → colisão. **Sem conflito de id** (triar:102-106 só vale para FT/EP): dois atendentes pegam o mesmo AT-nnn; sem `pull` prévio, README velho | idem | NÃO ESPECIFICADO (falha no meio; conflito de AT-nnn) |
| F1 / F3 | linha na seção `## Atendimento` de `<produto>/planejamento/sprints/sprint-<nn>.md` da sprint **aberta** | **Ambíguo/DIVERGENTE:** atender:25 e 38 dizem `sprints/sprint-<nn>.md` (relativo a quê?); o caminho real é `<produto>/planejamento/sprints/` (planejamento SKILL:22-23; arq:104). P3 copia `sprints/sprint-03.md` sem `<produto>/planejamento/` | `.md`, tabela | Seção `## Atendimento` (arq:126-134): linha `Reserva: <h>h · consumido: <h>h` + tabela `AT·Pedido·Origem·Responsável·Horas·Tarefa ELM·Situação` (7 col). atender só diz "uma linha" (atender:38) sem listar as colunas; **a linha `consumido` nunca é atualizada** (atender:58 só "situação"; P2/P3 confirmam) — a reserva estourada (atender:39-40) é calculada sobre um número que ninguém grava; `sdd-status` (sdd-status:31) lê "reserva × consumido" | commit na base ✔ (mesma lacuna de base/pull) | **Sem sprint aberta/Kanban**: atender não diz onde gravar (iniciar:75-77 trata Kanban; atender não) → NÃO ESPECIFICADO (P3 S06-X1 confirmado). Reserva 0 ou seção `## Atendimento` ausente: NÃO ESPECIFICADO | DIVERGENTE (caminho do sprint) · NÃO ESPECIFICADO (Kanban/sem sprint; `consumido`) |
| F2 executar | `.kiro/local/atendimentos/AT-<nnn>/<arquivo>` (atender:24, 47) | Sim; coincide com steer:14 (`.kiro/local/<origem>/<id>/`). Relativo à raiz do projeto (não à worktree) | CSV/planilha/tela (livre) | Sem formato; só o caminho vai no registro (`Arquivo: … (fora do git)`, atender:81) | Sem commit (correto: fora do git). `sdd-produto` tem `fs_write` em `.kiro/local/atendimentos/**` (prod.json:46, 237) ✔. `.gitignore` com `.kiro/local/` é garantido pelo **setup** (setup:246), mas atender **não verifica** antes de gravar dado real — P3 S06-F2 "skill não manda verificar" confirmado em atender, atenuado pelo setup. Quem grava o CSV: o agente principal (o `sdd-pesquisador` só escreve `research.md`) | Pasta `AT-<nnn>/` inexistente: criar — NÃO ESPECIFICADO (a ferramenta de escrita normalmente cria, não dito). Sem MCP de banco / bundle: **NÃO ESPECIFICADO** (P3 S06-X2 confirmado). Projeto sem `.kiro/local/` no `.gitignore`: NÃO ESPECIFICADO | NÃO ESPECIFICADO (dir; MCP ausente) |
| F2 | `AT-<nnn>-<slug>.md` — seção `## Consultas` | Sim | tabela `# · Consulta (SQL) · Resultado` (atender:77-79) | Confere; "resumo sem identificar pessoas" sem critério (P3 confirmado) | commit "só do registro" — **atender não prevê commit nesse passo** (só em 1.4 e 3.3); P3 F2 acrescentou "commit só do registro" sem regra | — | DIVERGENTE (P3 inventa o commit; regra não existe) |
| F3 concluir | `AT-<nnn>-<slug>.md` (`## Resposta enviada`, `## Horas`, `**ELM:**`, `Situação: concluido`), README, sprint-nn | Mesmos caminhos | idem | `## Horas` `\| Data \| Horas \|` (atender:86-89): **quem grava a tabela não é dito** (a `sdd-elm` modo horas lança no EWM, elm:190-195, e escreve `ELM pendente` "no registro do AT"; a tabela local fica sem autor) — P3 S06-F7 confirmado. `**ELM:** feito\|pendente` ✔. `Situação` só `aberto\|concluido` (atender:70) | Commit na base ✔ (atender:58); `[ATD]`: atender:56 "lança e conclui" × elm:194-195 "lançar não conclui" (P3 confirmado) | Idem F1 | DIVERGENTE (conclusão da `[ATD]`) · NÃO ESPECIFICADO (autor de `## Horas`) |
| F4 saída | `AT-<nnn>-<slug>.md` — `**Saída:**` | Sim | `—\|FT-040 (defeito)\|D-07 em aberto\|lição L-015` (atender:92) | Valores ok; o AT já foi commitado em 3.3 **antes** de a triagem criar o `FT-nnn` (atender:58-60); **sem passo de retorno** para gravar a Saída (P3 S06-F4 confirmado); `FT-nnn` virá de outra sessão/agente | — | `sdd-entrevistar`/`sdd-prd` direto (atender:61) sem `decisoes.md` de épico/fatia/ficha (entrev:18-20) nem `EP-nn` (sdd-prd:50 grava "na pasta do épico") → destino de gravação inexistente; atender:16-17 manda à triagem | CONFLITO/NÃO ESPECIFICADO (Saída tardia; destino da decisão) |
| F1 (de lote) | `AT-<nnn>-<slug>.md` — `**Origem:**` | Sim | `**Origem:** chamado 4521` (atender:69; entrev:117 recomenda "chamado") | O lote (triar:132-133, 153) só tira o item do próximo lote se o id (DF/IB) estiver em `**Origem:**`; nem atender nem entrevistar mandam gravá-lo → item reaparece em todo lote e o `[ATD]` não se liga ao IB de origem (P2/P3 confirmado como falha de persistência) | — | — | DIVERGENTE (atender:69 × triar:132) |
| F5/F6 | nenhum (devolve; "atendimentos abertos" sem fluxo) | — | — | P3 F5: "AT-013 não é reservado" — **confirmado**: o número só é lido depois da triagem (atender:29-32) e só persistido em 1.4 | — | AT **já aberto** que vira escrita (X5): situação só `aberto\|concluido` → NÃO ESPECIFICADO | sem escrita (F5, F6); NÃO ESPECIFICADO (X5) |

#### Achados de persistência — S06
- atender:38, 58 × triar:26-28 / backlog:6-7 / steer:61: "commit na base" sem verificar a base, `git pull --ff-only` nem árvore limpa — três artefatos de produto (AT, README, `sprint-<nn>.md`) podem ir parar numa branch de fatia ou em README velho. Sem push/PR e sem tratamento de conflito de `AT-nnn` (README `Próximo:` e linha de AT são o ponto de disputa; triar:102-106 só cobre FT/EP).
- atender:32 × atender:38: número "já incrementado" mas persistido só no fim; falha no meio deixa `[ATD] AT-013` no EWM sem README/AT correspondentes.
- atender:25/38 `sprints/sprint-<nn>.md` sem `<produto>/planejamento/`; `consumido` nunca atualizado (arq:128); sem tratamento de Kanban/sem sprint.
- atender:69 × triar:132: `**Origem:**` sem id do EWM; o item do lote nunca sai.
- atender:58-60, 92: `**Saída:**` depende de um passo que ocorre depois do commit; sem retorno.
- atender:56 × elm:194-195: quem conclui a `[ATD]` (muda o que `[ATD]` fica no EWM e o `**ELM:**` do AT).
- Permissões: `sdd-produto` grava tudo que o atender prescreve (`{{PRODUTO}}/**` + `.kiro/local/atendimentos/**`, prod.json:40-47) — **sem divergência de permissão**; `git push` negado (atender não pede push; só não fecha o ciclo).

---


## S07 · sdd-entrevistar

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S07-F1 · Entrevista completa em rodadas (épico, PRD, fatia, plano, ficha)
- **Gatilho:** "me entreviste", "grill me", "vamos alinhar", "quais decisões estão em aberto", "o que falta definir" (entrev:3); eventos: chamada por `sdd-prd`, `sdd-fatiar`, `sdd-plano` ao encontrar decisão em aberto (entrev:3), por `sdd-triar` na trilha padrão (triar:61-63) ou na rápida/direta (triar:64-65).
- **Pré-condições / lê:** a demanda (texto, work item), `decisoes.md` se existir, glossário (caminho em `sdd.md`, padrão `docs/glossario.md`), ADRs, steering de produto, PRD/fatia em questão (entrev:25-26). Destino: `<produto>/epicos/<EP>-<slug>/decisoes.md` (épico), `.kiro/specs/<ft>-<slug>/decisoes.md` (fatia na branch) ou seção Decisões da ficha `<produto>/fatias/FT-<nnn>-<slug>.md` (triagem sem épico); quem chamou informa; chamada direta → pergunta **uma vez** (entrev:17-21).
- **Processamento:**
  1. Passo 1 (sem perguntar nada): monta a **árvore** de decisões (escopo → atores → comportamento → exceções → dados → integrações → não funcionais → fora de escopo), ordenada por dependência (entrev:27-29).
  2. Responde sozinho o que tem fonte e cita: código (`arquivo:linha`), bundle ELM (busca de texto do Kiro), glossário, banco (MCP somente leitura, se o `sdd.md` declarar); vira decisão `confirmada — fonte: …` (entrev:30-36). Pode mandar o subagente `sdd-pesquisador` buscar fatos (entrev:55-56).
  3. Passo 2: a cada rodada, só a **fronteira** (decisões cujos pré-requisitos estão decididos); até ~5 perguntas, numeradas `D-nn`, cada uma com Contexto e **Recomendo** (com motivo em uma linha); "sim" aceita todas; formato do cabeçalho `Rodada n · ramo · faltam ~k` (entrev:40-58).
  4. Respostas: vaga ("tanto faz") → registra a recomendada e diz isso; resposta que abre ramos → próxima rodada; termo novo/ambíguo → pergunta o termo canônico na rodada seguinte (entrev:58-61).
  5. Termina com fronteira vazia: resume as decisões e **pede a confirmação do entendimento** antes de quem chamou escrever qualquer coisa; "chega" antes → o que restar fica `em aberto` (entrev:62-63).
  6. Passo 3: registra em `decisoes.md` (cria na primeira; só acréscimo; decisão revista = linha nova que **substitui**; situações `decidida|confirmada|em aberto|substituída`) (entrev:67-81). Passo 4: linguagem ubíqua (**S07-F4**).
  7. Saída para quem chamou: `Entrevista — <EP|FT> · N decisões: d decididas · c confirmadas por fonte · a em aberto` / `Termos no glossário` / `Em aberto (bloqueiam?)` (entrev:102-106).
- **Resultado:** `decisoes.md` (ou seção Decisões da ficha) criado/atualizado; glossário atualizado conforme F4; resumo final para o chamador; o chamador (prd/fatiar/plano/triar) segue.
- **Lacunas:**
  - `entrev:3` lista só `sdd-prd`, `sdd-fatiar`, `sdd-plano` como chamadores; `sdd-triar` (triar:61-65), `sdd-iniciar` (iniciar:68) e `sdd-atender` (atender:61) também chamam, sem `Entrada`/modo próprios.
  - **Rápida/direta da triagem:** triar:64-65 usa "o formato da entrevistar" para uma rodada, mas a Entrada (entrev:17-21) só prevê épico, fatia e ficha — sem ficha (rápida com origem clara, direta) não há destino das respostas.
  - **Quem é o P.O.:** entrev:128 "decisão de negócio é de uma pessoa (P.O. ou delegado)", mas a skill não define como identificar a pessoa que decide nem preenche a coluna "Fonte / quem decidiu" (exemplo `ana.souza (P.O.)`, entrev:74) — depende do login (mesma lacuna de S04-F2).

#### S07-F2 · Modo atendimento (chamado pela `sdd-atender`)
- **Gatilho:** evento: `sdd-atender` Passo 1.2 (atender:33-34); description: "Modo atendimento: uma rodada curta para abrir um AT".
- **Pré-condições:** pedido do cliente; `equipe.json` (campo `atende`) para recomendar "quem responde".
- **Processamento (entrev:108-123):**
  1. **Uma rodada só**, mesmo formato (numerada `A-1…A-5`, com Recomendo, "sim" aceita tudo), **sem árvore e sem glossário**: O que o cliente precisa receber · Origem · Prazo · Quem responde · Critério de pronto.
  2. Regra de negócio em aberto → **não decide aqui**; a `sdd-atender` encaminha para entrevista completa ou PRD.
- **Resultado:** respostas vão para o **cabeçalho do `AT-<nnn>-<slug>.md`** (não para `decisoes.md`) (entrev:122); retorno à `sdd-atender` (que cria o `[ATD]`).
- **Lacunas:** o cabeçalho do AT (atender:69-71) tem `Origem`, `Pedido por`, `Prazo`, `Responsável`, `Tarefa ELM`, `Situação`, `Critério de pronto`; A-1 ("o que receber") cai na seção `## Pedido`, não no cabeçalho, e **"Pedido por"** não é perguntado em nenhuma pergunta (A-1…A-5); sem dica para registrar o id do DF/IB como Origem (ver S06-F1). Ausência de "confirmação do entendimento" explícita (basta o "sim" da rodada).

#### S07-F3 · Modo autônomo (`AUTONOMO=true`, chamada por agente sem pessoa)
- **Gatilho:** evento: orquestrador/loop chama com `AUTONOMO=true` (entrev:130-132).
- **Processamento:** **não pergunta**; monta a árvore, resolve o que tem fonte (Passo 1) e registra o restante como `em aberto` com a recomendada na coluna Decisão entre parênteses `(recomendada: …)`. Quem chamou não pode tratar recomendação como decisão.
- **Resultado:** `decisoes.md` com decisões `confirmada` e linhas `em aberto (recomendada: …)`; saída "Em aberto (bloqueiam?)" ao chamador (entrev:102-106).
- **Lacunas:** `sdd-loop` e `sdd-implementar` modo autônomo (que chamam) dizem que lacuna → `bloqueada`; aqui nada diz se a entrevista autônoma pode escrever o glossário na branch da fatia (cai na regra entrev:96-98, `termo pendente`). Nenhum conflito direto.

#### S07-F4 · Linguagem ubíqua / glossário (Passo 4, base × fatia)
- **Gatilho:** durante F1: termo de negócio novo, renomeado ou desambiguado (entrev:60-61, 83-85).
- **Processamento:**
  1. Cada termo → linha `| Termo | Definição | Evitar | Fonte | ELM |` do glossário do projeto (caminho do `sdd.md`); um termo por conceito, sinônimos em "Evitar"; código novo usa o canônico (revisor confere) (entrev:85-93).
  2. Termo já existente no ELM (bundle) → cita o id na coluna ELM; novo → `—` e, **num épico**, vira conceito `GL-<termo>.md` em `elm/` (`sdd-prd`), publicado como Termo de Glossário (`sdd-elm`) (entrev:94-95).
  3. Glossário é artefato de produto (só na base): entrevista de **fatia na branch dela** → **não grava** o glossário; registra `termo pendente` no `decisoes.md` da fatia, e a `sdd-consolidar` o leva ao glossário depois do merge (entrev:96-98; consolidar:66).
  4. Triagem (sdd-triar) roda na base → grava o glossário direto (ficha:57).
- **Resultado:** `docs/glossario.md` (base) atualizado, ou linha `termo pendente` no `decisoes.md` da fatia; resumo `Termos no glossário: <novos> novos · <alterados> alterados`.
- **Lacunas:** a regra de base × fatia (entrev:96-98) não cita a entrevista da triagem sem épico (ficha na base — grava direto, ficha:57) nem o caso `sdd-plano` sobre fatia sem épico (branch dela, `decisoes.md` em `.kiro/specs/…` — consolidar:31 cobre). O glossário na base exige commit/push com "sim", não dito na entrevistar.

#### S07-F5 · Revisão de decisão e consulta do que está em aberto
- **Gatilho:** "quais decisões estão em aberto", "o que falta definir" (entrev:3); ou decisão já registrada que a pessoa quer mudar.
- **Processamento:** lê o `decisoes.md`/ficha existente (entrev:25), lista as `em aberto`; se a pessoa muda uma decisão → **nova linha** (`D-nn · (revisa D-xx) …`, "decidida — substitui D-xx"), a antiga vira `substituída` (entrev:67, 77, 80-81); rodadas só para o que falta.
- **Resultado:** `decisoes.md` com linha nova que substitui; saída padrão ao chamador.
- **Lacunas:** a description tem os gatilhos "quais decisões estão em aberto"/"o que falta definir" mas o corpo só descreve entrevista completa; não há modo "listar" (sem perguntar) nem diz o que fazer com a ficha **aprovada** quando se revisa uma decisão (volta a rascunho — triar:160-161 e S04-F10; entrevistar não menciona).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**Estado comum S07:** `sdd.md` com glossário em `docs/glossario.md` e ELM = sim; ficha `fatias/FT-035-<slug>.md` em rascunho, seção Decisões vazia (só o cabeçalho), e o código tem `DescontoService.java:88` (cálculo do desconto sem teto); bundle presente; MCP elm presente.

#### S07-F1 · Entrevista completa em rodadas (fatia sem épico, chamada pela triagem)

```text
S07-F1 · Entrevista completa (chamada pela sdd-triar) ("me entreviste sobre o teto do desconto de pontualidade (FT-035)")
1. INPUT EXATO: "me entreviste sobre o teto do desconto de pontualidade (FT-035)"
   ESTADO: estado comum S07; chamador = sdd-triar (trilha padrão); destino = Decisões da ficha FT-035.
2. REGRAS:
   SE "me entreviste" ENTÃO a skill entra — entrev:3
   SE chamador é a triagem sem épico ENTÃO destino = seção Decisões da ficha — entrev:18-20
   SE Passo 1 ENTÃO lê demanda, decisões (vazias), glossário, ADRs, steering, ficha — entrev:25-26
   SE Passo 1 ENTÃO monta árvore: escopo → atores → comportamento → exceções → dados → integrações → não funcionais → fora de escopo — entrev:27-29
   SE fato tem fonte ENTÃO responde sozinho e cita — entrev:30-31 (código: DescontoService.java:88 → D-01 confirmada)
   SE não tem fonte e não é fato ENTÃO vai à fronteira (decisão da pessoa) — entrev:55-56 e 40-42 ("teto por parcela ou contrato" → D-02)
   SE rodada ENTÃO até ~5 perguntas, numeradas, cada uma com Contexto e Recomendo; "sim" aceita todas; cabeçalho "Rodada n · ramo · faltam ~k" — entrev:40-58
3. OUTPUT GERADO:
   "Rodada 1 · ramo: regra · faltam ~2 decisões depois desta rodada
    D-02 · O teto vale por parcela ou por contrato?
         Contexto: DescontoService.java:88 não tem teto.
         Recomendo: por parcela — é o que a demanda descreve.
    'sim' aceita as recomendações · ou responda por número"
   ARQUIVOS ESCRITOS: nenhum nesta rodada; depois das respostas, ficha FT-035 seção Decisões (criada na primeira vez; só acréscimo)
4. VEREDITO MECÂNICO: DETERMINÍSTICO
```

#### S07-F2 · Modo atendimento (chamado pela sdd-atender)

```text
S07-F2 · Modo atendimento ("Modo atendimento: AT-013 — extração de contas bloqueadas para a auditoria")
1. INPUT EXATO: chamada da sdd-atender: "Modo atendimento: AT-013 · pedido: lista de contas bloqueadas de setembro para a auditoria (chamado 4521)"
   ESTADO: estado comum S07; equipe.json com joao.lima atende: true; AT-013 em abertura.
2. REGRAS:
   SE modo atendimento ENTÃO uma rodada só, sem árvore nem glossário — entrev:108-110
   SE rodada ENTÃO perguntas A-1…A-5 com Recomendo: o que receber, origem, prazo, quem responde, critério de pronto — entrev:113-119; atender:33-34
   SE resposta ENTÃO vai para o cabeçalho do AT-<nnn>-<slug>.md, não para decisoes.md — entrev:122
   SE A-1 ("o que receber") ENTÃO atender:73-74 põe isso na seção ## Pedido do AT, não no cabeçalho
   SE regra de negócio em aberto ENTÃO não decide aqui; encaminha à sdd-atender — entrev:122-123
3. OUTPUT GERADO: "Atendimento AT-013 · 5 perguntas" + A-1…A-5 com Recomendo (formato entrev:113-119) · "sim aceita tudo"
   ARQUIVOS ESCRITOS: depois das respostas, AT-013-<slug>.md: cabeçalho (Origem, Prazo, Responsável, Critério de pronto) e seção ## Pedido (A-1) — conforme a regra pedir
4. VEREDITO MECÂNICO: CONFLITO (entrev:122 manda todas as respostas para o cabeçalho do AT × atender:73-74 põe "o que o cliente precisa receber" na seção ## Pedido; e "Pedido por" (atender:69) não é perguntado em nenhuma das cinco perguntas)
```

#### S07-F3 · Modo autônomo (AUTONOMO=true)

```text
S07-F3 · Modo autônomo ("AUTONOMO=true: FT-031 — rodada de decisões (chamado pelo sdd-loop)")
1. INPUT EXATO: "AUTONOMO=true · FT-031 (fatia do EP-03, na branch feature/ft-031-bloquear-conta) · decidir a mensagem da tela de bloqueio"
   ESTADO: fatia em worktree/branch; .kiro/specs/ft-031-bloquear-conta/ existe; D-03 = "mensagem da tela de bloqueio" sem resposta; MSG 2005 existe no bundle (fonte).
2. REGRAS:
   SE AUTONOMO=true ENTÃO não pergunta — entrev:130-131
   SE modo autônomo ENTÃO árvore; resolve o que tem fonte — entrev:130-131
   SE sem fonte ENTÃO registra como em aberto com a recomendada entre parênteses "(recomendada: …)" — entrev:131-132
   SE Passo 3 ENTÃO grava em decisoes.md (cria na primeira; só acréscimo) — entrev:67
   SE decisões de fatia ENTÃO o destino é .kiro/specs/<ft>/decisoes.md — entrev:18-19
   SE Passo 2 termina ENTÃO pede a confirmação do entendimento antes de quem chamou escrever — entrev:62-63 (em autônomo não há pessoa)
   SE saída ao chamador ENTÃO "Em aberto (bloqueiam?)" — entrev:102-106
3. OUTPUT GERADO: "Entrevista — FT-031 · N decisões: d decididas · c confirmadas por fonte · 1 em aberto
    Em aberto (bloqueiam?): D-03 mensagem da tela — sim: muda o comportamento (recomendada: MSG 2005)"
   ARQUIVOS ESCRITOS: .kiro/specs/ft-031-bloquear-conta/decisoes.md (linha D-03 em aberto (recomendada: MSG 2005)) — sem commit definido
4. VEREDITO MECÂNICO: AMBÍGUO (entrev:62-63 exige a confirmação do entendimento antes de escrever, e em modo autônomo não há pessoa para confirmar; a skill não diz se a confirmação cai ou se a escrita é feita sem ela)
```

#### S07-F4 · Linguagem ubíqua (termo renomeado na triagem)

```text
S07-F4 · Linguagem ubíqua ("o 'bloqueio' de conta passa a se chamar 'suspensão' de conta")
1. INPUT EXATO: "na FT-035: o 'bloqueio' de conta passa a se chamar 'suspensão' de conta; 'bloqueio' deixa de ser usado"
   ESTADO: triagem na base (main); docs/glossario.md tem a linha "Bloqueio de conta" com ELM GL 2050; sem épico.
2. REGRAS:
   SE termo renomeado ou desambiguado ENTÃO vai para o glossário — entrev:85
   SE um termo por conceito ENTÃO a linha canônica é "suspensão de conta"; "bloqueio" vai para Evitar — entrev:93
   SE termo já existe no ELM ENTÃO cita o id na coluna ELM (GL 2050) — entrev:94
   SE triagem roda na base ENTÃO grava o glossário direto — ficha:57; entrev:96 (só fatia na branch dela não grava)
   SE gravou ENTÃO resumo: Termos no glossário: 0 novos · 1 alterado — entrev:104
3. OUTPUT GERADO: "Termos no glossário: 0 novos · 1 alterado (Bloqueio de conta → Suspensão de conta; 'bloqueio' em Evitar; ELM GL 2050 mantido)"
   ARQUIVOS ESCRITOS: docs/glossario.md (linha alterada) · commit/push não citados pela entrevistar (ver nota)
4. VEREDITO MECÂNICO: DETERMINÍSTICO (o commit do glossário não está nesta skill, mas o passo que a skill descreve, a gravação, está definido)
```

#### S07-F5 · Revisão de decisão e consulta do que está em aberto

```text
S07-F5 · Revisão de decisão ("quais decisões estão em aberto na FT-035?" e depois "muda a D-02: teto de 12% por parcela")
1. INPUT EXATO: "quais decisões estão em aberto na FT-035?" · depois: "muda a D-02: o teto é 12% por parcela"
   ESTADO: decisoes (seção da ficha FT-035): D-01 decidida (teto por parcela, 10%), D-02 em aberto, D-03 confirmada (código). Ficha em rascunho.
2. REGRAS:
   SE gatilho "quais decisões estão em aberto" ENTÃO lê o decisoes/ficha existente — entrev:3, 25
   SE listar em aberto ENTÃO a skill não tem modo de listar; a lista só aparece na saída ao chamador (Passo 4; entrev:102-106) — entrev:3 × Passo 1–3
   SE "muda" uma decisão ENTÃO nova linha "D-nn · (revisa D-xx)" e a antiga vira substituída — entrev:67, 77, 80-81
   SE a decisão revisada era em aberto ENTÃO "revisa" não se aplica (não havia decisão anterior) — entrev:77 (escrito para decisão revista)
   SE a decisão aprovada muda ENTÃO ficha volta a rascunho — (triar:160 cobre; entrevistar não diz)
3. OUTPUT GERADO: sem modo de listar: a saída mais próxima é "Entrevista — FT-035 · … · 1 em aberto" (entrev:103) ou uma rodada (entrev:40-58). Depois: nova linha "D-04 · (revisa D-02) teto 12% por parcela | decidida — substitui D-02" (formato entrev:77) — mas D-02 estava em aberto, não decidida.
   ARQUIVOS ESCRITOS: ficha FT-035 (seção Decisões: nova linha)
4. VEREDITO MECÂNICO: AMBÍGUO (o gatilho "quais decisões estão em aberto" (entrev:3) não tem modo de listagem no corpo: a skill pode listar sem perguntar ou rodar uma rodada; e o formato "revisa" (entrev:77) não diz o que fazer com uma decisão que estava em aberto)
```

#### S07-X1 · Borda: chamada direta para tarefa rápida (sem ficha)

```text
S07-X1 · Borda: chamada direta de entrevista para um defeito de trilha rápida
1. INPUT EXATO: "me entreviste sobre o DF 4570 (erro de CPF sem máscara)"
   ESTADO: chamada direta (sem sdd-triar, sem épico); DF 4570 tem comportamento esperado escrito, então a ficha não é obrigatória (triar:92-94); nenhuma ficha existe para o DF 4570.
2. REGRAS:
   SE chamada direta ENTÃO pergunta uma vez onde registrar — entrev:20
   SE destino ENTÃO as opções do Entrada são épico (pasta do EP), fatia (.kiro/specs/<ft>/decisoes.md) ou ficha (Decisões) — entrev:17-20
   SE rápida sem ficha ENTÃO não existe pasta de fatia nem ficha — (sem regra: a entrevista não tem modo ou destino para rápida; triar:64-65 manda "o formato" sem destino)
3. OUTPUT GERADO: "Onde registro as decisões? (a) épico (b) fatia (.kiro/specs/…) (c) ficha da FT-…"
   A resposta "nenhum: é rápida sem ficha" não tem destino no texto da skill.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA (entrev:17-20 não tem destino para decisões de rápida sem ficha; triar:64-65 usa o "formato" da entrevista sem dizer onde gravar)
```

#### Tabela-resumo S07

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S07-F1 | DETERMINÍSTICO | rodada com destino na ficha (entrev:18-20, 40-58) |
| S07-F2 | CONFLITO | respostas no cabeçalho (entrev:122) × A-1 na seção ## Pedido (atender:73-74); Pedido por sem pergunta |
| S07-F3 | AMBÍGUO | confirmação do entendimento (entrev:62-63) × modo autônomo sem pessoa (entrev:130-132) |
| S07-F4 | DETERMINÍSTICO | termo renomeado na base: linha alterada, ELM mantido (entrev:85-94; ficha:57) |
| S07-F5 | AMBÍGUO | "quais em aberto" sem modo de listagem (entrev:3); "revisa" para decisão em aberto (entrev:77) |
| S07-X1 | SEM REGRA | chamada direta para rápida sem ficha: sem destino (entrev:17-20; triar:64-65) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1 (épico) | `<produto>/epicos/<EP>-<slug>/decisoes.md` (entrev:18) | Sim (`{{PRODUTO}}/**` permitido). Pasta do épico criada pela `sdd-prd` (backlog:23 link `epicos/EP-03-…/prd.md`); numa chamada direta antes do PRD, a pasta pode não existir: NÃO ESPECIFICADO | `.md`, tabela | entrev:70-78: cabeçalho `# Decisões — <EP-xx\|FT-xxx> <título>`, tabela 6 colunas `D·Pergunta·Decisão·Fonte/quem decidiu·Data·Situação`, situações `decidida·confirmada·em aberto·substituída`. **"Só acréscimo" (entrev:67) × situação `substituída` (entrev:80-81)**: a linha antiga teria de ser editada para `substituída`, mas o exemplo (entrev:74,77) deixa D-01 `decidida` e a nova diz "substitui D-01" → quem muda a Situação da antiga? (P3 S07-F5 confirmado e ampliado) | **Nenhum commit prescrito pela entrevistar**; quem chamou commita (sdd-prd:120 "Commit do PRD, do `decisoes.md`…") — chamada direta ("me entreviste") deixa `decisoes.md` não rastreado na base → árvore suja para a próxima triagem (triar:27). Termina com "confirmação do entendimento" antes de quem chamou escrever (entrev:62-63): gravação do `decisoes.md` pela entrevistar é no Passo 3 (entrev:67) — ordem confirmação × gravação **ambígua** | `sdd-produto` ✔. Fora da base? entrevistar não checa branch: se o épico é gravado numa branch de fatia → viola "só na base" (backlog:6-7) | NÃO ESPECIFICADO (commit/branch em chamada direta; Situação da linha substituída) |
| F1 (fatia em branch) | `.kiro/specs/<ft>-<slug>/decisoes.md` (entrev:19) | Sim; `.kiro/specs/*/decisoes.md` permitido ao `sdd-produto` (prod.json:44) e a `.kiro/specs/**` do orquestrador; na worktree `.kiro/local/wt/*/.kiro/specs/*/decisoes.md` (prod.json:45) ✔ | `.md` | idem | `decisoes.md` na branch da fatia; commit do `sdd-plano`/chamador; entrevistar silenciosa | Pasta `.kiro/specs/<ft>-<slug>/` ainda inexistente (triagem sem épico ainda não iniciou) → n/a, porque usa a ficha | OK (com commit do chamador) |
| F1 (triagem sem épico) | seção `## Decisões` dentro de `<produto>/fatias/FT-<nnn>-<slug>.md` (entrev:19-20; ficha:56) | Sim | `.md`, mesma tabela de 6 colunas (ficha:36-38 ✔ igual a entrev:72) | Confere com ficha. "Cria na primeira; só acréscimo" aplicado à seção; a ficha ainda não existe se a entrevista rodar antes (triar:62 diz que a ficha nasce na triagem) ✔ | Commit no Passo 3 da triagem (triar:101) — queda antes disso perde decisões (P2 já notou) | idem F4 do S04 | OK |
| F2 (modo atendimento) | cabeçalho de `AT-<nnn>-<slug>.md` (entrev:122) — a entrevistar não grava nada; devolve à `sdd-atender` | Sim (via atender) | — | A-1…A-5 × cabeçalho de atender:69-71: ver S06 (A-1 vai para `## Pedido`; `Pedido por` ausente) → CONFLITO confirmado | Quem grava: `sdd-atender` (1.4) ✔ | — | DIVERGENTE (entrev:122 × atender:73-74) |
| F3 autônomo | `.kiro/specs/<ft>-<slug>/decisoes.md` (e na worktree do loop) | Sim; o orquestrador tem `.kiro/local/wt/*/.kiro/specs/**` (orq.json:42) ✔ (a skill `sdd-entrevistar` não está nos resources do orquestrador, orq.json:16-20; seria invocada via outro agente) | `.md` | `em aberto` + `(recomendada: …)` na coluna Decisão (entrev:130-132) — coluna "Situação" `em aberto` ✔ | **entrev:62-63 exige confirmação do entendimento antes de gravar; em autônomo não há pessoa** → grava sem confirmação? Sem commit definido (P3 S07-F3 confirmado) | — | NÃO ESPECIFICADO (commit; confirmação em autônomo) |
| F4 glossário | `<glossário do sdd.md>` (padrão `docs/glossario.md`) — entrevista de fatia **na base** grava; na branch → `termo pendente` no `decisoes.md` (entrev:96-98) | Sim. `{{GLOSSARIO}}` permitido ao `sdd-produto` (prod.json:42) ✔; o `sdd-codificador` tem `./**` e **não** negaria o glossário (só `{{PRODUTO}}/**`), ou seja, a regra "só na base" não tem trava de permissão (só texto) | `.md`, tabela 5 colunas (entrev:88) | Confere. Formato do `termo pendente` no `decisoes.md` (qual coluna/Situação): **NÃO ESPECIFICADO** — a tabela só tem as 4 situações (`decidida·confirmada·em aberto·substituída`); `termo pendente` não é uma delas | **entrev:96-98 não cobre a triagem sem épico (base, grava direto — ficha:57) nem prescreve commit** (triar:101 também omite) → glossário alterado sem commit (ver S04); P3 S07-F4 "determinístico" é verdadeiro para a gravação, mas o fechamento (commit) falta | Glossário "não há": **NÃO ESPECIFICADO** (setup remove a permissão e as regras dos agentes, setup:123-125; entrevistar não tem ramo). Glossário inexistente: NÃO ESPECIFICADO | NÃO ESPECIFICADO (commit; "não há"; `termo pendente`) |
| X1 (rápida/direta sem ficha) | — (sem destino) | **NÃO ESPECIFICADO**: entrev:17-20 só prevê épico, fatia (`.kiro/specs/…`) e ficha; triar:64-65 usa o "formato" sem destino (P3 S07-X1 confirmado) | — | — | respostas ficam só na conversa | — | NÃO ESPECIFICADO |

sem escrita: F2 (a skill só devolve respostas; grava a `sdd-atender`); "quais decisões estão em aberto" (F5 do plano) não tem passo de listagem — só lê.

#### Achados de persistência — S07
- entrev:67 × entrev:80-81 × exemplo entrev:74,77: "só acréscimo" × linha antiga `substituída`.
- entrev:62-63 × entrev:67 × entrev:130-132: confirmação do entendimento antes de gravar; autônomo não tem pessoa.
- Entrevistar não define commit nem branch para `decisoes.md`/glossário; depende do chamador (sdd-prd:120 commita; chamada direta e triagem não: triar:101 omite o glossário).
- entrev:96-98: `termo pendente` não é um valor de Situação (entrev:80-81) e não tem coluna própria.
- entrev:21 × setup:123-125: glossário "não há" → agentes perdem a permissão (prod.json:42) e a skill não prevê o ramo.
- entrev:122 × atender:73-74: onde cai A-1.

---


## S08 · sdd-prd

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S08-F1 · Produzir o PRD do épico (entender → entrevistar → similares → escrever → revisão independente)
- **Gatilho inicial:** frases da description (prd:3): "escreve o PRD", "documenta a demanda", "épico", "especificar a demanda". Evento: a `sdd-triar` classificou a demanda como **épico** e registrou `EP-nn` `rascunho`, `prd` `—` (prd:24, 40; triar:78; sdd/SKILL:83). Só épico chega aqui; fatia com regra clara é padrão sem épico, com ficha (prd:24-25).
- **Pré-condições / arquivos lidos:** `.kiro/steering/sdd.md` e o steering de produto (prd:27); descrição longa da demanda (da triagem ou pedida à pessoa); linha do épico em `<produto>/backlog.md` (prd:40); bundle do ELM `<rm.download.path>`, código, glossário e ADRs (prd:35-38); work item do EWM via `elm-ccm` se existir (prd:32-33); `references/prd-template.md`, `references/okf-elm.md`; rubrica P de `../sdd-revisar/references/rubricas.md` (prd:103).
- **Processamento interno:**
  1. **Passo 1.1** — pedir/ler a descrição longa (quem pediu, problema, exemplos, prazos); item do EWM → `elm-ccm`.
  2. **Passo 1.2** — explorar antes de perguntar (subagente `sdd-pesquisador` se houver, senão você, só leitura): bundle do ELM (o PRD **altera**, não duplica), código, glossário/ADRs; registrar fontes (id ELM, `arquivo:linha`).
  3. **Passo 1.3** — id: o `EP-nn` registrado pela triagem. Se **não há registro** → a demanda não passou pela triagem → carregar `sdd-triar` (prd:40-41). Pasta `<produto>/epicos/<EP>-<slug>/` (kebab, sem acento); na linha do épico, `prd` = link do `prd.md`.
  4. **Passo 1.4** — projeto com ELM e coluna `elm` do épico `—`/`pendente` → `sdd-elm` modo *backlog*, só o épico (`[EP-nn] <título>`, descrição = problema), com confirmação; id vai para a coluna `elm`. Sem MCP → `ELM pendente: épico EP-nn` no rodapé do PRD.
  5. **Passo 2** — rodar `sdd-entrevistar` gravando `decisoes.md` na pasta do épico; termina quando a árvore de decisões fecha ou a pessoa diz "chega" (prd:50-51).
  6. **Passo 3.1 (obrigatório, projeto com ELM)** — listar os artefatos propostos (tipo, título provisório, palavras-chave) → `sdd-elm` modo *similares* (nunca o MCP direto) → mostrar a tabela e pedir **uma decisão por artefato com acerto**: igual → reutilizar (ou criar com motivo); sobrepõe → alterar (ou criar com motivo); relacionado → criar novo citando o existente em `## Relações`; nenhum → criar. Registrar cada decisão em `decisoes.md` (`D-nn`) e na coluna "No ELM" (`reusa <id>` · `altera <id>` · `novo (verificado <data>)`; sem MCP: `novo (só bundle <data>)`). Artefato surgido depois passa por aqui de novo. Projeto sem ELM → pula.
  7. **Passo 3.2** — preencher `prd.md` (template) e criar em `elm/` um conceito OKF por artefato (`HF-nn-<slug>.md`, `REG-nn-<slug>.md`, `GL-<termo>.md`) com `status: draft`, `sources`, `generated`; mais `index.md` e entrada `**Creation**` no `log.md`. Regras: histórias com 4 tipos de cenário (feliz, não aceito, repetição, erro em um item) e "Então" verificável; regras testáveis com valor e `D-nn`; **alteração** → copiar o conceito do bundle (ou `rm_get_requirement` via `elm-rm`) mantendo `resource`/`id`/`sources` do ELM, `draft`, `generated` novo, reescrever no estado depois; **reutilizar** → HF embute a REG existente, sem arquivo em `elm/`; HF→REG por link relativo (vira embed na publicação); decisões de implementação sem caminho/código; propor **pontos de teste (seams)** e **confirmar com a pessoa**; > ~8 histórias ou > 1 objetivo → propor dividir em dois épicos **antes** de escrever.
  8. **Passo 4** — `sdd-revisor` com rubrica **P** (sem o agente, aplicar você mesmo sem usar o raciocínio do autor); corrigir achados (até 2 rodadas); decisão de negócio volta à entrevista; `status: em-revisao` durante.
- **Resultado final (output):**
  - Resposta: o PRD pronto para o GATE (segue para S08-F2); perguntas de decisão por artefato com acerto, confirmação dos seams, proposta de divisão em dois épicos se for o caso.
  - Arquivos: `<produto>/epicos/<EP>-<slug>/prd.md` (frontmatter `id`, `titulo`, `status`, `po`, `demanda`, `atualizado`; seções Problema, Solução, Atores, tabela de artefatos, Decisões de implementação, Decisões de teste, Não funcionais, Fora de escopo, Em aberto, rodapé "Artefato produzido com apoio de IA…"), `<pasta>/decisoes.md`, `<pasta>/elm/{HF,REG,GL}-*.md`, `elm/index.md`, `elm/log.md`; coluna `prd` (e `elm`) na linha do épico em `backlog.md`.
  - ELM: só o épico no EWM (Passo 1.4) e leituras (similares); nenhuma escrita de requisito até o GATE.
  - Próximo passo: GATE do PRD (S08-F2).
- **Lacunas observadas:**
  - **Dono do "épico no EWM" diverge:** mapeamento:13 diz "quando o `EP-nn` nasce (`sdd-prd`)"; elm:126-127 e triar:78-82 dizem que a `sdd-triar` o cria (a `sdd-prd` só se ficou `pendente`, prd:43-46); elm:160 dá ainda ao planejamento o caso `pendente`/`—`. Três donos para o mesmo passo; o texto do mapeamento está desatualizado.
  - **Nenhuma checagem/menção à `[ESP]` do épico:** prd:45 só diz que o pai "existe para a `[ESP]` do planejamento". O PRD pode ser escrito sem `[ESP]` na sprint (plan:57-60 só planeja `[ESP]` para épicos "em entrevista/PRD/fatiamento nesta sprint") e a skill não avisa nem pergunta; contradiz "toda hora tem tarefa" (steering:16, plan:134). As horas só são tratadas em fatiar:80-83.
  - **Status do épico no `backlog.md` não é gravado nas transições:** backlog.md:62 atribui o "status do PRD" à `sdd-prd`, mas prd só cita o `backlog.md` no commit do GATE (prd:121) e na gravação do link `prd` (prd:42); `rascunho→em-revisao` (prd:105) não diz se atualiza a coluna `status` do épico.
  - Divisão em dois épicos (prd:98) não tem fluxo: não diz quem registra o segundo `EP-nn` (pelo `Próximos ids`/`sdd-triar`), nem como repartir `decisoes.md`.
  - "Até 2 rodadas" (prd:104): o que fazer se restarem achados BLOQUEANTE na 3ª — só o card do GATE tem "achados aceitos" (prd:113), sem regra de quem pode aceitar um BLOQUEANTE.
  - O pesquisador não tem o MCP do ELM (sdd/SKILL:122-124), mas prd:35-37 manda explorar "ELM" por ele: só dá para o bundle; consultas ao vivo ficam para a `sdd-elm` (aceitável, mas não dito).

#### S08-F2 · GATE do PRD (aprovação pelo P.O.)
- **Gatilho inicial:** "aprova o PRD" (prd:3) ou fim do S08-F1 com revisão limpa (prd:107).
- **Pré-condições / arquivos lidos:** `prd.md` (`em-revisao`), `decisoes.md`, `elm/*.md`, resultado da revisão (rubrica P, incl. P8 e P11); quem aprova = "o P.O. ou quem ele delegou" (prd:114; sdd/SKILL:50 diz P.O.).
- **Processamento interno:**
  1. Mostrar o card (prd:109-115): histórias (e cenários), regras, termos novos, "No ELM" (reusa/altera/novos verificados), decisões decididas × em aberto (bloqueantes), resultado da revisão; perguntar "Aprovar?".
  2. Decisão **em aberto que muda comportamento** → **não há aprovação**; volta à entrevista (prd:117).
  3. Aprovado → `prd.md`: `status: aprovado`, versão `1.0`, data e aprovador no rodapé; **em cada** conceito de `elm/`: `status: stable` e `verified: { by: human:<login de quem aprovou>, at: <agora> }` (sem esse `verified` a `sdd-elm` não publica, okf:61); `**Update**` no `log.md`; commit de PRD, `decisoes.md`, `elm/` e `backlog.md` na **base**, direto ou por PR curto (steering:61); nunca em branch de fatia.
  4. Próximo passo na mesma resposta: (1) `sdd-elm` modo *requisitos* (se usa ELM e publicação = `na-aprovacao`); (2) `sdd-fatiar`.
- **Resultado final (output):**
  - Resposta: confirmação da aprovação + os dois próximos passos.
  - Arquivos: `prd.md` (aprovado, 1.0), `elm/*.md` (stable + verified), `elm/log.md`, `backlog.md` (ver lacuna), commit na base; push/PR só com "sim" (o agente `sdd-produto` entrega o comando, steering:61).
  - ELM: nada ainda; publicação via S11-F2 se `na-aprovacao`.
  - Handoff: `sdd-elm` requisitos → `sdd-fatiar`.
- **Lacunas observadas:**
  - **Sem condição de entrada:** "aprova o PRD" numa sessão nova com PRD em `rascunho` (sem revisão) ou `em-revisao` não tem regra (reexecutar a rubrica P? reapresentar o card?). prd:107-126 assume continuidade do F1.
  - **Origem do login** em `verified.by: human:<login>` (prd:119): não diz como o agente obtém o login do aprovador (perguntar? `whoami`?). okf:61 diz "login do P.O." e prd:119 "login de quem aprovou" (delegado) — pequena divergência.
  - **Atualização do épico no EWM depois do GATE:** elm:130 prevê que a descrição do épico receba "solução do PRD + link do PRD" depois do GATE, mas o handoff de prd:123-126 não chama `sdd-elm` modo *backlog* para isso.
  - **Publicação `no-merge`:** prd:124-125 só trata `na-aprovacao`; para `no-merge` não diz o que dizer à pessoa (a publicação fica para `sdd-consolidar`, consolidar:40-41) — e isso interage com a lacuna do link "implementa" em S11-F4.
  - Os dois "próximos passos" são numerados 1 e 2, mas a ordem importa quando a publicação é `na-aprovacao` (HF/REG/GL antes dos IBs, para o link "implementa"); o texto não diz que 1 precede 2.
  - Quais campos de `backlog.md` mudam no commit (status do épico `aprovado`?) não é dito (prd:121).

#### S08-F3 · Mudança depois de aprovado (PRD `aprovado`/`fatiado`)
- **Gatilho inicial:** "pedido explícito" de mudança num PRD aprovado/fatiado (prd:130). Eventos de outras skills: drift de **negócio** na consolidação (consolidar:34-35 manda acionar a `sdd-prd`); "nova fatia: cenário novo exige PRD alterado antes" (fatiar:100); retorno do P.O. na review que pede cenário novo (plan:110-111).
- **Pré-condições / arquivos lidos:** `prd.md` aprovado/fatiado, `decisoes.md`, `elm/` (com `resource`/`id` se já publicado), `backlog.md` (fatias que cobrem o que muda).
- **Processamento interno:**
  1. Incrementar a versão: `1.1` correção, `2.0` mudança de escopo; registrar no rodapé.
  2. Voltar a `em-revisao` **só o que mudou**; repetir revisão (S08-F1 Passo 4) e **GATE** (S08-F2).
  3. Conceito alterado: `status: draft`, `generated.at` novo; no GATE, **acrescentar** novo `verified` à lista (okf:69-70). Artefato novo passa pelos *similares* (prd:71-72).
  4. A `sdd-elm` atualiza os mesmos artefatos (pelo `resource`/`id`); conflito com mudança feita no ELM → a pessoa decide (okf:143).
  5. Fatias já entregues que dependem do que mudou → **avisar e propor fatias novas**; **não alterar fatia concluída** (prd:133-134).
- **Resultado final (output):**
  - Resposta: nova versão do PRD aprovada, lista de conceitos alterados, aviso das fatias afetadas.
  - Arquivos: `prd.md` (versão, rodapé), `elm/*.md` (draft→stable, `verified` acumulado), `log.md` (`**Update**`), commit na base.
  - ELM: republicação via S11-F2 (atualiza mesmos ids).
  - Handoff: `sdd-elm` requisitos; `sdd-fatiar` para fatias novas (refinamento).
- **Lacunas observadas:**
  - **Efeito no backlog não é dito:** backlog.md:75 manda fatia `pronta` voltar a `backlog` quando "PRD reaberto/decisão nova em aberto", mas prd:128-134 não manda ninguém conferir a DoR das fatias `pronta`/em sprint; nem diz o que acontece com fatia **em andamento** (status.md em branch) quando o cenário dela muda.
  - **Status de retorno:** não diz se o PRD volta a `aprovado` ou `fatiado` depois do novo GATE (fatiar:16 exige `aprovado` como entrada; backlog.md:75 aceita `fatiado`).
  - **Critérios de aceite nos IBs:** elm:142-143 diz atualizar o campo "gerado do PRD" quando a fatia for refinada, mas nada no fluxo de mudança do PRD dispara isso.
  - Mudança de PRD `concluido` não é tratada (prd:130 cita só `aprovado`/`fatiado`).
  - Fatia sem épico (ficha): drift de negócio vai para a ficha pela `sdd-triar` (consolidar:35); a F3 do PRD não cobre, o que é coerente, mas não há ponteiro de volta em prd:128-134.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S08-F1 · Produzir o PRD do épico (entender → entrevistar → similares → escrever → revisão)
1. INPUT EXATO: "escreve o PRD do EP-03"
   ESTADO: P. backlog.md: EP-03 status `rascunho`, prd `—`, elm `—`. Pasta epicos/EP-03-*/ inexistente. Bundle do ELM existe (sincronismo 2026-10-10). MCP elm: sim.
2. REGRA APLICADA:
   - SE a frase casa com a description → ativa a skill — fonte: prd:3
   - SE falta a descrição longa → pedir à pessoa (quem pediu, problema, exemplos, prazos) — fonte: prd:31
   - SE é preciso entender antes de perguntar → explorar bundle, código, glossário/ADRs (delegado: sdd-pesquisador, senão você, só leitura) — fonte: prd:34-39
   - SE EP-03 tem registro `rascunho` com prd `—` → id = EP-03, pasta epicos/EP-03-<slug kebab>/ — fonte: prd:40-41
   - SE projeto com ELM e coluna elm = `—` → sdd-elm modo backlog, só o épico, com confirmação; id vai para a coluna elm — fonte: prd:43-45 (regra de escrita: elm:27-30)
   - ENTÃO a etapa seguinte é a entrevista (sdd-entrevistar, delegado; grava decisoes.md) — fonte: prd:50-51
   - AMBÍGUO: prd:43-46 manda confirmar o épico no EWM "com confirmação", e prd:50 manda entrevistar. O texto não diz se a entrevista espera o "sim" da prévia (elm:27-30 só proíbe a escrita) ou se segue com elm pendente.
   - ENTÃO 3.1 similares (obrigatório): listar artefatos propostos → sdd-elm modo similares → uma decisão por acerto — fonte: prd:55-72
   - ENTÃO 3.2 escrever prd.md (prd-tpl) e elm/ (okf), index.md e log.md — fonte: prd:74-98
   - SE mais de ~8 histórias ou mais de um objetivo → propor dividir em dois épicos antes de escrever — fonte: prd:98
   - ENTÃO 4 revisão independente (rubrica P, até 2 rodadas); status em-revisao — fonte: prd:100-105; rubricas:10-26
3. OUTPUT GERADO: resposta com a prévia do épico ("Ação | Alvo | Título | Tipo/Pasta": criar `[EP-03] <título>`, tipo do steering) e, na sequência, as perguntas da entrevista. Tabela de similares com decisão por artefato. Resultado final: PRD pronto para o GATE.
   ARQUIVOS ESCRITOS (ao fim da F1): epicos/EP-03-<slug>/prd.md (prd-tpl) · decisoes.md · elm/HF-*.md, REG-*.md, GL-*.md (okf) · elm/index.md · elm/log.md · backlog.md (prd = link; elm = id só após "sim").
   ESCRITA NO ELM: pendente (criação do épico aguarda "sim"); similares são só leitura.
4. VEREDITO MECÂNICO: AMBÍGUO (prd:43-46 × prd:50 — não diz se a entrevista espera a confirmação da escrita no EWM). Subnota: prd:42 manda gravar prd = link do prd.md na linha do épico antes de o prd.md existir (prd:42 × prd:32 — ordem não dita).
```

```text
S08-F2 · GATE do PRD (aprovação pelo P.O.)
1. INPUT EXATO: "aprova o PRD do EP-03"
   ESTADO: prd.md `em-revisao`. Rubrica P rodada 1 = PRONTO (rubricas:26). decisoes.md com 0 "em aberto". elm/: HF-01, REG-01, GL-tentativa-de-login com `status: draft`, `generated.at` 2026-10-14, sem `verified`. Publicação `na-aprovacao`. Commit direto na base.
2. REGRA APLICADA:
   - SE "aprova o PRD" → entra no GATE — fonte: prd:3, prd:44
   - ENTÃO mostrar o card e perguntar "Aprovar?" — fonte: prd:109-115 (template literal)
   - SE há decisão em aberto que muda comportamento → não há aprovação — fonte: prd:117 (não se aplica: 0 em aberto)
   - ENTÃO prd.md: `status: aprovado`, versão 1.0, data e quem aprovou no rodapé — fonte: prd:118
   - ENTÃO em cada conceito de elm/: `status: stable` e `verified: { by: human:<login de quem aprovou>, at: <agora> }` — fonte: prd:118-119; okf:61
   - AMBÍGUO: a origem do login de `verified.by`. prd:119 diz "login de quem aprovou" (o P.O. ou quem ele delegou, prd:114); okf:61 diz "login do P.O."; prd-tpl:5 tem o campo `po`. Não há passo que diga como obter o login.
   - ENTÃO entrada **Update** no log.md; commit de prd, decisoes, elm e backlog na base — fonte: prd:120-122; steering:61
   - ENTÃO status do épico em backlog.md = `aprovado` (derivado: backlog.md:43 define o status do épico igual ao do PRD e backlog.md:62 põe o "status do PRD" na sdd-prd); prd:121 não diz qual campo muda
   - SE publicação = na-aprovacao → próximos passos na mesma resposta: (1) sdd-elm modo requisitos; (2) sdd-fatiar — fonte: prd:123-126
3. OUTPUT GERADO: card literal (prd:110-115):
   📄 PRD EP-03 — <título>
   Histórias: n (c cenários) · Regras: n · Termos novos: n · No ELM: reusa … · altera … · novos verificados n
   Decisões: d decididas · 0 em aberto (—)
   Revisão: OK na rodada 1
   Aprovar? (o P.O. ou quem ele delegou)
   Após "sim": confirmação da aprovação + os dois próximos passos.
   ARQUIVOS ESCRITOS: prd.md (aprovado, 1.0) · elm/*.md (stable + verified) · elm/log.md (Update) · backlog.md (status do épico) · commit na base. Mensagem do commit: o padrão do steering é `FT-<nnn> …`, sem FT para um épico; não há regra para essa mensagem (SEM REGRA, sub-item).
   ESCRITA NO ELM: nenhuma nesta etapa; a publicação (requisitos) vem como próximo passo e exige "sim".
4. VEREDITO MECÂNICO: AMBÍGUO (origem do login de `verified.by`: prd:119 "quem aprovou" × okf:61 "login do P.O." × prd-tpl:5 `po`). Subnotas: mensagem de commit sem FT (steering:59); quem é o aprovador quando não é o P.O. (prd:114) não tem verificação.
```

```text
S08-F3 · Mudança depois de aprovado (PRD aprovado/fatiado)
1. INPUT EXATO: "muda o PRD do EP-03: o limite de tentativas passa de 3 para 5"
   ESTADO: prd.md `aprovado` 1.0. HF-01 e REG-01 publicados (resource e id no elm/). backlog.md: FT-031 `pronta` (cobre REG-01), não concluída, sem status.md.
2. REGRA APLICADA:
   - SE "pedido explícito" de mudança num PRD aprovado/fatiado → entra no fluxo — fonte: prd:130
   - ENTÃO incrementar versão: 1.1 para correção, 2.0 para mudança de escopo — fonte: prd:130, prd:68
   - AMBÍGUO: "3 para 5" é correção (1.1) ou mudança de escopo (2.0)? Nenhuma regra dá o critério. Fonte: prd:130.
   - ENTÃO voltar a em-revisao só o que mudou — fonte: prd:131. `em-revisao` é status do PRD (prd-tpl:4); conceitos têm draft/stable/deprecated (okf:62). Não se sabe se o "o que mudou" é o PRD, o conceito ou ambos.
   - ENTÃO repetir revisão (S08-F1 passo 4) e GATE (S08-F2) — fonte: prd:131-132
   - ENTÃO conceito alterado: copiar do bundle (prd:85-89), `status: draft`, `generated.at` novo — fonte: prd:132; okf:69
   - ENTÃO sdd-elm atualiza os mesmos ids (resource/id) — fonte: prd:132-133
   - SE fatia `pronta` depende do cenário alterado → backlog.md:75 manda voltar a `backlog` quando o "PRD reaberto" — fonte: backlog.md:75 (prd:133-134 só fala de fatia concluída). Não se sabe se esta mudança é "reabrir".
   - SEM REGRA (sub): status do PRD depois do novo GATE — `aprovado` ou `fatiado`? (fatiar:16 pede aprovado; backlog.md:75 fala em fatiado).
3. OUTPUT GERADO: nova versão (1.1 ou 2.0), lista de conceitos alterados e aviso das fatias afetadas (prd:133-134). Sem template literal.
   ARQUIVOS ESCRITOS: prd.md (versão, rodapé) · elm/*.md (draft; verified acumulado no próximo GATE) · elm/log.md (Update) · commit na base · backlog.md (FT-031 volta a backlog? — depende da AMBÍGUO acima).
   ESCRITA NO ELM: republicação via S11-F2 depois do novo GATE.
4. VEREDITO MECÂNICO: AMBÍGUO (prd:130 não define o critério entre correção 1.1 e escopo 2.0; prd:131 "em-revisao só o que mudou" não diz a que se aplica). Subnota: status de retorno depois do GATE sem regra.
```

```text
S08-X1 · Negativo: pedido de PRD para algo sem EP registrado
1. INPUT EXATO: "escreve o PRD da cobrança de juros"
   ESTADO: backlog.md sem nenhum EP-nn sobre juros. Sem pasta em epicos/.
2. REGRA APLICADA:
   - SE a frase casa com a description → skill — fonte: prd:3
   - SE não há registro EP-nn (rascunho, prd `—`) → a demanda não passou pela triagem → carregar sdd-triar antes — fonte: prd:40-41
   - ENTÃO a triagem decide épico ou padrão (triar:53-56); se padrão, a fatia não passa pela sdd-prd — fonte: prd:24-25
3. OUTPUT GERADO: desvio para sdd-triar. Nenhum arquivo do PRD é criado.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: DETERMINÍSTICO (desvio para a triagem; a decisão épico × padrão cabe à triagem).
```

```text
S08-X2 · Negativo: mudança em PRD `concluido`
1. INPUT EXATO: "muda o PRD do EP-01: o prazo de bloqueio passa a 60 minutos"
   ESTADO: prd.md EP-01 `concluido` (todas as fatias concluídas). HF e REG publicados.
2. REGRA APLICADA:
   - SE "pedido explícito" de mudança num PRD aprovado/fatiado → fluxo de mudança — fonte: prd:130
   - SE o status é `concluido` → não está na lista de prd:130 (só aprovado/fatiado); `concluido` existe em prd-tpl:4 e backlog.md:43 sem tratamento de mudança
3. OUTPUT GERADO: nenhum definido.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: SEM REGRA (prd:130 cita só aprovado/fatiado; `concluido` não tem tratamento).
```

```text
S08-X3 · Negativo: "não" na pergunta de aprovação sem decisão em aberto
1. INPUT EXATO: "não, não aprovo ainda"  (resposta a "Aprovar?")
   ESTADO: prd.md `em-revisao`. Rubrica P PRONTO. decisoes.md com 0 "em aberto".
2. REGRA APLICADA:
   - SE a resposta ao GATE é negativa → prd:117 trata só o caso "decisão em aberto que muda comportamento" (volta à entrevista) — não se aplica, pois não há decisão em aberto
   - Nenhuma outra regra trata recusa do P.O. sem motivo escrito (fonte: prd:107-126)
3. OUTPUT GERADO: nenhum definido.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: SEM REGRA (não há tratamento de "não" sem decisão em aberto: o status fica em-revisao? volta a rascunho? abre-se uma pergunta? — nada escrito).
```

#### Tabela-resumo · S08

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S08-F1 · Produzir PRD | AMBÍGUO | prd:43-46 × prd:50: confirmação do épico no EWM não diz se a entrevista espera o "sim" |
| S08-F2 · GATE do PRD | AMBÍGUO | origem do login em `verified.by`: prd:119 × okf:61 × prd-tpl:5 |
| S08-F3 · Mudança depois de aprovado | AMBÍGUO | correção (1.1) × escopo (2.0) sem critério; "em-revisao só o que mudou" |
| S08-X1 · PRD sem EP registrado | DETERMINÍSTICO | desvio para sdd-triar (prd:40-41) |
| S08-X2 · Mudança em PRD `concluido` | SEM REGRA | prd:130 só cobre aprovado/fatiado |
| S08-X3 · "Não" no GATE sem decisão em aberto | SEM REGRA | prd:117 só cobre decisão em aberto |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| S08-F1 | `<produto>/epicos/<EP>-<slug>/prd.md` (prd:16, 41) | Sim, mas a P3 omitiu `<produto>`. Slug kebab sem acento (prd:41). Escrito onde o HEAD estiver: nenhum passo manda estar na base antes de escrever | `.md`, frontmatter YAML + corpo (prd-tpl:1-80) | Parcial. Campos `po` e `demanda` sem fonte prescrita (prd-tpl:5-6; `demanda` duplica a coluna `elm` do backlog); `atualizado` sem regra de atualização; rodapé só tem "Versão · data" (prd-tpl:80) e prd:118 pede "quem aprovou" no rodapé (sem campo) | Escreve: `sdd-prd`/`sdd-produto`. **Commit só no GATE** (prd:120-122): durante rascunho/revisão (dias) fica não commitado, na branch corrente. Sem regra de commit de WIP. Push: "sim", pela pessoa | I-git (pior aqui: a P3 não viu que `sdd-prd` nunca manda ir para a base, ao contrário de `sdd-triar`). Árvore suja de PRD em andamento faz `sdd-triar`/`consolidar`/`iniciar` pararem. I-perm: permitido | NÃO ESPECIFICADO (branch de trabalho do rascunho e commit de WIP; fonte de `po`/`demanda`; slot do aprovador). Confirma a P3 (ordem prd:42 × prd:32) e acrescenta a branch |
| S08-F1 | `<produto>/epicos/<EP>-<slug>/decisoes.md` (prd:50, entrev:18) | Sim. Quem grava é `sdd-entrevistar` (delegado), não `sdd-prd`; `ag-prod` tem a skill (ag-prod:16) | `.md`, tabela `D \| Pergunta \| Decisão \| Fonte \| Data \| Situação` (entrev:67-76) | Sim para a estrutura. prd:68 exige registrar ali a decisão por artefato (`D-nn`: artefato, id ELM, relação, decisão, motivo) — não cabe nas 6 colunas de entrev:70 (a skill não diz onde vão "id ELM" e "relação") | Mesmo regime do `prd.md` (sem commit até o GATE). Entrevista roda **antes** do `prd.md` existir, então é o 1º arquivo não commitado | I-git. I-perm: permitido (`{{PRODUTO}}/**`) | DIVERGENTE leve (colunas do `decisoes.md` não comportam o registro do prd:68) |
| S08-F1 | `<produto>/epicos/<EP>-<slug>/elm/HF-nn-<slug>.md`, `REG-nn-<slug>.md`, `GL-<termo-kebab>.md` (prd:76-77, okf:12, 29) | Sim (P3 igual). Ao **alterar**, prd:85-86 manda copiar o arquivo do bundle (`<id>-<slug>.md`) "para `elm/`" sem dizer se renomeia para `HF-nn-<slug>.md` (okf:29) — Concept ID "não muda" (okf:27) | `.md` com frontmatter YAML OKF v0.2 | Validado com PyYAML (mesmo frontmatter de okf:34-50): faz parse e `generated.at` vira datetime. **Quebra** se `title`/`description` tiver `: ` (ex. `HF - Bloqueio: conta…` → "mapping values are not allowed here"); okf não manda aspas e a P11 só detecta depois. Campos obrigatórios `type`, `status: draft`, `sources`, `generated` conferem. `generated.by` de exemplo é `sdd/2.1.0` (okf:48) mas o power é 2.3.0 | Escreve `sdd-prd`; sem commit até o GATE. Reutilizar → nenhum arquivo (prd:90-91) | I-git; I-perm: permitido. `elm/` inexistente: criação implícita | DIVERGENTE (frontmatter sem regra de aspas; nome do arquivo na Alteração sem regra) |
| S08-F1 | `elm/index.md` (okf:18, 148-160) | Sim | `.md`, frontmatter `okf_version: "0.2"` + `# Histórias/# Regras/# Termos` com `* [título](arquivo) - descrição` | Confere com okf:148-160. prd:78 só diz "mais o `index.md`": a regra de conteúdo está em okf, não em prd | Mesmo regime | I-git; I-perm | OK |
| S08-F1 | `elm/log.md` (okf:19, 162-163) | Sim | `.md`: `# Directory Update Log`, `## AAAA-MM-DD`, `* **Creation**: …` | Confere (P3 acertou "Creation"). Mais nova primeiro | Mesmo regime | I-git; I-perm | OK |
| S08-F1 | `<produto>/backlog.md` — coluna `prd` (link) e `elm` do épico (prd:42-44) | Sim. Link relativo ao `backlog.md`: `[prd](epicos/EP-03-<slug>/prd.md)` (backlog.md:23). prd:42 grava o link antes de o arquivo existir | `.md`, tabela `## Épicos` (backlog.md:21-23) | Confere. `status` do épico `rascunho→em-revisao` (prd:105): regra só indireta (backlog.md:43 "o mesmo do PRD", :62 "status do PRD = sdd-prd"); prd não manda atualizar | Escreve `sdd-prd`; `elm` do épico pelo `sdd-elm`. Commit: só no GATE (prd:121). Nesse intervalo `backlog.md` fica modificado no working tree **da branch corrente** (backlog.md:6-7 proíbe branch de fatia) | I-git. A P3 ("elm = id só após sim") confere (elm:29-30) | NÃO ESPECIFICADO (quando o `status` do épico muda e em que commit). Confirma P2 |
| S08-F2 | `prd.md` → `status: aprovado`, versão `1.0`, data e aprovador no rodapé (prd:118) | Sim | `.md` | Divergente do template: rodapé tem `Versão <x.y> · <data>` e nenhum campo de aprovador (prd-tpl:80). `status` `aprovado` está no fluxo do frontmatter (prd-tpl:4) | Commit **na base**, "direto ou PR curto" (prd:120-122). Padrão da setup = PR curto (setup:115): **nenhuma skill nomeia a branch do PR curto** nem diz que o commit anterior (WIP) vai junto. Mensagem: padrão `FT-<nnn> …` (steering:59) sem FT para épico — SEM REGRA. Push/PR: só "sim"; agente entrega o comando (steering:61) | I-git. Com HEAD em branch de fatia, prd:122 diz só "nunca numa branch de fatia" e não diz como mover o conteúdo | DIVERGENTE (rodapé × template) + NÃO ESPECIFICADO (branch do PR curto, mensagem) |
| S08-F2 | `elm/*.md` — `status: stable` + `verified: { by: human:<login>, at: <agora> }` (prd:118-119; okf:61) | Sim | YAML. Validado: `verified` em objeto faz parse (`by: human:ana.souza` sem aspas OK em PyYAML) | **Tipo inconsistente:** prd:119/okf:61 mostram objeto único; prd:132 e okf:70 falam em "acrescentar à lista"/"a lista `verified` acumula". O 1º GATE não diz se grava lista de 1 item ou objeto; o 2º GATE exige conversão. `at: <agora>`: fuso/formato não dito (okf:48 usa `Z`). Origem do login: prd:119 "quem aprovou" × okf:61 "login do P.O." × prd-tpl:5 `po` (confirma P3) | Mesmo commit do GATE. Comparação `verified.at > generated.at` funciona com timestamps (testado) | I-git; I-perm | DIVERGENTE (objeto × lista; login) — confirma P3 e acrescenta o tipo |
| S08-F2 | `elm/log.md` — `**Update**` (prd:120) | Sim | `.md` | Confere (okf:162-163) | Mesmo commit | I-git | OK |
| S08-F2 | `<produto>/backlog.md` — `status` do épico `aprovado` (prd:121 só cita o arquivo no commit) | Sim | tabela de épicos | `aprovado` é valor válido (backlog.md:43). P3 derivou corretamente de backlog.md:43+:62, mas prd:121 não diz o campo | Mesmo commit | I-git | NÃO ESPECIFICADO (derivável; confirma P3) |
| S08-F3 | `prd.md` (versão `1.1`/`2.0`, rodapé) · `elm/*.md` (`draft`, `generated.at` novo; `verified` acumulado no GATE) · `elm/log.md` (`**Update**`) · `backlog.md` | Sim (prd:130-133) | idem F1/F2 | `verified` "acrescentado à lista" confirma o achado de tipo. Rodapé "registre no rodapé": formato do histórico de versões não existe no template (só 1 linha) | Commit na base como F2 (o texto da mudança não repete a regra; vale prd:120-122 por analogia — não escrito). `backlog.md`: fatia `pronta` que depende do cenário → backlog.md:75 manda voltar a `backlog`, prd:133-134 só trata fatia concluída | I-git. Conceito já publicado: `resource`/`id` mantidos (prd:132) | NÃO ESPECIFICADO (commit/branch da mudança; histórico de versões no rodapé). Confirma P3 (1.1×2.0) |
| S08-X1..X3 | — | — | — | — | — | — | sem escrita: S08-X1 (desvio para `sdd-triar`), S08-X2 (PRD `concluido`: SEM REGRA, nada gravado), S08-X3 ("não" no GATE: SEM REGRA, o `status` fica `em-revisao` por omissão) |

---


## S09 · sdd-fatiar

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S09-F1 · Fatiar um PRD aprovado (rascunho → pergunta → GATE do backlog → gravar → próximos passos)
- **Gatilho inicial:** frases da description (fatiar:3): "fatiar o PRD", "quebrar em histórias", "gerar o backlog", "criar os itens de backlog", "PRD para issues". Evento: handoff da `sdd-prd` após o GATE (prd:126).
- **Pré-condições / arquivos lidos:** PRD `aprovado` em `<produto>/epicos/<EP>-<slug>/prd.md` (fatiar:16) + `decisoes.md` (fatiar:44); `backlog.md` na base (`git switch <base>` + `git pull --ff-only`, backlog.md:82); código dos módulos tocados (subagente `sdd-pesquisador`, se houver); DoR em backlog.md:70-75; linha "Backlog no EWM" do `sdd.md` (steering:72).
- **Processamento interno:**
  1. **Passo 1** — ler PRD e `decisoes.md`; reler código das fatias que mexem em módulos existentes (a fatia tem de ser possível no código real); montar tabela `FT | Título | Cobre | Bloqueada por | Tam. | Modo`; conferir **cobertura** (todo cenário em exatamente uma fatia — compartilhado vai para a primeira que o entrega); cenário sem fatia ou fatia sem cenário → corrigir **antes** de mostrar. Critérios de "boa fatia": vertical (tracer bullet; a 1ª é a mais fina), verificável sozinha, cabe numa janela de contexto, tamanho ≤ G, não fina demais ("o que dá para demonstrar?"), critério falsificável (cada cenário falha hoje na base — dizer a observação), prefactoring, independente quando der, AFK/HITL (tipo de trabalho novo começa HITL).
  2. **Passo 2** — card "🍰 EP-nn — n fatias · AFK/HITL · tamanhos" + tabela + cobertura + 3 perguntas (granularidade, dependências, AFK×HITL invertido); ajustar e repetir até "ok". **O "ok" é o GATE do backlog** (P.O. ou time).
  3. **Passo 3** — gravar na base: `backlog.md` (épico `status: fatiado`; uma linha por fatia com prioridade pela ordem da tabela respeitando dependências, `elm` `—`, `status` `pronta` se passa na DoR, senão `backlog` com `falta:` em `obs`; ids `FT-nnn` sequenciais, nunca reaproveitados); `prd.md` → `status: fatiado`; commit (padrão do `sdd.md`) de `backlog.md` + `prd.md`; push/PR curto só com "sim" (backlog.md:83).
  4. **Passo 3.4 (com ELM)** — o GATE conclui a `[ESP]`: perguntar as horas de quem especificou (descontando o já lançado) → `sdd-elm` modo *horas* (lançar) e modo *conclusão* na `[ESP] EP-nn`, com confirmação. Especificação que continua (refinamento na próxima sprint) → **não** conclui. Sem MCP → `ELM pendente: lançar <h>h em [ESP] EP-nn` no rodapé do PRD.
  5. **Passo 4** — próximos passos na mesma resposta: (com ELM) `sdd-elm` modo *backlog* (S11-F4: épico se faltar + um IB por fatia, ligados às histórias "implementa" e ao épico, com critérios de aceite; `Planejado para` = iteração indicada); `sdd-planejamento` (encaixar na sprint ou Kanban); "vamos trabalhar na FT-031" (`sdd-iniciar`).
- **Resultado final (output):**
  - Resposta: card do passo 2 até o "ok"; depois lista dos próximos passos.
  - Arquivos: `<produto>/backlog.md` (épico `fatiado`; linhas das fatias na seção `## Fatias — <EP> <título>`), `prd.md` (`status: fatiado`; rodapé com `ELM pendente` se for o caso); commit na base.
  - ELM: horas e conclusão da `[ESP]` (com confirmação); IBs via S11-F4.
  - Handoff: `sdd-elm` backlog → `sdd-planejamento` → `sdd-iniciar`.
- **Lacunas observadas:**
  - **Notação de `cobre` diverge:** fatiar:51 usa `HF-01 · 1.1, 1.2 · REG-01`; backlog.md:29 e :47 usam `HF-01#1.1, HF-01#1.2, REG-01`. A conversão fica implícita.
  - **"IB por fatia" incondicional vs condicional:** fatiar:87-89 manda criar o IB de cada fatia depois do GATE; elm:135-136 só o faz se `backlog no EWM` = `ao-fatiar` (se `na-sprint`, é o planejamento que cria, elm:160; o padrão da setup é `na-sprint`, sdd-setup/SKILL:138). A skill não lê nem cita a linha do `sdd.md`.
  - **Link "implementa" × publicação `no-merge`:** o passo 4 manda ligar o IB às histórias do DOORS Next (fatiar:87-88), mas com publicação `no-merge` (steering:72) as HF não têm id no ELM no momento do fatiamento; nem fatiar nem elm:144-145 dizem adiar o link nem como retomá-lo.
  - **`[ESP]` pode não existir:** fatiar:80-83 pressupõe `[ESP] EP-nn` já criada pelo planejamento (elm:167); se o épico foi especificado fora de sprint, modo *horas* (elm:190-191: "a `[ESP]` vem do `sprint-<nn>.md`; dúvida → pergunte") não tem saída definida. Além disso, o modo *conclusão* (elm:220-221) só lista tarefas e IB da **fatia** e o épico — não a `[ESP]`; e a coluna "Situação" da seção Especificação do `sprint-<nn>.md` (arquivos:122,156: `concluida`) não tem quem a atualize no GATE.
  - **DoR em duas versões:** `acordos.md` (arquivos:73-78) tem "cabe em uma janela de contexto" e "dependências concluídas ou na **mesma sprint**"; backlog.md:70-75 (usada por fatiar:76-77) não tem o primeiro e diz "concluídas ou planejadas antes", que no momento do fatiar (sem sprint) não é verificável.
  - **Sem guarda de entrada:** fatiar:16 diz "Entrada: PRD `aprovado`", mas não manda recusar PRD `rascunho`/`em-revisao`, nem diz como tratar `fatiado` (re-fatiar = refinamento).
  - `Próximos ids` (backlog.md:16,79): fatiar:76-77 não diz para incrementar; só "só cresce".
  - A skill não manda ler `.kiro/steering/sdd.md` (prd:27 manda); precisa dele para padrão de commit, "Backlog no EWM" e "Fatia dividida no EWM".

#### S09-F2 · Refinamento — dividir fatia
- **Gatilho inicial:** "refinar o backlog", "a FT-033 está grande demais" (fatiar:95, description fatiar:3). Evento: `sdd-planejamento` "Fatia que cresceu (passou de `G` no plano) → volte para a `sdd-fatiar` (dividir)" (plan:89); `sdd-plano`/revisão idem (implícito).
- **Pré-condições / arquivos lidos:** `backlog.md` (base), PRD do épico, a fatia (e sua pasta `.kiro/specs/<ft>-<slug>/` se já iniciada), `sdd.md` ("Fatia dividida no EWM", steering:74).
- **Processamento interno:**
  1. Original → `status: dividida`, `obs`/`substituida-por: [FT-x, FT-y]`.
  2. Novas fatias herdam a cobertura (**repartida**, mantendo a regra "cada cenário em exatamente uma fatia", fatiar:56-57), as dependências e o épico; ids novos (nunca reaproveitados).
  3. No EWM, `sdd-elm` (modo *backlog*, item 4: elm:146-147) aplica a linha "Fatia dividida no EWM": novos IBs filhos do IB original (que segue filho do épico) **ou** fecha o original e cria novos.
  4. Conferir a DoR das fatias novas (S09-F5).
- **Resultado final (output):** `backlog.md` com a fatia original `dividida` e as novas linhas; commit na base; no EWM, IBs novos (com confirmação, S11-F4); resposta com a nova tabela.
- **Lacunas observadas:**
  - **Fatia já em andamento** (que é o gatilho real de plan:89 — "passou de G no plano"): a skill só protege fatia `concluida` (fatiar:108); não diz o que fazer com `status.md`, branch, `.kiro/specs/<ft>-<slug>/`, plano aprovado, tarefas `[DEV]/[REV]/[VER]` já criadas no EWM e `sprint`/`responsavel` da original (elm:146-147 só trata IBs, não as tarefas).
  - **Fatia sem épico:** "herdam a cobertura" (fatiar:97) pressupõe `cobre` e PRD; fatia sem épico tem ficha com cenários `C<n>` e nenhum `cobre` (backlog.md:47), e `sdd-fatiar` só é acionada para PRD (fatiar:16). Quem divide uma padrão sem épico (e reparte a ficha aprovada pelo P.O.) não está definido.
  - Não diz se o refinamento exige novo "ok"/GATE do backlog (o passo 2 é descrito só para o fatiamento inicial).
  - `sprint`/`responsavel` das novas fatias não é dito (herdar? voltar a `—`?).

#### S09-F3 · Refinamento — juntar fatias
- **Gatilho inicial:** "refinar o backlog" com pedido de juntar (fatiar:99); fatias finas demais ("doze fatias para uma mudança de três linhas", fatiar:27-28).
- **Pré-condições:** só fatias ainda em `backlog` (fatiar:99); `backlog.md`.
- **Processamento interno:** juntar as fatias; "a que some" fica `status: cancelada` com `motivo`; unir cobertura e dependências na que fica; conferir DoR.
- **Resultado final (output):** `backlog.md` atualizado (uma `cancelada` com motivo em `obs`, backlog.md:48); commit na base.
- **Lacunas observadas:**
  - Não diz qual fatia fica nem como ficam `cobre`, `bloqueada-por`, tamanho e modo da resultante (maior tamanho? tamanho > G → "divida"?).
  - EWM: nenhuma regra para o IB da fatia cancelada; elm:46 proíbe apagar e manda "roteiro manual", mas não há modo/roteiro para cancelamento por junção.
  - "só fatias ainda em `backlog`" exclui `pronta` — mas fatia `pronta` e na sprint é o caso comum; não diz o que fazer.
  - Sem "ok" explícito.

#### S09-F4 · Refinamento — fatia nova (faltou uma fatia)
- **Gatilho inicial:** "faltou uma fatia" (fatiar:95).
- **Pré-condições:** PRD aprovado/fatiado cobrindo o cenário.
- **Processamento interno:** "cenário novo exige PRD alterado antes" → `sdd-prd` (S08-F3, mudança depois de aprovado); só depois criar a fatia.
- **Resultado final (output):** nova linha em `backlog.md` (ou desvio para `sdd-prd`).
- **Lacunas observadas:**
  - Duas situações misturadas: (a) cenário já existe no PRD mas ficou sem fatia (não exige PRD novo; é correção de cobertura) e (b) cenário novo. A skill só descreve (b).
  - Depois do novo GATE do PRD, não há passo de retorno ("agora fatie o cenário novo") nem em prd:128-134 nem aqui.
  - Fatia nova que nasce de pedido sem relação com PRD → `sdd-triar` (não citada).

#### S09-F5 · Refinamento — reconferir a Definition of Ready
- **Gatilho inicial:** a cada refinamento (fatiar:101-102); também chamada de fato no planejamento (plan:61-62, backlog.md:63-64).
- **Pré-condições:** `backlog.md`; DoR em backlog.md:70-75; PRD aprovado/fatiado; decisões `em aberto`.
- **Processamento interno:** conferir as fatias `backlog`, gravar `pronta` nas que passam, e **voltar a `backlog`** as que deixaram de passar (com `falta:` em `obs`).
- **Resultado final (output):** `backlog.md` (`status`/`obs`), commit na base.
- **Lacunas observadas:**
  - Mesma divergência de DoR: backlog.md:70-75 × arquivos:73-78 (ver S09-F1). O planejamento (plan:61) reconfere "a Definition of Ready" sem dizer qual das duas.
  - Fatia `pronta` em andamento (status.md em branch) que deixa de passar: a regra de "volta a `backlog`" (backlog.md:75) conflita com "em andamento não é gravado" (backlog.md:51).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S09-F1 · Fatiar um PRD aprovado (rascunho → card → GATE do backlog → gravar → próximos passos)
1. INPUT EXATO: "fatiar o PRD do EP-03"
   ESTADO: prd.md aprovado (1.0). decisoes.md sem "em aberto". backlog.md com EP-03 `aprovado`, sem fatias, base atualizada. EP-03 elm 612001. Backlog no EWM `ao-fatiar`. Tarefa [ESP] EP-03 existe na sprint 3 (rita.melo, 16 h previstas, 0 h lançadas). MCP sim.
2. REGRA APLICADA:
   - SE "fatiar o PRD" → ativa a skill — fonte: fatiar:3
   - SE PRD `aprovado` → entrada válida — fonte: fatiar:16
   - ENTÃO ler PRD e decisoes.md; reler código dos módulos tocados (delegado: sdd-pesquisador) — fonte: fatiar:44-45
   - ENTÃO montar tabela FT | Título | Cobre | Bloqueada por | Tam. | Modo; cobertura: cada cenário em exatamente uma fatia; cenário sem fatia → corrigir antes de mostrar — fonte: fatiar:46-57
   - ENTÃO aplicar critérios de boa fatia (vertical, falsificável, AFK/HITL…) — fonte: fatiar:19-40
   - ENTÃO card + 3 perguntas; ajustar até "ok"; o "ok" é o GATE do backlog — fonte: fatiar:61-70
   - ENTÃO gravar na base (git switch base + pull --ff-only) — fonte: backlog.md:82
     - épico `fatiado`; uma linha por fatia; elm `—`; status `pronta` se passa na DoR (backlog.md:70-75), senão `backlog` com `falta:` — fonte: fatiar:74-77
     - ids FT-nnn sequenciais — fonte: fatiar:77; backlog.md:79
     - nota (sem regra): quem incrementa "Próximos ids" (backlog.md:16) não está em fatiar:74-77
   - ENTÃO prd.md `status: fatiado` — fonte: fatiar:78
   - ENTÃO commit (padrão do steering) de backlog.md e prd.md; push/PR só com "sim" — fonte: fatiar:79; backlog.md:83; steering:59, :61
   - SE com ELM → perguntar as horas de quem especificou (descontando o já lançado); chamar sdd-elm modo horas (lançar) — fonte: fatiar:80-83; elm:188-192
   - SE a especificação está concluída → chamar modo conclusão na [ESP] EP-03 — fonte: fatiar:81
   - CONFLITO: elm:220-221 define o modo conclusão como "tarefas e IB da fatia" e "épico"; a [ESP] não está nessa lista. fatiar:81 manda usar o modo para a [ESP].
   - ENTÃO próximos passos: sdd-elm modo backlog (S11-F4); sdd-planejamento; sdd-iniciar — fonte: fatiar:85-91
3. OUTPUT GERADO: card literal (fatiar:62-65):
   🍰 EP-03 — 4 fatias · 2 AFK · 2 HITL · tamanhos M/P
   [tabela FT-031…FT-034]
   Cobertura: n/n cenários · Primeira fatia (tracer bullet): FT-031
   - A granularidade está boa? - As dependências estão certas? - Alguma fatia deveria ser HITL/AFK ao contrário?
   Após "ok": confirmação da gravação; pergunta de horas da [ESP]; próximos passos.
   ARQUIVOS ESCRITOS: backlog.md (épico `fatiado`; linhas FT-031…FT-034 em "## Fatias — EP-03") · prd.md (`fatiado`) · commit na base.
   ESCRITA NO ELM: horas e conclusão da [ESP] (após "sim"); IBs via S11-F4 (após "sim").
4. VEREDITO MECÂNICO: CONFLITO (fatiar:81 manda concluir a [ESP] pelo modo conclusão; elm:220-221 restringe o modo a tarefas e IB da fatia e ao épico). Subnotas: DoR usada é a de backlog.md:70-75 (é a que fatiar cita; a de arquivos:73-78 é outra, ver S10-F2).
```

```text
S09-F2 · Refinamento — dividir fatia
1. INPUT EXATO: "refinar o backlog: a FT-033 está grande demais, divide em duas"
   ESTADO: FT-033 `backlog` (sem status.md, sem branch), cobre HF-02#2.1, HF-02#2.2, HF-02#2.3; sprint `—`; elm [612010] (IB criado no ao-fatiar). steering: "Fatia dividida no EWM" = itens novos como filhos do item original.
2. REGRA APLICADA:
   - SE "refinar o backlog" + "a FT-033 está grande demais" → refinamento: dividir — fonte: fatiar:95
   - ENTÃO a original fica `status: dividida` com `substituida-por: [FT-x, FT-y]` — fonte: fatiar:96
   - CONFLITO de formato: backlog.md:47-48 e :51 mandam `dividida` com a informação em `obs` ("substituida-por FT-…"); a tabela (backlog.md:27) não tem coluna `substituida-por`. fatiar:96 usa campo próprio.
   - ENTÃO as novas herdam cobertura (repartida, cada cenário em exatamente uma fatia), dependências e épico; ids novos — fonte: fatiar:97; fatiar:56-57
   - AMBÍGUO (sub): quem reparte os cenários e se há ok/GATE. O passo 2 (fatiar:61-70) só descreve o fatiamento inicial.
   - ENTÃO no EWM: sdd-elm modo backlog, item 4 (novos IBs filhos do IB 612010, que segue filho do épico) — fonte: elm:146-147; steering:74
   - ENTÃO conferir a DoR das novas — fonte: fatiar:101-102
3. OUTPUT GERADO: backlog.md com a original `dividida` e as novas linhas; resposta com a nova tabela. Sem template literal.
   ARQUIVOS ESCRITOS: backlog.md · commit na base.
   ESCRITA NO ELM: IBs novos (após "sim", S11-F4).
4. VEREDITO MECÂNICO: CONFLITO (fatiar:96 `substituida-por: [FT-x, FT-y]` como campo × backlog.md:47-48, :51 como texto em `obs`; a tabela não tem a coluna).
```

```text
S09-F3 · Refinamento — juntar fatias
1. INPUT EXATO: "refinar o backlog: junta a FT-035 e a FT-036"
   ESTADO: FT-035 `backlog` (P, cobre HF-03#3.1). FT-036 `backlog` (P, cobre HF-03#3.2, bloqueada-por FT-035). Sem IB no EWM (elm `—`).
2. REGRA APLICADA:
   - SE "refinar" + pedido de juntar → fonte: fatiar:99
   - SE ambas estão em `backlog` → juntar é permitido — fonte: fatiar:99
   - ENTÃO "a que some" fica `status: cancelada` com `motivo` — fonte: fatiar:99 (motivo como campo; backlog.md:48 põe o motivo em obs)
   - SEM REGRA: qual das duas some? Nenhuma regra escolhe.
   - SEM REGRA: como ficam cobre, bloqueada-por, tamanho e modo da resultante (fatiar:99 só diz "unir cobertura e dependências"; sem regra de tamanho)
   - SEM REGRA: IB da fatia cancelada no EWM — elm:46 proíbe apagar e manda roteiro manual, mas não há roteiro para cancelamento por junção
3. OUTPUT GERADO: nenhum definido.
   ARQUIVOS ESCRITOS: nenhum definido. ESCRITA NO ELM: nenhuma definida.
4. VEREDITO MECÂNICO: SEM REGRA (qual fatia fica; cobre, dependências e tamanho da resultante; tratamento do IB da cancelada).
```

```text
S09-F4 · Refinamento — fatia nova ("faltou uma fatia")
1. INPUT EXATO: "faltou uma fatia: o cenário 4.2 da HF-04 (estorno parcial) não está em nenhuma fatia"
   ESTADO: HF-04 cenário 4.2 JÁ EXISTE no prd.md (aprovado), sem fatia que o cubra. backlog.md tem FT-040…FT-042 cobrindo outros cenários de HF-04.
2. REGRA APLICADA:
   - SE "faltou uma fatia" → refinamento "nova fatia" — fonte: fatiar:95
   - SE o cenário é novo → PRD alterado antes (sdd-prd, S08-F3) — fonte: fatiar:100
   - SE o cenário NÃO é novo (já está no PRD) → fatiar:100 não se aplica; a regra de cobertura "cenário sem fatia → corrigir antes de mostrar" está no passo 1 (rascunho) — fonte: fatiar:57
   - AMBÍGUO: fatiar:57 é regra do fatiamento inicial. Não se sabe se vale no refinamento, nem se a correção vira uma nova linha direta ou desvio para sdd-prd.
   - SEM REGRA (sub): depois do novo GATE do PRD, não há passo que volte a fatiar o cenário novo (fatiar:100 termina no desvio)
   - SEM REGRA (sub): fatia nova que nasce de pedido sem relação com PRD → sdd-triar não citada aqui
3. OUTPUT GERADO: nenhum definido (ou desvio para sdd-prd, se for cenário novo).
   ARQUIVOS ESCRITOS: backlog.md (nova linha) — só se o caminho for a correção direta. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: AMBÍGUO (cenário existente sem fatia: fatiar:57 manda corrigir na montagem, fatiar:100 só trata cenário novo; o caminho escolhido não é dito).
```

```text
S09-F5 · Refinamento — reconferir a Definition of Ready
1. INPUT EXATO: "refinar o backlog: reconfere a Definition of Ready"
   ESTADO: FT-034 `backlog` com `falta: decisão D-07` já resolvida; cenários definidos; P/AFK. Passa na DoR. FT-031 `pronta` (sprint 3), com branch feature/FT-031-… e status.md (fase: implementar); a decisão D-09 foi reaberta (em aberto que muda comportamento) → deixa de passar.
2. REGRA APLICADA:
   - SE refinamento → conferir a DoR das fatias `backlog` e gravar `pronta` nas que passam — fonte: fatiar:101-102; backlog.md:70-75
   - SE FT-034 passa → `pronta` — fonte: fatiar:101
   - SE uma fatia deixa de passar → volta a `backlog` com `falta:` em obs — fonte: fatiar:102; backlog.md:75
   - fatiar:101 aplica a DoR só às fatias `backlog`; FT-031 está `pronta`, então fora desse escopo — mas backlog.md:75 manda voltar a `backlog` fatia `pronta` que deixa de passar
   - AMBÍGUO: backlog.md:51 diz que "em andamento não é gravado: é a fatia que tem status.md numa branch". Não se sabe se FT-031 deve voltar a `backlog` no backlog.md, nem o que acontece com a branch.
3. OUTPUT GERADO: lista das fatias conferidas (FT-034 `pronta`; FT-031 — indefinido). Sem template literal.
   ARQUIVOS ESCRITOS: backlog.md (status/obs de FT-034; FT-031 indefinido) · commit na base.
   ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: AMBÍGUO (FT-031 `pronta` em andamento: fatiar:101 só confere `backlog`; backlog.md:75 manda voltar; backlog.md:51 não grava andamento. Nota: o plano aponta conflito aqui; pelo texto é tensão, não duas ordens diretas).
```

```text
S09-X1 · Negativo: fatiar PRD que ainda não foi aprovado
1. INPUT EXATO: "fatiar o PRD do EP-04"
   ESTADO: prd.md EP-04 `em-revisao`; rubrica P rodada 1 = AJUSTAR.
2. REGRA APLICADA:
   - SE "fatiar o PRD" → skill — fonte: fatiar:3
   - SE entrada = PRD `aprovado` → fonte: fatiar:16 ("Entrada: PRD `aprovado`") — é pré-condição, sem ramo para entrada inválida
   - SEM REGRA: nenhuma regra manda recusar nem diz o que fazer quando o PRD não está aprovado; prd:126 só ocorre depois do GATE
3. OUTPUT GERADO: nenhum definido.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: SEM REGRA (fatiar:16 define a entrada sem ramo para o caso inválido; `fatiado` (re-fatiar) também não tem tratamento).
```

```text
S09-X2 · Negativo: sessão sem MCP do ELM
1. INPUT EXATO: "fatiar o PRD do EP-03"  (sessão sem MCP elm)
   ESTADO: igual a S09-F1, mas MCP elm ausente. steering: "Usa ELM: sim".
2. REGRA APLICADA:
   - SE sem MCP → não publicar; registrar `ELM pendente: <modo> <alvo>` no status.md (fatia) ou no rodapé do PRD (épico) — fonte: elm:23-25; sdd:122-124
   - ENTÃO horas da [ESP] sem MCP → `ELM pendente: lançar <h>h em [ESP] EP-03` no rodapé do PRD — fonte: fatiar:83
   - ENTÃO IB das fatias (passo 4) → sdd-elm modo backlog — fonte: fatiar:87
   - AMBÍGUO: para o IB de uma fatia, elm:24 prevê o status.md da fatia, que ainda não existe (é criado no iniciar); o rodapé do PRD é só para épico. Não se sabe onde registrar a pendência.
   - AMBÍGUO (sub): backlog.md:53 define `elm` = `pendente` para registro sem MCP, mas fatiar:75 grava `elm` = `—`
3. OUTPUT GERADO: rodapé do PRD com `ELM pendente: lançar 4h em [ESP] EP-03`. A pendência do IB não tem lugar definido.
   ARQUIVOS ESCRITOS: prd.md (rodapé) e backlog.md (elm `—` ou `pendente`, indefinido). ESCRITA NO ELM: pendente.
4. VEREDITO MECÂNICO: AMBÍGUO (onde e com qual valor registrar a pendência do IB de fatia: elm:24 × fatiar:75 × backlog.md:53).
```

#### Tabela-resumo · S09

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S09-F1 · Fatiar PRD aprovado | CONFLITO | fatiar:81 manda concluir a [ESP] pelo modo conclusão; elm:220-221 não inclui a [ESP] |
| S09-F2 · Dividir fatia | CONFLITO | `substituida-por` como campo (fatiar:96) × texto em `obs` (backlog.md:47-48, :51) |
| S09-F3 · Juntar fatias | SEM REGRA | não diz qual fica, nem cobre/tamanho da resultante, nem IB da cancelada |
| S09-F4 · Fatia nova | AMBÍGUO | cenário já existente sem fatia: fatiar:57 × fatiar:100 (só cenário novo) |
| S09-F5 · Reconferir DoR | AMBÍGUO | FT-031 `pronta` em andamento: backlog.md:75 × backlog.md:51 |
| S09-X1 · PRD não aprovado | SEM REGRA | fatiar:16 é pré-condição sem ramo para o caso inválido |
| S09-X2 · Sem MCP | AMBÍGUO | onde registrar `ELM pendente` do IB: elm:24 × fatiar:75 × backlog.md:53 |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| S09-F1 | `<produto>/backlog.md` — épico `status: fatiado` + seção `## Fatias — <EP> <título>` com uma linha por fatia (fatiar:74-77; backlog.md:25-29, 37) | Sim. A P3 escreveu o cabeçalho `## Fatias — EP-03` **sem o título**: backlog.md:25/37 exigem `<EP> <título>`. Seção nova deve ir "na ordem de prioridade dos épicos" e antes de `## Fatias — sem épico` (backlog.md:37): com `prioridade` do épico `—` (triar, triar:77-78) a posição não é definida; o backlog mínimo da setup (setup:241-242) não tem seção alguma | `.md`, tabela de 13 colunas (backlog.md:27) | **Divergências:** (1) `cobre`: o card usa `HF-01 · 1.1, 1.2 · REG-01` e `HF-02 · 2.1–2.3` (fatiar:51, 53), o arquivo exige `HF-01#1.1, HF-01#1.2, REG-01` e lista (backlog.md:29, 47): a conversão, inclusive de faixa `2.1–2.3`, não está escrita; (2) `modo` no card pode vir `HITL (texto do e-mail)` (fatiar:53), no arquivo só `AFK`/`HITL` (backlog.md:50); (3) "Próximos ids" (backlog.md:16, 79) não é atualizado por `sdd-fatiar` (fatiar:77 só diz "sequenciais, nunca reaproveitados"; triar:101 atualiza o dele); (4) `prioridade` da fatia: global ou por épico não dito; (5) colunas `sprint`, `responsavel`, `concluida-em`, `obs` = `—` só por backlog.md:38 | Escreve `sdd-fatiar`/`sdd-produto`, após `git switch <base>` + `pull --ff-only` (backlog.md:82). Commit "padrão do sdd.md" (fatiar:79), `backlog.md`+`prd.md` juntos. Branch: base, "direto ou PR curto" (setup default PR curto). Push: só "sim", pela pessoa | I-git (switch sem "sim" × steering:13; sem ramo para pull falho/árvore suja). I-perm: permitido | DIVERGENTE (cabeçalho da seção, notação de `cobre`, `modo`, Próximos ids). A P3 estava certa sobre Próximos ids; errou o cabeçalho |
| S09-F1 | `<produto>/epicos/<EP>-<slug>/prd.md` — `status: fatiado` (fatiar:78) | Sim | `.md` | `atualizado` sem regra (como em S08) | Mesmo commit (fatiar:79). **Ordem:** a pendência `ELM pendente: lançar <h>h em [ESP] EP-nn` no **rodapé do PRD** (fatiar:83) é escrita no passo 4, **depois** do commit do passo 3 → fica modificada e não commitada; nenhum segundo commit é prescrito. O `sdd-elm` modo backlog do Passo 4 comita de novo (elm:42), mas só "backlog" | I-git; I-elm | NÃO ESPECIFICADO (commit da pendência no rodapé) |
| S09-F1 | `<produto>/backlog.md` — coluna `elm` das fatias (via `sdd-elm`, Passo 4) | Sim | `[<id>](<url>)` | Confere com backlog.md:53 | `sdd-elm` grava e comita (`<FT\|EP> - Publicar no ELM`, elm:42 × steering:59, confirma P3) | I-elm: sem MCP o valor correto é `pendente` (backlog.md:53), mas fatiar:75 grava `—` e elm:24 só cita status.md (inexistente) / rodapé do PRD (é de épico). Confirma P3 | NÃO ESPECIFICADO (onde/como registrar a pendência do IB) |
| S09-F2 | `backlog.md` — original `status: dividida`, novas linhas | Sim | idem | **`substituida-por`**: fatiar:96 `substituida-por: [FT-x, FT-y]` (campo) × backlog.md:27 (a tabela não tem a coluna) e :48/:51 (`obs`: `substituida-por FT-…`, sem dois-pontos nem colchetes). `sprint`/`responsavel` das novas não definidos. Cabeçalho da seção/Próximos ids como em F1 | Commit na base (nenhum texto específico do refinamento; vale o do Passo 3 por analogia) | I-git. Fatia com `status.md`/branch (original em andamento): só `concluida` é protegida (fatiar:108); backlog.md:51 | DIVERGENTE (formato de `substituida-por`) — confirma P3 (CONFLITO de formato, não de comportamento) |
| S09-F3 | `backlog.md` — a fatia que some `status: cancelada` + motivo | Sim | idem | `motivo` vai em `obs` (backlog.md:48), fatiar:99 diz "com `motivo`" (campo) — mesma divergência. **Correção à P3:** fatiar:99 não diz "unir cobertura e dependências" (só "só fatias ainda em backlog; a que some fica cancelada com motivo"). A P3 atribuiu ao texto uma regra que ele não tem; sem regra, `cobre`/`bloqueada-por` da sobrevivente ficam sem atualização | Sem commit/ok descritos | I-git | NÃO ESPECIFICADO (qual fica; atualização de `cobre`/tamanho; erro da P3 em fatiar:99) |
| S09-F4 | `backlog.md` — nova linha (cenário já existente sem fatia) | Sim | idem | Linha nova segue backlog.md:27. Id novo + Próximos ids como em F1 | Sem regra de ok/commit | I-git | NÃO ESPECIFICADO (caminho quando o cenário já existe no PRD) — confirma P3 |
| S09-F5 | `backlog.md` — `status` `pronta`/`backlog` + `falta:` em `obs` | Sim | `falta: <…>` (backlog.md:48) | Confere. DoR de duas versões (backlog.md:70-75 × arquivos:73-78); fatiar usa a de backlog.md | Commit na base | I-git. Fatia `pronta` com `status.md` em branch: backlog.md:75 × :51 | DIVERGENTE (DoR duplicada; "em andamento" não é gravado) — confirma P3 (tensão, não conflito direto) |
| S09-X2 | `prd.md` rodapé (`ELM pendente: lançar …`) e `backlog.md` `elm` | Sim | texto livre no rodapé; `elm` = `pendente` ou `—` | rodapé: formato livre; baixa por `ELM feito:` (status-template:40, status:22) **não** é instruída por fatiar/elm/prd | Sem MCP: não commitado (ver F1) | I-elm | NÃO ESPECIFICADO (confirma P3 e acrescenta: nada instrui a baixa) |
| S09-X1 | — | — | — | — | — | — | sem escrita (PRD não aprovado: SEM REGRA, nada gravado) |

---


## S10 · sdd-planejamento

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S10-F1 · Modo inicial — acordos, equipe e roadmap
- **Gatilho inicial:** "monta o planejamento", "roadmap", "capacidade do time", "acordos do time" (plan:3). Evento: projeto novo sem `<produto>/planejamento/`; `sdd-iniciar` quando "nenhuma sprint aberta e nada no `acordos.md`" (iniciar:76-77).
- **Pré-condições / arquivos lidos:** `<produto>/planejamento/{equipe.json,acordos.md,roadmap.md}` se existirem; `assets/equipe.schema.json` e `references/arquivos.md` (do power instalado, não do projeto, plan:12-14); `backlog.md` (épicos); `members` do `pa_*.json` (logins); `git pull --ff-only` antes de gravar (arquivos:3).
- **Processamento interno:**
  1. **Equipe:** `equipe.json` existe → mostrar e perguntar só o que mudou. Por pessoa: nome, papel (único: P.O./Analista/Dev/QA/SM), login do ELM, horas/semana, ausências, horas de **revisão+verificação** (`horas-revisao-semana`), de **especificação** (`horas-especificacao-semana`, P.O. e Analista) e se **atende** (`atende`). Gravar no formato do schema, **validado antes de mostrar**.
  2. **Acordos:** propor e ajustar — cadência (Scrum, padrão sprints de 2 semanas com fluxo puxado; ou Kanban), WIP (1 fatia por sessão de agente; fatias esperando pessoa ≤ capacidade de revisão, ex. 2 por revisor; PR parado > 1 dia → destravar antes, exceção registrada `WIP excedido`), DoR e DoD (padrão em arquivos:73-86), tamanhos e pontos (`2/3/5`), reserva de atendimento (20% das horas de quem atende) e lançamento de horas (na conclusão da tarefa).
  3. **Roadmap:** épicos do `backlog.md` por valor e risco (maior incerteza mais cedo), agrupados em releases com um objetivo; épico sem PRD = "a descobrir" (`sdd-prd`); previsão = `fatias restantes ÷ vazão média`, com faixa se houver histórico (arquivos:101-102).
  - Regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar (plan:25).
- **Resultado final (output):** Resposta: propostas por etapa. Arquivos: `<produto>/planejamento/equipe.json`, `acordos.md`, `roadmap.md`. ELM: nenhum. Próximo passo: modo sprint (S10-F2).
- **Lacunas observadas:**
  - **Campos obrigatórios do schema sem pergunta:** `equipe.json` exige `projeto.nome`, `cadencia`, `duracao-sprint-semanas`, `inicio`, `pontos-por-tamanho`, `historico` (arquivos:17-28; schema `required`); plan:29-43 só pergunta pessoas, cadência (no passo 2) e pontos — **nunca pergunta a data de início da sprint 1 nem o nome do projeto**, mas a numeração e as datas da sprint dependem de `inicio` (S10-F2).
  - **Sem commit/push no modo inicial:** o modo sprint tem commit na base (plan:81-82); o inicial só tem "ok antes de gravar" (plan:25, arquivos:3-4). São artefatos de produto (steering:61) — falta o commit/PR curto.
  - **Cerimônias:** `acordos.md` traz a linha "Cerimônias" (arquivos:67), mas plan:34-43 não a pede.
  - **Chamadas parciais** ("acordos do time", "capacidade do time", description plan:3): o modo inicial é único e longo; não há regra para "só rever acordos" nem para "capacidade do time" (provavelmente o passo 1 do modo sprint, mas não dito). Quando `acordos.md` já existe, só `equipe.json` tem a regra "pergunte só o que mudou".
  - "Valide antes de mostrar" (plan:33, arquivos:10): sem ferramenta/método definido para validar o JSON contra o schema.
  - A skill não manda ler `.kiro/steering/sdd.md` nem trata projeto sem ELM.
  - `acordos.md` WIP: plan:38 lista `plano-em-revisao` + `aceita` + `pr-aberto`; arquivos:68 diz "revisão + PR aberto"; iniciar:84 diz "2 fatias esperando pessoa" — consistentes, mas `plano-em-revisao` só aparece em plan.

#### S10-F2 · Modo sprint — planejar a próxima sprint
- **Gatilho inicial:** "planejar a sprint" (plan:3, plan:47). Eventos: fim da virada ("replaneje a próxima pelo modo sprint", plan:124); handoff de `sdd-fatiar` (fatiar:90); `sdd-iniciar` quando não há sprint aberta (iniciar:76-77).
- **Pré-condições / arquivos lidos:** `equipe.json`, `acordos.md`, `roadmap.md`, `backlog.md`, sprint anterior (`sprints/sprint-<nn>.md`), `iterations` do `pa_*.json`, histórico (vazão das últimas 3 sprints).
- **Processamento interno:**
  1. **Capacidade** (horas da sprint = `horas-semana × semanas − ausências`, arquivos:56): revisão humana (limite principal); HITL (horas de dev acompanhando); vazão (média das últimas 3 sprints; 1ª sprint: 1 fatia por dev por semana) e velocidade em pontos; especificação; reserva de atendimento (% do `acordos.md` descontado antes de selecionar fatias).
  2. **Especificação:** épicos que entram em entrevista/PRD/fatiamento (do `roadmap.md` — os "a descobrir" do topo — e os `EP` `rascunho` com `prd` `—` do `backlog.md` ainda fora do roadmap, propondo a posição) → um `[ESP]` por épico, com responsável e horas previstas dentro da capacidade de especificação.
  3. **Seleção:** conferir a DoR das fatias do topo e gravar `pronta`/`backlog`; entram as `pronta` (de épico e sem épico, **inclusive as diretas**), respeitando `bloqueada-por`; parar ao atingir a **menor** das capacidades; fatia não `pronta` no topo → apontar o que falta (decisão, PRD, fatiar) antes de pular; cada fatia ganha **revisor** e **verificador** (não quem implementa) cabendo nas horas de revisão de cada um.
  4. **Meta da sprint:** uma frase de resultado de negócio.
  5. **Iteração:** perguntar a iteração do EWM (de `iterations` do `pa_*.json`) = `plannedFor` de todos os IBs e tarefas.
  6. **Proposta** (card 🗓️ com Fatias, Especificação, Atendimento, Capacidade, "Fica de fora (por capacidade)").
  7. "ok" → gravar `sprints/sprint-<nn>.md`, `sprint`/`responsavel`/`status` no `backlog.md`, commit na base, e **chamar sempre `sdd-elm` modo *sprint*** (S11-F5). Sem MCP ou com falha → coluna "Tarefa ELM" `pendente`.
- **Resultado final (output):** Resposta: card da sprint → confirmação. Arquivos: `<produto>/planejamento/sprints/sprint-<nn>.md` (Meta, Iteração, Situação `aberta`, Fatias, Especificação, Atendimento, Capacidade — formato arquivos:104-157), `<produto>/backlog.md` (`sprint`, `responsavel`, `status`, `pronta`/`backlog`). ELM: planos, IBs (`plannedFor`) e tarefas `[DEV][REV][VER][ESP]` via S11-F5, ids em "Tarefa ELM". Próximo passo: `sdd-iniciar` por fatia ("próxima fatia").
- **Lacunas observadas:**
  - **Datas e numeração:** o card exige `<início> → <fim>` e `<nn>` (plan:72), mas a skill não diz como derivá-los (de `equipe.json.projeto.inicio` + `duracao-sprint-semanas` + sprints existentes) — e `inicio` nunca é perguntado (S10-F1).
  - **Sprint anterior ainda `aberta`:** o modo sprint não verifica nem trata; arquivos:111 diz que "o painel usa a última `aberta`", o que quebra com duas abertas.
  - **Estimativa de horas das tarefas:** elm:162 exige "estimativa em horas" para `[DEV]/[REV]/[VER]`, mas o card da sprint (plan:73-78) só tem horas para `[ESP]` ("Horas previstas") — de onde vêm as horas de `[DEV]/[REV]/[VER]` não é dito.
  - **Quem grava os ids:** plan:83-84/elm:174-175 dizem que a `sdd-elm` grava "Tarefa ELM" no `sprint-<nn>.md` e `elm` no `backlog.md`; isso gera um segundo commit na base (elm:42), não previsto em plan:81-82.
  - **Kanban:** plan:35 oferece Kanban, mas todo o modo sprint, `sprint-<nn>.md` e a iteração são Scrum; nada define o equivalente (como entram as fatias, de onde vem `plannedFor` — só iniciar:75-76 diz "iteração corrente" do EWM).
  - **`status` no `backlog.md`** (plan:81): backlog.md:51 diz que "em andamento" não é gravado; o que se grava em `status` nesse momento (só `pronta`/`backlog`) não é dito.
  - **Projeto sem ELM:** passos 5 e 7 (iteração e `sdd-elm`) não têm ramo "sem ELM".
  - **"Capacidade do time"** (trigger do plan:3) mapeia para o passo 1 deste modo? não explicitado.

#### S10-F3 · Durante a sprint — acompanhamento
- **Gatilho inicial:** "Como está a sprint?" (plan:88 — **não consta da description**; sdd/SKILL:79 roteia "onde parei" ao `sdd-status`). Eventos: fatia cresceu; atendimento estoura a reserva.
- **Pré-condições / arquivos lidos:** `sprint-<nn>.md` aberta, `backlog.md`, `status.md` das branches (via `sdd-status`).
- **Processamento interno:**
  1. "Como está a sprint?" → `sdd-status` **filtrado pela sprint** (fase de cada fatia, bloqueios, WIP de revisão, PRs parados).
  2. Fatia que cresceu (passou de `G` no plano) → `sdd-fatiar` dividir (S09-F2), em vez de esticar.
  3. Atendimento que estoura a reserva → mostrar ao P.O.; **ele** decide qual fatia sai da sprint; o atendimento nunca tira fatia sozinho.
- **Resultado final (output):** Resposta: painel filtrado / decisão pedida ao P.O. Arquivos: nenhum gravado explicitamente neste modo. ELM: nenhum. Handoff: `sdd-fatiar`; decisão do P.O.
- **Lacunas observadas:**
  - **Remoção de fatia por estouro de reserva** (plan:90-91): não diz como se grava a saída (a mecânica existe só no Encaixe "entra no lugar de", plan:97, que volta `sprint` para `—` e move tarefas); aqui o texto para no "P.O. decide".
  - Não diz como o refinamento (dividir) devolve capacidade/vazão à sprint (a sprint foi planejada com a fatia original; as novas não estão no `sprint-<nn>.md`).
  - O trigger "como está a sprint" fora da description pode colidir com `sdd-status`.

#### S10-F4 · Encaixe de fatia fora da sprint
- **Gatilho inicial:** "encaixe na sprint" (plan:3). Evento: `sdd-iniciar` Passo 3.3 manda para cá fatia `pronta` (de qualquer trilha, inclusive direta) que não está na sprint aberta (plan:93-94; iniciar:72-75; loop:27).
- **Pré-condições / arquivos lidos:** `backlog.md` (fatia: trilha, tamanho, modo, origem), `sprint-<nn>.md` aberta, `equipe.json`/`acordos.md` para a capacidade restante.
- **Processamento interno:**
  1. Mostrar ao P.O. a fatia (trilha, tamanho, modo, origem), o que sobra da capacidade (revisão, vazão, HITL) e as opções com a recomendada: **entra na folga** · **entra no lugar de FT-…** (uma ainda não iniciada, que volta para `sprint` `—`) · **fica para a próxima sprint**.
  2. Com a decisão do P.O. (ou delegado): gravar `sprint` e `responsavel` (e revisor/verificador ≠ quem implementa) no `backlog.md`; linha no `sprint-<nn>.md` com Observação `encaixe: <decisão> (<quem decidiu>, <data>)`; commit na base; `sdd-elm` modo *sprint* para as tarefas da fatia; na troca, as tarefas da fatia que sai vão para a próxima iteração (só `plannedFor`).
  3. Voltar à `sdd-iniciar` (Passo 3, item 4 = WIP). Sem decisão, a fatia não começa; urgência acelera a decisão, não a dispensa.
- **Resultado final (output):** Resposta: opções + decisão registrada. Arquivos: `backlog.md`, `sprints/sprint-<nn>.md`. ELM: tarefas da fatia na iteração (S11-F5). Handoff: `sdd-iniciar`.
- **Lacunas observadas:**
  - Confere que o item de iniciar (Passo 3, item 4) é o WIP — correto (iniciar:78); mas **depois** dele, iniciar:83-85 exige o registro publicado em `origin/<base>` (push/PR curto), que não é mencionado aqui.
  - Não manda reconferir a DoR (a fatia é dada como `pronta`; pode estar desatualizada) nem a capacidade de revisão específica de revisor/verificador escolhidos (só "o que sobra da capacidade").
  - Kanban: iniciar:75 diz que não há encaixe; plan:93 não ressalva.
  - Fatia direta no encaixe: a `[DEV]` é a única tarefa (elm:172), mas o texto fala em revisor/verificador sem distinguir.

#### S10-F5 · Review da sprint
- **Gatilho inicial:** "review da sprint" (plan:3, plan:107).
- **Pré-condições / arquivos lidos:** `sprint-<nn>.md` (fatias concluídas), `verificacao.md` de cada fatia (`.kiro/specs/<ft>-<slug>/`, só citado como "`verificacao.md`"), `backlog.md`.
- **Processamento interno:** para cada fatia concluída, mostrar o cenário entregue e a **evidência** do `verificacao.md` (resposta, contagem, screenshot); registrar o retorno do P.O. no `sprint-<nn>.md` (seção Review, arquivos:137-138); pedido novo vira cenário/fatia nova pela `sdd-prd`/`sdd-fatiar` — **não reabre** fatia concluída.
- **Resultado final (output):** Resposta: demonstração por fatia. Arquivos: `sprints/sprint-<nn>.md` (seção Review). ELM: nenhum. Handoff: `sdd-prd` (S08-F3) / `sdd-fatiar` (S09-F4) para pedidos novos.
- **Lacunas observadas:**
  - Sem "ok"/commit explícito (a regra de ouro de plan:25 cobre "cada etapa", mas aqui não há gravação descrita) e sem dizer o que fazer se a fatia está "concluída" mas a evidência com dado real está em `.kiro/local/` (steering:14: nunca para o git) — como exibi-la e o que registrar no `sprint-<nn>.md`.
  - Pedido novo de fatia **sem épico** deveria ir à `sdd-triar` (não citada em plan:110-111).
  - Entregas de `[ESP]` e `[ATD]` não entram na review.
  - Caminho de `verificacao.md` não é dado (só inferível do layout `.kiro/specs/<ft>-<slug>/`, sdd/SKILL:106).

#### S10-F6 · Retrospectiva e virada de sprint
- **Gatilho inicial:** "virada de sprint", "fechar a sprint" (plan:3, plan:113).
- **Pré-condições / arquivos lidos:** `sprint-<nn>.md` aberta, `backlog.md` (status das fatias), `equipe.json`, `acordos.md`, dados da retrospectiva (via `sdd-aprender`), timesheets do EWM.
- **Processamento interno:**
  1. **Retrospectiva com dados:** `sdd-aprender` modo retrospectiva (vazão, lead time, rodadas de revisão, correções humanas por causa, AFK que chegaram ao PR sozinhas); registrar no `sprint-<nn>.md`: bom · melhorar · ações (cada ação com dono).
  2. **Horas:** `sdd-elm` modo *horas* relatório (S11-F9) por tipo e por pessoa; preencher "Números" (planejadas × lançadas) e apontar tarefas concluídas sem horas — só aqui.
  3. **Fechar:** concluídas contam na vazão e pontos; não concluídas (fatias, `[ESP]`, `[ATD]`) **migram** para a próxima sprint (no arquivo antigo ficam "→ sprint <nn+1>"; histórico não apagado); `**Situação:** fechada`.
  4. Recalcular vazão média, velocidade e horas por tipo (`equipe.json` → `projeto.historico`, incluindo `horas-lancadas` e `reserva-atendimento`), **recalibrar** a reserva de atendimento pelo consumido e **replanejar a próxima** pelo modo sprint (migradas consomem capacidade primeiro).
  5. **ELM:** `sdd-elm` modo *sprint* virada (S11-F6): tarefas/IBs não concluídos só mudam `plannedFor` para a nova iteração, as novas são publicadas; roteiro manual de baseline se o projeto exige.
- **Resultado final (output):** Resposta: retro + números + próxima sprint proposta. Arquivos: `sprints/sprint-<nn>.md` (Retrospectiva, Números, Situação `fechada`, "→ sprint nn+1"), `equipe.json` (`historico`), `acordos.md` (reserva recalibrada); depois `sprint-<nn+1>.md` (S10-F2). ELM: via S11-F6 e S11-F9.
- **Lacunas observadas:**
  - **Coluna `sprint` do `backlog.md` não é atualizada na migração:** plan:121 só muda o `sprint-<nn>.md` antigo ("→ sprint nn+1"); backlog.md:64 diz que `sprint`/`responsavel` são do planejamento, mas a virada não manda regravar `sprint` das fatias migradas (nem das `AT`/`[ESP]` em `atendimentos/`).
  - **Ordem:** o passo 3 grava `fechada` antes do passo 5 (ELM) e de replanejar; falha do ELM no meio deixa a sprint fechada com tarefas na iteração antiga (só há a regra "Sem MCP → pendente" para o modo sprint, plan:83-84, não para a virada).
  - **Roadmap:** a previsão do `roadmap.md` (arquivos:101-102) depende da vazão; a virada recalcula vazão (plan:123) mas não manda atualizar `roadmap.md` nem fechar release.
  - **Sem commit/"ok"** descritos na virada; vários arquivos de produto mudam (sprint, equipe, acordos).
  - **Kanban:** não há virada de sprint (nem retro por sprint) definida para a cadência Kanban oferecida em plan:35.
  - `sdd-aprender` modo retrospectiva é a fonte dos números; se a skill não tiver os dados (fatias sem `status.md`/`verificacao.md` na base), a skill não define fallback.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S10-F1 · Modo inicial — acordos, equipe e roadmap
1. INPUT EXATO: "monta o planejamento do projeto"
   ESTADO: <produto>/planejamento/ inexistente. backlog.md: EP-03 `fatiado` (prd); EP-04 `rascunho` prd `—`; EP-05 `rascunho` prd `—`. pa_*.json com members (ana.souza, joao.lima, rita.melo). MCP sim.
2. REGRA APLICADA:
   - SE "monta o planejamento" → fonte: plan:3 (description)
   - SE equipe.json não existe → perguntar por pessoa: nome, papel (um de P.O./Analista/Dev/QA/SM), login, horas/semana, ausências, horas de revisão+verificação, horas de especificação, atende — fonte: plan:29-33; arquivos:45-57
   - SE pa_*.json tem members → login vem de lá — fonte: plan:30
   - ENTÃO gravar no formato do schema, "validado antes de mostrar" — fonte: plan:33; arquivos:10
   - SEM REGRA: nenhum método de validação é dito (ferramenta, comando, ou leitura manual?)
   - SE o schema exige `projeto.nome`, `cadencia`, `duracao-sprint-semanas`, `inicio`, `pontos-por-tamanho`, `historico` (schema:14, :20; arquivos:17-28) → o plano pergunta cadência e pontos (plan:29-43), mas NÃO pergunta nome do projeto, data de início da sprint 1 nem duração
   - SEM REGRA: origem de `projeto.nome`, `inicio` e `duracao-sprint-semanas`
   - ENTÃO regra de ouro: cada etapa termina com a proposta na tela e "ok" antes de gravar — fonte: plan:25
   - ENTÃO acordos: cadência, WIP, DoR e DoD (arquivos:73-86), tamanhos 2/3/5, reserva 20%, lançamento de horas — fonte: plan:34-43
   - ENTÃO roadmap: épicos por valor e risco; épico sem PRD = "a descobrir" → EP-04 e EP-05 — fonte: plan:44-45
   - AMBÍGUO (sub): previsão do roadmap = fatias restantes ÷ vazão média (arquivos:101-102); sem histórico não há vazão média. A regra de 1ª sprint (plan:52-53) é do modo sprint.
   - SEM REGRA (sub): commit no modo inicial (plan:81-82 só existe no modo sprint)
3. OUTPUT GERADO: propostas por etapa (equipe → acordos → roadmap), cada uma com "ok". Sem template literal.
   ARQUIVOS ESCRITOS (após cada "ok"): planejamento/equipe.json (schema) · acordos.md (arquivos:61-88) · roadmap.md (arquivos:92-99). Commit: SEM REGRA.
   ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: SEM REGRA (projeto.nome, inicio e duracao-sprint-semanas são obrigatórios no schema e não têm pergunta nem fonte). Subs: método de validação ausente; previsão sem histórico; commit.
```

```text
S10-F2 · Modo sprint — planejar a sprint 3
1. INPUT EXATO: "planeja a sprint 3"
   ESTADO: equipe.json: scrum, 2 semanas, inicio 2026-10-06; historico sprints 1–3 com fatias-concluidas 5, 4, 6 (pontos 15, 12, 18). acordos.md: WIP 2 por revisor; reserva 20%. roadmap.md presente. backlog.md: FT-031 `pronta` (EP-03, M, AFK, elm 612002); FT-032 `backlog` (falta: decisão; P; bloqueada-por FT-031); FT-033 `pronta` (EP-03, M, HITL, bloqueada-por FT-031); EP-05 "a descobrir". sprints/sprint-002.md `fechada`. pa_*.json iterations: "Sprint 3". Membros: ana.souza P.O. (10 h/sem, revisão 4, especificação 4, atende); joao.lima Dev (30 h/sem, revisão 6); rita.melo Analista (20 h/sem, revisão 2, especificação 8).
2. REGRA APLICADA:
   - SE "planeja a sprint" → fonte: plan:3, plan:47
   - ENTÃO capacidade de horas = horas-semana × semanas − ausências — fonte: plan:49; arquivos:56 (cálculo determinístico)
   - ENTÃO revisão humana = soma de horas-revisao-semana × semanas (limite principal) — fonte: plan:50
   - SEM REGRA: FT-033 é HITL — "consome horas de dev acompanhando" (plan:51), mas quantas horas por fatia HITL? Nenhum número nem fórmula.
   - ENTÃO vazão = média das últimas 3 sprints = 5 fatias — fonte: plan:52-53; schema:31-59
   - ENTÃO especificação: horas-especificacao-semana × semanas — fonte: plan:54
   - ENTÃO épicos para especificação = roadmap "a descobrir" + EP `rascunho` sem PRD fora do roadmap (EP-04, EP-05); um [ESP] por épico — fonte: plan:57-60
   - SEM REGRA: quem define as "horas previstas" do [ESP]? plan:59 manda "com responsável e horas previstas", sem dizer quem escolhe
   - ENTÃO reserva = 20% das horas-semana de quem atende (ana.souza: 10 × 2 × 20% = 4 h) — fonte: plan:55-56; arquivos:70
   - CONFLITO (seleção): "confira a DoR das fatias do topo e grave pronta" — qual DoR? backlog.md:70-75 ("dependências concluídas ou planejadas antes"; sem "cabe em janela de contexto") × arquivos:73-78 ("dependências concluídas ou na mesma sprint antes dela"; com "cabe em uma janela de contexto"). Ambos os arquivos são citados como padrão e os dois dão `pronta` (backlog.md:63-64).
   - ENTÃO FT-031 e FT-033 são candidatas; FT-032 (`backlog`) → apontar o que falta — fonte: plan:61-66
   - ENTÃO FT-033 entra só se FT-031 entra antes (bloqueada-por) — fonte: plan:62-64
   - ENTÃO cada fatia ganha revisor e verificador (não quem implementa), com soma cabendo nas horas de revisão — fonte: plan:65-66
   - AMBÍGUO (sub): quem escolhe o revisor e o verificador? plan:65 não diz
   - ENTÃO iteração: perguntar a iteração de iterations do pa_*.json → "Sprint 3" → plannedFor — fonte: plan:68-69
   - ENTÃO meta: uma frase de resultado de negócio — fonte: plan:67 (quem a escreve, não diz)
   - AMBÍGUO (sub): datas `<início> → <fim>` do card: plan:72 pede, sem fórmula; schema:20 diz só "início da sprint 1"
   - ENTÃO card (template literal, plan:71-80)
   - ENTÃO "ok" → gravar sprints/sprint-003.md (formato arquivos:104-157), sprint/responsavel/status no backlog.md, commit na base, e sdd-elm modo sprint — fonte: plan:81-84
3. OUTPUT GERADO: card literal (plan:71-80):
   🗓️ Sprint 3 · <início> → <fim> · iteração Sprint 3 · meta: <…>
   Fatias: FT-031 (M, AFK, ana/ana), FT-033 (M, HITL, …)
   Especificação: EP-05 · rita.melo · <h> h
   Atendimento: reserva 4h (20% de ana.souza)
   Capacidade: revisão <h>h · especificação <h>h · vazão prevista 2 fatias / 6 pts · HITL <h>h (sem regra)
   Fica de fora (por capacidade): FT-032 (falta decisão)
   Após "ok": gravações e chamada do elm.
   ARQUIVOS ESCRITOS: planejamento/sprints/sprint-003.md (Situação `aberta`) · backlog.md (sprint 3, responsavel, status pronta) · commit na base.
   ESCRITA NO ELM: sdd-elm modo sprint (S11-F5) após "sim"; ids da coluna "Tarefa ELM" gravados em seguida (elm:174-175), com segundo commit (elm:42).
4. VEREDITO MECÂNICO: CONFLITO (DoR: backlog.md:70-75 × arquivos:73-78; ambos usados para gravar `pronta`, backlog.md:63-64). Subnotas: horas por fatia HITL (SEM REGRA); horas previstas do [ESP] (SEM REGRA); datas (AMBÍGUO); revisor/verificador (AMBÍGUO).
```

```text
S10-F3 · Durante a sprint — acompanhamento
1. INPUT EXATO: "como está a sprint 3?"
   ESTADO: sprint-003 `aberta`. FT-031 em andamento (status.md na branch). FT-033 com status.md "bloqueada: aguardando texto do e-mail". PR de FT-031 parado há 2 dias. AT-013 consumiu 6 h da reserva de 4 h.
2. REGRA APLICADA:
   - AMBÍGUO (rota): "como está a sprint" não está na description (plan:3); plan:88 manda para sdd-status; sdd:79 roteia "saber onde parei / o que fazer agora" para sdd-status. Não é dito qual skill atende a frase.
   - ENTÃO (se roteado para sdd-status) painel filtrado pela sprint — fonte: plan:88 (delegado)
   - SE fatia passou de G no plano → sdd-fatiar (dividir), não esticar — fonte: plan:89
   - SE atendimento estoura a reserva → mostrar ao P.O.; ele decide qual fatia sai; atendimento não tira fatia sozinho — fonte: plan:90-91
   - SEM REGRA (sub): como gravar a saída de fatia (sprint `—`?) — plan:211 (mecânica só existe no encaixe)
3. OUTPUT GERADO: painel (delegado) e pedido de decisão ao P.O.: "AT-013 excedeu a reserva em 2 h: qual fatia sai?"
   ARQUIVOS ESCRITOS: nenhum (plan:209). ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: AMBÍGUO (rota: plan:3 não lista o gatilho; sdd:79 e plan:88 apontam para sdd-status — qual skill responde a frase não é dito).
```

```text
S10-F4 · Encaixe de fatia fora da sprint
1. INPUT EXATO: "vamos trabalhar na FT-036"  (sdd-iniciar encaminha ao planejamento)
   ESTADO: sprint-003 aberta com FT-031 e FT-033. Revisão restante de ana.souza = 0 h. FT-036 `pronta` (padrão, M, AFK, origem EP-03), fora da sprint. FT-033 `pronta` na sprint 3, responsavel joao.lima, sem status.md (não iniciada).
2. REGRA APLICADA:
   - SE fatia `pronta` (de qualquer trilha) fora da sprint aberta → encaixe — fonte: plan:93-94 (handoff de iniciar, delegado)
   - ENTÃO mostrar a fatia (trilha, tamanho, modo, origem), o que sobra (revisão, vazão, HITL) e as opções — fonte: plan:95-98
   - Cálculo: revisão restante 0 h → "entra na folga" não cabe — fonte: plan:96 (determinístico)
   - SEM REGRA: critério da opção "recomendada" (plan:98 "com a recomendada" não diz como escolher)
   - SE decisão = "entra no lugar de FT-033" → FT-033 volta a `sprint` `—`; suas tarefas vão para a próxima iteração (só plannedFor) — fonte: plan:97; plan:103-104; elm:172-175
   - ENTÃO gravar sprint e responsavel (e revisor/verificador ≠ implementador) no backlog.md — fonte: plan:100-101
   - ENTÃO linha no sprint-003.md com Observação `encaixe: entra no lugar de FT-033 (ana.souza, <data>)` — fonte: plan:101-102 (a linha da FT-033 — status — não tem regra)
   - ENTÃO commit na base; sdd-elm modo sprint para as tarefas da fatia — fonte: plan:102-103
   - ENTÃO voltar a sdd-iniciar (Passo 3, item 4) — fonte: plan:104
   - SE sem decisão → a fatia não começa — fonte: plan:105
   - SEM REGRA (sub): DoR não é reconferida no encaixe; capacidade específica de revisor e verificador não é checada (plan:93-105)
3. OUTPUT GERADO: bloco de opções (formato livre); após a decisão: confirmações de gravação.
   ARQUIVOS ESCRITOS: backlog.md (FT-036 sprint 3; FT-033 sprint `—`) · sprints/sprint-003.md (Observação `encaixe`) · commit na base.
   ESCRITA NO ELM: sdd-elm modo sprint (S11-F5) para as tarefas de FT-036 e o replanejamento de FT-033 (só plannedFor), após "sim".
4. VEREDITO MECÂNICO: SEM REGRA (critério da opção "recomendada", plan:95-98; além disso, DoR e capacidade específica de revisor/verificador no encaixe não estão escritas).
```

```text
S10-F5 · Review da sprint
1. INPUT EXATO: "review da sprint 3"
   ESTADO: sprint-003 `aberta`. FT-031 `concluida` no sprint-003.md. .kiro/specs/FT-031-<slug>/verificacao.md com evidência (POST /bloqueio → 423; contagem de 14 contas). FT-033 em andamento. Evidência sem dado de cliente (não vai para .kiro/local).
2. REGRA APLICADA:
   - SE "review da sprint" → fonte: plan:3, plan:107
   - ENTÃO para cada fatia concluída (linha com Status `concluida`) → mostrar o cenário entregue e a evidência do verificacao.md — fonte: plan:109; arquivos:117
   - ENTÃO caminho do verificacao.md = .kiro/specs/<ft>-<slug>/ — fonte: sdd:106
   - SE a evidência tem dado real → fica em .kiro/local/ (não se aplica) — fonte: steering:14
   - ENTÃO registrar o retorno do P.O. no sprint-003.md, seção Review — fonte: plan:111; arquivos:137-138
   - "ok" antes de gravar — fonte: plan:25
   - ENTÃO artefato de produto na base; commit — fonte: steering:61
   - SE pedido novo → vira cenário/fatia nova; não reabre fatia concluída — fonte: plan:110-111 (ver S10-X2 para o destino do pedido novo)
3. OUTPUT GERADO: demonstração por fatia: "FT-031 · cenário 1.1 · evidência: 423 / 14 contas"; "Registrado: FT-031 aceito pelo P.O.".
   ARQUIVOS ESCRITOS: planejamento/sprints/sprint-003.md (seção Review) · commit na base.
   ESCRITA NO ELM: nenhuma (plan:235 — fora do escopo).
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S10-F6 · Retrospectiva e virada de sprint
1. INPUT EXATO: "virada de sprint: fecha a sprint 3"
   ESTADO: sprint-003 `aberta`. FT-031 concluida (concluida-em 2026-10-28). FT-033 em andamento. [ESP] EP-03: 16 h previstas, 12 h lançadas, tarefa não concluída. AT-013 `aberto` (IB Atendimento 612005). pa_*.json iterations: "Sprint 4" existe. equipe.json com historico das sprints 1–2. acordos.md: reserva 20%. Manual no DOORS Next: nada.
2. REGRA APLICADA:
   - SE "virada de sprint" → fonte: plan:3, plan:113
   - ENTÃO retrospectiva com dados: sdd-aprender modo retrospectiva (delegado) → bom · melhorar · ações (dono) em sprint-003.md — fonte: plan:115-117
   - ENTÃO horas: sdd-elm modo horas relatório; preencher Números; apontar tarefas concluídas sem horas — fonte: plan:118-119; elm:199-201
   - ENTÃO fechar: concluídas contam; FT-033, [ESP] e [ATD] migram para a próxima sprint ("→ sprint 4" no arquivo antigo); `**Situação:** fechada` — fonte: plan:120-122; arquivos:111, :118
   - AMBÍGUO (sub): a coluna `sprint` do backlog.md das migradas não é regravada na virada (plan:121 só muda o arquivo antigo); backlog.md:64 põe `sprint` no planejamento. FT-033 fica com `sprint 3` até ser replanejada.
   - ENTÃO recalcular vazão, velocidade e horas por tipo em equipe.json → historico — fonte: plan:123; schema:31-59
   - SEM REGRA: "recalibrar a reserva de atendimento pelo consumido" — fonte: plan:123; nenhuma fórmula
   - ENTÃO replanejar a próxima pelo modo sprint (migradas consomem capacidade primeiro) — fonte: plan:124
   - ENTÃO sdd-elm modo sprint virada (S11-F6) — fonte: plan:125-126; elm:176-178
3. OUTPUT GERADO: retro + números + próxima sprint proposta (plan:249). Sem template literal de "Números" além do arquivo (arquivos:144-153).
   ARQUIVOS ESCRITOS: sprint-003.md (Retrospectiva, Números, `fechada`, "→ sprint 4") · equipe.json (historico) · acordos.md (reserva — sem fórmula) · backlog.md (sprint das migradas — AMBÍGUO) · sprint-004.md (depois do replanejamento).
   ESCRITA NO ELM: S11-F6 (plannedFor de [ESP], [ATD] e FT-033) e S11-F9 (relatório) após "sim".
4. VEREDITO MECÂNICO: SEM REGRA (recalibração da reserva de atendimento "pelo consumido", plan:123, sem fórmula). Subs: coluna sprint do backlog.md (AMBÍGUO); falha do ELM no passo 5 com a sprint já fechada (passo 3) — sem regra.
```

```text
S10-X1 · Negativo: chamada parcial "acordos do time" com planejamento já existente
1. INPUT EXATO: "acordos do time: só rever a reserva de atendimento"
   ESTADO: equipe.json, acordos.md e roadmap.md existem.
2. REGRA APLICADA:
   - SE "acordos do time" casa com description → fonte: plan:3
   - SE equipe.json existe → "mostre e pergunte só o que mudou" — fonte: plan:29 (vale para equipe.json, não para acordos)
   - SE acordos.md existe → NENHUMA regra de revisão parcial. O modo inicial é único e completo: passos 1 a 3 (plan:27-45).
   - SEM REGRA: "só a reserva" é escopo parcial sem regra
3. OUTPUT GERADO: nenhum definido.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: SEM REGRA (o modo inicial não tem escopo parcial; a regra "só o que mudou" vale só para equipe.json).
```

```text
S10-X2 · Negativo: pedido novo do P.O. durante a review
1. INPUT EXATO: "o relatório também precisa exportar em CSV"  (pedido novo, sem épico, durante review)
   ESTADO: sprint-003 em review. FT-031 concluída. Sem ficha, sem épico relacionado.
2. REGRA APLICADA:
   - SE pedido novo na review → "vira cenário/fatia nova pela sdd-prd/sdd-fatiar" — fonte: plan:110-111
   - SE toda demanda nova → entra pela sdd-triar — fonte: sdd:22; triar:16
   - CONFLITO: plan:110-111 manda o pedido para sdd-prd/sdd-fatiar; sdd:22 e triar:16 mandam toda demanda nova para sdd-triar. Nenhuma regra diz qual vale quando não há épico.
3. OUTPUT GERADO: duas rotas possíveis (sdd-prd/sdd-fatiar ou sdd-triar).
   ARQUIVOS ESCRITOS: nenhum agora. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: CONFLITO (plan:110-111 "sdd-prd/sdd-fatiar" × sdd:22 e triar:16 "sdd-triar" para toda demanda nova).
```

```text
S10-X3 · Negativo: P.O. não escolhe entre as três opções do encaixe
1. INPUT EXATO: "a FT-036 não entra nesta sprint, nem no lugar de nada"  (resposta ao encaixe)
   ESTADO: igual a S10-F4.
2. REGRA APLICADA:
   - SE encaixe → opções: entra na folga · entra no lugar de FT-… · fica para a próxima sprint — fonte: plan:96-98
   - SE sem decisão → a fatia não começa — fonte: plan:104-105
   - AMBÍGUO: "não entra" equivale a "fica para a próxima sprint" (então registrar a decisão em sprint-003.md) ou é "sem decisão" (então nada é gravado)? As regras não dizem.
3. OUTPUT GERADO: indefinido (duas leituras).
   ARQUIVOS ESCRITOS: indefinido (sprint-003.md com Observação `encaixe: fica para a próxima` ou nenhum). ESCRITA NO ELM: indefinida.
4. VEREDITO MECÂNICO: AMBÍGUO (plan:96-98 × plan:104-105: recusa sem nome de opção pode ser "fica para a próxima" ou "sem decisão").
```

#### Tabela-resumo · S10

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S10-F1 · Modo inicial | SEM REGRA | projeto.nome, inicio, duração obrigatórios no schema e sem pergunta |
| S10-F2 · Modo sprint | CONFLITO | DoR: backlog.md:70-75 × arquivos:73-78, ambas gravam `pronta` |
| S10-F3 · Durante a sprint | AMBÍGUO | "como está a sprint" fora da description; sdd:79 × plan:88 |
| S10-F4 · Encaixe | SEM REGRA | critério da opção "recomendada" não escrito (plan:98) |
| S10-F5 · Review | DETERMINÍSTICO | — |
| S10-F6 · Retro e virada | SEM REGRA | recalibração da reserva "pelo consumido" sem fórmula (plan:123) |
| S10-X1 · Acordos parcial | SEM REGRA | modo inicial sem escopo parcial |
| S10-X2 · Pedido novo na review | CONFLITO | plan:110-111 × sdd:22 e triar:16 |
| S10-X3 · "Não entra" no encaixe | AMBÍGUO | recusa = "fica para a próxima" ou "sem decisão"? (plan:96-98 × plan:104-105) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template/schema? | Sucesso (gravado e fechado) | Inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| S10-F1 | `<produto>/planejamento/equipe.json` (plan:22-23) | Sim (P3 sem `<produto>`). `planejamento/` existe vazia desde a setup (setup:242) | `.json`, `$schema` primeiro e sempre a URL raw (arquivos:10-11) | **Validado com jsonschema 4.26 (Draft 2020-12):** o exemplo de arquivos:14-43 passa; o estado da P3 passa; **o que o modo inicial pergunta (plan:29-33) NÃO passa**: faltam `projeto.nome`, `projeto.duracao-sprint-semanas`, `projeto.inicio` (a P3 viu) e também `membros[].ativo` (obrigatório no schema, nunca perguntado; a P3 **não** viu) e `projeto.historico` (obrigatório; sem instrução de gravar `[]` na 1ª vez; vazio é aceito). Kanban continua exigindo `duracao-sprint-semanas` e `inicio` sem valor sentinela. O schema **não** impõe "revisão+especificação ≤ horas-semana" (arquivos:49: 9+9 em 10 h passa) nem "exatamente um P.O." além de `contains` (esse, sim, é imposto) | Escreve `sdd-planejamento`/`sdd-produto`; "ok" antes (plan:25) e `pull --ff-only` (arquivos:3). **Sem commit/branch/push no modo inicial** (confirma P3; o commit existe só no modo sprint, plan:81-82). "Valide antes de mostrar" sem método (arquivos:10) — o agente só tem shell restrito (ag-prod:61-76 não inclui python/ajv) | I-git (só pull: arquivos:3). I-perm: permitido | DIVERGENTE (schema exige 4 campos que o roteiro não coleta — `ativo` é novo) + NÃO ESPECIFICADO (commit; método de validação) |
| S10-F1 | `<produto>/planejamento/acordos.md` (arquivos:61-88) | Sim | `.md`, tabela `Item \| Acordo` + DoR/DoD em checklists | Confere com o template; `Cerimônias` está no template (arquivos:67) mas plan:34-43 não pergunta. DoR do template ≠ DoR de backlog.md:70-75 (acordos tem "janela de contexto" e "mesma sprint"); `sdd-fatiar` lê a de backlog.md, nunca a editada aqui | Sem commit (idem) | I-git; I-perm | NÃO ESPECIFICADO (commit) + DIVERGENTE (DoR duplicada, confirma P3) |
| S10-F1 | `<produto>/planejamento/roadmap.md` (arquivos:92-99) | Sim | `.md`, tabela `Release \| Objetivo \| Épicos \| Previsão` | Confere. Previsão sem histórico: "—" no exemplo (arquivos:98), sem regra textual | Sem commit | I-git | NÃO ESPECIFICADO (commit; previsão sem histórico) |
| S10-F2 | `<produto>/planejamento/sprints/sprint-<nn>.md` (plan:81; arquivos:104) | **A P3 escreveu `sprint-003.md`** (zero-padding de 3 dígitos); o texto só tem `<nn>` e "Sprint 3" (arquivos:107; backlog.md:52 "número da sprint"). `iniciar:73` e `status:31` comparam `sprint` do backlog com o arquivo: o padding é regra implícita não escrita. `sprints/` não existe até a 1ª gravação | `.md` | Template arquivos:106-154 tem 9 seções; o card (plan:72-80) só alimenta Meta/Iteração/Fatias/Especificação/Atendimento/Capacidade. Faltam regras: valor inicial de `Situação` de cada linha de Especificação (`entrevista\|PRD\|fatiamento`, arquivos:156), `Status` inicial das Fatias, se criam-se vazias as seções Review/Retrospectiva/Números; datas `<início> → <fim>` sem fórmula (P3 viu). A tabela Fatias do arquivo **não tem coluna "Tarefa ELM"** (arquivos:115) — só Especificação (:122) e Atendimento (:130) a têm | `sdd-planejamento` grava após "ok", commit na base (plan:81-82), depois `sdd-elm` modo sprint, que grava ids e faz **segundo commit** (elm:41-42, 174-175; confirma P3). Push: "sim" | I-git. Sprint anterior ainda `aberta`: arquivos:111 supõe uma só, sem regra | NÃO ESPECIFICADO (nome do arquivo: padding; valores iniciais) + DIVERGENTE (P3 `sprint-003`) |
| S10-F2 | `<produto>/backlog.md` — `sprint`, `responsavel`, `status`, `pronta`/`backlog` (plan:61-66, 81) | Sim | idem F1 | `status` gravado = só `pronta`/`backlog` (backlog.md:51: "em andamento" não existe). **`revisor`/`verificador` não têm coluna no backlog** (backlog.md:27/33); só em sprint-<nn>.md (arquivos:115): plan:100-101 escreve "`sprint` e `responsavel` no `backlog.md` (e revisor e verificador…)", o que sugere gravá-los no backlog. A P3 não notou | mesmo commit do sprint-<nn>.md | I-git | DIVERGENTE (plan:100-101 × colunas do backlog) |
| S10-F2 (pós-ELM) | `sprint-<nn>.md` col. "Tarefa ELM" (Especificação, Atendimento) e `backlog.md` col. `elm` (tarefas `<prefixo> [<id>](<url>)` separadas por ` · `, backlog.md:53) | Sim | — | **A P3 (S11-F5) diz "sprint-003.md (coluna Tarefa ELM)" para todas as tarefas: só vale para `[ESP]` e `[ATD]`.** Ids de `[DEV]/[REV]/[VER]` não têm coluna no sprint-<nn>.md; ficam no `elm` do backlog (backlog.md:53). `pendente` (plan:83-84) só existe na Especificação/Atendimento; para fatias o equivalente não está escrito | segundo commit pelo `sdd-elm` (elm:42), mensagem `<FT\|EP> - …` não cobre sprint | I-elm; `sdd-codificador` **negaria** essa gravação (ag-cod:44-45/246-247) — por isso iniciar:112-114 manda não gravar; elm:174-175 não conhece a exceção (explica a contradição da P3, não a resolve no texto) | DIVERGENTE (elm:174-175/plan:83-84 × arquivos:115) |
| S10-F4 | `backlog.md` (`sprint`, `responsavel`; FT que sai volta a `sprint` `—`) e `sprint-<nn>.md` (linha com `encaixe: <decisão> (<quem>, <data>)`) (plan:100-103) | Sim | idem | Observação existe na tabela Fatias (arquivos:115). A linha da fatia que **sai** (Status `→ sprint <nn+1>`? remover?) sem regra (confirma P3). Revisor/verificador: ver acima | commit na base (plan:102); `sdd-elm` sprint a seguir. iniciar:83-85 exige o registro em `origin/<base>` (push/PR curto, "sim"): plan não cita (confirma P2) | I-git | NÃO ESPECIFICADO (linha da fatia que sai; commit/push) |
| S10-F5 | `sprint-<nn>.md` seção `## Review` (plan:110-111; arquivos:137-138) | Sim | texto livre: "retorno do P.O. por fatia; pedidos novos → backlog" | Sem estrutura. P3 deu **DETERMINÍSTICO** e "ok + commit na base": nada disso está no texto de Review (plan:107-111); o "ok" é plan:25 (regra geral) e o commit é inferência de steering:61. Evidência com dado real: steering:14, `.kiro/local/` fora do git | commit **inferido**, não prescrito | I-git | NÃO ESPECIFICADO (commit da Review) — refuta o DETERMINÍSTICO da P3 |
| S10-F6 | `sprint-<nn>.md` — Retrospectiva, Números, `Situação: fechada`, `→ sprint <nn+1>` nas migradas (plan:115-122; arquivos:140-157) | Sim | seções do template | `→ sprint <nn+1>` vai em Fatias.Status, Especificação.Situação, Atendimento.Situação (arquivos:156-157): confere. **Ordem:** `fechada` é gravada (passo 3) antes do passo 5 (ELM) e do replanejamento; falha do ELM deixa a sprint fechada com `plannedFor` antigo; plan:83-84 (pendente) é só do modo sprint — confirma P3 | sem commit/ok/branch descritos (confirma P3) | I-git; I-elm sem regra para a virada | NÃO ESPECIFICADO (ordem/falha; commit) |
| S10-F6 | `<produto>/planejamento/equipe.json` — `projeto.historico[]` (plan:123) | Sim | JSON | Validado: entrada `{sprint, fatias-concluidas, pontos}` obrigatórias, `horas-lancadas` com 5 chaves, `reserva-atendimento` ∈ [0,1], `pontos` inteiro (15.5 falha). `reserva-atendimento` é razão (0.2) × acordos "20%" (conversão implícita). "velocidade" não é gravada (derivada). O estado da P3 (histórico 1–3 enquanto planeja a sprint 3, S10-F2) é aceito pelo schema mas contradiz "uma entrada por sprint fechada" (schema:31) — erro de cenário da P3 | sem commit | I-git | OK (estrutura) / NÃO ESPECIFICADO (commit) |
| S10-F6 | `acordos.md` — reserva recalibrada (plan:123) | Sim | linha `Reserva de atendimento` (arquivos:70) | Sem fórmula (P3 viu) | sem commit | I-git | NÃO ESPECIFICADO (fórmula, commit) |
| S10-F6 | `backlog.md` — `sprint` das migradas | Sim | — | plan:121 só muda o arquivo antigo. **Refinamento da P3:** se a fatia migra e entra na nova sprint pelo modo sprint (plan:124 "migradas consomem capacidade primeiro"), `sprint` é regravada no passo 7 (plan:81); só não é se a pessoa não der "ok" ou ficar de fora por capacidade | — | I-git | AMBÍGUO só parcialmente (a P3 exagerou) |
| S10-F6 | `sprint-<nn+1>.md` (modo sprint) | Sim | idem F2 | Linhas migradas (Tarefa ELM copiada de `[ESP]/[ATD]`) sem regra de cópia dos ids (migradas não são recriadas, elm:176-177) | idem F2 | I-git | NÃO ESPECIFICADO (cópia dos ids de tarefa) |
| S10-F3, S10-X1..X3 | — | — | — | — | — | — | sem escrita: F3 (acompanhamento; saída de fatia por estouro de reserva sem mecânica de gravação, plan:90-91), X1 (acordos parcial: SEM REGRA), X2 (pedido novo: CONFLITO plan:110-111 × sdd:22), X3 (recusa no encaixe: AMBÍGUO; se registrar `encaixe: fica para a próxima`, escreve em sprint-<nn>.md) |

---


## S11 · sdd-elm

### Parte 2 — Plano do fluxo esperado (Sonnet)


Observação sobre o recorte: a skill tem 9 modos; dois deles têm sub-fluxos com gatilhos e chamadores distintos, por isso aparecem em itens separados (**backlog** → F3 épico/Sustentação e F4 itens das fatias; **sprint** → F5 planos/tarefas e F6 virada; **horas** → F8 lançar e F9 relatório). Frases-gatilho da description (elm:3): "publica no ELM", "sobe o PRD para o DOORS", "cria os itens no EWM", "publica a sprint", "liga os testes", "fecha no ELM", "lança 4h", "relatório de horas".

Pré-condições comuns (elm:16-47): power `elm` + MCP `elm` na sessão (senão `ELM pendente: <modo> <alvo>` no Histórico do `status.md` ou rodapé do PRD); skills `elm`, `elm-rm`, `elm-ccm`, `elm-qm`, `elm-gc` carregadas antes das tools; `.kiro/config/power/elm/pa_*.json`; seção **ELM** do `sdd.md`; projeto sem ELM → nada a fazer. Regras de toda publicação (elm:27-47): (1) prévia `Ação | Alvo | Título | Tipo/Pasta` e **uma** confirmação para o lote; (2) idempotência (id no repositório → atualizar; sem id → procurar publicação interrompida → perguntar se é ele; senão criar); (3) conflito (`rm_list_modified` > `last_modified`) → mostrar os dois lados e perguntar; (4) gravar de volta no repositório a cada item + commit `<FT|EP> - Publicar no ELM`; (5) nomes legíveis, nunca `FR_`/`OT_`/uuid; (6) nunca apagar no ELM (roteiro manual). Saída padrão (elm:225-229): `🏛️ ELM — <modo> · <EP|FT|Sprint N>` · Criados/Atualizados/Sem mudança/Links/Conflitos · Pendências manuais.

#### S11-F1 · Modo similares (só leitura, antes de especificar)
- **Gatilho inicial:** evento de skill: chamado pela `sdd-prd` (S08-F1 passo 3.1), pela `sdd-triar` para a regra da ficha (triar:62, elm:51-52) e pelo modo *requisitos* antes de criar conceito novo (elm:96-99). Não pede confirmação (só lê).
- **Pré-condições / arquivos lidos:** lista de artefatos propostos (tipo HF|REG|GL, título provisório, 3–6 palavras-chave); bundle `<rm.download.path>` (steering:31); `pa_*.json`; MCP `elm` via `elm-rm`.
- **Processamento interno:**
  1. **Bundle:** busca de texto do Kiro pelo título e por cada palavra-chave; anotar a data do último sincronismo da `elm-sync`.
  2. **DOORS Next ao vivo** (`elm-rm`): uma `rm_search_requirements(text=…)` por palavra-chave e pelo título (**só `text`**: com `folder`/`requirement_type` junto devolve HTTP 400), filtrando pelos tipos do mapeamento; `rm_list_modified` desde o último sincronismo. Sem MCP → só bundle, saída `verificação no ELM ao vivo pendente`.
  3. **Ler e classificar** cada acerto: **igual** · **sobrepõe** · **relacionado** · acerto só por palavra em comum → descarta.
  4. **Saída:** tabela `Proposto | No ELM (id · título · tipo · pasta) | Relação | Recomendação`, com recomendação por relação (igual → reutilizar; sobrepõe → alterar; relacionado → criar novo citando o existente; nenhum → criar novo). A decisão é da pessoa; a `sdd-prd` registra.
- **Resultado final (output):** resposta: bloco `🔎 Similares no ELM — EP-nn · bundle de <data> · ao vivo: <sim|pendente>` + tabela. Arquivos: nenhum. ELM: só leitura. Handoff: volta para `sdd-prd` (ou `sdd-triar`) decidir e registrar.
- **Lacunas observadas:**
  - **Sem bundle** (`não há`, steering:31) não existe "data do último sincronismo" para o `rm_list_modified` (elm:61): a skill não diz que janela usar.
  - O bloco de saída é "por EP" (`EP-<nn>`), mas é chamado também para ficha de fatia sem épico e para um único conceito (elm:96-99): o cabeçalho não tem variante.
  - Sem limite de acertos a ler/classificar nem critério para quando 2+ acertos têm relações diferentes com o mesmo proposto.
  - `rm_get_requirement` está citado como leitura; a skill não diz qual skill do `elm-rm` consultar para pasta/tipo de acerto vindos de `rm_search_requirements`.

#### S11-F2 · Modo requisitos (conceitos OKF aprovados → DOORS Next)
- **Gatilho inicial:** "publica no ELM", "sobe o PRD para o DOORS" (elm:3). Eventos: handoff do GATE do PRD (prd:124-125, publicação `na-aprovacao`); `sdd-consolidar` Passo 2 (publicação `no-merge`, drift, ou regra da ficha; consolidar:39-45).
- **Pré-condições / arquivos lidos:** `<produto>/epicos/<EP>-<slug>/elm/` (ou `.kiro/specs/<ft>-<slug>/elm/` para a regra da ficha); só publica conceito `status: stable` com `verified` humano (`by: human:…`) **posterior** ao `generated.at`; o resto aparece na prévia como "aguardando aprovação" (elm:90-91); `pa_*.json` (`rm.requirements-types`, `rm.folders`); formato em `../sdd-prd/references/okf-elm.md`; `references/mapeamento.md`.
- **Processamento interno:** ordem **de baixo para cima**: termos (GL) → regras (REG) → histórias (HF). Para cada conceito:
  0. **Similares** (conceito novo, sem `resource`): coluna "No ELM" tem de ser `novo (verificado <data>)`; senão, ou se `rm_list_modified` mostra artefato do mesmo tipo criado depois, rodar S11-F1 só para ele. Acerto `igual`/`sobrepõe` → **não cria**, devolve à `sdd-prd` decidir; o resto do lote segue.
  1. Tipo e pasta: `type` → `rm.requirements-types`; `tags[0]` → `rm.folders`; não casou → perguntar uma vez (vale para o lote).
  2. Texto: corpo sem `## Relações`; links relativos trocados — para regra já publicada → embed `[<id>](<id>)` + id em `embedded`; termo publicado → hyperlink; conceito sem id → só o título; link do bundle/URL do ELM como está. Markdown direto.
  3. Criar (sem `resource`): `rm_create_requirement(type, pasta, title, text, embedded)`; Atualizar (com `id`): conferir conflito (regra 3), mostrar diff do corpo, `rm_update_requirement(id, title, text, embedded)` com texto inteiro.
  4. Gravar de volta: `resource`, `id`, entrada `{ id: elm, resource, last_modified }` em `sources`, `**Publication**` no `log.md`; termos também na coluna ELM do glossário.
  - Prévia + **uma** confirmação do lote antes de escrever (regra 1). Atributos e links requisito↔requisito ficam só nos conceitos (roteiro manual se o projeto exigir — mapeamento:56-63). Publicar **não** muda o status do PRD.
- **Resultado final (output):** resposta: prévia + saída padrão (Criados/Atualizados/Sem mudança/Links/Conflitos/Pendências). Arquivos: `elm/*.md` (`resource`, `id`, `sources`), `elm/log.md`, glossário do projeto (coluna ELM); commit na base `<FT|EP> - Publicar no ELM`. ELM: GL/REG/HF criados/atualizados no DOORS Next. Handoff: sugerir `elm-sync` (o bundle passa a ser a versão viva; `elm/` fica como registro).
- **Lacunas observadas:**
  - **HF publicada sem sua REG embutida:** elm:96-106 só publica `stable`+`verified`; se a REG citada está "aguardando aprovação" (ainda sem id), o texto da HF vira "só o título como texto" (elm:105) — publica-se a HF sem embed silenciosamente. Falta regra de bloquear/adiar a HF até a REG ter id (a ordem GL→REG→HF só garante isso para o que está no mesmo lote).
  - **Devolução a `sdd-prd` para ficha:** elm:98-99 manda devolver `igual`/`sobrepõe` à `sdd-prd`; no caso da regra da ficha (fatia sem épico, elm:87-89) não há PRD — o dono da decisão seria `sdd-triar`/`sdd-consolidar`.
  - **Link "rastreia" (épico → histórias)** prometido em mapeamento:33 ("publicação do épico") e em elm:130 ("quando publicadas"): nenhum passo do modo requisitos (nem do backlog) o cria depois que as HF ganham id — a ordem natural (épico nasce antes, elm:126) torna o link impossível na criação.
  - **Mensagem de commit:** elm:42 `<FT|EP> - Publicar no ELM` × padrão de commit configurável do projeto (steering:59, ex. `FT-<nnn> <verbo> <descrição>` / `Task <id> - …`).
  - Glossário: "o id também na coluna ELM do glossário" (elm:112-113) sem formato nem caminho de edição definidos nesta skill (steering:30 só dá o caminho).
  - Tool de listagem para conflito: `rm_list_modified` é citado, mas não há instrução de como obter `last_modified` quando o conceito nunca foi publicado por esta skill (copiado do bundle numa "Alteração": okf:59,143 cobre).

#### S11-F3 · Modo backlog — épico, Sustentação e Atendimento
- **Gatilho inicial:** evento: `sdd-triar` ao registrar o `EP-nn` (triar:78-82; elm:126); `sdd-prd` Passo 1.4 se o épico ficou `pendente` (prd:43); `sdd-planejamento` quando o épico tem `elm` `—`/`pendente` (elm:160); primeira necessidade de pai de Sustentação (elm:133). Frase: "cria os itens no EWM" (elm:3).
- **Pré-condições / arquivos lidos:** linha do épico no `backlog.md`; tipo de épico do `sdd.md` (steering:76: pode ser "Item de Backlog pai"); linha `Sustentação:` do `backlog.md` (vazia → criar); item de origem no EWM se houver.
- **Processamento interno:** ordem obrigatória épico → IB → tarefa; `Planejado para` obrigatório em IB e tarefa.
  1. **Épico:** título `[EP-03] <título>`, descrição = problema (e, depois do GATE, solução do PRD + link do PRD); links **rastreia** → histórias, quando publicadas. Épico que nasce de item do EWM: se o item já é do tipo épico, ele é o épico; senão o item vira filho do épico novo (`ccm_update_workitem(id, parent=<épico>)`).
  2. **Sustentação e Atendimento** (uma vez por release/ano, se a linha `Sustentação:` estiver vazia): épico `[SUS-<ano>] Sustentação` e, filho dele, o IB `Atendimento` (pai das `[ATD]`); ids na linha `Sustentação:`.
  3. Prévia + confirmação (regras 1–4); gravar `elm` na linha do épico/`Sustentação:` do `backlog.md` (na base).
- **Resultado final (output):** resposta: saída padrão. Arquivos: `backlog.md` (coluna `elm` do épico; linha `Sustentação:`); commit. ELM: épico `[EP-nn]`, opcionalmente `[SUS-<ano>]` e IB `Atendimento`. Handoff: S11-F4 depois do GATE do backlog.
- **Lacunas observadas:**
  - **Atualização depois do GATE** ("e, depois do GATE, solução do PRD + link do PRD", elm:130): nenhuma skill chama este modo para essa atualização (ver S08-F2).
  - **"rastreia"**: sem passo que o grave (ver S11-F2).
  - mapeamento:13 atribui a criação ao `sdd-prd` (desatualizado frente a triar:78).
  - `Planejado para` obrigatório (elm:123) para o épico criado cedo (na triagem, sem sprint): a skill diz "use sempre a iteração que a pessoa indicar" — para épico/IB de backlog do produto, fatiar:88-89 diz "a da entrega ou release"; fora de fatiar não há orientação.
  - Quem cria a linha `Sustentação:` quando o primeiro atendimento chega antes de qualquer épico/fatia (S11-F7 abre `[ATD]` sob "Atendimento" — elm:182 — sem mandar executar este passo 2 antes).

#### S11-F4 · Modo backlog — itens de backlog (IB) das fatias, e fatia dividida
- **Gatilho inicial:** handoff de `sdd-fatiar` Passo 4 (fatiar:87-89); `sdd-triar` para fatia sem épico quando `backlog no EWM` = `ao-fatiar` (triar:95-97); `sdd-planejamento`/S11-F5 passo 2 ("fatias sem IB" → modo backlog primeiro, elm:160). Frase: "cria os itens no EWM", "criar os itens de backlog".
- **Pré-condições / arquivos lidos:** `backlog.md` (fatias e `cobre`), PRD (cenários Dado/Quando/Então; fatia sem épico: ficha), `sdd.md` (`backlog no EWM`, tabela de pontos, linha "Critérios de aceite no IB", "Fatia dividida no EWM"), ids de HF publicadas, IBs das fatias em `bloqueada-por`.
- **Processamento interno:**
  1. Disparo conforme `backlog no EWM`: `ao-fatiar` (logo após o GATE do backlog; fatia sem épico: ao registrar na triagem) ou `na-sprint` (o planejamento cria).
  2. Título `[FT-031] <título>`; `parent` = épico (fatia sem épico sem item de origem → épico de Sustentação; com item de origem → **não há IB novo**; direta → sem IB); pontos pelo tamanho (tabela do `sdd.md`); descrição com modo AFK/HITL, `bloqueada por`, pasta prevista; responsável = P.O.
  3. **Critérios de aceite:** cenários que a fatia cobre em Dado/Quando/Então copiados do PRD (ficha, se sem épico), no campo da linha "Critérios de aceite no IB" (Markdown), ou na seção "Critérios de aceite" da descrição; com aviso "gerado do PRD — não edite aqui"; atualizar quando a fatia for refinada ou a `sdd-consolidar` registrar mudança as-built.
  4. **Links:** **implementa** → cada história coberta; **depende de** → IBs das fatias em `bloqueada-por` (se `link-types` tiver; senão na descrição) — conferir links existentes antes (mapeamento:41-42).
  5. **Fatia dividida:** conforme "Fatia dividida no EWM": IBs novos filhos do IB original (que segue filho do épico) **ou** fecha o original e cria novos; pai errado → `ccm_update_workitem(id, parent=<novo pai>)`.
  6. Prévia + confirmação; gravar `elm` de cada fatia no `backlog.md` (base); commit.
- **Resultado final (output):** resposta: saída padrão. Arquivos: `backlog.md` (coluna `elm` com `[<id>](<url>)`). ELM: um IB por fatia com pontos, critérios, links implementa/depende de. Handoff: `sdd-planejamento` (encaixar na sprint) ou `sdd-iniciar`.
- **Lacunas observadas:**
  - **"implementa" com HF sem id** (publicação `no-merge`): sem regra de adiamento/retomada do link (ver S09-F1).
  - **Conflito fatiar:87 × elm:135** sobre quando o IB é criado (ver S09-F1).
  - **Fatia dividida em andamento:** só IBs são tratados; tarefas `[DEV][REV][VER]` da original não (ver S09-F2).
  - **Cancelamento por junção** (fatiar:99) não tem tratamento aqui (e elm:46 proíbe apagar).
  - Atualização do campo "gerado do PRD" quando o PRD muda (S08-F3) não tem gatilho definido.
  - Fatia sem épico **com** item de origem: "não há IB novo" (elm:138) — então "implementa" e critérios de aceite vão para onde? (o item de origem pode ser DF, não IB).

#### S11-F5 · Modo sprint — planos, IBs e tarefas na iteração
- **Gatilho inicial:** "publica a sprint" (elm:3). Evento: `sdd-planejamento` **sempre** depois do "ok" da sprint (plan:81-84; elm:152); encaixe (plan:101-104); `sdd-iniciar` Passo 4.4 quando a tarefa não existe (encaixe aprovado agora, Kanban, publicação que falhou; iniciar:103-114); `sdd-loop` (loop:29).
- **Pré-condições / arquivos lidos:** número da sprint, iteração, time e as três seções do `sprint-<nn>.md` (fatias com responsável/revisor/verificador; especificação; reserva); `pa_*.json` (iterations, `workitem-types`, classificação, timesheet); linha "Tarefas" e "Classificação da tarefa" do `sdd.md`.
- **Processamento interno:**
  1. **Planos** por iteração e time: plano de backlog (`com.ibm.team.apt.plantype.product.backlog`) e plano da sprint (`…plantype.default`); faltou algum (ou a iteração) → criar pela `elm-setup` (`ccm_create_iteration` / `ccm_create_iteration_plan`; exige permissão de modificar iterações — se falhar, pedir a quem administra a PA).
  2. Fatias sem IB e épicos com `elm` `pendente`/`—` → S11-F3/S11-F4 **primeiro** (a `[ESP]` nunca nasce sem pai); para cada IB da sprint: `plannedFor` = iteração (responsável continua o P.O.).
  3. **Tarefas** (títulos da linha "Tarefas"; responsável, estimativa em horas, `plannedFor`): `[ESP] EP-05 Especificação` (pai = épico, responsável = quem especifica); `[DEV] FT-031 Implementar` (responsável da fatia, pai IB); `[REV] FT-031 Revisar` (revisor); `[VER] FT-031 Verificar` (verificador). Fatia sem épico com item de origem → pai = o item (sem IB novo); direta → só `[DEV] FT-nnn <pedido>`, pai = item de origem ou Sustentação. Campos obrigatórios da Tarefa (categoria de horas, OTR, classificação, Clarity) pela `elm-ccm` (Criar) e linha "Classificação da tarefa".
  4. Gravar ids na coluna "Tarefa ELM" do `sprint-<nn>.md` e no `elm` do `backlog.md`.
  - Prévia + confirmação (regras 1–4).
- **Resultado final (output):** resposta: saída padrão (Criados/Atualizados/…). Arquivos: `sprint-<nn>.md` (Tarefa ELM), `backlog.md` (`elm`); commit na base. Quando chamado da branch da fatia (iniciar:112-114): **não** grava `backlog.md` nem `sprint-<nn>.md`; ids no `status.md` (a `sdd-consolidar` os leva ao backlog). ELM: planos, IBs com `plannedFor`, tarefas. Pendência → `pendente` na coluna e publica depois.
- **Lacunas observadas:**
  - **Contradição na gravação dos ids:** elm:174-175 manda gravar no `sprint-<nn>.md` e `backlog.md` incondicionalmente; iniciar:112-114 manda **não** gravar quando chamada da branch da fatia. A skill não conhece essa exceção (e o "Entrada" de elm:152 descreve só o chamador `sdd-planejamento`).
  - **Origem da "estimativa em horas"** de `[DEV]/[REV]/[VER]` (ver S10-F2).
  - **Kanban:** iniciar:75-76 diz que o modo põe tarefas "na iteração corrente do EWM"; elm:152-160 só descreve a entrada com sprint e iteração informadas.
  - Falha parcial: regra 4 (rodar de novo retoma) cobre IBs/tarefas, mas não diz como lidar com plano/iteração criados e tarefas parciais.
  - Fatia direta sem item de origem: o pai é o épico de Sustentação (elm:172-173), mas esse épico pode não existir (precisa de S11-F3 passo 2 antes; não é citado aqui).

#### S11-F6 · Modo sprint — virada (migrar para a nova iteração)
- **Gatilho inicial:** `sdd-planejamento` na virada, passo 5 (plan:125-126); frases "virada de sprint", "fechar a sprint" (plan:3).
- **Pré-condições / arquivos lidos:** `sprint-<nn>.md` (fechada) e a nova iteração; tarefas não concluídas (inclusive `[ESP]` e `[ATD]`) e IBs não concluídos no EWM.
- **Processamento interno:** tarefas e IBs não concluídos → **só o `plannedFor`** muda para a nova iteração (o pai não muda; move, nunca recria); as novas são publicadas (S11-F5); roteiro manual de **baseline** (componente RM + GC) se o projeto exige baseline por sprint (mapeamento:62). Prévia + confirmação.
- **Resultado final (output):** resposta: saída padrão + roteiro manual de baseline se aplicável. Arquivos: `sprint-<nn+1>.md`/`backlog.md` conforme S11-F5. ELM: `plannedFor` atualizado (move). Handoff: volta ao `sdd-planejamento`.
- **Lacunas observadas:**
  - A skill assume que a nova iteração já existe; se não existe vale o passo 1 do S11-F5 (criar pela `elm-setup`), mas não é remetido aqui.
  - Quem "marca" as tarefas como migradas no `sprint-<nn>.md` antigo é o planejamento (plan:121), não a skill; e a `elm` coluna "Tarefa ELM" do novo arquivo não é mencionada.
  - IB não concluído com tarefas concluídas parcialmente: não distingue quais tarefas migram (todas "não concluídas").

#### S11-F7 · Modo atendimento (abrir e concluir `[ATD]`)
- **Gatilho inicial:** evento: `sdd-atender` (atender:35-37 abrir; atender:55-56 concluir); no `sdd.md`/README, "atendimento" (sdd/SKILL:31).
- **Pré-condições / arquivos lidos:** linha `Sustentação:` do `backlog.md` (IB "Atendimento"), iteração da sprint aberta (do `sprint-<nn>.md`) ou a indicada, `AT-<nnn>` e responsável.
- **Processamento interno:**
  - **Abrir:** `[ATD] AT-<nnn> <título>`, filha do IB "Atendimento", `plannedFor` = iteração da sprint aberta (ou a que a pessoa indicar), responsável = quem atende, estimativa, estado em andamento. Prévia + confirmação.
  - **Concluir:** depois do lançamento das horas (S11-F8), estado de conclusão da PA.
- **Resultado final (output):** resposta: saída padrão. Arquivos: nenhum próprio (`atender` grava o `AT-<nnn>-<slug>.md`, a linha no README de atendimentos e no `sprint-<nn>.md`). ELM: tarefa `[ATD]` criada/concluída. Handoff: de volta à `sdd-atender`.
- **Lacunas observadas:**
  - **Quem conclui a `[ATD]`:** elm:184 ("Concluir: depois das horas, estado de conclusão"), elm:194-195 ("lançar não conclui; concluir é do modo conclusão ou da skill que chamou") e atender:55 ("modo horas lança e conclui a tarefa") — três formulações; o modo conclusão (elm:218-221) só lista fatia/épico.
  - **IB "Atendimento" pode não existir:** elm:133-134 cria Sustentação/Atendimento "se a linha estiver vazia", mas o modo atendimento não manda executar esse passo antes de abrir a `[ATD]`.
  - **Sem sprint aberta** (Kanban ou antes do 1º planejamento): `plannedFor` não tem fonte além de "a que a pessoa indicar".

#### S11-F8 · Modo horas — lançar
- **Gatilho inicial:** "lança 4h", "lança 6h de ontem" (elm:3, elm:188-189). Evento: chamado na conclusão de uma tarefa por `sdd-fatiar` (`[ESP]`, fatiar:80-83), `sdd-verificar` (`[VER]`, verificar:76-79), `sdd-consolidar` (`[DEV]`, `[REV]`, consolidar:46-50), `sdd-atender` (`[ATD]`, atender:55), `sdd-loop` (loop:118).
- **Pré-condições / arquivos lidos:** tarefa (informada; senão a atual: `status.md` da branch dá a `[DEV]/[REV]/[VER]` do papel de quem pede; AT aberto dá a `[ATD]`; a `[ESP]` vem do `sprint-<nn>.md`); `pa_*.json` (time code, work type de `timesheet`); `ccm_list_timesheet`.
- **Processamento interno:**
  1. Identificar a tarefa; dúvida → perguntar.
  2. Listar as horas já lançadas (`ccm_list_timesheet`) → mostrar e **descontar**; uma linha por data; data futura não.
  3. Regras do EWM: só o responsável lança; máximo 16 h por dia; time code/work type do `pa_*.json`; confirmar e `ccm_add_timesheet`. **Lançar não conclui** a tarefa (tarefa de vários dias).
  4. Sem MCP ou com falha → `ELM pendente: lançar <h>h em <tarefa> (<data>)` no `status.md`, no registro do AT ou no `sprint-<nn>.md`; este modo lança depois.
- **Resultado final (output):** resposta: saída padrão (horas lançadas, restante). Arquivos: nenhum (ou a pendência nos arquivos citados). ELM: linhas de timesheet. Handoff: modo conclusão ou a skill chamadora conclui a tarefa.
- **Lacunas observadas:**
  - Tarefa de **outra pessoa** (o EWM só aceita o responsável): tratada em consolidar:49-50 (pendência com login) e não aqui; este modo diz só "só o responsável lança".
  - "Lançar depois" (elm:197): o gatilho para retomar pendências é de `sdd-status` (consolidar:51-52), não citado aqui.
  - Parsing de data relativa ("de ontem") sem regra de fuso/dia útil.

#### S11-F9 · Modo horas — relatório
- **Gatilho inicial:** "relatório de horas" (elm:3); evento: virada da sprint (plan:118-119).
- **Pré-condições / arquivos lidos:** tarefas da sprint (`sprint-<nn>.md`, coluna "Tarefa ELM"), `ccm_list_timesheet`.
- **Processamento interno:** horas por tipo (`[ESP] [DEV] [REV] [VER] [ATD]`) e por pessoa, planejadas × lançadas, e as tarefas concluídas **sem horas** (só no fechamento). Alimenta a retrospectiva e a recalibração da reserva.
- **Resultado final (output):** resposta: tabela por tipo e por pessoa; lista de tarefas sem horas. Arquivos: nenhum (o planejamento preenche "Números" e `historico[].horas-lancadas`, arquivos:51-52, 144-153). ELM: leitura.
- **Lacunas observadas:**
  - "Planejadas" depende das estimativas das tarefas (origem não definida, ver S10-F2).
  - Relatório "sob pedido" fora da virada: o "só no fechamento" para tarefas sem horas fica ambíguo (o que listar em relatório intermediário).
  - Tarefas sem `Tarefa ELM` registrado (pendentes) ficam fora do relatório sem aviso.

#### S11-F10 · Modo testes (CT.csv → ETM → links)
- **Gatilho inicial:** "liga os testes" (elm:3). Evento: `sdd-consolidar` Passo 2, "testes" (consolidar:44-45); `sdd-verificar` gera o `CT.csv` no ACEITO e adia a importação para a consolidação (verificar:88-90).
- **Pré-condições / arquivos lidos:** `CT.csv` na pasta da fatia (`.kiro/specs/<ft>-<slug>/`, formato em `sdd-verificar/references/ct-csv.md`); `verificacao.md`, `status.md`; `elm-qm`/`elm-gc`; ids das HF e do IB.
- **Processamento interno:**
  1. Entregar o caminho do `CT.csv`: "Importe no ETM (Importar → CSV)"; perguntar os ids criados (o MCP não cria caso de teste).
  2. Com os ids: ler cada caso pela `elm-qm` (`get_testartifact`) para obter a URL; ligar **valida** (CT → história coberta pelo cenário) e **testado por** (IB → CT); `gc_context` se o ETM usar configuração global (`elm-gc`).
  3. Registrar os ids no `verificacao.md` e no `status.md`.
- **Resultado final (output):** resposta: instrução de importação e depois saída padrão (Links: n). Arquivos: `verificacao.md`, `status.md`. ELM: links valida/testado por. Pendência manual: importar o `CT.csv` (mapeamento:63).
- **Lacunas observadas:**
  - **Pausa sem retomada definida:** o fluxo depende de a pessoa importar e voltar com os ids; não há registro `ELM pendente: importar CT.csv` explícito nem gatilho de retomada (mapeamento:54 fala da pendência em geral).
  - **Fatia sem épico/sem HF:** "valida" é CT → **História** (mapeamento:35; elm:206); fatia padrão sem épico tem só regra/ficha (e a direta/rápida nem isso) — o que ligar não é dito. "testado por" exige IB (inexistente para fatia com item de origem, elm:138).
  - Antes de ligar, listar os links existentes (mapeamento:41-42) não consta no passo do SKILL.
  - Regra 1 (prévia e confirmação) vale, mas o passo 2 não a menciona.

#### S11-F11 · Modo especificação técnica (ET as-built, opcional)
- **Gatilho inicial:** evento: `sdd-consolidar` Passo 2 "especificação técnica" (consolidar:43-45), só se a linha ET da seção ELM do `sdd.md` = `as-built no merge` (elm:213; steering:72).
- **Pré-condições / arquivos lidos:** `design.md` e o **código final** da fatia; tipo ET em `pa_*.json`/steering:75; `okf-elm.md`.
- **Processamento interno:** gerar `ET - FT-031 <título>` (interfaces, contratos, dados, integrações, decisões técnicas — nada do que não foi feito); gravar como conceito OKF em `.kiro/specs/<ft>-<slug>/elm/ET-<slug>.md` (`type` = tipo de ET do projeto); **mostrar**; publicar como os requisitos (S11-F2) **depois do `verified` humano**; ligar ao IB (**implementa**).
- **Resultado final (output):** resposta: o conceito mostrado + saída padrão. Arquivos: `.kiro/specs/<ft>-<slug>/elm/ET-<slug>.md` (+ `index.md`/`log.md` da pasta). ELM: artefato ET no DOORS Next + link com o IB.
- **Lacunas observadas:**
  - **Quem dá o `verified` humano na ET** (não há GATE de PRD aqui): a skill diz "depois do `verified` humano" sem dizer quem, quando, nem como o agente o grava.
  - **Ligação ao IB:** fatia sem épico com item de origem ou direta não tem IB (elm:138, 172); "ligue ao IB" fica sem alvo.
  - Nada diz o que fazer se a ET já existe (re-consolidação / mudança): aplicam-se as regras de atualização de S11-F2, mas não é remetido.
  - Mapeamento:24 coloca o ET na consolidação; elm:213 diz "só se ET = as-built no merge" — coerente, mas o tipo `Especificação Técnica` é "padrão" no mapeamento, enquanto steering:75 traz ET como `<… | —>`.

#### S11-F12 · Modo conclusão
- **Gatilho inicial:** "fecha no ELM" (elm:3). Evento: `sdd-consolidar` ("backlog — concluir as tarefas e o IB da fatia", consolidar:53-55); `sdd-fatiar` para a `[ESP]` (fatiar:81); `sdd-verificar` para a `[VER]` (verificar:77-78); `sdd-atender` para a `[ATD]` (atender:55).
- **Pré-condições / arquivos lidos:** horas já lançadas (S11-F8) em cada tarefa; `ccm_list_workitem_states` (estado de conclusão da PA); ids em `backlog.md`/`status.md`.
- **Processamento interno:** tarefas e IB da fatia → estado de conclusão da PA, **depois** das horas de cada tarefa; épico quando todas as fatias concluírem; comentário opcional no IB com PR, pasta e ids publicados. Prévia + confirmação.
- **Resultado final (output):** resposta: saída padrão. Arquivos: nenhum próprio. ELM: tarefas/IB/épico no estado concluído; comentário opcional. Handoff: volta à skill chamadora.
- **Lacunas observadas:**
  - **Escopo incompleto:** elm:220-221 só lista "tarefas e IB da fatia" e "épico"; os chamadores concluem também `[ESP]` (fatiar:81), `[VER]` (verificar:77), `[ATD]` (atender:55) e, na fatia sem épico com item de origem, o próprio item de origem — nenhum está no texto do modo.
  - **Épico no EWM sem gatilho:** consolidar:79 marca o épico `concluido` apenas no PRD e no backlog local; consolidar:53-55 só pede a conclusão de tarefas e IB — ninguém chama este modo para o épico.
  - Tarefa concluída sem horas não trava (consolidar:53-55), mas este modo não mostra aviso.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


```text
S11-F1 · Modo similares (só leitura, antes de especificar)
1. INPUT EXATO (chamada da sdd-prd, prd:57-59): "similares do EP-03: HF-01 'Bloquear conta após 3 tentativas' (login, tentativas, bloqueio); REG-01 'Limite de tentativas' (tentativas, 3, 15 minutos); GL-tentativa-de-login"
   ESTADO: bundle em docs/elm/pa_x, sincronismo 2026-10-10. MCP elm: sim. elm/ sem conceitos ainda.
2. REGRA APLICADA:
   - SE chamada da sdd-prd antes de criar HF/REG/GL → modo similares — fonte: elm:51-53
   - ENTÃO só lê; não pede confirmação — fonte: elm:54
   - ENTÃO busca no bundle por título e por cada palavra; anotar data do sincronismo — fonte: elm:57-58
   - ENTÃO DOORS Next ao vivo: rm_search_requirements(text=…) por palavra e por título (só text); filtrar pelos tipos; rm_list_modified desde 2026-10-10 — fonte: elm:59-62
   - ENTÃO classificar cada acerto: igual / sobrepõe / relacionado; "acerto só por palavra em comum" → descarta — fonte: elm:64-68
   - ENTÃO saída: um bloco por artefato proposto — fonte: elm:69-78
   - ENTÃO recomendação por relação: igual → reutilizar; sobrepõe → alterar; relacionado → criar novo citando; nenhum → criar — fonte: elm:80-83
3. OUTPUT GERADO (elm:72-78, cabeçalho EP-03):
   🔎 Similares no ELM — EP-03 · bundle de 2026-10-10 · ao vivo: sim
   | Proposto | No ELM (id · título · tipo · pasta) | Relação | Recomendação |
   [uma linha por acerto, com recomendação]
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma (só leitura).
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S11-F2 · Modo requisitos (conceitos OKF aprovados → DOORS Next)
1. INPUT EXATO: "publica no ELM o EP-03"
   ESTADO: epicos/EP-03/elm/: GL-tentativa-de-login (stable, verified humano 2026-10-15 > generated 2026-10-14); REG-01 (stable + verified); HF-01 (stable + verified; cita REG-01 e GL); HF-02 (draft, sem verified). Na tabela do PRD: REG-01, HF-01 e GL com "novo (verificado …)". Publicação na-aprovacao. pa_*.json com types e folders mapeados.
2. REGRA APLICADA:
   - SE "publica no ELM" → modo requisitos — fonte: elm:3, elm:85-91
   - SE conceito não é stable com verified humano posterior ao generated.at → "aguardando aprovação" na prévia (não publica) — fonte: elm:89-91 → HF-02 fica de fora
   - ENTÃO ordem de baixo para cima: GL → REG → HF — fonte: elm:93
   - ENTÃO (passo 0) conceito sem resource: coluna "No ELM" = "novo (verificado …)" → não rodar similares de novo — fonte: elm:96-99
   - ENTÃO (passo 1) tipo e pasta por pa_*.json (type → rm.requirements-types; tags[0] → rm.folders) — fonte: elm:100-101
   - ENTÃO (passo 2) texto: HF → REG = embed [<id>](<id>) com o id em embedded (REG já criada no lote) — fonte: elm:102-107; okf:94
   - ENTÃO (passo 3) rm_create_requirement(type, pasta, title, text, embedded) — fonte: elm:108
   - ENTÃO (passo 4) gravar resource, id, entrada de sources e linha **Publication** no log.md — fonte: elm:111-113
   - SEM REGRA (sub): "id também na coluna ELM do glossário" — formato e caminho de edição não definidos (elm:112-113; steering:30 só dá o caminho)
   - ENTÃO prévia + uma confirmação para o lote — fonte: elm:27-30
   - CONFLITO: commit "<FT|EP> - Publicar no ELM" (elm:42) × padrão do steering "FT-<nnn> <verbo> <descrição>" (steering:59)
   - ENTÃO sugerir elm-sync ao final — fonte: elm:117-118
   - Publicar não muda status do PRD — fonte: elm:91
3. OUTPUT GERADO: prévia (Ação | Alvo | Título | Tipo/Pasta) com criar GL, REG-01, HF-01 e "aguardando aprovação: HF-02". Após "sim": saída padrão (elm:225-229):
   🏛️ ELM — requisitos · EP-03
   Criados: 3 · Atualizados: 0 · Sem mudança: 0 · Links: n · Conflitos: 0
   Pendências manuais: HF-02 aguardando aprovação
   ARQUIVOS ESCRITOS: elm/*.md (resource, id, sources) · elm/log.md (Publication) · glossário (coluna ELM) · commit na base (mensagem: CONFLITO).
   ESCRITA NO ELM: criar GL, REG-01, HF-01 no DOORS Next (após "sim").
4. VEREDITO MECÂNICO: CONFLITO (elm:42 `<FT|EP> - Publicar no ELM` × steering:59 `FT-<nnn> <verbo> <descrição>` — dois padrões de mensagem para o mesmo commit).
```

```text
S11-F3 · Modo backlog — épico (e Sustentação)
1. INPUT EXATO (evento bruto de sdd-triar): "registrado EP-04 'Bloqueio de conta por inatividade' — rascunho, prd `—`, elm `—`; tipo de épico no steering = Épico; linha Sustentação: `—`"
   ESTADO: MCP sim. No EWM não existe [SUS-2026] Sustentação nem IB Atendimento.
2. REGRA APLICADA:
   - SE sdd-triar registra EP-nn com ELM → modo backlog, só o épico — fonte: triar:78; prd:43 (só o épico)
   - ENTÃO passo 1: título `[EP-04] <título>`, tipo do steering, descrição = problema — fonte: elm:126-130
   - ENTÃO passo 2: SE a linha Sustentação estiver vazia → criar épico [SUS-<ano>] Sustentação e IB Atendimento filho dele — fonte: elm:133-134 (passo do modo backlog)
   - CONFLITO: triar:78 e prd:43 pedem "só o épico"; elm:133-134 cria Sustentação e Atendimento dentro do mesmo modo quando a linha está vazia.
   - ENTÃO prévia + confirmação (regras 1-4); gravar elm do épico no backlog.md — fonte: elm:27-30; elm:148
   - SEM REGRA (nota): o plano diz que "Planejado para" é obrigatório no épico (elm:123). O texto exige só em IB e tarefa (elm:123: "obrigatório em IB e tarefa"). A lacuna do plano não existe no texto.
   - SEM REGRA (sub): link "rastreia" épico → histórias "quando publicadas" (elm:130; mapeamento:33) — nenhum passo o cria depois (ver S11-F2)
3. OUTPUT GERADO: prévia: criar [EP-04] (e, pelo passo 2, [SUS-2026] Sustentação + IB Atendimento — conflito). Após "sim": saída padrão.
   ARQUIVOS ESCRITOS: backlog.md (elm do EP-04; linha Sustentação se criada) · commit (mesmo padrão de mensagem de S11-F2).
   ESCRITA NO ELM: épico [EP-04] (e, pelo passo 2, SUS e Atendimento) após "sim".
4. VEREDITO MECÂNICO: CONFLITO (triar:78 e prd:43 "só o épico" × elm:133-134, que cria Sustentação/Atendimento no mesmo modo).
```

```text
S11-F4 · Modo backlog — itens de backlog (IB) das fatias
1. INPUT EXATO (evento de sdd-fatiar, passo 4, após GATE do backlog): "GATE do backlog do EP-03 aprovado: FT-031 (cobre HF-01#1.1, HF-01#1.2, REG-01; M; AFK) e FT-032 (cobre HF-01#1.3, REG-02; P; AFK; bloqueada-por FT-031)"
   ESTADO: EP-03 elm 612001. HF-01 publicada (id 2034). REG-01 (id 2101) e REG-02 (id 2102) publicadas. Campo "Critérios de aceite" no IB. link-types sem "depende de" (vai para a descrição). backlog no EWM = ao-fatiar. Pontos M=3, P=2.
2. REGRA APLICADA:
   - SE fatiar passo 4 e backlog no EWM = ao-fatiar → criar IB agora — fonte: elm:135; fatiar:87-89
   - ENTÃO título `[FT-031] <título>`; parent = épico 612001 — fonte: elm:137
   - ENTÃO pontos = tabela do steering (M = 3) — fonte: elm:137-138; steering:77
   - ENTÃO descrição com AFK/HITL, bloqueada por, pasta prevista; responsável = P.O. — fonte: elm:139
   - ENTÃO critérios de aceite: cenários cobertos em Dado/Quando/Então, copiados do PRD, no campo "Critérios de aceite" com aviso "gerado do PRD" — fonte: elm:139-143; steering:77
   - ENTÃO links: implementa → HF-01 (2034) — fonte: elm:144; mapeamento:32
   - ENTÃO depende de → sem link-type → texto na descrição — fonte: elm:145
   - ENTÃO prévia + confirmação — fonte: elm:27-30
   - ENTÃO gravar `elm` de cada fatia no backlog.md como [<id>](<url>) — fonte: elm:148; backlog.md:53
   - CONFLITO: commit "<FT|EP> - Publicar no ELM" (elm:42) × padrão do steering `FT-<nnn> <verbo> <descrição>` (steering:59)
3. OUTPUT GERADO: saída padrão: 🏛️ ELM — backlog · EP-03 · Criados: 2 · Links: 2 (implementa) · Pendências manuais: nenhuma.
   ARQUIVOS ESCRITOS: backlog.md (elm de FT-031 e FT-032) · commit (mensagem: CONFLITO).
   ESCRITA NO ELM: IB [FT-031] e [FT-032] com pontos, critérios e links implementa (após "sim").
4. VEREDITO MECÂNICO: CONFLITO (elm:42 × steering:59, mensagem de commit). Sem outras regras em conflito no caso.
```

```text
S11-F5 · Modo sprint — planos, IBs e tarefas na iteração
1. INPUT EXATO (evento de sdd-planejamento, após "ok" da sprint): "publica a sprint 3"
   ESTADO: sprint-003.md com FT-031 (joao.lima / ana.souza / ana.souza) e EP-05 [ESP] (rita.melo, 16 h, Situação PRD, Tarefa ELM `pendente`). EP-05 elm `—`. Iteração "Sprint 3" existe. Plano de backlog existe; plano da sprint não existe. IB de FT-031 existe (612002).
2. REGRA APLICADA:
   - SE "publica a sprint" / chamada da sdd-planejamento → modo sprint — fonte: elm:3; elm:152
   - ENTÃO passo 1: se faltar plano (ou a iteração) → criar pela elm-setup (ccm_create_iteration_plan); se falhar, pedir a quem administra a PA — fonte: elm:155-159 (elm-setup, delegado)
   - ENTÃO passo 2: épico com elm `—` → modo backlog primeiro (S11-F3) — fonte: elm:160
   - ENTÃO passo 2: para cada IB da sprint: plannedFor = iteração — fonte: elm:160-161
   - ENTÃO passo 3: tarefas [ESP] (pai épico), [DEV], [REV], [VER] (pai IB) — fonte: elm:162-170
   - ENTÃO [ESP] EP-05: horas previstas 16 (sprint-003.md) — fonte: elm:162
   - SEM REGRA: estimativa em horas de [DEV], [REV] e [VER]. elm:162 exige "estimativa em horas", mas nenhuma regra (nem plan:73-78) diz de onde ela vem.
   - ENTÃO campos obrigatórios (categoria de horas, OTR, classificação, Clarity) pela elm-ccm e steering:79 — fonte: elm:172-174 (delegado)
   - ENTÃO passo 4: gravar ids na coluna Tarefa ELM de sprint-003.md e no elm do backlog.md — fonte: elm:174-175
   - ENTÃO prévia + confirmação — fonte: elm:27-30
   - SEM REGRA (sub): commit com `<FT|EP> - Publicar no ELM` (elm:42) não cobre a sprint
3. OUTPUT GERADO: prévia: planos (se faltarem), IBs com plannedFor Sprint 3, 5 tarefas [ESP]/[DEV]/[REV]/[VER] com estimativa "—" (sem regra). Após "sim": saída padrão.
   ARQUIVOS ESCRITOS: sprint-003.md (coluna Tarefa ELM) · backlog.md (elm) · commit (mensagem: SEM REGRA).
   ESCRITA NO ELM: planos, IBs (plannedFor) e tarefas após "sim".
4. VEREDITO MECÂNICO: SEM REGRA (estimativa em horas de [DEV]/[REV]/[VER] exigida por elm:162 e sem origem definida; sub: mensagem de commit para sprint).
```

```text
S11-F6 · Modo sprint — virada (migrar para a nova iteração)
1. INPUT EXATO (evento de sdd-planejamento, passo 5 da virada): "virada: sprint 3 fechada; migrar o que não concluiu para a Sprint 4"
   ESTADO: sprint-003.md `fechada`. sprint-004.md ainda não existe. No EWM: [DEV] FT-033 (plannedFor Sprint 3, em andamento); [ESP] EP-05 (não concluída); [ATD] AT-013 (aberto); IB FT-033 (não concluído). Iteração "Sprint 4" existe no PA. Manual no DOORS Next: nada.
2. REGRA APLICADA:
   - SE virada (plan:125-126) → modo sprint virada — fonte: plan:125-126; elm:176
   - ENTÃO tarefas e IBs não concluídos → só o plannedFor muda; o pai não muda; move, nunca recria — fonte: elm:176-177; elm:354
   - ENTÃO as novas tarefas são publicadas (S11-F5) — fonte: plan:125-126
   - SE o projeto exige baseline por sprint → roteiro manual — fonte: elm:177-178; mapeamento:62 (steering: "Manual no DOORS Next: nada" → não se aplica)
   - SEM REGRA: se "Sprint 4" não existisse, o passo de criar a iteração (S11-F5 passo 1) não é remetido aqui (elm:355-357)
   - AMBÍGUO: coluna "Tarefa ELM" de sprint-004.md para as tarefas migradas. S11-F6 manda seguir S11-F5, que só grava ids de tarefas criadas (elm:174-175); plan:125-126 não diz.
   - ENTÃO prévia + confirmação — fonte: elm:27-30
3. OUTPUT GERADO: saída padrão: 🏛️ ELM — Sprint 4 · Criados: 0 · Atualizados: 3 (plannedFor) · Pendências manuais: nenhuma (baseline não exigido).
   ARQUIVOS ESCRITOS: sprint-004.md / backlog.md (conforme S11-F5; ver AMBÍGUO).
   ESCRITA NO ELM: plannedFor de FT-033 (IB e tarefa [DEV]), [ESP] EP-05 e [ATD] AT-013 → Sprint 4, após "sim".
4. VEREDITO MECÂNICO: AMBÍGUO (coluna Tarefa ELM de sprint-004.md para tarefas migradas: S11-F6 manda seguir S11-F5, que trata só tarefas novas).
```

```text
S11-F7 · Modo atendimento — abrir [ATD]
1. INPUT EXATO (evento de sdd-atender): "abre o AT-013 'Extração de contas bloqueadas em setembro', quem atende: ana.souza"
   ESTADO: sprint-003 aberta (iteração "Sprint 3"). backlog.md: Sustentação com IB Atendimento 612005 existente. MCP sim.
2. REGRA APLICADA:
   - SE abrir atendimento → fonte: elm:182
   - ENTÃO `[ATD] AT-013 <título>`, filha do IB Atendimento (612005), plannedFor = iteração da sprint aberta (Sprint 3), responsável = quem atende (ana.souza) — fonte: elm:182-183
   - SEM REGRA: "estimativa" da [ATD] (elm:183 pede) — nenhuma regra diz de onde vem
   - ENTÃO estado em andamento — fonte: elm:183
   - ENTÃO prévia + confirmação — fonte: elm:27-30
3. OUTPUT GERADO: prévia: criar [ATD] AT-013 (filha de Atendimento 612005), Sprint 3, responsável ana.souza, estimativa "—" (sem regra). Após "sim": saída padrão.
   ARQUIVOS ESCRITOS: nenhum próprio (elm:367; o registro do AT é do sdd-atender).
   ESCRITA NO ELM: tarefa [ATD] criada após "sim".
4. VEREDITO MECÂNICO: SEM REGRA (estimativa da [ATD], elm:183). Subs: (a) se a linha Sustentação estiver vazia, o modo atendimento não manda criar o IB Atendimento (elm:133-134 só no modo backlog) → SEM REGRA; (b) concluir a [ATD]: CONFLITO entre atender:55 ("modo horas lança e conclui a tarefa") e elm:194-195 ("lançar não conclui; concluir é do modo conclusão ou da skill que chamou").
```

```text
S11-F8 · Modo horas — lançar
1. INPUT EXATO: "lança 4h"  (sessão na branch feature/FT-031, usuário joao.lima)
   ESTADO: status.md da branch: [DEV] FT-031 do papel de joao.lima (Dev, responsável). ccm_list_timesheet hoje (2026-10-15): 2 h já lançadas em FT-031. time code e work type no pa_*.json. Hoje = 2026-10-15.
2. REGRA APLICADA:
   - SE "lança 4h" → modo horas, lançar — fonte: elm:188-189
   - ENTÃO tarefa: não informada → a atual: o status.md da branch dá a [DEV] do papel de quem pede → [DEV] FT-031 — fonte: elm:190-191
   - ENTÃO horas já lançadas: listar, mostrar e descontar; uma linha por data; data futura não — fonte: elm:192
   - AMBÍGUO: "descontar" — desconta do pedido (lança 4 − 2 = 2 h) ou o total do dia fica em 4 h (lança 2 h)? Nenhuma regra diz.
   - AMBÍGUO (sub): "lança 4h" sem data — elm:192 fala em "uma linha por data", mas não diz qual data é padrão (hoje?)
   - ENTÃO só o responsável lança — fonte: elm:193 (joao.lima é responsável: OK)
   - ENTÃO máximo 16 h por dia (2 + 4 = 6 ≤ 16) — fonte: elm:193
   - ENTÃO time code e work type do pa_*.json — fonte: elm:193
   - ENTÃO confirmar e ccm_add_timesheet — fonte: elm:193
   - ENTÃO lançar não conclui a tarefa — fonte: elm:194-195
3. OUTPUT GERADO: prévia: "Lançar X h em [DEV] FT-031 · data 2026-10-15 · já lançado 2 h · total do dia Y h — confirmar?" (X e Y dependem da AMBÍGUO).
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: timesheet após "sim".
4. VEREDITO MECÂNICO: AMBÍGUO (elm:192 "desconte": do pedido ou do total do dia; data padrão quando a pessoa não diz).
```

```text
S11-F9 · Modo horas — relatório
1. INPUT EXATO: "relatório de horas da sprint 3" (no meio da sprint, 2026-10-20)
   ESTADO: sprint-003 aberta. FT-031 concluída sem horas lançadas. Estimativas de [DEV]/[REV]/[VER] não gravadas (ver S11-F5). [ESP] com 16 h previstas. MCP sim. Uma tarefa de FT-033 está com Tarefa ELM `pendente`.
2. REGRA APLICADA:
   - SE "relatório de horas" → modo horas, relatório — fonte: elm:3; elm:199
   - ENTÃO ccm_list_timesheet das tarefas da sprint → horas por tipo e por pessoa, planejadas × lançadas — fonte: elm:199-200
   - SEM REGRA: "planejadas" de [DEV]/[REV]/[VER] — origem da estimativa não definida (elm:162)
   - AMBÍGUO (sub): tarefas concluídas sem horas — "só no fechamento" (elm:200-201); e aqui é relatório intermediário. Não se sabe se a lista entra.
   - SEM REGRA (sub): tarefas com Tarefa ELM `pendente` ficam fora sem aviso — nenhuma regra manda avisar
   - ENTÃO o relatório alimenta a retrospectiva e a recalibração da reserva — fonte: elm:201
3. OUTPUT GERADO: tabela por tipo e por pessoa (formato não dito; "planejadas" indefinido). Sem template literal.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: leitura.
4. VEREDITO MECÂNICO: SEM REGRA (coluna "planejadas" depende de estimativas de [DEV]/[REV]/[VER] sem origem; mesmo ponto de S11-F5).
```

```text
S11-F10 · Modo testes (CT.csv → ETM → links)
1. INPUT EXATO: "liga os testes da FT-031"
   ESTADO: .kiro/specs/FT-031-<slug>/CT.csv existe (verificação gerou, ACEITO). verificacao.md e status.md existem. IB FT-031 (612002) e HF-01 (2034) existem no EWM/DOORS. Nenhum link ainda. MCP sim (elm-qm).
2. REGRA APLICADA:
   - SE "liga os testes" → fonte: elm:3
   - ENTÃO entregar o caminho do CT.csv e "Importe no ETM (Importar → CSV)"; perguntar os ids criados — fonte: elm:205; mapeamento:63
   - SE o passo é manual (MCP não cria caso de teste) → registrar `ELM pendente: importar CT.csv` — fonte: mapeamento:54 (regra geral de pendência)
   - ENTÃO, com os ids: elm-qm get_testartifact para obter a URL — fonte: elm:206
   - ENTÃO antes de ligar: listar os links existentes — fonte: mapeamento:41-42
   - ENTÃO prévia + confirmação (regra 1) — fonte: elm:27-30 (regras de toda publicação)
   - ENTÃO valida: CT → HF-01 (cenário); testado por: IB 612002 → CT — fonte: elm:206; mapeamento:35-36
   - ENTÃO registrar ids em verificacao.md e status.md — fonte: elm:209
   - SEM REGRA (sub): gatilho de retomada da pendência (quem volta com os ids e quando) — mapeamento:54 não diz
3. OUTPUT GERADO: instrução de importação + pergunta dos ids. Após os ids: prévia de links; saída padrão (Links: n).
   ARQUIVOS ESCRITOS: verificacao.md e status.md (ids). ESCRITA NO ELM: links valida e testado por após "sim"; a importação do CT é manual.
4. VEREDITO MECÂNICO: DETERMINÍSTICO (sub: retomada da pendência sem gatilho).
```

```text
S11-F11 · Modo especificação técnica (ET as-built, opcional)
1. INPUT EXATO (evento de sdd-consolidar): "FT-031 foi mergeada; consolidar a especificação técnica"
   ESTADO: steering: ET = `as-built no merge`; tipo ET = Especificação Técnica. design.md e código final da fatia. IB FT-031 612002. .kiro/specs/FT-031-<slug>/elm/ inexistente. MCP sim.
2. REGRA APLICADA:
   - SE linha ET = `as-built no merge` → modo ET — fonte: elm:213; steering:72
   - ENTÃO gerar `ET - FT-031 <título>` do design.md e do código final (nada do que não foi feito) — fonte: elm:213-214
   - ENTÃO gravar .kiro/specs/FT-031-<slug>/elm/ET-<slug>.md em OKF, type = Especificação Técnica — fonte: elm:215; okf:32-50
   - ENTÃO mostrar — fonte: elm:216
   - ENTÃO publicar "como os requisitos, depois do verified humano" — fonte: elm:216
   - SEM REGRA: requisitos só publicam com `verified` humano; o verified vem do GATE do PRD (prd:118-119; okf:61). A ET não tem GATE: quem dá o verified, quando e com qual login? Nenhuma regra.
   - ENTÃO ligar ao IB (implementa) — fonte: elm:216; mapeamento:32
   - SEM REGRA (sub): ET já existente (re-consolidação) — elm:211-216 não remete às regras de atualização de S11-F2
3. OUTPUT GERADO: o conceito mostrado + saída padrão.
   ARQUIVOS ESCRITOS: .kiro/specs/FT-031-<slug>/elm/ET-<slug>.md · index.md · log.md da pasta.
   ESCRITA NO ELM: nenhuma até o verified; depois, ET e link implementa com o IB 612002 (após "sim").
4. VEREDITO MECÂNICO: SEM REGRA (quem dá o `verified` humano da ET, e quando: elm:216 pede "depois do verified humano", mas o verified é definido só para o GATE do PRD: prd:118-119; okf:61).
```

```text
S11-F12 · Modo conclusão
1. INPUT EXATO: "fecha no ELM a FT-031"
   ESTADO: FT-031 concluída (merge feito). Horas lançadas: [DEV] 16 h, [REV] 4 h, [VER] 3 h. IB 612002. FT-032 e FT-033 não concluídas (épico EP-03 não fecha). ccm_list_workitem_states disponível.
2. REGRA APLICADA:
   - SE "fecha no ELM" → fonte: elm:3
   - ENTÃO horas de cada tarefa primeiro (lançar, S11-F8) — fonte: elm:220-221
   - ENTÃO tarefas e IB da fatia → estado de conclusão da PA (ccm_list_workitem_states) — fonte: elm:220-221
   - SE todas as fatias do épico estão concluídas → épico — fonte: elm:221 (FT-032 e FT-033 não → não fecha)
   - ENTÃO comentário opcional no IB com PR, pasta e ids publicados — fonte: elm:221
   - ENTÃO prévia + confirmação — fonte: elm:27-30
   - SEM REGRA (sub): tarefa concluída sem horas — "não trava" (consolidar:53-55, fora desta skill), mas o modo não mostra aviso
3. OUTPUT GERADO: saída padrão: 🏛️ ELM — conclusão · FT-031 · Atualizados: 4 (DEV, REV, VER, IB) · Pendências manuais: nenhuma.
   ARQUIVOS ESCRITOS: nenhum próprio. ESCRITA NO ELM: tarefas e IB no estado concluído; comentário no IB (após "sim").
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S11-X1 · Negativo: similares para a regra da ficha de fatia sem épico
1. INPUT EXATO (chamada da sdd-triar, triar:62): "similares para a regra da ficha FT-040 (padrão, sem épico): REG-01 'Desconto por lote' (desconto, lote, percentual)"
   ESTADO: sem épico. Ficha em <produto>/fatias/FT-040-<slug>.md. Bundle sincronizado. MCP sim.
2. REGRA APLICADA:
   - SE chamada da sdd-triar → modo similares — fonte: elm:51-52; triar:62
   - ENTÃO saída: bloco com cabeçalho "🔎 Similares no ELM — EP-<nn> · …" — fonte: elm:72
   - AMBÍGUO: o cabeçalho pede EP-<nn>, mas a ficha não tem épico. Não há variante do cabeçalho para ficha (elm:72 só tem EP).
   - ENTÃO recomendação: igual/sobrepõe → "devolve à sdd-prd decidir" — fonte: elm:98-99
   - SEM REGRA: a ficha não tem sdd-prd; quem decide para a ficha? (triar:62 não diz)
3. OUTPUT GERADO: bloco de similares com cabeçalho indefinido.
   ARQUIVOS ESCRITOS: nenhum. ESCRITA NO ELM: nenhuma.
4. VEREDITO MECÂNICO: AMBÍGUO (cabeçalho `EP-<nn>` sem variante para ficha, elm:72; a devolução de decisão à sdd-prd, elm:98-99, não tem dono na ficha).
```

```text
S11-X2 · Negativo: sessão sem MCP do ELM
1. INPUT EXATO: "publica no ELM o EP-03"  (sessão sem MCP elm — revisor ou outra máquina)
   ESTADO: igual a S11-F2; MCP ausente.
2. REGRA APLICADA:
   - SE sem MCP nesta sessão → não publicar; registrar `ELM pendente: <modo> <alvo>` no rodapé do PRD (épico) — fonte: elm:23-25
   - ENTÃO sem prévia de escrita e sem gravação no ELM — fonte: elm:23-24; elm:27-30
   - ENTÃO registro: `ELM pendente: publicar requisitos EP-03` no rodapé do prd.md — fonte: elm:24-25
3. OUTPUT GERADO: rodapé do prd.md com "ELM pendente: publicar requisitos EP-03"; resposta informando a pendência.
   ARQUIVOS ESCRITOS: prd.md (rodapé). ESCRITA NO ELM: pendente.
4. VEREDITO MECÂNICO: DETERMINÍSTICO.
```

```text
S11-X3 · Negativo: HF estável com REG ainda em rascunho
1. INPUT EXATO: "publica no ELM o EP-03"
   ESTADO: HF-01 `stable` com verified humano. REG-01 `draft`, sem verified, sem id. PRD: REG-01 "novo (verificado …)". HF-01 cita REG-01 por link.
2. REGRA APLICADA:
   - SE conceito não é stable + verified → "aguardando aprovação"; não publica — fonte: elm:90-91 → REG-01 fica de fora (DETERMINÍSTICO)
   - SE HF stable + verified → publica — fonte: elm:96
   - ENTÃO HF → REG "sempre" por link e, na publicação, embed — fonte: prd:92; okf:94
   - SE o conceito citado ainda não tem id → "só o título, como texto" — fonte: elm:105
   - CONFLITO: prd:92 e okf:94 mandam embed sempre; elm:105 manda texto com o título quando a REG não tem id. REG-01 não pode ter id, pois não foi publicada.
   - (elm:93 — ordem GL → REG → HF — só garante o id quando a REG está no mesmo lote)
3. OUTPUT GERADO: HF-01 publicada com "REG - Limite de tentativas" como texto (pela leitura de elm:105), sem embed.
   ARQUIVOS ESCRITOS: elm/HF-01 (resource, id). ESCRITA NO ELM: criar HF-01 sem embed da REG-01.
4. VEREDITO MECÂNICO: CONFLITO (prd:92 / okf:94 "sempre embed" × elm:105 "sem id → só o título").
```

#### Tabela-resumo · S11

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S11-F1 · Similares | DETERMINÍSTICO | — |
| S11-F2 · Requisitos | CONFLITO | commit: elm:42 × steering:59; glossário sem formato (elm:112-113) |
| S11-F3 · Backlog — épico | CONFLITO | triar:78 e prd:43 "só o épico" × elm:133-134 (cria Sustentação) |
| S11-F4 · Backlog — IB | CONFLITO | commit: elm:42 × steering:59 (demais passos determinísticos) |
| S11-F5 · Sprint | SEM REGRA | estimativa em horas de [DEV]/[REV]/[VER] exigida (elm:162), sem origem |
| S11-F6 · Virada | AMBÍGUO | coluna "Tarefa ELM" do sprint-004.md para tarefas migradas (elm:174-175 × elm:176-178) |
| S11-F7 · Atendimento | SEM REGRA | estimativa da [ATD] (elm:183) sem origem; concluir: atender:55 × elm:194-195 |
| S11-F8 · Horas — lançar | AMBÍGUO | "descontar" (elm:192): do pedido ou do total do dia; data padrão |
| S11-F9 · Horas — relatório | SEM REGRA | coluna "planejadas" sem origem das estimativas (elm:162) |
| S11-F10 · Testes | DETERMINÍSTICO | sub: retomada da pendência do CT sem gatilho |
| S11-F11 · ET as-built | SEM REGRA | quem dá o `verified` da ET (elm:216 × prd:118-119; okf:61) |
| S11-F12 · Conclusão | DETERMINÍSTICO | — |
| S11-X1 · Similares para ficha | AMBÍGUO | cabeçalho `EP-<nn>` sem variante (elm:72); decisão sem dono (elm:98-99) |
| S11-X2 · Sem MCP | DETERMINÍSTICO | `ELM pendente` no rodapé do PRD (elm:23-25) |
| S11-X3 · HF com REG em rascunho | CONFLITO | embed sempre (prd:92; okf:94) × título como texto sem id (elm:105) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| S11-F2 | `<produto>/epicos/<EP>-<slug>/elm/{GL,REG,HF}-*.md` — `resource`, `id`, `sources[{id: elm, resource, last_modified}]` (elm:111-113; okf:58-59) | Sim | YAML OKF. `id` vira inteiro no parse (testado), `resource` string | Confere com okf:59-65. `id` é a única chave extra permitida (okf:64) | **Write-back por item** (elm:41-44) + `log.md` por item; **commit só ao final** (elm:42-43, `<FT\|EP> - Publicar no ELM` × steering:59, confirma P3). **Idempotência/falha parcial:** coberta para requisitos: id gravado → atualiza; sem id → busca `rm_search_requirements(text=<título>)` por tipo/pasta e pergunta "é ele?" (elm:31-37); recomeça (elm:43-44). Lacunas: (a) interrupção deixa `elm/*.md` modificados **não commitados**, e `sdd-triar`/`consolidar`/`iniciar` param com árvore suja; (b) a busca de EWM usa "título com `[FT-031]`" mas os títulos de tarefa são `[DEV] FT-031 Implementar`, `[ESP] EP-05 …`, `[ATD] AT-013 …` (steering:78) e **não contêm `[FT-031]`** → publicação interrompida de tarefa não é reencontrada (duplicata); (c) a pendência `ELM pendente:` nunca é baixada (`ELM feito:` só existe em status-template:40/status:22) | I-elm (rodapé do PRD). Permissão: `sdd-produto` grava (elm/ sob `{{PRODUTO}}`); **`sdd-codificador` não** (deny ag-cod:44, 246) — e `sdd-elm` está nos dois agentes (ag-cod:17) sem aviso | DIVERGENTE leve (busca por `[FT-…]` × títulos de tarefa) + NÃO ESPECIFICADO (commit parcial, baixa da pendência). A P3 acertou o CONFLITO de commit |
| S11-F2 | `elm/log.md` — `**Publication**: … (ELM <id>)` | Sim | `.md` | Confere (okf:162-163) | idem | idem | OK |
| S11-F2 | glossário (`<docs/glossario.md>`, steering:30) — coluna ELM do termo (elm:112-113) | Sim; `{{GLOSSARIO}}` está na allowlist de `sdd-produto` (ag-prod:42) | tabela `Termo \| Definição \| Evitar \| Fonte \| ELM` | **Refina a P3/P2** ("sem formato"): o formato existe em entrev:84-86 (`GL 3120`), só que `sdd-elm` não remete a ele | idem; commit no mesmo lote | glossário "não há" (setup:123-125): elm não trata | OK com ressalva (formato em outra skill) |
| S11-F3 | `backlog.md` — `elm` do épico (`[<id>](<url>)`) e linha `Sustentação:` (`[SUS-<ano>] [<id>](<url>) · Atendimento [<id>](<url>)`, backlog.md:17, 55) | Sim | idem | Confere com backlog.md:17/53/55. Sem "Planejado para" no repositório. A P3 chamou de CONFLITO a criação de Sustentação "dentro do modo épico": é passo condicional distinto (elm:133-134), não contradição de arquivo | commit `<FT\|EP> - Publicar no ELM`; EP/SUS — `<FT\|EP>` não cobre SUS | I-elm; épico `pendente` + sem MCP: backlog.md:53 (valor `pendente`) é o certo, elm:24 só cita rodapé do PRD que ainda não existe quando a triagem registra o épico | DIVERGENTE leve (P3 superestimou o conflito) |
| S11-F4 | `backlog.md` — `elm` das fatias | Sim | idem | Confere | commit idem | I-elm; I-perm: `sdd-produto` OK, `sdd-codificador` negado | OK |
| S11-F5 | `sprint-<nn>.md` col. "Tarefa ELM" (**só** Especificação/Atendimento) e `backlog.md` `elm` (todas as tarefas de fatia) | Sim | — | Ver S10-F2 (pós-ELM): coluna inexistente na tabela Fatias | segundo commit; da branch da fatia **não** grava (iniciar:112-114; coerente com deny do codificador) | I-elm | DIVERGENTE (P3 "sprint-003.md (Tarefa ELM)" só vale para `[ESP]`) |
| S11-F6 | (nenhum arquivo próprio) — mudança de `plannedFor` só no EWM | — | — | A P3 diz "sprint-004.md / backlog.md conforme S11-F5": a virada **não** grava (elm:176-178); quem grava o sprint-<nn+1> é o planejamento | — | I-elm | OK (corrige a P3) / NÃO ESPECIFICADO (ids copiados) |
| S11-F7 | — (o registro `AT-<nnn>-<slug>.md`, README e linha em sprint-<nn>.md são do `sdd-atender`, atender:38) | — | — | Quem grava o id da `[ATD]` no `AT-*.md`/linha da Atendimento não está escrito em elm:182-184 nem em atender:38 | — | I-elm; IB "Atendimento" ausente: elm:133-134 só no modo backlog | NÃO ESPECIFICADO (id da `[ATD]`) |
| S11-F8 | `ELM pendente: lançar <h>h em <tarefa> (<data>)` em `status.md` / registro do AT / `sprint-<nn>.md` (elm:196-197) | `status.md`: `.kiro/specs/<ft>-<slug>/` (sdd:106) — **`sdd-produto` não pode gravar lá** (só `decisoes.md`, ag-prod:43); `sdd-codificador` pode. `[ESP]` → `sprint-<nn>.md` (qual seção: Especificação, sem coluna de pendência) | texto livre | sem formato de linha no `sprint-<nn>.md` | sem commit prescrito | I-elm; I-perm para produto×status.md | NÃO ESPECIFICADO (onde pendura a pendência de `[ESP]`; permissão do agente de produto) |
| S11-F10 | `.kiro/specs/<ft>-<slug>/verificacao.md` e `status.md` (ids dos CTs) (elm:209) | Sim (sdd:106) | `.md` | formato dos ids não definido | sem commit no modo testes; chamado pela consolidação (base) | I-perm: `sdd-produto` negado, `sdd-codificador` permitido; pausa sem retomada (P3) | NÃO ESPECIFICADO (commit, formato) |
| S11-F11 | `.kiro/specs/<ft>-<slug>/elm/ET-<slug>.md` (+ `index.md`, `log.md` da pasta) (elm:215; okf:13-19) | Sim, consistente com okf:13. `index.md`/`log.md` só em okf, não em elm:215 | OKF; `type` = tipo de ET (steering:75 tem placeholder único `<… \| —>`: pasta/`tags` do ET não definida) | `verified` humano da ET sem GATE: confirma P3 (SEM REGRA) | idem; ET → IB (`implementa`) | I-perm: `sdd-produto` negado (`.kiro/specs/*/elm/**` não está na allowlist); `sdd-codificador` ok | NÃO ESPECIFICADO (verificação humana, tags/pasta, agente com permissão) |
| S11-F1, F9, F12 | — | — | — | — | — | — | sem escrita: F1 (só leitura), F9 (relatório; o planejamento grava "Números"/`historico`), F12 (conclusão só no EWM) |
| S11-X2 | `prd.md` rodapé `ELM pendente: publicar requisitos EP-03` | Sim | texto livre | rodapé sem formato; baixa por `ELM feito:` não instruída | não commitado | I-elm | OK / NÃO ESPECIFICADO (baixa) |

---


## S12 · sdd-pesquisar

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S12-F1 · Pesquisa pedida pela pessoa (sessão da pessoa, com ou sem agente)
- **Gatilho:** frases da description (pesq:3): "pesquisa o código para a FT-031", "onde isso está implementado", "research", "entender o código antes de planejar".
- **Pré-condições / lê:** pasta `.kiro/specs/<ft>-<slug>/` com `status.md`; a fatia no `backlog.md` (`cobre`); PRD do épico, ou ficha da fatia sem épico (`<produto>/fatias/`) (pesq:19-23); steering de estrutura, comando de teste único do `sdd.md` (pesq:35,45); bundle do ELM (pesq:43); skills de toolkit ligadas (pesq:46).
- **Processamento:**
  1. Prefere delegar ao agente `sdd-pesquisador` (somente leitura, contexto próprio); sem ele, faz inline e depois trabalha a partir do arquivo, não da memória (pesq:15-17).
  2. Passo 1: escreve 3–7 perguntas que o plano vai precisar responder, antes de abrir o código (pesq:25-31).
  3. Passo 2: estrutura (steering + glob); fluxo atual do ponto de entrada até o dado, lendo os arquivos; 1–2 análogos de ponta a ponta (com testes); reaproveitamento; dados (schema real pelo MCP de banco só leitura ou modelos/migrações — só consulta e contagem vão para o arquivo, nunca linha com dado real); documentação do bundle ELM (divergência código × documentação é achado importante); testes (como rodar só os da área); carrega skill da stack antes de interpretar código (pesq:33-46).
  4. Passo 3: grava `research.md` no template (Perguntas e respostas · Fluxo atual · Análogos · Reaproveitar · Dados · Testes · Documentação × código · Restrições e riscos · Não encontrado) (pesq:50-81). Só fatos com evidência; sem solução/recomendação; > ~150 linhas → cortar o que o plano não usa (pesq:83-84).
  5. Quando **não** é o agente pesquisador (sessão da pessoa): `status.md` → `fase: planejando` + linha no Histórico (pesq:85-87).
- **Output:** `.kiro/specs/<ft>-<slug>/research.md` (único arquivo, pesq:91); `status.md` com `fase: planejando` e linha de Histórico. Resposta: resumo curto do que foi achado (inclusive divergências ELM × código e "Não encontrado"). Próximo passo: `sdd-plano` (pesq:3 "primeiro passo da sdd-plano"; iniciar mapeia a fase para `sdd-plano`, `sdd-iniciar/SKILL.md:127`).
- **Lacunas:**
  - `research.md` já existente (reexecução, ou replanejar): a skill não diz se sobrescreve, atualiza ou pergunta (pesq:48-81; plano:27 só dispara quando "sem research.md").
  - `<rm.download.path>` (pesq:43) não é chave do `steer` (steer:31 chama a linha de "Bundle do ELM (OKF da elm-sync)"); sem bundle ("não há") a skill não diz o que fazer com a seção Documentação × código.
  - Não diz o que fazer quando o `status.md` está em outra fase (ex.: `implementando`): ela grava `planejando` incondicionalmente (pesq:85) — pode regredir a fase.

#### S12-F2 · Pesquisa chamada pela sdd-plano (Passo 1) via agente pesquisador
- **Gatilho:** evento: `sdd-plano` Passo 1, "Sem `research.md` → sdd-pesquisar (de preferência pelo agente sdd-pesquisador)" (plano:27; pesq:3 "como primeiro passo da sdd-plano").
- **Pré-condições / lê:** as mesmas de F1; pasta criada pela `sdd-iniciar` (fase `pesquisando`, stpl:11).
- **Processamento:** passos 1–4 de F1 pelo agente. O agente **nunca grava `status.md`**: quem o chamou registra (pesq:85-87). Ele devolve só o `research.md`/resumo (pesq:15-16). O `sdd-plano` então lê o arquivo (plano:27-28) e, se houver divergência ELM × código, pergunta à pessoa antes de seguir (plano:28-29).
- **Output:** `research.md` na pasta da fatia; nenhuma alteração em `status.md` por parte do pesquisador. Handoff: volta ao `sdd-plano` Passo 2.
- **Lacunas:**
  - Quem grava `fase: planejando` depois da pesquisa nesse caminho? `plano:56` só manda gravar `planejando` ao escrever o plano (Passo 3); entre o fim da pesquisa e o Passo 3 a fase continua `pesquisando`. O `loop:92` grava explicitamente "`planejando` depois da pesquisa"; o `plano` não.
  - O agente `sdd-pesquisador` só escreve em `research.md` (`sdd-setup/assets/agents/sdd-pesquisador.json`, write allowedPaths) — coerente; mas o `research.md` gerado não é commitado por ninguém nesse caminho (ver lacuna de commit em S13-F1).

#### S12-F3 · Pesquisa autônoma (sdd-loop fase 1 / workflow `sdd-planejar-fatia`)
- **Gatilho:** evento: `sdd-loop` Passo 3, fase 1, subagente `sdd-pesquisador` com `AUTONOMO=true`, id da fatia, caminho da worktree `.kiro/local/wt/<ft>` e rodada (loop:75-83); ou passo `pesquisa` do workflow, que pede `research.md` "sem perguntas; o que não achar vai para 'Não encontrado'" (wf-plan, step `pesquisa`).
- **Pré-condições:** worktree da fatia criada pelo loop (loop:51-65); comandos dentro dela com `cd .kiro/local/wt/<ft> && <cmd>` (`git -C` bloqueado, loop:67-70); caminho do arquivo `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/research.md` (permitido no agente).
- **Processamento:** F1 passos 1–4 sem perguntas; sem gravar `status.md` (agente). Orquestrador, depois da fase: grava `fase: planejando`, atualiza log, Rodadas e Histórico, commit pequeno na worktree (loop:92-94). Sai quando `research.md` gravado (loop:83).
- **Output:** `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/research.md`; commit feito pelo orquestrador. Próximo: fase 2 (plano, `sdd-codificador`).
- **Lacunas:**
  - A skill não menciona `AUTONOMO=true` (grep: só `plano`, `impl`, `sdd-entrevistar`). Comportamento autônomo vem só do loop/workflow; divergência ELM × código não tem tratamento autônomo (em `plano:28-29` a divergência exige pergunta).
  - Pasta da fatia inexistente: só o workflow trata (`send_message severity error`); a skill não define.

#### S12-F4 · Pesquisa da trilha rápida (defeito/pedido) — "pesquisa curta"
- **Gatilho:** fatia em trilha rápida, fase `pesquisando` (`sdd-iniciar/SKILL.md:52` "pesquisa curta → bugfix.md + tasks.md"); ou frase de F1 com um defeito/pedido.
- **Pré-condições / lê:** na trilha rápida a entrada é "o defeito/pedido" (pesq:22-23) no lugar de PRD/ficha; `cobre` vazio.
- **Processamento:** F1, com ênfase em: onde o defeito ocorre, fluxo atual com `arquivo:linha` (a causa raiz sai daqui — `tmpl:145`), testes vizinhos (o primeiro teste da trilha reproduz o defeito, `tmpl:85-86`), e evidências do comportamento atual (log/consulta, sem dado real).
- **Output:** `research.md` curto; mesmas regras de status de F1/F2.
- **Lacunas:** "curta" não é definida na skill: não diz quais seções do template são dispensadas nem um limite menor que ~150 linhas (pesq:84; `sdd-iniciar/SKILL.md:52`).

#### S12-F5 · Pesquisa sem agente (inline, na mesma sessão)
- **Gatilho:** "Sem o agente, faça você mesmo" (pesq:16-17) — sessão onde o `sdd-pesquisador` não está disponível/não foi ligado.
- **Processamento:** como F1, mas lendo muitos arquivos no contexto do planejador; ao terminar "trabalhe a partir do arquivo, não da memória da leitura" (pesq:16-17). Como não é o agente, grava `fase: planejando` + Histórico (pesq:85-86).
- **Output:** `research.md` + `status.md`.
- **Lacunas:** a skill não prevê compactar/limpar o contexto depois (só recomenda ler do arquivo); a regra "Nunca compacte no meio de uma fase" (`sdd/SKILL.md:115`) não é cruzada com esse caso.

#### S12-F6 · Pergunta pontual sem fatia (entrevista/PRD)
- **Gatilho:** "onde isso está implementado" fora de uma fatia (pesq:3) ou delegação de `sdd-entrevistar`/`sdd-prd` ao `sdd-pesquisador` (prompt do agente `sdd-setup/assets/agents/sdd-pesquisador.json`: "Pergunta pontual … responda direto, curto … não grave arquivo").
- **Processamento esperado:** Passo 2 sem Passo 3; responde com evidências `arquivo:linha`; não grava arquivo.
- **Output:** resposta curta na conversa; nenhum arquivo.
- **Lacunas:** a **skill** não descreve esse fluxo — exige pasta da fatia (pesq:19-23) e gravação do `research.md` (pesq:48-91; "Somente leitura: nenhum arquivo além de research.md", pesq:91). O fluxo só existe no prompt do agente (contradição de fonte).

> Trilha direta não tem pesquisa: pasta só com `status.md` (`impl:121-124`; `sdd-iniciar/SKILL.md:53`).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


#### S12-F1 · Pesquisa pedida pela pessoa (sessão da pessoa, agente disponível)
1. INPUT EXATO: "pesquisa o código para a FT-031"
   ESTADO: `.kiro/specs/ft-031-bloquear-conta/status.md` com `fase: pesquisando`, sem `research.md`; backlog com `cobre` = HF-01 1.1, 1.2; PRD do épico existe; trilha padrão; modo HITL; `sdd-pesquisador` disponível.
2. REGRAS:
   - SE agente `sdd-pesquisador` disponível ENTÃO delegar a ele, que devolve só o `research.md` — `pesq:15-16`
   - SE pasta com `status.md`, `cobre` e PRD presentes ENTÃO ler essa entrada — `pesq:21-23`
   - ANTES de abrir o código ENTÃO escrever de 3 a 7 perguntas — `pesq:25-31`
   - Investigar: estrutura, fluxo atual, análogos, reaproveitamento, dados, documentação, testes, skill da stack — `pesq:33-46`
   - Gravar `research.md` no template (Perguntas e respostas … Não encontrado) — `pesq:50-81`
   - SE a sessão que chamou o pesquisador é a da pessoa ENTÃO `status.md`: `fase: planejando` + linha no Histórico — `pesq:85-86`
3. OUTPUT GERADO: resumo curto da pesquisa (com divergências e "Não encontrado"); próximo passo `sdd-plano`.
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/research.md` · Markdown no template de `pesq:50-81` | `.kiro/specs/ft-031-bloquear-conta/status.md` · `fase: planejando` + linha de Histórico (o texto da linha não é fixado; o exemplo está em `stpl:42`).
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S12-F2 · Pesquisa chamada pela sdd-plano (Passo 1), via agente
1. INPUT EXATO: "planeja a FT-031" (sessão da pessoa, `sdd-plano` começa)
   ESTADO: pasta criada pela `sdd-iniciar` com `fase: pesquisando`; sem `research.md`; `sdd-pesquisador` disponível.
2. REGRAS:
   - SE sem `research.md` ENTÃO `sdd-pesquisar`, de preferência pelo agente — `plano:27`
   - Agente devolve `research.md` e nunca grava `status.md`; quem o chamou registra — `pesq:85-87`
   - Fase `planejando` é gravada ao escrever o plano (Passo 3) e vale também na análise do Passo 4 — `plano:56`
   - Trabalhar a partir do arquivo lido, não da memória — `plano:27-28`
3. OUTPUT GERADO: `research.md` pronto; `plano` segue para o Passo 2.
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/research.md` (pelo agente) | `status.md`: NÃO-DEFINIDO neste ponto (pesq:86-87 manda o chamador registrar; `plano:56` só manda `planejando` no Passo 3)
4. VEREDITO MECÂNICO: AMBIGUO (`pesq:86-87` manda o chamador registrar `planejando` logo após a pesquisa; `plano:56` manda gravar `planejando` só no Passo 3. Entre um e outro, a fase fica `pesquisando` ou vira `planejando`?)

#### S12-F3 · Pesquisa autônoma (sdd-loop fase 1)
1. INPUT EXATO: evento do orquestrador: "AUTONOMO=true · FT-031 · worktree .kiro/local/wt/ft-031 · rodada 1 · fase 1 (pesquisa)"
   ESTADO: worktree criada; `.kiro/local/wt/ft-031/.kiro/specs/ft-031-bloquear-conta/status.md` com `fase: pesquisando`; backlog e PRD presentes; sem divergência ELM × código; `sdd-pesquisador` disponível.
2. REGRAS:
   - SE fase 1 do loop ENTÃO subagente `sdd-pesquisador` recebe AUTONOMO, id, caminho da worktree, pasta e rodada — `loop:75-76`, `loop:83`
   - Comandos dentro da worktree com `cd .kiro/local/wt/ft-031 && …` — `loop:67-70`
   - Pesquisa: os passos de `pesq:25-81` sem perguntas à pessoa (a skill não pede resposta); só grava `research.md` — `pesq:91`
   - Agente não grava `status.md` — `pesq:85-87`
   - Depois da fase, o orquestrador grava `fase: planejando`, log, Rodadas e Histórico e faz commit pequeno na worktree — `loop:92-94`
3. OUTPUT GERADO: `research.md` gravado; sai da fase 1.
   ARQUIVOS ESCRITOS: `.kiro/local/wt/ft-031/.kiro/specs/ft-031-bloquear-conta/research.md` · template de `pesq:50-81` | `…/status.md` · `fase: planejando` + Histórico | commit na worktree (mensagem pelo padrão do `sdd.md` Git)
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S12-F4 · Pesquisa da trilha rápida ("pesquisa curta")
1. INPUT EXATO: "pesquisa curta do defeito 4567 (FT-040)"
   ESTADO: trilha rápida; `status.md` com `fase: pesquisando`; `cobre` vazio; o defeito está descrito no backlog ou no pedido.
2. REGRAS:
   - SE trilha rápida ENTÃO a entrada é o defeito/pedido no lugar do PRD — `pesq:21-23`
   - "pesquisa curta → bugfix.md + tasks.md" aparece na tabela de trilhas da `iniciar` — `iniciar:52`
   - Pesquisa: template completo com as 9 seções — `pesq:50-81`
   - "Curto" é só meta de tamanho: mais de ~150 linhas → cortar o que o plano não usa — `pesq:83-84`
   - `status.md` → `fase: planejando` + Histórico (sessão da pessoa) — `pesq:85-86`
3. OUTPUT GERADO: `research.md` curto (quantas seções? não definido); `status.md` `planejando`.
   ARQUIVOS ESCRITOS: `research.md` · template de `pesq:50-81` (seções dispensáveis: NÃO-DEFINIDO) | `status.md` · `fase: planejando`
4. VEREDITO MECÂNICO: AMBIGUO (`pesq:50-81` pede as 9 seções; `iniciar:52` fala em "pesquisa curta" sem dizer quais seções faltam; `pesq:84` só dá um teto de linhas. Uma leitura é "template integral, só mais curto"; a outra é "seções dispensadas").

#### S12-F5 · Pesquisa sem agente (inline)
1. INPUT EXATO: "pesquisa a FT-031"
   ESTADO: `sdd-pesquisador` indisponível nesta sessão; `status.md` com `fase: pesquisando`; sem `research.md`; sessão da pessoa.
2. REGRAS:
   - SE agente indisponível ENTÃO fazer você mesmo — `pesq:16-17`
   - Passos 1–3 como em S12-F1 — `pesq:25-81`
   - Ao terminar, trabalhar a partir do arquivo, não da memória da leitura — `pesq:16-17`
   - SE você não é o agente ENTÃO `status.md`: `fase: planejando` + Histórico — `pesq:85-86`
3. OUTPUT GERADO: `research.md` e resumo; `status.md` `planejando`.
   ARQUIVOS ESCRITOS: `research.md` · template de `pesq:50-81` | `status.md` · `fase: planejando` + Histórico
4. VEREDITO MECÂNICO: DETERMINISTIC (`sdd:115` pede não compactar no meio de uma fase, mas nenhuma regra manda compactar ou limpar o contexto depois da pesquisa, então não dispara)

#### S12-F6 · Pergunta pontual sem fatia
1. INPUT EXATO: "onde a senha é validada no login?"
   ESTADO: sem FT, sem `.kiro/specs/` correspondente, sem `status.md`; `sdd-pesquisador` disponível.
2. REGRAS:
   - SE pedido "onde isso está implementado" ENTÃO a skill é acionada (só pela description) — `pesq:3`
   - Entrada é a pasta da fatia com `status.md` — `pesq:19-21`
   - Nenhuma regra manda responder sem pasta, nem recusar, nem gravar em outro lugar. A única regra de escrita é `pesq:91` (só `research.md`)
3. OUTPUT GERADO: NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum (`pesq:91` proíbe qualquer arquivo além de `research.md`)
4. VEREDITO MECÂNICO: SEM REGRA (a resposta curta sem arquivo só aparece no prompt do agente pesquisador, que está fora das fontes permitidas)

#### S12-B1 (borda) · Pasta da fatia ausente
1. INPUT EXATO: "pesquisa a FT-031" (a FT-031 está no backlog, mas a pasta `.kiro/specs/ft-031-*` não existe)
   ESTADO: sem pasta nem `status.md`.
2. REGRAS:
   - Entrada obrigatória: pasta com `status.md` — `pesq:19-21`
   - Sem regra de ação para entrada ausente (não manda parar, nem criar a pasta, nem chamar a `iniciar`)
3. OUTPUT GERADO: NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA

#### S12-B2 (borda) · `research.md` já existe (reexecução)
1. INPUT EXATO: "pesquisa a FT-031 de novo"
   ESTADO: `research.md` de duas semanas atrás na pasta; `status.md` com `fase: planejando`.
2. REGRAS:
   - SE pedido de pesquisa ENTÃO investigar e gravar `research.md` no template — `pesq:48-81`
   - `plano:27` só se aplica "sem `research.md`", então não cobre o caso
   - Nenhuma regra fala em sobrescrever, atualizar ou perguntar
3. OUTPUT GERADO: `research.md` novo (ou atualizado: NÃO-DEFINIDO).
   ARQUIVOS ESCRITOS: `research.md` · "grava" sem dizer se apaga o anterior
4. VEREDITO MECÂNICO: AMBIGUO ("grava `research.md`" pode ser lido como sobrescrever o arquivo inteiro ou atualizar só as seções que mudaram)

#### S12-B3 (borda) · Pesquisa com divergência ELM × código, em modo AUTONOMO
1. INPUT EXATO: evento do loop: "AUTONOMO=true · FT-031 · fase 1" e, na fase 2, o `research.md` com a seção "Documentação × código: ELM diz 3 tentativas; o código conta 5"
   ESTADO: fase 2 recebe o `research.md` e o `sdd-codificador` tem subagente `sdd-revisor` (`steer:88`).
2. REGRAS:
   - Pesquisa registra a divergência como achado importante — `pesq:43-44`
   - SE divergência ELM × código apontada na pesquisa ENTÃO perguntar antes de seguir — `plano:28-29`
   - SE AUTONOMO=true ENTÃO sem perguntas; lacuna de negócio → `bloqueada` — `plano:95-98`
   - A divergência não é lacuna de negócio pela definição de `plano:33-34`, então `plano:97-98` não a cobre
3. OUTPUT GERADO: NÃO-DEFINIDO (perguntar não é permitido e `bloqueada` só vale para lacuna de negócio).
   ARQUIVOS ESCRITOS: NÃO-DEFINIDO
4. VEREDITO MECÂNICO: CONFLITO (`plano:28-29` manda perguntar antes de seguir × `plano:97` diz "sem perguntas" no modo AUTONOMO)

#### Resumo S12

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S12-F1 pesquisa pedida, agente | DETERMINISTIC | Delega, grava `research.md` e registra `planejando` |
| S12-F2 pesquisa chamada pela plano | AMBIGUO | Quem grava `planejando` após a pesquisa: `pesq:86-87` × `plano:56` |
| S12-F3 pesquisa autônoma (loop) | DETERMINISTIC | `loop:92` manda o orquestrador gravar `planejando` |
| S12-F4 pesquisa curta (rápida) | AMBIGUO | "Curta" não diz quais seções do template dispensar |
| S12-F5 pesquisa sem agente | DETERMINISTIC | Faz inline e registra `planejando` |
| S12-F6 pergunta pontual sem fatia | SEM REGRA | Só existe no prompt do agente, fora das fontes |
| S12-B1 pasta ausente | SEM REGRA | `pesq:19-21` declara entrada e não diz o que fazer sem ela |
| S12-B2 research.md já existe | AMBIGUO | "Grava" não diz sobrescrever ou atualizar |
| S12-B3 divergência em AUTONOMO | CONFLITO | `plano:28-29` pergunta × `plano:97` sem perguntas |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura confere com o template? | Sucesso (quem grava / commit / branch) | Inacessível / sem permissão / inexistente | Veredito |
|---|---|---|---|---|---|---|---|
| F1 pessoa + agente | `P/research.md` | Sim: `pesq:10,91` e A:pesquisador allow `.kiro/specs/*/research.md`. Relativo à raiz do projeto, branch da fatia | `.md` | Sim: 9 seções `pesq:50-81` (Perguntas e respostas · Fluxo atual · Análogos · Reaproveitar · Dados · Testes · Documentação × código · Restrições e riscos · Não encontrado); "~150 linhas" `pesq:84` | Grava o `sdd-pesquisador`. **Ninguém commita**: o agente não tem `git add/commit` (A:pesquisador deny); `pesq` não manda commitar; só entra no commit "dos arquivos do plano" (`plano:85`) se essa expressão incluir `research.md` — o texto não a define. Branch da fatia | NÃO ESPECIFICADO (pasta da fatia ausente: `pesq:19-23` só declara a entrada; sem permissão: nada) | NÃO ESPECIFICADO (commit/dono do `research.md`) |
| F1 pessoa + agente | `P/status.md` (`fase: planejando` + linha de Histórico) | Sim (`pesq:85-86`) | `.md`, tabela de campos + lista em Histórico | Campo `Fase` existe (`stpl:11`); **não há modelo de linha** para o Histórico da pesquisa — `stpl:42` é a linha da `sdd-iniciar` ("fatia iniciada"), não da pesquisa | Sessão da pessoa grava (agente não pode, `pesq:85-87`). Sem commit mandado; `plano:85` só commita em "Aprovado". `status.md` fica sujo | NÃO ESPECIFICADO | DIVERGENTE da Parte 3 (S12-F1 cita `stpl:42` como exemplo da linha — não é; o texto da linha é livre). Regra incondicional `pesq:85` pode regredir a fase se estava em `implementando` |
| F2 chamada por sdd-plano | `P/research.md` | Sim | `.md` | Sim (idem F1) | Grava o agente. `status.md`: `pesq:86-87` manda "quem o chamou registra (sdd-plano…)", mas `plano:27-29,56` não manda registrar `planejando` após a pesquisa — só no Passo 3 (`plano:56`). Entre os dois a fase fica `pesquisando` e a linha de Histórico da pesquisa não é escrita. No workflow `wf-plan` o passo `plano` grava `planejando` (preenche a lacuna); no loop `loop:92` idem; só o `sdd-plano` HITL não | NÃO ESPECIFICADO | NÃO ESPECIFICADO (quem grava `planejando`/Histórico no HITL) — confirma o AMBIGUO da Parte 3; efeito prático benigno (mesmo valor gravado depois) |
| F3 autônoma (loop) | `PW/research.md` | Sim: caminho vem do orquestrador (`loop:75-76,83`); A:pesquisador allow `.kiro/local/wt/*/.kiro/specs/*/research.md` (matcher: permitido). A **skill** não diz "relativo à worktree"; depende do chamador | `.md` | Sim | Grava o agente; `status.md` (`planejando`, log, Rodadas, Histórico) e **commit na worktree pelo orquestrador** (`loop:92-94`); branch da fatia na worktree | NÃO ESPECIFICADO na skill. O workflow `wf-plan` (passo `pesquisa`) trata "pasta inexistente → send_message error" | OK (confirma DETERMINISTIC da Parte 3) |
| F3 workflow `sdd-planejar-fatia` | `P/research.md` (checkout principal) | Sim; pasta achada por "nome começa pelo id em minúsculas" (wf-plan `pesquisa`) | `.md` | Sim | Grava o agente; **ninguém commita** no workflow (nem o passo `plano`/`ajustar`); `fase planejando` é do passo `plano` | wf-plan: erro via `send_message` se pasta inexistente; sem permissão: nada | OK para o arquivo; NÃO ESPECIFICADO o commit |
| F4 rápida ("pesquisa curta") | `P/research.md` | Sim | `.md` | Parcial: `ini:52` diz "pesquisa curta", `pesq` só tem o template de 9 seções e teto ~150 linhas; seções dispensáveis não definidas | idem F1 | NÃO ESPECIFICADO | NÃO ESPECIFICADO ("curta" sem estrutura) — confirma AMBIGUO |
| F5 inline | `P/research.md` + `P/status.md` | Sim | `.md` | Sim | Sessão da pessoa grava ambos (`pesq:85-86`); sem commit | NÃO ESPECIFICADO | OK (confirma DETERMINISTIC); commit idem F1 |
| F6 pergunta pontual | nenhum | n/a | n/a | n/a | **Skill:** `pesq:91` ("nenhum arquivo além de research.md") + `pesq:19-23` (exige pasta) não descrevem a resposta sem arquivo. **Agente:** A:pesquisador prompt "Pergunta pontual … responda direto, curto … não grave arquivo" — a regra existe, só não na skill | n/a | DIVERGENTE skill × agente. A Parte 3 marcou SEM REGRA por não ter lido o agente: refutado para o agente (há regra e a allowlist de escrita só tem `research.md`); permanece lacuna na skill |
| B2 `research.md` já existe | `P/research.md` | Sim | `.md` | n/a | "grava" (`pesq:50`) não diz sobrescrever/atualizar; a ferramenta de escrita sobrescreve e a história some | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma AMBIGUO |

Achados de persistência S12

- Commit do `research.md` não tem dono em nenhum caminho HITL: agente sem git (`A:pesquisador` deny `git add`/`git commit`), skill sem passo de commit (`pesq:85-92`), `plano:85` só cita "arquivos do plano". Só o loop cobre (`loop:92-94`); o workflow `wf-plan` não.
- `pesq:85` grava `fase: planejando` incondicionalmente (sem checar fase atual) — reexecução em `implementando`/`revisando` regride a fase.
- `pesq:43` usa `<rm.download.path>`, que não é chave do steering (`steering/sdd.md:31` chama "Bundle do ELM (OKF da elm-sync)"); sem bundle, a seção "Documentação × código" não tem valor definido além de "nenhuma encontrada" (`pesq:74`).

---


## S13 · sdd-plano

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S13-F1 · Plano padrão HITL, caminho feliz (GATE aprovado por pessoa)
- **Gatilho:** "planeja a FT-031", "gera a spec", "cria as tasks", "aprova o plano" (plano:3); ou encaminhamento da `sdd-iniciar` para fases `pesquisando`/`planejando`/`plano-em-revisao` (`sdd-iniciar/SKILL.md:127`).
- **Pré-condições / lê:** pasta `.kiro/specs/<ft>-<slug>/` criada pela `sdd-iniciar`, na branch da fatia (plano:20); lê `status.md`, a fatia no `backlog.md`, PRD do épico **ou** ficha da fatia sem épico `<produto>/fatias/` **ou** o defeito, `.kiro/steering/sdd.md` com regras aprendidas, steering de tecnologia/estrutura (plano:20-23); `references/plano-templates.md` (plano:18). Abre arquivos pelo caminho do power instalado, não pelo workspace (plano:12-14).
- **Processamento:**
  1. **Passo 1 — Pesquisa:** sem `research.md` → `sdd-pesquisar` (S12-F2). Trabalha a partir do arquivo (plano:27-29).
  2. **Passo 2 — Decisões em aberto:** lacuna de negócio → pare (S13-F6); escolha técnica com alternativas reais → apresenta à pessoa com a recomendada (HITL) e registra em "Decisões técnicas" (plano:31-36).
  3. **Passo 3 — Escrever:** (0) `.config.kiro` se não existe, `specType: feature` (plano:40; `tmpl:9-18`); (1) `requirements.md` com critérios EARS "falsificáveis na base" (observação que hoje mostra o critério falso) (plano:42-44; `tmpl:20-52`); (2) `design.md`: pattern grounding, forma do programa (árvore de arquivos com ação, assinaturas, árvore de chamadas), pontos de teste, erros/transação/reexecução, contrato de pronto, decisões técnicas (plano:45-48; `tmpl:88-143`); (3) `tasks.md`: uma tarefa por comportamento, teste primeiro, comando de pronto, `_Requirements: N.M_`, última = checkpoint de validação completa (plano:49-50; `tmpl:148-184`); (4) consulta skills de toolkit da stack (plano:51); (5) limite ~200 linhas / ~8 tarefas → propõe dividir (S13-F8). `status.md`: `fase: planejando` (plano:56).
  4. **Passo 4 — Análise independente:** incrementa "revisão do plano" em Rodadas; pede ao subagente `sdd-revisor` a rubrica L (passando só pasta e rodada); ele grava `analise-plano-<N>.md` (plano:60-62). `ANALISE: OK` → Passo 5; `AJUSTAR` com falta do plano → corrige e repete (até 2 rodadas); falta do PRD → Passo 2 (plano:64-65). Fluxos detalhados em S13-F9.
  5. **Passo 5 — GATE:** monta o cartão `🧭 Plano FT-… ` (plano:69-76) e grava `fase: plano-em-revisao` (conta no WIP de revisão humana, plano:78). HITL: sempre uma pessoa aprova; sugere que seja quem vai revisar o PR (plano:80). Aprovado → `fase: implementando`, linha no Histórico (quem aprovou), **commit** dos arquivos do plano (plano:85-86).
- **Output:** na pasta da fatia: `.config.kiro`, `research.md`, `requirements.md`, `design.md`, `tasks.md`, `analise-plano-<N>.md`; `status.md` com `fase: implementando`, Rodadas e Histórico; commit do plano. Resposta: cartão do GATE e, após o "sim", próximo passo `sdd-implementar` "numa sessão nova, de preferência" (plano:86-87).
- **Lacunas:**
  - **GATE reprovado/ajuste pedido não é descrito** em nenhum passo: o Passo 5 só tem "Aprovado →" (plano:85). O tratamento só aparece no `loop:97-98` ("Pediu ajuste → codificador (sdd-plano, replanejar) e nova análise"). Falta: fase a gravar, se zera a rodada de análise, e se volta ao Passo 3.
  - Quem muda a fase de `plano-em-revisao` para `implementando` numa sessão posterior ("aprova o plano da FT-031", gatilho de plano:3) não está num passo próprio: o texto está dentro do Passo 5 e só o `loop:96-98` descreve a retomada.

#### S13-F2 · Plano AFK com "análise basta" (sem GATE humano)
- **Gatilho:** fatia AFK (stpl:8) cujo `sdd.md` diz `Plano AFK: análise basta` (plano:81-82; `steer:63`); no loop, `loop:86` ("análise basta → grave `fase: implementando` e siga").
- **Pré-condições:** idem F1; `ANALISE: OK`.
- **Processamento:** Passos 1–4 como F1 (modo AFK: decisões técnicas "decida e registre", plano:35-36); no Passo 5 não espera pessoa: a fatia segue com `ANALISE: OK`; "quem conduz grava `fase: implementando`"; a pessoa revisa depois no PR (plano:81-83).
- **Output:** spec completa + `analise-plano-<N>.md` com `ANALISE: OK`; `status.md` `fase: implementando`.
- **Lacunas:**
  - **Commit do plano não é especificado** neste ramo: o commit só aparece para o caso "Aprovado" (plano:85). `loop:92-94` cobre o loop ("commit pequeno na worktree depois de cada fase"), mas na sessão da pessoa não. Consequência: `sdd-implementar` Passo 0 exige `git status` limpo "descontados" só `revisao-*.md`, `analise-*.md`, `verificacao.md`, `CT.csv`, `evidencias/`, `massa/` (impl:20-22) — `research.md`/`requirements.md`/`design.md`/`tasks.md` não estão na lista e fariam a implementação "avisar e parar".
  - O GATE (cartão) não é emitido quando "análise basta"; a pessoa só vê o plano no PR, mas o PR "não despeja o plano" (impl:114).

#### S13-F3 · Plano AFK com aprovação humana (loop pausa em plano-em-revisao)
- **Gatilho:** fatia AFK com `Plano AFK: aprovação humana` (`steer:63`); `loop:86` fase 4, ou passo `ajustar` do workflow ("OK com aprovação humana → fase plano-em-revisao", wf-plan).
- **Processamento:** F1 Passos 1–4; Passo 5: grava `plano-em-revisao`, commit do plano na worktree e **pare esta fatia** (loop:86). A pessoa lê o plano em `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/` e diz "aprovo o plano da FT-031" → orquestrador grava `fase: implementando` e retoma na fase 5 (loop:96-98).
- **Output:** plano commitado na worktree; fatia aguardando em `plano-em-revisao` (conta no WIP, plano:78; loop:33).
- **Lacunas:** nenhuma específica além das de S13-F1 (reprovação do GATE só no loop).

#### S13-F4 · Plano da trilha rápida (bugfix) — GATE `não` ou `sim`
- **Gatilho:** fatia de trilha rápida (defeito/ajuste ≤ 1 dia), `fase: pesquisando|planejando`; frases de F1.
- **Pré-condições:** `.config.kiro` com `specType: bugfix` (criado pela iniciar, `sdd-iniciar/SKILL.md:96-98`); `bugfix.md` no lugar de `requirements.md` (plano:42).
- **Processamento:** Passos 1–2 como F1 (sem PRD — o defeito). Passo 3: `bugfix.md` (Current/Expected/Unchanged Behavior, Bug Condition, Fix/Preservation Property; `tmpl:54-83`); `design.md` curto — Overview, causa raiz com `arquivo:linha` da research, a correção e Testing Strategy (exploração da condição do defeito, verificação da correção e da preservação) (`tmpl:145-146`); `tasks.md` cujas primeiras tarefas são **1.** teste que reproduz o defeito (vermelho) e **2.** testes de preservação (`tmpl:85-86`). Passo 4: rubrica L (L1 trata a rápida com `cobre` vazio, rub:32; L2 exige que bugfix comece pelo teste do defeito, rub:33). Passo 5: `GATE na trilha rápida` do `sdd.md` (`steer:63`): `não` → segue com `ANALISE: OK`; `sim` → como HITL (plano:83-84).
- **Output:** `bugfix.md`, `design.md` curto, `tasks.md`, `research.md`, `analise-plano-<N>.md` (se a análise não for pulada); `fase: implementando` (GATE não) ou `plano-em-revisao` → `implementando` (GATE sim).
- **Lacunas:**
  - Contradição de descrição: README diz "`bugfix.md` + `tasks.md`" (`sdd/SKILL.md:28`; `sdd-iniciar/SKILL.md:52`), mas `plano:45` e `tmpl:145` exigem também `design.md` curto (e o `impl:15` lê "`design.md` inteiro").
  - stpl:21-22 diz que na trilha rápida sem GATE "o passo é pulado" ao falar de `plano-em-revisao`; já `plano:83` diz "segue com `ANALISE: OK`" — ou seja, a análise **não** é pulada, só o GATE humano. Ambiguidade sobre se a análise independente é obrigatória na rápida.
  - Contrato de pronto: plano:47-48 o exige em todo design; no `design.md` rápido (`tmpl:145-146`) não há tabela de cenários, e `sdd-verificar/SKILL.md:30-31` cai para "comportamentos esperado e que não muda do bugfix.md" — não está no plano.

#### S13-F5 · Lacuna de negócio → parar e devolver ao P.O. (Passo 2)
- **Gatilho:** durante os Passos 1–3, regra sem valor, exceção sem comportamento, ou falta do PRD apontada pela análise (plano:33-34, 65).
- **Processamento:** **pare** (HITL): "Nunca decida regra no plano". Encaminha: `sdd-entrevistar`; se mudar o PRD aprovado, `sdd-prd` (mudança depois de aprovado); fatia sem épico → ficha aprovada, `sdd-triar` (plano:33-34; `sdd-triar/SKILL.md:41-42` aceita ficha devolvida pela `sdd-plano`). Após resposta, retoma no Passo 3.
- **Output:** pergunta clara para a pessoa; plano parcial (se houver) permanece em `planejando`. Fase pode virar `bloqueada (de: planejando)` — mas a skill só diz isso no modo autônomo (plano:97-98).
- **Lacunas:** HITL: sem instrução de gravar `bloqueada` nem de registrar a pergunta no `status.md`; `loop`/workflow a exigem (wf-plan: "registre a pergunta … no status.md").

#### S13-F6 · Divergência ELM × código apontada pela pesquisa (Passo 1)
- **Gatilho:** seção "Documentação × código" do `research.md` com divergência (pesq:73-74).
- **Processamento:** "pergunte antes de seguir (pode ser defeito, pode ser documentação velha)" (plano:28-29). Resposta define: defeito → `sdd-triar`/nova fatia ou rápida; documentação velha → segue e anota para a `sdd-consolidar` (inferido; a skill não diz o encaminhamento).
- **Output:** decisão da pessoa registrada (Histórico, não especificado); plano segue ou para.
- **Lacunas:** o texto só manda perguntar; não diz o destino de cada resposta nem onde registrar. No modo autônomo (plano:97-98) só existe "lacuna de negócio → bloqueada"; divergência não está coberta (o workflow trata como "divergência com o plano": wf-plan, passo `plano`).

#### S13-F7 · Fatia grande demais → propor divisão
- **Gatilho:** plano passa de ~200 linhas no total ou de ~8 tarefas (plano:52-54).
- **Processamento:** não escreve plano maior: propõe à pessoa dividir a fatia (`sdd-fatiar`, refinamento). Modo autônomo → `fase: bloqueada` com a proposta de divisão.
- **Output:** proposta de divisão; HITL: pessoa decide e vai para `sdd-fatiar`; autônomo: `bloqueada (de: planejando)` com a proposta.
- **Lacunas:** não diz o que fazer com `research.md`/rascunho já escrito; "~200 linhas no total" não diz se conta `requirements+design+tasks` ou também `research`; a rubrica L não verifica o limite (rub:30-41).

#### S13-F8 · Análise independente (Passo 4) — resultados OK / AJUSTAR / sem subagente
- **Gatilho:** plano escrito (fim do Passo 3), `fase: planejando` (plano:56).
- **Processamento:**
  1. Incrementa "revisão do plano" em Rodadas; chama `sdd-revisor` (rubrica L; passando só a pasta da fatia e a rodada); ele grava `analise-plano-<N>.md` (plano:60-62).
  2. `ANALISE: OK` → Passo 5 (S13-F1/F2/F3/F4).
  3. `ANALISE: AJUSTAR` com falta **do plano** → corrige só o plano e pede nova análise, **até 2 rodadas** (plano:65); falta **do PRD/ficha** → volta ao Passo 2 (S13-F5) (plano:65; `rub:43-45`).
  4. **Sem subagente disponível** (agente sem a ferramenta, passo de workflow) → pare e devolva a quem chamou: "plano pronto para análise" (plano:62-63).
- **Output:** `analise-plano-<N>.md` (última linha `ANALISE: OK|AJUSTAR`, rub:43); Rodadas atualizadas; handoff: GATE (Passo 5) ou bloqueio.
- **Lacunas:**
  - **O que fazer após a 2ª rodada sem `OK` não está no `plano`** (plano:65 termina em "até 2 rodadas"). Só o `loop:85` diz "2 rodadas sem OK → bloqueada"; em `impl:82` há o paralelo para código (bloqueada + 3 opções). Em HITL: indefinido.
  - Quem incrementa Rodadas diverge: `plano:60` manda incrementar **antes** de pedir; o workflow incrementa **depois** da revisão no passo `ajustar` (wf-plan); stpl:25-27 diz "quem pede a rodada".
  - O `rub` L **não verifica** itens exigidos pelo plano: critério "falsificável na base" (plano:42-44), forma do programa e contrato de pronto presentes em `design.md` (plano:45-48; GATE pede "Leia: forma do programa e contrato de pronto", plano:75), limite de tamanho (plano:52). L9 só cruza componentes × tarefas (rub:40).
  - Sem subagente dentro do `sdd-plano` (codificador autônomo): ver lacuna do modo autônomo (S13-F10).

#### S13-F9 · Aprovação/ajuste do plano em sessão posterior (fase `plano-em-revisao`)
- **Gatilho:** "aprova o plano" (plano:3); `sdd-iniciar` encaminha fase `plano-em-revisao` → `sdd-plano` (`sdd-iniciar/SKILL.md:127`); `sdd-status` lista "FT-031 plano-em-revisao há 1 dia → aprovar o plano (sdd-plano)" (`sdd-status/SKILL.md:47`).
- **Processamento esperado:** apresenta de novo o cartão do GATE (plano:69-76); com "sim": `fase: implementando`, Histórico (quem aprovou), commit dos arquivos do plano, próximo `sdd-implementar` em sessão nova (plano:85-87). Com ajuste pedido: **não definido** (ver F1).
- **Output:** `status.md` atualizado + commit; ou pedido de ajuste.
- **Lacunas:** não há passo/entrada específica para retomar em `plano-em-revisao` (ler o plano existente, reemitir GATE sem refazer Passos 1–4); descrito só implicitamente.

#### S13-F10 · Replanejar (implementação descobriu que o plano não serve)
- **Gatilho:** "replaneja" (plano:3); divergência reportada pela `sdd-implementar` ("muda o desenho → sdd-plano (replanejar)", `impl:57-58`); ajuste pedido no GATE pausado (loop:98).
- **Pré-condições:** `tasks.md` com tarefas já `[x]`; relato "Esperado × Encontrado × Por que importa" (`impl:53-56`).
- **Processamento:** atualiza `design.md`/`tasks.md` só no que mudou; **acrescenta** tarefas (nunca desmarca as prontas); registra o motivo no Histórico; repete Passos 4–5 só para a parte alterada (plano:89-93).
- **Output:** `design.md`/`tasks.md` editados, `analise-plano-<N+1>.md`, GATE reemitido; `status.md` com motivo no Histórico; depois `fase: implementando` e volta à `sdd-implementar`.
- **Lacunas:**
  - Fase durante o replanejamento não definida: `plano:56` (`planejando`) vale para o Passo 3, não para esta seção; a fatia está em `implementando`/`revisando` e passaria por `plano-em-revisao` (conta no WIP) sem regra explícita.
  - Contador de Rodadas "revisão do plano" e o limite de 2 rodadas: zera ou continua? Não diz.
  - Pode precisar alterar `requirements.md` (mudança de critério) — a skill só cita `design.md`/`tasks.md`; critério novo que mude negócio é de P.O. (plano:33-34).
  - Replanejar com GATE `análise basta` (AFK): reaplica a regra de `plano:81-83`? Não diz.

#### S13-F11 · Modo autônomo (`AUTONOMO=true`) — loop / workflow
- **Gatilho:** `sdd-loop` fases 2–4 (`sdd-codificador` "sdd-plano, Passos 2–3", loop:84; análise pelo `sdd-revisor`, loop:85; GATE pelo orquestrador, loop:86) ou passos `plano`/`analisar`/`ajustar` de `sdd-planejar-fatia` (wf-plan).
- **Processamento:** sem perguntas; decisão técnica com alternativas → escolhe a recomendada e registra em "Decisões técnicas"; lacuna de negócio → `fase: bloqueada` com a pergunta ao P.O. (plano:97-98). Escreve a spec (Passo 3); a análise é feita por **outro** subagente (loop) ou passo do workflow; o GATE é do orquestrador (loop:86) ou da pessoa (workflow termina no GATE). Fatia grande → `bloqueada` com a proposta de divisão (plano:53-54).
- **Output:** spec gravada; `status.md` `planejando` (ou `bloqueada`); depois, conforme `Plano AFK`: `implementando` ou `plano-em-revisao`.
- **Lacunas (alta gravidade):**
  - O texto do modo autônomo (plano:95-98) **não diz que o codificador deve parar depois do Passo 3**. O agente `sdd-codificador` tem ferramenta `subagent/sdd-revisor` (`sdd-setup/assets/agents/sdd-codificador.json`) e o Passo 4 manda pedir a análise ao subagente — sem a limitação "Passos 2–3" (loop:84) ou "Não rode a análise nem o GATE" (wf-plan, passo `plano`) o agente executaria o Passo 4 por conta própria, duplicando a fase 3 do loop e o contador de Rodadas.
  - O `loop:84` omite o Passo 1 (feito na fase 1) — coerente; mas o `plano` não declara que no autônomo o Passo 1 já foi feito por outra fase.
  - Divergência ELM × código no autônomo não coberta (ver S13-F6).

#### S13-F12 · Chamada indevida em trilha direta / sem pasta (guarda de entrada)
- **Gatilho:** "planeja a FT-xxx" para fatia direta (pasta só com `status.md`, `impl:121-124`) ou sem pasta criada pela `sdd-iniciar`.
- **Processamento esperado:** não definido: a skill assume a pasta criada pela `sdd-iniciar` (plano:20).
- **Lacunas:** não há regra de recusa/encaminhamento para a trilha direta (sem spec) nem para pasta/branch inexistente (a `sdd-iniciar` cuida da criação).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


#### S13-F1 · Plano padrão HITL, caminho feliz
1. INPUT EXATO: "planeja a FT-031" (depois do cartão, a pessoa responde "sim")
   ESTADO: `status.md` com `fase: pesquisando`; `research.md` presente; trilha padrão; HITL; `sdd-revisor` disponível; sem lacuna de negócio nem escolha técnica em aberto; plano com 190 linhas e 7 tarefas.
2. REGRAS:
   - SE `research.md` existe ENTÃO não pesquisa de novo — `plano:27`
   - SE não há lacuna de negócio nem escolha técnica em aberto ENTÃO seguir — `plano:31-36`
   - SE `.config.kiro` não existe ENTÃO criar com `specType: feature` — `plano:40`, `tmpl:9-18`
   - Escrever `requirements.md` (EARS falsificável na base) — `plano:42-44`, `tmpl:20-52`
   - Escrever `design.md` (pattern grounding, forma do programa, pontos de teste, erros, contrato de pronto, decisões) — `plano:45-48`, `tmpl:88-143`
   - Escrever `tasks.md` (uma tarefa por comportamento, teste primeiro, comando de pronto, `_Requirements_`) — `plano:49-50`, `tmpl:148-184`
   - SE plano ≤ ~200 linhas e ≤ ~8 tarefas ENTÃO segue — `plano:52-54`
   - `status.md`: `fase: planejando` — `plano:56`
   - Passo 4: Rodadas "revisão do plano" +1; pedir ao `sdd-revisor` a rubrica L, passando pasta e rodada; ele grava `analise-plano-1.md` — `plano:60-62`, `rub:28-45`
   - SE `ANALISE: OK` ENTÃO Passo 5 — `plano:64`
   - Passo 5: montar o cartão do GATE — `plano:69-76`
   - Aguardando aprovação → `fase: plano-em-revisao` — `plano:78`
   - HITL: sempre uma pessoa aprova — `plano:80`
   - SE aprovado ("sim") ENTÃO `fase: implementando`, linha no Histórico (quem aprovou) e commit dos arquivos do plano — `plano:85`
   - Próximo passo: `sdd-implementar` em sessão nova — `plano:86-87`
3. OUTPUT GERADO: cartão do GATE no formato de `plano:70-75` preenchido; depois do "sim", confirmação com o próximo passo.
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/.config.kiro` · uma linha JSON (`tmpl:14-16`) | `requirements.md`, `design.md`, `tasks.md` · templates | `analise-plano-1.md` (pelo `sdd-revisor`) | `status.md` · `fase: implementando`, Rodadas, Histórico | commit dos arquivos do plano
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S13-F2 · Plano AFK com "análise basta" (sessão da pessoa)
1. INPUT EXATO: "planeja a FT-031"
   ESTADO: modo AFK; `steer:63` diz `Plano AFK: análise basta`; trilha padrão; `research.md` presente; `sdd-revisor` disponível; não é AUTONOMO.
2. REGRAS:
   - SE modo AFK ENTÃO o GATE do plano segue o `sdd.md` — `plano:81`
   - SE `Plano AFK: análise basta` ENTÃO a fatia segue com `ANALISE: OK`; quem conduz grava `fase: implementando`; a pessoa revisa no PR — `plano:81-82`
   - Passos 1–4 como em S13-F1; decisões técnicas decididas e registradas — `plano:35-36`, `plano:56`, `plano:60-65`
   - Passo 5 "GATE do plano" (monta o cartão) está escrito como geral, mas o bullet AFK diz que não há aprovação humana — `plano:67-76` × `plano:81-82`
   - Commit do plano só aparece no ramo "Aprovado" — `plano:85`
3. OUTPUT GERADO: spec completa e `analise-plano-1.md` com `ANALISE: OK`; `status.md` `implementando`; cartão e commit NÃO-DEFINIDOS neste ramo.
   ARQUIVOS ESCRITOS: spec em `.kiro/specs/ft-031-bloquear-conta/` · templates | `analise-plano-1.md` | `status.md` · `fase: implementando` | commit: NÃO-DEFINIDO (o `impl:20-22` exige árvore limpa depois)
4. VEREDITO MECÂNICO: AMBIGUO (cartão e commit não estão definidos para "análise basta": `plano:67-76` manda montar o cartão no Passo 5, `plano:81-82` diz que não há GATE, e `plano:85` só prevê commit no aprovado)

#### S13-F3 · Plano AFK com aprovação humana (loop pausa)
1. INPUT EXATO: evento do loop: "ANALISE: OK na rodada 1 · Plano AFK = aprovação humana"; depois a pessoa escreve: "aprovo o plano da FT-031"
   ESTADO: fase 4 do loop; `status.md` com `fase: planejando` na worktree; `steer:63` diz `aprovação humana`.
2. REGRAS:
   - SE Plano AFK = aprovação humana ENTÃO commit do plano na worktree e parar esta fatia em `plano-em-revisao` — `loop:86`
   - Fase `plano-em-revisao` conta no WIP — `plano:78`
   - SE a pessoa aprova o plano ENTÃO gravar `fase: implementando` e retomar a fatia na fase 5 "(Passo 0)" — `loop:96-97`
   - "(Passo 0)" pode ser o Passo 0 do próprio loop, que pergunta se retoma (`loop:21-22`), ou o Passo 0 do `sdd-implementar` (`impl:18-29`)
   - Commit depois de cada fase — `loop:92-94`
3. OUTPUT GERADO: fatia em `plano-em-revisao` até a aprovação; depois da aprovação, `status.md` `implementando` e retomada da fase 5.
   ARQUIVOS ESCRITOS: `status.md` (`plano-em-revisao`, depois `implementando`) | commit do plano na worktree
4. VEREDITO MECÂNICO: AMBIGUO ("(Passo 0)" em `loop:97` pode ser o Passo 0 do loop, que manda perguntar se retoma, ou o Passo 0 do implementar, que só verifica a branch e o git)

#### S13-F4 · Plano da trilha rápida (defeito), GATE "não"
1. INPUT EXATO: "planeja o defeito 4567 (FT-040)"
   ESTADO: trilha rápida; `.config.kiro` com `specType: bugfix` criado pela `iniciar`; `research.md` presente; `status.md` `fase: planejando`; `steer:63` diz `GATE na trilha rápida: não`; `sdd-revisor` disponível.
2. REGRAS:
   - SE trilha rápida ENTÃO `bugfix.md` no lugar de `requirements.md` — `plano:42`, `tmpl:54-83`
   - `design.md` curto: Overview, causa raiz com `arquivo:linha`, correção, Testing Strategy — `tmpl:145-146`
   - `design.md` sempre com forma do programa e contrato de pronto — `plano:45-48` (sem exceção para a rápida)
   - `tasks.md`: 1 = teste que reproduz o defeito; 2 = testes de preservação — `tmpl:85-86`
   - Passo 4: análise pela rubrica L — `plano:60-65`
   - SE `GATE na trilha rápida = não` ENTÃO "segue com `ANALISE: OK`" — `plano:83`
   - "o passo é pulado quando o sdd.md permitir (… trilha rápida sem GATE)" — `stpl:21-22`
   - `fase: implementando` só é gravada em "Aprovado" — `plano:85`
3. OUTPUT GERADO: `bugfix.md`, `design.md` curto, `tasks.md`, `analise-plano-1.md` com `ANALISE: OK`.
   ARQUIVOS ESCRITOS: `bugfix.md`, `design.md`, `tasks.md` · templates | `analise-plano-1.md` | `status.md` · `fase: implementando`? NÃO-DEFINIDO no ramo "não"
4. VEREDITO MECÂNICO: AMBIGUO (`stpl:21-22` diz que "o passo é pulado" na trilha rápida sem GATE, sem dizer se é a análise ou o GATE; `plano:83` mantém a análise; a fase que deve ser gravada no ramo "não" não está escrita. Também `tmpl:145` (design curto) × `plano:45-48` (forma do programa sem exceção))

#### S13-F5 · Lacuna de negócio, HITL, parar e devolver ao P.O.
1. INPUT EXATO: "planeja a FT-031" (no Passo 2 aparece: "a regra de desbloqueio não diz o tempo de espera")
   ESTADO: `status.md` `fase: planejando`; PRD aprovado sem esse valor; trilha padrão; HITL.
2. REGRAS:
   - SE lacuna de negócio (regra sem valor) ENTÃO parar: é do P.O. — `plano:33-34`
   - Encaminhar: `sdd-entrevistar`; se muda PRD aprovado, `sdd-prd`; fatia sem épico, `sdd-triar` — `plano:33-34`
   - Nunca decidir regra no plano — `plano:34`
   - Desvio é gravado como `bloqueada (de: <fase>)` com motivo e pergunta exata — `stpl:18-20`
   - `bloqueada` é previsto em `plano:97-98` só para AUTONOMO
3. OUTPUT GERADO: pergunta ao P.O. (texto livre); o plano parcial fica como está.
   ARQUIVOS ESCRITOS: nenhum definido | `status.md`: NÃO-DEFINIDO (`bloqueada (de: planejando)` por `stpl:18-20`, ou sem alteração por `plano:33-34`)
4. VEREDITO MECÂNICO: AMBIGUO (`plano:33-34` manda só parar; `stpl:18-20` diz que desvio é `bloqueada`; `plano:97-98` restringe `bloqueada` ao autônomo)

#### S13-F6 · Divergência ELM × código apontada pela pesquisa
1. INPUT EXATO (1): "planeja a FT-031" (o `research.md` tem "Documentação × código: ELM diz 3 tentativas; código conta 5")
   INPUT EXATO (2): "é documentação velha, segue"
   ESTADO: HITL; `research.md` presente; `status.md` `planejando`.
2. REGRAS:
   - SE divergência ELM × código na pesquisa ENTÃO perguntar antes de seguir (pode ser defeito, pode ser documentação velha) — `plano:28-29`
   - Pergunta enviada; o destino de cada resposta não está escrito
   - Resposta (2): "documentação velha" → nenhuma regra diz o que fazer (seguir, anotar, registrar, encaminhar à `sdd-consolidar`)
3. OUTPUT GERADO (1): pergunta à pessoa. OUTPUT GERADO (2): NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA (a pergunta é determinada; a resposta não tem destino na skill)

#### S13-F7 · Fatia grande demais, propor divisão
1. INPUT EXATO: "planeja a FT-031"
   ESTADO: `requirements.md` 90 linhas + `design.md` 110 + `tasks.md` 60 = 260 linhas no plano; `research.md` com 120 linhas; 12 tarefas; HITL.
2. REGRAS:
   - SE plano passa de ~200 linhas no total ou de ~8 tarefas ENTÃO a fatia está grande: propor à pessoa dividir (`sdd-fatiar`) "em vez de escrever um plano maior" — `plano:52-54`
   - Item 5 vem depois dos itens 0–4 (que escrevem os arquivos), mas o texto diz "em vez de escrever"
   - Modo autônomo → `bloqueada` com a proposta — `plano:53-54`
3. OUTPUT GERADO: proposta de divisão à pessoa; próximo `sdd-fatiar`.
   ARQUIVOS ESCRITOS: `requirements.md`, `design.md`, `tasks.md` já escritos pelos itens 1–3, ou não? NÃO-DEFINIDO
4. VEREDITO MECÂNICO: AMBIGUO (a regra vale, mas não diz se os arquivos já escritos ficam, são apagados ou ficam como rascunho; "no total" também não diz se conta o `research.md`)

#### S13-F8 · Análise independente, AJUSTAR (falta do plano) e nova análise
1. INPUT EXATO: sessão da pessoa, após o Passo 3: "ANALISE: AJUSTAR · falta do plano: L8 — reexecução do `design.md` não tratada" (rodada 1)
   ESTADO: `sdd-revisor` disponível; HITL.
2. REGRAS:
   - Passo 4: Rodadas "revisão do plano" +1; pedir ao `sdd-revisor` a rubrica L — `plano:60-62`
   - SE `AJUSTAR` com falta do plano ENTÃO corrigir o plano e pedir nova análise, até 2 rodadas — `plano:65`
   - Cada achado diz se a falta é do plano ou do PRD/ficha — `rub:43-45`
   - SE `ANALISE: OK` ENTÃO Passo 5 — `plano:64`
3. OUTPUT GERADO: `design.md` corrigido; nova análise com rodada 2.
   ARQUIVOS ESCRITOS: `design.md` (alterado) | `analise-plano-1.md` (AJUSTAR) | `analise-plano-2.md` (na 2ª análise) | `status.md` · Rodadas "revisão do plano" = 2
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S13-F9 · Aprovação em sessão posterior (fase plano-em-revisao)
1. INPUT EXATO: "aprova o plano da FT-031"
   ESTADO: `status.md` `fase: plano-em-revisao`; `analise-plano-1.md` com `ANALISE: OK`; cartão do GATE emitido em sessão anterior; HITL.
2. REGRAS:
   - SE pedido "aprova o plano" ENTÃO a skill é `sdd-plano` — `plano:3`, `iniciar:127`
   - SE aprovado ENTÃO `fase: implementando`, linha no Histórico (quem aprovou), commit dos arquivos do plano — `plano:85`
   - Próximo passo: `sdd-implementar` em sessão nova — `plano:86-87`
   - Nenhuma regra manda reemitir o cartão antes da aprovação (o cartão está no Passo 5, que vem antes da aprovação)
3. OUTPUT GERADO: confirmação de aprovação e próximo passo.
   ARQUIVOS ESCRITOS: `status.md` (`fase: implementando`, Histórico) | commit dos arquivos do plano
4. VEREDITO MECÂNICO: DETERMINISTIC (o "quem aprovou" vem da pessoa; a skill não diz de onde tirar o nome, mas não muda a ação)

#### S13-F10 · Replanejar (implementação descobriu que o plano não serve)
1. INPUT EXATO: relato de `sdd-implementar`: "replaneja a FT-031 · Esperado: cache sem TTL · Encontrado: `cache.java:40` exige TTL · Por que importa: muda a tarefa 3"
   ESTADO: `status.md` `fase: implementando`; tarefas 1–2 `[x]`, 3 `[ ]`; HITL; `sdd-revisor` disponível.
2. REGRAS:
   - SE replanejar ENTÃO atualizar `design.md`/`tasks.md` só no que mudou — `plano:91`
   - Acrescentar tarefas, nunca desmarcar as prontas — `plano:92`
   - Registrar o motivo no Histórico — `plano:92`
   - Repetir Passos 4–5 para a parte alterada — `plano:92-93`
   - Passo 4: Rodadas "revisão do plano" +1 — `plano:60`
   - Passo 3 / Passo 4: `fase: planejando` — `plano:56`
   - Passo 5: GATE → `plano-em-revisao` — `plano:78`
   - Limite "até 2 rodadas" — `plano:65`; o contador zera ou continua no replanejar? não está escrito
   - Mudança de requisito (critério) não é coberta: `plano:91` cita só `design.md`/`tasks.md`
3. OUTPUT GERADO: `design.md` e `tasks.md` alterados; `analise-plano-N.md`; cartão do GATE; `status.md` com motivo.
   ARQUIVOS ESCRITOS: `design.md`, `tasks.md` (alterados) | `analise-plano-2.md` (ou rodada 1 de novo: NÃO-DEFINIDO) | `status.md`
4. VEREDITO MECÂNICO: AMBIGUO (o contador de rodadas e o limite de 2 não dizem se zeram no replanejar; `plano:65`)

#### S13-F11 · Modo autônomo: fase 2 do loop com subagente disponível
1. INPUT EXATO: evento do orquestrador ao `sdd-codificador`: "AUTONOMO=true · FT-031 · worktree .kiro/local/wt/ft-031 · rodada 1 · fase 2 (plano)"
   ESTADO: `research.md` gravado na worktree; `status.md` `planejando`; `steer:88`: codificador com subagente `sdd-revisor`; Plano AFK = aprovação humana.
2. REGRAS:
   - Subagente recebe só AUTONOMO, id, worktree, pasta, comandos e rodada — `loop:75-76`
   - Fase 2 = `sdd-plano`, "Passos 2–3"; sai quando a spec estiver gravada — `loop:84`
   - SE AUTONOMO=true ENTÃO sem perguntas; decisão técnica: recomendada e registrada; lacuna de negócio: `bloqueada` — `plano:95-98`
   - Passo 4: incrementar e pedir ao `sdd-revisor` a rubrica L — `plano:60-62`
   - SE subagente disponível ENTÃO pode pedir o `sdd-revisor` — `plano:62`, `steer:88`
   - `plano:95-98` (modo autônomo) não diz que o codificador para depois do Passo 3
3. OUTPUT GERADO (seguindo `plano`): spec gravada + `analise-plano-1.md` + rodada de análise feita pelo próprio codificador (duplica a fase 3 do loop).
   ARQUIVOS ESCRITOS: spec completa · `analise-plano-1.md` · `status.md` (Rodadas, fase)
4. VEREDITO MECÂNICO: CONFLITO (`loop:84` manda parar em "Passos 2–3" × `plano:60-62` manda fazer o Passo 4 com o subagente; e `loop:75-76` não repassa o limite ao subagente)

#### S13-F12 · Chamada indevida em trilha direta (guarda de entrada)
1. INPUT EXATO: "planeja a FT-040"
   ESTADO: trilha direta; pasta `.kiro/specs/ft-040-…/` com só `status.md`, `fase: implementando`; sem `research.md`, sem `.config.kiro`.
2. REGRAS:
   - SE pedido "planeja" ENTÃO a skill é `sdd-plano` — `plano:3`
   - Entrada: pasta criada pela `sdd-iniciar`, na branch da fatia — `plano:20`
   - Trilha direta não tem spec — `iniciar:53`, `impl:121-124`
   - Nenhuma regra manda recusar, encaminhar à `sdd-triar` ou gravar nada nesse caso
3. OUTPUT GERADO: NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA

#### S13-B1 (borda) · GATE respondido com "não, ajusta o requisito 2"
1. INPUT EXATO: "não, ajusta o requisito 2"
   ESTADO: `status.md` `plano-em-revisao`; cartão do GATE já emitido; HITL.
2. REGRAS:
   - SE aprovado ENTÃO `implementando` — `plano:85` (não se aplica)
   - SE replanejar ENTÃO os passos de `plano:89-93` — gatilho é "implementação descobriu que o plano não serve" (não se aplica)
   - `loop:98` (pediu ajuste → replanejar) vale só para o loop, não para a sessão da pessoa
3. OUTPUT GERADO: NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA

#### S13-B2 (borda) · Segunda análise também AJUSTAR (sessão da pessoa)
1. INPUT EXATO: "ANALISE: AJUSTAR · falta do plano" (rodada 2)
   ESTADO: rodada 2 de análise; HITL; sessão da pessoa.
2. REGRAS:
   - SE AJUSTAR ENTÃO corrigir e pedir nova análise "até 2 rodadas" — `plano:65`
   - Não há regra do que fazer depois da 2ª rodada sem OK em sessão HITL. `loop:85` (`bloqueada`) vale só para o loop
3. OUTPUT GERADO: NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA

#### S13-B3 (borda) · Divergência ELM × código com AUTONOMO=true
1. INPUT EXATO: evento do loop: "AUTONOMO=true · fase 2 (plano)"; o `research.md` tem "Documentação × código: divergência no limite de tentativas"
   ESTADO: codificador em modo autônomo.
2. REGRAS:
   - SE divergência apontada pela pesquisa ENTÃO perguntar antes de seguir — `plano:28-29`
   - SE AUTONOMO=true ENTÃO sem perguntas — `plano:97`
   - `bloqueada` só para lacuna de negócio — `plano:97-98`
3. OUTPUT GERADO: não há saída compatível com as duas regras.
   ARQUIVOS ESCRITOS: NÃO-DEFINIDO
4. VEREDITO MECÂNICO: CONFLITO (`plano:28-29` pede perguntar × `plano:97` proíbe perguntar, e a divergência não entra na lista de bloqueio de `plano:97-98`)

#### S13-B4 (borda) · Limite de tamanho: plano sem `research.md` cabe, com `research.md` não
1. INPUT EXATO: "planeja a FT-031"
   ESTADO: `requirements.md` + `design.md` + `tasks.md` = 190 linhas; `research.md` = 30 linhas; total = 220; 6 tarefas.
2. REGRAS:
   - SE plano passa de ~200 linhas no total ENTÃO dividir — `plano:52`
   - "No total" pode ser os três arquivos do plano ou também o `research.md`
3. OUTPUT GERADO: depende da leitura.
   ARQUIVOS ESCRITOS: depende da leitura
4. VEREDITO MECÂNICO: AMBIGUO (o texto não diz se "total" inclui `research.md`; com 190 linhas a resposta muda)

#### Resumo S13

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S13-F1 plano padrão HITL | DETERMINISTIC | Caminho completo até o commit |
| S13-F2 AFK análise basta | AMBIGUO | Cartão e commit não definidos neste ramo (`plano:67-85`) |
| S13-F3 AFK aprovação humana (loop) | AMBIGUO | "(Passo 0)" de `loop:97` pode ser o do loop ou o do implementar |
| S13-F4 rápida, GATE não | AMBIGUO | `stpl:21-22` não diz qual passo é pulado; fase não gravada no ramo "não" |
| S13-F5 lacuna de negócio (HITL) | AMBIGUO | `plano:33-34` só para; `stpl:18-20` manda `bloqueada` |
| S13-F6 divergência ELM × código | SEM REGRA | Pergunta determinada; a resposta não tem destino |
| S13-F7 fatia grande | AMBIGUO | Escreve antes ou propõe antes? "No total" não diz se conta research |
| S13-F8 análise AJUSTAR (1ª) | DETERMINISTIC | Corrige, nova análise, rodada 2 |
| S13-F9 aprovação posterior | DETERMINISTIC | `plano:85` |
| S13-F10 replanejar | AMBIGUO | Contador de rodadas e limite de 2 não dizem se zeram |
| S13-F11 AUTONOMO fase 2 com subagente | CONFLITO | `loop:84` (Passos 2–3) × `plano:60-62` (Passo 4) |
| S13-F12 guarda de entrada (direta) | SEM REGRA | Nenhuma regra de recusa ou encaminhamento |
| S13-B1 GATE "não" | SEM REGRA | Só `loop:98` cobre ajuste, e só no loop |
| S13-B2 2ª análise AJUSTAR (HITL) | SEM REGRA | `plano:65` para em "até 2 rodadas" |
| S13-B3 divergência em AUTONOMO | CONFLITO | `plano:28-29` × `plano:97` |
| S13-B4 limite com research | AMBIGUO | "No total" é ambíguo |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura confere com o template? | Sucesso (quem grava / commit / branch) | Inacessível / sem permissão / inexistente | Veredito |
|---|---|---|---|---|---|---|---|
| F1 HITL | `P/.config.kiro` | Sim (`plano:40`, `tmpl:9-18`). Normalmente já criado pela `sdd-iniciar` (`ini:95-98`) | **sem extensão** (dotfile), 1 linha JSON; amostra parseia | Sim: `{"specId","workflowType":"requirements-first","specType":"feature\|bugfix"}` (`tmpl:15`). UUID: `uuidgen` ou `python3 -c …` (`tmpl:11-12`); A:codificador só libera `uuidgen.*` (python3 não está na allowlist) | Criado pela `sdd-iniciar` (HITL: `ini:115` só manda commitar "o `status.md`", não o `.config.kiro`) ou pelo plano; **commit só em "Aprovado"** (`plano:85`). No loop, o commit inicial da worktree o inclui (`loop:62-63`) | NÃO ESPECIFICADO (pasta ausente; `uuidgen` ausente, p.ex. Windows) | OK no formato; DIVERGENTE no commit (`ini:115` × `loop:62-63`) |
| F1 HITL | `P/requirements.md` | Sim (`plano:42`) | `.md` | Sim: Introduction/Glossary/Requirements, EARS PT (QUANDO/ENQUANTO/SE…ENTÃO/ONDE … DEVE), critérios `N.M`, `**Origem:**`, `**Falsificável na base:**` (`tmpl:20-52`). A linha "Falsificável na base" aparece uma vez no fim do exemplo — por requisito ou por documento não é dito. A rubrica L não a cobra (ver S15-F2) | Grava quem conduz o plano (pessoa/codificador); commit em `plano:85` | NÃO ESPECIFICADO | OK com ressalva (posição de "Falsificável na base") |
| F4 rápida | `P/bugfix.md` (no lugar de `requirements.md`) | Sim (`plano:42`) | `.md` | Sim: Current/Expected/Unchanged Behavior, Bug Condition, Fix/Preservation Property, itens `1.1/2.1/3.1` (`tmpl:54-83`) | idem | NÃO ESPECIFICADO | OK |
| F1/F4 | `P/design.md` | Sim | `.md` | Padrão: Overview · Architecture (pattern grounding + Forma do programa) · Components · Data Models · Correctness Properties · Error Handling · Testing Strategy (pontos de teste + Contrato de pronto) · Decisões técnicas · Riscos (`tmpl:88-143`) — confere com `plano:45-48`. Rápida: `tmpl:145-146` "curto"; `plano:45-48` não abre exceção; `ini:52` e `sdd/SKILL.md:28` falam em "bugfix.md + tasks.md" sem `design.md` | idem; **decisão técnica "equivalente" altera `design.md` sem novo GATE** (`impl:58`) | NÃO ESPECIFICADO | DIVERGENTE (`ini:52`/`sdd/SKILL.md:28` omitem `design.md` que `plano:45` e `impl:15` exigem) |
| F1/F4 | `P/tasks.md` | Sim | `.md` | Divergências internas: (a) `plano:49-50` "a última é o checkpoint de validação completa **+ revisão**" × `tmpl:170-171` "A revisão não é tarefa daqui"; (b) `tmpl:178` "Toda tarefa diz o comando" × o checkpoint do exemplo e a tarefa opcional `3` não têm "Pronto quando"/comando; (c) tarefa opcional `- [ ]*` (`tmpl:168,174`) nunca fica `[x]` sem regra, e `impl:24` ("primeiro item não marcado") / `impl:67` ("todas as tarefas `[x]`") não tratam opcional nem o checkpoint (que é o Passo 2 em si); (d) subtarefas `1.1/1.2` × "marque `- [x]`" (`impl:46`): não diz se marca pai e filhas | idem | NÃO ESPECIFICADO | DIVERGENTE (a) e (b); NÃO ESPECIFICADO (c) e (d) |
| F1 | `P/analise-plano-<N>.md` | Sim (`rev:55`; A:revisor allow `.kiro/specs/*/analise-*.md`; matcher ok). `<N>` ver S15-F2 | `.md` | Formato `rub:85-101`; última linha `ANALISE: OK\|AJUSTAR` (`rub:43`) | Grava o `sdd-revisor` (subagente). **Revisor não commita** (`rev:20`); quem commita: loop (`loop:93-94`) ou `impl:20-22` na sessão seguinte ("commite-os primeiro"); no HITL `plano:85` "arquivos do plano" não o nomeia | NÃO ESPECIFICADO (sem permissão → revisor não consegue gravar; skill não diz) | NÃO ESPECIFICADO (commit do relatório no caminho plano→GATE) |
| F1 | `P/status.md` | Sim | `.md` | Campos `Fase`, `Rodadas` ("revisão do plano N"), Histórico (`stpl:11,13,42`) | Fases: `planejando` (`plano:56`) → `plano-em-revisao` (`plano:78`, **sem commit**) → `implementando` + Histórico + commit (`plano:85`). O commit grava `implementando`; **o estado `plano-em-revisao` nunca é commitado no HITL**, mas `plano:78` diz que ele "conta no WIP" e `ini:78-79` conta WIP lendo `status.md` "das branches" → plano esperando GATE só é visível no loop (`loop:86` commita antes de pausar) | NÃO ESPECIFICADO | DIVERGENTE (`plano:78` × `plano:85` × `ini:78-79`) |
| F1 | commit "dos arquivos do plano" | Sim (`plano:85`) | — | "arquivos do plano" indefinido: `research.md`, `.config.kiro`, `analise-plano-<N>.md`, `status.md`? `impl:20-22` descontará só `revisao-*`, `analise-*`, `verificacao.md`, `CT.csv`, `evidencias/`, `massa/` — `research/requirements/design/tasks/.config.kiro/status.md` não estão | Quem: sessão da pessoa/codificador (A:codificador tem `git add`/`commit`) — OK; push: não faz (`push` negado ao agente; `plano` não manda push) | n/a | NÃO ESPECIFICADO (conjunto de arquivos) |
| F2 AFK "análise basta" | spec + `analise-plano-<N>.md` + `status.md` | Sim | idem F1 | idem F1 | `plano:81-82`: "quem conduz grava `implementando`", **sem commit** (`plano:85` só no ramo Aprovado). `impl:20-22` vai parar com a árvore suja | NÃO ESPECIFICADO | NÃO ESPECIFICADO (commit) — confirma AMBIGUO; achado de bloqueio, ver abaixo |
| F2 workflow `sdd-planejar-fatia` com "análise basta" / rápida sem GATE | `P/status.md` + spec | Sim | — | — | `wf-plan` passo `ajustar`: "OK sem GATE pendente → **nada mais**": nenhuma fase `implementando` gravada, nenhum commit. O workflow `sdd-entregar-fatia` exige `fase: implementando` (`impl:12-13`) e árvore limpa (`impl:20-22`) → trava | NÃO ESPECIFICADO | DIVERGENTE (`plano:82` "quem conduz grava" × `wf-plan` `ajustar`) |
| F3 AFK aprovação humana (loop) | `PW/` (plano) + `PW/status.md` | Sim: `loop:96` cita `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/` | — | — | Orquestrador commita o plano na worktree e para em `plano-em-revisao` (`loop:86,92-94`) — **este** caminho commita a fase de espera. Aprovação: `implementando` pelo orquestrador (`loop:96-97`) | NÃO ESPECIFICADO | OK |
| F4 rápida GATE não/sim | spec + `status.md` | Sim | — | — | `não`: `plano:83` "segue com `ANALISE: OK`" — não grava `implementando` nem commita (`plano:85` só em "Aprovado"). `stpl:21-22` diz "o passo é pulado" sem dizer qual. No loop, `loop:86` só conhece "Plano AFK"; `GATE na trilha rápida: não` (`steering/sdd.md:63`) não é tratado → a rápida AFK pausaria em `plano-em-revisao` mesmo com GATE `não` | NÃO ESPECIFICADO | NÃO ESPECIFICADO (fase+commit no ramo "não"); DIVERGENTE `loop:86` × `plano:83` |
| F5 lacuna de negócio | `P/status.md`? | `bloqueada (de: planejando)` seria `stpl:18-20`; `plano:33-34` só diz "pare" | — | `bloqueada` exige motivo + pergunta exata (`stpl:18-20`); onde no arquivo (Histórico? Achados abertos?) não é dito | — | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma AMBIGUO |
| F6 divergência ELM × código | (registro da decisão) | — | — | — | `plano:28-29` só manda perguntar; onde registrar a resposta (Histórico? `design.md`?) não é dito | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma SEM REGRA |
| F7 fatia grande | `requirements.md`, `design.md`, `tasks.md` | Sim | — | `plano:52-54` vem depois dos itens 0–4 que já escreveram os arquivos; nada diz se ficam como rascunho, são apagados ou commitados | Autônomo: `fase: bloqueada` com a proposta — em qual arquivo a proposta é gravada? não dito | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma AMBIGUO |
| F8 AJUSTAR / re-análise | `P/analise-plano-<N+1>.md`; `design.md`/`tasks.md` corrigidos | Sim | `.md` | idem | Rodadas: `plano:60` incrementa **antes** de pedir; `wf-plan` incrementa **depois** (passo `ajustar`); `stpl:25-27` "quem pede a rodada". Após 2ª rodada sem `OK`: `plano:65` não diz; só `loop:85` | NÃO ESPECIFICADO | DIVERGENTE (momento do incremento) + NÃO ESPECIFICADO (2ª rodada em HITL) |
| F9 aprovação posterior | `P/status.md` + commit | Sim (`plano:85`) | — | — | Grava `implementando` + Histórico (quem aprovou) + commit — aqui sim | NÃO ESPECIFICADO | OK (DETERMINISTIC confirmado) |
| F10 replanejar | `P/design.md`, `P/tasks.md`, `P/analise-plano-<N>.md`, `P/status.md` | Sim (`plano:91-93`) | — | Pode exigir `requirements.md`/`bugfix.md` (`plano:91` só cita design/tasks). `N` do relatório e contador de rodadas: continua ou zera? não dito | Fase durante o replanejamento (planejando? plano-em-revisao?) e commit: não ditos | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma AMBIGUO |
| F11 autônomo (loop fase 2 / `wf-plan` `plano`) | spec em `PW/` ou `P/` | Sim: A:codificador permite `./**` (inclui `.kiro/local/wt/*/.kiro/specs/*`, matcher ok) | — | — | `plano:95-98` não limita o escopo aos Passos 2–3; `loop:84` e `wf-plan` ("Não rode a análise nem o GATE") limitam. O A:codificador tem `subagent/sdd-revisor` e o prompt dele manda "análise… do subagente sdd-revisor": sem o limite do chamador, o codificador pediria `analise-plano-<N>.md` e incrementaria Rodadas, duplicando a fase 3 do loop (dois relatórios, numeração colidida) | NÃO ESPECIFICADO | DIVERGENTE skill × loop/workflow (confirma CONFLITO da Parte 3) |
| F12 direta / sem pasta | nenhum | `plano:20` presume pasta da `sdd-iniciar`; na direta só há `status.md` e **não há `.config.kiro`** (`ini:97-98`), mas `plano:40` o criaria com `specType: feature` | — | — | Sem recusa/encaminhamento | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma SEM REGRA |
| B1 GATE respondido "não" | — | — | — | — | Nenhuma regra (só `loop:98`) | NÃO ESPECIFICADO | confirma SEM REGRA |

Achados de persistência S13

- `plano:85` é o único ponto de commit do plano e só no ramo "Aprovado". Ficam sem commit: "análise basta" (`plano:81-82`), rápida sem GATE (`plano:83`), `plano-em-revisao` HITL (`plano:78`), replanejar (`plano:91-93`). Consequência em cadeia: `impl:20-22` ("qualquer outra alteração → avise e pare") não desconta `research.md`/`requirements.md`/`design.md`/`tasks.md`/`.config.kiro`/`status.md`.
- `plano:78` × `plano:85` × `ini:78-79`: `plano-em-revisao` conta no WIP lendo `status.md` das branches, mas nunca é commitado no HITL (o commit leva `implementando`). O mesmo vale para `aceita` (gravada pelo verificador, `sdd-verificar/SKILL.md:76`, que não commita).
- `wf-plan` passo `ajustar` ("OK sem GATE pendente → nada mais") nunca grava `implementando` nem commita, contra `plano:82` ("quem conduz grava"). O `wf-ent` exige `fase: implementando` e árvore limpa.
- `tmpl:170-171` × `plano:50` (revisão no checkpoint ou não); `tmpl:174` tarefa opcional `[ ]*` × `impl:24,67` (nunca `[x]`, Passo 2 nunca dispara por leitura literal); checkpoint do exemplo sem `_Requirements_` e sem comando × `tmpl:178`.
- `.config.kiro`: `ini:115` commita só o `status.md` (o `.config.kiro` fica não rastreado até o plano ser aprovado); `loop:62-63` commita ambos. `tmpl:12` oferece `python3`, que o A:codificador não libera (só `uuidgen`).

---


## S14 · sdd-implementar

### Parte 2 — Plano do fluxo esperado (Sonnet)


#### S14-F1 · Implementação padrão (HITL, sessão da pessoa): Passos 0 → 4 → PR
- **Gatilho:** "implementa a FT-031", "executa as tasks", "continua a implementação", "abre o PR", "corrige os achados" (impl:3); ou evento: `fase: implementando` (GATE do plano aprovado) → `sdd-iniciar` encaminha (`sdd-iniciar/SKILL.md:128`). Alternativa Kiro: botão **"Start task"** em `tasks.md` (impl:13; S14-F11).
- **Pré-condições / lê:** `.kiro/specs/<ft>-<slug>/` com plano aprovado (fase `implementando`), na branch da fatia (impl:12-13); lê `design.md` inteiro, `research.md`, `.kiro/steering/sdd.md` (comandos, regras críticas, regras aprendidas) (impl:15-16).
- **Processamento:**
  1. **Passo 0 — Onde estou:** branch = a do `status.md` (senão avisa e para); `git status` limpo **descontando** relatórios de outros papéis (`revisao-*.md`, `analise-*.md`, `verificacao.md`, `CT.csv`, `evidencias/`, `massa/`), que são commitados primeiro (`FT-<nnn> registrar revisão/verificação`); qualquer outra alteração → avisa e para (impl:20-22). Atualiza: `git pull --ff-only` (com upstream) ou `git fetch` (worktree nova) (impl:23-24). Retoma do **primeiro item não marcado** do `tasks.md`; achados abertos viram tarefas `[R<n>]` no fim (S14-F3) (impl:24-27). Roda os testes uma vez: vermelho antes de começar = ambiente/base, registra e avisa, não conserta (impl:28-29).
  2. **Passo 1 — por tarefa:** (a) carrega a skill da stack que a tarefa cita; (b) **vermelho**: teste pelo ponto de teste do `design.md`, só ele, falha pelo motivo certo (corretiva: o teste que reproduz o defeito primeiro); (c) **verde**: menor mudança imitando o análogo; (d) arruma só o que escreveu; (e) **backpressure**: compilar + testes da área + lint (comandos do `sdd.md`); (f) marca `- [x]` e commit pequeno com id da fatia; (g) linha no Histórico `<data> — tarefa N ok · <testes> · <commit curto>` (impl:33-47). Regras do ciclo (impl:49-65): nunca apagar/desabilitar/enfraquecer teste; divergência → S14-F4; nada fora do escopo; duas correções sem sair do lugar → registra e continua em sessão nova, persistindo `bloqueada`; banco só leitura, DDL é do time de banco (campo Banco); contexto cheio → atualiza `status.md` e continua em sessão nova.
  3. **Passo 2 — Validação completa:** com todas `[x]`: compilar, suíte **inteira**, lint; cobertura com gate do `sdd.md` medida nos arquivos da fatia; erro de ambiente → `AMBIENTE` no `status.md` (impl:67-71).
  4. **Passo 3 — Revisão independente:** `fase: revisando`; incrementa "revisão do código" em Rodadas; chama `sdd-revisor` (subagente) com rubrica **C** passando só id da fatia, pasta, branch/worktree e rodada ("nunca o seu raciocínio"); ele grava `revisao-codigo-<N>.md` (impl:73-78). `APROVADO` → Passo 4; `REVISAR` → S14-F5; 2ª reprovação → S14-F6.
  5. **Passo 4 — Verificação de aceite:** incrementa "verificação" em Rodadas e segue para `sdd-verificar` (de preferência pelo agente `sdd-verificador`): `ACEITO` → fase `aceita`; `REJEITADO` → devolve cenários reprovados (Passo 0) (impl:85-89; S14-F7).
  5. **Passo 5 — PR:** S14-F8.
- **Output:** código + testes commitados em commits pequenos (id da fatia); `tasks.md` com `[x]`; `status.md` (Histórico por tarefa, Rodadas, fase); `revisao-codigo-<N>.md`, `verificacao.md`, `CT.csv` (gerados por outros papéis); depois `fase: pr-aberto` e link do PR. Próximo: merge por uma pessoa e **`sdd-consolidar`** (impl:119).
- **Lacunas:**
  - **`status.md` e commits:** o passo 1(g) escreve no Histórico *depois* do commit (1(f)); o `status.md` fica sujo e o Passo 0 da próxima sessão exige árvore limpa descontando só os relatórios (impl:20-22) — `status.md` não está na lista de exceções. Idem para plano não commitado (ver S13-F2).
  - `vermelho antes de começar` (impl:28-29): "registre e avise" — não diz se continua ou para; o backpressure por tarefa não faz sentido com base vermelha (o `steer:39` diz "Falha de ambiente → AMBIENTE, nunca consertar").
  - `AMBIENTE` no Passo 2 (impl:70-71): sem fase/handoff (a `rub:80` trata AMBIENTE na revisão e a `sdd-verificar/SKILL.md:84` manda `bloqueada`; aqui não).
  - Template do PR usa `(EP-<nn> · IB <id ELM | —>)` (impl:104) sem variante para fatia sem épico (`— (sem épico)` em `stpl:5`).

#### S14-F2 · Trilha rápida (corretiva)
- **Gatilho:** fatia rápida com plano aprovado (`bugfix.md` + `design.md` curto + `tasks.md`); mesmas frases de F1 / "corrigir o defeito 4567" (via iniciar).
- **Processamento:** F1 com as diferenças já dentro do ciclo: tarefa 1 = teste que reproduz o defeito (vermelho), tarefa 2 = testes de preservação (verdes antes e depois) (`tmpl:85-86`; impl:38-39 "Corretiva: o teste que reproduz o defeito vem primeiro"). Revisão rubrica C com `bugfix.md` no lugar de `requirements.md` (rub:56); verificação parte do `bugfix.md` (`sdd-verificar/SKILL.md:30-31`); PR.
- **Output:** como F1; no PR, "Cobre:" sem HF/REG (impl:106 não prevê `cobre` vazio).
- **Lacunas:** o texto do PR (impl:104-112) não tem variante da rápida (sem `HF`, `IB`, `cenários`); "Aceite: verificacao.md (ACEITO, <n> cenários)" (impl:108) não define o "n" para `bugfix.md`.

#### S14-F3 · Corrigir achados (revisão / verificação / PR / pessoa) — tarefas `[R<n>]`
- **Gatilho:** "corrige os achados" (impl:3); retorno da revisão `REVISAR` (impl:81), cenários `REJEITADO` da verificação (impl:88-89), comentários do PR ou achados da seção "Achados abertos" do `status.md` (impl:25-26).
- **Processamento:** Passo 0: acrescenta, numeradas em sequência no fim do `tasks.md`, tarefas `- [ ] 7. [R1] <achado> — origem: revisao-codigo-2.md` para: (a) "Achados abertos" do `status.md` (PR, pessoa); (b) achados do último `revisao-codigo-<N>.md` com `VEREDITO: REVISAR`; (c) cenários rejeitados do `verificacao.md` (impl:24-27); as anteriores estão marcadas, então as `[R]` são as primeiras não marcadas. Depois: ciclo do Passo 1 por tarefa (teste vermelho → verde → backpressure → commit); marca no `status.md` "resolvido — tarefa <n>" (`stpl:31-32`). Volta ao Passo 2 (impl:81).
- **Output:** novas tarefas `[R<n>]` marcadas, commits, `status.md` com Situação "resolvido — tarefa <n>".
- **Lacunas:**
  - Após corrigir cenários **rejeitados da verificação**, o `impl` não diz se volta pelo Passo 3 (nova revisão C) ou direto ao Passo 4 (impl:88-89 "Passo 0"; `sdd-verificar/SKILL.md:82-83` "a verificação roda de novo", sem nova revisão; `loop:89` "volta à 5 uma vez", sem dizer se a fase 6 repete). Contador de "revisão do código" e limite de 2 rodadas depois disso: indefinidos.
  - Achado vindo do **PR aberto** (fase `pr-aberto`): não há transição definida de `pr-aberto` de volta a `implementando`, nem se exige nova revisão/verificação.
  - Achado de revisão que seja "do plano" (rub:43-45 diz "do plano / do PRD"): o `impl` só trata no relatório de divergência (S14-F4), não ao receber `REVISAR`.

#### S14-F4 · Divergência plano × código (pare e reporte)
- **Gatilho:** durante o ciclo, o código real não bate com o plano (impl:52).
- **Processamento:** **pare**, sem improvisar; reporta no formato `Divergência na tarefa N — Esperado: … · Encontrado: … arquivo:linha · Por que importa: …` (impl:53-56). Encaminhamento: muda comportamento de negócio → P.O. (`sdd-entrevistar` / `sdd-prd`); muda o desenho → `sdd-plano` (replanejar, S13-F10); decisão técnica equivalente → decide e registra no `design.md` (Decisões técnicas) (impl:57-58). Autônomo: registra bloqueio/`bloqueada`.
- **Output:** mensagem de divergência (e, se a fase mudar, `status.md` `bloqueada (de: implementando)`); eventualmente `design.md` com a decisão técnica.
- **Lacunas:** HITL não diz se grava `bloqueada` ou registra no `status.md`; o workflow `sdd-entregar-fatia` pede "registre a pergunta (ou Esperado / Encontrado / Por que importa) no status.md" (wf-ent) — a skill não. A decisão técnica "equivalente" altera `design.md` aprovado sem novo GATE (impl:58); o limite do que é "equivalente" não está definido.

#### S14-F5 · Revisão independente → `REVISAR` (1ª rodada) e re-revisão
- **Gatilho:** `revisao-codigo-<N>.md` com `VEREDITO: REVISAR` (impl:80-81).
- **Processamento:** corrige **só** os achados (como `[R<n>]`, Passo 0), volta ao Passo 2 (validação completa) e depois ao Passo 3 com rodada seguinte; "até 2 rodadas" (impl:81).
- **Output:** `revisao-codigo-<N+1>.md`; `fase: revisando`; Rodadas "revisão do código".
- **Lacunas:** quem incrementa Rodadas difere: `impl:75` incrementa antes de pedir; o workflow `sdd-entregar-fatia` incrementa "se existe `revisao-codigo-<N>.md` mais novo que a última rodada registrada" no passo do codificador (wf-ent). Em `stpl:25-27` "quem pede a rodada".

#### S14-F6 · Segunda reprovação → `bloqueada` com 3 opções
- **Gatilho:** 2ª `REVISAR` (impl:82).
- **Processamento:** `fase: bloqueada`; mostra à pessoa os relatórios e as opções: (a) orientar a correção (zera as rodadas), (b) voltar ao plano, ou (c) aceitar explicitamente os achados restantes (quem e por quê no `status.md`) (impl:82-84).
- **Output:** `status.md` `bloqueada (de: revisando)` com motivo; decisão da pessoa; seguinte: Passo 0 (a), `sdd-plano` (b) ou Passo 4 (c).
- **Lacunas:** "zera as rodadas" (a) conflita com a numeração `<N>` do arquivo (`rub:55-56` usa "próxima rodada" — contagem por arquivo existente?) — ver S15-F3. No loop o tratamento é só "bloqueada" sem as 3 opções (`loop:88,105-106`) e o workflow usa `onMaxIterations: pause` (wf-ent).

#### S14-F7 · Verificação de aceite (Passo 4) — ACEITO / REJEITADO / só ambiente
- **Gatilho:** revisão `APROVADO` (impl:80,85).
- **Processamento:** incrementa "verificação" em Rodadas e segue para `sdd-verificar` (de preferência pelo `sdd-verificador`). `ACEITO` → ela deixa `fase: aceita` (e gera `CT.csv`); `REJEITADO` → devolve cenários reprovados à `sdd-implementar` (S14-F3) (impl:85-89; `sdd-verificar/SKILL.md:76-84`); só ambiente → `bloqueada`.
- **Output:** `verificacao.md`, `CT.csv`, `fase: aceita` (ACEITO).
- **Lacunas:** `stpl:25-27` e `sdd-verificar/SKILL.md:92-93` dizem que o verificador **não** incrementa Rodadas, mas o workflow `sdd-entregar-fatia` manda o verificador "Incremente 'verificação' em Rodadas no status.md" e gravar a fase (wf-ent). O `impl:85` não trata o caso `bloqueada` por ambiente.

#### S14-F8 · Abertura do PR (Passo 5) — sessão da pessoa, e branch desatualizada
- **Gatilho:** "abre o PR" (impl:3); `fase: aceita` (revisão `APROVADO` e verificação `ACEITO`) (impl:93; `sdd-iniciar/SKILL.md:130`).
- **Processamento:** (1) `git fetch`, compara com `origin/<base>`: desatualizada → numa sessão com a pessoa, com o "sim" dela, `git merge origin/<base>` (conflito → resolve e repete Passos 2–4); como agente, para e devolve "branch desatualizada com a base" (impl:98-101). (2) Monta o texto do PR (título `FT-<nnn> — <título> (EP · IB)`, O quê, Cobre, Plano, Revisão, Backpressure, Banco (DDL), Como ler, Reversível?) (impl:102-114). (3) **Uma** confirmação da pessoa para push + abertura com a ferramenta do `sdd.md` (sem ferramenta → entrega título e descrição) (impl:115-116). (4) `status.md`: `fase: pr-aberto` + link; commit e push com o mesmo "sim" (impl:117).
- **Output:** PR aberto (ou texto pronto); `status.md` `pr-aberto` commitado e enviado. Próximo: merge por uma pessoa → `sdd-consolidar` (impl:119).
- **Lacunas:**
  - A `sdd-loop` não tem passo para o retorno "branch desatualizada com a base" nem para quando o orquestrador "faz o merge": o impl:100-101 diz que o merge é "sempre de uma pessoa", e `loop:90` só trata push/PR (fica sem tratamento no AFK).
  - Passo 3 do impl (PR) exige que a base seja a do `sdd.md`; o orquestrador/pessoa: `steer:61` (PR curto para artefatos de produto) — não relacionado a esse passo.

#### S14-F9 · Pronta para o PR / pronta para a revisão (agente `sdd-codificador` sem push e sem subagente)
- **Gatilho:** execução do `sdd-codificador` (sem push; pode ter ou não subagente) ao chegar em Passo 3 ou Passo 5.
- **Processamento:** Passo 3: "Sem subagente disponível (você é um agente sem essa ferramenta) → pare aqui e devolva a quem chamou: 'pronta para a revisão (rodada <N>)'" (impl:76-78). Passo 5: "Como agente `sdd-codificador`, que não faz push, pare em 'pronta para o PR' e entregue o título e a descrição do item 2" (impl:95-97).
- **Output:** mensagem de handoff com rodada, ou título + descrição do PR.
- **Lacunas:** o `sdd-codificador` **tem** `subagent/sdd-revisor` (`sdd-setup/assets/agents/sdd-codificador.json`), então a condição "agente sem essa ferramenta" quase nunca vale; mas o prompt do agente manda "Análise do plano e revisão do código são do subagente sdd-revisor… sem a ferramenta → devolva" — consistente. A fronteira entre esse caminho e o autônomo (F10) é nebulosa: o codificador do loop **também** tem o subagente e, pelo texto do `impl`, rodaria o Passo 3 sozinho.

#### S14-F10 · Modo autônomo (`AUTONOMO=true`: sdd-loop / workflow `sdd-entregar-fatia`)
- **Gatilho:** `loop` fase 5 (`sdd-codificador`, "Passos 0–2", loop:87) e fases 6–8 (revisor, verificador, orquestrador); ou passos `implementar` do workflow ("Passos 0 a 2… Não peça revisão, não faça push nem abra PR", wf-ent).
- **Processamento:** sem perguntas; trabalha só na worktree recebida (`cd .kiro/local/wt/<ft> && <cmd>`, loop:67-70); **não** faz push nem abre PR (o orquestrador faz); bloqueio vira `fase: bloqueada` com o motivo e para (impl:131-134). Executa Passos 0–2 (ver F1/F3); o orquestrador gerencia Rodadas, a revisão (fase 6), a verificação (fase 7) e a entrega (fase 8) (loop:87-90).
- **Output:** tarefas `[x]` + backpressure verde, commits na worktree, `status.md` atualizado; ou `bloqueada` com motivo.
- **Lacunas (alta gravidade):**
  - O modo autônomo (impl:131-134) **não limita o escopo a "Passos 0–2"**: quem limita é o `loop:87` e o workflow. Sem isso, o `sdd-codificador` (que tem `subagent/sdd-revisor`) pelo texto da skill executaria o Passo 3 (revisão) e Passo 4 (verificação via `sdd-verificar`) — duplicando as fases 6–7 do orquestrador e o contador de Rodadas.
  - "Duas correções seguidas sem sair do lugar → continue numa sessão nova" (impl:60-62) não se aplica no autônomo: deveria ir direto a `bloqueada` (não dito).
  - "Divergência" no autônomo: só "bloqueio vira `bloqueada`" (impl:133-134); o formato Esperado/Encontrado é do HITL.

#### S14-F11 · "Start task" do Kiro — execução de uma única tarefa
- **Gatilho:** botão **Start task** / **Run all tasks** do `tasks.md` (impl:13; `tmpl:3-4,179-181`).
- **Processamento:** "As regras valem igual" (impl:13): cada tarefa roda o ciclo do Passo 1 (skill da stack → vermelho → verde → arrumar → backpressure → `[x]` + commit + Histórico). O **Run all tasks** pode rodar tarefas independentes em paralelo (`tmpl:179-181`).
- **Output:** a tarefa marcada, commit, Histórico.
- **Lacunas:** Passo 0 (branch correta, `git status` limpo, testes rodados antes de mexer) e Passos 2–5 não têm gatilho nesse modo; execução paralela de tarefas conflita com "uma tarefa por vez" (impl:31) e com o Passo 0 (testes antes de mexer) — a skill não trata.

#### S14-F12 · Trilha direta (sem spec, sem `tasks.md`)
- **Gatilho:** fatia de trilha direta (diff cabe numa frase, tamanho P), pasta só com `status.md`, `fase: implementando` (impl:121-124; `sdd-iniciar/SKILL.md:53,97-98`); mencionado como "(trilha direta: a seção Trilha direta)" no encaminhamento (`sdd-iniciar/SKILL.md:128`).
- **Processamento:** (1) teste que falha, quando há comportamento (texto/configuração pura não têm); (2) a mudança; (3) backpressure; (4) revisão pela `sdd-revisar` (rubrica C sobre o diff, com o **pedido** no lugar dos critérios; relatório na conversa); (5) PR curto: `FT-<nnn> — <pedido> (<id do item | —>)` · O quê · Backpressure · `Revisão: APROVADO` · Como ler; `status.md` com `fase: pr-aberto` + link do PR (impl:125-128). Se surgir regra de negócio ou mais de um comportamento → pare e devolva à `sdd-triar` (é rápida ou padrão) (impl:128-129).
- **Output:** código/testes + commit(s); relatório de revisão só na conversa; PR curto; `status.md` `pr-aberto`.
- **Lacunas:**
  - **Revisão `REVISAR`/limite de rodadas/`bloqueada`** não são definidos para a direta (impl:121-129 não tem equivalente de impl:80-84); sem Rodadas nem fase `revisando`.
  - "Relatório na conversa" (impl:127; `rev:30`) contradiz `rev:54-58` ("grave o relatório na pasta do artefato") e as permissões do agente revisor (só grava `revisao-*.md`/`analise-*.md` em `.kiro/specs/*/`).
  - O PR da direta cita "Revisão: APROVADO" sem arquivo; Passos 2 (validação completa), 4 (verificação) e `sdd-consolidar` pós-merge não estão definidos para a direta.
  - Autônomo: o loop exclui a direta (loop:30) — ok; mas `impl:131-134` não diz.
  - Push/branch: o Passo 0 e a Regras (impl:138) valem; "PR curto" usa a ferramenta do `sdd.md` e confirmação — não repetido na seção.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


#### S14-F1 · Implementação padrão, HITL, sessão da pessoa (Passos 0 → 5)
1. INPUT EXATO: "implementa a FT-031"
   ESTADO: branch = a do `status.md`; árvore limpa e commitada; upstream existe; `status.md` `fase: implementando`; tarefas 1–3 `[x]`, tarefa 4 `[ ]`; sem achados abertos; testes verdes na base; `sdd-revisor` e `sdd-verificador` disponíveis; `origin/develop` sem commits novos; sessão da pessoa.
2. REGRAS:
   - SE `fase: implementando` na branch da fatia ENTÃO entrar — `impl:12-13`
   - Ler `design.md`, `research.md`, `sdd.md` — `impl:15-16`
   - Passo 0: branch = a do `status.md` — `impl:20`
   - Passo 0: árvore limpa (relatórios descontados) — `impl:20-22`
   - Passo 0: `git pull --ff-only` (tem upstream) — `impl:23`
   - Passo 0: retomar do primeiro item não marcado (tarefa 4) — `impl:24-27`
   - Passo 0: testes uma vez, verdes — `impl:28-29`
   - Passo 1, tarefa 4: skill da stack → teste vermelho pelo ponto de teste → verde → arrumar → backpressure → `[x]` + commit → linha no Histórico — `impl:35-47`
   - Regras do ciclo: nada apagado nem enfraquecido; sem divergência; escopo — `impl:50`, `impl:52`, `impl:59`
   - SE todas `[x]` ENTÃO Passo 2: compilar, suíte inteira, lint, cobertura — `impl:67-71`
   - Passo 3: `fase: revisando`; Rodadas "revisão do código" +1; pedir ao `sdd-revisor` a rubrica C (id, pasta, branch, rodada) — `impl:73-76`
   - SE `VEREDITO: APROVADO` ENTÃO Passo 4 — `impl:80`
   - Passo 4: Rodadas "verificação" +1; `sdd-verificar` (de preferência `sdd-verificador`) — `impl:85-87`
   - SE `ACEITO` ENTÃO `fase: aceita` — `verif:76`
   - Passo 5: branch atualizada com a base → sem merge necessário — `impl:98`
   - Passo 5: texto do PR — `impl:102-114`
   - Passo 5: "numa só confirmação da pessoa": push e abertura do PR — `impl:115-116`
   - Passo 5: `fase: pr-aberto`, link, commit e push com o mesmo "sim" — `impl:117`
3. OUTPUT GERADO: depois de Passo 1 e de Passos 2–4, a resposta mostra o texto do PR (`impl:103-113`) e pede a confirmação única (`impl:115`).
   ARQUIVOS ESCRITOS: `tasks.md` (tarefa 4 `[x]`) | código e testes (commits pequenos) | `status.md` (Histórico, Rodadas, fase revisando → aceita → pr-aberto) | `revisao-codigo-1.md` (`sdd-revisor`) | `verificacao.md` e `CT.csv` (`sdd-verificar`)
4. VEREDITO MECÂNICO: DETERMINISTIC (dentro da mesma sessão. O `status.md` fica sujo entre o Histórico e o commit final; o problema aparece só na sessão seguinte, em S14-B1)

#### S14-F2 · Trilha rápida (corretiva) até o PR
1. INPUT EXATO: "corrige o defeito 4567 (FT-040)"
   ESTADO: trilha rápida; `bugfix.md`, `design.md` curto e `tasks.md` (1 = teste que reproduz o defeito; 2 = preservação), tudo `[ ]`; `fase: implementando`; `cobre` vazio; sem épico; `sdd-revisor` disponível.
2. REGRAS:
   - Corretiva: o teste que reproduz o defeito vem primeiro — `impl:39-40`
   - Passos 0–2 e 1 por tarefa como em S14-F1 — `impl:18-47`
   - Revisão rubrica C, com `bugfix.md` no lugar de `requirements.md` — `rub:56`, `impl:73-78`
   - Verificação parte de `bugfix.md` — `verif:30-31`
   - Passo 5: PR com o template de `impl:104-112`: `FT-<nnn> — <título> (EP-<nn> · IB <id ELM | —>)`, `Cobre: HF-01 · 1.1 …`, `Aceite: verificacao.md (ACEITO, <n> cenários com evidência)`
   - Não existe variante do template de PR para a trilha rápida: `EP-<nn>` não existe (sem épico), `Cobre` vem vazio, e não está definido o que é `<n>` para `bugfix.md`
3. OUTPUT GERADO: PR com o template de `impl:104-112` e campos sem valor definido.
   ARQUIVOS ESCRITOS: como S14-F1 (`tasks.md`, código, testes, `status.md`, `revisao-codigo-1.md`, `verificacao.md`, `CT.csv`)
4. VEREDITO MECÂNICO: AMBIGUO (o template de PR não tem variante para trilha rápida: `EP-<nn>`, `Cobre` vazio e `<n> cenários` com `bugfix.md`, `impl:104-108`)

#### S14-F3 · Corrigir achados numa sessão nova (fase revisando)
1. INPUT EXATO: "corrige os achados da revisão"
   ESTADO: sessão nova; `status.md` `fase: revisando`; `revisao-codigo-1.md` com `VEREDITO: REVISAR` (achados C2 e C4); "Achados abertos" vazio; tarefas 1–6 `[x]`.
2. REGRAS:
   - Entrada: `fase: implementando` — `impl:12`
   - Fase `revisando` roteia para `sdd-implementar` — `iniciar:128`
   - Passo 0: acrescentar tarefas `[R<n>]` no fim do `tasks.md` com os achados de `revisao-codigo-1.md` com `REVISAR` — `impl:24-27`
   - Passo 1 por tarefa `[R]` — `impl:31-47`
   - Marcar no `status.md`: `resolvido — tarefa <n>` — `stpl:31-32`
   - SE `REVISAR` ENTÃO corrigir só os achados e voltar ao Passo 2 — `impl:81`
   - Passo 3 de nova rodada: Rodadas +1 — `impl:75`
3. OUTPUT GERADO: tarefas `[R1]` e `[R2]` no `tasks.md`, código, `status.md` com "resolvido".
   ARQUIVOS ESCRITOS: `tasks.md` (novas tarefas) | código e testes | `status.md`
4. VEREDITO MECÂNICO: AMBIGUO (`impl:12` exige `fase: implementando` para entrar, mas `iniciar:128` manda `revisando` para `sdd-implementar`; o texto não diz se a sessão deve parar ou seguir)

#### S14-F4 · Divergência plano × código (pare e reporte)
1. INPUT EXATO: no meio da tarefa 3, o código real tem `LoginService.java:42` usando `Instant`, e o `design.md` diz `LocalDateTime`
   ESTADO: sessão da pessoa; `status.md` `implementando`; HITL.
2. REGRAS:
   - SE código não bate com o plano ENTÃO pare e reporte no formato "Divergência na tarefa N — Esperado · Encontrado · Por que importa" — `impl:52-56`
   - Muda comportamento de negócio → P.O. — `impl:57`
   - Muda o desenho → `sdd-plano` (replanejar) — `impl:57`
   - Decisão técnica equivalente → decidir e registrar no `design.md` — `impl:58`
   - "Equivalente" não tem critério escrito
   - Registrar bloqueio no `status.md` em HITL: não está escrito (`stpl:18-20` fala em desvio → `bloqueada`)
3. OUTPUT GERADO: mensagem de divergência; `design.md` (se decisão equivalente).
   ARQUIVOS ESCRITOS: `design.md` (se equivalente) | `status.md`: NÃO-DEFINIDO
4. VEREDITO MECÂNICO: AMBIGUO (`Instant` × `LocalDateTime`: é "decisão técnica equivalente" (`impl:58`) ou "muda o desenho" (`impl:57`)? A skill não diz)

#### S14-F5 · REVISAR na 1ª rodada, na mesma sessão
1. INPUT EXATO: o `sdd-revisor` devolveu `revisao-codigo-1.md` com `VEREDITO: REVISAR` (achados C2 e C4); a sessão continua: "corrige os achados"
   ESTADO: `fase: revisando` gravada no Passo 3 desta sessão; Rodadas revisão do código = 1; HITL.
2. REGRAS:
   - SE `REVISAR` ENTÃO corrigir só os achados, como `[R<n>]` (Passo 0) — `impl:81`, `impl:24-27`
   - Volta ao Passo 2 e depois ao Passo 3 da rodada seguinte — `impl:81`
   - Passo 3: Rodadas +1 antes de pedir — `impl:75`
   - Revisor grava `revisao-codigo-2.md` com `<N>` = próxima rodada — `rev:55-56`
   - "Até 2 rodadas" — `impl:81`
3. OUTPUT GERADO: tarefas `[R1]`, `[R2]` concluídas; `revisao-codigo-2.md`.
   ARQUIVOS ESCRITOS: `tasks.md` | código e testes | `revisao-codigo-2.md` | `status.md` (Rodadas = 2)
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S14-F6 · Segunda reprovação → bloqueada com três opções
1. INPUT EXATO: o `sdd-revisor` devolveu `revisao-codigo-2.md` com `VEREDITO: REVISAR` (mesma sessão)
   ESTADO: Rodadas revisão do código = 2; HITL.
2. REGRAS:
   - SE 2ª reprovação ENTÃO `fase: bloqueada`; mostrar relatórios e as opções (a) orientar a correção, (b) voltar ao plano, (c) aceitar explicitamente os restantes — `impl:82-84`
   - Desvio é `bloqueada (de: revisando)` com motivo — `stpl:18-20`
   - Opção (a): "zera as rodadas" — `impl:82-83`
   - Revisor grava `revisao-codigo-<N>.md` com `<N>` = próxima rodada — `rev:55-56`
   - Rodadas: quem pede a rodada incrementa — `stpl:25-27`
   - Destino de (a), (b), (c) depois da escolha: não está escrito (a leitura de Passo 0, `sdd-plano` e Passo 4 é inferência)
3. OUTPUT GERADO: `status.md` `bloqueada (de: revisando)` + menu de opções.
   ARQUIVOS ESCRITOS: `status.md` (fase, motivo, Rodadas)
4. VEREDITO MECÂNICO: CONFLITO (`impl:82-83` manda zerar as rodadas na opção (a) × `rev:55-56` manda numerar o relatório como "próxima rodada" pelos arquivos já existentes; zerado, o próximo relatório seria `revisao-codigo-1.md`, que já existe)

#### S14-F7 · Verificação de aceite, ACEITO
1. INPUT EXATO: "verifica a FT-031" (sessão da pessoa, depois de `revisao-codigo-1.md` com `APROVADO`)
   ESTADO: `sdd-verificador` disponível, sem MCP do ELM nesta sessão; massa por script; ambiente local; campo Banco = `não se aplica`; cenários de `design.md`.
2. REGRAS:
   - Passo 4: Rodadas "verificação" +1; seguir para `sdd-verificar` — `impl:85-87`
   - Roteiro: `status.md` `verificando`; `verificacao.md` escrito antes de executar — `verif:27`, `verif:29-31`
   - Executar cenário a cenário, registrar resultado e evidência — `verif:52-58`
   - SE todos aceitos ENTÃO gerar `CT.csv`, `fase: aceita`, e devolver — `verif:76`, `verif:88-90`
   - Horas da `[VER]`: sem MCP → `ELM pendente: lançar <h>h em [VER] FT-nnn` no Histórico — `verif:77-80`
   - Verificador não incrementa Rodadas — `verif:92-93`
3. OUTPUT GERADO: `🔎 Verificação FT-031 — rodada 1 · Cenários: N aceitos · VERIFICACAO: ACEITO` (`verif:70-74`).
   ARQUIVOS ESCRITOS: `verificacao.md` · roteiro e registros | `CT.csv` (`verif:88-90`, `ct-csv.md`) | `status.md` · `fase: aceita` + Histórico (`ELM pendente`)
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S14-F8 · Abertura do PR com branch desatualizada (sem conflito)
1. INPUT EXATO: "abre o PR da FT-031"
   ESTADO: `fase: aceita`; branch 2 commits atrás de `origin/develop`, sem conflito; pessoa presente; `gh` disponível (`steer`: ferramenta de PR).
2. REGRAS:
   - SE `fase: aceita` ENTÃO Passo 5 — `impl:93`
   - Passo 5.1: `git fetch`, comparar com `origin/<base>` — `impl:98`
   - SE desatualizada e numa sessão com a pessoa ENTÃO, com o "sim" dela, `git merge origin/<base>` — `impl:98-100`
   - "Conflito → resolva e repita Passos 2–4" — `impl:99`
   - Passo 5.2: texto do PR — `impl:102-114`
   - Passo 5.3: uma confirmação para push e abertura — `impl:115-116`
   - Passo 5.4: `fase: pr-aberto` + commit/push com o mesmo "sim" — `impl:117`
   - Merge é de uma pessoa — `impl:100-101`, `impl:119`
3. OUTPUT GERADO: pergunta: "branch 2 commits atrás de origin/develop: confirma o merge?" (`impl:98-100`). Depois do "sim": merge, PR text, confirmação única.
   ARQUIVOS ESCRITOS: nenhum antes do "sim" | depois: merge commit na branch | `status.md` `pr-aberto`
4. VEREDITO MECÂNICO: AMBIGUO ("conflito → resolva e repita Passos 2–4" (`impl:99`) pode ser lido como: repetir 2–4 só quando há conflito, ou sempre que a branch estava atrás)

#### S14-F9 · Pronta para revisão (codificador sem subagente)
1. INPUT EXATO: "implementa a FT-031" (dispara o `sdd-codificador` como agente, sem a ferramenta de subagente nesta sessão)
   ESTADO: tarefas `[x]`; Passo 2 concluído e verde; agente sem push; `steer:88` diz que o codificador tem o `sdd-revisor`, mas nesta sessão a ferramenta não foi concedida.
2. REGRAS:
   - Passo 3: `fase: revisando`; Rodadas "revisão do código" +1 — `impl:75`
   - SE sem subagente disponível ENTÃO pare e devolva "pronta para a revisão (rodada <N>)" — `impl:76-78`
   - Quem conduz a sessão grava a fase — `stpl:23-24`
   - Agente codificador não faz push e para em "pronta para o PR" no Passo 5 — `impl:95-96`
3. OUTPUT GERADO: "pronta para a revisão (rodada 1)".
   ARQUIVOS ESCRITOS: `status.md` · `fase: revisando` + Rodadas 1
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S14-F10 · Modo autônomo: fase 5 do loop
1. INPUT EXATO: evento do orquestrador ao `sdd-codificador`: "AUTONOMO=true · FT-031 · worktree .kiro/local/wt/ft-031 · rodada 1 · fase 5 (implementação)"
   ESTADO: plano aprovado; `status.md` `implementando`; tarefas 1–N `[ ]`; `steer:88`: codificador com `sdd-revisor`.
2. REGRAS:
   - Subagente recebe só AUTONOMO, id, worktree, pasta, comandos e rodada — `loop:75-76`
   - Fase 5 = `sdd-implementar`, "Passos 0–2" — `loop:87`
   - SE AUTONOMO=true ENTÃO sem perguntas; trabalhar só na worktree; sem push nem PR; bloqueio → `bloqueada` e para — `impl:131-134`
   - Passo 3 (revisão) com subagente disponível pede o `sdd-revisor` — `impl:75-76`
   - `impl:131-134` não limita o escopo aos Passos 0–2
3. OUTPUT GERADO (seguindo `impl`): tarefas `[x]`, Passo 2, Passo 3 com `sdd-revisor` e, pelo Passo 4, `sdd-verificar`.
   ARQUIVOS ESCRITOS: código, testes, `tasks.md`, `status.md`, `revisao-codigo-1.md`, `verificacao.md`
4. VEREDITO MECÂNICO: CONFLITO (`loop:87` manda parar em "Passos 0–2" × `impl:73-78` e `impl:85-87`, que mandam seguir para revisão e verificação; `impl:131-134` não diz o limite, e o subagente não recebe o limite, `loop:75-76`)

#### S14-F11 · "Start task": execução de uma tarefa pelo botão do Kiro
1. INPUT EXATO: clique em "Start task" na tarefa 3 ("- [ ] 3. Login usa o bloqueio") com tarefas 1–2 `[x]`
   ESTADO: sessão do Kiro; `status.md` `implementando`; a branch é a da fatia.
2. REGRAS:
   - "Start task" → "as regras valem igual" — `impl:13`
   - Passo 0: retomar do primeiro item não marcado — `impl:24`
   - Passo 1 por tarefa — `impl:31-47`
   - Passo 2 só quando todas `[x]` — `impl:67`
   - "Uma tarefa por vez" — `impl:31`
   - "As regras valem igual" pode incluir o Passo 0 (branch, árvore limpa, pull, testes antes de mexer) ou só o Passo 1
3. OUTPUT GERADO: tarefa 3 em ciclo de teste; `[x]` e commit.
   ARQUIVOS ESCRITOS: código e testes, `tasks.md`, `status.md` (Histórico)
4. VEREDITO MECÂNICO: AMBIGUO (`impl:13` "as regras valem igual" não diz se o Passo 0 roda a cada clique; e "retome do primeiro item não marcado" (`impl:24`) conflita com a tarefa escolhida pelo botão quando há tarefa anterior não marcada)

#### S14-F12 · Trilha direta (sem spec)
1. INPUT EXATO: "implementa o pedido: trocar o rótulo do botão Salvar por Gravar (FT-050, direta)"
   ESTADO: pasta `.kiro/specs/ft-050-…/` com só `status.md` (`fase: implementando`); mudança de texto puro (sem comportamento); `sdd-revisor` disponível.
2. REGRAS:
   - Trilha direta: sem spec nem `tasks.md` — `impl:121-124`
   - Teste que falha só quando há comportamento; texto puro não tem — `impl:125`
   - Mudança e backpressure — `impl:125`
   - Revisão pela `sdd-revisar`, rubrica C sobre o diff, com o pedido no lugar dos critérios; "relatório na conversa" — `impl:126-127`
   - "Relatório só na conversa" — `rev:30`
   - "Grave o relatório na pasta do artefato" (`revisao-codigo-<N>.md`, `<N>` = próxima rodada) — `rev:54-58`
   - SE APROVADO ENTÃO PR curto e `fase: pr-aberto` — `impl:127-128`
3. OUTPUT GERADO: relatório na conversa (ou em arquivo: NÃO-DEFINIDO); PR curto; `status.md` `pr-aberto`.
   ARQUIVOS ESCRITOS: código e testes (texto), `status.md`, e o relatório: NÃO-DEFINIDO (conversa ou `revisao-codigo-<N>.md`)
4. VEREDITO MECÂNICO: CONFLITO (`rev:30` e `impl:126-127` mandam relatório só na conversa × `rev:54-58` manda gravar na pasta do artefato, que na trilha direta só tem `status.md`)

#### S14-B1 (borda) · Sessão nova com `status.md` sujo (Histórico gravado depois do commit)
1. INPUT EXATO: "implementa a FT-031" (sessão nova, depois de a tarefa 3 ser concluída na sessão anterior)
   ESTADO: tarefas 1–3 `[x]` e commitadas; o Histórico "tarefa 3 ok" foi gravado depois do commit, então `git status` mostra ` M status.md`.
2. REGRAS:
   - Passo 0: `git status` limpo, descontados só os relatórios; qualquer outra alteração → avisar e parar — `impl:20-22`
   - `status.md` não está na lista de exceções — `impl:20-22`
   - Passo 1, item 7: Histórico gravado depois do commit do item 6 — `impl:46-47`
   - Contexto cheio: `status.md` atualizado e sessão nova — `impl:64-65`
3. OUTPUT GERADO: avisar que `status.md` está modificado e parar (`impl:22`).
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: CONFLITO (`impl:46-47` e `impl:64-65` criam e mandam retomar a partir do `status.md` numa sessão nova × `impl:20-22` faz a sessão nova parar com `status.md` modificado)

#### S14-B2 (borda) · Branch diferente do `status.md`
1. INPUT EXATO: "implementa a FT-031" na branch `main`; o `status.md` está em `feature/ft-031-bloquear-conta`
   ESTADO: árvore limpa.
2. REGRAS:
   - "Branch = a do `status.md` (senão avise e pare)" — `impl:20`
3. OUTPUT GERADO: aviso de branch e parada.
   ARQUIVOS ESCRITOS: nenhum
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S14-B3 (borda) · Falha de ambiente no Passo 2
1. INPUT EXATO: "valida a FT-031 completa" (a suíte inteira falha com "connection refused" no banco de teste)
   ESTADO: tarefas todas `[x]`; `sdd.md`: "Falha de ambiente → AMBIENTE, nunca consertar" (`steer:39`).
2. REGRAS:
   - SE erro de ambiente ENTÃO `AMBIENTE` no `status.md`, não código — `impl:70-71`
   - Não há fase nem handoff para `AMBIENTE` no Passo 2. `rub:80` (revisão) e `verif:84` (verificação) têm regras, mas o caso é do Passo 2
3. OUTPUT GERADO: `AMBIENTE` no `status.md`; a parada depois disso não está escrita.
   ARQUIVOS ESCRITOS: `status.md` (`AMBIENTE`)
4. VEREDITO MECÂNICO: SEM REGRA

#### S14-B4 (borda) · Duas correções sem sair do lugar, em AUTONOMO
1. INPUT EXATO: evento do loop: "AUTONOMO=true · fase 5 · tarefa 4: duas correções seguidas sem sair do lugar"
   ESTADO: subagente `sdd-codificador` no modo autônomo.
2. REGRAS:
   - SE duas correções sem sair do lugar ENTÃO registrar o que foi tentado e continuar numa sessão nova; persistindo → `bloqueada` — `impl:60-62`
   - SE AUTONOMO=true ENTÃO bloqueio vira `bloqueada` com o motivo, e para — `impl:133-134`
   - Não está escrito se "duas correções" é um bloqueio, nem se "sessão nova" vale no autônomo
3. OUTPUT GERADO: depende da leitura (registrar e continuar, ou `bloqueada` e parar).
   ARQUIVOS ESCRITOS: `status.md` (tentativas) ou `status.md` (`bloqueada`)
4. VEREDITO MECÂNICO: AMBIGUO (`impl:60-62` "continue numa sessão nova" × `impl:133-134` "bloqueio vira bloqueada e para")

#### Resumo S14

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S14-F1 padrão HITL | DETERMINISTIC | Dentro da mesma sessão, até a confirmação do PR |
| S14-F2 trilha rápida até PR | AMBIGUO | Template de PR sem variante para a rápida |
| S14-F3 corrigir achados (sessão nova) | AMBIGUO | `impl:12` (implementando) × `iniciar:128` (revisando) |
| S14-F4 divergência plano × código | AMBIGUO | "Decisão técnica equivalente" sem critério |
| S14-F5 REVISAR 1ª rodada | DETERMINISTIC | Corrige, volta ao Passo 2, rodada 2 |
| S14-F6 2ª reprovação | CONFLITO | "Zera as rodadas" × numeração "próxima rodada" pelos arquivos |
| S14-F7 verificação ACEITO | DETERMINISTIC | `verif:76`, sem MCP → `ELM pendente` |
| S14-F8 PR com branch desatualizada | AMBIGUO | "Conflito → repita 2–4": só com conflito? |
| S14-F9 codificador sem subagente | DETERMINISTIC | Para em "pronta para a revisão (rodada 1)" |
| S14-F10 autônomo fase 5 | CONFLITO | `loop:87` (Passos 0–2) × `impl:73-78` e `impl:85-87` |
| S14-F11 Start task | AMBIGUO | "As regras valem igual": inclui o Passo 0? |
| S14-F12 trilha direta | CONFLITO | `rev:30` (conversa) × `rev:54-58` (pasta do artefato) |
| S14-B1 sessão nova com status sujo | CONFLITO | `impl:20-22` × `impl:46-47` e `impl:64-65` |
| S14-B2 branch diferente | DETERMINISTIC | Avisa e para |
| S14-B3 AMBIENTE no Passo 2 | SEM REGRA | Não há handoff para AMBIENTE no Passo 2 |
| S14-B4 duas correções em AUTONOMO | AMBIGUO | "Sessão nova" × "bloqueio → bloqueada" |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura confere com o template? | Sucesso (quem grava / commit / branch) | Inacessível / sem permissão / inexistente | Veredito |
|---|---|---|---|---|---|---|---|
| F1 HITL | código + testes | Pelo `design.md` (forma do programa); A:codificador `./**` | do projeto | n/a | Codificador/pessoa; **commit pequeno por tarefa** com id da fatia (`impl:46`, padrão do `sdd.md`, `A:codificador` `git add/commit`); branch = a do `status.md` (`impl:20`). Push: só pela pessoa com "sim" (`impl:115-117`); agente: `git push` negado | Branch errada/árvore suja: avisa e para (`impl:20-22`); permissão/arquivo ausente: NÃO ESPECIFICADO | OK |
| F1 | `P/tasks.md` (`- [x]`) | Sim | `.md` | Marcação `[x]` por tarefa (`impl:46`) sobre o `tasks.md` de `tmpl:148-184`; opcional `[ ]*` e checkpoint sem regra (ver S13) | Grava e commita junto com a tarefa | NÃO ESPECIFICADO | NÃO ESPECIFICADO (opcional/checkpoint/subtarefas) |
| F1 | `P/status.md` (Histórico por tarefa; Rodadas; fase) | Sim | `.md` | Linha `<data> — tarefa N ok · <testes> · <commit curto>` (`impl:47`) | **Gravada depois do commit da tarefa** (`impl:46-47`) → `git status` sempre sujo em `status.md`. Passo 0 da sessão seguinte desconta só relatórios (`impl:20-22`) e `impl:64-65` manda justamente continuar em sessão nova "a partir do `status.md`" → sessão nova para. Confirma CONFLITO B1 da Parte 3 | NÃO ESPECIFICADO | DIVERGENTE (`impl:20-22` × `impl:46-47,64-65`) |
| F1 | `P/revisao-codigo-<N>.md` | Sim (`rev:55-56`; A:revisor allow `.kiro/specs/*/revisao-*.md` e `.kiro/local/wt/*/.kiro/specs/*/revisao-*.md`) | `.md`, fecho `VEREDITO: APROVADO\|REVISAR` | `rub:85-101`; uma tabela por eixo (`rub:92`) | Revisor grava; **ninguém commita no HITL de sessão única**: `impl:20-22` ("commite-os primeiro") só roda no Passo 0 da **próxima** sessão; o Passo 5 só commita o `status.md` (`impl:117`) | NÃO ESPECIFICADO | DIVERGENTE (PR cita `revisao-codigo-<N>.md` em `impl:108` sem garantir que ele foi commitado/enviado) |
| F7 | `P/verificacao.md`, `P/CT.csv`, `evidencias/`, `massa/` | Sim (A:verificador allow) | `.md`/`.csv` | `ct-csv.md` | Verificador grava (sem git). Mesmo problema: sem commit antes do PR no HITL; `sdd-consolidar/SKILL.md:47` usa o `CT.csv` **depois do merge** — se não foi commitado, não chega à base | NÃO ESPECIFICADO | NÃO ESPECIFICADO (commit de `verificacao.md`/`CT.csv` antes do PR) |
| F8 | PR (texto + abertura) | Texto `impl:103-113` | — | Template do PR tem `(EP-<nn> · IB <id\|—>)`, `Cobre`, `Plano: … (research · requirements · design · tasks)`, `<n> cenários` — sem variante para rápida (`bugfix.md`), sem épico, direta | Uma confirmação: push + abertura (`impl:115-116`); `status.md` `pr-aberto` + link, commit e **segundo push** com o mesmo "sim" (`impl:117`). Sem ferramenta de PR: "entregue título e descrição" — o que gravar em `status.md` (`pr-aberto` sem link?) não é dito | NÃO ESPECIFICADO | NÃO ESPECIFICADO (variantes do PR; `status.md` sem ferramenta de PR) |
| F2 rápida | código/testes, `tasks.md`, `status.md`, relatórios | Sim | — | `bugfix.md` no lugar de `requirements.md` na revisão (`rub:56`) | idem F1 | — | NÃO ESPECIFICADO (PR `Cobre:` vazio) — confirma AMBIGUO |
| F3 corrigir achados | `P/tasks.md` (`- [ ] N. [R<n>] <achado> — origem: revisao-codigo-<N>.md`) | Sim (`impl:25`) | `.md` | Item sem `_Requirements_` nem "Pronto quando" (fora do template `tmpl:148-184`); acrescentado depois do checkpoint | Codificador grava/commita; `status.md` "Achados abertos" marca "resolvido — tarefa <n>" (`stpl:31-32`) | NÃO ESPECIFICADO | OK com ressalva (formato de `[R<n>]` não está no template) |
| F4 divergência | `P/design.md` (decisão técnica) e/ou `P/status.md` | Sim (`impl:58`) | — | Formato da mensagem `impl:53-56`; para o `status.md` o HITL não manda registrar (`wf-ent` `implementar` manda) | — | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma AMBIGUO |
| F5/F6 REVISAR | `P/revisao-codigo-<N+1>.md`; `status.md` | Sim | — | — | `<N>`: `rev:56` "próxima rodada" × `impl:75` (incrementa antes de pedir; passa a rodada) × `wf-ent` (codificador incrementa depois, se existe `revisao-codigo-<N>.md` mais novo) × `impl:82` "zera as rodadas" → próximo relatório seria `revisao-codigo-1.md`, que já existe; a skill não diz o que o revisor faz se o arquivo existe (a ferramenta sobrescreve) | NÃO ESPECIFICADO | DIVERGENTE (confirma CONFLITO F6 da Parte 3) |
| F9 sem subagente / agente sem push | `P/status.md` (`revisando`, Rodadas) | Sim | — | — | Para em "pronta para a revisão (rodada <N>)" / "pronta para o PR"; nada commitado pelo `status.md` | NÃO ESPECIFICADO | OK |
| F10 autônomo (loop fase 5 / `wf-ent` `implementar`) | código, `tasks.md`, `status.md` em `PW/…`/worktree | Sim: A:codificador `./**` cobre `.kiro/local/wt/*/…`; comandos com `cd .kiro/local/wt/<ft> && <cmd>` (`loop:67-70`) | — | — | Orquestrador commita relatórios e status depois de cada fase (`loop:93-94`). No `wf-ent` **ninguém commita** `status.md`/relatórios entre os passos "cada passo roda numa sessão nova" → 2ª iteração do `construir` começa com `M status.md` (+ `?? revisao-codigo-1.md`, descontado) e o Passo 0 manda "avise e pare" | NÃO ESPECIFICADO | DIVERGENTE (`wf-ent` × `impl:20-22`); `impl:131-134` sem limite aos Passos 0–2 — confirma CONFLITO da Parte 3 |
| F11 Start task | `P/tasks.md`, código | Sim | — | Hook `sdd.json` PostTaskExec roda compilar+testes; não grava arquivo | — | — | NÃO ESPECIFICADO (Passo 0) — confirma AMBIGUO |
| F12 direta | código + testes, `P/status.md` (só ele existe na pasta) | Sim (`impl:123-124`) | — | `status.md` `fase: pr-aberto` + link (`impl:128`) | **Relatório da revisão**: `impl:126-127` e `rev:30` "só na conversa" × `rev:54-58` "grave … `revisao-codigo-<N>.md`" × A:revisor permite gravar `P/revisao-*.md` → a gravação é viável, a regra manda conversa. Sem arquivo, o PR cita "Revisão: APROVADO" sem referência | NÃO ESPECIFICADO | DIVERGENTE (confirma CONFLITO da Parte 3); `REVISAR`/rodadas/`bloqueada` na direta: NÃO ESPECIFICADO |
| B3 AMBIENTE no Passo 2 | `P/status.md` ("AMBIENTE") | Sim (`impl:70-71`) | — | **O template `stpl` não tem campo/seção para AMBIENTE** (nem em "Achados abertos") — onde escrever não é definido; fase/handoff: nenhum (`rub:80`/`verif:84` cobrem outros passos) | — | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma SEM REGRA, e acrescenta: sem local no template |

Achados de persistência S14

- `impl:46-47` (Histórico após o commit) × `impl:20-22` (árvore limpa, só relatórios descontados) × `impl:64-65` (retomar por `status.md` em sessão nova): `status.md` nunca está limpo. Com o `wf-ent` isso derruba a 2ª iteração.
- Relatórios de outros papéis (`revisao-codigo-<N>.md`, `verificacao.md`, `CT.csv`, `evidencias/`) só são commitados no Passo 0 da **próxima** sessão (`impl:21-22`) ou pelo orquestrador no loop (`loop:93-94`). No fluxo HITL de sessão única o Passo 5 (`impl:117`) commita só o `status.md`: o PR cita `revisao-codigo-<N>.md`/`verificacao.md` (`impl:108`) que podem não estar na branch, e o `CT.csv` não chega à base para a `sdd-consolidar`.
- `impl:82-83` "zera as rodadas" × `rev:56` "`<N>` = próxima rodada" → colisão de nome; o revisor sobrescreve sem aviso (nenhum agente tem regra de "arquivo existe").
- `stpl` não tem lugar para `AMBIENTE` (`impl:70-71`).

---


## S15 · sdd-revisar

### Parte 2 — Plano do fluxo esperado (Sonnet)


Padrão comum a todas as rubricas: o revisor começa **sem** o contexto de quem escreveu (rev:16-18); prefere o agente `sdd-revisor` (somente leitura) ou sessão nova; **não edita** artefato/código/`tasks.md`, não faz commit, escreve só o relatório da rodada (rev:20-21); ignora justificativas (commit, comentário, texto do pedido) (rev:20-21). Sempre lê `.kiro/steering/sdd.md` (comandos, regras críticas, regras aprendidas) e o steering de tecnologia/estrutura (rev:33-34). Calibragem (rev:46-50) e relatório (rev:52-58) idênticos; severidade: BLOQUEANTE e IMPORTANTE reprovam, SUGESTÃO nunca (rub:3-5; rev:60). Formato do relatório em rub:83-103; **última linha** exatamente o fecho.

#### S15-F1 · Rubrica P — PRD de um épico
- **Gatilho:** "revisa o PRD" (rev:3); evento: fim da `sdd-prd` (rev:3; `sdd-prd/SKILL.md:103` pede o `sdd-revisor` com a rubrica P).
- **Pré-condições / lê:** `prd.md`, conceitos de `elm/`, `decisoes.md`, glossário, bundle do ELM (para P6) (rev:27) + steering (rev:33-34); `<produto>/aprendizado/licoes.md` (rev:48); rubrica P inteira (rev:32; rub:10-26).
- **Processamento:**
  1. Passo 2: cruza item a item (regra → origem) (rev:38). Banco só por MCP de leitura (rev:44).
  2. Aplica P1–P11 (rub:12-24): P1 problema/solução sem tecnologia (IMPORTANTE); P2 história com cenários e "Então" verificável (BLOQUEANTE); P3 caminho feliz/inválido/repetição/erro (BLOQUEANTE); P4 regra testável com origem (BLOQUEANTE); P5 nada inventado (BLOQUEANTE); P6 ELM reutilizado ou alterado, coluna "No ELM" (BLOQUEANTE); P7 termos do glossário (IMPORTANTE); P8 nenhuma decisão `em aberto` que mude comportamento (BLOQUEANTE); P9 sem caminho/classe/SQL (SUGESTÃO); P10 fora de escopo explícito (SUGESTÃO); P11 conceitos OKF v0.2 conformes (BLOQUEANTE).
  3. Calibra (Passo 3): para cada IMPORTANTE/SUGESTÃO, se o mesmo tipo de problema já escapou antes (lição com causa `revisao-branda` em `licoes.md`), sobe uma severidade; regras promovidas valem como itens extras (rev:48-50; rub:7-8).
  4. Relatório: tabela de Achados (# · Severidade · Achado · Evidência · Correção · Origem), tabela de Verificações (✅ ❌ N/A AMBIENTE) (rub:85-101).
- **Output:** `revisao-prd-<N>.md` na pasta do épico (rev:56; `<produto>/epicos/<EP>-<slug>/`) com última linha `RESULTADO: PRONTO` ou `RESULTADO: AJUSTAR` (rub:26). Zero BLOQUEANTE e zero IMPORTANTE → aprovado (rev:60). Handoff: volta à `sdd-prd` (GATE do PRD).
- **Lacunas:**
  - P11 cita "`okf-elm.md` da `sdd-prd`" (rub:24) sem o caminho relativo `../sdd-prd/references/okf-elm.md` — a skill diz que os arquivos fora dela são citados com `../<skill>/…` (rev:12-14), mas aqui não há.
  - Não há saída JSON de veredito para P (rev:56-58 só `plano.json` e `codigo.json`) — workflows/loop não o consomem; ok, mas não dito.
  - Arquivo em `{{PRODUTO}}/epicos/*/revisao-*.md` (permissão do agente) — o produto "só na branch base" (`sdd/SKILL.md:105`) vs revisor numa worktree: caminho não definido.

#### S15-F2 · Rubrica L — plano da fatia
- **Gatilho:** "analisa o plano", "revisa a FT-031" (plano) (rev:3); evento: `sdd-plano` Passo 4 (plano:60-62), `loop` fase 3 (loop:85), passo `analisar` do workflow (wf-plan).
- **Pré-condições / lê:** `.kiro/specs/<ft>/`: `research.md`, `requirements.md` (ou `bugfix.md`), `design.md`, `tasks.md`; PRD do épico; `backlog.md` (`cobre`) (rev:28); steering; regras aprendidas; rubrica L inteira (rub:28-45). Para L4 abre os caminhos citados (rev:38).
- **Processamento:**
  1. Cruza cenário → critério → tarefa (rev:38).
  2. Aplica L1–L10 (rub:30-41): L1 cada cenário do `cobre` (ou `C<n>` da ficha) tem critério e nenhum critério fora dele; trilha rápida: `bugfix.md` com comportamento atual (evidência), esperado (fonte), o que não muda (BLOQUEANTE); L2 todo critério/item 2.x/3.x tem tarefa `_Requirements_`; bugfix começa pelo teste do defeito e preservação (BLOQUEANTE); L3 nenhuma regra fora de PRD/ELM/`decisoes.md`/ficha (BLOQUEANTE); L4 caminhos/classes/análogos existem (ou "a criar") (BLOQUEANTE); L5 design segue steering/regras críticas/lições (BLOQUEANTE); L6 tarefas em ciclo de teste (IMPORTANTE); L7 tarefas pequenas, na ordem, com comando (IMPORTANTE); L8 reexecução/transação/concorrência (BLOQUEANTE); L9 componente do design ↔ tarefa (IMPORTANTE); L10 nada fora do escopo (IMPORTANTE).
  3. Calibra (lições) e escreve o relatório; em cada achado diz se a falta é **do plano** (codificador corrige) ou **do PRD/da ficha** (volta ao P.O. pela `sdd-prd`; sem épico, pela `sdd-triar`) (rub:43-45).
  4. Se o chamador (workflow/loop) pediu: grava `.kiro/local/wf/<id>/plano.json` com `{"resultado": "OK"}` ou `{"resultado": "AJUSTAR"}` (rev:56-58).
- **Output:** `analise-plano-<N>.md` na pasta da fatia (rev:56), última linha `ANALISE: OK` ou `ANALISE: AJUSTAR` (rub:43); opcional `plano.json`. Handoff: `sdd-plano` (Passo 5 se OK; correção/Passo 2 se AJUSTAR).
- **Lacunas:**
  - Tabela de entradas de L (rev:28) não inclui a **ficha da fatia sem épico** (`<produto>/fatias/`), embora L1 e L3 a usem (rub:32,34) e a `sdd-plano` a leia (plano:21-22).
  - **L não cobre** itens que o plano exige e que o GATE manda ler: "falsificável na base" (plano:42-44), forma do programa (árvore de arquivos, assinaturas, árvore de chamadas), pontos de teste e contrato de pronto (plano:45-48,75), limite ~200 linhas/~8 tarefas (plano:52). Um plano sem contrato de pronto pode sair `ANALISE: OK`.
  - Rubrica L não diz como avaliar a trilha rápida quanto ao `design.md` curto (`tmpl:145-146`).

#### S15-F3 · Rubrica C — código da fatia (dois eixos: Spec × Padrões)
- **Gatilho:** "revisa a FT-031", "code review", "judge" (rev:3); evento: `sdd-implementar` Passo 3 (impl:75-78), `loop` fase 6 (loop:88), passo `revisar` do workflow (wf-ent).
- **Pré-condições / lê:** diff `git diff origin/<base>...HEAD` (em worktree: `cd <worktree> && git diff origin/<base>...HEAD`), a pasta da fatia (`requirements.md`/`bugfix.md`, `design.md`, `tasks.md`, `status.md`), o PRD (rev:29); recebe só: id da fatia, pasta, branch/worktree e rodada — nunca o raciocínio do autor (impl:75-77); rubrica C inteira (rub:47-81).
- **Processamento:**
  1. Passo 2 (rev:39-43): começa por `git diff --stat`; lê o diff inteiro dos arquivos de produção e de teste; **executa** os comandos de backpressure (C3) — não confia em "os testes passaram"; procura testes removidos/enfraquecidos (`git diff --diff-filter=D --name-only`, `@Disabled`, `@Ignore`, `skip`, `xit`, `assertTrue(true)`, asserts apagados, `catch` vazio) (C4). Avalia os dois eixos **separadamente**; "com subagentes disponíveis, um revisor por eixo, em paralelo".
  2. **Eixo Spec:** C1 critério → `arquivo:linha` (BLOQUEANTE); C2 cenário → teste pelo ponto de teste do `design.md` (BLOQUEANTE); C3 backpressure passa, executado (BLOQUEANTE); C4 oráculo protegido (BLOQUEANTE); C5 reexecução segura (BLOQUEANTE); C6 tarefas `[x]` com código no diff (BLOQUEANTE); C7 escopo (IMPORTANTE) (rub:54-62).
  3. **Eixo Padrões:** C8 regras críticas/steering/regras aprendidas (BLOQUEANTE); C9 segurança (BLOQUEANTE); C10 entidade × schema real via MCP de banco (N/A sem MCP) (BLOQUEANTE); C11 análogo/forma do programa (IMPORTANTE); C12 nomes do glossário (IMPORTANTE); C13 módulos profundos (IMPORTANTE); C14 sem TODO/log de depuração/código comentado, registros obrigatórios (IMPORTANTE) (rub:66-74). Reprovação em qualquer eixo é `REVISAR` (rub:49-50).
  4. Calibra (rev:46-50) e aplica a calibragem de ceticismo (rub:76-78). C3 por ambiente → `AMBIENTE`, não conta como achado, diz o que falhou (rub:80).
  5. Relatório: uma tabela de achados **por eixo** (rub:92-94), tabela de Verificações. Se pedido, `.kiro/local/wf/<id>/codigo.json` com `{"veredito": "APROVADO"}` ou `{"veredito": "REVISAR"}` (rev:56-58).
- **Output:** `revisao-codigo-<N>.md` na pasta da fatia, última linha `VEREDITO: APROVADO` ou `VEREDITO: REVISAR` (rub:81); opcional `codigo.json`. Handoff: APROVADO → `sdd-verificar`; REVISAR → `sdd-implementar` corrige (S14-F5); 2ª reprovação → bloqueada (S14-F6).
- **Lacunas:**
  - **Veredito com ambiente fora do ar:** com C3 em `AMBIENTE` o achado não conta (rub:80), então o relatório pode fechar `VEREDITO: APROVADO` sem que nenhum comando de backpressure tenha sido executado — contradiz "Execute… não confie" (rev:40-41). A rubrica não diz que veredito dar nem quem trata (o `loop:107-108` trata ambiente fora do ar como problema sistêmico, mas o veredito já foi emitido).
  - "Com subagentes disponíveis, um revisor por eixo, em paralelo" (rev:42-43) — o agente `sdd-revisor` **não tem** ferramenta de subagente (`sdd-setup/assets/agents/sdd-revisor.json`; `steer:89` Subagentes `—`); sem dizer quem consolida os dois relatórios num único arquivo.
  - Número da rodada `<N>`: "próxima rodada" (rev:56), mas o `impl:82` prevê "zera as rodadas" e o chamador passa a rodada (plano:60-62; impl:77): não diz se `<N>` vem do contador do `status.md` ou da contagem de arquivos `revisao-codigo-*.md`. Zerar o contador do `status.md` sem renomear arquivos gera colisão/sobrescrita (a skill não diz o que o revisor faz se `revisao-codigo-<N>.md` já existe).
  - Passo 3 (calibração): "suba uma severidade" (rev:48-49) transforma SUGESTÃO em IMPORTANTE (que reprova) — conflita com "Sugestões nunca reprovam" (rev:60; rub:3-4) e não diz se é limitado a um nível/uma vez.
  - Fatia sem épico/rápida: a entrada diz "o PRD" (rev:29) — a ficha/`bugfix.md` não são citados; C2 fala em "cenário da fatia", inexistente na rápida (rub:57).

#### S15-F4 · Rubrica C — trilha direta (diff + pedido)
- **Gatilho:** `sdd-implementar` trilha direta item 4 ("revisão pela `sdd-revisar`, rubrica C sobre o diff, com o **pedido** no lugar dos critérios", impl:125-127); "revisa" sobre um diff sem pasta de spec.
- **Pré-condições / lê:** diff + o pedido (rev:30); `sdd.md`, steering, regras aprendidas (rev:33-34); pasta da fatia só com `status.md`.
- **Processamento:** Aplica C com **C1, C2 e C6 contra o pedido** (rev:30); demais itens normalmente (executa backpressure C3; oráculo C4; padrões C8–C14). Eixos separados. Calibra (lições).
- **Output:** relatório **só na conversa** (rev:30) com última linha `VEREDITO: APROVADO|REVISAR`; sem `revisao-codigo-<N>.md`, sem `codigo.json` (inferido).
- **Lacunas:**
  - Contradição interna: "relatório só na conversa" (rev:30) × Passo 4 "Grave o relatório na pasta do artefato" (rev:54-58); o agente `sdd-revisor` só escreve `revisao-*.md`/`analise-*.md`/JSON (`sdd-setup/assets/agents/sdd-revisor.json`). Sem `<N>` (rodada), sem registro em `status.md`.
  - C6 ("tarefas `[x]` do `tasks.md`"), C7 ("arquivos fora do `design.md`") e C11 ("forma do programa do `design.md`") dependem de `tasks.md`/`design.md`, que não existem na direta; a tabela (rev:30) adapta só C1, C2 e C6.
  - Sem regra para `REVISAR` na direta (ver S14-F12).

#### S15-F5 · Execução fora do agente (sessão nova ou "ignore o raciocínio anterior") e pedido sem rubrica explícita
- **Gatilho:** "revisa", "judge" sem dizer o artefato (rev:3); ou `sdd-revisor` indisponível.
- **Processamento:** "Sem ele, rode esta skill numa sessão nova ou, no mínimo, ignore todo o raciocínio anterior da conversa e trabalhe só com os arquivos" (rev:16-18). Escolhe a rubrica pela tabela do Passo 1 (rev:25-30): PRD → P; plano → L; código → C.
- **Output:** relatório da rubrica correspondente.
- **Lacunas:** a skill não diz como escolher quando o pedido é ambíguo (ex.: "revisa a FT-031" pode ser L ou C) — presume-se pela fase do `status.md` (`planejando|plano-em-revisao` → L; `revisando` → C), mas isso não está escrito. Também não trata revisão de **ficha** da fatia sem épico nem de `bugfix.md` isolado como rubrica própria.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


#### S15-F1 · Rubrica P, PRD de um épico
1. INPUT EXATO: "revisa o PRD do EP-03"
   ESTADO: `prd.md`, `decisoes.md`, glossário, conceitos de `elm/`, bundle do ELM, `licoes.md` presentes; épico sem `status.md`; `sdd-revisor` disponível.
2. REGRAS:
   - SE pedido "revisa o PRD" ENTÃO rubrica P — `rev:3`, `rev:25-27`
   - Entrada P: `prd.md`, conceitos de `elm/`, `decisoes.md`, glossário, bundle do ELM (para P6) — `rev:27`
   - Ler a rubrica inteira antes de começar — `rev:32`
   - Passo 2: cruzar item a item — `rev:38`
   - Aplicar P1–P11 — `rub:12-24`
   - Passo 3: calibrar pelas lições — `rev:48-50`
   - Relatório no formato da rubrica: Achados e Verificações — `rub:85-101`
   - Grava `revisao-prd-<N>.md` na pasta do artefato, `<N>` = próxima rodada — `rev:55-56`
   - Zero BLOQUEANTE e zero IMPORTANTE → aprovado — `rev:60`
   - Última linha: `RESULTADO: PRONTO` ou `RESULTADO: AJUSTAR` — `rub:26`
   - P11 cita "`okf-elm.md` da `sdd-prd`" sem caminho — `rub:24`; `rev:12-14` só dá caminho para `../<skill>/…` citado
3. OUTPUT GERADO: relatório com `RESULTADO: …` na última linha.
   ARQUIVOS ESCRITOS: `revisao-prd-<N>.md` na pasta do épico · formato de `rub:85-101` (N: NÃO-DEFINIDO)
4. VEREDITO MECÂNICO: AMBIGUO ("próxima rodada" (`rev:56`) para o PRD não tem contador. O épico não tem `status.md` com Rodadas, e nada diz como contar. P11 também não tem caminho para o `okf-elm.md`)

#### S15-F2 · Rubrica L, plano da fatia (pedido do sdd-plano, rodada 1)
1. INPUT EXATO: "analisa o plano da FT-031 · rodada 1" (pedido pelo `sdd-plano`, Passo 4)
   ESTADO: `research.md`, `requirements.md`, `design.md`, `tasks.md` na pasta; PRD do épico; `backlog.md` com `cobre`; defeito: `design.md` não trata reexecução (L8) e tarefa 2 não cita `_Requirements_`.
2. REGRAS:
   - SE "analisa o plano" ENTÃO rubrica L — `rev:3`, `rev:25-28`
   - Entrada L: research, requirements, design, tasks, PRD, `backlog.md` (`cobre`) — `rev:28`
   - Ler a rubrica inteira — `rev:32`
   - Sempre: `sdd.md`, steering, regras aprendidas — `rev:33-34`
   - Cruzar cenário → critério → tarefa; abrir os caminhos citados (L4) — `rev:38`
   - L1–L10 — `rub:32-41`; L2 (tarefa sem `_Requirements_`) — `rub:33`; L8 (reexecução) BLOQUEANTE — `rub:39`
   - Falta do plano → codificador corrige; falta do PRD → volta ao P.O. — `rub:43-45`
   - Calibrar pelas lições — `rev:48-50`
   - Gravar `analise-plano-1.md` na pasta da fatia; última linha `ANALISE: AJUSTAR` — `rev:55-56`, `rub:43`
3. OUTPUT GERADO: `analise-plano-1.md` com os achados L8 e L2 (falta do plano) e `ANALISE: AJUSTAR`.
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/analise-plano-1.md` · formato de `rub:85-101`
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S15-F3 · Rubrica C, código da fatia (pedido do sdd-implementar, rodada 1)
1. INPUT EXATO: "revisa o código da FT-031 · rodada 1" (pedido pelo `sdd-implementar`, Passo 3)
   ESTADO: `git diff origin/develop...HEAD` disponível; `tasks.md` com todas `[x]`; C3 (backpressure) executado e verde; `steer:89`: `sdd-revisor` sem subagentes; sem lições promovidas; `licoes.md` sem `revisao-branda`.
2. REGRAS:
   - SE "revisa" com artefato de código ENTÃO rubrica C — `rev:25-30`
   - Ler a rubrica inteira — `rev:32`
   - Passo 2: `git diff --stat`, diff inteiro, executar C3, procurar testes removidos (C4) — `rev:39-42`
   - SE subagentes disponíveis ENTÃO um revisor por eixo — `rev:42-43`; aqui não há subagente, então um revisor só
   - Eixo Spec: C1–C7 — `rub:52-62`
   - Eixo Padrões: C8–C14 — `rub:66-74`
   - Calibragem: só o que afeta correção, requisito, segurança ou manutenção — `rub:76-78`
   - Gravar `revisao-codigo-1.md`; tabela de achados por eixo — `rev:55-56`, `rub:91-94`
   - Última linha: `VEREDITO: APROVADO` se não há BLOQUEANTE nem IMPORTANTE — `rub:81`, `rev:60`
3. OUTPUT GERADO: `revisao-codigo-1.md` com `VEREDITO: APROVADO`.
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/revisao-codigo-1.md` · formato de `rub:85-101`
4. VEREDITO MECÂNICO: DETERMINISTIC

#### S15-F4 · Rubrica C, trilha direta (diff + pedido)
1. INPUT EXATO: "revisa o diff da FT-050 (direta) · pedido: trocar o rótulo do botão Salvar por Gravar"
   ESTADO: pasta `.kiro/specs/ft-050-…/` com só `status.md`; `git diff` disponível; `sdd-revisor` disponível.
2. REGRAS:
   - SE trilha direta ENTÃO rubrica C sobre o diff, com C1, C2 e C6 contra o pedido — `rev:30`
   - Relatório "só na conversa" — `rev:30`
   - Passo 4: "Grave o relatório na pasta do artefato … `<N>` = próxima rodada" — `rev:54-56`
   - Pasta da direta só tem `status.md`; não há `revisao-codigo-<N>.md` possível
   - C7 (arquivos fora do `design.md`) e C11 (forma do programa) dependem de `design.md`, que a direta não tem; `rev:30` não os lista
3. OUTPUT GERADO: relatório na conversa (`rev:30`) OU arquivo `revisao-codigo-<N>.md` (`rev:54-58`), e a última linha `VEREDITO: …`.
   ARQUIVOS ESCRITOS: CONFLITO: nenhum (conversa) ou `revisao-codigo-<N>.md` (N: sem rodada)
4. VEREDITO MECÂNICO: CONFLITO (`rev:30` manda relatório só na conversa × `rev:54-58` manda gravar na pasta do artefato com `<N>`; na direta não há pasta de artefato)

#### S15-F5 · Pedido sem nome do artefato, sem agente
1. INPUT EXATO: "revisa a FT-031"
   ESTADO: fase `revisando` no `status.md`; `sdd-revisor` indisponível; sessão com a conversa anterior de implementação.
2. REGRAS:
   - SE sem agente ENTÃO sessão nova, ou ignorar o raciocínio anterior e trabalhar só com os arquivos — `rev:16-18`
   - Escolher rubrica pela tabela: "plano de uma fatia" → L; "código de uma fatia" → C — `rev:25-30`
   - "Revisa a FT-031" casa com as duas linhas da tabela; a tabela não tem desempate
   - A fase `revisando` não é citada na tabela, então não ajuda a escolher
3. OUTPUT GERADO: relatório de L ou de C, a escolher.
   ARQUIVOS ESCRITOS: `analise-plano-N.md` ou `revisao-codigo-N.md`: depende da rubrica
4. VEREDITO MECÂNICO: AMBIGUO (`rev:25-30` tem duas linhas que casam com "a FT-031" e nenhum critério de desempate)

#### S15-B1 (borda) · C3 cai por ambiente
1. INPUT EXATO: "revisa o código da FT-031 · rodada 1" com o comando de testes retornando "connection refused: banco de teste"
   ESTADO: `sdd-revisor` sem subagente; nenhum achado de código.
2. REGRAS:
   - C3 (backpressure) é BLOQUEANTE: "passam — executar" — `rub:58`
   - "Não confie em 'os testes passaram' de ninguém" — `rev:39-40`
   - C3 por ambiente → `AMBIENTE`, não conta como achado — `rub:80`
   - Zero BLOQUEANTE e zero IMPORTANTE → aprovado — `rev:60`
   - Fecho: `VEREDITO: APROVADO` ou `REVISAR` — `rub:81`
   - Não está escrito se AMBIENTE conta para o veredito
3. OUTPUT GERADO: `VEREDITO: APROVADO` (pela regra de `rev:60`, sem C3 executado) ou `REVISAR` (pela regra de `rub:58`).
   ARQUIVOS ESCRITOS: `revisao-codigo-1.md`
4. VEREDITO MECÂNICO: CONFLITO (`rub:58` exige C3 passando e executado × `rub:80` diz que AMBIENTE não é achado × `rev:60` aprova sem achado bloqueante)

#### S15-B2 (borda) · Lição `revisao-branda` sobe uma SUGESTÃO
1. INPUT EXATO: "revisa o código da FT-031 · rodada 1"; o revisor aponta, como SUGESTÃO, "renomear `util` para `ContaUtils`"; `licoes.md` tem uma lição com causa `revisao-branda` para o mesmo tipo de problema
   ESTADO: sem outros achados.
2. REGRAS:
   - Para cada achado IMPORTANTE ou SUGESTÃO, se a lição `revisao-branda` existe → "suba uma severidade" — `rev:48-49`
   - SUGESTÃO não reprova nem reabre ciclo — `rub:3-4`
   - Sugestões nunca reprovam — `rev:60`
   - Gosto pessoal é SUGESTÃO "quando muito" — `rub:76-78`
3. OUTPUT GERADO: depende da regra aplicada: IMPORTANTE (reprova) ou SUGESTÃO (não reprova).
   ARQUIVOS ESCRITOS: `revisao-codigo-1.md`
4. VEREDITO MECÂNICO: CONFLITO (`rev:48-49` transforma SUGESTÃO em IMPORTANTE, que reprova, × `rub:3-4` e `rev:60` dizem que SUGESTÃO nunca reprova)

#### S15-B3 (borda) · Revisar a ficha de uma fatia sem épico
1. INPUT EXATO: "revisa a ficha da FT-060 (fatia sem épico)"
   ESTADO: ficha em `<produto>/fatias/`; sem épico.
2. REGRAS:
   - Tabela de entradas: PRD → P; plano → L; código → C; direta → C sobre o diff — `rev:25-30`
   - Ficha da fatia não aparece em nenhuma linha. `rub` não tem rubrica para ficha
3. OUTPUT GERADO: NÃO-DEFINIDO.
   ARQUIVOS ESCRITOS: nenhum definido
4. VEREDITO MECÂNICO: SEM REGRA

#### S15-B4 (borda) · Plano sem contrato de pronto nem forma do programa
1. INPUT EXATO: "analisa o plano da FT-031 · rodada 1"
   ESTADO: `design.md` sem a seção "Contrato de pronto" nem "Forma do programa"; os itens L1–L10 todos atendidos.
2. REGRAS:
   - Entrada L com o `design.md` — `rev:28`
   - L1–L10 não têm item para forma do programa, contrato de pronto ou "falsificável na base" — `rub:32-41`
   - `plano:45-48` e `plano:75` exigem esses itens no plano, mas não são critério da rubrica L
   - SE nenhum item de L é violado ENTÃO `ANALISE: OK` — `rub:43`, `rev:60`
3. OUTPUT GERADO: `ANALISE: OK` com `design.md` sem contrato de pronto.
   ARQUIVOS ESCRITOS: `analise-plano-1.md`
4. VEREDITO MECÂNICO: SEM REGRA (a rubrica não tem item para o que o `plano` exige no `design.md`)

#### Resumo S15

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S15-F1 rubrica P (PRD) | AMBIGUO | "Próxima rodada" sem contador para o épico; P11 sem caminho |
| S15-F2 rubrica L (plano) | DETERMINISTIC | AJUSTAR com achados do plano |
| S15-F3 rubrica C (código) | DETERMINISTIC | Um revisor, C3 executado, `revisao-codigo-1.md` |
| S15-F4 rubrica C (direta) | CONFLITO | `rev:30` (só conversa) × `rev:54-58` (grava na pasta) |
| S15-F5 pedido sem artefato | AMBIGUO | L e C casam igualmente com "a FT-031" |
| S15-B1 C3 por ambiente | CONFLITO | `rub:58` × `rub:80` × `rev:60` |
| S15-B2 lição sobe SUGESTÃO | CONFLITO | `rev:48-49` × `rub:3-4` e `rev:60` |
| S15-B3 ficha sem épico | SEM REGRA | Ficha não está nas entradas nem há rubrica |
| S15-B4 plano sem contrato de pronto | SEM REGRA | `plano:45-48` exige, `rub:32-41` não checa |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho prescrito) | Diretório confere? | Extensão/formato | Estrutura confere com o template? | Sucesso (quem grava / commit / branch) | Inacessível / sem permissão / inexistente | Veredito |
|---|---|---|---|---|---|---|---|
| F1 rubrica P | `<produto>/epicos/<EP>-<slug>/revisao-prd-<N>.md` | Skill diz só "pasta do artefato" (`rev:55`); o caminho completo sai de `sdd/SKILL.md:105` + A:revisor allow `{{PRODUTO}}/epicos/*/revisao-*.md` (matcher: permitido). Só na branch base (`sdd/SKILL.md:105`); worktree negada ao produto | `.md`, fecho `RESULTADO: PRONTO\|AJUSTAR` (`rub:26`) | Formato `rub:85-101`: Resumo · Achados (tabela) · Verificações (✅ ❌ N/A AMBIENTE) · última linha = fecho | Revisor grava; **ninguém commita**: o GATE do PRD commita "PRD, `decisoes.md`, `elm/` e `backlog.md`" (`sdd-prd/SKILL.md:119-122`) — `revisao-prd-<N>.md` não está na lista. `<N>`: o épico não tem contador de Rodadas (`status.md` só da fatia) → "próxima rodada" (`rev:56`) indefinida; `sdd-prd/SKILL.md:113` usa "OK na rodada N" | NÃO ESPECIFICADO | NÃO ESPECIFICADO (`<N>` do PRD; commit do relatório) — confirma AMBIGUO da Parte 3 |
| F2 rubrica L | `P/analise-plano-<N>.md` | Sim (`rev:55-56`; A:revisor allow `.kiro/specs/*/analise-*.md`; também `PW`) | `.md`, fecho `ANALISE: OK\|AJUSTAR` | `rub:85-101`; cada achado diz "do plano" ou "do PRD/ficha" (`rub:43-45`). A tabela de entradas `rev:28` não lista a ficha da fatia sem épico (`<produto>/fatias/`), que L1/L3 usam | Revisor grava, não commita (`rev:20`). `<N>`: caller passa a rodada já incrementada (`plano:60-62`, `loop:76,93`) mas `rev:56` diz "próxima rodada" e o `wf-plan` `analisar` **não passa rodada** (incrementa depois). Leitura "contador + 1" dá `analise-plano-2.md` na 1ª rodada via `sdd-plano`; leitura "arquivos existentes + 1" funciona nos três | NÃO ESPECIFICADO | DIVERGENTE potencial (definição de `<N>`); Parte 3 (S15-F2 DETERMINISTIC) assumiu `…-1.md` — válido só com "usa a rodada recebida" |
| F2 opcional | `.kiro/local/wf/<id>/plano.json` | `rev:57` não define `<id>`; `wf-plan` usa `{{fatia}}` (ex. "FT-031"), enquanto a pasta é minúscula (`ft-031-…`). Relativo à raiz do projeto, **fora do git** (`sdd/SKILL.md` tabela: `.kiro/local/`). A:revisor allow `.kiro/local/wf/*/plano.json` (permitido). O A:codificador **nega** `.kiro/local/wf/**`: um revisor chamado como subagente do codificador herda o deny (`agentes.md:33-35`, "deny-wins") e não grava o JSON — só funciona como passo de workflow | `.json` | `{"resultado": "OK"}` / `{"resultado": "AJUSTAR"}` — chaves e valores conferem com `rev:57` e com `fileCheck` de `wf-plan` (`jsonPath: resultado`, `value: OK`). O passo `zerar` grava `"PENDENTE"`, valor que a skill não define (só OK/AJUSTAR) | Revisor grava; não commita (fora do git) | Diretório `.kiro/local/wf/<id>/` inexistente: **NÃO ESPECIFICADO** (nada cria; depende de a ferramenta de escrita criar a pasta) | OK no formato; NÃO ESPECIFICADO (`<id>` e criação da pasta) |
| F3 rubrica C | `P/revisao-codigo-<N>.md` | Sim (`rev:55-56`; permitido, inclusive `PW`) | `.md`, fecho `VEREDITO: APROVADO\|REVISAR` (`rub:81`) | `rub:85-101` com uma tabela por eixo (Spec, Padrões); C3 `AMBIENTE` não conta como achado (`rub:80`) → relatório pode fechar `APROVADO` sem backpressure executado, contra `rev:39-41` | Revisor grava, não commita; commit: loop (`loop:93-94`) ou Passo 0 seguinte (`impl:21-22`). Eixo único: A:revisor não tem subagente (`steering/sdd.md:89`), então `rev:42-43` ("um revisor por eixo") é inexecutável e não há consolidação | NÃO ESPECIFICADO | OK no caminho/formato (confirma DETERMINISTIC); NÃO ESPECIFICADO (commit) |
| F3 opcional | `.kiro/local/wf/<id>/codigo.json` | idem `plano.json` | `.json` | `{"veredito": "APROVADO"}` / `{"veredito": "REVISAR"}` — confere com `rev:57-58` e `fileCheck` de `wf-ent` (`jsonPath: veredito`, `value: APROVADO`); `zerar` grava `"PENDENTE"` | idem | idem | OK / NÃO ESPECIFICADO |
| F4 direta | "relatório só na conversa" × `P/revisao-codigo-<N>.md` | `rev:30` × `rev:54-58`; a pasta da direta só tem `status.md`; A:revisor **permite** gravar `P/revisao-*.md` | — | Fecho `VEREDITO: …` | Se arquivo: sem `<N>` (direta não tem Rodadas usadas), sem commit | NÃO ESPECIFICADO | DIVERGENTE (confirma CONFLITO da Parte 3) |
| F5 sem agente / pedido ambíguo | idem F2/F3 (por rubrica) | Idem; sessão da pessoa usa as permissões dela | — | — | A tabela `rev:25-30` não desempata "revisa a FT-031" | NÃO ESPECIFICADO | NÃO ESPECIFICADO — confirma AMBIGUO |

Achados de persistência S15

- `rev:56` "`<N>` = próxima rodada" é a única definição, e é incompatível com quem incrementa antes (`plano:60`, `impl:75`, `loop:93`), com quem incrementa depois (`wf-plan` `ajustar`, `wf-ent` `implementar`) e com "zera as rodadas" (`impl:82`). Sem regra "arquivo já existe".
- `.kiro/local/wf/<id>/`: `<id>` indefinido (`rev:57`), pasta nunca criada por skill/setup (grep `local/wf|mkdir`: só `agentes.md:87`).
- O revisor como subagente do codificador não consegue gravar `plano.json`/`codigo.json` (deny do codificador em `.kiro/local/wf/**`, A:codificador `write.deniedPaths`), embora `rev:56-58` permita "se quem chamou pediu".
- O `revisao-prd-<N>.md` está fora do commit do GATE do PRD (`sdd-prd/SKILL.md:119-122`).

---


## S16 · sdd-verificar

### Parte 2 — Plano do fluxo esperado (Sonnet)


Contexto comum aos fluxos F1–F4 (lido por inteiro: SV 1–100, CT 1–48):
- Skill preferencialmente executada pelo agente `sdd-verificador` (SV:17), contexto limpo, que **não** tem o MCP `elm` (README "O MCP do ELM entra só nos agentes…"; `sdd-setup/assets/agents/sdd-verificador.json`: tools read/shell/write; sem git add/commit/push; escrita só em `verificacao.md`, `CT.csv`, `status.md`, `evidencias/`, `massa/`, `.kiro/local/verificacao/`).
- Entrada: pasta da fatia com revisão `APROVADO`, na branch da fatia (SV:22). Configuração (tipo de projeto, Executar, Onde verificar, massa, ambiente, http.sh): seção "Verificação de aceite" do `.kiro/steering/sdd.md` (SV:22-23; STEER:174-180).

#### S16-F1 · Verificação ACEITA (roteiro → execução → ACEITO → CT.csv → handoff para PR)

- **Gatilho inicial**
  - Frases (description, SV:3): "verifica a FT-031", "testa a fatia", "executa os cenários", "teste de aceitação", "gera os CTs".
  - Eventos: `sdd-implementar` Passo 4 (SI:85-89) após `VEREDITO: APROVADO` (SI:80); fase 7 do `sdd-loop` (SL:89) via `sdd-verificador`.
- **Pré-condições / arquivos lidos**
  - Branch/worktree da fatia; revisão `APROVADO` (`revisao-codigo-<N>.md`); `design.md` (contrato de pronto, "acordado no GATE do plano", SV:29-30); `bugfix.md`/requisitos para trilha rápida (SV:31); `status.md` (campo **Banco**, SV:48); `.kiro/steering/sdd.md` (Verificação de aceite).
  - Aplicação/job/ambiente local ou de teste disponível; nunca produção (SV:44, 98).
- **Processamento interno**
  1. (Passo 1, SV:25-39) Grava no `status.md` `fase: verificando` + linha no Histórico. Para cada cenário do contrato de pronto escreve, **antes de executar**, em `verificacao.md`, o bloco `### HF-01 · 1.2 — título` com Massa / Executar / Esperado / Verificar em.
  2. (Passo 2, SV:41-48) Sobe a aplicação com o comando **Executar** do `sdd.md`. Massa: scripts da convenção do projeto; sem convenção, cria em `.kiro/specs/<ft>-<slug>/massa/`. Escrita em banco só pelos scripts de massa; consultas pelo MCP de banco, somente leitura. Se `Banco = pendente` → ver S16-F3.
  3. (Passo 3, SV:50-66) Executa cenário por cenário e registra abaixo do roteiro `Resultado (✅/❌/⚠️) · Obtido · Evidência`. Por tipo: backend → `sh .kiro/sdd/http.sh <MÉTODO> <caminho> [corpo]` (corpo de `massa/`; senão `curl`, que pede confirmação) + estado no banco; batch → execução do job, status e contagens; frontend → browser real (Playwright/MCP), screenshot em `evidencias/`; dados → carga + consultas. Roda também **repetição** (duas execuções) e **erro em um item** (SV:65).
  4. Evidência com dado real de pessoa → `.kiro/local/verificacao/<ft>/` (fora do git); no `verificacao.md` ficam consulta, contagem, caminho e resumo sem identificar pessoas (SV:98-100).
  5. (Passo 4, SV:68-84) Emite o bloco `🔎 Verificação FT-<nnn> — rodada <N> · Cenários: a aceitos · r rejeitados · e ambiente · VERIFICACAO: ACEITO | REJEITADO`. Todos aceitos → **ACEITO**.
  6. ACEITO → gera `CT.csv` (Passo 5; ver S16-F4) e grava `fase: aceita` no `status.md` (SV:76-77).
  7. **Horas da `[VER]`** (SV:77-80): pergunta as horas a quem verificou (descontando o já lançado) → `sdd-elm` modo *horas* e modo *conclusão* na `[VER] FT-nnn`, com confirmação (ELM:186-197, 218-221). Sem o MCP nesta sessão (caso do agente `sdd-verificador`) → grava `ELM pendente: lançar <h>h em [VER] FT-nnn` no Histórico do `status.md`.
  8. Rodadas: quem pediu a verificação incrementa "verificação" (a `sdd-implementar` — SI:87 — ou o orquestrador — SL:92-94); só no pedido direto de pessoa, a própria skill incrementa (SV:92-93).
- **Resultado final esperado**
  - Resposta: bloco `🔎 Verificação FT-<nnn> — rodada <N>` com `VERIFICACAO: ACEITO`; pergunta das horas (sessão com pessoa) ou nota `ELM pendente` (agente).
  - Arquivos: `.kiro/specs/<ft>-<slug>/verificacao.md` (roteiro + resultados); `.kiro/specs/<ft>-<slug>/CT.csv`; `evidencias/ft-031-1.2.png` etc. (quando houver); `massa/` (se sem convenção); `status.md` (`fase: aceita`, Histórico, ELM pendente se for o caso); eventual `.kiro/local/verificacao/<ft>/` (fora do git). Nada é commitado pela skill (o verificador não tem `git add/commit`; commit vem do codificador, `SI:20-22`, ou do orquestrador, `SL:93-94`).
  - Próximo passo: devolve para a `sdd-implementar` abrir o PR (Passo 5 dela, SI:91-119); na consolidação (pós-merge) a `sdd-elm` modo *testes* importa o CT.csv (SV:89-91).
- **Lacunas observadas**
  - **Horas `[VER]` em modo autônomo/agente não fecham.** SV:77-80 manda "perguntar as horas a quem verificou"; o `sdd-loop` passa `AUTONOMO=true` ao `sdd-verificador` (SL:75, 89), mas SV não tem modo autônomo (só `sdd-entrevistar`, `sdd-plano`, `sdd-implementar` têm: grep `AUTONOMO`). O verificador também não tem MCP. O SL:118-119 diz que "as `[REV]` e `[VER]` são lançadas por quem revisa e verifica, na conclusão de cada uma" — mas no loop quem verificou foi um subagente. O SC:48 só cobra horas de `[DEV]` e `[REV]` no merge, nunca da `[VER]`. Resultado: o `ELM pendente: lançar h em [VER]` fica só no `status.md` e só aparece no `sdd-status` (SC:55-56; `sdd-status/SKILL.md:22`); nenhuma skill diz quem o executa nem que a `[VER]` é concluída sem horas (SC:52-53 apenas "não trava").
  - **Responsável do CT.csv**: CT:22 "login do ELM de quem verificou" — o verificador não tem MCP/`whoami` (só `git config user.name/email`, que não é login ELM). Fonte do valor não definida. Idem "Planejado para: sprint" (CT:25; não diz de onde ler: `sprint-<nn>.md`?).
  - Sem definição de **estrutura multi-rodada** do `verificacao.md` (acrescenta rodada? sobrescreve?). O `sdd-implementar` Passo 0 lê "cenários rejeitados do `verificacao.md`" (SI:26-27) e o CT.csv exige "um caso por cenário verificado" (SV:88) — com várias rodadas, não há marca de qual resultado é o vigente.
  - "Gera os CTs" como pedido isolado (description SV:3) não tem fluxo próprio (ver S16-F4).
  - Entrada diz "revisão `APROVADO`" (SV:22) mas não manda conferir `fase`/relatório nem trata a trilha direta (que não tem verificação: SI:121-129).

#### S16-F2 · Verificação REJEITADA (volta para sdd-implementar, depois re-verificação)

- **Gatilho inicial**: mesmo de S16-F1; condição: ao menos um cenário `❌ rejeitado` (e nenhum conserto de ambiente pendente).
- **Pré-condições / arquivos lidos**: as de S16-F1 (roteiro e execução já realizados, Passos 1-3).
- **Processamento interno**
  1. Passo 4 (SV:81-83): emite `VERIFICACAO: REJEITADO` com contagem.
  2. Para cada cenário rejeitado, registra **esperado × obtido + evidência** no `status.md` como **achados** (seção "Achados abertos", cf. SI:25-26).
  3. Grava `fase: implementando`.
  4. Decisão: se o problema é o **cenário estar errado no PRD** → diz isso explicitamente; é com o P.O. (`sdd-prd`/`sdd-entrevistar`), não com o código (SV:82-83).
  5. A `sdd-implementar` (Passo 0, SI:24-27) transforma os rejeitados em tarefas `[R<n>]`, corrige, volta a Passos 2-3 (revisão de código novamente, SI:73-83) e reentra na verificação (Passo 4); a verificação reexecuta "só os rejeitados + os de repetição" (SV:83).
  6. No `sdd-loop` (fase 7, SL:89): `REJEITADO` → volta à fase 5 **uma vez**; nova rejeição → `fase: bloqueada` (SL:89, 105-106).
  7. CT.csv **não** é gerado (Passo 5 só depois de ACEITO, SV:76).
  8. Rodadas: o solicitante incrementa "verificação" a cada nova rodada (SV:92-93).
- **Resultado final esperado**
  - Resposta: bloco `🔎 … REJEITADO` + lista de achados esperado × obtido; recomendação de ir ao P.O. quando o cenário é o errado.
  - Arquivos: `verificacao.md` (resultados ❌), `status.md` (`fase: implementando`, achados, Histórico), evidências em `evidencias/`.
  - Próximo: `sdd-implementar` corrige; nova rodada de `sdd-verificar`. No loop, 2ª rejeição → bloqueada com pergunta no `status.md`.
- **Lacunas observadas**
  - **Loop × SV sobre limite de rodadas**: SV não impõe limite; SL:89 limita a uma volta (2ª = `bloqueada`). Fora do loop, o número de rodadas de verificação não tem teto nem opção de escalonamento como a revisão de código tem (SI:81-83: orientar, replanejar ou aceitar achados).
  - **Loop fase 7 → 5 não diz se a fase 6 (revisão de código) roda de novo** depois do conserto (SL:87-89), embora SI:81-83 exija voltar à revisão a cada alteração (Passo 2→3). Ambiguidade que pode deixar código modificado sem revisão independente.
  - Cenário "errado no PRD" (SV:82-83) não tem `fase` nem handoff: não diz se a fatia fica `implementando` ou `bloqueada`/`plano-em-revisao`, nem como o loop distingue isso de rejeição por código (SL:105-106 só fala em "verificação rejeitada duas vezes").
  - Achados da verificação são registrados em `status.md`; SA:30 trata "cenário rejeitado na verificação" como gatilho de lição, mas SV não manda acionar a `sdd-aprender` (só SC:80-81 o faz no pós-merge, e o SL:115 só lista "Lições para registrar").

#### S16-F3 · Bloqueio por ambiente / DDL pendente (fase: bloqueada)

- **Gatilho inicial**: durante os Passos 2-3, (a) `status.md` com campo **Banco = `pendente`** (SV:48); (b) falha de ambiente: serviço fora do ar, credencial de teste (SV:66).
- **Pré-condições / arquivos lidos**: `status.md` (campo Banco), `sdd.md` (Executar / ambiente).
- **Processamento interno**
  1. Banco `pendente` → **pare**: "a verificação depende da DDL aplicada em dev" (SV:48). Nenhuma execução.
  2. Falha por ambiente durante a execução → marca o cenário `⚠️ ambiente` (não rejeição) e diz o que faltou (SV:66).
  3. Se, ao final, só há `⚠️ ambiente` → `fase: bloqueada` com o que falta; "ninguém corrige código" (SV:84).
  4. Misto (alguns ❌ e outros ⚠️): a skill só define REJEITADO se houver ❌ (SV:81-83); não define como ficam os ⚠️.
  5. Loop: ambiente fora do ar / build quebrado na base / mesmo erro em duas fatias → problema **sistêmico**, o loop **para o lote inteiro** (SL:107-108).
- **Resultado final esperado**
  - Resposta: bloco `🔎 … ⚠️ ambiente` com a lista do que faltou; `VERIFICACAO` indefinido (não há valor para "bloqueada" no bloco, SV:70-74).
  - Arquivos: `verificacao.md` (resultados ⚠️ e o que faltou), `status.md` (`fase: bloqueada`, Histórico).
  - Próximo: alguém (DBA/infra/pessoa) resolve; reabrir a verificação ("retoma a verificação da FT-031" — fase `bloqueada` no mapa de retomada da `sdd-iniciar`).
- **Lacunas observadas**
  - **Banco = pendente**: SV:48 diz só "pare". No Passo 1 a skill já gravou `fase: verificando` (SV:27) — a fatia fica nessa fase sem `bloqueada` nem mensagem padronizada; SV:84 só cobre "só ambiente". Contradição de ordem: o Passo 1 (grava fase) vem antes do Passo 2 (checa Banco).
  - Quem desbloqueia e como a fatia volta para `verificando` não está nesta skill (depende do mapa de fases da `sdd-iniciar`).
  - Formato `VERIFICACAO:` (SV:73) só admite ACEITO | REJEITADO; o caso "bloqueada por ambiente" não tem valor de saída, o que dificulta o parser do orquestrador (SL:89 espera `ACEITO`/`REJEITADO`).

#### S16-F4 · Geração do CT.csv (e consumo posterior no ETM)

- **Gatilho inicial**
  - Evento: SV Passo 4 → ACEITO (SV:76) → Passo 5 (SV:86-91).
  - Frase: "gera os CTs" (description SV:3) — como pedido direto, ver lacuna.
- **Pré-condições / arquivos lidos**: `verificacao.md` com cenários aceitos e evidência; `.kiro/config/power/elm/pa_*.json` e linha `CT.csv` da seção ELM do `sdd.md` (CT:14-16; STEER:207); `design.md`/PRD para ids HF/REG; `status.md` (título da fatia).
- **Processamento interno**
  1. Cria `.kiro/specs/<ft>-<slug>/CT.csv`: UTF-8 **com BOM**, quebras **LF**, separador `;` — gravado já nesse formato (CT:8-10).
  2. **Um caso por cenário verificado** (aceito com evidência) (CT:3).
  3. Colunas na ordem: Tipo · Resumo (`<FT-nnn> <título curto> : CT<nn> - <título do cenário>`) · Responsável · Status · Categoria · Planejado para · Descrição (CT:18-26). Sem ELM → colunas desconhecidas vazias (CT:14-15). Ordem/nomes/valores fixos vêm do template do ETM do projeto (CT:15-16; STEER:207).
  4. Descrição: bloco com OBJETIVO / PRÉ-CONDIÇÕES / PASSOS / RESULTADO ESPERADO / EVIDÊNCIA DA VERIFICAÇÃO, entre aspas duplas com quebras reais; aspas internas dobradas (CT:28-48).
  5. **Importação e link "valida"**: não é desta skill. Depois do merge, na consolidação, `sdd-elm` modo *testes* (SV:89-91; SC:47; ELM:203-209): entrega o caminho do CT.csv ("Importe no ETM (Importar → CSV)"), pergunta os ids criados, lê cada caso via `elm-qm` (`get_testartifact`) para obter a URL, liga **valida** (CT → história) e **testado por** (IB → CT), registra ids no `verificacao.md` e `status.md`.
- **Resultado final esperado**
  - Resposta: menção de que o `CT.csv` foi gerado em `.kiro/specs/<ft>-<slug>/CT.csv`; importação fica para a consolidação.
  - Arquivos: `CT.csv` (BOM + LF + `;`).
  - Próximo: PR (`sdd-implementar` Passo 5); pós-merge: `sdd-consolidar` → `sdd-elm` modo *testes* (importação manual pela UI do ETM; o MCP só lê o ETM — CT:3-4).
- **Lacunas observadas**
  - **Pedido direto "gera os CTs"** (SV:3): não há fluxo (Passo 5 só é alcançado após ACEITO; não diz o que fazer com fatia já aceita ou já mergeada).
  - **Contradição interna sobre colunas** (CT:14-16 vs CT:18-26): a tabela fixa as 7 colunas "nesta ordem" e, ao mesmo tempo, diz que ordem/nomes vêm do template do ETM do projeto. Não diz qual prevalece quando divergem.
  - Cenários extras de **repetição** e **erro em um item** (SV:65) viram CT? "Cenário verificado" (CT:3) e "cenário que a fatia cobre" (SV:30) não esclarecem.
  - **Dado real no CT.csv**: SV:98-100 manda manter dado real fora do git no `verificacao.md`; CT.csv é commitado e tem o campo "EVIDÊNCIA… resumo do obtido" (CT:44-45) sem a mesma restrição.
  - Importação sem retorno de ids na mesma sessão (pessoa importa depois): ELM:205-209 não define pendência (`ELM pendente: importar/ligar CT`) nem prazo — ver S17-F1.
  - Responsável/Planejado para: ver lacuna em S16-F1.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**S16-F1 · Verificação ACEITA**

1. INPUT EXATO: "verifica a FT-031" (pessoa, sessão com MCP elm).
   ESTADO: branch `feature/ft-031-bloquear-conta`; `revisao-codigo-1.md` com `VEREDITO: APROVADO`; status.md `fase: revisando`, Rodadas `verificação 0`, Banco `não se aplica`, ELM `[VER] FT-031 · id 5521`; sdd.md "Verificação de aceite" preenchida (backend, `http.sh` registrado, sem convenção de massa); design.md com cenários 1.1, 1.2, 1.3; app de teste sobe; os três cenários passam com evidência.
2. REGRA APLICADA:
   - SE a pasta tem revisão APROVADO na branch da fatia ENTÃO segue — SV:22.
   - SE sempre ENTÃO status.md `fase: verificando` + linha no Histórico — SV:27.
   - PARA cada cenário, ANTES de executar, escreve o bloco `### HF-01 · 1.1 — título` (Massa/Executar/Esperado/Verificar em) em verificacao.md — SV:29-39.
   - SE Executar aponta app local ou de teste (nunca produção) ENTÃO sobe a aplicação — SV:43-44.
   - SE não há convenção de massa ENTÃO cria em `.kiro/specs/ft-031-bloquear-conta/massa/` — SV:45-46.
   - SE Banco = `não se aplica` ENTÃO não para (só `pendente` para) — SV:48.
   - SE backend ENTÃO `sh .kiro/sdd/http.sh <MÉTODO> <caminho> [corpo]`, corpo de `massa/` — SV:60-62.
   - PARA cada cenário ENTÃO registra `Resultado / Obtido / Evidência` logo abaixo do roteiro — SV:52-58.
   - SE sempre ENTÃO roda a repetição (duas execuções) e o erro em um item — SV:65.
   - SE todos ✅ ENTÃO decisão ACEITO e bloco `🔎 … VERIFICACAO: ACEITO` — SV:76, SV:70-74.
   - SE ACEITO ENTÃO gera CT.csv (Passo 5) — SV:76, SV:86-88.
   - SE ACEITO ENTÃO `fase: aceita` no status.md — SV:76.
   - SE ACEITO e sessão com pessoa e MCP ENTÃO pergunta as horas da [VER] (descontando o já lançado) e lança modo horas e conclusão com confirmação — SV:77-79; SE:192 (desconta), SE:193-195 (confirma e lança), SE:220-221 (conclusão).
   - SE pedido direto de pessoa ENTÃO incrementa "verificação" em Rodadas — SV:92-93; ST:25-27.
   - CT.csv: colunas na ordem de CT:18-26; Tipo = Caso de Teste — STEER:80; Responsável = "login do ELM de quem verificou" — CT:22; Planejado para = sprint — CT:25.
3. OUTPUT GERADO:
   > 🔎 Verificação FT-031 — rodada 1 · Cenários: 3 aceitos · 0 rejeitados · 0 ambiente · VERIFICACAO: ACEITO
   Mais a pergunta de horas da [VER] (texto livre; SV:77-78 não dá template).
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/verificacao.md` (roteiro + Resultado) · `evidencias/` (se houver) · `massa/` (convenção ausente) · `.kiro/specs/ft-031-bloquear-conta/CT.csv` (BOM, LF, `;`) · `status.md` (`fase: aceita`, Histórico, Rodadas verificação 1) · ELM: horas e conclusão da [VER] só após "sim". Nenhum commit prescrito por esta skill.
4. VEREDITO MECÂNICO: AMBÍGUO — (a) Responsável do CT.csv: "login do ELM de quem verificou" (CT:22) sem fonte escrita nesta skill (IN:102 `whoami` × SS:35-36 `git config` cruzado com `equipe.json`); (b) "rodada <N>" do bloco (SV:71) sem regra de cálculo; o incremento vem depois, em SV:92-93.

**S16-F2 · Verificação REJEITADA**

1. INPUT EXATO: "verifica a FT-031" — cenário 1.2 retorna 200 onde o Esperado é 403; 1.1 e 1.3 ✅.
   ESTADO: igual a S16-F1 (fase `revisando`, revisão APROVADO, MCP elm presente, pessoa na sessão).
2. REGRA APLICADA:
   - SE sempre ENTÃO roteiro, execução e registro como em S16-F1 — SV:22, SV:27, SV:29-39, SV:52-58; 1.2 fica `❌ rejeitado`, Obtido 200, Evidência — SV:55-57.
   - SE há ❌ (não há ⚠️ nem cenário faltando) ENTÃO decisão REJEITADO — SV:81 (a condição não está escrita; deduzida de SV:76 e SV:84).
   - PARA cada cenário rejeitado ENTÃO esperado × obtido + evidência como achado no status.md — SV:81; ST:29-35 (colunas Origem, Achado, Situação).
   - SE REJEITADO ENTÃO `fase: implementando` — SV:82; ST:18-22.
   - SE REJEITADO ENTÃO CT.csv NÃO é gerado — SV:76 (só ACEITO).
   - SE pedido direto de pessoa ENTÃO Rodadas verificação +1 — SV:92-93.
   - SE fase `implementando` ENTÃO próxima skill = sdd-implementar — IN:125-128; SI:88-89 (devolve os cenários reprovados, Passo 0).
3. OUTPUT GERADO:
   > 🔎 Verificação FT-031 — rodada 1 · Cenários: 2 aceitos · 1 rejeitados · 0 ambiente · VERIFICACAO: REJEITADO
   Achado: "1.2 — esperado 403, obtido 200, evidência <trecho>", Situação `aberto` (valor implícito; ST:31-32 só mostra `resolvido — tarefa <n>`).
   ARQUIVOS ESCRITOS: `verificacao.md` (❌ + evidência) · `status.md` (`fase: implementando`, achado, Histórico, Rodadas verificação 1) · `evidencias/` (se houver). Sem CT.csv.
4. VEREDITO MECÂNICO: DETERMINÍSTICO para a rodada única. Nota fora deste bloco: uma 2ª rejeição em sessão direta não tem limite nem escalonamento escrito (SV não tem; SI:81-83 cobre só a revisão).

**S16-F3 · Parada por DDL pendente (Banco = pendente)**

1. INPUT EXATO: "verifica a FT-031".
   ESTADO: status.md `Banco (DDL): pendente`; fase `revisando`; revisão APROVADO; MCP elm presente.
2. REGRA APLICADA:
   - SE sempre ENTÃO status.md `fase: verificando` + Histórico (Passo 1 vem antes do Passo 2) — SV:27.
   - SE sempre ENTÃO roteiro escrito em verificacao.md antes de executar — SV:29-39.
   - SE Banco = `pendente` ENTÃO pare: "a verificação depende da DDL aplicada em dev"; nenhuma execução — SV:48.
   - [sem regra] o que fica gravado após a parada (a fase continua `verificando`? vira `bloqueada`?) e qual é a saída. SV:84 trata bloqueio só depois da execução.
   - Próxima invocação: fase `verificando` → sdd-verificar, que para de novo — IN:129.
3. OUTPUT GERADO: texto "pare: a verificação depende da DDL aplicada em dev" (SV:48; sem template).
   ARQUIVOS ESCRITOS: `verificacao.md` (roteiro) · `status.md` (`fase: verificando`, Histórico).
4. VEREDITO MECÂNICO: SEM REGRA — o estado e a saída da parada por Banco pendente não estão escritos.

**S16-F4 · Geração do CT.csv (fatia aceita)**

1. INPUT EXATO: "gera os CTs" (pessoa, sessão em FT-031).
   ESTADO: status.md `fase: aceita`; verificacao.md com 1.1, 1.2 e 1.3 ✅ e evidências; sdd.md com a linha `CT.csv` da seção ELM (STEER:80); sem CT.csv ainda.
2. REGRA APLICADA:
   - SE o pedido é "gera os CTs" ENTÃO é gatilho da description — SV:3; o corpo só gera CT após ACEITO — SV:76, SV:86-88 (já ACEITO, condição cumprida).
   - SE "um caso por cenário verificado (aceito com evidência)" ENTÃO 3 casos — SV:88; CT:3.
   - Arquivo: `.kiro/specs/ft-031-bloquear-conta/CT.csv`, UTF-8 com BOM, quebra LF, separador `;`, gravado assim — CT:8-10.
   - Coluna 1 Tipo = Caso de Teste — CT:20; STEER:80.
   - Coluna 2 Resumo = `FT-031 Bloquear a conta após 3 tentativas : CT1.1 - <título do cenário>` — CT:21.
   - Coluna 3 Responsável = login do ELM de quem verificou — CT:22.
   - Coluna 4 Status = estado inicial do projeto — CT:23; STEER:80.
   - Coluna 5 Categoria = se houver; STEER:80 não traz categoria, então vazia — CT:24.
   - Coluna 6 Planejado para = sprint (iteração do EWM) — CT:25; sem fonte escrita.
   - Coluna 7 Descrição = OBJETIVO / PRÉ-CONDIÇÕES / PASSOS / RESULTADO ESPERADO / EVIDÊNCIA, entre aspas, aspas internas dobradas — CT:28-48.
   - CT:14-16 manda a ordem e os nomes do template do ETM (STEER:80); a ordem é a mesma de CT:18-26, sem conflito efetivo.
3. OUTPUT GERADO: texto livre: "CT.csv gerado em `.kiro/specs/ft-031-bloquear-conta/CT.csv`; importação fica para a consolidação" (SV:89-91).
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/CT.csv` · 3 casos · BOM + LF + `;`.
4. VEREDITO MECÂNICO: AMBÍGUO — (a) Responsável: fonte do login não escrita nesta skill (IN:102 × SS:35-36); (b) Planejado para: iteração sem fonte; (c) CT:12-26 não diz se a primeira linha do CSV é cabeçalho com os nomes das colunas.

**S16-X1 · Cenário errado no PRD (borda)**

1. INPUT EXATO: "verifica a FT-031" — o cenário 1.3 falha; a pessoa confirma que o PRD diz "bloqueio de 30 min" e a regra aprovada é "bloqueio até o suporte liberar".
   ESTADO: como S16-F1, com 1.3 ❌.
2. REGRA APLICADA:
   - SE REJEITADO ENTÃO achados no status.md e `fase: implementando` — SV:81-82.
   - SE o problema é o cenário estar errado no PRD ENTÃO diga isso: é com o P.O., não com o código — SV:82-83.
   - Conflito: SV:82 manda a sdd-implementar corrigir e reverificar; SV:83 diz que o problema não é do código.
   - [sem regra] fase ou handoff para "aguarda P.O."; IN:125-132 não tem esse estado.
3. OUTPUT GERADO: bloco `VERIFICACAO: REJEITADO` (SV:70-74) mais a frase "é com o P.O.".
   ARQUIVOS ESCRITOS: `status.md` (`fase: implementando`, achado) · `verificacao.md`.
4. VEREDITO MECÂNICO: CONFLITO — SV:82 ("a sdd-implementar corrige e a verificação roda de novo") × SV:83 ("é com o P.O., não com o código").

**S16-X2 · Verificação por agente sem MCP (ACEITO) (borda negativa)**

1. INPUT EXATO: evento do orquestrador: "verificar FT-031", delegado ao `sdd-verificador`, sem pessoa na sessão; todos os cenários ✅.
   ESTADO: sessão do agente com tools read/shell/write e sem MCP elm (AG-V); status.md `fase: revisando`.
2. REGRA APLICADA:
   - SV:17 — agente `sdd-verificador` é o preferido.
   - SE ACEITO ENTÃO CT.csv e `fase: aceita` — SV:76.
   - SE ACEITO e sem MCP nesta sessão ENTÃO grava `ELM pendente: lançar <h>h em [VER] FT-031` no Histórico — SV:77-80; SE:23-24.
   - [sem regra] o valor de `<h>`: SV:77 manda perguntar a quem verificou; o agente não tem a pessoa na sessão e SV não tem modo autônomo (grep de AUTONOMO em sdd-verificar: nenhum).
   - Escrita permitida pelo AG-V: verificacao.md, CT.csv, status.md, evidencias/, massa/.
3. OUTPUT GERADO: bloco `VERIFICACAO: ACEITO`; linha no Histórico `ELM pendente: lançar ?h em [VER] FT-031`.
   ARQUIVOS ESCRITOS: `verificacao.md` · `CT.csv` · `status.md` (`fase: aceita`, Histórico) · `evidencias/`.
4. VEREDITO MECÂNICO: AMBÍGUO — o valor de `<h>` não tem fonte no fluxo do agente; "0h" e linha sem valor são duas leituras.

**S16-X3 · Todos os cenários em ⚠️ ambiente (borda)**

1. INPUT EXATO: "verifica a FT-031" — serviço de teste fora do ar; 1.1, 1.2 e 1.3 com ⚠️.
   ESTADO: Banco `não se aplica`; app responde 503.
2. REGRA APLICADA:
   - SE falha por ambiente ENTÃO ⚠️ ambiente, não rejeição; diz o que faltou — SV:66.
   - SE só ⚠️ ambiente ENTÃO `fase: bloqueada` com o que falta; ninguém corrige código — SV:84.
   - Bloco SV:70-74: `VERIFICACAO: ACEITO | REJEITADO` — não há valor para este caso.
   - Formato da fase: SV:84 escreve `bloqueada`; ST:19 escreve `bloqueada (de: <fase>)` com motivo e pergunta exata.
3. OUTPUT GERADO: `🔎 Verificação FT-031 — rodada 1 · Cenários: 0 aceitos · 0 rejeitados · 3 ambiente` + linha `VERIFICACAO:` sem valor.
   ARQUIVOS ESCRITOS: `verificacao.md` (⚠️ + o que faltou) · `status.md` (`bloqueada`).
4. VEREDITO MECÂNICO: SEM REGRA — o template de saída só tem ACEITO | REJEITADO (SV:73). Também há ambiguidade no formato da fase (SV:84 × ST:19).

**S16-X4 · Misto: ✅ + ⚠️ sem ❌ (borda)**

1. INPUT EXATO: "verifica a FT-031" — 1.1 ✅, 1.2 ✅, 1.3 ⚠️ (fila de mensagens fora do ar).
   ESTADO: como S16-X3, mas só um cenário em ambiente.
2. REGRA APLICADA:
   - SE todos aceitos ENTÃO ACEITO — SV:76: falso, 1.3 não é aceito.
   - SE só ⚠️ ENTÃO bloqueada — SV:84: falso, há ✅.
   - SE REJEITADO ENTÃO esperado × obtido dos reprovados — SV:81: não há ❌; a condição de REJEITADO não está escrita (ver S16-F2).
   - [sem regra] decisão para ✅ + ⚠️.
3. OUTPUT GERADO: não determinado pelas regras.
   ARQUIVOS ESCRITOS: `verificacao.md` · `status.md` (indefinido).
4. VEREDITO MECÂNICO: AMBÍGUO — ACEITO por exclusão, REJEITADO ou bloqueada são todas plausíveis; nenhuma regra decide.

**Tabela-resumo S16**

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S16-F1 · Verificação ACEITA | AMBÍGUO | Responsável do CT (fonte do login) e número da rodada sem regra de cálculo |
| S16-F2 · Verificação REJEITADA | DETERMINÍSTICO | Rodada única. 2ª rejeição direta sem limite escrito |
| S16-F3 · Parada por DDL pendente | SEM REGRA | Estado e saída após o "pare" de Banco pendente não escritos |
| S16-F4 · Geração do CT.csv | AMBÍGUO | Responsável e Planejado para sem fonte; cabeçalho do CSV não definido |
| S16-X1 · Cenário errado no PRD | CONFLITO | SV:82 (implementar corrige) × SV:83 (é com o P.O., não com o código) |
| S16-X2 · Agente sem MCP, ACEITO | AMBÍGUO | Valor de `<h>` da [VER] sem fonte para o agente |
| S16-X3 · Todos ⚠️ ambiente | SEM REGRA | Linha VERIFICACAO sem valor (SV:73); formato de fase divergente |
| S16-X4 · ✅ + ⚠️ sem ❌ | AMBÍGUO | SV:76, SV:81 e SV:84 não decidem este caso |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1, F2, F3, X1, X3 | `.kiro/specs/<ft>-<slug>/verificacao.md` (SV:31; na worktree do loop: `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/verificacao.md`, SL:69, 75-76) | Sim: P3 escreveu `.kiro/specs/ft-031-bloquear-conta/verificacao.md`; relativo ao checkout da branch da fatia (SV:22). AG-V permite os dois caminhos (AG-V:33-34) | `.md` | Parcial. Blocos `### HF-01 · 1.2 — título` + Massa/Executar/Esperado/Verificar em (SV:34-38) e `Resultado/Obtido/Evidência` (SV:55-57) conferem. O bloco `VERIFICACAO: ACEITO\|REJEITADO` (SV:70-74) **não** diz se é gravado no arquivo (só impresso); sem título do arquivo; sem cabeçalho de rodada. P3 não viu | Escrito pelo verificador (AG-V) ou pela sessão. **Nenhum commit prescrito em SV.** Quem commita: no loop, o orquestrador (SL:93-94); fora do loop, só `sdd-implementar` Passo 0 na reentrada (SI:20-22). Passo 5 da `sdd-implementar` (SI:93-117, o passo que vem depois do ACEITO) só comita o `status.md` (SI:117). O workflow `sdd-entregar-fatia` termina na verificação sem commit | NÃO ESPECIFICADO: escrita negada/pasta ausente (SV não trata; só trata "Banco pendente" SV:48 e "⚠️ ambiente" SV:66). Permissão do agente: OK (AG-V:33-34). Rodada 2: se `verificacao.md` é sobrescrito ou acrescido (SV:82-83 "só os rejeitados + repetição") não está escrito | NÃO ESPECIFICADO (decisão não persistida no arquivo; commit pós-ACEITO fora do loop; sobrescrita × acréscimo na rodada 2) |
| F1, F2 | `.kiro/specs/<ft>-<slug>/evidencias/<ft>-<cenário>.<ext>` (SV:57, 63; ex. `evidencias/ft-031-1.2.png`) | Sim (P3: "`evidencias/` (se houver)"). Divergência sobre dado real: SV:57/63 mandam evidência para `evidencias/` (versionada); SV:98-100 e STEER:14 mandam evidência **com dado real** para `.kiro/local/verificacao/<ft>/` (fora do git). Conciliável (o segundo vale para o caso de dado real), mas SV:63 (screenshot de frontend em `evidencias/`) não faz a ressalva; no loop, `.kiro/local/verificacao/<ft>/` é relativo à raiz, enquanto SL:69 manda tudo pelo caminho `.kiro/local/wt/<ft>/…`: o subagente pode gravar em `.kiro/local/wt/<ft>/.kiro/local/verificacao/…`, caminho **não** permitido ao AG-V (AG-V só tem `.kiro/local/verificacao/**` na raiz, AG-V:43) | `.png` (browser), texto/trecho (API/batch); sem extensão prescrita para os demais | Sem template; só "resposta, consulta, linha de log, screenshot" (SV:57) | Binário (PNG) não passa pela ferramenta `write` de texto nem por `cp`/`mv` (fora do allow, AG-V:55-76): depende de o MCP de browser gravar direto em `evidencias/`. SV:63 não diz como. Commit: ver linha acima | NÃO ESPECIFICADO: `evidencias/` ou `.kiro/local/verificacao/<ft>/` ausentes (criação do diretório não dita). `.kiro/local/verificacao/**` está no allow do AG-V, mas **não** no allow do orquestrador (AG-O:39-44); AGR diz que subagente herda as regras de quem o chamou ("sem dizer se os allow se cruzam") | DIVERGENTE (SV:63 × SV:98-100 sem ressalva; caminho relativo à raiz × à worktree no loop) · NÃO ESPECIFICADO (como o PNG chega ao disco) |
| F1 (sem convenção) | `.kiro/specs/<ft>-<slug>/massa/` (SV:46); com convenção: a pasta do projeto (SV:45) | Sim para o fallback (P3 correto). Com convenção (ex. `src/test/resources/`, `sdd-setup/SKILL.md:102`) AG-V só escreve em `massa/` da fatia; AGR:52 diz que a setup acrescenta "a pasta de massa do projeto" ao write, mas o template AG-V não traz placeholder para isso | scripts/fixtures (`.sql`, `.json`, `.sh`); corpo HTTP em `.json` (http.sh:8) | `http.sh` exige corpo em `.kiro/specs/*/massa/*` ou `.kiro/local/wt/*/.kiro/specs/*/massa/*` e rejeita `..` (http.sh:31-35): bate com SV:61. Convenção do projeto × `massa/` da fatia: o script mora na convenção, o corpo tem de ser copiado para `massa/` (SV não diz) | Verificador grava; não commita (ver linha 1). `massa/` vai ao git (pasta da fatia): com dado real, SV:98 proíbe, mas não há checagem | NÃO ESPECIFICADO: pasta de convenção sem permissão de escrita no template; execução de script de massa (shell do AG-V só tem git e `sh .kiro/sdd/http.sh`; comandos de massa/Executar dependem da setup, AGR:51) | NÃO ESPECIFICADO (convenção × allowlist de escrita; corpo na convenção × `massa/` do http.sh) |
| F1, X2 (ACEITO) | `.kiro/specs/<ft>-<slug>/CT.csv` (CT:8; SV:88) | Sim (P3: `.kiro/specs/ft-031-bloquear-conta/CT.csv`). AG-V permite raiz e worktree (AG-V:35-36) | `.csv`, UTF-8 com BOM, LF, `;` (CT:8-10) | **Não confere inteiro com o template.** (a) Sem linha de cabeçalho prescrita: CT:12-26 lista colunas mas não diz se há cabeçalho; sem cabeçalho o BOM cola no 1º valor (`'﻿Caso de Teste'` lido com `utf-8`; some com `utf-8-sig`) (validado). (b) Só a Descrição é citada entre aspas (CT:26, 48): um `;` no Resumo (título do cenário) **não** é citado e abre 8ª coluna (validado: linha 1 do exemplo = 8 campos, linha 2 = 7). (c) `Resumo` = `CT<nn>` (CT:21): P3 escreveu `CT1.1`; o texto manda número do caso (`CT01`), não o id do cenário. (d) 7 colunas e ordem de CT:18-26 batem com STEER:80 | Escrito pelo verificador/sessão; **sem commit prescrito** (ver linha 1) → o `sdd-elm` modo *testes* (SE:205) lê o arquivo na consolidação, depois do merge (SV:89-91): só existe na base se tiver ido no PR. Sem `.gitattributes`, checkout com autocrlf (Windows, citado em CT:10) pode converter LF em CRLF | NÃO ESPECIFICADO: diretório da fatia ausente; permissão OK (AG-V:35-36). F2/X3 não geram CT.csv (SV:76): P3 correto | DIVERGENTE (P3 `CT1.1` × CT:21 `CT<nn>`) · NÃO ESPECIFICADO (cabeçalho; aspas fora da Descrição; commit antes do PR) |
| F4 ("gera os CTs", fase `aceita`) | `.kiro/specs/<ft>-<slug>/CT.csv` | Sim (mesmo caminho). Onde a sessão está não é dito: fatia `aceita` ainda na branch da fatia (SV:22), ou já na base se o PR foi mergeado | idem | idem; Responsável/Planejado para sem fonte (P3 correto) | Gerado depois do `aceita`: já pode haver PR aberto; CT.csv novo exige commit e push na branch da fatia, nada dito | NÃO ESPECIFICADO | NÃO ESPECIFICADO (commit/branch quando o CT é gerado pós-`aceita`) |
| F1, F2, F3, X1, X2, X3 | `.kiro/specs/<ft>-<slug>/status.md` (SV:27, 76, 81-84; ST) | Sim. AG-V permite (AG-V:37-38) | `.md`, tabela de campos (ST:3-16) | Fase conforme ST:18-19: `verificando`, `aceita`, `implementando`, `bloqueada (de: <fase>)`. SV:84 escreve só `bloqueada` (sem `(de: <fase>)`, motivo nem pergunta exata, ST:19): P3 acertou a nota. Achado na tabela `# \| Origem \| Achado \| Situação` (ST:34-35) ✓. **Rodadas:** ST:26-27 "O revisor e o verificador não incrementam"; SV:92-93 manda o verificador incrementar no pedido direto; o workflow `sdd-entregar-fatia` manda o **verificador** incrementar (prompt do passo `verificar`) enquanto ST:26 diz "o passo do codificador que vem depois" | Gravado pelo verificador/sessão; comitado como na linha 1 (loop: SL:92-94 comita; fora do loop: SI:117 comita o `status.md` do `pr-aberto`, junto) | F3 (Banco `pendente`): SV:48 "pare" sem dizer o estado deixado (fica `verificando`, com roteiro gravado e sem decisão): NÃO ESPECIFICADO. X2: `ELM pendente: lançar <h>h em [VER] FT-031` no Histórico (SV:79-80 ✓; formato do `<h>` sem fonte) | DIVERGENTE (SV:92-93 e workflow × ST:26-27; SV:84 × ST:19) · NÃO ESPECIFICADO (estado após parada por DDL) |
| F1 (com MCP) | ELM: horas e conclusão da `[VER]` (SV:77-79); registro local `ELM pendente` no `status.md` | n/a (ELM). P3 correto em "só após sim". Nota: o verificador (sem MCP, SE:23) nunca grava no ELM: só a sessão da pessoa com MCP | n/a | n/a | n/a | Falha do MCP → `ELM pendente` (SE:23-24) | OK |

Sem escrita: **S16-X4** (misto ✅+⚠️ sem ❌: SV não decide; o que fica gravado é indefinido, P3 correto).

#### Achados de persistência · S16
- `sdd-verificar/SKILL.md:76-93` · `sdd-implementar/SKILL.md:20-22, 93-117` · `AG-V:105-107`: o ACEITO deixa `verificacao.md`, `CT.csv`, `evidencias/` e `massa/` fora do git; o verificador não comita; o Passo 5 (PR) só comita `status.md`; o comando que comita esses arquivos (`FT-<nnn> registrar revisão/verificação`) só roda na reentrada pelo Passo 0. Fora do loop (sessão da pessoa e workflow `sdd-entregar-fatia`) o PR pode abrir sem CT.csv/evidência, e o `sdd-elm` *testes* (SE:205) depende do CT.csv na base. P3 disse "Nenhum commit prescrito" (confirmado) mas não tirou a consequência.
- `ct-csv.md:12-26, 48`: sem regra de cabeçalho, sem aspas no Resumo; reproduzido em `tmp/p4/ct-sample.csv` (8 campos na linha com `;` no título). P3 (S16-F4 c) viu só o cabeçalho; `CT1.1` em P3 contradiz `CT<nn>` (CT:21).
- `SV:63` × `SV:98-100`: screenshot de frontend vai para `evidencias/` (versionada), dado real vai para `.kiro/local/verificacao/<ft>/`; sem teste "esta tela tem dado real?" antes de gravar; no loop o caminho relativo da raiz conflita com SL:69 (tudo por `.kiro/local/wt/<ft>/…`), e AG-V só autoriza `.kiro/local/verificacao/**` na raiz (AG-V:43).
- `SV:70-74`: `VERIFICACAO: ACEITO | REJEITADO` só no bloco de saída; o revisor grava `VEREDITO` no arquivo, o verificador não. O orquestrador (SL:89) lê a decisão só de `fase:` do `status.md`.
- `ST:26-27` × `SV:92-93` × workflow `sdd-entregar-fatia` (passo `verificar`): três respostas diferentes para quem incrementa "verificação".

---


## S17 · sdd-consolidar

### Parte 2 — Plano do fluxo esperado (Sonnet)


Contexto comum (SC 1-98): executada na **sessão de uma pessoa** (nenhum agente `sdd-*.json` carrega `sdd-consolidar` — grep em `sdd-setup/assets/agents/*.json`: produto, codificador, orquestrador, revisor, verificador e pesquisador não a listam); escreve só na **base** (SC:17-19; STEER:188 "Artefatos de produto").

#### S17-F1 · Consolidação com MCP `elm` (fatia padrão/rápida, de épico ou sem épico)

- **Gatilho inicial**
  - Frases (description SC:3): "PR mergeado", "fecha a FT-031", "consolidar", "concluir a fatia", "a fatia foi entregue".
  - Evento: merge do PR por uma pessoa (SI:119 "Depois do merge: `sdd-consolidar`").
- **Pré-condições / arquivos lidos**
  - Fatia em `fase: pr-aberto`, PR **mergeado** (confere por `git branch -r --merged origin/<base>` ou ferramenta de PR) (SC:16-17).
  - Lê: `status.md`, `design.md` (Decisões técnicas, achados aceitos), `verificacao.md`, `decisoes.md` do épico/fatia (ou a **ficha** na fatia sem épico), conceitos de `elm/` (histórias e regras cobertas), bundle do ELM, `backlog.md`, `CT.csv`, `.kiro/steering/sdd.md` (seção ELM, Git, Artefatos de produto, caminhos de ADR e glossário).
  - MCP `elm` ativo na sessão; skills `elm`, `elm-rm`, `elm-ccm`, `elm-qm`, `elm-gc` (ELM:16-19).
- **Processamento interno**
  1. **Entrada** (SC:16-19): confirmado o merge, pergunta "Troco para `<base>`? (sim)" e faz `git pull --ff-only`; alterações locais não commitadas → avisa e **para** (nunca oferece descartar/`stash`/`reset`).
  2. **Passo 1 — Drift** (SC:23-35): compara entregue × documentação em 4 fontes (`design.md`; `verificacao.md`; `decisoes.md`/ficha; conceitos `elm/` × bundle: `stable` sem `resource` = publicação pendente; corpo do bundle ≠ conceito = alguém mudou no ELM). Drift de **negócio** (regra, cenário, valor) → mostra a diferença e aciona `sdd-prd` (mudança depois de aprovado) **antes de publicar** (fatia sem épico: a ficha, pela `sdd-triar`). Drift só técnico → nada no PRD.
  3. **Passo 2 — ELM** (SC:37-59), pela `sdd-elm`, **numa confirmação só** (prévia + "sim", ELM:29-30):
     - *requisitos* (publicação `no-merge` no `sdd.md`, ou drift do Passo 1) — conceitos `stable` com `verified` humano (ELM:87-91);
     - *regra da ficha* (fatia padrão sem épico com regra nova/alterada): gera conceito OKF as-built em `.kiro/specs/<ft>-<slug>/elm/`, mostra, e com o `verified` humano publica pelo modo *requisitos* (SC:42-44);
     - *especificação técnica* (só se o `sdd.md` diz "as-built no merge", ELM:213): gera ET as-built de `design.md` + código final, publica;
     - *testes*: `CT.csv` pronto para importar no ETM; após a importação, links "valida" (SC:47; ELM:203-209);
     - *horas*: o merge conclui `[DEV]` e `[REV]`; pergunta as horas de cada (descontando o já lançado) e lança via modo *horas*. O EWM só aceita horas do responsável: tarefa de outra pessoa → `ELM pendente: lançar <h>h em [REV] FT-nnn (<login>)` (SC:48-51);
     - *backlog*: conclui tarefas e IB no EWM (estado de conclusão da PA); concluída sem horas não trava, "a virada aponta" (SC:52-53).
     - Bundle do ELM no repositório (`rm.download.path`) → sugere rodar `elm-sync` (SC:58-59).
  4. **Passo 3 — Conhecimento que dura** (SC:61-71): ADRs de decisões "Vira ADR? sim" → ADR curto na pasta de ADRs (contexto · decisão · consequências · origem FT-nnn), mostra e grava com "ok"; glossário (termos novos/renomeados e `termo pendente` do `decisoes.md`) → corrige com "ok" ou abre correção de código como fatia; **lint do conhecimento** a cada épico concluído ou a pedido (contradições entre glossário, ADRs, bundle e steering) → lista de achados, cada um vira correção ou fatia.
  5. **Passo 4 — Fechar** (SC:73-83), na base: `status.md` com `fase: concluida` e data; `backlog.md` com `status: concluida`, `concluida-em` e ids de tarefa do campo ELM do `status.md` que a coluna `elm` ainda não tem; ADRs e glossário; todas as fatias do épico concluídas → épico `concluido` (PRD e backlog). Chama `sdd-aprender` modo **registrar** para cada correção humana (achados que chegaram à pessoa, verificações rejeitadas, mudanças pedidas no PR) e modo **retrospectiva** se a pessoa quiser. Commit (padrão do `sdd.md`) com `status.md`, `backlog.md` e o que mudou — direto ou por PR curto conforme "Artefatos de produto" (várias fatias podem ir no mesmo PR de consolidação). Branch da fatia pode ser apagada.
  6. **Passo 5 — Próximo** (SC:85-92): emite o resumo.
- **Resultado final esperado**
  - Resposta:
    ```
    ✅ FT-<nnn> concluída — <título>
    ELM: <publicado | pendente: …> · Drift: <nenhum | PRD v1.1>
    Épico EP-<nn>: <c>/<t> fatias · próxima pronta: FT-<…> (<AFK|HITL>, desbloqueada agora)
    Lições: <n> registradas
    ```
    + a saída da `sdd-elm` (`🏛️ ELM — <modo> · FT` com Criados/Atualizados/Sem mudança/Links/Conflitos, ELM:225-229).
  - Arquivos (na base): `.kiro/specs/<ft>-<slug>/status.md` (`fase: concluida`, data), `<produto>/backlog.md` (`status: concluida`, `concluida-em`, coluna `elm`), conceitos `elm/*.md` com `resource`/`id`/`sources` + `log.md` (gravados pela `sdd-elm`, ELM:41-44), ADR novo (pasta de ADRs do `sdd.md`), glossário, PRD/backlog do épico se concluído, `<produto>/aprendizado/licoes.md` (via `sdd-aprender`). Pasta da fatia **não** é apagada (SC:96-97).
  - Próximo passo: próxima fatia pronta do épico (`sdd-iniciar`); ações manuais no ELM (importar CT.csv, `elm-sync`, horas de outro responsável).
- **Lacunas observadas**
  - **`[VER]` fora do escopo de horas**: SC:48 só cita `[DEV]` e `[REV]`; as horas/conclusão da `[VER]` ficam para SV:77-80, que no agente/loop não fecha (ver S16-F1). O backlog (SC:52-53) conclui "as tarefas", incluindo a `[VER]`, possivelmente sem horas.
  - **Ordem de lint × conclusão do épico**: o lint roda "a cada épico concluído" (SC:69) no Passo 3, mas o épico só é marcado `concluido` no Passo 4 (SC:79). Não diz se o lint se refere ao épico que **esta** fatia está concluindo.
  - **Drift de negócio bloqueia o resto?** SC:34-35 manda acionar `sdd-prd`/`sdd-triar` "antes de publicar", mas não diz se o fluxo pausa (e como retoma o Passo 2) enquanto o P.O. aprova a nova versão.
  - **Detecção do merge**: `git branch -r --merged origin/<base>` (SC:16-17) não detecta squash/rebase merge; só a alternativa "ferramenta de PR" cobre esse caso, sem dizer o que fazer quando a ferramenta não existe.
  - **Worktree do loop**: SL:120 diz que as worktrees ficam "até o merge; remova depois (`git worktree remove .kiro/local/wt/<ft>`)", mas SC:82-83 só menciona apagar a branch; nenhum passo do consolidar remove a worktree, e o orquestrador nega `git worktree remove` (`sdd-orquestrador.json:95,192`) — handoff sem dono.
  - **Importação do CT.csv**: SC:47 "após a importação, links valida" supõe que a pessoa importou na mesma sessão; sem importação não há pendência padronizada (ver S16-F4).
  - **Fatia sem épico/direta/rápida** no Passo 5 (SC:90): a linha "Épico EP-<nn>: <c>/<t>…" não se aplica; o formato de saída não prevê esses casos.
  - A skill não está em nenhum agente (`sdd-produto` conduz o resto dos artefatos de produto, STEER:188, mas não carrega `sdd-consolidar`); só roda na sessão principal da pessoa.

#### S17-F2 · Consolidação sem MCP do ELM (ou com falha)

- **Gatilho inicial**: os mesmos de S17-F1, em sessão **sem** o MCP `elm`, ou com falha de chamada (SC:55-56).
- **Pré-condições / arquivos lidos**: as de S17-F1; ausência do MCP na sessão ou erro em alguma chamada.
- **Processamento interno**
  1. Entrada e Passo 1 (drift) idênticos a S17-F1 (o drift contra o bundle local ainda é possível; a checagem ao vivo não).
  2. Passo 2: nenhuma publicação. Para **cada ação** que seria feita (requisitos, regra da ficha, ET, testes, horas, backlog/conclusão) registra `ELM pendente: <ação>` no Histórico do `status.md` (SC:55-56; ELM:23-25). Horas: `ELM pendente: lançar <h>h em <tarefa> (<data>)` (ELM:196-197).
  3. O `sdd-status` lista as pendências até alguém executá-las numa sessão com MCP (SC:55-56; `sdd-status/SKILL.md:22`).
  4. Projeto que **não usa ELM** (`sdd.md` → ELM: não usa) → "nada a fazer" no Passo 2 (ELM:25).
  5. Passos 3 (ADR/glossário/lint), 4 (fechar: `fase: concluida`, `backlog.md` com `status: concluida`, `concluida-em`, `elm` com `ids` já no `status.md`) e 5 (resumo) seguem normalmente; `sdd-aprender` registrar idem.
- **Resultado final esperado**
  - Resposta: o mesmo resumo do Passo 5, com `ELM: pendente: <lista>`.
  - Arquivos: `status.md` (`fase: concluida` + linhas `ELM pendente:`), `backlog.md`, ADR/glossário/`licoes.md`; **nada** no ELM.
  - Próximo: numa sessão com MCP: "lança 2h na REV da FT-031" (SC:50-51), republicar requisitos, importar CT.csv, concluir tarefas.
- **Lacunas observadas**
  - **Pendência sem consumidor**: o `sdd-status` as **lista** (SC:55-56) mas nenhuma skill descreve o modo "esvaziar pendências" (re-executar cada `ELM pendente:` e registrar `ELM feito:`); `sdd-status/SKILL.md:22` pressupõe `ELM feito:` sem que `sdd-elm` o defina.
  - `fase: concluida` é gravada mesmo com pendências de requisito/backlog no ELM: o ELM "nunca trava o fluxo" (README/sdd/SKILL), mas o `backlog.md` fica sem ids na coluna `elm` quando o MCP faltou na criação; SC:77-78 só cobre os ids que já estão no `status.md`.
  - Falha **parcial** no meio do lote (SC:55 "ou com falha"): a idempotência está no `sdd-elm` (ELM:41-44) mas SC não diz como mostrar/registrar quais itens já foram publicados antes da falha.

#### S17-F3 · Consolidação da trilha direta

- **Gatilho inicial**: "PR mergeado" / "fecha a FT-031" para fatia de **trilha direta** em `pr-aberto` (SC:21; SI:121-129).
- **Pré-condições / arquivos lidos**: só `status.md` (a pasta tem só ele); `backlog.md`; `sdd.md` (seção ELM); merge confirmado e base atualizada (Entrada, SC:16-19).
- **Processamento interno**
  1. Entrada: confere merge; "Troco para `<base>`?"; `git pull --ff-only`.
  2. **Pula** Passo 1 (drift) e Passo 3 (conhecimento): "não há plano nem cenário para conferir" (SC:21).
  3. Passo 2 reduzido: *horas* (só a `[DEV]`, pergunta as horas descontando o lançado; lança pela `sdd-elm`; se a tarefa é de outra pessoa → `ELM pendente`) e *backlog* (conclui tarefa e item de origem, quando houver; direta não tem IB, ELM:137-138, 172-173).
  4. Passo 4: `status.md` `fase: concluida`; `backlog.md` `status: concluida`, `concluida-em` (+ ids ELM); `sdd-aprender` registrar se houve correção humana; commit.
  5. Passo 5: resumo.
- **Resultado final esperado**: resposta com bloco `✅ FT-<nnn> concluída` (Épico: "—"); arquivos `status.md`, `backlog.md`; pendências `ELM pendente` se aplicável; próximo: a próxima fatia/pedido.
- **Lacunas observadas**
  - SC:21 diz "só as *horas* e o *backlog* do Passo 2 e o Passo 4", mas não diz se o Passo 4 inclui a chamada à `sdd-aprender` e os ADR/glossário (o texto do Passo 4 mistura ambos); aqui interpretado como "Passo 4 inteiro, exceto ADR/glossário (Passo 3)".
  - O `[REV]` da direta: SC:48 "direta: só a `[DEV]`" (consistente com ELM:172-173) mas a `sdd-implementar` direta ainda exige revisão pela `sdd-revisar` (SI:126) sem tarefa `[REV]` para lançar horas — não fecha para quem revisa.
  - Formato do Passo 5 (SC:90) não prevê "direta".

#### S17-F4 · Parada na Entrada (PR não mergeado / alterações locais pendentes)

- **Gatilho inicial**: "fecha a FT-031" / "consolidar" com PR **não mergeado**, ou com alterações locais não commitadas na hora de trocar para a base.
- **Pré-condições / arquivos lidos**: `status.md` (`fase: pr-aberto`, link do PR), refs remotas, estado do PR.
- **Processamento interno**
  1. Confere merge (`git branch -r --merged origin/<base>` ou ferramenta de PR); **não mergeado → pare** (SC:16-17).
  2. Merge ok mas há alterações locais não commitadas → "avise e pare; nunca ofereça descartar, `stash` ou `reset`" (SC:18-19).
- **Resultado final esperado**: aviso curto (qual condição falhou); **nenhum** arquivo alterado; próximo: a pessoa faz/aguarda o merge, ou commita/descarta por conta própria, e repete o pedido.
- **Lacunas observadas**: fatia em `fase` diferente de `pr-aberto` (ex.: `aceita` com PR já aberto fora do fluxo, ou `bloqueada`) não é tratada (SC:16 só diz "em `pr-aberto`"). Sem texto de resposta padronizado para a parada.

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**S17-F1 · Consolidação completa (PR mergeado, MCP elm)**

1. INPUT EXATO: "PR mergeado, fecha a FT-031. Já importei o CT.csv: ids 9001, 9002, 9003."
   ESTADO: status.md `fase: pr-aberto`; merge commit de `feature/ft-031-bloquear-conta` em `develop` (aparece em `git branch -r --merged origin/develop`); árvore limpa; FT-031 no épico EP-03, com outras fatias pendentes; sdd.md: publicação de requisitos `no-merge` (STEER:72), ET `não publica` (STEER:72); conceitos de elm/ `stable` com `verified` humano; [DEV] 6h e [REV] 2h por lançar; [VER] já concluída (S16-F1); nenhum ADR nem termo novo; MCP elm presente.
2. REGRA APLICADA:
   - SE PR mergeado ENTÃO segue — SC:16-17.
   - SE "Troco para `develop`? (sim)" e a pessoa diz sim ENTÃO `git pull --ff-only` — SC:17-18.
   - SE alterações locais não commitadas ENTÃO avisa e para — SC:18-19 (não se aplica: árvore limpa).
   - Passo 1: compara as quatro fontes; sem drift ENTÃO nada no PRD — SC:23-35.
   - Passo 2, numa confirmação só, pela sdd-elm — SC:39-40.
   - SE publicação `no-merge` ENTÃO modo requisitos (conceitos `stable` com `verified`) — SC:40-41; SE:87-91.
   - SE fatia sem épico com regra nova, ou ET — não se aplica (épico; ET não publica) — SC:42-46; STEER:72.
   - SE testes ENTÃO links "valida" e "testado por" com os ids informados — SC:47; SE:205-209.
   - SE horas ENTÃO pergunta [DEV] e [REV] (descontando o já lançado) e lança modo horas — SC:48-51; SE:190-197.
   - SE backlog ENTÃO conclui tarefas e IB no EWM; [VER] já concluída, sem mudança — SC:52-53; SE:218-221.
   - SE bundle local ENTÃO sugere `elm-sync` — SC:58-59.
   - Passo 3: sem "Vira ADR? sim", sem termo novo; lint só ao concluir o épico (EP-03 não concluído) — SC:63-71.
   - Passo 4: status.md `fase: concluida` + data; backlog.md `status: concluida` + `concluida-em`; épico não concluído, não muda — SC:75-79; ST:11.
   - SE não há correção humana ENTÃO sdd-aprender não é chamado — SC:80-81; SA:28-31.
   - Commit com status.md e backlog.md — SC:82-83; direto na base, conforme STEER:61 do projeto.
   - Passo 5 — SC:85-92. Pasta da fatia não é apagada — SC:96-97.
3. OUTPUT GERADO:
   > ✅ FT-031 concluída — Bloquear a conta após 3 tentativas
   > ELM: publicado · Drift: nenhum
   > Épico EP-03: 2/5 fatias · próxima pronta: FT-033 (AFK, desbloqueada agora)
   > Lições: 0 registradas
   Mais o bloco da sdd-elm `🏛️ ELM — testes · FT-031` (SE:226-229).
   ARQUIVOS ESCRITOS: `.kiro/specs/ft-031-bloquear-conta/status.md` (`fase: concluida`, data) · `<produto>/backlog.md` (status, `concluida-em`, coluna elm) · conceitos `elm/*.md` com `resource`/`id`/`sources` e `log.md` (SE:41-44) · commit na base.
4. VEREDITO MECÂNICO: AMBÍGUO — "próxima pronta" e "desbloqueada agora" (SC:90) não têm regra de cálculo em SC; IN:33 define só "a pronta de maior prioridade da sprint aberta sem status.md"; "desbloqueada" (bloqueada-por concluída) aparece só em SL:30-31.

**S17-F2 · Consolidação sem MCP elm**

1. INPUT EXATO: "PR mergeado, fecha a FT-031" (sessão sem MCP elm).
   ESTADO: como S17-F1, sem MCP; conceitos `stable` sem `resource` (publicação pendente); [DEV] 6h e [REV] 2h por lançar.
2. REGRA APLICADA:
   - SE PR mergeado ENTÃO segue; pull — SC:16-19.
   - Passo 1: o drift contra o bundle local é possível, ao vivo não; conceito `stable` sem `resource` = publicação pendente — SC:32.
   - SE sem MCP nesta sessão ENTÃO `ELM pendente: <ação>` no Histórico, para cada ação — SC:55-56; SE:23-24.
   - SE horas de tarefa ENTÃO `ELM pendente: lançar <h>h em [REV] FT-nnn (<login>)` — SC:48-51; SE:196-197.
   - SE backlog ENTÃO pendência de conclusão — SC:52-53, SC:55-56.
   - Passos 3 e 4 seguem normalmente, com `fase: concluida` — SC:61-78.
   - Passo 5 com `ELM: pendente: <lista>` — SC:88-89.
3. OUTPUT GERADO:
   > ELM: pendente: requisitos (publicar elm/), lançar 6h em [DEV] FT-031, lançar 2h em [REV] FT-031, concluir backlog
   ARQUIVOS ESCRITOS: `status.md` (`fase: concluida` + linhas `ELM pendente:`) · `backlog.md` (sem ids novos) · commit na base. Nada no ELM.
4. VEREDITO MECÂNICO: AMBÍGUO — três formatos de `ELM pendente` para o mesmo caso: `ELM pendente: <ação>` (SC:55-56), `ELM pendente: <modo> <alvo>` (SE:23-24), `ELM pendente: lançar <h>h em <tarefa> (<data>)` (SE:196-197). Para horas, SC:50-51 e SE:196 concordam; para requisitos e backlog, não.

**S17-F3 · Trilha direta**

1. INPUT EXATO: "PR mergeado, fecha a FT-040".
   ESTADO: FT-040 trilha direta ("texto do rodapé do e-mail"); pasta só com status.md (ST: Origem `DF 4567`, ELM `[DEV] 4521 (direta: só [DEV])`, Rodadas revisão do código 1); `fase: pr-aberto`; PR mergeado; MCP elm presente; backlog.md com a linha FT-040.
2. REGRA APLICADA:
   - SE PR mergeado ENTÃO segue; pull — SC:16-19.
   - SE trilha direta ENTÃO só horas e backlog do Passo 2 e o Passo 4; pula Passos 1 e 3 — SC:21.
   - SE direta ENTÃO horas só da [DEV] → pergunta as horas da [DEV] 4521 (descontando) — SC:48; SE:190-197.
   - Concluir "as tarefas e o item de backlog da fatia" — SC:52-53; direta não tem IB (SE:138; SE:172-173); o DF 4567 é item de origem externo, e SC não diz se ele é concluído.
   - Passo 4: status.md `fase: concluida`; backlog.md `status: concluida`, `concluida-em` — SC:75-78.
   - Passo 5 — SC:88-92: o template traz `Épico EP-<nn>` e `próxima pronta`; não há caso para direta.
3. OUTPUT GERADO: `✅ FT-040 concluída — <título>`; a linha de épico não tem valor previsto.
   ARQUIVOS ESCRITOS: `status.md` · `backlog.md` · commit na base; ELM: horas da [DEV] só após "sim".
4. VEREDITO MECÂNICO: SEM REGRA — o Passo 5 (SC:88-92) não prevê trilha direta, e nenhuma regra manda concluir ou fechar o item de origem DF 4567.

**S17-F4 · Parada: PR não mergeado**

1. INPUT EXATO: "fecha a FT-031".
   ESTADO: status.md `fase: pr-aberto`; PR aberto e não mergeado; `git branch -r --merged origin/develop` não lista a branch; árvore limpa.
2. REGRA APLICADA:
   - SE PR não mergeado ENTÃO pare — SC:16-17.
3. OUTPUT GERADO: aviso curto dizendo que o merge não foi confirmado (texto livre; SC sem template).
   ARQUIVOS ESCRITOS: nenhum.
4. VEREDITO MECÂNICO: DETERMINÍSTICO.

**S17-X1 · Fase `aceita` com PR mergeado fora do fluxo (borda)**

1. INPUT EXATO: "a fatia foi entregue" (FT-031).
   ESTADO: status.md `fase: aceita`; PR já mergeado (aberto fora do fluxo); árvore limpa.
2. REGRA APLICADA:
   - SE o pedido casa a description ENTÃO a skill carrega — SC:3.
   - SC:16 — a entrada é fatia em `pr-aberto`; esta está em `aceita`; não há regra para fase diferente.
   - IN:130 — `aceita` → sdd-implementar (Passo 5, abrir o PR); aponta para um PR que já foi mergeado.
   - SS:70-81 — lista as inconsistências; "aceita com PR mergeado" não está.
3. OUTPUT GERADO: não determinado.
   ARQUIVOS ESCRITOS: nenhum.
4. VEREDITO MECÂNICO: SEM REGRA — SC não trata a fase, IN:130 roteia para abrir PR, e SS não aponta a inconsistência.

**S17-X2 · Squash merge (borda)**

1. INPUT EXATO: "PR mergeado, fecha a FT-031" — PR feito com squash em `develop`.
   ESTADO: `git branch -r --merged origin/develop` não lista a branch (o commit squash não é ancestral); MCP elm presente; sdd.md: abrir PR com `gh pr create` (STEER:60).
2. REGRA APLICADA:
   - SC:16-17 — confirma por `git branch -r --merged origin/<base>` ou pela "ferramenta de PR"; não mergeado → pare.
   - STEER:60 — a ferramenta cadastrada é `gh` para criar PR; nenhum comando de consulta de estado é escrito.
3. OUTPUT GERADO: depende da ferramenta escolhida (não determinado).
   ARQUIVOS ESCRITOS: nenhum até confirmar.
4. VEREDITO MECÂNICO: AMBÍGUO — "ferramenta de PR" pode ser `gh` (STEER:60), perguntar à pessoa ou o "pare" de SC:17; nenhuma regra diz qual comando consulta o merge.

**S17-X3 · Drift de negócio durante a consolidação (borda)**

1. INPUT EXATO: "PR mergeado, fecha a FT-031".
   ESTADO: verificacao.md mostra que o limite de 3 tentativas virou 5 (decisão de negócio ajustada na verificação); PRD v1.0 diz 3; MCP presente.
2. REGRA APLICADA:
   - SE drift de negócio ENTÃO mostra a diferença e aciona sdd-prd (mudança depois de aprovado) antes de publicar — SC:34-35.
   - SE há publicação pendente ENTÃO a publicação espera a nova versão do PRD — SC:34-35 ("antes de publicar"), SC:37-40.
   - [sem regra] se os Passos 2 a 5 param enquanto o P.O. aprova a versão nova, ou seguem com `fase: concluida`.
3. OUTPUT GERADO: diferença mostrada + pedido para acionar sdd-prd.
   ARQUIVOS ESCRITOS: nenhum até a nova versão do PRD.
4. VEREDITO MECÂNICO: AMBÍGUO — "antes de publicar" pode significar só a publicação (Passos 3 a 5 seguem) ou a consolidação inteira (pausa); SC:34-35 não diz.

**Tabela-resumo S17**

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S17-F1 · Consolidação completa | AMBÍGUO | "Próxima pronta" e "desbloqueada agora" (SC:90) sem regra de cálculo |
| S17-F2 · Sem MCP elm | AMBÍGUO | Três formatos de `ELM pendente` (SC:55-56; SE:23-24; SE:196-197) |
| S17-F3 · Trilha direta | SEM REGRA | Passo 5 sem caso de direta; item de origem DF 4567 não tratado |
| S17-F4 · PR não mergeado | DETERMINÍSTICO | Para em SC:16-17 |
| S17-X1 · Fase aceita com PR mergeado | SEM REGRA | SC:16 exige pr-aberto; IN:130 manda abrir PR; SS não aponta |
| S17-X2 · Squash merge | AMBÍGUO | "Ferramenta de PR" sem comando de consulta (STEER:60) |
| S17-X3 · Drift de negócio | AMBÍGUO | "Antes de publicar" não diz se a consolidação pausa (SC:34-35) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1, F2, F3 | `.kiro/specs/<ft>-<slug>/status.md` na **base** (SC:17, 76-77) | Sim (P3: base `develop`). A pasta da fatia já está na base pelo merge (SC:83) | `.md` | `fase: concluida` + data ✓ (ST:18-19). A "data" não tem campo (só no Histórico, ST:37-42): sem formato | **Base**, escrito pela sessão da pessoa. Commit "padrão do `sdd.md`" (SC:82), junto com `backlog.md`. Push/PR: SC não diz; vale STEER:61 (`PR curto` é o padrão da setup, `sdd-setup/SKILL.md:115`) e STEER:13 ("push só com sim") — mas SC:17-19 manda commitar **na base local** e não nomeia branch para o PR curto: se a base é protegida, o commit fica local e diverge de `origin/<base>`; o próximo `git pull --ff-only` (SC:18) falha | Árvore suja → avise e pare (SC:18-19) ✓. PR não mergeado → pare (SC:17) ✓. `pull --ff-only` falhando (base divergiu) → NÃO ESPECIFICADO. Agente: nenhum agente carrega a skill; AG-P não escreve `status.md` (AG-P write) | NÃO ESPECIFICADO (nome da branch do PR curto e destino do commit local na base protegida; agente que executa) |
| F1, F2, F3 | `<produto>/backlog.md` na base (SC:77; BK:6, 66) | Sim. `<produto>` = pasta do `sdd.md` | `.md`, tabelas | `status: concluida`, `concluida-em` `AAAA-MM-DD`, coluna `elm` com `<prefixo> [<id>](<url>) · …` (BK:53-54) ✓ P3. Linha na seção do épico (13 colunas) ou "sem épico" (14 colunas, BK:27, 33) | Mesmo commit do `status.md`; BK:82 manda "commit pequeno só com ele" quando não houver outro artefato de produto junto: SC:82 junta tudo, coerente | Conflito no `backlog.md` → BK:84 (mantenha o remoto) ✓. Falta do arquivo: n/a | OK (F3 direta: SC:21 só horas + backlog + Passo 4: P3 coerente) |
| F1 | `<produto>/epicos/<EP>-<slug>/elm/*.md`, `index.md`, `log.md` (SE:41-43, 87; okf-elm.md:19, 146-162) — requisitos `no-merge` (STEER:72) | P3 escreveu "`elm/*.md`… e `log.md`" sem caminho; o certo é a pasta `elm/` do **épico**. Fatia sem épico: `.kiro/specs/<ft>-<slug>/elm/` (SC:42-44; SE:87-89) | `.md` com frontmatter YAML (OKF v0.2); `log.md` seções `## AAAA-MM-DD`, mais novo primeiro | `resource`, `id` e `sources` por conceito + linha `**Publication**` no `log.md` (SE:111-113) ✓ | **Segundo commit** do `sdd-elm`: `<FT\|EP> - Publicar no ELM` (SE:42-43, 118) além do commit de SC:82. Na base. Falha no meio: ids já gravados ficam (SE:43-44) | Sem MCP → só `ELM pendente` (SC:55-56); conceito sem `verified` humano não publica (SE:90) | DIVERGENTE (P3 sem caminho; dois commits em duas skills, SC:82 × SE:42-43) |
| F1 | `verificacao.md` e `status.md`: ids dos CT importados (SE:209 "Registre os ids no `verificacao.md` e no `status.md`") | Base, pasta da fatia | `.md` | Sem formato para registrar os ids | Gravado na consolidação, **não listado** em SC:77-78 (Passo 4 cita só `status.md`, `backlog.md`, ADR, glossário) nem em P3 (P3 lista `status.md`, `backlog.md`, conceitos) | NÃO ESPECIFICADO | DIVERGENTE (SC:77-82 omite o que SE:209 manda gravar; P3 também omitiu) |
| F1 | glossário (`<docs/glossario.md>`, coluna ELM do termo, SE:112-113; Passo 3 SC:66-68) | Caminho do `sdd.md` (seção Projeto, STEER:30) | `.md` | Sem template | Correção "com ok" (SC:68); commit idem | **`sdd.md` = "não há"** para glossário/ADR (STEER:30): SC:63-68 não diz o que fazer (criar? pular?) → NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| F1 (se houver) | ADR: arquivo na pasta de ADRs do `sdd.md` (SC:63-65) | Pasta vem de STEER:30; sem nome/numeração de arquivo | `.md` | "contexto · decisão · consequências · origem FT-nnn" (SC:64-65), sem template em `references/` | "mostre e grave com ok"; commit junto (SC:82) | Pasta "não há" (STEER:30) → NÃO ESPECIFICADO | NÃO ESPECIFICADO (nome/numeração; pasta inexistente) |
| F2 | `ELM pendente: <ação>` no Histórico do `status.md` (SC:55-56) | `status.md` na base | linha de texto | Três formatos para o mesmo caso (SC:55-56 `<ação>`; SE:23-24 `<modo> <alvo>`; SE:196-197 `lançar <h>h em <tarefa> (<data>)`) e **três lugares**: `status.md` (SC:55, SE:23), "rodapé do PRD" para épico (SE:24; SC:55 diz status.md para requisitos de épico), `sprint-<nn>.md` (SE:197). `ELM feito:` (ST:40) não é gravado por SC | Mesmo commit | n/a | DIVERGENTE (lugar da pendência de requisitos de épico: SE:24 rodapé do PRD × SC:55-56 `status.md`; P3 só citou `status.md`) |
| F1 (último da série) | `prd.md` do épico (`status: concluido`) e linha do épico em `backlog.md` (SC:79; BK:43) | `<produto>/epicos/<EP>-<slug>/prd.md` | `.md` frontmatter | só se todas as fatias estiverem concluídas; F1 tem pendentes, P3 certo em não gravar | idem | n/a | OK |
| F1 (revisão de conhecimento) | lint do conhecimento (SC:69-71): "liste como achados" | sem arquivo prescrito | — | — | só listado no chat | NÃO ESPECIFICADO onde ficam os achados | NÃO ESPECIFICADO |
| F1 | worktree `.kiro/local/wt/<ft>/` e branch da fatia após o merge (SC:83 "branch pode ser apagada"; SL:120 "remova depois: `git worktree remove`") | n/a | n/a | n/a | `git worktree remove` está **negado** em todos os agentes (AG-V:81, AG-O:95); SC não manda remover; `git branch -d` não está no allow de ninguém; a branch não sai enquanto a worktree existir | NÃO ESPECIFICADO quem remove e quando | NÃO ESPECIFICADO |

Sem escrita: **S17-F4** (PR não mergeado: para em SC:16-17, P3 correto) · **S17-X1** (fase `aceita` com PR mergeado: SC:16 só aceita `pr-aberto`) · **S17-X2** (squash: "ferramenta de PR" sem comando) · **S17-X3** (drift de negócio: nada até a nova versão do PRD; quando houver, `sdd-prd` grava o PRD na base).

#### Achados de persistência · S17
- `SC:17-19, 75-83` × `STEER:61` × `sdd-setup/SKILL.md:115`: o padrão da setup é "PR curto para a base", mas a skill manda trocar para a base, pull e commit nela; não há nome de branch para o PR curto nem tratamento do commit local que sobra na base. Vale igual para `sdd-aprender` (SA:19-21) e para `sdd-triar/prd/fatiar`.
- `SC:77-82` × `SE:42-43, 118, 209`: a consolidação grava mais do que SC lista (conceitos `elm/` do épico, `index.md`, `log.md`, coluna ELM do glossário, ids de CT em `verificacao.md`) e há um segundo commit do `sdd-elm`.
- `SC:55-56` × `SE:24, 196-197`: onde fica o `ELM pendente` depende da skill que se lê.
- `STEER:30` ("`não há`" para glossário/ADRs) × `SC:63-68`: sem regra para pasta ausente.
- `SL:120` × `SC:83` × todos os `AG-*` negando `git worktree remove`: ninguém tem a incumbência de apagar a worktree; ela e a branch ficam (a worktree também retém uma cópia da pasta da fatia com `status.md` em `pr-aberto`, lido por `sdd-status` em "worktrees", `sdd-iniciar/SKILL.md:24`).
- `AG-P`/`AG-C`: nenhum agente tem as skills nem permissão para escrever `status.md` na base; P3 não perguntou qual sessão executa.

---


## S18 · sdd-aprender

### Parte 2 — Plano do fluxo esperado (Sonnet)


Contexto comum (SA 1-97): arquivos versionados `<produto>/aprendizado/licoes.md` (log, só acréscimo) e seção **Regras aprendidas** de `.kiro/steering/sdd.md` (STEER:220-227). Os dois só mudam na **branch base**: antes de gravar `git switch <base>` + `git pull --ff-only` (com alterações pendentes na branch da fatia → commite ou peça à pessoa); depois, commit pequeno + push ou PR curto com o "sim" (SA:19-21). Ordem de preferência: (1) mecânico → checagem determinística (lint/teste/hook/CI), não vira texto; (2) julgamento → Regras aprendidas; (3) domínio → glossário/ADR/PRD/ELM; (4) stack → skill do toolkit (SA:23-26). Nenhum agente carrega `sdd-aprender` (grep nos `agents/*.json`); roda na sessão principal.

#### S18-F1 · Registrar lição

- **Gatilho inicial**
  - Frases (description SA:3): "isso está errado, aprenda", "registra a lição", "o agente sempre erra X".
  - Eventos (SA:30-31): achado da revisão que chegou ao humano, cenário rejeitado na verificação, PR com mudança pedida, pessoa dizendo "não é assim", bloqueio por falta de informação; chamada do `sdd-consolidar` Passo 4 (SC:80-81); e "quando a revisão, a verificação ou o PR reprovarem algo que um humano teve de corrigir" (SA:3).
- **Pré-condições / arquivos lidos**: `status.md` da fatia (Histórico/achados), `revisao-*.md`, `verificacao.md`, o PR, `<produto>/aprendizado/licoes.md` (para a numeração `L-<nnn>` e para detectar recorrência), `.kiro/steering/sdd.md`.
- **Processamento interno**
  1. **Base**: `git switch <base>` + `git pull --ff-only` (SA:19-21).
  2. **Fatos** (só verificados; o que a pessoa disse é registrado como dito por ela): o que foi feito (`arquivo:linha`, trecho) × o que era o certo; onde a informação certa estava — ou que não estava em lugar nenhum (SA:33-35).
  3. **Causa** (SA:36-46): propõe uma de `contexto-ausente | contexto-ignorado | prd-incompleto | plano-errado | revisao-branda | skill-desatualizada | ambiente`; **a pessoa confirma**. Cada causa traz a correção na fonte (ex.: `contexto-ignorado` mecânico → checagem determinística, senão regra; `prd-incompleto` → `sdd-prd` + publicar no ELM; `plano-errado` → R-nn aplica a plano; `revisao-branda` → R-nn aplica a revisor — rubricas ficam no power e não são editadas no projeto; `skill-desatualizada` → corrigir a skill do toolkit e avisar quem mantém; `ambiente` → registrar, **não vira regra**).
  4. **Grava** em `licoes.md` (SA:48-55):
     ```
     ## L-<nnn> · <AAAA-MM-DD> · FT-<nnn> · <causa>
     - Feito: <…> (`arquivo:linha`)
     - Certo: <…> — fonte: <onde estava | "não estava escrito">
     - Correção na fonte: <proposta> · Situação: <proposta | aplicada | promovida → R-<nn> | descartada>
     ```
  5. **Recorrência** (SA:57): mesma causa e mesmo tipo de erro já registrado (2ª ocorrência) **ou** a pessoa pede → propõe a promoção (→ S18-F2).
  6. Commit pequeno e push/PR curto com o "sim" da pessoa (SA:20-21).
- **Resultado final esperado**
  - Resposta: resumo da lição (L-nnn, causa, correção proposta na fonte, Situação) e, se for o caso, a proposta de promoção.
  - Arquivos: `<produto>/aprendizado/licoes.md` (+1 seção `L-<nnn>`, só acréscimo); commit na base.
  - Próximo: promover (F2), aplicar a correção na fonte (checagem, PRD v+1 via `sdd-prd`, skill do toolkit), ou nada (`ambiente`).
- **Lacunas observadas**
  - **Base × worktree do loop**: SA:19-21 exige `git switch <base>`; numa worktree do `sdd-loop` (SL:56-60), a base já está em uso no checkout principal e a troca falha. Não há instrução para registrar lição a partir de dentro da worktree nem a partir do orquestrador (que não carrega a skill).
  - **Detecção da recorrência** (SA:57) não manda ler `licoes.md` (só o `sdd-revisar`/`SKILL.md:48` o faz): "mesmo tipo de erro" não tem critério de igualdade (tag/título).
  - **Numeração** `L-<nnn>`/`R-<nn>` sem regra de cálculo (próximo livre?); sem dono quando duas sessões gravam em paralelo.
  - **Correção na fonte** para `skill-desatualizada`/regra de stack ("avisar quem mantém", SA:45, 71-72) não tem canal nem artefato: o handoff termina em texto.
  - **Checagem determinística** (SA:23-24, 41): a skill diz "ponto final, não vira texto", mas não diz quem cria o lint/hook/teste nem onde a `Situação` fica rastreada (tem `aplicada`, sem referência).
  - Gatilho "bloqueio por falta de informação" (SA:31) e "o agente sempre erra X" (SA:3) não têm passo de coleta de fatos quando não há achado formal.
  - Mudança/lição no loop AFK: SL:115 lista "Lições para registrar", mas o orquestrador não tem a skill nem escrita em `<produto>/aprendizado/` (verificado em `sdd-orquestrador.json`: escrita só em `.kiro/local/loop-*.md`, worktrees, etc.).

#### S18-F2 · Promover regra para "Regras aprendidas" do steering

- **Gatilho inicial**: proposta do Modo registrar (2ª ocorrência mesma causa/tipo, SA:57) **ou** pedido da pessoa ("promove a L-007", "vira regra").
- **Pré-condições / arquivos lidos**: `licoes.md` (lições de origem `L-nnn`), seção "Regras aprendidas" do `.kiro/steering/sdd.md`; base atualizada (SA:19-21).
- **Processamento interno**
  1. Verifica a ordem de preferência: se o erro é **mecânico** → não promove, aponta checagem determinística (SA:23-24); conhecimento de domínio/stack → glossário/ADR/PRD/skill (SA:25-26).
  2. Redige a regra **curta, imperativa, verificável e com exemplo** (SA:61-68):
     ```
     ### R-<nn> · <título> · aplica a: <codificador | revisor | plano | PRD | todos> · severidade: <BLOQUEANTE | IMPORTANTE>
     <A regra em 1–2 frases imperativas.>
     - ✅ <exemplo certo> · ❌ <exemplo errado>
     - Origem: L-<nnn>, L-<nnn>
     ```
  3. **Mostra o diff** da seção Regras aprendidas do `sdd.md` e **grava só com "ok"** (o resto do arquivo não muda) (SA:70-71; Regras SA:97).
  4. Regra pertence à stack → **propõe também** levá-la para a skill do toolkit (SA:71-72).
  5. Atualiza a `Situação` da lição para `promovida → R-<nn>` (SA:54).
  6. **Manutenção** (SA:74-77): regras que viraram checagem determinística, rubrica, ADR ou skill saem da seção com `→ movida para <destino>` no `licoes.md`. Lições reais viram **casos de avaliação** em `<produto>/aprendizado/avaliacoes/` (pedido + resultado esperado) para conferir quando o modelo/fluxo mudar.
  7. Commit pequeno + push/PR curto com "sim" (SA:20-21).
- **Resultado final esperado**
  - Resposta: o diff da seção; após "ok", confirmação da gravação.
  - Arquivos: `.kiro/steering/sdd.md` (seção **Regras aprendidas**; só ela), `<produto>/aprendizado/licoes.md` (Situação → `promovida → R-<nn>` ou `→ movida para <destino>`), opcional `<produto>/aprendizado/avaliacoes/<caso>` (formato não especificado).
  - Próximo: o `sdd-revisar` cobra a regra como item de rubrica e o plano a respeita (STEER:222-223); proposta paralela à skill do toolkit, se for de stack.
- **Lacunas observadas**
  - **Casos de avaliação** (SA:75-77): "guarde o pedido e o resultado esperado em `avaliacoes/`" sem formato, nome de arquivo, quando criar nem quem os executa (README:205 diz que a execução automatizada é "v2"): handoff aberto e sem verificação.
  - Placeholder `<!-- Nenhuma regra promovida ainda. -->` (STEER:227): SA não manda removê-lo na 1ª promoção.
  - Regra com `aplica a: PRD` ou `plano` (SA:64, 43): a skill não diz quem (`sdd-revisar` rubrica P/L) lê a seção para PRD e plano; só consta no steering "O revisor as cobra…" (STEER:222-223) — sem a lista de quais rubricas leem quais `aplica a:`.
  - "Mantenha a seção curta" (SA:74): sem limite numérico nem gatilho de revisão periódica (nem cadência no `sdd-planejamento`: só SA:79 retrospectiva).
  - **Edição do steering na base com "ok"** vs. regra do steering "troca de branch e push só com sim" (STEER:140): ok, mas a promoção pode ocorrer enquanto a fatia está em outra branch — resolvido só por "commite ou peça" (SA:19-20).

#### S18-F3 · Retrospectiva (fatia, épico ou sprint)

- **Gatilho inicial**
  - Frases (description SA:3): "retrospectiva", "resumo das lições".
  - Eventos: `sdd-consolidar` Passo 4 "modo retrospectiva se a pessoa quiser" (SC:80-81); `sdd-planejamento` (retrospectiva com dados, `sdd-planejamento/SKILL.md:115`); `sdd-loop` sugere "na retrospectiva" tratar tipo de fatia como HITL (SL:136).
- **Pré-condições / arquivos lidos**: `status.md` das fatias (Histórico), `revisao-*.md`, `verificacao.md`, `licoes.md`, `backlog.md` (SA:91-92).
- **Processamento interno**
  1. Define o escopo: FT, EP ou Sprint N.
  2. Levanta **dados, não impressões** (SA:81): fatias concluídas, lead time médio (dias), retrabalho (rodadas de revisão / verificações), L-nnn por causa, autonomia (AFK × HITL; quantas AFK chegaram ao PR sem intervenção).
  3. Formula as **propostas** (promoções, rubricas, skills, steering).
  4. Emite o bloco:
     ```
     🔁 Retrospectiva — <FT | EP | Sprint N>
     Fluxo: <fatias concluídas> · lead time médio <d> dias · retrabalho <n> rodadas de revisão / <n> verificações
     Onde o humano corrigiu: <lista de L-nnn por causa>
     Autonomia: AFK <n> (<x> chegaram ao PR sem intervenção) · HITL <n>
     Propostas: <promoções, rubricas, skills, steering>
     ```
  5. **Termina perguntando quais propostas aplicar** (SA:91-92); as aceitas seguem pelo Modo promover (F2) ou pelas outras fontes.
- **Resultado final esperado**
  - Resposta: o bloco acima + pergunta final "quais propostas aplicar?".
  - Arquivos: nenhum por padrão (a skill não manda gravar a retrospectiva); eventuais promoções/lições seguem as regras de F1/F2.
  - Próximo: aplicar propostas aceitas; sprint: continua com a virada/`sdd-planejamento`; sugerir tratar tipo de fatia que bloqueia muito como HITL (SL:136).
- **Lacunas observadas**
  - **Retrospectiva não é persistida** em lugar nenhum (SA:79-92): nem `licoes.md` nem arquivo próprio — o resultado desaparece com a conversa, embora os dados venham de arquivos e o `sdd-planejamento` use a retrospectiva da sprint.
  - Fontes (SA:91): como calcular "lead time", "rodadas" e "chegaram ao PR sem intervenção" não está definido (os `status.md` de fatias concluídas moram na base, mas a **rodada** está em `Rodadas` do `status.md`; não é dito).
  - **"Resumo das lições"** (description SA:3) não corresponde a nenhum modo — não é Registrar, Promover ou Retrospectiva; falta passo (listar `licoes.md` por causa/situação?).
  - Retrospectiva de sprint é também chamada pelo `sdd-planejamento` (linha 115), mas o texto de SA só descreve "fim de fatia, épico ou sprint" sem tratar a sprint com horas (relatório de horas da `sdd-elm`, ELM:199-201).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**S18-F1 · Registrar lição**

1. INPUT EXATO: "isso está errado, aprenda: usou LocalDate.now() no BloqueioService; o design.md manda Clock injetado".
   ESTADO: branch `feature/ft-031-bloquear-conta`, árvore limpa, base `develop`; achado da revisão já chegou à pessoa; `<produto>/aprendizado/licoes.md` com L-001 a L-006; design.md "Decisões técnicas" contém "Clock injetado" (escrito); STEER "Regras aprendidas" com o placeholder (STEER:100).
2. REGRA APLICADA:
   - SE achado da revisão chegou ao humano, ou "isso está errado, aprenda" ENTÃO modo registrar — SA:3; SA:28-31.
   - SE não está na base ENTÃO `git switch develop` + `git pull --ff-only`; troca de branch só com "sim" — SA:19-21; STEER:13.
   - Fatos: o feito (`BloqueioService.java:<linha>`) × o certo (Clock injetado); fonte: design.md, "estava escrito" — SA:33-35.
   - Causa: propõe uma das sete (SA:38-46) e a pessoa confirma — SA:36.
   - Escolha: `contexto-ignorado` (SA:41), porque a regra estava escrita.
   - SE contexto-ignorado e mecânico ENTÃO checagem determinística; senão regra em Regras aprendidas — SA:41; "mecânico" definido em SA:23-24 só por exemplos (lint, teste, hook, CI).
   - Grava `## L-007 · 2026-10-15 · FT-031 · contexto-ignorado` com Feito, Certo, Correção na fonte e Situação — SA:48-55.
   - SE é a 1ª ocorrência ENTÃO não promove — SA:57.
   - Commit pequeno; push ou PR curto com "sim" — SA:20-21.
3. OUTPUT GERADO: resumo com L-007, causa contexto-ignorado, correção proposta e `Situação: proposta` (SA:50-55; sem template de resposta).
   ARQUIVOS ESCRITOS: `<produto>/aprendizado/licoes.md` (+ seção L-007, só acréscimo) na base · commit após "sim".
4. VEREDITO MECÂNICO: AMBÍGUO — (a) mecânico × julgamento sem critério operacional (SA:23-24, SA:41), o que decide entre checagem e regra; (b) numeração `L-<nnn>` sem regra de cálculo (SA:51).

**S18-F2 · Promover regra (2ª ocorrência)**

1. INPUT EXATO: "promove a L-007, vira regra".
   ESTADO: licoes.md com L-003 e L-007 (mesma causa, contexto-ignorado, classificadas como julgamento; Situação `proposta`); STEER "Regras aprendidas" com o placeholder (STEER:100); base atualizada; nenhum R-nn.
2. REGRA APLICADA:
   - SE 2ª ocorrência da mesma causa, ou pedido da pessoa, ENTÃO propõe promoção — SA:57; SA:59.
   - SE julgamento ENTÃO regra em Regras aprendidas, não checagem — SA:23-24.
   - Redige `### R-<nn> · título · aplica a: <…> · severidade: <…>`, 1–2 frases imperativas, ✅/❌ e `Origem: L-003, L-007` — SA:61-68.
   - "aplica a" e "severidade" são escolhidos por quem? Não escrito; assumido: codificador e IMPORTANTE.
   - Numeração de R-<nn>: sem regra de cálculo (como L-nnn).
   - Mostra o diff da seção Regras aprendidas; SE "ok" ENTÃO grava; o resto do arquivo não muda — SA:70-71.
   - STEER:100: se a 1ª regra entra, o placeholder fica ou sai? SA não diz.
   - SE a regra é de stack ENTÃO propõe a skill do toolkit — SA:71-72; regra de domínio, não se aplica.
   - Situação de L-003 e L-007 → `promovida → R-01` — SA:54.
   - Lições reais também viram casos de avaliação: guardar pedido e resultado esperado em `<produto>/aprendizado/avaliacoes/` — SA:74-77; nome e formato não escritos.
   - Commit pequeno; push ou PR curto com "sim" — SA:20-21.
3. OUTPUT GERADO: diff de `### R-01 …` na seção Regras aprendidas do sdd.md; pergunta "Grava? (ok)".
   ARQUIVOS ESCRITOS (após "ok"): `.kiro/steering/sdd.md` (seção Regras aprendidas) · `licoes.md` (Situação) · `avaliacoes/<caso>` (formato não definido).
4. VEREDITO MECÂNICO: AMBÍGUO — numeração R-<nn>; quem escolhe `aplica a` e `severidade`; placeholder de STEER:100 mantido ou removido; nome e formato dos casos de avaliação (SA:75-77).

**S18-F3 · Retrospectiva do épico EP-03**

1. INPUT EXATO: "retrospectiva do EP-03".
   ESTADO: EP-03 com 4 fatias `concluida`, cada uma com status.md (Histórico, Rodadas), verificacao.md e revisao-*.md; licoes.md com L-001 a L-009 (L-004 e L-007 com causa contexto-ignorado, de FT-033 e FT-031); backlog.md.
2. REGRA APLICADA:
   - SE "retrospectiva" ENTÃO modo retrospectiva — SA:3; SA:79.
   - Dados, não impressões; escopo EP-03 — SA:81.
   - Fontes: status.md (Histórico), revisao-*, verificacao.md, licoes.md, backlog.md — SA:91.
   - Lead time: início = linha `fatia iniciada` do Histórico (ST:42); fim = data de `concluida` (SC:75-76). Corridos ou úteis não escrito; SS:74 usa dias úteis em outro contexto.
   - Retrabalho = Rodadas (ST:13).
   - "Onde o humano corrigiu" = L-nnn por causa — SA:86.
   - "Autonomia: AFK <n> (<x> chegaram ao PR sem intervenção)": "sem intervenção" não definido — SA:87.
   - Termina perguntando quais propostas aplicar — SA:91-92.
   - [sem regra] gravar a retrospectiva: nenhuma linha manda.
3. OUTPUT GERADO:
   > 🔁 Retrospectiva — EP-03
   > Fluxo: 4 concluídas · lead time médio <d> dias · retrabalho <n> rodadas de revisão / <n> verificações
   > Onde o humano corrigiu: L-004 (contexto-ignorado), L-007 (contexto-ignorado)
   > Autonomia: AFK <n> (<x> chegaram ao PR sem intervenção) · HITL <n>
   > Propostas: <…>
   + "Quais propostas aplicar?"
   ARQUIVOS ESCRITOS: nenhum.
4. VEREDITO MECÂNICO: AMBÍGUO — "lead time" (corridos ou úteis; início e fim) e "chegaram ao PR sem intervenção" sem definição (SA:81-87).

**S18-X1 · "resumo das lições" (borda)**

1. INPUT EXATO: "resumo das lições".
   ESTADO: licoes.md com L-001 a L-009.
2. REGRA APLICADA:
   - SE "resumo das lições" ENTÃO é gatilho da description — SA:3.
   - Modos existentes: registrar (SA:28), promover (SA:59), retrospectiva (SA:79). Nenhum lista lições.
3. OUTPUT GERADO: não determinado.
   ARQUIVOS ESCRITOS: nenhum.
4. VEREDITO MECÂNICO: SEM REGRA — o gatilho existe, mas não há modo para listar licoes.md.

**S18-X2 · Pessoa nega as causas propostas (borda)**

1. INPUT EXATO (após a proposta de L-007 com contexto-ignorado): "não é nenhuma dessas: a causa é pressa do time".
   ESTADO: L-007 em rascunho, ainda não gravado.
2. REGRA APLICADA:
   - SE a pessoa não confirma a causa proposta ENTÃO a proposta é reformulada — SA:36 ("proponha; a pessoa confirma"); não há regra para isso.
   - A tabela de causas é fechada (SA:38-46); não há fallback "outra" nem "nenhuma".
3. OUTPUT GERADO: não determinado.
   ARQUIVOS ESCRITOS: nenhum (licoes.md só após confirmação; SA:48).
4. VEREDITO MECÂNICO: SEM REGRA — a causa é fechada e não há registro de "outra causa".

**S18-X3 · Lição durante o loop, a partir da worktree (borda)**

1. INPUT EXATO: no loop AFK, um achado do revisor chega ao humano: "isso está errado, aprenda" — sessão em `.kiro/local/wt/ft-040`.
   ESTADO: base `develop` ocupada no checkout principal; worktree em `feature/ft-040-…`; agente sdd-orquestrador, cujos resources são sdd-loop, sdd-iniciar, sdd-status e sdd-elm (AG-O), sem sdd-aprender.
2. REGRA APLICADA:
   - SE a base precisa ser a atual ENTÃO `git switch <base>` antes de gravar — SA:19-20; não há alternativa escrita quando a base não pode ser trocada nesta worktree.
   - SA:21 — "alterações pendentes na branch da fatia → commite ou peça à pessoa"; não cobre a troca bloqueada.
   - SL:115 — "Lições para registrar" só aparece no resumo; SL não manda gravar.
   - AG-O — escrita permitida não inclui `<produto>/aprendizado/` (AG-O write: `.kiro/local/loop-*.md`, `.kiro/specs/**`, `.kiro/local/wt/*/**`).
3. OUTPUT GERADO: não determinado.
   ARQUIVOS ESCRITOS: nenhum.
4. VEREDITO MECÂNICO: SEM REGRA — nenhuma regra dá o destino da lição quando a base não pode ser trocada e o agente não carrega a skill.

**Tabela-resumo S18**

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S18-F1 · Registrar lição | AMBÍGUO | "Mecânico × julgamento" sem critério (SA:23-24, SA:41); numeração L-nnn sem regra |
| S18-F2 · Promover regra | AMBÍGUO | Numeração R-nn; quem escolhe aplica a e severidade; placeholder STEER:100; avaliacoes sem formato |
| S18-F3 · Retrospectiva | AMBÍGUO | "Lead time" e "sem intervenção" sem definição (SA:81-87) |
| S18-X1 · "Resumo das lições" | SEM REGRA | Gatilho sem modo (SA:3 × SA:28, 59, 79) |
| S18-X2 · Causa negada | SEM REGRA | Lista de causas fechada (SA:38-46) |
| S18-X3 · Lição no loop | SEM REGRA | Base não pode ser trocada na worktree; orquestrador sem a skill (AG-O) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1, F2 | `<produto>/aprendizado/licoes.md` (SA:15, 48) | Sim, na **base** (SA:19; sdd/SKILL.md:105 "só na branch base"); P3 correto. Obriga `git switch <base>` + `git pull --ff-only` (SA:19-20); STEER:13 exige "sim" para trocar de branch | `.md` | `## L-<nnn> · <AAAA-MM-DD> · FT-<nnn> · <causa>` + Feito/Certo/Correção na fonte · Situação (SA:51-54) ✓. `L-<nnn>` sem regra de cálculo (próximo = maior + 1?). Arquivo criado só pela setup com `# Lições` (`sdd-setup/SKILL.md:243`) | Escrito pela sessão da pessoa. SA:20-21: "commit pequeno e push ou PR curto com o sim": o "sim" é do push/PR (P3 escreveu "commit após sim", leve deslocamento). Mesma lacuna do PR curto/base protegida de S17. Sem volta prescrita à branch da fatia depois de gravar na base | Arquivo/pasta ausente (setup não rodada ou projeto antigo) → NÃO ESPECIFICADO. Troca de branch com alterações pendentes: SA:20-21 ✓ (commitar ou pedir). Sem agente com a skill (AG-P escreveria `licoes.md`, mas não tem `sdd-aprender`) | NÃO ESPECIFICADO (numeração; arquivo ausente; PR curto) |
| F2 (promover, "ok") | `licoes.md`: `Situação` da L-003 e L-007 → `promovida → R-<nn>` (SA:54); `→ movida para <destino>` (SA:74-75) | Mesmo arquivo | idem | SA:15 e SA:97 ("só acréscimo", "Nunca apague lição") × SA:54/74-75 (alterar a Situação de lições já gravadas): contradição; P3 não apontou | Mesmo commit da regra? SA não diz | idem | DIVERGENTE (SA:15, 97 × SA:54, 74-75) |
| F2 | `.kiro/steering/sdd.md`, seção "Regras aprendidas" (SA:16, 70-71; STEER:93-100) | Sim; na base (SA:19). P3 correto. Steering é versionado | `.md` (frontmatter `inclusion: always`) | `### R-<nn> · <título> · aplica a: … · severidade: …` + regra + `- ✅ … · ❌ …` + `- Origem: L-<nnn>, L-<nnn>` (SA:64-68) bate com STEER:97-98 (STEER:98 mostra `Origem: L-<nnn>` simples). Placeholder `<!-- Nenhuma regra promovida ainda. -->` (STEER:100): SA não manda remover (setup só preserva as regras, `sdd-setup/SKILL.md:234`); `R-<nn>` sem regra de cálculo | Só com "ok" (SA:70-71) ✓. Sem commit separado nem push dito além de SA:20-21. Mudança no steering vale para sessões novas (carregado `always`) e as worktrees em curso têm o steering antigo — nada dito | Quem pode escrever: só a sessão da pessoa (AG-C nega `**/.kiro/steering/**`; AG-P não inclui `.kiro/steering`; AG-O nega steering dentro da worktree, AG-O:45-52). Arquivo ausente (sem setup): SA não trata | NÃO ESPECIFICADO (placeholder; numeração; efeito sobre worktrees em curso) |
| F2 | `<produto>/aprendizado/avaliacoes/<caso>` (SA:74-77) | Caminho sim; **nome do arquivo, formato e conteúdo ("pedido e resultado esperado") não existem** | indefinida | sem template | indefinido | A pasta não é criada pela setup (`sdd-setup/SKILL.md:243`) | NÃO ESPECIFICADO (P3 correto) |
| F3 (retrospectiva EP/FT) | nenhum arquivo prescrito (SA:79-92) | — | bloco de chat `🔁 Retrospectiva` (SA:83-89) | — | O resultado só existe no chat; **a retrospectiva de sprint é registrada por `sdd-planejamento` em `sprint-<nn>.md`** (`sdd-planejamento/SKILL.md:115-116`); para épico/fatia não há destino | — | NÃO ESPECIFICADO (retro de épico/fatia sem destino; P3 "ARQUIVOS: nenhum" confirmado) |
| X3 (lição durante o loop) | `licoes.md` na base | não alcançável a partir da worktree: `git switch <base>` falha se a base está em uso no checkout principal; AG-O não tem `sdd-aprender` e sua escrita exclui `<produto>` (AG-O:45-52 nega `.kiro/local/wt/*/{{PRODUTO}}/**`; `{{PRODUTO}}/**` na raiz não está em AG-O:39-44) | — | — | — | NÃO ESPECIFICADO (SL:115 "Lições para registrar" só no resumo) | NÃO ESPECIFICADO (P3 correto, confirmado em AG-O) |

Sem escrita: **S18-X1** ("resumo das lições": sem modo) · **S18-X2** (causa negada: lista fechada, nada gravado até confirmar, SA:36, 48) · **S18-F3** (retrospectiva de épico: só chat).

#### Achados de persistência · S18
- `sdd-aprender/SKILL.md:15, 97` × `54, 74-75`: "só acréscimo" × edição retroativa da Situação/`→ movida para`.
- `sdd-aprender/SKILL.md:19-21` × `STEER:13, 61`: gravar exige base + pull + "sim" para trocar de branch; no meio da fatia (gatilho típico: revisão/PR reprovando) a pessoa precisa abandonar a branch; não diz como voltar nem onde fica a lição se a base está bloqueada por worktree.
- `sdd-aprender/SKILL.md:74-77`: `avaliacoes/` sem nome, formato nem criação do diretório.
- `sdd-aprender/SKILL.md:79-92`: retrospectiva de épico/fatia sem gravação (só sprint tem destino, em `sdd-planejamento`).
- `AG-P:write`, `AG-C:deniedPaths`, `AG-O:39-52`: nenhum agente pode executar o modo promover (steering) nem registrar (`aprendizado/`, só AG-P tem o write, sem a skill); a skill é só da sessão da pessoa.

---


## S19 · sdd-loop

### Parte 2 — Plano do fluxo esperado (Sonnet)


Contexto comum (SL 1-136): executado pelo agente `sdd-orquestrador` (ou a sessão da pessoa com os mesmos passos); coordena e registra; cada fase é um subagente de contexto limpo que lê o estado em disco; a pessoa fica **sobre** o loop: aprova o lote no início e lê os PRs no fim (SL:12-14). Leitura prévia: `.kiro/steering/sdd.md` (Git, banco e autonomia; Comandos) e `<produto>/planejamento/acordos.md` (WIP; sem o arquivo, limite 2) (SL:16-17). O agente `sdd-orquestrador` só carrega `sdd-loop`, `sdd-iniciar`, `sdd-status`, `sdd-elm` (`sdd-setup/assets/agents/sdd-orquestrador.json`).

#### S19-F1 · Retomar o loop (Passo 0)

- **Gatilho inicial**
  - Frases (description SL:3): "retoma o loop"; também ao acionar qualquer "roda as fatias AFK"/"modo AFK" quando existe estado anterior.
  - Evento: a skill sempre inicia pelo Passo 0.
- **Pré-condições / arquivos lidos**: `.kiro/local/loop-*.md` com fatias não finalizadas (SL:19-22); `status.md` de cada fatia (fase, Rodadas, Histórico); `acordos.md`; `.kiro/steering/sdd.md`.
- **Processamento interno**
  1. Procura `.kiro/local/loop-*.md` com fatias não finalizadas.
  2. Existe → **mostra o estado** (fatia, fase, rodada, último resultado) e **pergunta se retoma**.
  3. "Sim" → **continua cada fatia da fase registrada no `status.md` dela** (SL:22). Fatia em `plano-em-revisao` já aprovada: "aprovo o plano da FT-031" → ver S19-F3.
  4. "Não" → segue para o Passo 1 (novo lote).
- **Resultado final esperado**: resposta com o quadro de estado (fatia · fase · rodada · último resultado) e a pergunta "retoma?"; sem retomar, nenhum arquivo muda; ao retomar, o log `.kiro/local/loop-<data>.md` e os `status.md` voltam a ser atualizados a cada fase (SL:92-94); próximo: as fases do Passo 3 a partir da fase registrada.
- **Lacunas observadas**
  - **Retomada não diz o que revalidar**: worktree ausente (removida/ perdida) → Passo 2 comandos de criação (`git worktree add … <branch>` "já existe", SL:58-59) não é citado em Passo 0; autorização de push/PR (guardada no cabeçalho do log, SL:125) e limite de WIP/paralelo (SL:32-34) não são reconfirmados; **mais de um** `loop-*.md` não finalizado não é tratado.
  - "Fatias não finalizadas": critério não definido (fase `plano-em-revisao`/`aceita` aguardando pessoa contam?). Fatia só `bloqueada` com pergunta pendente — retoma como? (SL:105-106 só diz registrar a pergunta).
  - **Fatias em fase `pr-aberto`/concluída** não saem do log; sem regra de encerramento do arquivo `loop-*.md`.
  - Rodada: "continuar da fase registrada no `status.md`" supõe que `status.md` e log estão consistentes; não define qual vale em divergência.

#### S19-F2 · Lote novo: fronteira, confirmação, worktrees e fases até o PR

- **Gatilho inicial**
  - Frases (SL:3): "roda as fatias AFK", "modo AFK", "leva a FT-031 e a FT-032 até o PR", "trabalha sozinho nas prontas da sprint".
- **Pré-condições / arquivos lidos**: `sdd.md` (paralelismo padrão 1, máx. 3; "Plano AFK"; "Push e PR no loop"; Comandos); `<produto>/planejamento/acordos.md` (WIP; Kanban); `backlog.md` (fatias `pronta` + `AFK`, `bloqueada-por`, DoR); sprint atual; `status.md` das branches (para contar WIP); MCP `elm` (se houver) e `pa_*.json`.
- **Processamento interno**
  1. **Passo 0**: sem log pendente (ou "não retomar") → segue.
  2. **Candidatas** (SL:26-29): as fatias pedidas, ou as `pronta` + `AFK` da sprint atual por prioridade. Pedida fora da sprint aberta → fica de fora até o **encaixe** (`sdd-planejamento`, seção Encaixe). **Kanban** (`acordos.md`): sem sprint/encaixe — vale a `pronta` do topo do backlog, e as `[DEV]` nascem na confirmação (`sdd-elm` modo *sprint*, iteração corrente).
  3. **Ficam de fora** (diga o motivo): HITL; trilha direta ("é da sessão da pessoa"); Definition of Ready não atendida; `bloqueada-por` não concluída e não presente antes no lote; já em andamento com outra pessoa (SL:30-31).
  4. **Limite** (SL:32-34): paralelismo do `sdd.md` (padrão 1, máx. 3) **e** vagas de WIP de revisão humana (limite dos acordos menos as fatias esperando pessoa: `plano-em-revisao`, `aceita`, `pr-aberto`).
  5. **Proposta — uma confirmação para o lote todo** (SL:35-46): bloco `🤖 Loop AFK — <n> fatias · paralelo <p> · base <branch>` com tabela FT/Título/Branch/Worktree; linha "Plano AFK: aprovação humana → o loop para no GATE do plano | análise basta → segue até o PR"; "push + PR? (sim/não) — nunca merge" (só se o `sdd.md` diz "perguntar a cada lote"; com "não — a pessoa abre" a linha é omitida e o loop para em `aceita`); "EWM: assumir as `[DEV]` do lote (responsável: <login de quem dispara>) e colocá-las em andamento"; "Confirma?".
  6. Com "sim" e MCP `elm`: assume as `[DEV]` (`sdd-elm`); sem MCP/falha → `ELM pendente: assumir a tarefa` no `status.md` de cada fatia (SL:47-48).
  7. Cria o **log** `.kiro/local/loop-<AAAA-MM-DD-HHMM>.md` (formato: `# Loop AFK <data> — paralelo <p> · push/PR: <sim|não>` + tabela FT/Worktree/Branch/Fase/Rodada/Último resultado/Atualizado) (SL:49, 122-128).
  8. **Passo 2 — Worktree por fatia** (SL:51-71): `git fetch --quiet` + `git worktree add .kiro/local/wt/<ft> -b <branch> origin/<base>` (nova) ou `… <branch>` (já existe). Dentro, faz só os itens 2 e o commit (item 5) do Passo 4 da `sdd-iniciar`: pasta `.kiro/specs/<ft>-<slug>/`, `status.md` com `Responsável: agente:sdd-orquestrador`, `.config.kiro`, sem perguntas; EWM já tratado; sem push; `backlog.md` não muda (só na base).
  9. **Comandos dentro da worktree** (SL:67-71): `cd .kiro/local/wt/<ft> && <comando>` (nunca `git -C`); arquivos por `.kiro/local/wt/<ft>/<caminho>` — informar a cada subagente.
  10. **Passo 3 — Fases** (SL:73-98): cada fase é um subagente novo recebendo só `AUTONOMO=true`, id da fatia, caminho da worktree e da pasta da fatia, como rodar comandos e a rodada; fatias diferentes em paralelo até o limite. Com **Workflows** do Kiro ligados, espera cada execução terminar antes de abrir a seguinte da mesma fatia (SL:77-79).

      | # | Fase | Subagente | Sai quando |
      |---|---|---|---|
      | 1 | pesquisa | `sdd-pesquisador` (`sdd-pesquisar`) | `research.md` gravado |
      | 2 | plano | `sdd-codificador` (`sdd-plano` Passos 2-3) | spec do Kiro gravada · ou `bloqueada` |
      | 3 | análise do plano | `sdd-revisor` (rubrica L) → `sdd-codificador` corrige | `ANALISE: OK` · 2 rodadas sem OK → `bloqueada` |
      | 4 | GATE do plano | orquestrador | Plano AFK = aprovação humana → commit do plano na worktree, **pare esta fatia** em `plano-em-revisao` e siga com as outras (→ S19-F3); "análise basta" → grava `fase: implementando` e segue |
      | 5 | implementação | `sdd-codificador` (`sdd-implementar` Passos 0-2) | tarefas `[x]` e backpressure verde · ou `bloqueada` |
      | 6 | revisão do código | `sdd-revisor` (rubrica C) → volta à 5 com os achados | `VEREDITO: APROVADO` · 2ª reprovação → `bloqueada` |
      | 7 | verificação | `sdd-verificador` (`sdd-verificar`) | `ACEITO` · `REJEITADO` → volta à 5 uma vez; de novo → `bloqueada` |
      | 8 | entrega | orquestrador | `fase: aceita`; commit do que faltar; push + PR se autorizado no lote (texto do Passo 5 da `sdd-implementar`; o Kiro ainda pode pedir confirmação a cada push) → `fase: pr-aberto` |

  11. Depois de cada fase (SL:92-94): grava a fase seguinte (`planejando` depois da pesquisa, `revisando` antes da revisão do código), atualiza o log, as **Rodadas** e o **Histórico** do `status.md`; **commit pequeno na worktree** (inclusive dos relatórios do revisor e do verificador, que não commitam).
  12. Kiro Workflows do sdd **não** fazem parte do loop (SL:100-101).
- **Resultado final esperado**
  - Resposta: a tabela de proposta + "Confirma?" no início; ao fim, o resumo do Passo 4 (S19-F4).
  - Arquivos: `.kiro/local/loop-<AAAA-MM-DD-HHMM>.md`; por fatia, worktree `.kiro/local/wt/<ft>/` (ignorada pelo git), branch `<prefixo><ft>-<slug>`, `.kiro/specs/<ft>-<slug>/` com `status.md`, `.config.kiro`, `research.md`, `requirements.md`/`bugfix.md`, `design.md`, `tasks.md`, `analise-*.md`, `revisao-codigo-<N>.md`, `verificacao.md`, `CT.csv`, evidências; commits na worktree; push/PR se autorizado; tarefas `[DEV]` assumidas no EWM (ou `ELM pendente`).
  - Próximo: pessoa aprova planos pausados (S19-F3), revisa PRs, responde bloqueios; pós-merge: `sdd-consolidar`.
- **Lacunas observadas**
  - **Trilha rápida não está no loop**: SL:30 só exclui a trilha direta; mas as fases 1-4 (pesquisa, plano, análise L, GATE) pressupõem trilha padrão. A trilha rápida (README/`sdd/SKILL.md:28`: `bugfix.md` + `tasks.md`, sem pesquisa/GATE obrigatório; STEER:190 "GATE na trilha rápida") não tem fluxo descrito — uma fatia rápida `AFK` entraria no loop sem fases correspondentes.
  - **Fase 7 → 5 não reentra na fase 6** (SL:87-89), enquanto SI:73-83 exige revisão após qualquer correção (ver S16-F2). Também a "1 volta" da verificação (SL:89) contradiz a ausência de limite em SV.
  - **Fase 8 e "branch desatualizada com a base"**: SI:98-100 manda parar e devolver ("branch desatualizada com a base") quando agente; SL:90 não prevê esse caso nem diz que o merge `origin/<base>` → branch é "sempre de uma pessoa".
  - **Subagente verificador autônomo e as horas `[VER]`** (SV:77-80): ver S16-F1.
  - SL:62-63 delega à `sdd-iniciar` "item 2 e o commit do item 5 do Passo 4" — o item 5 da `sdd-iniciar` inclui "com sim, push da branch" (`sdd-iniciar/SKILL.md:113`); SL diz explicitamente "não há push nesta hora" (SL:64) — a remissão é ambígua (só o commit?) mas coerente com a intenção.
  - Ids das `[DEV]` assumidas: SL:47-48 não diz onde grava os ids das tarefas (no `status.md` campo ELM, como em `sdd-iniciar/SKILL.md:110`?), e em qual `status.md` (o da worktree só nasce no Passo 2, depois da confirmação).
  - Responsável da `[DEV]`: "<login de quem dispara>" (SL:44) × `Responsável: agente:sdd-orquestrador` no `status.md` (SL:63) — dois responsáveis, sem dizer qual lança horas (SL:117-119 assume a pessoa).
  - **Retomada de fase `aceita` sem push autorizado**: o loop "para em `aceita`" (SL:42-43) mas não registra quem abre o PR e com qual texto (SI:93-95 diz que a sessão da pessoa abre; sem link).

#### S19-F3 · Aprovação de plano pausado (reentrada na fase 5)

- **Gatilho inicial**: frase "aprovo o plano da FT-031" (SL:96-97), após o loop ter parado a fatia em `plano-em-revisao` (fase 4, "Plano AFK = aprovação humana").
- **Pré-condições / arquivos lidos**: plano em `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/` (ou na branch, se o push foi autorizado); `status.md`; log do loop.
- **Processamento interno**
  1. A pessoa lê o plano (`requirements.md`/`bugfix.md`, `design.md`, `tasks.md`).
  2. "Aprovo" → grava `fase: implementando` e **retoma a fatia na fase 5** pelo Passo 0 (SL:96-98) — nos moldes de S19-F1 (retomar).
  3. Pediu **ajuste** → `sdd-codificador` (`sdd-plano`, replanejar) e nova análise (fase 3) (SL:98).
  4. Resto do fluxo: fases 5-8 como em S19-F2.
- **Resultado final esperado**: `status.md` com `fase: implementando` (e Histórico); log atualizado; próximo: fases 5→8 até `aceita`/`pr-aberto`; no ajuste: novo `design.md`/`tasks.md` + `analise-*.md`.
- **Lacunas observadas**
  - Vagas de WIP e paralelismo são recontados na reentrada? SL:32-34 só conta no Passo 1; aprovações tardias podem estourar o limite.
  - Quem aprova: a "frase" não diz se é preciso `GATE do plano` por "dev (de preferência quem vai revisar o PR)" (`sdd/SKILL.md:53`), nem registra a identidade no `status.md`.
  - Reentrada exige um orquestrador/sessão ativos: `sdd-loop` não define "retoma só esta fatia" × "retoma o lote" (relação com S19-F1).
  - Plano aprovado por quem ficou sem a worktree: sem passo para recriar a worktree (SL:58-59).

#### S19-F4 · Parada: bloqueio de fatia, problema sistêmico, resumo final, horas e limpeza

- **Gatilho inicial**: eventos do loop: fase termina em `bloqueada` (lacuna de negócio, divergência com o plano, 2 reprovações, verificação rejeitada duas vezes — SL:105-106), erro sistêmico (SL:107-108) ou fim natural das fases do lote (SL:109).
- **Pré-condições / arquivos lidos**: `status.md` de cada fatia; log `.kiro/local/loop-<data>.md`; MCP `elm` (para horas).
- **Processamento interno**
  1. **Fatia bloqueada** → registra o **motivo e a pergunta exata** no `status.md`; **segue com as outras** (SL:105-106).
  2. **Problema sistêmico** (build quebrado na base, ambiente fora do ar, mesmo erro em duas fatias) → **pare o lote inteiro**: "o loop não conserta ambiente" (SL:107-108).
  3. Ao fim, emite o resumo (SL:109-116):
     ```
     🤖 Loop AFK — resultado
     | FT | Resultado | PR | Rodadas (plano/código/aceite) | Observação |
     Aguardando pessoa: <planos para aprovar · PRs para revisar · bloqueios com pergunta>
     ELM pendente: <o que falhou ou ficou sem o MCP>
     Lições para registrar: <correções que o loop precisou — sdd-aprender>
     ```
  4. **Horas, numa pergunta só** (com MCP `elm`): tabela `tarefa | horas sugeridas` com as `[DEV]` do lote; a pessoa ajusta e confirma de uma vez → `sdd-elm` modo *horas*. As `[REV]` e `[VER]` são lançadas por quem revisa e verifica, na conclusão de cada uma (SL:117-119).
  5. **Worktrees** ficam até o merge; remover depois com `git worktree remove .kiro/local/wt/<ft>` (sem `--force`) (SL:120).
  6. Regras permanentes (SL:130-136): nunca merge, nunca `--force`, nunca push sem a autorização do lote; ELM só pelo que o lote confirmou; nunca relaxar um gate para o loop andar ("bloqueio é informação, não falha"); tipo de fatia que bloqueia com frequência → sugerir na retrospectiva tratá-lo como HITL.
- **Resultado final esperado**
  - Resposta: o bloco `🤖 Loop AFK — resultado` + pergunta única de horas.
  - Arquivos: `status.md` por fatia (`fase: bloqueada` + motivo + pergunta, ou `aceita`/`pr-aberto`, `ELM pendente`), log `.kiro/local/loop-<data>.md` final, PRs (se autorizado), lançamentos de horas no ELM.
  - Próximo: pessoa aprova planos, revisa PRs, responde bloqueios (devolve para a fase da fatia, S19-F1), registra lições (`sdd-aprender`), faz o merge; depois `sdd-consolidar` e remoção da worktree.
- **Lacunas observadas**
  - **"Lições para registrar"** (SL:115): o orquestrador não carrega `sdd-aprender` nem escreve em `<produto>/aprendizado/`; a lição fica na lista do resumo sem dono, e fora de worktree o `git switch <base>` de SA:19-21 inviabiliza um registro in loco (ver S18-F1).
  - **Horas `[DEV]` duplicadas**: SL:117-118 lança horas das `[DEV]` ao fim do loop; SC:48 volta a perguntar `[DEV]` no merge ("descontando o já lançado") — não diz qual das duas é a principal nem como evitar a dupla pergunta (concluir a `[DEV]` sem horas?). Também: `[DEV]` "concluída" só no merge (SC:48-52) mas as horas já foram lançadas.
  - **`[REV]` e `[VER]` "por quem revisa e verifica"** (SL:118-119): no loop, revisor e verificador são subagentes sem MCP e sem pessoa; ninguém lança — ver S16-F1.
  - **Bloqueio sem destino**: "pergunta exata no `status.md`" (SL:105-106) mas sem formato nem lista central (o resumo lista; o `sdd-status` pode ler `status.md`); a volta da fatia a partir da resposta humana não é descrita (só indirectamente em S19-F1/F3).
  - **Remoção da worktree** (SL:120) não está em nenhuma skill de fechamento (`sdd-consolidar`) e o orquestrador nega `git worktree remove` (`sdd-orquestrador.json:95,192`): depende de a pessoa fazer manualmente.
  - **Erro sistêmico** (SL:107-108) não define critério objetivo ("mesmo erro em duas fatias"), como as fatias já em curso são marcadas (ficam em `bloqueada`? `AMBIENTE` como em SI:70-71?), nem como retomar (S19-F1).

---


### Parte 3 — Teste do Quarto Chinês (Haiku)


**S19-F1 · Retomar o loop**

1. INPUT EXATO: "retoma o loop".
   ESTADO: `.kiro/local/loop-2026-10-14-0930.md` com FT-031 `verificando` (rodada de verificação 1, último resultado "revisão APROVADO") e FT-032 `implementando` (rodada 0); status.md de FT-031 `fase: verificando` e de FT-032 `fase: implementando`; nenhum outro loop-*.md; acordos.md presente.
2. REGRA APLICADA:
   - SE "retoma o loop" ENTÃO carrega a skill — SL:3.
   - Leia sdd.md (Git, banco e autonomia; Comandos) e acordos.md — SL:16-17.
   - SE existe loop-*.md com fatias não finalizadas ENTÃO mostra estado (fatia, fase, rodada, último resultado) e pergunta se retoma — SL:19-21.
   - "Fatias não finalizadas": critério não escrito (uma fatia `aceita` esperando pessoa conta?).
   - SE "sim" ENTÃO continua cada fatia da fase registrada no status.md dela — SL:22.
   - `verificando` → fase 7 e `implementando` → fase 5: o mapa entre a fase do status (ST:18-19) e a fase do loop (SL:81-90) não está escrito; só se deduz de SL:92-93.
   - Após cada fase: grava status, log e commit — SL:92-94.
3. OUTPUT GERADO: quadro de estado + "retoma?". Após "sim", FT-031 segue na fase 7 e FT-032 na fase 5 (dedução do mapa acima).
   ARQUIVOS ESCRITOS: nenhum até retomar; depois `.kiro/local/loop-*.md` e status.md de cada fatia.
4. VEREDITO MECÂNICO: AMBÍGUO — mapa entre fase do status e fase do loop não escrito; "fatia não finalizada" sem critério.

**S19-F2 · Lote novo, da confirmação ao GATE do plano**

1. INPUT EXATO: "roda as fatias AFK da sprint"; depois, à pergunta "Confirma?", a pessoa responde "sim".
   ESTADO: sprint-07 aberta; FT-040 `pronta`, AFK, trilha padrão, DoR ok; FT-041 `pronta`, AFK, `bloqueada-por` FT-039 (não concluída); FT-042 HITL; FT-043 trilha direta; acordos.md com WIP 3 e duas fatias já esperando pessoa (FT-029 `pr-aberto`, FT-030 `plano-em-revisao`); sdd.md: paralelo 1, "Plano AFK: aprovação humana", "Push e PR no loop: perguntar a cada lote" (STEER:63-64); MCP elm presente; sem loop-*.md.
2. REGRA APLICADA:
   - SE sem log pendente ENTÃO segue — SL:19-22.
   - Candidatas: `pronta` + AFK da sprint aberta → FT-040 e FT-041 — SL:26-29.
   - Fica de fora: FT-041 (`bloqueada-por` não concluída), FT-042 (HITL), FT-043 (direta) — SL:30-31.
   - Limite: min(paralelo 1 [STEER:63]; WIP 3 − 2 = 1) → 1 fatia: FT-040 — SL:32-34.
   - Proposta: `🤖 Loop AFK — 1 fatia · paralelo 1 · base develop`, tabela, "Plano AFK: aprovação humana → o loop para no GATE do plano", "push + PR? (sim/não)" (STEER:64), "EWM: assumir as [DEV] do lote (responsável: <login de quem dispara>)", "Confirma?" — SL:35-46.
   - Login de quem dispara: fonte não escrita — SL:44.
   - SE "sim" e MCP ENTÃO assume a [DEV] via sdd-elm — SL:47-48.
   - Log `.kiro/local/loop-2026-10-15-HHMM.md` com `push/PR: <sim|não>` — SL:49; SL:122-128.
   - Worktree: `git fetch --quiet`; `git worktree add .kiro/local/wt/ft-040 -b feature/ft-040-<slug> origin/develop`; pasta, status.md (`Responsável: agente:sdd-orquestrador`) e `.config.kiro`; commit; sem push — SL:51-65.
   - Comandos com `cd .kiro/local/wt/ft-040 && <comando>` — SL:67-71.
   - Fases 1 a 3 (pesquisa, plano, análise L); fase 4 GATE: "Plano AFK = aprovação humana" → commit do plano; FT-040 para em `plano-em-revisao` — SL:83-86.
   - Após cada fase: fase seguinte, log, Rodadas, Histórico, commit — SL:92-94.
3. OUTPUT GERADO: proposta de SL:35-46; após "sim", log criado e FT-040 em `plano-em-revisao`. O resumo final fica para S19-F4.
   ARQUIVOS ESCRITOS: `.kiro/local/loop-2026-10-15-HHMM.md` · worktree `.kiro/local/wt/ft-040/` com `.kiro/specs/ft-040-<slug>/` (status.md, .config.kiro, research.md, requirements.md, design.md, tasks.md) · commits na worktree · ELM: [DEV] FT-040 assumida, ou `ELM pendente: assumir a tarefa`.
4. VEREDITO MECÂNICO: AMBÍGUO — (a) "login de quem dispara" (SL:44) sem fonte: `whoami` (IN:102) × `git config user.name` cruzado com equipe.json (SS:35-36); (b) "push + PR? (sim/não)" (SL:42-43) e "Confirma?" (SL:45): um único "sim" pode valer para as duas perguntas.

**S19-F3 · Aprovação de plano pausado**

1. INPUT EXATO: "aprovo o plano da FT-040".
   ESTADO: status.md de FT-040 `fase: plano-em-revisao`; worktree `.kiro/local/wt/ft-040` com o plano commitado; loop log com FT-040 em `plano-em-revisao`; push não autorizado; WIP com FT-029, FT-030 e FT-040 esperando pessoa.
2. REGRA APLICADA:
   - Roteamento: a frase não consta nos gatilhos de SL:3 nem de IN:3 ("retomar a FT-031" leva ao Passo 5 de IN:37-40); IN:127 manda `plano-em-revisao` para sdd-plano (replanejar), não para aprovação.
   - SE a pessoa aprova o plano ENTÃO grava `fase: implementando` — SL:96-97.
   - Retoma a fatia na fase 5 pelo Passo 0 — SL:97-98.
   - Após a fase: status, log e commit — SL:92-94.
   - WIP é contado só no Passo 1 — SL:32-34; não é recontado na reentrada (sem regra).
   - Quem aprova: "a pessoa"; identidade não é gravada — SL:96.
3. OUTPUT GERADO: `fase: implementando` + linha no Histórico; fase 5 (sdd-implementar Passos 0–2) com `AUTONOMO=true` na worktree.
   ARQUIVOS ESCRITOS: status.md de FT-040 · loop log · commit na worktree.
4. VEREDITO MECÂNICO: AMBÍGUO — a frase de aprovação não tem gatilho de roteamento (SL:3, IN:3, IN:127); quando o sdd-loop é carregado, SL:96-98 é determinístico.

**S19-F4 · Parada: bloqueio, PR, resumo e horas**

1. INPUT EXATO: "roda as fatias AFK"; ao fim do lote, FT-040 fica bloqueada com a pergunta "CPF inválido conta como tentativa?"; FT-041 chega a `aceita`; a pessoa autorizou push e PR no lote; sem erro sistêmico; MCP elm presente.
   ESTADO: FT-041 com [DEV] assumida; [REV] feita pelo sdd-revisor no loop (subagente, sem MCP); [VER] feita pelo sdd-verificador (subagente, sem MCP).
2. REGRA APLICADA:
   - SE fatia bloqueada ENTÃO registra motivo e pergunta exata no status.md e segue com as outras — SL:105-106 (FT-040).
   - SE problema sistêmico ENTÃO para o lote — SL:107-108; não se aplica.
   - SE FT-041 `aceita` e push e PR autorizados ENTÃO push e PR → `fase: pr-aberto` — SL:90; SI:117.
   - Resumo: tabela FT | Resultado | PR | Rodadas | Observação; "Aguardando pessoa"; "ELM pendente"; "Lições para registrar" — SL:109-116.
   - Horas, numa pergunta só, com tabela das [DEV] do lote (FT-040 e FT-041); a pessoa confirma → sdd-elm modo horas — SL:117-119; SE:186-197.
   - "As [REV] e [VER] são lançadas por quem revisa e verifica, na conclusão de cada uma" — SL:118-119.
   - "O merge conclui a [DEV] e a [REV] (…); pergunte as horas de cada uma (descontando o já lançado)" — SC:48.
   - "Horas lançadas na conclusão, nunca nos GATEs" — STEER:16 (não diz quem).
   - Worktrees ficam até o merge — SL:120.
   - "Lições para registrar" sem executor: AG-O não carrega sdd-aprender.
3. OUTPUT GERADO:
   > 🤖 Loop AFK — resultado
   > FT-040 bloqueada (pergunta registrada) · FT-041 pr-aberto (PR <link>)
   > Aguardando pessoa: pergunta de FT-040 · PR de FT-041
   > ELM pendente: —
   > Lições para registrar: —
   Mais a pergunta única de horas das [DEV].
   ARQUIVOS ESCRITOS: status.md de FT-040 (bloqueada + motivo + pergunta; formato não definido por SL) · status.md de FT-041 (`pr-aberto` + link) · loop log final · lançamentos de horas após "sim".
4. VEREDITO MECÂNICO: CONFLITO — SL:118-119 (a [REV] é lançada por quem revisa, na conclusão da revisão) × SC:48 (o merge conclui a [REV] e pergunta as horas dela). Ambas tratam o mesmo lançamento de [REV]; STEER:16 diz "na conclusão", sem resolver a divergência.

**S19-X1 · Trilha rápida AFK no lote (borda)**

1. INPUT EXATO: "leva a FT-050 até o PR" — FT-050 trilha rápida, AFK, `pronta`, DoR da rápida ok.
   ESTADO: backlog.md com FT-050 `pronta`, AFK, trilha rápida; STEER:63 com "GATE na trilha rápida: sim".
2. REGRA APLICADA:
   - SE trilha direta ENTÃO fica de fora — SL:30; a rápida não é excluída, então entra como candidata.
   - Fases 1 a 4 descrevem a trilha padrão: pesquisa, spec do Kiro (SL:84), análise L, GATE (SL:83-86).
   - A trilha rápida usa `bugfix.md` + `tasks.md` (IN:52), sem as fases descritas.
   - STEER:63 manda "GATE na trilha rápida: sim"; SL não lê essa coluna do sdd.md.
3. OUTPUT GERADO: não determinado (a proposta incluiria FT-050 sem fases equivalentes).
   ARQUIVOS ESCRITOS: nenhum até a confirmação.
4. VEREDITO MECÂNICO: SEM REGRA — o sdd-loop não tem fases para a trilha rápida, e o GATE da rápida (STEER:63) não é citado.

**S19-X2 · Erro sistêmico: mesmo erro em duas fatias (borda)**

1. INPUT EXATO: "roda as fatias AFK"; FT-040 e FT-041 falham na fase 5 com "cannot find symbol Clock" (mesma mensagem, arquivos diferentes).
   ESTADO: lote em curso; sem erro de ambiente registrado.
2. REGRA APLICADA:
   - SE problema sistêmico (build quebrado na base, ambiente fora do ar, mesmo erro em duas fatias) ENTÃO pare o lote inteiro — SL:107-108.
   - "Mesmo erro": mesma mensagem, mesma causa ou mesmo arquivo? Não definido.
   - SE erro de ambiente ENTÃO `AMBIENTE` no status.md, não código — SI:70-71.
   - SE não é sistêmico ENTÃO a fatia fica bloqueada e o lote segue — SL:105-106.
   - O que acontece com as fatias já em curso quando o lote para: não escrito.
3. OUTPUT GERADO: se sistêmico, lote parado; se não, FT-040 e FT-041 bloqueadas. Depende da leitura.
   ARQUIVOS ESCRITOS: status.md das fatias afetadas; loop log.
4. VEREDITO MECÂNICO: AMBÍGUO — "mesmo erro em duas fatias" (SL:107-108) aceita duas leituras (mensagem idêntica ou causa idêntica).

**Tabela-resumo S19**

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S19-F1 · Retomar o loop | AMBÍGUO | Mapa entre fase do status e fase do loop não escrito; "fatia não finalizada" sem critério |
| S19-F2 · Lote novo | AMBÍGUO | "Login de quem dispara" sem fonte (SL:44); um "sim" pode valer para lote e push/PR (SL:42-45) |
| S19-F3 · Aprovação de plano | AMBÍGUO | Frase "aprovo" sem gatilho (SL:3, IN:3, IN:127); WIP não recontado |
| S19-F4 · Parada e horas | CONFLITO | [REV] lançada na conclusão da revisão (SL:118-119) × no merge (SC:48) |
| S19-X1 · Trilha rápida no lote | SEM REGRA | Fases e GATE da rápida (STEER:63) não tratados pelo SL |
| S19-X2 · Mesmo erro em duas fatias | AMBÍGUO | "Mesmo erro" sem critério (SL:107-108) |

---


### Parte 4 — Persistência e artefatos (Sonnet)


| Fluxo | Arquivo (caminho exato prescrito) | Diretório confere? | Extensão/formato | Estrutura interna confere com o template? | Sucesso (gravado e fechado) | Diretório inacessível / sem permissão / não existe | Veredito |
|---|---|---|---|---|---|---|---|
| F1, F2, F4 | `.kiro/local/loop-<AAAA-MM-DD-HHMM>.md` (SL:49; cabeçalho de SL:122 usa `<data>`) | Sim, na raiz do checkout principal. P3 `loop-2026-10-15-HHMM.md` ✓. AG-O permite `.kiro/local/loop-*.md` (AG-O:40, 262) | `.md` | `# Loop AFK <data> — paralelo <p> · push/PR: <sim\|não>` + tabela de 7 colunas (SL:125-127) ✓. Resumo final (SL:109-116) **não** vai para o log | Escrito pelo orquestrador após cada fase (SL:92-93). **Fora do git** (`.kiro/local/`), logo existe só na máquina de quem rodou. Nunca é marcado finalizado: o Passo 0 (SL:21) reabre logs antigos com fatias `bloqueada`/`aceita`/`plano-em-revisao`. Retomada: usa o log antigo ou cria outro? SL:49 só cria no lote novo | `.kiro/local/` ausente: NÃO ESPECIFICADO (a setup só ignora, não cria). Sem permissão: AG-O permite | NÃO ESPECIFICADO (fim de vida do log; retomada no mesmo arquivo) |
| F2 | worktree `.kiro/local/wt/<ft>/` (SL:53-59), branch `<prefixo><ft>-<slug>` | Sim: `git worktree add .kiro/local/wt/ft-040 -b feature/ft-040-<slug> origin/develop` bate com SL:58 e com AG-O:80 (`git worktree add \.kiro/local/wt/.*`). Comando mora no `cd` + comando simples (AGR:27-30) | diretório git | n/a | Criada pelo orquestrador; fica até o merge (SL:120); remover é `git worktree remove` sem `--force`, **negado a todos os agentes** (AG-O:95) → só a pessoa | Branch já em uso (a pessoa está nela no checkout principal) → `git worktree add` recusa: NÃO ESPECIFICADO. Pasta já existente (retomada com restos): NÃO ESPECIFICADO. `git fetch` offline: NÃO ESPECIFICADO | NÃO ESPECIFICADO (branch em uso, diretório existente, remoção) |
| F2 | `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/status.md` e `.config.kiro` (SL:62-63, via sdd-iniciar Passo 4 item 2) | Sim: AG-O permite `.kiro/local/wt/*/.kiro/specs/**` (AG-O:42, 264). Backlog não muda (SL:64-65) ✓ | `.md`; `.config.kiro` JSON | `status-template.md` (ST:3-16, 37-42): `Responsável: agente:sdd-orquestrador` ✓ (ST:12). **O campo ELM** (`IB <id> · [DEV] <id> · [REV] <id> · [VER] <id>`, ST:15) não tem fonte no loop: SL:62 só faz os itens 2 e 5 e pula o item 4 (que grava os ids no `status.md`, `sdd-iniciar/SKILL.md:112`). Sem os ids, as horas (SE:190) não acham a tarefa. SL:47-48 grava `ELM pendente` no `status.md` **antes** de ele existir (Passo 1, item 4, antes do Passo 2) | Commit pequeno na worktree (SL:62-63, item 5 sem push, SL:64) pelo orquestrador (AG-O:78) | `.kiro/local/wt/*/.kiro/steering/**` etc. negados ao AG-O; `status.md` permitido ✓ | NÃO ESPECIFICADO (origem dos ids de tarefa no campo ELM; ordem entre pendência e criação do `status.md`) |
| F2, F3 | spec e relatórios na worktree: `research.md` (pesquisador, AG pesquisador write `.kiro/local/wt/*/.kiro/specs/*/research.md`), `requirements.md`, `design.md`, `tasks.md` (codificador `./**`), `analise-plano-<N>.md`, `revisao-codigo-<N>.md` (revisor, `.kiro/local/wt/*/.kiro/specs/*/revisao-*.md`/`analise-*.md`) | Sim: todos sob `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/` (SL:75-76, 96) | `.md` | Fora do escopo desta parte (templates das skills de plano/revisão) | Revisor, pesquisador e verificador não commitam (AG revisor/pesquisador: sem add/commit; AG-V:105-107); o **orquestrador comita, inclusive relatórios** (SL:93-94) ✓; fase 4: "commit do plano na worktree" (SL:86) ✓ | Escrita negada ao subagente: AGR:36-37 manda comparar com as regras do orquestrador; `.kiro/local/verificacao/**` do AG-V não está no allow do AG-O | OK (commit); NÃO ESPECIFICADO (herança de allow/deny entre orquestrador e subagente) |
| F2 (fase 7), F4 | `verificacao.md`, `CT.csv`, `evidencias/`, `massa/` na worktree | Sim: AG-V:33-43 inclui `.kiro/local/wt/*/.kiro/specs/*/…`. Exceto `.kiro/local/verificacao/<ft>/` (só na raiz) | ver S16 | ver S16 | **Aqui o commit existe:** SL:93-94 "commit pequeno na worktree (inclusive dos relatórios do revisor e do verificador, que não commitam)". Verificação rejeitada duas vezes → `bloqueada` (SL:89, 105-106) | ver S16 | OK (único lugar onde o commit dos relatórios é prescrito) |
| F3 | `status.md` da worktree: `fase: implementando` (SL:96-98) | Sim. P3: "branch, se o push foi autorizado" — **SL:96-97 supõe o plano na branch, mas nenhum passo faz push antes da fase 8** (SL:64 "não há push nesta hora"; fase 4 só comita, SL:86) | `.md` | ST:19 (`plano-em-revisao` → `implementando`) ✓. Aprovador não é gravado (SL:96) | Orquestrador grava + comita (SL:92-94); sem push | n/a | DIVERGENTE (SL:96-97 "na branch, se o push foi autorizado" × ausência de push antes da entrega; a pessoa só tem a cópia da worktree) |
| F4 (bloqueio) | `status.md` da fatia bloqueada: motivo + pergunta exata (SL:105-106) | Sim (worktree) | `.md` | ST:19: `bloqueada (de: <fase>)` com motivo e pergunta; SL:105-106 não diz o formato (P3 correto: "formato não definido por SL") | Orquestrador grava e comita (fim de fase) | n/a | NÃO ESPECIFICADO (formato; coberto por ST:19 se lido) |
| F4 (entrega) | `status.md` com `fase: pr-aberto` + link do PR (SL:90; SI:117) | Sim (worktree → branch da fatia) | `.md` | ST:14 campo `PR` | O PR só existe depois do push (autorizado no lote): então o `status.md` com o link vai num **2º commit + 2º push** (SI:117 "commit e, com o mesmo sim, push"). P3 não listou o 2º commit/push. Push `ask` no AG-O (AG-O:228), pelo Kiro; `--force` negado | Push/PR negado pelo usuário no `ask` → NÃO ESPECIFICADO (estado: fica `aceita`, commit local). Com `não — a pessoa abre`: o loop para em `aceita` (SL:42-43), sem push; quem empurra a branch não é dito | NÃO ESPECIFICADO (2º push; recusa do ask; quem faz push no "não — a pessoa abre") |
| F4 | pendências no `status.md`: `ELM pendente: <…>` (SL:47-48, 133-134), horas (SL:117-119) | Sim | texto | Formato como em S17 | Grava na worktree/branch da fatia; commit na worktree | MCP ausente → `ELM pendente` ✓ (SL:134) | OK (formato ver S17) |

Sem escrita: **S19-X1** (trilha rápida: sem fases/GATE; nada gravado até a confirmação do lote) · **S19-X2** (mesmo erro em duas fatias: grava `status.md` das afetadas e o log, sem decisão sobre as demais) · **S19-F1** (retomada: só lê até o "sim", P3 correto).

#### Achados de persistência · S19
- `sdd-loop/SKILL.md:96-97` × `64, 86, 90`: o plano pausado só existe na worktree até a fase 8; "na branch, se o push foi autorizado" não corresponde a nenhum passo.
- `sdd-loop/SKILL.md:21, 109-128`: o log nunca é fechado nem arquivado; o resumo não vai para ele; Passo 0 reabre logs antigos.
- `sdd-loop/SKILL.md:62-65` × `sdd-iniciar/SKILL.md:112-114` × `ST:15`: o campo ELM do `status.md` da worktree fica sem ids (o loop pula o item 4).
- `sdd-loop/SKILL.md:120` × `AG-O:95`/`AG-V:81`: worktrees ficam para sempre salvo ação manual; a branch não pode ser apagada enquanto isso (S17).
- `sdd-loop/SKILL.md:58-59`: branch em uso no checkout principal impede `worktree add`; sem tratamento.
- `AG-O:39-44` × `AG-V:43`: `.kiro/local/verificacao/<ft>/` não está no allow do orquestrador; no loop, o caminho a usar (raiz × worktree) não é dito.

---


## Parte 5 — Consolidação (orquestrador · Opus)

### 5.1 Matriz por skill

Contagens tiradas das tabelas das Partes 2–4 (Parte 3: linhas da tabela-resumo e blocos com veredito; Parte 4: última coluna das tabelas de arquivos). São indicativas, não uma nota de qualidade.

| Skill | Fluxos (P2) | Determinístico | Ambíguo | Sem regra | Conflito | Arquivos OK | Divergente | Não especificado |
|---|---|---|---|---|---|---|---|---|
| S01 `sdd` | 3 | 2 | 2 | 0 | 2 | 0 | 0 | 0 |
| S02 `sdd-setup` | 5 | 2 | 5 | 1 | 2 | 6 | 6 | 4 |
| S03 `sdd-status` | 4 | 3 | 2 | 2 | 1 | 1 | 1 | 1 |
| S04 `sdd-triar` | 11 | 4 | 6 | 3 | 2 | 2 | 4 | 4 |
| S05 `sdd-iniciar` | 12 | 3 | 6 | 2 | 3 | 3 | 3 | 0 |
| S06 `sdd-atender` | 7 | 1 | 4 | 4 | 2 | 0 | 5 | 4 |
| S07 `sdd-entrevistar` | 5 | 2 | 2 | 1 | 1 | 2 | 1 | 4 |
| S08 `sdd-prd` | 3 | 1 | 3 | 2 | 0 | 3 | 4 | 4 |
| S09 `sdd-fatiar` | 5 | 0 | 3 | 2 | 2 | 0 | 3 | 5 |
| S10 `sdd-planejamento` | 6 | 1 | 2 | 4 | 2 | 1 | 3 | 8 |
| S11 `sdd-elm` | 12 | 4 | 3 | 4 | 4 | 5 | 3 | 4 |
| S12 `sdd-pesquisar` | 6 | 3 | 3 | 2 | 1 | 3 | 2 | 4 |
| S13 `sdd-plano` | 12 | 3 | 7 | 4 | 2 | 5 | 6 | 9 |
| S14 `sdd-implementar` | 12 | 5 | 6 | 1 | 4 | 3 | 5 | 7 |
| S15 `sdd-revisar` | 5 | 2 | 2 | 2 | 3 | 3 | 2 | 2 |
| S16 `sdd-verificar` | 4 | 1 | 4 | 2 | 1 | 1 | 3 | 3 |
| S17 `sdd-consolidar` | 4 | 1 | 4 | 2 | 0 | 2 | 3 | 5 |
| S18 `sdd-aprender` | 3 | 0 | 3 | 3 | 0 | 0 | 1 | 5 |
| S19 `sdd-loop` | 4 | 0 | 4 | 1 | 1 | 3 | 1 | 5 |

### 5.2 Veredito geral

**O fluxo é coeso no desenho e no caminho principal; a execução literal quebra nas bordas, nos commits entre papéis e nas permissões dos agentes.**

O que se sustenta (confirmado nas Partes 1–4):

- **Caminho feliz fechado.** Numa sessão da pessoa, com o power carregado, todo handoff do caminho principal tem
  origem, destino e artefato em disco: triar → iniciar → pesquisar → plano → GATE → implementar → revisar →
  verificar → PR → merge → consolidar → aprender.
- **A máquina de estados da fatia é a mesma em todas as skills.** `status.md` tem as mesmas fases na `sdd-iniciar`,
  na `sdd-status`, no `sdd-loop` e no template, e o WIP de revisão humana (`plano-em-revisao` + `aceita` +
  `pr-aberto`) é contado igual nas três skills que o usam.
- **Gates e regras de ouro aplicados de forma uniforme.** "Sim" para ELM, push e branch; "ELM nunca trava" vira
  `ELM pendente`; dado de cliente vai para `.kiro/local/`; teste nunca é afrouxado; `backlog.md` só é escrito na base.
- **Assets válidos.** Os 6 agentes, o hook, os 2 workflows e o schema passam em `json.tool`, e o `http.sh` passa em
  `sh -n`. Os blocos de permissão V2 e V3 são espelhos, e os caminhos de escrita prescritos pelas skills batem
  com as allowlists dos agentes que as executam (G4).

O que não se sustenta, em resumo:

- Um executor mecânico chega a um veredito **não determinístico na maioria dos fluxos** (matriz 5.1). São
  ambiguidades de critério (tamanho, "PR parado", "pesquisa curta"), destinos ausentes (o que fazer no 2º
  AJUSTAR, no GATE recusado ou em "só ambiente") e conflitos entre skills.
- **Nenhuma das 19 skills define o comportamento para falha de escrita**: diretório inexistente, permissão
  negada, recusa da confirmação do Kiro ou gravação parcial. As únicas exceções são "crie a pasta se não existir"
  (fichas) e o `ELM pendente` do ELM. Para a pergunta "o que acontece se o diretório estiver inacessível?", a
  resposta é **NÃO ESPECIFICADO** em todos os fluxos com escrita.

### 5.3 Achados priorizados

Verificação do orquestrador: **CONFIRMADO** = conferido direto na fonte · **VALIDADO** = executado pelo agente
(schema ou parse) · **PLAUSÍVEL** = coerente com o texto, mas depende de como o agente é instruído em tempo de
execução.

| # | Sev. | Achado | Skills | Partes | Verificação |
|---|---|---|---|---|---|
| A1 | Alta | **Skills sem agente e agentes sem permissão.** `sdd-consolidar`, `sdd-aprender`, `sdd-setup` e `sdd` não estão em nenhum agente; `sdd-iniciar` e `sdd-status` estão só no `sdd-orquestrador`, que não tem `git switch` nem `git pull --ff-only`. O `sdd-produto` oferece "começar agora" sem ter a `sdd-iniciar` e nega `git push` (a triagem manda "push com sim"). Fora do loop, só a sessão padrão executa o ciclo completo, e nenhuma skill diz isso. | S04 S05 S17 S18 S03 | P1 (O1), P4 G2/G5 | CONFIRMADO (`assets/agents/*.json`) |
| A2 | Alta | **Artefatos dos papéis sem dono de commit.** Revisor, verificador e pesquisador não têm `git add`/`commit`. Os relatórios só entram no Passo 0 da *próxima* sessão da `sdd-implementar`, e o Passo 5 (PR) commita só o `status.md`. O PR pode abrir citando `revisao-codigo-<N>.md` e `verificacao.md` que não estão na branch, e o `CT.csv` pode não chegar à base para a `sdd-elm` modo *testes*. `revisao-prd-<N>.md` também fica fora do commit do GATE do PRD. | S12 S14 S15 S16 S17 S08 | P4 G4/G5 | CONFIRMADO (`sdd-verificador.json`; `sdd-implementar` Passos 0 e 5) |
| A3 | Alta | **Estado nunca limpo entre sessões.** A `sdd-implementar` grava o Histórico *depois* do commit da tarefa (Passo 1, itens 6→7). A `sdd-plano` só commita no ramo "Aprovado", então "análise basta", rápida sem GATE e `plano-em-revisao` ficam sem commit. O Passo 0 desconta só relatórios, e assim a sessão seguinte "avisa e para". O workflow `sdd-planejar-fatia` (passo `ajustar`: "OK sem GATE pendente → nada mais") nem grava `fase: implementando`, e o `sdd-entregar-fatia` não começa. | S13 S14 + workflows | P3 G4, P4 G4 | CONFIRMADO (`sdd-implementar:20-22,46-47`; `sdd-plano:85`; `sdd-planejar-fatia.workflow.json`) |
| A4 | Alta | **Revisão de código pode aprovar sem backpressure executado.** C3 é BLOQUEANTE e "executar", mas "C3 falhando por ambiente → `AMBIENTE`, não conta como achado". Com zero achados, o veredito é `APROVADO`. | S15 | P2 G4, P3 G4 | CONFIRMADO (`sdd-revisar/references/rubricas.md:58,80`) |
| A5 | Alta | **`[VER]` concluída antes do PR; `[REV]` com dois momentos.** A `sdd-verificar` lança as horas e conclui a `[VER]` no ACEITO, antes da leitura humana do PR; mudança pedida no PR reabre a verificação com a tarefa fechada. Sem MCP (agente verificador, loop), a `[VER]` vira `ELM pendente` e nenhuma skill a recolhe: a consolidação trata só `[DEV]`/`[REV]`. O loop manda lançar a `[REV]` na conclusão da revisão; a consolidação, no merge. | S16 S17 S19 | P1 (O2), P2 G5, P3 G5 | CONFIRMADO |
| A6 | Alta | **Escrita na base sem o preâmbulo de base, e "PR curto" sem branch.** Triar, consolidar e aprender fazem `switch` para a base, `pull --ff-only` e param com árvore suja. Atender, planejamento e prd só dizem "commit na base"; o PRD grava rascunhos desde o Passo 1 e só commita no GATE, deixando a árvore suja e travando as outras skills. Com o padrão "PR curto para a base", nenhuma skill nomeia a branch do PR, e o próximo `pull --ff-only` (ou a `sdd-fatiar` procurando o PRD aprovado) não vê o que está no PR. | S06 S08 S09 S10 S17 S18 | P1 (O4), P4 G2/G3/G5 | CONFIRMADO (atender); PLAUSÍVEL (efeito do PR curto) |
| M1 | Média | **Modo autônomo sem limite de passos na própria skill.** O loop delega "sdd-plano, Passos 2–3" e "sdd-implementar, Passos 0–2", mas o modo autônomo das skills não para antes da análise e da revisão. O codificador tem `subagent/sdd-revisor` e rodaria análise e revisão por conta própria, duplicando fases e o contador de rodadas. | S13 S14 S19 | P2 G4, P3 G4, P4 G4 | PLAUSÍVEL (depende do prompt do orquestrador) |
| M2 | Média | **Destinos ausentes.** Os casos sem destino definido: 2ª análise `AJUSTAR` fora do loop (`sdd-plano:65`); GATE do plano recusado; verificação só com `⚠️ ambiente` (sem linha `VERIFICACAO:`); "Banco pendente → pare" sem fase; `REVISAR` na trilha direta (sem rodadas nem bloqueio); `AMBIENTE` na validação completa, sem campo no `status.md`. | S13 S14 S15 S16 | P3 G4/G5 | CONFIRMADO (texto) |
| M3 | Média | **Numeração das rodadas incompatível.** O `<N>` do relatório é "próxima rodada" (revisar). Plano, implementar e loop incrementam *antes* de pedir; os workflows, *depois*. "Zerar as rodadas" (2ª reprovação) faz o revisor sobrescrever `revisao-codigo-1.md`. O épico não tem contador para `revisao-prd-<N>`. | S13 S14 S15 S19 | P4 G4 | PLAUSÍVEL |
| M4 | Média | **Idempotência do EWM e baixa de pendências.** A busca de publicação interrompida usa "título com `[FT-031]`", que não casa com tarefas `[DEV] FT-031 Implementar`, e a tarefa é duplicada no rerun. `ELM feito:` só aparece no template: nenhuma skill manda escrevê-lo, então a `sdd-status` lista as pendências para sempre. | S11 S03 | P4 G3 | CONFIRMADO (texto da `sdd-elm`, "Regras de toda publicação") |
| M5 | Média | **Atendimento incompleto.** Sem regra para Kanban ou para sprint não aberta. O `AT-nnn` é incrementado antes da confirmação. `**Origem:**` não leva o id do EWM, e o item volta a cada lote de importação. A conclusão diz que o "modo horas lança e conclui", mas a `sdd-elm` diz que lançar não conclui. O caminho `sprints/sprint-<nn>.md` está sem o prefixo `<produto>/planejamento/`. | S06 S11 S04 | P1 (O5/O6), P3 G2, P4 G2 | CONFIRMADO |
| M6 | Média | **`equipe.json` do modo inicial não passa no schema.** O schema exige `projeto.nome`, `inicio`, `duracao-sprint-semanas`, `membros[].ativo` e `historico: []`, e o roteiro não coleta nenhum deles. | S10 | P3 G3, P4 G3 | VALIDADO (jsonschema, pelo agente) |
| M7 | Média | **Formatos divergentes entre arquivos.** Os casos encontrados: `padrao/rapida` (status.md) × `padrão/rápida` (backlog, ficha); `Cobre` do status.md sem `C1…Cn` da ficha; `cobre` `HF-01 · 1.1` × `HF-01#1.1`; `substituida-por` como campo × texto em `obs`; `verified` como objeto × lista; YAML quebra com `: ` no título; `CT.csv` sem regra de cabeçalho e com `;` livre no Resumo; coluna "Tarefa ELM" que não existe na tabela Fatias do `sprint-<nn>.md`; `decisoes.md` "só acréscimo" × marcar a linha antiga como `substituída`. | S04 S05 S07 S08 S09 S10 S11 S16 | P4 G2/G3/G5 | CONFIRMADO (amostras) |
| M8 | Média | **`sdd-setup` grava fora do escopo e antes do "Gravar?".** Ela escreve em `~/.kiro/settings/mcp.json`, roda `kiro-cli settings --workspace`, faz exclusões em tsconfig/jest/lint, chama a `elm-setup` e roda build/testes, contra "nada gravado antes do Passo 8" e "nada fora de `.kiro/`…". O commit sugerido não tem branch, e a regra "nada de `<…>` sobrando" é impossível de cumprir com o template do `sdd.md`. Na migração `sdd2`, os workflows continuam citando agentes removidos. | S02 | P3 G1, P4 G1 | PLAUSÍVEL |
| M9 | Média | **Loop: trilha rápida, log e worktree.** A rápida entra no lote sem fases nem GATE próprios. O log `.kiro/local/loop-*.md` nunca é fechado, e o Passo 0 reabre logs antigos. O loop pula o item 4 do Passo 4 da iniciar, então o campo ELM fica sem ids e as horas não acham a tarefa. `git worktree remove` é negado a todos os agentes e nenhuma skill é dona da remoção. A lição do loop não pode ir à base de dentro da worktree. | S19 S18 S17 | P2 G5, P3 G5, P4 G5 | CONFIRMADO (deny no `sdd-orquestrador.json`) |
| M10 | Média | **Roteamento conflitante para o mesmo pedido.** "Retomar a FT-031" pode ir para a `sdd-status` (description) ou para a `sdd-iniciar` (guia). Pedido novo na review vai para `sdd-prd`/`sdd-fatiar` (planejamento) ou para a `sdd-triar` ("toda demanda nova entra pela triagem"). | S01 S03 S05 S10 | P3 G1/G3 | CONFIRMADO |
| B1 | Baixa | **Gatilhos sem fluxo.** Estes gatilhos de description não têm passo correspondente: "como está a sprint" (status filtrado), "resumo das lições" (aprender), "atendimentos abertos" (atender), "quais decisões em aberto" (entrevistar). | S03 S06 S07 S18 | P3 G1/G2/G5 | CONFIRMADO |
| B2 | Baixa | **Critérios sem limiar.** Faltam limiares para: tamanho P/M/G na triagem; "PR parado"; "pesquisa curta"; "mesmo erro em duas fatias"; mecânico × julgamento na lição; "correção (1.1) × escopo (2.0)" no PRD; "recomendada" no encaixe. | vários | P3 todos | CONFIRMADO |
| B3 | Baixa | **Resumos omitem o `design.md` da rápida.** README, guia e `sdd-iniciar` resumem a rápida como `bugfix.md` + `tasks.md`; os templates têm um `design.md` curto. | S01 S05 S13 | P1 (O3) | CONFIRMADO (`plano-templates.md:145`) |
| B4 | Baixa | **Escrita negada a subagentes herdados.** O revisor chamado como subagente do codificador herda o deny de `.kiro/local/wf/**` e não grava `plano.json`/`codigo.json`. O `<id>` de `.kiro/local/wf/<id>/` não é definido (`FT-031` × `ft-031`). | S15 + workflows | P4 G4 | PLAUSÍVEL ("deny-wins intersection", não testado) |

Refutações relevantes da Parte 3 feitas na Parte 4. Elas mostram o limite do executor mecânico, e o detalhe está em
cada grupo no Anexo A:

- **S12-F6:** a pergunta pontual tem regra no prompt do agente pesquisador, então não é `SEM REGRA`.
- **Pasta da fatia:** a convenção é `ft-031-…` em minúscula, não `FT-031-…`.
- **S10-F5:** a Review não prescreve "ok + commit", então ela não é `DETERMINÍSTICO` como a Parte 3 marcou.
- **S11-F6:** a virada no ELM não grava arquivo.
- **Calibrar:** "lição `revisao-branda` sobe a severidade" não é conflito com "sugestão nunca reprova". A
  severidade sobe *antes* do veredito, e isso é o comportamento pretendido (avaliação do orquestrador).
- **O7 (Parte 1):** o encaixe voltar ao "Passo 3, item 4" da iniciar é a continuação correta, não um erro. O
  achado foi retirado pelo orquestrador.

### 5.4 Correções sugeridas (ordem de custo-benefício)

1. **Uma regra de commit por papel.** Quem pede a rodada (plano, implementar, loop) commita o relatório que recebe,
   logo depois de recebê-lo. Isso inclui `research.md`, `analise-*`, `revisao-*`, `verificacao.md` e `CT.csv`.
   Grave o Histórico *antes* do commit da tarefa, e acrescente os arquivos do plano às exceções do Passo 0. Fecha
   A2 e A3.
2. **Tabela "skill → agente → comandos".** Inclua `sdd-iniciar` no `sdd-codificador` (ou `git switch`/`pull` no
   orquestrador) e `sdd-consolidar`/`sdd-aprender` no `sdd-produto`, com escrita no `status.md` da fatia. Ou declare
   no guia que essas skills rodam só na sessão padrão. Fecha A1.
3. **Um bloco "Gravar na base" único**, em `backlog.md` → regras, citado por toda skill que escreve artefato de
   produto (atender, planejamento, prd, entrevistar, setup). Ele deve nomear a branch do PR curto. Fecha A6.
4. **C3 por ambiente → `VEREDITO: REVISAR` com `AMBIENTE`, nunca `APROVADO`** (rubricas). Fecha A4.
5. **`[VER]` concluída no merge, junto com `[DEV]`/`[REV]`**, e uma única regra de horas no loop. Fecha A5.
6. **Uma linha "falha de escrita" nas regras de ouro do guia**: diretório inexistente → criar; permissão negada ou
   confirmação recusada → `bloqueada` com o caminho; gravação parcial → o próximo passo retoma pelo que está no
   disco. Responde à Parte 4 para todas as skills.
7. Normalizar os formatos de M7 num só lugar (template e reference) e completar o roteiro do `equipe.json` (M6).


## Anexo A — Notas de método e resumos por grupo

### Parte 2 — Plano do fluxo esperado · G1


Base: `powers/sdd/` (README.md, skills/). Citações no formato `arquivo:linha`, caminhos
relativos a `skills/` salvo indicação. Somente leitura: nada foi alterado no repositório.

Abreviações: `SKILL` = `<skill>/SKILL.md`; `agentes.md` = `sdd-setup/references/agentes.md`; `toolkits.md` =
`sdd-setup/references/toolkits.md`; `automacoes.md` = `sdd-setup/references/automacoes.md`.

---


### Parte 2 — Plano do fluxo esperado · G2


Convenções: linhas citadas são de `powers/sdd/skills/<skill>/SKILL.md` salvo indicação.
`triar:NN` = sdd-triar/SKILL.md; `ficha:NN` = sdd-triar/references/ficha.md; `iniciar:NN`; `atender:NN`; `entrev:NN`;
`tmpl:NN` = sdd-iniciar/references/status-template.md; `backlog:NN` = sdd-fatiar/references/backlog.md;
`plan:NN` = sdd-planejamento/SKILL.md; `elm:NN` = sdd-elm/SKILL.md; `steer:NN` = sdd-setup/assets/steering/sdd.md;
`guia:NN` = sdd/SKILL.md; `readme:NN` = README.md do power.

---

### Resumo de lacunas mais graves (as 3 do relatório)

1. **Saída do atendimento e origem EWM não fecham** — atender:16-17 (devolver à triagem) × atender:61 (ir direto a `sdd-entrevistar`/`sdd-prd`, sem destino de decisões/EP registrado: entrev:18-20, prd:40); e o `**Origem:**` do AT não recebe o id DF/IB (atender:69, entrev:117) embora o lote da triagem dependa dele (triar:132-133,153), então itens de atendimento reaparecem em todo lote e a `[ATD]` não se liga ao item de origem.
2. **Aprovação da ficha e retomada da triagem sem procedimento** — gatilho "aprova a ficha da FT-040" (triar:3) não tem passo; login/identidade do P.O. indefinidos (ficha:46); e ficha de fatia já iniciada cai ao mesmo tempo em "retome" (triar:40-44) e "pare" (triar:45-46) com triar:160-161 supondo um caso que o Passo 1 não detecta.
3. **Handoffs entre skills que não fecham** — (a) `plan:104` manda voltar à `sdd-iniciar` "Passo 3, item 4" (WIP) em vez do item 3/5; (b) `sdd-iniciar` só está nos recursos do agente `sdd-orquestrador` (sdd-setup/assets/agents/sdd-orquestrador.json:18), não em `sdd-produto` nem `sdd-codificador`, apesar de `sdd-triar`/`sdd-atender` (agente `sdd-produto`) lhe oferecerem "começar agora"; (c) `atender:56` (horas "lança e conclui") × `elm:194-195` (lançar não conclui).

Outras lacunas menores estão nos fluxos acima (Kanban em atender; "atendimentos abertos" sem fluxo; `tmpl` trilha sem acento × `backlog`; base/árvore limpa/push no atender; dirty tree no iniciar para branch nova; WIP lido antes de `git fetch`).

### Parte 2 — Plano do fluxo esperado · G3


Convenções de citação (todas relativas a `powers/sdd/`):
`prd:NN` = skills/sdd-prd/SKILL.md · `prd-tpl:NN` = sdd-prd/references/prd-template.md · `okf:NN` = sdd-prd/references/okf-elm.md ·
`fatiar:NN` = skills/sdd-fatiar/SKILL.md · `backlog.md:NN` = sdd-fatiar/references/backlog.md ·
`plan:NN` = skills/sdd-planejamento/SKILL.md · `arquivos:NN` = sdd-planejamento/references/arquivos.md ·
`elm:NN` = skills/sdd-elm/SKILL.md · `mapeamento:NN` = sdd-elm/references/mapeamento.md ·
`steering:NN` = skills/sdd-setup/assets/steering/sdd.md · `README:NN` · `sdd/SKILL:NN` = skills/sdd/SKILL.md ·
`triar:NN`, `iniciar:NN`, `consolidar:NN`, `atender:NN`, `verificar:NN`, `loop:NN` = skills/<skill>/SKILL.md.

Premissas comuns (steering/sdd.md): artefatos de produto vão para a branch base, nunca para branch de fatia (steering:61, backlog.md:6-7);
toda escrita no ELM só com "sim" (steering:13, sdd/SKILL:120); sem MCP → `ELM pendente` (sdd/SKILL:122-124); horas só na conclusão da tarefa, nunca nos GATEs (steering:16).

---

#### Resumo transversal (cruzamento README / skills)
- Contradição entre `README:13-15`/`sdd/SKILL:37-39` (fluxo triar → PRD → ELM) e `mapeamento:13` (épico "nasce" pela `sdd-prd`): a triagem é o dono real (triar:78).
- Handoffs que não fecham: (a) PRD alterado → fatias `pronta` não reconferidas (S08-F3); (b) `rastreia` e `afeta` (mapeamento:33-34) sem modo que os grave (`afeta` não é citado em nenhuma skill); (c) conclusão do épico no EWM (S11-F12); (d) divisão de fatia em andamento (S09-F2).

### Parte 2 — Plano do fluxo esperado · G4


Base: `powers/sdd/skills/`. Citações `arquivo:linha` são relativas a essa pasta. Abreviações de arquivo:
`pesq` = `sdd-pesquisar/SKILL.md` · `plano` = `sdd-plano/SKILL.md` · `tmpl` = `sdd-plano/references/plano-templates.md` ·
`impl` = `sdd-implementar/SKILL.md` · `rev` = `sdd-revisar/SKILL.md` · `rub` = `sdd-revisar/references/rubricas.md` ·
`stpl` = `sdd-iniciar/references/status-template.md` · `loop` = `sdd-loop/SKILL.md` · `steer` = `sdd-setup/assets/steering/sdd.md` ·
`wf-plan` / `wf-ent` = `sdd-setup/assets/workflows/sdd-planejar-fatia.workflow.json` / `sdd-entregar-fatia.workflow.json`.

Fases da fatia (stpl:18-27): `pesquisando → planejando → plano-em-revisao → implementando → revisando → verificando → aceita → pr-aberto → concluida`; desvio `bloqueada (de: <fase>)`.

---

#### Resumo dos IDs

S12: F1 Pesquisa pedida pela pessoa · F2 Pesquisa chamada pela sdd-plano (agente) · F3 Pesquisa autônoma (loop/workflow) · F4 Pesquisa da trilha rápida · F5 Pesquisa sem agente (inline) · F6 Pergunta pontual sem fatia
S13: F1 Plano padrão HITL (GATE aprovado) · F2 Plano AFK "análise basta" · F3 Plano AFK com aprovação humana (pausa no loop) · F4 Plano da trilha rápida (bugfix; GATE não/sim) · F5 Lacuna de negócio → parar · F6 Divergência ELM × código · F7 Fatia grande → propor divisão · F8 Análise independente (OK / AJUSTAR / sem subagente) · F9 Aprovação em sessão posterior (plano-em-revisao) · F10 Replanejar · F11 Modo autônomo · F12 Guarda de entrada (direta/sem pasta)
S14: F1 Implementação padrão HITL · F2 Trilha rápida (corretiva) · F3 Corrigir achados ([R<n>]) · F4 Divergência plano × código · F5 Revisão REVISAR (1ª rodada) · F6 2ª reprovação → bloqueada · F7 Verificação de aceite · F8 Abertura do PR · F9 Pronta para revisão/PR (agente sem push/subagente) · F10 Modo autônomo · F11 "Start task" do Kiro · F12 Trilha direta
S15: F1 Rubrica P (PRD) · F2 Rubrica L (plano) · F3 Rubrica C (código, dois eixos) · F4 Rubrica C trilha direta · F5 Execução sem agente / pedido sem rubrica explícita

#### Lacunas mais sérias (ranking)

1. **Modo autônomo não delimita o escopo do codificador (S13-F11, S14-F10):** `plano:95-98` e `impl:131-134` não dizem "pare antes do Passo 4 / Passo 3". O `sdd-codificador` tem `subagent/sdd-revisor`; só o `loop:84,87` ("Passos 2–3", "Passos 0–2") e os workflows ("Não rode a análise nem o GATE", "Não peça revisão") impõem o limite — a skill sozinha duplicaria análise/revisão/verificação e as Rodadas.
2. **Plano/estado não commitado quebra a implementação, e GATE reprovado/2 análises sem OK sem destino (S13-F1/F2/F8, S14-F1):** o commit do plano só é mandado quando "Aprovado" (`plano:85`); no ramo "análise basta"/rápida sem GATE e após cada tarefa o `status.md` fica sujo, e `impl:20-22` exige árvore limpa descontando só relatórios (não `research/requirements/design/tasks/status`). Além disso `plano:65` ("até 2 rodadas") e o Passo 5 não definem o que acontece na 2ª reprovação da análise ou quando a pessoa **não** aprova o GATE (só no `loop:85,97-98`).
3. **Revisão/veredito frágil (S15-F3, S15-F4, S14-F12):** (a) `rub:80` faz C3 por AMBIENTE "não contar como achado", permitindo `VEREDITO: APROVADO` sem nunca executar o backpressure (contra rev:40-41); (b) rubrica L não verifica forma do programa, contrato de pronto, "falsificável na base" nem o limite de tamanho (rub:30-41 × plano:42-52,75); (c) trilha direta tem relatório "só na conversa" (`rev:30`) contra `rev:54-58`, adapta só C1/C2/C6 e `impl:121-129` não define `REVISAR`/rodadas/bloqueio.

Outras: fluxo REJEITADO da verificação não diz se repete a revisão C (impl:88-89 × `loop:89`); incrementador de Rodadas diverge (impl:75, plano:60, `stpl:25-27`, wf-plan/wf-ent — o workflow faz o verificador incrementar, o template diz que não); "branch desatualizada" sem tratamento no loop (impl:100-101); pesquisa "curta" da trilha rápida sem definição (S12-F4); `sdd-pesquisar` não cobre a "pergunta pontual" do prompt do agente (S12-F6).

### Parte 2 — Plano do fluxo esperado · G5


Base: `powers/sdd/skills/`. Citações `arquivo:linha` são relativas a essa pasta, salvo `README.md` (`../README.md`).
Abreviações: SV = `sdd-verificar/SKILL.md`, CT = `sdd-verificar/references/ct-csv.md`, SC = `sdd-consolidar/SKILL.md`, SA = `sdd-aprender/SKILL.md`, SL = `sdd-loop/SKILL.md`, SI = `sdd-implementar/SKILL.md`, ELM = `sdd-elm/SKILL.md`, STEER = `sdd-setup/assets/steering/sdd.md`.
Somente leitura: nada no repositório foi alterado.

---

#### Resumo das lacunas mais sérias (ordem de gravidade)

1. **Horas/conclusão da `[VER]` (e `[REV]` no loop) não fecham em modo agente/AFK** — SV:77-80 manda perguntar horas a "quem verificou" e lançar via `sdd-elm`; o `sdd-verificador` não tem MCP, não tem modo `AUTONOMO` e o loop (SL:75, 89, 118-119) delega a "quem revisa e verifica"; SC:48 só trata `[DEV]`/`[REV]` no merge. A `[VER]` fica só como `ELM pendente` no `status.md`, sem skill que a esvazie (ver S16-F1, S17-F1, S19-F4).
2. **Loop × rejeição da verificação/revisão** — SL:89 (REJEITADO → volta à fase 5 "uma vez") não manda repetir a fase 6 (revisão de código) após o conserto, contrariando SI:73-83; SV não tem limite de rodadas e não define estrutura multi-rodada do `verificacao.md`; SL:90 ignora "branch desatualizada" (SI:98-100); e a trilha **rápida** não tem fluxo no loop (SL:30, 81-90) (ver S16-F2, S19-F2).
3. **Dono ausente para `sdd-consolidar`/`sdd-aprender` e handoffs de limpeza** — nenhum agente `sdd-*.json` carrega `sdd-consolidar` nem `sdd-aprender`; o loop acumula "Lições para registrar" (SL:115) e worktrees (SL:120) sem passo que as consuma; SA:19-21 exige `git switch <base>`, impossível dentro da worktree do loop; `sdd-consolidar` não remove worktree nem trata o orquestrador negar `git worktree remove` (ver S17-F1, S18-F1, S19-F4).

### Parte 3 — Teste do Quarto Chinês · G1


Executor mecânico: cada bloco aplica só o texto das fontes. Nada foi alterado no repositório (somente leitura).

**Fontes usadas como regra:** `skills/sdd/SKILL.md`, `skills/sdd-setup/SKILL.md`, `skills/sdd-status/SKILL.md`, e os
arquivos que estes citam: `sdd-setup/references/toolkits.md`, `sdd-setup/references/agentes.md`,
`sdd-setup/references/automacoes.md`, `sdd-setup/assets/steering/sdd.md`, `sdd-setup/assets/hooks/sdd.json`.
**Não usadas como regra:** SKILL de outras skills (ex.: `sdd-iniciar`, `sdd-triar`, `sdd-planejamento`) e o
`status-template.md` de `sdd-iniciar` (nenhuma das três skills o cita). Quando a regra depende disso, o veredito é
SEM REGRA ou AMBÍGUO.
**Do plano (Parte 2)** usei só os IDs, nomes e gatilhos dos fluxos. Os vereditos vêm das fontes.

Critérios de veredito: DETERMINÍSTICO = um único resultado possível; AMBÍGUO = uma regra admite duas leituras que
produzem saídas diferentes; SEM REGRA = o input não tem regra que o trate; CONFLITO = duas regras mandam coisas
incompatíveis (ambas citadas).

Convenção: "`:N`" = linha do arquivo indicado no início da regra (`sdd/SKILL.md` para S01, `sdd-setup/SKILL.md` para S02,
`sdd-status/SKILL.md` para S03, salvo indicação).

---

#### Resumo consolidado (somente não-DETERMINÍSTICOS)

| Skill | Fluxo | Veredito | Nota curta |
|---|---|---|---|
| sdd | S01-F1 Explicar o fluxo | AMBÍGUO | Princípios sem condição; checagem de sdd.md sem ação |
| sdd | S01-F3 Consulta de referência | AMBÍGUO | "Quem aprova o plano" não casa gatilho literal |
| sdd | S01-E1 Demanda + "o que faço agora" | CONFLITO | :79 × :80 |
| sdd | S01-E2 Trabalho com sdd.md ausente | CONFLITO | :17-18 × :81 |
| sdd-setup | S02-F1 Primeira configuração | CONFLITO | Glossário ausente: :25-26 × :123; também :26 × :152-153 |
| sdd-setup | S02-F2 Atualização | AMBÍGUO | Colunas não definidas; passos reexecutados não mapeados (:45-46) |
| sdd-setup | S02-F3 Migração sdd2 | AMBÍGUO | Momento do git mv/rm: :50 × :26 |
| sdd-setup | S02-F4 Migração v1 | AMBÍGUO | "sai com git rm e ok" sem momento (:64-65) |
| sdd-setup | S02-F5 Ligar toolkit | AMBÍGUO | Proposta completa (:183) × só novas (toolkits.md:128-130) |
| sdd-setup | S02-E1 gh ausente | AMBÍGUO | Aviso de instalação só para GitLab (:113) |
| sdd-setup | S02-E2 "nada — só regenerar" | SEM REGRA | Versão e data do sdd.md sem fonte (assets/steering/sdd.md:19; :232) |
| sdd-setup | S02-E4 KIRO_HOME fora do home | CONFLITO | :38-39 (pede caminho absoluto) × :40-43 (nunca absoluto) |
| sdd-status | S03-F1 Painel "onde parei" | SEM REGRA | Skill de "revisar o PR" ausente (:49); dias restantes (:41); PR parado (:66) |
| sdd-status | S03-F2 Painel "como está a sprint" | AMBÍGUO | Modo filtrado citado (:3) e não definido |
| sdd-status | S03-F4 Fechar a sessão | AMBÍGUO | "Pronto e verde" (:93) sem critério |
| sdd-status | S03-E2 Fechar sessão sem fatia | SEM REGRA | Só trata sessão numa fatia (:88) |
| sdd-status | S03-E4 "Retomar a FT-031" | CONFLITO | sdd-status:3 × sdd:81 |

Totais: 24 fluxos (12 do plano + 12 bordas/negativos). DETERMINÍSTICO: 7. Não-determinísticos: 17
(CONFLITO 5 · AMBÍGUO 9 · SEM REGRA 3).

Achados transversais (para a Parte 4, se houver):
- Escrita antes do Passo 8 na sdd-setup (:26) contradita por :50, :64-65 e :152-153. (Os "ok" do Passo 9, em :272-273, vêm depois do Passo 8 e não entram aqui.)
- Sem regra de escolha de fatia para "fechar a sessão" (sdd-status :88, :91).
- status.md e tasks.md usados sem formato citado em sdd-status (:21-23).
- Sobreposição de gatilhos "o que fazer agora" / "retomar" entre sdd, sdd-status e sdd-iniciar (sdd:79-81; sdd-status:3).

### Parte 3 — Teste do Quarto Chinês · G2


Fontes usadas (somente leitura): `powers/sdd/skills/<skill>/SKILL.md` das quatro skills, seus `references/` (`sdd-triar/references/ficha.md`, `sdd-iniciar/references/status-template.md`, `sdd-fatiar/references/backlog.md`), e os trechos das skills que elas citam para um passo concreto: `sdd-elm/SKILL.md` (modos similares, backlog, sprint, atendimento, horas), `sdd-planejamento/SKILL.md:93-105` (Encaixe). O campo do `.kiro/steering/sdd.md` foi conferido no template `sdd-setup/assets/steering/sdd.md`, porque as quatro skills leem valores dele.

Não consultadas (não citadas pelas quatro skills nos passos simulados): sdd-plano, sdd-fatiar, sdd-prd, sdd-consolidar, sdd-status, sdd-loop.

Convenções: `triar:NN`, `iniciar:NN`, `atender:NN`, `entrev:NN` = linhas do SKILL.md da skill; `ficha:NN`, `tmpl:NN`, `backlog:NN`, `elm:NN`, `plan:NN` = arquivos citados acima. O bloco ESTADO descreve premissas do teste (não fatos do repositório). "Estado comum" de cada skill vale para todos os fluxos da skill, salvo indicação.

Vereditos: DETERMINÍSTICO · AMBÍGUO · SEM REGRA · CONFLITO.

Nota transversal (não repetida em cada bloco): o nome da branch e o da ficha usam `<slug>` (iniciar:91, triar:85 e 86, ficha:58 não definem o formato). Só vira veredito próprio onde é o único problema do fluxo.

---

#### Vereditos não-DETERMINÍSTICOS (para o caller)

| Fluxo | Veredito | Nota curta |
|---|---|---|
| S04-F1 | AMBÍGUO | "regra de negócio clara" (triar:53) × "diga a trilha" (triar:59): quem julga? |
| S04-F2 | SEM REGRA | login do P.O. e como confirmar o aprovador (ficha:46) |
| S04-F4 | SEM REGRA | login do P.O. em "aprovada por"; tamanho P/M/G sem critério |
| S04-F5 | AMBÍGUO | tamanho P/M sem critério em dias (triar:54 × triar:87-91) |
| S04-F6 | AMBÍGUO | AFK × HITL sem teste definido para trocar texto (triar:87-88) |
| S04-F7 | AMBÍGUO | bloco 📥 sem status nem modo para atendimento; AT sem id (triar:111) |
| S04-F9 | CONFLITO | pergunta épico × filho dentro do lote (triar:80-81) × confirmação única (triar:137-138) |
| S04-F11 | AMBÍGUO | renumeração não cita cabeçalho da ficha nem links da linha (ficha:11; backlog:46) |
| S04-X2 | AMBÍGUO | ficha de fatia já iniciada: retomar (triar:40-41) × parar (triar:45-46) |
| S04-X4 | CONFLITO | sem MCP: sdd-elm requer MCP (elm:16-17) × similares só com bundle (elm:62-63); No ELM sem valor pendente (ficha:52-53) |
| S04-X8 | SEM REGRA | "não fazer" de item do EWM sem MCP não tem registro |
| S05-F1 | AMBÍGUO | <slug> da branch sem regra de formação (iniciar:91) |
| S05-F2 | CONFLITO | Cobre do status.md: tmpl:9 × ficha:49-50 (C1…Cn são o cobre) |
| S05-F3 | AMBÍGUO | "pesquisa curta" (iniciar:52) sem skill; sdd-plano para pesquisando (iniciar:127); "rapida" × "rápida" |
| S05-F4 | AMBÍGUO | só o <slug> da branch (iniciar:91) |
| S05-F5 | SEM REGRA | papel [REV] × fase implementando: "a fase decide" sem tabela (iniciar:26-27) |
| S05-F6 | AMBÍGUO | "maior prioridade" com número: sentido não definido (iniciar:33; backlog:37) |
| S05-F9 | CONFLITO | planejamento:104 volta ao item 4 (WIP) × iniciar:57-58, 72-74, 83-85 |
| S05-F10 | CONFLITO | Kanban: iniciar:75-76 usa sdd-elm modo sprint × elm:152-153 (sprint-<nn>.md, "ok da sprint") |
| S05-F11 | SEM REGRA | como medir "PR parado" não está escrito (iniciar:80-81) |
| S05-F12 | AMBÍGUO | DoR falha com regra nova: triar (iniciar:46-47) × triar, entrevistar ou fatiar (iniciar:68-69) |
| S05-X7 | AMBÍGUO | fatia só remota: troca de branch sem passo para trazê-la (iniciar:39) |
| S06-F1 | AMBÍGUO | "Pedido por" sem pergunta nem regra de preenchimento (atender:69; atender:33-34) |
| S06-F2 | AMBÍGUO | "resumo sem identificar pessoas" sem critério; .gitignore não verificado (atender:48) |
| S06-F3 | CONFLITO | modo horas "lança e conclui" (atender:56) × "lançar não conclui" (elm:194-195) |
| S06-F4 | AMBÍGUO | **Saída:** com o FT-nnn criado depois do commit do AT; sem passo de retorno (atender:54-58, 92) |
| S06-F6 | SEM REGRA | "atendimentos abertos" é gatilho da description sem passo no corpo (atender:3) |
| S06-F7 | AMBÍGUO | "sob pedido" × "nunca no meio" na mesma regra (atender:101); tabela ## Horas sem autor |
| S06-X1 | SEM REGRA | Kanban / sem sprint aberta: sem onde gravar nem plannedFor (atender:25, 36) |
| S06-X2 | SEM REGRA | sem MCP de banco: sem caminho alternativo nem aviso (atender:44-46) |
| S06-X4 | CONFLITO | regra não decidida: triagem (atender:16-17, 99) × entrevista ou PRD direto (atender:61) |
| S06-X5 | SEM REGRA | AT já aberto que precisa de escrita: sem situação nem destino (atender:70, 99) |
| S07-F2 | CONFLITO | respostas no cabeçalho (entrev:122) × A-1 na seção ## Pedido (atender:73-74) |
| S07-F3 | AMBÍGUO | confirmação do entendimento (entrev:62-63) × modo autônomo sem pessoa (entrev:130-132) |
| S07-F5 | AMBÍGUO | "quais em aberto" sem modo de listagem (entrev:3); "revisa" para decisão em aberto (entrev:77) |
| S07-X1 | SEM REGRA | chamada direta para rápida sem ficha: sem destino (entrev:17-20; triar:64-65) |

Totais: 35 fluxos do plano + 11 casos de borda extras (S04: 4, S05: 2, S06: 4, S07: 1). DETERMINÍSTICOS: S04-F3, S04-F8, S04-F10, S04-X1, S05-F7, S05-F8, S05-X8, S06-F5, S07-F1, S07-F4. Os demais estão na tabela acima.

### Parte 3 — Teste do Quarto Chinês · G3


Executor mecânico: só as regras escritas. Onde a regra não existe, o veredito é SEM REGRA; onde há dois caminhos, AMBÍGUO; onde duas regras mandam coisas diferentes, CONFLITO.

#### Legenda de citações

Base: `powers/sdd/`. Os números de linha seguem o plano (`prd:NN` etc.).

| Abrev. | Arquivo |
|---|---|
| `prd` | skills/sdd-prd/SKILL.md |
| `prd-tpl` | skills/sdd-prd/references/prd-template.md |
| `okf` | skills/sdd-prd/references/okf-elm.md |
| `fatiar` | skills/sdd-fatiar/SKILL.md |
| `backlog.md` | skills/sdd-fatiar/references/backlog.md |
| `plan` | skills/sdd-planejamento/SKILL.md |
| `arquivos` | skills/sdd-planejamento/references/arquivos.md |
| `schema` | skills/sdd-planejamento/assets/equipe.schema.json |
| `elm` | skills/sdd-elm/SKILL.md |
| `mapeamento` | skills/sdd-elm/references/mapeamento.md |
| `steering` | skills/sdd-setup/assets/steering/sdd.md |
| `sdd` | skills/sdd/SKILL.md |
| `triar` | skills/sdd-triar/SKILL.md |
| `rubricas` | skills/sdd-revisar/references/rubricas.md |

Delegado (citado por uma skill testada, não lido nesta parte; tratado como caixa-preta e marcado "delegado"): sdd-entrevistar, sdd-revisor, sdd-pesquisador, sdd-iniciar, sdd-status, sdd-aprender, sdd-atender, elm-setup, elm-ccm, elm-rm, elm-qm, elm-gc, elm-sync.

#### Premissas de ESTADO comuns (P)

Valem em todos os blocos, salvo quando o bloco diz outra coisa.
- Projeto usa ELM (`steering`: "Usa ELM: sim"); publicação de requisitos `na-aprovacao`; backlog no EWM `ao-fatiar`; ET `as-built no merge`; artefatos de produto `direto na branch base`; padrão de commit `FT-<nnn> <verbo> <descrição>`; MCP `elm` disponível na sessão.
- Tipos no `pa_*.json`: épico = Épico; IB = Item de Backlog; HF = História de Usuário; REG = Regra; GL = Termos de Glossário; ET = Especificação Técnica. Tarefas com títulos de `steering`:78.
- `link-types` do `pa_*.json` sem "depende de" (então a dependência vai para a descrição, `elm`:145).
- Campo "Critérios de aceite" existe em `workitem-types[IB].fields`.
- Pontos: P=2, M=3, G=5 (`steering`:77; `mapeamento`:47).
- Membros: ana.souza (P.O., ativa, atende), joao.lima (Dev), rita.melo (Analista).

---

#### Resumo transversal

- Gravação de commit: elm:42 (`<FT|EP> - Publicar no ELM`) diverge de steering:59 (`FT-<nnn> <verbo> <descrição>`) e não cobre épico sem FT nem sprint. Afeta S08-F2, S11-F2, S11-F3, S11-F4, S11-F5.
- Estimativa em horas de [DEV]/[REV]/[VER]/[ATD]: exigida (elm:162, elm:183), sem origem em nenhuma skill. Afeta S11-F5, S11-F7, S11-F9.
- DoR em duas versões: backlog.md:70-75 × arquivos:73-78, ambas gravam `pronta` (backlog.md:63-64). Afeta S09-F5, S10-F2.
- Épico no EWM: triar:78 e prd:43 dizem "só o épico"; elm:133-134 cria Sustentação na mesma chamada. Afeta S11-F3.
- Conclusão da [ESP]: fatiar:81 × elm:220-221. Afeta S09-F1.
- `substituida-por` e `cancelada`: campo (fatiar:96, :99) × texto em `obs` (backlog.md:47-48, :51). Afeta S09-F2, S09-F3.
- Nota ao plano: a "lacuna" de `Planejado para` obrigatório no épico (plano, S11-F3) não está no texto (elm:123 diz "obrigatório em IB e tarefa").

### Parte 3 — Teste do Quarto Chinês · G4


Executor mecânico: cada bloco aplica só o texto das skills, sem conhecimento externo. Onde a regra não existe, o veredito é SEM REGRA; onde admite duas leituras, AMBIGUO; onde duas regras mandam coisas diferentes, CONFLITO.

#### Fontes e convenções

Base: `powers/sdd/skills/`. Abreviações usadas nas citações (`arquivo:linha`):

- `pesq` = sdd-pesquisar/SKILL.md
- `plano` = sdd-plano/SKILL.md
- `tmpl` = sdd-plano/references/plano-templates.md
- `impl` = sdd-implementar/SKILL.md
- `rev` = sdd-revisar/SKILL.md
- `rub` = sdd-revisar/references/rubricas.md
- `stpl` = sdd-iniciar/references/status-template.md
- `iniciar` = sdd-iniciar/SKILL.md
- `loop` = sdd-loop/SKILL.md
- `verif` = sdd-verificar/SKILL.md
- `sdd` = sdd/SKILL.md
- `steer` = sdd-setup/assets/steering/sdd.md, usado só como valores do `.kiro/steering/sdd.md` do projeto (entram como ESTADO, não como regra da skill)

Fora das fontes: `sdd-setup/assets/workflows/*.json` e `sdd-setup/assets/agents/*.json` não são citados pelos SKILL.md de S12–S15, então não entram como regra. Consequência: o que só existe no workflow ou no prompt do agente sai SEM REGRA. O plano cita esses arquivos, mas o teste cego não os consulta.

Premissas de ESTADO comuns: `.kiro/steering/sdd.md` existe com comandos, Git e agentes preenchidos (`steer:88` dá ao `sdd-codificador` os subagentes `sdd-pesquisador` e `sdd-revisor`; `steer:89` dá ao `sdd-revisor` nenhum subagente). Quando o bloco não diz o contrário, o subagente está disponível.

---

#### Resumo geral

| Skill | Fluxos do plano (DET / AMB / CONF / SEM) | Bordas (DET / AMB / CONF / SEM) |
|---|---|---|
| S12 sdd-pesquisar | 6 (3 / 2 / 0 / 1) | 3 (0 / 1 / 1 / 1) |
| S13 sdd-plano | 12 (3 / 6 / 1 / 2) | 4 (0 / 1 / 1 / 2) |
| S14 sdd-implementar | 12 (4 / 5 / 3 / 0) | 4 (1 / 1 / 1 / 1) |
| S15 sdd-revisar | 5 (2 / 2 / 1 / 0) | 4 (0 / 0 / 2 / 2) |

Total: 50 blocos (35 fluxos do plano + 15 bordas). Não-DETERMINISTIC: 37 de 50.

### Parte 3 — Teste do Quarto Chinês · G5


Executor mecânico: aplicou só as regras escritas. Fontes: plano `p2/G5.md` (lista de fluxos) e as regras em `powers/sdd/skills/` (SKILL.md, references e assets citados). Somente leitura; nada no repositório foi alterado.

Legenda (caminhos relativos a `powers/sdd/skills/`, salvo indicação):
- SV = sdd-verificar/SKILL.md · CT = sdd-verificar/references/ct-csv.md
- SC = sdd-consolidar/SKILL.md · SA = sdd-aprender/SKILL.md · SL = sdd-loop/SKILL.md
- SI = sdd-implementar/SKILL.md · IN = sdd-iniciar/SKILL.md · ST = sdd-iniciar/references/status-template.md
- SE = sdd-elm/SKILL.md · SS = sdd-status/SKILL.md · SDD = sdd/SKILL.md
- STEER = sdd-setup/assets/steering/sdd.md · AG-V / AG-O = sdd-setup/assets/agents/sdd-verificador.json / sdd-orquestrador.json · RM = powers/sdd/README.md

Notas transversais (aparecem em vários blocos):
- Fonte do "login" de responsável: CT:22 pede "login do ELM"; IN:102 diz `whoami`; SS:35-36 diz `git config user.name` cruzado com `equipe.json`. Nenhuma skill do fluxo escolhe um.
- Formato de fase bloqueada: SV:84 e SL:105-106 escrevem só `bloqueada`; ST:19 escreve `bloqueada (de: <fase>)` com motivo e pergunta.
- `ELM pendente`: SS:22 lista pendências "sem `ELM feito:` correspondente", mas nenhuma skill define como gravar `ELM feito:`.

---

#### Resumo geral

Blocos: 27 (15 fluxos do plano + 12 bordas acrescentadas: S16 4, S17 3, S18 3, S19 2). Vereditos não-DETERMINÍSTICOS: 25. DETERMINÍSTICOS: 2 (S16-F2, S17-F4).

### Parte 4 — Persistência e artefatos · G1


Base: `powers/sdd/`. Citações `arquivo:linha`; `SETUP` = `skills/sdd-setup/SKILL.md`, `STATUS` = `skills/sdd-status/SKILL.md`,
`TPL-steering` = `sdd-setup/assets/steering/sdd.md`, `agentes.md` = `sdd-setup/references/agentes.md`.
Somente leitura no repositório. Validações rodadas fora do repositório:
`python3 -m json.tool` em 6 agentes, `hooks/sdd.json`, 2 workflows e `toolkit.schema.json` = todos OK; `sh -n scripts/http.sh` = OK.
Os blocos V2 (`toolsSettings.write`) e V3 (`permissions fs_write`) dos 5 agentes que têm escrita estão em espelho (allow e deny idênticos).
Os templates só são JSON/sh válidos **com os placeholders** (`{{POWER}}` ×29, `{{PRODUTO}}` ×10, `{{SKILLS_EXTRAS}}` ×6, `{{GLOSSARIO}}` ×3,
`{{ADR}}` ×3, `{{SUBAGENTES}}` ×2, `{{COMPILAR}}`/`{{TESTES}}` ×1, `{{URL_TESTE}}` ×1); a validade depois da substituição só é conferida no Passo 9.

Regras gerais de persistência que valem para todo o S02 (citadas nas linhas da tabela como "geral"):
- Quem executa: nenhum agente `sdd-*` carrega a `sdd-setup` (`resources` dos 6 JSON); roda no agente padrão do Kiro, sem allowlist. Se a pessoa estiver
  com `sdd-codificador` ativo, a escrita em `.kiro/steering|agents|hooks|workflows|sdd` e na pasta do produto é **negada** (`sdd-codificador.json` deny);
  com `sdd-produto`, só `{{PRODUTO}}`, glossário, ADRs, `decisoes.md` e `.kiro/local/atendimentos/` são graváveis. A skill não diz "rode com o agente padrão".
- Raiz: `git rev-parse --show-toplevel` (SETUP:31); todos os caminhos gravados são relativos à raiz (projeto) ou ao home (power/usuário) (SETUP:40-43).
- Gravação: só depois do resumo e do "ok" do Passo 8 (SETUP:26, 248-258); o Kiro ainda pede confirmação por arquivo em `.kiro/agents/`, `.kiro/hooks/`,
  `.kiro/workflows/` (SETUP:261-262; agentes.md:89-92). Commit: apenas "sugira" (SETUP:291-292), sem branch, sem autor, sem push.
- Falha de escrita (diretório inexistente, sem permissão, pessoa nega a confirmação do Kiro, disco/FS somente leitura, escrita parcial): **NÃO ESPECIFICADO**
  em todo o SETUP. O que existe: sem git → avisa (SETUP:31); power não achado → pergunta (SETUP:35-36); workspace não confiável → avisa (SETUP:288-289);
  Passo 9 detecta resultado inválido, não falha de escrita.

---

#### Achados de persistência

1. **Setup não prescreve onde commitar e conflita com a regra "produto só na base".** `sdd-setup/SKILL.md:291-292` só "sugere o commit", sem branch, sem quem, sem push, enquanto
   `sdd-fatiar/references/backlog.md:6-9` e `TPL-steering:61` exigem que `<produto>/backlog.md` e demais artefatos de produto nunca sejam gravados em branch de fatia
   (direto na base ou "PR curto para a base"). A setup roda onde a pessoa estiver; também não diz que `.kiro/steering/sdd.md` e `.kiro/agents/` precisam chegar à base para
   existirem nas branches criadas por `sdd-iniciar` a partir de `origin/<base>` (`sdd-iniciar/SKILL.md:89-90`).
2. **Migração sdd2: o mv "sem mudar o conteúdo" produz arquivos quebrados e o momento é incerto.** `sdd-setup/SKILL.md:55-56,58` renomeia hook, workflows e `http.sh` sem alterar conteúdo, mas
   os workflows `sdd2-*` apontam para agentes `sdd2-*` que a mesma regra remove (SETUP:54), e SETUP:47-48 manda regerar tudo dos templates. Falta dizer: quando rodam `git mv`/`git rm`
   (SETUP:50 × 26), o que fazer com árvore suja, destino existente ou estado parcial; e SETUP:57 × 119-121 (se `.kiro/produto/backlog.md` já existe, a "pasta do produto" é a própria `.kiro/produto/`).
   Mesmo vazio de momento/segurança na migração v1 (`SETUP:64-65`).
3. **Fechar a sessão (`sdd-status/SKILL.md:86-96`) escreve sem alvo, dono nem branch definidos.** Falta: como achar a fatia (STATUS:91), branch/worktree do commit, tratamento de `status.md` ausente
   (branch base, sessão de produto, P3 S03-E2 confirmado) e de trilha direta sem `tasks.md` (STATUS:93 × `sdd-iniciar/SKILL.md:53`), e o formato da linha do Histórico
   (`status-template.md:42`, não citado). Só o `sdd-orquestrador` carrega a skill (`orquestrador.json:19`); com `sdd-produto` a escrita é negada
   (`sdd-produto.json` fs_write só `decisoes.md`), e o codificador não tem a skill. **Refutação da P3:** `.kiro/specs/FT-031-cadastro/` (P3 S03-F4) usa `<ft>` maiúsculo, contra a convenção
   minúscula (`sdd-iniciar/SKILL.md:91`, workflow `sdd-planejar-fatia` passo `pesquisa`, `http.sh:8`); a P3 inventou a caixa.
4. **Regras de verificação dos arquivos gerados são inexequíveis ou mal escopadas.** `SETUP:232` ("nada de `<…>` sobrando") não pode valer para o `sdd.md`, cujo template tem `<ft>`, `<origem>/<id>`,
   `<nn>`, `FT-<nnn>`, `L-<nnn>` fixos (TPL-steering:14,17,39,78,97-98); `SETUP:266` ("nenhum `{{…}}`") só vale para agentes: os workflows trazem `{{fatia}}` legítimo; `{{COMPILAR}}`, `{{TESTES}}`
   e `{{URL_TESTE}}` não aparecem em `agentes.md`, e o "comandos" dos agentes (SETUP:236; agentes.md:51) não tem placeholder/âncora nos 6 templates; não há instrução de escape JSON
   para comandos substituídos (aspas, `\` do Windows em `hooks/sdd.json:10`). `{{GLOSSARIO}}`/`{{ADR}}` removidos podem deixar vírgula pendente (SETUP:124-125).
5. **A setup grava fora do escopo que ela mesma declara e antes do "Gravar?".** `SETUP:26` ("nada é gravado antes do Passo 8") e `SETUP:299-300` ("não altere nada fora de `.kiro/`, produto, glossário/ADRs, `.gitignore`") contradizem
   `~/.kiro/settings/mcp.json` (SETUP:152-153), `kiro-cli settings --workspace` (SETUP:286-287), exclusões em tsconfig/jest/lint (SETUP:272-273), a `elm-setup` (SETUP:130) e a execução de build/testes (SETUP:94-95).
   Nenhum desses entra no resumo do Passo 8 (SETUP:256-257) nem no commit (SETUP:291-292).
6. **Divergências template × texto da skill no `sdd.md`/agentes.** Linha do orquestrador com MCP `—` (TPL-steering:91) × MCP `elm` marcado nele (SETUP:199-200; TPL-steering:71; agentes.md:54);
   subagentes do `sdd-produto` presentes no template e no JSON (TPL-steering:86; `sdd-produto.json` tools `subagent/sdd-pesquisador`, `subagent/sdd-revisor`) × SETUP:204 "só codificador e orquestrador";
   tabela do Passo 8 (SETUP:254) com colunas diferentes da do `sdd.md`; `<x.y.z>`/`<AAAA-MM-DD>` sem fonte (TPL-steering:19; versão disponível em `plugin.json` e `metadata.version`).
7. **Backlog mínimo e pasta vazia.** `SETUP:241-242` cria `backlog.md` sem `## Fatias — sem épico` nem cabeçalho de colunas (formato em `sdd-fatiar/references/backlog.md:13-35`); `<produto>/planejamento/`
   (SETUP:243) é diretório vazio que o git não versiona, sem `.gitkeep`.
8. **Falha de escrita não é tratada em nenhum dos três SKILL.md.** Diretório inexistente, sem permissão, recusa da confirmação por arquivo do Kiro (SETUP:261-262), escrita parcial, árvore suja antes de `git mv`/`git rm`,
   `.gitignore` ausente: NÃO ESPECIFICADO. Quem executa a setup (agente padrão) também não é dito; com `sdd-codificador` ativo as escritas em `.kiro/{steering,agents,hooks,workflows,sdd}` seriam negadas.
9. **S01 e tabela "Onde as coisas moram" (`sdd/SKILL.md:101-109`)** omitem `<produto>/fatias/FT-<nnn>-<slug>.md` (`sdd-triar/SKILL.md:92`), `roadmap.md`, `planejamento/equipe.json|acordos.md|sprints/` e `.kiro/local/loop-*.md` / `.kiro/local/wf/`,
   que `sdd-status` (STATUS:25,28,34,35) e os agentes (`orquestrador.json`, `revisor.json`) leem/gravam. Sem ajuste o leitor não acha onde esses arquivos moram.
10. **`git fetch` do painel (STATUS:17) escreve em `.git`** (refs remotas, `FETCH_HEAD`), contra "não altera arquivo, branch nem ELM" (STATUS:12). Efetivamente permitido no orquestrador (`git fetch*`), mas o texto da skill não o ressalva.

### Parte 4 — Persistência e artefatos · G2


Convenções: `triar:NN`, `iniciar:NN`, `atender:NN`, `entrev:NN` = SKILL.md; `ficha:NN` = sdd-triar/references/ficha.md; `tmpl:NN` = sdd-iniciar/references/status-template.md; `backlog:NN` = sdd-fatiar/references/backlog.md; `steer:NN` = sdd-setup/assets/steering/sdd.md; `plt:NN` = sdd-plano/references/plano-templates.md; `arq:NN` = sdd-planejamento/references/arquivos.md; `prod.json:NN` / `orq.json:NN` = sdd-setup/assets/agents/sdd-produto.json / sdd-orquestrador.json.
`<produto>` = "Pasta do produto" do `sdd.md` (padrão `.kiro/planejamento`, setup SKILL:120-122). Exemplos de formato montados em `(rascunho local) tmp/p4/ex/` (`.config.kiro` validado como JSON de uma linha; linha de backlog sem épico = 14 colunas = cabeçalho de backlog:33).

Permissões de escrita (resumo verificado nos JSON):
- `sdd-produto` (tem triar, entrevistar, atender; NÃO tem iniciar): grava `{{PRODUTO}}/**`, `{{GLOSSARIO}}`, `{{ADR}}/**`, `.kiro/specs/*/decisoes.md`, `.kiro/local/wt/*/.kiro/specs/*/decisoes.md`, `.kiro/local/atendimentos/**` (prod.json:40-47; espelho 229-240). **Não** grava `.kiro/specs/*/status.md` nem `.config.kiro`. Shell: `git add/commit/fetch/pull --ff-only/switch` permitidos (prod.json:70-74); `git push` **negado** (prod.json:112; steer:61 "entrega o comando"); `stash/rebase/merge` negados.
- `sdd-orquestrador` (único com `sdd-iniciar`, orq.json:18): grava `.kiro/specs/**`, `.kiro/local/wt/*/.kiro/specs/**`, `.kiro/local/loop-*.md` (orq.json:39-44); **não** grava `{{PRODUTO}}/**` fora das worktrees nem o glossário. Shell permitido: `git add/commit/fetch/worktree add/uuidgen` (orq.json:57-82); **não há `git switch`, `git pull`, `whoami`**; `git push *` é `ask` (orq.json:226-232).
- `sdd-codificador`: `./**` menos `{{PRODUTO}}/**` e `.kiro/steering|agents|hooks|workflows|sdd/**`; não tem as quatro skills.
- `sdd-pesquisador`: só `research.md`.

---

#### Confirmações / refutações de afirmações de arquivo da Parte 3
- CONFIRMA: S05-F2 (Cobre × ficha), S05-F3 (`rapida` × `rápida`), S04-F11 (renumeração incompleta), S04-X2, S06-F1 (`Pedido por`), S06-F4 (Saída tardia), S06-F7 (`## Horas` sem autor), S07-F2 (cabeçalho × `## Pedido`), S07-F3 (autônomo sem commit/confirmação), S07-X1.
- CORRIGE: S04-F3/F4 "push com sim" — `sdd-produto` não pode `git push` (prod.json:112) e a skill não diz "entregue o comando"; S06-F2 "commit só do registro" — não existe em atender; S06 "sprints/sprint-03.md" — caminho real `<produto>/planejamento/sprints/sprint-03.md` (arq:104); S06-F2 ".gitignore não verificado" — o setup garante `.kiro/local/` (setup:246), só atender não confere; S05-F1/F2 omitem que o único agente com a skill não tem `git switch -c` no allowlist (orq.json:57-82) e que `.config.kiro` não está no commit (iniciar:115); vários blocos S04/S06 omitem o prefixo `<produto>/`.
- NÃO COBERTO pela P3: backlog:79 (nunca renumerado) × triar:106; glossário fora do commit da triagem (triar:101); ficha órfã por queda antes do Passo 3 (triar:62/101); ordem `git fetch` × leitura de `origin/<base>` (iniciar:83-85 × 94); permissões do `sdd-orquestrador` para iniciar; README/AT sem base/pull/conflito de id.

### Parte 4 — Persistência e artefatos · G3


Base das citações: `powers/sdd/`. `prd:NN`, `prd-tpl:NN`, `okf:NN`, `fatiar:NN`, `backlog.md:NN`, `plan:NN`, `arquivos:NN`, `elm:NN`, `mapeamento:NN`, `steering:NN` (= sdd-setup/assets/steering/sdd.md), `setup:NN` (= sdd-setup/SKILL.md), `entrev:NN`, `atender:NN`, `status:NN` como na Parte 2/3. `ag-prod:NN` e `ag-cod:NN` = sdd-setup/assets/agents/sdd-produto.json e sdd-codificador.json (número da linha do arquivo).

`<produto>` = "Pasta do produto" do `sdd.md` (steering:26; padrão `.kiro/planejamento`, setup:119-121). A Parte 3 escreveu os caminhos sem esse prefixo (`epicos/EP-03-…`, `planejamento/…`): é abreviação, não divergência, salvo onde marcado.

#### Chaves usadas na coluna "Inacessível" (repetidas em quase toda linha)

- **I-git** — árvore suja / `git pull --ff-only` falha / HEAD numa branch de fatia: **NÃO ESPECIFICADO** em `sdd-prd` (nenhum passo de "trocar para a base", nem de pull) e em `sdd-elm`. `sdd-fatiar` (backlog.md:82) manda `git switch <base>` + `pull --ff-only` sem tratar falha nem árvore suja, e **sem pedir "sim"** (steering:13 e sdd/SKILL:120 exigem "sim" para troca de branch). `sdd-planejamento` (arquivos:3) cobre só a falha do pull ("peça à pessoa que a atualize"). Contraste: `sdd-triar` (triar:26-28), `sdd-consolidar` (consolidar:17-19) e `sdd-iniciar` (iniciar:39-40) mandam "avisar e parar" com árvore suja.
- **I-perm** — escrita negada pelo agente / pasta inexistente: **NÃO ESPECIFICADO** nas 4 skills (nenhuma diz "pare e avise", nem "crie a pasta"). Conferência das permissões: `sdd-produto` tem `fs_write` allow `{{PRODUTO}}/**`, `{{GLOSSARIO}}`, `{{ADR}}/**`, `.kiro/specs/*/decisoes.md`, `.kiro/local/wt/*/.kiro/specs/*/decisoes.md`, `.kiro/local/atendimentos/**` (ag-prod:41-46 e 232-237, as duas listas são idênticas) → cobre tudo sob `<produto>/` e o glossário; **não cobre** `.kiro/specs/<ft>-<slug>/{elm/**, status.md, verificacao.md}`. `sdd-codificador` tem allow `./**` e **deny `{{PRODUTO}}/**`** (ag-cod:44-45, 246-247) → não grava nada sob `<produto>/` (backlog.md, elm/ do épico, sprint-<nn>.md), mas grava em `.kiro/specs/**`. Pasta `<produto>/` e `backlog.md` mínimo são criados pela setup (setup:241-243: só `backlog.md`, `planejamento/` vazia, `aprendizado/`, `atendimentos/`); `epicos/`, `epicos/<EP>-<slug>/elm/`, `planejamento/sprints/` **não** são criadas por ninguém de forma explícita (criação implícita ao gravar).
- **I-elm** — sem MCP ou falha de escrita no ELM: elm:23-25 (`ELM pendente: <modo> <alvo>` no Histórico do `status.md` ou no rodapé do PRD; "o ELM nunca trava o fluxo"). Ver achado sobre a baixa da pendência (`ELM feito:`).
- **Quem grava/push (comum)**: quem escreve é o agente `sdd-produto` (PRD, fatiar, planejamento, sdd-elm em sessão de produto); ele tem `git add/commit/switch/pull --ff-only` e **nega `git push`** (ag-prod:70-74, 112); push/PR só com "sim" e é a pessoa quem executa (steering:61). O padrão que a setup grava em "Artefatos de produto" é **`PR curto para a base`** (setup:115), não "direto na base".

---

#### Achados de persistência

1. **Branch de trabalho, árvore suja e "PR curto" não são tratados em `sdd-prd`, `sdd-elm` e (parcialmente) `sdd-fatiar`/`sdd-planejamento`.**
   `prd:16-50` grava `prd.md`/`decisoes.md`/`elm/` desde o Passo 1 sem mandar estar na base (`sdd-triar` manda: triar:26-28); o commit só vem no GATE (prd:120-122), então o rascunho passa dias não commitado na branch corrente, e `triar/consolidar/iniciar` param com árvore suja (triar:27-28, consolidar:18-19, iniciar:39-40). `backlog.md:82` faz `git switch <base>` sem pedir "sim" (contra steering:13 e sdd/SKILL:120) e sem ramo para falha. O padrão gravado pela setup é "PR curto para a base" (setup:115), mas nenhuma skill diz o nome da branch do PR curto nem como os commits encadeados (GATE do PRD, `sdd-elm` requisitos, `sdd-fatiar`) ficam visíveis uns para os outros: `fatiar` faz `git switch <base>` + `pull` e não encontrará o `prd.md` `aprovado` que está numa branch de PR ainda não mergeada (fatiar:16, backlog.md:82). O `sdd-produto` pode criar a branch (`git switch .*`, ag-prod:74) e não pode dar push (ag-prod:112).

2. **`equipe.json`: o roteiro do modo inicial não coleta quatro campos que o schema exige.** Validado (jsonschema 4.26, Draft 2020-12): o exemplo de arquivos:14-43 passa; um JSON só com o que plan:29-33 pergunta falha por falta de `projeto.nome`, `projeto.duracao-sprint-semanas`, `projeto.inicio` (a P3 viu) e `membros[].ativo` (`ativo` a P3 não viu); `projeto.historico` também é obrigatório (aceita `[]`, mas nada manda gravar vazio). Kanban continua exigindo `duracao-sprint-semanas` e `inicio`. O schema não impõe "revisão + especificação ≤ horas-semana" (arquivos:49; 9+9 em 10 h passa) — "valide antes de mostrar" (plan:33) não pega isso, e o agente `sdd-produto` não tem ferramenta de validação no shell (ag-prod:61-76). O modo inicial também não tem commit (plan:25 só "ok"; commit só em plan:81-82).

3. **Gravação dos ids de tarefa em coluna que não existe, e `sprint-<nn>.md` sem nome definido.** `elm:174-175` e `plan:83-84` mandam gravar/`pendente` na coluna "Tarefa ELM" do `sprint-<nn>.md`, mas essa coluna só existe nas tabelas Especificação e Atendimento (arquivos:122, 130); a tabela Fatias (arquivos:115) não a tem — os ids de `[DEV][REV][VER]` só cabem em `backlog.md` `elm` (backlog.md:53). A P3 (S10-F2/S11-F5) afirma o contrário. `plan:100-101` sugere gravar revisor/verificador "no backlog.md", que não tem essas colunas (backlog.md:27). O nome do arquivo é `sprint-<nn>.md` sem regra de padding; a P3 usou `sprint-003.md` e `iniciar:73`/`status:31` comparam com o número da coluna `sprint`. A contradição elm:174-175 × iniciar:112-114 que a P3 apontou tem explicação fora das skills: `sdd-codificador` nega `{{PRODUTO}}/**` (ag-cod:44, 246) e `sdd-elm` está nos dois agentes (ag-cod:17) sem saber disso.

4. **Falha parcial na publicação: a regra de idempotência cobre requisitos, mas não o restante.** Coberto (elm:31-37, 41-44): write-back por item (`resource`, `id`, `sources`, `log.md`) e busca de publicação interrompida por `rm_search_requirements(text=<título>)` filtrado por tipo/pasta, com "é ele?". Não coberto: (a) o commit é só no fim (elm:42), então uma interrupção deixa `elm/*.md` modificados e não commitados (ver achado 1); (b) a busca de EWM é "título com `[FT-031]`" mas as tarefas se chamam `[DEV] FT-031 Implementar`, `[ESP] EP-05 …`, `[ATD] AT-013 …` (steering:78), que não casam — tarefa criada e não gravada será duplicada no rerun; (c) `ELM pendente:` no rodapé do PRD/status.md nunca é baixado: a convenção `ELM feito:` existe só em iniciar/references/status-template.md:40 e é lida por status:22, mas nenhuma das quatro skills manda escrevê-la; (d) fatiar:79 comita antes de fatiar:83 gravar o `ELM pendente: lançar …` no rodapé, que fica sem commit.

5. **Formato dos arquivos OKF e do `prd.md` com defeitos de especificação.** `verified` aparece como objeto `{by, at}` (prd:119, okf:61) e como lista (prd:132, okf:70 "a lista `verified` acumula"); o 1º GATE não diz qual gravar. `title`/`description` com `: ` quebram o frontmatter (validado: "mapping values are not allowed here") e okf não manda aspas; a P11 só detecta depois. Ao alterar um conceito do bundle (prd:85-86) não se diz se o arquivo é renomeado de `<id>-<slug>.md` para `HF-nn-<slug>.md` (okf:29) com Concept ID "que não muda" (okf:27). O rodapé do `prd.md` (prd-tpl:80) não tem campo para "quem aprovou" (prd:118). `backlog.md` ganha seção `## Fatias — <EP> <título>` (backlog.md:25, 37): a P3 omitiu o título; `cobre` muda de `HF-01 · 1.1, 1.2` para `HF-01#1.1, HF-01#1.2` (inclusive faixas `2.1–2.3`) sem regra de conversão; `substituida-por` é campo em fatiar:96 e texto em `obs` em backlog.md:48/51; "Próximos ids" não é atualizado por `sdd-fatiar`.

##### Afirmações da Parte 3 sobre arquivos que esta verificação refuta ou corrige

- S09-F3: "fatiar:99 só diz 'unir cobertura e dependências'" — fatiar:99 não diz isso; só "a que some fica `cancelada` com `motivo`".
- S09-F1: cabeçalho `## Fatias — EP-03` — o template exige `## Fatias — <EP> <título>` (backlog.md:25, 37).
- S10-F2 / S11-F5: ids de tarefa em "coluna Tarefa ELM do sprint-003.md" — só para `[ESP]`/`[ATD]`; `[DEV][REV][VER]` vão no `elm` do backlog (arquivos:115, 122, 130; backlog.md:53).
- S10-F2: arquivo `sprint-003.md` — padding não está escrito (`sprint-<nn>.md`).
- S10-F5: DETERMINÍSTICO com "ok + commit" — o texto de Review não prescreve nenhum dos dois (inferidos de plan:25 e steering:61).
- S10-F6: "coluna `sprint` das migradas fica AMBÍGUA" — se entram na nova sprint pelo modo sprint (plan:124), `sprint` é regravada no passo 7 (plan:81).
- S10-F1: "SEM REGRA para nome/início/duração" confere; falta acrescentar `ativo` e `historico` (validação por schema).
- S11-F3: CONFLITO "só o épico" × Sustentação — o passo 2 é condicional e separado (elm:133-134); o risco real é a falta de `<FT|EP>` para SUS na mensagem de commit (elm:42).
- S11-F2: "glossário sem formato" — formato existe em entrev:84-86 (`GL 3120`), só não é citado por `sdd-elm`.
- S11-F6: "sprint-004.md / backlog.md conforme S11-F5" — a virada não grava arquivo (elm:176-178).
- S10-S09 estado da P3: `historico` com sprint 3 enquanto se planeja a sprint 3 (S10-F2), e datas (`inicio 2026-10-06` + 2 sprints de 2 semanas = sprint 3 começa em 2026-11-03, mas a P3 usa 2026-10-15/10-28 dentro da sprint 3): cenário inconsistente com schema:31 ("uma entrada por sprint fechada").

Arquivos de apoio da validação (fora do repositório): `(rascunho local) tmp/p4/work/v.py` (schema) e `y.py` (frontmatter OKF).

### Parte 4 — Persistência e artefatos · G4


Base: `powers/sdd/skills/`. Citações `arquivo:linha` relativas a essa pasta. Abreviações: `pesq`=sdd-pesquisar/SKILL.md · `plano`=sdd-plano/SKILL.md · `tmpl`=sdd-plano/references/plano-templates.md · `impl`=sdd-implementar/SKILL.md · `rev`=sdd-revisar/SKILL.md · `rub`=sdd-revisar/references/rubricas.md · `stpl`=sdd-iniciar/references/status-template.md · `ini`=sdd-iniciar/SKILL.md · `loop`=sdd-loop/SKILL.md · `agentes.md`=sdd-setup/references/agentes.md · `A:<papel>`=sdd-setup/assets/agents/sdd-<papel>.json · `wf-plan`/`wf-ent`=sdd-setup/assets/workflows/sdd-planejar-fatia / sdd-entregar-fatia.workflow.json.

Convenções de caminho: `P` = `.kiro/specs/<ft>-<slug>/` (relativo à raiz do projeto, na branch da fatia; `<ft>` minúsculo, `ini:91`); `PW` = `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/` (pasta da fatia dentro da worktree do loop, `loop:62-76,96`).

Método: li os 4 SKILL.md, `tmpl`, `rub`, `stpl`, `loop`, `ini`, steering `sdd.md`, os 6 agentes e os 2 workflows. Casei cada caminho prescrito contra `fs_write` allow/deny dos agentes com um matcher de glob (`*` = um segmento, `**` = recursivo; script em `(rascunho local) tmp/p4/chk.py`); amostras de `.config.kiro`, `plano.json` e `codigo.json` parseiam como JSON válido (chaves `specId/workflowType/specType`, `resultado`, `veredito`). Permissões resumidas:

- `sdd-pesquisador` grava **só** `P/research.md` e `PW/research.md` (A:pesquisador `write.allowedPaths`); sem `git add/commit/push` (deny). Nunca `status.md` — coerente com `pesq:85-87`.
- `sdd-revisor` grava `P|PW/revisao-*.md`, `P|PW/analise-*.md`, `<produto>/epicos/*/revisao-*.md`, `.kiro/local/wf/*/plano.json|codigo.json` (A:revisor); nada de `status.md`/`tasks.md`; sem git de escrita. Coerente com `rev:20-21,56-58`.
- `sdd-codificador` grava `./**` (inclui `P`, `PW`, `.config.kiro`, código) **menos** `.kiro/agents|hooks|workflows|steering`, `<produto>/**`, `.kiro/local/wf/**`, `.git`; `git add`/`git commit`/`fetch`/`pull --ff-only`/`uuidgen` liberados; `git push` negado (A:codificador). Subagentes: só `sdd-pesquisador` e `sdd-revisor`.
- `sdd-orquestrador` grava `P` (`.kiro/specs/**`), `.kiro/local/wt/*/**` (menos `.kiro/{agents,hooks,workflows,steering,sdd}` e produto) e `.kiro/local/loop-*.md`; commit liberado; push/PR `ask`.
- `sdd-verificador` grava `verificacao.md`, `CT.csv`, `status.md`, `evidencias/**`, `massa/**` (P e PW); sem git de escrita.
- Nenhum agente do G4 tem regra para "pasta/arquivo inexistente" nem para "escrita negada" — e nenhuma das 4 skills trata isso (grep `permiss|negad|inexist|não existe|não consegu` em pesq, plano, impl, rev, tmpl, rub: zero ocorrências sobre escrita). Em todas as linhas abaixo, "NÃO ESPECIFICADO" nessa coluna significa exatamente isso.

---

#### Cinco achados mais sérios

1. **Estado nunca commitado e Passo 0 que não o aceita** (`impl:20-22` × `impl:46-47,64-65` × `plano:78,81-85` × `ini:78-79` × `wf-ent`). `status.md` fica sempre sujo depois do commit da tarefa; plano em "análise basta", rápida sem GATE e `plano-em-revisao` não são commitados (`plano:85` só no "Aprovado"); `research.md`, `requirements/design/tasks/.config.kiro/status.md` não estão nas exceções do Passo 0. No `sdd-entregar-fatia` a 2ª iteração do `construir` para por "árvore suja". O WIP que `ini:78-79` conta "nas branches" não enxerga `plano-em-revisao` nem `aceita`.
2. **Workflow `sdd-planejar-fatia` não fecha o plano** (`wf-plan` `ajustar`: "OK sem GATE pendente → nada mais"). Nenhum `fase: implementando`, nenhum commit; `plano:82` diz "quem conduz grava", `impl:12-13` exige `implementando`. Com "análise basta" ou rápida GATE `não`, o `sdd-entregar-fatia` não tem como começar.
3. **Relatórios de revisão/verificação não chegam ao PR no HITL** (`impl:21-22,117`, `rev:20`, A:revisor/A:verificador sem git). `revisao-codigo-<N>.md`, `analise-plano-<N>.md`, `verificacao.md`, `CT.csv`, `evidencias/` só são commitados na próxima sessão ou pelo orquestrador; o PR (`impl:108`) cita arquivos que podem não estar na branch e o `CT.csv` (`sdd-consolidar/SKILL.md:47`) não chega à base. `revisao-prd-<N>.md` fica fora do commit do GATE do PRD (`sdd-prd/SKILL.md:119-122`).
4. **Numeração `<N>` do relatório sem definição única** (`rev:56` × `plano:60` × `impl:75,82` × `loop:93` × `wf-plan`/`wf-ent`). Quem incrementa antes e quem incrementa depois produzem `<N>` diferentes; "zera as rodadas" (`impl:82`) manda o revisor reescrever `revisao-codigo-1.md`, que já existe, e nenhuma regra diz o que fazer com arquivo existente (sobrescrita silenciosa). Vale também para `revisao-prd-<N>` (épico sem contador).
5. **Nenhuma skill do G4 trata diretório inexistente nem escrita negada** (grep sem ocorrências). Agravantes: `.kiro/local/wf/<id>/` (`<id>` indefinido, ninguém cria a pasta, `FT-031` × `ft-031`); revisor chamado por subagente do codificador herda o deny de `.kiro/local/wf/**` e não grava o JSON de veredito; `AMBIENTE` (`impl:70-71`) não tem campo no `status.md`; direta tem `rev:30` (conversa) × `rev:54-58` (arquivo) com o agente permitido a gravar. Também: `tmpl:170-171`×`plano:50` (revisão no checkpoint) e tarefa opcional `[ ]*` que nunca vira `[x]` (`tmpl:174` × `impl:24,67`).

##### Confirmações e refutações da Parte 3 (arquivos)

- S12-F1: **refutado** em parte — `stpl:42` não é exemplo da linha da pesquisa (é a da `sdd-iniciar`); não há modelo.
- S12-F3 (`PW/research.md`, commit do orquestrador): **confirmado** (A:pesquisador allow + `loop:92-94`).
- S12-F6 (SEM REGRA): **refutado para o agente** (A:pesquisador prompt manda não gravar; allowlist só tem `research.md`); lacuna só na skill.
- S13-F11 / S14-F10 (CONFLITO): **confirmados**; o A:codificador tem `subagent/sdd-revisor` e o prompt dele não limita aos Passos 2–3/0–2; só `loop:84,87` e os workflows.
- S13-F2/F4 (commit/fase indefinidos): **confirmados e agravados** pelo `wf-plan` `ajustar` ("nada mais").
- S14-B1 (CONFLITO `status.md` sujo): **confirmado**; agravado no `wf-ent`.
- S14-F12 / S15-F4 (CONFLITO relatório): **confirmado**; A:revisor tem permissão para gravar `P/revisao-*.md`, então a regra "só na conversa" é escolha, não restrição.
- S15-F2 e S15-F3 (DETERMINISTIC com `…-1.md`): **válidos só** se o revisor usa a rodada recebida; com "próxima rodada" lida do contador pós-incremento o nome sai `-2` (DIVERGENTE potencial).
- S14-B3 (AMBIENTE SEM REGRA): **confirmado**, e o template `stpl` não tem local para o registro.
- S12-F2 / S13-B1 / S13-B2 / S13-F12 / S15-B3: **confirmados** (nenhuma regra em skills, agentes ou workflows).

### Parte 4 — Persistência e artefatos · G5


Base: `powers/sdd/skills/` (somente leitura). Siglas: SV/CT/SC/SA/SL/SI/SE/ST/STEER como na Parte 3; AG-V = `sdd-setup/assets/agents/sdd-verificador.json`, AG-O = `sdd-orquestrador.json`, AG-P = `sdd-produto.json`, AG-C = `sdd-codificador.json`; BK = `sdd-fatiar/references/backlog.md`; AGR = `sdd-setup/references/agentes.md`.
Validação feita em `tmp/p4/ct-sample.csv` (CT.csv de exemplo lido com `python3 csv`, `delimiter=';'`): ver S16.

Premissas verificadas que valem para os quatro blocos:
- **Nenhum agente do power carrega `sdd-consolidar` nem `sdd-aprender`** (resources: AG-P = triar, entrevistar, prd, fatiar, planejamento, atender, elm; AG-C = plano, implementar, elm; AG-O = loop, iniciar, status, elm). Logo as duas skills só rodam na sessão da pessoa (agente padrão do Kiro). AG-P escreve só `{{PRODUTO}}/**`, glossário, ADR, `decisoes.md`, `.kiro/local/atendimentos/**` (AG-P write.allowedPaths): **não** grava `status.md` de fatia nem `.kiro/steering/sdd.md`; AG-C nega `**/.kiro/steering/**` e `{{PRODUTO}}/**` (AG-C deniedPaths). Nenhuma skill diz isso.
- O verificador (AG-V:8, 105-107, 183-187) **não commita, não dá `git add`, não dá push, não cria worktree**; escreve só nos 11 padrões de AG-V:33-43 (espelhados em AG-V:227-237). O orquestrador (AG-O:78-80, 171-173) faz `git add`, `git commit`, `git fetch`, `git worktree add .kiro/local/wt/*`; `push`/`gh pr create` com `ask` (AG-O:228); `git worktree remove` negado em todos os agentes (AG-V:81, AG-O:95).
- `.kiro/local/` é ignorado pelo git (`sdd-setup/SKILL.md:246`, "se faltar"); `.kiro/sdd/` e `.kiro/steering/` são versionados (AG-O nega escrita neles dentro da worktree, AG-O:45-52).
- Artefatos de produto: STEER:61 (`direto na branch base | PR curto para a base`); o padrão da setup é **PR curto** (`sdd-setup/SKILL.md:115`).

---

#### Confirmações e refutações de afirmações de arquivo da Parte 3
- **Confirmado:** S16-F1 "nenhum commit prescrito por esta skill" (SV sem `git`); S16-F2 sem `CT.csv`; S16-F4 caminho/BOM/LF/`;`; S17-F1 `status.md` + `backlog.md` + commit na base; S17-F4/X1/X2 sem escrita; S18-F1 `licoes.md` na base; S18-F3 sem arquivo; S18-X3 AG-O sem `<produto>` e sem a skill; S19-F2 log `loop-<data>-HHMM.md`, worktree `.kiro/local/wt/ft-040/`, commit sem push; S19-F3 `status.md` + log + commit na worktree.
- **Refutado/corrigido:** S16-F4 `CT1.1` (CT:21 manda `CT<nn>`); S16-F1 "Rodadas verificação 1" no pedido direto está de acordo com SV:92-93, mas contradiz ST:26-27; S17-F1 "conceitos `elm/*.md` e `log.md`" sem caminho (é `<produto>/epicos/<EP>-<slug>/elm/`) e sem `index.md`, coluna ELM do glossário e ids de CT em `verificacao.md` (SE:112-113, 209); S17-F2 `ELM pendente` só no `status.md` (SE:24 manda o rodapé do PRD para requisitos de épico); S18-F1 "commit após sim" (o "sim" é do push/PR, SA:20-21); S19-F4 não lista o 2º commit/push do `pr-aberto` (SI:117).
- **Não visto por P3:** nenhum agente carrega `sdd-consolidar`/`sdd-aprender`; AG-V não comita; PR curto × commit na base; `.kiro/local/verificacao/**` fora do allow do orquestrador; `git worktree remove` negado a todos; `STEER:30` "não há" sem regra em SC.

