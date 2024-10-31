from flask import Blueprint, jsonify
from utils import executePostgresQuery, executeMongoUnique

filters_bp = Blueprint('filters', __name__)

def filtersPostres():
    languages = "SELECT DISTINCT Language FROM Song"
    genres = "SELECT DISTINCT Genres FROM Artist"
    artists = "SELECT * FROM Artist"
    return jsonify({
        "languages": list(executePostgresQuery(languages)),
        "genres": list(executePostgresQuery(genres)),
        "artists": list(executePostgresQuery(artists))
    })
    
def filtersMongo():
    languages, genres, artists = executeMongoUnique()
    return jsonify({
         "languages": list(languages),
         "genres": list(genres),
         "artists": list(artists)
    })

@filters_bp.route("/filters/<database_id>", methods=['GET'])
def filters(database_id):
    # Posgress
    database_id = int(database_id)
    if database_id == 1:
        return filtersPostres(), 200
    # Mongo
    if database_id == 2:
        return filtersMongo(), 200