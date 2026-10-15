# Validação e Verificação das Skills do Power SDD

> **Gerado em:** 2026-10-15 | **Power:** sdd v2.3.0 — 19 skills | **Método:** Orquestrador + 8 subagents em paralelo

---


## Índice de Skills

| # | Skill | Papel |
|---|---|---|
| 1 | `sdd` | Guia do fluxo — redireciona para skills corretas |
| 2 | `sdd-setup` | Instala o fluxo no projeto |
| 3 | `sdd-status` | Painel somente leitura |
| 4 | `sdd-triar` | Porta de entrada de todo trabalho novo |
| 5 | `sdd-iniciar` | Ponto de compromisso — começa/retoma |
| 6 | `sdd-entrevistar` | Entrevista "grill me" — fecha decisões |
| 7 | `sdd-prd` | Escreve o PRD do épico |
| 8 | `sdd-fatiar` | PRD → fatias verticais |
| 9 | `sdd-planejamento` | Sprint, roadmap, acordos |
| 10 | `sdd-pesquisar` | Pesquisa somente leitura antes de planejar |
| 11 | `sdd-plano` | Spec do Kiro — requirements, design, tasks |
| 12 | `sdd-implementar` | TDD — ciclo vermelho→verde→refatorar |
| 13 | `sdd-revisar` | Revisão independente (rubricas P/L/C) |
| 14 | `sdd-verificar` | Verificação de aceite ponta a ponta |
| 15 | `sdd-consolidar` | Fecha a fatia após o merge |
| 16 | `sdd-aprender` | Aprendizado composto — lições + regras |
| 17 | `sdd-elm` | Alimenta o IBM ELM |
| 18 | `sdd-atender` | Trilha AT sem mudança de repositório |
| 19 | `sdd-loop` | Execução AFK de várias fatias até o PR |

---

# PARTE 1 — Mapeamento dos Fluxos de Trabalho

## Arquitetura Geral

O power SDD implementa **engenharia agêntica orientada a especificação** com 5 trilhas e o princípio: **alinhar antes de escrever, verificar acima de gerar**.

```
ENTRADA       sdd-triar ──► backlog: EP · FT (padrão/rápida/direta) · AT ──► sdd-atender
                 │
PRODUTO       sdd-entrevistar ──► sdd-prd ──► GATE PRD ──► sdd-elm (HF/REG/GL)
                                                                │
              sdd-fatiar ──► GATE Backlog ──► sdd-planejamento (sprint)
                                                    │
FATIA         sdd-iniciar ──► sdd-pesquisar ──► sdd-plano ──► GATE Plano
                                                                    │
              sdd-implementar (TDD) ──► sdd-revisar ──► sdd-verificar ──► PR
                                                                            │
DEPOIS        merge (pessoa) ──► sdd-consolidar ──► sdd-aprender

AUTÔNOMO      sdd-loop ──► N fatias AFK em paralelo até o PR
```

## Trilhas

| Trilha | Quando | Caminho |
|---|---|---|
| **direta** | diff cabe em 1 frase, sem regra nova | teste falha → correção → revisão C (diff) → PR |
| **rápida** | defeito ≤ 1 dia, comportamento correto já conhecido | bugfix.md + tasks.md → TDD → revisão → verificação → PR |
| **padrão** | fatia com regra clara, ficha aprovada | pesquisa → plano → GATE plano → TDD → revisão → verificação → PR → consolidação |
| **épico** | várias histórias ou decisão de produto em aberto | entrevista → PRD → GATE PRD → ELM → fatias → GATE backlog → planejamento → cada fatia na trilha padrão |
| **atendimento** | consulta/extração sem mudar o repositório | entrevista curta → AT no EWM → banco somente leitura → resposta → horas |

## Gates Humanos

| Gate | Quem | O que se aprova |
|---|---|---|
| PRD | P.O. | o quê e o porquê: histórias, cenários, regras, fora de escopo |
| Backlog | P.O. + time | as fatias: granularidade, dependências, AFK/HITL |
| Ficha | P.O. | fatia padrão sem épico: regras e cenários |
| Plano | dev (preferencialmente o futuro revisor) | a forma do programa e o contrato de pronto |
| PR | quem revisa | o código lido de verdade, com evidência de aceite |

## Agentes do Fluxo

| Agente | Skills | MCP ELM |
|---|---|---|
| `sdd-produto` | triar, entrevistar, prd, fatiar, planejamento, atender | ✅ escrita com confirmação |
| `sdd-pesquisador` | pesquisar | ❌ somente banco (leitura) |
| `sdd-codificador` | plano, implementar | ✅ escrita com confirmação |
| `sdd-revisor` | revisar | ❌ |
| `sdd-verificador` | verificar | ❌ |
| `sdd-orquestrador` | loop, iniciar, status | ✅ escrita com confirmação |

## Diagrama dos 8 Subagents desta Análise

```
Orquestrador (sessão principal)
├── Subagent 1 ──► sdd · sdd-setup · sdd-status
├── Subagent 2 ──► sdd-triar · sdd-iniciar
├── Subagent 3 ──► sdd-entrevistar · sdd-prd
├── Subagent 4 ──► sdd-fatiar · sdd-planejamento
├── Subagent 5 ──► sdd-pesquisar · sdd-plano
├── Subagent 6 ──► sdd-implementar · sdd-revisar · sdd-verificar
├── Subagent 7 ──► sdd-consolidar · sdd-aprender
└── Subagent 8 ──► sdd-elm · sdd-atender · sdd-loop
```

---

# PARTES 2, 3 e 4 — Análise por Skill

> As partes 2 (Plano de Fluxo), 3 (Teste do Quarto Chinês) e 4 (Verificação de Artefatos)
> são apresentadas juntas por skill para facilitar a rastreabilidade.


---

## SKILL: sdd (principal)

> **Papel:** Guia do fluxo — explica trilhas, gates, princípios; direciona para a skill correta quando nenhuma outra se encaixa.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Consulta e explicação do fluxo
| Campo | Descrição |
|---|---|
| Gatilho | Usuário diz "como funciona o sdd", "qual o fluxo", "o que eu faço agora", "sdd" — ou nenhuma outra skill sdd se encaixa no pedido |
| Processamento | Verifica se `.kiro/steering/sdd.md` existe (→ Fluxo 2 se não). Lê seções Trilhas, Gates e Princípios; identifica a dúvida pelo texto livre; localiza na tabela "O que dizer" a skill correspondente ao intent detectado; se o intent não mapeia, responde com a visão geral |
| Output | Explicação textual do fluxo (trilhas, gates, princípios) e/ou indicação direta da skill adequada |

#### Fluxo 2: Diagnóstico de pré-condição — sem sdd.md
| Campo | Descrição |
|---|---|
| Gatilho | Qualquer pedido à skill sdd quando `.kiro/steering/sdd.md` não existe |
| Processamento | Tenta localizar `.kiro/steering/sdd.md` → ausente → interrompe todo processamento imediatamente |
| Output | `"Sem .kiro/steering/sdd.md — comece por 'configurar o sdd' (sdd-setup)"` |

#### Fluxo 3: Seleção de trilha por tamanho de demanda
| Campo | Descrição |
|---|---|
| Gatilho | Usuário descreve uma demanda nova sem mencionar trilha |
| Processamento | Avalia indicadores: diff numa frase/sem regra nova → direta; defeito/≤1 dia/comportamento conhecido → rápida; fatia com ficha → padrão; múltiplas histórias/decisão em aberto → épico; consulta sem mudança no repo → atendimento. Toda demanda nova passa antes pela `sdd-triar` |
| Output | Trilha identificada + sequência de skills a seguir |

#### Fluxo 4: Direcionamento pontual via tabela "O que dizer"
| Campo | Descrição |
|---|---|
| Gatilho | Usuário expressa intent específico mapeável (ex.: "quero lançar horas", "quero revisar o PRD") |
| Processamento | Localiza o intent na tabela "O que dizer" (26 entradas); retorna a skill mapeada sem executar nenhuma ação |
| Output | Resposta direta: "use `sdd-elm` modo horas" / "use `sdd-revisar`" etc. |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | `"como funciona o sdd"` |
| Regra IF/THEN | IF `.kiro/steering/sdd.md` existe E input ∈ {"como funciona", "qual o fluxo", "o que eu faço agora", "sdd"} → exibir tabela Trilhas + Gates + "O que dizer" + 10 Princípios; ELSE IF nenhuma skill encaixou → visão geral completa |
| Output Gerado | Tabela das 5 trilhas, tabela dos 5 gates, tabela "O que dizer" com skills, lista dos 10 princípios |

#### Fluxo 2
| Campo | Descrição |
|---|---|
| Input Exato | `"qual a próxima fatia"` quando `.kiro/steering/sdd.md` não existe |
| Regra IF/THEN | IF `.kiro/steering/sdd.md` NOT EXISTS → bloquear → retornar mensagem de ausência; ELSE → prosseguir |
| Output Gerado | `"Sem .kiro/steering/sdd.md — o fluxo não está configurado. Comece por 'configurar o sdd'."` |

#### Fluxo 3
| Campo | Descrição |
|---|---|
| Input Exato | `"preciso corrigir um NPE no cálculo de parcelas — uma linha no validador"` |
| Regra IF/THEN | IF diff_cabe_numa_frase=true AND sem_regra_nova=true → trilha=direta; ELSE IF ≤1 dia AND comportamento_certo_conhecido=true → trilha=rápida; ELSE IF fatia_única AND regra_clara → trilha=padrão; ELSE IF múltiplas_histórias OR decisão_produto_aberta → trilha=épico; ELSE IF consulta_sem_mudança → trilha=atendimento |
| Output Gerado | `"Trilha direta → sdd-triar (registra) → teste que falha → correção → revisão → PR"` |

#### Fluxo 4
| Campo | Descrição |
|---|---|
| Input Exato | `"quero entender o código antes de planejar"` |
| Regra IF/THEN | IF input matcheia entrada na tabela "O que dizer" → retornar skill mapeada; ELSE → Fluxo 1 |
| Output Gerado | `"Use sdd-pesquisar."` |

### PARTE 4 — Verificação de Artefatos

> A skill `sdd` é exclusivamente de orientação e leitura. **Não grava arquivos.** Os artefatos que ela referencia são criados por outras skills.

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Todos | Nenhum | — | Skill responde textualmente; zero I/O de arquivo | Não aplicável |


---

## SKILL: sdd-setup

> **Papel:** Configura o fluxo sdd num projeto — detecta stack, inventa 6 agentes, gera `.kiro/steering/sdd.md`, hooks e workflows opcionais.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Primeira instalação
| Campo | Descrição |
|---|---|
| Gatilho | `"configurar o sdd"` sem `.kiro/steering/sdd.md` nem `.kiro/agents/sdd-*.json` existentes |
| Processamento | **P0**: detecta raiz git e pasta do power instalado. **P1**: lê README/build files/árvore (2-3 níveis)/git log; propõe tipo+stack+testes numa mensagem; aguarda "sim/corrija". **P2**: detecta e propõe comandos de build/testes/lint/cobertura; oferece rodá-los. **P3**: detecta branch base, prefixo, padrão de commit, ferramenta de PR pelo host do `origin`, MCP de banco. **P4**: define pasta do produto, glossário, ADRs, ELM (sem perguntas quando `pa_*.json` encontrado). **P5**: inventaria skills (projeto, usuário, outros powers, toolkits) excluindo sdd-* e elm-*. **P6**: para cada um dos 6 agentes, uma mensagem só com proposta pré-marcada pelos papéis do toolkit + MCPs; aguarda "ok" ou linha que muda. **P7**: hook + Kiro Workflows opcionais. **P8**: monta tudo em memória a partir dos templates de `assets/`; exibe resumo; grava com "ok". **P9**: valida JSON, placeholders, MCPs, paths, `kiro-cli agent validate`. |
| Output | `.kiro/steering/sdd.md` · 6 `.kiro/agents/sdd-*.json` · (opcional) hook, workflows, http.sh · `<produto>/backlog.md`, `planejamento/`, `aprendizado/licoes.md`, `atendimentos/README.md` · `.gitignore` com `.kiro/local/` |

#### Fluxo 2: Modo atualização
| Campo | Descrição |
|---|---|
| Gatilho | `"atualizar os agentes do sdd"` — `.kiro/steering/sdd.md` ou `sdd-*.json` já existem |
| Processamento | Exibe configuração atual; pergunta o que muda; **sempre** regenera agentes dos templates atuais do power; para agente editado à mão: exibe diff e pergunta antes de sobrescrever; preserva seção "Regras aprendidas" do sdd.md; pasta produto: só acrescenta o que falta; executa P9 ao final |
| Output | Agentes regenerados com diff exibido · `sdd.md` atualizado (Regras aprendidas intactas) · relatório de validação |

#### Fluxo 3: Migração sdd2 → sdd
| Campo | Descrição |
|---|---|
| Gatilho | P0 detecta `.kiro/steering/sdd2*.md` ou `.kiro/agents/sdd2-*.json` |
| Processamento | Propõe plano de migração em uma só mensagem + aguarda "ok": merge sdd2→sdd.md; lições → Regras aprendidas; `sdd2-fechar-sessao.md` removido; `sdd2-*.json` removidos e substituídos; renomeia hooks, workflows, http.sh; nota que fatias em andamento (`.kiro/specs/`) não mudam; executa P9 |
| Output | Layout v2.3 completo · arquivos sdd2 removidos · 6 novos agentes `sdd-*.json` |

#### Fluxo 4: Validação (P9)
| Campo | Descrição |
|---|---|
| Gatilho | Execução automática após gravação ("ok" no P8) |
| Processamento | Para cada `.json`: parse, verifica `name`, `{{…}}` sobrando, `includeMcpJson`, MCPs de ELM somente em produto/codificador/orquestrador, paths `skill://`/`file://` existentes e relativos. Se `kiro-cli` disponível: `kiro-cli agent validate --path` para cada agente. Erros → exibe e oferece correção |
| Output | Relatório de validação (ok ou erros) + sugestão de commit + próximo passo |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Primeira instalação
| Campo | Descrição |
|---|---|
| Input Exato | `"configurar o sdd"` (sem sdd.md e sem sdd-*.json no repositório) |
| Regra IF/THEN | IF sdd.md NOT EXISTS AND sdd-*.json NOT EXISTS AND sdd2*.md NOT EXISTS AND sdd-projeto.md NOT EXISTS → executar P0→P9; ELSE IF sdd.md OR sdd-*.json EXISTS → Fluxo 2; ELSE IF sdd2*.md EXISTS → Fluxo 3; ELSE IF sdd-projeto.md EXISTS WITHOUT sdd.md → Fluxo migração v1 |
| Output Gerado | Sequência de mensagens por passo; ao final do P8: `"⚙️ sdd — <projeto> ... Gravar? (ok)"` |

#### Fluxo 2 — Atualização
| Campo | Descrição |
|---|---|
| Input Exato | `"atualizar os agentes do sdd"` (com sdd.md existente) |
| Regra IF/THEN | IF sdd.md EXISTS → mostrar tabela configuração atual → perguntar o que muda → regenerar TODOS os agentes dos templates (mesmo os corretos) → PARA CADA agente com edição manual: mostrar diff + perguntar → NUNCA apagar Regras aprendidas do sdd.md |
| Output Gerado | Tabela configuração atual + diff por agente + `"Gravar? (ok)"` |

