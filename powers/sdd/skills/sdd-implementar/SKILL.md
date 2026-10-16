---
name: sdd-implementar
description: "Implementa uma fatia do fluxo sdd a partir do plano aprovado (tasks.md), uma tarefa por vez, em ciclo de teste (vermelho → verde → refatorar), com backpressure — compilar, testes, lint e cobertura do sdd.md têm de passar antes de marcar a tarefa; commits pequenos, progresso registrado no status.md e abertura do PR. HITL: revisão automática (rubrica C por subagente) como backpressure antes do PR, que encerra a [DEV]; revisão e verificação oficiais são das pessoas, sobre o PR. AFK: revisão (até 2 rodadas) e verificação por subagente antes do PR. Retoma o retrabalho reaberto na REV ou na VER, no mesmo PR. Usa as skills do toolkit ligadas ao agente codificador antes de escrever cada artefato. Também corrige achados da revisão, da verificação e do PR. Use em \"implementa a FT-031\", \"executa as tasks\", \"continua a implementação\", \"Start task\", \"abre o PR\", \"corrige os achados\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "2.6.2"
---

# sdd-implementar — Ciclo curto, verificação sempre

Entrada: `.kiro/specs/<ft>-<slug>/` com o plano aprovado (`status.md` com fase `implementando` ou `retrabalho (de:
…)`), na branch da fatia. O **modo** do `status.md` decide o fim: **HITL** termina no PR (Passo 5), com a `[DEV]`
concluída; **AFK** passa antes pela revisão e pela verificação por subagente (Passos 3–4). No Kiro, cada tarefa também pode ser executada pelo **"Start task"** do `tasks.md` — as regras valem igual.

Leia antes: `design.md` inteiro, `research.md`, `.kiro/steering/sdd.md` (comandos, regras críticas,
regras aprendidas).

## Passo 0 — Onde estou

- Branch = a do `status.md` (senão avise e pare). `git status` limpo, **descontados** os relatórios que outros
  papéis gravaram na pasta da fatia (`revisao-*.md`, `analise-*.md`, `verificacao.md`, `CT.csv`, `evidencias/`,
  `massa/`) e o `status.md`/`tasks.md` com mudança só de fase, Rodadas, Histórico, Achados ou marcação de tarefa:
  commite-os primeiro (mensagem no padrão do `sdd.md`, `registrar revisão/verificação`). Qualquer outra alteração →
  avise e pare.
- Atualize: a branch tem upstream → `git pull --ff-only`; não tem (worktree nova) → `git fetch` basta.
- Retome do **primeiro item não marcado** do `tasks.md`. Achados abertos viram as próximas tarefas, numeradas em
  sequência no fim da seção `## Tasks` do `tasks.md` (`- [ ] 7. [R1] <achado> — origem: revisao-codigo-2.md`;
  dependência de outra tarefa → linha no `## Task Dependency Graph`): os da seção "Achados
  abertos" do `status.md` (PR, pessoa), os do último `revisao-codigo-<N>.md` com `VEREDITO: REVISAR` e os cenários
  rejeitados do `verificacao.md`. Como as anteriores estão marcadas, elas são as primeiras não marcadas.
- **Retrabalho** (`fase: retrabalho (de: em-revisao | em-verificacao)`, HITL): **`sdd-elm` modo *assumir***
  com retrabalho — reabre a `[DEV]` (com "sim"; sem ação de reabertura na PA → `ELM pendente [<chave>]: reabrir [DEV]
  FT-<nnn>` e aviso). Os achados vêm do último `revisao-codigo-<N>.md` ou dos cenários rejeitados do
  `verificacao.md`; `fase: implementando`, linha no Histórico. Ao fim, o mesmo PR é atualizado (Passo 5).
- Rode o comando de **testes** uma vez antes de mexer: vermelho antes de começar = problema do ambiente ou da
  base, não seu. Registre e avise; não "conserte" o que não é da fatia.

## Passo 1 — Uma tarefa por vez

