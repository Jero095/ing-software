from api_conect import get_owned_games
from api_conect import get_steamid64_from_vanity
from Metacritic import buscar_metacritic
import time

API_KEY = '4015C2DD9E04E39D3DA0CC9DAD264D4E'
VANITY_URL = input("ingresa tu nombre de usuario : ")


steamid64 = get_steamid64_from_vanity(API_KEY, VANITY_URL)
print("SteamID64:", steamid64)


juegos = get_owned_games(API_KEY, steamid64)
for i, juego in enumerate(juegos, 1):
    print(f"{i}. {juego}")


for juego in juegos:
    score = buscar_metacritic(juego)
    print(f"{juego}: {score}")
    time.sleep(2)