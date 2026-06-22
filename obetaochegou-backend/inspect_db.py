import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.core.database import SessionLocal
from app.models.match import Match

db = SessionLocal()
matches = db.query(Match).filter(Match.date >= datetime.now().date()).all()

for match in matches:
    print(f"Match: {match.home_team} vs {match.away_team}")
    if match.predictions_data and "obetao_rationale" in match.predictions_data:
        print(f"Rationale:\n{match.predictions_data['obetao_rationale']}\n")
    else:
        print("No rationale found.\n")