#### Fluxo 4 — Validação P9
| Campo | Descrição |
|---|---|
| Input Exato | P9 iniciado automaticamente após "ok" no P8 |
| Regra IF/THEN | PARA CADA .json: IF parse falha → erro; IF `name` ≠ nome_arquivo → erro; IF `{{…}}` sobrando → erro; IF `@servidor/tool` em tools AND `includeMcpJson` ≠ true → erro; IF ELM escrita em revisor/verificador/pesquisador → erro; IF skill:// ou file:// inexistente ou absoluto → erro. IF kiro-cli disponível → `kiro-cli agent validate --path` para cada um. IF algum erro → exibir + oferecer correção ELSE → sugerir commit |
| Output Gerado | `"✅ validação ok"` + sugestão de commit + frase do próximo passo |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| 1, 2, 3 | `.kiro/steering/sdd.md` | `.md` (seções: Projeto, Git, ELM, Autonomia, Comandos, Regras aprendidas) | Criado/atualizado com todos os `{{…}}` substituídos; Regras aprendidas preservadas no modo atualização | Erro do sistema de arquivos exibido; nada gravado antes do "ok" do P8 |
| 1, 2, 3 | `.kiro/agents/sdd-<agente>.json` (6 arquivos) | `.json` (blocos V2+V3 em espelho, `toolsSettings`+`allowedTools`+`permissions.rules`) | 6 arquivos gravados; Kiro pede confirmação por arquivo neste diretório | Erro de permissão exibido; arquivo não sobrescrito se confirmação negada |
| 1, 3 (opcional) | `.kiro/hooks/sdd.json` | `.json` (trigger PostTaskExec, ação shell com comandos de compilar+testes) | Criado com "ok"; Kiro pede confirmação | Kiro exibe erro; arquivo não criado; fluxo funciona sem ele |
| 1, 3 (opcional) | `.kiro/workflows/sdd-*.workflow.json` | `.workflow.json` (receita Kiro Workflows) | Criados somente se recurso habilitado | Kiro exibe erro; fluxo funciona sem eles |
| 1, 3 (opcional) | `.kiro/sdd/http.sh` | `.sh` (template com `{{URL_TESTE}}` substituído) | Criado com URL base do ambiente de teste | Erro de permissão; verificação passa a pedir confirmação por curl |
| 1, 2, 3 | `<produto>/backlog.md`, `planejamento/`, `aprendizado/licoes.md`, `atendimentos/README.md` | `.md` | Criados apenas onde ausentes; existentes não são sobrescritos | Erro de permissão; skill reporta o erro |
| 1, 2, 3 | `.gitignore` (raiz) | texto plano | Linha `.kiro/local/` acrescentada ao final se ausente | Erro de permissão; linha não acrescentada; loop não deve ser usado sem esta exclusão |


---

## SKILL: sdd-status

> **Papel:** Painel somente leitura — onde parei e o que fazer agora; fecha a sessão de trabalho.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Exibição do painel completo
| Campo | Descrição |
|---|---|
| Gatilho | `"onde parei"`, `"status"`, `"painel"`, `"bom dia"`, `"o que tem pendente"`, `"qual a próxima fatia"`, `"como está a sprint"`, `"retomar"` |
| Processamento | **Coleta**: git fetch → `.kiro/specs/*/status.md` (branch atual + worktrees + branches remotas via `git for-each-ref`) → extrai de cada: fatia, fase, rodadas, achados, PR, pendências ELM; de `tasks.md`: `[x]`/total; de `backlog.md` (base): épicos, fatias prontas, sprint atual; de `acordos.md`: limites WIP; de `licoes.md`: lições propostas; de `sprint-<nn>.md`: especificação/atendimento; de `.kiro/local/loop-*.md`: lotes autônomos. Identifica "minhas" fatias via `git config user.name` × `equipe.json`. **Renderiza painel** com 8 seções. **Aplica 9 regras de inconsistência**. **Calcula sugestão** pela hierarquia fixa (desbloquear gate → atendimento com prazo → terminar em andamento → começar próxima pronta → produto) |
| Output | Dashboard `📊 sdd — <projeto>` com 8 seções: Em andamento, Esperando pessoa (WIP), Prontas, Produto, Atendimento, ELM pendente/Lições, Inconsistências, Sugestão |

#### Fluxo 2: Fechar a sessão
| Campo | Descrição |
|---|---|
| Gatilho | `"fechar a sessão"`, `"encerrar por hoje"` |
| Processamento | Identifica branch atual → localiza `.kiro/specs/<ft>/status.md`. (1) Append no Histórico: o que foi feito + próximo passo exato + decisões. (2) Marca `tasks.md` somente itens realmente prontos e verdes. (3) Exibe `git status`. (4) Propõe commit com os arquivos prontos — aguarda "ok" explícito; **nunca faz push**. (5) Termina com frase de retomada |
| Output | `status.md` atualizado (Histórico + próximo passo) · `tasks.md` com marcações corretas · proposta de commit (sem execução automática) · frase de retomada |

#### Fluxo 3: Sem sdd.md
| Campo | Descrição |
|---|---|
| Gatilho | Qualquer trigger quando `.kiro/steering/sdd.md` não existe |
| Processamento | Tenta localizar `.kiro/steering/sdd.md` → ausente → interrompe; nenhum comando git executado |
| Output | `"O fluxo sdd não está configurado. Use 'configurar o sdd' (sdd-setup)."` |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Painel completo
| Campo | Descrição |
|---|---|
| Input Exato | `"onde parei"` |
| Regra IF/THEN | IF sdd.md NOT EXISTS → Fluxo 3. ELSE: executar sequência de coleta em ordem estrita → identificar "minhas" fatias (IF git user.name ∈ equipe.json → match; ELSE perguntar login uma vez) → renderizar 8 seções → PARA CADA fatia aplicar 9 regras de inconsistência → calcular sugestão pela hierarquia |
| Output Gerado | `"📊 sdd — <projeto> · sprint <nn> (<dias> dias restantes) · meta: <…>"` com 8 seções + Inconsistências (lista ou "nenhuma") + Sugestão |

#### Fluxo 2 — Fechar sessão
| Campo | Descrição |
|---|---|
| Input Exato | `"fechar a sessão"` (na branch de uma fatia ativa) |
| Regra IF/THEN | IF trigger ∈ {"fechar a sessão", "encerrar por hoje"} → identificar branch → localizar status.md → APPEND Histórico → marcar tasks.md SOMENTE itens concluídos (IF item=verde → [x]; ELSE manter [ ]) → exibir git status → propor commit → IF usuário diz "ok" → gravar; ELSE não gravar → NEVER push → ALWAYS terminar com frase "vamos trabalhar na FT-<id>" |
| Output Gerado | `status.md` com Histórico atualizado · `tasks.md` com marcações · `git status` exibido · `"Proposta de commit: <padrão>. Confirma? (ok)"` · frase de retomada |

#### Fluxo 3 — Sem sdd.md
| Campo | Descrição |
|---|---|
| Input Exato | `"bom dia"` quando sdd.md ausente |
| Regra IF/THEN | IF sdd.md NOT EXISTS → bloquear → retornar mensagem de ausência + oferecer sdd-setup |
| Output Gerado | `"O fluxo sdd não está configurado neste projeto."` |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Fluxo 1 (painel) | Nenhum — coleta somente leitura | — | Painel exibido com dados reais; nenhum arquivo modificado | `git fetch` falha: usa dados locais disponíveis; branches remotas não atualizadas |
| Fluxo 2 (fechar sessão) | `.kiro/specs/<ft>/status.md` | `.md` — seção `## Histórico` recebe linha nova com data + o que foi feito + próximo passo | `status.md` atualizado; dados persistem para retomada por qualquer agente ou pessoa | Dir. `.kiro/specs/<ft>/` inacessível: erro exibido; sessão não fechada formalmente |
| Fluxo 2 (fechar sessão) | `.kiro/specs/<ft>/tasks.md` | `.md` — `[ ]` → `[x]` somente para itens realmente concluídos | Marcações corretas; itens incompletos mantidos como `[ ]` | Arquivo não gravável: erro exibido; progresso não registrado |
| Fluxo 2 (commit) | Git staging (raiz) | Nenhum arquivo extra — proposta de commit aguardando "ok" | Commit criado com padrão do sdd.md; **push nunca executado** | Usuário não confirma: nenhum commit; arquivos modificados permanecem unstaged |


---

## SKILL: sdd-triar

> **Papel:** Porta de entrada de todo trabalho novo — decide trilha, registra no backlog, não começa nada.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Pedido em texto
| Campo | Descrição |
|---|---|
| Gatilho | Usuário descreve nova funcionalidade, bug ou melhoria em linguagem natural |
| Processamento | 1. Troca para branch base + `git pull --ff-only`; 2. Lê o texto; 3. Verifica duplicatas (backlog.md, atendimentos, branches); 4. Classifica trilha: épico / padrão / rápida / direta / atendimento; 5. Registra no backlog.md (EP-nn em rascunho ou linha FT-nnn); 6. Se padrão: roda sdd-entrevistar → escreve ficha → aguarda aprovação P.O.; 7. Atualiza "Próximos ids"; commit + push com "sim"; 8. Pergunta se inicia agora |
| Output | Linha nova em `<produto>/backlog.md`; ficha `<produto>/fatias/FT-nnn-slug.md` (se trilha padrão); commit na base |

#### Fluxo 2: EWM simples (número único)
| Campo | Descrição |
|---|---|
| Gatilho | Usuário fornece número único de work item EWM |
| Processamento | 1. Troca para branch base; 2. Lê item via mcp-elm; 3. Verifica duplicatas; 4. Mapeia tipo/estado EWM para trilha; 5. Registra linha FT-nnn; 6. Se padrão: entrevista + ficha + aprovação P.O.; 7. Commit + push com "sim" |
| Output | Linha FT-nnn em backlog.md; ficha opcional (padrão); commit na base |

#### Fluxo 3: Lote EWM
| Campo | Descrição |
|---|---|
| Gatilho | `"importar do EWM"`, `"triar os defeitos do time"` |
| Processamento | 1. Filtra itens por time/tipo/estado via mcp-elm (precisa do MCP); 2. Lê cada item individualmente; 3. Monta proposta em tabela com trilhas sugeridas e duplicatas marcadas; 4. Aguarda UMA confirmação; 5. Registra todos os itens não-duplicata; 6. Atualiza "Próximos ids"; commit único + push |
| Output | N linhas em backlog.md; commit único; sem fichas neste momento |

#### Fluxo 4: Retomada de triagem
| Campo | Descrição |
|---|---|
| Gatilho | P.O. retorna com aprovação de ficha, ou quer continuar entrevista interrompida |
| Processamento | 1. Troca para branch base; 2. Localiza ficha FT-nnn existente; 3. Verifica status no backlog.md ("aguardando aprovação"); 4a. Se aprovação recebida: atualiza status → "aprovada" + commit; 4b. Se quer reeditar: reabre ficha, reinicia aprovação |
| Output | backlog.md com status "aprovada"; commit; pergunta sobre sdd-iniciar |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | `"preciso adicionar validação de CPF no cadastro"` |
| Regra IF/THEN | IF duplicata em backlog.md/branches → reporta, para, sem gravar; ELSE IF sem mudança código AND sem artefato → trilha=atendimento; ELSE IF diff numa frase/sem regra nova → trilha=direta; ELSE IF sem regra nova/comportamento correto → trilha=rápida; ELSE IF escopo multi-fatia → trilha=épico; ELSE → trilha=padrão → sdd-entrevistar → ficha → aguarda "sim" do P.O. antes do commit |
| Output Gerado | Linha FT-nnn (ou EP-nn) em backlog.md; mensagem de confirmação; `"Inicia agora?"` |

#### Fluxo 2
| Campo | Descrição |
|---|---|
| Input Exato | Número inteiro EWM: `98765` |
| Regra IF/THEN | IF número já em backlog.md ou branch → reporta duplicata, para; ELSE CALL mcp-elm(get_workitem, id=98765); IF tipo=defeito AND sem regra nova AND ≤1 dia → trilha=rápida; IF descrição numa frase AND sem regra → trilha=direta; ELSE → trilha=padrão; Gera FT-nnn; registra; commit+push com "sim" |
| Output Gerado | Linha FT-nnn em backlog.md; confirmação; ficha somente se padrão |

#### Fluxo 3
| Campo | Descrição |
|---|---|
| Input Exato | `"todos os defeitos abertos do time Alfa"` (sem MCP elm) |
| Regra IF/THEN | IF MCP elm NÃO disponível → `"importação precisa do MCP — pare"`; ELSE CALL mcp-elm(list_workitems); FOR EACH item: IF já em backlog.md → marca "duplicata" na tabela; ELSE → classifica trilha; APRESENTA tabela; aguarda UMA resposta "sim"; IF "sim" → FOR EACH não-duplicata: registra FT-nnn; commit único; push |
| Output Gerado | Tabela de proposta exibida; após "sim": N linhas em backlog.md + 1 commit |

#### Fluxo 4
| Campo | Descrição |
|---|---|
| Input Exato | `"P.O. aprovou a FT-042"` |
| Regra IF/THEN | IF FT-nnn NÃO existe em `<produto>/fatias/` → "FT não encontrada", para; IF status ≠ "aguardando aprovação" → reporta status atual, para; IF aprovação confirmada → atualiza status para "aprovada"; commit; push com "sim"; pergunta sdd-iniciar |
| Output Gerado | backlog.md com status "aprovada"; commit; pergunta de encaminhamento |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| 1 – Pedido em texto | `<produto>/backlog.md` | `.md` — tabela com colunas trilha, ficha, modo, status, ids | Linha FT-nnn ou EP-nn inserida; "Próximos ids" incrementado; commit gerado | Erro de escrita → reporta; sem commit; interrompe fluxo |
| 1 – Trilha padrão (ficha) | `<produto>/fatias/FT-<nnn>-<slug>.md` | `.md` — ficha com campos de entrevista | Ficha gravada; referência adicionada à linha do backlog.md | Pasta `fatias/` inexistente → cria; se falhar → erro |
| 2 – EWM simples | `<produto>/backlog.md` | `.md` | Linha FT-nnn com metadados do EWM; commit gerado | Item não registrado; usuário notificado; sem commit |
| 3 – Lote EWM | `<produto>/backlog.md` | `.md` | N linhas inseridas atomicamente em um único commit | Nenhuma linha gravada (commit único não realizado) |
| 4 – Retomada | `<produto>/backlog.md` | `.md` | Status FT-nnn de "aguardando aprovação" para "aprovada"; commit | Status não alterado; usuário notificado |


---

## SKILL: sdd-iniciar

> **Papel:** Ponto de compromisso — confere DoR, responsável, sprint, WIP; cria pasta spec e branch; assume tarefa no EWM.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Início limpo por FT-nnn
| Campo | Descrição |
|---|---|
| Gatilho | `"vamos trabalhar na FT-031"`, `"pegar a task 123"`, `"começar"`, `"próxima fatia"` |
| Processamento | 1. Localiza FT-nnn no backlog.md (ou EWM com mcp-elm); 2. Determina trilha; 3. Verifica DoR completa; 4. Verifica responsável; 5. Verifica sprint (oferece encaixe via sdd-planejamento se fora); 6. Verifica WIP em acordos.md; 7. Verifica publicação em origin; 8. Sugere nome de branch → aguarda "sim"; 9. `git fetch` + `git switch -c <branch> origin/<base>`; 10. Cria `.kiro/specs/<ft>-<slug>/` + `status.md` + `.config.kiro` (não na trilha direta); 11. Assume tarefa [DEV] no EWM com "sim" (ou sdd-elm cria se inexistente); 12. Commit do status.md + push com "sim"; 13. Encaminha pela fase |
| Output | Branch criada · `.kiro/specs/<ft>-<slug>/status.md` · `.config.kiro` (trilhas padrão/rápida) · tarefa EWM assumida |

#### Fluxo 2: Retomada (spec e branch já existentes)
| Campo | Descrição |
|---|---|
| Gatilho | FT-nnn com branch e pasta `.kiro/specs/<ft>-<slug>/` já criadas |
| Processamento | 1. Detecta branch e pasta spec existentes; 2. Lê `status.md` → extrai campo "fase"; 3. Encaminha pela tabela: pesquisando/planejando/plano-em-revisao → sdd-plano; implementando/revisando → sdd-implementar; verificando → sdd-verificar; aceita → sdd-implementar Passo 5; pr-aberto → aguardar merge; bloqueada → exibe motivo; 4. Não recria nenhum artefato existente |
| Output | Mensagem com fase atual e instrução de encaminhamento; zero novos artefatos |

#### Fluxo 3: Pedido não registrado
| Campo | Descrição |
|---|---|
| Gatilho | Usuário descreve demanda nova sem FT-nnn, EWM ou EP identificável no backlog.md |
| Processamento | 1. Tenta extrair padrão FT-\d+, EWM-\d+ ou EP-\d+ do input; 2. Busca aproximada por título no backlog.md; 3. Não encontra correspondência; 4. Redireciona para sdd-triar sem criar nenhum artefato |
| Output | `"Pedido não registrado; use sdd-triar primeiro."` — zero artefatos gravados |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | `"iniciar FT-042"` |
| Regra IF/THEN | IF FT-042 NÃO em backlog.md → "não registrado; use sdd-triar", para; IF `.kiro/specs/ft-042-*/` existe → Fluxo 2 (retomada); ELSE verifica DoR: IF campo obrigatório ausente → lista faltantes, para; IF responsável indefinido → solicita, para; IF fora da sprint ativa → oferece encaixe; aguarda "sim"; IF WIP excedido → alerta, para; IF não publicado em origin → "faça push da base primeiro", para; ELSE sugere branch; aguarda "sim"; IF "sim" → cria branch; cria pasta spec; grava status.md; IF trilha≠direta → grava .config.kiro; assume EWM [DEV]; commit; push |
| Output Gerado | Branch criada; `status.md` e `.config.kiro` em `.kiro/specs/<ft>-<slug>/`; tarefa EWM assumida; encaminhamento para sdd-plano |

