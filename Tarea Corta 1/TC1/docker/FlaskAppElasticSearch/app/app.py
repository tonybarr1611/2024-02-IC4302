# Flask App for PostgreSQL
from flask import Flask
from os import getenv
from elasticsearch import Elasticsearch, helpers

ELASTIC = getenv("ELASTIC")
ELASTIC_USER = getenv("ELASTIC_USER")
ELASTIC_PASSWORD = getenv("ELASTIC_PASSWORD")

print(f"Elasticsearch: {ELASTIC}")
print(f"Elasticsearch User: {ELASTIC_USER}")
print(f"Elasticsearch Password: {ELASTIC_PASSWORD}")

app = Flask(__name__)

elasticsearch_connection = None
queryAll = {
    "size": 1000,
    "query": {
        "match_all": {}
    }
}

try:
    elasticsearch_connection = Elasticsearch([ELASTIC], basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD])
except Exception as e:
    print(f"Error connecting to Elasticsearch: {e}")
    exit(1)
    
def getIndex(fileName: str):
    page = elasticsearch_connection.search(index=f"f1_records_{fileName}", body=queryAll, scroll="800ms")
    
    scroll_id = page["_scroll_id"]
    
    all_documents = page["hits"]["hits"]
    
    while len(page["hits"]["hits"]) > 0:
        page = elasticsearch_connection.scroll(scroll_id=scroll_id, scroll="800ms")
        scroll_id = page["_scroll_id"]
        all_documents.extend(page["hits"]["hits"])
    
    elasticsearch_connection.clear_scroll(scroll_id=scroll_id)
    return all_documents

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/drivers", methods=['GET'])
def get_drivers():
    document = getIndex("drivers")
    
    return f"<h1>ElasticSearch</h1><p>{document}</p>"

@app.route("/constructors", methods=['GET'])
def get_constructors():
    document = getIndex("constructors")
    
    return f"<h1>ElasticSearch</h1><p>{document}</p>"

@app.route("/circuits", methods=['GET'])
def get_laps():
    document = getIndex("circuits")
    
    return f"<h1>ElasticSearch</h1><p>{document}</p>"

@app.route("/races", methods=['GET'])
def get_laps_driver():
    document = getIndex("races")
    
    return f"<h1>ElasticSearch</h1><p>{document}</p>"

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host='localhost', port=5000)
