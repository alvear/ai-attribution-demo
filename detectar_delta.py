#!/usr/bin/env python3
"""detectar_delta.py — CAMADA 3 / LINHA 3: vazamento via telemetria vs trailer."""
import csv, subprocess, sys

def git(repo,*a): return subprocess.run(["git","-C",repo,*a],capture_output=True,text=True,check=True).stdout

def declarados(repo):
    s=set()
    for sha in git(repo,"log","--format=%H").split():
        if "Co-Authored-By: AI Assistant" in git(repo,"show","-s","--format=%B",sha):
            for arq in git(repo,"show","--name-only","--format=",sha).split(): s.add(arq)
    return s

def observados(csv_path):
    s=set()
    with open(csv_path,newline="") as f:
        for r in csv.DictReader(f):
            if int(r.get("linhas_geradas_ia",0))>0: s.add(r["arquivo_tocado"])
    return s

repo, tele = sys.argv[1], sys.argv[2]
d, o = declarados(repo), observados(tele)
vaz = o - d
print("="*56); print("DETECTOR DE VAZAMENTO (Camada 3 / Linha 3)"); print("="*56)
print(f"IA observada (telemetria): {len(o)} | declarada (Git): {len(d & o)} | VAZADA: {len(vaz)}")
for a in sorted(d & o): print(f"  OK     {a}")
for a in sorted(vaz):   print(f"  VAZOU  {a}")
taxa = len(vaz)/len(o) if o else 0
print("-"*56); print(f"TAXA DE VAZAMENTO: {taxa:.1%}")
sys.exit(0)
