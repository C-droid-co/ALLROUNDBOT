from pymongo import MongoClient
from config import MONGODB_URI

# Initialize the MongoDB client
client = MongoClient(MONGODB_URI)

# Select the database
db = client["telegram_bot"]

# Function to fetch a specific collection
def get_collection(name):
    return db[name]

# Add, update, and fetch user info
def add_user(user_id, user_data):
    users_collection = get_collection("users")
    users_collection.update_one({"user_id": user_id}, {"$set": user_data}, upsert=True)

def get_user(user_id):
    users_collection = get_collection("users")
    return users_collection.find_one({"user_id": user_id})

def remove_user(user_id):
    users_collection = get_collection("users")
    users_collection.delete_one({"user_id": user_id})
