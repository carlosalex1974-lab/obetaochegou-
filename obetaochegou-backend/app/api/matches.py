from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.match import Match
from app.services.api_football import get_todays_matches, get_fixture_predictions, get_fixture_statistics
from app.services.predictions import generate_predictions
from app.services.ai_bot import validate_predictions

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/today")
def read_todays_matches(db: Session = Depends(get_db)):
    """Retorna as partidas do dia, buscando da API-Football"""
    data = get_todays_matches()
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

@router.post("/sync")
def sync_todays_matches(db: Session = Depends(get_db)):
    """Busca as partidas do dia na API-Football e salva no banco de dados"""
    data = get_todays_matches()
    
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
        
    matches_data = data.get("matches", [])
    synced_count = 0
    
    for match_data in matches_data:
        fixture_id = match_data["fixture"]["id"]
        
        # Verifica se já existe
        existing_match = db.query(Match).filter(Match.api_fixture_id == fixture_id).first()
        if existing_match:
            continue
            
        # Parse da data
        try:
            match_date = datetime.fromisoformat(match_data["fixture"]["date"].replace("Z", "+00:00"))
        except ValueError:
            match_date = datetime.now()
            
        # Busca as estatísticas reais para a partida
        real_predictions = get_fixture_predictions(fixture_id)
        
        # Gera o texto mágico do OBetão via Gemini!
        if real_predictions:
            from app.services.ai_bot import generate_ai_rationale
            ai_text = generate_ai_rationale(
                match_data["teams"]["home"]["name"], 
                match_data["teams"]["away"]["name"], 
                real_predictions
            )
            if ai_text:
                real_predictions["obetao_rationale"] = ai_text

        new_match = Match(
            api_fixture_id=fixture_id,
            date=match_date,
            status=match_data["fixture"]["status"]["short"],
            home_team=match_data["teams"]["home"]["name"],
            away_team=match_data["teams"]["away"]["name"],
            home_goals=match_data["goals"]["home"],
            away_goals=match_data["goals"]["away"],
            raw_data=match_data,
            predictions_data=real_predictions
        )
        db.add(new_match)
        synced_count += 1
        
    db.commit()
    
    return {"message": f"{synced_count} partidas sincronizadas com sucesso!"}

@router.get("/predictions")
def get_match_predictions(db: Session = Depends(get_db)):
    """Retorna as predições para as partidas do dia, a partir do banco de dados"""
    # Usaremos um "mock" struct baseado no model Match, só com os campos que o predictions.py espera
    class MatchMock:
        pass
        
    db_matches = db.query(Match).order_by(Match.date.desc()).limit(20).all()
    
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
        
        # Novos campos para validação
        mock.is_finished = m.is_finished
        mock.home_goals = m.home_goals
        mock.away_goals = m.away_goals
        mock.validation_results = m.validation_results
        
        match_objects.append(mock)
        
    predictions = generate_predictions(match_objects)
    return {"predictions": predictions}

@router.post("/validate")
def validate_finished_matches(db: Session = Depends(get_db)):
    """Busca os resultados dos jogos terminados e valida os palpites com a IA"""
    db_matches = db.query(Match).filter(Match.is_finished == False).all()
    validated_count = 0
    
    for match in db_matches:
        # Puxa o status atualizado do jogo na API
        stats = get_fixture_statistics(match.api_fixture_id)
        if not stats:
            continue
            
        status = stats.get("fixture", {}).get("status", {}).get("short")
        if status in ["FT", "AET", "PEN"]:
            # Jogo acabou!
            match.is_finished = True
            match.home_goals = stats.get("goals", {}).get("home")
            match.away_goals = stats.get("goals", {}).get("away")
            match.match_stats = stats
            
            # Hora de usar a IA para validar os palpites!
            rationale = match.predictions_data.get("obetao_rationale", "") if match.predictions_data else ""
            if rationale:
                validation_json = validate_predictions(rationale, stats)
                match.validation_results = validation_json
                
            validated_count += 1
            db.commit() # salva cada jogo validado
            
    return {"message": f"{validated_count} partidas validadas e auditadas com sucesso!"}

@router.post("/revalidate")
def revalidate_error_matches(db: Session = Depends(get_db)):
    """Busca jogos que terminaram mas a validação deu erro e tenta novamente"""
    db_matches = db.query(Match).filter(Match.is_finished == True).all()
    revalidated_count = 0
    errors = []
    
    for match in db_matches:
        if match.validation_results:
            rationale = match.predictions_data.get("obetao_rationale", "") if match.predictions_data else ""
            stats = match.match_stats
            if rationale and stats:
                validation_json = validate_predictions(rationale, stats)
                match.validation_results = validation_json
                if validation_json.get("status") != "error":
                    revalidated_count += 1
                else:
                    errors.append(validation_json.get("message"))
                db.commit()
                
    return {"message": f"{revalidated_count} partidas revalidadas com sucesso.", "errors": errors}

@router.post("/wipe")
def wipe_db(db: Session = Depends(get_db)):
    db.query(Match).delete()
    db.commit()
    return {"message": "Tabela apagada!"}
