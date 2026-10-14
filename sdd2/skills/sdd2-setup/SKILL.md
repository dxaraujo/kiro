---
name: sdd2-setup
description: "Configura o fluxo sdd2 num projeto: entende o repositório (tipos de projeto — backend, batch, frontend, mobile, dados —, stack, módulos, comandos de build e teste, como verificar o aceite, git, banco, ELM), descobre as skills disponíveis no projeto, na pasta do usuário, em outros powers e nos toolkits de stack, e cria os agentes sdd2 (produto, pesquisador, codificador, revisor, verificador, orquestrador) perguntando, agente por agente, a quais skills e MCPs cada um terá acesso — ex.: num projeto Spring Batch, as skills de batch e Java para o codificador. Gera .kiro/steering/sdd2*.md, .kiro/agents/sdd2-*.md, hooks e workflows opcionais, e refaz tudo em modo atualização. Use em \"configurar o sdd2\", \"setup do sdd2\", \"criar os agentes do sdd2\", \"atualizar os agentes do sdd2\", \"ligar o toolkit\", \"atualizar a configuração do sdd2\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-setup — Configurar o fluxo no projeto

O power `sdd2` só entrega skills (o formato de power do Kiro não instala steering, agentes, hooks nem workflows):
esta skill instala no projeto o que o fluxo precisa, a partir de [assets/](assets/), e é a **única** parte do
fluxo que conhece os toolkits de stack ([references/toolkits.md](references/toolkits.md)).

**Pergunte uma coisa por vez**, sempre mostrando o que foi detectado e a opção recomendada ("sim" aceita).
Nada é gravado antes do resumo do Passo 8 e do "ok". Nunca leia nem mostre arquivos de credenciais.

## Passo 0 — Onde estou

1. **Raiz do repositório:** `git rev-parse --show-toplevel` (sem git → avise: o fluxo depende de branches e PRs).
2. **Pasta do power instalado** (`{{POWER}}` dos templates): procure, nesta ordem, até achar
   `skills/sdd2-setup/SKILL.md`:
   `~/.kiro/powers/installed/sdd2/` → qualquer `~/.kiro/powers/**/sdd2/` (`find ~/.kiro/powers -path
   '*sdd2/skills/sdd2-setup/SKILL.md'`) → a pasta de onde esta skill foi carregada. Escreva o caminho **relativo
   ao home** (`~/.kiro/powers/installed/sdd2`), com `/`. Não achou → pergunte à pessoa onde o power está.
