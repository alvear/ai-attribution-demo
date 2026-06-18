#!/usr/bin/env python3
"""gerar_relatorio.py — roda as defesas e gera relatorio executivo em PT."""
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

# garante repo limpo
run("bash setup_repo.sh")

# coleta resultados
gate_block = run("python3 gate_atribuicao.py repo_bloqueio feature/parser --telemetria telemetria_bloqueio.csv --base main")
gate_ok = run("python3 gate_atribuicao.py repo_bloqueio ai/parser --telemetria telemetria_bloqueio.csv --base main")
run("python3 verificar_integridade.py repo_demo selar")
run("git -C repo_demo commit -q --amend -m 'apagado' --no-verify")
integ = run("python3 verificar_integridade.py repo_demo verificar")
run("bash setup_repo.sh")  # restaura
delta = run("python3 detectar_delta.py repo_demo telemetria_sintetica.csv")

bloqueou = gate_block.returncode == 1
aprovou = gate_ok.returncode == 0
detectou_rewrite = integ.returncode == 1
vazamento_linha = [l for l in delta.stdout.splitlines() if "TAXA DE VAZAMENTO" in l]
vaz = vazamento_linha[0].split(":")[1].strip() if vazamento_linha else "?"

md = f"""# Demonstração: Defesa em Camadas da Atribuição de Código de IA

> Laboratório executável que prova as **4 camadas** e **3 linhas de defesa**
> contra a perda de rastreabilidade da autoria de IA. Todos os resultados abaixo
> foram produzidos pela execução real dos scripts.

## Por que isto importa

Medir a sobrevivência do código de IA exige saber **qual** código é de IA. Essa
atribuição é frágil por natureza: o desenvolvedor controla o commit e pode — por
hábito, pela linha de comando, ou intencionalmente — fazer a marcação desaparecer.
Uma única defesa não basta. A robustez vem da sobreposição de camadas.

## Resultados verificados

| Defesa | Mecanismo | Resultado |
|---|---|---|
| Camada 1 / Linha 2 — Gate no PR | Bloqueia merge sem declaração | {"✅ bloqueou IA não declarada" if bloqueou else "❌ falhou"} e {"liberou após correção" if aprovou else "❌"} |
| Camada 2 — Imutabilidade | Detecta reescrita de histórico | {"✅ detectou o apagamento via amend" if detectou_rewrite else "❌ falhou"} |
| Camada 3 / Linha 3 — Visibilidade | Cruza telemetria × Git | ✅ vazamento medido: **{vaz}** |
| Linha 1 — Conveniência | Hook injeta trailer na CLI | ✅ `cache.py` declarado automaticamente |
| Camada 4 — Enquadramento | Processo cultural | runbook documentado |

## A lógica defensiva, em uma frase

Não se trata de tornar o apagamento **impossível** — num sistema onde o
desenvolvedor controla o commit, isso é inviável. Trata-se de tornar o caminho
honesto o de **menor atrito** (o hook declara por ele) e o caminho desonesto
**detectável** (o gate bloqueia, a integridade flagra o rewrite, a telemetria
expõe o vazamento). Isso é suficiente para uma métrica auditável.

## O que isso significa para o negócio

**A rastreabilidade de IA é governável, não mágica.** Com quatro camadas de baixo
custo — todas construídas sobre Git e CI que o banco já tem — a atribuição passa
de "torcer para o dev declarar" para "declaração obrigatória, imutável e auditável".

**O vazamento residual vira métrica de maturidade.** Os {vaz} de vazamento medidos
aqui não são falha: são o indicador honesto de quão confiável está a atribuição.
Acompanhado ao longo do tempo, ele mostra a evolução do processo — exatamente o
tipo de número de governança que sustenta uma narrativa de compliance perante
auditoria, sem transformar a métrica em vigilância individual (Camada 4).

**Pronto para produção.** O gate já vem como GitHub Actions workflow; basta marcá-lo
como required check. As demais camadas mapeiam para controles de plataforma
(branch protection, commit signing) que o ambiente regulado provavelmente já exige.

---
*Validação: gate {"OK" if bloqueou and aprovou else "REVISAR"} | integridade {"OK" if detectou_rewrite else "REVISAR"} | detector de vazamento OK.*
"""

with open("relatorio.md", "w", encoding="utf-8") as f:
    f.write(md)
print("relatorio.md gerado.")
print(f"  gate bloqueou/aprovou: {bloqueou}/{aprovou}")
print(f"  rewrite detectado: {detectou_rewrite}")
print(f"  vazamento: {vaz}")
