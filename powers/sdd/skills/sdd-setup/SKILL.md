---
name: sdd-setup
description: "Configura o fluxo sdd num projeto: entende o repositório (tipos de projeto — backend, batch, frontend, mobile, dados —, stack, módulos, comandos de build e teste, como verificar o aceite, git, banco, ELM), descobre as skills disponíveis no projeto, na pasta do usuário, em outros powers e nos toolkits de stack, e cria os agentes sdd (produto, pesquisador, codificador, revisor, verificador, orquestrador) perguntando, agente por agente, a quais skills e MCPs cada um terá acesso — ex.: num projeto Spring Batch, as skills de batch e Java para o codificador. Gera o .kiro/steering/sdd.md (único steering do fluxo), a pasta do produto, .kiro/agents/sdd-*.json (formato universal do Kiro, validado pelo kiro-cli), hooks e workflows opcionais, e refaz tudo em modo atualização. Use em \"configurar o sdd\", \"setup do sdd\", \"criar os agentes do sdd\", \"atualizar os agentes do sdd\", \"ligar o toolkit\", \"atualizar a configuração do sdd\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.0.0"
---

# sdd-setup — Configurar o fluxo no projeto

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-setup/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

O power `sdd` só entrega skills (o formato de power do Kiro não instala steering, agentes, hooks nem workflows):
esta skill instala no projeto o que o fluxo precisa, a partir de [assets/](assets/), e é a **única** parte do
fluxo que conhece os toolkits de stack ([references/toolkits.md](references/toolkits.md)).

**Padrão primeiro.** O que tem padrão — detectado no projeto ou recomendado no template — é decidido **sem
perguntar** e aparece numa tabela **Padrões aplicados** ao fim de cada bloco (projeto, git, produto, ELM,
autonomia, automações), com **uma** confirmação: "ok" aceita tudo, ou a pessoa diz só a linha que muda. **Pergunte**
apenas o que não tem padrão nem dá para detectar (ex.: a URL do ambiente de teste, qual `pa_*.json` é o padrão quando
há mais de um), uma coisa por vez, mostrando o que foi detectado. Nunca pergunte o que só confirma um padrão.
Não achou o que procurava (arquivo, pasta, power, configuração) → **pergunte** onde está; nunca conclua "não há"
sem a pessoa confirmar. Nada é gravado antes do resumo do Passo 8 e do "ok". Nunca leia nem mostre arquivos de
credenciais.

## Passo 0 — Onde estou

Rode esta skill na **sessão padrão** do Kiro (sem agente `sdd-*`): ela grava em `.kiro/steering`, `.kiro/agents`,
`.kiro/hooks` e `.kiro/workflows`, que os agentes do fluxo não podem escrever. Num agente `sdd-*` → peça para
trocar para a sessão padrão e pare.

1. **Raiz do repositório:** `git rev-parse --show-toplevel` (sem git → avise: o fluxo depende de branches e PRs).
2. **Pasta do power instalado** (`{{POWER}}` dos templates): o Kiro instala em `~/.kiro/powers/installed/sdd/`
   (conferido com o `kiro-cli` 2.31). Confirme que `skills/sdd-setup/SKILL.md` existe ali; senão procure
   (`find ~/.kiro/powers -path '*sdd/skills/sdd-setup/SKILL.md'`) ou use a pasta de onde esta skill foi
   carregada. Escreva o caminho **relativo ao home** (`~/.kiro/powers/installed/sdd`), com `/`. Não achou →
   pergunte à pessoa onde o power está.
   `KIRO_HOME` definida → o Kiro guarda a configuração global ali, não em `~/.kiro`: procure o power em
   `$KIRO_HOME/powers/installed/sdd/`; fora do home, avise que os agentes gerados só valerão nesta máquina e peça
   "ok" para usar o caminho absoluto.
