from api_call import fetch_game_data
from mongodb_interaction import fetch_from_database, read_high_metacritic_games, save_to_database, create_game, delete_game, games_by_platform
from s3_interaction import save_to_s3
from recommendation_algorithm import generate_embeddings, generate_faiss_index, search_similar_games


def run_pipeline():
    print("--- STARTING PIPELINE ---")
    
    games = fetch_game_data()
    
    save_to_database(games)

    # #Create a new game document to insert into the database
    # new_game = {
    #     "rawg_id": 123456,
    #     "slug": "New Game",
    #     "name": "New Game Name",
    #     "tba": False,
    #     "release_date": "2024-01-01",
    #     "metacritic_score": 85,
    #     "playtime_hours": 10,
    #     "description": "This is a description of the new game.",
    #     "esrb_rating": "E",
    #     "developers": ["New Game Developer"],
    #     "publishers": ["New Game Publisher"],
    #     "genres": ["Action", "Adventure"],
    #     "platforms": ["PC", "PlayStation 5"],
    #     "tags": ["Multiplayer", "Open World"],
    #     "background_image": "https://example.com/new-game-image.jpg"
    # }

    # create_game(new_game)

    # Read and print games with a Metacritic score of 90 or higher
    # read_high_metacritic_games()


    #deletes a game from the database using its name.
    # delete_game("New Game Name")


    # Reads and prints the platform along with the total number of games available on that platform from the database.
    # games_by_platform()

 


    # # Generate embeddings for the game descriptions
    # games_with_embeddings = generate_embeddings(games)

    # save_to_database(games_with_embeddings)

    # index = generate_faiss_index(games_with_embeddings)

    # similar_games = search_similar_games(index, games_with_embeddings, "A thrilling open-world adventure game with dragons and magic.", k=3)

    # print(similar_games)


    # Fetches all except vectors from db to insert into AWS S3
    gamesToUpload = fetch_from_database(['background_image', 'description', 'genres', 'platforms', 'metacritic_score', 'name', 'playtime_hours', 'publishers', 'release_date', 'slug', 'tba', 'tags', 'esrb_rating', 'developers', 'rawg_id'])

    # Upload to S3
    save_to_s3(gamesToUpload)



    # games = fetch_games_by_id(similar_games)

    # print("\n--- Similar Games ---")
    # for game in games:
    #     print(f"Name: {game['name']}, Description: {game['description']}")

    # -----------TODO--------------

    # save_to_s3(games)

    # -----------------------------

    print("--- PIPELINE COMPLETE ---")

# This is a standard Python safeguard. It ensures the script only runs 
# if you execute this file directly (e.g., 'python main.py')
if __name__ == "__main__":
    run_pipeline()



