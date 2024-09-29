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

# Initialize multiple MongoDB clients for different databases
db_clients = [
    MongoClient("mongodb+srv://<username>:<password>@cluster1.mongodb.net/db1?retryWrites=true&w=majority"),
    MongoClient("mongodb+srv://<username>:<password>@cluster2.mongodb.net/db2?retryWrites=true&w=majority"),
    # Add more database clients here
]

# Select the appropriate database based on the group ID, storage, or other criteria
def select_database(group_id):
    # Logic to select the appropriate database
    # Example: Group 1 uses db_clients[0], Group 2 uses db_clients[1], etc.
    db_index = group_id % len(db_clients)
    return db_clients[db_index]["telegram_bot"]
