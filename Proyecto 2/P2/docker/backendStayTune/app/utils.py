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
    
def executeMongoQuery(text):
    global mongodb_connection
    db = mongodb_connection[MONGO_DB]
    collection = db[collection]

    # Create index search
    sampleDocument = collection.find_one()
    if sampleDocument:
        fields = list(sampleDocument.keys())[1:]
        index_spec = [(field, "text") for field in fields]
        collection.create_index(index_spec)

    results = collection.find({"$text": {"$search": text}})

    return results

def executeQuery(database, query):
    if database.lower() == "postgres":
        executePostgresQuery(query)
    elif database.lower() == "mongo":
        executeMongoQuery(query)