3. **Caminhos nos arquivos gerados — sempre relativos, nunca absolutos** (são versionados e usados em Linux,
   macOS e Windows): do projeto → relativos à raiz (`file://.kiro/steering/sdd.md`); do power ou do usuário →
   relativos ao home (`skill://~/.kiro/powers/installed/sdd/skills/...`, `skill://~/.kiro/skills/...`); separador
   `/`; nunca `/home/…`, `/Users/…`, `C:\…`, `\` nem variáveis de ambiente.
4. **Modo:** já existe `.kiro/steering/sdd.md` ou `.kiro/agents/sdd-*.json` → **atualização**: mostre a
   configuração atual numa tabela e pergunte o que mudar ("nada — só regenerar os agentes", útil depois de
   atualizar o power ou um toolkit). Refaça só o que mudou nas respostas, mas agentes, hook e workflows
   **sempre** a partir dos templates atuais do power (com os valores do projeto), mesmo os que já têm o nome certo
   — renomear um arquivo antigo não o atualiza. Mostre o diff de cada um.
   **Configurado com o nome `sdd2`** (o nome deste fluxo antes da v2: `.kiro/steering/sdd2*.md`,
   `.kiro/agents/sdd2-*.json`) → proponha a migração, com o plano numa só mensagem e "ok":
   - `.kiro/steering/sdd2.md` e `sdd2-projeto.md` → os valores vão para as seções do novo `.kiro/steering/sdd.md`;
     `sdd2-licoes.md` → as regras promovidas vão para a seção Regras aprendidas, sem perder nenhuma;
     `sdd2-fechar-sessao.md` → removido (fechar a sessão agora é da `sdd-status`). Todos saem do repositório;
   - `.kiro/agents/sdd2-*.json` → removidos (os `sdd-*.json` são gerados de novo pelo Passo 8);
     `.kiro/hooks/sdd2.json` → `.kiro/hooks/sdd.json`; `.kiro/workflows/sdd2-*.workflow.json` →
     `.kiro/workflows/sdd-*.workflow.json`; `.kiro/sdd2/http.sh` → `.kiro/sdd/http.sh`;
   - `.kiro/produto/` → a pasta do produto (Passo 4) e `.kiro/aprendizado/` → `<produto>/aprendizado/`;
   - tudo com `git mv`/`git rm` (arquivo não versionado → `mv`/`rm`), sem mudar o conteúdo dos movidos; diga que
     as fatias em andamento (`.kiro/specs/`) não mudam.
5. **Vindo da v1 do `sdd`?** Existe `.kiro/steering/sdd-projeto.md` sem `.kiro/steering/sdd.md` → ofereça
   reaproveitar dele: steering, branch base, prefixo, padrão de commit, ferramenta de PR, comandos, gate de
   cobertura, banco, testes funcionais, ELM e skills por agente. Os agentes `sdd-codificador`, `sdd-revisor` e
   `sdd-orquestrador` da v1 têm o mesmo nome dos novos: são **substituídos** no Passo 8 (mostre o diff). O que só a
   v1 tinha sai com `git rm` e "ok": `.kiro/agents/sdd-especificador.json`, `.kiro/agents/prompts/sdd-*.md` e
   `.kiro/steering/sdd-projeto.md`.

## Passo 1 — Entender o projeto

Leia antes de perguntar: `README*`, `AGENTS.md`, `CONTRIBUTING*`, `.kiro/steering/*.md`, arquivos de build na
raiz e nos módulos (`pom.xml`, `build.gradle*`, `package.json`, `pyproject.toml`, `go.mod`, `*.csproj`,
`Cargo.toml`, `Makefile`), a árvore de pastas (2–3 níveis) e os últimos `git log --oneline -20`.

Proponha numa só mensagem e confirme:

```
🔎 Entendi assim — <nome do projeto>
Tipos: batch (spring-batch-core em batch/pom.xml) + backend (spring-boot-starter-web em api/pom.xml)
Stack: Java 21 · Spring Boot 3.3 · Spring Batch 5 · Oracle (ojdbc11) · Maven multi-módulo (api, batch, comum)
Testes: JUnit 5 + Spring Batch Test · cobertura JaCoCo (gate 80% em pom.xml)
Steering: product.md ✅ · tech.md ✅ · structure.md ❌
Está certo? (sim / corrija)
```

Tipos de projeto e sinais: tabela de [references/toolkits.md](references/toolkits.md). Depois:

- **Steering de produto/tecnologia/estrutura:** padrão do Kiro (`.kiro/steering/product.md`, `tech.md`,
  `structure.md`) → confirme; faltando → pergunte, um papel por vez, qual arquivo faz aquele papel (liste os `.md`
  candidatos) ou ofereça gerar (o Kiro tem "Generate Steering Docs"); "nenhum" é resposta válida.
- **Regras críticas:** leia o steering de tecnologia/estrutura e proponha as regras que, violadas, causam perda de
  dado, duplicidade ou falha em produção; a pessoa confirma, edita ou diz "nenhuma além do steering".

## Passo 2 — Backpressure e verificação

Proponha os comandos (do arquivo de build, do steering, do README ou dos `comandos` do toolkit detectado) e
**ofereça rodá-los uma vez** — backpressure que não roda não é backpressure:

| Item | Como detectar |
|---|---|
| compilar, testes, teste único, lint, cobertura + gate | build + plugins de teste/cobertura/lint configurados |
| executar a aplicação/job | README, scripts, `spring-boot:run`, `npm start`, parâmetros de job |
| exercitar e verificar um cenário | tipo de projeto (tabela do `toolkits.md`) + `verificacao` do toolkit |
| massa de teste | pastas `massa/`, `seed/`, `fixtures/`, `src/test/resources/` |

Falhou ao rodar → mostre o erro; a pessoa decide (corrigir o comando, seguir assim ou parar).

## Passo 3 — Git, PR e banco

| Item | Como detectar |
|---|---|
| Branch base | `git symbolic-ref refs/remotes/origin/HEAD`; `develop`/`main`/`master` — vai também no `{{BASE}}` dos agentes (push para a base negado) |
| Prefixo da branch | branches remotas existentes; padrão `feature/` |
| Padrão de commit | `git log --oneline -20` (Task/IB do EWM? Conventional Commits?) |
| PR (merge request) | pelo MCP **`gitlabpr`** do power (GitLab, API v4, CE 10.8+; projeto vem do `origin` da raiz do workspace, informada em `pasta` a cada chamada; fora de um repositório, a URL do projeto colada pela pessoa vai em `url_projeto`). Teste uma vez com `gitlab_listar_mrs(pasta=<raiz do workspace>, limite=1)`: respondeu → `MCP gitlabpr`. Erro de credencial → mostre o modelo de `~/.config/mcp-gitlabpr/gitlabpr.properties` (`url` do GitLab e `token` pessoal com escopo `api`; a pessoa cria o arquivo, o agente não lê nem grava credencial) e teste de novo. `origin` fora do GitLab, ou a pessoa segue sem credencial → "entregar título e descrição" (troca depois por "atualizar a configuração do sdd"). Nunca `gh` nem `glab` |
| MCP de banco | servidores em `.kiro/settings/mcp.json` e `~/.kiro/settings/mcp.json` — qual é o de consulta e **qual tool** só consulta (ou "não há"); recomende um usuário de banco somente leitura |
| Artefatos de produto | a base é protegida? → `PR curto para a base`; senão o padrão também é `PR curto para a base` (a pessoa troca por `direto na branch base` na tabela) |

## Passo 4 — Produto, conhecimento e ELM

1. **Pasta do produto** (`{{PRODUTO}}` dos templates e `<produto>` nas skills): onde ficam `backlog.md`, épicos
   e PRDs, planejamento e aprendizado — versionada. Já existe um `backlog.md` do sdd no repositório → a pasta dele;
   senão o padrão `.kiro/planejamento`. Vai para os Padrões aplicados. Grave o caminho real na seção Projeto do
   `sdd.md`.
2. **Glossário** (padrão `docs/glossario.md`) e **ADRs** (padrão `docs/adr`, sem barra no fim) — use os que já
   existirem; não existindo, o padrão é criá-los (Padrões aplicados). A pessoa recusou na tabela → registre
   "não há" e remova dos agentes as regras e linhas que os citam (`{{GLOSSARIO}}`, `{{ADR}}`).
3. **ELM** — o MCP `elm` vem com o power. `.kiro/config/sdd/pa_*.json` no repositório (um por project area)?
   - Não há e a pessoa diz que o projeto não usa ELM → `Usa ELM: não` (o fluxo funciona igual; os ids vêm do
     `backlog.md`).
   - **Gerar o `pa`:** `elm_status` (sem `projeto`) confere a credencial — erro `credencial` → peça o
     `~/.config/mcp-elm/elm.properties` (`server`, `user`, `password`; você não lê nem grava esse arquivo) e pare.
     Pergunte um trecho do nome da project area do EWM (e do DOORS Next e do ETM, se forem outras) →
     `elm_setup_descobrir(ccm, rm?, qm?)` devolve PAs, times e categorias, os tipos do fluxo com campos, obrigatórios
     e `enumeracoes`, links, iterações recentes, pastas e tipos do RM. A PA também exige campos por regra de processo,
     que não vêm como obrigatórios: chame de novo com `valores_de` = as `enumeracoes` que o fluxo grava (na Tarefa,
     categoria de horas, OTR e classificação; no IB, a categoria) para ter os valores. Monte o `pa` pelo schema
     [assets/pa.schema.json](assets/pa.schema.json), **sem perguntas** onde der, e mostre numa tabela só
     (**ELM — padrões aplicados**) para um "ok" ou a linha que muda:

     | Item | Padrão |
     |---|---|
     | Time e categoria (`filedAgainst`) | o time de quem configura; a categoria dele |
     | Tipos `ib` · `defeito` · `tarefa` | Item de Backlog (também o épico, se a PA não tem Épico) · Defeito · Tarefa |
     | Campos de cada tipo | os obrigatórios + Planejado para, Responsável, Estimativa e, no IB, o de critérios de aceite (nome com "aceite") |
     | `obrigatorios` | os campos que a PA exige por processo, além dos que o tipo marca (Tarefa: Estimativa, Clarity, categoria de horas, OTR; Defeito: ex.: Ambiente) |
     | `padroes` | um valor por obrigatório de enumeração, o mais próximo do trabalho (IB: "Melhoria"; Tarefa: categoria de horas, OTR, Clarity; Defeito: os que a PA exige por processo, ex.: Ambiente) |
     | `por-prefixo` (Tarefa) | classificação por prefixo: `[ESP]` análise · `[DEV]` desenvolvimento · `[VER]` testes · `[ATD]` suporte · demais "outra" |
     | Links | pai, filhos, implementa, relacionado; `depende` só se a PA tiver |
     | Horas | o time code e o tipo de trabalho padrão da PA |
     | Artefatos do RM `HF` · `REG` · `GL` · `ET` | tipo e pasta por proximidade de nome |
     | Bundle (`rm.download`) | `docs/elm/<nome>` |
     | `qm` | a PA do ETM associada; não há → sem casos de teste no ETM (o `CT.csv` fica) |

     Valor sem nome parecido → aí sim pergunte, só esse. "Planejado para" não vai em `padroes` (é sempre a iteração
     da sprint). Com "ok", grave `.kiro/config/sdd/pa_<nome>.json` (caminho relativo à raiz, `/`, sem segredos — vai
     para o git) e confira com `elm_status(projeto)`: `valido` e `faltando` vazio. **Validação opcional** (a PA
     recusa o que o `pa` não cobre): com "sim", `elm_criar_wi` de uma tarefa `[TESTE] sdd-setup` (pai = um IB que a
     pessoa indicar), de um IB e de um defeito, e `elm_transicao` de cada um até concluir → cada recusa `precondicao` traz o `campo`
     que a PA exige por regra de processo (na criação, numa mudança de estado ou no lançamento de horas, mesmo que o
     tipo o marque como opcional): ponha-o em `obrigatorios` do tipo e o valor em `padroes` (pegue-o por
     `valores_de`) e tente de novo — daí em diante o MCP o exige já na criação. Os itens criados a pessoa cancela
     na UI. Outra project area → repita (outro `pa_<nome>.json`) e diga na seção ELM qual é o padrão.
   - Seção ELM do `sdd.md`, também sem perguntas: publicar requisitos `na-aprovacao`, ET `não publica`, manual
     `nada`, pontos `não`, fatia dividida "filhos do item original", categoria do IB de defeito (o valor de
     correção), títulos das tarefas e colunas do `CT.csv` do template. Sustentação e Atendimento não são
     perguntados: nascem na primeira sprint ([elm-sprint.md](../sdd-planejamento/references/elm-sprint.md) §2).
   - **Bundle do RM** (`rm.download` do `pa`): pastas com `index.md` de `okf_version` → mostre e confirme; vazio →
     ofereça a `elm-sync` (baixar). É a base que os agentes consultam **pelo MCP `okf`**, nunca lendo os arquivos —
     rode `okf_index` (`root` = raiz do repositório + `rm.download`, absoluto) até `restantes=0` e mostre quantos
     documentos há; o caminho vai no `{{BUNDLE}}` dos agentes, como leitura negada (no `.gitignore` → avise que só
     existe nesta máquina, depois da `elm-sync`).

## Passo 5 — Inventário de skills e toolkits

Siga [references/toolkits.md](references/toolkits.md): procure toolkits (com e sem manifesto) e skills avulsas
do projeto (`.kiro/skills/*/SKILL.md`), do usuário (`~/.kiro/skills/*/SKILL.md`) e de outros powers
(`~/.kiro/powers/installed/*/skills/*/SKILL.md`; não achou nada ali → `~/.kiro/powers/**/skills/*/SKILL.md`),
**exceto** as do fluxo (`sdd`, `sdd-*`, `elm-*` deste power, e `sdd2`, `sdd2-*` de uma instalação antiga). Para cada uma:
nome, início da `description`, origem e, se houver, toolkit e papéis. Toolkit cujo `deteccao` casa com o projeto
→ "detectado".

## Passo 6 — Agentes, um de cada vez

Para cada agente, nesta ordem, monte a proposta com o inventário **agrupado por toolkit/origem** e as skills
pré-marcadas pelos `papeis` do toolkit e pelo tipo de projeto (formato em `toolkits.md`):

| Agente | Já tem (do fluxo) | Sugestão de extras |
|---|---|---|
| `sdd-produto` | triar, entrevistar, especificar, prd, fatiar, planejamento, atender, consolidar, aprender (registrar), iniciar, status | skills de domínio/negócio |
| `sdd-pesquisador` | pesquisar | skills de stack para ler o código (ex.: `java`) |
| `sdd-codificador` | desenvolver, plano, implementar, iniciar, status | skills de stack e de teste do toolkit (ex.: `spring-batch-job`, `java`) |
| `sdd-revisor` | revisar, iniciar, status | skills de padrões e de revisão da stack |
| `sdd-verificador` | verificar, iniciar, status | skills de teste de aceite (Playwright, teste de job, API) |
| `sdd-orquestrador` | loop, desenvolver, plano, implementar, status | normalmente nenhuma |

Aprender e setup rodam na **sessão padrão** (sem agente); o modo registrar da aprender também no `sdd-produto`,
na consolidação. A consolidação é do P.O. ou do SM, no `sdd-produto`
(grava na base, publica a ET *as-built* e os casos de teste).

Para cada agente, **uma mensagem só**: a proposta completa já marcada pelos padrões e **uma** confirmação ("ok", ou
o que muda — marcar/desmarcar uma skill, um MCP, trocar o modelo). Nada é perguntado item a item:

```
🤖 sdd-codificador — já tem: desenvolver, plano, implementar, iniciar, status
Skills  [x] java (toolkit java)  [x] spring-batch-job (toolkit batch)  [ ] angular (toolkit front)
MCPs    [x] elm (leitura; escrita com confirmação)  [x] banco: @<servidor>/<tool de consulta>
Modelo  padrão do Kiro
Subagentes  sdd-pesquisador, sdd-revisor, sdd-verificador  [ ] <agente do projeto> — <para quê>
ok?
```

Padrões da proposta:
1. **Skills:** marcadas só as de toolkits **detectados** com o papel do agente; as outras aparecem desmarcadas.
2. **MCPs:** o de banco entra como somente leitura em pesquisador, codificador, revisor e verificador — só a tool
   de consulta (`@<servidor>/<tool>`), nunca o servidor inteiro se ele tiver tool de escrita; browser/Playwright
   marcado no verificador em projeto `frontend`. **ELM** (projeto com ELM): as tools `@elm/elm_*` que o template de cada agente já traz (leitura liberada; escrita
   com `ask`) — `sdd-produto`, `sdd-codificador`, `sdd-orquestrador`, `sdd-revisor` e `sdd-verificador` (estes dois
   só para a própria tarefa); o pesquisador não tem. Projeto sem ELM ou desmarcado pela pessoa → tire as `@elm/…` e
   as regras `sdd/elm/…` do agente (a escrita vira `ELM pendente`).
3. **Modelo:** sempre o padrão do Kiro — não pergunte; a pessoa troca na proposta se quiser.
4. Só codificador e orquestrador: **subagentes** — os `sdd-*` do fluxo marcados; agentes do projeto
   (`.kiro/agents/*`, `~/.kiro/agents/*`, exceto `sdd-*`) listados desmarcados, com o tipo de tarefa que a descrição
   deles indica. Agente com o campo `hooks` (mesmo vazio) é ignorado pela IDE: fica desmarcado, com o aviso.

Registre também as skills **oferecidas e recusadas** por agente (coluna própria no `sdd.md`): no modo
atualização, só skill que não está em nenhuma das duas colunas é "nova".

Depois, a autonomia (seção Git, banco e autonomia do template), **sem perguntas** — Padrões aplicados: GATE do
plano pela senioridade de quem implementa (fixo: Júnior sempre, Pleno pergunta, Sênior nunca — `sdd-plano` Passo 5);
paralelismo do loop `1`; push e PR no loop perguntando a cada lote (o orquestrador tem regra `ask` para push e PR, então
o Kiro confirma cada um; a pessoa muda para "não — a pessoa abre" → a regra vira `deny`); **push pelo agente**
no codificador, no revisor e no verificador (fixo, não é perguntado): no bloco V3, `git push *` com `ask` (o Kiro
pergunta sempre), com as negações do orquestrador (`--force`, `-f`, `+ref`, `:ref`, `--mirror`, `--all`, `--prune`,
`--delete`) e a do push para a branch base (`{{BASE}}`); revisor e verificador só publicam a branch do PR; no bloco
V2 (sem `ask`) o push fica negado — o agente entrega o comando pronto e espera a pessoa dizer que publicou; e, se a verificação chama a
aplicação por HTTP, o **script de chamada** do verificador `.kiro/sdd/http.sh` (o verificador roda só esse script sem
perguntar, só contra a URL de teste e com corpo da pasta `massa/`; precisa de `sh` e `curl`; a pessoa pode trocar por
"nenhum": cada `curl` pede confirmação, e no loop a verificação fica para a sessão dela). A única pergunta aqui é a
**URL base do ambiente de teste**, quando não está no repositório (`.env.example`, `application-*.yml`, README).
Nunca uma URL de produção.

## Passo 7 — Hook e workflows (opcionais)

Padrões aplicados, conforme [references/automacoes.md](references/automacoes.md): hook `sdd-backpressure` **ligado**
quando há comandos de compilar e testar; receitas de Kiro Workflows **instaladas** só quando o recurso já está
habilitado (`kiroAgent.workflows.enabled` ou `chat.enableWorkflows`), senão de fora. Na tabela, diga quem dispara as
receitas (a pessoa, no chat do Kiro; nenhum agente as dispara) e que os dois exigem a IDE ou a engine V3 do
`kiro-cli`. A pessoa tira um da tabela → não instale.

## Passo 8 — Montar, mostrar, gravar

Em memória:
1. `.kiro/steering/sdd.md` ← [assets/steering/sdd.md](assets/steering/sdd.md) com as respostas (nada de `<…>`
   sobrando; o que não se aplica fica "não há"/"nenhum"). É o **único** steering do fluxo. No modo atualização, a
   seção Regras aprendidas fica como está (nunca apague regras promovidas).
2. `.kiro/agents/sdd-<agente>.json` ← [assets/agents/](assets/agents/), para cada agente, montados como manda
   [references/agentes.md](references/agentes.md): placeholders, skills, MCPs, comandos e caminhos **nos dois
   blocos** (V2 e V3) em espelho; as regras só da V3 ficam; nunca regenere o bloco `permissions` pelo `kiro-cli`.
3. Hook e workflows escolhidos (Passo 7); script de chamada do verificador, se escolhido (Passo 6):
   `.kiro/sdd/http.sh` ← [assets/scripts/http.sh](assets/scripts/http.sh) com `{{URL_TESTE}}` trocado pela URL
   base do ambiente de teste (sem barra no fim).
4. `<produto>/` (só o que não existir): `backlog.md` mínimo
   (`# Backlog — <nome>`, `Próximos ids: EP-01 · FT-001 · AT-001`, `Sustentação: —` e as tabelas `## Épicos`,
   `## Fatias — sem épico` e `## Atendimentos` vazias — formato na `sdd-fatiar`),
   `<produto>/aprendizado/licoes.md` com o título `# Lições` (a pasta `atendimentos/` nasce
   com o primeiro AT, pela `sdd-triar`) e `fatias/` (as fichas). O `equipe.json` e o `acordos.md` não: são da
   `sdd-planejamento` (modo inicial), que só grava a equipe depois dos acordos (cadência e duração da sprint). No modo atualização, acrescente só o que falta —
   nunca recrie o que existe; subpasta `<produto>/planejamento/` (layout da 2.6.0) →
   ofereça mover o conteúdo dela para a raiz de `<produto>/` com `git mv` (com "ok"), sem sobrescrever o que já
   estiver lá, e apagar a subpasta vazia.
5. `.gitignore`: acrescente `.kiro/local/` se faltar. Migração do layout antigo (Passo 0), se aceita.

Mostre o resumo e, no modo atualização, o diff de cada arquivo que muda:

```
⚙️ sdd — <projeto> · tipos <…> · toolkits <…>
Comandos: compilar <…> · testes <…> · lint <…> · cobertura <…> (rodados: ok)
Verificação: <como> · Git: base <…> · prefixo <…> · PR <…> · Banco: <MCP | não há> · ELM: <…>
| Agente | Skills extras | MCPs | Modelo |
Hooks: <…> · Workflows: <…> · Autonomia: GATE do plano pela senioridade · paralelo <n>
Arquivos: .kiro/steering/sdd.md · .kiro/agents/sdd-*.json · .kiro/hooks/… · .kiro/workflows/… · .kiro/sdd/…
          <produto>/ · .gitignore
Gravar? ("ok")
```

Agente existente e editado à mão → mostre o diff e pergunte antes de sobrescrever. O Kiro pede confirmação para
cada arquivo gravado em `.kiro/agents/`, `.kiro/hooks/` e `.kiro/workflows/` — avise antes.

## Passo 9 — Validar

- JSON de cada agente faz parse; `name` = nome do arquivo; nenhum `{{…}}` sobrando; agente com `@<servidor>/…` de MCP do
  projeto em `tools` tem `"includeMcpJson": true` e a regra `mcp` (`allow` para as de leitura, que também estão em
  `allowedTools`; `ask` para as de escrita, que **não** estão em `allowedTools`); as do `okf` e do `gitlabpr` (MCPs do power)
  ficam na regra `power` (`sdd/okf/<tool>`, `sdd/gitlabpr/<tool>`, `sdd/elm/<tool>`), nunca na `mcp`; `includePowers:
  true` em todos; nenhuma `@elm/…` no pesquisador nem servidor `elm` no `mcp.json` do projeto; `.kiro/steering/` tem só o
  `sdd.md` do fluxo (nenhum `sdd2*.md` nem `sdd-projeto.md` sobrando), e nenhum `.kiro/agents/sdd2-*.json`.
- Ferramentas que varrem a raiz do repositório (test runners, linters, `tsc`, varredura de arquivos) ignoram
  `.kiro/local/` — onde o loop cria as worktrees? Não ignoram → acrescente a exclusão na configuração delas (com
  "ok") ou registre no `sdd.md` que o loop não deve ser usado.
- Todo `skill://` e `file://` aponta para arquivo existente (resolvendo `~` no home e o resto a partir da raiz) e
  é relativo — nenhum `/…` absoluto, `C:\…`, `\` ou variável.
- JSON dos hooks e workflows faz parse; agentes citados nos workflows existem em `.kiro/agents/` (o validador de
  receitas não confere isso). Com Workflows ligado, peça ao Kiro `validate_workflow` em cada
  `.kiro/workflows/*.workflow.json`; erro → mostre-o e ofereça remover o arquivo (o fluxo funciona sem ele).
- `kiro-cli` disponível → para cada agente, `kiro-cli agent validate --path .kiro/agents/<agente>.json` (saída
  vazia = válido; erro aponta o campo); `kiro-cli agent list` (na raiz do repositório) lista os seis;
  `kiro-cli agent upgrade --dry-run .kiro/agents` diz `out of sync (not rebuilt)` para eles — esperado (ver
  [references/agentes.md](references/agentes.md)). No CLI V3, `/config` e `/hooks` mostram os agentes, as
  permissões e o hook carregados.
- Herança: por padrão, agentes customizados recebem também o steering, as skills e o `AGENTS.md` padrão do
  workspace e do usuário — as skills de `~/.kiro/skills` chegam a todos, além das escolhidas no Passo 6. Para que
  cada agente tenha só as suas, no CLI: `kiro-cli settings --workspace chat.disableInheritingDefaultResources
  true` (ofereça; a IDE não documenta essa opção).
- Workspace não confiável → avise: até a pessoa confiar nele, o Kiro não carrega os agentes, o steering, as skills
  e os workflows do projeto e pergunta antes de cada comando de shell.

Sugira o commit (`.kiro/steering/sdd.md`, `.kiro/agents/sdd-*.json`, `.kiro/hooks/`, `.kiro/workflows/`,
`.kiro/sdd/`, `<produto>/`, `.gitignore` e o que a migração moveu ou removeu) — só com confirmação — e termine
com o próximo passo — sem `<produto>/equipe.json`, primeiro "monte o planejamento" (`sdd-planejamento`, modo
inicial: equipe com a senioridade, acordos e roadmap; sem ela não há modo da fatia, GATE do plano nem revisor); depois
"nova demanda: …" (`sdd-triar`: faz a triagem e registra no backlog; épico → `sdd-prd`), "iniciar <id>" ou "minha próxima tarefa"
(`sdd-iniciar`: o hub diz a skill do papel) ou "onde parei?" (`sdd-status`).

## Regras

- Não altere nada fora de `.kiro/`, da pasta do produto, do glossário/ADRs que a pessoa pediu para criar e do
  `.gitignore`.
- As skills `sdd-*` ficam no power — nunca as copie para o projeto (uma atualização do power as atualiza; depois
  rode esta skill em modo atualização para refazer caminhos e agentes).
- Toolkit nunca é ligado sem a pessoa dizer sim, agente por agente.
