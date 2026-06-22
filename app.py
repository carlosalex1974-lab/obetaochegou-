import requests
import pandas as pd

API_KEY = "SUA_CHAVE_API"
BASE_URL = "https://v3.football.api-sports.io/"

def fetch_match_data():
    url = BASE_URL + "fixtures"
    headers = {"x-apisports-key": API_KEY}
    params = {"date": "2025-08-08"}  # Data de hoje
    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    matches = []
    for fixture in data["response"]:
        stats_url = BASE_URL + "fixtures/statistics"
        stats_params = {"fixture": fixture["fixture"]["id"]}
        stats_res = requests.get(stats_url, headers=headers, params=stats_params).json()

        corners = next((s["statistics"][0]["value"] for s in stats_res["response"] if s["team"]["id"] == fixture["teams"]["home"]["id"]), 0)
        shots = next((s["statistics"][2]["value"] for s in stats_res["response"] if s["team"]["id"] == fixture["teams"]["home"]["id"]), 0)

        matches.append({
            "home": fixture["teams"]["home"]["name"],
            "away": fixture["teams"]["away"]["name"],
            "corners_for_avg": corners,
            "shots_for_avg": shots,
            "plays_by_sides": 1,  # exemplo fixo
            "match_context": 1
        })

    return pd.DataFrame(matches)
