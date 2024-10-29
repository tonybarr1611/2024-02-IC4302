from flask import Blueprint, request, jsonify
from databases import mongodb_connection

refine_bp = Blueprint('refine_mongo', __name__)

# Initialize MongoDB connection
mongo_db = mongodb_connection['MONGO_DB']  
artist_collection = mongo_db['Artist']  
song_collection = mongo_db['Song']  

@refine_bp.route('/refine', methods=['GET'])
def refine_search():
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