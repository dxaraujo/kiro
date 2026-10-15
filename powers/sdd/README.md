# sdd

Power do Kiro para **engenharia agêntica orientada a especificação**, com o **IBM ELM** como fonte oficial da
documentação e o **planejamento ágil** dentro do fluxo. É a versão 2 do `sdd` (substitui a v1 e o power `sdd2`, nome
desta versão durante o desenvolvimento): menos cerimônia onde ela não paga, mais verificação onde ela paga, e cada
decisão ancorada no que os principais praticantes de desenvolvimento com agentes defendem hoje (outubro de 2026).

O agente escreve muito código rápido; o que limita o resultado é o **alinhamento** antes e a **verificação**
depois. O sdd põe as pessoas onde elas têm mais alavanca — decidir o quê, aprovar o como, ler o código — e deixa
o resto com agentes de contexto limpo, presos a feedback automático.

```
PRODUTO   entrevistar ─► PRD ─► GATE PRD ─► ELM (HF/REG/GL) ─► fatiar ─► GATE backlog ─► sprint (EWM)
                                                                                 │
FATIA     iniciar ─► pesquisar ─► plano (spec do Kiro) ─► GATE plano ─► implementar (TDD) ─► revisar ─► verificar ─► PR
                                                                                                                  │
DEPOIS    merge (pessoa) ─► consolidar (drift, ELM as-built, CTs, ADRs) ─► aprender (lições)
```

## O que muda em relação ao `sdd`

| `sdd` v1 | `sdd` v2 |
|---|---|
| um fluxo para tudo (HF/REG/ET/CT + spec SDD em todo IB) | **trilhas** pelo tamanho: direta, rápida (bugfix spec), padrão, épico — e atendimento, sem código |
| especificação por IB, em três papéis assíncronos | **PRD por épico** + **fatias verticais** que cabem numa janela de contexto |
| entrevista uma pergunta por vez | entrevista em **rodadas pela fronteira** de decisões, sempre com recomendação |
| spec SDD → implementação → judge | **pesquisa** compactada → **plano com a forma do programa** e o **contrato de pronto** → **GATE do plano** |
| judge com rubrica única | revisão em **dois eixos separados** (spec × padrões) + **verificação de aceite** de ponta a ponta |
| testes unitários + cobertura | **teste primeiro**, **backpressure** a cada tarefa, **oráculo protegido** |
| ELM publicado antes do código | ELM como **registro oficial**: requisitos no GATE do PRD, **as-built** e drift na consolidação |
| retrabalho por causa raiz | **aprendizado composto**: erro mecânico vira checagem, julgamento vira regra do revisor |
| lote de IBs | **AFK/HITL** por fatia e **loop AFK** limitado pela capacidade de revisão humana |
| planejamento por pontos/hora e Excel | **vazão** de fatias, WIP de revisão, meta da sprint; pontos mantidos no EWM |
| agentes JSON com permissões amplas | agentes no **formato universal** do Kiro (IDE e as duas engines do CLI), permissões mínimas por papel e **skills de toolkit escolhidas por agente** |

## Fundamentos

