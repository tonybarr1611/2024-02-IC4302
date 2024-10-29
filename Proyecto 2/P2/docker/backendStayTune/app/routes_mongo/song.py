from flask import Blueprint, jsonify
from databases import mongodb_connection
from bson import ObjectId

song_bp = Blueprint('song_mongo', __name__)

# Initialize MongoDB connection
mongo_db = mongodb_connection['MONGO_DB']  
mongo_collection = mongo_db['Song']  

@song_bp.route('/song/<song_id>', methods=['GET'])
def get_song(song_id):
    try:
        song = mongo_collection.find_one({"_id": ObjectId(song_id)})
        if song:
            return jsonify(dict(song))
        else:
            return jsonify({"error": "Canción no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
