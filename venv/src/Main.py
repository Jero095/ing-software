from api_conect import get_owned_games, get_steamid64_from_vanity
from Metacritic import buscar_metacritic
from game_sorter import sort_games_by_playtime
import time

API_KEY = '4015C2DD9E04E39D3DA0CC9DAD264D4E'
#STEAM_ID = '76561198815929818'

# Solicitar nombre de usuario
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

# Obtener puntajes de Metacritic
print("\nPuntajes de Metacritic:")
for juego in top_juegos:
    score = buscar_metacritic(juego['name'])
    print(f"{juego['name']}: {score if score is not None else 'No disponible'} (Metascore)")
    time.sleep(3)