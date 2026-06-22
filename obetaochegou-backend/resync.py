from app.core.database import SessionLocal
from app.models.match import Match
import requests

db = SessionLocal()
try:
    # Remove all matches
    db.query(Match).delete()
    db.commit()
    print("Database cleared.")
    
    # Resync
    response = requests.post("http://localhost:8000/api/v1/matches/sync")
    print("Sync response:", response.json())
except Exception as e:
    print("Error:", e)
finally:
    db.close()
