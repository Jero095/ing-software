import requests
from bs4 import BeautifulSoup
import re
import time

def buscar_metacritic(game_name):
    """
    Busca el Metascore de un juego en Metacritic, probando múltiples plataformas y búsqueda general.
    
    Args:
        game_name (str): Nombre del juego.
        
    Returns:
        int or None: El Metascore como entero, o None si no se encuentra.
    """
    # Formatear el nombre del juego para la URL
    nombre_url = re.sub(r'[^a-zA-Z0-9\s]', '', game_name.lower()).replace(' ', '-')
    
    # Lista de plataformas a probar
    platforms = ['pc', 'playstation-4', 'xbox-one', 'nintendo-switch']
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for platform in platforms:
        try:
            # Probar la URL directa del juego
            url = f"https://www.metacritic.com/game/{platform}/{nombre_url}"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"No se pudo acceder a {url}: Código {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar el Metascore usando la clase 'metascore_w'
            score_element = soup.find('span', class_='metascore_w')
            if score_element and score_element.text.isdigit():
                print(f"Encontrado Metascore para {game_name} en {platform}: {score_element.text}")
                return int(score_element.text)
            
            # Si no se encuentra en la URL directa, intentar con la página de búsqueda
            search_url = f"https://www.metacritic.com/search/game/{nombre_url}/results"
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"No se pudo acceder a la búsqueda {search_url}: Código {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find('a', class_='product_title')
            if result:
                # Obtener la URL del juego desde los resultados de búsqueda
                game_url = f"https://www.metacritic.com{result['href']}"
                response = requests.get(game_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    score_element = soup.find('span', class_='metascore_w')
                    if score_element and score_element.text.isdigit():
                        print(f"Encontrado Metascore para {game_name} vía búsqueda: {score_element.text}")
                        return int(score_element.text)
                        
        except Exception as e:
            print(f"Error al buscar en Metacritic para {game_name} en {platform}: {e}")
            continue
            
        # Pausa para evitar bloqueos
        time.sleep(2)
    
    print(f"No se encontró Metascore para {game_name} en ninguna plataforma.")
    return None