import os
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict, Any, Optional

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

class SupabaseCollection:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.table = supabase.table(table_name) if supabase else None
    
    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.table:
            return None
        
        try:
            # Build query
            result = self.table.select("*")
            
            for key, value in query.items():
                if isinstance(value, dict) and "$regex" in value:
                    # Handle regex queries (case-insensitive username search)
                    pattern = value["$regex"].replace("^", "").replace("$", "")
                    if "$options" in value and "i" in value["$options"]:
                        result = result.ilike(key, f"%{pattern}%")
                    else:
                        result = result.like(key, f"%{pattern}%")
                else:
                    result = result.eq(key, value)
            
            response = result.limit(1).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error in find_one: {e}")
            return None
    
    def find(self, query: Optional[Dict[str, Any]] = None, projection: Optional[Dict[str, int]] = None):
        if not self.table:
            return SupabaseCursor([])
        
        try:
            result = self.table.select("*")
            
            if query:
                for key, value in query.items():
                    result = result.eq(key, value)
            
            response = result.execute()
            return SupabaseCursor(response.data or [])
        except Exception as e:
            print(f"Error in find: {e}")
            return SupabaseCursor([])
    
    def insert_one(self, document: Dict[str, Any]) -> Dict[str, Any]:
        if not self.table:
            return document
        
        try:
            # Remove _id if present (Supabase uses auto-generated ids)
            doc_copy = {k: v for k, v in document.items() if k != "_id"}
            response = self.table.insert(doc_copy).execute()
            return response.data[0] if response.data else document
        except Exception as e:
            print(f"Error in insert_one: {e}")
            return document
    
    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        if not self.table:
            return False
        
        try:
            # Find the record first
            record = self.find_one(query)
            if not record:
                return False
            
            update_data = {}
            
            if "$set" in update:
                update_data.update(update["$set"])
            
            if "$push" in update:
                for key, value in update["$push"].items():
                    current_list = record.get(key, [])
                    if not isinstance(current_list, list):
                        current_list = []
                    current_list.append(value)
                    update_data[key] = current_list
            
            # Update using the record's id
            result = self.table.update(update_data).eq("id", record["id"]).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error in update_one: {e}")
            return False

class SupabaseCursor:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
    
    def sort(self, sort_spec: List[tuple]):
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
users_collection = SupabaseCollection("users")
quizzes_collection = SupabaseCollection("quizzes")
results_collection = SupabaseCollection("results")