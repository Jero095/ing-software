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