| # | Princípio | Quem defende |
|---|---|---|
| 1 | Alinhar antes de escrever: entrevista em rodadas, com resposta recomendada; fatos o agente busca, decisões a pessoa toma | Matt Pocock (`grilling`), Anthropic (entrevista → spec), Dex Horthy (QRSPI), Andrej Karpathy (modelos não pedem esclarecimento) |
| 2 | Cerimônia do tamanho do trabalho | Birgitta Böckeler ("marreta para quebrar noz"), Anthropic ("se o diff cabe numa frase, pule o plano"), Horthy (~40% *oneshot*), Spec Kit |
| 3 | Spec é registro de decisão, sem caminho de arquivo; o que dura é glossário, ADR e — aqui — o ELM | Pocock (`to-spec`), Böckeler (*spec-anchored*), Kent Beck e Martin Fowler (aprender durante a implementação) |
| 4 | Linguagem ubíqua num glossário usado no PRD, nos testes e no código | Pocock (`domain-modeling`), DDD |
| 5 | Fatias verticais (*tracer bullets*) que cabem numa janela de contexto nova, com critérios falsificáveis | Pocock (`to-tickets`), Horthy ("modelos amam planos horizontais"), Anthropic (uma funcionalidade por vez), Geoffrey Huntley (um item por loop) |
| 6 | Pesquisar → planejar → implementar, com compactação em arquivo e revisão humana do plano | Horthy (*Advanced Context Engineering*), Boris Cherny (comece no plan mode) |
| 7 | Desenhar a forma do programa antes do código (árvore de arquivos, assinaturas, árvore de chamadas) | Horthy (*Why Software Factories Fail*, 2026), Pocock (módulos profundos) |
| 8 | Teste primeiro, vermelho → verde, nos pontos de teste combinados | Beck, Simon Willison (*red/green TDD*), Karpathy ("dê critérios de sucesso, peça os testes primeiro"), Pocock (`tdd`) |
| 9 | Backpressure: compilar, testes e lint a cada passo; evidência em vez de afirmação | Huntley, Anthropic, Cherny ("dê ao agente como verificar o trabalho"), Willison ("first run the tests") |
| 10 | Proteger o oráculo: teste não se apaga nem se afrouxa | Anthropic (*long-running harnesses*), Beck ("o gênio trapaceando"), Karpathy (`autoresearch`) |
| 11 | Gerador ≠ avaliador; revisão em contexto limpo e em eixos separados; avaliador cético mas sem caçar gosto | Anthropic (*harness design*), Pocock (`code-review`), Cherny |
| 12 | Contexto limpo por fatia e estado em disco | Horthy (zona burra acima de ~40%), Pocock (*smart zone*), Huntley, Anthropic (*context engineering*) |
| 13 | Slider de autonomia: HITL até o tipo de trabalho provar que anda sozinho; WIP limitado pela revisão humana | Karpathy ("Iron Man suits"), Pocock (AFK/HITL), Addy Osmani (*orchestration tax*), DORA 2025 |
| 14 | Leia o código: PRs pequenos, com caminho de leitura e evidência | Horthy ("read the dang code"), Willison, Osmani (*comprehension debt*), Thoughtworks Radar vol. 34 |
| 15 | Aprendizado composto: cada correção muda o ambiente — checagem determinística primeiro | Mitchell Hashimoto (*engineer the harness*), Cherny, Pocock (`retro`), Fowler (*guides & sensors*) |
| 16 | Conhecimento mantido por LLM, com *lint* de contradições | Karpathy (*LLM Wiki*) — aqui, o bundle do ELM + glossário + ADRs |
| 17 | Harness mínimo, revisto a cada modelo; segurança sem a "tríade letal" | Anthropic, Fowler (*Are Harnesses Worth the Cost?*), Willison |

Fontes no fim deste arquivo.

## Conteúdo

| Skill | Função |
|---|---|
| `sdd` | guia do fluxo: trilhas, gates, princípios, qual skill usar |
| `sdd-setup` | configura o projeto: entende o repositório, descobre skills e toolkits, cria os agentes perguntando as skills de cada um |
| `sdd-status` | painel "onde parei", WIP de revisão, próxima ação de maior alavanca |
| `sdd-iniciar` | porta de entrada: triagem por trilha (inclusive atendimento), Definition of Ready, pasta, branch, item do EWM |
| `sdd-entrevistar` | alinhamento em rodadas (grill), decisões e glossário |
| `sdd-prd` | PRD do épico (o quê e por quê) e GATE do PRD |
| `sdd-fatiar` | PRD → fatias verticais AFK/HITL, backlog e GATE do backlog |
| `sdd-planejamento` | roadmap, acordos (cadência, DoR/DoD, WIP, reserva de atendimento), sprint com especificação e atendimento, review, retrospectiva, virada |
| `sdd-atender` | atendimento de cliente sem mudar o repositório: AT-nnn, tarefa `[ATD]`, consulta só leitura, extração fora do git, horas |
| `sdd-pesquisar` | pesquisa do código compactada em `research.md` |
| `sdd-plano` | spec do Kiro (`requirements.md`/`bugfix.md`, `design.md`, `tasks.md`) e GATE do plano |
| `sdd-implementar` | TDD + backpressure, commits pequenos, revisão e PR |
| `sdd-revisar` | revisão independente: PRD (P), plano (L), código (C, dois eixos) |
| `sdd-verificar` | aceite de ponta a ponta com evidência; `CT.csv` para o ETM |
| `sdd-consolidar` | pós-merge: drift, ELM as-built, ADRs, lint do conhecimento, conclusão |
| `sdd-elm` | alimenta o ELM: similares antes de especificar (só leitura), requisitos (DOORS Next), backlog e sprint (EWM), atendimento, horas, testes (ETM), links |
| `sdd-loop` | fatias AFK até o PR, uma worktree por fatia, uma fase por contexto limpo |
| `sdd-aprender` | lições, promoção de regras, retrospectiva com dados, casos de avaliação |

