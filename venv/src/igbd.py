import requests
client_id = 'wknux0efm22z5j9pgp19bc88mfxlxt'
access_token = '5wa4qj0u9bm4rf4gm9qp55avw7qls5'

def get_igdb_access_token(client_id, client_secret):
    """
    Obtiene un access_token para la API de IGDB usando el flujo de client credentials.
    
    Args:
        client_id (str): Client ID de la API de IGDB.
        client_secret (str): Client Secret de la API de IGDB.
        
    Returns:
        str or None: El access_token, o None si falla la solicitud.
    """
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
        if access_token:
            print(f"Access token obtenido: {access_token[:10]}... (ocultado por seguridad)")
            return access_token
        else:
            print("No se encontró access_token en la respuesta.")
            return None
            
    except Exception as e:
        print(f"Error al obtener access_token: {e}")
        return None

def buscar_igdb(game_name,client_id, access_token):
    """
    Busca el puntaje promedio de un juego en IGDB usando su API.
    
    Args:
        game_name (str): Nombre del juego.
        client_id (str): Client ID de la API de IGDB.
        access_token (str): Access Token de la API de IGDB.
        
    Returns:
        int or None: Puntaje promedio (0-100), o None si no se encuentra.
    """
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'text/plain'
    }
    
    # Buscar el juego por nombre
    search_query = f'search "{game_name}"; fields name,rating; where rating > 0;'
    try:
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=search_query, timeout=10)
        if response.status_code != 200:
            print(f"No se pudo acceder a IGDB para {game_name}: Código {response.status_code}")
            return None
        
        games = response.json()
        if not games:
            print(f"No se encontró {game_name} en IGDB.")
            return None
        
        # Tomar el primer resultado con rating
        for game in games:
            if 'rating' in game:
                rating = round(game['rating'])
                print(f"Encontrado puntaje para {game_name}: {rating}")
                return rating
        
        print(f"No se encontró puntaje para {game_name} en IGDB.")
        return None
        
    except Exception as e:
        print(f"Error al buscar en IGDB para {game_name}: {e}")
        return None