Para cada tarefa do `tasks.md`, nesta ordem:

1. **Carregue a skill** da stack que a tarefa cita (toolkit ligado ao agente) **antes** de escrever. Nunca escreva
   de memória o que uma skill do projeto padroniza.
2. **Vermelho:** escreva o teste do comportamento (um cenário ou critério por vez), **pelo ponto de teste do
   `design.md`** — interface pública, sem mock de detalhe interno, sem recalcular o esperado do jeito que o código
   calcula — e rode só ele (comando de teste único). Ele tem de **falhar pelo motivo certo**. Corretiva: o teste
   que reproduz o defeito vem primeiro, e ele e a correção são **um ciclo só** — marcados e commitados juntos, já
   verdes (o vermelho fica registrado no Histórico: `teste do defeito vermelho: <falha observada>`); os testes de
   preservação rodam verdes antes da correção.
3. **Verde:** a menor mudança de produção que faz o teste passar, imitando o análogo do `design.md`.
4. **Arrumar** só o que você acabou de escrever (nomes do glossário, duplicação), com os testes verdes.
   Refatorar código existente não é desta tarefa: vira sugestão para a revisão ou fatia própria.
5. **Backpressure:** compilar + testes da área + lint (comandos do `sdd.md`). Falhou → corrija antes de
   seguir; não acumule vermelho.
6. Marque `- [x]` e acrescente a linha no Histórico do `status.md`: `<data> — tarefa N ok · <testes>`.
7. **Commit** pequeno (padrão do `sdd.md`, com o id da fatia) com o código, os testes, o `tasks.md` e o
   `status.md` — a árvore fica limpa a cada tarefa.

Regras do ciclo:
- **Nunca** apague, desabilite, pule ou enfraqueça um teste para ficar verde. Teste que parece errado → pare e
  pergunte (ou, autônomo, registre como bloqueio).
- O código real não bate com o plano → **pare** e reporte, sem improvisar:
  ```
  Divergência na tarefa N — Esperado: <o que o plano diz> · Encontrado: <o que o código tem, arquivo:linha>
  · Por que importa: <o que muda>
  ```
  Muda comportamento de negócio → P.O. (`sdd-entrevistar` / `sdd-prd`); muda o desenho → `sdd-plano`
  (replanejar). Decisão técnica equivalente → decida e registre no `design.md` (Decisões técnicas).
- Nada de funcionalidade que a fatia não pediu, mesmo "aproveitando".
- Duas correções seguidas sem sair do lugar → pare de tentar variações: registre no `status.md` o que foi tentado e
  continue numa sessão nova a partir dele (contexto poluído piora a terceira tentativa); persistindo,
  `fase: bloqueada (de: implementando)`, com motivo e pergunta.
- Banco: somente leitura pelo MCP; DDL é do time de banco (registre no `status.md`, campo Banco).
- Contexto cheio ou sessão longa → atualize o `status.md` (o que foi feito, próximo passo, decisões), **commite-o**
  e continue numa sessão nova a partir dele. O estado vive nos arquivos, não na conversa.

## Passo 2 — Validação completa

Todas as tarefas `[x]`: rode compilar, a suíte **inteira** de testes e o lint; a cobertura, com o gate do
`sdd.md` (se houver), é medida no que a fatia criou ou alterou — as linhas e os ramos do diff. Falta de cobertura
que já existia no arquivo antes da fatia (fora do diff) não é tarefa dela: registre no Histórico (`cobertura
pré-existente: <arquivo> <o que falta>`) e siga. Erro de ambiente → `AMBIENTE` no `status.md`, não código.

## Passo 3 — Revisão independente

**HITL — revisão automática (backpressure):** peça ao agente **`sdd-revisor`** (subagente) a rubrica **C**
passando id, pasta, branch e "pré-PR" — relatório só na conversa, sem `revisao-codigo-<N>.md` e sem contar rodada.
`REVISAR` → corrija os achados (tarefas `[R<n>]`) e repita, até 2 vezes; persistindo, mostre à pessoa, que decide
seguir para o PR (os achados vão listados no texto do PR) ou corrigir antes. `APROVADO` → **Passo 5**: a revisão
oficial (`[REV]`) e a verificação (`[VER]`) são das pessoas, sobre o PR. Sem subagente → siga para o Passo 5.

