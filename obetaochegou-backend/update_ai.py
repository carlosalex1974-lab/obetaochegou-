import os
import sys

# Adiciona o diretório atual ao path para poder importar o app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.match import Match
from app.services.ai_bot import generate_ai_rationale

db = SessionLocal()

matches = db.query(Match).all()
updated_count = 0

for match in matches:
    if match.predictions_data:
        print(f"Gerando IA para: {match.home_team} vs {match.away_team}...")
        
        ai_text = generate_ai_rationale(match.home_team, match.away_team, match.predictions_data)
        
        if ai_text:
            # SQLAlchemy mutations tracking requires re-assignment or flag_modified for JSON
            pred_data = match.predictions_data.copy()
            pred_data["obetao_rationale"] = ai_text
            match.predictions_data = pred_data
            
            db.add(match)
            updated_count += 1
            print("Gerado com sucesso!")
        else:
            print("Falhou ou vazio.")

if updated_count > 0:
    db.commit()
    print(f"Banco atualizado com {updated_count} novas análises de IA!")
else:
    print("Nenhuma partida precisava de atualização.")

db.close()
