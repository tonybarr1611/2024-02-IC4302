from flask import Blueprint, request, jsonify
from databases import connect_to_postgres

refine_bp = Blueprint('refine_postgres', __name__)

# Initialize PostgreSQL connection
postgres_conn, postgres_cursor = connect_to_postgres()

@refine_bp.route('/refine', methods=['GET'])
def refine_search():
    language = request.args.get('language')
    genres = request.args.get('genres')
    popularity = request.args.get('popularity')
    
    query_filters = []
    if language:
        query_filters.append(f"language = '{language}'")
    if genres:
        query_filters.append(f"genres IN ({', '.join([f'\'{g}\'' for g in genres.split(',')])})")
    if popularity:
        query_filters.append(f"popularity >= {popularity}")
    filter_sql = " AND ".join(query_filters) if query_filters else "1=1"
    query_sql = f"SELECT * FROM songs WHERE {filter_sql};"
    postgres_cursor.execute(query_sql)
    results = postgres_cursor.fetchall()
    results = [dict(row) for row in results]

    return jsonify(results)