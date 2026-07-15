from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(game_descriptions):
    """
    Takes a list of dicts: [{"rawg_id": 123, "description": "..."}]
    Returns a list of dicts: [{"rawg_id": 123, "vector": [...]}]
    """
    print(f"Generating embeddings for {len(game_descriptions)} games...")
    
    # Extract the descriptions from the list of dictionaries
    text_list = [game["description"] for game in game_descriptions]
    
    # Generate embeddings for descriptions
    raw_embeddings = model.encode(text_list)
    
    # Build the list of dictionaries with rawg_id and vector
    vector_objects = []
    
    for i, game in enumerate(game_descriptions):
        vector_objects.append({
            "rawg_id": game["rawg_id"],
            "vector": raw_embeddings[i].tolist() 
        })
        
    print("Embeddings generated successfully!")
    return vector_objects