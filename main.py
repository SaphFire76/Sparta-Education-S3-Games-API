import os
from dotenv import load_dotenv

# Load environment api key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

BASE_URL = "https://api.rawg.io/api/games"

