from flask import Flask, request, jsonify
from flask_cors import CORS
from api_conect import get_owned_games, get_steamid64_from_vanity
from igbd import get_igdb_access_token, get_game_details
from game_sorter import sort_games_by_playtime
from recommender import generate_recommendations
import time

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "http://localhost:5173"}})

# Configuración
API_KEY = '4015C2DD9E04E39D3DA0CC9DAD264D4E'
IGDB_CLIENT_ID = 'wknux0efm22z5j9pgp19bc88mfxlxt'  # Reemplaza con tu Client ID de IGDB
IGDB_CLIENT_SECRET = '35umbc7k6bcxihq6sttrfttrvfily8'  # Reemplaza con tu Client Secret de IGDB

# Obtener access_token para IGDB
access_token = get_igdb_access_token(IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
if not access_token:
    print("No se pudo obtener el access_token de IGDB. Finalizando.")
    exit()

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()

        if not username:
            return jsonify({'error': 'Username or SteamID64 is required'}), 400

        # Obtener SteamID64
        steamid64 = None
        if username.isdigit() and len(username) == 17:
            steamid64 = username
        else:
            steamid64 = get_steamid64_from_vanity(API_KEY, username)
            if not steamid64:
                return jsonify({'error': 'Invalid username. Please check or use SteamID64'}), 400

        # Validar SteamID64
        if not steamid64 or not steamid64.isdigit() or len(steamid64) != 17:
            return jsonify({'error': 'Invalid SteamID64. Must be a 17-digit number'}), 400

        # Obtener juegos
        juegos = get_owned_games(API_KEY, steamid64)
        if not juegos:
            return jsonify({'error': 'No games found. Ensure your profile is public'}), 400

        # Obtener top 10
        top_juegos = sort_games_by_playtime(juegos, top_n=10)

        # Obtener detalles de IGDB
        game_details = []
        for juego in top_juegos:
            details = get_game_details(juego['name'], IGDB_CLIENT_ID, access_token)
            if details:
                game_details.append(details)
            time.sleep(2)  # Respetar límites de IGDB

        # Generar recomendaciones
        recommendations = generate_recommendations(top_juegos, game_details)

        # Formatear respuesta
        response = {
            'top_games': [
                {
                    'name': juego['name'],
                    'playtime_hours': juego['playtime_hours'],
                    'rating': details.get('rating') if details else juego.get('review_score', None),
                    'genres': details.get('genres', []) if details else [],
                    'keywords': details.get('keywords', [])[:5] if details else []
                }
                for juego, details in zip(top_juegos, game_details + [None] * (len(top_juegos) - len(game_details)))
            ],
            'recommendations': [
                {
                    'name': rec['name'],
                    'rating': rec['rating']
                }
                for rec in recommendations
            ]
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error en /recommend: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)