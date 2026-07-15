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


def create_game(game):

    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    try:
        client = MongoClient(mongo_uri)

        db = client["video_game_db"]
        collection = db["games"]

        result = collection.insert_one(game)

        print(f"Game created with ID: {result.inserted_id}")

    except Exception as e:
        print(f"Error creating game: {e}")

    finally:
        client.close()



def read_high_metacritic_games():

    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    try:
        client = MongoClient(mongo_uri)

        db = client["video_game_db"]
        collection = db["games"]

        # Find games with a Metacritic score of 90 or higher
        games = collection.find(
            {
                "metacritic_score": {
                    "$gte": 90
                }
            },
            {
                "_id": 0,
                "name": 1,
                "metacritic_score": 1,
                "release_date": 1,
                "genres": 1
            }
        )

        print("\n--- Highly Rated Metacritic Games ---")

        for game in games:
            pp.pprint(game)


    except errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB. Error: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")


def update_metacritic_score(game_name, new_score):

    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    try:
        client = MongoClient(mongo_uri)

        db = client["video_game_db"]
        collection = db["games"]

        result = collection.update_one(
            {
                "name": game_name
            },
            {
                "$set": {
                    "metacritic_score": new_score
                }
            }
        )

        if result.modified_count > 0:
            print(f"{game_name} score updated to {new_score}")

        else:
            print("No game found or score already the same")

    except Exception as e:
        print(f"Error updating game: {e}")

    finally:
        client.close()


def delete_game(game_name):

    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    try:

        client = MongoClient(mongo_uri)

        db = client["video_game_db"]
        collection = db["games"]


        result = collection.delete_one(
            {
                "name":game_name
            }
        )


        print(
            f"Deleted documents: {result.deleted_count}"
        )


    except Exception as e:
        print(f"Error deleting game: {e}")

    finally:
        client.close()


def games_by_platform():

    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

    client = MongoClient(mongo_uri)

    db = client["video_game_db"]
    collection = db["games"]


    pipeline = [

        {
            "$unwind": "$platforms"
        },

        {
            "$group": {
                "_id": "$platforms",
                "total_games": {
                    "$count": {}
                }
            }
        },

        {
            "$sort": {
                "total_games": -1
            }
        }

    ]


    results = collection.aggregate(pipeline)


    for platform in results:
        pp.pprint(platform)


    client.close()