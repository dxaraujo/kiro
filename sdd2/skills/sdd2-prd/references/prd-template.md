---
id: EP-<nn>
titulo: <título curto, linguagem do negócio>
status: rascunho            # rascunho → em-revisao → aprovado → publicado → fatiado → concluido
po: <login do P.O.>
demanda: <id da demanda/épico no EWM | —>
atualizado: <AAAA-MM-DD>
elm: {}                     # preenchido pela sdd2-elm: { HF-01: {id, url, hash}, REG-01: {…}, GL: {…} }
---

# PRD — EP-<nn> <título>

> O quê e por quê, na linguagem do negócio. O **como** técnico fica no plano de cada fatia (`design.md`).
> Decisões: `decisoes.md` (nesta pasta) · Glossário e ADRs: caminhos no `.kiro/steering/sdd2-projeto.md`

## Problema

<O problema do ponto de vista de quem sofre com ele: quem, quando, quanto custa hoje. 3–6 linhas.>

## Solução

<A solução do ponto de vista do usuário: o que passa a ser possível. Sem tecnologia. 3–6 linhas.>

## Atores

| Ator | Quem é | Como interage |
|---|---|---|
| <Operador do faturamento> | <perfil> | <tela X · API · agendamento · arquivo do parceiro> |

## Histórias

<!-- Uma história por comportamento observável. Cada uma vira um artefato "História" no DOORS Next (sdd2-elm).
     Cenários são os critérios de aceite: cada um é verificável e vira caso de teste (ETM). -->

### HF-01 — <nome da história>

**Como** <ator>, **quero** <capacidade>, **para** <benefício>.

**Gatilho:** <ação na tela | chamada de API | agendamento | evento> · **Entradas:** <…> · **Pré-condições:** <…>

**Cenários (critérios de aceite)**

1.1 <título do cenário — caminho feliz>
**Dado que** <estado antes>
**Quando** <o ator faz X>
**Então** <efeito verificável: valor gravado, resposta, mensagem, contagem>
**Conforme** REG-01

1.2 <o que NÃO deve ser aceito/processado>
…

1.3 <repetição / reexecução: rodar de novo não duplica nem corrompe>
…

**Regras:** REG-01, REG-02

### HF-02 — …

## Regras de negócio

<!-- Uma regra por bloco. Cada uma vira um artefato "Regra" no DOORS Next. -->

### REG-01 — <nome da regra>

<Enunciado testável, com valores. Ex.: "Após **3** tentativas de login inválidas em **15 minutos**, a conta fica
**Bloqueada** por **30 minutos**." Origem: D-02.>

## Decisões de implementação

<!-- Estilo Pocock: módulos, interfaces e contratos — sem caminho de arquivo nem código (eles envelhecem rápido).
     Só o que precisa de acordo antes de fatiar. -->

- **Módulos afetados:** <módulo e o que muda nele; módulo novo e sua interface pública>
- **Contratos:** <API, arquivo, mensagem — formato e versão>
- **Dados:** <entidades/tabelas novas ou alteradas — a DDL é do time de banco>
- **Integrações:** <sistema, sentido, frequência>

## Decisões de teste

- **Pontos de teste (seams):** <onde os testes entram — o mais alto possível; ex.: "a API `POST /login`" e
  "o módulo de bloqueio, pela interface pública">
- **O que é um bom teste aqui:** <comportamento externo, sem mock de detalhe interno, sem recalcular o esperado
  do jeito que o código calcula>
- **Precedente no código:** <testes vizinhos que servem de modelo>

## Não funcionais

| Tema | Requisito |
|---|---|
| Volume | <ordem de grandeza> |
| Desempenho | <tempo máximo, janela de execução> |
| Segurança e auditoria | <quem pode, o que é registrado> |

## Fora de escopo

- <o que fica explicitamente de fora — evita fatias que crescem sozinhas>

## Em aberto

<!-- Decisões "em aberto" do decisoes.md. Uma que muda comportamento impede a aprovação (GATE PRD). -->

| D | Tema | Bloqueia? |
|---|---|---|

---
Artefato produzido com apoio de IA generativa — fluxo sdd2 · Versão <x.y> · <AAAA-MM-DD>
