from config import MONGO_DB
from databases import DatabaseConnections
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')

def getEmbeddings(prompt):
    embedding = model.encode(prompt).tolist()
    return embedding

def executePostgresQuery(query, params=None):
    connection = None
    cursor = None
    try:
        connection = DatabaseConnections.getPostgresConnection().getconn()
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        DatabaseConnections.getPostgresConnection().putconn(connection)
        return result
    
    except Exception as e:
        print(f"No data found: {e}")
        return []
    
    
def executeMongoQuery(text, collectionS):
    conn = DatabaseConnections.getMongoConnection()
    db = conn[MONGO_DB]
    collection = db[collectionS]

    sampleDocument = collection.find_one()
    if sampleDocument:
        fields = list(sampleDocument.keys())[1:]
        index_spec = [(field, "text") for field in fields]
        collection.create_index(index_spec)

    cursor = collection.find({"$text": {"$search": text}})
    
    results = []
    for result in cursor:
        result.pop('_id', None)
        results.append(result)
        if len(results) >= 15:
            break

    return results


def executeMongoUnique():
    conn = DatabaseConnections.getMongoConnection()
    db = conn[MONGO_DB]
    artist_collection = db['Artist']

    artists = []
    for artist in artist_collection.find():
        artist.pop('_id', None)
        artists.append(artist)
    
    return artists