## O que a setup instala no projeto

O formato de power recomendado pelo Kiro (Agent Plugins, `plugin.json`) carrega só `skills/` e `mcp.json` — steering,
agentes, hooks e workflows dentro de um power são ignorados. Por isso a `sdd-setup` instala no projeto, a partir
de `skills/sdd-setup/assets/`:

| Arquivo | O quê |
|---|---|
| `.kiro/steering/sdd.md` | o único steering do fluxo (sempre carregado): resumo, configuração do projeto (pasta do produto, comandos, verificação, git, banco, autonomia, ELM, agentes) e regras aprendidas |
| `.kiro/agents/sdd-*.json` | `produto`, `pesquisador`, `codificador`, `revisor`, `verificador`, `orquestrador` — cada um com as skills e MCPs que a pessoa liberou |
| `.kiro/hooks/sdd.json` (opcional) | backpressure: compila e testa depois de cada tarefa de spec |
| `.kiro/workflows/sdd-*.workflow.json` (opcional, experimental) | `planejar-fatia` e `entregar-fatia` nos Kiro Workflows — quem dispara é a pessoa, no chat do Kiro ("rode o workflow `sdd-entregar-fatia` para a FT-031" ou `/workflow-run`), uma fatia por vez; nenhum agente as dispara |
| `.kiro/sdd/http.sh` (opcional) | única chamada HTTP que o verificador faz sem perguntar: só à URL de teste, com corpo da pasta `massa/` |
| pasta do produto (perguntada na setup; padrão `.kiro/planejamento`) | `backlog.md`, épicos e PRDs, `planejamento/`, `atendimentos/`, `aprendizado/` — versionada; o que é local fica em `.kiro/local/` (fora do git) |

O MCP do ELM entra só nos agentes que conduzem sessão com a pessoa (`sdd-produto`, `sdd-codificador`,
`sdd-orquestrador`), pelo `mcp.json`, com leitura liberada e escrita com confirmação; revisor, verificador e
pesquisador não o têm, e nenhum agente recebe os powers (sem `includePowers`). Sem o MCP, a escrita vira
pendência registrada.

Cada agente tem as permissões mínimas do papel, nos dois blocos do formato universal (`toolsSettings` para a
engine V2, `permissions` para a V3 e a IDE): lê o projeto e o power, mas não `.env`, chaves, `~/.ssh`, `~/.aws` nem
as credenciais do ELM; escreve só o que produz; no shell, git de leitura e, conforme o papel, `add`/`commit`. Merge,
rebase, `--force`, `reset --hard` e `git -C` (que esconde o subcomando das regras) são negados em todos; push e PR
só no orquestrador, com confirmação a cada um. Detalhes em
[`skills/sdd-setup/references/agentes.md`](skills/sdd-setup/references/agentes.md).

## Toolkits

O fluxo não sabe programar em nenhuma stack: o conhecimento de Java, Spring Batch, Angular, React etc. vem de
**toolkits** — pacotes de skills mantidos fora do power, um por tipo de projeto ou stack. A `sdd-setup` é a única
parte do fluxo que sabe procurá-los (`.kiro/toolkits/`, `~/.kiro/toolkits/`, powers instalados com `toolkit.json`,
ou skills com `metadata.toolkit`), detecta o tipo do projeto e **pergunta, agente por agente**, quais skills ligar —
num projeto 100% Spring Batch, o codificador recebe as de batch e Java que a pessoa escolher, e não as de REST ou
frontend. Contrato em [`skills/sdd-setup/references/toolkits.md`](skills/sdd-setup/references/toolkits.md) e
schema em [`toolkit.schema.json`](skills/sdd-setup/assets/toolkit.schema.json).

## IBM ELM

O ELM é o sistema de registro; o repositório guarda as propostas de mudança (PRD, fatias) e como cada mudança foi
feita. Mapeamento padrão (ajustável na setup): história → artefato *História de Usuário* (DOORS Next); regra →
*Regra*; termo → *Termos de Glossário*; épico → *Épico* (EWM); fatia → *Item de Backlog* que **implementa** as
histórias; tarefas filhas na sprint; cenário verificado → *Caso de Teste* (ETM) que **valida** a história.
Cada história, regra e termo nasce como um conceito **OKF v0.2** na pasta da spec (o mesmo formato do bundle da
`elm-sync`), com aprovação registrada em `verified`; sobe para o DOORS Next só depois do GATE, de baixo para cima,
com HF → REG como embed, sem nada extra no texto publicado e sempre com prévia e confirmação. Atributos e links entre
requisitos ficam registrados nos conceitos, porque o MCP não os grava. Detalhes em [`skills/sdd-elm/references/mapeamento.md`](skills/sdd-elm/references/mapeamento.md).

