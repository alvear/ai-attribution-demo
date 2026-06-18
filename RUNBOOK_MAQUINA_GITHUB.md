# Runbook de Operação — Demo das 4 Camadas e 3 Linhas na sua máquina + GitHub

Guia para **configurar, simular e ver funcionando** as defesas de atribuição de
IA, usando **Cowork** para orquestrar, **Antigravity** como ambiente onde você
roda e assiste, e um **repositório privado pessoal** no seu GitHub.

## Legenda das raias

- 🤖 **COWORK** — o agente executa (gerar arquivos, montar cenários, rodar scripts).
- 👤 **VOCÊ** — ações que tocam credenciais/acesso do GitHub; ninguém faz por você.
- 🛰️ **ANTIGRAVITY** — onde você abre o projeto, gera código com IA e observa.

---

## Pré-requisitos (👤 VOCÊ, uma vez)

1. **Git instalado** — confirme no terminal: `git --version`.
2. **Conta no GitHub** com acesso à criação de repositórios privados.
3. **Antigravity instalado e aberto** na máquina.
4. **Cowork** disponível no Claude Desktop (deixe o app aberto durante a execução —
   se fechar, a sessão encerra).

> Você optou por **não usar o gh CLI**. Então as ações no GitHub serão pela
> **interface web** (criar repo, branch protection) e por **git puro** (push).

---

## FASE 1 — Montar o projeto local (🤖 COWORK)

Aponte o Cowork para uma pasta de trabalho dedicada (ex.: `~/demos/ai-attribution`)
e use o prompt em `PROMPT_COWORK.md`. Ele vai:

1. Recriar a estrutura de arquivos da demo (scripts, hook, workflow, telemetria).
2. Rodar `setup_repo.sh` para gerar os repositórios de cenário localmente.
3. Rodar `demonstrar.sh` e `gerar_relatorio.py` para provar que tudo funciona
   **antes** de tocar o GitHub.
4. Deixar pronto um `COMANDOS_GITHUB.txt` com os comandos git que VOCÊ vai disparar.

✅ Resultado esperado: gate bloqueia/aprova, integridade detecta rewrite,
vazamento = 33,3%, hook injeta trailer. (Igual à validação do laboratório.)

---

## FASE 2 — Criar o repositório no GitHub (👤 VOCÊ)

Pela interface web (github.com):

1. Canto superior direito → **New repository**.
2. Nome: `ai-attribution-demo` (ou o que preferir).
3. Visibilidade: **Private**. ✔️
4. **Não** inicialize com README/gitignore (o projeto local já tem conteúdo).
5. **Create repository**. Copie a URL HTTPS que aparece (ex.:
   `https://github.com/SEU_USUARIO/ai-attribution-demo.git`).

> Por que VOCÊ e não o Cowork: criar repositório e autenticar são ações de
> acesso à sua conta. O agente não deve assumir suas credenciais.

---

## FASE 3 — Conectar o local ao GitHub e dar push (👤 VOCÊ)

O Cowork deixou os comandos prontos em `COMANDOS_GITHUB.txt`. Revise e rode você
mesmo, no terminal, dentro da pasta principal do projeto:

```bash
# transforma a pasta do projeto num repo git "de verdade" (o main que vai pro GitHub)
git init -b main
git add gate_atribuicao.py detectar_delta.py verificar_integridade.py \
        gerar_relatorio.py setup_repo.sh demonstrar.sh \
        hooks/ .github/ telemetria_sintetica.csv telemetria_bloqueio.csv \
        README.md CAMADAS_E_LINHAS.md
git commit -m "chore: estrutura inicial da demo de atribuicao de IA"

# conecta ao repo que VOCÊ criou na Fase 2
git remote add origin https://github.com/SEU_USUARIO/ai-attribution-demo.git
git push -u origin main
```

> Na primeira vez, o git vai pedir autenticação. Use seu **Personal Access Token**
> (Settings → Developer settings → Tokens) como senha — o GitHub não aceita mais
> senha de conta no push. Isso é VOCÊ; não compartilhe o token com nenhum agente.

---

## FASE 4 — Ativar as defesas server-side (👤 VOCÊ, pela web)

Aqui ativamos de verdade a **Camada 1** (gate obrigatório) e a **Camada 2**
(imutabilidade). Tudo em **Settings** do repo:

