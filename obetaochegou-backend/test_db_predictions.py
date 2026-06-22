import os
import sys
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.match import Match
from app.services.predictions import generate_predictions

class MatchMock:
    pass

db = SessionLocal()
db_matches = db.query(Match).filter(Match.date >= datetime.now().date()).all()

match_objects = []
for m in db_matches:
    mock = MatchMock()
    mock.id = m.id
    mock.home_team = m.home_team
    mock.away_team = m.away_team
    mock.league = m.raw_data.get("league", {}).get("name", "Desconhecida") if m.raw_data else "Desconhecida"
    mock.match_time = m.date
    mock.status = m.status
    mock.predictions_data = m.predictions_data
    match_objects.append(mock)

print("Calling generate_predictions...")
predictions = generate_predictions(match_objects)
print("Result of first match rationale:")
print(predictions[0]["predictions"]["rationale"])
