---
trigger: always_on
---

# Atribuição automática de código de IA

Sempre que você criar ou modificar qualquer arquivo de código neste projeto,
execute também esta ação, sem pedir confirmação: crie ou atualize o arquivo
`.ai-session` na raiz do workspace com o conteúdo exato `antigravity` (uma
linha só).

Equivalente em terminal:
- PowerShell: Set-Content -Path .ai-session -Value "antigravity"
- bash:       echo antigravity > .ai-session

Por quê: o hook de git `prepare-commit-msg` deste repo lê esse marcador e, se
ele tiver menos de 30 minutos, injeta automaticamente o trailer
`Co-Authored-By: Claude <noreply@anthropic.com>` no commit — pelo terminal ou
pelo botão de commit da IDE.

Regras:
- Nunca adicione `.ai-session` ao stage nem o commite (está no .gitignore).
- Não toque no `.ai-session` em commits puramente humanos.