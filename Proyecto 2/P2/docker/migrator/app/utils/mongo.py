from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import getenv

MONGO_URI = getenv("MONGO_URI")
MONGO_DB = getenv("MONGO_DB")

# Ensures only one connection to MongoDB is made
class MongoConnectionSingleton:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnectionSingleton, cls).__new__(cls)
            try:
                cls._client = MongoClient(
                    MONGO_URI,
                    server_api=ServerApi('1'),
                    maxPoolSize=10,
                    minPoolSize=1
                )
                print("MongoDB connection established with a pool.")
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                cls._client = None
        return cls._instance

    def get_client(self):
        return self._client

# Gives a connection to the MongoDB database
def generateMongoConnection():
    singleton = MongoConnectionSingleton()
    return singleton.get_client()

# Reads data from MongoDB
def readDataMongo(collectionName: str):
    connection = generateMongoConnection()
    if not connection:
        print("Failed to connect to MongoDB. Exiting.")
        return

    try:
        db = connection.get_database(MONGO_DB)
        collection = db.get_collection(collectionName)
        
        documents = collection.find()
        
        # Parse the documents into a list
        return [doc for doc in documents]
        
    except Exception as e:
        print(f"Error reading data: {e}")
    finally:
        connection.close()