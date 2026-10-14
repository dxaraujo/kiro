# Agentes — como montar `.kiro/agents/sdd2-*.json`

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
| tool de MCP | `tools` e `allowedTools`: `@<servidor>/<tool>` · `"includeMcpJson": true` | `mcp` `allow`: `<servidor>/<tool>` |
| **só V3** | — | `skill` `allow` (todos) · `shell` `ask` de push/PR (orquestrador) · `shell` `ask` de `curl`/`wget` (verificador) |

Regex → glob: `.*` → `*` e tire o escape (`\.` → `.`). Um padrão por **comando simples**: o Kiro separa um comando
composto (`;`, `&&`, `||`, `|`) e avalia cada parte — `cd .kiro/local/wt/<ft> && mvn test` precisa do `cd` (já
liberado) e do `mvn *`. Padrão encadeado (`cd … && mvn …`) não é convertido. `deny` vence `ask`, que vence
`allow`; uma regra `ask` explícita pergunta sempre, sem a opção "sempre permitir".

Os subagentes herdam as regras da sessão que os chamou (a documentação diz "deny-wins intersection"). Se, no loop,
um subagente falhar por permissão num comando de build ou teste liberado para ele, libere o mesmo comando no
orquestrador.

## O que a setup preenche

| Onde | O quê |
|---|---|
| `{{POWER}}` (nos dois blocos) | a pasta do power (Passo 0) |
| `{{GLOSSARIO}}`, `{{ADR}}` (produto, nos dois blocos) | os caminhos do Passo 4 |
| `{{SKILLS_EXTRAS}}` (no `prompt`) | `Skills do projeto ligadas a você: `a`, `b` — carregue a do artefato antes de escrevê-lo.` ou nada |
| `{{SUBAGENTES}}` (no `prompt`) | `Subagentes do projeto: `x` (<tipo de tarefa>)` ou nada |
| `resources` | `file://` do steering de produto/tecnologia/estrutura e dos extras; `skill://` de cada skill escolhida |
| leitura | a pasta de cada skill escolhida que fique fora do projeto e do power (`~/.kiro/skills/<skill>/**`, `~/.kiro/powers/installed/<toolkit>/**`) e o bundle do ELM, se estiver fora do projeto |
| comandos | codificador e revisor: compilar, testes, teste único, lint, cobertura · verificador: executar, testes, scripts de massa |
| escrita do verificador | a pasta de massa do projeto, se houver |
| MCP de banco | só a tool de consulta, como na tabela acima |
| subagentes do projeto | como na tabela acima (codificador e orquestrador) |
| `model` | o modelo escolhido, se houver |
| push/PR "nunca" (Autonomia) | no orquestrador, a regra `ask` de push/PR vira `deny` |

Fixos em todos: `"allowedTools"` sem `read` (liberaria a leitura do disco inteiro); `"includePowers": false` (a
documentação não garante o padrão, e com powers o agente receberia o MCP do `elm`); nunca o campo `hooks` (a IDE
ignora agentes que o têm).

## O que os templates já trazem

- **Leitura:** o projeto (`./**`) e o power; negadas `.env`, `.env.*`, `*.pem`, `*.key`, `~/.ssh`, `~/.aws` e a
  pasta de credenciais do ELM. Os agentes leem e procuram arquivos com as ferramentas do Kiro (que respeitam essas
  regras), não com `cat`/`grep` no shell.
- **Shell:** git de leitura (`status`, `diff`, `log`, `show`, `grep`, `ls-files`, `ls-tree`, `rev-parse`, listagem de
  branches, `worktree list`, `for-each-ref`, `config user.name/email`) e `cd .kiro/local/wt/*`; codificador e produto
  também `add`, `commit`, `fetch`, `pull --ff-only` (produto: `switch`); orquestrador: `add`, `commit`, `fetch`,
  `worktree add .kiro/local/wt/*`, e push/PR com `ask`; verificador: `sh .kiro/sdd2/http.sh *`.
- **Negados em todos:** `git -C` (com ele as regras não enxergam o subcomando: `git -C <dir> push …` passaria por um
  allow de `git -C <dir> show*`), `git -c`, merge, rebase (inclusive `pull --rebase`), `reset --hard`, `clean`,
  `checkout --`/`checkout .`, `restore`, `stash`, `worktree remove`, `branch -D/-M`, `--force`, `--delete`,
  `--no-verify`, `gh pr merge`, `glab mr merge`, `rm -rf`, e opções que executam outro programa ou gravam arquivo
  (`find -exec/-ok/-delete`, `rg --pre`, `git grep -O`, `git difftool`, `--upload-pack`, `--receive-pack`,
  `git … --output`, `git … --no-index`). Push negado em todos, menos no orquestrador (`ask`, com `-f`, `+ref`,
  `:ref`, `--mirror`, `--all`, `--prune` negados).
- **Escrita:** só o que o papel produz (ver cada template); o codificador escreve no projeto, menos `.kiro/agents`,
  `hooks`, `workflows`, `steering`, `produto`, `.kiro/local/wf`, `.kiro/sdd2` e `.git`.

## Gravação

O Kiro **sempre pergunta** antes de gravar em `.kiro/agents/`, `.kiro/hooks/` e `.kiro/workflows/` (nenhuma regra
remove essa pergunta): avise a pessoa de que haverá uma confirmação por arquivo.