### 4a. Tornar o gate obrigatório (Camada 1 / Linha 2)
Primeiro deixe o workflow rodar uma vez (a Fase 5 cria um PR). Depois:
- **Settings → Branches → Add branch protection rule**
- Branch name pattern: `main`
- ✔️ **Require status checks to pass before merging**
- Procure e marque **AI Attribution Gate** na lista de checks.

### 4b. Imutabilidade (Camada 2)
Na mesma regra de proteção:
- ✔️ **Require signed commits** (autoria à prova de adulteração).
- ✔️ **Do not allow force pushes** (impede reescrita de histórico).
- ✔️ **Do not allow deletions**.

> Estas três caixas são o que, na demo local, o `verificar_integridade.py`
> apenas *simulava*. Aqui passam a ser cumpridas de verdade pelo GitHub.

---

## FASE 5 — Simular os cenários e VER funcionando (🛰️ ANTIGRAVITY + 👤 VOCÊ)

Abra a pasta do projeto no **Antigravity**. Cada cenário abaixo é uma prova viva.

### Cenário A — Hook salva o commit via terminal (Linha 1)
1. No Antigravity, peça ao agente de IA para gerar uma função nova num arquivo
   (ex.: `def desconto(v, p): ...` em `promocoes.py`). Isso liga a "sessão de IA".
2. Garanta que o hook está ativo: copie `hooks/prepare-commit-msg` para
   `.git/hooks/` e `chmod +x`. (O Cowork deixa isso pronto num script.)
3. Commit pelo **terminal**, sem trailer manual:
   `git add promocoes.py && git commit -m "feat: calculo de desconto"`
4. **Observe:** o hook detecta a sessão e injeta o trailer sozinho.
   Confirme com `git show -s --format=%B HEAD` — o `Co-Authored-By` está lá.

### Cenário B — Gate bloqueia IA não declarada (Camada 1 / Linha 2)
1. Crie uma branch `feature/sem-declaracao`, gere código com IA, e commite
   **sem** trailer (desligue o hook temporariamente, ou renomeie `.ai-session`).
2. Abra um **Pull Request** dessa branch para `main` no GitHub.
3. **Observe:** o workflow **AI Attribution Gate** roda e **falha** — o merge
   fica bloqueado. (Se você configurou a telemetria; veja nota abaixo.)
4. Corrija: renomeie a branch para `ai/...` ou adicione o label `ai-assisted`.
   O check passa e o merge libera.

### Cenário C — Imutabilidade barra o apagamento (Camada 2)
1. Tente reescrever um commit já no `main` para remover o trailer:
   `git commit --amend` e `git push --force`.
2. **Observe:** o GitHub **rejeita o force-push** por causa da branch protection.
   A tentativa de apagar a atribuição falha no servidor.

### Cenário D — Detector de vazamento expõe o que escapou (Camada 3 / Linha 3)
1. Rode localmente: `python3 detectar_delta.py repo_demo telemetria_sintetica.csv`
2. **Observe:** os arquivos com IA na telemetria mas sem trailer no Git aparecem
   como "VAZADO". É a rede de segurança que não depende do commit.

### Camada 4 — Enquadramento
Não tem cenário técnico: é a regra de que declarar IA é neutro e nunca entra em
avaliação individual. Está documentada em `CAMADAS_E_LINHAS.md` para você levar
junto na apresentação.

---

## Nota sobre a telemetria no GitHub real

No laboratório, a telemetria é um CSV sintético. Em produção, o workflow precisa
de telemetria **real** da sua ferramenta (Cursor analytics / export OTEL do
Claude Code / dados do Antigravity) salva como `telemetria.csv` no job de CI.
Enquanto você não pluga isso, o gate roda só com os sinais do Git (trailer,
branch, label) — o que já demonstra os Cenários A, B e C. O Cenário B com
**detecção por telemetria** (bloquear quem usou IA e não declarou) só fica
completo quando a telemetria real estiver conectada.

---

## Checklist de execução

- [ ] FASE 1 — Cowork montou e validou o projeto local
- [ ] FASE 2 — VOCÊ criou o repo privado na web
- [ ] FASE 3 — VOCÊ deu push do main
- [ ] FASE 4 — VOCÊ ativou gate obrigatório + signed commits + no force-push
- [ ] FASE 5A — hook injetou trailer no commit via terminal
- [ ] FASE 5B — gate bloqueou PR sem declaração
- [ ] FASE 5C — GitHub rejeitou o force-push
- [ ] FASE 5D — detector de vazamento apontou os arquivos vazados
```
