import requests
import json
import time
import os
from datetime import datetime, timedelta

def get_igdb_access_token(client_id, client_secret, token_file="igdb_token.json"):
    """
    Obtiene un access_token para la API de IGDB, reutilizando uno válido si existe.
    
    Args:
        client_id (str): Client ID de la API de IGDB.
        client_secret (str): Client Secret de la API de IGDB.
        token_file (str): Archivo donde se almacena el token.
        
    Returns:
        str or None: El access_token, o None si falla la solicitud.
    """
    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            access_token = token_data.get('access_token')
            expires_at = token_data.get('expires_at')
            if access_token and expires_at:
                if datetime.fromtimestamp(expires_at) > datetime.now():
                    print(f"Reutilizando access_token existente: {access_token[:10]}...")
                    return access_token
                else:
                    print("El access_token almacenado ha expirado.")
        except Exception as e:
            print(f"Error al leer el token almacenado: {e}")

    url = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"Error al obtener access_token: Código {response.status_code}")
            return None
        
        data = response.json()
        access_token = data.get('access_token')
        expires_in = data.get('expires_in', 0)
        if access_token:
            expires_at = int(time.time()) + expires_in - 300
            token_data = {
                'access_token': access_token,
                'expires_at': expires_at
            }
            with open(token_file, 'w') as f:
                json.dump(token_data, f, indent=4)
            print(f"Nuevo access_token obtenido y guardado: {access_token[:10]}...")
            return access_token
        else:
            print("No se encontró access_token en la respuesta.")
            return None
            
    except Exception as e:
        print(f"Error al obtener access_token: {e}")
        return None

def get_genre_names(genre_ids, client_id, access_token):
    """
    Obtiene los nombres de géneros desde el endpoint /genres.
    
    Args:
        genre_ids (list): Lista de IDs de géneros.
        client_id (str): Client ID de la API de IGDB.
        access_token (str): Access Token de la API de IGDB.
        
    Returns:
        list: Lista de nombres de géneros.
    """
    if not genre_ids:
        return []
    
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/plain'
    }
    
    genre_query = f'fields name; where id = ({",".join(map(str, genre_ids))});'
    try:
        response = requests.post('https://api.igdb.com/v4/genres', headers=headers, data=genre_query, timeout=10)
        if response.status_code != 200:
            print(f"No se pudieron obtener nombres de géneros: Código {response.status_code}, Respuesta: {response.text}")
            return []
        
        genres = response.json()
        return [genre['name'] for genre in genres]
    except Exception as e:
        print(f"Error al obtener nombres de géneros: {e}")
        return []

def get_keyword_names(keyword_ids, client_id, access_token):
    """
    Obtiene los nombres de keywords desde el endpoint /keywords.
    
    Args:
        keyword_ids (list): Lista de IDs de keywords.
        client_id (str): Client ID de la API de IGDB.
        access_token (str): Access Token de la API de IGDB.
        
    Returns:
        list: Lista de nombres de keywords.
    """
    if not keyword_ids:
        return []
    
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/plain'
    }
    
    keyword_query = f'fields name; where id = ({",".join(map(str, keyword_ids))});'
    try:
        response = requests.post('https://api.igdb.com/v4/keywords', headers=headers, data=keyword_query, timeout=10)
        if response.status_code != 200:
            print(f"No se pudieron obtener nombres de keywords: Código {response.status_code}, Respuesta: {response.text}")
            return []
        
        keywords = response.json()
        return [keyword['name'] for keyword in keywords]
    except Exception as e:
        print(f"Error al obtener nombres de keywords: {e}")
        return []

def get_game_details(game_name, client_id, access_token):
    """
    Obtiene detalles de un juego en IGDB, incluyendo puntaje, géneros, keywords y juegos similares.
    
    Args:
        game_name (str): Nombre del juego.
        client_id (str): Client ID de la API de IGDB.
        access_token (str): Access Token de la API de IGDB.
        
    Returns:
        dict or None: Diccionario con nombre, puntaje, géneros, keywords y juegos similares, o None si no se encuentra.
    """
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/plain'
    }
    
    # Consulta a /games: obtener ID, rating, genres (IDs), keywords (IDs), y similar_games
    search_query = f'search "{game_name}"; fields id,name,rating,genres,keywords,similar_games.name,similar_games.rating; where rating > 0; limit 1;'
    try:
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=search_query, timeout=10)
        if response.status_code != 200:
            print(f"No se pudo acceder a IGDB para {game_name}: Código {response.status_code}, Respuesta: {response.text}")
            return None
        
        games = response.json()
        if not games:
            print(f"No se encontró {game_name} en IGDB.")
            return None
        
        game = games[0]
        genre_ids = game.get('genres', [])
        keyword_ids = game.get('keywords', [])
        
        # Obtener nombres de géneros y keywords
        genres = get_genre_names(genre_ids, client_id, access_token)
        keywords = get_keyword_names(keyword_ids, client_id, access_token)
        
        result = {
            'name': game.get('name', game_name),
            'rating': round(game.get('rating', 0)) if game.get('rating') else None,
            'genres': genres,
            'keywords': keywords,
            'similar_games': [
                {
                    'name': sg['name'],
                    'rating': round(sg.get('rating', 0)) if sg.get('rating') else None
                }
                for sg in game.get('similar_games', [])
            ]
        }
        
        print(f"Detalles completos para {game_name}: {result}")
        return result
        
    except Exception as e:
        print(f"Error al buscar en IGDB para {game_name}: {e}")
        return None