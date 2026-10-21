# Agentes — como montar `.kiro/agents/sdd-*.json`

Os templates de [../assets/agents/](../assets/agents/) estão no **formato universal** do Kiro: o mesmo JSON
carrega na IDE e nas engines V2 e V3 do `kiro-cli`. São dois blocos que dizem a mesma coisa:

- `toolsSettings` e `allowedTools` — lidos pela V2, com **expressões regulares** nos comandos;
- `permissions.rules` — lido pela V3 e pela IDE, com **globs** (`*` casa qualquer sequência nos comandos).

Toda mudança entra **nos dois blocos**, em espelho. Os templates foram gerados pelo `kiro-cli agent upgrade` a
partir do bloco V2 e receberam depois as regras que só existem na V3 (tabela abaixo). Por isso:

- **não regenere** o `permissions` com `kiro-cli agent upgrade` nem com `/upgrade-agent` — o conversor não produz
  as regras só da V3 (sem a de `skill`, cada skill pediria aprovação na V3);
- `kiro-cli agent upgrade --dry-run` mostra `out of sync (not rebuilt)` para eles — é o esperado e significa que o
  Kiro não os reescreve.

## Correspondência

| O quê | V2 | V3 / IDE |
|---|---|---|
| leitura permitida / negada | `toolsSettings.read.allowedPaths` / `deniedPaths` | `fs_read` `allow` / `deny` |
| escrita permitida / negada | `toolsSettings.write.allowedPaths` / `deniedPaths` | `fs_write` `allow` / `deny` |
| comando liberado | `toolsSettings.shell.allowedCommands`: `mvn .*` | `shell` `allow`: `mvn *` |
| comando negado | `toolsSettings.shell.deniedCommands`: `.*git push.*` | `shell` `deny`: `*git push*` |
| subagente | `tools`: `subagent/<nome>` · `toolsSettings.subagent.availableAgents` e `trustedAgents`: `<nome>` | `subagent` `allow`: `<nome>` |
| tool de MCP | `tools` e `allowedTools`: `@<servidor>/<tool>` · `"includeMcpJson": true` | `mcp` `allow`: `<servidor>/<tool>` (com `/`, nunca `<servidor>::<tool>`) |
| tool de MCP de **power** | `tools` e `allowedTools`: `@<servidor>/<tool>` (o `kiro-cli` V2 não carrega powers: sem efeito lá) | `power` (não `mcp`): `<power>/<servidor>/<tool>` — a IDE chama pela tool `kiro_powers` e sobe o servidor como `power-<power>-<servidor>`, que regra `mcp` `<servidor>/…` não casa |
| **só V3** | — | `skill` `allow` (todos) · `shell` `ask` de push (orquestrador, codificador, revisor e verificador) · `power` `ask` de `sdd/gitlabpr/gitlab_criar_mr` (codificador, produto e orquestrador) e de `sdd/gitlabpr/gitlab_mesclar_mr` (codificador) · `shell` `ask` de `curl`/`wget` (verificador) |

Regex → glob: `.*` → `*` e tire o escape (`\.` → `.`). Um padrão por **comando simples**: o Kiro separa um comando
composto (`;`, `&&`, `||`, `|`) e avalia cada parte — `cd .kiro/local/wt/<ft> && mvn test` precisa do `cd` (já
liberado) e do `mvn *`. Padrão encadeado (`cd … && mvn …`) não é convertido. `deny` vence `ask`, que vence
`allow`; uma regra `ask` explícita pergunta sempre, sem a opção "sempre permitir".

Os subagentes herdam as regras da sessão que os chamou (a documentação diz "deny-wins intersection", sem dizer se
os `allow` também se cruzam). Por isso o orquestrador já escreve nas worktrees (`.kiro/local/wt/*/**`, menos
`.kiro`, a pasta do produto e `.git`), e a setup também põe nele os comandos de build, teste e verificação dos
subagentes e o `sh .kiro/sdd/http.sh *`, nos dois blocos. Se, no primeiro lote, um subagente ainda falhar por
permissão, compare as regras dele com as do orquestrador.

