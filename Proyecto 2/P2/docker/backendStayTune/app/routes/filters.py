from flask import Blueprint, jsonify
from utils import executePostgresQuery, executeMongoUnique

filters_bp = Blueprint('filters', __name__)

def filtersPostres():
    artists = "SELECT * FROM Artist"
    artists = list(executePostgresQuery(artists))
    artistsDict = []
    for artist in artists:
        artistsDict.append({
            'Name': artist[0],
            'Genres': artist[1],
            'Songs': artist[2],
            'Popularity': artist[3],
            'Link': artist[4],
        })
    
    return jsonify({
        "artists": artistsDict
    })
    
def filtersMongo():
    artists = executeMongoUnique()
    return jsonify({
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