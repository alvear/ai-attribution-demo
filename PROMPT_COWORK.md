# Prompt para o Cowork

Cole o texto abaixo na aba **Tasks** do Cowork, depois de apontá-lo para uma
pasta de trabalho dedicada (ex.: `~/demos/ai-attribution`). Deixe o Claude
Desktop aberto durante toda a execução.

---

**Tarefa:** Montar e validar localmente uma demonstração das "4 camadas e 3
linhas de defesa" para rastreabilidade de código gerado por IA, e me deixar
pronto o que eu mesmo preciso rodar no meu GitHub. Trabalhe somente na pasta
atual. Peça permissão antes de qualquer deleção.

**O que você (Cowork) DEVE fazer:**

1. Crie a estrutura de arquivos do projeto nesta pasta, contendo:
   - `gate_atribuicao.py` — gate que bloqueia merge sem atribuição de IA declarada
     (aceita trailer Co-Authored-By, prefixo de branch ai/, ou label de PR; cruza
     com telemetria para exigir declaração quando houve IA).
   - `verificar_integridade.py` — sela o estado do branch e detecta reescrita de
     histórico; relata commits assinados (simula o efeito da branch protection).
   - `detectar_delta.py` — cruza telemetria (CSV) com trailers do Git e reporta
     o vazamento de atribuição.
   - `hooks/prepare-commit-msg` — hook que injeta o trailer de IA automaticamente
     quando detecta sessão de IA ativa (variável AI_SESSION ou arquivo .ai-session
     com menos de 30 min), funcionando inclusive em commit pela linha de comando.
   - `.github/workflows/ai-attribution-gate.yml` — workflow que roda o gate em
     todo Pull Request, pronto para virar required check.
   - `setup_repo.sh` — monta dois repositórios git de cenário (um com commits de
     IA com e sem trailer; outro isolado com um PR de IA sem declaração).
   - `demonstrar.sh` — roda a demonstração narrada de ponta a ponta.
   - `gerar_relatorio.py` — roda tudo, valida contra o esperado e gera relatorio.md.
   - `telemetria_sintetica.csv` e `telemetria_bloqueio.csv` — telemetria de exemplo.
   - `preparar_github.sh` — instala o hook e gera COMANDOS_GITHUB.txt.
   - `README.md`, `CAMADAS_E_LINHAS.md`, `RUNBOOK_MAQUINA_GITHUB.md`.

   > Se eu já tiver anexado o pacote pronto destes arquivos, apenas use-os em vez
   > de reescrever do zero — confira que estão completos e executáveis.

2. Torne executáveis: `chmod +x setup_repo.sh demonstrar.sh preparar_github.sh
   hooks/prepare-commit-msg *.py`.

3. Rode a validação local, NESTA ordem, e me mostre a saída de cada uma:
   - `bash setup_repo.sh`
   - `bash demonstrar.sh`
   - `python3 gerar_relatorio.py`
   Confirme que: o gate bloqueia o PR sem declaração e aprova quando há marcador;
   o verificador de integridade detecta a reescrita; o detector de vazamento
   reporta 33,3%; e o hook injeta o trailer num commit feito por linha de comando.

4. Rode `bash preparar_github.sh` para instalar o hook e gerar o
   `COMANDOS_GITHUB.txt`.

5. Ao final, me apresente um resumo curto com: o que foi validado, o conteúdo do
   `relatorio.md`, e instruções claras de quais comandos eu (humano) devo rodar
   em seguida para conectar ao meu GitHub.

**O que você (Cowork) NÃO deve fazer — é meu, por envolver credenciais/acesso:**
- Não rode `git push`, `git remote add`, nem nada que contate o GitHub remoto.
- Não tente autenticar no GitHub nem manipular tokens.
- Não configure branch protection (isso é pela interface web, por mim).
- Apenas deixe esses comandos prontos em `COMANDOS_GITHUB.txt` para eu revisar.

Se o ambiente tiver alguma restrição (git ausente, pasta sem permissão), me avise
em vez de contornar.

---

## Depois que o Cowork terminar

Siga o `RUNBOOK_MAQUINA_GITHUB.md` a partir da **Fase 2**: criar o repo privado
na web, dar push (Fase 3), ativar as proteções (Fase 4) e simular os cenários no
**Antigravity** (Fase 5), vendo cada defesa reagir.
