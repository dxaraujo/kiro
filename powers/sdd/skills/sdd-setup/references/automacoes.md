# Automações opcionais — hook e workflows

As duas exigem a IDE ou a engine V3 do `kiro-cli` (a V2 não lê `.kiro/hooks/*.json` nem receitas). O fluxo funciona
sem elas.

## Hook `sdd-backpressure`

[../assets/hooks/sdd.json](../assets/hooks/sdd.json) → `.kiro/hooks/sdd.json`.

- Depois de cada tarefa de spec (`PostTaskExec`: Start task, Run all tasks), compila e roda os testes. Troque
  `{{COMPILAR}}` e `{{TESTES}}` pelos comandos do Passo 2; suíte lenta → sugira o conjunto rápido.
- A saída vai para a saída de erro (`1>&2`) porque, na IDE, é a saída de erro de uma falha que chega ao agente
  (Maven, Gradle e pytest escrevem a falha na saída padrão). No CLI V3 a falha vira aviso.
- **Não bloqueia** a próxima tarefa, e no Run all tasks pode rodar enquanto outra tarefa começa. O portão é o
  backpressure que o próprio agente roda a cada tarefa; o hook é a rede de segurança.
- O comando roda no shell de quem usa o Kiro. No Windows: `cmd /c "(<compilar> && <testes>) 1>&2"`.
- `timeout` em segundos (900 no template); `"enabled": false` desliga sem apagar.

## Kiro Workflows

[../assets/workflows/](../assets/workflows/) → `.kiro/workflows/`. Experimental: na IDE, a opção
`kiroAgent.workflows.enabled`; no CLI, `chat.enableWorkflows` (e reiniciar). Sem a opção **Workflows** nas
configurações, o recurso ainda não está disponível para a conta.

| Receita | Para | Faz | Termina |
|---|---|---|---|
| `sdd-planejar-fatia` | fatia HITL ou AFK | zera o veredito → pesquisa → plano → análise ↔ ajuste (até 2 rodadas) → registrar | plano commitado: `implementando` (AFK sem épico, rápida sem GATE) ou `plano-em-revisao` (GATE de uma pessoa) |
| `sdd-entregar-fatia` | só fatia **AFK** | zera o veredito → implementação ↔ revisão (até 2 rodadas, cada uma registrada) → verificação → registrar | fatia `aceita` e commitada, pronta para o PR que uma pessoa abre |

As receitas são o caminho AFK de **uma** fatia sem o `sdd-loop` (que leva várias, em worktrees). Fatia HITL não
usa a `sdd-entregar-fatia`: a `sdd-implementar` termina no PR, e a revisão e a verificação são das pessoas.

- **Quem dispara: a pessoa**, no chat principal do Kiro (com o agente padrão ou qualquer outro), **uma fatia por
  vez**, na branch da fatia, no checkout principal: "rode o workflow `sdd-entregar-fatia` com fatia FT-031" ou, na
  IDE 1.3+, `/workflow-run sdd-entregar-fatia fatia="FT-031"`; no CLI, a família de comandos `/workflow`. Nenhum
  agente `sdd-*` dispara receitas — nem o orquestrador, que usa subagentes no `sdd-loop`. Cada passo roda com o
  agente que a receita indica (pesquisador, codificador, revisor, verificador).
- Cada passo roda numa sessão nova, com os agentes `sdd-*` do projeto.
- Lacuna de negócio num passo → o agente pausa a execução com a pergunta (`send_message` `warning`); responda na
  aba do passo e ele continua. Bloqueio técnico ou aceite rejeitado → o passo falha e a execução para (`error`).
- Pausou no **teto de rodadas** → **Stop** e trate a fatia na sessão interativa. O **Resume** não dá rodada nova
  (para de novo no mesmo teto); relançar a receita zera o veredito no primeiro passo. Na entrega, nunca
  "Stop looping and continue": a verificação rodaria sobre código não aprovado. (Na Web, "Run N more" dá rodadas.)
- Com Workflows ligado, a IDE pode transformar a delegação a um agente numa execução em segundo plano — o
  `sdd-loop` já espera cada fase terminar.
