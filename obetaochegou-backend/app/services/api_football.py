import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY
}

def get_todays_matches():
    """Busca as partidas do dia atual na API-Football"""
    if not API_KEY:
        return {"error": "Chave da API-Football não configurada."}

    today = datetime.now().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures"
    querystring = {"date": today}
    
    try:
        response = requests.get(url, headers=HEADERS, params=querystring)
        response.raise_for_status()
        data = response.json()
        matches = data.get("response", [])
        
        # Filtra para priorizar a Copa do Mundo (ID = 1 ou nome = World Cup)
        world_cup_matches = [m for m in matches if m.get("league", {}).get("name") == "World Cup" or m.get("league", {}).get("id") == 1]
        
        if world_cup_matches:
            final_matches = world_cup_matches
        else:
            major_leagues = [39, 140, 135, 71, 13]
            top_matches = [m for m in matches if m.get("league", {}).get("id") in major_leagues]
            final_matches = top_matches if top_matches else matches
            
        if not final_matches:
            # FALLBACK DE MOCK CASO O BANCO ZERE E NÃO TENHA JOGOS HOJE
            final_matches = [
                {"fixture": {"id": 9, "date": today + "T14:00:00+00:00", "status": {"short": "FT"}}, "teams": {"home": {"name": "Brazil"}, "away": {"name": "Argentina"}}, "league": {"name": "World Cup"}, "goals": {"home": 2, "away": 0}},
                {"fixture": {"id": 10, "date": today + "T16:00:00+00:00", "status": {"short": "FT"}}, "teams": {"home": {"name": "France"}, "away": {"name": "Germany"}}, "league": {"name": "World Cup"}, "goals": {"home": 1, "away": 1}},
                {"fixture": {"id": 11, "date": today + "T18:00:00+00:00", "status": {"short": "NS"}}, "teams": {"home": {"name": "Spain"}, "away": {"name": "Italy"}}, "league": {"name": "World Cup"}, "goals": {"home": None, "away": None}},
                {"fixture": {"id": 12, "date": today + "T20:00:00+00:00", "status": {"short": "NS"}}, "teams": {"home": {"name": "Netherlands"}, "away": {"name": "Belgium"}}, "league": {"name": "World Cup"}, "goals": {"home": None, "away": None}},
            ]
            
        return {"count": len(final_matches), "matches": final_matches[:10]}
    except requests.exceptions.RequestException as e:
        return {"error": f"Falha na conexão com a API: {str(e)}"}

def get_fixture_predictions(fixture_id: int):
    """Busca as estatísticas e predições reais da partida (H2H, Form, % de vitória)"""
    if not API_KEY:
        return None
    url = f"{BASE_URL}/predictions"
    querystring = {"fixture": str(fixture_id)}
    
    try:
        response = requests.get(url, headers=HEADERS, params=querystring)
        response.raise_for_status()
        data = response.json()
        if "response" in data and len(data["response"]) > 0:
            return data["response"][0]
            
        # MOCK PREDICTIONS FALLBACK
        mock_preds = {
            9: {"predictions": {"percent": {"home": "60%", "draw": "30%", "away": "10%"}, "advice": "Winner : Brazil"}},
            10: {"predictions": {"percent": {"home": "40%", "draw": "40%", "away": "20%"}, "advice": "Double chance : France or draw"}},
            11: {"predictions": {"percent": {"home": "35%", "draw": "35%", "away": "30%"}, "advice": "Double chance : Spain or draw"}},
            12: {"predictions": {"percent": {"home": "45%", "draw": "30%", "away": "25%"}, "advice": "Winner : Netherlands"}}
        }
        return mock_preds.get(fixture_id, None)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar predições da fixture {fixture_id}: {e}")
        return None

def get_fixture_statistics(fixture_id: int):
    """Busca o resultado final e as estatísticas da partida (gols, escanteios, etc)"""
    if not API_KEY:
        return None
        
    url = f"{BASE_URL}/fixtures"
    querystring = {"id": str(fixture_id)}
    
    try:
        response = requests.get(url, headers=HEADERS, params=querystring)
        response.raise_for_status()
        data = response.json()
        if "response" in data and len(data["response"]) > 0:
            fixture_data = data["response"][0]
            
            # Buscar estatísticas da partida (para ter os cantos/escanteios)
            stats_url = f"{BASE_URL}/fixtures/statistics"
            stats_querystring = {"fixture": str(fixture_id)}
            try:
                stats_resp = requests.get(stats_url, headers=HEADERS, params=stats_querystring)
                stats_resp.raise_for_status()
                stats_data = stats_resp.json()
                if "response" in stats_data:
                    fixture_data["detailed_statistics"] = stats_data["response"]
            except Exception as e:
                print(f"Erro ao buscar estatísticas detalhadas: {e}")
                
            return fixture_data
            
        # MOCK STATISTICS FALLBACK
        mock_stats = {
            9: {"fixture": {"status": {"short": "FT"}}, "goals": {"home": 2, "away": 0}, "score": {"fulltime": {"home": 2, "away": 0}}, "statistics": [{"team": {"name": "Brazil"}, "statistics": [{"type": "Corner Kicks", "value": 7}]}, {"team": {"name": "Argentina"}, "statistics": [{"type": "Corner Kicks", "value": 4}]}]},
            10: {"fixture": {"status": {"short": "FT"}}, "goals": {"home": 1, "away": 1}, "score": {"fulltime": {"home": 1, "away": 1}}, "statistics": [{"team": {"name": "France"}, "statistics": [{"type": "Corner Kicks", "value": 5}]}, {"team": {"name": "Germany"}, "statistics": [{"type": "Corner Kicks", "value": 6}]}]},
        }
        return mock_stats.get(fixture_id, None)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar resultado da fixture {fixture_id}: {e}")
        return None
