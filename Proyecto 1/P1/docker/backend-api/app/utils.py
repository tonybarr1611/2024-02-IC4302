import time
import requests
from functools import wraps
from config import HUGGINGFACE
from database import mariadb_connection
from metrics import avg_processing_time, max_processing_time, min_processing_time

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

# Function used to measure the processing time of a function
def measure_processing_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        processing_time = time.time() - start_time
        
        # Observe the processing time
        avg_processing_time.observe(processing_time)
        
        # Update the max processing time
        max_processing_time.set(max(max_processing_time._value.get(), processing_time))
        
        # Update the min processing time
        # Do not let the min processing time to be 0
        if min_processing_time._value.get() == 0:
            min_processing_time.set(processing_time)
        else:
            min_processing_time.set(min(min_processing_time._value.get(), processing_time))
        
        return result
    return wrapper