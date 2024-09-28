from pymongo import MongoClient

def connect_mongo(uri):
    try:
        client = MongoClient(uri)
        db = client['group_management_bot']  # Replace with your database name
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


# Function to set a welcome message in the database
def set_welcome_message(group_id, welcome_message):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        db.welcome.update_one(
            {"group_id": group_id}, 
            {"$set": {"welcome_message": welcome_message, "enabled": True}}, 
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error setting welcome message: {e}")
        return False

# Function to get a welcome message from the database
def get_welcome_message(group_id):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        welcome_data = db.welcome.find_one({"group_id": group_id})
        if welcome_data:
            return welcome_data.get("welcome_message"), welcome_data.get("enabled")
        return None, False
    except Exception as e:
        print(f"Error getting welcome message: {e}")
        return None, False

# Function to toggle the welcome message status (enabled/disabled)
def toggle_welcome(group_id, status):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        db.welcome.update_one(
            {"group_id": group_id}, 
            {"$set": {"enabled": status}}, 
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error toggling welcome status: {e}")
        return False
