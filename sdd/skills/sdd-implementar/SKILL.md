---
name: sdd2-implementar
description: "Implementa uma fatia do fluxo sdd2 a partir do plano aprovado (tasks.md), uma tarefa por vez, em ciclo de teste (vermelho → verde → refatorar), com backpressure — compilar, testes, lint e cobertura do sdd2.md têm de passar antes de marcar a tarefa; commits pequenos, progresso registrado no status.md, revisão independente (sdd2-revisar, rubrica C, até 2 rodadas) e abertura do PR. Usa as skills do toolkit ligadas ao agente codificador antes de escrever cada artefato. Também corrige achados da revisão, da verificação e do PR. Use em \"implementa a FT-031\", \"executa as tasks\", \"continua a implementação\", \"Start task\", \"abre o PR\", \"corrige os achados\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "0.1.0"
---

# sdd2-implementar — Ciclo curto, verificação sempre

Entrada: `.kiro/specs/<ft>-<slug>/` com o plano aprovado (`status.md` com fase `implementando`), na branch da
fatia. No Kiro, cada tarefa também pode ser executada pelo **"Start task"** do `tasks.md` — as regras valem igual.

Leia antes: `design.md` inteiro, `research.md`, `.kiro/steering/sdd2.md` (comandos, regras críticas,
regras aprendidas).

## Passo 0 — Onde estou

- Branch = a do `status.md` (senão avise e pare). `git status` limpo, **descontados** os relatórios que outros
  papéis gravaram na pasta da fatia (`revisao-*.md`, `analise-*.md`, `verificacao.md`, `CT.csv`, `evidencias/`,
  `massa/`): commite-os primeiro (`FT-<nnn> registrar revisão/verificação`). Qualquer outra alteração → avise e pare.
- Atualize: a branch tem upstream → `git pull --ff-only`; não tem (worktree nova) → `git fetch` basta.
- Retome do **primeiro item não marcado** do `tasks.md`. Achados abertos viram as próximas tarefas, numeradas em
  sequência no fim do `tasks.md` (`- [ ] 7. [R1] <achado> — origem: revisao-codigo-2.md`): os da seção "Achados
  abertos" do `status.md` (PR, pessoa), os do último `revisao-codigo-<N>.md` com `VEREDITO: REVISAR` e os cenários
  rejeitados do `verificacao.md`. Como as anteriores estão marcadas, elas são as primeiras não marcadas.
- Rode o comando de **testes** uma vez antes de mexer: vermelho antes de começar = problema do ambiente ou da
  base, não seu. Registre e avise; não "conserte" o que não é da fatia.

## Passo 1 — Uma tarefa por vez

Para cada tarefa do `tasks.md`, nesta ordem:

1. **Carregue a skill** da stack que a tarefa cita (toolkit ligado ao agente) **antes** de escrever. Nunca escreva
   de memória o que uma skill do projeto padroniza.
2. **Vermelho:** escreva o teste do comportamento (um cenário ou critério por vez), **pelo ponto de teste do
   `design.md`** — interface pública, sem mock de detalhe interno, sem recalcular o esperado do jeito que o código
   calcula — e rode só ele (comando de teste único). Ele tem de **falhar pelo motivo certo**. Corretiva: o teste
   que reproduz o defeito vem primeiro.
3. **Verde:** a menor mudança de produção que faz o teste passar, imitando o análogo do `design.md`.
4. **Arrumar** só o que você acabou de escrever (nomes do glossário, duplicação), com os testes verdes.
   Refatorar código existente não é desta tarefa: vira sugestão para a revisão ou fatia própria.
5. **Backpressure:** compilar + testes da área + lint (comandos do `sdd2.md`). Falhou → corrija antes de
   seguir; não acumule vermelho.
6. Marque `- [x]` e faça **commit** pequeno (padrão do `sdd2.md`), com o id da fatia.
7. Uma linha no Histórico do `status.md`: `<data> — tarefa N ok · <testes> · <commit curto>`.

Regras do ciclo:
- **Nunca** apague, desabilite, pule ou enfraqueça um teste para ficar verde. Teste que parece errado → pare e
  pergunte (ou, autônomo, registre como bloqueio).
- O código real não bate com o plano → **pare** e reporte, sem improvisar:
  ```
  Divergência na tarefa N — Esperado: <o que o plano diz> · Encontrado: <o que o código tem, arquivo:linha>
  · Por que importa: <o que muda>
  ```
  Muda comportamento de negócio → P.O. (`sdd2-entrevistar` / `sdd2-prd`); muda o desenho → `sdd2-plano`
  (replanejar). Decisão técnica equivalente → decida e registre no `design.md` (Decisões técnicas).