## O que a setup preenche

| Onde | O quê |
|---|---|
| `{{POWER}}` (nos dois blocos) | a pasta do power (Passo 0) |
| `{{PRODUTO}}` (produto, revisor, codificador; nos dois blocos) | a pasta do produto (Passo 4), padrão `.kiro/planejamento` |
| `{{GLOSSARIO}}`, `{{ADR}}` (produto, nos dois blocos) | os caminhos do Passo 4 |
| `{{BASE}}` (codificador, revisor e verificador; só no bloco V3) | a branch base do `sdd.md` (Passo 3), sem `origin/` — nas negações de push para a base |
| `{{BUNDLE}}` (todos, leitura negada, nos dois blocos) | o bundle do ELM (Passo 4): a consulta é pelo MCP `okf`, nunca pelos arquivos. "não há" → remova a linha |
| `{{SKILLS_EXTRAS}}` (no `prompt`) | `Skills do projeto ligadas a você: `a`, `b` — carregue a do artefato antes de escrevê-lo.` ou nada |
| `{{SUBAGENTES}}` (no `prompt`) | `Subagentes do projeto: `x` (<tipo de tarefa>)` ou nada |
| `resources` | `file://` do steering de produto/tecnologia/estrutura e dos extras; `skill://` de cada skill escolhida |
| leitura | a pasta de cada skill escolhida que fique fora do projeto e do power (`~/.kiro/skills/<skill>/**`, `~/.kiro/powers/installed/<toolkit>/**`) |
| comandos | codificador e revisor: compilar, testes, teste único, lint, cobertura · verificador: executar, testes, scripts de massa · orquestrador: todos esses e `sh .kiro/sdd/http.sh *` (se instalado) |
| escrita do verificador | a pasta de massa do projeto, se houver |
| MCP de banco | só a tool de consulta, em **quatro** lugares: `tools` e `allowedTools` (`@<servidor>/<tool>`), `"includeMcpJson": true` (o template vem com `false`: sem trocar, o agente não carrega nenhum MCP) e a regra `mcp` `allow` `<servidor>/<tool>` |
| ELM (projeto com `Usa ELM: sim`) | `"includePowers": true` (fixo em todos) — o power `elm` traz o MCP e as skills `elm-*`; nenhuma tool `@elm/…` no agente nem servidor `elm` no `mcp.json` (as skills do `sdd` pedem operações às `elm-*`). O pesquisador recebe o power pelo `okf`, mas não pede nada ao ELM |
| subagentes do projeto | como na tabela acima (codificador e orquestrador) |
| `model` | o modelo escolhido, se houver |
| push e PR no loop = "não — a pessoa abre" | no orquestrador, as regras `ask` de push (`shell`) e de `sdd/gitlabpr/gitlab_criar_mr` (`power`) viram `deny` |

Fixos em todos: `"allowedTools"` sem `read` (liberaria a leitura do disco inteiro); `"includePowers"`: `true` em
todos — o próprio `sdd` traz os MCPs `okf` e `gitlabpr`; nunca o campo `hooks` (a IDE ignora agentes que o têm).
Com o power, o Kiro pede confirmação para as tools do `elm` que o agente não tem em `allowedTools` — nenhuma
está lá: toda chamada ao ELM é confirmada, além do "sim" da skill. Já liberadas em todos (`tools`, `allowedTools` e `power` `allow`, como `sdd/okf/<tool>` e `sdd/gitlabpr/<tool>`):
as de leitura do `okf` (`okf_index`, `okf_search`, `okf_get_document`, `okf_list_documents`) e do `gitlabpr`
(`gitlab_listar_mrs`, `gitlab_obter_mr`). `gitlab_criar_mr`: `ask` no codificador, no produto e no orquestrador (abrem o PR depois do
push), `deny` no pesquisador, no revisor e no verificador. `gitlab_mesclar_mr`: `ask` só no codificador (o merge do PR
aprovado), `deny` nos demais.

