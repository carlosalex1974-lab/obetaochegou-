def generate_predictions(matches: list) -> list:
    """
    Gera predições para uma lista de partidas usando dados da API-Football.
    """
    predicted_matches = []
    
    for match in matches:
        if hasattr(match, "predictions_data") and match.predictions_data and "predictions" in match.predictions_data:
            preds = match.predictions_data["predictions"]
            home_win_prob = preds.get("percent", {}).get("home", "33%")
            draw_prob = preds.get("percent", {}).get("draw", "33%")
            away_win_prob = preds.get("percent", {}).get("away", "33%")
            recommended_bet = preds.get("advice", "Sem recomendação")
            
            # Simple heuristic for over 2.5: check if both teams tend to score
            goals_home = match.predictions_data.get("teams", {}).get("home", {}).get("last_5", {}).get("goals", {}).get("for", {}).get("average", "1.0")
            goals_away = match.predictions_data.get("teams", {}).get("away", {}).get("last_5", {}).get("goals", {}).get("for", {}).get("average", "1.0")
            try:
                over_2_5 = (float(goals_home) + float(goals_away)) > 2.5
            except (ValueError, TypeError):
                over_2_5 = False
                
            rationale_ai = match.predictions_data.get("obetao_rationale")
            print(f"DEBUG: obetao_rationale present? {'yes' if rationale_ai else 'no'}")
            if rationale_ai:
                rationale = rationale_ai
            else:
                rationale = (f"A recomendação da inteligência para essa partida é: {recommended_bet}. "
                             f"As probabilidades baseadas no histórico recente indicam {home_win_prob} de chance "
                             f"para o {match.home_team}, {draw_prob} para empate e {away_win_prob} para o {match.away_team}.")
        else:
            home_win_prob = "N/A"
            draw_prob = "N/A"
            away_win_prob = "N/A"
            recommended_bet = "Indisponível"
            over_2_5 = False
            rationale = "Não há estatísticas e predições suficientes fornecidas pela API para esta partida. Tente ressincronizar os jogos."

        match_data = {
            "id": match.id,
            "home_team": match.home_team,
            "away_team": match.away_team,
            "league": match.league,
            "match_time": match.match_time.isoformat() if match.match_time else None,
            "status": match.status,
            "predictions": {
                "home_win_prob": home_win_prob,
                "draw_prob": draw_prob,
                "away_win_prob": away_win_prob,
                "recommended_bet": recommended_bet,
                "over_2_5_goals": over_2_5,
                "rationale": rationale
            },
            "validation": {
                "is_finished": getattr(match, "is_finished", False),
                "home_goals": getattr(match, "home_goals", None),
                "away_goals": getattr(match, "away_goals", None),
                "results": getattr(match, "validation_results", None)
            }
        }
        predicted_matches.append(match_data)
        
    return predicted_matches
