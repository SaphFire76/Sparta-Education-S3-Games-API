import os
import requests
import pprint as pp
from dotenv import load_dotenv

# Load environment api key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

def fetch_game_data():


    url = "https://rawg.io/api/games"

    query_params = {
        "key": api_key,
        "page_size": 5,
        "ordering": "-metacritic"
    }

    try:
        response = requests.get(url, params=query_params)

        if response.status_code == 200:

            data = response.json()
            games_list = data.get("results", [])

            # Create a new list to store the transformed documents
            games = []

            for game in games_list:
                # Fetch additional details for each game using its ID
                response2 = requests.get(url+f'/{game.get("id")}', params=query_params)
                gamedata = response2.json()
                

                game_document = {
                    "rawg_id": game.get("id"),
                    "name": game.get("name"),
                    "release_date": game.get("released"),
                    "rating": game.get("rating"),
                    "metacritic_score": game.get("metacritic"),
                    "playtime_hours": game.get("playtime"),
                    "description": gamedata.get("description_raw"),

                    "genres": [
                        genre.get("name")
                        for genre in game.get("genres", [])
                    ],

                    "platforms": [
                        platform.get("platform", {}).get("name")
                        for platform in game.get("platforms", [])
                    ],

                    "tags": [
                        tag.get("name")
                        for tag in game.get("tags", [])
                    ],

                    "background_image": game.get("background_image")
                }

                games.append(game_document)

            # Just to check everything worked
            print(f"Extracted {len(games)} games.\n")

            for game in games:
                pp.pprint(game)

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")