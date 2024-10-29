from flask import Blueprint, jsonify
from databases import postgres_connection

song_bp = Blueprint('song_postgres', __name__)

@song_bp.route('/song/<song_id>', methods=['GET'])
def get_song(song_id):
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
