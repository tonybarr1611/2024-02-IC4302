import mariadb
from elasticsearch import Elasticsearch
from pymemcache.client.base import Client
from config import *

mariadb_connection = None
elasticsearch_connection = None

def init_mariadb():
    global mariadb_connection
    try:
        mariadb_connection = mariadb.ConnectionPool(
            pool_name="mariadb_pool",
            pool_size=5,
            host=MARIADB,
            user=MARIADB_USER,
            password=MARIADB_PASSWORD,
            database="control"
        )
    except Exception as e:
        print(f"Error connecting to MariaDB: {e}")
        exit(1)
        
def init_memcached():
    global memcached_connection
    try:
        memcached_connection = Client((MEMCACHED, MEMCACHED_PORT))
    except Exception as e:
        print(f"Error connecting to Memcached: {e}")
        exit(1)

def init_elasticsearch():
    global elasticsearch_connection
    try:
        elasticsearch_connection = Elasticsearch([ELASTIC], basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD])
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        exit(1)

# Initialize the connections
init_mariadb()
init_memcached()
init_elasticsearch()
