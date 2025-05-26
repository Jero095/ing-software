import requests

API_KEY = '4015C2DD9E04E39D3DA0CC9DAD264D4E'
#STEAM_ID = '76561198815929818'



def get_steamid64_from_vanity(api_key, vanity_url):
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {
        'key':API_KEY,
        'vanityurl': vanity_url.strip()
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error en la solicitud a ResolveVanityURL: {response.status_code}")
            return None

        data = response.json()
        if data['response']['success'] == 1:
            return data['response']['steamid']
        else:
            print(f"No se pudo resolver el SteamID para '{vanity_url}'. Mensaje: {data['response'].get('message', 'Sin mensaje')}")
            return None
    except Exception as e:
        print(f"Excepción al resolver SteamID para '{vanity_url}': {e}")
        return None


def get_owned_games(api_key, steam_id):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': 1,  # para traer nombre de los juegos
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error en la solicitud a GetOwnedGames: {response.status_code}")
            return []

        data = response.json()
        juegos = data['response'].get('games', [])
        
        # Extraer nombre y horas jugadas (convertidas de minutos a horas)
        juegos_info = [
            {
                'name': juego['name'],
                'playtime_hours': round(juego.get('playtime_forever', 0) / 60, 2)  # Convertir minutos a horas
            }
            for juego in juegos
        ]
        return juegos_info
    except Exception as e:
        print(f"Excepción al obtener juegos: {e}")
        return []
    
def get_steam_review_score(appid):
    """
    Obtiene el porcentaje de reseñas positivas para un juego desde la API de Steam.
    
    Args:
        appid (int): ID del juego en Steam.
        
    Returns:
        int or None: Porcentaje de reseñas positivas (0-100), o None si no hay datos.
    """
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"No se pudo obtener reseñas para appid {appid}: Código {response.status_code}")
            return None
        
        data = response.json()
        if data.get('success') == 1 and 'query_summary' in data:
            review_score = data['query_summary'].get('review_score', 0)
            total_positive = data['query_summary'].get('total_positive', 0)
            total_reviews = data['query_summary'].get('total_reviews', 0)
            if total_reviews > 0:
                percentage = round((total_positive / total_reviews) * 100)
                print(f"Puntaje de reseñas para appid {appid}: {percentage}% ({total_reviews} reseñas)")
                return percentage
        return None
    except Exception as e:
        print(f"Error al obtener reseñas para appid {appid}: {e}")
        return None
