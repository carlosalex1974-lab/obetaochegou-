# 🤖 Contexto para o Agente - OBetãoChegou

> **Aviso para o Agente**: Ao iniciar uma nova conversa com o usuário para continuar o projeto "OBetãoChegou", leia este documento para recuperar todo o contexto imediatamente.

## 📌 Resumo do Projeto
O **OBetãoChegou** é uma aplicação focada em prever resultados esportivos (probabilidade de vitória, empate, e over 2.5 gols) de partidas de futebol reais. Os dados são extraídos diretamente da **API-Football** e salvos no banco de dados.

## 📂 Arquitetura e Diretórios
Os projetos estão na pasta: `C:\Users\carlo\Documents\codigo\`

### 1. Backend (`obetaochegou-backend`)
- **Stack**: Python, FastAPI, SQLAlchemy, PostgreSQL.
- **Banco de Dados**: Roda no Docker (`docker-compose.yml` disponível na pasta). O banco possui uma tabela `matches` que armazena os jogos e as estatísticas brutas na coluna `predictions_data` (tipo JSON).
- **Scripts úteis**:
  - `run_backend.bat`: Script à prova de falhas para ativar o `venv` e subir o Uvicorn na porta 8000.
  - `test_api.py`: Script de debug para testar as rotas de sincronização (`/sync`) e predições (`/predictions`).

### 2. Frontend (`obetaochegou-frontend`)
- **Stack**: HTML, CSS, JavaScript (puro/vanilla). Sem Node.js ou bundlers complexos.
- **Como executar**: Como as rotas da API possuem CORS liberado (`allow_origins=["*"]`), o frontend pode ser simplesmente acessado **abrindo o arquivo `index.html`** no navegador, ou rodando um servidor simples (`python -m http.server 5500`).
- **Comunicação**: O arquivo `app.js` bate na API em `http://localhost:8000/api/v1/matches/predictions`.

## ✅ O que já foi feito (Até 19/06/2026)
- Removemos os antigos algoritmos de valores "aleatórios" para palpites.
- Integrados com sucesso na `api_football.py` para extrair as *real stats*, percentuais de vitória/empate e conselho oficial (advice).
- Consertamos o banco de dados adicionando a nova coluna `predictions_data` para guardar as estatísticas dinâmicas sem quebrar a API.
- Reestabelecemos a comunicação entre o Frontend (Dashboard HTML) e o Backend, resolvendo os problemas de `ERR_CONNECTION_REFUSED`.

## 🚀 Como Iniciar a Aplicação (Tutorial rápido)
1. Certifique-se de que o Docker está rodando (para o Postgres, caso ele tenha sido desligado).
2. Na pasta raiz (`codigo`), dê dois cliques no arquivo `start_backend.bat` para subir a API de forma contínua.
3. Abra a pasta `obetaochegou-frontend` e arraste o arquivo `index.html` para o seu navegador (ou dê dois cliques nele).
4. Pressione "Atualizar Previsões" na tela!

## 🎯 Próximos Passos
- (A ser definido pelo usuário na próxima sessão). Você pode focar em melhorias de interface, adição de novas ligas, ou aprimoramento do bot de análise textual.
