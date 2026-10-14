---
name: sdd2-pesquisar
description: "Pesquisa do código para uma fatia do fluxo sdd2, antes de planejar — somente leitura: localiza onde o comportamento mora, as funcionalidades análogas (pattern grounding), o que pode ser reaproveitado, os testes vizinhos, o schema real e as restrições; compacta tudo em research.md com fatos e arquivo:linha, sem opinião nem solução. Mantém o contexto de quem planeja limpo (o pesquisador lê muito e devolve pouco). Use em \"pesquisa o código para a FT-031\", \"onde isso está implementado\", \"research\", \"entender o código antes de planejar\", e como primeiro passo da sdd2-plano."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-pesquisar — Entender antes de planejar

Uma linha errada na pesquisa vira um plano errado, que vira centenas de linhas de código erradas. A pesquisa é
barata de revisar e cara de errar — por isso ela é um arquivo curto, factual e verificável.

Prefira o agente **`sdd2-pesquisador`** (somente leitura, contexto próprio): ele lê dezenas de arquivos e devolve
só o `research.md`. Sem o agente, faça você mesmo e, ao terminar, trabalhe a partir do arquivo, não da memória da
leitura.

## Entrada

Pasta da fatia `.kiro/specs/<ft>-<slug>/` com `status.md`; a fatia no `backlog.json` (`cobre`); o PRD do épico
(histórias e regras cobertas) ou, na trilha rápida, o defeito/pedido.

## Passo 1 — Perguntas da pesquisa

Antes de abrir o código, escreva de 3 a 7 perguntas que o plano vai precisar responder. Exemplos:
- Onde o login é validado hoje e onde a falha é registrada?
- Qual funcionalidade existente faz algo parecido (bloqueio, contador, janela de tempo)?
- Que tabela guarda as tentativas? Há coluna de situação?
- Como os testes de serviço desta camada são escritos (base, fixtures, banco de teste)?

## Passo 2 — Investigar

- Estrutura: steering de estrutura do projeto e `glob` dos módulos envolvidos.
- Fluxo atual: siga do ponto de entrada (rota, job, tela, consumidor) até o dado, lendo os arquivos — não
  deduza pelo nome.
- **Análogos:** 1–2 funcionalidades reais do mesmo tipo (mesma camada, mesma forma de entrada/saída). Leia de ponta
  a ponta, incluindo os testes.
- **Reaproveitamento:** serviços, utilitários, componentes, queries e clientes de integração existentes.
- **Dados:** schema real pelo MCP de banco (somente leitura) ou pelos modelos/migrações; volumetria se importar.
- **Documentação:** histórias e regras do bundle do ELM (`<rm.download.path>`) que tratam do mesmo comportamento —
  divergência entre código e documentação é um achado importante.
- **Testes:** como rodar só os testes da área (comando de teste único do `sdd2-projeto.md`) e o que já cobrem.
- Skills do toolkit do projeto ligadas a você: carregue a da stack antes de interpretar código dela.

## Passo 3 — `research.md`

```markdown
# Pesquisa — FT-<nnn> <título>

## Perguntas e respostas
1. <pergunta> → <resposta factual> (`caminho/arquivo.ext:42`, `:88-97`)

## Fluxo atual
<ponto de entrada → … → dado, com arquivo:linha em cada passo>

## Análogos (pattern grounding)
| Funcionalidade | Arquivos | O que imitar |
|---|---|---|

## Reaproveitar
| Componente | Onde | Para quê |
|---|---|---|

## Dados
<tabelas/colunas reais envolvidas; índices e chaves que importam para reexecução>

## Testes
<onde estão, como rodar só eles, o que já cobrem, base/fixtures a usar>

## Documentação × código
<divergências entre o bundle do ELM e o comportamento real — ou "nenhuma encontrada">

## Restrições e riscos
<concorrência, volume, transação, dependências externas, DDL necessária>

## Não encontrado
<o que foi procurado e não existe — evita que o plano invente>
```

- Só fatos com evidência; nada de solução ou recomendação (isso é do plano).
- Curto: o objetivo é caber inteiro no contexto de quem planeja. Mais de ~150 linhas → corte o que o plano não usa.
- `status.md`: fase `planejando`, linha no Histórico — **só** quando você não é o agente `sdd2-pesquisador`
  (sessão da pessoa). O agente pesquisador nunca grava o `status.md`: quem o chamou registra (`sdd2-plano`,
  `sdd2-loop`).

## Regras

- Somente leitura: nenhum arquivo além de `research.md` (e, fora do agente pesquisador, a linha do `status.md`).
- Nunca invente arquivo, classe, coluna ou rota. Não achou → seção "Não encontrado".
