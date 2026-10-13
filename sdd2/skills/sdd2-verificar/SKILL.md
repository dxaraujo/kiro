---
name: sdd2-verificar
description: "Verificação de aceite de uma fatia do fluxo sdd2 — executa de ponta a ponta, na aplicação de verdade, cada cenário que a fatia cobre (API, job batch, tela no browser, carga de dados — conforme o tipo de projeto e o toolkit), com massa de teste, evidência por cenário (resposta, contagem, log, screenshot) e decisão ACEITO/REJEITADO; gera os casos de teste (CT.csv) para o ETM a partir dos cenários verificados. Cenário reprovado volta para a sdd2-implementar com esperado × obtido. Use em \"verifica a FT-031\", \"testa a fatia\", \"executa os cenários\", \"teste de aceitação\", \"gera os CTs\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-verificar — O comportamento existe de verdade?

Teste unitário verde prova que o código faz o que o teste diz; a verificação prova que o **sistema** faz o que o
cenário do PRD diz. Prefira o agente **`sdd2-verificador`** (contexto limpo; não implementou a fatia).

Seja cético: quem implementou tende a achar que terminou, e funcionalidade pela metade costuma passar em teste de
unidade. "Feito" é uma afirmação; a evidência é a prova.

Entrada: pasta da fatia com revisão `APROVADO`, na branch da fatia. Tipo de projeto, como executar e onde ver o
resultado: seção **Verificação** do `.kiro/steering/sdd2-projeto.md` (vem do toolkit, confirmado na setup).

## Passo 1 — Roteiro

`status.md`: `fase: verificando`, linha no Histórico.

O roteiro parte do **contrato de pronto** do `design.md` (acordado no GATE do plano, antes do código) — não o
afrouxe agora. Para cada cenário que a fatia cobre, escreva-o em `verificacao.md` **antes** de executar
(trilha rápida: os comportamentos esperado e que não muda do `bugfix.md`):

```markdown
### HF-01 · 1.2 — Rejeitar após a terceira tentativa inválida
- Massa: <script/fixture e o estado que ele cria>
- Executar: <requisição HTTP | comando do job com parâmetros | passos no browser | carga>
- Esperado: <exatamente o "Então" do cenário, com valores>
- Verificar em: <resposta | SELECT … | log | tela>
```

## Passo 2 — Ambiente e massa

- Suba a aplicação/job como o `sdd2-projeto.md` manda (comando **Executar**) — ambiente local ou de teste,
  **nunca produção**.
- Massa de teste: scripts da convenção do projeto (se houver); senão crie fixtures na pasta de testes da fatia.
  Escrita em banco **só** pelos scripts de massa declarados; consultas pelo MCP de banco, somente leitura.
- DDL pendente (campo Banco do `status.md` diferente de `aplicada em dev`) → pare: a verificação depende dela.

## Passo 3 — Executar e registrar

Execute cenário por cenário e registre logo abaixo do roteiro:

```markdown
- Resultado: ✅ aceito | ❌ rejeitado | ⚠️ ambiente
- Obtido: <o que aconteceu, com valores>
- Evidência: <trecho da resposta | resultado da consulta | linha de log | evidencias/ft-031-1.2.png>
```

- Por tipo de projeto: **backend** → chamada HTTP e estado no banco; **batch** → execução do job com a massa,
  status da execução e contagens; **frontend** → navegação real no browser (Playwright ou MCP de browser ligado ao
  agente), screenshot em `evidencias/`; **dados** → carga e consultas de verificação.
- Rode também os cenários de **repetição** (execute duas vezes; conte de novo) e de **erro em um item**.
- Falha por ambiente (serviço fora do ar, credencial de teste) → `⚠️ ambiente`, não rejeição; diga o que faltou.

## Passo 4 — Decisão

```
🔎 Verificação FT-<nnn> — rodada <N>
Cenários: <a> aceitos · <r> rejeitados · <e> ambiente
VERIFICACAO: ACEITO | REJEITADO
```

- **ACEITO** (todos aceitos) → gere o `CT.csv` (Passo 5) e devolva para a `sdd2-implementar` abrir o PR.
- **REJEITADO** → para cada cenário, esperado × obtido + evidência, registrados no `status.md` como achados;
  `fase: implementando`; a `sdd2-implementar` corrige e a verificação roda de novo (só os rejeitados + os de
  repetição). Se o problema é o cenário estar errado no PRD, diga isso: é com o P.O., não com o código.
- Só `⚠️ ambiente` → `fase: bloqueada` com o que falta; ninguém corrige código.

## Passo 5 — Casos de teste para o ETM

Gere `CT.csv` na pasta da fatia — um caso por cenário verificado — no formato de
[references/ct-csv.md](references/ct-csv.md). A importação no ETM e o link "valida" com a história são feitos
pela **`sdd2-elm`** (modo *testes*) na consolidação, depois do merge.

## Regras

- Nunca marque aceito sem evidência. Nunca altere código de produção aqui — só massa, fixtures e evidências.
- Nunca rode contra produção, nem com dado real de pessoa.
