from pymongo import MongoClient
import os

# Use MongoDB Atlas connection string from environment, fall back to localhost
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["quiz_app"]

users_collection = db["users"]
quizzes_collection = db["quizzes"]
results_collection = db["results"]

users_collection.create_index("username", unique=True)
quizzes_collection.create_index("code", unique=True)
