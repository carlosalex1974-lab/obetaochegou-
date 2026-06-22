from app.core.database import SessionLocal
from app.models.match import Match

db = SessionLocal()
matches = db.query(Match).all()
for m in matches:
    print(m.raw_data)
    break
db.close()
