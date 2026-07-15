import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import pprint as pp


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
        print(f"Could not connect to MongoDB. Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")

def fetch_from_database(keys_to_fetch):
    """
    Connects to MongoDB, fetches specific fields for all game documents, 
    and returns them as a list of dictionaries.
    
    Args:
        keys_to_fetch (list): A list of strings representing the keys you want to return.
    """

    print("Connecting to MongoDB...")
    
    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    
    try:
        client = MongoClient(mongo_uri)
        db = client["video_game_db"]      
        collection = db["games"]           
        
        # 1. Build the projection dictionary
        # We ALWAYS exclude the MongoDB _id (0 means exclude)
        # We ALWAYS include the rawg_id (1 means include)
        projection = {"_id": 0, "rawg_id": 1}
        
        # 2. Loop through the user's list and add those keys to our projection
        for key in keys_to_fetch:
            projection[key] = 1
            
        # 3. Fetch the data
        # {} means "find everything", and our projection dictionary filters the fields
        cursor = collection.find({}, projection)
        games_list = list(cursor)
        
        print(f"Successfully fetched {len(games_list)} games from the database!")
        return games_list
            
    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB. Error: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")