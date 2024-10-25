from flask import Blueprint, request, jsonify
from databases import connect_to_mongo

refine_bp = Blueprint('refine_mongo', __name__)

# Initialize MongoDB connection
mongo_collection = connect_to_mongo()

@refine_bp.route('/refine', methods=['GET'])
def refine_search():
    language = request.args.get('language')
    genres = request.args.get('genres')
    popularity = request.args.get('popularity')
    
    filters = {}
    if language:
        filters["language"] = language
    if genres:
        filters["genres"] = {"$in": genres.split(",")}
    if popularity:
        filters["popularity"] = {"$gte": int(popularity)}
    
    results = mongo_collection.find(filters)
    results = list(results)
    
    return jsonify(results)