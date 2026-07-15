from api_call import fetch_game_data
from mongodb_interaction import fetch_from_database, save_to_database
from s3_interaction import save_to_s3
from recommendation_algorithm import generate_embeddings, generate_faiss_index, search_similar_games

def run_pipeline():
    print("--- STARTING PIPELINE ---")
    
    games = fetch_game_data()
    
    save_to_database(games)
    
    games = fetch_from_database(["description"])

    # Generate embeddings for the game descriptions
    games_with_embeddings = generate_embeddings(games)

    save_to_database(games_with_embeddings)

    index = generate_faiss_index(games_with_embeddings)

    similar_games = search_similar_games(index, games_with_embeddings, "A thrilling open-world adventure game with dragons and magic.", k=3)

    print(similar_games)

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