O MCP do power `elm` ainda não grava atributos de requisito, links requisito↔requisito, módulos, change sets,
baselines nem casos de teste: quando o processo do projeto exige algum deles, a `sdd-elm` entrega o roteiro manual
e registra a pendência.

## Pré-requisitos

- Kiro IDE 1.x ou Kiro CLI 2.31+; repositório git com branch base e PRs. Na engine V2 do CLI os agentes e as
  skills funcionam, mas o hook e os workflows exigem a IDE ou a engine V3.
- Kiro Web não lê `~/.kiro`: os agentes do projeto aparecem lá, mas sem as skills do power — use a IDE ou o CLI.
- Opcional: power [`elm`](../elm/) (IBM ELM) com `elm-setup` feito; MCP de consulta ao banco (somente leitura);
  MCP de browser/Playwright para verificar frontend; Kiro Workflows habilitado (IDE: `kiroAgent.workflows.enabled`;
  CLI: `chat.enableWorkflows`) para as receitas experimentais.
- Toolkits da stack do projeto (opcional — sem eles os agentes dependem do steering e do código vizinho).

## Primeiros passos

1. Instale pelo painel **Powers** do Kiro (pasta `sdd` deste repositório ou uma cópia local).
2. No projeto, peça **"configurar o sdd"** e responda às perguntas (uma por vez).
3. Comece: **"nova demanda: …"** (a `sdd-iniciar` faz a triagem; épico → PRD), **"vamos trabalhar na FT-031"** (fatia), **"corrigir o defeito
   4567"** (trilha rápida) — ou **"onde parei?"**.

Depois de atualizar o power ou um toolkit: "atualizar os agentes do sdd". Projeto configurado com o power
`sdd2` ou com a v1 do `sdd`: desinstale o power antigo, instale este e peça "atualizar a configuração do sdd" — a
setup pergunta a pasta do produto, junta os steerings num só, renomeia hooks, workflows e agentes e move
`.kiro/produto/` e `.kiro/aprendizado/` com `git mv`.

Não use o `/upgrade-agent` (nem `kiro-cli agent upgrade`) para regenerar os agentes `sdd-*`: o conversor não
produz as regras que só existem na V3 (skill liberada, confirmação de push/PR) — ele já os deixa de lado
("out of sync").

## Como foi verificado

**Documentação oficial do Kiro**, lida inteira nas páginas `.md` de `kiro.dev/docs` em 14/10/2026 (powers, skills,
steering, custom agents e referência de configuração, subagentes, permissões, hooks, specs, workflows, CLI V3 e
migração), mais o schema do `plugin.json` (Agent Plugins) e a especificação Agent Skills. Uma auditoria do power
contra essas páginas gerou as correções desta versão: `git -C` negado, leitura restrita, confirmação de push e PR,
delegação a subagente sem pergunta por agente, falha do hook na saída de erro, pausa e falha dos passos de workflow
por `send_message`, chamada HTTP do verificador por script.

Com o **Kiro CLI 2.31.0** (o binário oficial):

- `kiro-cli powers install <pasta>` instala o power em `~/.kiro/powers/installed/sdd/`, com todas as skills,
  `references/` e `assets/` — o caminho que a setup usa nos agentes;
- o bloco `permissions` dos templates foi gerado pelo próprio `kiro-cli agent upgrade` a partir do `toolsSettings`
  (V2) e conferido regra a regra; depois receberam o que só existe na V3: `skill` liberada (com leitura restrita o
  conversor avisa que cada skill pediria aprovação), `ask` de push/PR no orquestrador e de `curl`/`wget` no
  verificador. `subagent/<nome>` em `tools` e a regra `subagent` vêm do conversor (de `availableAgents` e
  `trustedAgents`);
- os seis agentes, com os placeholders preenchidos, passam no `kiro-cli agent validate`, aparecem no
  `kiro-cli agent list`, e o `kiro-cli agent upgrade --dry-run` os deixa intactos (`out of sync (not rebuilt)`);
- o formato `.md` de agente **não** é carregado pela engine V2 do CLI (ainda a padrão), por isso os agentes são
  JSON universais; padrões de comando encadeado (`cd … && …`) são descartados pelo conversor, por isso as
  permissões usam comandos simples;
- o `http.sh` foi exercitado contra um servidor local (método, caminho e corpo fora da pasta `massa/` recusados).

