from api_call import fetch_game_data
from mongodb_interaction import save_to_database

def run_pipeline():
    print("--- STARTING PIPELINE ---")
    
    games = fetch_game_data()
    
    save_to_database(games)

    print("--- PIPELINE COMPLETE ---")

# This is a standard Python safeguard. It ensures the script only runs 
# if you execute this file directly (e.g., 'python main.py')
if __name__ == "__main__":
    run_pipeline()

