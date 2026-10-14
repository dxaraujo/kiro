# Templates do plano da fatia (formato de spec do Kiro)

Os arquivos ficam em `.kiro/specs/<ft>-<slug>/` no formato de spec do Kiro: o painel de specs reconhece a pasta e o
`tasks.md` ganha **Start task** / **Run all tasks**. O texto é no idioma do projeto; os marcadores que o Kiro lê
(`.config.kiro`, `- [ ]`, `- [ ]*`, `_Requirements: …_`, `**Validates: Requirements …**`) ficam exatamente como
abaixo. Plano curto: quem aprova tem de ler tudo numa sentada — um plano de 1.000 linhas esconde decisões em vez
de mostrá-las.

## `.config.kiro`

Uma linha de JSON, criada pela `sdd2-iniciar` junto com a pasta (a `sdd2-plano` cria se faltar; `specId` = um
UUID novo: `uuidgen` ou `python3 -c "import uuid; print(uuid.uuid4())"`):

```json
{"specId": "<uuid>", "workflowType": "requirements-first", "specType": "feature"}
```

`specType`: `feature` (trilha padrão) ou `bugfix` (trilha rápida, com `bugfix.md` no lugar do `requirements.md`).

## `requirements.md` (trilha padrão)

```markdown
# Requirements Document

## Introduction
FT-<nnn> — <título>. <O comportamento que esta fatia entrega, em 2–3 frases.>
Épico: EP-<nn> · PRD: `<caminho>` · ELM: HF <id>, REG <id> · Fora de escopo: <lista curta>

## Glossary
- **Sistema_Login**: <o componente que responde pelos critérios — termo usado nos critérios EARS>
- **<Termo do domínio>**: <definição do glossário do projeto> (só os termos usados aqui)

## Requirements

### Requirement 1: <nome>
**User Story:** Como <ator>, quero <…>, para <…>.
**Origem:** HF-01 · cenários 1.1, 1.2 · REG-01

#### Acceptance Criteria
1. QUANDO o usuário errar a senha pela 3ª vez em 15 minutos, O Sistema_Login DEVE marcar a conta como **Bloqueada**.
2. ENQUANTO a conta estiver **Bloqueada**, O Sistema_Login DEVE recusar a autenticação com a mensagem MSG 2005.
3. SE a mesma falha for registrada duas vezes, ENTÃO O Sistema_Login DEVE contá-la uma vez só.

**Falsificável na base:** <a observação que mostra os critérios falsos hoje — ex.: "a 4ª tentativa ainda autentica">
```

- Padrões EARS: `QUANDO <gatilho>, O <Sistema> DEVE …` · `ENQUANTO <estado>, O <Sistema> DEVE …` ·
  `SE <condição indesejada>, ENTÃO O <Sistema> DEVE …` · `ONDE <variação opcional>, O <Sistema> DEVE …` ·
  sem gatilho: `O <Sistema> DEVE …`. O `<Sistema>` é um termo do Glossary.
- Um requisito por grupo de cenários da fatia; critérios numerados `N.M`, citados pelo `tasks.md`.
- Só o que a fatia cobre (`cobre` no backlog). Nada de regra que não esteja no PRD/ELM/`decisoes.md`.

## `bugfix.md` (trilha rápida — defeito)

```markdown
# Bugfix Requirements Document

## Introduction
FT-<nnn> — <título> (DF <id>). Fonte do comportamento correto: <HF/REG do ELM | decisão D-nn | regra óbvia>.

## Bug Analysis

### Current Behavior (Defect)
1.1 QUANDO <condição>, ENTÃO o sistema <faz o errado> — evidência: <log, consulta, passo a passo>

### Expected Behavior (Correct)
2.1 QUANDO <condição>, ENTÃO o sistema DEVE <o certo>

### Unchanged Behavior (Regression Prevention)
3.1 QUANDO <condição vizinha>, ENTÃO o sistema DEVE CONTINUAR A <comportamento correto de hoje>

### Bug Condition
    FUNÇÃO condicaoDoDefeito(entrada)
      RETORNA <predicado que separa as entradas afetadas das não afetadas>
    FIM

### Fix Property
Para toda entrada com `condicaoDoDefeito`, o resultado é o de 2.x.

### Preservation Property
Para toda entrada sem `condicaoDoDefeito`, o resultado é igual ao de antes da correção.
```

As primeiras tarefas do `tasks.md` de um bugfix são sempre: **1.** teste que reproduz a condição do defeito
(vermelho) e **2.** testes de preservação (verdes antes e depois da correção).

