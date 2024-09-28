from pymongo import MongoClient

def connect_mongo(uri):
    try:
        client = MongoClient(uri)
        db = client['group_management_bot']  # Replace with your database name
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
