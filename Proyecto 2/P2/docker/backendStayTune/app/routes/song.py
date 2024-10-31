from flask import Blueprint, jsonify
from utils import executePostgresQuery, executeMongoQuery

song_bp = Blueprint('song', __name__)

def postgresSongs(query: str):
    query_P = f"SELECT * FROM Song WHERE Lyric LIKE '%{query}%' OR Artist LIKE '%{query}%'"
    return jsonify(executePostgresQuery(query_P)), 200

def mongoSongs(query: str):
    return jsonify(executeMongoQuery(query)), 200

@song_bp.route('/song/<query>/<database_id>', methods=['GET'])
def get_song(query, database_id):
    # Posgress
    database_id = int(database_id)
    if database_id == 1:
        postgresSongs(query)
    # Mongo
    if database_id == 2:
        mongoSongs(query)