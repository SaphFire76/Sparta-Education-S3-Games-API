import os
import requests
import pprint as pp
from dotenv import load_dotenv

# Load environment api key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

def fetch_game_data():
    BASE_URL = "https://api.rawg.io/api/games"

    params = {
        "key": api_key,
        "page_size": 1
    }

    try:
        response = requests.get(BASE_URL, params=params)
        
        response.raise_for_status()
        
        data = response.json()

        #print(f"Found {len(data['results'])} games:\n")
        pp.pprint(data['results'])

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")