---
name: sdd-prd
description: "Escreve o PRD de um épico ou demanda no fluxo sdd — o quê e o porquê na linguagem do negócio: problema, solução, atores, histórias com cenários de aceite (Gherkin), regras de negócio, decisões de implementação e de teste em nível de módulo, não funcionais e fora de escopo. Explora o código e a documentação do ELM antes, entrevista a pessoa (sdd-entrevistar) e conduz o GATE do PRD (aprovação do P.O.), depois do qual as histórias, regras e termos vão para o DOORS Next pela sdd-elm. Use em \"escreve o PRD\", \"documenta a demanda\", \"nova funcionalidade\", \"épico\", \"especificar a demanda\", \"aprova o PRD\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.1.0"
---

# sdd-prd — O quê e por quê (épico)

> **Arquivos desta skill** (`references/`, `assets/` e os `../<skill>/…` citados abaixo) ficam na pasta da skill, dentro do
> power instalado (ex.: `~/.kiro/powers/installed/sdd/skills/sdd-prd/`), não no projeto: abra-os por esse
> caminho, relativo a este `SKILL.md`. A busca no workspace não os encontra — não procure no projeto.

Saída, em `<produto>/epicos/<EP>-<slug>/`: o `prd.md` no formato de
[references/prd-template.md](references/prd-template.md), o `decisoes.md` e a pasta `elm/` com **um conceito OKF
v0.2 por história, regra e termo novo** — o formato de [references/okf-elm.md](references/okf-elm.md), o mesmo do
bundle que a `elm-sync` mantém. São esses arquivos que sobem para o DOORS Next depois do GATE; até lá, ficam aqui.

O PRD é um **registro de decisões** e a **proposta de mudança** da documentação oficial — não um documento vivo.
Depois de aprovado, as histórias (HF), regras (REG) e termos (GL) vão para o DOORS Next (`sdd-elm`), que é a fonte
oficial; o que vale a longo prazo é o ELM, o glossário e os ADRs. Se o PRD afirma algo que ninguém decidiu, é um
defeito do PRD. Trabalho que cabe numa sessão (uma fatia, um ajuste) **não precisa de PRD**: vá de
`sdd-entrevistar` direto para `sdd-iniciar`.

Leia antes: `.kiro/steering/sdd.md` (ELM, caminhos, papéis) e o steering de produto que ele aponta.

## Passo 1 — Entender a demanda

1. Peça (ou leia, se veio da `sdd-iniciar`) a descrição **longa** da demanda: quem pediu, o problema, exemplos
   reais, prazos. Work item do EWM → pela skill `elm-ccm` do power `elm` (se instalado), com descrição e
   comentários.
2. **Explore antes de perguntar** (subagente `sdd-pesquisador`, se houver; senão você mesmo, só leitura):
   - documentação atual no bundle do ELM (`<rm.download.path>`): histórias e regras que já tratam do assunto —
     o PRD **altera** o que existe, não duplica;
   - código: onde o comportamento mora hoje, funcionalidades análogas;
   - glossário e ADRs (caminhos na seção Projeto do `sdd.md`): termos e decisões que já valem.
   Registre o que achou como fontes (id ELM, `arquivo:linha`).
3. Defina o id: próximo `EP-<nn>` livre em `<produto>/backlog.md` (crie o arquivo se não existir —
   formato na `sdd-fatiar`). Pasta: `<produto>/epicos/<EP>-<slug>/` (`slug` em kebab-case, sem acento).
4. **Registre o épico no EWM já agora** (projeto com ELM): `sdd-elm` modo *backlog*, só o épico (`[EP-nn]
   <título>`, descrição = o problema), com confirmação; o id vai para a coluna `elm` do `backlog.md`. Assim o pai
   existe para a `[ESP]` do planejamento e para os IBs das fatias. Sem MCP → `ELM pendente: épico EP-nn` no rodapé
   do PRD.

## Passo 2 — Entrevistar

Rode a **`sdd-entrevistar`** sobre a demanda, gravando em `decisoes.md` da pasta do épico. Ela termina quando a
árvore de decisões está fechada ou a pessoa diz "chega".

## Passo 3 — Escrever