#### Fluxo 2
| Campo | Descrição |
|---|---|
| Input Exato | `"retomar FT-042"` com branch e spec já existentes |
| Regra IF/THEN | IF branch existe AND pasta `.kiro/specs/<ft>-slug/` existe → READ status.md → campo "fase"; IF fase IN [pesquisando, planejando, plano-em-revisao] → "encaminho para sdd-plano"; IF fase IN [implementando, revisando] → "encaminho para sdd-implementar"; IF fase=verificando → "encaminho para sdd-verificar"; IF fase=aceita → "encaminho para sdd-implementar (passo PR)"; IF fase=pr-aberto → "aguarde merge; mergeado → sdd-consolidar"; IF fase=bloqueada → exibe campo motivo; NÃO cria artefato |
| Output Gerado | Mensagem com fase atual + instrução de encaminhamento; zero escrita |

#### Fluxo 3
| Campo | Descrição |
|---|---|
| Input Exato | `"quero adicionar relatório mensal de benefícios"` (sem FT, EWM ou EP) |
| Regra IF/THEN | SCAN input por regex FT-\d+, EWM-\d+, EP-\d+; IF nenhum padrão → busca aproximada em backlog.md; IF sem correspondência → "pedido não registrado; use sdd-triar primeiro"; NÃO cria branch; NÃO cria pasta spec; NÃO grava arquivo |
| Output Gerado | Mensagem de redirecionamento para sdd-triar; zero artefatos |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| 1 – Início limpo | `.kiro/specs/<ft>-<slug>/status.md` | `.md` — campos: fase, id, trilha, responsável, sprint, Histórico, ELM | Arquivo criado com fase inicial; incluído no commit; legível pelas skills subsequentes | Reporta impossibilidade; para antes de criar branch |
| 1 – Padrão/rápida | `.kiro/specs/<ft>-<slug>/.config.kiro` | Formato de spec do Kiro (specType: feature ou bugfix) | Arquivo criado; skills subsequentes reconhecem o contexto da spec | Falha reportada; trilha não configurada |
| 1 – Trilha direta | `.kiro/specs/<ft>-<slug>/.config.kiro` | — | **NÃO criado** — regra explícita: trilha direta não cria .config.kiro | Não aplicável: ausência é o comportamento correto |
| 2 – Retomada | Nenhum novo arquivo | — | Leitura de status.md existente; encaminhamento correto sem escrita | Se status.md ausente: reporta "spec inconsistente"; solicita intervenção manual |
| 3 – Não registrado | Nenhum arquivo | — | Mensagem de redirecionamento; zero escrita | Não aplicável: fluxo de rejeição |


---

## SKILL: sdd-entrevistar

> **Papel:** Entrevista de alinhamento "grill me" — percorre árvore de decisões em rodadas; responde sozinha o que já tem fonte.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Padrão (alinhamento de demanda, PRD, fatia ou plano)
| Campo | Descrição |
|---|---|
| Gatilho | `"me entreviste"`, `"grill me"`, `"vamos alinhar"`, `"quais decisões estão em aberto"` — ou chamada por sdd-prd, sdd-fatiar, sdd-plano |
| Processamento | 1. Lê artefatos existentes (demanda, decisoes.md, glossário, ADRs, steering, PRD); 2. Monta árvore de decisões: escopo → atores → comportamento → exceções → dados → integrações → NF → fora de escopo; 3. Resolve automaticamente o que tem fonte (código/ELM/glossário/banco somente leitura), citando-a; 4. Pergunta em rodadas pela fronteira: numeradas, com recomendação, "sim" aceita todas; 5. Repete rodadas até árvore esgotada; 6. Appenda em decisoes.md; 7. Registra termos novos |
| Output | `decisoes.md` atualizado (append); glossário atualizado (branch base) ou "termos pendentes" em decisoes.md (branch de fatia) |

#### Fluxo 2: Modo atendimento
| Campo | Descrição |
|---|---|
| Gatilho | Chamada por sdd-atender em modo atendimento |
| Processamento | 1. Executa apenas UMA rodada curta (5 perguntas: o que receber, origem, prazo, quem responde, critério de pronto); 2. Sem árvore completa, sem glossário; 3. Retorna dados ao fluxo chamador |
| Output | Dados mínimos de alinhamento entregues ao sdd-atender; sem gravação de decisoes.md de épico/fatia |

#### Fluxo 3: Modo autônomo (AUTONOMO=true)
| Campo | Descrição |
|---|---|
| Gatilho | Chamada com flag AUTONOMO=true por agente sem pessoa na conversa |
| Processamento | 1. Lê artefatos; 2. Monta árvore completa; 3. Para cada nó: se há fonte → resolve e classifica como "decidida"; se não há → registra como "em aberto" com recomendação entre parênteses na coluna Decisão; 4. Nenhuma pergunta feita ao usuário; 5. Appenda todas as decisões em decisoes.md |
| Output | `decisoes.md` com decisões "decidida" ou "em aberto" + recomendação; sem interação humana |

#### Fluxo 4: Linguagem ubíqua
| Campo | Descrição |
|---|---|
| Gatilho | Identificação de termo novo durante qualquer fluxo (subtarefa embarcada) |
| Processamento | 1. Detecta termo não presente no glossário; 2. SE branch base → appenda em `docs/glossario.md`; SE branch de fatia → registra "termo pendente: X" em decisoes.md da fatia, para sdd-consolidar levar ao glossário depois do merge |
| Output | `docs/glossario.md` com novo termo (branch base) OU linha "termo pendente" em decisoes.md da fatia |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | Artefatos disponíveis: demanda, decisoes.md atual, glossário, ADRs, steering, PRD |
| Regra IF/THEN | IF artefato com resposta para decisão D existe nas fontes → resolve D automaticamente, fonte registrada; ELSE IF pré-requisitos de D decididos → inclui D na próxima rodada com recomendação; ELSE IF pré-requisitos não decididos → adia D; IF usuário responde "sim" → aceita todas as recomendações da rodada; IF decisão registrada → append em decisoes.md (NUNCA sobrescreve linha existente) |
| Output Gerado | Rodadas numeradas com perguntas e recomendações → confirmações → `decisoes.md` com novas linhas, situação "decidida" ou "confirmada" |

#### Fluxo 2
| Campo | Descrição |
|---|---|
| Input Exato | Chamada interna de sdd-atender com modo=atendimento |
| Regra IF/THEN | IF modo=atendimento → executa exatamente UMA rodada (5 perguntas fixas); IF rodada concluída → retorna dados ao sdd-atender; ELSE (modo padrão) → múltiplas rodadas até árvore esgotada |
| Output Gerado | Dados mínimos entregues ao fluxo chamador (sem gravação própria neste ponto) |

#### Fluxo 3
| Campo | Descrição |
|---|---|
| Input Exato | Invocação com AUTONOMO=true + artefatos existentes lidos |
| Regra IF/THEN | IF AUTONOMO=true → NEVER emite pergunta ao usuário; IF existe fonte para D → registra D como "decidida" com fonte; IF não existe fonte para D → registra D como "em aberto" com "(recomendação: X)" entre parênteses; append em decisoes.md |
| Output Gerado | `decisoes.md` gravado com todas as decisões em uma passagem; sem aguardar input |

#### Fluxo 4
| Campo | Descrição |
|---|---|
| Input Exato | Termo T identificado durante entrevista + contexto de branch atual |
| Regra IF/THEN | IF T já existe em glossario.md → não duplica; IF T é novo E branch=base → append T em glossario.md; IF T é novo E branch=fatia → append linha "termo pendente: T" em decisoes.md da fatia |
| Output Gerado | Entrada nova em `docs/glossario.md` (base) OU linha "termo pendente: T" em `decisoes.md` da fatia |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| 1 – épico | `<produto>/epicos/<EP>-<slug>/decisoes.md` | `.md` — tabela D \| Pergunta \| Decisão \| Fonte \| Data \| Situação | Novas linhas appendadas; histórico preservado | Pasta não existe ou sem permissão → erro; nenhuma linha gravada |
| 1 – fatia | `.kiro/specs/<ft>-<slug>/decisoes.md` | `.md` — mesma tabela | Novas linhas appendadas | Pasta `.kiro/specs/<ft>-<slug>/` não existe → erro |
| 3 – autônomo | `<produto>/epicos/<EP>-<slug>/decisoes.md` ou `.kiro/specs/<ft>-<slug>/decisoes.md` | `.md` — coluna Situação="em aberto"; coluna Decisão com "(recomendação: X)" | Todas as decisões gravadas sem interação | Diretório inacessível → erro; arquivo não gravado |
| 4 – glossário (base) | `docs/glossario.md` | `.md` — lista ou tabela de termos | Termo novo inserido; arquivo atualizado | Pasta `docs/` não existe ou sem permissão → erro |
| 4 – fatia | `.kiro/specs/<ft>-<slug>/decisoes.md` | `.md` — linha "termo pendente: X" appendada | Linha inserida com indicação de consolidação futura | decisoes.md não existe ou inacessível → erro |


---

## SKILL: sdd-prd

> **Papel:** Escreve o PRD de um épico — o quê e o porquê. Histórias com cenários Gherkin, regras, termos. Conceitos OKF v0.2 em `elm/`. Conduz GATE do PRD.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Novo PRD
| Campo | Descrição |
|---|---|
| Gatilho | `"escreve o PRD"`, `"documenta a demanda"`, `"épico"` — pasta do épico inexistente |
| Processamento | 1. Lê descrição longa (ou item EWM via mcp-elm); 2. Explora bundle ELM, código, glossário, ADRs; 3. Define EP-nn e slug; cria pasta `<produto>/epicos/<EP>-<slug>/`; 4. Registra épico no EWM via sdd-elm modo backlog; 5. Roda sdd-entrevistar → grava decisoes.md; 6. Similares no ELM via sdd-elm modo similares (**obrigatório** antes de criar qualquer elm/); 7. Escreve prd.md + conceitos OKF: HF-nn-slug.md, REG-nn-slug.md, GL-termo.md, index.md, log.md; 8. Se >~8 histórias: propõe dividir em dois épicos; 9. Revisão independente pelo sdd-revisor (rubrica P), até 2 rodadas; 10. GATE do PRD (P.O.); 11. Pós-aprovação: elm/ recebe `status: stable` + `verified` humano; commit na BASE |
| Output | Pasta épico completa com todos os artefatos; backlog.md atualizado; PRD commitado na BASE; disparo de sdd-elm modo requisitos e sdd-fatiar |

#### Fluxo 2: GATE do PRD
| Campo | Descrição |
|---|---|
| Gatilho | PRD completo após revisão rubrica P aprovada |
| Processamento | 1. Apresenta ao P.O.: Histórias, Regras, Termos, Decisões, No ELM, Revisão; 2. SE P.O. aprova: cada conceito elm/ recebe `status: stable` + `verified` humano; commit na BASE; 3. SE P.O. solicita ajustes: volta ao ciclo de escrita |
| Output | Artefatos elm/ com `status:stable` e `verified`; commit na BASE; sdd-elm modo requisitos + sdd-fatiar acionados |

#### Fluxo 3: Mudança depois de aprovado
| Campo | Descrição |
|---|---|
| Gatilho | Solicitação de alteração em PRD já com `status:stable` e commitado |
| Processamento | 1. Linha da decisão afetada em decisoes.md: situação → "substituída" + nova decisão; 2. Atualiza prd.md e/ou conceito elm/ afetado (status:stable removido); 3. Re-executa revisão rubrica P (≤2 rodadas); 4. Novo GATE com P.O.; 5. Pós-aprovação: novo `status:stable` + `verified` humano; novo commit na BASE |
| Output | Artefatos alterados com novo `status:stable`; decisoes.md com histórico de substituições; novo commit na BASE |

#### Fluxo 4: Alteração de artefato existente no ELM
| Campo | Descrição |
|---|---|
| Gatilho | Comportamento já documentado no ELM precisa ser alterado (sdd-elm modo similares encontrou relação "sobrepõe") |
| Processamento | 1. Copia arquivo do artefato do bundle para `elm/`, mantendo `resource`, `id`, `sources`; 2. Coloca `status: draft` + novo `generated`; 3. Reescreve no estado depois da mudança; 4. `sdd-elm` atualiza o artefato existente em vez de criar outro; 5. Na tabela do PRD, coluna "No ELM" = `altera <id>` |
| Output | Conceito elm/ com referência ao artefato ELM existente; publicação via sdd-elm atualiza o mesmo id |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | Descrição longa da demanda (texto livre) + nome do produto |
| Regra IF/THEN | IF pasta `<produto>/epicos/<EP>-<slug>/` não existe → cria + define EP-nn sequencial; IF bundle ELM acessível → sdd-elm modo similares ANTES de criar qualquer elm/; IF sdd-entrevistar não rodado → roda; aguarda decisoes.md; IF prd.md tem >~8 histórias → propõe dividir em dois épicos; IF HF referencia REG → usa link embed (nunca inline); IF revisão retornou AJUSTAR AND rodadas ≤ 2 → corrige e resubmete; IF P.O. aprova → aplica `status:stable` + `verified` em cada elm/; commit na BASE |
| Output Gerado | Pasta épico completa; backlog.md atualizado; commit na BASE; ativação de sdd-elm + sdd-fatiar |

