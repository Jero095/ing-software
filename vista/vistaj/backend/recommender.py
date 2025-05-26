def generate_recommendations(top_games, game_details):
    """
    Genera recomendaciones de juegos basadas en los juegos más jugados y sus detalles.
    
    Args:
        top_games (list): Lista de diccionarios con 'name', 'playtime_hours', 'review_score'.
        game_details (list): Lista de diccionarios con detalles de IGDB (genres, keywords, similar_games).
        
    Returns:
        list: Lista de hasta 5 juegos recomendados (nombre y puntaje).
    """
    if not top_games or not game_details:
        print("No hay juegos o detalles para generar recomendaciones.")
        return []

    # Calcular el peso de cada juego según las horas jugadas
    total_hours = sum(game.get('playtime_hours', 0) for game in top_games)
    game_weights = {
        game['name']: game.get('playtime_hours', 0) / total_hours if total_hours > 0 else 1/len(top_games)
        for game in top_games
    }

    # Recolectar géneros y keywords preferidos
    preferred_genres = {}
    preferred_keywords = {}
    similar_games_pool = []
    
    for details, top_game in zip(game_details, top_games):
        if not details:
            continue
        game_name = details['name']
        weight = game_weights.get(game_name, 0)
        
        # Contar géneros
        for genre in details.get('genres', []):
            preferred_genres[genre] = preferred_genres.get(genre, 0) + weight
        
        # Contar keywords
        for keyword in details.get('keywords', []):
            preferred_keywords[keyword] = preferred_keywords.get(keyword, 0) + weight
        
        # Añadir juegos similares al pool
        for similar_game in details.get('similar_games', []):
            rating = similar_game.get('rating', top_game.get('review_score', 0))
            similar_games_pool.append({
                'name': similar_game['name'],
                'rating': rating,
                'genres': details.get('genres', []),
                'keywords': details.get('keywords', [])
            })

    if not similar_games_pool:
        print("No se encontraron juegos similares para generar recomendaciones.")
        return []

    # Eliminar juegos que ya están en la biblioteca del usuario
    owned_games = set(game['name'] for game in top_games)
    similar_games_pool = [game for game in similar_games_pool if game['name'] not in owned_games]

    # Calcular puntaje para cada juego candidato
    recommendations = []
    for candidate in similar_games_pool:
        score = 0
        # Puntuación por géneros compartidos
        for genre in candidate.get('genres', []):
            score += preferred_genres.get(genre, 0)
        # Puntuación por keywords compartidos
        for keyword in candidate.get('keywords', []):
            score += preferred_keywords.get(keyword, 0) * 0.5  # Keywords tienen menos peso
        # Ajustar por rating
        if candidate['rating']:
            score *= (candidate['rating'] / 100)
        else:
            score *= 0.5  # Penalizar juegos sin rating
        
        recommendations.append({
            'name': candidate['name'],
            'rating': candidate['rating'],
            'score': score
        })

    # Ordenar por puntaje
    recommendations = sorted(recommendations, key=lambda x: x['score'], reverse=True)

    # Relajar filtro si no hay recomendaciones
    if not recommendations:
        print("No se encontraron recomendaciones. Mostrando sin filtro.")
        recommendations = [
            {'name': rec['name'], 'rating': rec['rating']}
            for rec in recommendations[:5]
        ]
    else:
        recommendations = [
            {'name': rec['name'], 'rating': rec['rating']}
            for rec in recommendations[:5] if rec['score'] > 0
        ]

    if not recommendations:
        print("No se generaron recomendaciones debido a datos insuficientes.")
    
    return recommendations