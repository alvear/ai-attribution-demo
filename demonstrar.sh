#!/usr/bin/env bash
#
# demonstrar.sh — Roda a demonstracao completa das 4 CAMADAS e 3 LINHAS
# de defesa, em sequencia narrada. Cada bloco anuncia o que prova.
#
set -uo pipefail

linha() { printf '\n\033[1m%s\033[0m\n' "$1"; printf '%s\n' "------------------------------------------------------------"; }

linha "PREPARACAO — montando o repositorio de cenarios"
bash setup_repo.sh

linha "LINHA 1 (Conveniencia) — prepare-commit-msg hook"
echo "Ja demonstrado acima: no Cenario 4, o dev commitou pela CLI sem trailer,"
echo "mas o hook detectou a sessao de IA (.ai-session) e injetou o trailer."
echo "Compare: relatorio.py (antes do hook) VAZOU; cache.py (com hook) ficou OK."

linha "LINHA 2 / CAMADA 1 (Robustez / Obrigatoriedade) — gate no PR"
echo ">> Cenario que deve BLOQUEAR (IA na telemetria, nada declarado):"
python3 gate_atribuicao.py repo_bloqueio "feature/parser" --telemetria telemetria_bloqueio.csv --base main
echo "[exit=$?]"
echo ""
echo ">> Mesmo PR, dev corrige renomeando a branch para ai/ (deve APROVAR):"
python3 gate_atribuicao.py repo_bloqueio "ai/parser" --telemetria telemetria_bloqueio.csv --base main
echo "[exit=$?]"

linha "CAMADA 2 (Imutabilidade) — deteccao de reescrita + assinaturas"
echo ">> Selando o estado do branch protegido:"
python3 verificar_integridade.py repo_demo selar
echo ""
echo ">> Dev tenta apagar a atribuicao reescrevendo o historico (amend):"
git -C repo_demo commit -q --amend -m "feat: cache (atribuicao apagada)" --no-verify
echo ">> Verificador detecta a reescrita (branch protection rejeitaria no servidor):"
python3 verificar_integridade.py repo_demo verificar
echo "[exit=$?]"
echo ""
echo ">> Relatorio de assinaturas (autoria garantida?):"
python3 verificar_integridade.py repo_demo assinaturas | tail -4

linha "CAMADA 3 / LINHA 3 (Visibilidade / Rede de seguranca) — detector de vazamento"
bash setup_repo.sh >/dev/null 2>&1   # restaura repo limpo
python3 detectar_delta.py repo_demo telemetria_sintetica.csv

linha "CAMADA 4 (Enquadramento) — nao-executavel"
echo "Esta camada e cultural, nao tecnica: declarar uso de IA deve ser NEUTRO."
echo "Se 'codigo de IA' virar sinonimo de 'codigo de segunda', os devs apagam"
echo "o trailer e todo o dado se perde. A metrica mede a FERRAMENTA e o PROCESSO,"
echo "nunca a competencia individual. Ver runbook em CAMADAS_E_LINHAS.md."

linha "FIM — gere o relatorio executivo com: python3 gerar_relatorio.py"