3. **Caminhos nos arquivos gerados — sempre relativos, nunca absolutos** (são versionados e usados em Linux,
   macOS e Windows): do projeto → relativos à raiz (`file://.kiro/steering/sdd2.md`); do power ou do usuário →
   relativos ao home (`skill://~/.kiro/powers/installed/sdd2/skills/...`, `skill://~/.kiro/skills/...`); separador
   `/`; nunca `/home/…`, `/Users/…`, `C:\…`, `\` nem variáveis de ambiente.
4. **Modo:** já existe `.kiro/steering/sdd2-projeto.md` ou `.kiro/agents/sdd2-*.md` → **atualização**: mostre a
   configuração atual numa tabela e pergunte o que mudar ("nada — só regenerar os agentes", útil depois de
   atualizar o power ou um toolkit). Refaça só o que mudou.
5. **Vindo do power `sdd` (v1)?** Existe `.kiro/steering/sdd-projeto.md` → ofereça reaproveitar dele: steering,
   branch base, prefixo, padrão de commit, ferramenta de PR, comandos, gate de cobertura, banco, testes funcionais,
   ELM e skills por agente. Os dois fluxos convivem; o sdd2 não altera arquivos do `sdd`.

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
| Branch base | `git symbolic-ref refs/remotes/origin/HEAD`; `develop`/`main`/`master` |
| Prefixo da branch | branches remotas existentes; padrão `feature/` |
| Padrão de commit | `git log --oneline -20` (Task/IB do EWM? Conventional Commits?) |
| Abrir PR | `gh`/`glab` no PATH e o host do `origin`; senão "entregar título e descrição" |
| MCP de banco | servidores em `.kiro/settings/mcp.json` e `~/.kiro/settings/mcp.json` — qual é o de consulta e **qual tool** só consulta (ou "não há"); recomende um usuário de banco somente leitura |
| Artefatos de produto | a base é protegida? → `PR curto para a base`; senão pergunte (`direto na branch base` ou PR) |

## Passo 4 — Conhecimento e ELM

1. **Glossário** (padrão `docs/glossario.md`) e **ADRs** (padrão `docs/adr`, sem barra no fim) — use os que já
   existirem; não existindo, pergunte "criar `docs/glossario.md` e `docs/adr`? (recomendado)". Recusou → registre
   "não há" e remova dos agentes as regras e linhas que os citam (`{{GLOSSARIO}}`, `{{ADR}}`).
2. **ELM:** power `elm` instalado (`~/.kiro/powers/**/elm/`) e `.kiro/config/power/elm/pa_*.json` no repositório?
   - Sem power → `Usa ELM: não` (o fluxo funciona igual; os ids vêm do `backlog.json`).
   - Com power e sem `pa_*.json` → ofereça rodar a `elm-setup` antes (ela mapeia tipos, pastas, iterações).
   - Com `pa_*.json`: proponha o mapeamento da seção ELM do template (tipos e pastas pelos nomes do
     `rm.requirements-types`/`rm.folders`/`workitem-types`, por proximidade) e pergunte, um de cada vez: quando
     publicar os requisitos (`na-aprovacao` recomendado), quando criar os itens no EWM (`na-sprint` recomendado —
     sprints futuras mudam), se publica ET as-built, o que o processo exige manualmente no DOORS Next (change set,
     módulo, baseline), pontos por tamanho, o template de tarefas por fatia e as colunas do `CT.csv` (tabela
     Testes (ETM): tipo, status inicial, categoria — pergunte pelo template de importação do ETM do projeto).
   - Bundle do RM no repositório (`rm.download.path`) → registre em Conhecimento: é a base que os agentes leem.

## Passo 5 — Inventário de skills e toolkits

Siga [references/toolkits.md](references/toolkits.md): procure toolkits (com e sem manifesto) e skills avulsas
do projeto (`.kiro/skills/*/SKILL.md`), do usuário (`~/.kiro/skills/*/SKILL.md`) e de outros powers
(`~/.kiro/powers/installed/*/skills/*/SKILL.md`; não achou nada ali → `~/.kiro/powers/**/skills/*/SKILL.md`),
**exceto** as `sdd2-*` e as `sdd-*` (fluxos), e as do power `elm` (o ELM fica na sessão da pessoa). Para cada uma:
nome, início da `description`, origem e, se houver, toolkit e papéis. Toolkit cujo `deteccao` casa com o projeto
→ "detectado".

## Passo 6 — Agentes, um de cada vez

Para cada agente, nesta ordem, mostre o inventário **agrupado por toolkit/origem**, com as skills pré-marcadas
pelos `papeis` do toolkit e pelo tipo de projeto, e pergunte (formato em `toolkits.md`):

| Agente | Já tem (do fluxo) | Sugestão de extras |
|---|---|---|
| `sdd2-produto` | entrevistar, prd, fatiar, planejamento | skills de domínio/negócio |
| `sdd2-pesquisador` | pesquisar | skills de stack para ler o código (ex.: `java`) |
| `sdd2-codificador` | plano, implementar | skills de stack e de teste do toolkit (ex.: `spring-batch-job`, `java`) |
| `sdd2-revisor` | revisar | skills de padrões e de revisão da stack |
| `sdd2-verificador` | verificar | skills de teste de aceite (Playwright, teste de job, API) |
| `sdd2-orquestrador` | loop, iniciar, status | normalmente nenhuma |

Para cada agente, nesta sequência — **uma pergunta por mensagem**:
1. **Skills** (o inventário acima). Pré-marcadas só as de toolkits **detectados** com o papel do agente.
2. **MCPs** (lista dos servidores configurados): o de banco entra como somente leitura em pesquisador,
   codificador, revisor e verificador — ligue só a tool de consulta (`@<servidor>/<tool>`), nunca o servidor
   inteiro se ele tiver tool de escrita; browser/Playwright é sugerido para o verificador em projeto `frontend`.
   **Nunca ofereça o MCP `elm`** — o ELM é do power `elm`, com as regras das skills dele, na sessão da pessoa.
3. **Modelo** (opcional; padrão: o do Kiro). Ex.: um modelo mais rápido para o pesquisador.
4. Só codificador e orquestrador: **agentes do projeto** (`.kiro/agents/*`, `~/.kiro/agents/*`, exceto `sdd2-*`)
   que podem ser chamados como subagentes, e para que tipo de tarefa.

Registre também as skills **oferecidas e recusadas** por agente (coluna própria no `sdd2-projeto.md`): no modo
atualização, só skill que não está em nenhuma das duas colunas é "nova".

Depois, a seção **Autonomia** do template, uma pergunta por vez: plano de fatia AFK (aprovação humana recomendada
até o time confiar), se a trilha rápida pede GATE do plano (não, recomendado — a análise independente basta),
paralelismo do loop (1), push e PR no loop (perguntar a cada lote, recomendado; "sim" → acrescente ao
orquestrador a ferramenta de PR na regra `ask`).

## Passo 7 — Hooks e workflows (opcionais)

- **Hooks** ([assets/hooks/sdd2.json](assets/hooks/sdd2.json) → `.kiro/hooks/sdd2.json`): `sdd2-backpressure`
  (depois de cada tarefa de spec, compila e testa — troque `{{COMPILAR}}`/`{{TESTES}}` pelos comandos; sugira o
  conjunto rápido se a suíte for lenta) e `sdd2-fechar-sessao` (botão manual que atualiza o `status.md` e deixa o
  git limpo). Pergunte por cada um; o recusado sai do array (ou fica com `"enabled": false`, se a pessoa preferir).
  O comando roda no shell de quem usa o Kiro: no Windows com PowerShell 5, `&&` não existe — use
  `cmd /c "<compilar> && <testes>"` ou `;` conforme o caso.
- **Kiro Workflows** (experimental; exige a opção `kiroAgent.workflows.enabled`): as receitas de
  [assets/workflows/](assets/workflows/) → `.kiro/workflows/` — `sdd2-planejar-fatia` (pesquisa → plano → análise)
  e `sdd2-entregar-fatia` (implementação ↔ revisão → verificação). São disparadas pela pessoa, **uma fatia por
  vez**, na branch da fatia, no checkout principal — não fazem parte do `sdd2-loop`.

## Passo 8 — Montar, mostrar, gravar

Em memória:
1. `.kiro/steering/sdd2.md` ← [assets/steering/sdd2.md](assets/steering/sdd2.md) (como está).
2. `.kiro/steering/sdd2-projeto.md` ← [assets/steering/sdd2-projeto.md](assets/steering/sdd2-projeto.md) com as
   respostas (nada de `<…>` sobrando; o que não se aplica fica "não há"/"nenhum").
3. `.kiro/steering/sdd2-licoes.md` ← [assets/steering/sdd2-licoes.md](assets/steering/sdd2-licoes.md) **só se não
   existir** (nunca sobrescreva regras promovidas).
4. `.kiro/agents/sdd2-<agente>.md` ← [assets/agents/](assets/agents/), para cada agente:
   - `{{POWER}}` → a pasta do power (Passo 0); `{{GLOSSARIO}}`/`{{ADR}}` → os caminhos do Passo 4;
   - `resources`: acrescente `file://` do steering de produto/tecnologia/estrutura e extras e `skill://` de cada
     skill escolhida para o agente;
   - `tools`: acrescente `@<servidor>` (ou `@<servidor>/<tool>`) dos MCPs escolhidos e, se houver algum, mude
     `includeMcpJson` para `true` (os `tools` limitam o que o agente vê); `includePowers` fica sempre `false`;
   - `permissions`: acrescente à regra `shell` de `allow` os comandos do Passo 2 que o agente usa, nas duas formas —
     direto e dentro de uma worktree do loop (ex.: `"mvn *"` e `"cd .kiro/local/wt/* && mvn *"`) — codificador e
     revisor: compilar, testes, lint, cobertura; verificador: executar, testes, scripts de massa e o host do ambiente
     de teste no `curl` (ex.: `"curl *dev.interno*"`); a pasta de massa do projeto na regra `fs_write` dele;
   - `model` (se escolhido); subagentes do projeto em `toolsSettings.subagent.availableAgents` e na linha
     `{{SUBAGENTES}}` do corpo (`Subagentes do projeto: \`x\` (<tipo de tarefa>)`), senão remova a linha;
   - `{{SKILLS_EXTRAS}}` → `Skills do projeto ligadas a você: \`a\`, \`b\` — carregue a do artefato antes de
     escrevê-lo.` (ou remova a linha);
   - agentes **sem** campo `hooks` (a IDE ignora agentes que o têm).
5. Hooks e workflows escolhidos (Passo 7).
6. `.kiro/produto/` (só o que não existir): `backlog.json` mínimo
   (`{"projeto": "<nome>", "atualizado": "<data>", "proximo": {"EP": 1, "FT": 1}, "epicos": [], "fatias": []}`),
   `planejamento/`; `.kiro/aprendizado/licoes.md` com o título `# Lições`.
7. `.gitignore`: acrescente `.kiro/local/` se faltar.

Mostre o resumo e, no modo atualização, o diff de cada arquivo que muda:

```
⚙️ sdd2 — <projeto> · tipos <…> · toolkits <…>
Comandos: compilar <…> · testes <…> · lint <…> · cobertura <…> (rodados: ok)
Verificação: <como> · Git: base <…> · prefixo <…> · PR <…> · Banco: <MCP | não há> · ELM: <…>
| Agente | Skills extras | MCPs | Modelo |
Hooks: <…> · Workflows: <…> · Autonomia: plano AFK <…> · paralelo <n>
Arquivos: .kiro/steering/sdd2*.md · .kiro/agents/sdd2-*.md · .kiro/hooks/… · .kiro/workflows/… · .kiro/produto/ · .gitignore
Gravar? ("ok")
```

Agente `.md` existente e editado à mão → mostre o diff e pergunte antes de sobrescrever.

## Passo 9 — Validar

- Frontmatter YAML de cada agente faz parse; `name` = nome do arquivo; nenhum `{{…}}` sobrando.
- Ferramentas que varrem a raiz do repositório (test runners, linters, `tsc`, varredura de arquivos) ignoram
  `.kiro/local/` — onde o loop cria as worktrees? Não ignoram → acrescente a exclusão na configuração delas (com
  "ok") ou registre no `sdd2-projeto.md` que o loop não deve ser usado.
- Todo `skill://` e `file://` aponta para arquivo existente (resolvendo `~` no home e o resto a partir da raiz) e
  é relativo — nenhum `/…` absoluto, `C:\…`, `\` ou variável.
- JSON dos hooks e workflows faz parse; agentes citados nos workflows existem em `.kiro/agents/`. Depois de
  instalar, peça à pessoa para abrir os painéis de hooks e de workflows do Kiro: erro de formato aparece ali — se
  aparecer, mostre-o e ofereça remover o arquivo (o fluxo funciona sem eles).
- `kiro-cli` disponível → confira que os agentes aparecem (`/agent` no chat do kiro-cli, ou `kiro-cli agent list`).
  `kiro-cli agent validate` só entende JSON: não use nos `.md`.
- Workspace não confiável → avise: o Kiro só carrega agentes do workspace depois de a pessoa confiar nele.

Sugira o commit (`.kiro/steering/sdd2*.md`, `.kiro/agents/sdd2-*.md`, `.kiro/hooks/`, `.kiro/workflows/`,
`.kiro/produto/`, `.kiro/aprendizado/`, `.gitignore`) — só com confirmação — e termine com o próximo passo:
"nova demanda" (`sdd2-prd`), "vamos trabalhar na <id>" (`sdd2-iniciar`) ou "onde parei?" (`sdd2-status`).

## Regras

- Não altere nada fora de `.kiro/`, do glossário/ADRs que a pessoa pediu para criar e do `.gitignore`.
- As skills `sdd2-*` ficam no power — nunca as copie para o projeto (uma atualização do power as atualiza; depois
  rode esta skill em modo atualização para refazer caminhos e agentes).
- Toolkit nunca é ligado sem a pessoa dizer sim, agente por agente.
