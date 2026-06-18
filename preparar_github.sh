#!/usr/bin/env bash
#
# preparar_github.sh — Roda pelo COWORK. Prepara o que e seguro automatizar:
#   - instala o hook no repo principal (.git/hooks)
#   - gera COMANDOS_GITHUB.txt com os comandos que VOCE vai revisar e disparar
#
# NAO executa nenhuma acao que toque suas credenciais ou o GitHub remoto.
# Push, criacao de repo e branch protection ficam com VOCE (ver runbook).
#
set -uo pipefail

HOOK_SRC="hooks/prepare-commit-msg"

echo "== Preparando hook local =="
if [ -d ".git" ]; then
  mkdir -p .git/hooks
  cp "$HOOK_SRC" .git/hooks/prepare-commit-msg
  chmod +x .git/hooks/prepare-commit-msg
  echo "  Hook instalado em .git/hooks/prepare-commit-msg"
else
  echo "  (Ainda nao ha .git aqui — o hook sera instalado apos 'git init' na Fase 3.)"
fi

echo ""
echo "== Gerando COMANDOS_GITHUB.txt (para VOCE revisar e rodar) =="
cat > COMANDOS_GITHUB.txt <<'EOF'
# ============================================================
# COMANDOS PARA VOCE RODAR — nao deixe o agente executar estes.
# Eles tocam suas credenciais e seu GitHub remoto.
# Substitua SEU_USUARIO e o nome do repo conforme criou na web.
# ============================================================

# --- FASE 3: conectar local ao GitHub e push ---
git init -b main
git add gate_atribuicao.py detectar_delta.py verificar_integridade.py \
        gerar_relatorio.py setup_repo.sh demonstrar.sh preparar_github.sh \
        hooks/ .github/ telemetria_sintetica.csv telemetria_bloqueio.csv \
        README.md CAMADAS_E_LINHAS.md RUNBOOK_MAQUINA_GITHUB.md

# reinstala o hook (git init recriou .git/hooks)
mkdir -p .git/hooks && cp hooks/prepare-commit-msg .git/hooks/ && chmod +x .git/hooks/prepare-commit-msg

git commit -m "chore: estrutura inicial da demo de atribuicao de IA"
git remote add origin https://github.com/SEU_USUARIO/ai-attribution-demo.git
git push -u origin main

# Na autenticacao, use seu Personal Access Token como senha.
# (GitHub > Settings > Developer settings > Personal access tokens)

# --- FASE 5B: criar a branch do cenario de bloqueio ---
git checkout -b feature/sem-declaracao
# ... gere codigo com IA no Antigravity, commite SEM trailer ...
git push -u origin feature/sem-declaracao
# Depois abra o Pull Request pela web e observe o gate falhar.

# --- FASE 5C: tentar reescrever historico (deve ser REJEITADO pelo GitHub) ---
git commit --amend -m "tentativa de apagar atribuicao"
git push --force   # <- a branch protection deve recusar este push
EOF

echo "  COMANDOS_GITHUB.txt gerado."
echo ""
echo "== Pronto. Proximos passos sao seus (ver RUNBOOK_MAQUINA_GITHUB.md, Fases 2-5)."
