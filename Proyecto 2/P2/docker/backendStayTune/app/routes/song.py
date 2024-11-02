from flask import Blueprint, request, jsonify
from utils import executePostgresQuery, executeMongoQuery

song_bp = Blueprint('song', __name__)

def postgresSongs(query: str):
    query_P = """
        SELECT S.*
        FROM Song S 
        INNER JOIN Artist A ON S.ArtistLink = A.Link 
        WHERE S.Lyric ILIKE %s OR A.Name ILIKE %s
        LIMIT 15
    """
    params = ('%' + query + '%', '%' + query + '%')
    results = executePostgresQuery(query_P, params)
    resultsDicts = []
    for result in results:
        resultsDicts.append({
            'ArtistLink': result[0],
            'Name': result[1],
            'Link': result[2],
            'Lyric': result[3],
            'Language': result[4]
        })
    return jsonify(resultsDicts), 200

def mongoSongs(query: str):
    return jsonify(executeMongoQuery(query, 'Song')), 200

@song_bp.route('/song/<database_id>', methods=['POST'])
def get_song(database_id):
    data = request.json
    query = data.get('query')
    # Posgress
    database_id = int(database_id)
    if database_id == 1:
        return postgresSongs(query)
    # Mongo
    if database_id == 2:
        return mongoSongs(query)
    return "Invalid database id", 400