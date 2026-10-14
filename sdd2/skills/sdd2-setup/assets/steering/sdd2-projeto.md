---
inclusion: manual
---

# Configuração do sdd2 — <nome do projeto>

> Gerado pela skill `sdd2-setup` (power `sdd2`, versão <x.y.z>) em <AAAA-MM-DD>. Para mudar: "atualizar a
> configuração do sdd2". As skills `sdd2-*` e os agentes `sdd2-*` leem os valores daqui.

## Projeto

| Item | Valor |
|---|---|
| Tipos de projeto | `<backend, batch, frontend, mobile, dados, biblioteca, infra>` |
| Stack | <ex.: Java 21, Spring Boot 3.3, Spring Batch 5, Oracle 19> |
| Toolkits | <nome (origem) — ou "nenhum — <tipo>"> |
| Módulos | <pastas/módulos principais, se multi-módulo> |

## Steering do projeto

| Papel | Arquivo |
|---|---|
| Produto e domínio | `<.kiro/steering/product.md>` |
| Tecnologia | `<.kiro/steering/tech.md>` |
| Estrutura | `<.kiro/steering/structure.md>` |
| Extras | `<lista | nenhum>` |

**Regras críticas** (BLOQUEANTE na revisão; vêm do steering de tecnologia/estrutura):
- <ex.: escrita em lote sempre idempotente por chave de negócio>

## Conhecimento duradouro

| Item | Caminho |
|---|---|
| Glossário (linguagem ubíqua) | `<docs/glossario.md>` |
| ADRs (decisões técnicas que duram) | `<docs/adr>` |
| Documentação do ELM no repositório (bundle OKF da `elm-sync`) | `<docs/elm/<pa>/ | não há>` |

## Comandos (backpressure)

Uma coluna por tipo/módulo quando o repositório tem mais de um (ex.: `batch`, `api`, `web`); a fatia usa a do
módulo que ela altera (o `design.md` diz qual).

| Ação | `<tipo/módulo>` |
|---|---|
| Compilar / checar tipos | `<…>` |
| Testes (todos) | `<…>` |
| Teste único (`{alvo}` = classe/arquivo) | `<…>` |
| Lint / análise estática | `<… | não há>` |
| Cobertura e gate | `<comando> · <ex.: linha ≥ 80% nos arquivos alterados | sem gate>` |

Falha de ambiente (banco, rede, dependência fora do ar) → `AMBIENTE`, nunca "consertar" o ambiente.
Dentro de uma worktree do `sdd2-loop`: `cd .kiro/local/wt/<ft> && <comando>`.

## Verificação de aceite

Uma coluna por tipo/módulo, como em Comandos.

| Item | `<tipo/módulo>` |
|---|---|
| Como executar a aplicação/job | `<comando, perfil, porta | job + parâmetros>` |
| Como exercitar um cenário | <requisição HTTP | execução do job | navegação no browser (Playwright/MCP) | carga> |
| Onde verificar | <resposta, consultas no banco, log em `<caminho>`, tela> |
| Massa de teste | `<pasta e convenção dos scripts | fixtures na pasta de testes>` |
| Ambiente | <local | dev — nunca produção> |

## Git e PR

| Item | Valor |
|---|---|
| Branch base | `<develop>` |
| Prefixo da branch | `<feature/>` (branch da fatia: `<prefixo><ft>-<slug>`) |
| Mensagem de commit | `<FT-<nnn> <verbo no infinitivo> <descrição> | Task <id ELM> - …>` |
| Abrir PR | `<gh pr create … | glab mr create … | entregar título e descrição para a pessoa>` |
| Artefatos de produto (`.kiro/produto/`, glossário, ADRs, consolidação) | `<direto na branch base | PR curto para a base>` — nunca em branch de fatia |

## Banco de dados

| Item | Valor |
|---|---|
| MCP de consulta | `<@servidor | @servidor/tool | não há>` |
| Uso | **somente leitura** (`SELECT`/`WITH`), exceto os scripts de massa da verificação |
| DDL | fora do fluxo — com o time de banco; campo Banco do `status.md` |

