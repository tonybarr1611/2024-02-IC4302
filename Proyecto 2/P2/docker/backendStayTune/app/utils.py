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
    song_collection = db['Song']
    artist_collection = db['Artist']
    
    languages = set(song_collection.distinct('Language'))
    genres = set(artist_collection.distinct('Genres'))
    popularities = song_collection.aggregate([
    {
        "$group": {
            "_id": None,
            "max": {"$max": "$Popularity"},
            "min": {"$min": "$Popularity"}
        }
    }
])
    artists = {artist for artist in artist_collection.find()}
    
    return languages, genres, popularities, artists