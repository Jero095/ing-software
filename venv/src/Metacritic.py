import requests
from bs4 import BeautifulSoup
import time

# scraper_metacritic.py

import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

def buscar_metacritic(game_name):
    nombre_url = game_name.lower().replace(" ", "-")
    url = f"https://www.metacritic.com/game/pc/{nombre_url}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        score_tag = soup.find("span", itemprop="ratingValue")
        if not score_tag:
            return None

        return int(score_tag.text.strip())

    except Exception as e:
        print(f"Error con {game_name}: {e}")
        return None
