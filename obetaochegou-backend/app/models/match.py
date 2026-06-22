from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.core.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    api_fixture_id = Column(Integer, unique=True, index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, index=True)
    
    # Podemos salvar o JSON completo da resposta por conveniência ou normalizar os campos.
    # Por enquanto, campos importantes ficam normalizados.
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)
    
    # Dados brutos da API caso precise de algo que não foi normalizado
    raw_data = Column(JSON, nullable=True)
    
    # Estatísticas de predição (percentuais, h2h, form) recebidas da API
    predictions_data = Column(JSON, nullable=True)