Preencha o template do `prd.md` e crie, em `elm/`, um arquivo por artefato (`HF-nn-<slug>.md`,
`REG-nn-<slug>.md`, `GL-<termo>.md`), com `status: draft`, `sources` (PRD, decisões), `generated` e o corpo do tipo
(formato em [references/okf-elm.md](references/okf-elm.md)), mais o `index.md` e uma entrada no `log.md`. O `prd.md`
só aponta para eles. Regras de escrita:

- **Histórias** pequenas o bastante para caber em poucas fatias; cada uma com cenários que cubram: caminho feliz,
  o que **não** deve ser aceito, repetição/reexecução, erro em um item (a operação continua? o que fica
  registrado?). "Então" sempre verificável — nada de "corretamente".
- **Regras** testáveis, com valores, uma por bloco, citando a decisão de origem (`D-nn`) ou a fonte.
- **Alteração** de comportamento documentado → copie o arquivo do artefato do bundle da `elm-sync`
  (`<rm.download.path>/…/<id>-<slug>.md`) para `elm/`, mantendo `resource`, `id` e o `sources` do ELM; ponha
  `status: draft` e um `generated` novo; reescreva no estado **depois** da mudança. Sem bundle, leia o artefato
  pela `elm-rm` (`rm_get_requirement`) e grave a mesma estrutura. A `sdd-elm` atualiza o artefato existente em vez
  de criar outro. Na tabela do PRD, coluna "Altera no ELM" = o id.
- **HF → REG** sempre por link para o arquivo da regra: na publicação ele vira **embed**. Relações entre requisitos
  (restringe, satisfaz) vão na seção `## Relações` do conceito — ficam só no repositório.
- **Decisões de implementação** sem caminho de arquivo e sem código — módulos, interfaces e contratos.
- **Decisões de teste:** proponha os **pontos de teste** (seams) — o mais alto possível, idealmente um por
  comportamento — e confirme com a pessoa: é por eles que as fatias vão provar que funcionam.
- Termos do glossário em todo o texto; termo novo já registrado pela entrevista.
- Mais de ~8 histórias ou mais de um objetivo de negócio → proponha dividir em dois épicos antes de escrever.

## Passo 4 — Revisão independente

Peça ao agente **`sdd-revisor`** a revisão do PRD (rubrica **P** de
[../sdd-revisar/references/rubricas.md](../sdd-revisar/references/rubricas.md)); sem o agente, aplique a rubrica
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
- Aprovado → no `prd.md`: `status: aprovado`, versão `1.0`, data e quem aprovou no rodapé. Em **cada** conceito de
  `elm/`: `status: stable` e um `verified` com `{ by: human:<login de quem aprovou>, at: <agora> }` — sem esse
  `verified` humano a `sdd-elm` não publica. Entrada `**Update**` no `log.md`. Commit do PRD, do `decisoes.md`, de
  `elm/` e do `backlog.md` (padrão de commit do `sdd.md`) — artefatos de produto vão para a **base**,
  direto ou por PR curto, conforme "Artefatos de produto" no `sdd.md`; nunca numa branch de fatia.
- Próximo passo, na mesma resposta:
  1. **`sdd-elm`** modo *requisitos* — publicar HF/REG/GL no DOORS Next (se o projeto usa ELM e a publicação é
     `na-aprovacao` no `sdd.md`);
  2. **`sdd-fatiar`** — quebrar em fatias verticais para o backlog.

## Mudança depois de aprovado

PRD `aprovado`/`fatiado` só muda por um pedido explícito: incremente a versão (`1.1` correção, `2.0` mudança de
escopo), registre no rodapé, volte a `em-revisao` só o que mudou e repita o GATE. Conceito alterado: `status:
draft`, `generated.at` novo; no GATE, um `verified` novo é acrescentado à lista. A `sdd-elm` atualiza os mesmos
artefatos (pelo `resource`/`id` de cada conceito). Fatias já entregues que dependem do que mudou → avise e proponha
fatias novas; não altere fatia concluída.

## Regras

- Nunca invente regra, valor ou ator: sem fonte e sem decisão de uma pessoa, é `em aberto`.
- O PRD não tem caminho de arquivo, nome de classe nem SQL — isso é do plano da fatia.
- Escreva no idioma do projeto; nomes de sistemas, tabelas e campos na forma original.
