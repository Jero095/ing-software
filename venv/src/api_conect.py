import requests

API_KEY = '4015C2DD9E04E39D3DA0CC9DAD264D4E'
STEAM_ID = '76561198815929818'

VANITY_URL = input("ingresa tu nombre de usuario : ")

def get_steamid64_from_vanity(api_key, vanity_url):
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {
        'key':API_KEY,
        'vanityurl': VANITY_URL
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error en la solicitud:", response.status_code)
        return []

    data = response.json()
    if data['response']['success'] == 1:
        return data['response']['steamid']
    else:
        print("No se pudo resolver el SteamID.")
        return None



def get_owned_games(api_key, steam_id):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': api_key,
        'steamid': steam_id,
        'include_appinfo': 1,  # para traer nombre de los juegos
        'format': 'json'
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Error en la solicitud:", response.status_code)
        return []

    data = response.json()
    juegos = data['response'].get('games', [])
    
    # Extraer solo los nombres de los juegos
    nombres = [juego['name'] for juego in juegos]
    return nombres


steamid64 = get_steamid64_from_vanity(API_KEY, VANITY_URL)
print("SteamID64:", steamid64)


juegos = get_owned_games(API_KEY, STEAM_ID)
for i, juego in enumerate(juegos, 1):
    print(f"{i}. {juego}")

