from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer
from databases import elasticsearch_connection

transform_bp = Blueprint('transform', __name__)

es_client = elasticsearch_connection

# Load embeddings model
model = SentenceTransformer('all-mpnet-base-v2')

@transform_bp.route('/lyrics-to-apartments', methods=['POST'])
def lyrics_to_apartments():
    data = request.json
    text = data.get('selected_text')

    # Generate embedding
    embedding = model.encode(text)

    # Search in Elasticsearch
    es_query = {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'description_embedding') + 1.0",
                    "params": {"query_vector": embedding.tolist()}
                }
            }
        },
        "_source": ["name_embedding", "summary_embedding", "description_embedding", "reviews_embeddings"]
    }

    try:
        es_results = es_client.search(index="listingsAndReviews", body=es_query, size=10)
        hits = es_results['hits']['hits']
        results = [hit['_source'] for hit in hits]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

