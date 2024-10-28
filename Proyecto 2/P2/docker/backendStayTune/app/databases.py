from config import *
from psycopg2 import pool
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
        return None