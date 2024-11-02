from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from contextlib import contextmanager
from os import getenv

MONGO_URI = getenv("MONGO_URI")
MONGO_DB = getenv("MONGO_DB")

class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(
                    MONGO_URI,
                    server_api=ServerApi('1'),
                    maxPoolSize=10,
                    minPoolSize=1
                )
                print("MongoDB connection established with a pool.")
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                cls._instance = None
        return cls._instance

@contextmanager
def get_mongo_connection():
    client = MongoDBConnection()
    if client is None:
        raise Exception("Failed to connect to MongoDB.")
    
    try:
        yield client
    finally:
        pass

def initDB():
    with get_mongo_connection() as connection:
        db = connection.get_database(MONGO_DB)
        collections = db.list_collection_names()
        
        if collections:
            for collection_name in collections:
                db.drop_collection(collection_name)
            print(f"Cleared existing collections in database '{MONGO_DB}'.")
            db.create_collection("Song")
            db.create_collection("Artist")
        else:
            print(f"No collections found in database '{MONGO_DB}'. It is already empty.")

def insertDataMongo(collection_name, fields, data):
    with get_mongo_connection() as connection:
        db = connection.get_database(MONGO_DB)
        collection = db.get_collection(collection_name)

        documents = [dict(zip(fields, values)) for values in data]
        
        if documents:
            collection.insert_many(documents)
            print(f"Inserted {len(documents)} documents into the collection '{collection_name}'.")
        else:
            print(f"No valid documents to insert into the collection '{collection_name}'.")