## Autonomia

| Item | Valor |
|---|---|
| Plano de fatia AFK | `<aprovação humana | análise independente basta>` |
| Trilha rápida pede GATE do plano | `<sim | não>` |
| Fatias em paralelo no `sdd2-loop` | `<1>` (máximo 3) |
| Push e PR no `sdd2-loop` | `<perguntar no início de cada lote (o Kiro confirma cada push e PR) | não — a pessoa abre>` |
| Chamada HTTP do verificador | `<sh .kiro/sdd2/http.sh — URL <url de teste> | curl com confirmação a cada chamada>` |
| Kiro Workflows instalados (uma fatia por vez, disparados pela pessoa) | `<sim — .kiro/workflows/sdd2-*.workflow.json | não>` |

## ELM

| Item | Valor |
|---|---|
| Usa ELM | `<sim — .kiro/config/power/elm/pa_<nome>.json | não>` |
| Publicar requisitos (HF/REG/GL) | `<na-aprovacao (GATE do PRD) | no-merge (consolidação)>` |
| Backlog no EWM | `<ao-fatiar | na-sprint>` |
| Especificação técnica (ET) | `<não publica | publicar no merge (as-built)>` |
| Exige no DOORS Next (manual) | `<change set por publicação, módulo por épico, links restringe, baseline por sprint | nada>` |

| Artefato sdd2 | Tipo no ELM | Pasta / plano |
|---|---|---|
| História (HF) | `<História de Usuário>` | `<02-Histórias>` |
| Regra (REG) | `<Regra>` | `<03-Regras>` |
| Termo (GL) | `<Termos de Glossário>` | `<09-Glossário>` |
| ET as-built | `<Especificação Técnica | —>` | `<…>` |
| Épico | `<Épico | Item de Backlog>` | — |
| Fatia | `<Item de Backlog>` | — |

| Tamanho | Pontos |
|---|---|
| P · M · G | `<2 · 3 · 5>` |

Testes (ETM) — colunas do `CT.csv` na ordem do template de importação do projeto:

| Coluna | Valor fixo ou origem |
|---|---|
| `<Tipo>` | `<Caso de Teste>` |
| `<Resumo>` | `<FT-nnn> <título> : CT<nn> - <cenário>` |
| `<Responsável>` | login de quem verificou |
| `<Status>` | `<estado inicial>` |
| `<Categoria>` | `<… | vazio>` |
| `<Planejado para>` | sprint (iteração) |
| `<Descrição>` | bloco OBJETIVO / PRÉ-CONDIÇÕES / PASSOS / RESULTADO ESPERADO / EVIDÊNCIA |

Tarefas criadas por fatia na sprint:

| Prefixo | Título | Responsável |
|---|---|---|
| `<[DEV]>` | `<[DEV] FT-<nnn> Implementar>` | quem implementa |
| `<[VER]>` | `<[VER] FT-<nnn> Verificar>` | quem verifica |

## Agentes

| Agente | Skills extras | Oferecidas e recusadas | MCP | Modelo | Subagentes |
|---|---|---|---|---|---|
| `sdd2-produto` | <…> | <…> | <…> | <padrão> | `sdd2-pesquisador`, `sdd2-revisor` |
| `sdd2-pesquisador` | <…> | <…> | <…> | <padrão> | — |
| `sdd2-codificador` | <…> | <…> | <…> | <padrão> | `sdd2-pesquisador`, `sdd2-revisor` <+ do projeto> |
| `sdd2-revisor` | <…> | <…> | <…> | <padrão> | — |
| `sdd2-verificador` | <…> | <…> | <…> | <padrão> | — |
| `sdd2-orquestrador` | <…> | <…> | — | <padrão> | os `sdd2-*` <+ do projeto> |

Instalados: hook `<.kiro/hooks/sdd2.json (sdd2-backpressure) | nenhum>` · comando `</sdd2-fechar-sessao | não>` · workflows
`<.kiro/workflows/sdd2-planejar-fatia.workflow.json, sdd2-entregar-fatia.workflow.json | nenhum>`
