import psycopg2
from config import MONGO_DB
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')

def getEmbeddings(prompt):
    embedding = model.encode(prompt).tolist()
    return embedding

def executePostgresQuery(query):
    global postgres_connection
    connection = None
    cursor = None
    try:
        connection = postgres_connection.getconn()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    except Exception as e:
        print(f"No data found: {e}")
        return []
    
def executeMongoQuery(collection, query):
    global mongodb_connection
    db = mongodb_connection[MONGO_DB]
    collection = db[collection]
    results = collection.find(query)

    return results