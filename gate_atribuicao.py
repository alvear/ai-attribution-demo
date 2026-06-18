#!/usr/bin/env python3
"""
gate_atribuicao.py — CAMADA 1 (Obrigatoriedade) + LINHA 2 (Robustez)

Gate server-side que valida, na fronteira do PR, se o trabalho de IA esta
DECLARADO. Roda no CI; se falhar, o merge e bloqueado pela branch protection.

A declaracao pode vir de TRES fontes (qualquer uma satisfaz), em ordem de
granularidade:
  1. Trailer Co-Authored-By no(s) commit(s)   -> melhor (nivel de linha)
  2. Marcador de branch (ex: ai/, feat-ai/)   -> nivel de PR
  3. Label de PR / arquivo de declaracao       -> nivel de PR

Filosofia: a ancora NAO e o commit individual (fragil, o dev controla),
e a DECLARACAO na fronteira do PR (server-side, governavel).

O gate so EXIGE declaracao quando ha sinal de que houve IA. Como o CI nao
ve a IDE, ele cruza com a telemetria: se a telemetria registrou IA para
aquele autor/periodo mas nada foi declarado, o gate FALHA pedindo declaracao.

Uso:
  gate_atribuicao.py <repo> <branch_atual> [--pr-label LABEL] [--telemetria CSV]
Saida: exit 0 (aprovado) / exit 1 (bloqueado)
"""
import argparse
import csv
import subprocess
import sys
from datetime import datetime


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True, check=True).stdout


def commits_do_pr(repo, base="main"):
    """Commits que o PR adiciona sobre a base. Na demo, todos os commits."""
    try:
        shas = git(repo, "log", base + "..HEAD", "--format=%H").split()
        if not shas:
            shas = git(repo, "log", "--format=%H").split()
    except subprocess.CalledProcessError:
        shas = git(repo, "log", "--format=%H").split()
    return shas


def tem_trailer(repo, sha):
    corpo = git(repo, "show", "-s", "--format=%B", sha)
    return "Co-Authored-By: AI Assistant" in corpo


def branch_marca_ia(branch):
    return any(branch.startswith(p) for p in ("ai/", "feat-ai/", "ia/"))


def autores_dos_commits(repo, shas):
    out = set()
    for sha in shas:
        email = git(repo, "show", "-s", "--format=%ae", sha).strip()
        data = git(repo, "show", "-s", "--format=%aI", sha).strip()[:10]
        out.add((email, data))
    return out


def telemetria_indica_ia(csv_path, autores_datas):
    """True se a telemetria registrou IA para algum (autor, data) do PR."""
    if not csv_path:
        return False
    datas_autores = {(e, d) for e, d in autores_datas}
    try:
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                chave = (row["dev"], row["data"])
                if chave in datas_autores and int(row.get("linhas_geradas_ia", 0)) > 0:
                    return True
    except FileNotFoundError:
        return False
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("branch")
    ap.add_argument("--pr-label", default="")
    ap.add_argument("--telemetria", default="")
    ap.add_argument("--base", default="main")
    args = ap.parse_args()

    shas = commits_do_pr(args.repo, args.base)
    print(f"[gate] avaliando {len(shas)} commit(s) na branch '{args.branch}'")

    # Sinais de declaracao
    algum_trailer = any(tem_trailer(args.repo, s) for s in shas)
    branch_ok = branch_marca_ia(args.branch)
    label_ok = args.pr_label.lower() in ("ai", "ia", "ai-assisted", "ia-assistida")
    declarado = algum_trailer or branch_ok or label_ok

    # Sinal de que HOUVE ia (telemetria)
    autores = autores_dos_commits(args.repo, shas)
    houve_ia = telemetria_indica_ia(args.telemetria, autores)

    print(f"[gate] declaracao: trailer={algum_trailer} branch={branch_ok} label={label_ok}")
    print(f"[gate] telemetria indica IA neste PR: {houve_ia}")

    # Regra de decisao
    if houve_ia and not declarado:
        print("\n[gate] ❌ BLOQUEADO")
        print("  A telemetria registrou uso de IA neste PR, mas nada foi declarado.")
        print("  Acoes para desbloquear (qualquer uma):")
        print("   - commitar com trailer Co-Authored-By, OU")
        print("   - renomear a branch para ai/... , OU")
        print("   - aplicar o label 'ai-assisted' no PR")
        return 1

    if declarado:
        print("\n[gate] ✅ APROVADO — trabalho de IA declarado corretamente.")
    else:
        print("\n[gate] ✅ APROVADO — nenhum sinal de IA; PR humano.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
