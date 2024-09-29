from database import mariadb_connection, elasticsearch_connection
from config import HUGGINGFACE
import requests

errResult = {'result': '401'}

def executeQuery(query):
    global mariadb_connection
    conn = mariadb_connection.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    result = []
    try:
        result = cur.fetchall()
    except Exception as e:
        print("No result dataset")
    conn.commit()
    conn.close()
    return result

def getEmbeddings(prompt):
    response = requests.post(f'http://{HUGGINGFACE}:5000/encode', json={'text': prompt})
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('embedding')
    else:
        raise Exception(f"Failed to get embeddings: {response.status_code}, {response.text}")

def getVectorSearchQuery(vector):
    return {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                    "params": {"query_vector": vector}
                }
            }
        }
    }
