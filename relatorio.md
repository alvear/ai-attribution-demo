# Demonstração: Defesa em Camadas da Atribuição de Código de IA

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
| Camada 1 / Linha 2 — Gate no PR | Bloqueia merge sem declaração | ✅ bloqueou IA não declarada e liberou após correção |
| Camada 2 — Imutabilidade | Detecta reescrita de histórico | ✅ detectou o apagamento via amend |
| Camada 3 / Linha 3 — Visibilidade | Cruza telemetria × Git | ✅ vazamento medido: **33.3%** |
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

**O vazamento residual vira métrica de maturidade.** Os 33.3% de vazamento medidos
aqui não são falha: são o indicador honesto de quão confiável está a atribuição.
Acompanhado ao longo do tempo, ele mostra a evolução do processo — exatamente o
tipo de número de governança que sustenta uma narrativa de compliance perante
auditoria, sem transformar a métrica em vigilância individual (Camada 4).

**Pronto para produção.** O gate já vem como GitHub Actions workflow; basta marcá-lo
como required check. As demais camadas mapeiam para controles de plataforma
(branch protection, commit signing) que o ambiente regulado provavelmente já exige.

---
*Validação: gate OK | integridade OK | detector de vazamento OK.*
