import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

def generate_ai_rationale(home_team: str, away_team: str, predictions_data: dict) -> str:
    """Usa o Llama 3 (via Groq) para gerar uma análise carismática da partida."""
    
    preds = predictions_data.get("predictions", {})
    home_win_prob = preds.get("percent", {}).get("home", "33%")
    draw_prob = preds.get("percent", {}).get("draw", "33%")
    away_win_prob = preds.get("percent", {}).get("away", "33%")
    recommended_bet = preds.get("advice", "Sem recomendação")

    if not client:
        return _fallback_heuristic(home_team, away_team, home_win_prob, draw_prob, away_win_prob, recommended_bet)
        
    try:
        preds = predictions_data.get("predictions", {})
        home_win_prob = preds.get("percent", {}).get("home", "33%")
        draw_prob = preds.get("percent", {}).get("draw", "33%")
        away_win_prob = preds.get("percent", {}).get("away", "33%")
        recommended_bet = preds.get("advice", "Sem recomendação")
        
        # Extrair dados ricos
        teams_data = predictions_data.get("teams", {})
        home_form = teams_data.get("home", {}).get("last_5", {}).get("form", "N/A")
        away_form = teams_data.get("away", {}).get("last_5", {}).get("form", "N/A")
        
        home_goals_for = teams_data.get("home", {}).get("last_5", {}).get("goals", {}).get("for", {}).get("average", "N/A")
        home_goals_against = teams_data.get("home", {}).get("last_5", {}).get("goals", {}).get("against", {}).get("average", "N/A")
        
        away_goals_for = teams_data.get("away", {}).get("last_5", {}).get("goals", {}).get("for", {}).get("average", "N/A")
        away_goals_against = teams_data.get("away", {}).get("last_5", {}).get("goals", {}).get("against", {}).get("average", "N/A")

        prompt = f"""
Você é o 'OBetão', um super especialista e analista tático de futebol e apostas esportivas do Brasil.
Você faz análises profundas, mas fala de um jeito carismático, empolgante e direto ao ponto.

Confronto: {home_team} (Casa) vs {away_team} (Fora)

ESTATÍSTICAS DA API:
- Probabilidades de Vitória: Casa: {home_win_prob} | Empate: {draw_prob} | Fora: {away_win_prob}
- Fase atual (aproveitamento últimos 5 jogos): {home_team}: {home_form} | {away_team}: {away_form}
- Média de Gols Marcados (últimos 5): {home_team}: {home_goals_for} | {away_team}: {away_goals_for}
- Média de Gols Sofridos (últimos 5): {home_team}: {home_goals_against} | {away_team}: {away_goals_against}
- Recomendação Oficial: {recommended_bet}

Escreva uma ANÁLISE OBJETIVA, DIRETA E BASEADA EM DADOS.
IMPORTANTE: Comece o texto exatamente com: "O OBetão recomenda para essa partida..."

Sua resposta deve conter DUAS PARTES:

PARTE 1: Resumo Analítico (1 parágrafo curto)
Seja extremamente direto, claro e analítico. Evite rodeios. Justifique a expectativa da partida cruzando as probabilidades de vitória, o aproveitamento recente e as médias de gols.

PARTE 2: 5 Palpites de Apostas
Forneça EXATAMENTE 5 palpites de apostas para o jogo.
IMPORTANTE: Pelo menos UM dos 5 palpites DEVE ser no mercado de Cantos (Escanteios). Como os dados exatos de cantos não estão listados, faça uma dedução lógica baseada no poder de ataque (ex: times mais favoritos ou jogos mais pegados costumam ter +8.5 ou +9.5 cantos).

Para CADA palpite, forneça:
- O Palpite (O que apostar)
- Força (Alta, Média ou Baixa)
- Probabilidade Estimada (%)

Formate a Parte 2 como uma lista clara e legível. Entregue informações precisas e consistentes. Não invente dados absurdos, deduza as probabilidades de forma lógica com base nas estatísticas fornecidas. Apenas texto direto ao ponto.
"""
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao gerar análise com Groq: {e}. Usando Heurística Local.")
        return _fallback_heuristic(home_team, away_team, home_win_prob, draw_prob, away_win_prob, recommended_bet)

def _fallback_heuristic(home_team, away_team, home_win_prob, draw_prob, away_win_prob, recommended_bet):
    home_is_fav = False
    away_is_fav = False
    if "%" in home_win_prob:
        hw = int(home_win_prob.replace("%", ""))
        if hw > 50: home_is_fav = True
    if "%" in away_win_prob:
        aw = int(away_win_prob.replace("%", ""))
        if aw > 50: away_is_fav = True
        
    p1 = f"OBetão recomenda para essa partida: Analisando os dados do confronto, "
    if home_is_fav:
        p1 += f"o {home_team} vem com uma força absurda jogando em casa, com {home_win_prob} de chance de vitória. Eles são os francos favoritos para amassar o {away_team}."
    elif away_is_fav:
        p1 += f"o {away_team} é o grande favorito mesmo jogando fora de casa, segurando {away_win_prob} de probabilidade. O {home_team} vai ter que suar muito a camisa para segurar a zebra."
    else:
        p1 += f"esse jogo tá com uma cara de ser extremamente truncado e brigado no meio de campo! As probabilidades de {home_team} ({home_win_prob}) e {away_team} ({away_win_prob}) estão muito equilibradas."
        
    p2 = f"Minha recomendação cravada baseada nos algoritmos é: {recommended_bet}. Pode ir sem medo que a estatística está do nosso lado pra buscar esse green!"
    
    return f"{p1}\n\n{p2}"

def validate_predictions(original_rationale: str, match_stats: dict) -> dict:
    """Usa o Llama 3 (via Groq) para ler o palpite dado e o resultado do jogo, e dar o selo de Green/Red."""
    if not client:
        return {"status": "error", "message": "Groq client not initialized"}
        
    prompt = f"""
Você é um auditor implacável de apostas esportivas.
Abaixo está o texto de "5 Palpites de Apostas" que o OBetão gerou ANTES do jogo começar.
E também estão as Estatísticas Finais reais de como o jogo terminou.

Sua tarefa é avaliar CADA UM dos 5 palpites (e apenas os 5 palpites da Parte 2) e decidir de forma puramente matemática se foi GREEN (Acertou) ou RED (Errou).

TEXTO ORIGINAL GERADO PELO OBETÃO ANTES DO JOGO:
{original_rationale}

ESTATÍSTICAS FINAIS DO JOGO (API FOOTBALL):
{match_stats}

RETORNE EXATAMENTE UM JSON, E NADA MAIS. O JSON DEVE TER O SEGUINTE FORMATO:
{{
    "results": [
        {{
            "palpite": "texto do palpite 1",
            "resultado": "GREEN" ou "RED",
            "explicacao": "ex: Placar final foi 2x1 (3 gols), portanto bateu."
        }},
        ... os outros 4 palpites ...
    ]
}}
"""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"},
            max_tokens=800,
        )
        import json
        return json.loads(completion.choices[0].message.content.strip())
    except Exception as e:
        print(f"Erro ao validar predições com Groq: {str(e)}")
        return {"status": "error", "message": str(e)}

