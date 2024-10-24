from pymongo import MongoClient
import psycopg2
import os
from config import *

#Mongo connection function
def connect_to_mongo():
    mongo_uri = os.getenv('MONGO_URI', 'tu_mongo_uri') # Parameters for the connection
    client = MongoClient(mongo_uri)
    
    # Database and collection
    db = client['LyricsDB']
    collection = db['LyricsCollection']
    
    print("Successful connection to MongoDB")
    return collection

#Postgres connection function  
def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            user=os.getenv('POSTGRES_USER', 'tu_usuario'),
            password=os.getenv('POSTGRES_PASSWORD', 'tu_contraseña'),
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            database=os.getenv('POSTGRES_DB', 'LyricsDB')
        )
        cursor = connection.cursor()
        print("Succefull connection to PostgreSQL")
        return connection, cursor
    except (Exception, psycopg2.Error) as error:
        print(f"Error conecting to PostGreSQL: {error}")
        return None, None
