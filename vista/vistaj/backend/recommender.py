from collections import Counter
import random

def generate_recommendations(top_games, game_details, max_recommendations=5):
    """
    Genera recomendaciones basadas en los juegos más jugados y sus detalles.
    
    Args:
        top_games (list): Lista de juegos más jugados (con 'name', 'playtime_hours', 'appid').
        game_details (list): Lista de detalles de IGDB (con 'name', 'genres', 'keywords', 'similar_games').
        max_recommendations (int): Número máximo de recomendaciones.
        
    Returns:
        list: Lista de juegos recomendados con 'name', 'rating', 'description'.
    """
    if not top_games or not game_details:
        return []

    # Extraer géneros y keywords de los juegos del usuario para el algoritmo
    all_genres = []
    all_keywords = []
    for details in game_details:
        if details:
            all_genres.extend(details.get('genres', []))
            all_keywords.extend(details.get('keywords', []))

    # Contar frecuencias
    genre_counts = Counter(all_genres)
    keyword_counts = Counter(all_keywords)

    # Obtener géneros y keywords más comunes
    top_genres = [genre for genre, _ in genre_counts.most_common(3)]
    top_keywords = [keyword for keyword, _ in keyword_counts.most_common(5)]

    # Recolectar juegos similares
    similar_games = []
    for details in game_details:
        if details and 'similar_games' in details:
            for sim_game in details['similar_games']:
                # Usar géneros y keywords del juego principal para el puntaje
                score = (len(set(details.get('genres', [])) & set(top_genres)) * 2 +
                         len(set(details.get('keywords', [])) & set(top_keywords)))
                similar_games.append({
                    'name': sim_game['name'],
                    'rating': sim_game['rating'],
                    'description': sim_game['description'],
                    'score': score
                })

    # Ordenar por puntaje y evitar duplicados
    seen = set()
    recommendations = []
    for game in sorted(similar_games, key=lambda x: x['score'], reverse=True):
        if game['name'] not in seen and game['name'] not in [g['name'] for g in top_games]:
            recommendations.append({
                'name': game['name'],
                'rating': game['rating'],
                'description': game['description']
            })
            seen.add(game['name'])
        if len(recommendations) >= max_recommendations:
            break

    # Si no hay suficientes recomendaciones, añadir algunas aleatorias
    while len(recommendations) < max_recommendations and similar_games:
        game = random.choice(similar_games)
        if game['name'] not in seen and game['name'] not in [g['name'] for g in top_games]:
            recommendations.append({
                'name': game['name'],
                'rating': game['rating'],
                'description': game['description']
            })
            seen.add(game['name'])
        if len(recommendations) >= max_recommendations:
            break

    return recommendations