---
name: elm-sync
description: "Sincroniza o bundle OKF do DOORS Next com o ELM nas duas vias, pelo MCP elm: plano (o que baixar, o que enviar, conflitos), baixar a versão oficial, enviar o que mudou no repositório, e reindexar no okf. Usa a pasta e a project area do pa_<nome>.json do projeto. Use em \"sincroniza o ELM\", \"baixa os requisitos\", \"atualiza o bundle\", \"envia os requisitos alterados\", \"sync do DOORS\"."
license: MIT
metadata:
  author: "Daniel Xavier Araújo"
  version: "3.0.0"
---

# elm-sync — Bundle do DOORS Next nas duas vias

O bundle (pasta `rm.download` do `pa`) é a cópia local, em OKF, dos requisitos oficiais: a `sdd-prd` e os similares
o leem pelo MCP `okf`. Regras comuns: [../sdd/references/elm.md](../sdd/references/elm.md).

1. `elm_sync(projeto, pa, direcao "plano")` → mostre: a baixar (mudou no ELM), a enviar (mudou no bundle) e
   **conflitos** (mudou nos dois lados, com as duas datas).
2. Conflito → mostre o diff de cada um e pergunte qual fica (ELM → baixar aquele id; repositório → enviar). Nunca
   sobrescreva o ELM sem "sim".
3. Com "sim": `elm_sync(direcao "baixar", ids?)` e, se houver, `elm_sync(direcao "enviar", ids)`. Envio é escrita no
   ELM: um "sim" para o lote, com a lista.
4. `okf_index` na pasta do bundle. Commit `ELM - Sincronizar bundle` com o que baixou.

Saída: `🔄 Sync ELM · baixados <n> · enviados <n> · conflitos <n resolvidos> · bundle de <data>`.
