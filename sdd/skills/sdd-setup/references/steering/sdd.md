---
inclusion: always
---

# Fluxo SDD neste projeto

Este repositório usa o fluxo **SDD** (power `sdd`): cada IB passa por três papéis assíncronos — especificador,
codificador, testador —, com gates humanos, devoluções com causa raiz e aprendizado contínuo.

- **Processo** (papéis, gates, fases, pasta e branch, ELM, devoluções, convenções): skill **`sdd`** — leia-a antes
  de qualquer skill `sdd-*`.
- **Configuração do projeto** (steering, comandos, branch base, banco, executores, regras promovidas):
  `.kiro/steering/sdd-projeto.md`.
- **Começar uma Task:** "vamos trabalhar na task <id>" (`sdd-tarefa`). **Onde parei:** `sdd-status`.
- Uma pasta por IB em `.kiro/specs/ib-<id>-<slug>/`; o campo `fase` do `status.md` diz de quem é a vez.
- GATE 1 (requisitos) e GATE 3 (PR) são sempre de uma pessoa. Agente nunca faz merge nem `--force`; push e toda
  alteração no ELM só com "sim" de uma pessoa. Banco somente leitura. Nada inventado: confirme no código, no banco
  ou na documentação.
