from api_call import fetch_game_data
from mongodb_interaction import fetch_from_database, save_to_database
from s3_interaction import save_to_s3
from recommendation_algorithm import generate_embeddings

def run_pipeline():
    print("--- STARTING PIPELINE ---")
    
    games = fetch_game_data()
    
    save_to_database(games)
    
    games = fetch_from_database(["description"])

    # Generate embeddings for the game descriptions
    games_with_embeddings = generate_embeddings(games)

    save_to_database(games_with_embeddings)

    # -----------TODO--------------

    # save_to_s3(games)

    # -----------------------------

    print("--- PIPELINE COMPLETE ---")

# This is a standard Python safeguard. It ensures the script only runs 
# if you execute this file directly (e.g., 'python main.py')
if __name__ == "__main__":
    run_pipeline()