**AFK:** `fase: revisando`; incremente "revisão do código" em Rodadas. Peça ao agente **`sdd-revisor`** (subagente) a
rubrica **C** passando só: id da fatia, pasta, branch/worktree e rodada — **nunca** o seu raciocínio. Ele grava o
`revisao-codigo-<N>.md`. Sem subagente disponível (você é um agente sem essa ferramenta) → pare aqui e devolva a
quem chamou: "pronta para a revisão (rodada <N>)".

Assim que o `revisao-codigo-<N>.md` estiver gravado, **commite-o imediatamente com o `status.md`** (fase,
Rodadas) antes de prosseguir — mensagem no padrão do `sdd.md`, `registrar revisão <N>`; não espere a próxima
sessão nem o Passo 0. O PR cita esse arquivo e
ele precisa estar na branch antes da abertura.

- `VEREDITO: APROVADO` → Passo 4.
- `REVISAR` → corrija **só** os achados (como tarefas `[R<n>]`, Passo 0) e volte ao Passo 2. Até 2 rodadas.
- 2ª reprovação → `fase: bloqueada (de: revisando)`; mostre à pessoa os relatórios e as opções: orientar a correção (zera as
  rodadas), voltar ao plano, ou aceitar explicitamente os achados restantes (quem e por quê no `status.md`).

## Passo 4 — Verificação de aceite (só AFK)

Incremente "verificação" em Rodadas e siga para a **`sdd-verificar`** (cenários de aceite executados de ponta a ponta, com evidência; de preferência
pelo agente `sdd-verificador`). `ACEITO` → ela deixa a fatia em `fase: aceita`; `REJEITADO` → devolve para cá
os cenários reprovados (Passo 0). Teto de 2 rodadas, como na revisão: 2ª rejeição seguida → `fase: bloqueada (de:
verificando)` com as mesmas opções do Passo 3. Corrigida uma rejeição, volte ao Passo 2 e ao Passo 3 (a nova
revisão conta no teto de rodadas) antes de verificar de novo.

Com `ACEITO` ou `REJEITADO`: **commite imediatamente** `verificacao.md`, `CT.csv`, `evidencias/`, `massa/` e o
`status.md` antes de prosseguir — mensagem no padrão do `sdd.md`, `registrar verificação`. O PR cita esses arquivos e eles precisam estar na branch antes da abertura.

## Passo 5 — PR e conclusão da `[DEV]`

Com a revisão automática feita (HITL) ou com `fase: aceita` (AFK: revisão `APROVADO` e verificação `ACEITO`):

Quem abre o PR é a sessão da pessoa (com o "sim" dela) ou o `sdd-orquestrador` no loop. Como agente
`sdd-codificador`, que não faz push, pare em "pronta para o PR" e entregue o título e a descrição do item 2.

1. Branch atualizada com a base? (`git fetch` e compare com `origin/<base>`). Desatualizada → numa sessão com a
   pessoa, com o "sim" dela, `git merge origin/<base>` (conflito → resolva e repita Passos 2–4); como agente,
   pare e devolva "branch desatualizada com a base". O "nunca merge" do fluxo é sobre o PR: esse merge é sempre de
   uma pessoa.
