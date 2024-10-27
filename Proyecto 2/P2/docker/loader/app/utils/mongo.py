from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import getenv

MONGO_URI = getenv("MONGO_URI")
MONGO_DB = getenv("MONGO_DB")

def generateMongoConnection():
    try:
        client = MongoClient(
            MONGO_URI,
            server_api=ServerApi('1'),
            maxPoolSize=10, 
            minPoolSize=1 
        )
        print("MongoDB connection established with a pool.")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
    
def initDB(connection):
    if not connection:
        print("Failed to connect to MongoDB. Exiting.")
        return

    try:
        db = connection.get_database(MONGO_DB)

        collections = db.list_collection_names()
        if collections:
            for collection_name in collections:
                db.drop_collection(collection_name)
        else:
            print(f"No collections found in database '{MONGO_DB}'. It is already empty.")

    except Exception as e:
        print(f"Error wiping database '{MONGO_DB}': {e}")
    finally:
        connection.close()

def insertDataMongo(connection, collection_name, fields, data):
    if not connection:
        print("Failed to connect to MongoDB. Exiting.")
        return

    try:
        print('1.')
        db = connection.get_database(MONGO_DB)
        collection = db.get_collection(collection_name)
        print('2.')
        documents = []
        counter = 0
        for values in data:
            document = dict(zip(fields, values))
            documents.append(document)
            counter += 1
        print('6.')
        if documents:
            collection.insert_many(documents)
            print('7.')
        else:
            print(f"No valid documents to insert into the collection '{collection_name}'.")

    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        connection.close()