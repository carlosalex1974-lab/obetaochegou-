from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from app.core.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    api_fixture_id = Column(Integer, unique=True, index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, index=True)
    
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)
    
    raw_data = Column(JSON, nullable=True)
    predictions_data = Column(JSON, nullable=True)
    
    is_finished = Column(Boolean, default=False)
    match_stats = Column(JSON, nullable=True)
    validation_results = Column(JSON, nullable=True)

