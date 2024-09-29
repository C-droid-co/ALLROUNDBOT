from pymongo import MongoClient
import os
import time

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

import time

# Function to add a message record for a user
def add_message_record(group_id, user_id):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        timestamp = time.time()
        db.spam_records.update_one(
            {"group_id": group_id, "user_id": user_id},
            {"$push": {"messages": timestamp}},
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error adding message record: {e}")
        return False

# Function to check if a user is spamming
def is_spamming(group_id, user_id, message_limit=5, time_limit=10):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        record = db.spam_records.find_one({"group_id": group_id, "user_id": user_id})
        
        if record:
            messages = record["messages"]
            # Filter messages that are within the time limit
            recent_messages = [msg for msg in messages if time.time() - msg < time_limit]
            
            if len(recent_messages) >= message_limit:
                # If user is spamming, remove old records
                db.spam_records.update_one(
                    {"group_id": group_id, "user_id": user_id},
                    {"$set": {"messages": recent_messages}}
                )
                return True
            
            # Update messages to reflect recent activity
            db.spam_records.update_one(
                {"group_id": group_id, "user_id": user_id},
                {"$set": {"messages": recent_messages}}
            )
        return False
    except Exception as e:
        print(f"Error checking spam: {e}")
        return False

# Function to set the group lock status
def set_group_lock(group_id, lock_status):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        db.group_settings.update_one(
            {"group_id": group_id},
            {"$set": {"locked": lock_status}},
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error setting group lock: {e}")
        return False

# Function to get the group lock status
def get_group_lock(group_id):
    try:
        db = connect_mongo(os.getenv("MONGO_URI"))
        record = db.group_settings.find_one({"group_id": group_id})
        if record and "locked" in record:
            return record["locked"]
        return False
    except Exception as e:
        print(f"Error getting group lock: {e}")
        return False