- Nada de funcionalidade que a fatia não pediu, mesmo "aproveitando".
- Duas correções seguidas sem sair do lugar → pare de tentar variações: registre no `status.md` o que foi tentado e
  continue numa sessão nova a partir dele (contexto poluído piora a terceira tentativa); persistindo,
  `fase: bloqueada`.
- Banco: somente leitura pelo MCP; DDL é do time de banco (registre no `status.md`, campo Banco).
- Contexto cheio ou sessão longa → atualize o `status.md` (o que foi feito, próximo passo, decisões) e continue
  numa sessão nova a partir dele. O estado vive nos arquivos, não na conversa.

## Passo 2 — Validação completa

Todas as tarefas `[x]`: rode compilar, a suíte **inteira** de testes e o lint; a cobertura, com o gate do
`sdd2.md` (se houver), é medida nos arquivos que a fatia criou ou alterou. Erro de ambiente → `AMBIENTE`
no `status.md`, não código.

## Passo 3 — Revisão independente

`fase: revisando`; incremente "revisão do código" em Rodadas. Peça ao agente **`sdd2-revisor`** (subagente) a
rubrica **C** passando só: id da fatia, pasta, branch/worktree e rodada — **nunca** o seu raciocínio. Ele grava o
`revisao-codigo-<N>.md`. Sem subagente disponível (você é um agente sem essa ferramenta) → pare aqui e devolva a
quem chamou: "pronta para a revisão (rodada <N>)".

- `VEREDITO: APROVADO` → Passo 4.
- `REVISAR` → corrija **só** os achados (como tarefas `[R<n>]`, Passo 0) e volte ao Passo 2. Até 2 rodadas.
- 2ª reprovação → `fase: bloqueada`; mostre à pessoa os relatórios e as opções: orientar a correção (zera as
  rodadas), voltar ao plano, ou aceitar explicitamente os achados restantes (quem e por quê no `status.md`).

## Passo 4 — Verificação de aceite

Incremente "verificação" em Rodadas e siga para a **`sdd2-verificar`** (cenários de aceite executados de ponta a ponta, com evidência; de preferência
pelo agente `sdd2-verificador`). `ACEITO` → ela deixa a fatia em `fase: aceita`; `REJEITADO` → devolve para cá
os cenários reprovados (Passo 0).

## Passo 5 — PR

Com `fase: aceita` (revisão `APROVADO` e verificação `ACEITO`):

Quem abre o PR é a sessão da pessoa (com o "sim" dela) ou o `sdd2-orquestrador` no loop. Como agente
`sdd2-codificador`, que não faz push, pare em "pronta para o PR" e entregue o título e a descrição do item 2.

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
   Revisão: revisao-codigo-<N>.md (APROVADO) · Aceite: verificacao.md (ACEITO, <n> cenários com evidência)
   Backpressure: compilar ok · testes ok · lint ok · cobertura <x% | sem gate>
   Banco (DDL): <não se aplica | pendente — implantação bloqueada>
   Como ler: <ordem sugerida dos arquivos — do teste do cenário principal para o código que ele exercita>
   Reversível? <sim, só reverter o PR | não: dado migrado/contrato publicado — o que fazer>
   ```
   O PR é para uma pessoa **ler o código**: pequeno, com a evidência e o caminho de leitura, sem despejar o plano.
3. Numa só confirmação da pessoa: push e abertura do PR com a ferramenta do `sdd2.md` (sem ferramenta →
   entregue título e descrição prontos).
4. `status.md`: `fase: pr-aberto`, link do PR; commit e, com o mesmo "sim", push (o `status.md` vai junto no PR).

O merge é de uma pessoa. Depois do merge: **`sdd2-consolidar`**.

## Trilha direta

Sem pasta de spec nem `tasks.md` (a `sdd2-iniciar` decidiu que o diff cabe numa frase):
1. Teste que falha, quando há comportamento (texto e configuração pura não têm); 2. a mudança; 3. backpressure;
4. revisão pela **`sdd2-revisar`** (rubrica C sobre o diff, com o **pedido** no lugar dos critérios; relatório na
conversa); 5. PR curto: `<pedido> (<id do item | —>)` · `O quê` · `Backpressure` · `Revisão: APROVADO` ·
`Como ler`. Se no caminho aparecer regra de negócio ou mais de um comportamento → pare: é trilha rápida ou padrão.

## Modo autônomo

`AUTONOMO=true` (chamado pelo `sdd2-orquestrador`/`sdd2-loop`): sem perguntas; trabalhe só na worktree recebida;
**não** faça push nem abra PR (o orquestrador faz); bloqueio vira `fase: bloqueada` com o motivo, e você para.

## Regras

- Nunca `--force`; merge só o da base para a branch, por uma pessoa (Passo 5); push só com confirmação (ou pelo
  orquestrador, com a autorização do lote).
- Nada fora do escopo do `design.md`; melhoria vista no caminho vira sugestão de item no backlog.
