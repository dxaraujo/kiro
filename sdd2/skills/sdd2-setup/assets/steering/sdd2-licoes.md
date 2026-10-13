---
inclusion: manual
---

# Regras aprendidas (sdd2)

Regras de **julgamento** promovidas pela skill `sdd2-aprender` a partir de correções humanas
(`.kiro/aprendizado/licoes.md`). O revisor (`sdd2-revisar`) as cobra como itens da rubrica; o plano
(`sdd2-plano`) as respeita. Erro mecânico não entra aqui: vira checagem determinística (lint, teste, hook, CI).

Formato de cada regra:

```
### R-<nn> · <título> · aplica a: <codificador | revisor | plano | PRD | todos> · severidade: <BLOQUEANTE | IMPORTANTE>
<A regra em 1–2 frases imperativas.>
- ✅ <exemplo certo> · ❌ <exemplo errado>
- Origem: L-<nnn>
```

<!-- Nenhuma regra promovida ainda. -->
