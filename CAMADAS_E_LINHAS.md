# Runbook — 4 Camadas e 3 Linhas de Defesa da Atribuição de IA

Este documento mapeia cada defesa ao seu artefato executável (ou ao controle
de plataforma que a implementa em produção) e ao que ela prova.

## As 4 Camadas (defesa contra "o dev apaga a atribuição")

### Camada 1 — Obrigatoriedade
**O quê:** tornar a declaração de IA obrigatória na fronteira do PR.
**Artefato:** `gate_atribuicao.py` + `.github/workflows/ai-attribution-gate.yml`.
**Como funciona:** o gate roda no CI; se a telemetria indica IA mas nada foi
declarado (trailer, branch ou label), o job falha. Marcado como *required
status check*, a branch protection impede o merge.
**Prova na demo:** bloqueia o PR `feature/parser` e aprova quando vira `ai/parser`.

### Camada 2 — Imutabilidade
**O quê:** impedir que a atribuição seja apagada depois do merge.
**Em produção:** branch protection (proíbe force-push/rewrite) + commit signing.
**Artefato (simula o efeito):** `verificar_integridade.py`.
**Como funciona:** sela o estado do branch; se um commit selado muda de SHA
(rewrite), detecta — exatamente o que a branch protection rejeitaria no servidor.
Também relata quais commits estão assinados.
**Prova na demo:** detecta o `amend` que tentou apagar o trailer; reporta 0/4 assinados.

### Camada 3 — Visibilidade
**O quê:** tornar o vazamento detectável, já que nenhuma defesa é 100%.
**Artefato:** `detectar_delta.py`.
**Como funciona:** cruza o que o Git declara (trailer) com o que a telemetria
observou. A diferença é o vazamento — uma métrica de maturidade, não uma acusação.
**Prova na demo:** detecta `relatorio.py` como IA vazada (33,3%).

### Camada 4 — Enquadramento
**O quê:** garantir que declarar IA seja neutro, para não incentivar o apagamento.
**Natureza:** cultural/organizacional — não há artefato de código.
**Princípio:** a métrica mede a **ferramenta e o processo**, nunca a competência
individual. Em ambiente regulado, casa com a narrativa de compliance: rastreabilidade
de proveniência é requisito de auditoria, não vigilância de produtividade.
**Operacionalização:** comunicação explícita na adoção; nunca usar o número de
"código de IA" em avaliação individual de desempenho.

## As 3 Linhas de Defesa (caso "dev commita pela CLI, não pela IDE")

### Linha 1 — Conveniência
**Artefato:** `hooks/prepare-commit-msg`.
**Cobre:** o commit via terminal. Detecta sessão de IA (variável de ambiente,
marcador `.ai-session`, ou prompt) e injeta o trailer automaticamente.
**Limite honesto:** client-side, logo burlável. É conveniência, não garantia.
**Prova na demo:** no Cenário 4, injeta o trailer num commit feito pela CLI.

### Linha 2 — Robustez
**Artefato:** o mesmo gate da Camada 1 (`gate_atribuicao.py`).
**Cobre:** o que escapou do hook. Atribui na fronteira do PR (server-side),
independentemente de como cada commit nasceu.
**Por que é robusta:** a fronteira do PR é governável; o commit individual não.

### Linha 3 — Rede de segurança
**Artefato:** o mesmo detector da Camada 3 (`detectar_delta.py`).
**Cobre:** o que escapou de tudo. A telemetria observa a *geração* de código,
não o commit — então pega IA mesmo sem trailer, sem branch, sem label.

## Mapa de sobreposição

Repare que Camada 1 ≡ Linha 2 (o gate) e Camada 3 ≡ Linha 3 (o detector). Não é
redundância: são o mesmo mecanismo cumprindo papéis em dois enquadramentos
diferentes (defesa contra apagamento vs. defesa contra commit-via-CLI). O
conjunto mínimo de artefatos que cobre tudo é:

| Artefato | Camadas/Linhas que cobre |
|---|---|
| `hooks/prepare-commit-msg` | Linha 1 |
| `gate_atribuicao.py` + workflow | Camada 1, Linha 2 |
| `verificar_integridade.py` | Camada 2 |
| `detectar_delta.py` | Camada 3, Linha 3 |
| (processo) | Camada 4 |
