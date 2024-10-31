from config import *
from psycopg2 import pool
from elasticsearch import Elasticsearch
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

postgres_connection = None
mongodb_connection = None
elasticsearch_connection = None

def generatePostgresConnection():
    try:
        postgres_connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=5,
            host=POSTGRES,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB
        )
        return postgres_connection_pool
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        exit(1)

def generateMongoConnection():
    try:
        client = MongoClient(
            MONGO_URI,
            server_api=ServerApi('1'),
            maxPoolSize=10, 
            minPoolSize=1 
        )
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        exit(1)

def generateElasticsearchConnection():
    try:
        connection = Elasticsearch([ELASTIC], basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD])
        return connection
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        exit(1)

postgres_connection = generatePostgresConnection()
mongodb_connection = generateMongoConnection()
elasticsearch_connection = generateElasticsearchConnection()