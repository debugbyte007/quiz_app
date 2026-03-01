"""
Script to migrate local JSON data to MongoDB Atlas.
Usage: python migrate_to_atlas.py
"""

import json
import sys
from pymongo import MongoClient
import os

def migrate_to_atlas(mongo_uri):
    """Migrate local JSON data to Atlas cluster."""
    
    try:
        # Connect to Atlas
        client = MongoClient(mongo_uri)
        db = client["quiz_app"]
        
        # Test connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB Atlas!")
        
        # Load and insert data
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        
        # Users
        with open(os.path.join(data_dir, "users.json"), "r") as f:
            users_data = json.load(f)
        
        users_collection = db["users"]
        users_collection.delete_many({})  # Clear existing
        if users_data.get("users"):
            result = users_collection.insert_many(users_data["users"])
            print(f"✓ Inserted {len(result.inserted_ids)} users")
        
        # Quizzes
        with open(os.path.join(data_dir, "quizzes.json"), "r") as f:
            quizzes_data = json.load(f)
        
        quizzes_collection = db["quizzes"]
        quizzes_collection.delete_many({})  # Clear existing
        if quizzes_data.get("quizzes"):
            result = quizzes_collection.insert_many(quizzes_data["quizzes"])
            print(f"✓ Inserted {len(result.inserted_ids)} quizzes")
        
        # Results
        with open(os.path.join(data_dir, "results.json"), "r") as f:
            results_data = json.load(f)
        
        results_collection = db["results"]
        results_collection.delete_many({})  # Clear existing
        if results_data.get("results"):
            result = results_collection.insert_many(results_data["results"])
            print(f"✓ Inserted {len(result.inserted_ids)} results")
        
        # Create indexes
        users_collection.create_index("username", unique=True)
        quizzes_collection.create_index("code", unique=True)
        print("✓ Created indexes")
        
        print("\n✅ Migration complete! All data is now in MongoDB Atlas.")
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("MongoDB Atlas Migration Script")
    print("=" * 50)
    
    mongo_uri = input("\nEnter your MongoDB Atlas connection string:\n(mongodb+srv://...): ").strip()
    
    if not mongo_uri.startswith("mongodb"):
        print("❌ Invalid connection string!")
        sys.exit(1)
    
    migrate_to_atlas(mongo_uri)
