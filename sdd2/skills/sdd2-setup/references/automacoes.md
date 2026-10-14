# Automações opcionais — hook, fechar sessão e workflows

As três exigem a IDE ou a engine V3 do `kiro-cli`: a V2 não lê `.kiro/hooks/*.json` e deixa de fora o steering
`manual`. O fluxo funciona sem elas.

## Hook `sdd2-backpressure`

[../assets/hooks/sdd2.json](../assets/hooks/sdd2.json) → `.kiro/hooks/sdd2.json`.

- Depois de cada tarefa de spec (`PostTaskExec`: Start task, Run all tasks), compila e roda os testes. Troque
  `{{COMPILAR}}` e `{{TESTES}}` pelos comandos do Passo 2; suíte lenta → sugira o conjunto rápido.
- A saída vai para a saída de erro (`1>&2`) porque, na IDE, é a saída de erro de uma falha que chega ao agente
  (Maven, Gradle e pytest escrevem a falha na saída padrão). No CLI V3 a falha vira aviso.
- **Não bloqueia** a próxima tarefa, e no Run all tasks pode rodar enquanto outra tarefa começa. O portão é o
  backpressure que o próprio agente roda a cada tarefa; o hook é a rede de segurança.
- O comando roda no shell de quem usa o Kiro. No Windows: `cmd /c "(<compilar> && <testes>) 1>&2"`.
- `timeout` em segundos (900 no template); `"enabled": false` desliga sem apagar.

## Comando `/sdd2-fechar-sessao`

[../assets/steering/sdd2-fechar-sessao.md](../assets/steering/sdd2-fechar-sessao.md) → `.kiro/steering/`.
Steering `manual`, que o Kiro mostra como comando de barra: atualiza o `status.md`, deixa o git limpo e diz como
retomar. A IDE não cria hook de gatilho manual; a documentação do Kiro recomenda steering manual no lugar.

## Kiro Workflows

[../assets/workflows/](../assets/workflows/) → `.kiro/workflows/`. Experimental: na IDE, a opção
`kiroAgent.workflows.enabled`; no CLI, `chat.enableWorkflows` (e reiniciar). Sem a opção **Workflows** nas
configurações, o recurso ainda não está disponível para a conta.

| Receita | Faz | Termina |
|---|---|---|
| `sdd2-planejar-fatia` | zera o veredito → pesquisa → plano → análise ↔ ajuste (até 2 rodadas) | no GATE do plano, que é de uma pessoa |
| `sdd2-entregar-fatia` | zera o veredito → implementação ↔ revisão (até 2 rodadas) → verificação | fatia `aceita`, pronta para o PR que uma pessoa abre |

- A pessoa dispara, **uma fatia por vez**, na branch da fatia, no checkout principal (IDE 1.3+:
  `/workflow-run sdd2-entregar-fatia fatia="FT-031"`). Não fazem parte do `sdd2-loop`.
- Cada passo roda numa sessão nova, com os agentes `sdd2-*` do projeto.
- Lacuna de negócio num passo → o agente pausa a execução com a pergunta (`send_message` `warning`); responda na
  aba do passo e ele continua. Bloqueio técnico ou aceite rejeitado → o passo falha e a execução para (`error`).
- Pausou no **teto de rodadas** → **Stop** e trate a fatia na sessão interativa. O **Resume** não dá rodada nova
  (para de novo no mesmo teto); relançar a receita zera o veredito no primeiro passo. Na entrega, nunca
  "Stop looping and continue": a verificação rodaria sobre código não aprovado. (Na Web, "Run N more" dá rodadas.)
- Com Workflows ligado, a IDE pode transformar a delegação a um agente numa execução em segundo plano — o
  `sdd2-loop` já espera cada fase terminar.
