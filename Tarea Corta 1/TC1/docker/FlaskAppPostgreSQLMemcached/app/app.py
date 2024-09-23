# Flask App for PostgreSQL
from flask import Flask
from os import getenv
import psycopg2
from psycopg2 import pool
from pymemcache.client.base import Client
import json

POSTGRES = getenv("POSTGRES")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRESQL_PASSWORD = getenv("POSTGRES_PASSWORD")
MEMCACHED_HOST = getenv("MEMCACHED_HOST", "localhost")
MEMCACHED_PORT = int(getenv("MEMCACHED_PORT_NUMBER ", 11211))

print(f"PostgreSQL: {POSTGRES}")
print(f"PostgreSQL User: {POSTGRES_USER}")
print(f"PostgreSQL Password: {POSTGRESQL_PASSWORD}")

app = Flask(__name__)

postgres_connection = None
try:
    postgres_connection = psycopg2.pool.SimpleConnectionPool(
            minconn = 1,
            maxconn = 5,
            host = POSTGRES,
            user = POSTGRES_USER,
            password = POSTGRESQL_PASSWORD,
            dbname = 'f1_records'
        )
except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    exit(1)

# Memcached Connection
memcached_client = Client((MEMCACHED_HOST, MEMCACHED_PORT))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/drivers", methods=['GET'])
def get_drivers():
    cache_key = "drivers"
    cached_result = memcached_client.get(cache_key)

    if cached_result:
        results_psql = json.loads(cached_result)
    else:
        query = "SELECT * FROM DRIVER ORDER BY driverId;"
        
        conn_psql = postgres_connection.getconn()
        cursor_psql = conn_psql.cursor()
        cursor_psql.execute(query)
        results_psql = cursor_psql.fetchall()
        cursor_psql.close()
    
    return f"<h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/constructors", methods=['GET'])
def get_constructors():
    cache_key = "constructors"
    cached_result = memcached_client.get(cache_key)

    if cached_result:
        results_psql = json.loads(cached_result)
    else:
        query = "SELECT * FROM CONSTRUCTOR ORDER BY constructorId;"
        
        conn_psql = postgres_connection.getconn()
        cursor_psql = conn_psql.cursor()
        cursor_psql.execute(query)
        results_psql = cursor_psql.fetchall()
        cursor_psql.close()
    
    return f"<h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/circuits", methods=['GET'])
def get_laps():
    cache_key = "circuits"
    cached_result = memcached_client.get(cache_key)
    
    if cached_result:
        results_psql = json.loads(cached_result)
    else:
        query = "SELECT * FROM CIRCUIT ORDER BY circuitId"
        
        conn_psql = postgres_connection.getconn()
        cursor_psql = conn_psql.cursor()
        cursor_psql.execute(query)
        results_psql = cursor_psql.fetchall()
        cursor_psql.close()
    
    return f"<h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/races", methods=['GET'])
def get_laps_driver():
    cache_key = "races"
    cached_result = memcached_client.get(cache_key)
    
    if cached_result:
        results_psql = json.loads(cached_result)
    else:
        query = "SELECT * FROM RACE ORDER BY raceId"
        
        conn_psql = postgres_connection.getconn()
        cursor_psql = conn_psql.cursor()
        cursor_psql.execute(query)
        results_psql = cursor_psql.fetchall()
        cursor_psql.close()
    
    return f"<h1>PostgreSQL</h1><p>{results_psql}</p>"

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host='localhost', port=5000)