## O que os templates já trazem

- **Leitura:** o projeto (`./**`) e o power; negadas `.env`, `.env.*`, `*.pem`, `*.key`, `~/.ssh`, `~/.aws`, as
  pastas de credenciais do ELM e do GitLab (`~/.config/mcp-gitlabpr`) e o bundle do ELM (`{{BUNDLE}}`). Os agentes leem e procuram arquivos com as ferramentas do Kiro (que respeitam essas
  regras), não com `cat`/`grep` no shell.
- **Shell:** git de leitura (`status`, `diff`, `log`, `show`, `grep`, `ls-files`, `ls-tree`, `rev-parse`, listagem de
  branches, `worktree list`, `for-each-ref`, `config user.name/email`) e `cd .kiro/local/wt/*`; codificador e produto
  também `add`, `commit`, `fetch`, `pull --ff-only`, `switch`; revisor e verificador os mesmos, para o modo HITL
  (commit do relatório e da fase na branch do PR, e o push dela); orquestrador: `add`, `commit`, `fetch`,
  `worktree add .kiro/local/wt/*`, e push com `ask` (o PR, pela `gitlab_criar_mr`, também com `ask`); verificador: `sh .kiro/sdd/http.sh *`.
- **Negados em todos:** `git -C` (com ele as regras não enxergam o subcomando: `git -C <dir> push …` passaria por um
  allow de `git -C <dir> show*`), `git -c`, merge, rebase (inclusive `pull --rebase`), `reset --hard`, `clean`,
  `checkout --`/`checkout .`, `restore`, `stash`, `worktree remove`, `branch -D/-M`, `--force`, `--delete`,
  `--no-verify`, `gh pr merge`, `glab mr merge`, `rm -rf`, e opções que executam outro programa ou gravam arquivo
  (`find -exec/-ok/-delete`, `rg --pre`, `git grep -O`, `git difftool`, `--upload-pack`, `--receive-pack`,
  `git … --output`, `git … --no-index`).
- **Push:** negado no produto e no pesquisador. No orquestrador, no codificador, no revisor e no verificador, o
  bloco V3 tem `git push *` com `ask` (o Kiro pergunta sempre) e nega `-f`, `+ref`, `:ref`, `--mirror`, `--all`,
  `--prune` (e `--force`, `--delete`, como em todos); codificador, revisor e verificador negam também o push para a base (`{{BASE}}`
  como destino: ` <base>`, `:<base>`, `heads/<base>`). Push sem destino (`git push` puro) não é pego pelo padrão: as
  skills mandam sempre `git push -u origin <branch>`, só a branch da fatia (revisor e verificador: a do PR). No
  bloco V2 (sem `ask`) o push continua negado nos três (`.*git push.*`): o agente entrega o comando pronto e
  espera a pessoa dizer que publicou.
- **Escrita:** só o que o papel produz (ver cada template); o codificador escreve no projeto, menos `.kiro/agents`,
  `hooks`, `workflows`, `steering`, a pasta do produto, `.kiro/local/wf`, `.kiro/sdd` e `.git`.
  O produto, além da pasta do produto, do glossário e dos ADRs, escreve o `decisoes.md`, e — para a consolidação,
  que é dele (P.O. ou SM) — o `status.md`, o `verificacao.md` e a pasta `elm/` de cada fatia (`.kiro/specs/*/`);
  o código ele só lê (a ET *as-built*).

## Gravação

O Kiro **sempre pergunta** antes de gravar em `.kiro/agents/`, `.kiro/hooks/` e `.kiro/workflows/` (nenhuma regra
remove essa pergunta): avise a pessoa de que haverá uma confirmação por arquivo.
