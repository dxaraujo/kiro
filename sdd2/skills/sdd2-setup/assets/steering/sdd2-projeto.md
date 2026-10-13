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
| ADRs (decisões técnicas que duram) | `<docs/adr/>` |
| Documentação do ELM no repositório (bundle OKF da `elm-sync`) | `<docs/elm/<pa>/ | não há>` |

## Comandos (backpressure)

| Ação | Comando |
|---|---|
| Compilar / checar tipos | `<…>` |
| Testes (todos) | `<…>` |
| Teste único (`{alvo}` = classe/arquivo) | `<…>` |
| Lint / análise estática | `<… | não há>` |
| Cobertura e gate | `<comando> · <ex.: linha ≥ 80% nos arquivos alterados | sem gate>` |

Falha de ambiente (banco, rede, dependência fora do ar) → `AMBIENTE`, nunca "consertar" o ambiente.

## Verificação de aceite

| Item | Valor |
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
| Push e PR no `sdd2-loop` | `<perguntar no início de cada lote | não — a pessoa abre>` |
| Execução autônoma | `<agente sdd2-orquestrador | Kiro Workflows (.kiro/workflows/sdd2-*.workflow.json)>` |

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

Tarefas criadas por fatia na sprint:

| Prefixo | Título | Responsável |
|---|---|---|
| `<[DEV]>` | `<[DEV] FT-<nnn> Implementar>` | quem implementa |
| `<[VER]>` | `<[VER] FT-<nnn> Verificar>` | quem verifica |

## Agentes

| Agente | Skills extras | MCP | Modelo | Subagentes |
|---|---|---|---|---|
| `sdd2-produto` | <…> | <…> | <padrão> | `sdd2-pesquisador`, `sdd2-revisor` |
| `sdd2-pesquisador` | <…> | <…> | <padrão> | — |
| `sdd2-codificador` | <…> | <…> | <padrão> | <…> |
| `sdd2-revisor` | <…> | <…> | <padrão> | — |
| `sdd2-verificador` | <…> | <…> | <padrão> | — |
| `sdd2-orquestrador` | <…> | — | <padrão> | os `sdd2-*` <+ do projeto> |

Instalados: hooks `<.kiro/hooks/sdd2-backpressure.json | nenhum>` · workflows `<.kiro/workflows/sdd2-*.workflow.json | nenhum>`
