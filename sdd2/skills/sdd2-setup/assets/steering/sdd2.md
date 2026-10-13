---
inclusion: always
---

# Fluxo sdd2 neste projeto

Este repositório usa o fluxo **sdd2** (power `sdd2`): alinhar antes de escrever, fatias verticais pequenas, plano
aprovado por uma pessoa, teste primeiro com backpressure, revisão e verificação independentes, PR lido por uma
pessoa, e o IBM ELM como registro oficial da documentação.

- **Configuração** (comandos, verificação, git, ELM, agentes): `.kiro/steering/sdd2-projeto.md` — leia antes de
  qualquer skill `sdd2-*` (fica fora do contexto até ser preciso).
- **Regras aprendidas** (o revisor cobra): `.kiro/steering/sdd2-licoes.md`.
- **Onde parei / o que fazer:** skill `sdd2-status`. **Começar qualquer trabalho:** `sdd2-iniciar`.
  **Como funciona:** skill `sdd2`.
- **Estado em disco:** backlog em `.kiro/produto/backlog.json`; cada fatia em `.kiro/specs/<ft>-<slug>/`
  (comece pelo `status.md`).
- Nada inventado (confirme no código, no banco — só leitura — ou no ELM). Nunca apague nem afrouxe teste.
  Push, troca de branch e escrita no ELM só com "sim" de uma pessoa. Agente nunca faz merge.
