import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv


# Implementation for saving data to MongoDB
def save_to_database(game_list):
    print("Connecting to MongoDB...")

    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    try:
        client = MongoClient(mongo_uri)
        
        db = client["video_game_db"]      
        collection = db["games"]           
        
        print(f"Processing {len(game_list)} games...")
        inserted_count = 0
        updated_count = 0

        # Loop through the list of dictionaries
        for game in game_list:
            result = collection.update_one(
                {"rawg_id": game["rawg_id"]},  
                {"$set": game},      
                upsert=True               
            )
            
            if result.upserted_id:
                inserted_count += 1
            else:
                updated_count += 1

        print(f"\nDatabase sync complete! Inserted: {inserted_count} | Updated: {updated_count}")
            
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB. Check your URI string. Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")

def fetch_from_database(query):
    pass