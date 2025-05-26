from api_conect import get_owned_games, get_steamid64_from_vanity
from igbd import get_igdb_access_token, get_game_details
from game_sorter import sort_games_by_playtime
from recommender import generate_recommendations
import time

API_KEY = '4015C2DD9E04E39D3DA0CC9DAD264D4E'
#STEAM_ID = '76561198815929818'
IGDB_CLIENT_ID = 'wknux0efm22z5j9pgp19bc88mfxlxt'
IGDB_CLIENT_SECRET = '5wa4qj0u9bm4rf4gm9qp55avw7qls5'

# Solicitar nombre de usuario

access_token = get_igdb_access_token(IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
if not access_token:
    print("No se pudo obtener el access_token de IGDB. Finalizando.")
    exit()
VANITY_URL = input("Ingresa tu nombre de usuario de Steam (o presiona Enter para ingresar SteamID64 directamente): ").strip()

# Obtener SteamID64
steamid64 = None
if VANITY_URL:
    steamid64 = get_steamid64_from_vanity(API_KEY, VANITY_URL)
    if not steamid64:
        print("No se pudo resolver el nombre de usuario. Por favor, verifica que sea correcto.")
        print("Puedes encontrar tu nombre de usuario en la URL de tu perfil de Steam (steamcommunity.com/id/<tu_nombre>).")
        print("Alternativamente, ingresa tu SteamID64 (un número como 7656119xxxxxxxxxxx).")
        steamid64 = input("Ingresa tu SteamID64: ").strip()
else:
    steamid64 = input("Ingresa tu SteamID64: ").strip()

# Validar SteamID64
if not steamid64 or not steamid64.isdigit() or len(steamid64) != 17:
    print("SteamID64 inválido. Debe ser un número de 17 dígitos.")
    exit()

print("SteamID64:", steamid64)

# Obtener juegos y horas jugadas
juegos = get_owned_games(API_KEY, steamid64)
if not juegos:
    print("No se encontraron juegos en la biblioteca. Verifica que el perfil sea público y que la API key sea válida.")
    exit()

# Mostrar lista de juegos con horas jugadas
#print("\nJuegos en tu biblioteca:")
#for i, juego in enumerate(juegos, 1):
   # print(f"{i}. {juego['name']} - {juego['playtime_hours']} horas")

top_juegos = sort_games_by_playtime(juegos, top_n=10)
print("\nTop de juegos por horas jugadas:")
if top_juegos:
    for i, juego in enumerate(top_juegos, 1):
        print(f"{i}. {juego['name']} - {juego['playtime_hours']} horas")
else:
    print("No hay juegos con horas jugadas.")

print("\nPuntajes y detalles de IGDB para el top 10:")
print("\nDetalles de IGDB para el top 10:")
game_details = []
for juego in top_juegos:
    details = get_game_details(juego['name'], IGDB_CLIENT_ID, access_token)
    if details:
        game_details.append(details)
        genres_str = ', '.join(details['genres']) if details['genres'] else 'No disponible'
        keywords_str = ', '.join(details['keywords'][:5]) if details['keywords'] else 'No disponible'
        print(f"{juego['name']}: {details['rating'] if details.get('rating') else juego.get('review_score', 'No disponible')}% (Puntaje {'IGDB' if details.get('rating') else 'Steam'}), Géneros: {genres_str}, Keywords: {keywords_str}")
    else:
        print(f"{juego['name']}: {juego.get('review_score', 'No disponible')}% (Puntaje Steam), Géneros: No disponible, Keywords: No disponible")
    time.sleep(2)

# Generar recomendaciones

recommendations = generate_recommendations(top_juegos, game_details)
print("\nJuegos recomendados para ti:")
if recommendations:
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['name']} - {rec['rating'] if rec.get('rating') else 'No disponible'}")
else:
    print("No se pudieron generar recomendaciones.")