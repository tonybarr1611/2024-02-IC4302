from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.docs import generateDocumentEmbeddings, serializableDoc
from utils.elastic import indexDocument
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
    print("Reading data from MongoDB")
    connection = generateMongoConnection()
    if not connection:
        print("Failed to connect to MongoDB. Exiting.")
        return

    try:
        print("Connected to MongoDB")
        db = connection.get_database(MONGO_DB)
        collection = db.get_collection(collectionName)
        print(f"Reading data from {collectionName} collection")
        
        documents = collection.find()
        print("Data read successfully")
        # Parse the documents into a list
        n = 1
        for doc in documents:
            print(f"Processing document {n}")
            embeddedDoc = generateDocumentEmbeddings(doc)
            indexDocument(serializableDoc(embeddedDoc))
            print(f"Document {n} processed and indexed")
            n += 1 
        return n
    except Exception as e:
        print(f"Error reading data: {e}")
    finally:
        connection.close()