Não foi possível testar uma conversa (exige login) nem abrir a IDE.

**O que a documentação não resolve** (comportamento a observar no primeiro uso): o formato do `.config.kiro` das
specs; EARS em português no Analyze Requirements; se os subagentes somam ou intersectam os `allow` de quem os
chama (a doc diz "deny-wins intersection" — se um subagente do loop falhar por permissão, libere o comando também
no orquestrador); se um passo de workflow pode pedir aprovação; o alcance de `trustedAgents`; e as páginas de
steering e de configuração divergem sobre agentes herdarem o steering padrão (a setup oferece
`chat.disableInheritingDefaultResources` no CLI).

## Limitações conhecidas e próxima versão

- O `validate_workflow` do Kiro não confere se os agentes citados existem: a setup confere.
- Kiro Workflows é experimental: as receitas são opcionais; `/workflow-run` exige a IDE 1.3+.
- **v2:** toolkits oficiais (backend Java/Spring, Spring Batch, frontend Angular/React); execução automatizada dos
  casos de avaliação que a `sdd-aprender` já guarda em `<produto>/aprendizado/avaliacoes/`; e — quando o MCP do ELM
  suportar — atributo de chave, links entre requisitos, módulos, change sets e baselines automáticos.

## Fontes (consultadas em 13 e 14/10/2026)

- Andrej Karpathy — *Software Is Changing (Again)*, YC AI Startup School, jun/2025 · *2025 LLM Year in Review*,
  dez/2025 · notas sobre programar com agentes, jan/2026 · [autoresearch](https://github.com/karpathy/autoresearch),
  mar/2026 · [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), abr/2026 · Sequoia AI
  Ascent, abr/2026
- Matt Pocock — [mattpocock/skills](https://github.com/mattpocock/skills) (v1.3.1, out/2026: `grilling`, `to-spec`,
  `to-tickets`, `tdd`, `code-review`, `triage`, `retro`) · *Software Fundamentals Matter More Than Ever*, AI Engineer
  Europe 2026 · dicas de Ralph, jan/2026
- Dex Horthy / HumanLayer — [12-factor agents](https://github.com/humanlayer/12-factor-agents) ·
  [Advanced Context Engineering](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents) ·
  *No Vibes Allowed*, nov/2025 · *Everything We Got Wrong About RPI*, mar/2026 · *Why Software Factories Fail*, jul/2026
- Geoffrey Huntley — *Ralph Wiggum as a software engineer*, 2025 · [Ralph Playbook](https://github.com/ghuntley/how-to-ralph-wiggum), jan/2026
- Anthropic Engineering — *Effective context engineering for AI agents* (set/2025) · *Effective harnesses for
  long-running agents* (nov/2025) · *Demystifying evals for AI agents* (jan/2026) · *Harness design for long-running
  application development* (mar/2026) · [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Boris Cherny — fios sobre o fluxo de trabalho com Claude Code, jan/2026
- Simon Willison — *The lethal trifecta* (jun/2025) · *Vibe engineering* (out/2025) · *Agentic Engineering Patterns* (2026)
- Kent Beck — *Augmented Coding: Beyond the Vibes* (jun/2025) · crítica ao SDD citada por Martin Fowler (jan/2026)
- Birgitta Böckeler / Martin Fowler — [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
  (out/2025) · *Harness Engineering* (2026) · *Are Harnesses Worth the Cost?* (out/2026)
- Addy Osmani — *How to write a good spec for AI agents* (jan/2026) · *Comprehension debt* (mar/2026) · *Loop Engineering* (jun/2026)
- Mitchell Hashimoto — *My AI Adoption Journey* (fev/2026) · Armin Ronacher — *The Coming Loop* (jun/2026)
- Thoughtworks Technology Radar vol. 33 (nov/2025) e vol. 34 (abr/2026) · DORA *State of AI-assisted Software
  Development* 2025 · [GitHub Spec Kit](https://github.com/github/spec-kit)
- Kiro — [docs](https://kiro.dev/docs/) (powers, skills, custom agents, steering, specs, hooks, workflows),
  [kirodotdev/powers](https://github.com/kirodotdev/powers), [Agent Plugins](https://github.com/agentplugins/agent-plugins-spec),
  [Agent Skills](https://agentskills.io/specification)
- IBM — ELM 7.2 (dez/2025) · Engineering AI Hub 1.3/1.4 (MCP oficial, agente de geração de testes) · vocabulário
  [OSLC RM](https://github.com/oslc-op/oslc-specs)

## Licença

[MIT](../../LICENSE)
