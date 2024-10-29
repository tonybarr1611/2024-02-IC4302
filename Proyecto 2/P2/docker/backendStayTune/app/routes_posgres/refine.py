from flask import Blueprint, request, jsonify
from databases import postgres_connection

refine_bp = Blueprint('refine_postgres', __name__)

@refine_bp.route('/refine', methods=['GET'])
def refine_search():
    language = request.args.get('language')
    genres = request.args.get('genres')
    popularity = request.args.get('popularity')
    
    query_filters = []
    if language:
        query_filters.append(f"Language = '{language}'")  
    if genres:
        query_filters.append(f"Genres IN ({', '.join([f'\'{g}\'' for g in genres.split(',')])})")  
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