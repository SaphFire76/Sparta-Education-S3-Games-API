import os
from time import time
import requests
import pprint as pp
from dotenv import load_dotenv

# Load environment api key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

def fetch_game_details(game_id, api_key):
    url = f"https://rawg.io/api/games/{game_id}"

    response = requests.get(url, params={"key": api_key})
    response.raise_for_status()

    return response.json()



def fetch_game_data(target_count=100):
    """
    Fetches games from RAWG, following pagination until either
    target_count games have been collected or there are no more pages.
    """
    url = "https://rawg.io/api/games"
    query_params = {
        "key": api_key,
        "page_size": 40,  # RAWG caps this at 40 regardless of what you request
        # "ordering": "-metacritic"
    }

    games = []

    try:
        while url and len(games) < target_count:
            response = requests.get(url, params=query_params)

            if response.status_code != 200:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                break

            data = response.json()
            games_list = data.get("results", [])

            for game in games_list:
                if len(games) >= target_count:
                    break

                gamedata = fetch_game_details(game.get("id"), api_key)

                game_document = {
                    "rawg_id": game.get("id"),
                    "slug": game.get("slug"),
                    "name": game.get("name"),
                    "tba": game.get("tba"),
                    "release_date": game.get("released"),
                    "metacritic_score": game.get("metacritic"),
                    "playtime_hours": game.get("playtime"),
                    "description": gamedata.get("description_raw"),

                    "esrb_rating": (
                        gamedata.get("esrb_rating", {}) or {}
                                    ).get("name"),

                    "developers": [
                        developer.get("name")
                        for developer in gamedata.get("developers", [])
                    ],

                    "publishers": [
                        publisher.get("name")
                        for publisher in gamedata.get("publishers", [])
                    ],

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


            print(f"Fetched {len(games)} games so far...")

            # RAWG gives you the full next-page URL (with query params already included)
            url = data.get("next")
            query_params = {}  # params are already baked into `next`, so clear these

        print(f"\nExtracted {len(games)} games total.\n")
        return games

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return games  # return whatever was collected before the error