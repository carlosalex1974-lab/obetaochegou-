import urllib.request
import json
try:
    req = urllib.request.Request("http://127.0.0.1:8000/api/v1/matches/predictions")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if "predictions" in data and len(data["predictions"]) > 0:
            print("First match rationale from API:")
            print(data["predictions"][0]["predictions"]["rationale"])
        else:
            print("No predictions returned by API.")
except Exception as e:
    print("Erro:", e)
