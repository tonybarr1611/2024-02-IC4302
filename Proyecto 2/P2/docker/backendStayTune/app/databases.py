from config import *
from psycopg2 import pool
from elasticsearch import Elasticsearch
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

from psycopg2 import pool
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from elasticsearch import Elasticsearch

class DatabaseConnections:
    _postgres_connection_pool = None
    _mongo_client = None
    _elasticsearch_client = None

    @staticmethod
    def getPostgresConnection():
        if DatabaseConnections._postgres_connection_pool is None or DatabaseConnections._postgres_connection_pool.closed:
            try:
                DatabaseConnections._postgres_connection_pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=20,
                    host=POSTGRES,
                    user=POSTGRES_USER,
                    password=POSTGRES_PASSWORD,
                    dbname=POSTGRES_DB
                )
            except Exception as e:
                print(f"Error connecting to PostgreSQL: {e}")
                exit(1)
        return DatabaseConnections._postgres_connection_pool

    @staticmethod
    def getMongoConnection():
        if DatabaseConnections._mongo_client is None:
            try:
                DatabaseConnections._mongo_client = MongoClient(
                    MONGO_URI,
                    server_api=ServerApi('1'),
                    maxPoolSize=10, 
                    minPoolSize=1 
                )
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                exit(1)
        return DatabaseConnections._mongo_client

    @staticmethod
    def getESConnection():
        if DatabaseConnections._elasticsearch_client is None:
            try:
                DatabaseConnections._elasticsearch_client = Elasticsearch(
                    [ELASTIC],
                    basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD]
                )
            except Exception as e:
                print(f"Error connecting to Elasticsearch: {e}")
                exit(1)
        return DatabaseConnections._elasticsearch_client

