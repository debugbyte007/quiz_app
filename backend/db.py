import os
from dotenv import load_dotenv

load_dotenv()

# Check if Supabase credentials are available
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Try Supabase first, fall back to JSON if it fails
try:
    if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "your_supabase_project_url_here":
        # Test Supabase connection
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Quick test to see if credentials work
        supabase.table("users").select("*").limit(1).execute()
        print("🚀 Using Supabase database for production scaling")
        from supabase_db import users_collection, quizzes_collection, results_collection
    else:
        raise Exception("Supabase credentials not available")
except Exception as e:
    # Use JSON files for local development or if Supabase fails
    print(f"📁 Using JSON files (Supabase error: {str(e)[:50]}...)")
    import json
    from datetime import datetime

    # Simple JSON-based storage for local development
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    class JSONCollection:
        def __init__(self, filename):
            self.filepath = os.path.join(DATA_DIR, filename)
            self.data = self._load_data()
        
        def _load_data(self):
            if os.path.exists(self.filepath):
                try:
                    with open(self.filepath, 'r') as f:
                        return json.load(f)
                except:
                    return []
            return []
        
        def _save_data(self):
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=2)
        
        def find_one(self, query):
            for item in self.data:
                if self._matches_query(item, query):
                    return item
            return None
        
        def find(self, query=None, projection=None):
            results = []
            for item in self.data:
                if query is None or self._matches_query(item, query):
                    if projection and "_id" in projection and projection["_id"] == 0:
                        # Remove _id field if projection excludes it
                        item_copy = {k: v for k, v in item.items() if k != "_id"}
                        results.append(item_copy)
                    else:
                        results.append(item)
            return JSONCursor(results)
        
        def insert_one(self, document):
            # Add a simple _id if not present
            if "_id" not in document:
                document["_id"] = len(self.data) + 1
            self.data.append(document)
            self._save_data()
            return document
        
        def update_one(self, query, update):
            for item in self.data:
                if self._matches_query(item, query):
                    if "$set" in update:
                        item.update(update["$set"])
                    if "$push" in update:
                        for key, value in update["$push"].items():
                            if key not in item:
                                item[key] = []
                            item[key].append(value)
                    self._save_data()
                    return True
            return False
        
        def _matches_query(self, item, query):
            for key, value in query.items():
                if key not in item:
                    return False
                
                if isinstance(value, dict):
                    if "$regex" in value:
                        import re
                        pattern = value["$regex"]
                        flags = 0
                        if "$options" in value and "i" in value["$options"]:
                            flags = re.IGNORECASE
                        if not re.search(pattern, str(item[key]), flags):
                            return False
                    else:
                        return False
                elif item[key] != value:
                    return False
            return True

    class JSONCursor:
        def __init__(self, data):
            self.data = data
        
        def sort(self, sort_spec):
            def sort_key(item):
                keys = []
                for field, direction in sort_spec:
                    value = item.get(field, 0)
                    if direction == -1:
                        # For descending, negate numeric values
                        if isinstance(value, (int, float)):
                            keys.append(-value)
                        else:
                            keys.append(value)
                    else:
                        keys.append(value)
                return keys
            
            self.data.sort(key=sort_key)
            return self
        
        def __iter__(self):
            return iter(self.data)

    # Collections
    users_collection = JSONCollection("users.json")
    quizzes_collection = JSONCollection("quizzes.json")
    results_collection = JSONCollection("results.json")