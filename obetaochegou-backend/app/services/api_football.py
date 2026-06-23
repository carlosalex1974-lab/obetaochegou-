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
            # Fallback: se não tiver Copa, tenta ligas principais (Premier League 39, La Liga 140, Serie A 135, Brasileirao 71, Libertadores 13)
            major_leagues = [39, 140, 135, 71, 13]
            top_matches = [m for m in matches if m.get("league", {}).get("id") in major_leagues]
            
            final_matches = top_matches if top_matches else matches
            
        # Retorna apenas as primeiras 10 partidas focadas
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
        return None
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
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar resultado da fixture {fixture_id}: {e}")
        return None
