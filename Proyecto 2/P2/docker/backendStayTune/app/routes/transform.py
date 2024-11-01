from flask import Blueprint, request, jsonify
from databases import DatabaseConnections
from utils import getEmbeddings

transform_bp = Blueprint('transform', __name__)

@transform_bp.route('/lyrics-to-apartments', methods=['POST'])
def lyrics_to_apartments():
    data = request.json
    text = data.get('selected_text')

    # Generate embedding
    embedding = getEmbeddings(text)

    # Search in Elasticsearch
    es_query = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "should": [
                            {"match_all": {}}
                        ]
                    }
                },
                "script": {
                    "source": """
                    double score = Math.max(
                        cosineSimilarity(params.query_vector, 'name_embedding'),
                        0) + 
                        Math.max(
                            cosineSimilarity(params.query_vector, 'summary_embedding'),
                            0) + 
                        Math.max(
                            cosineSimilarity(params.query_vector, 'description_embedding'),
                            0);
                    
                    // Ensure score from nested documents is non-negative
                    for (def review : params.reviews) {
                        score += Math.max(
                            cosineSimilarity(params.query_vector, review.embedding),
                            0);
                    }
                    return Math.max(score, 0); // Ensure final score is non-negative
                    """,
                    "params": {
                        "query_vector": embedding,
                        "reviews": [] 
                    }
                }
            }
        },
        "_source": ["name", "summary", "description", "reviews"]
    }



    try:
        es_client = DatabaseConnections.getESConnection()
        es_results = es_client.search(index="listingsandreviews", body=es_query, size=6)
        hits = es_results['hits']['hits']
        results = [hit['_source'] for hit in hits]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

