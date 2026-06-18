# Demo: Defesa em Camadas da Atribuição de Código de IA

Laboratório executável que monta, configura e demonstra as **4 camadas** e as
**3 linhas de defesa** contra a perda de rastreabilidade da autoria de IA —
construídas no chat sobre Git e CI.

## Rodar tudo

```bash
bash demonstrar.sh          # demonstracao narrada, ponta a ponta
python3 gerar_relatorio.py  # gera relatorio.md executivo
```

## Componentes

| Arquivo | Papel | Camada / Linha |
|---|---|---|
| `hooks/prepare-commit-msg` | Injeta trailer mesmo no commit via CLI | Linha 1 |
| `gate_atribuicao.py` | Bloqueia merge sem IA declarada | Camada 1 / Linha 2 |
| `.github/workflows/ai-attribution-gate.yml` | Gate no GitHub real (colar e usar) | Camada 1 / Linha 2 |
| `verificar_integridade.py` | Detecta rewrite + valida assinaturas | Camada 2 |
| `detectar_delta.py` | Vazamento via telemetria × Git | Camada 3 / Linha 3 |
| `CAMADAS_E_LINHAS.md` | Runbook completo (inclui Camada 4 cultural) | todas |
| `setup_repo.sh` | Monta os cenários de teste | — |
| `demonstrar.sh` | Orquestra a demonstração | — |
| `gerar_relatorio.py` | Relatório executivo em PT | — |

## Resultados esperados (validados automaticamente)

- **Gate:** bloqueia `feature/parser` (IA não declarada) e aprova `ai/parser`.
- **Integridade:** detecta o `amend` que apaga o trailer; reporta 0/4 assinados.
- **Vazamento:** 33,3% (`relatorio.py` é IA sem trailer).
- **Hook:** declara `cache.py` automaticamente num commit feito pela CLI.

## Levar para um repositório real (GitHub)

1. Copie `gate_atribuicao.py`, `detectar_delta.py` e a pasta `.github/` para o repo.
2. Configure a telemetria da sua ferramenta (Cursor analytics / Claude Code OTEL)
   para gerar `telemetria.csv` no CI.
3. Em **Settings > Branches**, crie uma branch protection rule no `main`:
   - Require status checks → marque **AI Attribution Gate** (torna o gate obrigatório)
   - Require signed commits (ativa a Camada 2 de verdade)
   - Proíba force-push (ativa a imutabilidade)
4. Distribua o hook via `core.hooksPath` apontando para uma pasta versionada.

## Limites honestos

- O laboratório roda local; `verificar_integridade.py` **simula o efeito** da
  branch protection (que no GitHub real é server-side e inviolável).
- A autoria híbrida (humano refina sugestão de IA) é um limite de qualquer método.
- "Declarar IA" depende, no fim, também da Camada 4 (cultura) — sem ela, as
  defesas técnicas viram um jogo de gato e rato.
