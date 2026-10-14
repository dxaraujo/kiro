---
name: sdd2-prd
description: "Escreve o PRD de um épico ou demanda no fluxo sdd2 — o quê e o porquê na linguagem do negócio: problema, solução, atores, histórias com cenários de aceite (Gherkin), regras de negócio, decisões de implementação e de teste em nível de módulo, não funcionais e fora de escopo. Explora o código e a documentação do ELM antes, entrevista a pessoa (sdd2-entrevistar) e conduz o GATE do PRD (aprovação do P.O.), depois do qual as histórias, regras e termos vão para o DOORS Next pela sdd2-elm. Use em \"escreve o PRD\", \"documenta a demanda\", \"nova funcionalidade\", \"épico\", \"especificar a demanda\", \"aprova o PRD\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-prd — O quê e por quê (épico)

Saída: `.kiro/produto/epicos/<EP>-<slug>/prd.md` no formato de [references/prd-template.md](references/prd-template.md)
e `decisoes.md` ao lado.

O PRD é um **registro de decisões** e a **proposta de mudança** da documentação oficial — não um documento vivo.
Depois de aprovado, as histórias (HF), regras (REG) e termos (GL) vão para o DOORS Next (`sdd2-elm`), que é a fonte
oficial; o que vale a longo prazo é o ELM, o glossário e os ADRs. Se o PRD afirma algo que ninguém decidiu, é um
defeito do PRD. Trabalho que cabe numa sessão (uma fatia, um ajuste) **não precisa de PRD**: vá de
`sdd2-entrevistar` direto para `sdd2-iniciar`.

Leia antes: `.kiro/steering/sdd2-projeto.md` (ELM, caminhos, papéis) e o steering de produto que ele aponta.

## Passo 1 — Entender a demanda

1. Peça (ou leia, se veio da `sdd2-iniciar`) a descrição **longa** da demanda: quem pediu, o problema, exemplos
   reais, prazos. Work item do EWM → pela skill `elm-ccm` do power `elm` (se instalado), com descrição e
   comentários.
2. **Explore antes de perguntar** (subagente `sdd2-pesquisador`, se houver; senão você mesmo, só leitura):
   - documentação atual no bundle do ELM (`<rm.download.path>`): histórias e regras que já tratam do assunto —
     o PRD **altera** o que existe, não duplica;
   - código: onde o comportamento mora hoje, funcionalidades análogas;
   - glossário e ADRs (caminhos no `sdd2-projeto.md`, seção Conhecimento): termos e decisões que já valem.
   Registre o que achou como fontes (id ELM, `arquivo:linha`).
3. Defina o id: próximo `EP-<nn>` livre em `.kiro/produto/backlog.json` (crie o arquivo se não existir —
   formato na `sdd2-fatiar`). Pasta: `.kiro/produto/epicos/<EP>-<slug>/` (`slug` em kebab-case, sem acento).

## Passo 2 — Entrevistar

Rode a **`sdd2-entrevistar`** sobre a demanda, gravando em `decisoes.md` da pasta do épico. Ela termina quando a
árvore de decisões está fechada ou a pessoa diz "chega".

## Passo 3 — Escrever

Preencha o template. Regras de escrita:

- **Histórias** pequenas o bastante para caber em poucas fatias; cada uma com cenários que cubram: caminho feliz,
  o que **não** deve ser aceito, repetição/reexecução, erro em um item (a operação continua? o que fica
  registrado?). "Então" sempre verificável — nada de "corretamente".
- **Regras** testáveis, com valores, uma por bloco, citando a decisão de origem (`D-nn`) ou a fonte.
- **Alteração** de comportamento documentado → cite o artefato do ELM que muda (`Altera: HF 2010`) e escreva a
  história no estado **depois** da mudança. A `sdd2-elm` atualiza o artefato existente em vez de criar outro.
- **Decisões de implementação** sem caminho de arquivo e sem código — módulos, interfaces e contratos.
- **Decisões de teste:** proponha os **pontos de teste** (seams) — o mais alto possível, idealmente um por
  comportamento — e confirme com a pessoa: é por eles que as fatias vão provar que funcionam.
- Termos do glossário em todo o texto; termo novo já registrado pela entrevista.
- Mais de ~8 histórias ou mais de um objetivo de negócio → proponha dividir em dois épicos antes de escrever.

## Passo 4 — Revisão independente

Peça ao agente **`sdd2-revisor`** a revisão do PRD (rubrica **P** de
[../sdd2-revisar/references/rubricas.md](../sdd2-revisar/references/rubricas.md)); sem o agente, aplique a rubrica
você mesmo, sem usar o raciocínio de quem escreveu como evidência. Corrija os achados (até 2 rodadas); o que for
decisão de negócio volta para a entrevista. `status: em-revisao` enquanto isso.

## Passo 5 — GATE do PRD (pessoa)

```
📄 PRD EP-<nn> — <título>
Histórias: <n> (<c> cenários) · Regras: <n> · Termos novos: <n> · Altera no ELM: <ids | nada>
Decisões: <d> decididas · <a> em aberto (<bloqueantes>)
Revisão: <OK na rodada N | achados aceitos: …>
Aprovar? (o P.O. ou quem ele delegou)
```

- Decisão **em aberto que muda comportamento** → não há aprovação; volte à entrevista.
- Aprovado → `status: aprovado`, versão `1.0`, data e quem aprovou no rodapé; commit do PRD, do `decisoes.md` e do
  `backlog.json` (padrão de commit do `sdd2-projeto.md`) — artefatos de produto vão para a **base**, direto ou por
  PR curto, conforme "Artefatos de produto" no `sdd2-projeto.md`; nunca numa branch de fatia.
- Próximo passo, na mesma resposta:
  1. **`sdd2-elm`** modo *requisitos* — publicar HF/REG/GL no DOORS Next (se o projeto usa ELM e a publicação é
     `na-aprovacao` no `sdd2-projeto.md`);
  2. **`sdd2-fatiar`** — quebrar em fatias verticais para o backlog.

## Mudança depois de aprovado

PRD `aprovado`/`fatiado` só muda por um pedido explícito: incremente a versão (`1.1` correção, `2.0` mudança de
escopo), registre no rodapé, volte a `em-revisao` só o que mudou e repita o GATE. A `sdd2-elm` atualiza os mesmos
artefatos (os ids ficam no frontmatter `elm`). Fatias já entregues que dependem do que mudou → avise e proponha
fatias novas; não altere fatia concluída.

## Regras

- Nunca invente regra, valor ou ator: sem fonte e sem decisão de uma pessoa, é `em aberto`.
- O PRD não tem caminho de arquivo, nome de classe nem SQL — isso é do plano da fatia.
- Escreva no idioma do projeto; nomes de sistemas, tabelas e campos na forma original.
