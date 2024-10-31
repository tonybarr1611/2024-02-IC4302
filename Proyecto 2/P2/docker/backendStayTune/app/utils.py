from config import MONGO_DB
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

def executeMongoUnique():
    global mongodb_connection
    db = mongodb_connection[MONGO_DB]
    song_collection = db['Song']
    artist_collection = db['Artist']
    
    languages = set(song_collection.distinct('Language'))
    genres = set(artist_collection.distinct('Genres'))
    artists = {artist for artist in artist_collection.find()}
    
    return languages, genres, artists