import urllib.request
import json
try:
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/matches/predictions")
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        data = json.loads(response.read().decode())
        print("Data keys:", data.keys())
        if "predictions" in data:
            print("Number of predictions:", len(data["predictions"]))
except Exception as e:
    print("Erro ao acessar API:", e)
