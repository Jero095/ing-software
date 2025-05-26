def sort_games_by_playtime(games, top_n = 10):
#devuelve el top de juegos por hora
    if not games:
        return []
    
    filtered_games = [game for game in games if game['playtime_hours'] > 0]
    
    # Ordenar la lista por 'playtime_hours' de forma descendente
    sorted_games = sorted(games, key=lambda x: x['playtime_hours'], reverse=True)
    return sorted_games[:top_n]