#### Fluxo 2
| Campo | Descrição |
|---|---|
| Input Exato | prd.md + elm/ + resultado revisão rubrica P (aprovado após ≤2 rodadas) |
| Regra IF/THEN | IF revisão aprovada → apresenta ao P.O.; IF P.O. aprova → para CADA elm/: adiciona `status: stable` + campo `verified` com identificação humana; commit na BASE; IF P.O. solicita ajustes → retorna ao ciclo, conta nova rodada; IF commit ok → aciona sdd-elm + sdd-fatiar |
| Output Gerado | elm/*.md com `status:stable` e `verified`; commit na BASE |

#### Fluxo 3
| Campo | Descrição |
|---|---|
| Input Exato | Referência ao épico + especificação da mudança + artefatos com `status:stable` |
| Regra IF/THEN | IF artefato tem `status:stable` → remove `status:stable` antes de editar; IF decisão D afetada → D: situação="substituída"; append D' como nova; IF prd.md alterado → re-executa revisão (≤2 rodadas) + novo GATE P.O.; IF P.O. aprova → aplica `status:stable` + novo `verified`; novo commit na BASE |
| Output Gerado | Artefatos atualizados; decisoes.md com D (substituída) + D' (decidida); novo commit na BASE |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| 1 – PRD | `<produto>/epicos/<EP>-<slug>/prd.md` | `.md` — seções: histórias+cenários Gherkin, regras testáveis, termos | prd.md gravado; HF linka REG via embed | Pasta não existe → cria; se falhar → erro |
| 1 – decisões | `<produto>/epicos/<EP>-<slug>/decisoes.md` | `.md` — tabela de decisões (gerado via sdd-entrevistar) | decisoes.md gravado com decisões do épico | Pasta não existe → erro no sdd-entrevistar |
| 1 – histórias OKF | `<produto>/epicos/<EP>-<slug>/elm/HF-nn-<slug>.md` | `.md` — OKF v0.2; link embed para REG | Arquivo gravado; links para REG válidos | Pasta `elm/` não existe → cria; se falhar → erro |
| 1 – regras OKF | `<produto>/epicos/<EP>-<slug>/elm/REG-nn-<slug>.md` | `.md` — OKF v0.2: testável, com valores, uma por bloco, D-nn | Arquivo gravado | Pasta `elm/` inacessível → erro |
| 1 – glossário OKF | `<produto>/epicos/<EP>-<slug>/elm/GL-<termo>.md` | `.md` — definição OKF v0.2 | Um arquivo por termo | Pasta `elm/` inacessível → erro |
| 1 – index e log | `elm/index.md` e `elm/log.md` | `.md` | Ambos gravados junto com os elm/ | Pasta `elm/` inacessível → erro |
| 2 – GATE | Todos os `elm/*.md` | `.md` — campos `status: stable` + `verified: <identificação humana>` | Todos atualizados; commit na BASE | Qualquer elm/ não gravável → GATE incompleto; commit não realizado |
| 3 – mudança pós-aprovação | `elm/` afetados + decisoes.md | `.md` | Histórico preservado; `status:stable` removido até nova aprovação | decisoes.md ou elm/ não graváveis → alteração bloqueada |


---

## SKILL: sdd-fatiar

> **Papel:** Quebra o PRD aprovado em fatias verticais (tracer bullets) — cada fatia atravessa todas as camadas, tem cenários de aceite, tamanho P/M/G, modo AFK/HITL.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Novo Fatiamento
| Campo | Descrição |
|---|---|
| Gatilho | `"fatiar o PRD"`, `"quebrar em histórias"`, `"gerar o backlog"` — PRD com `status: aprovado` |
| Processamento | 1. Lê PRD inteiro + decisoes.md; 2. Se fatia mexe em módulos existentes: aciona sdd-pesquisador; 3. Monta tabela: `FT \| Título \| Cobre (HF·cenário) \| Bloqueada por \| Tam. \| Modo`; 4. Confere cobertura: todo cenário de toda história em exatamente uma fatia; 5. Exibe tabela + 3 perguntas (granularidade / dependências / AFK↔HITL) |
| Output | Tabela de fatias exibida ao P.O./time; aguarda ajuste ou "ok" |

#### Fluxo 2: GATE do Backlog
| Campo | Descrição |
|---|---|
| Gatilho | P.O. responde "ok" à tabela de fatias |
| Processamento | 1. `git switch <base>` + `git pull --ff-only`; 2. Grava backlog.md: épico `status: fatiado`, linhas das fatias (ids FT-nnn sequenciais), `status: pronta` (se passa DoR) ou `backlog` (com o que falta); 3. PRD: `status: fatiado`; 4. Commit na base (backlog.md + prd.md); 5. Pergunta horas da `[ESP]`; 6. sdd-elm modo horas + conclusão com confirmação (ou `ELM pendente` no rodapé do PRD) |
| Output | `backlog.md` gravado e comitado; PRD com `status: fatiado`; horas lançadas no ELM ou pendência registrada |

#### Fluxo 3: Refinamento (Dividir / Juntar / Nova Fatia)
| Campo | Descrição |
|---|---|
| Gatilho | `"refinar o backlog"`, `"FT-033 está grande demais"`, `"faltou uma fatia"` |
| Processamento | **Dividir**: original → `status: dividida` + `obs: substituida-por FT-x, FT-y`; novas herdam cobertura, dependências, épico; sdd-elm cria filhos no EWM. **Juntar**: só em `backlog`; a que some → `status: cancelada` + motivo. **Nova fatia**: exige PRD alterado via sdd-prd antes. **Sempre**: reconfere DoR de todas as fatias `backlog` |
| Output | backlog.md atualizado; EWM atualizado via sdd-elm |

#### Fluxo 4: Publicação EWM
| Campo | Descrição |
|---|---|
| Gatilho | GATE do backlog concluído ("ok") + iteração EWM informada |
| Processamento | 1. Chama sdd-elm modo backlog; 2. Cria épico no EWM se não existe; 3. Para cada fatia: cria IB com critérios de aceite + pai=épico + link "implementa" DOORS Next; 4. `Planejado para` = iteração indicada; 5. sdd-elm preenche coluna `elm` do backlog.md |
| Output | IBs criados no EWM vinculados ao épico e ao DOORS Next; backlog.md com coluna `elm` preenchida |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | `"fatiar o PRD"` + caminho do PRD com `status: aprovado` |
| Regra IF/THEN | IF `prd.status != "aprovado"` → para; IF fatia referencia módulo existente → aciona sdd-pesquisador; FOR cada história do PRD: cria ≥1 fatia cobrindo seus cenários; IF cenário sem fatia OR fatia sem cenário → bloqueia e corrige BEFORE exibir; IF tamanho > G → divide; IF critério já passa na base → erro "critério não falsificável"; IF tipo de trabalho novo → força Modo=HITL; THEN exibe tabela + 3 perguntas |
| Output Gerado | `"🍰 EP-03 — 3 fatias · 2 AFK · 1 HITL"` + tabela + 3 perguntas |

#### Fluxo 2
| Campo | Descrição |
|---|---|
| Input Exato | `"ok"` do P.O. à tabela de fatias |
| Regra IF/THEN | IF `git pull --ff-only` falha → interrompe; IF MCP ELM disponível → pergunta horas e chama sdd-elm modo horas + conclusão; IF MCP ELM indisponível → grava pendência no rodapé do PRD; IF especificação continua na próxima sprint → NÃO conclui [ESP] |
| Output Gerado | Confirmação de commit; mensagem de horas lançadas ou `ELM pendente` no PRD |

#### Fluxo 3
| Campo | Descrição |
|---|---|
| Input Exato | `"a FT-033 está grande demais"` (dividir) |
| Regra IF/THEN | IF operação=dividir AND `FT.status != "concluida"` → original vira `dividida`; cria novas; sdd-elm cria filhos; ELSE IF `FT.status == "concluida"` → recusa: mudança de comportamento entregue = fatia nova; AFTER → reconfere DoR |
| Output Gerado | Confirmação das mudanças em backlog.md + resultado da verificação DoR |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| GATE do Backlog | `<produto>/backlog.md` | `.md` — tabela markdown, uma fatia por linha | `git pull --ff-only` OK + "ok" + commit | Branch divergiu → interrompe; dir. inacessível → erro |
| GATE do Backlog | `<produto>/epicos/<EP>-<slug>/prd.md` | `.md` — frontmatter `status: fatiado` | Mesmo arquivo ainda acessível + sem lock | Arquivo renomeado/movido entre leitura e gravação → inconsistência |
| GATE (ELM pendente) | Rodapé do `prd.md` | `.md` | MCP ELM indisponível + arquivo acessível | Arquivo inacessível → pendência perdida |
| Refinamento | `<produto>/backlog.md` | `.md` | Fatia alvo em `backlog`/`pronta`; branch base; `git pull --ff-only` OK | Fatia em `concluida` → recusado; branch de fatia → gravação bloqueada (só na base) |
| Publicação EWM | Coluna `elm` em `<produto>/backlog.md` | `.md` — formato `[<id>](<url>)` | MCP ELM disponível + IBs criados | MCP ELM indisponível → coluna fica `pendente` |

---

## SKILL: sdd-planejamento

> **Papel:** Planejamento ágil — roadmap, acordos do time, sprint por capacidade, review, retrospectiva, virada. Publica no EWM via sdd-elm.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Modo Inicial (Acordos + Roadmap)
| Campo | Descrição |
|---|---|
| Gatilho | `"monta o planejamento"`, `"acordos do time"`, `"roadmap"` — primeiro uso |
| Processamento | 1. Verifica se `equipe.json` existe (se sim: exibe, pergunta só o que mudou; se não: coleta tudo); 2. Valida JSON contra `equipe.schema.json`; 3. Propõe `acordos.md` (cadência Scrum/Kanban, WIP, DoR, DoD, tamanhos, reserva de atendimento 20%); 4. Monta `roadmap.md` dos épicos do backlog.md — ordena por valor e risco; épico sem PRD como "a descobrir" |
| Output | `equipe.json`, `acordos.md`, `roadmap.md` gravados em `<produto>/planejamento/` após "ok" |

#### Fluxo 2: Modo Sprint
| Campo | Descrição |
|---|---|
| Gatilho | `"planejar a sprint"`, chamada automática na virada |
| Processamento | 1. Calcula capacidade (revisão humana, HITL, vazão média 3 últimas sprints, especificação, reserva de atendimento); 2. Define especificação (`[ESP]` por épico); 3. Confere DoR → grava `pronta`/`backlog`; seleciona respeitando `bloqueada-por`; atribui revisor/verificador ≠ implementador; 4. Define meta (frase de resultado de negócio); 5. Pergunta iteração EWM; 6. Exibe proposta 3 seções; 7. "ok" → grava `sprint-<nn>.md` + atualiza backlog.md + commit na base + **sempre** chama sdd-elm modo sprint |
| Output | `sprint-<nn>.md` criado; backlog.md atualizado; IBs e tarefas `[DEV][REV][VER][ESP]` no EWM |

#### Fluxo 3: Encaixe
| Campo | Descrição |
|---|---|
| Gatilho | sdd-iniciar redireciona para cá quando a fatia não está na sprint aberta |
| Processamento | 1. Exibe ao P.O.: fatia + capacidade restante; 2. Apresenta opções com recomendada: (a) entra na folga; (b) entra no lugar de FT-xxx; (c) próxima sprint; 3. Com decisão: atualiza backlog.md + sprint-<nn>.md + commit + sdd-elm; 4. Sem decisão: fatia não começa; 5. Volta a sdd-iniciar |
| Output | backlog.md e sprint-<nn>.md atualizados; tarefas no EWM; ou "sem decisão, sem início" |

#### Fluxo 4: Review
| Campo | Descrição |
|---|---|
| Gatilho | `"review da sprint"` |
| Processamento | Para cada fatia `concluida` da sprint: apresenta cenário entregue + evidência do verificacao.md; registra retorno do P.O. em `sprint-<nn>.md`; pedido novo → encaminha para sdd-prd/sdd-fatiar; nunca reabre fatia concluída |
| Output | Seção `## Review` do `sprint-<nn>.md` preenchida; novos pedidos encaminhados ao backlog |

#### Fluxo 5: Retrospectiva e Virada
| Campo | Descrição |
|---|---|
| Gatilho | `"virada de sprint"`, `"fechar a sprint"`, `"retrospectiva"` |
| Processamento | 1. sdd-aprender modo retrospectiva; 2. Preenche `## Retrospectiva` (bom/melhorar/ações); 3. sdd-elm modo horas → `## Números` (planejadas × lançadas); 4. Concluídas: vazão+pontos; não concluídas: migram para próxima (histórico preservado); 5. Recalcula vazão, velocidade, recalibra reserva de atendimento → `equipe.json` + `historico[]`; 6. sdd-elm modo sprint virada: `plannedFor` da nova iteração (pai não muda); 7. Aciona Modo Sprint para a próxima (migradas consomem capacidade primeiro) |
| Output | `sprint-<nn>.md` com `Situação: fechada`; `equipe.json` com nova entrada em `historico`; EWM atualizado; nova sprint planejada |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 2 — Sprint
| Campo | Descrição |
|---|---|
| Input Exato | `"planejar a sprint 4"` com equipe.json, acordos.md, backlog.md existentes |
| Regra IF/THEN | IF historico.length >= 3 → vazão = média das 3 últimas; ELSE IF > 0 → usa o que tem; ELSE → 1 fatia/dev/semana; FOR cada fatia no topo: IF DoR passa → status=pronta; ELSE → aponta o que falta, NÃO pula automaticamente; WHILE capacidade > 0: seleciona próxima `pronta` sem bloqueio; IF capacidade atingida → move restantes para "Fica de fora"; IF revisor == implementador → troca revisor |
| Output Gerado | `"🗓️ Sprint 4 · <datas> · meta: <…>"` + 3 seções + linha de capacidade + lista de FTs fora |

#### Fluxo 3 — Encaixe
| Campo | Descrição |
|---|---|
| Input Exato | sdd-iniciar redireciona com FT-041 (trilha padrão, tam M, AFK) não planejada na sprint 4 |
| Regra IF/THEN | Calcula capacidade restante; IF (revisao_restante - custo_revisao_FT-041) >= 0 AND (vazão_restante - 1) >= 0 → opção (a) "entra na folga"; IF existe FT não iniciada na sprint → opção (b) "entra no lugar de FT-xxx"; ALWAYS opção (c) "próxima sprint"; IF P.O. escolhe (b) → fatia retirada: sprint=— no backlog; IF sem decisão → "fatia não começa sem decisão do P.O." |
| Output Gerado | Opções com recomendada marcada + ação imediata após decisão |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Modo Inicial | `<produto>/planejamento/equipe.json` | `.json` (validado contra `equipe.schema.json`; chaves em kebab-case) | Schema válido + "ok" + commit | JSON inválido → recusa e lista os erros; dir. inexistente → cria |
| Modo Inicial | `<produto>/planejamento/acordos.md` | `.md` (DoR e DoD como checklists) | "ok" + commit | Conflito git → mantém remoto, reaplica |
| Modo Inicial | `<produto>/planejamento/roadmap.md` | `.md` — tabela Release \| Objetivo \| Épicos \| Previsão | backlog.md legível + "ok" | backlog.md ausente → roadmap sem épicos, com aviso |
| Modo Sprint | `<produto>/planejamento/sprints/sprint-<nn>.md` | `.md` — seções: Fatias, Especificação, Atendimento, Capacidade, Review, Retrospectiva, Números | "ok" + `git pull --ff-only` OK + commit | `sprints/` inexistente → cria; sdd-elm falha → `Tarefa ELM = pendente` |
| Modo Sprint | `<produto>/backlog.md` | `.md` — colunas sprint, responsavel, status atualizadas | `git pull --ff-only` OK + sem conflito | Conflito → mantém remoto, reaplica linha a linha |
| Encaixe | `sprint-<nn>.md` | `.md` — linha adicionada em Fatias + Observação de encaixe | Sprint aberta encontrada + decisão do P.O. | Sprint não encontrada ou fechada → bloqueia e informa |
| Retro/Virada | `equipe.json` | `.json` — nova entrada em `historico[]` | Dados de horas recebidos + schema válido + "ok" | sdd-elm indisponível → horas omitidas ou estimadas |


---

## SKILL: sdd-pesquisar

> **Papel:** Pesquisa do código somente leitura — localiza onde o comportamento mora, análogos, o que reaproveitar, schema real, restrições. Compacta em `research.md`.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Pesquisa por agente (sdd-pesquisador)
| Campo | Descrição |
|---|---|
| Gatilho | sdd-plano, sdd-loop ou sessão invoca o agente sdd-pesquisador com o ft-slug |
| Processamento | 1. Agente recebe ft-slug; 2. Lê status.md, backlog.md, PRD/ficha/defeito; 3. Formula 3–7 perguntas que o plano precisará responder; 4. Investiga: estrutura do projeto, fluxo atual (ponto de entrada→dado com arquivo:linha), análogos (1–2 funcionalidades do mesmo tipo com testes), o que reaproveitar, schema real via MCP de banco (somente leitura), documentação ELM vs código, como rodar testes da área; 5. Compacta em research.md (≤150 linhas); 6. **NÃO grava status.md** — quem chamou o agente faz esse registro |
| Output | `.kiro/specs/<ft>-<slug>/research.md` com 9 seções: Perguntas/Respostas, Fluxo atual, Análogos, Reaproveitar, Dados, Testes, Documentação×código, Restrições e riscos, Não encontrado |

#### Fluxo 2: Pesquisa pela sessão (sem agente)
| Campo | Descrição |
|---|---|
| Gatilho | Agente sdd-pesquisador não disponível; skill executada diretamente pela sessão |
| Processamento | Mesmos passos do Fluxo 1; com diferença: a sessão **também atualiza `status.md`** com a fase de pesquisa concluída |
| Output | `research.md` + atualização da fase em `status.md` |

#### Fluxo 3: Análogos (subtarefa durante investigação)
| Campo | Descrição |
|---|---|
| Gatilho | Durante a investigação, ao mapear funcionalidades do mesmo tipo já existentes no projeto |
| Processamento | 1. Localiza 1–2 funcionalidades existentes do mesmo tipo (glob/steering/MCP); 2. Identifica arquivos com arquivo:linha; 3. Localiza testes correspondentes; 4. Extrai padrões reutilizáveis; 5. Se nenhum análogo encontrado: registra em "Não encontrado" sem inventar |
| Output | Seção **Análogos** em research.md com referências arquivo:linha e ponteiros para testes vizinhos |

#### Fluxo 4: Banco de dados
| Campo | Descrição |
|---|---|
| Gatilho | Fatia envolve dados; durante o passo "Dados" da investigação |
| Processamento | 1. Verifica disponibilidade do MCP de banco; 2. Se disponível: consulta schema em somente leitura (tabelas, colunas, tipos, índices, chaves); 3. Registra com referência exata; 4. Se MCP indisponível: registra limitação em "Restrições e riscos" e "Não encontrado"; 5. **NUNCA** infere ou inventa colunas, tabelas ou relações |
| Output | Seção **Dados** com schema real ou flag explícito de impossibilidade |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | Invocação com ft-slug; contexto da fatia presente (status.md, backlog.md, PRD/ficha/defeito) |
| Regra IF/THEN | IF research.md já existe e está atual → retorna existente sem regravar; IF research.md não existe → executa investigação completa → grava; IF arquivo não for localizado durante investigação → registra em "Não encontrado" sem inventar; NEVER grava status.md; NEVER inventa arquivo, classe, coluna ou rota; ALWAYS somente leitura exceto pela gravação de research.md |
| Output Gerado | `research.md` com ≤150 linhas preenchendo as 9 seções obrigatórias |

#### Fluxo 4 — Banco de dados
| Campo | Descrição |
|---|---|
| Input Exato | MCP de banco configurado (ou ausente); fatia envolve dados |
| Regra IF/THEN | IF MCP de banco disponível → consulta somente leitura → registra schema real; IF MCP de banco indisponível → registra em "Restrições e riscos": "schema não verificado — MCP indisponível"; NEVER assume tipo de coluna ou nome de tabela sem confirmação do MCP |
| Output Gerado | Seção Dados com schema real, OU aviso explícito de limitação |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Por agente | `.kiro/specs/<ft>-<slug>/research.md` | `.md` — 9 seções, ≤150 linhas, fatos com arquivo:linha | Arquivo criado/sobrescrito com evidências verificadas | Dir. inexistente → erro; fallback: sessão executa no lugar do agente |
| Pela sessão | `.kiro/specs/<ft>-<slug>/research.md` | Idem | Idem acima | Sem permissão de escrita → fase não avança |
| Pela sessão (fase) | `.kiro/specs/<ft>-<slug>/status.md` | `.md` | Fase de pesquisa registrada no Histórico | Conflito de escrita → relê e re-aplica |
| Análogos | (seção interna de research.md) | n/a | Referências arquivo:linha verificadas | Análogo inventado → VIOLAÇÃO da regra "nunca invente" |
| Banco de dados | (seção interna de research.md) | n/a | Schema real com fonte registrada | MCP indisponível → seção "Restrições" obrigatória; coluna inventada → VIOLAÇÃO |


---

## SKILL: sdd-plano

> **Papel:** Planeja uma fatia no formato de spec do Kiro — pesquisa, requirements/bugfix, design, tasks. Análise independente (rubrica L). GATE do plano.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Plano padrão (feature)
| Campo | Descrição |
|---|---|
| Gatilho | `"planeja a FT-031"`, `"gera a spec"`, `"cria as tasks"` — fatia do tipo feature |
| Processamento | 1. Verifica se research.md existe → chama sdd-pesquisar se ausente; 2. Analisa research.md: lacuna de negócio → PARA → sdd-entrevistar; 3. Escolhas técnicas abertas → apresenta (HITL) ou decide e registra (AFK); 4. Cria `.config.kiro` com `specType: feature`; 5. Escreve `requirements.md` (critérios EARS falsificáveis na base); 6. Escreve `design.md` (pattern grounding, árvore de arquivos+ação, assinaturas, árvore de chamadas, pontos de teste, erros/transação, contrato de pronto, decisões técnicas); 7. Escreve `tasks.md` (uma tarefa por comportamento, teste primeiro, `_Requirements: N.M_`, ≤8 tarefas); 8. Limite: >200 linhas total ou >8 tarefas → propõe dividir; 9. sdd-revisor rubrica L → `analise-plano-<N>.md`; 10. AJUSTAR → corrige (≤2 rodadas); OK → GATE |
| Output | `.config.kiro`, `requirements.md`, `design.md`, `tasks.md`, `analise-plano-<N>.md`, `status.md` atualizado |

#### Fluxo 2: Plano trilha rápida (bugfix)
| Campo | Descrição |
|---|---|
| Gatilho | Fatia classificada como bugfix |
| Processamento | 1–3: Mesmos passos; 4. `.config.kiro` com `specType: bugfix`; 5. Escreve `bugfix.md` (comportamento esperado, passo a passo, o que não muda) — **não** `requirements.md`; 6. Escreve `design.md` e `tasks.md`; 7. Análise rubrica L; 8. GATE opcional conforme sdd.md |
| Output | `.config.kiro`, `bugfix.md`, `design.md`, `tasks.md`, `analise-plano-<N>.md`, `status.md` |

#### Fluxo 3: GATE do plano — HITL
| Campo | Descrição |
|---|---|
| Gatilho | Plano completo + análise OK + modo HITL |
| Processamento | 1. Exibe resumo do plano; 2. `status.md` → `plano-em-revisao`; 3. **PAUSA incondicional** aguardando resposta humana; 4. Aprovado → `fase: implementando` + commit de todos os artefatos |
| Output | Commit com todos os artefatos; `status.md` fase=implementando |

#### Fluxo 4: GATE do plano — AFK
| Campo | Descrição |
|---|---|
| Gatilho | Plano completo + análise OK + modo AFK |
| Processamento | Se AFK com "análise basta": ANALISE OK é suficiente → avança sem pausa. Se AFK com "aprovação humana": pausa em `plano-em-revisao` mesmo em modo autônomo. Quando aprovado (por qualquer via): `fase: implementando` + commit |
| Output | Mesmo do GATE HITL; diferença é a condição de disparo do avanço |

#### Fluxo 5: Replanejamento
| Campo | Descrição |
|---|---|
| Gatilho | Implementação descobriu que o plano não serve (divergência esperado × encontrado) |
| Processamento | 1. Lê tasks.md atual; identifica tarefas prontas (mantém [x]); 2. **NUNCA desmarca** tarefas prontas; 3. Atualiza design.md só no que mudou; 4. Adiciona novas tarefas (nunca modifica as existentes prontas); 5. Registra motivo no Histórico; 6. Repete Passos 9–10 (nova análise rubrica L + novo GATE) para a parte alterada |
| Output | `design.md` e `tasks.md` com diff mínimo + novo `analise-plano-<N>.md` + Histórico atualizado |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Plano padrão
| Campo | Descrição |
|---|---|
| Input Exato | Comando com ft-slug; pasta `.kiro/specs/<ft>-<slug>/` acessível |
| Regra IF/THEN | IF research.md ausente → chama sdd-pesquisar → aguarda → prossegue; IF lacuna de negócio detectada → PARA → sdd-entrevistar; IF escolha técnica + HITL → apresenta opções; IF escolha técnica + AFK → decide e documenta; IF total > 200 linhas OR tasks.md > 8 tarefas → propõe dividir (não prossegue automaticamente); IF ANALISE: AJUSTAR AND rodadas ≤ 2 → corrige e reenvia; IF ANALISE: OK → avança para GATE |
| Output Gerado | `requirements.md` + `design.md` + `tasks.md` com _Requirements: N.M_ + `analise-plano-<N>.md` |

#### Fluxo 3 — GATE HITL
| Campo | Descrição |
|---|---|
| Input Exato | Plano finalizado + ANALISE: OK + modo HITL |
| Regra IF/THEN | IF modo HITL → SEMPRE exibe resumo e pausa; NEVER avança sem resposta humana explícita; IF aprovado → fase=implementando + commit; IF pedido ajuste → retorna à correção; IF rejeitado → descarta plano + registra motivo no Histórico |
| Output Gerado | `status.md` fase=implementando + commit atômico dos artefatos |

#### Fluxo 5 — Replanejamento
| Campo | Descrição |
|---|---|
| Input Exato | tasks.md com tarefa [x]; pedido de atualização do plano |
| Regra IF/THEN | IF tarefa marcada como pronta → NEVER desmarcar; IF mudança requerida em tarefa pronta → adicionar nova tarefa substituta, nunca editar a existente; IF mudança em design.md → diff mínimo; THEN novo analise-plano com N incrementado; THEN GATE repetido (conforme modo HITL/AFK) |
| Output Gerado | `design.md` e `tasks.md` com diff mínimo + `analise-plano-<N>.md` + Histórico com "replanejar" |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Padrão | `.kiro/specs/<ft>-<slug>/.config.kiro` | Formato spec Kiro (`specType: feature`) | Criado na primeira; não sobrescreve se já existe | Dir. inexistente → cria; conflito de tipo → alerta |
| Padrão | `.kiro/specs/<ft>-<slug>/requirements.md` | `.md` — critérios EARS falsificáveis, referenciáveis por N.M | Todos os critérios referenciáveis | Sem permissão → bloqueia todo o plano |
| Padrão | `.kiro/specs/<ft>-<slug>/design.md` | `.md` — seções: pattern grounding, árvore de arquivos+ação, assinaturas, árvore de chamadas, pontos de teste, erros/transação, contrato de pronto, decisões técnicas | Todas as seções obrigatórias presentes | Seção ausente → ANALISE: AJUSTAR pelo revisor |
| Padrão | `.kiro/specs/<ft>-<slug>/tasks.md` | `.md` — ≤8 tarefas com `_Requirements: N.M_` e comando de pronto | Rastreabilidade para requirements.md | >8 tarefas sem proposta de divisão → VIOLAÇÃO do limite |
| Rápida | `.kiro/specs/<ft>-<slug>/bugfix.md` | `.md` — comportamento esperado + passo a passo + o que não muda | Arquivo gravado; requirements.md NÃO criado | requirements.md gravado no lugar → VIOLAÇÃO de tipo |
| Análise | `.kiro/specs/<ft>-<slug>/analise-plano-<N>.md` | `.md` — rubrica L completa com ANALISE: OK ou AJUSTAR | sdd-revisor disponível + arquivo criado | sdd-revisor indisponível → plano não avança para GATE |
| GATE | `.kiro/specs/<ft>-<slug>/status.md` | `.md` — fase transicionada + entrada no Histórico | Transição ok + commit atômico após aprovação | Conflito de escrita → relê, re-aplica |


---

## SKILL: sdd-implementar

> **Papel:** Implementa uma fatia a partir do plano aprovado — uma tarefa por vez, ciclo TDD (vermelho→verde→refatorar), backpressure; revisão independente; PR.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: TDD Normal (tarefa a tarefa)
| Campo | Descrição |
|---|---|
| Gatilho | tasks.md com item não marcado; branch correta; testes passando antes de qualquer mudança |
| Processamento | 1. Carrega skill do toolkit; 2. Vermelho: escreve teste que falha pelo motivo certo (ponto de teste do design.md); 3. Verde: menor mudança que faz passar; 4. Arrumar: refatora o que acabou de escrever; 5. Backpressure: compilar + testes da área + lint; 6. Marca [x]; 7. Commit atômico; 8. Linha no Histórico do status.md; 9. Repete |
| Output | tasks.md com itens [x]; commits por tarefa; status.md com Histórico atualizado |

#### Fluxo 2: Revisão e Correção de Achados
| Campo | Descrição |
|---|---|
| Gatilho | Todos os itens [x]; validação completa (compilar + suíte inteira + lint + cobertura) passou |
| Processamento | 1. `status.md` → `fase: revisando`; 2. Dispara sdd-revisor subagente rubrica C; 3. Subagente grava `revisao-codigo-N.md`; 4. APROVADO → avança para sdd-verificar; 5. REVISAR → corrige e submete rodada 2; 6. REVISAR na 2ª rodada → `fase: bloqueada`, para |
| Output | `revisao-codigo-N.md`; status.md fase atualizada |

#### Fluxo 3: Divergência Código ≠ Plano
| Campo | Descrição |
|---|---|
| Gatilho | Código real encontrado diverge do que o design.md especifica |
| Processamento | 1. PARA imediatamente; 2. Registra: "Esperado: <plano> · Encontrado: <código, arquivo:linha> · Por que importa: <o que muda>"; 3. Muda comportamento de negócio → P.O. (sdd-entrevistar/sdd-prd); muda o desenho → sdd-plano (replanejar); decisão técnica equivalente → decide e registra em design.md |
| Output | Registro da divergência; implementação pausada |

#### Fluxo 4: Trilha Direta (sem spec)
| Campo | Descrição |
|---|---|
| Gatilho | Sem spec nem tasks.md; pedido direto de mudança pontual |
| Processamento | 1. Teste que falha (se comportamento); 2. Menor mudança que faz passar; 3. Backpressure; 4. sdd-revisar rubrica C sobre o diff (com o pedido no lugar dos critérios; relatório na conversa); 5. PR curto: `FT-<nnn> — <pedido> (<id | —>)` |
| Output | PR com diff revisado e aprovado; `status.md` fase pr-aberto |

#### Fluxo 5: Abertura de PR
| Campo | Descrição |
|---|---|
| Gatilho | sdd-verificar retornou ACEITO; `status.md` fase aceita |
| Processamento | 1. Branch atualizada em relação à base? (`git fetch` + compare); 2. Compõe texto do PR (FT-nnn, O quê, Cobre, Plano, Revisão, Aceite, Backpressure, Banco DDL, Como ler, Reversível?); 3. Aguarda confirmação da pessoa; 4. Push + abertura do PR; 5. `status.md` → `fase: pr-aberto` |
| Output | PR aberto; `status.md` fase pr-aberto |

#### Fluxo 6: Modo Autônomo (AUTONOMO=true)
| Campo | Descrição |
|---|---|
| Gatilho | AUTONOMO=true definido na invocação (pelo sdd-orquestrador/sdd-loop) |
| Processamento | 1. Executa todos os passos sem perguntas; 2. **NÃO** faz push; 3. **NÃO** abre PR; 4. Bloqueio → `fase: bloqueada` e para |
| Output | Implementação completa sem interação; branch local atualizada; sem PR |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — TDD Normal
| Campo | Descrição |
|---|---|
| Input Exato | tasks.md com `- [ ] 1.1 Criar endpoint POST /usuarios`; branch limpa; testes passando |
| Regra IF/THEN | IF item não marcado existe → carrega toolkit → escreve teste falhando → escreve código mínimo → IF teste passa → refatora → IF backpressure OK → marca [x] → commit → próximo item; ELSE IF backpressure falha → corrige antes de marcar |
| Output Gerado | Commit `feat: 1.1 criar endpoint`; tasks.md `- [x] 1.1`; linha em status.md |

#### Fluxo 3 — Divergência
| Campo | Descrição |
|---|---|
| Input Exato | design.md diz "campo `cpf` obrigatório"; código encontrado não valida `cpf` |
| Regra IF/THEN | IF código real ≠ especificação do design.md → PARA → registra divergência (onde no plano vs. onde no código, arquivo:linha) → não edita nem avança |
| Output Gerado | Mensagem de divergência registrada; nenhuma tarefa marcada; nenhum commit |

#### Fluxo 5 — Abertura de PR
| Campo | Descrição |
|---|---|
| Input Exato | `status.md` fase `aceita`; branch `ft-42-usuarios`; base `main` |
| Regra IF/THEN | IF fase=aceita → verifica `git log origin/main..HEAD` → IF atualizada → compõe texto PR → aguarda confirmação → IF confirmado → push → abre PR → status.md fase `pr-aberto`; ELSE IF não confirmado → aguarda |
| Output Gerado | PR aberto; `status.md` fase `pr-aberto` |

#### Fluxo 6 — Modo Autônomo
| Campo | Descrição |
|---|---|
| Input Exato | Invocação com AUTONOMO=true; tasks.md com itens pendentes |
| Regra IF/THEN | IF AUTONOMO=true → executa TDD sem perguntas → IF bloqueio → status.md `fase: bloqueada` → para → NÃO executa push → NÃO abre PR mesmo com ACEITO |
| Output Gerado | Commits locais; status.md atualizado; sem push; sem PR |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| TDD — status | `.kiro/specs/<ft>-<slug>/status.md` | `.md` | Linha de Histórico gravada após cada commit de tarefa | Dir. `.kiro/specs/<ft>-<slug>/` inexistente → erro |
| TDD — código | Caminhos conforme tasks.md | variável | Arquivos criados/modificados conforme especificado | Caminho do projeto inacessível |
| Revisão — relatório | `.kiro/specs/<ft>-<slug>/revisao-codigo-<N>.md` | `.md` — VEREDITO na última linha | Arquivo criado pelo sdd-revisor com VEREDITO: APROVADO ou REVISAR | Subagente sem permissão de escrita |
| PR — status | `.kiro/specs/<ft>-<slug>/status.md` | `.md` | Fase `pr-aberto` + link do PR | Git push falha → fase não atualizada |

---

## SKILL: sdd-revisar

> **Papel:** Revisão independente com contexto limpo — julga artefato contra sua fonte, escreve **apenas** o relatório, não edita nada, não faz commit.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Rubrica P (PRD)
| Campo | Descrição |
|---|---|
| Gatilho | Pedido de revisão de PRD; artefatos: prd.md, elm/, decisoes.md, glossário, bundle ELM |
| Processamento | 1. Lê PRD com contexto limpo (sem explicação de quem fez); 2. Cruza cada item: cenário → origem (D-nn); regra → testável e com valor; histórias → coerentes com glossário e bundle ELM; 3. Calibra severidade via licoes.md (causa `revisao-branda` → sobe severidade); 4. Grava `revisao-prd-N.md` com RESULTADO: PRONTO / AJUSTAR |
| Output | `revisao-prd-<N>.md` com RESULTADO na última linha |

#### Fluxo 2: Rubrica L (Plano da Fatia)
| Campo | Descrição |
|---|---|
| Gatilho | Pedido de análise do plano; artefatos: research.md, requirements/bugfix.md, design.md, tasks.md, PRD, código, steering |
| Processamento | 1. Lê todos os artefatos com contexto limpo; 2. Cruza: tasks.md → design.md → requirements.md → PRD (rastreabilidade); verifica que design.md cita análogos do research.md; 3. Calibra por licoes.md; 4. Grava `analise-plano-N.md` com ANALISE: OK / AJUSTAR |
| Output | `analise-plano-<N>.md` com ANALISE na última linha |

#### Fluxo 3: Rubrica C (Código da Fatia)
| Campo | Descrição |
|---|---|
| Gatilho | Pedido de revisão de código; artefatos: `git diff origin/<base>...HEAD`, pasta da fatia, PRD |
| Processamento | 1. Obtém diff; 2. **Executa** backpressure (compilar+testes+lint) — não confia em "os testes passaram"; 3. Verifica diff por testes removidos/enfraquecidos (@Disabled, skip, assertTrue(true), asserts apagados, catch vazio); 4. Analisa dois eixos separados: conformidade com spec (C1-C5) e padrões/qualidade (C6-C10); 5. Calibra por licoes.md; 6. Grava `revisao-codigo-N.md` |
| Output | `revisao-codigo-<N>.md` com VEREDITO: APROVADO / REVISAR |

#### Fluxo 4: Rubrica C sobre Diff (Trilha Direta)
| Campo | Descrição |
|---|---|
| Gatilho | Revisão de diff pontual sem spec formal; pedido substitui os critérios |
| Processamento | 1. Lê o diff; 2. Usa o pedido como critério no lugar da spec; 3. Verifica testes removidos/enfraquecidos; 4. Produz relatório **apenas na conversa** (sem gravar arquivo) |
| Output | Relatório inline na conversa; sem arquivo gravado |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Rubrica P
| Campo | Descrição |
|---|---|
| Input Exato | PRD do épico EP-07; elm/ com conceitos; decisoes.md; glossário; bundle ELM |
| Regra IF/THEN | IF licoes.md com causa `revisao-branda` → sobe severidade do achado correspondente; IF zero BLOQUEANTE AND zero IMPORTANTE → RESULTADO=PRONTO; ELSE → RESULTADO=AJUSTAR; grava revisao-prd-N.md |
| Output Gerado | `revisao-prd-1.md` com RESULTADO na última linha |

#### Fluxo 3 — Rubrica C
| Campo | Descrição |
|---|---|
| Input Exato | `git diff origin/main...HEAD`; pasta `src/usuarios/`; PRD; licoes.md |
| Regra IF/THEN | IF executa backpressure → IF testes falham → BLOQUEANTE; IF teste removido/enfraquecido no diff → BLOQUEANTE; IF zero BLOQUEANTE AND zero IMPORTANTE → VEREDITO=APROVADO; ELSE → VEREDITO=REVISAR; grava revisao-codigo-N.md |
| Output Gerado | `revisao-codigo-1.md` com VEREDITO: REVISAR e achado BLOQUEANTE explicado |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Rubrica P | `<produto>/epicos/<EP>-<slug>/revisao-prd-<N>.md` | `.md` — RESULTADO na última linha | Arquivo criado com evidência por item | Dir. do épico inexistente → erro |
| Rubrica L | `.kiro/specs/<ft>-<slug>/analise-plano-<N>.md` | `.md` — ANALISE e rastreabilidade item a item | Arquivo criado com ANALISE na última linha | `.kiro/specs/<ft>-<slug>/` não existe → erro |
| Rubrica C | `.kiro/specs/<ft>-<slug>/revisao-codigo-<N>.md` | `.md` — VEREDITO após backpressure concluído | Arquivo criado com VEREDITO na última linha | Backpressure não executa (ambiente quebrado) → revisão incompleta |
| Rubrica C trilha direta | Nenhum arquivo gravado | — | Relatório apenas na conversa | Não aplicável (sem persistência intencional) |
| Workflows (opcional) | `.kiro/local/wf/<id>/plano.json` ou `codigo.json` | `.json` — `{"resultado": "OK"}` ou `{"veredito": "APROVADO"}` | Gravado apenas se workflow solicitar explicitamente | Dir. `.kiro/local/wf/<id>/` inexistente |


---

## SKILL: sdd-verificar

> **Papel:** Verificação de aceite de ponta a ponta — executa cada cenário na aplicação real (API, job batch, browser, carga); gera CT.csv para o ETM.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Verificação Backend
| Campo | Descrição |
|---|---|
| Gatilho | Fase `verificando`; tipo de projeto backend (API HTTP); revisão APROVADO |
| Processamento | 1. `status.md` → `fase: verificando`; 2. Escreve `verificacao.md` **ANTES** de executar (cenário, massa, executar, esperado, verificar em); 3. Sobe aplicação (comando do sdd.md); 4. Executa scripts de massa (banco somente leitura); 5. Para cada cenário: HTTP via `sh .kiro/sdd/http.sh` (ou curl) → captura resposta → verifica estado no banco → registra ✅/❌/⚠️ + obtido + evidência |
| Output | `verificacao.md` com resultados por cenário |

#### Fluxo 2: Verificação Batch
| Campo | Descrição |
|---|---|
| Gatilho | Fase `verificando`; tipo de projeto batch (job Spring Batch ou similar) |
| Processamento | 1. Escreve `verificacao.md`; 2. Sobe aplicação; 3. Scripts de massa; 4. Executa job; 5. Verifica status de saída + contagens (registros processados, rejeitados); 6. Registra ✅/❌/⚠️ por cenário |
| Output | `verificacao.md` com status do job e contagens por cenário |

#### Fluxo 3: Verificação Frontend
| Campo | Descrição |
|---|---|
| Gatilho | Fase `verificando`; tipo de projeto frontend (browser) |
| Processamento | 1. Escreve `verificacao.md`; 2. Sobe aplicação; 3. Scripts de massa; 4. Abre browser via Playwright ou MCP browser; 5. Executa cada cenário; 6. Captura screenshot em `evidencias/`; 7. Registra ✅/❌/⚠️ + caminho do screenshot |
| Output | `verificacao.md` + screenshots em `.kiro/specs/<ft>-<slug>/evidencias/` |

#### Fluxo 4: ACEITO + CT.csv
| Campo | Descrição |
|---|---|
| Gatilho | Todos os cenários com resultado ✅ |
| Processamento | 1. Decisão ACEITO; 2. Gera `CT.csv` (um caso por cenário verificado); 3. `status.md` → `fase: aceita`; 4. Registra horas da `[VER]`; 5. sdd-elm modo horas + conclusão na `[VER] FT-nnn` com confirmação (ou `ELM pendente` no Histórico se sem MCP) |
| Output | `CT.csv`; `status.md` fase `aceita`; horas lançadas no ETM ou pendência registrada |

#### Fluxo 5: REJEITADO
| Campo | Descrição |
|---|---|
| Gatilho | Ao menos um cenário com ❌ |
| Processamento | 1. Decisão REJEITADO; 2. Registra achados no `status.md` (esperado × obtido + evidência); 3. `status.md` → `fase: implementando`; 4. sdd-implementar corrige (só os rejeitados + repetição); nova rodada de verificação |
| Output | `status.md` com achados e fase `implementando`; ciclo de correção reiniciado |

#### Fluxo 6: Bloqueio por Ambiente
| Campo | Descrição |
|---|---|
| Gatilho | Campo Banco do `status.md` = `pendente` OU todos os cenários com ⚠️ |
| Processamento | IF banco pendente → **PARA** antes de executar qualquer cenário; IF apenas ⚠️ → `status.md` → `fase: bloqueada` |
| Output | `status.md` fase `bloqueada` com motivo; **nenhuma** decisão ACEITO/REJEITADO emitida |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 4 — ACEITO + CT.csv
| Campo | Descrição |
|---|---|
| Input Exato | `verificacao.md` com CT-01 ✅, CT-02 ✅, CT-03 ✅ |
| Regra IF/THEN | IF todos os cenários = ✅ → ACEITO → gera CT.csv (id, cenário, resultado, evidência por linha) → status.md fase `aceita` → calcula horas de [VER] → IF MCP ELM disponível → sdd-elm horas+conclusão; ELSE → `ELM pendente: lançar <h>h em [VER] FT-nnn` no Histórico |
| Output Gerado | `CT.csv` com N linhas; `status.md` fase `aceita`; sdd-elm acionado ou pendência registrada |

#### Fluxo 5 — REJEITADO
| Campo | Descrição |
|---|---|
| Input Exato | `verificacao.md` com CT-01 ✅, CT-02 ❌ (obtido: 500 em vez de 201), CT-03 ✅ |
| Regra IF/THEN | IF qualquer cenário = ❌ → REJEITADO → registra em status.md: "CT-02 falhou: <esperado × obtido>" → status.md fase `implementando` → sdd-implementar corrige; NUNCA gera CT.csv |
| Output Gerado | `status.md` com achado de CT-02; fase `implementando`; nenhum CT.csv |

#### Fluxo 6 — Bloqueio
| Campo | Descrição |
|---|---|
| Input Exato | Banco Oracle não responde ao ping; ou todos os cenários retornam ⚠️ |
| Regra IF/THEN | IF banco indisponível BEFORE execução → PARA → registra "banco pendente" → fase `bloqueada`; ELSE IF todos ⚠️ AFTER execução → fase `bloqueada`; NÃO emite ACEITO nem REJEITADO |
| Output Gerado | `status.md` fase `bloqueada` com motivo (banco ou ambiente instável); zero CT.csv |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Backend/Batch/Frontend — roteiro | `.kiro/specs/<ft>-<slug>/verificacao.md` | `.md` — seções por cenário com Massa, Executar, Esperado, Verificar em | Criado ANTES da execução; resultados preenchidos linha a linha | Dir. inexistente → não inicia execução |
| Frontend — screenshots | `.kiro/specs/<ft>-<slug>/evidencias/ft-<nnn>-<n.n>.png` | `.png` | Screenshot gravado após cada cenário de browser | Playwright falha ou dir. `evidencias/` sem permissão |
| ACEITO — CT.csv | `.kiro/specs/<ft>-<slug>/CT.csv` | `.csv` — id, cenário, resultado, evidência | Gerado somente quando ACEITO | REJEITADO → arquivo NÃO gerado |
| ACEITO/REJEITADO — status | `.kiro/specs/<ft>-<slug>/status.md` | `.md` | Fase e Histórico atualizados | Arquivo não gravável → fase não atualizada |
| Evidência com dado real | `.kiro/local/verificacao/<ft>/` | variável | Gravado fora do git para dados reais de produção/homologação | Dir. `.kiro/local/` não existe → erro; dados NÃO vão para o git |


---

## SKILL: sdd-consolidar

> **Papel:** Fecha a fatia depois do merge do PR — verifica drift, atualiza documentação as-built, publica no ELM, conclui itens do EWM, registra lições.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Principal (todas as etapas)
| Campo | Descrição |
|---|---|
| Gatilho | PR mergeado confirmado; `"PR mergeado"`, `"fecha a FT-031"`, `"consolidar"` |
| Processamento | Confirma merge → `git switch <base>` + `git pull --ff-only`. **P1 Drift**: compara design.md→Decisões técnicas, verificacao.md, decisoes.md vs bundle ELM — separa drift de negócio (→ sdd-prd antes de publicar) de drift técnico (nada no PRD). **P2 ELM** (uma confirmação, via sdd-elm): publica/atualiza requisitos; ficha as-built; ET as-built (opcional); CT.csv no ETM; horas [DEV] e [REV]; conclui tarefas e IB do backlog. **P3 Conhecimento**: cria ADRs de decisões "Vira ADR? sim"; adiciona termos pendentes ao glossário; lint de contradições. **P4 Fechar na BASE**: `status.md` fase `concluida`; `backlog.md` com `status: concluida` + `concluida-em` + elm ids; épico concluído se todas as fatias concluídas; sdd-aprender para cada correção humana. **P5 Próximo**: resumo ✅ |
| Output | `status.md` (fase: concluida); `backlog.md` atualizado; ELM publicado; ADRs/glossário gravados; resumo ✅ |

#### Fluxo 2: Trilha Direta
| Campo | Descrição |
|---|---|
| Gatilho | Fatia mergeada identificada como trilha direta (sem design.md, verificacao.md, decisoes.md) |
| Processamento | Pula P1, P3 (não existem); executa apenas: horas + backlog do P2 e o P4 |
| Output | `status.md` (fase: concluida); `backlog.md` com horas e IB concluídos; sem ET, ADR ou glossário |

#### Fluxo 3: Sem MCP ELM
| Campo | Descrição |
|---|---|
| Gatilho | P2 tenta invocar sdd-elm → MCP retorna erro/timeout |
| Processamento | Para cada ação ELM bloqueada: registra `ELM pendente: <ação>` no Histórico do `status.md`; prossegue nos demais passos; sdd-status lista as pendências em consultas futuras |
| Output | `status.md` com pendências ELM no Histórico; todos os artefatos locais gravados normalmente |

#### Fluxo 4: Drift de Negócio Detectado
| Campo | Descrição |
|---|---|
| Gatilho | P1: divergência entre decisoes.md/design.md e bundle ELM classificada como **negócio** |
| Processamento | Pausa P2; invoca sdd-prd com contexto do drift; aguarda sdd-prd concluir PRD atualizado; retoma P2 com base no PRD corrigido |
| Output | PRD atualizado via sdd-prd; ELM publicado com dados consistentes |

#### Fluxo 5: ADRs e Glossário
| Campo | Descrição |
|---|---|
| Gatilho | design.md contém decisão com "Vira ADR? sim" E/OU decisoes.md contém `[termo pendente]` |
| Processamento | **ADR**: cria `docs/adr/ADR-<nnn>.md` (contexto · decisão · consequências · origem FT-nnn). **Glossário**: append em `docs/glossario.md`. **Lint**: varre contradições entre glossário, ADRs, bundle ELM e steering — reporta se encontrar |
| Output | `docs/adr/ADR-<nnn>.md` criado; `docs/glossario.md` atualizado; relatório de lint |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1
| Campo | Descrição |
|---|---|
| Input Exato | `"consolidar fatia FT-042"` — backlog.md `status: pr-aberto`; PR #17 confirmado mergeado |
| Regra IF/THEN | IF status=pr-aberto AND PR mergeado → executar P1→P5; IF drift_negócio detectado → pausar → sdd-prd → retomar P2; IF sdd-elm indisponível → registrar pendência e continuar; IF "Vira ADR? sim" → criar ADR; IF todas fatias do épico concluídas → marcar épico; ELSE → seguir fluxo linear |
| Output Gerado | `status.md: fase: concluida` → `backlog.md` com elm ids → resumo: `✅ FT-042 concluída — ELM: publicado, Drift: nenhum, Épico: em andamento, Lições: 0` |

#### Fluxo 3 — Sem MCP ELM
| Campo | Descrição |
|---|---|
| Input Exato | P2 tenta `sdd-elm publicar requisitos FT-042` → `ConnectionError: ELM unreachable` |
| Regra IF/THEN | IF sdd-elm retorna erro → para CADA ação: append `ELM pendente: <ação>` em `status.md → Histórico`; THEN continuar P3 e P4 normalmente; NÃO bloquear conclusão da fatia |
| Output Gerado | `status.md` com seção de pendências ELM; demais artefatos locais gravados; resumo ✅ com nota `ELM: pendente` |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Principal | `.kiro/specs/<ft>-<slug>/status.md` | `.md` | Campo `fase: concluida` gravado na BASE | Dir. spec não existe → erro; interrompe fluxo |
| Principal | `<produto>/backlog.md` | `.md` | `status: concluida`, `concluida-em`, `elm-ids` preenchidos | `backlog.md` não encontrado na BASE |
| Principal | `<produto>/epicos/<EP>-<slug>/prd.md` | `.md` | Épico marcado concluído quando todas as fatias concluídas | Pasta do épico não localizada |
| Sem MCP ELM | `.kiro/specs/<ft>-<slug>/status.md` | `.md` | Pendências ELM registradas no Histórico | `status.md` inacessível → pendências perdidas |
| ADRs | `docs/adr/ADR-<nnn>.md` | `.md` | ADR criado com contexto, decisão, consequências, origem FT-nnn | `docs/adr/` não existe → criar dir. ou reportar erro |
| Glossário | `docs/glossario.md` | `.md` | Novo termo em append | Arquivo inexistente ou sem permissão de escrita |

---

## SKILL: sdd-aprender

> **Papel:** Aprendizado composto — transforma cada correção humana em melhoria permanente. Registra lição, propõe promoção para Regras aprendidas do sdd.md, faz retrospectiva com dados.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Modo Registrar
| Campo | Descrição |
|---|---|
| Gatilho | Correção humana: achado de revisão que chegou ao humano; cenário rejeitado; PR com mudança pedida; pessoa diz "não é assim"; bloqueio por falta de informação |
| Processamento | 1. Coleta fatos: o que foi feito (arquivo:linha) × o que era o certo × onde a informação certa estava; 2. Classifica causa em 7 categorias; 3. Grava `## L-<nnn> · <data> · FT-<nnn> · <causa>` em `licoes.md`; 4. Verifica se é 2ª ocorrência → propõe modo promover |
| Output | Nova entrada L-nnn appendada em `licoes.md`; se 2ª ocorrência: proposta de promoção exibida |

#### Fluxo 2: Modo Promover
| Campo | Descrição |
|---|---|
| Gatilho | 2ª ocorrência do mesmo tipo de erro OU usuário pede promoção explicitamente |
| Processamento | 1. Formula regra R-nn: curta, imperativa, com exemplo, `aplica-a`, `severidade`; 2. Gera diff da seção "Regras aprendidas" do `sdd.md`; 3. Apresenta diff e aguarda confirmação; 4. Somente com "ok": grava em `.kiro/steering/sdd.md` |
| Output | Diff exibido; com "ok" → seção "Regras aprendidas" do `sdd.md` atualizada com R-nn |

#### Fluxo 3: Modo Retrospectiva
| Campo | Descrição |
|---|---|
| Gatilho | Fim de fatia, épico ou sprint; pessoa solicita retrospectiva |
| Processamento | 1. Coleta métricas (fatias concluídas, lead time médio, rodadas de revisão, retrabalho, AFK/HITL); 2. Analisa fontes: `status.md` das fatias, `revisao-*.md`, `verificacao.md`, `licoes.md`, `backlog.md`; 3. Grava retrospectiva em `licoes.md`; 4. Termina perguntando quais propostas aplicar |
| Output | Entrada retro appendada em `licoes.md` com métricas; eventual proposta de R-nn |

#### Fluxo 4: Skill Desatualizada
| Campo | Descrição |
|---|---|
| Gatilho | Modo registrar classifica causa como `skill-desatualizada` |
| Processamento | 1. Grava lição em `licoes.md` com causa `skill-desatualizada`; 2. Identifica qual skill do toolkit está desatualizada; 3. Emite aviso ao mantenedor da skill; 4. **Não** corrige a skill diretamente; 5. **Não** gera regra R-nn (causa `skill-desatualizada` não vira regra) |
| Output | Entrada L-nnn em `licoes.md`; aviso ao mantenedor; nenhuma R-nn |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Modo Registrar
| Campo | Descrição |
|---|---|
| Input Exato | Usuário: "o relatório devia ser JSON, não XML" — localização: `src/report.py:42`; informação certa estava em `docs/api-contract.md` |
| Regra IF/THEN | IF evento=correção_humana → extrair (feito vs. certo, arquivo:linha, onde estava a informação) → classificar causa → determinar nnn (max existente + 1) → append em `licoes.md`; IF mesma causa já em licoes.md E count >= 2 → propor modo promover; ELSE → registrar sem proposta |
| Output Gerado | `## L-001 · 2026-10-15 · FT-042 · contexto-ausente` + corpo com fatos; sem proposta de promoção (1ª ocorrência) |

#### Fluxo 2 — Modo Promover
| Campo | Descrição |
|---|---|
| Input Exato | L-001 e L-007 ambas com causa `contexto-ausente`; usuário: "promoção" |
| Regra IF/THEN | IF ocorrencias_mesma_causa >= 2 OR pedido_explicito=true → formular R-nn imperativa → definir aplica-a e severidade → gerar diff → exibir → aguardar resposta; IF resposta="ok" → gravar em `.kiro/steering/sdd.md`; IF resposta≠"ok" → descartar sem gravar |
| Output Gerado | Diff: `+ R-01 [IMPORTANTE] Verificar steering antes de gerar saída`; com "ok" → `sdd.md` atualizado |

#### Fluxo 4 — Skill Desatualizada
| Campo | Descrição |
|---|---|
| Input Exato | Modo registrar classifica: `causa = skill-desatualizada`; skill identificada: `sdd-revisar` |
| Regra IF/THEN | IF causa=skill-desatualizada → registrar em `licoes.md` (como modo registrar) → identificar skill → emitir aviso; NÃO criar R-nn; NÃO modificar nenhum arquivo da skill |
| Output Gerado | `## L-002 · 2026-10-15 · FT-042 · skill-desatualizada` em `licoes.md`; aviso: "⚠️ skill sdd-revisar pode estar desatualizada — notificar mantenedor" |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Modo registrar | `<produto>/aprendizado/licoes.md` | `.md` — append-only; entradas `## L-<nnn>` | Entrada L-nnn appendada (arquivo nunca sobrescrito) | Dir. `aprendizado/` inexistente → erro; lição perdida |
| Modo promover | `.kiro/steering/sdd.md` | `.md` — seção "Regras aprendidas" com R-nn | Seção atualizada somente após "ok" explícito | Arquivo não encontrado; ou gravação tentada sem "ok" → bloqueada |
| Modo retrospectiva | `<produto>/aprendizado/licoes.md` | `.md` | Entrada `retro-<FT\|EP\|Sprint>` appendada com métricas | Dir. `aprendizado/` inacessível |
| Skill desatualizada | `<produto>/aprendizado/licoes.md` | `.md` | Entrada com causa `skill-desatualizada` appendada; aviso ao mantenedor emitido | Dir. `aprendizado/` inacessível |
| Caso de avaliação (opcional) | `<produto>/aprendizado/avaliacoes/caso-L-<nnn>.md` | `.md` | Arquivo criado com situação, decisão, correção, regra | Dir. `avaliacoes/` não existe → criar ou reportar; falha não bloqueia outros fluxos |


---

## SKILL: sdd-elm

> **Papel:** Alimenta o IBM ELM (DOORS Next + EWM + ETM) a partir dos artefatos do fluxo sdd — sempre via power `elm`, com prévia e confirmação. Oito modos de operação.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Modo Similares (somente leitura)
| Campo | Descrição |
|---|---|
| Gatilho | sdd-prd (e sdd-triar) antes de criar qualquer HF, REG ou GL |
| Processamento | 1. Consulta bundle local por artefatos com título/conteúdo sobrepostos; 2. Consulta DOORS Next via MCP para artefatos iguais/sobrepostos/relacionados; 3. Classifica cada acerto: igual / sobrepõe / relacionado; acerto apenas por palavra em comum → descarte; 4. Exibe tabela — **modo somente leitura, nenhum artefato criado** |
| Output | Tabela de similares com links, relação e recomendação (igual→reutilizar; sobrepõe→alterar; relacionado→criar citando; nenhum→criar novo); zero escrita no ELM |

#### Fluxo 2: Modo Requisitos (PRD → DOORS Next)
| Campo | Descrição |
|---|---|
| Gatilho | Conceitos OKF aprovados em `elm/`; pedido de publicação no DOORS Next |
| Processamento | 1. Monta prévia (tabela Ação\|Alvo\|Título\|Tipo/Pasta); 2. UMA confirmação para o lote; 3. Idempotência: id preenchido → atualiza mesmo id; sem id → busca publicação interrompida; não achou → cria; 4. Publica na ordem: termos → regras → histórias; 5. Conflito → Fluxo 8; 6. Grava resource, id, sources em `elm/`; 7. Appenda `elm/log.md` |
| Output | Conceitos no DOORS Next; `elm/` com ids; `elm/log.md` atualizado; tabela Criados\|Atualizados\|Sem mudança\|Links\|Conflitos |

#### Fluxo 3: Modo Backlog (épicos e fatias → EWM)
| Campo | Descrição |
|---|---|
| Gatilho | Épico + IBs das fatias prontos para publicar no EWM |
| Processamento | 1. Prévia + UMA confirmação; 2. Idempotência por id EWM; 3. Cria/atualiza épico; 4. Cria/atualiza IBs com critérios de aceite + pai=épico + link "implementa" DOORS Next; 5. Grava coluna `elm` em `backlog.md`; 6. Appenda `elm/log.md` |
| Output | Épico + IBs no EWM; `backlog.md` com coluna `elm`; tabela de saída padrão |

#### Fluxo 4: Modo Sprint (planos e tarefas → EWM)
| Campo | Descrição |
|---|---|
| Gatilho | Planos e tarefas `[ESP][DEV][REV][VER]` prontos para publicar numa iteração |
| Processamento | 1. Prévia + UMA confirmação; 2. Idempotência; 3. Cria/atualiza planos na iteração; 4. Cria/atualiza tarefas com responsável, estimativa, `plannedFor`=iteração; 5. Grava coluna "Tarefa ELM" em `sprint-<nn>.md`; 6. Appenda `elm/log.md` |
| Output | Planos e tarefas no EWM; `sprint-<nn>.md` com coluna "Tarefa ELM" |

#### Fluxo 5: Modo Horas (lançar e relatório)
| Campo | Descrição |
|---|---|
| Gatilho | Conclusão de tarefa ou pedido manual `"lança 4h"`, `"relatório de horas"` |
| Processamento | Lançar: 1. Exibe prévia das horas; 2. Aguarda confirmação; 3. Lança via MCP elm; 4. Grava seção "Horas" em `AT-<nnn>-<slug>.md` (atendimento) ou `sprint-<nn>.md`; 5. Appenda `elm/log.md`. Relatório: consulta EWM → tabela por tipo e por pessoa, planejadas × lançadas |
| Output | Horas lançadas no EWM + arquivo de registro atualizado (lançamento); tabela de relatório (relatório) |

#### Fluxo 6: Modo Testes (CT.csv → ETM)
| Campo | Descrição |
|---|---|
| Gatilho | CT.csv com casos de teste prontos para publicar no ETM (na consolidação) |
| Processamento | 1. Prévia + UMA confirmação; 2. Idempotência por id CT; 3. Publica CTs no ETM; 4. Cria links "valida" CT → história coberta; 5. Grava ids em `verificacao.md` e `status.md`; 6. Appenda `elm/log.md` |
| Output | CTs no ETM; links "valida" criados; `verificacao.md` e `status.md` atualizados |

#### Fluxo 7: Sem MCP (ELM Pendente)
| Campo | Descrição |
|---|---|
| Gatilho | MCP elm responde com erro ou timeout em qualquer modo |
| Processamento | 1. Detecta falha; 2. Grava `"ELM pendente: <modo> <alvo>"` em `status.md`; 3. Se `status.md` inacessível → grava no rodapé do PRD; 4. **Continua o fluxo principal sem interromper** |
| Output | Pendência registrada; fluxo não para |

#### Fluxo 8: Conflito de Artefato
| Campo | Descrição |
|---|---|
| Gatilho | Durante publicação, versão ELM diverge da versão local |
| Processamento | 1. Detecta divergência; 2. Exibe ambos os lados lado a lado; 3. Pergunta qual versão prevalece; 4. Aguarda resposta explícita "sim"; 5. **NUNCA** sobrescreve sem confirmação; 6. Registra resolução em `elm/log.md` |
| Output | Artefato resolvido conforme escolha; linha na coluna Conflitos da tabela de saída |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 2 — Modo Requisitos
| Campo | Descrição |
|---|---|
| Input Exato | `"publique requisitos da fatia pagamento-pix"` + elm/ com conceitos OKF aprovados |
| Regra IF/THEN | PARA CADA conceito: IF campo `id` preenchido E MCP retorna artefato com esse id → atualiza; ELSE IF busca por título retorna resultado → retoma publicação parcial; ELSE → cria novo; IF versão ELM ≠ versão local → pausa e dispara Fluxo 8; APÓS todos: grava resource+id+sources em elm/; appenda elm/log.md; exibe tabela Criados\|Atualizados |
| Output Gerado | Tabela de saída padrão; `elm/` com ids preenchidos; `elm/log.md` atualizado |

#### Fluxo 7 — Sem MCP
| Campo | Descrição |
|---|---|
| Input Exato | `"publique backlog da fatia X"` quando MCP elm está offline |
| Regra IF/THEN | IF chamada MCP retorna erro/timeout → NÃO tenta publicar; IF `status.md` acessível → grava "ELM pendente: backlog fatia-X"; ELSE IF PRD acessível → grava no rodapé do PRD; fluxo principal continua; NÃO interrompe o agente |
| Output Gerado | `"ELM pendente: backlog fatia-X"` em `status.md` ou rodapé PRD; fluxo continua normalmente |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Similares | Nenhum arquivo gravado | — | Exibe tabela em tela | — |
| Requisitos | `<produto>/epicos/<EP>-<slug>/elm/*.md` | `.md` — resource, id, sources atualizados | ids gravados após publicação no DOORS Next | Pasta `elm/` inexistente → cria; se falhar → pendência em `elm/log.md` |
| Backlog | `<produto>/backlog.md` | `.md` | Coluna `elm` preenchida com ids EWM | Arquivo não encontrado → erro; fluxo para |
| Sprint | `<produto>/planejamento/sprints/sprint-<nn>.md` | `.md` | Coluna "Tarefa ELM" preenchida | Arquivo não encontrado → fluxo para |
| Horas | `<produto>/atendimentos/AT-<nnn>-<slug>.md` | `.md` | Seção "Horas" gravada após lançamento confirmado | Arquivo AT inexistente → erro; horas não lançadas |
| Testes | `.kiro/specs/<ft>-<slug>/verificacao.md` e `status.md` | `.md` | ids dos CTs gravados após publicação no ETM | Pasta spec inexistente → cria ou registra pendência |
| Sem MCP | `status.md` ou rodapé do PRD | `.md` | `"ELM pendente: <modo> <alvo>"` gravado | Se ambos inacessíveis → pendência perdida |
| Conflito | `elm/log.md` | `.md` | Resolução registrada (versão vencedora + data) | Se inacessível → conflito não resolvido; publicação bloqueada |
| Todos | `elm/log.md` | `.md` | Entrada appended após cada publicação | Falha → "ELM pendente" anotado em status.md |


---

## SKILL: sdd-atender

> **Papel:** Trilha de atendimento — demanda de cliente que não muda o repositório (consulta, extração, explicação). Abre AT-nnn, executa (banco somente leitura + bundle ELM), rascunha resposta, conclui lançando horas.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Abrir Atendimento
| Campo | Descrição |
|---|---|
| Gatilho | `"novo atendimento: o cliente X pediu …"` — pedido que não muda o repositório |
| Processamento | 1. Lê `Próximo: AT-nnn` do `README.md` e incrementa; 2. sdd-entrevistar modo atendimento (1 rodada): o que receber, origem, prazo, quem responde, critério de pronto; 3. sdd-elm modo atendimento: cria `[ATD] AT-<nnn> <título>`, filha do IB "Atendimento", com confirmação; 4. Grava `AT-<nnn>-<slug>.md` + linha no `README.md` + linha no `sprint-<nn>.md`; 5. Commit na BASE |
| Output | AT-nnn criado no EWM; 3 arquivos gravados; commit na BASE |

#### Fluxo 2: Executar (banco + bundle)
| Campo | Descrição |
|---|---|
| Gatilho | AT aberto; pronto para execução |
| Processamento | 1. Consulta banco via MCP somente leitura; 2. Consulta bundle do ELM; 3. Resultado com dado real → `.kiro/local/atendimentos/AT-<nnn>/` (**FORA do git**); 4. No registro: **apenas** SQL, contagem, caminho do arquivo, resumo anônimo; 5. Elabora rascunho da resposta; 6. Aguarda "ok" da pessoa antes de registrar como aprovado; **NÃO envia por conta própria** |
| Output | Rascunho aguardando "ok"; dados reais em `.kiro/local/` (não versionados); registro anônimo no `AT-<nnn>-<slug>.md` |

#### Fluxo 3: Concluir
| Campo | Descrição |
|---|---|
| Gatilho | `"enviei"`, `"conclui o AT-012"` |
| Processamento | 1. Grava "Resposta Enviada" (sem dado de cliente) em `AT-<nnn>-<slug>.md`; 2. sdd-elm modo horas com confirmação; 3. Atualiza `README.md` (status AT→concluído); 4. Atualiza `sprint-<nn>.md` (marca AT concluído); 5. Commit na BASE |
| Output | AT concluído; horas lançadas no EWM; arquivos atualizados; commit na BASE |

#### Fluxo 4: Encaminhar Saída
| Campo | Descrição |
|---|---|
| Gatilho | Conclusão revela ação downstream; OU demanda recebida é identificada como não-atendimento |
| Processamento | IF defeito encontrado → sdd-triar (trilha rápida com `origem: AT-nnn`); IF regra em aberto → sdd-entrevistar ou sdd-prd; IF consulta reaproveitável → sdd-aprender; IF demanda muda sistema → **NÃO** abre AT → redireciona para sdd-triar; IF regra sem decisão → redireciona para sdd-entrevistar/PRD |
| Output | Mensagem de encaminhamento com skill de destino e motivo |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Abrir
| Campo | Descrição |
|---|---|
| Input Exato | `"novo atendimento: o cliente Previdência pediu extração do total de benefícios ativos por município"` |
| Regra IF/THEN | IF `README.md` existe E contém "Próximo: AT-nnn" → extrai nnn; incrementa; aciona sdd-entrevistar (1 rodada); IF sdd-elm disponível → cria [ATD] AT-nnn no EWM; ELSE → registra "ELM pendente: atendimento AT-nnn"; SEMPRE: grava `AT-<nnn>-<slug>.md`; adiciona linha em `README.md`; adiciona linha em `sprint-<nn>.md`; commit |
| Output Gerado | `AT-<nnn>-<slug>.md` criado; `README.md` e `sprint-<nn>.md` atualizados; commit na BASE |

#### Fluxo 2 — Executar
| Campo | Descrição |
|---|---|
| Input Exato | AT-012 aberto; `"execute a consulta e elabore a resposta"` |
| Regra IF/THEN | IF MCP banco disponível → executa SQL somente leitura; IF resultado contém dado real → grava em `.kiro/local/atendimentos/AT-012/` (NÃO no git); grava em `AT-012-<slug>.md` APENAS: SQL+contagem+caminho+resumo-anônimo; elabora rascunho; aguarda "ok"; IF "ok" → marca rascunho como aprovado; NÃO envia por si mesmo |
| Output Gerado | `.kiro/local/atendimentos/AT-012/` com dados reais; `AT-012-<slug>.md` com registro anônimo; rascunho pronto |

#### Fluxo 3 — Concluir
| Campo | Descrição |
|---|---|
| Input Exato | `"enviei a resposta do AT-012"` |
| Regra IF/THEN | IF AT-012 existe E em estado de execução → grava "Resposta Enviada" (sem dado real); aciona sdd-elm modo horas; IF disponível → lança horas com confirmação; ELSE → "ELM pendente: horas AT-012"; atualiza `README.md`; atualiza `sprint-<nn>.md`; commit |
| Output Gerado | `AT-012-<slug>.md` com "Resposta Enviada"; `README.md` e `sprint-<nn>.md` atualizados; commit |

#### Fluxo 4 — Encaminhar
| Campo | Descrição |
|---|---|
| Input Exato | `"no AT-012 encontrei um defeito no cálculo de benefício"` |
| Regra IF/THEN | IF "defeito"/"bug"/"erro de sistema" detectado → "Encaminhando para sdd-triar: defeito encontrado no AT-012"; IF "regra indefinida" → "Encaminhando para sdd-entrevistar"; IF "consulta reaproveitável" → "Encaminhando para sdd-aprender"; IF demanda muda sistema → "Encaminhando para sdd-triar: nova funcionalidade, não atendimento" |
| Output Gerado | `"Encaminhando para <skill>: <motivo>"` |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Abrir | `<produto>/atendimentos/README.md` | `.md` | "Próximo: AT-nnn" incrementado; linha de status adicionada | Arquivo não encontrado → cria; dir. inexistente → cria dir. |
| Abrir | `<produto>/atendimentos/AT-<nnn>-<slug>.md` | `.md` — Origem, Pedido, Consultas, Resposta enviada, Horas, ELM, Saída | Arquivo criado com dados da entrevista | Dir. `atendimentos/` inexistente → cria; se falhar → erro crítico |
| Abrir | `<produto>/planejamento/sprints/sprint-<nn>.md` | `.md` | Linha adicionada na seção Atendimento | Arquivo de sprint não encontrado → registra pendência; fluxo não para |
| Executar — dados reais | `.kiro/local/atendimentos/AT-<nnn>/` | csv, json, txt (qualquer) | Dados reais gravados **fora do git**; caminho registrado em `AT-<nnn>-<slug>.md` | `.kiro/local/` inacessível → erro crítico; dados **NÃO** vão para o repositório em nenhuma hipótese |
| Executar — registro | `<produto>/atendimentos/AT-<nnn>-<slug>.md` | `.md` | Somente SQL, contagem, caminho, resumo anônimo gravados (nunca dado real) | Arquivo não gravável → erro; ação bloqueada |
| Concluir | `<produto>/atendimentos/README.md` + `sprint-<nn>.md` | `.md` | Status AT atualizado para concluído em ambos | Qualquer arquivo não gravável → erro; pendência registrada |

---

## SKILL: sdd-loop

> **Papel:** Execução autônoma (AFK) de várias fatias em paralelo — cria worktree por fatia em `.kiro/local/wt/`, leva cada uma da pesquisa ao PR por subagentes de contexto limpo.

### PARTE 2 — Plano de Fluxo

#### Fluxo 1: Iniciar Lote
| Campo | Descrição |
|---|---|
| Gatilho | `"roda as fatias AFK"`, `"modo AFK"`, `"leva a FT-031 e a FT-032 até o PR"` |
| Processamento | 0. Verifica `.kiro/local/loop-*.md` existente → oferta de retomada. 1. Candidatas: fatias pedidas ou `pronta + AFK` da sprint atual em ordem de prioridade; filtra HITL, direta, DoR não atendida, `bloqueada-por` não concluída, já em andamento por outra pessoa. 2. Limite: paralelismo do sdd.md (padrão 1, máx 3) E vagas WIP de revisão humana. 3. Proposta — **UMA confirmação para o lote todo** (fatias, branches, worktrees, plano AFK, push/PR autorizado ou não). 4. Com "sim" + MCP: assume `[DEV]` no EWM; sem MCP → `ELM pendente` no status.md. 5. Cria log `.kiro/local/loop-<data>.md` |
| Output | Log do lote criado; worktrees não criadas ainda (vêm no P2); `[DEV]` assumidas no EWM ou pendência registrada |

#### Fluxo 2: Execução por Fase (por fatia)
| Campo | Descrição |
|---|---|
| Gatilho | Lote confirmado; para cada fatia, em paralelo (até o limite) |
| Processamento | Cria worktree: `git worktree add .kiro/local/wt/<ft> -b <branch> origin/<base>`. Cria pasta spec + `status.md` (Responsável: agente:sdd-orquestrador). Fases em sequência, cada uma com subagente novo: (1) pesquisa → research.md; (2) plano → spec do Kiro; (3) análise do plano rubrica L → correção se AJUSTAR; (4) GATE do plano (para se "aprovação humana", avança se "análise basta"); (5) implementação → tasks [x] + backpressure; (6) revisão rubrica C → correção se REVISAR; (7) verificação → ACEITO; (8) entrega: commit + push + PR (se autorizado). Após cada fase: atualiza log + Histórico do `status.md` + commit na worktree |
| Output | Para cada fatia: spec completa, commits na worktree, PR aberto (se autorizado); `status.md` fase-a-fase |

#### Fluxo 3: Parada (Bloqueio de Fatia)
| Campo | Descrição |
|---|---|
| Gatilho | Lacuna de negócio, divergência com o plano, 2ª reprovação, verificação rejeitada 2× em qualquer fase |
| Processamento | 1. Registra motivo e pergunta exata no `status.md` da fatia bloqueada; 2. Continua com as outras fatias do lote; 3. Ao fim: inclui no resumo as fatias bloqueadas com a pergunta para a pessoa |
| Output | `status.md` fatia com `fase: bloqueada`; demais fatias continuam; resumo final lista bloqueios |

#### Fluxo 4: Parada Sistêmica
| Campo | Descrição |
|---|---|
| Gatilho | Build quebrado na base, ambiente fora do ar, mesmo erro em duas fatias diferentes |
| Processamento | **Para o lote inteiro** imediatamente; registra o problema no log; o loop não conserta ambiente |
| Output | Log atualizado com motivo sistêmico; nenhuma fatia avança |

#### Fluxo 5: Retomar Lote Anterior
| Campo | Descrição |
|---|---|
| Gatilho | `"retoma o loop"` com `.kiro/local/loop-*.md` existente com fatias não finalizadas |
| Processamento | 1. Mostra estado do log (fatia, fase, rodada, último resultado); 2. Pergunta se retoma; 3. Com "sim": continua cada fatia da fase registrada no `status.md` dela (não reinicia do zero) |
| Output | Retomada na fase correta; log atualizado |

### PARTE 3 — Teste do Quarto Chinês

#### Fluxo 1 — Iniciar Lote
| Campo | Descrição |
|---|---|
| Input Exato | `"roda as fatias AFK"` com sprint aberta, fatias FT-031 (AFK, pronta) e FT-032 (AFK, pronta) |
| Regra IF/THEN | IF loop-*.md com fatias não finalizadas existe → oferta de retomada BEFORE continuar; IF FT.modo=HITL OR FT.trilha=direta OR DoR_não_atendida → fica de fora; IF paralelismo_sdd_md < 2 → somente FT-031 (1 de cada vez); IF vagas_WIP_revisão < 2 → ajusta para vagas disponíveis; EXIBE proposta; aguarda UMA confirmação; IF "sim" + MCP ELM → assume [DEV] no EWM; grava loop-<data>.md |
| Output Gerado | `loop-<data>.md` criado; confirmação do EWM ou `ELM pendente`; worktrees ainda não criadas |

#### Fluxo 3 — Parada de Fatia
| Campo | Descrição |
|---|---|
| Input Exato | FT-031 na fase de revisão recebe REVISAR pela 2ª vez; FT-032 em implementação |
| Regra IF/THEN | IF REVISAR AND rodada = 2 → status.md FT-031 `fase: bloqueada` + motivo + pergunta exata; sdd-loop NÃO para; continua com FT-032; ao fim: resumo lista FT-031 como bloqueada com a pergunta |
| Output Gerado | `status.md` FT-031 `fase: bloqueada`; FT-032 continua; resumo com item "Aguardando pessoa: FT-031 — <pergunta>" |

#### Fluxo 4 — Parada Sistêmica
| Campo | Descrição |
|---|---|
| Input Exato | Build quebrado na base durante implementação de FT-031; mesmo erro ocorre ao tentar FT-032 |
| Regra IF/THEN | IF mesmo erro sistêmico em 2 fatias → PARA TUDO imediatamente; registra no log: "Parada sistêmica: build quebrado na base"; NÃO tenta corrigir o ambiente; NÃO avança nenhuma outra fatia |
| Output Gerado | `loop-<data>.md` com nota de parada sistêmica; zero novos commits |

### PARTE 4 — Verificação de Artefatos

| Fluxo | Caminho | Extensão | Sucesso | Falha |
|---|---|---|---|---|
| Iniciar Lote | `.kiro/local/loop-<AAAA-MM-DD-HHMM>.md` | `.md` — tabela FT\|Worktree\|Branch\|Fase\|Rodada\|Último resultado\|Atualizado | Criado ao confirmar o lote | Dir. `.kiro/local/` inexistente → criar; se falhar → loop não inicia |
| Execução por Fase | `.kiro/local/wt/<ft>/` | Dir. (worktree git) | `git worktree add` bem-sucedido; pasta criada dentro do workspace para acesso dos agentes | Erro no `git worktree add` (branch já existe, base divergiu) → registra no log; fatia bloqueada |
| Execução por Fase | `.kiro/local/wt/<ft>/.kiro/specs/<ft>-<slug>/status.md` | `.md` | Criado com Responsável: agente:sdd-orquestrador; atualizado fase a fase | Falha de escrita → fatia bloqueada |
| Execução por Fase | `.kiro/local/wt/<ft>/` (todos os artefatos) | variável | Spec completa (research, requirements, design, tasks, revisoes, verificacao, CT.csv) gravada dentro da worktree | Subagente sem permissão → artefato não criado; fase bloqueada |
| Entrega | Git (push + PR) | — | Push + PR somente se autorizado no lote ("push/PR: sim"); NUNCA merge | Kiro pede confirmação a cada push (regra `ask`); se usuário nega → fatia fica em `fase: aceita` |
| Worktrees pós-merge | `.kiro/local/wt/<ft>/` | Dir. | `git worktree remove .kiro/local/wt/<ft>` (sem `--force`) após o merge humano | Remoção com `--force` nunca executada; worktrees com mudanças pendentes não são removidas |


---

# Sumário Executivo

## Cobertura da Análise

| Métrica | Valor |
|---|---|
| Skills analisadas | 19 de 19 (100%) |
| Fluxos mapeados | 65+ fluxos distintos |
| Testes do Quarto Chinês | 65+ testes IF/THEN |
| Artefatos verificados | 80+ entradas de persistência |
| Subagents utilizados | 8 em paralelo |

## Achados Gerais de Coesão

### ✅ Pontos Fortes

1. **Trilhas bem definidas**: As 5 trilhas (direta, rápida, padrão, épico, atendimento) têm fronteiras claras. A regra de classificação é determinística e documentada na `sdd-triar`.

2. **Consistência de gates**: Os 5 gates são sempre de uma pessoa, nunca de um agente. As rubricas (P/L/C) da `sdd-revisar` garantem critérios objetivos de aprovação.

3. **Separação gerador ≠ avaliador**: `sdd-implementar` aciona `sdd-revisar` como subagente independente (contexto limpo), que aciona `sdd-verificar` também independente.

4. **Estado em disco**: O `status.md` carrega a fase atual, garantindo que sessões novas (incluindo agentes autônomos) retomem exatamente onde pararam.

5. **Fallback de MCP ELM**: Todas as skills que usam o MCP elm têm o mesmo padrão de fallback: `"ELM pendente: <ação>"` registrado em `status.md`, sem travar o fluxo.

6. **Proteção de dados**: `sdd-atender` e `sdd-verificar` têm lógica explícita para gravar dados reais em `.kiro/local/` (fora do git).

7. **Idempotência ELM**: `sdd-elm` implementa idempotência em todos os modos (busca por id existente antes de criar), evitando duplicatas no DOORS Next e EWM.

### ⚠️ Pontos de Atenção

1. **sdd-triar × sdd-iniciar**: A `sdd-triar` não começa nada — a `sdd-iniciar` é quem começa. Porém, a `sdd-iniciar` só aceita o que já está registrado no backlog.md **e** publicado em `origin`. Há uma janela de risco se o commit do backlog.md não for empurrado antes de tentar iniciar.

2. **sdd-loop × gates humanos**: O loop AFK para em `plano-em-revisao` quando configurado com "aprovação humana", e **nunca** faz merge. Isso garante o controle humano, mas exige que a pessoa monitore as worktrees em `.kiro/local/wt/`.

3. **Número de rodadas de revisão**: O limite de 2 rodadas tanto em `sdd-implementar` (revisão do código) quanto em `sdd-plano` (análise do plano) é um gate implícito. Na 2ª reprovação, a fatia vai para `fase: bloqueada` e exige intervenção humana.

4. **sdd-consolidar como fase final**: A skill de consolidação é acionada **depois** do merge (por uma pessoa), não automaticamente. Há risco de drift não sendo fechado se a consolidação for esquecida. O `sdd-status` lista inconsistências que ajudam a detectar isso.

5. **sdd-loop e ferramentas que varrem a raiz**: As worktrees ficam em `.kiro/local/wt/` que deve estar no `.gitignore` e nas exclusões de test runners, linters e `tsc`. O `sdd-setup` valida isso no Passo 9.

### 📋 Mapa de Artefatos por Localização

| Localização | O quê | Quem escreve |
|---|---|---|
| `.kiro/steering/sdd.md` | Configuração única do fluxo + Regras aprendidas | sdd-setup, sdd-aprender |
| `.kiro/agents/sdd-*.json` | 6 agentes do fluxo | sdd-setup |
| `.kiro/specs/<ft>-<slug>/` | status.md, research.md, design, tasks, revisões, verificação, CT.csv | sdd-iniciar → sdd-verificar |
| `.kiro/local/` (fora do git) | Worktrees, dados reais de AT, evidências com dado real | sdd-loop, sdd-atender, sdd-verificar |
| `<produto>/backlog.md` | Épicos, fatias, status | sdd-triar, sdd-fatiar, sdd-planejamento, sdd-consolidar |
| `<produto>/epicos/<EP>/` | prd.md, decisoes.md, elm/ (OKF) | sdd-prd, sdd-entrevistar |
| `<produto>/fatias/FT-*.md` | Fichas de fatias sem épico | sdd-triar |
| `<produto>/planejamento/` | equipe.json, acordos.md, roadmap.md, sprints/ | sdd-planejamento |
| `<produto>/atendimentos/` | README.md, AT-*.md (sem dado real) | sdd-atender |
| `<produto>/aprendizado/` | licoes.md, avaliacoes/ | sdd-aprender, sdd-consolidar |
| `docs/glossario.md`, `docs/adr/` | Glossário e ADRs | sdd-entrevistar, sdd-consolidar |

---

*Documento gerado via Orquestrador + 8 subagents em paralelo a partir das 19 skills do power `sdd` v2.3.0.*
