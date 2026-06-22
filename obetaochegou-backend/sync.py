import requests

try:
    response = requests.post("http://localhost:8000/api/v1/matches/sync")
    print(response.json())
except Exception as e:
    print("Error:", e)
