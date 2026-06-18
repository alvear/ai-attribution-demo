#!/usr/bin/env python3
"""
verificar_integridade.py — CAMADA 2 (Imutabilidade), demonstrada em codigo.

Na vida real, a imutabilidade vem de controles de PLATAFORMA (branch
protection proibindo force-push, commits assinados via GPG/SSH). Aqui
SIMULAMOS o EFEITO desses controles para provar que funcionam:

  A) Deteccao de history rewrite: compara o estado atual do branch contra
     um "selo" salvo (shas conhecidos). Se um commit ja selado sumiu ou
     mudou de SHA, houve rewrite — exatamente o que a branch protection
     impede no servidor.

  B) Validacao de assinatura: verifica se os commits estao assinados.
     Em ambiente regulado, commit nao-assinado = autoria nao garantida.

Uso:
  verificar_integridade.py <repo> selar          # salva o selo atual
  verificar_integridade.py <repo> verificar      # checa rewrite vs selo
  verificar_integridade.py <repo> assinaturas    # relatorio de assinatura
"""
import json
import subprocess
import sys
import os

SELO = "selo_integridade.json"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args],
                          capture_output=True, text=True).stdout


def estado_atual(repo):
    linhas = git(repo, "log", "--format=%H %s").strip().splitlines()
    return [{"sha": l.split(maxsplit=1)[0], "msg": l.split(maxsplit=1)[1]}
            for l in linhas if l]


def selar(repo):
    estado = estado_atual(repo)
    with open(SELO, "w") as f:
        json.dump(estado, f, indent=2)
    print(f"[integridade] selo salvo: {len(estado)} commits registrados.")
    print("  (representa o branch protegido — qualquer reescrita sera detectada)")


def verificar(repo):
    if not os.path.exists(SELO):
        print("[integridade] sem selo previo. Rode 'selar' primeiro.")
        return 1
    with open(SELO) as f:
        antigo = json.load(f)
    atual = estado_atual(repo)
    shas_antigos = [c["sha"] for c in antigo]
    shas_atuais = [c["sha"] for c in atual]

    sumiram = [c for c in antigo if c["sha"] not in shas_atuais]

    print("[integridade] verificando reescrita de historico...")
    if not sumiram:
        print("  ✅ OK — todos os commits selados continuam presentes e intactos.")
        print("     (branch protection faria cumprir isso no servidor)")
        return 0
    print("  ❌ REESCRITA DETECTADA — commits selados desapareceram:")
    for c in sumiram:
        print(f"     - {c['sha'][:8]} \"{c['msg']}\"")
    print("\n  No servidor real, a branch protection REJEITARIA este force-push.")
    print("  Aqui, detectamos o efeito: a tentativa de apagar a atribuicao falharia.")
    return 1


def assinaturas(repo):
    shas = git(repo, "log", "--format=%H").split()
    print("[integridade] relatorio de assinatura de commits:")
    assinados = 0
    for sha in shas:
        # %G? = status da assinatura: G=boa, N=nenhuma, etc.
        status = git(repo, "show", "-s", "--format=%G?", sha).strip()
        msg = git(repo, "show", "-s", "--format=%s", sha).strip()
        ok = status == "G"
        assinados += int(ok)
        marca = "✅ assinado" if ok else "⚠️  NAO assinado"
        print(f"  {marca}  {sha[:8]} \"{msg[:40]}\"")
    total = len(shas)
    print(f"\n  {assinados}/{total} commits assinados.")
    if assinados < total:
        print("  Em ambiente bancario, commits nao-assinados nao garantem autoria.")
        print("  Recomendacao: exigir commit signing na branch protection.")
    return 0 if assinados == total else 1


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    repo, cmd = sys.argv[1], sys.argv[2]
    return {"selar": selar, "verificar": verificar, "assinaturas": assinaturas}.get(
        cmd, lambda r: print("comando invalido") or 2)(repo) or 0


if __name__ == "__main__":
    sys.exit(main())