## `design.md`

```markdown
# Design Document: FT-<nnn> <título>

## Overview
<Abordagem em 3–6 linhas.>

## Architecture
### Padrões a seguir (pattern grounding)
| Referência real (research) | O que imitar |
|---|---|
| `<caminho>` | <estrutura, transação, teste> |

### Forma do programa
Árvore de arquivos:
    src/…/LoginService.java          alterar  conta tentativas e consulta o bloqueio
    src/…/BloqueioConta.java         criar    regra de bloqueio (módulo profundo: 1 método público)
    test/…/BloqueioContaTest.java    criar

Árvore de chamadas do caminho principal:
    LoginController.autenticar → LoginService.autenticar → BloqueioConta.registrarFalha → TentativaRepository.contar

## Components and Interfaces
    BloqueioConta.registrarFalha(login: String, instante: Instant): ResultadoBloqueio

## Data Models
<tabelas/colunas reais (research), queries, contratos de API/arquivo; DDL necessária → time de banco>

## Correctness Properties
*Uma propriedade é algo que deve valer em toda execução válida — vira teste baseado em propriedades quando o
toolkit do projeto tiver a biblioteca; senão, testes de exemplo.*

### Property 1: <título>
*Para qualquer* sequência de falhas de um mesmo login, a conta DEVE ficar **Bloqueada** se e só se houver 3 ou mais
falhas numa janela de 15 minutos.
**Validates: Requirements 1.1, 1.3**

## Error Handling
<o que é rejeitado, registrado, desfeito; transação; como repetir não duplica>

## Testing Strategy
- **Pontos de teste (seams):** <o mais alto possível; ex.: `BloqueioConta` pela interface pública; `POST /login`>
- **Contrato de pronto (verificação de aceite):**

| Cenário | Como executar | Esperado | Onde verificar |
|---|---|---|---|
| HF-01 · 1.2 | 4× `POST /login` com senha errada (massa: usuário `teste.bloqueio`) | 4ª resposta 423, conta **Bloqueada** | resposta + `SELECT situacao FROM conta WHERE login=…` |

## Decisões técnicas
| Decisão | Alternativas | Motivo | Vira ADR? |
|---|---|---|---|

## Riscos
<concorrência, volume, dependências, DDL pendente>
```

Na trilha rápida, o `design.md` é curto: Overview, causa raiz (com `arquivo:linha` da research), a correção, e a
Testing Strategy com exploração da condição do defeito, verificação da correção e da preservação.

## `tasks.md`

```markdown
# Implementation Plan: FT-<nnn> <título>

## Overview
<1–2 linhas: ordem e estratégia (teste primeiro, do núcleo para a borda).>

## Tasks

- [ ] 1. Bloqueio após a terceira falha (unidade)
  - [ ] 1.1 Teste em `BloqueioContaTest`: 3 falhas em 15 min → **Bloqueada**; 2 falhas → **Ativa** (vermelho)
  - [ ] 1.2 Implementar `BloqueioConta.registrarFalha` imitando `<análogo>` (verde)
  - Pronto quando: `<comando de teste único> BloqueioContaTest` verde
  - _Requirements: 1.1, 1.3_
- [ ] 2. Login usa o bloqueio (integração)
  - [ ] 2.1 Teste de `POST /login` 4× → 423 (vermelho)
  - [ ] 2.2 `LoginService` consulta `BloqueioConta`; resposta 423 com a MSG 2005 (verde)
  - Pronto quando: `<comando>` verde
  - _Requirements: 1.1, 1.2_
- [ ]* 3. Teste de propriedade da Property 1
  - _Requirements: 1.1, 1.3_
- [ ] 4. Checkpoint — validação completa (compilar, suíte inteira, lint, cobertura)
  - A revisão não é tarefa daqui: é da `sdd2-revisar`, em outro contexto (quem implementou não se revisa)

## Notes
- Tarefas com `*` são opcionais.
```

- Uma tarefa = um comportamento, começando pelo teste que falha (corretiva: o teste que reproduz o defeito).
- Toda tarefa diz o comando que prova que terminou.
- Ordem de dependência. O **Run all tasks** do Kiro roda em ondas e em paralelo só tarefas que não mexem nos
  mesmos arquivos — deixe explícito quando uma depende da outra.
- Mudança em código compartilhado → primeiro a tarefa de **preparação** ("deixar a mudança fácil"), depois a
  mudança; refatoração larga usa expandir → migrar → contrair, em fatias próprias.
- DDL não vira tarefa: vai para Riscos e para o campo Banco do `status.md`.