2. Texto do PR:
   ```
   FT-<nnn> — <título>   (EP-<nn> · IB <id ELM | —>)
   O quê: <1–3 linhas do comportamento entregue>
   Cobre: HF-01 · 1.1, 1.2 · REG-01   (ELM: <ids | pendente>)
   Plano: .kiro/specs/<ft>-<slug>/ (research · requirements · design · tasks)
   Revisão: <AFK: revisao-codigo-<N>.md (APROVADO) · Aceite: verificacao.md (ACEITO, <n> cenários) | HITL: revisão automática OK (achados aceitos: …) — revisão e aceite no PR>
   Backpressure: compilar ok · testes ok · lint ok · cobertura <x% | sem gate>
   Banco (DDL): <não se aplica | pendente — implantação bloqueada>
   Como ler: <ordem sugerida dos arquivos — do teste do cenário principal para o código que ele exercita>
   Reversível? <sim, só reverter o PR | não: dado migrado/contrato publicado — o que fazer>
   ```
   O PR é para uma pessoa **ler o código**: pequeno, com a evidência e o caminho de leitura, sem despejar o plano.
3. Numa só confirmação da pessoa: push e abertura do PR com a ferramenta do `sdd.md` (sem ferramenta →
   entregue título e descrição prontos).
4. **Conclusão da `[DEV]`:** mostre as horas já lançadas (`elm-ccm` › horas lançadas) e pergunte só o saldo →
   `sdd-elm` modo *horas*, depois modo *conclusão* só da `[DEV]`, numa confirmação. Sem o power `elm` → `ELM pendente [<chave>]:
   lançar <h>h e concluir [DEV] FT-<nnn>` no Histórico.
5. `status.md`: HITL → `fase: pr-aberto`; AFK → `fase: pronta-para-merge`; link do PR (sem PR aberto — push "não"
   ou sem ferramenta — `PR: texto entregue`, e a fase é a mesma), o resultado do item 4 no
   Histórico (retrabalho: as horas na tabela Retrabalho); commit e, com o mesmo "sim", push (o `status.md` vai junto
   no PR; retrabalho → atualiza o mesmo PR). HITL: avise que a `[REV]` está disponível para o revisor.

O merge é de uma pessoa (HITL: depois de `pronta-para-merge`, quando a VER aceita). Depois do merge:
**`sdd-consolidar`**.

## Trilha direta

Sem spec nem `tasks.md` — a pasta da fatia tem só o `status.md`; o critério é a **ficha** de três linhas
(`<produto>/fatias/FT-<nnn>-<slug>.md`: pronto quando · como verificar · não muda):
1. Teste que falha, quando há comportamento (texto e configuração pura não têm); 2. a mudança; 3. backpressure;
4. revisão pela **`sdd-revisar`** (rubrica C sobre o diff, com a ficha no lugar dos critérios: "pronto quando"
cumprido, "não muda" preservado; relatório na conversa); 5. **como verificar**: execute o que a ficha diz e guarde
a evidência (saída, log, print) para o PR; 6. PR curto: `FT-<nnn> — <título> (<id do item | —>)` · `O quê` ·
`Pronto quando` · `Evidência` (do item 5) · `Backpressure` · `Revisão: APROVADO` · `Como ler`; 7. **conclusão da
`[DEV]`** como no Passo 5, item 4 (saldo de horas e conclusão, numa confirmação); 8. `status.md` com
`fase: pr-aberto` e o link do PR — sem PR aberto (push "não" ou sem ferramenta) → `PR: texto entregue` e a mesma
fase; o merge é de uma pessoa e a `sdd-consolidar` aceita a direta em `pr-aberto`. Se no caminho aparecer regra de
negócio ou mais de um comportamento → pare: devolva à `sdd-triar` (é trilha rápida ou padrão).

## Modo autônomo

`AUTONOMO=true` (chamado pelo `sdd-orquestrador`/`sdd-loop`): sem perguntas; trabalhe só na worktree recebida;
**não** faça push nem abra PR (o orquestrador faz); bloqueio vira `fase: bloqueada (de: <fase>)` com o motivo e a pergunta, e você para.

## Regras

- Nunca `--force`; merge só o da base para a branch, por uma pessoa (Passo 5); push só com confirmação (ou pelo
  orquestrador, com a autorização do lote).
- Nada fora do escopo do `design.md`; melhoria vista no caminho vira sugestão de item no backlog (registrada pela `sdd-triar`).
