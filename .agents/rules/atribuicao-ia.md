---
description: Marca automaticamente a sessao de IA para rastreabilidade de atribuicao
activation: always_on
---

# Atribuicao automatica de codigo gerado por IA

Este projeto rastreia qual codigo foi escrito com auxilio de IA. Sempre que
voce (agente do Antigravity) criar ou modificar QUALQUER arquivo de codigo,
execute tambem esta acao, sem pedir confirmacao:

1. Crie ou atualize o arquivo `.ai-session` na raiz do workspace com o conteudo
   exato `antigravity` (uma unica linha, sem aspas).

   Equivalente em terminal:
   - PowerShell: `Set-Content -Path .ai-session -Value "antigravity"`
   - bash:       `echo antigravity > .ai-session`

Por que: o hook de git `prepare-commit-msg` deste repo le esse marcador e, se
ele tiver menos de 30 minutos, injeta automaticamente o trailer
`Co-Authored-By: Claude <noreply@anthropic.com>` / `AI-Tool: antigravity` no
commit — seja pelo terminal, seja pelo botao de commit da IDE. Assim a
atribuicao de IA fica registrada sem o desenvolvedor precisar digitar nada.

Regras importantes:
- NUNCA adicione `.ai-session` ao stage nem o commite (ele esta no .gitignore).
- NAO toque no `.ai-session` em commits puramente humanos (quando voce nao
  gerou codigo). O marcador deve refletir apenas atividade real de IA.
- Atualize o timestamp do `.ai-session` a cada nova edicao de codigo, para que
  a janela de 30 minutos do hook continue valida.
