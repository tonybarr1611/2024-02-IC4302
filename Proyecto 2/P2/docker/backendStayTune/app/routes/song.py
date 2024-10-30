from flask import Blueprint, jsonify
from databases import postgres_connection
from databases import mongodb_connection
from bson import ObjectId

song_bp = Blueprint('song', __name__)

@song_bp.route('/song/<song_id>/<database_id>', methods=['GET'])
def get_song(song_id, database_id):
    # Posgress
    if database_id == 1:
        conn = postgres_connection.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Song WHERE id = %s;", (song_id,))
            song = cursor.fetchone()
            if song:
                return jsonify(dict(song))
            else:
                return jsonify({"error": "Canción no encontrada"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            postgres_connection.putconn(conn)
    # Mongo
    if database_id == 2:
        mongo_db = mongodb_connection['MONGO_DB']  
        mongo_collection = mongo_db['Song']  
        try:
            song = mongo_collection.find_one({"_id": ObjectId(song_id)})
            if song:
                return jsonify(dict(song))
            else:
                return jsonify({"error": "Canción no encontrada"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500