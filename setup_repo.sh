#!/usr/bin/env bash
#
# setup_repo.sh — Monta o repositorio que exercita as 4 CAMADAS e as
# 3 LINHAS DE DEFESA. Cria cenarios controlados:
#
#   - commit de IA COM trailer (fluxo IDE / hook funcionou)
#   - commit de IA SEM trailer (dev usou a CLI sem o hook -> vazamento)
#   - commit humano puro
#   - instala o hook prepare-commit-msg e demonstra ele injetando sozinho
#
set -euo pipefail

REPO_DIR="repo_demo"
HOOK_SRC="hooks/prepare-commit-msg"

rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"
cd "$REPO_DIR"

git init -q -b main
git config user.name  "Dev BV"
git config user.email "dev@bv.com.br"
git config commit.gpgsign false

commit_data () {  # <dias_atras> <msg> [--trailer cursor]
  local dias="$1"; local msg="$2"; local trailer="${3:-}"
  local data
  data="$(python3 -c "import datetime,sys;print((datetime.datetime(2026,6,18,12)-datetime.timedelta(days=int(sys.argv[1]))).strftime('%Y-%m-%dT%H:%M:%S'))" "$dias")"
  local full="$msg"
  if [ "$trailer" = "cursor" ]; then
    full="$msg

Co-Authored-By: AI Assistant <ai@noreply.local>
AI-Tool: cursor"
  fi
  GIT_AUTHOR_DATE="$data" GIT_COMMITTER_DATE="$data" git add -A
  GIT_AUTHOR_DATE="$data" GIT_COMMITTER_DATE="$data" git commit -q -m "$full"
}

echo "=== Cenario 1: commit humano puro ==="
echo "def login(u,p): return check(u,p)" > auth.py
commit_data 30 "base: autenticacao"

echo "=== Cenario 2: IA COM trailer (fluxo correto) ==="
echo "def juros(v,t,n): return v*(1+t)**n" > juros.py
commit_data 25 "feat: juros compostos" cursor

echo "=== Cenario 3: IA SEM trailer (dev commitou pela CLI -> VAZAMENTO) ==="
echo "def relatorio(d): return tabela(d)" > relatorio.py
commit_data 20 "feat: geracao de relatorio"

echo ""
echo "=== Agora instalamos o hook prepare-commit-msg (Linha 1) ==="
mkdir -p .git/hooks
cp "../$HOOK_SRC" .git/hooks/prepare-commit-msg
chmod +x .git/hooks/prepare-commit-msg
echo "Hook instalado em .git/hooks/prepare-commit-msg"

echo ""
echo "=== Cenario 4: dev commita pela CLI, mas agora COM sessao de IA ativa ==="
echo "  (marcador .ai-session presente -> o hook deve injetar o trailer sozinho)"
echo "cursor" > .ai-session
echo "def cache(k): return store.get(k)" > cache.py
git add cache.py
# NAO passamos trailer na mensagem; o hook deve adiciona-lo
GIT_AUTHOR_DATE="2026-06-08T12:00:00" GIT_COMMITTER_DATE="2026-06-08T12:00:00" \
  git commit -q -m "feat: camada de cache"
rm -f .ai-session
# .ai-session nunca foi adicionado ao index (so cache.py foi), entao nada a remover do index

echo ""
echo "=== Resultado: historico do repositorio ==="
git log --format="  %h %s" || true

cd ..

# ---------------------------------------------------------------------------
# Repo isolado para o cenario de BLOQUEIO do gate: um PR com um unico commit
# de IA SEM trailer (vazamento puro), para o gate ter o que bloquear.
# ---------------------------------------------------------------------------
BLOQ_DIR="repo_bloqueio"
rm -rf "$BLOQ_DIR"; mkdir -p "$BLOQ_DIR"; cd "$BLOQ_DIR"
git init -q -b main
git config user.name "Dev BV"; git config user.email "dev@bv.com.br"; git config commit.gpgsign false
echo "x=1" > base.py
GIT_AUTHOR_DATE="2026-06-01T12:00:00" GIT_COMMITTER_DATE="2026-06-01T12:00:00" git add -A
GIT_AUTHOR_DATE="2026-06-01T12:00:00" GIT_COMMITTER_DATE="2026-06-01T12:00:00" git commit -q -m "base humana"
git checkout -q -b feature/parser
echo "def parse(t): return t.split(',')" > parser.py
GIT_AUTHOR_DATE="2026-06-08T12:00:00" GIT_COMMITTER_DATE="2026-06-08T12:00:00" git add -A
GIT_AUTHOR_DATE="2026-06-08T12:00:00" GIT_COMMITTER_DATE="2026-06-08T12:00:00" git commit -q -m "feat: parser de extrato"
cd ..

echo ""
echo "Repos prontos: $REPO_DIR e $BLOQ_DIR"
