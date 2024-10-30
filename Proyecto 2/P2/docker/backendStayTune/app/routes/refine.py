from flask import Blueprint, request, jsonify
from databases import postgres_connection
from databases import mongodb_connection

refine_bp = Blueprint('refine', __name__)

@refine_bp.route('/refine/<database_id>', methods=['GET'])
def refine_search(database_id):
    #Posgress
    if database_id == 1 :
        language = request.args.get('language')
        genres = request.args.get('genres')
        popularity = request.args.get('popularity')
        
        query_filters = []
        if language:
            query_filters.append(f"Language = '{language}'")  
        if genres:
            query_filters.append(f"Genres @> ARRAY{genres}") 
        if popularity:
            query_filters.append(f"Popularity >= {popularity}")  
        filter_sql = " AND ".join(query_filters) if query_filters else "1=1"
        query_sql = f"SELECT * FROM Song WHERE {filter_sql};"
        
        try:
            # Get a connection from the pool
            conn = postgres_connection.getconn()
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute(query_sql)
            results = cursor.fetchall()
            results = [dict(row) for row in results]
            
            # Release the connection back to the pool
            cursor.close()
            postgres_connection.putconn(conn)
            
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    #Mongo
    if database_id == 2 :
        mongo_db = mongodb_connection['MONGO_DB']  
        artist_collection = mongo_db['Artist']  
        song_collection = mongo_db['Song']  

        language = request.args.get('language')
        genres = request.args.get('genres')
        popularity = request.args.get('popularity')
        
        filters = {}
        results = []

        if language:
            filters["Language"] = language  
            results = song_collection.find(filters)
            
        artist_filters = {}
        if genres:
            artist_filters["Genres"] = {"$in": genres.split(",")}  
        if popularity:
            artist_filters["Popularity"] = {"$gte": int(popularity)}  
        
        artist_results = artist_collection.find(artist_filters)
        artist_links = [artist["Link"] for artist in artist_results]
        
        if artist_links:
            filters["ArtistLink"] = {"$in": artist_links}
            results = song_collection.find(filters)

        results = list(results)
        
        return jsonify(results)
            
