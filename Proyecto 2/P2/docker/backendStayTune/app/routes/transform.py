from flask import Blueprint, request, jsonify
from databases import elasticsearch_connection
from utils import getEmbeddings

transform_bp = Blueprint('transform', __name__)

es_client = elasticsearch_connection

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
                "match_all": {}
            },
            "script": {
                "source": """
                cosineSimilarity(params.query_vector, 'name_embedding') + 
                cosineSimilarity(params.query_vector, 'summary_embedding') + 
                cosineSimilarity(params.query_vector, 'description_embedding') + 
                cosineSimilarity(params.query_vector, 'reviews_embeddings') + 
                4.0
                """,
                "params": { "query_vector": embedding.tolist() }
            }
            }
        },
        "_source": True
    }

    try:
        es_results = es_client.search(index="listingsAndReviews", body=es_query, size=5)
        hits = es_results['hits']['hits']
        results = [hit['_source'] for hit in hits]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

